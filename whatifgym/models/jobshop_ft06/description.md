# Job-shop scheduling (ft06)

**Domain:** scheduling · **Type:** MILP · **Size:** 163 variables (90 binary), 252 constraints · **Sense:** minimise makespan

The classic Fisher-Thompson 6x6 job shop. Six jobs each pass through all six machines in a fixed job-specific
order (`operations.step`, `operations.machine`) with a processing time per operation. A machine processes one
operation at a time, without interruption, and a job's next step starts only after its previous step ends. The
goal is the shortest makespan: the time the last job finishes. `jobs.release_time` (0 in the base data) is the
earliest start of a job's first step.

Decisions: `start`/`end[job, step]`, `makespan`, and `goes_first[machine, job, other_job]` (one binary per pair
of jobs on each machine, job < other_job).

Reference optimum (original OR-Tools CP-SAT): **55**. Many optimal schedules exist: per-job completion times
(e.g. J2 anywhere in 37–55) and the total completion time (301–323) are not unique; makespan, machine idle time
within the makespan and utilisation are.

Port notes: the original is a CP-SAT model (73 variables, 73 constraints: 36 intervals, 6 no-overlap, 30
precedences, 1 max-equality). The MILP keeps start/end per operation; each no-overlap becomes two big-M rows per
job pair per machine, and the max-equality becomes "makespan >= end of each last step" (tight when minimising).
The big-M is the horizon, a structural constant computed from the data: latest release time + sum of all
processing times (197 on the base data, the original's horizon); start and end times are bounded by it.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `operations` | J1's step 3 takes 14 instead of 10; machine M5 runs 20% slower (scale its processing times). |
| `jobs` | J3's material arrives at time 10 (release time); every job is released 5 later. |

Rules and fixed decisions address `start`/`end` (by `job`, `step`), `makespan`, and `goes_first` (by `machine`,
`job`, `other_job`). Examples: "J0 must finish by 40"; "J5 goes before J1 on M3".

Source: Google OR-Tools `examples/python/jobshop_ft06_sat.py` (Apache-2.0); ft06 data from Fisher & Thompson
(1963). Re-implemented from the published data.
