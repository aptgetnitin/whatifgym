"""Food Manufacture I — six-month raw-oil purchasing, storage and blending plan (LP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``food_manufacturing/food_manufacture_1.ipynb`` (Apache-2.0), itself based on H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 1. Only the published data values
are reused; the code here is new.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class FoodManufacture(BaseModel):
    name = "food_manufacture"
    title = "Food Manufacture I (Williams, example 1)"
    domain = "production_planning"
    sense = "max"
    problem_type = "LP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="food_manufacturing/food_manufacture_1.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/food_manufacturing/food_manufacture_1.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("months", "oils", "purchase_prices")
    MEASURE_DIMS = {
        "buy": ("month", "oil"),
        "consume": ("month", "oil"),
        "store": ("month", "oil"),
        "produce": ("month",),
    }
    SCORING_KPIS = ["profit", "revenue", "food_produced"]  # KPIs that are unique at the optimum; the scorer compares these
    # Refining lines (structure, not data): oil category -> parameter holding that line's monthly capacity.
    REFINING_LINES = {"veg": "veg_refining_capacity", "nonveg": "nonveg_refining_capacity"}

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]):
        months = [r["month"] for r in sorted(data["months"], key=lambda r: r["order"])]
        oils = [r["oil"] for r in data["oils"]]
        category = {r["oil"]: r["category"] for r in data["oils"]}
        hardness = {r["oil"]: r["hardness"] for r in data["oils"]}
        price = {(r["month"], r["oil"]): r["price"] for r in data["purchase_prices"]}
        return months, oils, category, hardness, price

    def _lines(self, oils: list, category: dict) -> dict[str, list]:
        """Oils refined on each line; a line with no oils is left out (no capacity row for it)."""
        out = {}
        for cat in self.REFINING_LINES:
            members = [o for o in oils if category[o] == cat]
            if members:
                out[cat] = members
        return out

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        months, oils, category, hardness, price = self._index(data)
        P = data["params"]
        first, last = months[0], months[-1]

        prob = pulp.LpProblem("food_manufacture", pulp.LpMaximize)
        produce = {m: pulp.LpVariable(f"produce_{m}", lowBound=0) for m in months}
        # No purchase-price row for (month, oil) means the oil cannot be bought that month.
        buy = {(m, o): pulp.LpVariable(f"buy_{m}_{o}", lowBound=0, upBound=None if (m, o) in price else 0)
               for m in months for o in oils}
        # An oil whose category has no refining line cannot be refined.
        consume = {(m, o): pulp.LpVariable(f"consume_{m}_{o}", lowBound=0,
                                           upBound=None if category[o] in self.REFINING_LINES else 0)
                   for m in months for o in oils}
        store = {(m, o): pulp.LpVariable(f"store_{m}_{o}", lowBound=0, upBound=P["storage_capacity"])
                 for m in months for o in oils}

        # Objective: sales of the blended product minus raw-oil purchases minus month-end storage cost
        prob += (P["product_price"] * pulp.lpSum(produce.values())
                 - pulp.lpSum(price[m, o] * buy[m, o] for (m, o) in buy if (m, o) in price)
                 - P["holding_cost"] * pulp.lpSum(store.values())), "profit"

        for o in oils:
            # Stock balance: opening stock + purchases = oil refined + closing stock
            prob += P["initial_stock"] + buy[first, o] == consume[first, o] + store[first, o], f"initial_balance_{o}"
            for prev, m in zip(months, months[1:]):
                prob += store[prev, o] + buy[m, o] == consume[m, o] + store[m, o], f"balance_{m}_{o}"
            # Horizon closure: the notebook's balance family also holds a first-month row that wraps the last
            # month's stock into the first month. Written with this right-hand side (0 in the notebook data, so
            # the row is identical there) it is implied by initial_balance + end_stock for any data.
            prob += (store[last, o] + buy[first, o] - consume[first, o] - store[first, o]
                     == P["final_stock"] - P["initial_stock"]), f"horizon_closure_{o}"
            # End-of-horizon stock target
            prob += store[last, o] == P["final_stock"], f"end_stock_{o}"

        # Refining capacity per line and month
        for cat, members in self._lines(oils, category).items():
            for m in months:
                prob += pulp.lpSum(consume[m, o] for o in members) <= P[self.REFINING_LINES[cat]], \
                    f"refining_{cat}_{m}"

        for m in months:
            # Hardness of the blend (blends linearly) within bounds
            blend_hardness = pulp.lpSum(hardness[o] * consume[m, o] for o in oils)
            prob += blend_hardness >= P["min_hardness"] * produce[m], f"hardness_min_{m}"
            prob += blend_hardness <= P["max_hardness"] * produce[m], f"hardness_max_{m}"
            # No refining loss: oil refined = food produced
            prob += pulp.lpSum(consume[m, o] for o in oils) == produce[m], f"mass_balance_{m}"

        prob._wig = {"buy": buy, "consume": consume, "store": store, "produce": produce}  # handles for kpis()
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        months, oils, category, hardness, price = self._index(data)
        P = data["params"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        produced = sum(val(v["produce"][m]) for m in months)
        bought = sum(val(v["buy"][m, o]) for m in months for o in oils)
        revenue = P["product_price"] * produced
        purchase = sum(price[m, o] * val(v["buy"][m, o]) for m in months for o in oils if (m, o) in price)
        holding = P["holding_cost"] * sum(val(v["store"][m, o]) for m in months for o in oils)
        utilisation = {}
        for cat, members in self._lines(oils, category).items():
            avail = P[self.REFINING_LINES[cat]] * len(months)
            used = sum(val(v["consume"][m, o]) for m in months for o in members)
            utilisation[cat] = round(used / avail, 4) if avail else None
        return {
            "profit": round(revenue - purchase - holding, 2),
            "revenue": round(revenue, 2),
            "purchase_cost": round(purchase, 2),
            "holding_cost": round(holding, 2),
            "food_produced": round(produced, 1),
            "oil_bought": round(bought, 1),
            "refining_utilisation": utilisation,
            "food_produced_by_month": {m: round(val(v["produce"][m]), 1) for m in months},
        }
