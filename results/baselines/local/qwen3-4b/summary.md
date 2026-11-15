# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | chained_scenario (nl) | data_change | data_change (nl) | fixed_decision | fixed_decision (nl) | infeasible_request | infeasible_request (nl) | logical_rule | logical_rule (nl) | new_limit | new_limit (nl) | objective_change | objective_change (nl) | relative_rule | relative_rule (nl) | relax_remove | relax_remove (nl) | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:4b` | 4651 | 0.256 | 0.323 | 0.72 | 0.91 | 0.48 (469) | 0.37 (132) | 0.51 (512) | 0.46 (152) | 0.16 (423) | 0.28 (116) | 0.09 (324) | 0.12 (82) | 0.16 (381) | 0.13 (126) | 0.45 (375) | 0.33 (131) | 0.20 (217) | 0.24 (50) | 0.18 (427) | 0.15 (110) | 0.06 (108) | 0.10 (30) | 0.01 (486) | 0.23 (580) | 0.21 (2652) | 0.35 (1419) | 5.8 |

## By base model

| base model | `ollama/qwen3:4b` |
|---|---|
| `airline_planning` | 0.13 (181) |
| `assignment_with_constraints` | 0.38 (148) |
| `battery_scheduling` | 0.21 (217) |
| `bin_packing` | 0.24 (86) |
| `car_rental` | 0.22 (194) |
| `car_rental_2` | 0.28 (250) |
| `covid19_facility_location` | 0.25 (219) |
| `drone_network` | 0.38 (183) |
| `economic_planning` | 0.28 (220) |
| `factory_planning` | 0.22 (275) |
| `factory_planning_2` | 0.28 (216) |
| `fantasy_basketball` | 0.26 (105) |
| `farm_planning` | 0.34 (226) |
| `food_manufacture` | 0.33 (212) |
| `food_supply` | 0.28 (196) |
| `jobshop_ft06` | 0.24 (195) |
| `manpower_planning` | 0.19 (264) |
| `mining` | 0.22 (227) |
| `multiple_knapsack` | 0.30 (132) |
| `optimize_power_schedule` | 0.26 (182) |
| `power_generation_hydro` | 0.29 (220) |
| `railway_dispatching` | 0.09 (217) |
| `single_machine_scheduling` | 0.22 (55) |
| `technician_routing_scheduling` | 0.36 (196) |
| `wedding_seating` | 0.03 (35) |

## By template (where the misses are)

### `ollama/qwen3:4b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | demand_zero | 0.00 (2) | result differs from reference |
| data_change | install | 0.00 (1) | result differs from reference |
| data_change | margin_set | 0.00 (6) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| data_change | outage | 0.00 (4) | invalid DSL: row is missing columns ['machines_down'] |
| data_change | param | 0.00 (5) | result differs from reference |
| data_change | retire | 0.00 (3) | result differs from reference |
| data_change (nl) | outage | 0.00 (2) | result differs from reference |
| data_change (nl) | param | 0.00 (2) | result differs from reference |
| infeasible_request | i_floor_total | 0.00 (45) | result differs from reference |
| infeasible_request (nl) | i_floor_total | 0.00 (8) | invalid DSL: row is missing columns ['country'] |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | invalid DSL: unknown table 'max_inventory'; tables are ['downtime', 'machines', 'max_sales',  |
| new_limit | cap_total_make | 0.00 (5) | result differs from reference |
| new_limit | cap_total_store | 0.00 (3) | result differs from reference |
| new_limit (nl) | cap_store_month | 0.00 (2) | result differs from reference |
| new_limit (nl) | cap_total_make | 0.00 (4) | result differs from reference |
| objective_change | o_then_min | 0.00 (10) | result differs from reference |
| objective_change (nl) | o_reorder | 0.00 (4) | invalid DSL: unknown measure 'response_objective'; measures are ['assign', 'linked_load', 'op |
| relative_rule (nl) | r_share_of_total | 0.00 (40) | invalid DSL: '4564' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| relax_remove | combo | 0.00 (6) | result differs from reference |
| relax_remove (nl) | combo | 0.00 (4) | result differs from reference |
| relax_remove (nl) | x_full | 0.00 (6) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | needed clarification not asked |
| under_specified | ask_cap_make_months | 0.00 (1) | needed clarification not asked |
| under_specified | ask_cap_store_month | 0.00 (1) | invalid DSL: unknown table 'max_inventory'; tables are ['downtime', 'machines', 'max_sales',  |
| under_specified | ask_cap_total_make | 0.00 (2) | needed clarification not asked |
| under_specified | ask_cap_total_store | 0.00 (2) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_cap_two_products_month | 0.00 (2) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_demand_scale | 0.00 (3) | needed clarification not asked |
| under_specified | ask_demand_zero | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_add_row | 0.00 (17) | invalid DSL: row is missing columns ['weight'] |
| under_specified | ask_g_cap_measure_scope | 0.00 (48) | invalid DSL: no row of 'flights' matches {"flight": ["4576", "3103", "4264"]} |
| under_specified | ask_g_cap_measure_total | 0.00 (45) | invalid DSL: no row of 'flights' matches {"flight": ["4576", "3103", "4264"]} |
| under_specified | ask_g_floor_measure_scope | 0.00 (44) | needed clarification not asked |
| under_specified | ask_g_param | 0.00 (41) | needed clarification not asked |
| under_specified | ask_g_remove_row | 0.00 (33) | needed clarification not asked |
| under_specified | ask_g_scale_all_rows | 0.00 (77) | invalid DSL: no row of 'flights' matches {"flight": ["1", "2", "3", "4", "5", "6", "7", "8",  |
| under_specified | ask_install | 0.00 (1) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_margin_scale | 0.00 (1) | invalid DSL: "The planner's question is vague about which parameter to change. The model has  |
| under_specified | ask_margin_set | 0.00 (1) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_outage | 0.00 (1) | needed clarification not asked |
| under_specified | ask_outage_cancel | 0.00 (1) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_retire | 0.00 (2) | needed clarification not asked |
| under_specified | ask_g_set_column | 0.01 (84) | invalid DSL: no row of 'flights' matches {"flight": ["4576"]} |
| under_specified | ask_g_scale_column | 0.03 (77) | invalid DSL: column 'revenue' is numeric; got 'revenue' |
| objective_change | o_then_max | 0.04 (23) | result differs from reference |
| relax_remove | x_scoped | 0.05 (86) | result differs from reference |
| infeasible_request (nl) | i_commit | 0.06 (36) | result differs from reference |
| logical_rule (nl) | l_at_most_k | 0.06 (32) | invalid DSL: unknown table 'works'; tables are ['allowed_teams', 'costs', 'tasks', 'workers'] |
| logical_rule | l_at_most_k | 0.06 (108) | invalid DSL: no row of 'flights' matches {"flight": ["4572", "3095", "3112", "3069", "4571"]} |
| objective_change (nl) | o_then_max | 0.07 (14) | result differs from reference |
| fixed_decision | f_force_one | 0.07 (67) | result differs from reference |
| infeasible_request | i_commit | 0.08 (133) | result differs from reference |
| infeasible_request | i_floor | 0.08 (88) | result differs from reference |
| fixed_decision | f_fix_zero | 0.08 (122) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| fixed_decision (nl) | f_fix_zero | 0.09 (34) | result differs from reference |
| objective_change | o_reorder | 0.10 (48) | invalid DSL: unknown measure 'revenue'; measures are ['connect', 'operate']; for the model's  |
| infeasible_request (nl) | i_floor | 0.12 (26) | invalid DSL: unknown table 'repairs'; tables are ['days', 'demand', 'depots', 'expansion_opti |
| relative_rule | r_two_measures | 0.12 (52) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| data_change | g_param | 0.12 (60) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| new_limit (nl) | g_cap_measure_total | 0.12 (34) | invalid DSL: invalid set change: {'aircraft': ['TranspCom#1', 'TranspCom#3', 'TranspCom#2', ' |
| fixed_decision | f_fix_scope | 0.12 (67) | invalid DSL: unknown table 'rentals'; tables are ['days', 'demand', 'depots', 'rental_lengths |
| logical_rule | l_never_both | 0.12 (48) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| relax_remove | x_full | 0.12 (16) | result differs from reference |
| relative_rule | r_share_of_total | 0.13 (146) | invalid DSL: '4514' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| logical_rule (nl) | l_never_both | 0.14 (14) | invalid DSL: '4576' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| logical_rule (nl) | l_none_or_batch | 0.14 (42) | invalid DSL: unknown table 'soc'; tables are ['hours'] |
| relax_remove (nl) | x_scoped | 0.15 (20) | result differs from reference |
| logical_rule (nl) | l_if_then | 0.16 (38) | result differs from reference |
| data_change | demand_set | 0.17 (6) | result differs from reference |
| fixed_decision | f_fix_level | 0.18 (85) | result differs from reference |
| relative_rule | combo | 0.18 (93) | result differs from reference |
| fixed_decision (nl) | f_force_one | 0.19 (16) | result differs from reference |
| logical_rule | l_none_or_batch | 0.19 (122) | result differs from reference |
| data_change (nl) | g_param | 0.20 (20) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| relative_rule (nl) | r_two_measures | 0.20 (10) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| infeasible_request | i_two_floors | 0.21 (58) | result differs from reference |
| fixed_decision (nl) | f_fix_level | 0.21 (24) | result differs from reference |
| relative_rule (nl) | combo | 0.21 (28) | invalid DSL: '4513' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| objective_change | o_three_stages | 0.23 (40) | invalid DSL: '*' is not a hour; known values: ['00-01', '01-02', '02-03', '03-04', '04-05', ' |
| logical_rule | l_if_then | 0.23 (103) | result differs from reference |
| objective_change (nl) | o_then_min | 0.25 (4) | result differs from reference |
| relative_rule (nl) | r_two_values | 0.25 (32) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| relative_rule | r_two_values | 0.26 (136) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| chained_scenario (nl) | c_add | 0.26 (62) | result differs from reference |
| new_limit | g_cap_measure_total | 0.26 (87) | invalid DSL: invalid set change: {'aircraft': ['all'], 'flight': ['all']} is not valid under  |
| fixed_decision (nl) | f_fix_scope | 0.27 (22) | result differs from reference |
| new_limit (nl) | g_cap_measure_scope | 0.29 (21) | invalid DSL: unknown table 'operate'; tables are ['aircraft', 'airports', 'flights'] |
| objective_change | o_then_scoped | 0.29 (96) | result differs from reference |
| chained_scenario (nl) | c_undo | 0.30 (30) | invalid DSL: table 'hours' has no column 'soc'; columns are ['export_price', 'hour', 'import_ |
| chained_scenario | c_add | 0.31 (174) | result differs from reference |
| data_change | process_hours | 0.33 (3) | result differs from reference |
| new_limit (nl) | g_floor_measure_scope | 0.33 (33) | invalid DSL: no row of 'tasks' matches {"task": "worker_10"} |
| objective_change (nl) | o_then_scoped | 0.33 (18) | result differs from reference |
| data_change (nl) | combo | 0.36 (36) | result differs from reference |
| fixed_decision | combo | 0.37 (82) | result differs from reference |
| objective_change (nl) | o_three_stages | 0.40 (10) | invalid DSL: '2.22' is not a hour; known values: ['00-01', '01-02', '02-03', '03-04', '04-05' |
| infeasible_request (nl) | i_two_floors | 0.42 (12) | result differs from reference |
| new_limit | g_floor_measure_scope | 0.45 (82) | result differs from reference |
| data_change | combo | 0.46 (114) | result differs from reference |
| chained_scenario | c_undo | 0.47 (144) | invalid DSL: '1' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '104' |
| data_change | g_scale_column | 0.49 (76) | result differs from reference |
| data_change (nl) | g_add_row | 0.50 (4) | invalid DSL: row is missing columns ['weight', 'value'] |
| data_change (nl) | g_remove_row | 0.50 (12) | result differs from reference |
| data_change (nl) | margin_scale | 0.50 (2) | result differs from reference |
| new_limit | cap_two_products_month | 0.50 (2) | result differs from reference |
| data_change (nl) | g_scale_all_rows | 0.52 (27) | invalid DSL: no row of 'flights' matches {"flight": ["1", "2", "3", "4", "5", "6", "7", "8",  |
| new_limit | g_cap_measure_scope | 0.54 (105) | invalid DSL: '1' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '104' |
| data_change | g_add_row | 0.56 (18) | invalid DSL: row is missing columns ['weight'] |
| new_limit | combo | 0.57 (86) | invalid DSL: '1' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '104' |
| data_change (nl) | g_set_column | 0.57 (21) | result differs from reference |
| data_change | g_remove_row | 0.58 (19) | result differs from reference |
| new_limit (nl) | combo | 0.59 (37) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| chained_scenario (nl) | c_revise | 0.60 (40) | result differs from reference |
| data_change (nl) | g_scale_column | 0.67 (24) | result differs from reference |
| data_change | g_scale_all_rows | 0.69 (95) | invalid DSL: no row of 'flights' matches {"flight": ["1", "2", "3", "4", "5", "6", "7", "8",  |
| chained_scenario | c_revise | 0.70 (151) | result differs from reference |
| data_change | g_set_column | 0.71 (86) | result differs from reference |
| fixed_decision (nl) | combo | 0.75 (20) | invalid DSL: unknown table 'damaged_left'; tables are ['days', 'demand', 'depots', 'rental_le |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change (nl) | demand_set | 1.00 (2) |  |

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/qwen3:4b` | 2174 | 1285 | 3 | 3 | 0 | 1063 |
