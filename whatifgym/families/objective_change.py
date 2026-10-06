"""Task family 4 — *objective change*: the planner changes what "best" means.

"Keep profit at its maximum, then minimise the stock we carry", "as little oil bought as possible first, then
the best profit that allows", "profit first, then as few start-ups as possible, then as much pumping as possible". The answer is the ``objective`` list of the DSL: one to three lexicographic stages, each ``min`` or
``max`` of the model's own objective (``original``) or of the total of a decision measure over a scope.

The reference objective of such a task is the value of the *last* stage, so an agent that leaves the objective
untouched is wrong by construction; the scoring KPIs still have to match, which pins the plan the stages select.
"""
from __future__ import annotations

from .base import FamilyContext, TaskFamily
from .new_limit import _label, _usable

# a short noun for each model's own objective, used in questions; falls back to the first scoring KPI
OBJECTIVE_NOUN = {
    "factory_planning": "profit", "factory_planning_2": "profit", "food_manufacture": "profit", "mining": "discounted profit",
    "manpower_planning": "total redundancy", "power_generation_hydro": "total generating cost", "multiple_knapsack": "packed value",
    "bin_packing": "the number of bins used", "wedding_seating": "total unhappiness", "car_rental": "weekly profit",
    "car_rental_2": "weekly profit", "farm_planning": "five-year profit", "battery_scheduling": "daily profit",
    "food_supply": "total cost",
}


def _noun(ctx: FamilyContext) -> str:
    return OBJECTIVE_NOUN.get(ctx.model.name) or ctx.model.SCORING_KPIS[0].replace("_", " ")


def _verb(ctx: FamilyContext) -> str:
    return "maximum" if ctx.model.sense == "max" else "minimum"


def _candidates(ctx: FamilyContext):
    """Measures whose total is positive in the base plan (so minimising it is a real change)."""
    return [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m)]


def o_then_min(rng, ctx: FamilyContext):
    ms = _candidates(ctx)
    if not ms:
        return None
    m = rng.choice(ms)
    label = _label(ctx, m)
    q = rng.choice([
        f"Keep {_noun(ctx)} at its {_verb(ctx)}, then minimise the total {label}.",
        f"What if, among all plans that keep {_noun(ctx)} at its {_verb(ctx)}, we pick the one with the least {label} overall?",
        f"Same {_noun(ctx)} as today, but carry as little {label} as possible. What does that plan look like?",
    ])
    stages = [{"sense": ctx.model.sense, "measure": "original"}, {"sense": "min", "measure": m}]
    return q, {"objective": stages}, {"measure": m, "second": "min"}, "medium"


def o_then_max(rng, ctx: FamilyContext):
    ms = _candidates(ctx)
    if not ms:
        return None
    m = rng.choice(ms)
    label = _label(ctx, m)
    q = rng.choice([
        f"Keep {_noun(ctx)} at its {_verb(ctx)}, then maximise the total {label}.",
        f"What if, without giving up any {_noun(ctx)}, we want as much {label} as possible in total?",
    ])
    stages = [{"sense": ctx.model.sense, "measure": "original"}, {"sense": "max", "measure": m}]
    return q, {"objective": stages}, {"measure": m, "second": "max"}, "medium"


def _is_binary(ctx: FamilyContext, measure: str) -> bool:
    vals = ctx.measure_values.get(measure, {})
    return bool(vals) and ctx.measure_integral.get(measure, False) and all(abs(x) < 1e-9 or abs(x - 1) < 1e-9 for x in vals.values())


def o_then_scoped(rng, ctx: FamilyContext):
    """Second stage on a scope of a measure (one key value), not its total. Not for 0/1 measures: pushing a single
    yes/no decision is a fixed decision, not an objective."""
    ms = [m for m in _candidates(ctx) if ctx.model.MEASURE_DIMS[m] and not _is_binary(ctx, m)]
    if not ms:
        return None
    m = rng.choice(ms)
    dim = rng.choice(list(ctx.model.MEASURE_DIMS[m]))
    vals = [v for v in ctx.dim_values(m, dim) if ctx.measure_sum(m, {dim: v}) > 0]
    if not vals:
        return None
    v = rng.choice(vals)
    sense = rng.choice(["min", "max"])
    label, dl = _label(ctx, m), ctx.dim_label(dim)
    q = rng.choice([
        f"Keep {_noun(ctx)} at its {_verb(ctx)}, then {'minimise' if sense == 'min' else 'maximise'} the {label} for {dl} {v}.",
        f"What if we first make sure {_noun(ctx)} stays at its {_verb(ctx)} and then make the {label} for {dl} {v} as {'small' if sense == 'min' else 'large'} as possible?",
    ])
    stages = [{"sense": ctx.model.sense, "measure": "original"}, {"sense": sense, "measure": m, "scope": {dim: v}}]
    return q, {"objective": stages}, {"measure": m, "dim": dim, "value": v, "second": sense}, "medium"


def o_reorder(rng, ctx: FamilyContext):
    """Put a measure first and the original objective second: minimise the measure, then the best original."""
    ms = _candidates(ctx)
    if not ms:
        return None
    m = rng.choice(ms)
    label = _label(ctx, m)
    q = rng.choice([
        f"Minimise the total {label} first; among those plans, take the one with the {_verb(ctx)} {_noun(ctx)}.",
        f"What if the least possible total {label} comes first and {_noun(ctx)} only second?",
        f"New priority: as little {label} as possible, then the {_verb(ctx)} {_noun(ctx)} that allows.",
    ])
    stages = [{"sense": "min", "measure": m}, {"sense": ctx.model.sense, "measure": "original"}]
    return q, {"objective": stages}, {"measure": m, "first": "min"}, "medium"


def o_three_stages(rng, ctx: FamilyContext):
    ms = _candidates(ctx)
    if len(ms) < 2:
        return None
    a, b = rng.sample(ms, 2)
    sa, sb = rng.choice(["min", "max"]), rng.choice(["min", "max"])
    la, lb = _label(ctx, a), _label(ctx, b)
    q = rng.choice([
        f"Priorities in order: {_noun(ctx)} at its {_verb(ctx)} first, then {'the least' if sa == 'min' else 'the most'} total {la}, and after that {'the least' if sb == 'min' else 'the most'} total {lb}.",
        f"What if we keep {_noun(ctx)} at its {_verb(ctx)}, then {'minimise' if sa == 'min' else 'maximise'} the total {la}, and only then {'minimise' if sb == 'min' else 'maximise'} the total {lb}?",
    ])
    stages = [{"sense": ctx.model.sense, "measure": "original"}, {"sense": sa, "measure": a}, {"sense": sb, "measure": b}]
    return q, {"objective": stages}, {"measures": [a, b], "senses": [sa, sb]}, "hard"


GENERIC_TEMPLATES = {"o_then_min": o_then_min, "o_then_max": o_then_max, "o_then_scoped": o_then_scoped,
                     "o_reorder": o_reorder, "o_three_stages": o_three_stages}


class ObjectiveChangeFamily(TaskFamily):
    name = "objective_change"
    description = ("The planner changes what counts as best: keep the original objective at its optimum and then "
                   "minimise or maximise a decision measure (or several, in order), or replace the objective; the "
                   "answer is the DSL's lexicographic `objective` stages, re-solved.")
    generic_templates = GENERIC_TEMPLATES
    combo_share = 0.0   # three-stage questions are the hard variant of this family

    def accept(self, scenario, ref):
        """Drop candidates whose stages leave the plan where it was: every scored KPI equal to the base plan AND the
        last stage's value equal to that measure's base total (the base plan already optimised it)."""
        from ..scoring import REL_TOL, compare_results

        stages = scenario["objective"]
        last = stages[-1]
        base_d = self.ctx.base.to_dict()
        if last["measure"] == "original":
            # the objective is the model's own again: the plan itself must differ from the base plan
            return not compare_results(base_d, ref.to_dict(), self.model.SCORING_KPIS, rel_tol=3 * REL_TOL).match
        base_total = self.ctx.measure_sum(last["measure"], last.get("scope"))
        # at least a 1 % move of the last-stage quantity: anything smaller is the lexicographic tolerance leaking
        moved = abs(ref.objective - base_total) > 0.01 * max(1.0, abs(base_total))
        kpis_moved = not compare_results({**base_d, "objective": ref.objective}, ref.to_dict(),
                                         self.model.SCORING_KPIS, rel_tol=3 * REL_TOL).match
        return moved or kpis_moved
