"""Task family 1 — *data change*: the planner changes one or two input numbers; the right answer is the
corresponding data edit, re-solved. First instantiated over ``factory_planning``.

Every template is a function ``(rng, data) -> (question, scenario, slots, difficulty)``. Questions are
phrased several ways so that surface form, not just numbers, varies. The reference result is produced by
the oracle on the gold scenario; the scorer compares KPIs, never text, so any equivalent spelling of the
edit (``scale`` by 0.8 or ``set`` to the resulting numbers) earns the same reward.
"""
from __future__ import annotations

import random
from typing import Any, Callable

from ..oracle import solve_scenario
from ..scoring import REL_TOL, compare_results
from ..registry import get_model
from ..tasks import Task, split_for

Template = Callable[[random.Random, dict[str, Any]], tuple[str, dict[str, Any], dict[str, Any], str]]

MONTH_NAMES = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April", "May": "May", "Jun": "June"}
MACHINE_NAMES = {"grinder": "grinder", "vertDrill": "vertical drill", "horiDrill": "horizontal drill",
                 "borer": "borer", "planer": "planer"}


def _months(data):
    return [r["month"] for r in sorted(data["months"], key=lambda r: r["order"])]


def _products(data):
    return [r["product"] for r in data["products"]]


def _join(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _pct_phrase(pct: int, up: bool) -> str:
    return f"{pct}% {'higher' if up else 'lower'}"


# --------------------------------------------------------------------------- templates (factory_planning)
def t_demand_scale(rng, data):
    products = _products(data)
    months = _months(data)
    p = rng.choice(products)
    k = rng.choice([1, 1, 2, 3])
    start = rng.randrange(0, len(months) - k + 1)
    ms = months[start:start + k]
    # only months with non-zero demand make a visible change
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
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [
        {"op": "scale", "table": "max_sales", "column": "max_sales",
         "where": {"product": p, "month": ms if len(ms) > 1 else ms[0]}, "factor": factor}]}
    return q, sc, {"product": p, "months": ms, "pct": pct, "up": up}, ("easy" if k == 1 else "medium")


def t_demand_zero(rng, data):
    nonzero = [(r["month"], r["product"]) for r in data["max_sales"] if r["max_sales"] > 0]
    m, p = rng.choice(nonzero)
    q = rng.choice([
        f"What if we cannot sell any {p} in {MONTH_NAMES[m]}?",
        f"The {p} market disappears in {MONTH_NAMES[m]}. Effect on the plan?",
        f"Assume there is zero demand for {p} in {MONTH_NAMES[m]}.",
    ])
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [
        {"op": "set", "table": "max_sales", "column": "max_sales", "where": {"product": p, "month": m}, "value": 0}]}
    return q, sc, {"product": p, "month": m}, "easy"


def t_demand_set(rng, data):
    rows = [r for r in data["max_sales"] if r["max_sales"] > 0]
    r = rng.choice(rows)
    v = int(round(r["max_sales"] * rng.choice([0.5, 0.6, 0.75, 1.25, 1.5, 2.0]) / 50.0) * 50) or 50
    q = rng.choice([
        f"What if we can sell at most {v} units of {r['product']} in {MONTH_NAMES[r['month']]}?",
        f"The market limit for {r['product']} in {MONTH_NAMES[r['month']]} becomes {v} units.",
        f"Cap {r['product']} sales in {MONTH_NAMES[r['month']]} at {v}.",
    ])
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [
        {"op": "set", "table": "max_sales", "column": "max_sales",
         "where": {"product": r["product"], "month": r["month"]}, "value": v}]}
    return q, sc, {"product": r["product"], "month": r["month"], "value": v}, "easy"


def t_outage(rng, data):
    installed = {r["machine"]: r["installed"] for r in data["machines"]}
    down = {(r["month"], r["machine"]): r["machines_down"] for r in data["downtime"]}
    months = _months(data)
    mc = rng.choice(list(installed))
    m = rng.choice(months)
    n = rng.randint(1, installed[mc])
    while down.get((m, mc), 0) == n:  # make sure something changes
        m = rng.choice(months)
        n = rng.randint(1, installed[mc])
    name = MACHINE_NAMES[mc]
    q = rng.choice([
        f"What if {n} {name}{'s are' if n > 1 else ' is'} down for maintenance in {MONTH_NAMES[m]}?",
        f"Maintenance is rescheduled so that {n} {name}{'s' if n > 1 else ''} will be unavailable in {MONTH_NAMES[m]}.",
        f"Assume {n} of the {installed[mc]} {name}{'s' if installed[mc] > 1 else ''} {'are' if n > 1 else 'is'} out of service in {MONTH_NAMES[m]}.",
    ])
    if (m, mc) in down:
        change = {"op": "set", "table": "downtime", "column": "machines_down", "where": {"month": m, "machine": mc}, "value": n}
    else:
        change = {"op": "add", "table": "downtime", "rows": [{"month": m, "machine": mc, "machines_down": n}]}
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [change]}
    return q, sc, {"machine": mc, "month": m, "machines_down": n}, "medium"


def t_outage_cancel(rng, data):
    r = rng.choice(data["downtime"])
    name = MACHINE_NAMES[r["machine"]]
    q = rng.choice([
        f"What if the {name} maintenance planned for {MONTH_NAMES[r['month']]} is cancelled?",
        f"No {name}s are down in {MONTH_NAMES[r['month']]} after all. How much is that worth?",
    ])
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [
        {"op": "set", "table": "downtime", "column": "machines_down", "where": {"month": r["month"], "machine": r["machine"]}, "value": 0}]}
    return q, sc, {"machine": r["machine"], "month": r["month"]}, "easy"


def t_install(rng, data):
    r = rng.choice(data["machines"])
    k = rng.choice([1, 1, 2])
    name = MACHINE_NAMES[r["machine"]]
    q = rng.choice([
        f"What if we install {k} more {name}{'s' if k > 1 else ''}?",
        f"We are buying {'another' if k == 1 else f'{k} additional'} {name}{'s' if k > 1 else ''}, available all six months. Profit impact?",
    ])
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [
        {"op": "shift", "table": "machines", "column": "installed", "where": {"machine": r["machine"]}, "delta": k}]}
    return q, sc, {"machine": r["machine"], "delta": k}, "easy"


def t_retire(rng, data):
    rows = [r for r in data["machines"] if r["installed"] >= 2]
    r = rng.choice(rows)
    name = MACHINE_NAMES[r["machine"]]
    q = rng.choice([
        f"What if we retire one {name}?",
        f"One of the {r['installed']} {name}s is scrapped for the whole horizon.",
    ])
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [
        {"op": "shift", "table": "machines", "column": "installed", "where": {"machine": r["machine"]}, "delta": -1}]}
    return q, sc, {"machine": r["machine"], "delta": -1}, "easy"


def t_margin_set(rng, data):
    r = rng.choice(data["products"])
    v = max(1, int(round(r["profit_per_unit"] * rng.choice([0.5, 0.75, 1.25, 1.5, 2.0]))))
    while v == r["profit_per_unit"]:
        v += 1
    q = rng.choice([
        f"What if the profit contribution of {r['product']} becomes {v} per unit?",
        f"A price change moves {r['product']}'s contribution from {r['profit_per_unit']} to {v}.",
    ])
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [
        {"op": "set", "table": "products", "column": "profit_per_unit", "where": {"product": r["product"]}, "value": v}]}
    return q, sc, {"product": r["product"], "value": v}, "easy"


def t_margin_scale(rng, data):
    r = rng.choice(data["products"])
    pct = rng.choice([10, 20, 25, 30, 50])
    up = rng.random() < 0.5
    q = rng.choice([
        f"What if {r['product']}'s contribution per unit is {_pct_phrase(pct, up)}?",
        f"Raw-material prices move: {r['product']} earns {pct}% {'more' if up else 'less'} per unit.",
    ])
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [
        {"op": "scale", "table": "products", "column": "profit_per_unit", "where": {"product": r["product"]},
         "factor": round(1 + pct / 100, 4) if up else round(1 - pct / 100, 4)}]}
    return q, sc, {"product": r["product"], "pct": pct, "up": up}, "medium"


def t_process_hours(rng, data):
    r = rng.choice(data["process_hours"])
    v = round(r["hours_per_unit"] * rng.choice([0.5, 0.75, 1.25, 1.5, 2.0]), 3)
    name = MACHINE_NAMES[r["machine"]]
    q = rng.choice([
        f"What if {r['product']} needs {v} hours per unit on the {name} instead of {r['hours_per_unit']}?",
        f"A process change makes {r['product']} take {v} {name} hours per unit.",
    ])
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": [
        {"op": "set", "table": "process_hours", "column": "hours_per_unit",
         "where": {"machine": r["machine"], "product": r["product"]}, "value": v}]}
    return q, sc, {"machine": r["machine"], "product": r["product"], "value": v}, "medium"


def t_param(rng, data):
    P = data["params"]
    kind = rng.choice(["holding_cost", "max_inventory", "store_target", "hours_per_month"])
    if kind == "holding_cost":
        f = rng.choice([2.0, 3.0, 0.5])
        q = {2.0: "What if storage cost doubles?", 3.0: "What if storage cost triples?",
             0.5: "What if storage cost halves?"}[f]
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
    return q, {"version": "0.1", "base_model": "factory_planning", "data_changes": [change]}, slots, "easy"


SINGLE_TEMPLATES: dict[str, Template] = {
    "demand_scale": t_demand_scale, "demand_zero": t_demand_zero, "demand_set": t_demand_set,
    "outage": t_outage, "outage_cancel": t_outage_cancel, "install": t_install, "retire": t_retire,
    "margin_set": t_margin_set, "margin_scale": t_margin_scale, "process_hours": t_process_hours, "param": t_param,
}


def _clause(question: str) -> str:
    """The core clause of a generated question: first sentence, no 'What if', no trailing punctuation."""
    import re

    first = re.split(r"[?.!](?:\s|$)", question, maxsplit=1)[0]
    first = re.sub(r"^(What if|Suppose|Assume)\s+", "", first).strip().rstrip("?.,;")
    starters = {"The", "We", "No", "A", "An", "One", "Our", "Storage", "Sales", "Raw-material", "Maintenance",
                "Cap", "There", "Two", "Each", "Demand"}
    if first and first.split(" ", 1)[0] in starters:
        first = first[0].lower() + first[1:]
    return first


def _touches(scenario: dict) -> set:
    out = set()
    for ch in scenario["data_changes"]:
        key = ch.get("table") or ch.get("name")
        where = ch.get("where") or (ch["rows"][0] if ch.get("op") == "add" else {})
        out.add((key, tuple(sorted((k, str(v)) for k, v in where.items() if k in ("product", "month", "machine")))))
        out.add((key, ()))  # same table twice counts as overlap too, keeps combos readable
    return out


def t_combo(rng, data):
    """Two independent single changes on different tables, in one question (hard)."""
    for _ in range(20):
        names = rng.sample([n for n in SINGLE_TEMPLATES if n != "param"], 2)
        q1, s1, sl1, _ = SINGLE_TEMPLATES[names[0]](rng, data)
        q2, s2, sl2, _ = SINGLE_TEMPLATES[names[1]](rng, data)
        if not (_touches(s1) & _touches(s2)):
            break
    c1, c2 = _clause(q1), _clause(q2)
    q = rng.choice([f"What if {c1}, and at the same time {c2}?",
                    f"Two things change together: {c1}; and {c2}. What happens to profit?",
                    f"Suppose {c1}. On top of that, {c2}."])
    sc = {"version": "0.1", "base_model": "factory_planning", "data_changes": s1["data_changes"] + s2["data_changes"]}
    return q, sc, {"parts": names, "slots": [sl1, sl2]}, "hard"


class DataChangeFamily:
    name = "data_change"
    description = "The planner changes one or two input numbers (demand, capacity, maintenance, margins, process times, policy parameters); the answer is the data edit, re-solved."
    models = ("factory_planning",)
    kpi_keys = {"factory_planning": ["profit", "holding_cost", "sales_contribution"]}

    def __init__(self, model_name: str = "factory_planning", solver: str = "highs"):
        if model_name not in self.models:
            raise ValueError(f"{self.name} has no templates for {model_name!r} yet")
        self.model = get_model(model_name)
        self.solver = solver
        self.data = self.model.load_data()

    def generate(self, n: int, seed: int = 0, combo_share: float = 0.15) -> list[Task]:
        rng = random.Random(seed)
        tasks: list[Task] = []
        seen_hashes: set[str] = set()
        names = list(SINGLE_TEMPLATES)
        attempts = 0
        while len(tasks) < n and attempts < 50 * n:
            attempts += 1
            if rng.random() < combo_share:
                tname, template = "combo", t_combo
            else:
                tname = names[len(tasks) % len(names)] if rng.random() < 0.6 else rng.choice(names)
                template = SINGLE_TEMPLATES[tname]
            question, scenario, slots, difficulty = template(rng, self.data)
            ref = solve_scenario(self.model, scenario, self.data, solver=self.solver, keep_decisions=False)
            if ref.status not in ("optimal", "infeasible"):
                continue
            if ref.scenario_hash in seen_hashes:
                continue
            # a task must move the scored KPIs by clearly more than the scoring tolerance, or "no change"
            # would be an accepted answer
            if ref.status == "optimal" and compare_results(self.base_result.to_dict(), ref.to_dict(),
                                                           self.kpi_keys[self.model.name], rel_tol=3 * REL_TOL).match:
                continue
            seen_hashes.add(ref.scenario_hash)
            tid = f"{self.model.name}-{self.name}-{seed:03d}-{len(tasks):04d}"
            tasks.append(Task(id=tid, family=self.name, model=self.model.name, question=question,
                              scenario=scenario, reference=ref.to_dict(),
                              kpi_keys=self.kpi_keys[self.model.name], difficulty=difficulty,
                              template=tname, slots=slots, split=split_for(tid),
                              tags=[tname, difficulty, ref.status]))
        return tasks

    @property
    def base_result(self):
        if not hasattr(self, "_base"):
            self._base = solve_scenario(self.model, {"version": "0.1", "data_changes": []}, self.data,
                                        solver=self.solver, keep_decisions=False)
        return self._base
