"""Assignment with group constraints — cover every task at least cost; in each worker group only an allowed team
may work (IP).

Clean-room re-implementation of the public OR-Tools example ``examples/python/assignment_with_constraints_sat.py``
(Apache-2.0), a CP-SAT model, as a 0-1 integer program. Only the published data values are reused: the 12 x 6 cost
matrix, the task sizes, the per-worker size limit (15) and the three tables of allowed working pairs.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class AssignmentWithConstraints(BaseModel):
    name = "assignment_with_constraints"
    title = "Assignment with allowed worker teams per group (OR-Tools example)"
    domain = "packing_assignment_covering"
    sense = "min"
    problem_type = "IP"
    source = Source(
        repo="google/or-tools",
        path="examples/python/assignment_with_constraints_sat.py",
        url="https://github.com/google/or-tools/blob/stable/examples/python/assignment_with_constraints_sat.py",
        license="Apache-2.0",
        notes="Data values from the CP-SAT example; AddAllowedAssignments and AddMaxEquality re-formulated as linear "
              "constraints over binaries; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("workers", "tasks", "costs", "allowed_teams")
    HAS_PARAMS = False
    MEASURE_DIMS = {"assign": ("worker", "task"), "works": ("worker",), "team": ("team",)}
    SCORING_KPIS = ["total_cost", "assignments", "workers_used", "max_worker_load", "extra_assignments"]

    @staticmethod
    def _index(data: dict[str, Any]):
        workers = [r["worker"] for r in data["workers"]]
        group = {r["worker"]: r["group"] for r in data["workers"]}
        capacity = {r["worker"]: r["size_capacity"] for r in data["workers"]}
        tasks = [r["task"] for r in data["tasks"]]
        size = {r["task"]: r["size"] for r in data["tasks"]}
        need = {r["task"]: r["min_workers"] for r in data["tasks"]}
        cost = {(r["worker"], r["task"]): r["cost"] for r in data["costs"]
                if r["worker"] in group and r["task"] in size}  # a missing pair = worker cannot do that task
        teams: dict[str, dict[str, int]] = {}
        for r in data["allowed_teams"]:
            teams.setdefault(r["team"], {})[r["worker"]] = r["works"]
        # a team belongs to the group of its listed workers; listed-but-absent workers are ignored
        team_group = {k: next(group[w] for w in rows if w in group) for k, rows in teams.items()
                      if any(w in group for w in rows)}
        return workers, group, capacity, tasks, size, need, cost, teams, team_group

    def build(self, data: dict[str, Any]):
        import pulp

        workers, group, capacity, tasks, size, need, cost, teams, team_group = self._index(data)
        prob = pulp.LpProblem("assignment_with_constraints", pulp.LpMinimize)
        assign = {(w, t): pulp.LpVariable(f"assign_{w}_{t}", cat=pulp.LpBinary) for (w, t) in cost}
        works = {w: pulp.LpVariable(f"works_{w}", cat=pulp.LpBinary) for w in workers}
        team = {k: pulp.LpVariable(f"team_{k}", cat=pulp.LpBinary) for k in team_group}

        prob += pulp.lpSum(cost[k] * v for k, v in assign.items()), "total_cost"
        for w in workers:
            mine = [v for (ww, _), v in assign.items() if ww == w]
            # works[w] = max_t assign[w, t]  (the original's AddMaxEquality), linearised for binaries
            prob += pulp.lpSum(mine) <= len(mine) * works[w], f"works_if_assigned_{w}"
            prob += works[w] <= pulp.lpSum(mine), f"works_only_if_assigned_{w}"
            prob += pulp.lpSum(size[t] * v for (ww, t), v in assign.items() if ww == w) <= capacity[w], f"size_{w}"
        for t in tasks:
            prob += pulp.lpSum(v for (_, tt), v in assign.items() if tt == t) >= need[t], f"cover_{t}"
        # AddAllowedAssignments(works of the group, allowed rows): pick one allowed team per group, and each
        # group member works exactly when the chosen team says so
        for g in sorted(set(team_group.values())):
            mine = [k for k in team_group if team_group[k] == g]
            prob += pulp.lpSum(team[k] for k in mine) == 1, f"one_team_{g}"
            for w in workers:
                if group[w] == g:
                    prob += works[w] == pulp.lpSum(teams[k].get(w, 0) * team[k] for k in mine), f"team_pattern_{w}"

        prob._wig = {"assign": assign, "works": works, "team": team}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        workers, group, capacity, tasks, size, need, cost, teams, team_group = self._index(data)
        chosen = sorted(k for k, v in prob._wig["assign"].items() if (v.value() or 0) > 0.5)
        load = {w: sum(size[t] for ww, t in chosen if ww == w) for w in workers}
        total = sum(cost[k] for k in chosen)
        return {
            "total_cost": total,
            "assignments": len(chosen),
            "workers_used": sum(1 for w in workers if load[w] > 0),
            "max_worker_load": max(load.values(), default=0),
            "extra_assignments": len(chosen) - sum(need.values()),
            "average_cost_per_assignment": round(total / len(chosen), 4) if chosen else None,
            "teams_chosen": sorted(k for k, v in prob._wig["team"].items() if (v.value() or 0) > 0.5),
            "assignment": {w: [t for ww, t in chosen if ww == w] for w in workers if load[w] > 0},
        }
