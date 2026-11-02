"""Single machine scheduling with sequence-dependent setup times, release dates and deadlines (MILP).

Clean-room re-implementation of the public OR-Tools example
``examples/python/single_machine_scheduling_with_setup_release_due_dates_sat.py`` (Apache-2.0), a CP-SAT model, as
a mixed-integer program. Only the published data values are reused: 15 job durations, the 16 x 15 setup-time matrix
(first row = setup from the empty machine), release dates, due dates (hard deadlines) and two precedences.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source

START, END = "start", "end"  # dummy node of the machine's sequence: empty machine before / after all jobs


class SingleMachineScheduling(BaseModel):
    name = "single_machine_scheduling"
    title = "Single machine scheduling with setup times, release and due dates (OR-Tools example)"
    domain = "scheduling"
    sense = "min"
    problem_type = "MILP"
    source = Source(
        repo="google/or-tools",
        path="examples/python/single_machine_scheduling_with_setup_release_due_dates_sat.py",
        url="https://github.com/google/or-tools/blob/stable/examples/python/"
            "single_machine_scheduling_with_setup_release_due_dates_sat.py",
        license="Apache-2.0",
        notes="Data values from the CP-SAT example; AddCircuit + enforced precedences + AddMaxEquality re-formulated "
              "as an assignment/big-M sequencing MILP; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("jobs", "setup_times", "precedences")
    HAS_PARAMS = False
    MEASURE_DIMS = {"follows": ("from_job", "to_job"), "runs_before": ("job", "other_job"),
                    "start_time": ("job",), "end_time": ("job",)}
    SCORING_KPIS = ["makespan"]

    @staticmethod
    def _index(data: dict[str, Any]):
        jobs = [r["job"] for r in data["jobs"]]
        dur = {r["job"]: r["duration"] for r in data["jobs"]}
        rel = {r["job"]: r["release_date"] or 0 for r in data["jobs"]}
        setup = {(r["from_job"], r["to_job"]): r["setup_time"] for r in data["setup_times"]
                 if r["from_job"] in dur | {START: 0} and r["to_job"] in dur and r["from_job"] != r["to_job"]}
        for i in [START] + jobs:
            for j in jobs:
                if i != j and (i, j) not in setup:
                    raise ValueError(f"setup_times has no row from {i} to {j}")
        # horizon as in the original: every job plus its largest incoming setup (the latest any plan can end)
        horizon = sum(dur.values()) + sum(max(s for (_, jj), s in setup.items() if jj == j) for j in jobs)
        due = {r["job"]: r["due_date"] if r["due_date"] is not None else horizon for r in data["jobs"]}
        prec = [(r["before"], r["after"]) for r in data["precedences"] if r["before"] in dur and r["after"] in dur]
        return jobs, dur, rel, due, setup, prec, horizon

    def build(self, data: dict[str, Any]):
        import pulp

        jobs, dur, rel, due, setup, prec, horizon = self._index(data)
        prob = pulp.LpProblem("single_machine_scheduling", pulp.LpMinimize)
        arcs = list(setup) + [(j, END) for j in jobs]
        m_in = {j: min(sv for (i, jj), sv in setup.items() if jj == j and i != START) for j in jobs}  # after a job
        m_any = {j: min(m_in[j], setup[START, j]) for j in jobs}  # least setup into j from anywhere
        x = {a: pulp.LpVariable(f"follows_{a[0]}_{a[1]}", cat=pulp.LpBinary) for a in arcs}
        # z[i, j] = end time of i if j directly follows i, else 0 (time carried along the arc)
        z = {a: pulp.LpVariable(f"handover_{a[0]}_{a[1]}", lowBound=0) for a in arcs if a[0] != START}
        s = {j: pulp.LpVariable(f"start_{j}", lowBound=max(rel[j], m_any[j])) for j in jobs}
        e = {j: pulp.LpVariable(f"end_{j}", upBound=due[j]) for j in jobs}
        cmax = pulp.LpVariable("makespan", lowBound=0)

        prob += cmax, "makespan"
        # AddCircuit over {empty machine} + jobs: one arc out of and one arc into every node
        prob += pulp.lpSum(x[START, j] for j in jobs) == 1, "first_job"
        prob += pulp.lpSum(x[j, END] for j in jobs) == 1, "last_job"
        for j in jobs:
            prob += pulp.lpSum(v for (a, b), v in x.items() if a == j) == 1, f"one_next_{j}"
            prob += pulp.lpSum(v for (a, b), v in x.items() if b == j) == 1, f"one_before_{j}"
            prob += e[j] == s[j] + dur[j], f"duration_{j}"
            prob += pulp.lpSum(v for (a, b), v in z.items() if a == j) == e[j], f"handover_out_{j}"
            # the enforced "start_j >= end_i + setup[i, j] if j follows i" rows, aggregated over the incoming arcs
            prob += s[j] >= pulp.lpSum(z[i, j] for (i, jj) in setup if jj == j and i != START) + pulp.lpSum(
                setup[i, j] * x[i, j] for (i, jj) in setup if jj == j), f"sequence_{j}"
        for (a, b), v in z.items():
            latest = due[a] if b == END else min(due[a], due[b] - dur[b] - setup[a, b])
            prob += v <= latest * x[a, b], f"handover_max_{a}_{b}"
            prob += v >= (s[a].lowBound + dur[a]) * x[a, b], f"handover_min_{a}_{b}"
        prob += cmax == pulp.lpSum(z[j, END] for j in jobs), "makespan_is_last_end"
        # Strengthening (valid, not in the original): before[i, j] = 1 if i runs anywhere before j. A job starts
        # after all jobs before it plus their least setups; the makespan is at least its end plus all jobs after it.
        y = {(a, b): pulp.LpVariable(f"before_{a}_{b}", cat=pulp.LpBinary)
             for n, a in enumerate(jobs) for b in jobs[n + 1:]}
        before = {**y, **{(b, a): 1 - v for (a, b), v in y.items()}}
        for (a, b), v in before.items():
            prob += x[a, b] <= v, f"follows_is_before_{a}_{b}"
            prob += s[b] >= e[a] + m_in[b] - (due[a] + m_in[b] - s[b].lowBound) * (1 - v), f"before_{a}_{b}"
        for j in jobs:
            rest = [k for k in jobs if k != j]
            prob += s[j] >= m_any[j] + pulp.lpSum(before[k, j] * (dur[k] + m_any[k]) for k in rest), f"head_{j}"
            prob += cmax >= e[j] + pulp.lpSum(before[j, k] * (dur[k] + m_in[k]) for k in rest), f"tail_{j}"
        for a, b in prec:
            prob += s[b] >= e[a], f"precedence_{a}_{b}"

        prob._wig = {"follows": x, "runs_before": y, "start_time": s, "end_time": e}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        jobs, dur, rel, due, setup, prec, horizon = self._index(data)
        nxt = {a: b for (a, b), v in prob._wig["follows"].items() if (v.value() or 0) > 0.5}
        order, cur = [], START
        while nxt.get(cur, END) != END:
            cur = nxt[cur]
            order.append(cur)
        end = {j: round(prob._wig["end_time"][j].value(), 4) for j in jobs}
        makespan = max(end.values())
        total_setup = sum(setup[a, b] for a, b in zip([START] + order, order))
        deadlines = [r["job"] for r in data["jobs"] if r["due_date"] is not None]
        return {
            "makespan": makespan,
            "total_setup_time": total_setup,
            "total_idle_time": round(makespan - sum(dur.values()) - total_setup, 4),
            "min_deadline_slack": min((round(due[j] - end[j], 4) for j in deadlines), default=None),
            "first_job": order[0] if order else None,
            "last_job": order[-1] if order else None,
            "sequence": order,
        }
