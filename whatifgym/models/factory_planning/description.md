# Factory Planning I

**Domain:** production planning · **Type:** LP · **Size:** 126 variables, 79 constraints · **Sense:** maximise profit

A factory makes seven products on five machine types (grinders, vertical drills, horizontal drills, a borer, a
planer) over a six-month horizon. Each product earns a fixed profit contribution per unit sold and needs a known
number of hours on some of the machines. Every month some machines are down for maintenance, and the market caps
how many units of each product can be sold. Up to 100 units of each product can be carried in stock at a holding
cost per unit-month, and the plan must end with 50 units of every product in stock.

Decisions per month and product: how much to **make**, **sell** and **store**.

Constraints: inventory balance (opening stock + production = sales + closing stock, zero opening stock),
end-of-horizon stock target, machine-hour capacity per machine type and month net of maintenance, and the
per-month market limit on sales (a variable bound).

Reference optimum (original Gurobi notebook): **93 715.18**.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `max_sales` | Demand for Prod5 in May drops 20 % — what happens to profit? Which products lose volume? |
| `downtime` | The grinder maintenance moves from January to March; a second borer outage in June. |
| `machines` | We buy a second borer. We retire one grinder. |
| `process_hours` | A process improvement cuts Prod3 horizontal-drill time from 0.8 h to 0.6 h. |
| `products` | Prod7's margin falls to 2; a price rise lifts Prod1's contribution to 12. |
| `params` | Holding cost doubles; warehouse limit becomes 150; no end-of-horizon stock target. |

Source: Gurobi `modeling-examples/factory_planning/factory_planning_1.ipynb` (Apache-2.0), after
H. P. Williams, *Model Building in Mathematical Programming*, 5th ed., example 3. Re-implemented from the
published data; no code copied.
