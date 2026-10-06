"""Task family 3 — *relative rule*: a limit expressed relative to another quantity of the plan.

"Prod1 production may be at most 80 % of Prod2's", "Glasgow must account for at least 30 % of all rentals",
"stock may never exceed a quarter of what we make". The answer is a rule with ``relative_to`` and ``factor``
instead of an absolute ``value``; the factor is chosen from the base plan so that the rule binds.

Three generic templates (any model with a measure that has at least one dimension) plus the two-part combo.
"""
from __future__ import annotations

import re

from .base import FamilyContext, TaskFamily
from .new_limit import _label, _usable

RATIOS = [0.25, 0.5, 0.6, 0.75, 0.8, 0.9, 1.0, 1.25, 1.5, 2.0, 3.0]


def _ratio_phrase(f: float) -> str:
    if f == 1.0:
        return "the same as"
    if f < 1.0:
        return f"{int(round(f * 100))}% of"
    return f"{f:g} times"


def _pick_binding(base_ratio: float, sense: str, rng, candidates=RATIOS):
    """A factor that makes the rule bind: below the current ratio for a cap, above it for a floor."""
    if sense == "<=":
        opts = [f for f in candidates if f < base_ratio * 0.97]
    else:
        opts = [f for f in candidates if f > base_ratio * 1.03]
    return rng.choice(opts) if opts else None


def _rel_rule(measure, scope, sense, ref_measure, ref_scope, factor, name):
    return {"measure": measure, "scope": scope, "sense": sense,
            "relative_to": {"measure": ref_measure, "scope": ref_scope}, "factor": factor, "name": name}


def _dims_with_values(ctx: FamilyContext, measure: str, min_values: int = 2):
    out = []
    for dim in ctx.model.MEASURE_DIMS[measure]:
        vals = [v for v in ctx.dim_values(measure, dim) if ctx.measure_sum(measure, {dim: v}) > 0]
        if len(vals) >= min_values:
            out.append((dim, vals))
    return out


def r_two_values(rng, ctx: FamilyContext):
    """Same measure, two values of one dimension: A at most / at least f x B."""
    measures = [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m) and _dims_with_values(ctx, m)]
    if not measures:
        return None
    measure = rng.choice(measures)
    dim, vals = rng.choice(_dims_with_values(ctx, measure))
    a, b = rng.sample(vals, 2)
    sa, sb = ctx.measure_sum(measure, {dim: a}), ctx.measure_sum(measure, {dim: b})
    sense = rng.choice(["<=", ">="])
    f = _pick_binding(sa / sb, sense, rng)
    if f is None:
        return None
    label, dl = _label(ctx, measure), ctx.dim_label(dim)
    q = rng.choice([
        f"What if the {label} for {dl} {a} may be at {'most' if sense == '<=' else 'least'} {_ratio_phrase(f)} the {label} for {dl} {b}?",
        f"New policy: the {label} for {dl} {a} must be at {'most' if sense == '<=' else 'least'} {_ratio_phrase(f)} the {label} for {dl} {b}.",
    ])
    rule = _rel_rule(measure, {dim: a}, sense, measure, {dim: b}, f, f"rel_{measure}_{a}_vs_{b}")
    return q, {"rules": [rule]}, {"measure": measure, "dim": dim, "a": a, "b": b, "factor": f, "sense": sense}, "medium"


def r_share_of_total(rng, ctx: FamilyContext):
    """One value's share of the measure total: at least / at most s of everything."""
    measures = [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m) and _dims_with_values(ctx, m)]
    if not measures:
        return None
    measure = rng.choice(measures)
    dim, vals = rng.choice(_dims_with_values(ctx, measure))
    a = rng.choice(vals)
    share = ctx.measure_sum(measure, {dim: a}) / ctx.measure_sum(measure)
    sense = rng.choice(["<=", ">="])
    f = _pick_binding(share, sense, rng, candidates=[0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75])
    if f is None:
        return None
    label, dl = _label(ctx, measure), ctx.dim_label(dim)
    pct = int(round(f * 100))
    q = rng.choice([
        f"What if {dl} {a} must account for at {'most' if sense == '<=' else 'least'} {pct}% of all {label}?",
        f"Suppose at {'most' if sense == '<=' else 'least'} {pct}% of the total {label} may go to {dl} {a}.",
    ])
    rule = _rel_rule(measure, {dim: a}, sense, measure, {}, f, f"share_{measure}_{a}")
    return q, {"rules": [rule]}, {"measure": measure, "dim": dim, "a": a, "factor": f, "sense": sense}, "medium"


def r_two_measures(rng, ctx: FamilyContext):
    """Total of one measure relative to the total of another ("stock at most 20 % of production")."""
    measures = [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m)]
    if len(measures) < 2:
        return None
    a, b = rng.sample(measures, 2)
    if ctx.measure_integral.get(a) != ctx.measure_integral.get(b):
        return None  # do not relate a count of 0/1 decisions to a continuous quantity
    ratio = ctx.measure_sum(a) / ctx.measure_sum(b)
    sense = rng.choice(["<=", ">="])
    f = _pick_binding(ratio, sense, rng)
    if f is None:
        return None
    la, lb = _label(ctx, a), _label(ctx, b)
    q = rng.choice([
        f"What if the total {la} may be at {'most' if sense == '<=' else 'least'} {_ratio_phrase(f)} the total {lb}?",
        f"Keep the total {la} at {'or below' if sense == '<=' else 'or above'} {_ratio_phrase(f)} the total {lb}. Effect on the plan?",
    ])
    rule = _rel_rule(a, {}, sense, b, {}, f, f"rel_{a}_vs_{b}")
    return q, {"rules": [rule]}, {"measure": a, "ref_measure": b, "factor": f, "sense": sense}, "medium"


GENERIC_TEMPLATES = {"r_two_values": r_two_values, "r_share_of_total": r_share_of_total, "r_two_measures": r_two_measures}


def _clause(question: str) -> str:
    first = re.split(r"[?.!](?:\s|$)", question, maxsplit=1)[0]
    first = re.sub(r"^(What if|Suppose|New policy:|Keep)\s+", "", first).strip().rstrip("?.,;")
    if first and first.split(" ", 1)[0] in {"The", "At"}:
        first = first[0].lower() + first[1:]
    return first


class RelativeRuleFamily(TaskFamily):
    name = "relative_rule"
    description = ("The planner states a limit relative to another quantity of the plan (a ratio between two "
                   "scopes, a share of a total, one measure against another); the answer is a rule with "
                   "`relative_to` and `factor`, re-solved.")
    generic_templates = GENERIC_TEMPLATES
    combo_share = 0.15

    def combo(self, rng):
        templates = self.templates()
        names = list(templates)
        for _ in range(20):
            a, b = rng.sample(names, 2) if len(names) >= 2 else (names[0], names[0])
            pa, pb = templates[a](rng, self.ctx), templates[b](rng, self.ctx)
            if pa is None or pb is None:
                continue
            ka = {(r["measure"], str(r["scope"])) for r in pa[1]["rules"]}
            kb = {(r["measure"], str(r["scope"])) for r in pb[1]["rules"]}
            if not (ka & kb):
                break
        else:
            return None
        q = rng.choice([f"What if {_clause(pa[0])}, and in addition {_clause(pb[0])}?",
                        f"Two relative limits at once: {_clause(pa[0])}; and {_clause(pb[0])}."])
        return q, {"rules": pa[1]["rules"] + pb[1]["rules"]}, {"parts": [a, b], "slots": [pa[2], pb[2]]}, "hard"
