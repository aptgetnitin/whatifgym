"""Task family 5 — *fixed decision*: the planner commits part of the plan and asks for the best rest.

"Commit to making exactly 100 units of Prod3 in January", "do not rent anything out of Glasgow on Monday",
"work Mine2 in every year", "keep the stock of Prod1 at 50 units every month". The answer is the DSL's
``fixed_decisions``: every variable of a measure inside a scope is fixed to one value. Values come from the base
plan so that the commitment changes it (a different level, zero, or a 0/1 decision flipped).
"""
from __future__ import annotations

import re

from .base import FamilyContext, TaskFamily, nice
from .new_limit import _label, _usable

LEVEL_FACTORS = [0.5, 0.75, 1.25, 1.5, 2.0]


def _index_dict(ctx: FamilyContext, measure: str, key: tuple) -> dict:
    return dict(zip(ctx.model.MEASURE_DIMS[measure], key))


def _describe(ctx: FamilyContext, scope: dict) -> str:
    return ", ".join(f"{ctx.dim_label(d)} {v}" for d, v in scope.items())


def _entries(ctx: FamilyContext, measure: str, positive: bool = True):
    vals = ctx.measure_values.get(measure, {})
    return [(k, v) for k, v in vals.items() if (v > 1e-9) == positive]


def f_fix_level(rng, ctx: FamilyContext):
    """Fix one entry of a continuous or integer measure to a different level."""
    ms = [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m) and not _is_binary(ctx, m) and _entries(ctx, m)]
    if not ms:
        return None
    m = rng.choice(ms)
    key, v = rng.choice(_entries(ctx, m))
    w = ctx.round_for(m, v * rng.choice(LEVEL_FACTORS), v)
    if w == v or w <= 0:
        return None
    scope = _index_dict(ctx, m, key)
    label = _label(ctx, m)
    q = rng.choice([
        f"Commit to exactly {w} {label} for {_describe(ctx, scope)} and optimise the rest.",
        f"What if the {label} for {_describe(ctx, scope)} is fixed at {w}?",
        f"Management has decided: {_describe(ctx, scope)} gets {w} {label}, no more and no less. Re-plan everything else.",
    ])
    fd = {"measure": m, "scope": scope, "value": w}
    return q, {"fixed_decisions": [fd]}, {"measure": m, "scope": scope, "value": w, "base": v}, "medium"


def f_fix_zero(rng, ctx: FamilyContext):
    """Fix one entry that is positive in the base plan to zero."""
    ms = [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m) and _entries(ctx, m)]
    if not ms:
        return None
    m = rng.choice(ms)
    key, v = rng.choice(_entries(ctx, m))
    scope = _index_dict(ctx, m, key)
    label = _label(ctx, m)
    if _is_binary(ctx, m):
        q = rng.choice([f"What if {_describe(ctx, scope)} is ruled out (fix that {label} decision to 0)?",
                        f"Suppose we decide against {_describe(ctx, scope)}: set its {label} to 0 and re-plan."])
    else:
        q = rng.choice([f"What if there is no {label} at all for {_describe(ctx, scope)} (fixed at zero)?",
                        f"Fix the {label} for {_describe(ctx, scope)} at 0 and optimise the rest."])
    fd = {"measure": m, "scope": scope, "value": 0}
    return q, {"fixed_decisions": [fd]}, {"measure": m, "scope": scope, "value": 0, "base": v}, "easy"


def f_force_one(rng, ctx: FamilyContext):
    """Force a 0/1 decision that is 0 in the base plan to 1."""
    ms = [m for m in ctx.model.MEASURE_DIMS if _is_binary(ctx, m) and _usable(ctx, m) and _entries(ctx, m, positive=False)]
    if not ms:
        return None
    m = rng.choice(ms)
    key, _ = rng.choice(_entries(ctx, m, positive=False))
    scope = _index_dict(ctx, m, key)
    label = _label(ctx, m)
    q = rng.choice([f"What if {_describe(ctx, scope)} must happen (fix that {label} decision to 1)?",
                    f"Suppose we commit to {_describe(ctx, scope)}: set its {label} to 1 and optimise the rest."])
    fd = {"measure": m, "scope": scope, "value": 1}
    return q, {"fixed_decisions": [fd]}, {"measure": m, "scope": scope, "value": 1, "base": 0}, "medium"


def f_fix_scope(rng, ctx: FamilyContext):
    """Fix every entry of a measure for one value of one dimension to the same level."""
    ms = [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m) and not _is_binary(ctx, m) and len(ctx.model.MEASURE_DIMS[m]) >= 2]
    if not ms:
        return None
    m = rng.choice(ms)
    dims = ctx.model.MEASURE_DIMS[m]
    dim = rng.choice(list(dims))
    vals = [v for v in ctx.dim_values(m, dim) if ctx.measure_sum(m, {dim: v}) > 0]
    if not vals:
        return None
    v = rng.choice(vals)
    entries = [(k, x) for k, x in ctx.measure_values[m].items() if k[dims.index(dim)] == v]
    avg = sum(x for _, x in entries) / len(entries)
    w = ctx.round_for(m, avg * rng.choice([0.5, 0.75, 1.0, 1.25]), avg)
    if w <= 0:
        return None
    other = [d for d in dims if d != dim]
    label, dl = _label(ctx, m), ctx.dim_label(dim)
    each = " and ".join(ctx.dim_label(d) for d in other)
    q = rng.choice([
        f"What if the {label} for {dl} {v} is fixed at {w} for every {each}?",
        f"Level it out: {dl} {v} gets exactly {w} {label} in each {each}. Optimise the rest.",
    ])
    fd = {"measure": m, "scope": {dim: v}, "value": w}
    return q, {"fixed_decisions": [fd]}, {"measure": m, "dim": dim, "value": v, "level": w}, "hard"


def _is_binary(ctx: FamilyContext, measure: str) -> bool:
    vals = ctx.measure_values.get(measure, {})
    return bool(vals) and ctx.measure_integral.get(measure, False) and all(abs(x) < 1e-9 or abs(x - 1) < 1e-9 for x in vals.values())


GENERIC_TEMPLATES = {"f_fix_level": f_fix_level, "f_fix_zero": f_fix_zero, "f_force_one": f_force_one, "f_fix_scope": f_fix_scope}


def _clause(question: str) -> str:
    first = re.split(r"[?.!](?:\s|$)", question, maxsplit=1)[0]
    first = re.sub(r"^(What if|Suppose|Commit to|Fix|Level it out:|Management has decided:)\s+", "", first).strip().rstrip("?.,;")
    if first and first.split(" ", 1)[0] in {"The", "There"}:
        first = first[0].lower() + first[1:]
    return first


class FixedDecisionFamily(TaskFamily):
    name = "fixed_decision"
    description = ("The planner commits part of the plan (a level, zero, a 0/1 choice, a whole scope) and asks for "
                   "the best remainder; the answer is the DSL's `fixed_decisions`, re-solved.")
    generic_templates = GENERIC_TEMPLATES
    combo_share = 0.15

    def combo(self, rng):
        templates = self.templates()
        names = list(templates)
        for _ in range(20):
            a, b = rng.sample(names, 2)
            pa, pb = templates[a](rng, self.ctx), templates[b](rng, self.ctx)
            if pa is None or pb is None:
                continue
            ka = {(f["measure"], str(f["scope"])) for f in pa[1]["fixed_decisions"]}
            kb = {(f["measure"], str(f["scope"])) for f in pb[1]["fixed_decisions"]}
            if not (ka & kb) and {f["measure"] for f in pa[1]["fixed_decisions"]} != {f["measure"] for f in pb[1]["fixed_decisions"]}:
                break
        else:
            return None
        q = rng.choice([f"Two commitments at once: {_clause(pa[0])}; and {_clause(pb[0])}. Optimise the rest.",
                        f"What if {_clause(pa[0])}, and at the same time {_clause(pb[0])}?"])
        return q, {"fixed_decisions": pa[1]["fixed_decisions"] + pb[1]["fixed_decisions"]}, {"parts": [a, b], "slots": [pa[2], pb[2]]}, "hard"
