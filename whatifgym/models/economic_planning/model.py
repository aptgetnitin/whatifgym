"""Economic Planning — dynamic Leontief input-output model with capacity building (LP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``economic_planning/economic_planning.ipynb`` (Apache-2.0), itself based on H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 9. Only the published data values
are reused; the code here is new.

``build`` is the notebook's dynamic model (maximise employment over the planning years). The notebook's static
model is only used for the steady-state production levels, which are solved here as a small linear system.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


def _steady_state(industries: list, io: dict, demand: dict) -> dict:
    """Solve (I - A) x = demand by Gauss-Jordan elimination with partial pivoting (the static Leontief model)."""
    n = len(industries)
    rows = [[(1.0 if i == j else 0.0) - io.get((industries[i], industries[j]), 0.0) for j in range(n)]
            + [float(demand[industries[i]])] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(rows[r][c]))
        if abs(rows[p][c]) < 1e-12:
            raise ValueError("input-output matrix is singular: no steady-state production exists")
        rows[c], rows[p] = rows[p], rows[c]
        for r in range(n):
            if r != c:
                f = rows[r][c] / rows[c][c]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[c])]
    return {industries[i]: rows[i][n] / rows[i][i] for i in range(n)}


class EconomicPlanning(BaseModel):
    name = "economic_planning"
    title = "Economic Planning (Williams, example 9)"
    domain = "revenue_resource_planning"
    sense = "max"
    problem_type = "LP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="economic_planning/economic_planning.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/economic_planning/economic_planning.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("industries", "input_output", "years")
    HAS_PARAMS = False
    MEASURE_DIMS = {
        "production": ("year", "industry"),
        "stock": ("year", "industry"),
        "extra_capacity": ("year", "industry"),
    }
    SCORING_KPIS = ["employment", "production_employment", "capacity_building_employment", "total_production",
                    "capacity_built", "final_capacity_by_industry"]  # unique at the optimum; production_by_year is not
    # Lead times (structure, not data): output of year t feeds production in t+1 and capacity built in t+2.
    PRODUCTION_LEAD = 1
    CAPACITY_LEAD = 2

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]):
        years = [r["year"] for r in sorted(data["years"], key=lambda r: r["order"])]
        ind = {r["industry"]: r for r in data["industries"]}
        io_out = {(r["supplier"], r["user"]): r["input_per_unit_output"] for r in data["input_output"]}
        io_cap = {(r["supplier"], r["user"]): r["input_per_unit_capacity"] for r in data["input_output"]}
        return years, list(ind), ind, io_out, io_cap

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        years, industries, ind, io_out, io_cap = self._index(data)
        plan, last = years[:-1], years[-1]  # the last year stands for the steady state beyond the horizon
        pos = {y: k for k, y in enumerate(years)}
        steady = _steady_state(industries, io_out, {i: ind[i]["external_demand"] for i in industries})

        prob = pulp.LpProblem("economic_planning", pulp.LpMaximize)
        # Nothing is produced in the first year (its output is the opening stock).
        production = {(y, i): pulp.LpVariable(f"production_{y}_{i}", lowBound=0, upBound=0 if pos[y] == 0 else None)
                      for y in years for i in industries}
        stock = {(y, i): pulp.LpVariable(f"stock_{y}_{i}", lowBound=0) for y in plan for i in industries}
        # Capacity can be built only from the third year (two-year lead time) and not in the steady-state year.
        extra = {(y, i): pulp.LpVariable(f"extra_capacity_{y}_{i}", lowBound=0,
                                         upBound=0 if pos[y] < self.CAPACITY_LEAD or y == last else None)
                 for y in years for i in industries}

        prob += (pulp.lpSum(ind[i]["labor_per_unit_output"] * production[y, i]
                            + ind[i]["labor_per_unit_capacity"] * extra[y, i] for y in plan for i in industries),
                 "employment")

        for k, y in enumerate(plan):
            nxt = years[k + self.PRODUCTION_LEAD]
            cap_year = years[k + self.CAPACITY_LEAD] if k + self.CAPACITY_LEAD < len(years) else None
            for i in industries:
                supply = ind[i]["initial_stock"] if k == 0 else production[y, i] + stock[plan[k - 1], i]
                use = pulp.lpSum(io_out.get((i, j), 0) * production[nxt, j] for j in industries)
                if cap_year is not None:
                    use += pulp.lpSum(io_cap.get((i, j), 0) * extra[cap_year, j] for j in industries)
                # Output available (opening stock in year 1) = inputs to next year's output and to capacity
                # completed two years on + external demand + closing stock
                prob += supply == use + ind[i]["external_demand"] + stock[y, i], f"balance_{y}_{i}"

        for i in industries:
            prob += production[last, i] >= steady[i], f"steady_production_{i}"
        for y in plan:
            for i in industries:
                prob += (production[y, i] - pulp.lpSum(extra[t, i] for t in plan if pos[t] <= pos[y])
                         <= ind[i]["initial_capacity"]), f"capacity_{y}_{i}"

        prob._wig = {"production": production, "stock": stock, "extra_capacity": extra}  # handles for kpis()
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        years, industries, ind, _, _ = self._index(data)
        plan = years[:-1]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        prod_labor = sum(ind[i]["labor_per_unit_output"] * val(v["production"][y, i]) for y in plan for i in industries)
        cap_labor = sum(ind[i]["labor_per_unit_capacity"] * val(v["extra_capacity"][y, i])
                        for y in plan for i in industries)
        return {
            "employment": round(prod_labor + cap_labor, 2),
            "production_employment": round(prod_labor, 2),
            "capacity_building_employment": round(cap_labor, 2),
            "total_production": round(sum(val(v["production"][y, i]) for y in plan for i in industries), 2),
            "capacity_built": round(sum(val(v["extra_capacity"][y, i]) for y in plan for i in industries), 2),
            "final_capacity_by_industry": {i: round(ind[i]["initial_capacity"]
                                                    + sum(val(v["extra_capacity"][y, i]) for y in plan), 2)
                                           for i in industries},
            "production_by_year": {y: round(sum(val(v["production"][y, i]) for i in industries), 2) for y in plan},
        }
