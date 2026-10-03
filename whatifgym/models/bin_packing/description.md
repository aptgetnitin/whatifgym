# Bin packing

**Domain:** packing / assignment · **Type:** IP (binary) · **Size:** 132 variables, 22 constraints · **Sense:** minimise bins used

Eleven items weighing 19 to 48 units (370 in total) must each be packed into exactly one bin. Every bin holds at
most 100 units, and eleven bins are available, one per item, so a feasible packing always exists. The goal is to
use as few bins as possible.

Decisions: `x[item, bin] = 1` if the item is packed into the bin (121 variables); `y[bin] = 1` if the bin is used
(11 variables).

Constraints: every item goes into exactly one bin (11 rows), and the weight packed into a bin may not exceed its
capacity, which counts only if the bin is used: `sum weight * x <= capacity * y` (11 rows).

Reference optimum (original OR-Tools sample, SCIP): **4 bins**. The total weight of 370 needs at least four bins of
100, so the optimum meets this weight bound and leaves 30 units of space in the four used bins. Many packings reach
it, so which bins are used, and what each holds, differs between solvers.

The sample uses one capacity for every bin; here capacity is a column of `bins`, so a what-if can resize a single
bin. With the shipped data every bin holds 100 and the model is exactly the original.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `items` | item0 now weighs 80 (5 bins: total weight 402); item2 weighs 49 (5 bins: the total is exactly 400, but no four full bins exist); a new 45-unit item arrives; every item is 10 % heavier. |
| `bins` | Bins hold 90 instead of 100 (5 bins); bin0 is a larger 150-unit bin; only three bins are available (infeasible). |

Rules and fixed decisions act on the measures `x[item, bin]` and `y[bin]`, for example: at most two items in bin0,
item6 and item7 must share bin3, or at most three bins may be used (infeasible).

KPIs: bins used, total weight, capacity of the used bins, spare capacity, fill rate, the weight bound
(`min_bins_by_weight`), and the load and items of each used bin.

Solvers: PuLP formulation on HiGHS / SCIP / CBC, plus a native OR-Tools CP-SAT formulation (`build_cpsat`).
CP-SAT needs integers, so after a fractional edit it scales all weights and capacities by one power of ten.

Source: Google OR-Tools `ortools/linear_solver/samples/bin_packing_mip.py` (Apache-2.0). Re-implemented from the
published data; no code copied.
