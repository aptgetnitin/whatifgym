# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | chained_scenario (nl) | data_change | data_change (nl) | fixed_decision | fixed_decision (nl) | infeasible_request | infeasible_request (nl) | logical_rule | logical_rule (nl) | new_limit | new_limit (nl) | objective_change | objective_change (nl) | relative_rule | relative_rule (nl) | relax_remove | relax_remove (nl) | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:8b` | 4636 | 0.597 | 0.676 | 0.83 | 0.94 | 0.72 (469) | 0.63 (132) | 0.82 (512) | 0.91 (150) | 0.60 (423) | 0.68 (116) | 0.69 (324) | 0.77 (82) | 0.25 (381) | 0.17 (126) | 0.74 (375) | 0.64 (118) | 0.59 (217) | 0.64 (50) | 0.58 (427) | 0.55 (110) | 0.54 (108) | 0.63 (30) | 0.33 (486) | 0.65 (575) | 0.60 (2647) | 0.58 (1414) | 5.9 |

## By base model

| base model | `ollama/qwen3:8b` |
|---|---|
| `airline_planning` | 0.56 (181) |
| `assignment_with_constraints` | 0.61 (148) |
| `battery_scheduling` | 0.62 (217) |
| `bin_packing` | 0.74 (86) |
| `car_rental` | 0.55 (191) |
| `car_rental_2` | 0.56 (250) |
| `covid19_facility_location` | 0.66 (219) |
| `drone_network` | 0.51 (183) |
| `economic_planning` | 0.63 (220) |
| `factory_planning` | 0.53 (275) |
| `factory_planning_2` | 0.65 (216) |
| `fantasy_basketball` | 0.75 (105) |
| `farm_planning` | 0.51 (226) |
| `food_manufacture` | 0.69 (210) |
| `food_supply` | 0.52 (196) |
| `jobshop_ft06` | 0.56 (195) |
| `manpower_planning` | 0.57 (258) |
| `mining` | 0.58 (223) |
| `multiple_knapsack` | 0.62 (132) |
| `optimize_power_schedule` | 0.60 (182) |
| `power_generation_hydro` | 0.70 (220) |
| `railway_dispatching` | 0.60 (217) |
| `single_machine_scheduling` | 0.76 (55) |
| `technician_routing_scheduling` | 0.58 (196) |
| `wedding_seating` | 0.34 (35) |

## By template (where the misses are)

### `ollama/qwen3:8b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | invalid DSL: invalid set_param change: Additional properties are not allowed ('table', 'where |
| data_change | margin_set | 0.00 (6) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| data_change (nl) | outage | 0.00 (2) | invalid DSL: no row of 'downtime' matches {"month": "Jan", "machine": "vertDrill"} |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | result differs from reference |
| new_limit (nl) | cap_store_month | 0.00 (2) | result differs from reference |
| new_limit (nl) | cap_total_make | 0.00 (4) | result differs from reference |
| objective_change (nl) | o_reorder | 0.00 (4) | invalid DSL: [] is not valid under any of the given schemas: [] should be non-empty |
| relax_remove (nl) | combo | 0.00 (4) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | invalid scenario |
| under_specified | ask_cap_make_months | 0.00 (1) | needed clarification not asked |
| under_specified | ask_cap_store_month | 0.00 (1) | needed clarification not asked |
| under_specified | ask_cap_total_make | 0.00 (2) | needed clarification not asked |
| under_specified | ask_cap_total_store | 0.00 (2) | result differs from reference |
| under_specified | ask_cap_two_products_month | 0.00 (2) | invalid scenario |
| under_specified | ask_demand_zero | 0.00 (1) | invalid scenario |
| under_specified | ask_install | 0.00 (1) | result differs from reference |
| under_specified | ask_margin_scale | 0.00 (1) | invalid scenario |
| under_specified | ask_outage | 0.00 (1) | invalid DSL: row is missing columns ['machines_down'] |
| under_specified | ask_g_cap_measure_total | 0.04 (45) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| logical_rule (nl) | l_never_both | 0.07 (14) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| logical_rule | l_if_then | 0.08 (103) | invalid DSL: '>' is not one of ['<=', '>=', '=='] |
| under_specified | ask_g_remove_row | 0.09 (33) | needed clarification not asked |
| under_specified | ask_g_param | 0.15 (41) | needed clarification not asked |
| logical_rule (nl) | l_at_most_k | 0.16 (32) | result differs from reference |
| logical_rule | l_at_most_k | 0.16 (108) | invalid DSL: '3074' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| logical_rule (nl) | l_if_then | 0.16 (38) | result differs from reference |
| relax_remove | combo | 0.17 (6) | invalid DSL: '*' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'worker |
| under_specified | ask_g_add_row | 0.24 (17) | needed clarification not asked |
| logical_rule (nl) | l_none_or_batch | 0.24 (42) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| under_specified | ask_g_cap_measure_scope | 0.27 (48) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| under_specified | ask_g_floor_measure_scope | 0.27 (44) | invalid DSL: '*' is not a task; known values: ['task_0', 'task_1', 'task_2', 'task_3', 'task_ |
| chained_scenario (nl) | c_add | 0.31 (62) | result differs from reference |
| infeasible_request | i_floor_total | 0.31 (45) | result differs from reference |
| logical_rule | l_never_both | 0.31 (48) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| data_change | process_hours | 0.33 (3) | result differs from reference |
| new_limit | cap_total_store | 0.33 (3) | invalid DSL: '*' is not a product; known values: ['Prod1', 'Prod2', 'Prod3', 'Prod4', 'Prod5' |
| relax_remove (nl) | x_full | 0.33 (6) | invalid DSL: '*' is not a machine; known values: ['borer', 'grinder', 'horiDrill', 'planer',  |
| objective_change | o_reorder | 0.35 (48) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| chained_scenario | c_add | 0.36 (174) | result differs from reference |
| fixed_decision | f_fix_scope | 0.37 (67) | result differs from reference |
| relax_remove | x_full | 0.38 (16) | invalid DSL: '*' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'worker |
| relative_rule (nl) | r_two_measures | 0.40 (10) | result differs from reference |
| fixed_decision (nl) | f_fix_scope | 0.41 (22) | invalid DSL: '*' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', 'Tu |
| relative_rule | r_share_of_total | 0.41 (146) | result differs from reference |
| relative_rule (nl) | r_share_of_total | 0.42 (40) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| under_specified | ask_g_set_column | 0.44 (84) | needed clarification not asked |
| relative_rule | combo | 0.44 (93) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| logical_rule | l_none_or_batch | 0.44 (122) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| objective_change | o_three_stages | 0.45 (40) | invalid DSL: 'all' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| under_specified | ask_g_scale_all_rows | 0.45 (77) | invalid DSL: invalid scale change: [1, 73, 2, 74, 75, 3, 76, 4, 5, 77, 6, 78, 79, 7, 80, 8, 9 |
| relative_rule (nl) | combo | 0.46 (28) | invalid DSL: 'all' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| objective_change | o_then_max | 0.48 (23) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| relative_rule | r_two_measures | 0.48 (52) | invalid DSL: '*' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'worker |
| objective_change | o_then_min | 0.50 (10) | result differs from reference |
| under_specified | ask_retire | 0.50 (2) | result differs from reference |
| fixed_decision | f_fix_zero | 0.52 (122) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| new_limit | combo | 0.53 (86) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| fixed_decision | combo | 0.56 (82) | invalid DSL: unknown table 'assign'; tables are ['allowed_teams', 'costs', 'tasks', 'workers' |
| new_limit (nl) | g_cap_measure_total | 0.57 (30) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| objective_change (nl) | o_then_max | 0.57 (14) | result differs from reference |
| under_specified | ask_g_scale_column | 0.57 (77) | needed clarification not asked |
| relax_remove | x_scoped | 0.59 (86) | result differs from reference |
| new_limit (nl) | combo | 0.59 (32) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| new_limit | cap_total_make | 0.60 (5) | result differs from reference |
| objective_change (nl) | o_three_stages | 0.60 (10) | invalid DSL: 'all' is not a machine; known values: ['M0', 'M1', 'M2', 'M3', 'M4', 'M5'] |
| infeasible_request (nl) | i_floor_total | 0.62 (8) | result differs from reference |
| new_limit | g_cap_measure_total | 0.64 (87) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| data_change | retire | 0.67 (3) | result differs from reference |
| under_specified | ask_demand_scale | 0.67 (3) | invalid scenario |
| infeasible_request | i_commit | 0.67 (133) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| fixed_decision (nl) | f_fix_zero | 0.68 (34) | invalid DSL: unknown table 'operate'; tables are ['aircraft', 'airports', 'flights'] |
| data_change | combo | 0.70 (114) | invalid DSL: no row of 'costs' matches {"worker": "*", "task": "*"} |
| fixed_decision | f_fix_level | 0.72 (85) | result differs from reference |
| new_limit (nl) | g_floor_measure_scope | 0.73 (30) | result differs from reference |
| fixed_decision (nl) | f_force_one | 0.75 (16) | invalid DSL: unknown table 'assign'; tables are ['allowed_teams', 'costs', 'tasks', 'workers' |
| infeasible_request (nl) | i_two_floors | 0.75 (12) | invalid DSL: unknown table 'herd'; tables are ['ages', 'land_groups', 'years'] |
| objective_change (nl) | o_then_min | 0.75 (4) | result differs from reference |
| infeasible_request (nl) | i_floor | 0.77 (26) | invalid DSL: unknown table 'repairs'; tables are ['days', 'demand', 'depots', 'expansion_opti |
| fixed_decision (nl) | f_fix_level | 0.79 (24) | invalid DSL: unknown table 'repairs'; tables are ['days', 'demand', 'depots', 'rental_lengths |
| chained_scenario (nl) | c_undo | 0.80 (30) | invalid DSL: table 'hours' has no column 'soc'; columns are ['export_price', 'hour', 'import_ |
| data_change | g_scale_all_rows | 0.80 (95) | invalid DSL: invalid shift change: [1, 73, 2, 74, 75, 3, 76, 4, 5, 77, 6, 78, 79, 7, 80, 8, 9 |
| fixed_decision (nl) | combo | 0.80 (20) | invalid DSL: unknown table 'damaged_left'; tables are ['days', 'demand', 'depots', 'rental_le |
| objective_change | o_then_scoped | 0.80 (96) | result differs from reference |
| infeasible_request (nl) | i_commit | 0.81 (36) | result differs from reference |
| infeasible_request | i_floor | 0.81 (88) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| objective_change (nl) | o_then_scoped | 0.83 (18) | result differs from reference |
| data_change | g_set_column | 0.84 (86) | result differs from reference |
| relative_rule (nl) | r_two_values | 0.84 (32) | result differs from reference |
| infeasible_request | i_two_floors | 0.84 (58) | invalid DSL: table 'hours' has no column 'soc'; columns are ['export_price', 'hour', 'import_ |
| relax_remove (nl) | x_scoped | 0.85 (20) | invalid DSL: unknown constraint family 'team_pattern[worker]'; families are ['cover', 'one_te |
| fixed_decision | f_force_one | 0.85 (67) | invalid DSL: '4696' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| chained_scenario | c_undo | 0.86 (144) | invalid DSL: no row of 'costs' matches {"worker": "*", "task": "*"} |
| data_change (nl) | g_param | 0.90 (20) | invalid DSL: unknown table 'params'; tables are ['machines', 'maintenance', 'max_sales', 'mon |
| data_change (nl) | g_set_column | 0.90 (20) | invalid DSL: unknown parameter 'cost_per_hour'; parameters are ['pump_mwh_per_m', 'reserve_ma |
| new_limit (nl) | g_cap_measure_scope | 0.90 (20) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| new_limit | g_floor_measure_scope | 0.90 (82) | result differs from reference |
| relative_rule | r_two_values | 0.90 (136) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.90 (105) | result differs from reference |
| data_change | g_param | 0.92 (60) | result differs from reference |
| data_change (nl) | combo | 0.92 (36) | result differs from reference |
| data_change (nl) | g_remove_row | 0.92 (12) | invalid scenario |
| data_change (nl) | g_scale_column | 0.92 (24) | invalid DSL: invalid scale_param change: Additional properties are not allowed ('where' was u |
| data_change | g_scale_column | 0.93 (76) | result differs from reference |
| data_change | g_add_row | 0.94 (18) | invalid DSL: row is missing columns ['rank'] |
| data_change (nl) | g_scale_all_rows | 0.96 (26) | invalid DSL: no row of 'setup_times' matches {"from_job": "job", "to_job": "job"} |
| chained_scenario | c_revise | 0.99 (151) | result differs from reference |
| chained_scenario (nl) | c_revise | 1.00 (40) |  |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_remove_row | 1.00 (19) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change (nl) | demand_set | 1.00 (2) |  |
| data_change (nl) | g_add_row | 1.00 (4) |  |
| data_change (nl) | margin_scale | 1.00 (2) |  |
| data_change (nl) | param | 1.00 (2) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| under_specified | ask_margin_set | 1.00 (1) |  |
| under_specified | ask_outage_cancel | 1.00 (1) |  |

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/qwen3:8b` | 1079 | 787 | 6 | 6 | 0 | 0 |
