"""Task family 1 — *data change*: the planner changes one or two input numbers; the right answer is the
corresponding data edit, re-solved.

Two kinds of templates:
* **specific** templates for ``factory_planning`` with natural planner language (demand, outages, margins, ...);
* **generic** templates that work on any registered model from its ``schema.json`` labels (scale a numeric column
  of one row, change a parameter). Their language is plainer but unambiguous: every selector names the table key.

The reference result is produced by the oracle on the gold scenario; the scorer compares KPIs, never text, so any
equivalent spelling of the edit (``scale`` by 0.8 or ``set`` to the resulting numbers) earns the same reward.
"""
from __future__ import annotations

import re

from .base import FamilyContext, TaskFamily, describe_key, nice

MONTH_NAMES = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April", "May": "May", "Jun": "June"}
MACHINE_NAMES = {"grinder": "grinder", "vertDrill": "vertical drill", "horiDrill": "horizontal drill",
                 "borer": "borer", "planer": "planer"}


def _months(data):
    return [r["month"] for r in sorted(data["months"], key=lambda r: r["order"])]


def _join(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _pct_phrase(pct: int, up: bool) -> str:
    return f"{pct}% {'higher' if up else 'lower'}"


# =========================================================================== factory_planning templates
def t_demand_scale(rng, ctx):
    data = ctx.data
    products = [r["product"] for r in data["products"]]
    months = _months(data)
    p = rng.choice(products)
    k = rng.choice([1, 1, 2, 3])
    start = rng.randrange(0, len(months) - k + 1)
    ms = months[start:start + k]
    nonzero = {(r["month"], r["product"]) for r in data["max_sales"] if r["max_sales"] > 0}
    ms = [m for m in ms if (m, p) in nonzero] or [m for m in months if (m, p) in nonzero][:1]
    pct = rng.choice([10, 15, 20, 25, 30, 40, 50])
    up = rng.random() < 0.5
    factor = round(1 + pct / 100, 4) if up else round(1 - pct / 100, 4)
    mnames = _join([MONTH_NAMES[m] for m in ms])
    q = rng.choice([
        f"What if demand for {p} is {_pct_phrase(pct, up)} in {mnames}?",
        f"Sales now forecast {p} demand {'up' if up else 'down'} {pct}% for {mnames}. What does that do to profit?",
        f"Suppose the market for {p} {'grows' if up else 'shrinks'} by {pct}% in {mnames}.",
    ])
    sc = {"data_changes": [{"op": "scale", "table": "max_sales", "column": "max_sales",
                            "where": {"product": p, "month": ms if len(ms) > 1 else ms[0]}, "factor": factor}]}
    return q, sc, {"product": p, "months": ms, "pct": pct, "up": up}, ("easy" if k == 1 else "medium")


def t_demand_zero(rng, ctx):
    nonzero = [(r["month"], r["product"]) for r in ctx.data["max_sales"] if r["max_sales"] > 0]
    m, p = rng.choice(nonzero)
    q = rng.choice([
        f"What if we cannot sell any {p} in {MONTH_NAMES[m]}?",
        f"The {p} market disappears in {MONTH_NAMES[m]}. Effect on the plan?",
        f"Assume there is zero demand for {p} in {MONTH_NAMES[m]}.",
    ])
    sc = {"data_changes": [{"op": "set", "table": "max_sales", "column": "max_sales", "where": {"product": p, "month": m}, "value": 0}]}
    return q, sc, {"product": p, "month": m}, "easy"


def t_demand_set(rng, ctx):
    rows = [r for r in ctx.data["max_sales"] if r["max_sales"] > 0]
    r = rng.choice(rows)
    v = int(round(r["max_sales"] * rng.choice([0.5, 0.6, 0.75, 1.25, 1.5, 2.0]) / 50.0) * 50) or 50
    q = rng.choice([
        f"What if we can sell at most {v} units of {r['product']} in {MONTH_NAMES[r['month']]}?",
        f"The market limit for {r['product']} in {MONTH_NAMES[r['month']]} becomes {v} units.",
        f"Cap {r['product']} sales in {MONTH_NAMES[r['month']]} at {v}.",
    ])
    sc = {"data_changes": [{"op": "set", "table": "max_sales", "column": "max_sales",
                            "where": {"product": r["product"], "month": r["month"]}, "value": v}]}
    return q, sc, {"product": r["product"], "month": r["month"], "value": v}, "easy"


def t_outage(rng, ctx):
    data = ctx.data
    installed = {r["machine"]: r["installed"] for r in data["machines"]}
    down = {(r["month"], r["machine"]): r["machines_down"] for r in data["downtime"]}
    months = _months(data)
    mc = rng.choice(list(installed))
    m = rng.choice(months)
    n = rng.randint(1, installed[mc])
    while down.get((m, mc), 0) == n:
        m = rng.choice(months)
        n = rng.randint(1, installed[mc])
    name = MACHINE_NAMES[mc]
    q = rng.choice([
        f"What if {n} {name}{'s are' if n > 1 else ' is'} down for maintenance in {MONTH_NAMES[m]}?",
        f"Additional maintenance is scheduled: {n} {name}{'s' if n > 1 else ''} will be unavailable in {MONTH_NAMES[m]} (on top of the existing plan for other machines).",
        f"Assume {n} of the {installed[mc]} {name}{'s' if installed[mc] > 1 else ''} {'are' if n > 1 else 'is'} out of service in {MONTH_NAMES[m]}.",
    ])
    if (m, mc) in down:
        change = {"op": "set", "table": "downtime", "column": "machines_down", "where": {"month": m, "machine": mc}, "value": n}
    else:
        change = {"op": "add", "table": "downtime", "rows": [{"month": m, "machine": mc, "machines_down": n}]}
    return q, {"data_changes": [change]}, {"machine": mc, "month": m, "machines_down": n}, "medium"


def t_outage_cancel(rng, ctx):
    r = rng.choice(ctx.data["downtime"])
    name = MACHINE_NAMES[r["machine"]]
    q = rng.choice([
        f"What if the {name} maintenance planned for {MONTH_NAMES[r['month']]} is cancelled?",
        f"No {name}s are down in {MONTH_NAMES[r['month']]} after all. How much is that worth?",
    ])
    sc = {"data_changes": [{"op": "set", "table": "downtime", "column": "machines_down",
                            "where": {"month": r["month"], "machine": r["machine"]}, "value": 0}]}
    return q, sc, {"machine": r["machine"], "month": r["month"]}, "easy"


def t_install(rng, ctx):
    r = rng.choice(ctx.data["machines"])
    k = rng.choice([1, 1, 2])
    name = MACHINE_NAMES[r["machine"]]
    q = rng.choice([
        f"What if we install {k} more {name}{'s' if k > 1 else ''}?",
        f"We are buying {'another' if k == 1 else f'{k} additional'} {name}{'s' if k > 1 else ''}, available all six months. Profit impact?",
    ])
    sc = {"data_changes": [{"op": "shift", "table": "machines", "column": "installed", "where": {"machine": r["machine"]}, "delta": k}]}
    return q, sc, {"machine": r["machine"], "delta": k}, "easy"


def t_retire(rng, ctx):
    rows = [r for r in ctx.data["machines"] if r["installed"] >= 2]
    r = rng.choice(rows)
    name = MACHINE_NAMES[r["machine"]]
    q = rng.choice([
        f"What if we retire one {name}?",
        f"One of the {r['installed']} {name}s is scrapped for the whole horizon.",
    ])
    sc = {"data_changes": [{"op": "shift", "table": "machines", "column": "installed", "where": {"machine": r["machine"]}, "delta": -1}]}
    return q, sc, {"machine": r["machine"], "delta": -1}, "easy"


def t_margin_set(rng, ctx):
    r = rng.choice(ctx.data["products"])
    v = max(1, int(round(r["profit_per_unit"] * rng.choice([0.5, 0.75, 1.25, 1.5, 2.0]))))
    while v == r["profit_per_unit"]:
        v += 1
    q = rng.choice([
        f"What if the profit contribution of {r['product']} becomes {v} per unit?",
        f"A price change moves {r['product']}'s contribution from {r['profit_per_unit']} to {v}.",
    ])
    sc = {"data_changes": [{"op": "set", "table": "products", "column": "profit_per_unit", "where": {"product": r["product"]}, "value": v}]}
    return q, sc, {"product": r["product"], "value": v}, "easy"


def t_margin_scale(rng, ctx):
    r = rng.choice(ctx.data["products"])
    pct = rng.choice([10, 20, 25, 30, 50])
    up = rng.random() < 0.5
    q = rng.choice([
        f"What if {r['product']}'s contribution per unit is {_pct_phrase(pct, up)}?",
        f"Raw-material prices move: {r['product']} earns {pct}% {'more' if up else 'less'} per unit.",
    ])
    sc = {"data_changes": [{"op": "scale", "table": "products", "column": "profit_per_unit", "where": {"product": r["product"]},
                            "factor": round(1 + pct / 100, 4) if up else round(1 - pct / 100, 4)}]}
    return q, sc, {"product": r["product"], "pct": pct, "up": up}, "medium"


def t_process_hours(rng, ctx):
    r = rng.choice(ctx.data["process_hours"])
    v = round(r["hours_per_unit"] * rng.choice([0.5, 0.75, 1.25, 1.5, 2.0]), 3)
    name = MACHINE_NAMES[r["machine"]]
    q = rng.choice([
        f"What if {r['product']} needs {v} hours per unit on the {name} instead of {r['hours_per_unit']}?",
        f"A process change makes {r['product']} take {v} {name} hours per unit.",
    ])
    sc = {"data_changes": [{"op": "set", "table": "process_hours", "column": "hours_per_unit",
                            "where": {"machine": r["machine"], "product": r["product"]}, "value": v}]}
    return q, sc, {"machine": r["machine"], "product": r["product"], "value": v}, "medium"


def t_param(rng, ctx):
    kind = rng.choice(["holding_cost", "max_inventory", "store_target", "hours_per_month"])
    if kind == "holding_cost":
        f = rng.choice([2.0, 3.0, 0.5])
        q = {2.0: "What if storage cost doubles?", 3.0: "What if storage cost triples?", 0.5: "What if storage cost halves?"}[f]
        change = {"op": "scale_param", "name": "holding_cost", "factor": f}
        slots = {"param": kind, "factor": f}
    elif kind == "max_inventory":
        v = rng.choice([50, 150, 200, 300])
        q = rng.choice([f"What if the warehouse can hold {v} units of each product?",
                        f"Storage capacity per product changes to {v} units a month."])
        change = {"op": "set_param", "name": "max_inventory", "value": v}
        slots = {"param": kind, "value": v}
    elif kind == "store_target":
        v = rng.choice([0, 0, 100, 25])
        q = ("What if there is no end-of-horizon stock requirement?" if v == 0
             else f"What if we must end June with {v} units of every product in stock?")
        change = {"op": "set_param", "name": "store_target", "value": v}
        slots = {"param": kind, "value": v}
    else:
        v = rng.choice([3 * 8 * 24, 8 * 24, 2 * 8 * 20])
        q = {576: "What if we run three shifts (576 machine hours a month instead of 384)?",
             192: "What if we drop to one shift (192 machine hours a month)?",
             320: "What if each month has only 20 working days (320 machine hours a month)?"}[v]
        change = {"op": "set_param", "name": "hours_per_month", "value": v}
        slots = {"param": kind, "value": v}
    return q, {"data_changes": [change]}, slots, "easy"


FACTORY_TEMPLATES = {
    "demand_scale": t_demand_scale, "demand_zero": t_demand_zero, "demand_set": t_demand_set,
    "outage": t_outage, "outage_cancel": t_outage_cancel, "install": t_install, "retire": t_retire,
    "margin_set": t_margin_set, "margin_scale": t_margin_scale, "process_hours": t_process_hours, "param": t_param,
}


# =========================================================================== generic templates (any model)
def _pick_numeric_row(rng, ctx: FamilyContext):
    """A (table, column, row) with a non-zero numeric value, drawn over tables that have numeric columns."""
    options = [(t, c) for t in ctx.schema["tables"] for c in ctx.numeric_columns(t) if ctx.data.get(t)]
    rng.shuffle(options)
    for table, column in options:
        rows = [r for r in ctx.data[table] if isinstance(r.get(column), (int, float)) and not isinstance(r.get(column), bool) and r[column] != 0]
        if rows:
            return table, column, rng.choice(rows)
    return None


def g_scale_column(rng, ctx):
    pick = _pick_numeric_row(rng, ctx)
    if pick is None:
        return None
    table, column, row = pick
    pct = rng.choice([10, 20, 25, 30, 50])
    up = rng.random() < 0.5
    factor = round(1 + pct / 100, 4) if up else round(1 - pct / 100, 4)
    where = {k: row[k] for k in ctx.schema["tables"][table]["key"]}
    q = rng.choice([
        f"What if the {ctx.label('column', table, column)} for {describe_key(ctx, table, row)} is {_pct_phrase(pct, up)}?",
        f"Suppose the {ctx.label('column', table, column)} of {describe_key(ctx, table, row)} (in the {ctx.label('table', table)} table) {'rises' if up else 'falls'} by {pct}%.",
    ])
    sc = {"data_changes": [{"op": "scale", "table": table, "column": column, "where": where, "factor": factor}]}
    return q, sc, {"table": table, "column": column, "where": where, "pct": pct, "up": up}, "medium"


def g_set_column(rng, ctx):
    pick = _pick_numeric_row(rng, ctx)
    if pick is None:
        return None
    table, column, row = pick
    is_int = ctx.schema["tables"][table]["columns"][column].get("type") in ("int", "integer")
    v = row[column] * rng.choice([0.5, 0.75, 1.5, 2.0])
    v = int(round(v)) if is_int else nice(v, row[column])
    if v == row[column] or (is_int and v < 0):
        return None
    where = {k: row[k] for k in ctx.schema["tables"][table]["key"]}
    q = rng.choice([
        f"What if the {ctx.label('column', table, column)} for {describe_key(ctx, table, row)} becomes {v}?",
        f"Assume the {ctx.label('column', table, column)} of {describe_key(ctx, table, row)} is now {v}.",
    ])
    sc = {"data_changes": [{"op": "set", "table": table, "column": column, "where": where, "value": v}]}
    return q, sc, {"table": table, "column": column, "where": where, "value": v}, "easy"


def g_scale_all_rows(rng, ctx):
    """Scale a numeric column for every row ("all demand up 10%")."""
    options = [(t, c) for t in ctx.schema["tables"] for c in ctx.numeric_columns(t) if len(ctx.data.get(t, [])) >= 2]
    if not options:
        return None
    table, column = rng.choice(options)
    pct = rng.choice([10, 20, 25])
    up = rng.random() < 0.5
    factor = round(1 + pct / 100, 4) if up else round(1 - pct / 100, 4)
    q = rng.choice([
        f"What if the {ctx.label('column', table, column)} is {_pct_phrase(pct, up)} for every row of the {ctx.label('table', table)} table?",
        f"Every {ctx.label('column', table, column)} in the {ctx.label('table', table)} table {'rises' if up else 'falls'} by {pct}%. Effect?",
    ])
    sc = {"data_changes": [{"op": "scale", "table": table, "column": column, "factor": factor}]}
    return q, sc, {"table": table, "column": column, "pct": pct, "up": up}, "medium"


def _share_like(name: str, label: str) -> bool:
    text = f"{name} {label}".lower()
    return any(w in text for w in ("share", "fraction", "rate", "probability", "proportion", "attrition"))


def g_param(rng, ctx):
    params = ctx.numeric_params()
    if not params:
        return None
    name = rng.choice(params)
    base = ctx.data["params"][name]
    label = ctx.label("param", name)
    if rng.random() < 0.5 and base != 0:
        f = rng.choice([0.5, 0.75, 1.25, 1.5, 2.0])
        if not ctx.param_in_bounds(name, base * f) or (_share_like(name, label) and 0 <= base <= 1 and base * f > 1):
            return None
        phrase = {2.0: "doubled", 0.5: "halved"}.get(f, f"{int(round(abs(f - 1) * 100))}% {'higher' if f > 1 else 'lower'}")
        q = rng.choice([f"What if the {label} is {phrase}?", f"The {label} changes by a factor of {f}."])
        return q, {"data_changes": [{"op": "scale_param", "name": name, "factor": f}]}, {"param": name, "factor": f}, "easy"
    is_int = ctx.schema.get("params", {}).get(name, {}).get("type") in ("int", "integer")
    v = nice(base * rng.choice([0.5, 0.75, 1.5, 2.0]), base) if base != 0 else rng.choice([1, 5, 10])
    if is_int:
        v = int(round(v))
    if v == base or not ctx.param_in_bounds(name, v) or (_share_like(name, label) and 0 <= base <= 1 and v > 1):
        return None
    q = rng.choice([f"What if the {label} is set to {v}?", f"Assume the {label} becomes {v}."])
    return q, {"data_changes": [{"op": "set_param", "name": name, "value": v}]}, {"param": name, "value": v}, "easy"


def _singular(ctx: FamilyContext, table: str) -> str:
    """The natural noun for one row of an entity table: the label of its key column ("item", "guest", "generator type")."""
    keys = ctx.schema["tables"][table].get("key", [])
    if len(keys) == 1:
        return ctx.label("column", table, keys[0])
    label = ctx.label("table", table)
    return label[:-1] if label.endswith("s") and not label.endswith("ss") else label


def g_remove_row(rng, ctx):
    """Drop one row of a free-standing table ("item 4 is no longer needed", "guest K cancels")."""
    tables = ctx.removable_tables()
    if not tables:
        return None
    table = rng.choice(tables)
    row = rng.choice(ctx.data[table])
    keys = ctx.schema["tables"][table]["key"]
    where = {k: row[k] for k in keys}
    who = describe_key(ctx, table, row)
    q = rng.choice([
        f"What if {who} is removed from the {ctx.label('table', table)} table?",
        f"Suppose {who} drops out entirely (delete that {_singular(ctx, table)} and re-plan).",
        f"Assume {who} is no longer part of the problem. What does the plan look like without it?",
    ])
    sc = {"data_changes": [{"op": "remove", "table": table, "where": where}]}
    return q, sc, {"table": table, "where": where}, "medium"


def g_add_row(rng, ctx):
    """Add one row to a free-standing table, copying a sibling row's shape with perturbed numbers."""
    tables = [t for t in ctx.removable_tables()
              if all(cs.get("type") in ("number", "int", "integer", "float") or c in ctx.schema["tables"][t]["key"]
                     for c, cs in ctx.schema["tables"][t]["columns"].items())
              and len(ctx.schema["tables"][t]["key"]) == 1]
    if not tables:
        return None
    table = rng.choice(tables)
    spec = ctx.schema["tables"][table]
    key = spec["key"][0]
    existing = {r[key] for r in ctx.data[table]}
    new_key = next(k for k in (f"new_{key}", "new_1", "new_2", "new_3") if k not in existing)
    sibling = rng.choice(ctx.data[table])
    row = {key: new_key}
    parts = []
    for c, cs in spec["columns"].items():
        if c == key:
            continue
        v = sibling[c]
        if cs.get("editable") is False:
            # structural column: an ordering (all values distinct) continues after the current maximum; a state
            # column (repeated values, e.g. "on at start") takes its smallest, i.e. default, value
            vals = [r[c] for r in ctx.data[table] if isinstance(r[c], (int, float))]
            if vals:
                v = (max(vals) + 1) if len(set(vals)) == len(vals) else min(vals)
        elif isinstance(v, (int, float)) and not isinstance(v, bool) and v != 0:
            v = v * rng.choice([0.6, 0.8, 1.0, 1.25, 1.5])
            v = int(round(v)) if cs.get("type") in ("int", "integer") else nice(v, sibling[c])
        row[c] = v
        parts.append(f"{ctx.label('column', table, c)} {v}")
    q = rng.choice([
        f"What if a new {_singular(ctx, table)} '{new_key}' is added with {_join(parts)}?",
        f"Add one more row to the {ctx.label('table', table)} table: {ctx.label('column', table, key)} {new_key}, {_join(parts)}. Effect on the plan?",
    ])
    sc = {"data_changes": [{"op": "add", "table": table, "rows": [row]}]}
    return q, sc, {"table": table, "row": row}, "medium"


GENERIC_TEMPLATES = {"g_scale_column": g_scale_column, "g_set_column": g_set_column,
                     "g_scale_all_rows": g_scale_all_rows, "g_param": g_param,
                     "g_remove_row": g_remove_row, "g_add_row": g_add_row}


# =========================================================================== combos
def _clause(question: str) -> str:
    first = re.split(r"[?.!](?:\s|$)", question, maxsplit=1)[0]
    first = re.sub(r"^(What if|Suppose|Assume|Set)\s+", "", first).strip().rstrip("?.,;")
    starters = {"The", "We", "No", "A", "An", "One", "Our", "Storage", "Sales", "Raw-material", "Maintenance",
                "Cap", "There", "Two", "Each", "Demand", "Every", "Additional", "Add"}
    if first and first.split(" ", 1)[0] in starters:
        first = first[0].lower() + first[1:]
    return first


def _touches(scenario: dict) -> set:
    return {(ch.get("table") or ch.get("name")) for ch in scenario["data_changes"]}


class DataChangeFamily(TaskFamily):
    name = "data_change"
    description = ("The planner changes one or two input numbers (demand, capacity, maintenance, margins, process times, "
                   "policy parameters); the answer is the data edit, re-solved.")
    specific_templates = {"factory_planning": FACTORY_TEMPLATES}
    generic_templates = GENERIC_TEMPLATES
    combo_share = 0.15

    def templates(self):
        # a model with rich specific templates uses only those; the others use the generic set
        return dict(self.specific_templates.get(self.model.name) or self.generic_templates)

    def combo(self, rng):
        templates = self.templates()
        names = [n for n in templates if n not in ("param", "g_param")]
        if len(names) < 2:
            return None
        for _ in range(20):
            a, b = rng.sample(names, 2)
            pa, pb = templates[a](rng, self.ctx), templates[b](rng, self.ctx)
            if pa is None or pb is None:
                continue
            if not (_touches(pa[1]) & _touches(pb[1])):
                break
        else:
            return None
        c1, c2 = _clause(pa[0]), _clause(pb[0])
        q = rng.choice([f"What if {c1}, and at the same time {c2}?",
                        f"Two things change together: {c1}; and {c2}. What happens to the plan?",
                        f"Suppose {c1}. On top of that, {c2}."])
        sc = {"data_changes": pa[1]["data_changes"] + pb[1]["data_changes"]}
        return q, sc, {"parts": [a, b], "slots": [pa[2], pb[2]]}, "hard"
