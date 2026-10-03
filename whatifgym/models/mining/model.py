"""Mining — multi-year mine operation and ore blending plan (MILP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example ``mining/mining.ipynb``
(Apache-2.0), itself based on H. P. Williams, *Model Building in Mathematical Programming*, 5th ed.,
example 7. Only the published data values are reused; the code here is new.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class Mining(BaseModel):
    name = "mining"
    title = "Mining operations and ore blending (Williams, example 7)"
    domain = "production_planning"
    sense = "max"
    problem_type = "MILP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="mining/mining.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/mining/mining.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("mines", "years")
    MEASURE_DIMS = {
        "extract": ("year", "mine"),
        "operate": ("year", "mine"),
        "open": ("year", "mine"),
        "blend": ("year",),
    }
    SCORING_KPIS = ["profit", "discounted_revenue", "discounted_royalties", "ore_sold_tons"]  # KPIs that are unique at the optimum; the scorer compares these

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]):
        years = [r["year"] for r in sorted(data["years"], key=lambda r: r["order"])]
        order = {r["year"]: r["order"] for r in data["years"]}
        target = {r["year"]: r["quality_target"] for r in data["years"]}
        mines = [r["mine"] for r in data["mines"]]
        royalty = {r["mine"]: r["royalty"] for r in data["mines"]}
        capacity = {r["mine"]: r["capacity"] for r in data["mines"]}
        quality = {r["mine"]: r["quality"] for r in data["mines"]}
        rate = data["params"]["discount_rate"]
        if 1 + rate <= 0:
            raise ValueError(f"discount_rate must be greater than -1, got {rate!r}")
        # Present-value factor: the year with order 1 is undiscounted, each later year one more period.
        discount = {y: (1 / (1 + rate)) ** (order[y] - 1) for y in years}
        return years, mines, target, royalty, capacity, quality, discount

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        years, mines, target, royalty, capacity, quality, discount = self._index(data)
        P = data["params"]

        prob = pulp.LpProblem("mining", pulp.LpMaximize)
        blend = {y: pulp.LpVariable(f"blend_{y}", lowBound=0) for y in years}
        extract = {(y, m): pulp.LpVariable(f"extract_{y}_{m}", lowBound=0) for y in years for m in mines}
        operate = {(y, m): pulp.LpVariable(f"operate_{y}_{m}", cat=pulp.LpBinary) for y in years for m in mines}
        is_open = {(y, m): pulp.LpVariable(f"open_{y}_{m}", cat=pulp.LpBinary) for y in years for m in mines}

        # Objective: discounted sales revenue minus discounted royalties on every mine kept open
        prob += (pulp.lpSum(P["price"] * discount[y] * blend[y] for y in years)
                 - pulp.lpSum(royalty[m] * discount[y] * is_open[y, m] for y in years for m in mines)), "npv_profit"

        # At most max_mines mines worked in any year
        for y in years:
            prob += pulp.lpSum(operate[y, m] for m in mines) <= P["max_mines"], f"max_operating_{y}"

        # The blend must hit the year's quality target (grades mix linearly by tonnage)
        for y in years:
            prob += pulp.lpSum(quality[m] * extract[y, m] for m in mines) == target[y] * blend[y], f"quality_{y}"

        # Tons blended and sold = tons extracted
        for y in years:
            prob += pulp.lpSum(extract[y, m] for m in mines) == blend[y], f"mass_balance_{y}"

        # A mine produces only when worked, up to its yearly limit
        for y in years:
            for m in mines:
                prob += extract[y, m] <= capacity[m] * operate[y, m], f"capacity_{y}_{m}"

        # A mine can be worked only while it is open (royalty paid)
        for y in years:
            for m in mines:
                prob += operate[y, m] <= is_open[y, m], f"open_to_operate_{y}_{m}"

        # Once closed, a mine stays closed
        for prev, y in zip(years, years[1:]):
            for m in mines:
                prob += is_open[y, m] <= is_open[prev, m], f"stay_closed_{y}_{m}"

        prob._wig = {"extract": extract, "operate": operate, "open": is_open, "blend": blend}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        years, mines, target, royalty, capacity, quality, discount = self._index(data)
        P = data["params"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        ore = {y: val(v["blend"][y]) for y in years}
        extracted = {(y, m): val(v["extract"][y, m]) for y in years for m in mines}
        kept_open = {(y, m): val(v["open"][y, m]) > 0.5 for y in years for m in mines}
        revenue = sum(P["price"] * discount[y] * ore[y] for y in years)
        royalties = sum(royalty[m] * discount[y] for (y, m), is_open in kept_open.items() if is_open)
        # "worked" = actually producing; an idle mine may carry operate = 1 at no cost, so count tonnage instead
        worked = {y: sum(1 for m in mines if extracted[y, m] > 1e-6 * max(capacity[m], 1.0)) for y in years}
        utilisation = {}
        for m in mines:
            avail = capacity[m] * len(years)
            utilisation[m] = round(sum(extracted[y, m] for y in years) / avail, 4) if avail > 0 else None
        return {
            "profit": round(revenue - royalties, 2),
            "discounted_revenue": round(revenue, 2),
            "discounted_royalties": round(royalties, 2),
            "ore_sold_tons": round(sum(ore.values()), 1),
            "ore_sold_by_year": {y: round(ore[y], 1) for y in years},
            "mines_worked_by_year": worked,
            "years_open_by_mine": {m: sum(1 for y in years if kept_open[y, m]) for m in mines},
            "mine_utilisation": utilisation,
        }
