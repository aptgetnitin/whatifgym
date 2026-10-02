# Multiple knapsack

**Domain:** packing / assignment · **Type:** IP (binary) · **Size:** 75 variables, 20 constraints · **Sense:** maximise packed value

Fifteen items, each with a weight and a value, must be packed into five bins of capacity 100. An item goes into
at most one bin, the weight in each bin may not exceed its capacity, and the goal is to maximise the total value
packed. The model is small but has the classic what-if structure of allocation problems: capacity, demand
(items) and value all change independently.

Decisions: `x[item, bin] = 1` if the item is placed in the bin.

Reference optimum (original OR-Tools CP-SAT and SCIP samples): **395** (packed weight 438, three items left out).

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `bins` | Add a sixth bin; shrink bin2 to 60; what capacity would be needed to pack everything? |
| `items` | item3's value drops to 20; a new 50-kg item worth 60 arrives; item9 is withdrawn. |

Solvers: PuLP formulation on HiGHS / SCIP / CBC, plus a native OR-Tools CP-SAT formulation (`build_cpsat`).

Source: Google OR-Tools `ortools/sat/samples/multiple_knapsack_sat.py` and
`ortools/linear_solver/samples/multiple_knapsack_mip.py` (Apache-2.0). Re-implemented from the published data.
