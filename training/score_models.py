#!/usr/bin/env python3
"""Score the training base and trained adapters on the whole current task set, with no training.

    python training/score_models.py --adapters trained-run5-seed1=/root/adapter --workers 28
    python training/score_models.py --fake --limit 3 --workers 4        # no GPU: checks the episode logic

What it does:
* loads the same 4-bit model as `grpo_pilot.py` (Unsloth + vLLM in one process), once;
* answers every task of the current set (templates and paraphrases) greedily: first with no adapter (label
  `training-base`), then once per adapter given with --adapters LABEL=DIR;
* plays whole episodes: if the model asks a question, the simulated planner answers and the model gets a second
  turn (up to the environment's three turns), so `under_specified` tasks are scored too;
* uses the system prompt, user prompt and JSON extraction of `scripts/run_baseline.py`, and writes result files in
  its record format: OUT/<label>/<base model>.<task file stem>.jsonl, readable by `scripts/summarise_results.py`.

A task whose prompt is longer than --max-prompt-tokens gets an empty answer (scored wrong) and is counted.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

_TASKS: dict = {}
EMPTY = {"version": "0.1", "note": "unparseable model output", "data_changes": []}


# ------------------------------------------------------------------ episode workers (separate processes)
def _init_worker(task_files: list[str]) -> None:
    global _TASKS
    from whatifgym.tasks import load_tasks

    _TASKS = {t.id: t for f in task_files for t in load_tasks(f)}


def _play(job: tuple[str, list[str], str]) -> dict:
    """Replay one episode with the answers collected so far.

    Returns the finished result record, or the prompt of the next turn if the episode is still open. Replaying
    from the start keeps the workers stateless; the environment is deterministic.
    """
    task_id, texts, label = job
    from run_baseline import _extract_json, build_prompt
    from whatifgym.env import WhatIfEnv

    task = _TASKS[task_id]
    env = WhatIfEnv([task])
    obs = env.reset(task)
    state: dict = {"model": label, "turns": 0}
    done, reward, info, actions = False, 0.0, {}, []
    for text in texts:
        state["turns"] += 1
        state["raw_output"] = text[:4000]
        try:
            scenario = _extract_json(text)
            if not isinstance(scenario, dict):
                raise ValueError("not a JSON object")
            action = {"type": "scenario", "scenario": scenario}
        except Exception:
            state["parse_error"] = text[:500]
            action = {"type": "scenario", "scenario": dict(EMPTY)}
        actions.append(action)
        try:
            obs, reward, done, info = env.step(action)
        except Exception as exc:  # an answer the environment cannot process is a wrong answer, not a crash
            state["step_error"] = repr(exc)[:300]
            obs, reward, done, info = env.step({"type": "scenario", "scenario": dict(EMPTY)}) if not env.done else (obs, 0.0, True, info)
        if done:
            break
    if not done:
        return {"task_id": task_id, "done": False, "prompt": build_prompt(obs)}
    score = info.get("score", {})
    rec = {"task_id": task.id, "template": task.template, "difficulty": task.difficulty, "split": task.split,
           "reward": reward, **{k: score.get(k) for k in ("correct", "valid_dsl", "asked", "route_correct", "ask_needed")},
           "notes": score.get("notes", ""), "validation_errors": info.get("validation_errors", []),
           "final_action": actions[-1], "agent_state": state}
    if "result" in info:
        rec["candidate_objective"] = info["result"].get("objective")
        rec["reference_objective"] = task.reference.get("objective")
    return {"task_id": task_id, "done": True, "record": rec}


# ------------------------------------------------------------------ one model over all tasks
def score_label(label: str, generate, tasks_by_file: dict[str, list], pool, count_tokens, max_prompt_tokens: int,
                out: Path) -> dict:
    """Play every episode in rounds: all open episodes get one answer per round, in one batch."""
    from run_baseline import SYSTEM_PROMPT

    ids = [t.id for ts in tasks_by_file.values() for t in ts]
    texts: dict[str, list[str]] = {i: [] for i in ids}
    records: dict[str, dict] = {}
    too_long: list[str] = []
    open_ids, t0, rounds = ids, time.perf_counter(), 0
    while open_ids:
        rounds += 1
        results = list(pool.map(_play, [(i, texts[i], f"vllm/{label}") for i in open_ids], chunksize=8))
        prompts, ask = [], []
        for r in results:
            if r["done"]:
                records[r["task_id"]] = r["record"]
                continue
            messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": r["prompt"]}]
            if count_tokens(messages) > max_prompt_tokens:
                texts[r["task_id"]].append("")        # no answer: scored as unparseable
                if r["task_id"] not in too_long:
                    too_long.append(r["task_id"])
            else:
                prompts.append(messages)
                ask.append(r["task_id"])
        if prompts:
            answers = generate(prompts, ask)
            for i, a in zip(ask, answers):
                texts[i].append(a)
        open_ids = [r["task_id"] for r in results if not r["done"]]
        print(f"[{label}] round {rounds}: {len(prompts)} answers, {len(records)} of {len(ids)} episodes finished, "
              f"{time.perf_counter() - t0:.0f} s", flush=True)
    for i in too_long:
        records[i]["agent_state"]["prompt_too_long"] = True
    folder = out / label
    folder.mkdir(parents=True, exist_ok=True)
    for f, ts in tasks_by_file.items():
        p = Path(f)
        with (folder / f"{p.parent.name}.{p.stem}.jsonl").open("w", encoding="utf-8") as fh:
            for t in ts:
                fh.write(json.dumps(records[t.id]) + "\n")
    correct = {i: bool(records[i]["correct"]) for i in ids}
    nl = [i for i in ids if i.rsplit("-p", 1)[-1].isdigit() and "-p" in i]
    tpl = [i for i in ids if i not in set(nl)]
    pct = lambda v: round(100 * sum(correct[i] for i in v) / len(v), 2) if v else None  # noqa: E731
    return {"label": label, "tasks": len(ids), "accuracy_templates": pct(tpl), "templates": len(tpl),
            "accuracy_paraphrases": pct(nl), "paraphrases": len(nl), "prompt_too_long": len(too_long),
            "valid": round(100 * sum(bool(records[i]["valid_dsl"]) for i in ids) / len(ids), 2),
            "seconds": round(time.perf_counter() - t0, 1), "correct": correct}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="unsloth/Qwen3-4B-Instruct-2507")
    ap.add_argument("--adapters", nargs="*", default=[], metavar="LABEL=DIR", help="LoRA adapters to score after the base")
    ap.add_argument("--no-base", action="store_true", help="skip the run without an adapter")
    ap.add_argument("--tasks", nargs="*", default=None, help="task files (default: the current set with its paraphrases)")
    ap.add_argument("--limit", type=int, default=None, help="tasks per file (smoke test)")
    ap.add_argument("--max-prompt-tokens", type=int, default=31000)
    ap.add_argument("--max-completion", type=int, default=768, help="as in grpo_pilot.py, so its evaluation can be reproduced")
    ap.add_argument("--lora-rank", type=int, default=32)
    ap.add_argument("--gpu-mem", type=float, default=0.85)
    ap.add_argument("--batch", type=int, default=256, help="prompts handed to vLLM at once")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--check-ids", default=str(ROOT / "training" / "results" / "run5_seed1_eval_task_ids.json"),
                    help="eval_task_ids.json of a training run: accuracy on those task sets is printed, to compare")
    ap.add_argument("--fake", action="store_true", help="no GPU: answer with the gold scenario (asks first when needed)")
    ap.add_argument("--out", default=str(ROOT / "results" / "baselines" / "pod"))
    args = ap.parse_args(argv)

    from whatifgym.tasks import current_task_files, load_tasks

    files = [str(Path(f)) for f in (args.tasks or current_task_files(paraphrases=True))]
    tasks_by_file = {f: load_tasks(f)[:args.limit] for f in files}
    n = sum(len(v) for v in tasks_by_file.values())
    print(f"{n} tasks in {len(files)} files", flush=True)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    runs: list[tuple[str, str | None]] = [] if args.no_base else [("training-base", None)]
    for spec in args.adapters:
        label, _, folder = spec.partition("=")
        if not folder or not Path(folder).is_dir():
            raise SystemExit(f"--adapters {spec!r}: expected LABEL=DIR with an existing folder")
        runs.append((label, folder))

    if args.fake:
        gold = {t.id: t for ts in tasks_by_file.values() for t in ts}
        count_tokens = lambda messages: 0  # noqa: E731
        asked: set[str] = set()

        def make_generate(_lora):
            def generate(prompts, ids):
                answers = []
                for i in ids:
                    t = gold[i]
                    if t.family == "under_specified" and i not in asked:
                        asked.add(i)
                        answers.append(json.dumps({"ask": "Which one do you mean?"}))
                    else:
                        answers.append("```json\n" + json.dumps(t.scenario) + "\n```")
                return answers
            return generate
    else:
        from unsloth import FastLanguageModel  # import before transformers: Unsloth patches it
        from vllm import SamplingParams

        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=args.model, max_seq_length=args.max_prompt_tokens + args.max_completion, load_in_4bit=True,
            fast_inference=True, max_lora_rank=args.lora_rank, gpu_memory_utilization=args.gpu_mem)
        model = FastLanguageModel.get_peft_model(
            model, r=args.lora_rank, lora_alpha=args.lora_rank, random_state=0,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"])
        count_tokens = lambda messages: len(tokenizer.apply_chat_template(  # noqa: E731
            messages, tokenize=True, add_generation_prompt=True))
        params = SamplingParams(temperature=0.0, max_tokens=args.max_completion)

        def make_generate(folder):
            lora = model.load_lora(folder) if folder else None

            def generate(prompts, ids):
                answers = []
                for k in range(0, len(prompts), args.batch):
                    chunk = [tokenizer.apply_chat_template(m, tokenize=False, add_generation_prompt=True)
                             for m in prompts[k:k + args.batch]]
                    outs = model.fast_generate(chunk, sampling_params=params, lora_request=lora)
                    answers += [o.outputs[0].text for o in outs]
                    print(f"  generated {len(answers)} of {len(prompts)}", flush=True)
                return answers
            return generate

    check = json.loads(Path(args.check_ids).read_text(encoding="utf-8")) if Path(args.check_ids).is_file() else {}
    pool = ProcessPoolExecutor(max_workers=args.workers, initializer=_init_worker, initargs=(files,),
                               mp_context=multiprocessing.get_context("spawn"))
    summary = []
    for label, folder in runs:
        s = score_label(label, make_generate(folder), tasks_by_file, pool, count_tokens, args.max_prompt_tokens, out)
        correct = s.pop("correct")
        for name, id_list in check.items():
            have = [i for i in id_list if i in correct]
            if have:
                s[f"check_{name}"] = {"tasks": len(have), "of": len(id_list),
                                      "accuracy": round(100 * sum(correct[i] for i in have) / len(have), 2)}
        summary.append(s)
        (out / "score_models_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
        print("SCORED " + json.dumps(s), flush=True)
    pool.shutdown()
    print("ALL_SCORED", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
