# Technician routing and scheduling

**Domain:** network routing · **Type:** MILP · **Size:** 660 variables (630 binary), 217 constraints · **Sense:** minimise penalty

A service company sends seven technicians from two depots (Heidelberg, Freiburg im Breisgau) to seven customer
jobs in towns of Baden-Württemberg. Each job has a type (priority, duration) and a time window for the service
start and a due time; each technician has a daily capacity (service + travel minutes) and a set of job types they
are qualified for. A dispatched technician drives one tour from the home depot through the assigned
customers and back. Penalties, all multiplied by the job's priority: 6,100 per unfilled job, 61 per minute a
service starts outside its window, 1 per minute a job finishes after its due time. Travel itself costs nothing
except capacity.

Decisions: `assign`, `use`, `route[from, to, technician]`, `start_time[location]`, `lateness`, `early_start`,
`late_start`, `unfilled`. Subtours are cut by big-M sequencing of start times (big-M = day length + duration +
travel, a structural constant built from `day_length_min`).

Data: the notebook's scenario workbook `data-Sce3.xlsx` (capacities 240/180 min); the base workbook `Sce0`
has optimum 0 and is not used. Reference optimum (original notebook, Gurobi): **12,410** — Customer4
(installation, priority 2) unfilled (12,200) and Customer5 105 min late (210). Same formulation and size; no
reformulation.

Quirks kept from the original: Customer5 has due time 0 (window 0–600), so it is always late; an unfilled job
may still be visited by an unqualified technician (the one-technician row sums over everybody); start times are
per location, so customers must be in different towns; depot self-loop and depot-to-depot legs exist but do
nothing. Technicians used and travel minutes vary across optimal plans.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `technicians` | Bob is off sick; Flor works a full 240-min day; Ed moves to the Freiburg depot. |
| `job_types` | Installations take 90 min; critical repairs get priority 5. |
| `skills` | Albert is trained for installations; Gina loses critical repairs. |
| `customers` | Customer4's window opens at 60; Customer5 is due at 120; a job changes type. |
| `travel_times` | Roadworks add 20 min between Karlsruhe and Baden-Baden. |
| `params` | Unfilled jobs cost 10,000; window violations 100/min; a 480-min day. |

Source: Gurobi modeling-examples `technician_routing_scheduling/technician_routing_scheduling.ipynb` and
`data-Sce3.xlsx` (Apache-2.0, fictional data). Re-implemented from the published data.
