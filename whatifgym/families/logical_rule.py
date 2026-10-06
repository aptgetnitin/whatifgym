"""Task family 8 — *logical rule*: an either-or condition that a linear limit cannot state.

"Prod1 and Prod2 may not both be made in March", "If Mine2 is worked in Year3, at least 1,500 tons must come
from it", "If any Prod4 is made in May, at least 200 units of Prod5 must be made too", "At most two of these
products may be sold in June". The answer is a ``logic`` entry: at least ``k`` of several conditions hold, with
negations written out ("never both A and B" is "at least one of not-A, not-B").

Every template picks conditions the base plan violates, so the rule binds. Four generic templates; they work on
any model with a measure that has at least one dimension.
"""
from __future__ import annotations

from .base import FamilyContext, TaskFamily
from .new_limit import _label, _usable

BATCH_FACTORS = [1.5, 2.0, 2.5, 3.0]


def _active_scopes(ctx: FamilyContext, measure: str) -> list[dict]:
    """Scopes (one value of one dimension, or a full index) whose sum is positive in the base plan."""
    dims = ctx.model.MEASURE_DIMS[measure]
    out = []
    for dim in dims:
        for v in ctx.dim_values(measure, dim):
            if ctx.measure_sum(measure, {dim: v}) > 1e-6:
                out.append({dim: v})
    if len(dims) > 1:
        for key, val in ctx.measure_values.get(measure, {}).items():
            if val > 1e-6:
                out.append(dict(zip(dims, key)))
    return out


def _where(ctx: FamilyContext, scope: dict) -> str:
    return ", ".join(f"{ctx.dim_label(d)} {v}" for d, v in scope.items())


def _cond(measure: str, scope: dict, sense: str, value) -> dict:
    return {"measure": measure, "scope": scope, "sense": sense, "value": value}


def _measures(ctx: FamilyContext) -> list[str]:
    return [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m) and _active_scopes(ctx, m)]


def l_never_both(rng, ctx: FamilyContext):
    """Two quantities that are both positive in the base plan may not both be positive."""
    measures = _measures(ctx)
    if not measures:
        return None
    m = rng.choice(measures)
    scopes = _active_scopes(ctx, m)
    same_dims = [s for s in scopes if len(s) == len(scopes[0])]
    if len(same_dims) < 2:
        return None
    a, b = rng.sample(same_dims, 2)
    if a.keys() != b.keys():
        return None
    label = _label(ctx, m)
    q = rng.choice([
        f"What if we may not have both {label} for {_where(ctx, a)} and {label} for {_where(ctx, b)}?",
        f"New rule: {_where(ctx, a)} and {_where(ctx, b)} cannot both have {label}. Re-plan.",
    ])
    rule = {"at_least": 1, "of": [_cond(m, a, "<=", 0), _cond(m, b, "<=", 0)], "name": f"never_both_{m}"}
    return q, {"logic": [rule]}, {"measure": m, "a": a, "b": b}, "medium"


def l_none_or_batch(rng, ctx: FamilyContext):
    """A positive quantity must be either zero or at least a minimum batch above its base value."""
    measures = [m for m in _measures(ctx) if not ctx.measure_integral.get(m)]
    if not measures:
        return None
    m = rng.choice(measures)
    scope = rng.choice(_active_scopes(ctx, m))
    base = ctx.measure_sum(m, scope)
    q_min = ctx.round_for(m, base * rng.choice(BATCH_FACTORS), base)
    if q_min <= base * 1.05:
        return None
    label = _label(ctx, m)
    q = rng.choice([
        f"What if the {label} for {_where(ctx, scope)} must be either zero or at least {q_min}?",
        f"Minimum batch: if there is any {label} for {_where(ctx, scope)}, it must be at least {q_min}.",
    ])
    rule = {"at_least": 1, "of": [_cond(m, scope, "<=", 0), _cond(m, scope, ">=", q_min)], "name": f"batch_{m}"}
    return q, {"logic": [rule]}, {"measure": m, "scope": scope, "min": q_min}, "medium"


def l_if_then(rng, ctx: FamilyContext):
    """If A is positive, B must reach a level above its base value: at least one of (A <= 0, B >= q)."""
    measures = _measures(ctx)
    if not measures:
        return None
    ma = rng.choice(measures)
    same_kind = [m for m in measures if ctx.measure_integral.get(m) == ctx.measure_integral.get(ma)]
    mb = rng.choice(same_kind)
    a = rng.choice(_active_scopes(ctx, ma))
    b = rng.choice(_active_scopes(ctx, mb))
    if ma == mb and not any(d in b and b[d] != v for d, v in a.items()):
        return None  # same measure: the two scopes must be disjoint, or the question reads as a tautology
    base_b = ctx.measure_sum(mb, b)
    q_min = ctx.round_for(mb, base_b * rng.choice([1.25, 1.5, 2.0]), base_b)
    if q_min <= base_b * 1.05:
        return None
    la, lb = _label(ctx, ma), _label(ctx, mb)
    q = rng.choice([
        f"What if any {la} for {_where(ctx, a)} requires at least {q_min} {lb} for {_where(ctx, b)}?",
        f"Suppose that if there is {la} for {_where(ctx, a)}, the {lb} for {_where(ctx, b)} must be at least {q_min}.",
    ])
    rule = {"at_least": 1, "of": [_cond(ma, a, "<=", 0), _cond(mb, b, ">=", q_min)], "name": f"if_{ma}_then_{mb}"}
    return q, {"logic": [rule]}, {"if": [ma, a], "then": [mb, b], "min": q_min}, "hard"


def l_at_most_k(rng, ctx: FamilyContext):
    """At most k of n values of one dimension may have any of the measure (all n are positive in the base plan)."""
    measures = _measures(ctx)
    if not measures:
        return None
    m = rng.choice(measures)
    dims = ctx.model.MEASURE_DIMS[m]
    dim = rng.choice(list(dims))
    active = [v for v in ctx.dim_values(m, dim) if ctx.measure_sum(m, {dim: v}) > 1e-6]
    if len(active) < 3:
        return None
    n = min(len(active), rng.choice([3, 4, 5]))
    picked = rng.sample(active, n)
    k = rng.randint(1, n - 1)
    label, dl = _label(ctx, m), ctx.dim_label(dim)
    names = ", ".join(str(v) for v in picked[:-1]) + f" and {picked[-1]}"
    q = rng.choice([
        f"What if at most {k} of {dl} {names} may have any {label}?",
        f"Only {k} of these may have {label}: {dl} {names}. Re-plan.",
    ])
    rule = {"at_least": n - k, "of": [_cond(m, {dim: v}, "<=", 0) for v in picked], "name": f"at_most_{k}_{m}"}
    return q, {"logic": [rule]}, {"measure": m, "dim": dim, "values": picked, "k": k}, "hard"


GENERIC_TEMPLATES = {"l_never_both": l_never_both, "l_none_or_batch": l_none_or_batch,
                     "l_if_then": l_if_then, "l_at_most_k": l_at_most_k}


class LogicalRuleFamily(TaskFamily):
    name = "logical_rule"
    description = ("The planner states an either-or condition (never both, none or a minimum batch, if-then, at most "
                   "k of n); the answer is a `logic` entry (at least k of several conditions), re-solved.")
    generic_templates = GENERIC_TEMPLATES
    combo_share = 0.0
    distinct_outcomes = True
    check_all_solvers = True   # indicator binaries make alternative optima with different KPIs more likely
