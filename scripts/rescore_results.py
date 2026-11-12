#!/usr/bin/env python3
"""Re-score saved episode records with the solver installed here, without calling any model.

    python scripts/rescore_results.py results/baselines/local/qwen3-4b [more folders] [--jobs 8]

Each record keeps the agent's final scenario and whether it asked first, so the episode can be replayed through the
environment. Use it when records were scored with another solver version: a different HiGHS release can return
another optimal plan of a degenerate model, and a correct answer is then marked wrong. The record files are rewritten
in place; a record whose score changes gets "rescored_from" with its old reward.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from whatifgym.env import WhatIfEnv  # noqa: E402
from whatifgym.tasks import current_task_files, load_tasks  # noqa: E402


def rescore_file(path: str) -> tuple[str, int, int, int]:
    records = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    model, stem = Path(path).name[: -len(".jsonl")].split(".", 1)
    tasks = {t.id: t for t in load_tasks(ROOT / "tasks" / model / f"{stem}.jsonl")}
    env = WhatIfEnv(list(tasks.values()))
    up = down = 0
    for r in records:
        env.reset(tasks[r["task_id"]])
        if r["asked"]:
            env.step({"type": "ask", "text": "replayed question"})
        done = False
        while not done:   # a final action that is itself a question ends the episode at the turn limit
            _, reward, done, info = env.step(r["final_action"])
        if abs(reward - r["reward"]) > 1e-9:
            up += reward > r["reward"]
            down += reward < r["reward"]
            r["rescored_from"] = r["reward"]
            r["reward"] = reward
            for k in ("correct", "valid_dsl", "route_correct"):
                r[k] = info["score"][k]
            r["notes"] = info["score"].get("notes", "")
    with open(path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, default=str) + "\n")
    return path, len(records), up, down


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folders", nargs="+")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args(argv)
    current = {f"{p.parent.name}.{p.stem}.jsonl" for p in current_task_files()}
    files = [str(f) for d in args.folders for f in sorted(Path(d).glob("*.jsonl")) if f.name in current]
    n = up = down = 0
    with ProcessPoolExecutor(args.jobs) as pool:
        for path, k, u, d in pool.map(rescore_file, files):
            n, up, down = n + k, up + u, down + d
            if u or d:
                print(f"{Path(path).parent.name}/{Path(path).name}: +{u} -{d}", flush=True)
    print(f"RESCORED {n} records in {len(files)} files: {up} now better, {down} now worse")
    return 0


if __name__ == "__main__":
    sys.exit(main())
