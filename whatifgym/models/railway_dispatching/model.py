"""Railway dispatching — re-time trains on a single-track line after a disruption (MILP).

Clean-room re-implementation of the Gurobi modeling-examples notebook ``railway_dispatching/railway_dispatching.ipynb``
(Apache-2.0), main ``linear`` dataset. Only published data values are reused: the 4 stations and 3 tracks
(duration, capacity), the two routes and the 6 trains with their current position.
"""
from __future__ import annotations

import itertools
import math
from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class RailwayDispatching(BaseModel):
    name = "railway_dispatching"
    title = "Railway dispatching after a delay (Gurobi modeling-examples)"
    domain = "network_routing"
    sense = "min"
    problem_type = "MILP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="railway_dispatching/railway_dispatching.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/railway_dispatching/railway_dispatching.ipynb",
        license="Apache-2.0",
        notes="Data values from data/linear/*.csv of the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("resources", "routes", "trains")
    HAS_PARAMS = False
    MEASURE_DIMS = {
        "entry_time": ("train", "resource"),
        "finish_time": ("train",),
        "goes_first": ("resource", "train", "other_train"),
        "meet": ("resource", "train", "other_train"),
    }
    SCORING_KPIS = ["total_delay", "trains_delayed"]

    @staticmethod
    def _index(data: dict[str, Any]):
        res = {r["resource"]: r for r in data["resources"]}
        routes = {r["route"]: [int(x) for x in str(r["resources"]).split("-")] for r in data["routes"]}
        paths, ready = {}, {}
        for tr in data["trains"]:
            route = routes[tr["route"]]
            if tr["start"] not in route:
                raise ValueError(f"train {tr['train']}: start {tr['start']} is not on route {tr['route']}")
            paths[tr["train"]] = route[route.index(tr["start"]):]
            ready[tr["train"]] = tr.get("ready_time") or 0
        return res, paths, ready

    def build(self, data: dict[str, Any]):
        import pulp

        res, paths, ready = self._index(data)
        dur = {r: res[r]["duration"] for r in res}
        prob = pulp.LpProblem("railway_dispatching", pulp.LpMinimize)
        t = {(i, r): pulp.LpVariable(f"t_{i}_{r}", lowBound=0) for i, p in paths.items() for r in p}
        tf = {i: pulp.LpVariable(f"tf_{i}", lowBound=0) for i in paths}
        for i, p in paths.items():
            t[i, p[0]].lowBound = t[i, p[0]].upBound = ready[i]  # the original fixes the first event at 0
            for a, b in zip(p, p[1:]):
                prob += t[i, b] - t[i, a] >= dur[a], f"run_{i}_{a}"
            prob += tf[i] - t[i, p[-1]] == dur[p[-1]], f"finish_{i}"

        def nxt(i, r):  # time the train enters the resource after r (its finish time after the last one)
            p = paths[i]
            k = p.index(r)
            return t[i, p[k + 1]] if k + 1 < len(p) else tf[i]

        # Reproduces the notebook: `sum(duration)` sums the dict's KEYS (resource ids), not the durations.
        big_m = sum(res) * len(paths)
        first, meet = {}, {}
        for r in res:
            visitors = [i for i in paths if r in paths[i]]
            pair_x = {}
            for i, j in itertools.combinations(visitors, 2):
                yij = pulp.LpVariable(f"y_{r}_{i}_{j}", cat=pulp.LpBinary)
                yji = pulp.LpVariable(f"y_{r}_{j}_{i}", cat=pulp.LpBinary)
                x = pulp.LpVariable(f"x_{r}_{i}_{j}", cat=pulp.LpBinary)
                prob += t[j, r] - nxt(i, r) >= -big_m * (1 - yij), f"order_{r}_{i}_{j}"
                prob += t[i, r] - nxt(j, r) >= -big_m * (1 - yji), f"order_{r}_{j}_{i}"
                prob += nxt(j, r) - t[i, r] >= -big_m * (1 - x), f"meet_a_{r}_{i}_{j}"
                prob += nxt(i, r) - t[j, r] >= -big_m * (1 - x), f"meet_b_{r}_{i}_{j}"
                prob += yij + yji + x == 1, f"one_case_{r}_{i}_{j}"
                first[r, i, j], first[r, j, i], meet[r, i, j] = yij, yji, x
                pair_x[i, j] = x
            cap = math.floor(res[r]["capacity"] + 1e-9)  # a scaled capacity (1.5 trains) still admits whole trains
            if len(visitors) <= cap:
                continue
            if cap > 1:
                rhs = math.comb(cap + 1, 2) - 1
                for sub in itertools.combinations(visitors, cap + 1):
                    prob += (pulp.lpSum(pair_x[a, b] for a, b in itertools.combinations(sub, 2)) <= rhs,
                             f"capacity_{r}_{'_'.join(map(str, sub))}")
            else:
                for x in pair_x.values():
                    x.upBound = 0

        min_run = {i: sum(dur[r] for r in p) for i, p in paths.items()}
        prob += pulp.lpSum(tf[i] - min_run[i] for i in paths), "total_delay"
        prob._wig = {"entry_time": t, "finish_time": tf, "goes_first": first, "meet": meet}
        prob._min_run = min_run
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        w = prob._wig
        delay = {i: round(v.value() - prob._min_run[i], 4) + 0.0 for i, v in w["finish_time"].items()}
        return {
            "total_delay": round(sum(delay.values()), 4),
            "max_train_delay": max(delay.values()),
            "trains_delayed": sum(1 for d in delay.values() if d > 1e-4),
            "last_arrival": round(max(v.value() for v in w["finish_time"].values()), 4),
            "delay_by_train": delay,
        }
