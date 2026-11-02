# Single machine scheduling with setups

**Domain:** scheduling · **Type:** MILP · **Size:** 601 variables (345 binary), 980 constraints · **Sense:** minimise makespan

Fifteen jobs run one at a time on one machine. Each job has a processing `duration`, may not start before its
`release_date` and, if it has a `due_date`, must finish by it (a hard deadline). Changing from one job to the next
costs a sequence-dependent setup time (`setup_times`, from `start` = the empty machine for the first job). Jobs
listed in `precedences` must finish before their successor starts. The goal is the shortest makespan (end of
the last job).

Decisions: `follows[from_job, to_job]` (to_job runs directly after from_job; `start`/`end` mark the first and last
job), `runs_before[job, other_job]` (job runs anywhere earlier), `start_time[job]`, `end_time[job]`.

Reference optimum (original OR-Tools CP-SAT): **112605**. job_7's window (release 48657, deadline 57364, duration
8706) pins it at about 48657; job_13 is always last. The sequence, total setup time (26504–27856) and the first
job (job_1 or job_5) have alternative optima.

The original is a CP-SAT model (271 variables, 245 constraints) using `AddCircuit`, `NoOverlap`, enforced
precedences and `AddMaxEquality`. The port is a MILP: the circuit becomes one-in/one-out rows on `follows`; the
setup rows become a time-flow formulation (`handover[i, j]` carries the end of i along the arc used). A plain
big-M port is not proven optimal within 60 s by the open solvers, so valid strengthening is added: the
`runs_before` binaries with big-M rows (M = deadline of i + least setup into j − earliest start of j; deadline =
horizon = all durations + largest incoming setups when there is none — a structural constant from the data) and
head/tail bounds on start times and makespan.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `jobs` | job_7 can only start at 52000; job_13 takes 9000; job_3 must be done by 60000; add a new job. |
| `setup_times` | Changing from job_1 to job_0 now takes 3000; the first setup of job_5 drops to 500. |
| `precedences` | job_9 must finish before job_4 starts; drop the job_1 → job_2 precedence. |

Rules and fixed decisions address `follows` (by `from_job`, `to_job`), `runs_before` (by `job`, `other_job`) and
`start_time`/`end_time` (by `job`). Examples: "job_8 directly after job_3"; "job_11 before job_4".

Source: Google OR-Tools `examples/python/single_machine_scheduling_with_setup_release_due_dates_sat.py`
(Apache-2.0). Re-implemented from the published data.
