"""Technician routing and scheduling — assign service jobs to technicians and route them from their depots (MILP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``technician_routing_scheduling/technician_routing_scheduling.ipynb`` (Apache-2.0), scenario workbook
``data-Sce3.xlsx``. Only the published data values are reused; the code here is new.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class TechnicianRoutingScheduling(BaseModel):
    name = "technician_routing_scheduling"
    title = "Technician routing and scheduling (Gurobi modeling-examples)"
    domain = "network_routing"
    sense = "min"
    problem_type = "MILP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="technician_routing_scheduling/technician_routing_scheduling.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/technician_routing_scheduling/technician_routing_scheduling.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook's scenario workbook data-Sce3.xlsx; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("technicians", "job_types", "skills", "customers", "travel_times")
    HAS_PARAMS = True
    MEASURE_DIMS = {
        "assign": ("customer", "technician"),
        "use": ("technician",),
        "route": ("from_location", "to_location", "technician"),
        "start_time": ("location",),
        "lateness": ("customer",),
        "early_start": ("customer",),
        "late_start": ("customer",),
        "unfilled": ("customer",),
    }
    SCORING_KPIS = ["total_penalty", "unfilled_penalty", "window_penalty", "lateness_penalty",
                    "jobs_unfilled", "lateness_minutes"]

    @staticmethod
    def _index(data: dict[str, Any]):
        techs = [r["technician"] for r in data["technicians"]]
        cap = {r["technician"]: r["capacity_min"] for r in data["technicians"]}
        depot = {r["technician"]: r["depot"] for r in data["technicians"]}
        jt = {r["job_type"]: r for r in data["job_types"]}
        skill = {(r["technician"], r["job_type"]) for r in data["skills"] if r["qualified"] == 1}
        custs = [r["customer"] for r in data["customers"]]
        cr = {r["customer"]: r for r in data["customers"]}
        loc = {c: cr[c]["location"] for c in custs}
        if len(set(loc.values())) != len(custs):
            raise ValueError("each customer needs its own location (service start times are per location)")
        dur = {c: jt[cr[c]["job_type"]]["duration_min"] for c in custs}
        prio = {c: jt[cr[c]["job_type"]]["priority"] for c in custs}
        can = {c: [k for k in techs if (k, cr[c]["job_type"]) in skill] for c in custs}
        locs: list[str] = []
        dist: dict[tuple[str, str], float] = {}
        for r in data["travel_times"]:
            a, b = r["from_location"], r["to_location"]
            dist[a, b] = dist[b, a] = r["travel_min"]
            locs += [l for l in (a, b) if l not in locs]
        for l in locs:
            dist[l, l] = 0
        depots = list(dict.fromkeys(depot[k] for k in techs))
        return techs, cap, depot, custs, cr, loc, dur, prio, can, locs, dist, depots

    def build(self, data: dict[str, Any]):
        import pulp

        techs, cap, depot, custs, cr, loc, dur, prio, can, locs, dist, depots = self._index(data)
        P = data["params"]
        H = P["day_length_min"]
        cust_locs = [loc[c] for c in custs]
        prob = pulp.LpProblem("technician_routing_scheduling", pulp.LpMinimize)
        x = {(c, k): pulp.LpVariable(f"assign_{c}_{k}", cat=pulp.LpBinary) for c in custs for k in techs}
        u = {k: pulp.LpVariable(f"use_{k}", cat=pulp.LpBinary) for k in techs}
        # as in the original: arcs over every location pair, arcs touching another technician's depot fixed to 0
        y = {(i, j, k): pulp.LpVariable(
                f"route_{i}_{j}_{k}", cat=pulp.LpBinary,
                upBound=0 if any(l in depots and l != depot[k] for l in (i, j)) else 1)
             for i in locs for j in locs for k in techs}
        t = {l: pulp.LpVariable(f"start_time_{l}", lowBound=0, upBound=H) for l in locs}
        z = {c: pulp.LpVariable(f"lateness_{c}", lowBound=0) for c in custs}
        xa = {c: pulp.LpVariable(f"early_start_{c}", lowBound=0) for c in custs}
        xb = {c: pulp.LpVariable(f"late_start_{c}", lowBound=0) for c in custs}
        g = {c: pulp.LpVariable(f"unfilled_{c}", cat=pulp.LpBinary) for c in custs}

        prob += (pulp.lpSum(P["lateness_penalty"] * prio[c] * z[c] for c in custs)
                 + pulp.lpSum(P["window_violation_penalty"] * prio[c] * (xa[c] + xb[c]) for c in custs)
                 + pulp.lpSum(P["unfilled_job_penalty"] * prio[c] * g[c] for c in custs)), "total_penalty"

        for c in custs:
            prob += pulp.lpSum(x[c, k] for k in can[c]) + g[c] == 1, f"cover_{c}"
        for c in custs:
            prob += pulp.lpSum(x[c, k] for k in techs) <= 1, f"one_technician_{c}"
        for k in techs:
            # explicit terms keep the zero-length depot self-loops in the model, as Gurobi's quicksum does
            work = pulp.LpAffineExpression([(x[c, k], dur[c]) for c in custs]
                                           + [(y[i, j, k], dist[i, j]) for i in locs for j in locs])
            prob += work <= cap[k] * u[k], f"capacity_{k}"
        for k in techs:
            for c in custs:
                prob += pulp.lpSum(y[i, loc[c], k] for i in locs) == x[c, k], f"arrive_{k}_{c}"
        for k in techs:
            for c in custs:
                prob += pulp.lpSum(y[loc[c], j, k] for j in locs) == x[c, k], f"leave_{k}_{c}"
        for k in techs:
            prob += pulp.lpSum(y[j, depot[k], k] for j in cust_locs) == u[k], f"return_depot_{k}"
        for k in techs:
            prob += pulp.lpSum(y[depot[k], j, k] for j in cust_locs) == u[k], f"leave_depot_{k}"
        # i == j included as in the original: it forbids a technician looping on one customer's location
        for a in custs:
            for b in custs:
                i, j = loc[a], loc[b]
                big_m = H + dur[a] + dist[i, j]
                prob += (t[j] >= t[i] + dur[a] + dist[i, j]
                         - big_m * (1 - pulp.lpSum(y[i, j, k] for k in techs))), f"sequence_{a}_{b}"
        for d in depots:
            for b in custs:
                j = loc[b]
                big_m = H + dist[d, j]
                prob += (t[j] >= t[d] + dist[d, j]
                         - big_m * (1 - pulp.lpSum(y[d, j, k] for k in techs))), f"from_depot_{d}_{b}"
        for c in custs:
            prob += t[loc[c]] + xa[c] >= cr[c]["window_start"], f"window_start_{c}"
        for c in custs:
            prob += t[loc[c]] - xb[c] <= cr[c]["window_end"], f"window_end_{c}"
        for c in custs:
            prob += z[c] >= t[loc[c]] + dur[c] - cr[c]["due_time"], f"due_{c}"

        prob._wig = {"assign": x, "use": u, "route": y, "start_time": t, "lateness": z,
                     "early_start": xa, "late_start": xb, "unfilled": g}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        techs, cap, depot, custs, cr, loc, dur, prio, can, locs, dist, depots = self._index(data)
        P = data["params"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        unfilled = [c for c in custs if val(v["unfilled"][c]) > 0.5]
        travel = sum(dist[i, j] for (i, j, k), y in v["route"].items() if val(y) > 0.5)
        late = sum(val(v["lateness"][c]) for c in custs)
        unf_pen = sum(P["unfilled_job_penalty"] * prio[c] for c in unfilled)
        win_pen = sum(P["window_violation_penalty"] * prio[c] * (val(v["early_start"][c]) + val(v["late_start"][c]))
                      for c in custs)
        late_pen = sum(P["lateness_penalty"] * prio[c] * val(v["lateness"][c]) for c in custs)
        return {
            "total_penalty": round(unf_pen + win_pen + late_pen, 4),
            "unfilled_penalty": round(unf_pen, 4),
            "window_penalty": round(win_pen, 4),
            "lateness_penalty": round(late_pen, 4),
            "jobs_unfilled": len(unfilled),
            "lateness_minutes": round(late, 4),
            "technicians_used": sum(1 for k in techs if val(v["use"][k]) > 0.5),
            "travel_minutes": round(travel, 4),
        }
