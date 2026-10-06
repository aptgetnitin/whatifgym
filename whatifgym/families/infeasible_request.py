"""Task family 9 — *infeasible request*: the planner asks for something the model cannot deliver.

"Sales wants at least 5,000 units of Prod1 in January. Can the plan deliver it?", "Commit to exactly 900 tons of
ore from Mine2 in Year1." The agent writes the request as a scenario, as for any other family; the oracle finds that
it is infeasible and why: the irreducible set of base-model constraints the request clashes with
(``ScenarioResult.conflict``). The scorer compares status *and* conflict, so an unrelated impossible scenario
does not score: the agent must encode the request the planner made.

Every template asks for a level well beyond the base plan; the generator keeps a candidate only when the oracle
finds it infeasible with a non-empty conflict (``accept``), and only when its conflict differs from every
accepted task's (``distinct_outcomes``).
"""
from __future__ import annotations

from .base import FamilyContext, TaskFamily
from .new_limit import _label, _usable

STRETCH = [2.0, 3.0, 5.0, 10.0]


def _where(ctx: FamilyContext, scope: dict) -> str:
    return ", ".join(f"{ctx.dim_label(d)} {v}" for d, v in scope.items())


def _active(ctx: FamilyContext, measure: str, full_key: bool) -> list[dict]:
    """Scopes with a positive base value: one dimension value, or (``full_key``) one full index."""
    dims = ctx.model.MEASURE_DIMS[measure]
    if full_key:
        return [dict(zip(dims, k)) for k, v in ctx.measure_values.get(measure, {}).items() if v > 1e-6]
    return [{d: v} for d in dims for v in ctx.dim_values(measure, d) if ctx.measure_sum(measure, {d: v}) > 1e-6]


def _measures(ctx: FamilyContext) -> list[str]:
    return [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m) and not ctx.measure_integral.get(m)]


def i_floor(rng, ctx: FamilyContext):
    """A floor far above what the base plan does on one scope."""
    measures = _measures(ctx)
    if not measures:
        return None
    m = rng.choice(measures)
    scope = rng.choice(_active(ctx, m, full_key=rng.random() < 0.5) or [None])
    if scope is None:
        return None
    base = ctx.measure_sum(m, scope)
    level = ctx.round_for(m, base * rng.choice(STRETCH), base)
    label = _label(ctx, m)
    q = rng.choice([
        f"Can the plan deliver at least {level} {label} for {_where(ctx, scope)}?",
        f"Management wants at least {level} {label} for {_where(ctx, scope)}. Is that possible?",
        f"What if we must reach {level} {label} for {_where(ctx, scope)}?",
    ])
    rule = {"measure": m, "scope": scope, "sense": ">=", "value": level, "name": f"floor_{m}"}
    return q, {"rules": [rule]}, {"measure": m, "scope": scope, "level": level}, "medium"


def i_commit(rng, ctx: FamilyContext):
    """One decision committed to a level far above the base plan."""
    measures = [m for m in _measures(ctx) if ctx.model.MEASURE_DIMS[m]]
    if not measures:
        return None
    m = rng.choice(measures)
    keys = _active(ctx, m, full_key=True)
    if not keys:
        return None
    scope = rng.choice(keys)
    base = ctx.measure_sum(m, scope)
    level = ctx.round_for(m, base * rng.choice(STRETCH), base)
    label = _label(ctx, m)
    q = rng.choice([
        f"Commit to exactly {level} {label} for {_where(ctx, scope)}, and plan the rest around it.",
        f"We have promised {level} {label} for {_where(ctx, scope)}, no more and no less. Re-plan.",
    ])
    fd = {"measure": m, "scope": scope, "value": level}
    return q, {"fixed_decisions": [fd]}, {"measure": m, "scope": scope, "level": level}, "medium"


def i_floor_total(rng, ctx: FamilyContext):
    """A floor on a measure's total, far above the base plan."""
    measures = _measures(ctx)
    if not measures:
        return None
    m = rng.choice(measures)
    base = ctx.measure_sum(m)
    level = ctx.round_for(m, base * rng.choice(STRETCH), base)
    label = _label(ctx, m)
    q = rng.choice([
        f"Can we reach a total of at least {level} {label}?",
        f"The target is now {level} {label} in total. Can the plan meet it?",
    ])
    rule = {"measure": m, "scope": {}, "sense": ">=", "value": level, "name": f"floor_total_{m}"}
    return q, {"rules": [rule]}, {"measure": m, "level": level}, "easy"


def i_two_floors(rng, ctx: FamilyContext):
    """Two floors, on two values of one dimension, that compete for the same limited resource."""
    measures = _measures(ctx)
    if not measures:
        return None
    m = rng.choice(measures)
    scopes = _active(ctx, m, full_key=False)
    if len(scopes) < 2:
        return None
    a, b = rng.sample(scopes, 2)
    if a.keys() != b.keys():
        return None
    f = rng.choice([1.5, 2.0, 3.0])
    la = ctx.round_for(m, ctx.measure_sum(m, a) * f)
    lb = ctx.round_for(m, ctx.measure_sum(m, b) * f)
    label = _label(ctx, m)
    q = (f"Two requests arrive together: at least {la} {label} for {_where(ctx, a)}, and at least {lb} {label} "
         f"for {_where(ctx, b)}. Can we do both?")
    rules = [{"measure": m, "scope": a, "sense": ">=", "value": la, "name": f"floor_{m}_a"},
             {"measure": m, "scope": b, "sense": ">=", "value": lb, "name": f"floor_{m}_b"}]
    return q, {"rules": rules}, {"measure": m, "a": a, "b": b, "levels": [la, lb]}, "hard"


GENERIC_TEMPLATES = {"i_floor": i_floor, "i_commit": i_commit, "i_floor_total": i_floor_total,
                     "i_two_floors": i_two_floors}


class InfeasibleRequestFamily(TaskFamily):
    name = "infeasible_request"
    description = ("The planner asks for something the model cannot deliver; the answer encodes the request, and the "
                   "oracle must find it infeasible for the same reason: the same base-model constraints in conflict.")
    generic_templates = GENERIC_TEMPLATES
    allow_infeasible = True
    combo_share = 0.0
    distinct_outcomes = True     # one conflict set per task: else a copied answer fits several questions
    check_all_solvers = True

    def accept(self, scenario, ref) -> bool:
        return ref.status == "infeasible" and bool(ref.conflict)
