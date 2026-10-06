# Battery Scheduling (price arbitrage, storage variant S)

**Domain:** energy and power · **Type:** LP · **Size:** 72 variables, 25 constraints · **Sense:** maximise profit

A battery sits behind a household meter and is run for one day in 24 hourly steps against a tariff that changes
by the hour. Charging buys electricity at that hour's import price (0.14 to 0.40 per kWh, cheapest at night,
dearest in the evening). Discharging sells electricity back at that hour's export price (0.10 flat until noon,
climbing through the afternoon to 0.30 in the evening, with a one-hour peak of 0.40 at 21-22). An hour's export
price is never above its import price, so money is made only by buying in cheap hours and selling in dear ones.
The battery holds 13.5 kWh at most, charges and discharges at up to 5 kW, stores 96 % of the energy it is charged
with and delivers 96 % of the energy it releases (a round trip of about 92 %). It starts the day holding 6 kWh and
must end it holding at least 6 kWh. This variant has no household load and no solar generation: the battery is a
pure arbitrage device.

Decisions per hour: **charge** power, **discharge** power, and the energy **stored** at the end of the hour (`soc`).

Constraints: the stored-energy balance of every hour (it links each hour to the previous one, and the first hour
to the initial charge), the minimum charge at the end of the day, and the variable bounds (capacity, charging
limit, discharging limit).

Reference optimum (original Gurobi notebook, default variant S): **1.56625** per day. The plan buys 7.8125 kWh in
the two cheapest hours (02-04, import price 0.14), which lifts the battery from 6 to 13.5 kWh, and sells 7.2 kWh
in the evening: 5 kW in 21-22, where the export price peaks at 0.40, and 2.2 kWh in a 0.30 hour. That is 2.66 of
export revenue against 1.09375 of import cost. The objective and these totals are unique. The hourly timing is
not: charging can be split freely over 02-03 and 03-04, and the 2.2 kWh can be sold in any of the four 0.30 hours
(19-20, 20-21, 22-23, 23-24), so solvers return different but equally good hourly plans. The scored KPIs are
therefore the profit and the daily totals, never the hourly breakdown.

Modelling notes:
* The notebook's storage variant uses one power bound for charging and discharging (its charge limit, 5 kW).
  Here `max_charge_kw` and `max_discharge_kw` are separate parameters, holding the notebook's two published
  limits (both 5), so the instance is the same and a planner can change them independently.
* The length of a time step (1 hour) is the column `hours.step_hours` and `hours.order` fixes the sequence of
  hours; both are structural, not what-if inputs.
* As in the notebook, nothing forbids charging and discharging in the same hour. It never pays with the base
  prices, but a scenario that puts an hour's export price clearly above its import price makes the model buy
  and sell in that hour to harvest the spread.
* Not ported: the notebook's other two variants. `LG` settles load minus solar generation at the tariff with no
  battery and needs no solver. `LGS` adds the load and PV profiles, grid import and export variables and a
  nonlinear power-law cycling cost, so it is not an LP. Load, PV and the cycling-cost inputs are used only by
  those two variants and are therefore not part of this model's data.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `hours` | The evening export price (18-22) falls 20 %. A cheap night tariff drops the import price in 00-06 to 0.10. The 21-22 peak export price falls to 0.30. A flat feed-in tariff lifts the 00-12 export price from 0.10 to 0.12. |
| `params` | A 20 kWh battery replaces the 13.5 kWh one. The inverter limits charging to 3 kW. Efficiency drops from 0.96 to 0.90 as the battery ages. The battery starts the day at 2 kWh. It must end the day full (13.5 kWh) or with no reserve at all. |

Measures for rules, fixed decisions and objective stages: `charge`, `discharge` and `soc`, each indexed by
`hour` (for example: no charging between 06 and 18, or at most 3 kW exported in 21-22).

Source: Gurobi `modeling-examples/battery_scheduling/battery_scheduling.ipynb` (Apache-2.0), default variant `S`.
Re-implemented from the published data; no code copied.
