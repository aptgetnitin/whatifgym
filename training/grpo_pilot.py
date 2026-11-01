#!/usr/bin/env python3
"""GRPO pilot: train a small LLM against the WhatIfGym reward on one consumer GPU (12 GB).

    python training/grpo_pilot.py --smoke                 # 5 steps on 20 tasks: memory, speed, reward (about 10 min)
    python training/grpo_pilot.py --max-steps 50          # the pilot (20 to 50 steps)

What it does:
* builds a dataset from the training split: the same system prompt and user prompt as `scripts/run_baseline.py`,
  so a trained model is measured on exactly the prompt the baselines saw;
* loads the model in 4 bit with a LoRA adapter (Unsloth) and generates with vLLM inside the same process;
* scores every completion with the environment: the oracle solves the scenario, the scorer compares it with the
  hidden reference, and the reward is the environment's (1.1 correct and valid, 0.1 valid only, 0 otherwise);
  a pool of worker processes does the solves, so the GPU does not wait for one solver at a time;
* scores a fixed set of test tasks (greedy) before and after training, with the same environment reward;
* writes the LoRA adapter, the log history and a summary (peak GPU memory, seconds per step, reward per step).

Single-turn pilot: `under_specified` tasks (they need a second turn) are left out, and a clarifying question on a
clear task earns 0. The multi-turn ask action comes in a later stage.
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


# ------------------------------------------------------------------ reward workers (separate processes)
def _init_worker(task_files: list[str]) -> None:
    global _TASKS
    from whatifgym.tasks import load_tasks

    _TASKS = {t.id: t for f in task_files for t in load_tasks(f)}


def _score(job: tuple[str, str]) -> float:
    """Reward of one completion for one task. Never raises: anything unusable earns 0."""
    task_id, text = job
    from run_baseline import _extract_json
    from whatifgym.env import WhatIfEnv

    task = _TASKS[task_id]
    try:
        action = _extract_json(text)
    except Exception:
        return 0.0
    if not isinstance(action, dict):
        return 0.0
    env = WhatIfEnv([task])
    env.reset(task)
    try:
        _, reward, done, _ = env.step({"type": "scenario", "scenario": action})
    except Exception:
        return 0.0
    return float(reward) if done else 0.0       # a question on a clear task: no second turn in this pilot


# ------------------------------------------------------------------ data
def task_files(families_excluded: tuple[str, ...]) -> list[str]:
    from whatifgym.tasks import current_task_files

    return [str(p) for p in current_task_files(paraphrases=False) if p.stem.rsplit("_v", 1)[0] not in families_excluded]


def build_rows(files: list[str], tokenizer, max_prompt_tokens: int, limit: int | None, seed: int,
               split: str | None = "train") -> list[dict]:
    import random

    from run_baseline import SYSTEM_PROMPT, build_prompt
    from whatifgym.env import WhatIfEnv
    from whatifgym.tasks import load_tasks

    rows, too_long = [], 0
    for f in files:
        for t in load_tasks(f, split=split):
            obs = WhatIfEnv([t]).reset(t)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": build_prompt(obs)}]
            n = len(tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True))
            if n > max_prompt_tokens:
                too_long += 1
                continue
            rows.append({"prompt": messages, "task_id": t.id, "family": t.family, "model": t.model})
    random.Random(seed).shuffle(rows)
    print(f"dataset ({split}): {len(rows)} tasks fit in {max_prompt_tokens} prompt tokens; {too_long} longer ones left out")
    return rows[:limit] if limit else rows


def evaluate(model, tokenizer, rows: list[dict], pool, max_tokens: int, lora_request=None) -> dict:
    """Greedy answers to one fixed task set, scored by the environment: the before/after number of the gate."""
    from vllm import SamplingParams

    texts = [tokenizer.apply_chat_template(r["prompt"], tokenize=False, add_generation_prompt=True) for r in rows]
    outs = model.fast_generate(texts, sampling_params=SamplingParams(temperature=0.0, max_tokens=max_tokens),
                               lora_request=lora_request)
    rewards = list(pool.map(_score, [(r["task_id"], o.outputs[0].text) for r, o in zip(rows, outs)]))
    by_family: dict[str, list[bool]] = {}
    for r, x in zip(rows, rewards):
        by_family.setdefault(r["family"], []).append(x >= 1.0)
    n = len(rows)
    return {"tasks": n, "accuracy": round(sum(x >= 1.0 for x in rewards) / n, 4),
            "valid": round(sum(x > 0 for x in rewards) / n, 4), "mean_reward": round(sum(rewards) / n, 4),
            "accuracy_by_family": {f: round(sum(v) / len(v), 3) for f, v in sorted(by_family.items())},
            "correct": "".join("1" if x >= 1.0 else "0" for x in rewards)}  # per task, in eval order: paired tests


def pass_rates(model, tokenizer, rows: list[dict], pool, k: int, max_tokens: int) -> dict[str, float]:
    """Share of k sampled answers (temperature 1, the training setting) that are correct, for each task."""
    from vllm import SamplingParams

    texts = [tokenizer.apply_chat_template(r["prompt"], tokenize=False, add_generation_prompt=True) for r in rows]
    outs = model.fast_generate(texts, sampling_params=SamplingParams(n=k, temperature=1.0, max_tokens=max_tokens))
    jobs = [(r["task_id"], c.text) for r, o in zip(rows, outs) for c in o.outputs]
    rewards = list(pool.map(_score, jobs, chunksize=16))
    return {r["task_id"]: sum(x >= 1.0 for x in rewards[i * k:(i + 1) * k]) / k for i, r in enumerate(rows)}


# ------------------------------------------------------------------ main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="unsloth/Qwen3-4B-Instruct-2507", help="Hugging Face id (Unsloth builds load fastest)")
    ap.add_argument("--smoke", action="store_true", help="5 steps on 20 tasks, then a memory and speed report")
    ap.add_argument("--max-steps", type=int, default=50)
    ap.add_argument("--tasks-limit", type=int, default=None, help="use only the first N training tasks (after shuffling)")
    ap.add_argument("--num-generations", type=int, default=4, help="completions per prompt (the GRPO group)")
    ap.add_argument("--grad-accum", type=int, default=8, help="prompts per step (one prompt per micro-batch)")
    ap.add_argument("--eval-tasks", type=int, default=200, help="test tasks scored before and after training; 0 skips")
    ap.add_argument("--max-prompt-tokens", type=int, default=7000, help="tasks with longer prompts are left out")
    ap.add_argument("--max-completion", type=int, default=768)
    ap.add_argument("--lora-rank", type=int, default=32)
    ap.add_argument("--lr", type=float, default=5e-6)
    ap.add_argument("--gpu-mem", type=float, default=0.55, help="share of GPU memory vLLM may take for generation")
    ap.add_argument("--workers", type=int, default=8, help="solver processes for the reward")
    ap.add_argument("--seed", type=int, default=3407, help="training seed; the evaluation tasks do not depend on it")
    ap.add_argument("--holdout-models", nargs="*", default=[], help="base models kept out of training, scored apart")
    ap.add_argument("--measure-pass", type=int, default=0, metavar="K",
                    help="only sample K answers per training task, write pass_rates.json and stop")
    ap.add_argument("--pass-rates", default=None, help="pass_rates.json from --measure-pass: train only on tasks ...")
    ap.add_argument("--pass-range", type=float, nargs=2, default=(0.1, 0.9), help="... with a pass rate in [LO, HI]")
    ap.add_argument("--out", default=str(ROOT / "results" / "training" / "pilot"))
    args = ap.parse_args(argv)
    if args.smoke:
        args.max_steps, args.tasks_limit, args.eval_tasks = 5, args.tasks_limit or 20, min(args.eval_tasks, 20)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    from unsloth import FastLanguageModel  # import before trl/transformers: Unsloth patches them

    import torch
    from datasets import Dataset
    from trl import GRPOConfig, GRPOTrainer

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model, max_seq_length=args.max_prompt_tokens + args.max_completion, load_in_4bit=True,
        fast_inference=True, max_lora_rank=args.lora_rank, gpu_memory_utilization=args.gpu_mem)
    model = FastLanguageModel.get_peft_model(
        model, r=args.lora_rank, lora_alpha=args.lora_rank, use_gradient_checkpointing="unsloth", random_state=args.seed,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"])

    files = task_files(families_excluded=("under_specified",))
    holdout = set(args.holdout_models)
    rows = [r for r in build_rows(files, tokenizer, args.max_prompt_tokens, None, args.seed) if r["model"] not in holdout]
    if args.pass_rates:
        rates = json.loads(Path(args.pass_rates).read_text(encoding="utf-8"))
        lo, hi = args.pass_range
        before = len(rows)
        rows = [r for r in rows if lo <= rates.get(r["task_id"], -1.0) <= hi]
        print(f"pass-rate filter [{lo}, {hi}]: {len(rows)} of {before} training tasks kept", flush=True)
    rows = rows[:args.tasks_limit] if args.tasks_limit else rows
    # One fixed draw (seed 0), so every training seed is scored on the same tasks
    eval_sets = {
        "test": [r for r in build_rows(files, tokenizer, args.max_prompt_tokens, None, 0, split="test")
                 if r["model"] not in holdout][:args.eval_tasks],
        "heldout_models": [r for r in build_rows(files, tokenizer, args.max_prompt_tokens, None, 0, split=None)
                           if r["model"] in holdout][:args.eval_tasks],
    } if args.eval_tasks else {}
    eval_sets = {name: rs for name, rs in eval_sets.items() if rs}
    (out / "eval_task_ids.json").write_text(json.dumps({n: [r["task_id"] for r in rs] for n, rs in eval_sets.items()}),
                                            encoding="utf-8")

    # spawn, not fork: this process already holds CUDA and vLLM threads, and a forked child can hang on them
    pool = ProcessPoolExecutor(max_workers=args.workers, initializer=_init_worker, initargs=(files,),
                               mp_context=multiprocessing.get_context("spawn"))
    if args.measure_pass:
        rates = pass_rates(model, tokenizer, rows, pool, args.measure_pass, args.max_completion)
        pool.shutdown()
        (out / "pass_rates.json").write_text(json.dumps(rates), encoding="utf-8")
        by_family: dict[str, list[float]] = {}
        for r in rows:
            by_family.setdefault(r["family"], []).append(rates[r["task_id"]])
        lo, hi = args.pass_range
        stats = lambda v: {"tasks": len(v), "pass@1": round(sum(v) / len(v), 3),  # noqa: E731
                           f"pass@{args.measure_pass}": round(sum(x > 0 for x in v) / len(v), 3),
                           "in_range": round(sum(lo <= x <= hi for x in v) / len(v), 3)}
        report = {"k": args.measure_pass, "all": stats(list(rates.values())),
                  "by_family": {f: stats(v) for f, v in sorted(by_family.items())}}
        print("PASS_RATES " + json.dumps(report), flush=True)
        print("PASS_RATES_FILE " + json.dumps(rates), flush=True)  # the whole file, one line: copy it off the pod
        return 0
    dataset = Dataset.from_list(rows)
    eval_before = {n: evaluate(model, tokenizer, rs, pool, args.max_completion) for n, rs in eval_sets.items()}
    print(f"EVAL before training: {json.dumps(eval_before)}", flush=True)
    reward_seconds: list[float] = []

    def whatifgym_reward(prompts, completions, task_id, **kwargs):
        t0 = time.perf_counter()
        texts = [c[0]["content"] if isinstance(c, list) else str(c) for c in completions]
        rewards = list(pool.map(_score, zip(task_id, texts)))
        reward_seconds.append(time.perf_counter() - t0)
        return rewards

    # The recipe of the plan, cut down for 12 GB. Options that this TRL version does not know are dropped and listed.
    wanted = dict(
        output_dir=str(out), learning_rate=args.lr, optim="adamw_8bit", lr_scheduler_type="constant", warmup_ratio=0.0,
        per_device_train_batch_size=args.num_generations, gradient_accumulation_steps=args.grad_accum,
        num_generations=args.num_generations, max_prompt_length=args.max_prompt_tokens,
        max_completion_length=args.max_completion, max_steps=args.max_steps, temperature=1.0,
        loss_type="dapo", epsilon_high=0.28, beta=0.0, mask_truncated_completions=True,
        logging_steps=1, save_steps=max(args.max_steps, 1), report_to="none", seed=args.seed)
    known = GRPOConfig.__dataclass_fields__
    dropped = sorted(k for k in wanted if k not in known)
    if dropped:
        print(f"note: this TRL version has no {dropped}; running without them")
    config = GRPOConfig(**{k: v for k, v in wanted.items() if k in known})

    trainer = GRPOTrainer(model=model, processing_class=tokenizer, reward_funcs=[whatifgym_reward],
                          args=config, train_dataset=dataset)
    torch.cuda.reset_peak_memory_stats()
    t0 = time.perf_counter()
    trainer.train()
    wall = time.perf_counter() - t0

    model.save_lora(str(out / "lora"))
    tokenizer.save_pretrained(str(out / "lora"))
    lora = model.load_lora(str(out / "lora"))
    eval_after = {n: evaluate(model, tokenizer, rs, pool, args.max_completion, lora_request=lora)
                  for n, rs in eval_sets.items()}
    print(f"EVAL after training: {json.dumps(eval_after)}", flush=True)
    pool.shutdown()
    history = trainer.state.log_history
    (out / "log_history.json").write_text(json.dumps(history, indent=1), encoding="utf-8")
    rewards = [h["reward"] for h in history if "reward" in h]
    summary = {
        "model": args.model, "seed": args.seed, "holdout_models": sorted(holdout), "pass_rates": args.pass_rates,
        "pass_range": list(args.pass_range) if args.pass_rates else None,
        "steps": args.max_steps, "tasks": len(rows), "num_generations": args.num_generations,
        "prompts_per_step": args.grad_accum, "eval_before": eval_before, "eval_after": eval_after,
        "max_prompt_tokens": args.max_prompt_tokens, "max_completion": args.max_completion,
        "peak_gpu_memory_gb": round(torch.cuda.max_memory_reserved() / 1e9, 2),
        "gpu": torch.cuda.get_device_name(0), "seconds_total": round(wall, 1),
        "seconds_per_step": round(wall / max(args.max_steps, 1), 1),
        "reward_seconds_per_step": round(sum(reward_seconds) / max(len(reward_seconds), 1), 2),
        "reward_by_step": [round(r, 3) for r in rewards], "dropped_config_options": dropped,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print("\n" + json.dumps(summary, indent=1))
    print("SUMMARY " + json.dumps(summary), flush=True)  # one line: easy to find in a pod log
    print(f"\nadapter, log and summary in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
