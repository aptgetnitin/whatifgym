# Power generation schedule (unit commitment with health costs)

**Domain:** energy and power · **Type:** MILP · **Size:** 960 variables (720 binary), 1 722 constraints · **Sense:** minimise cost

A utility schedules the power plants of the U.S. state of Georgia for one summer day (1 July 2011, 24
hours). Demand runs from 7 309 MWh (hour 8) to 12 583 MWh (hour 20), 239 001 MWh in the day. Ten plants or
plant groups have 16 601 MWh per hour of capacity: coal plants Scherer, Bowen and Jack McDonough, a merged
OTHER COAL group, nuclear plants Edwin I Hatch and Vogtle, and merged OIL, BIOMASS, GAS and HYDRO groups.

Each hour, generation must equal demand. A plant that is on generates between its minimum output fraction
of capacity (80 % nuclear, 1 % others) and its capacity; a plant that is off generates nothing. The nuclear
plants must run every hour. From one hour to the next a plant's output may change by at most its ramp
fraction of capacity (20 % nuclear, 25 % coal, no limit for the others). Costs depend on the plant's fuel:
a fuel cost per MWh, an operating cost per hour on, and a cost per start-up and per shut-down. The three
named coal plants also have an hourly health cost per MWh, higher in the evening.

Decisions per plant and hour: **output** (MWh), **on** (binary), **start** and **stop** (binary switch-on and
switch-off).

Reference optimum (original Gurobi notebook): **4 495 153.46**, proven at zero gap: fuel 4 293 478.55,
health 199 614.18, operating 1 622.73, start-ups 219, shut-downs 219. Bowen and Jack McDonough stay off.
OTHER COAL is off in hours 3-13 and GAS in hours 8-9. The total, its five parts, each plant's generation
and hours on are the same in every optimal plan. The next-best plan costs only 61.47 more (OTHER COAL
back on in hour 13).

Modelling notes: the formulation and size are the notebook's. Its fixed assumptions are data here: the
minimum output and ramp fractions (`plants`), the nuclear must-run rule (`plants.must_run`), and shut-down
cost = start-up cost (`fuels.shutdown_cost`). As in the notebook, hour 1 has no ramp or switch link to a
previous day: each plant's on/off state in hour 1 is free and costs no start-up. Health costs are the published 1 July 2007 values
(the notebook picks day 1 of the July 2007 health data); fuel and operating costs are 2011 averages. The OIL group burns
fuel BLQ (black liquor), as in the source data.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `hours` | A heat wave raises evening demand (hours 17-22) by 10 %. Demand at hour 20 reaches 13 500 MWh. |
| `plants` | Vogtle is down to half capacity. Scherer is offline (capacity 0). Coal may ramp only 15 % of capacity per hour. |
| `fuels` | Natural gas costs 50 % more. Coal (BIT) start-ups cost 500. Nuclear fuel costs 9 per MWh. |
| `health_costs` | Bowen's evening health cost doubles. Health costs are counted at half weight. |

Measures for rules, fixed decisions and objective stages: `output`, `on`, `start` and `stop` (plant, hour).
To let a nuclear plant switch off, relax the `must_run` constraints.

Source: Gurobi `modeling-examples/power_generation/optimize_power_schedule.ipynb` (Apache-2.0), data from
`demand.csv` and `small_plant_data/` in the same folder. Re-implemented from the published data; no code copied.
