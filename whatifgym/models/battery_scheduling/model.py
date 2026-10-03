"""Battery Scheduling, storage variant 'S' — one-day price arbitrage with a battery (LP).

Clean-room re-implementation in PuLP of the storage ("S") variant of the public Gurobi modeling example
``battery_scheduling/battery_scheduling.ipynb`` (Apache-2.0). Only the published data values are reused; the
code here is new. The notebook's other two variants (load and PV without a battery, and load, PV and battery
with a nonlinear cycling cost) are not ported.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


def _tag(value: Any) -> str:
    """A key value as a fragment that is safe inside a PuLP / LP-file name (``00-01`` -> ``00_01``)."""
    return "".join(ch if ch.isalnum() else "_" for ch in str(value))


class BatteryScheduling(BaseModel):
    name = "battery_scheduling"
    title = "Battery Scheduling, price arbitrage (Gurobi modeling-examples, storage variant S)"
    domain = "energy_power"
    sense = "max"
    problem_type = "LP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="battery_scheduling/battery_scheduling.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/battery_scheduling/battery_scheduling.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook (default variant 'S'); model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("hours",)
    HAS_PARAMS = True
    MEASURE_DIMS = {"charge": ("hour",), "discharge": ("hour",), "soc": ("hour",)}
    # KPIs that are unique at the optimum; the scorer compares these. They are the profit and the daily totals: the
    # hourly plan has alternative optima (equal prices in several hours), so no hourly KPI is scored.
    SCORING_KPIS = ["profit", "export_revenue", "import_cost", "energy_charged_kwh", "energy_discharged_kwh"]

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]) -> dict[str, Any]:
        rows = sorted(data["hours"], key=lambda r: r["order"])
        if not rows:
            raise ValueError("battery_scheduling needs at least one hour")
        P = data["params"]

        def num(name: str) -> float:
            value = P.get(name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be a number, got {value!r}")
            return float(value)

        eff_charge, eff_discharge = num("charge_efficiency"), num("discharge_efficiency")
        for name, eta in (("charge_efficiency", eff_charge), ("discharge_efficiency", eff_discharge)):
            if not 0 < eta <= 1:  # an efficiency of 0 divides by zero, above 1 the battery would create energy
                raise ValueError(f"{name} must be in (0, 1], got {eta!r}")
        return {
            "hours": [r["hour"] for r in rows],                        # in time order
            "step": {r["hour"]: r["step_hours"] for r in rows},        # length of each step in hours
            "buy": {r["hour"]: r["import_price"] for r in rows},       # price paid per kWh imported (charging)
            "sell": {r["hour"]: r["export_price"] for r in rows},      # price received per kWh exported (discharging)
            "capacity": num("energy_capacity_kwh"),
            "max_charge": num("max_charge_kw"),
            "max_discharge": num("max_discharge_kw"),
            "eff_charge": eff_charge,
            "eff_discharge": eff_discharge,
            "soc_start": num("initial_soc_kwh"),
            "soc_end": num("terminal_soc_kwh"),
        }

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        ix = self._index(data)
        hours, step, buy, sell = ix["hours"], ix["step"], ix["buy"], ix["sell"]

        prob = pulp.LpProblem("battery_scheduling", pulp.LpMaximize)
        charge = {h: pulp.LpVariable(f"charge_{_tag(h)}", lowBound=0, upBound=ix["max_charge"]) for h in hours}
        discharge = {h: pulp.LpVariable(f"discharge_{_tag(h)}", lowBound=0, upBound=ix["max_discharge"]) for h in hours}
        soc = {h: pulp.LpVariable(f"soc_{_tag(h)}", lowBound=0, upBound=ix["capacity"]) for h in hours}

        # Objective: energy sold to the grid while discharging, minus energy bought from the grid while charging
        prob += pulp.lpSum(step[h] * (sell[h] * discharge[h] - buy[h] * charge[h]) for h in hours), "profit"

        # Stored energy after an hour = stored before + energy that survives charging - energy taken out of the cells
        # to deliver the discharge (the cells give up more than the grid receives). The day starts at initial_soc_kwh.
        before = ix["soc_start"]
        for h in hours:
            prob += (soc[h] == before + ix["eff_charge"] * step[h] * charge[h]
                     - step[h] / ix["eff_discharge"] * discharge[h]), f"soc_balance_{_tag(h)}"
            before = soc[h]

        # The battery must end the day with at least the required charge
        prob += soc[hours[-1]] >= ix["soc_end"], "terminal_soc"

        prob._wig = {"charge": charge, "discharge": discharge, "soc": soc}  # handles for kpis()
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        ix = self._index(data)
        hours, step, buy, sell = ix["hours"], ix["step"], ix["buy"], ix["sell"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731

        charged = sum(step[h] * val(v["charge"][h]) for h in hours)        # kWh bought from the grid
        discharged = sum(step[h] * val(v["discharge"][h]) for h in hours)  # kWh sold to the grid
        revenue = sum(step[h] * sell[h] * val(v["discharge"][h]) for h in hours)
        cost = sum(step[h] * buy[h] * val(v["charge"][h]) for h in hours)
        # Energy lost in the charger and the inverter: bought + initial store = sold + final store + losses
        losses = (1 - ix["eff_charge"]) * charged + (1 / ix["eff_discharge"] - 1) * discharged
        cycles = discharged / ix["eff_discharge"] / ix["capacity"] if ix["capacity"] else None
        return {
            "profit": round(revenue - cost, 6),
            "export_revenue": round(revenue, 6),
            "import_cost": round(cost, 6),
            "energy_charged_kwh": round(charged, 6),
            "energy_discharged_kwh": round(discharged, 6),
            "conversion_losses_kwh": round(losses, 6),
            "full_cycles": round(cycles, 6) if cycles is not None else None,
            "peak_soc_kwh": round(max(val(v["soc"][h]) for h in hours), 6),
            "charge_kw_by_hour": {h: round(val(v["charge"][h]), 6) for h in hours if val(v["charge"][h]) > 1e-9},
            "discharge_kw_by_hour": {h: round(val(v["discharge"][h]), 6) for h in hours if val(v["discharge"][h]) > 1e-9},
        }
