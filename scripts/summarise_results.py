#!/usr/bin/env python3
"""Combine per-episode result files into the comparison tables the paper needs.

    python scripts/summarise_results.py                        # everything under results/baselines/
    python scripts/summarise_results.py results/baselines/local --out results/baselines/local/summary.md

Each input is a JSONL file written by scripts/run_baseline.py (one record per episode) or a folder of them.
Records are grouped by the model label stored in ``agent_state.model`` (falling back to the file name), and the
base model and family are read off the task id (``<base_model>-<family>-<seed>-<index>``).

Tables written: accuracy by model x family and by model x difficulty, accuracy by model x base model, and a
template-level breakdown for every model (where the misses are).
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_records(paths: list[Path]) -> list[dict]:
    files: list[Path] = []
    for p in paths:
        if p.is_dir():
            files += sorted(f for f in p.rglob("*.jsonl") if "raw_answers" not in f.parts and "scratch" not in f.parts)
        elif p.suffix == ".jsonl":
            files.append(p)
    records = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    r = json.loads(line)
                    r["_file"] = str(f.relative_to(ROOT) if f.is_relative_to(ROOT) else f)
                    r["_label"] = (r.get("agent_state") or {}).get("model") or f.stem
                    parts = r["task_id"].split("-")
                    r["_base_model"], r["_family"] = (parts[0], parts[1]) if len(parts) >= 4 else ("?", "?")
                    if len(parts) >= 5 and parts[4].startswith("p"):
                        r["_family"] += " (nl)"        # a verified natural-language paraphrase of a template task
                    records.append(r)
    return records


def _acc(rows: list[dict]) -> str:
    if not rows:
        return "–"
    return f"{sum(r['correct'] for r in rows) / len(rows):.2f} ({len(rows)})"


def build_tables(records: list[dict], skip_trivial: bool = True) -> str:
    trivial = {"oracle", "noop", "ask_then_oracle"}
    labels = sorted({r["_label"] for r in records if not (skip_trivial and r["_label"] in trivial)})
    by_label = {lab: [r for r in records if r["_label"] == lab] for lab in labels}
    families = sorted({r["_family"] for r in records})
    base_models = sorted({r["_base_model"] for r in records})
    difficulties = [d for d in ("easy", "medium", "hard") if any(r["difficulty"] == d for r in records)]

    lines = ["# Results summary", "",
             "Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and "
             "scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless "
             "clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of "
             "episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. "
             "Trivial agents are left out; see `results/trivial_baselines.md` for them.", ""]

    # ---- model x family / difficulty
    head = ["model", "episodes", "accuracy", "mean reward", "valid DSL", "route ok"] + [f"{f}" for f in families] + difficulties + ["s/episode"]
    lines += ["## By family and difficulty", "", "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for lab in labels:
        rows = by_label[lab]
        n = len(rows)
        lat = [r["agent_state"].get("latency_s") for r in rows if r.get("agent_state", {}).get("latency_s")]
        cells = [f"`{lab}`", str(n), f"{sum(r['correct'] for r in rows) / n:.3f}", f"{sum(r['reward'] for r in rows) / n:.3f}",
                 f"{sum(r['valid_dsl'] for r in rows) / n:.2f}", f"{sum(r.get('route_correct', True) for r in rows) / n:.2f}"]
        cells += [_acc([r for r in rows if r["_family"] == f]) for f in families]
        cells += [_acc([r for r in rows if r["difficulty"] == d]) for d in difficulties]
        cells.append(f"{sum(lat) / len(lat):.1f}" if lat else "–")
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")

    # ---- model x base model
    head = ["base model"] + [f"`{lab}`" for lab in labels]
    lines += ["## By base model", "", "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for bm in base_models:
        cells = [f"`{bm}`"] + [_acc([r for r in by_label[lab] if r["_base_model"] == bm]) for lab in labels]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")

    # ---- template breakdown per model (misses first)
    lines += ["## By template (where the misses are)", ""]
    for lab in labels:
        rows = by_label[lab]
        groups = collections.defaultdict(list)
        for r in rows:
            groups[(r["_family"], r["template"])].append(r)
        ordered = sorted(groups.items(), key=lambda kv: (sum(x["correct"] for x in kv[1]) / len(kv[1]), kv[0]))
        lines += [f"### `{lab}`", "", "| family | template | accuracy (n) | typical miss |", "|---|---|---|---|"]
        for (fam, tpl), rs in ordered:
            misses = [x for x in rs if not x["correct"]]
            note = ""
            if misses:
                m = misses[0]
                st = m.get("agent_state", {})
                if st.get("parse_error"):
                    note = "unparseable output"
                elif st.get("missing_answer"):
                    note = "no answer"
                elif m.get("validation_errors"):
                    note = "invalid DSL: " + str(m["validation_errors"][0].get("message", ""))[:80]
                else:
                    note = (m.get("notes") or "wrong result")[:80]
            lines.append(f"| {fam} | {tpl} | {_acc(rs)} | {note} |")
        lines.append("")

    # ---- failure modes
    lines += ["## Failure modes", "", "| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt |", "|---|---|---|---|---|---|"]
    for lab in labels:
        rows = by_label[lab]
        st = [r.get("agent_state", {}) for r in rows]
        invalid = sum(1 for r in rows if not r["valid_dsl"])
        unparse = sum(1 for s in st if s.get("parse_error"))
        wrong = sum(1 for r in rows if not r["correct"] and r["valid_dsl"])
        lines.append(f"| `{lab}` | {wrong} | {invalid} | {unparse} | {sum(1 for s in st if s.get('cut_off'))} | {sum(1 for s in st if s.get('truncated'))} |")
    lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", default=[str(ROOT / "results" / "baselines")])
    ap.add_argument("--out", default=str(ROOT / "results" / "baselines" / "summary.md"))
    ap.add_argument("--include-trivial", action="store_true")
    args = ap.parse_args(argv)
    records = load_records([Path(p) for p in args.paths])
    if not records:
        print("no records found")
        return 1
    text = build_tables(records, skip_trivial=not args.include_trivial)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    print(f"\nwrote {Path(args.out).relative_to(ROOT) if Path(args.out).is_relative_to(ROOT) else args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
