"""Electrical Power Generation 2 — one-day unit commitment of thermal and pumped-storage hydro units (MILP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``electrical_power_generation/electrical_power_2.ipynb`` (Apache-2.0), itself based on H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 16 (the hydro extension). Only the
published data values are reused; the code here is new.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


def _tag(value: Any) -> str:
    """A key value as a fragment that is safe inside a PuLP / LP-file name (``00-06`` -> ``00_06``)."""
    return "".join(ch if ch.isalnum() else "_" for ch in str(value))


class PowerGenerationHydro(BaseModel):
    name = "power_generation_hydro"
    title = "Electrical Power Generation 2, thermal plus hydro (Williams, example 16)"
    domain = "energy_power"
    sense = "min"
    problem_type = "MILP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="electrical_power_generation/electrical_power_2.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/electrical_power_generation/electrical_power_2.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("periods", "thermal_types", "hydro_units")
    HAS_PARAMS = True
    MEASURE_DIMS = {
        "ngen": ("period", "type"),
        "output": ("period", "type"),
        "nstart": ("period", "type"),
        "hydro_on": ("period", "hydro"),
        "hydro_start": ("period", "hydro"),
        "pump": ("period",),
        "reservoir_level": ("period",),
    }
    SCORING_KPIS = ["total_cost"]  # KPIs that are unique at the optimum; the scorer compares these

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]) -> dict[str, Any]:
        rows = sorted(data["periods"], key=lambda r: r["order"])
        if not rows:
            raise ValueError("power_generation_hydro needs at least one period")
        return {
            "periods": [r["period"] for r in rows],                      # in time order; the day is a cycle
            "hours": {r["period"]: r["hours"] for r in rows},
            "demand": {r["period"]: r["demand_mw"] for r in rows},
            "types": [r["type"] for r in data["thermal_types"]],
            "thermal": {r["type"]: r for r in data["thermal_types"]},
            "hydros": [r["hydro"] for r in data["hydro_units"]],
            "hydro": {r["hydro"]: r for r in data["hydro_units"]},
        }

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        ix = self._index(data)
        periods, hours, demand = ix["periods"], ix["hours"], ix["demand"]
        types, th, hydros, hy = ix["types"], ix["thermal"], ix["hydros"], ix["hydro"]
        P = data["params"]
        mwh_per_m = P["pump_mwh_per_m"]
        if not isinstance(mwh_per_m, (int, float)) or mwh_per_m <= 0:
            raise ValueError(f"pump_mwh_per_m must be a positive number, got {mwh_per_m!r}")

        PT = [(p, t) for p in periods for t in types]
        PH = [(p, h) for p in periods for h in hydros]

        prob = pulp.LpProblem("power_generation_hydro", pulp.LpMinimize)
        ngen = {(p, t): pulp.LpVariable(f"ngen_{_tag(p)}_{_tag(t)}", lowBound=0, cat=pulp.LpInteger) for p, t in PT}
        nstart = {(p, t): pulp.LpVariable(f"nstart_{_tag(p)}_{_tag(t)}", lowBound=0, cat=pulp.LpInteger)
                  for p, t in PT}
        output = {(p, t): pulp.LpVariable(f"output_{_tag(p)}_{_tag(t)}", lowBound=0) for p, t in PT}
        hydro_on = {(p, h): pulp.LpVariable(f"hydro_on_{_tag(p)}_{_tag(h)}", cat=pulp.LpBinary) for p, h in PH}
        hydro_start = {(p, h): pulp.LpVariable(f"hydro_start_{_tag(p)}_{_tag(h)}", cat=pulp.LpBinary)
                       for p, h in PH}
        pump = {p: pulp.LpVariable(f"pump_{_tag(p)}", lowBound=0) for p in periods}
        level = {p: pulp.LpVariable(f"reservoir_level_{_tag(p)}", lowBound=0) for p in periods}

        # Objective: thermal running cost per unit-hour, cost of output above each running unit's minimum,
        # thermal start-ups, hydro running cost per hour and hydro start-ups.
        prob += (
            pulp.lpSum(th[t]["cost_per_hour"] * hours[p] * ngen[p, t] for p, t in PT)
            + pulp.lpSum(th[t]["cost_per_mwh_above_min"] * hours[p] * (output[p, t] - th[t]["min_output_mw"] * ngen[p, t])
                         for p, t in PT)
            + pulp.lpSum(th[t]["startup_cost"] * nstart[p, t] for p, t in PT)
            + pulp.lpSum(hy[h]["cost_per_hour"] * hours[p] * hydro_on[p, h] for p, h in PH)
            + pulp.lpSum(hy[h]["startup_cost"] * hydro_start[p, h] for p, h in PH)
        ), "total_cost"

        # Units running cannot exceed the units of the type that exist
        for p, t in PT:
            prob += ngen[p, t] <= th[t]["units_available"], f"available_{_tag(p)}_{_tag(t)}"
        # Output of a type lies between the minimum and maximum output of its running units
        for p, t in PT:
            prob += output[p, t] >= th[t]["min_output_mw"] * ngen[p, t], f"min_output_{_tag(p)}_{_tag(t)}"
        for p, t in PT:
            prob += output[p, t] <= th[t]["max_output_mw"] * ngen[p, t], f"max_output_{_tag(p)}_{_tag(t)}"
        # Thermal plus hydro output covers predicted demand plus the power used for pumping
        for p in periods:
            prob += (pulp.lpSum(output[p, t] for t in types)
                     + pulp.lpSum(hy[h]["output_mw"] * hydro_on[p, h] for h in hydros)
                     >= demand[p] + pump[p]), f"demand_{_tag(p)}"
        # Reservoir: pumping raises the level, running hydro units draw it down. The day is a cycle: the
        # period before the first one is the last one, so the level ends the day where it started.
        for i, p in enumerate(periods):
            before = periods[i - 1]
            prob += (level[p] == level[before] + hours[p] / mwh_per_m * pump[p]
                     - pulp.lpSum(hy[h]["depletion_m_per_hour"] * hours[p] * hydro_on[p, h] for h in hydros)), \
                f"reservoir_{_tag(p)}"
        # Reserve: running thermal units at maximum output plus every hydro unit's output (running or not)
        # must cover predicted demand plus the reserve margin.
        hydro_capacity = sum(hy[h]["output_mw"] for h in hydros)
        for p in periods:
            prob += (pulp.lpSum(th[t]["max_output_mw"] * ngen[p, t] for t in types)
                     >= (1 + P["reserve_margin"]) * demand[p] - hydro_capacity), f"reserve_{_tag(p)}"
        # Start-ups: a unit running now that was not running in the previous period was started. Before the
        # first period, units_on_at_start thermal units of each type (and the hydro units with on_at_start = 1) run.
        for i, p in enumerate(periods):
            for t in types:
                running_before = th[t]["units_on_at_start"] if i == 0 else ngen[periods[i - 1], t]
                prob += ngen[p, t] <= running_before + nstart[p, t], f"thermal_startup_{_tag(p)}_{_tag(t)}"
        for i, p in enumerate(periods):
            for h in hydros:
                running_before = hy[h]["on_at_start"] if i == 0 else hydro_on[periods[i - 1], h]
                prob += hydro_on[p, h] <= running_before + hydro_start[p, h], f"hydro_startup_{_tag(p)}_{_tag(h)}"

        prob._wig = {"ngen": ngen, "output": output, "nstart": nstart, "hydro_on": hydro_on,
                     "hydro_start": hydro_start, "pump": pump, "reservoir_level": level}  # handles for kpis()
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        ix = self._index(data)
        periods, hours = ix["periods"], ix["hours"]
        types, th, hydros, hy = ix["types"], ix["thermal"], ix["hydros"], ix["hydro"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        PT = [(p, t) for p in periods for t in types]
        PH = [(p, h) for p in periods for h in hydros]

        running = sum(th[t]["cost_per_hour"] * hours[p] * val(v["ngen"][p, t]) for p, t in PT)
        above_min = sum(th[t]["cost_per_mwh_above_min"] * hours[p]
                        * (val(v["output"][p, t]) - th[t]["min_output_mw"] * val(v["ngen"][p, t])) for p, t in PT)
        starts = sum(th[t]["startup_cost"] * val(v["nstart"][p, t]) for p, t in PT)
        hydro_cost = sum(hy[h]["cost_per_hour"] * hours[p] * val(v["hydro_on"][p, h])
                         + hy[h]["startup_cost"] * val(v["hydro_start"][p, h]) for p, h in PH)
        return {
            "total_cost": round(running + above_min + starts + hydro_cost, 2),
            "thermal_running_cost": round(running, 2),
            "thermal_output_cost": round(above_min, 2),
            "thermal_startup_cost": round(starts, 2),
            "hydro_cost": round(hydro_cost, 2),
            "units_on": {t: {p: int(round(val(v["ngen"][p, t]))) for p in periods} for t in types},
            "hydro_hours": {h: round(sum(hours[p] * val(v["hydro_on"][p, h]) for p in periods), 2) for h in hydros},
            "pumped_energy_mwh": round(sum(hours[p] * val(v["pump"][p]) for p in periods), 1),
        }
