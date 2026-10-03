# Electrical Power Generation 2 (thermal plus hydro)

**Domain:** energy and power · **Type:** MILP · **Size:** 75 variables (50 integer, 20 of them binary), 85 constraints · **Sense:** minimise cost

A utility plans which generators to run tomorrow. The day is split into five demand periods of unequal
length (6, 3, 6, 3 and 6 hours) with predicted demand between 15 000 MW (night) and 40 000 MW (the 15-18
peak). There are three types of thermal units (12, 10 and 5 units available). A running unit produces
between its minimum and maximum output and costs a fixed amount per hour, plus a cost per MWh above its
minimum. Starting a unit also costs money. Five units of each type are already running at midnight and
need no start-up.

Two hydro units (900 MW and 1 400 MW) run at fixed output, with a small hourly cost and a start-up cost.
Both start the day switched off. Running them draws the reservoir down by 0.31 and 0.47 m per hour. Water is
pumped back up with electricity, at 3 000 MWh per metre. The pumping power adds to the demand of its
period, and the reservoir must end the day at the level where it started. For reserve, the running thermal
units at full output plus the full output of both hydro units must cover 115 % of predicted demand.

Decisions per period: thermal units **running** per type (`ngen`, integer), their total **output**, units
**started** (`nstart`, integer), each hydro unit **on/off** and **started** (binary), **pumping** power and
the **reservoir level**.

Constraints: units available per type; output between the running units' minimum and maximum; demand
plus pumping met by thermal and hydro output; reserve margin; start-up counting for thermal and hydro
units, linked from period to period; reservoir balance over a cyclic day.

Reference optimum (original Gurobi notebook): **1 000 630**, proven optimal at zero gap. All twelve
Thermal0 units run all day. Thermal1 runs 3 units at night and 9 for the rest of the day. One Thermal2 unit
covers the 15-18 peak. Only HydroB is used, from 15:00 to midnight, and the 12 690 MWh of water it uses
must be pumped back during the day. This commitment and hydro schedule is the only optimal one: the
cheapest plan that differs (HydroA instead of HydroB in the evening) costs 1 000 771, only 141 more. How
the pumping is split across periods has alternative optima (the notebook prints 815/0/950/0/350 MW, a
2026 Gurobi run gives 450/0/1315/0/350 MW), so the reservoir levels vary too.

Modelling notes: the formulation and size are the notebook's. Two of the notebook's fixed assumptions are
now data columns, so a planner can change them:
* `maxstart0 = 5` (thermal units running before the first period, the same number for every type) is
  `thermal_types.units_on_at_start`.
* "Hydro units are off at the start of the day" is `hydro_units.on_at_start = 0`.

The reserve counts every hydro unit's output whether or not it runs, as the notebook does. The reservoir
level is relative: the notebook sets no reservoir limits and no starting level, only non-negativity and the
cyclic end-equals-start condition. To impose a limit, write a DSL rule on the `reservoir_level` measure.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `periods` | Peak demand (15-18) is 10 % higher. Night demand falls to 12 000 MW. The 06-09 morning ramp needs 33 000 MW. |
| `thermal_types` | Two Thermal1 units are out for maintenance (10 to 8 available). Thermal2's start-up cost doubles. A fuel price rise puts Thermal0 at 2.5 per MWh above minimum. Only 2 units of each type are running at midnight. |
| `hydro_units` | HydroB is derated to 1 200 MW. HydroA's start-up cost falls to 500. Drought: drawdown per hour rises 20 %. HydroA is already running at midnight. |
| `params` | The reserve margin rises to 20 %. Pumping becomes less efficient (3 500 MWh per metre). |

Measures for rules, fixed decisions and objective stages: `ngen`, `output` and `nstart` (period, type);
`hydro_on` and `hydro_start` (period, hydro); `pump` and `reservoir_level` (period).

Source: Gurobi `modeling-examples/electrical_power_generation/electrical_power_2.ipynb` (Apache-2.0), after
H. P. Williams, *Model Building in Mathematical Programming*, 5th ed., example 16. Re-implemented from the
published data; no code copied.
