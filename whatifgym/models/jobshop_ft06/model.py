"""Job-shop scheduling, Fisher-Thompson ft06 (6 jobs x 6 machines), minimise the makespan (MILP).

Clean-room re-implementation of the OR-Tools example ``examples/python/jobshop_ft06_sat.py`` (Apache-2.0).
Only the published ft06 instance (processing times and machine routing) is reused. The original is a CP-SAT
interval / no-overlap model; this port is a disjunctive big-M MILP (one order binary per machine and job pair).
"""
from __future__ import annotations

import itertools
from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class JobshopFt06(BaseModel):
    name = "jobshop_ft06"
    title = "Job-shop scheduling, ft06 6x6 instance (OR-Tools examples)"
    domain = "scheduling"
    sense = "min"
    problem_type = "MILP"
    source = Source(
        repo="google/or-tools",
        path="examples/python/jobshop_ft06_sat.py",
        url="https://github.com/google/or-tools/blob/stable/examples/python/jobshop_ft06_sat.py",
        license="Apache-2.0",
        notes="ft06 data values from the example; CP-SAT interval model re-implemented as a big-M MILP in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("jobs", "machines", "operations")
    HAS_PARAMS = False
    MEASURE_DIMS = {
        "start": ("job", "step"),
        "end": ("job", "step"),
        "makespan": (),
        "goes_first": ("machine", "job", "other_job"),
    }
    # Alternative optimal schedules abound; only makespan-derived numbers are unique (see reference.json).
    SCORING_KPIS = ["makespan", "mean_utilisation", "idle_by_machine"]

    @staticmethod
    def _ops(data: dict[str, Any]):
        release = {j["job"]: j.get("release_time") or 0 for j in data["jobs"]}
        machines = {m["machine"] for m in data["machines"]}
        ops = {}
        for o in data["operations"]:
            if o["job"] not in release or o["machine"] not in machines:
                raise ValueError(f"operation {o['job']}/{o['step']}: unknown job or machine")
            ops.setdefault(o["job"], []).append(o)
        for j, lst in ops.items():
            lst.sort(key=lambda o: o["step"])
            if len({o["machine"] for o in lst}) < len(lst):
                raise ValueError(f"job {j} visits a machine twice")
        return release, ops

    def build(self, data: dict[str, Any]):
        import pulp

        release, ops = self._ops(data)
        dur = {(o["job"], o["step"]): o["duration"] for lst in ops.values() for o in lst}
        # Structural big-M = horizon: latest release + all processing in series bounds every end time.
        horizon = max(release.values(), default=0) + sum(dur.values())
        prob = pulp.LpProblem("jobshop_ft06", pulp.LpMinimize)
        s = {k: pulp.LpVariable(f"start_{k[0]}_{k[1]}", lowBound=0, upBound=horizon) for k in dur}
        e = {k: pulp.LpVariable(f"end_{k[0]}_{k[1]}", lowBound=0, upBound=horizon) for k in dur}
        cmax = pulp.LpVariable("makespan", lowBound=0, upBound=horizon)
        for k in dur:
            prob += e[k] - s[k] == dur[k], f"duration_{k[0]}_{k[1]}"
        for j, lst in ops.items():
            s[j, lst[0]["step"]].lowBound = release[j]
            for a, b in zip(lst, lst[1:]):
                prob += s[j, b["step"]] >= e[j, a["step"]], f"precedence_{j}_{a['step']}"
            prob += cmax >= e[j, lst[-1]["step"]], f"makespan_{j}"
        by_machine: dict[str, list] = {}
        for j, lst in ops.items():
            for o in lst:
                by_machine.setdefault(o["machine"], []).append((j, o["step"]))
        first = {}
        for m, lst in sorted(by_machine.items()):
            for a, b in itertools.combinations(sorted(lst), 2):
                y = pulp.LpVariable(f"first_{m}_{a[0]}_{b[0]}", cat=pulp.LpBinary)  # 1: a's job before b's job
                prob += s[b] >= e[a] - horizon * (1 - y), f"order_{m}_{a[0]}_{b[0]}"
                prob += s[a] >= e[b] - horizon * y, f"order_{m}_{b[0]}_{a[0]}"
                first[m, a[0], b[0]] = y
        prob += cmax, "makespan"
        prob._wig = {"start": s, "end": e, "makespan": {(): cmax}, "goes_first": first}
        prob._ops = ops
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        w = prob._wig
        cmax = round(w["makespan"][()].value(), 4)
        done = {j: round(w["end"][j, lst[-1]["step"]].value(), 4) for j, lst in prob._ops.items()}
        busy: dict[str, float] = {}
        for lst in prob._ops.values():
            for o in lst:
                busy[o["machine"]] = busy.get(o["machine"], 0) + o["duration"]
        busy = dict(sorted(busy.items()))
        return {
            "makespan": cmax,
            "completion_by_job": done,
            "total_completion_time": round(sum(done.values()), 4),
            "busy_by_machine": busy,
            "idle_by_machine": {m: round(cmax - b, 4) for m, b in busy.items()},
            "mean_utilisation": round(100 * sum(busy.values()) / (len(busy) * cmax), 2) if cmax else 0.0,
        }
