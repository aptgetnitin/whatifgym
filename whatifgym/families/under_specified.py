"""Task family 6 — *under-specified*: the planner's question is missing what is needed to act on it.

"What if demand changes?" (which product, how much, when), "suppose we cap production" (of what, at how much).
The correct first action is a clarifying question; the simulated planner answers from the hidden full
specification, and only then can the scenario be written. Each task is built from a fully specified task of
another family: the gold scenario and the reference are that task's, the visible question is a vague version,
and ``clarification.answer`` is the precise statement the planner gives when asked.

The reward for these tasks follows the environment's rules: answering without asking scores 0 even if the guess
happens to be right; asking and then answering correctly scores 1.1.
"""
from __future__ import annotations

import random
import re

from .base import FamilyContext, TaskFamily, describe_key
from .data_change import DataChangeFamily, _singular
from .new_limit import NewLimitFamily, _label

_LEAD = re.compile(r"^(What if|Suppose that|Suppose|Assume that|Assume|Say|Imagine)\s+", re.I)


def _statement(question: str) -> str:
    """The planner's precise answer, as a statement: first sentence of the precise question, lead-in removed."""
    first = re.split(r"(?<=[?.!])\s+", question.strip(), maxsplit=1)[0]
    first = _LEAD.sub("", first).strip().rstrip("?.!,;")
    if not first:
        first = question.strip().rstrip("?.!")
    return first[0].upper() + first[1:] + "."


def _where_text(ctx: FamilyContext, table: str, where: dict | None) -> str:
    if not where:
        return ""
    parts = []
    for k, v in where.items():
        vals = v if isinstance(v, list) else [v]
        parts.append(f"{ctx.label('column', table, k)} {' / '.join(str(x) for x in vals)}")
    return ", ".join(parts)


def _vague_data_change(rng: random.Random, ctx: FamilyContext, change: dict) -> tuple[str, str] | None:
    op = change["op"]
    if op in ("set_param", "scale_param", "shift_param"):
        label = ctx.label("param", change["name"])
        q = rng.choice([f"What if the {label} were different?", f"Suppose the {label} changes. What happens to the plan?",
                        f"We may have to revisit the {label}. Effect?"])
        return q, f"How does the {label} change (new value, or by how much)?"
    table = change["table"]
    tlabel = ctx.label("table", table)
    if op in ("scale", "set", "shift"):
        col = ctx.label("column", table, change["column"])
        where = _where_text(ctx, table, change.get("where"))
        if where and rng.random() < 0.6:
            q = rng.choice([f"What if the {col} for {where} changes?", f"Suppose the {col} for {where} moves. What does that do?"])
            hint = f"Does the {col} go up or down, and by how much (or to what value)?"
        elif where:
            q = rng.choice([f"What if one of the {col} values changes?", f"Suppose the {col} is different for one of the rows in the {tlabel} table."])
            hint = f"Which {tlabel} row, and what is the new {col}?"
        else:
            q = rng.choice([f"What if the {col} changes across the board?", f"Suppose the {col} shifts for every row of the {tlabel} table."])
            hint = f"By how much does the {col} change?"
        return q, hint
    if op == "add":
        one = _singular(ctx, table)
        q = rng.choice([f"What if we add another {one}?", f"Suppose a new {one} joins the {tlabel} table."])
        return q, f"What are the new {one}'s values?"
    if op == "remove":
        one = _singular(ctx, table)
        q = rng.choice([f"What if one of the {tlabel} drops out?", f"Suppose we lose a {one}."])
        return q, f"Which {one}?"
    return None


def _vague_rules(rng: random.Random, ctx: FamilyContext, rules: list[dict]) -> tuple[str, str] | None:
    measures = {r["measure"] for r in rules}
    if len(measures) != 1:
        return None
    m = next(iter(measures))
    label = _label(ctx, m)
    senses = {r["sense"] for r in rules}
    dims = ", ".join(ctx.dim_label(d) for d in ctx.model.MEASURE_DIMS[m]) or "scope"
    if senses == {"<="}:
        q = rng.choice([f"What if we put a cap on the {label}?", f"There is going to be an upper limit on {label}. How does the plan change?",
                        f"Suppose the {label} gets capped."])
        hint = f"Capped where ({dims}) and at what value?"
    elif senses == {">="}:
        q = rng.choice([f"What if we require a minimum {label}?", f"Suppose there is a floor on the {label}."])
        hint = f"A minimum for which {dims}, and how much?"
    else:
        q = rng.choice([f"What if we add a new limit on the {label}?"])
        hint = f"Which limit exactly ({dims}, direction, value)?"
    return q, hint


def _wrap(source_name: str, template, kind: str):
    def wrapped(rng: random.Random, ctx: FamilyContext):
        produced = template(rng, ctx)
        if produced is None:
            return None
        question, scenario, slots, _difficulty = produced
        if kind == "data_change":
            changes = scenario.get("data_changes", [])
            if len(changes) != 1:
                return None
            vague = _vague_data_change(rng, ctx, changes[0])
        else:
            vague = _vague_rules(rng, ctx, scenario.get("rules", []))
        if vague is None:
            return None
        vq, hint = vague
        clarification = {"question_hint": hint, "answer": _statement(question), "source_template": source_name}
        return vq, scenario, {**slots, "_clarification": clarification, "precise_question": question}, "medium"

    wrapped.__name__ = f"ask_{source_name}"
    return wrapped


class UnderSpecifiedFamily(TaskFamily):
    name = "under_specified"
    description = ("The question leaves out what is needed to act (which row, how much, which limit); the right "
                   "first move is a clarifying question, answered by the simulator from the hidden full "
                   "specification. Built from the data_change and new_limit templates.")
    combo_share = 0.0

    def templates(self):
        out = {}
        for fam, kind in ((DataChangeFamily, "data_change"), (NewLimitFamily, "new_limit")):
            source = dict(fam.specific_templates.get(self.model.name) or fam.generic_templates)
            for name, fn in source.items():
                out[f"ask_{name}"] = _wrap(name, fn, kind)
        return out
