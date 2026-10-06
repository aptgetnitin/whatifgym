"""Task family 10 — *chained scenario*: a new question on top of a change that is already applied.

The task carries a ``history``: an earlier question and its scenario, applied already. The new question builds on
it in one of three ways, and the answer is always the *complete* scenario:

* ``c_add``     "On top of that, cap Prod1 at 300 units."      -> earlier change + new change
* ``c_revise``  "Correction: make that 30 % lower, not 20 %."   -> the earlier change with the new number
* ``c_undo``    "Forget that change. Instead, ..."              -> the new change only

Each template checks, by solving, that the history matters: for ``c_add`` the result differs from either change
alone; for ``c_revise`` it differs from the old change and from both changes stacked; for ``c_undo`` it differs
from both changes together. Thus an agent that ignores the history, or copies it blindly, does not score.
"""
from __future__ import annotations

import copy

from . import data_change, new_limit
from .base import FamilyContext, TaskFamily
from ..oracle import solve_scenario
from ..scoring import compare_results

PARTS = ("data_changes", "rules")


def _pool(ctx: FamilyContext) -> dict:
    """The data-change and new-limit templates this model uses (specific ones where they exist)."""
    name = ctx.model.name
    dc = data_change.FACTORY_TEMPLATES if name == "factory_planning" else data_change.GENERIC_TEMPLATES
    nl = new_limit.FACTORY_TEMPLATES if name == "factory_planning" else new_limit.GENERIC_TEMPLATES
    return {**{f"dc:{k}": v for k, v in dc.items()}, **{f"nl:{k}": v for k, v in nl.items()}}


def _draw(rng, ctx):
    pool = _pool(ctx)
    for _ in range(10):
        name = rng.choice(sorted(pool))
        out = pool[name](rng, ctx)
        if out is not None:
            return name, out
    return None, None


def _merge(a: dict, b: dict) -> dict:
    out = {}
    for part in PARTS:
        items = list(a.get(part, [])) + list(b.get(part, []))
        if items:
            out[part] = items
    return out


def _full(ctx, sc: dict) -> dict:
    return {"version": "0.1", "base_model": ctx.model.name, **{k: v for k, v in sc.items() if k in PARTS}}


def _results(ctx, *scenarios):
    out = []
    for sc in scenarios:
        r = solve_scenario(ctx.model, _full(ctx, sc), ctx.data, keep_decisions=False, time_limit=60)
        if r.status != "optimal":
            return None
        out.append(r.to_dict())
    return out


def _same(ctx, r1, r2) -> bool:
    return compare_results(r1, r2, ctx.model.SCORING_KPIS).match


def _pct(f: float) -> str:
    return f"{round((1 - f) * 100)}% lower" if f < 1 else f"{round((f - 1) * 100)}% higher"


def c_add(rng, ctx: FamilyContext):
    na, a = _draw(rng, ctx)
    nb, b = _draw(rng, ctx)
    if a is None or b is None or a[1] == b[1]:
        return None
    ab = _merge(a[1], b[1])
    res = _results(ctx, ab, a[1], b[1])
    if res is None or _same(ctx, res[0], res[1]) or _same(ctx, res[0], res[2]):
        return None
    q = rng.choice([f"On top of that: {b[0]}", f"Keep that change. In addition: {b[0]}"])
    slots = {"first": na, "second": nb, "_history": [{"question": a[0], "scenario": _full(ctx, a[1])}]}
    return q, ab, slots, "medium"


def c_revise(rng, ctx: FamilyContext):
    na, a = _draw(rng, ctx)
    if a is None:
        return None
    sc = a[1]
    revised = copy.deepcopy(sc)
    if len(sc.get("data_changes", [])) == 1 and not sc.get("rules") and sc["data_changes"][0]["op"] == "scale":
        old = sc["data_changes"][0]["factor"]
        opts = [f for f in (0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1.1, 1.2, 1.25, 1.3, 1.5, 2.0)
                if f != old and (f < 1) == (old < 1)]
        if not opts:
            return None
        new = rng.choice(opts)
        revised["data_changes"][0]["factor"] = new
        q = f"Correction: make that {_pct(new)}, not {_pct(old)}."
    elif len(sc.get("rules", [])) == 1 and not sc.get("data_changes") and "value" in sc["rules"][0]:
        rule = sc["rules"][0]
        old = rule["value"]
        if rule["sense"] == "<=":
            new = ctx.round_for(rule["measure"], old * rng.choice([1.1, 1.2, 1.3]), old)   # a looser cap
        elif rule["sense"] == ">=":
            new = ctx.round_for(rule["measure"], old * rng.choice([0.8, 0.85, 0.9]), old)  # a looser floor
        else:
            return None
        if new == old:
            return None
        revised["rules"][0]["value"] = new
        q = f"Correction: make that limit {new}, not {old}."
    else:
        return None
    res = _results(ctx, revised, sc, _merge(sc, revised))
    if res is None or _same(ctx, res[0], res[1]) or _same(ctx, res[0], res[2]):
        return None
    slots = {"first": na, "_history": [{"question": a[0], "scenario": _full(ctx, sc)}]}
    return q, revised, slots, "hard"


def c_undo(rng, ctx: FamilyContext):
    na, a = _draw(rng, ctx)
    nb, b = _draw(rng, ctx)
    if a is None or b is None or a[1] == b[1]:
        return None
    res = _results(ctx, b[1], _merge(a[1], b[1]), a[1])
    if res is None or _same(ctx, res[0], res[1]) or _same(ctx, res[0], res[2]):
        return None
    q = rng.choice([f"Forget that change. Instead: {b[0]}", f"Drop the earlier change; consider only this: {b[0]}"])
    slots = {"first": na, "second": nb, "_history": [{"question": a[0], "scenario": _full(ctx, a[1])}]}
    return q, b[1], slots, "hard"


GENERIC_TEMPLATES = {"c_add": c_add, "c_revise": c_revise, "c_undo": c_undo}


class ChainedScenarioFamily(TaskFamily):
    name = "chained_scenario"
    description = ("A new question on top of an earlier change that is already applied (add to it, correct it, or "
                   "replace it); the answer is the complete scenario, re-solved.")
    generic_templates = GENERIC_TEMPLATES
    combo_share = 0.0
    distinct_outcomes = True
    check_all_solvers = True
