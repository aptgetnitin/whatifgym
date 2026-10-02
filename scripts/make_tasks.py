#!/usr/bin/env python3
"""Generate a task file for one family and one base model, with oracle reference solutions.

    python scripts/make_tasks.py --family data_change --model factory_planning --n 60 --seed 0 \
        --out tasks/factory_planning/data_change_v0.jsonl

Also prints the split counts, the template mix, and (with --check-solvers) whether the family's KPIs are
stable when the reference is re-solved with the other open solvers — the scorer is only fair if they are.
"""
from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from whatifgym.families import FAMILIES  # noqa: E402
from whatifgym.oracle import solve_scenario  # noqa: E402
from whatifgym.scoring import compare_results  # noqa: E402
from whatifgym.solvers import available_solvers  # noqa: E402
from whatifgym.tasks import save_tasks  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", default="data_change", choices=sorted(FAMILIES))
    ap.add_argument("--model", default="factory_planning")
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--solver", default="highs")
    ap.add_argument("--out", default=None)
    ap.add_argument("--check-solvers", action="store_true", help="re-solve every reference with the other open solvers")
    args = ap.parse_args(argv)

    family = FAMILIES[args.family](args.model, solver=args.solver)
    tasks = family.generate(args.n, seed=args.seed)
    out = Path(args.out or ROOT / "tasks" / args.model / f"{args.family}_v0.jsonl")
    n = save_tasks(tasks, out)

    print(f"wrote {n} tasks to {out.relative_to(ROOT)}")
    print("splits:", dict(collections.Counter(t.split for t in tasks)))
    print("difficulty:", dict(collections.Counter(t.difficulty for t in tasks)))
    print("status:", dict(collections.Counter(t.reference['status'] for t in tasks)))
    print("templates:", dict(collections.Counter(t.template for t in tasks)))

    if args.check_solvers:
        others = [s for s in available_solvers() if s not in (args.solver, "cpsat")]
        unstable = collections.Counter()
        for t in tasks:
            for s in others:
                r = solve_scenario(family.model, t.scenario, family.data, solver=s, keep_decisions=False)
                cmp = compare_results(t.reference, r.to_dict(), t.kpi_keys)
                if not cmp.match:
                    unstable[s] += 1
                    print(f"  {t.id} differs on {s}: status {r.status} obj {r.objective} vs {t.reference['objective']} mismatches {cmp.kpi_mismatches}")
        print("references unstable across solvers:", dict(unstable) or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
