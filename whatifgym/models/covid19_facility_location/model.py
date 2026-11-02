"""COVID-19 healthcare facility capacity — where to open temporary facilities and how to assign patients (MILP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``covid19_facility_location/covid19_facility_location.ipynb`` (Apache-2.0). Only the published data values are
reused (county centroids and demand, facility coordinates and capacities, travel and build costs, the 1e9 penalty);
the code here is new.
"""
from __future__ import annotations

from math import hypot
from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class Covid19FacilityLocation(BaseModel):
    name = "covid19_facility_location"
    title = "COVID-19 healthcare facility capacity (Gurobi modeling-examples)"
    domain = "supply_chain_logistics"
    sense = "min"
    problem_type = "MILP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="covid19_facility_location/covid19_facility_location.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/covid19_facility_location/covid19_facility_location.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook (base scenario); model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("counties", "facilities")
    HAS_PARAMS = True
    MEASURE_DIMS = {
        "assign": ("county", "facility"),
        "build": ("facility",),
        "extra_beds": ("facility",),
    }
    SCORING_KPIS = ["total_cost", "build_cost", "travel_cost", "temporary_built", "extra_beds_added", "patients_at_temporary"]

    @staticmethod
    def _index(data: dict[str, Any]):
        counties = [r["county"] for r in data["counties"]]
        demand = {r["county"]: r["demand"] for r in data["counties"]}
        facilities = [r["facility"] for r in data["facilities"]]
        temporary = [r["facility"] for r in data["facilities"] if r["kind"] == "temporary"]
        capacity = {r["facility"]: r["capacity"] for r in data["facilities"]}
        cpos = {r["county"]: (r["x"], r["y"]) for r in data["counties"]}
        fpos = {r["facility"]: (r["x"], r["y"]) for r in data["facilities"]}
        dist = {(c, f): hypot(cpos[c][0] - fpos[f][0], cpos[c][1] - fpos[f][1]) for c in counties for f in facilities}
        return counties, demand, facilities, temporary, capacity, dist

    def build(self, data: dict[str, Any]):
        import pulp

        counties, demand, facilities, temporary, capacity, dist = self._index(data)
        P = data["params"]
        prob = pulp.LpProblem("covid19_facility_location", pulp.LpMinimize)
        build = {t: pulp.LpVariable(f"build_{t}", cat=pulp.LpBinary) for t in temporary}
        assign = {(c, f): pulp.LpVariable(f"assign_{c}_{f}", lowBound=0) for c in counties for f in facilities}
        extra = {t: pulp.LpVariable(f"extra_beds_{t}", lowBound=0) for t in temporary}

        prob += (pulp.lpSum(P["travel_cost_per_patient_distance"] * dist[k] * assign[k] for k in assign)
                 + pulp.lpSum(P["temporary_build_cost"] * build[t] for t in temporary)
                 + pulp.lpSum(P["extra_capacity_penalty"] * extra[t] for t in temporary)), "total_cost"

        for c in counties:
            prob += pulp.lpSum(assign[c, f] for f in facilities) == demand[c], f"demand_{c}"
        for f in facilities:
            served = pulp.lpSum(assign[c, f] for c in counties)
            if f in build:
                # as in the original, extra beds are not tied to building the site
                prob += served - extra[f] <= capacity[f] * build[f], f"capacity_{f}"
            else:
                prob += served <= capacity[f], f"capacity_{f}"

        prob._wig = {"assign": assign, "build": build, "extra_beds": extra}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        counties, demand, facilities, temporary, capacity, dist = self._index(data)
        P = data["params"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        built = [t for t in temporary if val(v["build"][t]) > 0.5]
        travel = sum(P["travel_cost_per_patient_distance"] * dist[k] * val(x) for k, x in v["assign"].items())
        extra = sum(val(v["extra_beds"][t]) for t in temporary)
        build_cost = P["temporary_build_cost"] * len(built)
        penalty = P["extra_capacity_penalty"] * extra
        at_temp = sum(val(v["assign"][c, t]) for c in counties for t in temporary)
        total_dem = sum(demand.values())
        return {
            "total_cost": round(travel + build_cost + penalty, 2),
            "build_cost": round(build_cost, 2),
            "travel_cost": round(travel, 2),
            "temporary_built": len(built),
            "extra_beds_added": round(extra, 3),
            "patients_at_temporary": round(at_temp, 3),
            "avg_travel_distance": round(travel / P["travel_cost_per_patient_distance"] / total_dem, 4)
            if total_dem and P["travel_cost_per_patient_distance"] else None,
            "temporary_sites_built": built,
        }
