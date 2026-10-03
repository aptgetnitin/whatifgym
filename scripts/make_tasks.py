#!/usr/bin/env python3
"""Generate task files (questions + hidden gold scenarios + oracle references) for families and base models.

One family on one model:

    python scripts/make_tasks.py --family data_change --model factory_planning --n 60 --seed 0 \
        --out tasks/factory_planning/data_change_v0.jsonl

Every family on every registered model (the usual way to rebuild the benchmark):

    python scripts/make_tasks.py --family all --model all --n 20

Files land in ``tasks/<model>/<family>_v0.jsonl``. An existing file is **kept** unless ``--force`` is given, so
published task files stay frozen (baseline results refer to them) while new ones are added. Each run prints the
split counts, the template mix, why candidates were dropped, and (with ``--check-solvers``) whether every
reference is reproduced by the other open solvers — the scorer is only fair if it is.
"""
from __future__ import annotations

import argparse
import collections
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from whatifgym.families import FAMILIES  # noqa: E402
from whatifgym.oracle import solve_scenario  # noqa: E402
from whatifgym.registry import list_models  # noqa: E402
from whatifgym.scoring import compare_results  # noqa: E402
from whatifgym.solvers import available_solvers  # noqa: E402
from whatifgym.tasks import save_tasks  # noqa: E402


def generate_one(family_name: str, model_name: str, n: int, seed: int, solver: str, out: Path,
                 max_seconds: float | None, check_solvers: bool) -> dict:
    t0 = time.time()
    family = FAMILIES[family_name](model_name, solver=solver)
    tasks = family.generate(n, seed=seed, max_seconds=max_seconds)
    written = save_tasks(tasks, out) if tasks else 0
    if not tasks and out.exists():
        out.unlink()  # nothing to say for this family/model: leave no empty file behind
    info = {
        "family": family_name, "model": model_name, "n": written, "seconds": round(time.time() - t0, 1),
        "splits": dict(collections.Counter(t.split for t in tasks)),
        "difficulty": dict(collections.Counter(t.difficulty for t in tasks)),
        "status": dict(collections.Counter(t.reference["status"] for t in tasks)),
        "templates": dict(collections.Counter(t.template for t in tasks)),
        "skipped": dict(family.skipped),
        "unstable": {},
    }
    if check_solvers and tasks:
        others = [s for s in available_solvers() if s not in (solver, "cpsat")]
        unstable: collections.Counter = collections.Counter()
        for t in tasks:
            for s in others:
                r = solve_scenario(family.model, t.scenario, family.data, solver=s, keep_decisions=False)
                cmp = compare_results(t.reference, r.to_dict(), t.kpi_keys)
                if not cmp.match:
                    unstable[s] += 1
                    print(f"  {t.id} differs on {s}: status {r.status} obj {r.objective} vs {t.reference['objective']} "
                          f"mismatches {cmp.kpi_mismatches}")
        info["unstable"] = dict(unstable)
    return info


def frozen_files() -> set[Path]:
    """Task files listed in tasks/frozen.txt: published results cite them, so they are never regenerated silently."""
    listing = ROOT / "tasks" / "frozen.txt"
    out: set[Path] = set()
    if listing.exists():
        for line in listing.read_text(encoding="utf-8").splitlines():
            entry = line.split("#", 1)[0].strip()
            if entry:
                out.add((ROOT / entry).resolve())
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", default="data_change", help="a family name or 'all'")
    ap.add_argument("--model", default="factory_planning", help="a model name or 'all'")
    ap.add_argument("--n", type=int, default=60, help="tasks to aim for per (family, model)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--solver", default="highs")
    ap.add_argument("--out", default=None, help="output file (single family and model only)")
    ap.add_argument("--version", default="v0", help="suffix of the generated files: <family>_<version>.jsonl")
    ap.add_argument("--force", action="store_true", help="overwrite existing task files (they are kept by default)")
    ap.add_argument("--force-frozen", action="store_true", help="also overwrite files listed in tasks/frozen.txt")
    ap.add_argument("--max-seconds", type=float, default=900.0, help="wall-time budget per (family, model)")
    ap.add_argument("--check-solvers", action="store_true", help="re-solve every reference with the other open solvers")
    args = ap.parse_args(argv)

    families = sorted(FAMILIES) if args.family == "all" else [args.family]
    models = list_models() if args.model == "all" else [args.model]
    if args.out and (len(families) > 1 or len(models) > 1):
        ap.error("--out only applies to a single family and model")

    rows = []
    for model in models:
        for fam in families:
            out = Path(args.out) if args.out else ROOT / "tasks" / model / f"{fam}_{args.version}.jsonl"
            frozen = out.resolve() in frozen_files()
            if out.exists() and (not args.force or (frozen and not args.force_frozen)):
                why = "frozen: listed in tasks/frozen.txt" if frozen else "exists; use --force to regenerate"
                print(f"keep   {out.relative_to(ROOT)} ({why})")
                rows.append({"family": fam, "model": model, "n": sum(1 for _ in open(out, encoding="utf-8") if _.strip()),
                             "seconds": 0.0, "kept": True})
                continue
            print(f"make   {fam} on {model} ...", flush=True)
            info = generate_one(fam, model, args.n, args.seed, args.solver, out, args.max_seconds, args.check_solvers)
            rows.append(info)
            print(f"wrote  {info['n']} tasks to {out.relative_to(ROOT)} in {info['seconds']}s")
            print(f"       splits {info['splits']} difficulty {info['difficulty']} status {info['status']}")
            print(f"       templates {info['templates']}")
            print(f"       dropped candidates {info['skipped'] or 'none'}")
            if args.check_solvers:
                print(f"       references unstable across solvers: {info['unstable'] or 'none'}")

    print("\nsummary")
    total = 0
    for r in rows:
        total += r["n"]
        flag = " (kept)" if r.get("kept") else ""
        print(f"  {r['model']:24s} {r['family']:12s} {r['n']:4d} tasks{flag}")
    print(f"  {'total':24s} {'':12s} {total:4d} tasks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
