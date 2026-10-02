# Base models (30)

Public, permissively licensed optimization models with named data tables, 50 to 5 000 variables and an open-solver solve time under 2 s. Every number was **measured** on 2026-10-02 by running the original public implementation and then timing an open solver on the same model (see `scripts/build_base_model_table.py` for the exact method per source). Times are single-run wall-clock seconds on one sandbox CPU core and are indicative only. Three models are already ported into `whatifgym/models/`; the rest are the Phase 1-2 porting queue.

Domains: Supply chain & logistics (4), Production planning (5), Scheduling (workforce, machines, projects) (5), Energy & power (4), Packing, assignment & covering (4), Network & routing (4), Revenue & resource planning (4).

## Supply chain & logistics

| # | model | type | vars | cons | int | open solver | time (s) | reference objective | licence | what-if hooks |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [COVID-19 healthcare facility capacity optimization](https://github.com/Gurobi/modeling-examples/blob/master/covid19_facility_location/covid19_facility_location.ipynb)<br>`gurobi_covid19_facility_location` | MILP | 225 | 32 | 9 | HiGHS | 0.180 | 1.52165e+06 | Apache-2.0 | County demand forecasts, existing facility capacities, candidate temporary facility fixed costs and capacities, cost per mile (notebook also runs a +20% demand scenario) |
| 2 | [Customer assignment (facility location with clustered demand)](https://github.com/Gurobi/modeling-examples/blob/master/customer_assignment/customer_assignment.ipynb)<br>`gurobi_customer_assignment` | IP | 993 | 1024 | 993 | HiGHS | 0.022 | 5,815.04 | Apache-2.0 | Customer locations (pre-clustered with k-means), candidate facility sites, maximum facilities to open, distance threshold |
| 3 | [Drone-network design for out-of-hospital cardiac arrests](https://github.com/Gurobi/modeling-examples/blob/master/drone_network/drone_network.ipynb)<br>`gurobi_drone_network` | MILP | 966 | 1987 | 483 | HiGHS | 0.048 | 37.3232 | Apache-2.0 | Candidate drone bases, demand points and base-to-demand distances, response-time threshold, number of drones/bases to deploy |
| 4 | [Food supply chain for humanitarian aid (World Food Programme case)](https://github.com/Gurobi/modeling-examples/blob/master/food_program/food_supply.ipynb)<br>`gurobi_food_supply` | LP | 1397 | 437 | 0 | HiGHS | 0.025 | 4.00812e+08 | Apache-2.0 | Nutrient requirements, commodity nutritional values, procurement prices per supplier, transport cost per arc, beneficiaries per city |

## Production planning

| # | model | type | vars | cons | int | open solver | time (s) | reference objective | licence | what-if hooks |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | [Factory Planning I](https://github.com/Gurobi/modeling-examples/blob/master/factory_planning/factory_planning_1.ipynb)<br>`gurobi_factory_planning_1` **(ported)** | LP | 126 | 79 | 0 | HiGHS | 0.003 | 93,715.2 | Apache-2.0 | Monthly market limits per product, machine hours per product, maintenance (machines down) table, profit contributions, storage cost, end stock target |
| 6 | [Factory Planning II (maintenance schedule as a decision)](https://github.com/Gurobi/modeling-examples/blob/master/factory_planning/factory_planning_2.ipynb)<br>`gurobi_factory_planning_2` | MILP | 156 | 84 | 30 | HiGHS | 0.017 | 108,855 | Apache-2.0 | Same tables as Factory Planning I plus the number of machines of each type that must undergo maintenance in the horizon |
| 7 | [Food Manufacture I (oil blending and purchasing)](https://github.com/Gurobi/modeling-examples/blob/master/food_manufacturing/food_manufacture_1.ipynb)<br>`gurobi_food_manufacture_1` | LP | 96 | 70 | 0 | HiGHS | 0.002 | 107,843 | Apache-2.0 | Monthly oil purchase prices, hardness values, refining capacities, storage capacity and cost, product price, hardness bounds |
| 8 | [Farm Planning (multi-year herd, crop and capital plan)](https://github.com/Gurobi/modeling-examples/blob/master/farm_planning/farm_planning.ipynb)<br>`gurobi_farm_planning` | LP | 131 | 116 | 0 | HiGHS | 0.002 | 121,719 | Apache-2.0 | Land area, herd dynamics, yields and prices, labour hours per activity, capital and loan limits, housing capacity |
| 9 | [Mining (multi-year mine operation and blending)](https://github.com/Gurobi/modeling-examples/blob/master/mining/mining.ipynb)<br>`gurobi_mining` | MILP | 65 | 71 | 40 | HiGHS | 0.123 | 1.46862e+08 | Apache-2.0 | Per-mine royalty, extraction capacity and ore quality, yearly blended-quality targets, selling price, discount rate, maximum mines operated per year |

## Scheduling (workforce, machines, projects)

| # | model | type | vars | cons | int | open solver | time (s) | reference objective | licence | what-if hooks |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | [Manpower Planning (recruitment, retraining, redundancy over 3 years)](https://github.com/Gurobi/modeling-examples/blob/master/manpower_planning/manpower_planning.ipynb)<br>`gurobi_manpower_planning` | LP | 72 | 30 | 0 | HiGHS | 0.001 | 841.8 | Apache-2.0 | Yearly manpower requirements per skill level, attrition rates, recruitment caps, retraining capacities and costs, redundancy/overmanning/short-time costs |
| 11 | [Job-shop scheduling, Fisher-Thompson 6x6 instance](https://github.com/google/or-tools/blob/stable/examples/python/jobshop_ft06_sat.py)<br>`ortools_jobshop_ft06_sat` | CP-SAT | 73 | 73 | 73 | CP-SAT | 0.021 | 55 | Apache-2.0 | Job routings, processing times, machine availability; makespan objective |
| 12 | [Flexible job-shop scheduling](https://github.com/google/or-tools/blob/stable/examples/python/flexible_job_shop_sat.py)<br>`ortools_flexible_job_shop_sat` | CP-SAT | 109 | 136 | 109 | CP-SAT | 0.029 | 6 | Apache-2.0 | Alternative machines per task with different durations, job routings; makespan objective |
| 13 | [Single machine scheduling with setup times, release and due dates](https://github.com/google/or-tools/blob/stable/examples/python/single_machine_scheduling_with_setup_release_due_dates_sat.py)<br>`ortools_single_machine_scheduling_sat` | CP-SAT | 271 | 245 | 271 | CP-SAT | 0.271 | 112,605 | Apache-2.0 | Job durations, release dates, due dates, sequence-dependent setup matrix; weighted lateness objective |
| 14 | [Task allocation to time slots with capacity](https://github.com/google/or-tools/blob/stable/examples/python/task_allocation_sat.py)<br>`ortools_task_allocation_sat` | CP-SAT | 2552 | 2651 | 2552 | CP-SAT | 0.938 | 17 | Apache-2.0 | Task-to-slot eligibility table, per-slot capacity; minimise number of slots used |

## Energy & power

| # | model | type | vars | cons | int | open solver | time (s) | reference objective | licence | what-if hooks |
|---|---|---|---|---|---|---|---|---|---|---|
| 15 | [Battery scheduling against hourly prices with PV and load](https://github.com/Gurobi/modeling-examples/blob/master/battery_scheduling/battery_scheduling.ipynb)<br>`gurobi_battery_scheduling` | LP | 72 | 25 | 0 | HiGHS | 0.001 | 1.56625 | Apache-2.0 | Hourly import/export prices, load and PV profiles, battery energy capacity, charge/discharge limits and efficiencies, cycling cost |
| 16 | [Electrical Power Generation 2 (thermal units plus pumped hydro)](https://github.com/Gurobi/modeling-examples/blob/master/electrical_power_generation/electrical_power_2.ipynb)<br>`gurobi_electrical_power_2` | MILP | 75 | 85 | 50 | HiGHS | 0.155 | 1.00063e+06 | Apache-2.0 | Demand per period, generator min/max output, running and startup costs, hydro output and reservoir depletion, pumping efficiency |
| 17 | [Power generation schedule (unit commitment with startup and health costs)](https://github.com/Gurobi/modeling-examples/blob/master/power_generation/optimize_power_schedule.ipynb)<br>`gurobi_optimize_power_schedule` | MILP | 960 | 1722 | 720 | HiGHS | 0.047 | 4.49515e+06 | Apache-2.0 | Hourly demand curve, plant capacities, fuel, operating, startup and health-cost tables (small_plant_data/; a large variant ships too) |
| 18 | [PyPSA unit commitment example (two generators, 30 snapshots)](https://github.com/PyPSA/PyPSA/blob/master/docs/examples/unit-commitment.ipynb)<br>`pypsa_unit_commitment` | MILP | 240 | 598 | 180 | HiGHS (linopy) | 0.013 | 2.22745e+06 | MIT (code); CC-BY-4.0 (notebook) | Load profile, generator marginal and startup costs, min up/down times, ramp limits, minimum stable output |

## Packing, assignment & covering

| # | model | type | vars | cons | int | open solver | time (s) | reference objective | licence | what-if hooks |
|---|---|---|---|---|---|---|---|---|---|---|
| 19 | [Multiple knapsack](https://github.com/google/or-tools/blob/stable/ortools/sat/samples/multiple_knapsack_sat.py)<br>`ortools_multiple_knapsack` **(ported)** | IP | 75 | 20 | 75 | HiGHS / CP-SAT | 0.064 | 395 | Apache-2.0 | Item weights and values, bin capacities, number of bins |
| 20 | [Bin packing (minimise bins used)](https://github.com/google/or-tools/blob/stable/ortools/linear_solver/samples/bin_packing_mip.py)<br>`ortools_bin_packing_mip` | IP | 132 | 22 | 132 | SCIP (pywraplp) | 0.005 | 4 | Apache-2.0 | Item weights, bin capacity, number of candidate bins |
| 21 | [Wedding seating as set partitioning](https://github.com/coin-or/pulp/blob/master/examples/wedding.py)<br>`pulp_wedding_seating` **(ported)** | IP | 3213 | 18 | 3213 | HiGHS | 0.334 | 12 | MIT | Guest list and ranks, maximum tables, maximum table size |
| 22 | [Assignment with group constraints](https://github.com/google/or-tools/blob/stable/examples/python/assignment_with_constraints_sat.py)<br>`ortools_assignment_with_constraints_sat` | CP-SAT | 84 | 33 | 84 | CP-SAT | 0.027 | 239 | Apache-2.0 | Worker-task cost matrix, allowed group combinations (table constraints), tasks per worker |

## Network & routing

| # | model | type | vars | cons | int | open solver | time (s) | reference objective | licence | what-if hooks |
|---|---|---|---|---|---|---|---|---|---|---|
| 23 | [Technician routing and scheduling](https://github.com/Gurobi/modeling-examples/blob/master/technician_routing_scheduling/technician_routing_scheduling.ipynb)<br>`gurobi_technician_routing_scheduling` | MILP | 660 | 217 | 630 | HiGHS | 0.092 | 12,410 | Apache-2.0 | Technician skills, capacities and depots; job durations, priorities and time windows; distance matrix (Excel scenarios Sce0/Sce3) |
| 24 | [Railway dispatching (rescheduling trains after a delay)](https://github.com/Gurobi/modeling-examples/blob/master/railway_dispatching/railway_dispatching.ipynb)<br>`gurobi_railway_dispatching` | MILP | 218 | 367 | 180 | HiGHS | 0.562 | 47 | Apache-2.0 | Train timetable, track-segment occupancy, minimum headways, delay scenario |
| 25 | [Airline planning after flight disruption](https://github.com/Gurobi/modeling-examples/blob/master/aviation_planning/airlineplanning.ipynb)<br>`gurobi_airline_planning` | IP | 1930 | 536 | 1930 | HiGHS | 0.027 | 561,087 | Apache-2.0 | Flight rotation schedule, aircraft start/end positions, itinerary revenues (CSV files in data/) |
| 26 | [Travelling salesman with the circuit constraint (40 cities)](https://github.com/google/or-tools/blob/stable/examples/python/tsp_sat.py)<br>`ortools_tsp_sat` | CP-SAT | 1560 | 1 | 1560 | CP-SAT | 0.582 | 216,449 | Apache-2.0 | Distance matrix (fixed in the script); forbid or force arcs, add cities |

## Revenue & resource planning

| # | model | type | vars | cons | int | open solver | time (s) | reference objective | licence | what-if hooks |
|---|---|---|---|---|---|---|---|---|---|---|
| 27 | [Economic Planning (input-output model with capacity building)](https://github.com/Gurobi/modeling-examples/blob/master/economic_planning/economic_planning.ipynb)<br>`gurobi_economic_planning` | LP | 51 | 33 | 0 | HiGHS | 0.001 | 1,902.22 | Apache-2.0 | Input-output coefficients between industries, capacity-building coefficients, exogenous demand, initial stocks and capacities, manpower limits |
| 28 | [Fantasy basketball line-up under a salary cap (part 1)](https://github.com/Gurobi/modeling-examples/blob/master/fantasy_basketball/fantasy_basketball_part1.ipynb)<br>`gurobi_fantasy_basketball_1` | IP | 96 | 97 | 96 | HiGHS | 0.017 | 171.92 | Apache-2.0 | Predicted points per player, salaries, salary cap, position requirements |
| 29 | [Car Rental 1 (fleet positioning, transfers and repairs)](https://github.com/Gurobi/modeling-examples/blob/master/car_rental/car_rental_1.ipynb)<br>`gurobi_car_rental_1` | LP | 289 | 97 | 0 | HiGHS | 0.003 | 121,160 | Apache-2.0 | Daily rental demand per depot, price by rental length, return-depot shares, damage rates and repair capacities, transfer costs |
| 30 | [Car Rental 2 (adds repair-capacity expansion decisions)](https://github.com/Gurobi/modeling-examples/blob/master/car_rental/car_rental_2.ipynb)<br>`gurobi_car_rental_2` | MILP | 294 | 118 | 5 | HiGHS | 0.020 | 132,341 | Apache-2.0 | Same tables as Car Rental 1 plus repair-capacity expansion options and costs |

## Notes per model

1. `gurobi_covid19_facility_location` — Base scenario (solve 1 of 2 in the notebook).
2. `gurobi_customer_assignment` — Customer coordinates are generated with a fixed seed; the k-means preprocessing (scikit-learn) must be frozen into the data tables when porting.
3. `gurobi_drone_network` — Reads three CSV files shipped in the example folder.
4. `gurobi_food_supply` — Reads seven CSV files shipped in the example folder.
5. `gurobi_factory_planning_1` — PORTED: whatifgym/models/factory_planning (verified on HiGHS, SCIP, CBC, Gurobi).
7. `gurobi_food_manufacture_1` — Food Manufacture II adds logical (indicator) constraints that the LP-file route could not read in HiGHS; port directly if wanted.
10. `gurobi_manpower_planning` — Objective here is minimum redundancy (the notebook's first objective).
11. `ortools_jobshop_ft06_sat` — Interval/no-overlap model; a MIP port needs disjunctive big-M constraints.
13. `ortools_single_machine_scheduling_sat` — Run with the script's default flags.
14. `ortools_task_allocation_sat` — Largest CP-SAT model in the shortlist; still under one second.
15. `gurobi_battery_scheduling` — Default variant 'S'; the 'LGS' variant adds indicator constraints.
16. `gurobi_electrical_power_2` — Part 1 (45 variables) is just below the size floor.
17. `gurobi_optimize_power_schedule` — Reads CSV files from the example folder.
18. `pypsa_unit_commitment` — Data is inline in the notebook; the 4-snapshot variant is too small (32 variables).
19. `ortools_multiple_knapsack` — PORTED: whatifgym/models/multiple_knapsack (verified on HiGHS, SCIP, CBC, CP-SAT, Gurobi).
21. `pulp_wedding_seating` — PORTED: whatifgym/models/wedding_seating (verified on HiGHS, SCIP, CBC, CP-SAT).
22. `ortools_assignment_with_constraints_sat` — Uses table constraints; a MIP port enumerates the allowed combinations.
23. `gurobi_technician_routing_scheduling` — Objective for scenario Sce3 (Sce0 has objective 0). Data is an Excel workbook in the example folder.
25. `gurobi_airline_planning` — Notebook needs a one-line pandas-3 compatibility patch (groupby().apply(list)).
26. `ortools_tsp_sat` — Gurobi's tsp.ipynb uses lazy subtour cuts and is deferred until a cut loop exists on open solvers.
27. `gurobi_economic_planning` — Objective of the notebook's second model (maximise total production); the first model is 3 variables.
28. `gurobi_fantasy_basketball_1` — Predicted points come from a regression step in the notebook; freeze them into the data table when porting.

## Deferred candidates

Measured but kept out of the 30 for the stated reason; several are one fix away.

| id | why deferred | source |
|---|---|---|
| `gurobi_supply_network_design_2` | 49 variables (one below the floor); otherwise ideal S&OP model | [link](https://github.com/Gurobi/modeling-examples/blob/master/supply_network_design/supply_network_design_2.ipynb) |
| `gurobi_workforce_scheduling` | hierarchical two-objective model; needs a lexicographic two-solve port before timing on open solvers | [link](https://github.com/Gurobi/modeling-examples/blob/master/workforce/workforce_scheduling.ipynb) |
| `gurobi_tsp` | 1128 binaries; lazy subtour cuts via callback; needs a DFJ cut loop on open solvers | [link](https://github.com/Gurobi/modeling-examples/blob/master/traveling_salesman/tsp.ipynb) |
| `gurobi_milk_collection` | 442 binaries; same lazy-cut issue as tsp | [link](https://github.com/Gurobi/modeling-examples/blob/master/milk_collection/milk_collection.ipynb) |
| `gurobi_lost_luggage_distribution` | 1747 binaries; hierarchical objectives | [link](https://github.com/Gurobi/modeling-examples/blob/master/lost_luggage_distribution/lost_luggage_distribution.ipynb) |
| `ortools_shift_scheduling_sat` | 1462 booleans; CP-SAT 2.8 s with 8 workers (just over the 2 s bar) | [link](https://github.com/google/or-tools/blob/stable/examples/python/shift_scheduling_sat.py) |
| `ortools_wedding_optimal_chart_sat` | 901 booleans, 1.0 s; near-duplicate of pulp_wedding_seating | [link](https://github.com/google/or-tools/blob/stable/examples/python/wedding_optimal_chart_sat.py) |
| `egret_tiny_uc_2` | BSD-3; 1203 variables; SCIP 0.7 s but HiGHS 2.0 s; needs the Egret package | [link](https://github.com/grid-parity-exchange/Egret/blob/main/egret/models/tests/uc_test_instances/tiny_uc_2.json) |
| `switch_3zone_toy` | Apache-2.0; 618 variables, 0.009 s; needs the Switch package and its input-directory format | [link](https://github.com/switch-model/switch/tree/master/examples/3zone_toy) |
| `pso_economic_dispatch_24h` | 600 variables, 0.003 s; course material under CC-BY-4.0 (data) and MIT (code) | [link](https://github.com/east-winds/power-systems-optimization/blob/master/Notebooks/04-Economic-Dispatch.ipynb) |

## Licences

Gurobi modeling-examples and Google OR-Tools: Apache-2.0. PuLP: MIT. PyPSA: MIT code, CC-BY-4.0 notebook content. The what-if benchmark reuses only published data values and re-implements each model; see `ATTRIBUTION.md`.
