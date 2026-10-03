#!/usr/bin/env python3
"""Natural-language paraphrases of generated questions, verified by a round trip through the oracle.

The template questions are unambiguous but stilted ("the units sold, summed over everything with month = Feb,
must stay at or below 1100"); planners do not talk like that, and the first local baseline showed that small
models find template phrasing far easier than planner phrasing. This script rewrites each question the way a
planner would say it, then keeps a rewrite only if an independent model can translate it back into a scenario
that re-solves to the task's reference — so the gold scenario and reference of every paraphrased task are still
exactly right, and meaning drift is rejected mechanically rather than by eye.

    # paraphrase with a local 32B model, verify with a different local model, 3 rewrites per task
    python scripts/paraphrase_tasks.py --tasks tasks/mining/new_limit_v0.jsonl \
        --paraphraser ollama:qwen3:32b --verifier ollama:qwen3:14b --n 3

    # Anthropic API for either role (ANTHROPIC_API_KEY in the environment)
    python scripts/paraphrase_tasks.py --tasks ... --paraphraser anthropic:claude-opus-5-5 --verifier ollama:qwen3:14b

    # offline, in passes: export the paraphrase prompts, collect <task_id>.json replies elsewhere, import them;
    # optionally also export the verification prompts (<task_id>-c<i>.txt) and import the translations
    python scripts/paraphrase_tasks.py --tasks ... --export-paraphrase-prompts /tmp/pp
    python scripts/paraphrase_tasks.py --tasks ... --import-paraphrases /tmp/pp_answers --verifier ollama:qwen3:14b
    python scripts/paraphrase_tasks.py --tasks ... --import-paraphrases /tmp/pp_answers --export-verification-prompts /tmp/vp
    python scripts/paraphrase_tasks.py --tasks ... --import-paraphrases /tmp/pp_answers --verifier-answers /tmp/vp_answers

Output: ``tasks/<model>/<family>_<version>_nl.jsonl`` with one task per kept paraphrase (id ``<source id>-p<k>``,
same hidden scenario, reference and split as the source, ``tags`` + "paraphrase", provenance in ``slots``), and a
``..._nl.provenance.json`` recording the prompt version, both model ids and the acceptance counts, for the
disclosure section. Under-specified tasks are skipped (their vagueness is the point).

Caveat for evaluation: verification selects rewrites the verifier could solve, so evaluate the verifier model on
the original files, not on paraphrases it filtered.
"""
from __future__ import annotations

import argparse
import collections
import copy
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from run_baseline import SYSTEM_PROMPT, _extract_json, _ollama_request, build_prompt  # noqa: E402
from whatifgym.env import WhatIfEnv  # noqa: E402
from whatifgym.oracle import solve_scenario  # noqa: E402
from whatifgym.registry import get_model  # noqa: E402
from whatifgym.scoring import compare_results  # noqa: E402
from whatifgym.tasks import Task, load_tasks, save_tasks  # noqa: E402

PROMPT_VERSION = "paraphrase-v1 (2026-10-03)"

PARAPHRASE_SYSTEM = """You rewrite what-if questions for a planning team. You are given the description of an
optimization model a planner uses and one precise what-if question generated from a template. Rewrite it the way a
real planner would say it to a colleague — in an email, in a meeting, in a chat message — keeping EXACTLY the same
meaning: the same things (use the same product, month, depot or other names that appear in the question), the same
numbers, the same direction (higher/lower, at most/at least), the same scope (one row, several, or everything).
Never add a condition, never drop one, never make it vaguer or more specific. Vary the style across rewrites
(terse, chatty, formal), but never use table or column identifiers with underscores. Answer with JSON only:
{"paraphrases": ["...", "...", "..."]}"""


def paraphrase_prompt(task: Task, model, n: int) -> str:
    return "\n\n".join([
        f"# The planner's model: {model.title} (`{model.name}`)", model.description(),
        f"# Template question to rewrite\n{task.question}",
        f"Write {n} different rewrites with exactly the same meaning. JSON only.",
    ])


# ------------------------------------------------------------------------------------------------- backends
def make_chat(spec: str, host: str, num_ctx: int, max_tokens: int, temperature: float = 0.0):
    """``spec`` = 'ollama:<tag>' | 'anthropic:<model id>'. Returns chat(system, user, json_mode) -> (text, meta)."""
    kind, _, name = spec.partition(":")
    if kind == "ollama":
        tags = _ollama_request(host, "/api/tags", timeout=30)
        names = {m.get("name") for m in tags.get("models", [])} | {m.get("model") for m in tags.get("models", [])}
        if name not in names and f"{name}:latest" not in names:
            raise SystemExit(f"model {name!r} is not pulled; run `ollama pull {name}`")

        def chat(system, user, json_mode=True):
            body = {"model": name, "stream": False, "think": False,
                    "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                    "options": {"num_ctx": num_ctx, "temperature": temperature, "num_predict": max_tokens, "seed": 0}}
            if json_mode:
                body["format"] = "json"
            try:
                resp = _ollama_request(host, "/api/chat", body, timeout=900)
            except RuntimeError as exc:
                if "think" in str(exc).lower():
                    body.pop("think")
                    resp = _ollama_request(host, "/api/chat", body, timeout=900)
                else:
                    raise
            return (resp.get("message") or {}).get("content", ""), {"model": f"ollama/{name}", "input_tokens": resp.get("prompt_eval_count"),
                                                                     "output_tokens": resp.get("eval_count")}
        return chat
    if kind == "anthropic":
        try:
            import anthropic
        except ImportError as exc:
            raise SystemExit("pip install anthropic") from exc
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit("set ANTHROPIC_API_KEY in the environment")
        client = anthropic.Anthropic()

        def chat(system, user, json_mode=True):
            resp = client.messages.create(model=name, max_tokens=max_tokens, system=system, temperature=temperature,
                                          messages=[{"role": "user", "content": user}])
            text = "".join(getattr(b, "text", "") or "" for b in resp.content if getattr(b, "type", "") == "text")
            return text, {"model": name, "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}
        return chat
    raise SystemExit(f"unknown backend {spec!r}; use ollama:<tag> or anthropic:<model>")


# ------------------------------------------------------------------------------------------------- checks
def _identifier_leak(text: str, model) -> bool:
    """A rewrite that names tables or columns the way the schema does is not planner language."""
    schema = model.schema()
    idents = set(schema.get("tables", {})) | {c for t in schema.get("tables", {}).values() for c in t.get("columns", {})}
    idents |= set(schema.get("params", {})) | set(model.MEASURE_DIMS)
    words = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text))
    return any(w in words and "_" in w for w in idents)


def _candidate_ok(text: str, original: str, model) -> str | None:
    t = " ".join(text.split())
    if len(t) < 8 or len(t) > 500:
        return "length"
    if t.lower().rstrip("?.!") == original.lower().rstrip("?.!"):
        return "identical"
    if _identifier_leak(t, model):
        return "identifier leak"
    return None


def verification_prompt(task: Task, paraphrase: str, solver: str = "highs") -> str:
    """Exactly what an agent would see for the paraphrased question (the run_baseline prompt)."""
    probe = Task(**{**task.to_dict(), "question": paraphrase})
    env = WhatIfEnv([probe], solver=solver)
    return build_prompt(env.reset(probe))


def verify(task: Task, paraphrase: str, model, data, chat, solver: str, answer_text: str | None = None) -> tuple[bool, dict]:
    """Round trip: an independent translation of the paraphrase must re-solve to the task's reference.
    ``answer_text`` = a translation collected offline; otherwise ``chat`` is asked."""
    if answer_text is not None:
        text, meta = answer_text, {"model": "offline"}
    else:
        text, meta = chat(SYSTEM_PROMPT, verification_prompt(task, paraphrase, solver), json_mode=True)
    try:
        scenario = _extract_json(text)
    except Exception:
        return False, {"reason": "unparseable", **meta}
    try:
        result = solve_scenario(model, scenario, data, solver=solver, keep_decisions=False)
    except Exception as exc:  # a model may reject edited data in build()
        return False, {"reason": f"error: {type(exc).__name__}", **meta}
    if result.status == "invalid":
        return False, {"reason": "invalid: " + result.message[:120], **meta}
    cmp = compare_results(task.reference, result.to_dict(), task.kpi_keys)
    return cmp.match, {"reason": "" if cmp.match else "result differs", **meta}


# ------------------------------------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--split", default=None)
    ap.add_argument("--n", type=int, default=3, help="rewrites requested per task")
    ap.add_argument("--paraphraser", default=None, help="ollama:<tag> | anthropic:<model>")
    ap.add_argument("--verifier", default=None, help="ollama:<tag> | anthropic:<model>; omit with --no-verify")
    ap.add_argument("--no-verify", action="store_true", help="keep every rewrite (NOT for published files)")
    ap.add_argument("--export-paraphrase-prompts", default=None, metavar="DIR")
    ap.add_argument("--import-paraphrases", default=None, metavar="DIR", help="folder of <task_id>.json with {\"paraphrases\": [...]}")
    ap.add_argument("--export-verification-prompts", default=None, metavar="DIR", help="with --import-paraphrases: write <task_id>-c<i>.txt prompts and exit")
    ap.add_argument("--verifier-answers", default=None, metavar="DIR", help="folder of <task_id>-c<i>.json translations collected offline")
    ap.add_argument("--paraphraser-label", default=None, help="provenance label for offline paraphrases (which model/version produced them)")
    ap.add_argument("--verifier-label", default=None, help="provenance label for offline translations")
    ap.add_argument("--host", default=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))
    ap.add_argument("--num-ctx", type=int, default=16384)
    ap.add_argument("--max-tokens", type=int, default=2000)
    ap.add_argument("--solver", default="highs")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    tasks = [t for t in load_tasks(args.tasks, split=args.split) if t.clarification is None]
    if args.limit:
        tasks = tasks[:args.limit]
    if not tasks:
        print("no fully specified tasks in the file (under-specified tasks are skipped)")
        return 1
    model = get_model(tasks[0].model)
    data = model.load_data()

    if args.export_paraphrase_prompts:
        out_dir = Path(args.export_paraphrase_prompts)
        out_dir.mkdir(parents=True, exist_ok=True)
        for t in tasks:
            (out_dir / f"{t.id}.txt").write_text("SYSTEM:\n" + PARAPHRASE_SYSTEM + "\n\nUSER:\n" + paraphrase_prompt(t, model, args.n), encoding="utf-8")
        print(f"wrote {len(tasks)} paraphrase prompts to {out_dir}")
        return 0

    para_chat = make_chat(args.paraphraser, args.host, args.num_ctx, args.max_tokens, temperature=0.8) if args.paraphraser else None
    if para_chat is None and not args.import_paraphrases:
        ap.error("need --paraphraser or --import-paraphrases")
    ver_chat = None
    offline_verify = bool(args.verifier_answers) or bool(args.export_verification_prompts)
    if not args.no_verify and not offline_verify:
        if not args.verifier:
            ap.error("need --verifier, --verifier-answers, --export-verification-prompts or --no-verify")
        ver_chat = make_chat(args.verifier, args.host, args.num_ctx, args.max_tokens, temperature=0.0)
    if args.export_verification_prompts:
        Path(args.export_verification_prompts).mkdir(parents=True, exist_ok=True)

    counts = collections.Counter()
    kept: list[Task] = []
    para_model = ver_model = None
    t_start = time.time()
    for t in tasks:
        if args.import_paraphrases:
            f = Path(args.import_paraphrases) / f"{t.id}.json"
            if not f.exists():
                counts["no paraphrase file"] += 1
                continue
            try:
                cands = json.loads(f.read_text(encoding="utf-8")).get("paraphrases", [])
            except Exception:
                counts["unparseable paraphrase file"] += 1
                continue
            para_model = para_model or args.paraphraser_label or f"offline:{Path(args.import_paraphrases).name}"
        else:
            text, meta = para_chat(PARAPHRASE_SYSTEM, paraphrase_prompt(t, model, args.n), json_mode=True)
            para_model = meta.get("model")
            try:
                cands = _extract_json(text).get("paraphrases", [])
            except Exception:
                counts["unparseable paraphraser output"] += 1
                continue
        counts["candidates"] += len(cands)
        k = 0
        for i, cand in enumerate(cands):
            if not isinstance(cand, str):
                counts["rejected: not text"] += 1
                continue
            why = _candidate_ok(cand, t.question, model)
            if why:
                counts[f"rejected: {why}"] += 1
                continue
            if args.export_verification_prompts:
                (Path(args.export_verification_prompts) / f"{t.id}-c{i}.txt").write_text(
                    "SYSTEM:\n" + SYSTEM_PROMPT + "\n\nUSER:\n" + verification_prompt(t, cand, args.solver), encoding="utf-8")
                counts["verification prompts written"] += 1
                continue
            if args.verifier_answers:
                f = Path(args.verifier_answers) / f"{t.id}-c{i}.json"
                if not f.exists():
                    counts["rejected: no translation file"] += 1
                    continue
                ok, meta = verify(t, cand, model, data, None, args.solver, answer_text=f.read_text(encoding="utf-8"))
                ver_model = ver_model or args.verifier_label or f"offline:{Path(args.verifier_answers).name}"
                if not ok:
                    counts["rejected: round trip (" + meta["reason"].split(":")[0] + ")"] += 1
                    continue
            elif ver_chat is not None:
                ok, meta = verify(t, cand, model, data, ver_chat, args.solver)
                ver_model = meta.get("model")
                if not ok:
                    counts["rejected: round trip (" + meta["reason"].split(":")[0] + ")"] += 1
                    continue
            k += 1
            new = copy.deepcopy(t.to_dict())
            new["id"] = f"{t.id}-p{k}"
            new["question"] = " ".join(cand.split())
            new["tags"] = list(t.tags) + ["paraphrase"]
            new["slots"] = {**t.slots, "provenance": {"source_task_id": t.id, "original_question": t.question,
                                                      "paraphraser": para_model, "verifier": ver_model, "prompt_version": PROMPT_VERSION}}
            kept.append(Task.from_dict(new))
            counts["kept"] += 1
        print(f"{t.id}: kept {k}/{len(cands)}", flush=True)

    if args.export_verification_prompts:
        print(f"wrote {counts['verification prompts written']} verification prompts to {args.export_verification_prompts}; counts {dict(counts)}")
        return 0
    src = Path(args.tasks)
    out = Path(args.out or src.with_name(src.stem + "_nl.jsonl"))
    save_tasks(kept, out)
    prov = {"source_file": str(src.relative_to(ROOT) if src.is_relative_to(ROOT) else src), "prompt_version": PROMPT_VERSION,
            "paraphrase_system_prompt": PARAPHRASE_SYSTEM, "paraphraser": para_model, "verifier": ver_model,
            "verified": ver_chat is not None or bool(args.verifier_answers), "rewrites_requested_per_task": args.n, "source_tasks": len(tasks),
            "counts": dict(counts), "seconds": round(time.time() - t_start, 1), "date": time.strftime("%Y-%m-%d")}
    out.with_suffix("").with_suffix(".provenance.json").write_text(json.dumps(prov, indent=1), encoding="utf-8")
    print(f"\nwrote {len(kept)} paraphrased tasks to {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    print("counts:", dict(counts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
