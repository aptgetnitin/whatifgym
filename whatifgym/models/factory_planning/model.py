"""Factory Planning I — multi-period production, inventory and sales plan (LP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``factory_planning/factory_planning_1.ipynb`` (Apache-2.0), itself based on H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 3. Only the published data values
are reused; the code here is new.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class FactoryPlanning(BaseModel):
    name = "factory_planning"
    title = "Factory Planning I (Williams, example 3)"
    domain = "production_planning"
    sense = "max"
    problem_type = "LP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="factory_planning/factory_planning_1.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/factory_planning/factory_planning_1.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("months", "products", "machines", "process_hours", "downtime", "max_sales")

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]):
        months = [r["month"] for r in sorted(data["months"], key=lambda r: r["order"])]
        products = [r["product"] for r in data["products"]]
        profit = {r["product"]: r["profit_per_unit"] for r in data["products"]}
        installed = {r["machine"]: r["installed"] for r in data["machines"]}
        hours = {(r["machine"], r["product"]): r["hours_per_unit"] for r in data["process_hours"]}
        down = {(r["month"], r["machine"]): r["machines_down"] for r in data["downtime"]}
        max_sales = {(r["month"], r["product"]): r["max_sales"] for r in data["max_sales"]}
        return months, products, profit, installed, hours, down, max_sales

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        months, products, profit, installed, hours, down, max_sales = self._index(data)
        P = data["params"]

        prob = pulp.LpProblem("factory_planning", pulp.LpMaximize)
        make = {(m, p): pulp.LpVariable(f"make_{m}_{p}", lowBound=0) for m in months for p in products}
        store = {(m, p): pulp.LpVariable(f"store_{m}_{p}", lowBound=0, upBound=P["max_inventory"])
                 for m in months for p in products}
        sell = {(m, p): pulp.LpVariable(f"sell_{m}_{p}", lowBound=0, upBound=max_sales.get((m, p), 0))
                for m in months for p in products}

        # Objective: profit contribution of sales minus holding cost of stock
        prob += pulp.lpSum(profit[p] * sell[m, p] - P["holding_cost"] * store[m, p]
                           for m in months for p in products), "total_profit"

        # Inventory balance (initial stock is zero)
        for p in products:
            prob += make[months[0], p] == sell[months[0], p] + store[months[0], p], f"balance_{months[0]}_{p}"
            for prev, m in zip(months, months[1:]):
                prob += store[prev, p] + make[m, p] == sell[m, p] + store[m, p], f"balance_{m}_{p}"
            prob += store[months[-1], p] == P["store_target"], f"end_stock_{p}"

        # Machine capacity per month, net of machines down for maintenance
        for mc in installed:
            for m in months:
                available = P["hours_per_month"] * (installed[mc] - down.get((m, mc), 0))
                prob += pulp.lpSum(hours[mc, p] * make[m, p] for p in products if (mc, p) in hours) <= available, \
                    f"capacity_{m}_{mc}"

        prob._wig = {"make": make, "store": store, "sell": sell}  # handles for kpis()
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        months, products, profit, installed, hours, down, max_sales = self._index(data)
        P = data["params"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        total_sales = sum(val(v["sell"][m, p]) for m in months for p in products)
        total_make = sum(val(v["make"][m, p]) for m in months for p in products)
        revenue = sum(profit[p] * val(v["sell"][m, p]) for m in months for p in products)
        holding = sum(P["holding_cost"] * val(v["store"][m, p]) for m in months for p in products)
        utilisation = {}
        for mc in installed:
            used = sum(hours[mc, p] * val(v["make"][m, p]) for m in months for p in products if (mc, p) in hours)
            avail = sum(P["hours_per_month"] * (installed[mc] - down.get((m, mc), 0)) for m in months)
            utilisation[mc] = round(used / avail, 4) if avail else None
        demand = sum(max_sales.values())
        return {
            "profit": round(revenue - holding, 2),
            "sales_contribution": round(revenue, 2),
            "holding_cost": round(holding, 2),
            "units_sold": round(total_sales, 1),
            "units_made": round(total_make, 1),
            "demand_fill_rate": round(total_sales / demand, 4) if demand else None,
            "machine_utilisation": utilisation,
            "units_sold_by_product": {p: round(sum(val(v["sell"][m, p]) for m in months), 1) for p in products},
        }
