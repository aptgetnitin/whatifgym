# Assignment with allowed teams

**Domain:** packing / assignment · **Type:** IP (binary) · **Size:** 99 variables, 57 constraints · **Sense:** minimise cost

Twelve workers in three groups of four, six tasks. Every task must go to at least one worker; each assignment has a
cost (cost matrix) and each task a size, and the tasks a worker takes may total at most its size limit (15). Within
each group only certain pairs of workers may work (five allowed teams per group, e.g. workers 2 and 3); the
other two stay idle. The goal is the cheapest assignment.

Decisions: `assign[worker, task]`, `works[worker]` (has a task), `team[team]` (the chosen team of its group).

Reference optimum (original OR-Tools CP-SAT): **239**, unique: worker_0-task_4, worker_1-task_2, worker_5-task_5,
worker_6-task_3, worker_10-task_0, worker_11-task_1.

The original is a CP-SAT model (84 Booleans, 33 constraints) using `AddMaxEquality` and `AddAllowedAssignments`.
The port is a 0-1 IP: `works` is linked to `assign` by two linear rows per worker, and each allowed table becomes
one binary per allowed team, a pick-one-team row per group and one pattern row per worker.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `workers` | Raise worker_3's size limit to 25; tighten every limit to 12. |
| `tasks` | task_4 grows to size 18; task_0 needs two workers. |
| `costs` | worker_10's cost for task_0 rises to 60; worker_5 can no longer do task_5. |
| `allowed_teams` | Allow workers 0 and 3 to work together; forbid team 5+6. |

Source: Google OR-Tools `examples/python/assignment_with_constraints_sat.py` (Apache-2.0). Re-implemented from the published data.
