#!/usr/bin/env python3
"""Draw the hand-audit sample: N tasks at random from the current set, the same share of every family.

    python scripts/make_audit_pack.py                    # 200 tasks -> audit/audit_v1.{jsonl,md,csv}
    python scripts/make_audit_pack.py --n 200 --seed 1 --name audit_v2   # a fresh draw after a generator fix

The auditor reads each question next to its gold scenario and records one verdict per task in the .csv:

    ok          the scenario is what the question asks for
    wrong       the scenario does not match the question (a label error: counts against the 2 % gate)
    ambiguous   the question allows a second reading that gives a different answer (counts as an error too)
    wording     the label is right but the wording is odd (does not count; fix the template)

The draw depends only on --seed and the task ids, so it can be repeated.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from whatifgym.tasks import current_task_files, load_tasks  # noqa: E402


def draw(n: int, seed: int) -> list:
    by_family = defaultdict(list)
    for path in current_task_files():
        for t in load_tasks(path):
            by_family[t.family].append(t)
    total = sum(len(v) for v in by_family.values())
    rng = random.Random(seed)
    picked = []
    # largest-remainder shares, so the counts add up to n exactly
    shares = {f: n * len(v) / total for f, v in by_family.items()}
    counts = {f: int(s) for f, s in shares.items()}
    for f in sorted(shares, key=lambda f: shares[f] - counts[f], reverse=True)[: n - sum(counts.values())]:
        counts[f] += 1
    for f in sorted(by_family):
        picked += rng.sample(sorted(by_family[f], key=lambda t: t.id), counts[f])
    return sorted(picked, key=lambda t: t.id)


def _short(v):
    return f"{v:,.4g}" if isinstance(v, (int, float)) else str(v)


def card(i: int, t, base_objective) -> str:
    ref = t.reference
    lines = [f"### {i}. `{t.id}`", "", f"*{t.model} · {t.family} · template `{t.template}` · {t.difficulty}*", ""]
    for h in t.history or []:
        lines += [f"**Earlier question:** {h['question']}", "", "```json", json.dumps(h["scenario"]), "```", ""]
    lines += [f"**Question:** {t.question}", ""]
    if t.clarification:
        lines += [f"**Planner's answer when asked:** {t.clarification['answer']}", ""]
    lines += ["**Gold scenario:**", "", "```json", json.dumps(t.scenario, indent=1), "```", ""]
    if ref["status"] == "infeasible":
        lines.append(f"**Result:** infeasible; conflicting constraints: {', '.join(ref.get('conflict') or [])}")
    else:
        kpis = ", ".join(f"{k} {_short(v)}" for k, v in ref["kpis"].items() if k in t.kpi_keys and not isinstance(v, dict))
        lines.append(f"**Result:** objective {_short(base_objective)} → {_short(ref['objective'])}" + (f"; {kpis}" if kpis else ""))
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20261112)
    ap.add_argument("--name", default="audit_v1")
    args = ap.parse_args(argv)

    tasks = draw(args.n, args.seed)
    assert len(tasks) == args.n and len({t.id for t in tasks}) == args.n
    out = ROOT / "audit"
    out.mkdir(exist_ok=True)
    base = {}
    for t in tasks:
        if t.model not in base:
            base[t.model] = json.loads((ROOT / "whatifgym" / "models" / t.model / "reference.json").read_text())["objective"]
    with open(out / f"{args.name}.jsonl", "w", encoding="utf-8") as fh:
        for t in tasks:
            fh.write(json.dumps(t.to_dict()) + "\n")
    md = [f"# Hand audit {args.name}: {args.n} tasks (seed {args.seed})", "",
          "For each task: does the gold scenario say what the question asks? Record `ok`, `wrong`, `ambiguous` or "
          f"`wording` in `{args.name}.csv`. Made by `scripts/make_audit_pack.py`.", ""]
    md += [card(i, t, base[t.model]) for i, t in enumerate(tasks, 1)]
    (out / f"{args.name}.md").write_text("\n".join(md), encoding="utf-8")
    sheet = out / f"{args.name}.csv"
    if not sheet.exists():   # never overwrite verdicts already recorded
        with open(sheet, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["n", "task_id", "family", "model", "verdict", "note"])
            for i, t in enumerate(tasks, 1):
                w.writerow([i, t.id, t.family, t.model, "", ""])
    fam = defaultdict(int)
    for t in tasks:
        fam[t.family] += 1
    print(f"wrote audit/{args.name}.jsonl, .md, .csv: {len(tasks)} tasks, {len(base)} base models; by family {dict(sorted(fam.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
