"""Food Supply — least-cost food baskets for beneficiary camps in Syria, bought from suppliers and shipped
over a road network (LP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``food_program/food_supply.ipynb`` (Apache-2.0), a World Food Programme case motivated by Peters et al.
(INFORMS Journal on Optimization, 2021; INFORMS Journal on Applied Analytics, 2022). Only the published
data values (the six CSV files in ``food_program/data``) are reused; the code here is new.

For every beneficiary camp the model picks a daily ration per person (how much of each food) whose nutrient
content lies between each nutrient's minimum requirement and ``max_nutrient_factor`` times that minimum.
Every food is bought at supplier cities (at the supplier's local price when the data has one, otherwise at
the food's international price) and shipped along directed road links to the camps; the flow of each food
is conserved at every city. The objective is purchase cost plus transport cost.

Quantities follow the source data: nutrient contents are per 100 g and requirements per person per day, so
a ration is in 100-g units per person per day and purchases and shipments are in 100-g units per day.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


def _slug(value: Any) -> str:
    """Readable name fragment for a PuLP name (letters, digits and single underscores)."""
    return re.sub(r"[^0-9A-Za-z]+", "_", str(value)).strip("_") or "x"


def _linear(pulp, terms, keep_zeros: bool = False):
    """``LpAffineExpression`` from ``(variable, coefficient)`` pairs, adding up repeated variables (PuLP's own
    constructor keeps only the last pair of a repeated variable). Zero coefficients are dropped unless
    ``keep_zeros``."""
    coef: dict = {}
    for var, a in terms:
        coef[var] = coef.get(var, 0) + a
    return pulp.LpAffineExpression({v: a for v, a in coef.items() if keep_zeros or a != 0})


class _Names:
    """Unique readable names for variables and constraints (``ration_Beans_Ar_Raqqa``); a clash gets a suffix."""

    def __init__(self) -> None:
        self.used: set[str] = set()

    def __call__(self, *parts: Any) -> str:
        base = "_".join(_slug(p) for p in parts)
        name, k = base, 1
        while name in self.used:
            k += 1
            name = f"{base}_{k}"
        self.used.add(name)
        return name


class FoodSupply(BaseModel):
    name = "food_supply"
    title = "Food Supply (World Food Programme, Syria)"
    domain = "supply_chain_logistics"
    sense = "min"
    problem_type = "LP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="food_program/food_supply.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/food_program/food_supply.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook's six CSV files (food_program/data); model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("suppliers", "camps", "arcs", "foods", "nutrients", "food_nutrients", "local_prices")
    HAS_PARAMS = True
    MEASURE_DIMS = {
        "ration": ("food", "camp"),
        "purchase": ("food", "supplier"),
        "flow": ("food", "from_city", "to_city"),
    }
    # KPIs that are unique at the optimum (checked by min/max over the optimal face, at the base and over about
    # 300 generated what-ifs); the scorer compares these. Per-camp rations and per-supplier purchases can tie.
    SCORING_KPIS = ["total_cost", "procurement_cost", "transport_cost", "food_bought"]

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]) -> dict[str, Any]:
        """Sets and coefficients from the tables. Rows naming an unknown food or nutrient are ignored; a city is
        any supplier, camp or end of a link."""

        def unique(values):
            return list(dict.fromkeys(values))

        foods = unique(r["food"] for r in data["foods"])
        known_food = set(foods)
        nutrients = unique(r["nutrient"] for r in data["nutrients"])
        known_nutrient = set(nutrients)
        suppliers = unique(r["supplier"] for r in data["suppliers"])
        camps = unique(r["camp"] for r in data["camps"])
        arcs = unique((r["from_city"], r["to_city"]) for r in data["arcs"])
        cities = unique([*suppliers, *camps, *(c for arc in arcs for c in arc)])

        beneficiaries = {r["camp"]: r["beneficiaries"] or 0 for r in data["camps"]}
        transport = {(r["from_city"], r["to_city"]): r["transport_cost"] or 0 for r in data["arcs"]}
        minimum = {r["nutrient"]: r["min_per_person"] or 0 for r in data["nutrients"]}
        content = {(r["food"], r["nutrient"]): r["amount"] for r in data["food_nutrients"]
                   if r["food"] in known_food and r["nutrient"] in known_nutrient and r["amount"]}
        international = {r["food"]: r["international_price"] for r in data["foods"]
                         if r["international_price"] is not None}
        local = {(r["supplier"], r["food"]): r["price"] for r in data["local_prices"] if r["price"] is not None}
        # purchase price: the supplier's local price, else the international price (None = cannot be bought there)
        price = {(i, f): local.get((i, f), international.get(f)) for i in suppliers for f in foods}

        into = {c: [] for c in cities}
        out_of = {c: [] for c in cities}
        for a, b in arcs:
            out_of[a].append(b)
            into[b].append(a)
        return {
            "foods": foods, "nutrients": nutrients, "suppliers": suppliers, "camps": camps, "arcs": arcs,
            "cities": cities, "beneficiaries": beneficiaries, "transport": transport, "minimum": minimum,
            "content": content, "price": price, "into": into, "out_of": out_of,
        }

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        ix = self._index(data)
        P = data["params"]
        foods, camps, suppliers, arcs = ix["foods"], ix["camps"], ix["suppliers"], ix["arcs"]
        price, transport, content = ix["price"], ix["transport"], ix["content"]
        name = _Names()

        prob = pulp.LpProblem("food_supply", pulp.LpMinimize)
        # ration per person per day in each camp (100-g units)
        ration = {(f, j): pulp.LpVariable(name("ration", f, j), lowBound=0) for f in foods for j in camps}
        # food bought at each supplier; a food with no price at a supplier cannot be bought there
        purchase = {(f, i): pulp.LpVariable(name("purchase", f, i), lowBound=0,
                                            upBound=P["max_purchase"] if price[i, f] is not None else 0)
                    for f in foods for i in suppliers}
        # food shipped on each directed link
        flow = {(f, a, b): pulp.LpVariable(name("flow", f, a, b), lowBound=0) for f in foods for a, b in arcs}
        # nutrient intake above the minimum: the original's ranged rows m <= intake <= factor * m are kept as
        # intake - surplus = m with 0 <= surplus <= (factor - 1) * m, which is how Gurobi stores a ranged row
        factor = P["max_nutrient_factor"]
        surplus = {(u, j): pulp.LpVariable(name("nutrient_surplus", u, j), lowBound=0,
                                           upBound=(factor - 1) * ix["minimum"][u])
                   for u in ix["nutrients"] for j in camps}

        # Objective: purchase cost + transport cost. Zero costs are kept as explicit terms, so every link's
        # variables stay in the model even when they appear in no row (a link from a city to itself).
        prob += _linear(pulp, [(purchase[f, i], price[i, f]) for f in foods for i in suppliers
                               if price[i, f] is not None]
                        + [(flow[f, a, b], transport[a, b]) for f in foods for a, b in arcs],
                        keep_zeros=True), "total_cost"

        # Nutrition: per camp and nutrient, intake per person between the minimum and factor * minimum
        for u in ix["nutrients"]:
            for j in camps:
                terms = [(ration[f, j], content[f, u]) for f in foods if (f, u) in content]
                prob += _linear(pulp, terms + [(surplus[u, j], -1)]) == ix["minimum"][u], name("nutrition", u, j)

        # Flow balance per food and city: inflow - outflow = food handed out at a camp - food bought at a
        # supplier (a city that is both does both; a city that is neither passes food on). A link from a city to
        # itself enters and leaves the same row, so it nets out of it.
        is_supplier, is_camp = set(suppliers), set(camps)
        for f in foods:
            for c in ix["cities"]:
                terms = [(flow[f, a, c], 1) for a in ix["into"][c]] + [(flow[f, c, b], -1) for b in ix["out_of"][c]]
                if c in is_camp:
                    terms.append((ration[f, c], -ix["beneficiaries"][c]))
                if c in is_supplier:
                    terms.append((purchase[f, c], 1))
                prob += _linear(pulp, terms) == 0, name("balance", f, c)

        prob._wig = {  # handles for kpis() and the DSL, keys aligned with MEASURE_DIMS
            "ration": ration, "purchase": purchase,
            "flow": {k: v for k, v in flow.items() if k[1] != k[2]},
            "local_flow": {k: v for k, v in flow.items() if k[1] == k[2]},  # inert self-links, not a measure
            "nutrient_surplus": surplus,  # range slacks of the nutrition rows, not a measure
        }
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        ix = self._index(data)
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        procurement = sum(ix["price"][i, f] * val(x) for (f, i), x in v["purchase"].items()
                          if ix["price"][i, f] is not None)
        transport = sum(ix["transport"][a, b] * val(x) for part in ("flow", "local_flow")
                        for (f, a, b), x in v[part].items())
        people = sum(ix["beneficiaries"][j] for j in ix["camps"])
        bought = sum(val(x) for x in v["purchase"].values())
        by_supplier = {i: 0.0 for i in ix["suppliers"]}
        for (f, i), x in v["purchase"].items():
            by_supplier[i] += val(x)
        ration = {j: 0.0 for j in ix["camps"]}
        for (f, j), x in v["ration"].items():
            ration[j] += val(x)
        return {
            "total_cost": round(procurement + transport, 2),
            "procurement_cost": round(procurement, 2),
            "transport_cost": round(transport, 2),
            "cost_per_beneficiary": round((procurement + transport) / people, 4) if people else None,
            "food_bought": round(bought, 2),
            "food_bought_by_supplier": {i: round(q, 2) for i, q in by_supplier.items()},
            "ration_per_person": {j: round(q, 4) for j, q in ration.items()},
        }
