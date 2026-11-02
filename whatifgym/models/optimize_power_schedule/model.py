"""Optimize a power generation schedule — hourly unit commitment of Georgia's plants with health costs (MILP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``power_generation/optimize_power_schedule.ipynb`` (Apache-2.0). Only the published data values are reused
(small_plant_data/ and demand.csv for 1 July 2011); the code here is new.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class OptimizePowerSchedule(BaseModel):
    name = "optimize_power_schedule"
    title = "Power generation schedule, unit commitment with health costs (Gurobi modeling-examples)"
    domain = "energy_power"
    sense = "min"
    problem_type = "MILP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="power_generation/optimize_power_schedule.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/power_generation/optimize_power_schedule.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook's CSV files (small_plant_data, demand.csv); model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("hours", "plants", "fuels", "health_costs")
    HAS_PARAMS = False
    MEASURE_DIMS = {
        "output": ("plant", "hour"),
        "on": ("plant", "hour"),
        "start": ("plant", "hour"),
        "stop": ("plant", "hour"),
    }
    # Every KPI is unique at the optimum (min/max over optimal plans agree), but the runner-up plan is only 61.5
    # dearer (keeps OTHER COAL on in hour 13), inside the default 1e-4 MIP gap; it moves operating_cost,
    # plant_hours_on and GAS generation by more than the 1e-3 scoring tolerance, so only these three are scored.
    SCORING_KPIS = ["total_cost", "fuel_cost", "health_cost"]

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]) -> dict[str, Any]:
        hours = sorted(r["hour"] for r in data["hours"])
        if not hours:
            raise ValueError("optimize_power_schedule needs at least one hour")
        fuels = {r["fuel"]: r for r in data["fuels"]}
        plants = {r["plant"]: r for r in data["plants"]}
        for p, r in plants.items():
            if r["fuel"] not in fuels:
                raise ValueError(f"plant {p!r} burns fuel {r['fuel']!r}, which is not in the fuels table")
        health = {(r["plant"], r["hour"]): r["health_cost"] for r in data["health_costs"]}
        return {
            "hours": hours,
            "demand": {r["hour"]: r["demand_mwh"] for r in data["hours"]},
            "plants": list(plants),
            "plant": plants,
            "cost": {p: fuels[r["fuel"]] for p, r in plants.items()},       # per-fuel costs looked up per plant
            "health": lambda p, h: health.get((p, h), 0) or 0,              # a missing row means no health cost
        }

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        ix = self._index(data)
        hours, demand, plants, pl, cost, health = (ix[k] for k in ("hours", "demand", "plants", "plant", "cost",
                                                                    "health"))
        PH = [(p, h) for p in plants for h in hours]
        prev = dict(zip(hours[1:], hours[:-1]))  # the first hour has no predecessor (no initial state)

        prob = pulp.LpProblem("optimize_power_schedule", pulp.LpMinimize)
        output = {(p, h): pulp.LpVariable(f"output_{p}_{h}", lowBound=0) for p, h in PH}
        on = {(p, h): pulp.LpVariable(f"on_{p}_{h}", cat=pulp.LpBinary) for p, h in PH}
        start = {(p, h): pulp.LpVariable(f"start_{p}_{h}", cat=pulp.LpBinary) for p, h in PH}
        stop = {(p, h): pulp.LpVariable(f"stop_{p}_{h}", cat=pulp.LpBinary) for p, h in PH}

        # Fuel and health cost per MWh generated, operating cost per hour on, start-up and shut-down costs.
        prob += pulp.lpSum((cost[p]["fuel_cost"] + health(p, h)) * output[p, h]
                           + cost[p]["operating_cost"] * on[p, h]
                           + cost[p]["startup_cost"] * start[p, h]
                           + cost[p]["shutdown_cost"] * stop[p, h] for p, h in PH), "total_cost"

        for h in hours:
            prob += pulp.lpSum(output[p, h] for p in plants) == demand[h], f"demand_{h}"
        for p, h in PH:
            prob += output[p, h] >= pl[p]["min_output_fraction"] * pl[p]["capacity_mwh"] * on[p, h], \
                f"min_output_{p}_{h}"
        for p, h in PH:
            prob += output[p, h] <= pl[p]["capacity_mwh"] * on[p, h], f"max_output_{p}_{h}"
        for p, h in PH:
            if pl[p]["must_run"]:
                prob += output[p, h] >= pl[p]["min_output_fraction"] * pl[p]["capacity_mwh"], f"must_run_{p}_{h}"
        for p, h in PH:
            if h in prev:
                prob += output[p, h] - output[p, prev[h]] >= -pl[p]["ramp_fraction"] * pl[p]["capacity_mwh"], \
                    f"ramp_down_{p}_{h}"
        for p, h in PH:
            if h in prev:
                prob += output[p, h] - output[p, prev[h]] <= pl[p]["ramp_fraction"] * pl[p]["capacity_mwh"], \
                    f"ramp_up_{p}_{h}"
        for p, h in PH:
            prob += start[p, h] <= on[p, h], f"start_on_{p}_{h}"
        for p, h in PH:
            prob += stop[p, h] <= 1 - on[p, h], f"stop_off_{p}_{h}"
        for p, h in PH:
            if h in prev:
                prob += start[p, h] - stop[p, h] == on[p, h] - on[p, prev[h]], f"switch_{p}_{h}"

        prob._wig = {"output": output, "on": on, "start": start, "stop": stop}  # handles for kpis()
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        ix = self._index(data)
        hours, plants, cost, health = ix["hours"], ix["plants"], ix["cost"], ix["health"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        PH = [(p, h) for p in plants for h in hours]
        parts = {
            "fuel_cost": sum(cost[p]["fuel_cost"] * val(v["output"][p, h]) for p, h in PH),
            "health_cost": sum(health(p, h) * val(v["output"][p, h]) for p, h in PH),
            "operating_cost": sum(cost[p]["operating_cost"] * val(v["on"][p, h]) for p, h in PH),
            "startup_cost": sum(cost[p]["startup_cost"] * val(v["start"][p, h]) for p, h in PH),
            "shutdown_cost": sum(cost[p]["shutdown_cost"] * val(v["stop"][p, h]) for p, h in PH),
        }
        return {
            "total_cost": round(sum(parts.values()), 2),
            **{k: round(x, 2) for k, x in parts.items()},
            "generation_by_plant": {p: round(sum(val(v["output"][p, h]) for h in hours), 1) for p in plants},
            "plant_hours_on": {p: int(round(sum(val(v["on"][p, h]) for h in hours))) for p in plants},
        }
