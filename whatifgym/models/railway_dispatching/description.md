# Railway dispatching

**Domain:** network routing · **Type:** MILP · **Size:** 218 variables (180 binary), 367 constraints · **Sense:** minimise total delay

A line has 4 stations (0, 2, 4, 6; capacity 2 trains each) joined by 3 single tracks (1, 3, 5; capacity 1).
Six trains are already in the network: A–D run 0→6, E and F run 6→0, each starting from its current position
(`trains.start`). Each train must spend at least the resource's `duration` on every resource left on its route.
Dispatching decides when each train enters each resource, so that no resource ever holds more trains than its
capacity. Opposite trains can pass, and a faster train can overtake, only at stations.

For every pair of trains that share a resource, exactly one case holds: one goes first, the other goes first,
or they meet (overlap). Big-M rows link each case to the entry times. A capacity-1 resource forbids meets. On a
capacity-c resource, any c+1 trains may not all overlap pairwise. The objective is total delay: each train's
arrival time minus its minimum remaining running time.

Reference optimum (original notebook, Gurobi): **47 minutes**. Trains C and D are on time; A, B, E and F are
delayed (E by 6). The split of delay among A, B and F, and the last arrival (49–52), have alternative optima.

Port notes: notebook dataset `linear` (its default). The big-M is computed as in the notebook, which sums the
resource **ids** instead of the durations: M = 21 × 6 trains = 126, a structural constant, not data. It is not
binding on the base data. `ready_time` (0 in the base data) replaces the notebook's fixed start at time 0.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `trains` | Train E can only leave in 10 minutes; train B is cancelled; an extra train on route 0-6. |
| `resources` | Track 3 is slowed to 12 minutes; station 2 gets a third platform; track 5 is doubled (capacity 2). |

Rules and fixed decisions address `entry_time`/`finish_time` (by `train`, `resource`) and `goes_first`/`meet`
(by `resource`, `train`, `other_train`). Examples: "F must arrive before E"; "A must not meet E at station 4".

Source: Gurobi modeling-examples `railway_dispatching/railway_dispatching.ipynb` (Apache-2.0), data
`data/linear/*.csv`. Re-implemented from the published data.
