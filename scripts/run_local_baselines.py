#!/usr/bin/env python3
"""Run one or more local Ollama models over every task file and build the comparison tables.

    ollama pull qwen3:8b
    python scripts/run_local_baselines.py --models qwen3:8b
    python scripts/run_local_baselines.py --models qwen3:4b qwen3:8b qwen3:14b qwen3:32b gpt-oss:20b

Resumable: a (model, task file) pair whose result file already exists is skipped, so an interrupted overnight run
continues where it stopped. Per-episode records go to results/baselines/local/<model>/<base_model>.<family>.jsonl,
raw replies to results/baselines/local/<model>/raw_answers/, and the tables to results/baselines/local/summary.md
(plus results/baselines/summary.md across every baseline, frontier runs included).

Ollama's default context window (4096 tokens) would silently truncate our 4-7k-token prompts, so every call sets
--num-ctx (16384 by default). Thinking is off by default for speed and comparability; pass --think on to measure
the thinking variant (write it to a separate label with --label-suffix).
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import run_baseline  # noqa: E402
import summarise_results  # noqa: E402


def slug(model: str) -> str:
    return model.replace(":", "-").replace("/", "-")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", nargs="+", required=True, help="Ollama tags, e.g. qwen3:8b gpt-oss:20b")
    ap.add_argument("--tasks", nargs="*", default=None, help="task files (default: tasks/*/*_v0.jsonl and the tasks/*/*_v0_nl.jsonl paraphrases)")
    ap.add_argument("--split", default=None, help="train | dev | test (default: all tasks)")
    ap.add_argument("--host", default=None)
    ap.add_argument("--num-ctx", type=int, default=16384)
    ap.add_argument("--think", default="off")
    ap.add_argument("--no-json-mode", action="store_true")
    ap.add_argument("--max-tokens", type=int, default=2000)
    ap.add_argument("--think-max-tokens", type=int, default=8192, help="output budget when --think is not off")
    ap.add_argument("--label-suffix", default="", help="appended to the result folder name, e.g. -think")
    ap.add_argument("--limit", type=int, default=None, help="tasks per file (smoke test)")
    ap.add_argument("--force", action="store_true", help="re-run pairs whose result file exists")
    args = ap.parse_args(argv)

    files = [Path(p).resolve() for p in args.tasks] if args.tasks else sorted(ROOT.glob("tasks/*/*_v0.jsonl")) + sorted(ROOT.glob("tasks/*/*_v0_nl.jsonl"))
    out_root = ROOT / "results" / "baselines" / "local"
    t_all = time.time()
    for model in args.models:
        folder = out_root / (slug(model) + args.label_suffix)
        folder.mkdir(parents=True, exist_ok=True)
        print(f"\n===== {model} -> {folder.relative_to(ROOT)}")
        for path in files:
            out = folder / f"{path.parent.name}.{path.stem}.jsonl"
            if out.exists() and not args.force:
                print(f"skip   {out.relative_to(ROOT)} (exists)")
                continue
            argv_run = ["--tasks", str(path), "--agent", "ollama", "--model", model, "--num-ctx", str(args.num_ctx),
                        "--think", args.think, "--max-tokens", str(args.max_tokens), "--think-max-tokens", str(args.think_max_tokens), "--out", str(out),
                        "--save-answers", str(folder / "raw_answers" / path.parent.name)]
            if args.host:
                argv_run += ["--host", args.host]
            if args.split:
                argv_run += ["--split", args.split]
            if args.no_json_mode:
                argv_run.append("--no-json-mode")
            if args.limit:
                argv_run += ["--limit", str(args.limit)]
            t0 = time.time()
            print(f"run    {path.relative_to(ROOT)} ...", flush=True)
            run_baseline.main(argv_run)
            print(f"       done in {time.time() - t0:.0f}s", flush=True)
        summarise_results.main([str(folder), "--out", str(folder / "summary.md")])
    summarise_results.main([str(out_root), "--out", str(out_root / "summary.md")])
    summarise_results.main([str(ROOT / "results" / "baselines"), "--out", str(ROOT / "results" / "baselines" / "summary.md")])
    print(f"\nall done in {(time.time() - t_all) / 60:.1f} min")
    return 0


if __name__ == "__main__":
    sys.exit(main())
