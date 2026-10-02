#!/usr/bin/env python3
"""Solve every base model with every available open solver and compare against the reference optimum.

Each (model, solver) pair runs in its own subprocess, so HiGHS (highspy) and OR-Tools never share a process.

Usage::

    python scripts/verify_models.py                 # all models, all available open solvers
    python scripts/verify_models.py --solvers highs scip
    python scripts/verify_models.py --models factory_planning --json out.json
    python scripts/verify_models.py --include-gurobi  # add Gurobi as a cross-check if gurobipy is installed

Exit code 0 means every pair that ran solved to optimality with an objective matching the reference
(relative tolerance 1e-6, absolute 1e-6); anything else exits 1.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from whatifgym import get_model, list_models  # noqa: E402
from whatifgym.runner import run_subprocess  # noqa: E402
from whatifgym.solvers import available_solvers  # noqa: E402


def close(a: float | None, b: float | None, rel: float = 1e-6, abs_tol: float = 1e-6) -> bool:
    if a is None or b is None:
        return False
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_tol)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", nargs="*", default=None)
    ap.add_argument("--solvers", nargs="*", default=None)
    ap.add_argument("--include-gurobi", action="store_true")
    ap.add_argument("--time-limit", type=float, default=60.0)
    ap.add_argument("--json", default=None, help="write all results to this JSON file")
    args = ap.parse_args(argv)

    models = args.models or list_models()
    solvers = args.solvers or available_solvers(include_gurobi=args.include_gurobi)

    rows, ok = [], True
    for name in models:
        model = get_model(name)
        ref = model.reference()
        for solver in solvers:
            if solver == "cpsat" and not model.supports_cpsat:
                continue
            r = run_subprocess(name, solver, time_limit=args.time_limit)
            match = close(r.get("objective"), ref["objective"])
            passed = r["status"] == "optimal" and match
            if r["status"] == "error" and ("not available" in r.get("message", "") or solver == "gurobi"):
                passed = None  # solver not installed / licence too small: skip, do not fail
            ok = ok and passed is not False
            rows.append({"model": name, "solver": solver, "status": r["status"], "objective": r.get("objective"),
                         "reference": ref["objective"], "match": match, "time_s": r.get("time_s"),
                         "n_vars": r.get("n_vars"), "n_constraints": r.get("n_constraints"),
                         "n_int_vars": r.get("n_int_vars"), "passed": passed, "message": r.get("message", "")})

    # ---- report
    print("| model | solver | status | objective | reference | match | time (s) | vars | cons | int |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        flag = {True: "yes", False: "NO", None: "skipped"}[r["passed"]]
        obj = "" if r["objective"] is None else f"{r['objective']:.6g}"
        t = "" if r["time_s"] is None else f"{r['time_s']:.3f}"
        print(f"| {r['model']} | {r['solver']} | {r['status']} | {obj} | {r['reference']:.6g} | {flag} | {t} "
              f"| {r['n_vars']} | {r['n_constraints']} | {r['n_int_vars']} |")
    failures = [r for r in rows if r["passed"] is False]
    for r in failures:
        print(f"FAIL {r['model']}/{r['solver']}: status={r['status']} objective={r['objective']} {r['message'][:300]}")
    if args.json:
        Path(args.json).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    skipped = sum(1 for r in rows if r["passed"] is None)
    print(f"\n{len(rows) - len(failures) - skipped} matched, {len(failures)} failed, {skipped} skipped "
          f"out of {len(rows)} (model, solver) pairs.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
