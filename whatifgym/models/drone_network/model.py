"""Drone-network design for out-of-hospital cardiac arrests — which bases get a drone and which base answers each
incident location, minimising the expected response time of an M/G/1 queue per base (MILP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example ``drone_network/drone_network.ipynb``
(Apache-2.0). Only published data values are reused (the notebook's June 2019 incident window and 7-base subset of
OHCAs.csv, BaseStations.csv and Base_to_OHCA_distance.csv, drone count, speed and maintenance time); the code is new.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class DroneNetwork(BaseModel):
    name = "drone_network"
    title = "Drone-network design for cardiac arrests (Gurobi modeling-examples)"
    domain = "supply_chain_logistics"
    sense = "min"
    problem_type = "MILP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="drone_network/drone_network.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/drone_network/drone_network.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook's CSV files (its June 2019 window, 7 bases); model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("bases", "incidents", "distances")
    HAS_PARAMS = True
    MEASURE_DIMS = {
        "open": ("base",),
        "assign": ("location", "base"),
        "queue_load": ("base",),
        "linked_load": ("location", "base"),
    }
    SCORING_KPIS = ["response_objective", "bases_opened", "avg_wait_minutes", "avg_flight_minutes",
                    "max_base_utilization"]

    @staticmethod
    def _index(data: dict[str, Any]):
        P = data["params"]
        bases = [r["base"] for r in data["bases"]]
        hours = 24 * P["observation_days"]
        # arrivals per hour, rounded to 6 decimals as in the original
        rate = {r["location"]: round(r["incidents"] / hours, 6) for r in data["incidents"]}
        dist = {(r["location"], r["base"]): r["distance_m"] for r in data["distances"]
                if r["location"] in rate and r["base"] in bases}
        # service time (hours): maintenance + flight there and back
        serv = {k: P["maintenance_minutes"] / 60 + 2 * 0.001 * d / P["drone_speed_kmh"] for k, d in dist.items()}
        return bases, rate, dist, serv

    def build(self, data: dict[str, Any]):
        import pulp

        bases, rate, dist, serv = self._index(data)
        P = data["params"]
        pairs = list(dist)
        bidx = {b: n for n, b in enumerate(bases)}
        lidx = {loc: n for n, loc in enumerate(rate)}
        tag = {k: f"{lidx[k[0]]}_{bidx[k[1]]}" for k in pairs}  # numeric names: street names are not PuLP-safe
        v_bar = 2 * sum(serv.values())  # structural big-M, as in the original
        prob = pulp.LpProblem("drone_network", pulp.LpMinimize)
        x = {b: pulp.LpVariable(f"open_{bidx[b]}", cat=pulp.LpBinary) for b in bases}
        y = {k: pulp.LpVariable(f"assign_{tag[k]}", cat=pulp.LpBinary) for k in pairs}
        V = {b: pulp.LpVariable(f"queue_load_{bidx[b]}", lowBound=0, upBound=v_bar) for b in bases}
        nu = {k: pulp.LpVariable(f"linked_load_{tag[k]}", lowBound=0) for k in pairs}

        total_rate = sum(rate.values())
        prob += pulp.lpSum(rate[i] / total_rate * (0.5 * nu[i, j] + dist[i, j] / P["drone_speed_kmh"] * y[i, j])
                           for i, j in pairs), "response_objective"
        for k in pairs:
            prob += y[k] <= x[k[1]], f"select_{tag[k]}"
        prob += pulp.lpSum(x.values()) <= P["max_bases"], "drone_limit"
        for i in rate:
            prob += pulp.lpSum(y[i, j] for j in bases if (i, j) in y) == 1, f"ohca_{lidx[i]}"
        for j in bases:
            mine = [k for k in pairs if k[1] == j]
            prob += pulp.lpSum(rate[i] * serv[i, j] * y[i, j] for i, _ in mine) <= 1, f"stability_{bidx[j]}"
            prob += (V[j] == pulp.lpSum(rate[i] * serv[i, j] ** 2 * y[i, j] for i, _ in mine)
                     + pulp.lpSum(rate[i] * serv[i, j] * nu[i, j] for i, _ in mine)), f"aux0_{bidx[j]}"
        for k in pairs:
            prob += nu[k] <= V[k[1]], f"aux1_{tag[k]}"
            prob += nu[k] <= v_bar * y[k], f"aux2_{tag[k]}"
            prob += nu[k] >= v_bar * (y[k] - 1) + V[k[1]], f"aux3_{tag[k]}"

        prob._wig = {"open": x, "assign": y, "queue_load": V, "linked_load": nu}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        bases, rate, dist, serv = self._index(data)
        P = data["params"]
        w = prob._wig
        val = lambda v: v.value() or 0.0  # noqa: E731
        L = sum(rate.values())
        on = [k for k, v in w["assign"].items() if val(v) > 0.5]
        util = {j: sum(rate[i] * serv[i, j] for i, b in on if b == j) for j in bases}
        wait_h = sum(rate[i] * 0.5 * val(w["linked_load"][i, j]) for i, j in on) / L
        flight_h = sum(rate[i] * 0.001 * dist[i, j] / P["drone_speed_kmh"] for i, j in on) / L
        opened = [b for b in bases if val(w["open"][b]) > 0.5]
        return {
            "response_objective": round(prob.objective.value(), 6),
            "bases_opened": len(opened),
            "avg_wait_minutes": round(60 * wait_h, 4),
            "avg_flight_minutes": round(60 * flight_h, 4),
            "max_base_utilization": round(max(util.values()), 4),
            "locations_per_base": {b: sum(1 for _, j in on if j == b) for b in opened},
            "bases_selected": opened,
        }

