"""Factory Planning II — production, inventory, sales and maintenance-scheduling plan (MILP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``factory_planning/factory_planning_2.ipynb`` (Apache-2.0), itself based on H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 4. It is Factory Planning I with the fixed
maintenance calendar replaced by integer decisions: how many machines of each type to take down in each
month, so that every machine type receives its required number of maintenance slots over the horizon.
Only the published data values are reused; the code here is new.
"""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from ...base import BaseModel, Source


class FactoryPlanning2(BaseModel):
    name = "factory_planning_2"
    title = "Factory Planning II (Williams, example 4)"
    domain = "production_planning"
    sense = "max"
    problem_type = "MILP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="factory_planning/factory_planning_2.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/factory_planning/factory_planning_2.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("months", "products", "machines", "maintenance", "process_hours", "max_sales")
    MEASURE_DIMS = {
        "make": ("month", "product"),
        "store": ("month", "product"),
        "sell": ("month", "product"),
        "repair": ("month", "machine"),
    }
    SCORING_KPIS = ["profit", "sales_contribution", "holding_cost"]  # KPIs that are unique at the optimum; the scorer compares these

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]) -> SimpleNamespace:
        """Index sets and lookup dicts from the records (missing rows mean zero / not needed)."""
        return SimpleNamespace(
            months=[r["month"] for r in sorted(data["months"], key=lambda r: r["order"])],
            products=[r["product"] for r in data["products"]],
            machines=[r["machine"] for r in data["machines"]],
            profit={r["product"]: r["profit_per_unit"] for r in data["products"]},
            installed={r["machine"]: r["installed"] for r in data["machines"]},
            to_maintain={r["machine"]: r["machines_to_maintain"] for r in data["maintenance"]},
            hours={(r["machine"], r["product"]): r["hours_per_unit"] for r in data["process_hours"]},
            max_sales={(r["month"], r["product"]): r["max_sales"] for r in data["max_sales"]},
        )

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        ix = self._index(data)
        P = data["params"]
        months, products, machines = ix.months, ix.products, ix.machines

        prob = pulp.LpProblem("factory_planning_2", pulp.LpMaximize)
        make = {(m, p): pulp.LpVariable(f"make_{m}_{p}", lowBound=0) for m in months for p in products}
        store = {(m, p): pulp.LpVariable(f"store_{m}_{p}", lowBound=0, upBound=P["max_inventory"])
                 for m in months for p in products}
        sell = {(m, p): pulp.LpVariable(f"sell_{m}_{p}", lowBound=0, upBound=ix.max_sales.get((m, p), 0))
                for m in months for p in products}
        # Machines of each type taken down for maintenance in each month (general integer).
        repair = {(m, mc): pulp.LpVariable(f"repair_{m}_{mc}", lowBound=0, upBound=ix.to_maintain.get(mc, 0),
                                           cat=pulp.LpInteger)
                  for m in months for mc in machines}

        # Objective: profit contribution of sales minus holding cost of stock
        prob += pulp.lpSum(ix.profit[p] * sell[m, p] - P["holding_cost"] * store[m, p]
                           for m in months for p in products), "total_profit"

        # Inventory balance (opening stock is zero) and the closing-stock target
        first, last = months[0], months[-1]
        for p in products:
            prob += make[first, p] == sell[first, p] + store[first, p], f"balance_{first}_{p}"
            for prev, m in zip(months, months[1:]):
                prob += store[prev, p] + make[m, p] == sell[m, p] + store[m, p], f"balance_{m}_{p}"
            prob += store[last, p] == P["store_target"], f"end_stock_{p}"

        # Machine-hour capacity per type and month: only machines not down for maintenance can run
        for mc in machines:
            for m in months:
                used = pulp.lpSum(ix.hours[mc, p] * make[m, p] for p in products if (mc, p) in ix.hours)
                prob += used <= P["hours_per_month"] * (ix.installed[mc] - repair[m, mc]), f"capacity_{m}_{mc}"

        # Maintenance requirement: each type gets exactly its required number of machine-months of maintenance
        for mc in machines:
            prob += pulp.lpSum(repair[m, mc] for m in months) == ix.to_maintain.get(mc, 0), f"maintenance_{mc}"

        prob._wig = {"make": make, "store": store, "sell": sell, "repair": repair}  # handles for kpis() / DSL
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        ix = self._index(data)
        P = data["params"]
        months, products, machines = ix.months, ix.products, ix.machines
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731

        revenue = sum(ix.profit[p] * val(v["sell"][m, p]) for m in months for p in products)
        holding = sum(P["holding_cost"] * val(v["store"][m, p]) for m in months for p in products)
        total_sales = sum(val(v["sell"][m, p]) for m in months for p in products)
        down = {(m, mc): int(round(val(v["repair"][m, mc]))) for m in months for mc in machines}

        utilisation = {}
        for mc in machines:
            used = sum(ix.hours[mc, p] * val(v["make"][m, p])
                       for m in months for p in products if (mc, p) in ix.hours)
            avail = sum(P["hours_per_month"] * (ix.installed[mc] - down[m, mc]) for m in months)
            utilisation[mc] = round(used / avail, 4) if avail else None

        demand = sum(ix.max_sales.get((m, p), 0) for m in months for p in products)
        return {
            "profit": round(revenue - holding, 2),
            "sales_contribution": round(revenue, 2),
            "holding_cost": round(holding, 2),
            "units_sold": round(total_sales, 1),
            "demand_fill_rate": round(total_sales / demand, 4) if demand else None,
            "machine_utilisation": utilisation,
            "units_sold_by_product": {p: round(sum(val(v["sell"][m, p]) for m in months), 1) for p in products},
            # machine type -> {month: machines down}; only months with maintenance are listed
            "maintenance_plan": {mc: {m: down[m, mc] for m in months if down[m, mc]} for mc in machines},
        }
