# Factory Planning II

**Domain:** production planning · **Type:** MILP · **Size:** 156 variables (30 integer), 84 constraints · **Sense:** maximise profit

A factory makes seven products on five machine types (four grinders, two vertical drills, three horizontal
drills, a borer, a planer) over a six-month horizon. Each product earns a fixed profit contribution per unit sold
and needs a known number of hours on some of the machines. The market caps how many units of each product can be
sold each month. Up to 100 units of each product can be carried in stock at a holding cost per unit-month, and the
plan must end with 50 units of every product in stock.

Unlike Factory Planning I, the maintenance calendar is not given; it is decided together with the production
plan. Every machine must be down for maintenance in one of the six months, except the grinders, of which only two
of the four need maintenance. Several machines may be serviced in the same month, and a machine under maintenance
provides no hours that month. The number of machines installed and the number needing maintenance are separate
inputs: buying a machine does not by itself add a maintenance requirement.

Decisions per month and product: how much to **make**, **sell** and **store**. Per month and machine type: how
many machines to take down for maintenance (**repair**, an integer).

Constraints: inventory balance (opening stock + production = sales + closing stock, zero opening stock),
end-of-horizon stock target, machine-hour capacity per machine type and month net of the machines down for
maintenance, the maintenance requirement per machine type (the monthly counts add up to the required number), and
the per-month market limit on sales (a variable bound).

Reference optimum (original Gurobi notebook): **108 855**, which is 15 139.82 more than Factory Planning I with its
fixed calendar. The profit is unique but the maintenance calendar is not: different solvers return different
months at the same profit, so compare plans by profit, cost parts and volumes, not month by month.

Formulation note: the notebook passes the `repair` upper bound as a dict keyed by machine type, which gurobipy
silently ignores for variables indexed by (month, machine). This port applies the documented bound
0..`machines_to_maintain`. The maintenance equality implies that bound, so the optimum and model size are the
same.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `maintenance` | A third grinder must also be serviced this half-year. The planer's service is deferred to next half-year (no planer maintenance). |
| `max_sales` | Demand for Prod5 in May drops 20 %. Does the maintenance plan move, and what happens to profit? |
| `machines` | We buy a second borer. We retire one grinder. |
| `process_hours` | A process improvement cuts Prod3 horizontal-drill time from 0.8 h to 0.6 h. |
| `products` | Prod7's margin falls to 2; a price rise lifts Prod1's contribution to 12. |
| `params` | Holding cost doubles; warehouse limit becomes 150; no end-of-horizon stock target; a third shift. |

Questions about *when* maintenance happens act on the `repair` decision rather than on a table. "The grinders
must be serviced in January" fixes `repair` for grinder in Jan at 2. "No maintenance in June" fixes `repair` in
Jun at 0. "At most two machines down in April" is a rule on the sum of `repair` over April.

Source: Gurobi `modeling-examples/factory_planning/factory_planning_2.ipynb` (Apache-2.0), after
H. P. Williams, *Model Building in Mathematical Programming*, 5th ed., example 4. Re-implemented from the
published data; no code copied.
