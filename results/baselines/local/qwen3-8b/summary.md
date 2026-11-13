# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | data_change | data_change (nl) | fixed_decision | infeasible_request | logical_rule | new_limit | new_limit (nl) | objective_change | relative_rule | relax_remove | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:8b` | 3801 | 0.585 | 0.662 | 0.82 | 0.93 | 0.72 (469) | 0.82 (512) | 1.00 (6) | 0.60 (423) | 0.69 (325) | 0.23 (407) | 0.74 (378) | 0.59 (39) | 0.58 (219) | 0.57 (429) | 0.54 (108) | 0.33 (486) | 0.64 (465) | 0.59 (2198) | 0.56 (1138) | 3.0 |

## By base model

| base model | `ollama/qwen3:8b` |
|---|---|
| `airline_planning` | 0.49 (142) |
| `assignment_with_constraints` | 0.55 (128) |
| `battery_scheduling` | 0.63 (169) |
| `bin_packing` | 0.72 (68) |
| `car_rental` | 0.56 (164) |
| `car_rental_2` | 0.53 (194) |
| `covid19_facility_location` | 0.67 (181) |
| `drone_network` | 0.48 (151) |
| `economic_planning` | 0.64 (174) |
| `factory_planning` | 0.52 (223) |
| `factory_planning_2` | 0.69 (174) |
| `fantasy_basketball` | 0.73 (90) |
| `farm_planning` | 0.48 (187) |
| `food_manufacture` | 0.70 (178) |
| `food_supply` | 0.52 (164) |
| `jobshop_ft06` | 0.58 (169) |
| `manpower_planning` | 0.54 (210) |
| `mining` | 0.60 (194) |
| `multiple_knapsack` | 0.57 (108) |
| `optimize_power_schedule` | 0.59 (158) |
| `power_generation_hydro` | 0.71 (173) |
| `railway_dispatching` | 0.57 (167) |
| `single_machine_scheduling` | 0.78 (45) |
| `technician_routing_scheduling` | 0.50 (157) |
| `wedding_seating` | 0.30 (33) |

## By template (where the misses are)

### `ollama/qwen3:8b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | invalid DSL: invalid set_param change: Additional properties are not allowed ('table', 'where |
| data_change | margin_set | 0.00 (6) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | result differs from reference |
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
| logical_rule | l_if_then | 0.06 (129) | invalid DSL: '4514' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| under_specified | ask_g_remove_row | 0.09 (33) | needed clarification not asked |
| under_specified | ask_g_param | 0.15 (41) | needed clarification not asked |
| logical_rule | l_at_most_k | 0.16 (108) | invalid DSL: '3074' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| relax_remove | combo | 0.17 (6) | invalid DSL: '*' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'worker |
| under_specified | ask_g_add_row | 0.24 (17) | needed clarification not asked |
| under_specified | ask_g_cap_measure_scope | 0.27 (48) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| under_specified | ask_g_floor_measure_scope | 0.27 (44) | invalid DSL: '*' is not a task; known values: ['task_0', 'task_1', 'task_2', 'task_3', 'task_ |
| infeasible_request | i_floor_total | 0.30 (46) | result differs from reference |
| logical_rule | l_never_both | 0.31 (48) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| data_change | process_hours | 0.33 (3) | result differs from reference |
| new_limit | cap_total_store | 0.33 (3) | invalid DSL: '*' is not a product; known values: ['Prod1', 'Prod2', 'Prod3', 'Prod4', 'Prod5' |
| new_limit (nl) | g_cap_measure_total | 0.33 (12) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| objective_change | o_reorder | 0.35 (48) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| chained_scenario | c_add | 0.36 (174) | result differs from reference |
| fixed_decision | f_fix_scope | 0.37 (67) | result differs from reference |
| relax_remove | x_full | 0.38 (16) | invalid DSL: '*' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'worker |
| relative_rule | r_share_of_total | 0.39 (148) | result differs from reference |
| objective_change | o_then_min | 0.42 (12) | result differs from reference |
| relative_rule | combo | 0.42 (93) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| under_specified | ask_g_set_column | 0.44 (84) | needed clarification not asked |
| logical_rule | l_none_or_batch | 0.44 (122) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| objective_change | o_three_stages | 0.45 (40) | invalid DSL: 'all' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| under_specified | ask_g_scale_all_rows | 0.45 (77) | invalid DSL: invalid scale change: [1, 73, 2, 74, 75, 3, 76, 4, 5, 77, 6, 78, 79, 7, 80, 8, 9 |
| objective_change | o_then_max | 0.48 (23) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| relative_rule | r_two_measures | 0.48 (52) | invalid DSL: '*' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'worker |
| under_specified | ask_retire | 0.50 (2) | result differs from reference |
| fixed_decision | f_fix_zero | 0.52 (122) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| new_limit | combo | 0.52 (87) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| fixed_decision | combo | 0.56 (82) | invalid DSL: unknown table 'assign'; tables are ['allowed_teams', 'costs', 'tasks', 'workers' |
| under_specified | ask_g_scale_column | 0.57 (77) | needed clarification not asked |
| relax_remove | x_scoped | 0.59 (86) | result differs from reference |
| new_limit | cap_total_make | 0.60 (5) | result differs from reference |
| new_limit | g_cap_measure_total | 0.64 (87) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| data_change | retire | 0.67 (3) | result differs from reference |
| new_limit (nl) | g_cap_measure_scope | 0.67 (3) | invalid DSL: table 'retraining' has no column 'year'; columns are ['cost', 'from_skill', 'max |
| new_limit (nl) | g_floor_measure_scope | 0.67 (9) | invalid DSL: unknown table 'redundant'; tables are ['costs', 'requirements', 'retraining', 's |
| under_specified | ask_demand_scale | 0.67 (3) | invalid scenario |
| infeasible_request | i_commit | 0.67 (133) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| data_change | combo | 0.70 (114) | invalid DSL: no row of 'costs' matches {"worker": "*", "task": "*"} |
| fixed_decision | f_fix_level | 0.72 (85) | result differs from reference |
| new_limit (nl) | combo | 0.73 (15) | result differs from reference |
| data_change | g_scale_all_rows | 0.80 (95) | invalid DSL: invalid shift change: [1, 73, 2, 74, 75, 3, 76, 4, 5, 77, 6, 78, 79, 7, 80, 8, 9 |
| objective_change | o_then_scoped | 0.80 (96) | result differs from reference |
| infeasible_request | i_floor | 0.81 (88) | result differs from reference |
| data_change | g_set_column | 0.84 (86) | result differs from reference |
| infeasible_request | i_two_floors | 0.84 (58) | invalid DSL: table 'hours' has no column 'soc'; columns are ['export_price', 'hour', 'import_ |
| fixed_decision | f_force_one | 0.85 (67) | invalid DSL: '4696' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| chained_scenario | c_undo | 0.86 (144) | invalid DSL: no row of 'costs' matches {"worker": "*", "task": "*"} |
| new_limit | g_floor_measure_scope | 0.90 (82) | result differs from reference |
| relative_rule | r_two_values | 0.90 (136) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.91 (107) | result differs from reference |
| data_change | g_param | 0.92 (60) | result differs from reference |
| data_change | g_scale_column | 0.93 (76) | result differs from reference |
| data_change | g_add_row | 0.94 (18) | invalid DSL: row is missing columns ['rank'] |
| chained_scenario | c_revise | 0.99 (151) | result differs from reference |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_remove_row | 1.00 (19) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change (nl) | g_scale_all_rows | 1.00 (3) |  |
| data_change (nl) | g_set_column | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| under_specified | ask_margin_set | 1.00 (1) |  |
| under_specified | ask_outage_cancel | 1.00 (1) |  |

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/qwen3:8b` | 896 | 682 | 5 | 5 | 0 | 1 |
