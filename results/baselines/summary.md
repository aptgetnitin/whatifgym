# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | data_change | data_change (nl) | fixed_decision | infeasible_request | logical_rule | new_limit | new_limit (nl) | objective_change | relative_rule | relax_remove | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cowork-opus` | 60 | 1.000 | 1.100 | 1.00 | 1.00 | – | 1.00 (60) | – | – | – | – | – | – | – | – | – | – | 1.00 (28) | 1.00 (16) | 1.00 (16) | – |
| `cowork-sonnet` | 60 | 0.983 | 1.083 | 1.00 | 1.00 | – | 0.98 (60) | – | – | – | – | – | – | – | – | – | – | 1.00 (28) | 1.00 (16) | 0.94 (16) | – |
| `ollama/gpt-oss:20b` | 3767 | 0.895 | 0.989 | 0.96 | 0.99 | 0.97 (469) | 0.95 (512) | 1.00 (6) | 0.94 (423) | 0.93 (324) | 0.78 (381) | 0.98 (375) | 0.97 (39) | 0.91 (217) | 0.91 (427) | 0.98 (108) | 0.68 (486) | 0.97 (464) | 0.88 (2192) | 0.90 (1111) | 6.4 |
| `ollama/qwen3:14b` | 3767 | 0.724 | 0.807 | 0.87 | 0.93 | 0.78 (469) | 0.76 (512) | 1.00 (6) | 0.90 (423) | 0.87 (324) | 0.31 (381) | 0.91 (375) | 0.92 (39) | 0.78 (217) | 0.81 (427) | 0.86 (108) | 0.42 (486) | 0.86 (464) | 0.71 (2192) | 0.70 (1111) | 2.0 |
| `ollama/qwen3:4b` | 3767 | 0.255 | 0.319 | 0.72 | 0.89 | 0.48 (469) | 0.51 (512) | 0.50 (6) | 0.16 (423) | 0.09 (324) | 0.16 (381) | 0.45 (375) | 0.38 (39) | 0.20 (217) | 0.18 (427) | 0.06 (108) | 0.01 (486) | 0.24 (464) | 0.21 (2192) | 0.35 (1111) | 3.3 |
| `ollama/qwen3:8b` | 3767 | 0.591 | 0.668 | 0.82 | 0.93 | 0.72 (469) | 0.82 (512) | 1.00 (6) | 0.60 (423) | 0.69 (324) | 0.25 (381) | 0.74 (375) | 0.59 (39) | 0.59 (217) | 0.58 (427) | 0.54 (108) | 0.33 (486) | 0.64 (464) | 0.59 (2192) | 0.57 (1111) | 3.1 |

## By base model

| base model | `cowork-opus` | `cowork-sonnet` | `ollama/gpt-oss:20b` | `ollama/qwen3:14b` | `ollama/qwen3:4b` | `ollama/qwen3:8b` |
|---|---|---|---|---|---|---|
| `airline_planning` | – | – | 0.83 (135) | 0.63 (135) | 0.16 (135) | 0.52 (135) |
| `assignment_with_constraints` | – | – | 0.87 (124) | 0.79 (124) | 0.36 (124) | 0.57 (124) |
| `battery_scheduling` | – | – | 0.89 (169) | 0.64 (169) | 0.22 (169) | 0.63 (169) |
| `bin_packing` | – | – | 0.94 (68) | 0.69 (68) | 0.26 (68) | 0.71 (68) |
| `car_rental` | – | – | 0.94 (164) | 0.76 (164) | 0.23 (164) | 0.57 (164) |
| `car_rental_2` | – | – | 0.91 (194) | 0.70 (194) | 0.29 (194) | 0.53 (194) |
| `covid19_facility_location` | – | – | 0.91 (181) | 0.78 (181) | 0.21 (181) | 0.67 (181) |
| `drone_network` | – | – | 0.79 (147) | 0.59 (147) | 0.37 (147) | 0.49 (147) |
| `economic_planning` | – | – | 0.87 (174) | 0.70 (174) | 0.28 (174) | 0.64 (174) |
| `factory_planning` | 1.00 (60) | 0.98 (60) | 0.93 (223) | 0.70 (223) | 0.21 (223) | 0.52 (223) |
| `factory_planning_2` | – | – | 0.97 (174) | 0.75 (174) | 0.31 (174) | 0.70 (174) |
| `fantasy_basketball` | – | – | 0.91 (89) | 0.81 (89) | 0.27 (89) | 0.74 (89) |
| `farm_planning` | – | – | 0.90 (186) | 0.73 (186) | 0.33 (186) | 0.47 (186) |
| `food_manufacture` | – | – | 0.94 (178) | 0.76 (178) | 0.31 (178) | 0.70 (178) |
| `food_supply` | – | – | 0.80 (164) | 0.65 (164) | 0.28 (164) | 0.52 (164) |
| `jobshop_ft06` | – | – | 0.83 (167) | 0.75 (167) | 0.23 (167) | 0.59 (167) |
| `manpower_planning` | – | – | 0.90 (210) | 0.78 (210) | 0.20 (210) | 0.54 (210) |
| `mining` | – | – | 0.92 (191) | 0.81 (191) | 0.24 (191) | 0.61 (191) |
| `multiple_knapsack` | – | – | 0.95 (106) | 0.65 (106) | 0.31 (106) | 0.61 (106) |
| `optimize_power_schedule` | – | – | 0.92 (156) | 0.76 (156) | 0.26 (156) | 0.60 (156) |
| `power_generation_hydro` | – | – | 0.94 (172) | 0.83 (172) | 0.29 (172) | 0.72 (172) |
| `railway_dispatching` | – | – | 0.83 (163) | 0.75 (163) | 0.08 (163) | 0.59 (163) |
| `single_machine_scheduling` | – | – | 0.93 (45) | 0.78 (45) | 0.20 (45) | 0.78 (45) |
| `technician_routing_scheduling` | – | – | 0.89 (154) | 0.68 (154) | 0.30 (154) | 0.51 (154) |
| `wedding_seating` | – | – | 0.85 (33) | 0.27 (33) | 0.03 (33) | 0.30 (33) |

## By template (where the misses are)

### `cowork-opus`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | combo | 1.00 (16) |  |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | install | 1.00 (1) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage | 1.00 (4) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |

### `cowork-sonnet`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | combo | 0.94 (16) | result differs from reference |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | install | 1.00 (1) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage | 1.00 (4) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |

### `ollama/gpt-oss:20b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_make_months | 0.00 (1) | invalid scenario |
| under_specified | ask_cap_total_make | 0.00 (2) | invalid scenario |
| under_specified | ask_outage | 0.00 (1) | invalid scenario |
| under_specified | ask_outage_cancel | 0.00 (1) | invalid scenario |
| under_specified | ask_retire | 0.00 (2) | invalid scenario |
| under_specified | ask_g_cap_measure_total | 0.56 (45) | invalid scenario |
| under_specified | ask_g_set_column | 0.56 (84) | invalid scenario |
| logical_rule | l_at_most_k | 0.61 (108) | result differs from reference |
| under_specified | ask_g_add_row | 0.65 (17) | invalid scenario |
| logical_rule | l_never_both | 0.67 (48) | invalid DSL: unknown measure 'operate[aircraft, flight]'; measures are ['connect', 'operate'] |
| under_specified | ask_demand_scale | 0.67 (3) | invalid scenario |
| under_specified | ask_g_scale_column | 0.68 (77) | invalid scenario |
| under_specified | ask_g_param | 0.68 (41) | invalid scenario |
| objective_change | o_then_min | 0.70 (10) | result differs from reference |
| under_specified | ask_g_cap_measure_scope | 0.73 (48) | invalid scenario |
| under_specified | ask_g_floor_measure_scope | 0.75 (44) | invalid scenario |
| under_specified | ask_g_scale_all_rows | 0.79 (77) | result differs from reference |
| under_specified | ask_g_remove_row | 0.82 (33) | invalid scenario |
| infeasible_request | i_floor_total | 0.82 (45) | result differs from reference |
| relax_remove | combo | 0.83 (6) | invalid DSL: unknown constraint family 'housing[year]'; families are ['ageing', 'beet_feed',  |
| logical_rule | l_if_then | 0.83 (103) | invalid DSL: Additional properties are not allowed ('logical' was unexpected) |
| fixed_decision | f_force_one | 0.84 (67) | result differs from reference |
| data_change | g_scale_all_rows | 0.85 (95) | result differs from reference |
| relative_rule | combo | 0.87 (93) | result differs from reference |
| fixed_decision | combo | 0.90 (82) | result differs from reference |
| relative_rule | r_two_values | 0.90 (136) | result differs from reference |
| objective_change | o_then_scoped | 0.91 (96) | result differs from reference |
| objective_change | o_then_max | 0.91 (23) | result differs from reference |
| new_limit (nl) | g_cap_measure_total | 0.92 (12) | invalid DSL: 'unskilled' is not a from_skill; known values: ['semi_skilled', 'skilled'] |
| relative_rule | r_share_of_total | 0.92 (146) | result differs from reference |
| objective_change | o_three_stages | 0.93 (40) | result differs from reference |
| data_change | combo | 0.93 (114) | result differs from reference |
| relax_remove | x_full | 0.94 (16) | invalid DSL: removing these rows empties table 'maintenance' |
| logical_rule | l_none_or_batch | 0.94 (122) | result differs from reference |
| infeasible_request | i_floor | 0.94 (88) | result differs from reference |
| chained_scenario | c_undo | 0.94 (144) | result differs from reference |
| infeasible_request | i_commit | 0.95 (133) | result differs from reference |
| infeasible_request | i_two_floors | 0.95 (58) | result differs from reference |
| fixed_decision | f_fix_scope | 0.96 (67) | unparseable output |
| objective_change | o_reorder | 0.96 (48) | result differs from reference |
| data_change | g_scale_column | 0.96 (76) | result differs from reference |
| relative_rule | r_two_measures | 0.96 (52) | result differs from reference |
| new_limit | combo | 0.97 (86) | result differs from reference |
| chained_scenario | c_add | 0.97 (174) | result differs from reference |
| fixed_decision | f_fix_zero | 0.98 (122) | invalid DSL: '5145 RURITAN COURT' is not a base; known values: ['21 MUNICIPAL CTR Fire Statio |
| new_limit | g_floor_measure_scope | 0.98 (82) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.98 (105) | result differs from reference |
| data_change | g_param | 0.98 (60) | invalid DSL: unknown table 'params'; tables are ['costs', 'requirements', 'retraining', 'skil |
| fixed_decision | f_fix_level | 0.99 (85) | result differs from reference |
| data_change | g_set_column | 0.99 (86) | result differs from reference |
| chained_scenario | c_revise | 1.00 (151) |  |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (18) |  |
| data_change | g_remove_row | 1.00 (19) |  |
| data_change | install | 1.00 (1) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage | 1.00 (4) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |
| data_change (nl) | g_scale_all_rows | 1.00 (3) |  |
| data_change (nl) | g_set_column | 1.00 (3) |  |
| new_limit | cap_store_month | 1.00 (4) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit | g_cap_measure_total | 1.00 (87) |  |
| new_limit (nl) | combo | 1.00 (15) |  |
| new_limit (nl) | g_cap_measure_scope | 1.00 (3) |  |
| new_limit (nl) | g_floor_measure_scope | 1.00 (9) |  |
| relax_remove | x_scoped | 1.00 (86) |  |
| under_specified | ask_cap_store_month | 1.00 (1) |  |
| under_specified | ask_cap_total_store | 1.00 (2) |  |
| under_specified | ask_cap_two_products_month | 1.00 (2) |  |
| under_specified | ask_demand_zero | 1.00 (1) |  |
| under_specified | ask_install | 1.00 (1) |  |
| under_specified | ask_margin_scale | 1.00 (1) |  |
| under_specified | ask_margin_set | 1.00 (1) |  |

### `ollama/qwen3:14b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | invalid DSL: unknown parameter 'installed'; parameters are ['holding_cost', 'hours_per_month' |
| data_change | margin_set | 0.00 (6) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_store_month | 0.00 (1) | needed clarification not asked |
| under_specified | ask_install | 0.00 (1) | result differs from reference |
| under_specified | ask_margin_set | 0.00 (1) | needed clarification not asked |
| under_specified | ask_outage | 0.00 (1) | invalid DSL: row is missing columns ['machines_down'] |
| under_specified | ask_g_remove_row | 0.03 (33) | needed clarification not asked |
| under_specified | ask_g_cap_measure_total | 0.18 (45) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| logical_rule | l_if_then | 0.18 (103) | result differs from reference |
| logical_rule | l_at_most_k | 0.24 (108) | invalid DSL: [{'measure': 'operate', 'scope': {'flight': ['4265', '3074', '4514']}, 'sense':  |
| under_specified | ask_g_scale_all_rows | 0.26 (77) | needed clarification not asked |
| under_specified | ask_g_floor_measure_scope | 0.34 (44) | invalid DSL: [] is not valid under any of the given schemas: [] should be non-empty |
| data_change | margin_scale | 0.40 (5) | invalid DSL: invalid scale_param change: Additional properties are not allowed ('where' was u |
| under_specified | ask_g_add_row | 0.41 (17) | needed clarification not asked |
| logical_rule | l_never_both | 0.42 (48) | result differs from reference |
| under_specified | ask_g_cap_measure_scope | 0.42 (48) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| objective_change | o_then_max | 0.43 (23) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| logical_rule | l_none_or_batch | 0.44 (122) | result differs from reference |
| under_specified | ask_g_param | 0.49 (41) | result differs from reference |
| infeasible_request | i_floor_total | 0.49 (45) | invalid DSL: {'type': 'string'} is not valid under any of the given schemas: {'type': 'string |
| relax_remove | combo | 0.50 (6) | invalid DSL: unknown constraint family 'size[worker]'; families are ['cover', 'one_team', 'si |
| under_specified | ask_retire | 0.50 (2) | result differs from reference |
| data_change | g_scale_all_rows | 0.51 (95) | unparseable output |
| chained_scenario | c_add | 0.53 (174) | invalid DSL: {'type': 'string'} is not valid under any of the given schemas: {'type': 'string |
| data_change | combo | 0.55 (114) | invalid DSL: invalid scale change: {} should be non-empty |
| objective_change | o_then_min | 0.60 (10) | result differs from reference |
| under_specified | ask_g_set_column | 0.61 (84) | needed clarification not asked |
| under_specified | ask_g_scale_column | 0.61 (77) | invalid DSL: column 'revenue' is numeric; got 'new_revenue_value' |
| relative_rule | r_two_measures | 0.63 (52) | invalid DSL: 'all' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'work |
| under_specified | ask_demand_scale | 0.67 (3) | needed clarification not asked |
| fixed_decision | f_fix_scope | 0.70 (67) | result differs from reference |
| objective_change | o_three_stages | 0.72 (40) | invalid DSL: {'type': 'array', 'items': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06' |
| relative_rule | combo | 0.74 (93) | invalid DSL: 'all' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '10 |
| new_limit (nl) | g_cap_measure_total | 0.75 (12) | invalid DSL: 'unskilled' is not a from_skill; known values: ['semi_skilled', 'skilled'] |
| relative_rule | r_share_of_total | 0.79 (146) | invalid DSL: 'all' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '10 |
| objective_change | o_reorder | 0.81 (48) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| relax_remove | x_full | 0.81 (16) | invalid DSL: constraint family 'one_team' cannot be relaxed in this model; change the data or |
| new_limit | combo | 0.84 (86) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| new_limit | g_cap_measure_total | 0.84 (87) | invalid DSL: {'all': True} is not valid under any of the given schemas: {'all': True} is not  |
| chained_scenario | c_undo | 0.86 (144) | invalid DSL: invalid scale change: {} should be non-empty |
| infeasible_request | i_two_floors | 0.86 (58) | result differs from reference |
| fixed_decision | combo | 0.87 (82) | result differs from reference |
| objective_change | o_then_scoped | 0.89 (96) | invalid DSL: {'depot': ['Glasgow', 'Manchester', 'Birmingham', 'Plymouth']} is not valid unde |
| relax_remove | x_scoped | 0.90 (86) | invalid DSL: unknown constraint family 'team_pattern[worker]'; families are ['cover', 'one_te |
| data_change | g_scale_column | 0.91 (76) | result differs from reference |
| fixed_decision | f_fix_zero | 0.91 (122) | invalid DSL: '4265' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| relative_rule | r_two_values | 0.93 (136) | result differs from reference |
| infeasible_request | i_floor | 0.94 (88) | result differs from reference |
| data_change | g_param | 0.95 (60) | invalid DSL: invalid scale change: {} should be non-empty |
| infeasible_request | i_commit | 0.95 (133) | result differs from reference |
| new_limit | g_floor_measure_scope | 0.98 (82) | invalid DSL: at_least is 15 but there are only 6 conditions |
| fixed_decision | f_force_one | 0.99 (67) | result differs from reference |
| fixed_decision | f_fix_level | 0.99 (85) | invalid DSL: '2' is not a resource; known values: ['0', '1', '2', '3', '4', '5', '6'] |
| data_change | g_set_column | 0.99 (86) | invalid DSL: measure 'pick' has dimensions ['player'], not 'position' |
| new_limit | g_cap_measure_scope | 0.99 (105) | invalid DSL: {'train': 'D'} is not valid under any of the given schemas: {'train': 'D'} is no |
| chained_scenario | c_revise | 1.00 (151) |  |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (18) |  |
| data_change | g_remove_row | 1.00 (19) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |
| data_change (nl) | g_scale_all_rows | 1.00 (3) |  |
| data_change (nl) | g_set_column | 1.00 (3) |  |
| new_limit | cap_store_month | 1.00 (4) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit (nl) | combo | 1.00 (15) |  |
| new_limit (nl) | g_cap_measure_scope | 1.00 (3) |  |
| new_limit (nl) | g_floor_measure_scope | 1.00 (9) |  |
| under_specified | ask_cap_make_months | 1.00 (1) |  |
| under_specified | ask_cap_total_make | 1.00 (2) |  |
| under_specified | ask_cap_total_store | 1.00 (2) |  |
| under_specified | ask_cap_two_products_month | 1.00 (2) |  |
| under_specified | ask_demand_zero | 1.00 (1) |  |
| under_specified | ask_margin_scale | 1.00 (1) |  |
| under_specified | ask_outage_cancel | 1.00 (1) |  |

### `ollama/qwen3:4b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | demand_zero | 0.00 (2) | result differs from reference |
| data_change | install | 0.00 (1) | result differs from reference |
| data_change | margin_set | 0.00 (6) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| data_change | outage | 0.00 (4) | invalid DSL: row is missing columns ['machines_down'] |
| data_change | param | 0.00 (5) | result differs from reference |
| data_change | retire | 0.00 (3) | result differs from reference |
| infeasible_request | i_floor_total | 0.00 (45) | result differs from reference |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | invalid DSL: unknown table 'max_inventory'; tables are ['downtime', 'machines', 'max_sales',  |
| new_limit | cap_total_make | 0.00 (5) | result differs from reference |
| new_limit | cap_total_store | 0.00 (3) | result differs from reference |
| new_limit (nl) | g_cap_measure_total | 0.00 (12) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| objective_change | o_then_min | 0.00 (10) | result differs from reference |
| relax_remove | combo | 0.00 (6) | result differs from reference |
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
| logical_rule | l_at_most_k | 0.06 (108) | invalid DSL: no row of 'flights' matches {"flight": ["4572", "3095", "3112", "3069", "4571"]} |
| fixed_decision | f_force_one | 0.07 (67) | result differs from reference |
| infeasible_request | i_commit | 0.08 (133) | result differs from reference |
| infeasible_request | i_floor | 0.08 (88) | result differs from reference |
| fixed_decision | f_fix_zero | 0.08 (122) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| objective_change | o_reorder | 0.10 (48) | invalid DSL: unknown measure 'revenue'; measures are ['connect', 'operate']; for the model's  |
| relative_rule | r_two_measures | 0.12 (52) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| data_change | g_param | 0.12 (60) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| fixed_decision | f_fix_scope | 0.12 (67) | invalid DSL: unknown table 'rentals'; tables are ['days', 'demand', 'depots', 'rental_lengths |
| logical_rule | l_never_both | 0.12 (48) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| relax_remove | x_full | 0.12 (16) | result differs from reference |
| relative_rule | r_share_of_total | 0.13 (146) | invalid DSL: '4514' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| data_change | demand_set | 0.17 (6) | result differs from reference |
| fixed_decision | f_fix_level | 0.18 (85) | result differs from reference |
| relative_rule | combo | 0.18 (93) | result differs from reference |
| logical_rule | l_none_or_batch | 0.19 (122) | result differs from reference |
| infeasible_request | i_two_floors | 0.21 (58) | result differs from reference |
| objective_change | o_three_stages | 0.23 (40) | invalid DSL: '*' is not a hour; known values: ['00-01', '01-02', '02-03', '03-04', '04-05', ' |
| logical_rule | l_if_then | 0.23 (103) | result differs from reference |
| relative_rule | r_two_values | 0.26 (136) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| new_limit | g_cap_measure_total | 0.26 (87) | invalid DSL: invalid set change: {'aircraft': ['all'], 'flight': ['all']} is not valid under  |
| objective_change | o_then_scoped | 0.29 (96) | result differs from reference |
| chained_scenario | c_add | 0.31 (174) | result differs from reference |
| data_change | process_hours | 0.33 (3) | result differs from reference |
| data_change (nl) | g_scale_all_rows | 0.33 (3) | invalid DSL: no row of 'requirements' matches {"year": ["1", "2", "3"], "skill": ["unskilled" |
| fixed_decision | combo | 0.37 (82) | result differs from reference |
| new_limit (nl) | g_floor_measure_scope | 0.44 (9) | result differs from reference |
| new_limit | g_floor_measure_scope | 0.45 (82) | result differs from reference |
| data_change | combo | 0.46 (114) | result differs from reference |
| chained_scenario | c_undo | 0.47 (144) | invalid DSL: '1' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '104' |
| data_change | g_scale_column | 0.49 (76) | result differs from reference |
| new_limit | cap_two_products_month | 0.50 (2) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.54 (105) | invalid DSL: '1' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '104' |
| data_change | g_add_row | 0.56 (18) | invalid DSL: row is missing columns ['weight'] |
| new_limit | combo | 0.57 (86) | invalid DSL: '1' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '104' |
| data_change | g_remove_row | 0.58 (19) | result differs from reference |
| new_limit (nl) | combo | 0.60 (15) | result differs from reference |
| data_change (nl) | g_set_column | 0.67 (3) | result differs from reference |
| new_limit (nl) | g_cap_measure_scope | 0.67 (3) | invalid DSL: unknown table 'retrain'; tables are ['costs', 'requirements', 'retraining', 'ski |
| data_change | g_scale_all_rows | 0.69 (95) | invalid DSL: no row of 'flights' matches {"flight": ["1", "2", "3", "4", "5", "6", "7", "8",  |
| chained_scenario | c_revise | 0.70 (151) | result differs from reference |
| data_change | g_set_column | 0.71 (86) | result differs from reference |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | outage_cancel | 1.00 (4) |  |

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
| logical_rule | l_if_then | 0.08 (103) | invalid DSL: '>' is not one of ['<=', '>=', '=='] |
| under_specified | ask_g_remove_row | 0.09 (33) | needed clarification not asked |
| under_specified | ask_g_param | 0.15 (41) | needed clarification not asked |
| logical_rule | l_at_most_k | 0.16 (108) | invalid DSL: '3074' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| relax_remove | combo | 0.17 (6) | invalid DSL: '*' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'worker |
| under_specified | ask_g_add_row | 0.24 (17) | needed clarification not asked |
| under_specified | ask_g_cap_measure_scope | 0.27 (48) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| under_specified | ask_g_floor_measure_scope | 0.27 (44) | invalid DSL: '*' is not a task; known values: ['task_0', 'task_1', 'task_2', 'task_3', 'task_ |
| infeasible_request | i_floor_total | 0.31 (45) | result differs from reference |
| logical_rule | l_never_both | 0.31 (48) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| data_change | process_hours | 0.33 (3) | result differs from reference |
| new_limit | cap_total_store | 0.33 (3) | invalid DSL: '*' is not a product; known values: ['Prod1', 'Prod2', 'Prod3', 'Prod4', 'Prod5' |
| new_limit (nl) | g_cap_measure_total | 0.33 (12) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| objective_change | o_reorder | 0.35 (48) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| chained_scenario | c_add | 0.36 (174) | result differs from reference |
| fixed_decision | f_fix_scope | 0.37 (67) | result differs from reference |
| relax_remove | x_full | 0.38 (16) | invalid DSL: '*' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'worker |
| relative_rule | r_share_of_total | 0.41 (146) | result differs from reference |
| under_specified | ask_g_set_column | 0.44 (84) | needed clarification not asked |
| relative_rule | combo | 0.44 (93) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| logical_rule | l_none_or_batch | 0.44 (122) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| objective_change | o_three_stages | 0.45 (40) | invalid DSL: 'all' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| under_specified | ask_g_scale_all_rows | 0.45 (77) | invalid DSL: invalid scale change: [1, 73, 2, 74, 75, 3, 76, 4, 5, 77, 6, 78, 79, 7, 80, 8, 9 |
| objective_change | o_then_max | 0.48 (23) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| relative_rule | r_two_measures | 0.48 (52) | invalid DSL: '*' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'worker |
| objective_change | o_then_min | 0.50 (10) | result differs from reference |
| under_specified | ask_retire | 0.50 (2) | result differs from reference |
| fixed_decision | f_fix_zero | 0.52 (122) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| new_limit | combo | 0.53 (86) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
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
| infeasible_request | i_floor | 0.81 (88) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| data_change | g_set_column | 0.84 (86) | result differs from reference |
| infeasible_request | i_two_floors | 0.84 (58) | invalid DSL: table 'hours' has no column 'soc'; columns are ['export_price', 'hour', 'import_ |
| fixed_decision | f_force_one | 0.85 (67) | invalid DSL: '4696' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| chained_scenario | c_undo | 0.86 (144) | invalid DSL: no row of 'costs' matches {"worker": "*", "task": "*"} |
| new_limit | g_floor_measure_scope | 0.90 (82) | result differs from reference |
| relative_rule | r_two_values | 0.90 (136) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.90 (105) | result differs from reference |
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
| `cowork-opus` | 0 | 0 | 0 | 0 | 0 | 0 |
| `cowork-sonnet` | 1 | 0 | 0 | 0 | 0 | 0 |
| `ollama/gpt-oss:20b` | 239 | 157 | 16 | 164 | 0 | 0 |
| `ollama/qwen3:14b` | 562 | 476 | 3 | 3 | 0 | 0 |
| `ollama/qwen3:4b` | 1760 | 1048 | 3 | 3 | 0 | 853 |
| `ollama/qwen3:8b` | 878 | 662 | 5 | 5 | 0 | 1 |
