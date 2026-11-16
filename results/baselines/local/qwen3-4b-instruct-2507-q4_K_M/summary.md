# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | chained_scenario (nl) | data_change | data_change (nl) | fixed_decision | fixed_decision (nl) | infeasible_request | infeasible_request (nl) | logical_rule | logical_rule (nl) | new_limit | new_limit (nl) | objective_change | objective_change (nl) | relative_rule | relative_rule (nl) | relax_remove | relax_remove (nl) | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:4b-instruct-2507-q4_K_M` | 4636 | 0.441 | 0.502 | 0.67 | 0.92 | 0.64 (469) | 0.52 (132) | 0.67 (512) | 0.69 (150) | 0.57 (423) | 0.53 (116) | 0.43 (324) | 0.46 (82) | 0.14 (381) | 0.14 (126) | 0.70 (375) | 0.53 (118) | 0.46 (217) | 0.46 (50) | 0.10 (427) | 0.07 (110) | 0.55 (108) | 0.67 (30) | 0.20 (486) | 0.52 (575) | 0.40 (2647) | 0.49 (1414) | 7.5 |

## By base model

| base model | `ollama/qwen3:4b-instruct-2507-q4_K_M` |
|---|---|
| `airline_planning` | 0.20 (181) |
| `assignment_with_constraints` | 0.53 (148) |
| `battery_scheduling` | 0.40 (217) |
| `bin_packing` | 0.49 (86) |
| `car_rental` | 0.49 (191) |
| `car_rental_2` | 0.40 (250) |
| `covid19_facility_location` | 0.50 (219) |
| `drone_network` | 0.42 (183) |
| `economic_planning` | 0.50 (220) |
| `factory_planning` | 0.54 (275) |
| `factory_planning_2` | 0.46 (216) |
| `fantasy_basketball` | 0.50 (105) |
| `farm_planning` | 0.54 (226) |
| `food_manufacture` | 0.52 (210) |
| `food_supply` | 0.49 (196) |
| `jobshop_ft06` | 0.55 (195) |
| `manpower_planning` | 0.34 (258) |
| `mining` | 0.36 (223) |
| `multiple_knapsack` | 0.41 (132) |
| `optimize_power_schedule` | 0.46 (182) |
| `power_generation_hydro` | 0.48 (220) |
| `railway_dispatching` | 0.23 (217) |
| `single_machine_scheduling` | 0.55 (55) |
| `technician_routing_scheduling` | 0.38 (196) |
| `wedding_seating` | 0.34 (35) |

## By template (where the misses are)

### `ollama/qwen3:4b-instruct-2507-q4_K_M`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | result differs from reference |
| data_change | outage | 0.00 (4) | invalid DSL: row is missing columns ['machines_down'] |
| data_change (nl) | outage | 0.00 (2) | invalid DSL: no row of 'downtime' matches {"machine": "vertDrill", "month": "Jan"} |
| infeasible_request (nl) | i_floor_total | 0.00 (8) | invalid DSL: 'all' is not a camp; known values: ['Ar Raqqa', 'Daraa', 'Dayr_Az_Zor', 'Hassake |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| new_limit (nl) | cap_store_month | 0.00 (2) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| objective_change (nl) | o_reorder | 0.00 (4) | invalid DSL: '{"sense":"min","measure":"response_objective","scope":{"location":"location"}}' |
| relative_rule (nl) | r_share_of_total | 0.00 (40) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| relax_remove | combo | 0.00 (6) | unparseable output |
| relax_remove (nl) | combo | 0.00 (4) | invalid DSL: 'constraint' is not of type 'object' |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_store_month | 0.00 (1) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| under_specified | ask_cap_total_store | 0.00 (2) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| under_specified | ask_demand_zero | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_param | 0.00 (41) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| under_specified | ask_install | 0.00 (1) | needed clarification not asked |
| under_specified | ask_margin_scale | 0.00 (1) | invalid scenario |
| under_specified | ask_margin_set | 0.00 (1) | needed clarification not asked |
| under_specified | ask_outage | 0.00 (1) | invalid DSL: row is missing columns ['machines_down'] |
| under_specified | ask_outage_cancel | 0.00 (1) | needed clarification not asked |
| under_specified | ask_retire | 0.00 (2) | result differs from reference |
| relative_rule | r_share_of_total | 0.03 (146) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| logical_rule | l_never_both | 0.04 (48) | invalid DSL: [{'measure': 'operate', 'scope': {'flight': ['4563', '3103']}, 'sense': '==', 'v |
| infeasible_request | i_floor_total | 0.04 (45) | invalid DSL: '*' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', 'Tu |
| relative_rule (nl) | combo | 0.07 (28) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| relative_rule | r_two_values | 0.08 (136) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| under_specified | ask_g_cap_measure_total | 0.09 (45) | invalid DSL: [] is not valid under any of the given schemas: [] should be non-empty |
| logical_rule (nl) | l_at_most_k | 0.09 (32) | invalid DSL: unknown table 'works'; tables are ['allowed_teams', 'costs', 'tasks', 'workers'] |
| logical_rule | l_if_then | 0.10 (103) | invalid DSL: '>' is not one of ['<=', '>=', '=='] |
| logical_rule (nl) | l_if_then | 0.11 (38) | invalid DSL: '>' is not one of ['<=', '>=', '=='] |
| logical_rule | l_at_most_k | 0.11 (108) | invalid DSL: '4572' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| relative_rule | r_two_measures | 0.12 (52) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| relative_rule (nl) | r_two_values | 0.12 (32) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| under_specified | ask_g_remove_row | 0.15 (33) | needed clarification not asked |
| data_change | g_param | 0.17 (60) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| under_specified | ask_g_set_column | 0.18 (84) | needed clarification not asked |
| under_specified | ask_g_scale_column | 0.18 (77) | needed clarification not asked |
| objective_change | o_reorder | 0.19 (48) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| logical_rule (nl) | l_none_or_batch | 0.19 (42) | invalid DSL: unknown table 'soc'; tables are ['hours'] |
| new_limit | cap_total_make | 0.20 (5) | result differs from reference |
| objective_change | o_then_min | 0.20 (10) | invalid DSL: '*' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', 'Tu |
| relative_rule (nl) | r_two_measures | 0.20 (10) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| logical_rule (nl) | l_never_both | 0.21 (14) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| objective_change (nl) | o_then_max | 0.21 (14) | result differs from reference |
| relative_rule | combo | 0.22 (93) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| under_specified | ask_g_scale_all_rows | 0.22 (77) | unparseable output |
| chained_scenario (nl) | c_add | 0.24 (62) | result differs from reference |
| logical_rule | l_none_or_batch | 0.25 (122) | result differs from reference |
| data_change (nl) | g_param | 0.25 (20) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| new_limit (nl) | cap_total_make | 0.25 (4) | result differs from reference |
| under_specified | ask_g_add_row | 0.29 (17) | invalid DSL: row is missing columns ['weight'] |
| fixed_decision (nl) | f_fix_scope | 0.32 (22) | invalid DSL: unknown table 'undamaged_left'; tables are ['days', 'demand', 'depots', 'rental_ |
| data_change | retire | 0.33 (3) | result differs from reference |
| under_specified | ask_demand_scale | 0.33 (3) | needed clarification not asked |
| under_specified | ask_g_floor_measure_scope | 0.34 (44) | needed clarification not asked |
| infeasible_request | i_two_floors | 0.34 (58) | invalid DSL: unknown table 'soc'; tables are ['hours'] |
| objective_change | o_then_max | 0.35 (23) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| under_specified | ask_g_cap_measure_scope | 0.35 (48) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| chained_scenario | c_add | 0.36 (174) | result differs from reference |
| data_change | param | 0.40 (5) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| fixed_decision | f_fix_scope | 0.40 (67) | invalid DSL: unknown table 'rentals'; tables are ['days', 'demand', 'depots', 'rental_lengths |
| infeasible_request (nl) | i_floor | 0.42 (26) | invalid DSL: unknown table 'repairs'; tables are ['days', 'demand', 'depots', 'expansion_opti |
| relax_remove | x_full | 0.44 (16) | invalid DSL: 'worker' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'w |
| infeasible_request | i_floor | 0.47 (88) | invalid DSL: '*' is not a depot; known values: ['Birmingham', 'Glasgow', 'Manchester', 'Plymo |
| new_limit (nl) | g_cap_measure_total | 0.47 (30) | invalid DSL: 'flight' is not a flight; known values: ['1', '10', '100', '101', '102', '103',  |
| fixed_decision (nl) | f_fix_zero | 0.47 (34) | invalid DSL: unknown table 'operate'; tables are ['aircraft', 'airports', 'flights'] |
| fixed_decision (nl) | f_force_one | 0.50 (16) | invalid DSL: unknown table 'assign'; tables are ['allowed_teams', 'costs', 'tasks', 'workers' |
| infeasible_request (nl) | i_two_floors | 0.50 (12) | result differs from reference |
| objective_change | o_three_stages | 0.50 (40) | invalid DSL: [{'sense': 'max', 'measure': 'original'}, {'sense': 'max', 'measure': 'charge',  |
| fixed_decision | f_force_one | 0.51 (67) | invalid DSL: '4694' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| fixed_decision | f_fix_zero | 0.52 (122) | invalid DSL: unknown table 'operate'; tables are ['aircraft', 'airports', 'flights'] |
| data_change | combo | 0.53 (114) | result differs from reference |
| new_limit (nl) | combo | 0.56 (32) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| new_limit (nl) | g_floor_measure_scope | 0.57 (30) | result differs from reference |
| infeasible_request | i_commit | 0.58 (133) | invalid DSL: unknown table 'soc'; tables are ['hours'] |
| fixed_decision (nl) | f_fix_level | 0.58 (24) | result differs from reference |
| infeasible_request (nl) | i_commit | 0.58 (36) | invalid DSL: unknown table 'soc'; tables are ['hours'] |
| objective_change (nl) | o_three_stages | 0.60 (10) | invalid DSL: [{'sense': 'max', 'measure': 'original'}, {'sense': 'max', 'measure': 'charge',  |
| relax_remove | x_scoped | 0.60 (86) | result differs from reference |
| objective_change (nl) | o_then_scoped | 0.61 (18) | result differs from reference |
| new_limit | g_cap_measure_total | 0.62 (87) | invalid DSL: 'flight' is not a flight; known values: ['1', '10', '100', '101', '102', '103',  |
| chained_scenario (nl) | c_undo | 0.63 (30) | invalid DSL: unknown table 'soc'; tables are ['hours'] |
| objective_change | o_then_scoped | 0.64 (96) | result differs from reference |
| data_change (nl) | combo | 0.64 (36) | result differs from reference |
| fixed_decision | combo | 0.65 (82) | result differs from reference |
| new_limit (nl) | g_cap_measure_scope | 0.65 (20) | invalid DSL: 'aircraft' is a key column of 'aircraft'; keys cannot be edited (remove and add  |
| new_limit | combo | 0.66 (86) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| new_limit | cap_total_store | 0.67 (3) | result differs from reference |
| relax_remove (nl) | x_full | 0.67 (6) | result differs from reference |
| data_change (nl) | g_scale_all_rows | 0.69 (26) | invalid DSL: no row of 'flights' matches {"flight": ["1", "73", "2", "74", "75", "3", "76", " |
| data_change | g_scale_column | 0.71 (76) | result differs from reference |
| data_change | g_scale_all_rows | 0.72 (95) | invalid DSL: no row of 'flights' matches {"flight": ["1", "73", "2", "74", "75", "3", "76", " |
| chained_scenario | c_undo | 0.74 (144) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| data_change (nl) | g_scale_column | 0.75 (24) | result differs from reference |
| objective_change (nl) | o_then_min | 0.75 (4) | result differs from reference |
| fixed_decision | f_fix_level | 0.75 (85) | invalid DSL: unknown table 'repairs'; tables are ['days', 'demand', 'depots', 'rental_lengths |
| new_limit | g_floor_measure_scope | 0.77 (82) | result differs from reference |
| fixed_decision (nl) | combo | 0.80 (20) | invalid DSL: unknown table 'damaged_left'; tables are ['days', 'demand', 'depots', 'rental_le |
| relax_remove (nl) | x_scoped | 0.80 (20) | invalid DSL: 'group_0' is not a group; known values: [] |
| new_limit | g_cap_measure_scope | 0.81 (105) | invalid DSL: 'flight' is not a flight; known values: ['1', '10', '100', '101', '102', '103',  |
| chained_scenario (nl) | c_revise | 0.85 (40) | unparseable output |
| data_change (nl) | g_set_column | 0.85 (20) | invalid scenario |
| chained_scenario | c_revise | 0.88 (151) | unparseable output |
| data_change | g_set_column | 0.93 (86) | result differs from reference |
| data_change | g_add_row | 0.94 (18) | invalid DSL: row is missing columns ['capacity'] |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_remove_row | 1.00 (19) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change (nl) | demand_set | 1.00 (2) |  |
| data_change (nl) | g_add_row | 1.00 (4) |  |
| data_change (nl) | g_remove_row | 1.00 (12) |  |
| data_change (nl) | margin_scale | 1.00 (2) |  |
| data_change (nl) | param | 1.00 (2) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| under_specified | ask_cap_make_months | 1.00 (1) |  |
| under_specified | ask_cap_total_make | 1.00 (2) |  |
| under_specified | ask_cap_two_products_month | 1.00 (2) |  |

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/qwen3:4b-instruct-2507-q4_K_M` | 1078 | 1514 | 17 | 17 | 0 | 0 |
