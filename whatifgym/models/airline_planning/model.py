"""Airline planning after a flight disruption — cancel flights and re-route aircraft at reduced airport capacity (IP).

Clean-room re-implementation of the Gurobi modeling-examples notebook ``aviation_planning/airlineplanning.ipynb``
(Apache-2.0). Only published data values are reused: the 222 flights of ``flight_rotations_2006-07-01.csv`` between
the notebook's 4 busiest airports (ORY, CDG, LYS, NCE), the start/end airports of their 21 aircraft, the per-flight
revenue and passengers summed from ``flight_iterinaries.csv`` and the 50% capacity level.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source

DAY_START, DAY_END = 0, 23 * 60 + 59  # times of the source and sink nodes (00:00 and 23:59), as in the original


class AirlinePlanning(BaseModel):
    name = "airline_planning"
    title = "Airline planning after flight disruption (Gurobi modeling-examples)"
    domain = "network_routing"
    sense = "min"
    problem_type = "IP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="aviation_planning/airlineplanning.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/aviation_planning/airlineplanning.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook's data/*.csv (ROADEF 2009 / Amadeus), reduced to its 4 top airports; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("flights", "aircraft", "airports")
    HAS_PARAMS = False
    MEASURE_DIMS = {
        "operate": ("aircraft", "flight"),
        "connect": ("aircraft", "flight", "next_flight"),
    }
    SCORING_KPIS = ["lost_revenue", "revenue_kept", "passengers_carried", "revenue_flights_operated"]

    @staticmethod
    def _graph(data: dict[str, Any]):
        """Per aircraft: its nodes (flights + 'source' + 'sink') with (origin, dest, start, end), and the feasible arcs."""
        planes = {r["aircraft"]: r for r in data["aircraft"]}
        nodes: dict[str, dict] = {}
        for f in data["flights"]:
            if f["aircraft"] in planes:  # a grounded (removed) aircraft takes its flights with it
                nodes.setdefault(f["aircraft"], {})[f["flight"]] = (f["origin"], f["destination"], f["departure"], f["arrival"])
        arcs = {}
        for a, nd in nodes.items():
            # Reproduces the notebook: both pseudo-nodes have origin = end airport and destination = start airport.
            pseudo = (planes[a]["end_airport"], planes[a]["start_airport"])
            nd["source"] = pseudo + (DAY_START, DAY_START)
            nd["sink"] = pseudo + (DAY_END, DAY_END)
            arcs[a] = [(f1, f2) for f1 in nd for f2 in nd if f1 != f2 and (
                (nd[f1][3] < nd[f2][2] and nd[f1][1] == nd[f2][0]) or (f1 == "source" and f2 == "sink"))]
        return nodes, arcs

    def build(self, data: dict[str, Any]):
        import pulp

        nodes, arcs = self._graph(data)
        revenue = {f["flight"]: f["revenue"] for f in data["flights"]}
        tag = lambda a: a.replace("#", "_")
        prob = pulp.LpProblem("airline_planning", pulp.LpMinimize)
        x = {(a, f): pulp.LpVariable(f"x_{tag(a)}_{f}", cat=pulp.LpBinary) for a, nd in nodes.items() for f in nd}
        y = {(a, f1, f2): pulp.LpVariable(f"y_{tag(a)}_{f1}_{f2}", cat=pulp.LpBinary) for a in arcs for f1, f2 in arcs[a]}
        out = {k: [] for k in x}
        inn = {k: [] for k in x}
        for (a, f1, f2), v in y.items():
            out[a, f1].append(v)
            inn[a, f2].append(v)

        prob += pulp.lpSum((1 - x[a, f]) * revenue[f] for a, f in x if f not in ("source", "sink")), "lost_revenue"
        for a, nd in nodes.items():
            prob += pulp.lpSum(out[a, "source"]) == 1, f"leave_source_{tag(a)}"
            prob += pulp.lpSum(inn[a, "sink"]) == 1, f"reach_sink_{tag(a)}"
            for f in nd:
                if f not in ("source", "sink"):
                    prob += pulp.lpSum(out[a, f]) == pulp.lpSum(inn[a, f]), f"flow_{tag(a)}_{f}"
        for (a, f), v in x.items():  # also on source and sink, as in the original (x[sink] is forced to 0)
            prob += v <= pulp.lpSum(out[a, f]), f"fly_if_routed_{tag(a)}_{f}"
        # Reproduces the notebook: the pseudo-nodes count as departures/arrivals, both in the normal totals and in the LHS.
        for ap in data["airports"]:
            i, share = ap["airport"], ap["capacity_share"]
            dep = [x[a, f] for a, nd in nodes.items() for f in nd if nd[f][0] == i]
            arr = [x[a, f] for a, nd in nodes.items() for f in nd if nd[f][1] == i]
            prob += pulp.lpSum(dep) <= share * len(dep), f"departures_{i}"
            prob += pulp.lpSum(arr) <= share * len(arr), f"arrivals_{i}"

        prob._wig = {"operate": {k: v for k, v in x.items() if k[1] not in ("source", "sink")}, "connect": y}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        flights = {f["flight"]: f for f in data["flights"]}
        flown = [f for (a, f), v in prob._wig["operate"].items() if (v.value() or 0) > 0.5]
        planned = list(prob._wig["operate"])
        kept = sum(flights[f]["revenue"] for f in flown)
        total = sum(flights[f]["revenue"] for _, f in planned)
        return {
            "lost_revenue": round(total - kept, 4),
            "revenue_kept": round(kept, 4),
            "passengers_carried": sum(flights[f]["passengers"] for f in flown),
            "revenue_flights_operated": sum(1 for f in flown if flights[f]["revenue"] > 0),
            "flights_operated": len(flown),
            "aircraft_used": len({flights[f]["aircraft"] for f in flown}),
        }
