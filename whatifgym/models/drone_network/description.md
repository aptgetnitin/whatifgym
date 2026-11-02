# Drone-network design for cardiac arrests

**Domain:** supply chain / logistics · **Type:** MILP · **Size:** 966 variables (483 binary), 1,987 constraints · **Sense:** minimise expected response

Drones carrying defibrillators answer out-of-hospital cardiac arrests (OHCAs) in Virginia Beach. Seven candidate
bases (fire stations, rescue squads) and 68 incident locations (69 arrests, 31 May - 29 Jun 2019). Open at most
`max_bases` bases (one drone each) and assign every location to one open base. Each base is an M/G/1 queue:
arrival rate per location = incidents / (24 * observation_days) per hour (rounded to 6 decimals);
service time = maintenance + round-trip flight (2 * distance / speed). A base's utilisation must stay <= 1.
Objective: rate-weighted average over locations of queue wait plus flight time. The fractional, bilinear wait is
linearised with `queue_load[b]` (V) and `linked_load[l, b]` (nu = V * assign, big-M Vbar = 2 * sum of all service
times; Vbar is a structural constant, not data).

Reference optimum (original notebook, Gurobi): **37.3232102** — open 21 MUNICIPAL CTR, 800 VIRGINIA BEACH BLVD,
3769 E. STRATFORD ROAD and 5145 RURITAN COURT. Mean wait 0.26 min, mean flight 2.24 min. The plan is unique.

Notebook quirk kept: the flight term in the objective is `distance_m / speed_kmh` (meters over km/h, i.e.
1000x the hours) while the service time converts to km. So the objective is mostly flight distance, and
`response_objective` is in these mixed units. The KPIs `avg_wait_minutes` / `avg_flight_minutes` are in true minutes.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `bases` | 5145 RURITAN COURT is unavailable; drop all rescue squads. |
| `incidents` | Arrests at 1700 PLEASURE HOUSE RD triple; demand rises 50% everywhere. |
| `params` | Only 3 drones; 5 drones; drones fly at 80 km/h; maintenance takes 40 minutes. |

Source: Gurobi modeling-examples `drone_network/drone_network.ipynb` (Apache-2.0), data after Custodio & Lejeune
(2022, INFORMS J. Computing, github.com/INFORMSJoC/2020.1022) and Lejeune & Margot (2022). Re-implemented from the data.
