# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | data_change | data_change (nl) | fixed_decision | infeasible_request | logical_rule | new_limit | new_limit (nl) | objective_change | relative_rule | relax_remove | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:14b` | 3767 | 0.724 | 0.807 | 0.87 | 0.93 | 0.78 (469) | 0.76 (512) | 1.00 (6) | 0.90 (423) | 0.87 (324) | 0.31 (381) | 0.91 (375) | 0.92 (39) | 0.78 (217) | 0.81 (427) | 0.86 (108) | 0.42 (486) | 0.86 (464) | 0.71 (2192) | 0.70 (1111) | 2.0 |

## By base model

| base model | `ollama/qwen3:14b` |
|---|---|
| `airline_planning` | 0.63 (135) |
| `assignment_with_constraints` | 0.79 (124) |
| `battery_scheduling` | 0.64 (169) |
| `bin_packing` | 0.69 (68) |
| `car_rental` | 0.76 (164) |
| `car_rental_2` | 0.70 (194) |
| `covid19_facility_location` | 0.78 (181) |
| `drone_network` | 0.59 (147) |
| `economic_planning` | 0.70 (174) |
| `factory_planning` | 0.70 (223) |
| `factory_planning_2` | 0.75 (174) |
| `fantasy_basketball` | 0.81 (89) |
| `farm_planning` | 0.73 (186) |
| `food_manufacture` | 0.76 (178) |
| `food_supply` | 0.65 (164) |
| `jobshop_ft06` | 0.75 (167) |
| `manpower_planning` | 0.78 (210) |
| `mining` | 0.81 (191) |
| `multiple_knapsack` | 0.65 (106) |
| `optimize_power_schedule` | 0.76 (156) |
| `power_generation_hydro` | 0.83 (172) |
| `railway_dispatching` | 0.75 (163) |
| `single_machine_scheduling` | 0.78 (45) |
| `technician_routing_scheduling` | 0.68 (154) |
| `wedding_seating` | 0.27 (33) |

## By template (where the misses are)

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/qwen3:14b` | 562 | 476 | 3 | 3 | 0 | 0 |
