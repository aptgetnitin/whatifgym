#!/usr/bin/env python3
"""Run the three trivial agents over every task file and write one summary table.

    python scripts/run_trivial_baselines.py                 # all of tasks/*/*.jsonl
    python scripts/run_trivial_baselines.py --out results/trivial_baselines.md

The trivial agents pin the reward scale and catch leaks:

* ``oracle`` submits the hidden gold scenario — must score exactly 1.1 on every fully specified task (else the
  oracle, the scorer or the task file is broken);
* ``noop`` submits an empty but valid scenario — must score 0.1 everywhere (a correct noop means a task whose
  answer is "nothing changes", which the generator is supposed to drop);
* ``ask_then_oracle`` asks a question first — must score 0.9 on fully specified tasks (the −0.2 penalty for a
  needless ask).

Under-specified tasks (family ``under_specified``) invert this: answering without asking scores 0, so there
``oracle`` and ``noop`` must score 0.0 and ``ask_then_oracle`` 1.1. The expectations below are per task.

Per-episode records go to ``results/scratch/`` (git-ignored); the table goes to ``--out`` (committed).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from run_baseline import agent_ask_then_oracle, agent_noop, agent_oracle, run  # noqa: E402
from whatifgym.tasks import load_tasks  # noqa: E402

# expected reward per agent: (fully specified task, under-specified task)
AGENTS = {"oracle": (agent_oracle, (1.1, 0.0)), "noop": (agent_noop, (0.1, 0.0)), "ask_then_oracle": (agent_ask_then_oracle, (0.9, 1.1))}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tasks", nargs="*", default=None, help="task files (default: tasks/*/*_v0.jsonl)")
    ap.add_argument("--out", default=str(ROOT / "results" / "trivial_baselines.md"))
    ap.add_argument("--solver", default="highs")
    args = ap.parse_args(argv)

    files = [Path(p).resolve() for p in args.tasks] if args.tasks else sorted(ROOT.glob("tasks/*/*.jsonl"))
    scratch = ROOT / "results" / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    rows, problems = [], []
    for path in files:
        tasks = load_tasks(path)
        row = {"file": str(path.relative_to(ROOT)), "n": len(tasks)}
        for name, (agent, expected) in AGENTS.items():
            records = run(tasks, agent, solver=args.solver)
            mean = sum(r["reward"] for r in records) / len(records)
            row[name] = mean
            off = [r["task_id"] for r in records if abs(r["reward"] - expected[1 if r.get("ask_needed") else 0]) > 1e-9]
            if off:
                problems.append(f"{path.relative_to(ROOT)} / {name}: {len(off)} episodes off expectation {expected}: {off[:5]}")
            with open(scratch / f"{path.parent.name}.{path.stem}.{name}.jsonl", "w", encoding="utf-8") as fh:
                import json
                for r in records:
                    fh.write(json.dumps(r, default=str) + "\n")
        rows.append(row)
        print(f"{row['file']:55s} n={row['n']:3d} oracle {row['oracle']:.3f} noop {row['noop']:.3f} ask_then_oracle {row['ask_then_oracle']:.3f}", flush=True)

    lines = ["# Trivial baselines", "",
             "Mean reward of the three trivial agents on every task file (`scripts/run_trivial_baselines.py`). "
             "Expected on fully specified tasks: oracle 1.100 (gold scenario), noop 0.100 (valid but empty scenario: "
             "validity bonus only), ask_then_oracle 0.900 (gold scenario after one needless clarification). On "
             "`under_specified` files the expectations are 0.000 / 0.000 / 1.100, because answering without asking "
             "scores 0 there. Any other value is a bug or a leaked task.", "",
             "| task file | tasks | oracle | noop | ask_then_oracle |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['file']}` | {r['n']} | {r['oracle']:.3f} | {r['noop']:.3f} | {r['ask_then_oracle']:.3f} |")
    total = sum(r["n"] for r in rows)
    lines += ["", f"Total tasks: **{total}** in {len(rows)} files.", ""]
    if problems:
        lines += ["## Problems", ""] + [f"- {p}" for p in problems] + [""]
    else:
        lines += ["No deviations from the expected rewards.", ""]
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {Path(args.out).relative_to(ROOT) if Path(args.out).is_relative_to(ROOT) else args.out}")
    if problems:
        print("PROBLEMS:\n  " + "\n  ".join(problems))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
