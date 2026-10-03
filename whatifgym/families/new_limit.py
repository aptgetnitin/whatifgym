"""Task family 2 — *new limit*: the planner adds a constraint the model never had.

Unlike a data change there is no cell to edit: the answer is a **rule** on the sum of a decision measure over a
scope (`make[Feb,Prod1] + make[Mar,Prod1] <= 500`), or several rules ("never more than X in any month"). Values are
chosen from the base plan so that the limit binds — a cap below what the plan currently does, a floor above it —
and every task is kept only if the scored KPIs move and the reference is identical on a second solver.

Templates: specific ones for ``factory_planning`` (caps on production, floors on sales, stock limits, per-month
caps/floors) and generic ones for any model from its measures (cap or floor on a measure total over one key value,
or over everything).
"""
from __future__ import annotations

import re

from .base import FamilyContext, TaskFamily, nice
from .data_change import MONTH_NAMES, _join, _months

CAP_FACTORS = [0.5, 0.6, 0.7, 0.75, 0.8, 0.9]
FLOOR_FACTORS = [1.1, 1.2, 1.25, 1.5]


def _rule(measure, scope, sense, value, name=None):
    r = {"measure": measure, "scope": scope, "sense": sense, "value": value}
    if name:
        r["name"] = name
    return r


# =========================================================================== factory_planning templates
def t_cap_total_make(rng, ctx: FamilyContext):
    p = rng.choice([r["product"] for r in ctx.data["products"]])
    base = ctx.measure_sum("make", {"product": p})
    if base <= 0:
        return None
    v = nice(base * rng.choice(CAP_FACTORS), base)
    q = rng.choice([
        f"What if we may make at most {v} units of {p} over the whole six months?",
        f"Total {p} production is capped at {v} units for the horizon. Impact?",
        f"Suppose a supplier constraint limits {p} to {v} units in total.",
    ])
    return q, {"rules": [_rule("make", {"product": p}, "<=", v, f"cap_{p}_total")]}, {"product": p, "value": v}, "easy"


def t_cap_make_months(rng, ctx):
    months = _months(ctx.data)
    p = rng.choice([r["product"] for r in ctx.data["products"]])
    k = rng.choice([2, 2, 3])
    start = rng.randrange(0, len(months) - k + 1)
    ms = months[start:start + k]
    base = ctx.measure_sum("make", {"product": p, "month": ms})
    if base <= 0:
        return None
    v = nice(base * rng.choice(CAP_FACTORS), base)
    mn = _join([MONTH_NAMES[m] for m in ms])
    q = rng.choice([
        f"What if we may make at most {v} units of {p} in {mn} combined?",
        f"Across {mn}, {p} production must not exceed {v} units in total.",
    ])
    return q, {"rules": [_rule("make", {"product": p, "month": ms}, "<=", v, f"cap_{p}_{'_'.join(ms)}")]}, {"product": p, "months": ms, "value": v}, "medium"


def t_floor_sell(rng, ctx):
    months = _months(ctx.data)
    p = rng.choice([r["product"] for r in ctx.data["products"]])
    k = rng.choice([1, 2, 3, 6])
    ms = months if k == 6 else months[(s := rng.randrange(0, len(months) - k + 1)):s + k]
    base = ctx.measure_sum("sell", {"product": p, "month": ms})
    cap = sum(r["max_sales"] for r in ctx.data["max_sales"] if r["product"] == p and r["month"] in ms)
    if base <= 0 or cap <= base * 1.05:
        return None
    v = nice(min(base * rng.choice(FLOOR_FACTORS), cap), base)
    if v <= base:
        return None
    where = "over the whole horizon" if k == 6 else f"in {_join([MONTH_NAMES[m] for m in ms])}"
    q = rng.choice([
        f"What if we commit to selling at least {v} units of {p} {where}?",
        f"A contract requires at least {v} units of {p} to be sold {where}. What does it cost us?",
    ])
    scope = {"product": p} if k == 6 else {"product": p, "month": ms if len(ms) > 1 else ms[0]}
    return q, {"rules": [_rule("sell", scope, ">=", v, f"floor_{p}")]}, {"product": p, "months": ms, "value": v}, "medium"


def t_cap_store_month(rng, ctx):
    months = _months(ctx.data)
    m = rng.choice(months[:-1])  # the last month is pinned by the end-stock target
    base = ctx.measure_sum("store", {"month": m})
    if base <= 0:
        return None
    v = nice(base * rng.choice(CAP_FACTORS), base)
    q = rng.choice([
        f"What if total stock across all products at the end of {MONTH_NAMES[m]} may not exceed {v} units?",
        f"Warehouse space is tight: no more than {v} units in stock in total at the end of {MONTH_NAMES[m]}.",
    ])
    return q, {"rules": [_rule("store", {"month": m}, "<=", v, f"stock_cap_{m}")]}, {"month": m, "value": v}, "medium"


def t_cap_total_store(rng, ctx):
    base = ctx.measure_sum("store")
    if base <= 0:
        return None
    v = nice(base * rng.choice(CAP_FACTORS), base)
    q = rng.choice([
        f"What if total unit-months of stock over the horizon may not exceed {v}?",
        f"Finance caps inventory: the sum of month-end stock over all products and months must stay under {v} units.",
    ])
    return q, {"rules": [_rule("store", {}, "<=", v, "stock_cap_total")]}, {"value": v}, "hard"


def t_cap_each_month(rng, ctx):
    months = _months(ctx.data)
    p = rng.choice([r["product"] for r in ctx.data["products"]])
    per_month = [ctx.measure_sum("make", {"product": p, "month": m}) for m in months]
    if max(per_month) <= 0:
        return None
    v = nice(max(per_month) * rng.choice([0.5, 0.6, 0.75]), max(per_month))
    if v <= 0:
        return None
    q = rng.choice([
        f"What if we never make more than {v} units of {p} in any single month?",
        f"Level the load: {p} production is limited to {v} units per month, every month.",
    ])
    rules = [_rule("make", {"product": p, "month": m}, "<=", v, f"cap_{p}_{m}") for m in months]
    return q, {"rules": rules}, {"product": p, "value": v}, "hard"


def t_min_run_each_month(rng, ctx):
    months = _months(ctx.data)
    p = rng.choice([r["product"] for r in ctx.data["products"]])
    per_month = [ctx.measure_sum("make", {"product": p, "month": m}) for m in months]
    v = nice(max(10.0, min(per_month) + 0.25 * (max(per_month) - min(per_month)) if max(per_month) > 0 else 20.0), max(per_month) or 20.0)
    if v <= min(per_month):
        return None
    q = rng.choice([
        f"What if we must make at least {v} units of {p} every month to keep the line warm?",
        f"A minimum run of {v} units of {p} is required in each of the six months.",
    ])
    rules = [_rule("make", {"product": p, "month": m}, ">=", v, f"minrun_{p}_{m}") for m in months]
    return q, {"rules": rules}, {"product": p, "value": v}, "hard"


def t_cap_two_products_month(rng, ctx):
    months = _months(ctx.data)
    products = [r["product"] for r in ctx.data["products"]]
    p1, p2 = rng.sample(products, 2)
    m = rng.choice(months)
    base = ctx.measure_sum("make", {"product": [p1, p2], "month": m})
    if base <= 0:
        return None
    v = nice(base * rng.choice(CAP_FACTORS), base)
    q = rng.choice([
        f"What if {p1} and {p2} together may not exceed {v} units of production in {MONTH_NAMES[m]}?",
        f"In {MONTH_NAMES[m]}, combined output of {p1} and {p2} is limited to {v} units.",
    ])
    return q, {"rules": [_rule("make", {"product": [p1, p2], "month": m}, "<=", v, f"cap_{p1}_{p2}_{m}")]}, {"products": [p1, p2], "month": m, "value": v}, "medium"


FACTORY_TEMPLATES = {
    "cap_total_make": t_cap_total_make, "cap_make_months": t_cap_make_months, "floor_sell": t_floor_sell,
    "cap_store_month": t_cap_store_month, "cap_total_store": t_cap_total_store, "cap_each_month": t_cap_each_month,
    "min_run_each_month": t_min_run_each_month, "cap_two_products_month": t_cap_two_products_month,
}


# =========================================================================== generic templates (any model)
MAX_MEASURE_VARS = 1000  # a 0/1 measure over thousands of enumerated columns is not a planning quantity


def _usable(ctx: FamilyContext, measure: str) -> bool:
    """Measures with at least one dimension, a non-zero total in the base plan, and a sane number of entries."""
    return (len(ctx.model.MEASURE_DIMS[measure]) >= 1 and ctx.measure_sum(measure) > 0
            and len(ctx.measure_values.get(measure, {})) <= MAX_MEASURE_VARS)


def _label(ctx: FamilyContext, measure: str) -> str:
    """Measure label for a rule sentence; counts of 0/1 or integer measures read as "number of ..."."""
    label = re.sub(r"\s*\(0/1[^)]*\)", "", ctx.label("measure", measure))
    return f"number of {label}" if ctx.measure_integral.get(measure) else label


def g_cap_measure_scope(rng, ctx):
    measures = [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m)]
    if not measures:
        return None
    measure = rng.choice(measures)
    dim = rng.choice(list(ctx.model.MEASURE_DIMS[measure]))
    values = [v for v in ctx.dim_values(measure, dim) if ctx.measure_sum(measure, {dim: v}) > 0]
    if not values:
        return None
    v_dim = rng.choice(values)
    base = ctx.measure_sum(measure, {dim: v_dim})
    cap = ctx.round_for(measure, base * rng.choice(CAP_FACTORS), base)
    if cap <= 0 or cap >= base:
        return None
    label = _label(ctx, measure)
    q = rng.choice([
        f"What if the total {label} for {ctx.dim_label(dim)} {v_dim} may not exceed {cap}?",
        f"Add a limit: the {label}, summed over everything with {ctx.dim_label(dim)} = {v_dim}, must stay at or below {cap}.",
    ])
    return q, {"rules": [_rule(measure, {dim: v_dim}, "<=", cap, f"cap_{measure}_{v_dim}")]}, {"measure": measure, "dim": dim, "value": v_dim, "cap": cap}, "medium"


def g_floor_measure_scope(rng, ctx):
    measures = [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m)]
    if not measures:
        return None
    measure = rng.choice(measures)
    dim = rng.choice(list(ctx.model.MEASURE_DIMS[measure]))
    values = [v for v in ctx.dim_values(measure, dim) if ctx.measure_sum(measure, {dim: v}) > 0]
    if not values:
        return None
    v_dim = rng.choice(values)
    base = ctx.measure_sum(measure, {dim: v_dim})
    floor = ctx.round_for(measure, base * rng.choice(FLOOR_FACTORS), base)
    if floor <= base:
        return None
    label = _label(ctx, measure)
    q = rng.choice([
        f"What if the total {label} for {ctx.dim_label(dim)} {v_dim} must be at least {floor}?",
        f"Add a requirement: the {label}, summed over everything with {ctx.dim_label(dim)} = {v_dim}, must be at least {floor}.",
    ])
    return q, {"rules": [_rule(measure, {dim: v_dim}, ">=", floor, f"floor_{measure}_{v_dim}")]}, {"measure": measure, "dim": dim, "value": v_dim, "floor": floor}, "medium"


def g_cap_measure_total(rng, ctx):
    measures = [m for m in ctx.model.MEASURE_DIMS if _usable(ctx, m)]
    if not measures:
        return None
    measure = rng.choice(measures)
    base = ctx.measure_sum(measure)
    cap = ctx.round_for(measure, base * rng.choice(CAP_FACTORS), base)
    if cap <= 0 or cap >= base:
        return None
    label = _label(ctx, measure)
    q = rng.choice([
        f"What if the total {label}, summed over everything, may not exceed {cap}?",
        f"An overall cap of {cap} applies to the {label} in total.",
    ])
    return q, {"rules": [_rule(measure, {}, "<=", cap, f"cap_{measure}_total")]}, {"measure": measure, "cap": cap}, "easy"


GENERIC_TEMPLATES = {"g_cap_measure_scope": g_cap_measure_scope, "g_floor_measure_scope": g_floor_measure_scope,
                     "g_cap_measure_total": g_cap_measure_total}


def _clause(question: str) -> str:
    first = re.split(r"[?.!](?:\s|$)", question, maxsplit=1)[0]
    first = re.sub(r"^(What if|Suppose|Add a limit:|Add a requirement:|Require)\s+", "", first).strip().rstrip("?.,;")
    if first and first.split(" ", 1)[0] in {"Total", "Across", "A", "An", "Warehouse", "Finance", "Level", "In", "The"}:
        first = first[0].lower() + first[1:]
    return first


class NewLimitFamily(TaskFamily):
    name = "new_limit"
    description = ("The planner adds a constraint the model never had: a cap or floor on the sum of a decision measure "
                   "over a scope; the answer is one or more rules, re-solved.")
    specific_templates = {"factory_planning": FACTORY_TEMPLATES}
    generic_templates = GENERIC_TEMPLATES
    combo_share = 0.15

    def templates(self):
        return dict(self.specific_templates.get(self.model.name) or self.generic_templates)

    def combo(self, rng):
        templates = self.templates()
        names = list(templates)
        if len(names) < 2:
            return None
        for _ in range(20):
            a, b = rng.sample(names, 2)
            pa, pb = templates[a](rng, self.ctx), templates[b](rng, self.ctx)
            if pa is None or pb is None:
                continue
            ma = {(r["measure"], str(r.get("scope"))) for r in pa[1]["rules"]}
            mb = {(r["measure"], str(r.get("scope"))) for r in pb[1]["rules"]}
            if not (ma & mb) and len(pa[1]["rules"]) + len(pb[1]["rules"]) <= 8:
                break
        else:
            return None
        q = rng.choice([f"What if {_clause(pa[0])}, and in addition {_clause(pb[0])}?",
                        f"Two new limits at once: {_clause(pa[0])}; and {_clause(pb[0])}."])
        return q, {"rules": pa[1]["rules"] + pb[1]["rules"]}, {"parts": [a, b], "slots": [pa[2], pb[2]]}, "hard"
