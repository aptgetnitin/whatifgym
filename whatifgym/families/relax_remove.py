"""Task family 7 — *relax or remove*: a limit of the base model no longer applies.

"What if the machine-hours limit did not apply in March?", "Suppose a closed mine could reopen.", "Drop the
spinning-reserve requirement." The answer is a ``relax`` entry that names a constraint family of the base model,
in full or over a scope of its index.

Only *policy* constraints are relaxed: capacities, specifications, targets and caps a planner could choose to
lift. Balance, flow and definition constraints are left alone (removing them asks a physically meaningless
question), so the family keeps a per-model list of relaxable families with the planner's name for each.
"""
from __future__ import annotations

from .base import FamilyContext, TaskFamily
from ..dsl.apply import constraint_families, relax_targets

# model -> constraint family -> how a planner names it
RELAXABLE: dict[str, dict[str, str]] = {
    "battery_scheduling": {"terminal_soc": "the requirement to end the day with the battery at its terminal charge level"},
    "car_rental_2": {"repair_capacity": "the daily repair-capacity limit",
                     "expansion_limit": "the cap on how many workshop expansions may be ordered"},
    "factory_planning": {"capacity": "the machine-hours limit", "end_stock": "the end-of-horizon stock target"},
    "factory_planning_2": {"capacity": "the machine-hours limit", "end_stock": "the end-of-horizon stock target",
                           "maintenance": "the maintenance requirement"},
    "farm_planning": {"housing": "the housing-capacity limit", "labour": "the labour-hours limit",
                      "final_dairy_cows": "the cap on the size of the final dairy herd"},
    "food_manufacture": {"hardness_min": "the minimum hardness specification",
                         "hardness_max": "the maximum hardness specification",
                         "end_stock": "the end-of-horizon stock target"},
    "manpower_planning": {"retraining_limit": "the limit on retraining", "overmanning": "the cap on overmanning"},
    "mining": {"max_operating": "the limit on how many mines may operate in a year",
               "stay_closed": "the rule that a closed mine can never reopen",
               "quality": "the blend-quality target"},
    "multiple_knapsack": {"capacity": "the weight limit"},
    "power_generation_hydro": {"reserve": "the spinning-reserve requirement"},
    "wedding_seating": {"max_tables": "the limit on the number of tables"},
}


def _families(ctx: FamilyContext) -> dict[str, tuple[str, ...]]:
    dims = constraint_families(ctx.model)
    return {f: dims[f] for f in RELAXABLE.get(ctx.model.name, {}) if f in dims}


def _scope_values(ctx: FamilyContext, fam: str, dim: str) -> list:
    """Values of ``dim`` for which the family has at least one constraint (and so a relaxation does something)."""
    prob = getattr(ctx, "_relax_prob", None)
    if prob is None:  # built once per context and kept on it (an id()-keyed cache would be reused across models)
        prob = ctx.model.build(ctx.data)
        ctx._relax_prob = prob
    return [v for v in ctx.model.index_sets(ctx.data).get(dim, [])
            if relax_targets(ctx.model, prob, ctx.data, {"constraint": fam, "scope": {dim: v}})]


def x_full(rng, ctx: FamilyContext):
    """A whole constraint family is lifted."""
    fams = _families(ctx)
    if not fams:
        return None
    fam = rng.choice(sorted(fams))
    phrase = RELAXABLE[ctx.model.name][fam]
    q = rng.choice([f"What if {phrase} did not apply?",
                    f"Suppose we drop {phrase}. How does the plan change?",
                    f"Remove {phrase} and re-plan."])
    return q, {"relax": [{"constraint": fam}]}, {"constraint": fam}, "easy"


def x_scoped(rng, ctx: FamilyContext):
    """A constraint family is lifted for one or two values of one of its dimensions."""
    fams = {f: d for f, d in _families(ctx).items() if d}
    if not fams:
        return None
    fam = rng.choice(sorted(fams))
    dim = rng.choice(list(fams[fam]))
    values = _scope_values(ctx, fam, dim)
    if len(values) < 2:
        return None
    picked = rng.sample(values, 2) if rng.random() < 0.3 and len(values) >= 3 else [rng.choice(values)]
    phrase, dl = RELAXABLE[ctx.model.name][fam], ctx.dim_label(dim)
    which = f"{dl} {picked[0]}" if len(picked) == 1 else f"{dl} {picked[0]} and {picked[1]}"
    q = rng.choice([f"What if {phrase} did not apply for {which}?",
                    f"Suppose {phrase} is lifted for {which} only. Effect on the plan?"])
    scope = {dim: picked[0] if len(picked) == 1 else picked}
    return q, {"relax": [{"constraint": fam, "scope": scope}]}, {"constraint": fam, "dim": dim, "values": picked}, \
        "medium" if len(picked) == 1 else "hard"


GENERIC_TEMPLATES = {"x_full": x_full, "x_scoped": x_scoped}


class RelaxRemoveFamily(TaskFamily):
    name = "relax_remove"
    description = ("A limit of the base model no longer applies, in full or for part of its index; the answer is a "
                   "`relax` entry naming the constraint family (and scope), re-solved.")
    generic_templates = GENERIC_TEMPLATES
    combo_share = 0.15
    distinct_outcomes = True
    check_all_solvers = True

    def accept(self, scenario, ref) -> bool:
        """A two-part relaxation is kept only when each part matters (neither single part reproduces the result)."""
        from ..scoring import compare_results

        parts = scenario.get("relax", [])
        if len(parts) < 2:
            return True
        for part in parts:
            single = self._solve({**scenario, "relax": [part]}, self.solver)
            if single is None or compare_results(ref.to_dict(), single.to_dict(), self.model.SCORING_KPIS).match:
                return False
        return True

    def combo(self, rng):
        fams = _families(self.ctx)
        if len(fams) < 2:
            return None
        a, b = rng.sample(sorted(fams), 2)
        pa, pb = RELAXABLE[self.model.name][a], RELAXABLE[self.model.name][b]
        q = rng.choice([f"What if neither {pa} nor {pb} applied?",
                        f"Drop two limits at once: {pa}, and {pb}."])
        return q, {"relax": [{"constraint": a}, {"constraint": b}]}, {"parts": [a, b]}, "hard"
