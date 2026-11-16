# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | chained_scenario (nl) | data_change | data_change (nl) | fixed_decision | fixed_decision (nl) | infeasible_request | infeasible_request (nl) | logical_rule | logical_rule (nl) | new_limit | new_limit (nl) | objective_change | objective_change (nl) | relative_rule | relative_rule (nl) | relax_remove | relax_remove (nl) | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/gpt-oss:20b` | 4636 | 0.900 | 0.995 | 0.97 | 0.99 | 0.97 (469) | 0.97 (132) | 0.95 (512) | 0.97 (150) | 0.94 (423) | 0.93 (116) | 0.93 (324) | 0.94 (82) | 0.78 (381) | 0.79 (126) | 0.98 (375) | 0.97 (118) | 0.91 (217) | 0.94 (50) | 0.91 (427) | 0.90 (110) | 0.98 (108) | 0.97 (30) | 0.68 (486) | 0.96 (575) | 0.88 (2647) | 0.90 (1414) | 10.7 |
| `ollama/qwen3:14b` | 4636 | 0.726 | 0.810 | 0.87 | 0.94 | 0.78 (469) | 0.83 (132) | 0.76 (512) | 0.75 (150) | 0.90 (423) | 0.89 (116) | 0.87 (324) | 0.90 (82) | 0.31 (381) | 0.28 (126) | 0.91 (375) | 0.92 (118) | 0.78 (217) | 0.62 (50) | 0.81 (427) | 0.76 (110) | 0.86 (108) | 0.80 (30) | 0.42 (486) | 0.86 (575) | 0.71 (2647) | 0.70 (1414) | 6.3 |
| `ollama/qwen3:4b` | 4636 | 0.255 | 0.321 | 0.72 | 0.91 | 0.48 (469) | 0.37 (132) | 0.51 (512) | 0.45 (150) | 0.16 (423) | 0.28 (116) | 0.09 (324) | 0.12 (82) | 0.16 (381) | 0.13 (126) | 0.45 (375) | 0.31 (118) | 0.20 (217) | 0.24 (50) | 0.18 (427) | 0.15 (110) | 0.06 (108) | 0.10 (30) | 0.01 (486) | 0.23 (575) | 0.21 (2647) | 0.35 (1414) | 5.8 |
| `ollama/qwen3:4b-instruct-2507-q4_K_M` | 4636 | 0.441 | 0.502 | 0.67 | 0.92 | 0.64 (469) | 0.52 (132) | 0.67 (512) | 0.69 (150) | 0.57 (423) | 0.53 (116) | 0.43 (324) | 0.46 (82) | 0.14 (381) | 0.14 (126) | 0.70 (375) | 0.53 (118) | 0.46 (217) | 0.46 (50) | 0.10 (427) | 0.07 (110) | 0.55 (108) | 0.67 (30) | 0.20 (486) | 0.52 (575) | 0.40 (2647) | 0.49 (1414) | 7.5 |
| `ollama/qwen3:8b` | 4636 | 0.597 | 0.676 | 0.83 | 0.94 | 0.72 (469) | 0.63 (132) | 0.82 (512) | 0.91 (150) | 0.60 (423) | 0.68 (116) | 0.69 (324) | 0.77 (82) | 0.25 (381) | 0.17 (126) | 0.74 (375) | 0.64 (118) | 0.59 (217) | 0.64 (50) | 0.58 (427) | 0.55 (110) | 0.54 (108) | 0.63 (30) | 0.33 (486) | 0.65 (575) | 0.60 (2647) | 0.58 (1414) | 5.9 |

## By base model

| base model | `ollama/gpt-oss:20b` | `ollama/qwen3:14b` | `ollama/qwen3:4b` | `ollama/qwen3:4b-instruct-2507-q4_K_M` | `ollama/qwen3:8b` |
|---|---|---|---|---|---|
| `airline_planning` | 0.84 (181) | 0.64 (181) | 0.13 (181) | 0.20 (181) | 0.56 (181) |
| `assignment_with_constraints` | 0.87 (148) | 0.80 (148) | 0.38 (148) | 0.53 (148) | 0.61 (148) |
| `battery_scheduling` | 0.88 (217) | 0.61 (217) | 0.21 (217) | 0.40 (217) | 0.62 (217) |
| `bin_packing` | 0.94 (86) | 0.70 (86) | 0.24 (86) | 0.49 (86) | 0.74 (86) |
| `car_rental` | 0.94 (191) | 0.75 (191) | 0.21 (191) | 0.49 (191) | 0.55 (191) |
| `car_rental_2` | 0.91 (250) | 0.70 (250) | 0.28 (250) | 0.40 (250) | 0.56 (250) |
| `covid19_facility_location` | 0.91 (219) | 0.77 (219) | 0.25 (219) | 0.50 (219) | 0.66 (219) |
| `drone_network` | 0.83 (183) | 0.62 (183) | 0.38 (183) | 0.42 (183) | 0.51 (183) |
| `economic_planning` | 0.87 (220) | 0.72 (220) | 0.28 (220) | 0.50 (220) | 0.63 (220) |
| `factory_planning` | 0.92 (275) | 0.72 (275) | 0.22 (275) | 0.54 (275) | 0.53 (275) |
| `factory_planning_2` | 0.94 (216) | 0.73 (216) | 0.28 (216) | 0.46 (216) | 0.65 (216) |
| `fantasy_basketball` | 0.92 (105) | 0.79 (105) | 0.26 (105) | 0.50 (105) | 0.75 (105) |
| `farm_planning` | 0.91 (226) | 0.74 (226) | 0.34 (226) | 0.54 (226) | 0.51 (226) |
| `food_manufacture` | 0.95 (210) | 0.77 (210) | 0.31 (210) | 0.52 (210) | 0.69 (210) |
| `food_supply` | 0.80 (196) | 0.65 (196) | 0.28 (196) | 0.49 (196) | 0.52 (196) |
| `jobshop_ft06` | 0.84 (195) | 0.75 (195) | 0.24 (195) | 0.55 (195) | 0.56 (195) |
| `manpower_planning` | 0.91 (258) | 0.79 (258) | 0.18 (258) | 0.34 (258) | 0.57 (258) |
| `mining` | 0.93 (223) | 0.79 (223) | 0.22 (223) | 0.36 (223) | 0.58 (223) |
| `multiple_knapsack` | 0.96 (132) | 0.65 (132) | 0.30 (132) | 0.41 (132) | 0.62 (132) |
| `optimize_power_schedule` | 0.93 (182) | 0.77 (182) | 0.26 (182) | 0.46 (182) | 0.60 (182) |
| `power_generation_hydro` | 0.95 (220) | 0.83 (220) | 0.29 (220) | 0.48 (220) | 0.70 (220) |
| `railway_dispatching` | 0.85 (217) | 0.75 (217) | 0.09 (217) | 0.23 (217) | 0.60 (217) |
| `single_machine_scheduling` | 0.95 (55) | 0.78 (55) | 0.22 (55) | 0.55 (55) | 0.76 (55) |
| `technician_routing_scheduling` | 0.90 (196) | 0.70 (196) | 0.36 (196) | 0.38 (196) | 0.58 (196) |
| `wedding_seating` | 0.86 (35) | 0.31 (35) | 0.03 (35) | 0.34 (35) | 0.34 (35) |

## By template (where the misses are)

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
| logical_rule (nl) | l_never_both | 0.71 (14) | result differs from reference |
| under_specified | ask_g_cap_measure_scope | 0.73 (48) | invalid scenario |
| infeasible_request (nl) | i_floor_total | 0.75 (8) | result differs from reference |
| logical_rule (nl) | l_at_most_k | 0.75 (32) | result differs from reference |
| objective_change (nl) | o_then_min | 0.75 (4) | result differs from reference |
| under_specified | ask_g_floor_measure_scope | 0.75 (44) | invalid scenario |
| logical_rule (nl) | l_if_then | 0.76 (38) | result differs from reference |
| under_specified | ask_g_scale_all_rows | 0.79 (77) | result differs from reference |
| under_specified | ask_g_remove_row | 0.82 (33) | invalid scenario |
| relative_rule (nl) | combo | 0.82 (28) | result differs from reference |
| infeasible_request | i_floor_total | 0.82 (45) | result differs from reference |
| relax_remove | combo | 0.83 (6) | invalid DSL: unknown constraint family 'housing[year]'; families are ['ageing', 'beet_feed',  |
| relax_remove (nl) | x_full | 0.83 (6) | invalid DSL: removing these rows empties table 'maintenance' |
| logical_rule | l_if_then | 0.83 (103) | invalid DSL: Additional properties are not allowed ('logical' was unexpected) |
| fixed_decision | f_force_one | 0.84 (67) | result differs from reference |
| data_change | g_scale_all_rows | 0.85 (95) | result differs from reference |
| logical_rule (nl) | l_none_or_batch | 0.86 (42) | result differs from reference |
| relative_rule | combo | 0.87 (93) | result differs from reference |
| fixed_decision (nl) | f_force_one | 0.88 (16) | result differs from reference |
| fixed_decision (nl) | combo | 0.90 (20) | result differs from reference |
| new_limit (nl) | g_floor_measure_scope | 0.90 (30) | result differs from reference |
| relative_rule (nl) | r_share_of_total | 0.90 (40) | result differs from reference |
| fixed_decision | combo | 0.90 (82) | result differs from reference |
| relative_rule | r_two_values | 0.90 (136) | result differs from reference |
| objective_change | o_then_scoped | 0.91 (96) | result differs from reference |
| fixed_decision (nl) | f_fix_zero | 0.91 (34) | result differs from reference |
| objective_change | o_then_max | 0.91 (23) | result differs from reference |
| infeasible_request (nl) | i_two_floors | 0.92 (12) | result differs from reference |
| data_change (nl) | g_scale_all_rows | 0.92 (26) | result differs from reference |
| relative_rule | r_share_of_total | 0.92 (146) | result differs from reference |
| objective_change | o_three_stages | 0.93 (40) | result differs from reference |
| objective_change (nl) | o_then_max | 0.93 (14) | result differs from reference |
| data_change | combo | 0.93 (114) | result differs from reference |
| chained_scenario (nl) | c_add | 0.94 (62) | result differs from reference |
| relative_rule (nl) | r_two_values | 0.94 (32) | result differs from reference |
| relax_remove | x_full | 0.94 (16) | invalid DSL: removing these rows empties table 'maintenance' |
| logical_rule | l_none_or_batch | 0.94 (122) | result differs from reference |
| infeasible_request | i_floor | 0.94 (88) | result differs from reference |
| chained_scenario | c_undo | 0.94 (144) | result differs from reference |
| infeasible_request (nl) | i_commit | 0.94 (36) | result differs from reference |
| objective_change (nl) | o_then_scoped | 0.94 (18) | result differs from reference |
| infeasible_request | i_commit | 0.95 (133) | result differs from reference |
| infeasible_request | i_two_floors | 0.95 (58) | result differs from reference |
| data_change (nl) | g_set_column | 0.95 (20) | result differs from reference |
| fixed_decision | f_fix_scope | 0.96 (67) | unparseable output |
| fixed_decision (nl) | f_fix_level | 0.96 (24) | result differs from reference |
| objective_change | o_reorder | 0.96 (48) | result differs from reference |
| data_change | g_scale_column | 0.96 (76) | result differs from reference |
| relative_rule | r_two_measures | 0.96 (52) | result differs from reference |
| new_limit | combo | 0.97 (86) | result differs from reference |
| chained_scenario | c_add | 0.97 (174) | result differs from reference |
| new_limit (nl) | g_cap_measure_total | 0.97 (30) | result differs from reference |
| data_change (nl) | combo | 0.97 (36) | result differs from reference |
| fixed_decision | f_fix_zero | 0.98 (122) | invalid DSL: '5145 RURITAN COURT' is not a base; known values: ['21 MUNICIPAL CTR Fire Statio |
| new_limit | g_floor_measure_scope | 0.98 (82) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.98 (105) | result differs from reference |
| data_change | g_param | 0.98 (60) | invalid DSL: unknown table 'params'; tables are ['costs', 'requirements', 'retraining', 'skil |
| fixed_decision | f_fix_level | 0.99 (85) | result differs from reference |
| data_change | g_set_column | 0.99 (86) | result differs from reference |
| chained_scenario | c_revise | 1.00 (151) |  |
| chained_scenario (nl) | c_revise | 1.00 (40) |  |
| chained_scenario (nl) | c_undo | 1.00 (30) |  |
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
| data_change (nl) | demand_set | 1.00 (2) |  |
| data_change (nl) | g_add_row | 1.00 (4) |  |
| data_change (nl) | g_param | 1.00 (20) |  |
| data_change (nl) | g_remove_row | 1.00 (12) |  |
| data_change (nl) | g_scale_column | 1.00 (24) |  |
| data_change (nl) | margin_scale | 1.00 (2) |  |
| data_change (nl) | outage | 1.00 (2) |  |
| data_change (nl) | param | 1.00 (2) |  |
| fixed_decision (nl) | f_fix_scope | 1.00 (22) |  |
| infeasible_request (nl) | i_floor | 1.00 (26) |  |
| new_limit | cap_store_month | 1.00 (4) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit | g_cap_measure_total | 1.00 (87) |  |
| new_limit (nl) | cap_store_month | 1.00 (2) |  |
| new_limit (nl) | cap_total_make | 1.00 (4) |  |
| new_limit (nl) | combo | 1.00 (32) |  |
| new_limit (nl) | g_cap_measure_scope | 1.00 (20) |  |
| objective_change (nl) | o_reorder | 1.00 (4) |  |
| objective_change (nl) | o_three_stages | 1.00 (10) |  |
| relative_rule (nl) | r_two_measures | 1.00 (10) |  |
| relax_remove | x_scoped | 1.00 (86) |  |
| relax_remove (nl) | combo | 1.00 (4) |  |
| relax_remove (nl) | x_scoped | 1.00 (20) |  |
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
| data_change (nl) | outage | 0.00 (2) | invalid DSL: no row of 'downtime' matches {"month": "Jan", "machine": "vertDrill"} |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_store_month | 0.00 (1) | needed clarification not asked |
| under_specified | ask_install | 0.00 (1) | result differs from reference |
| under_specified | ask_margin_set | 0.00 (1) | needed clarification not asked |
| under_specified | ask_outage | 0.00 (1) | invalid DSL: row is missing columns ['machines_down'] |
| under_specified | ask_g_remove_row | 0.03 (33) | needed clarification not asked |
| logical_rule (nl) | l_at_most_k | 0.16 (32) | result differs from reference |
| logical_rule (nl) | l_if_then | 0.16 (38) | result differs from reference |
| under_specified | ask_g_cap_measure_total | 0.18 (45) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| logical_rule | l_if_then | 0.18 (103) | result differs from reference |
| logical_rule | l_at_most_k | 0.24 (108) | invalid DSL: [{'measure': 'operate', 'scope': {'flight': ['4265', '3074', '4514']}, 'sense':  |
| objective_change (nl) | o_reorder | 0.25 (4) | invalid DSL: {'type': 'string'} is not valid under any of the given schemas: {'type': 'string |
| under_specified | ask_g_scale_all_rows | 0.26 (77) | needed clarification not asked |
| logical_rule (nl) | l_none_or_batch | 0.33 (42) | result differs from reference |
| under_specified | ask_g_floor_measure_scope | 0.34 (44) | invalid DSL: [] is not valid under any of the given schemas: [] should be non-empty |
| data_change | margin_scale | 0.40 (5) | invalid DSL: invalid scale_param change: Additional properties are not allowed ('where' was u |
| under_specified | ask_g_add_row | 0.41 (17) | needed clarification not asked |
| logical_rule | l_never_both | 0.42 (48) | result differs from reference |
| under_specified | ask_g_cap_measure_scope | 0.42 (48) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| objective_change (nl) | o_then_max | 0.43 (14) | result differs from reference |
| objective_change | o_then_max | 0.43 (23) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| logical_rule | l_none_or_batch | 0.44 (122) | result differs from reference |
| under_specified | ask_g_param | 0.49 (41) | result differs from reference |
| infeasible_request | i_floor_total | 0.49 (45) | invalid DSL: {'type': 'string'} is not valid under any of the given schemas: {'type': 'string |
| data_change (nl) | g_scale_all_rows | 0.50 (26) | invalid DSL: invalid scale change: {'flight': [1, 73, 2, 74, 75, 3, 76, 4, 5, 77, 6, 78, 79,  |
| data_change (nl) | margin_scale | 0.50 (2) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| relax_remove | combo | 0.50 (6) | invalid DSL: unknown constraint family 'size[worker]'; families are ['cover', 'one_team', 'si |
| relax_remove (nl) | combo | 0.50 (4) | invalid DSL: unknown constraint family 'max_operating[year]'; families are ['capacity', 'mass |
| under_specified | ask_retire | 0.50 (2) | result differs from reference |
| data_change | g_scale_all_rows | 0.51 (95) | unparseable output |
| data_change (nl) | combo | 0.53 (36) | invalid DSL: invalid scale change: {} should be non-empty |
| chained_scenario | c_add | 0.53 (174) | invalid DSL: {'type': 'string'} is not valid under any of the given schemas: {'type': 'string |
| data_change | combo | 0.55 (114) | invalid DSL: invalid scale change: {} should be non-empty |
| relative_rule (nl) | r_share_of_total | 0.57 (40) | invalid DSL: 'all' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '10 |
| objective_change | o_then_min | 0.60 (10) | result differs from reference |
| under_specified | ask_g_set_column | 0.61 (84) | needed clarification not asked |
| under_specified | ask_g_scale_column | 0.61 (77) | invalid DSL: column 'revenue' is numeric; got 'new_revenue_value' |
| infeasible_request (nl) | i_floor_total | 0.62 (8) | result differs from reference |
| relative_rule | r_two_measures | 0.63 (52) | invalid DSL: 'all' is not a worker; known values: ['worker_0', 'worker_1', 'worker_10', 'work |
| chained_scenario (nl) | c_add | 0.65 (62) | invalid DSL: invalid scale change: {'set': [1, 73, 2, 74, 75, 3, 76, 4, 5, 77, 6, 78, 79, 7,  |
| under_specified | ask_demand_scale | 0.67 (3) | needed clarification not asked |
| fixed_decision | f_fix_scope | 0.70 (67) | result differs from reference |
| logical_rule (nl) | l_never_both | 0.71 (14) | result differs from reference |
| objective_change (nl) | o_then_scoped | 0.72 (18) | result differs from reference |
| objective_change | o_three_stages | 0.72 (40) | invalid DSL: {'type': 'array', 'items': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06' |
| new_limit (nl) | g_cap_measure_total | 0.73 (30) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| relative_rule | combo | 0.74 (93) | invalid DSL: 'all' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '10 |
| objective_change (nl) | o_then_min | 0.75 (4) | result differs from reference |
| relative_rule (nl) | combo | 0.79 (28) | invalid DSL: Additional properties are not allowed ('factor', 'relative_to' were unexpected) |
| relative_rule | r_share_of_total | 0.79 (146) | invalid DSL: 'all' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '10 |
| objective_change (nl) | o_three_stages | 0.80 (10) | invalid DSL: {'type': 'array', 'items': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06' |
| relative_rule (nl) | r_two_measures | 0.80 (10) | invalid DSL: 'all' is not a month; known values: ['Apr', 'Feb', 'Jan', 'Jun', 'Mar', 'May'] |
| objective_change | o_reorder | 0.81 (48) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| relax_remove | x_full | 0.81 (16) | invalid DSL: constraint family 'one_team' cannot be relaxed in this model; change the data or |
| fixed_decision (nl) | f_fix_scope | 0.82 (22) | invalid DSL: unknown table 'undamaged_stock'; tables are ['days', 'demand', 'depots', 'rental |
| data_change (nl) | g_scale_column | 0.83 (24) | invalid DSL: unknown parameter 'grain_yield'; parameters are ['beet_acre_cost', 'beet_labour_ |
| relax_remove (nl) | x_full | 0.83 (6) | invalid DSL: removing these rows empties table 'maintenance' |
| new_limit | combo | 0.84 (86) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| new_limit | g_cap_measure_total | 0.84 (87) | invalid DSL: {'all': True} is not valid under any of the given schemas: {'all': True} is not  |
| relax_remove (nl) | x_scoped | 0.85 (20) | invalid DSL: unknown constraint family 'team_pattern[worker]'; families are ['cover', 'one_te |
| fixed_decision (nl) | f_fix_zero | 0.85 (34) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| chained_scenario | c_undo | 0.86 (144) | invalid DSL: invalid scale change: {} should be non-empty |
| infeasible_request | i_two_floors | 0.86 (58) | result differs from reference |
| fixed_decision | combo | 0.87 (82) | result differs from reference |
| fixed_decision (nl) | f_force_one | 0.88 (16) | invalid DSL: unknown table 'assign'; tables are ['allowed_teams', 'costs', 'tasks', 'workers' |
| objective_change | o_then_scoped | 0.89 (96) | invalid DSL: {'depot': ['Glasgow', 'Manchester', 'Birmingham', 'Plymouth']} is not valid unde |
| relax_remove | x_scoped | 0.90 (86) | invalid DSL: unknown constraint family 'team_pattern[worker]'; families are ['cover', 'one_te |
| data_change | g_scale_column | 0.91 (76) | result differs from reference |
| fixed_decision | f_fix_zero | 0.91 (122) | invalid DSL: '4265' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| infeasible_request (nl) | i_two_floors | 0.92 (12) | result differs from reference |
| infeasible_request (nl) | i_floor | 0.92 (26) | invalid DSL: unknown table 'repairs'; tables are ['days', 'demand', 'depots', 'expansion_opti |
| relative_rule | r_two_values | 0.93 (136) | result differs from reference |
| infeasible_request | i_floor | 0.94 (88) | result differs from reference |
| infeasible_request (nl) | i_commit | 0.94 (36) | result differs from reference |
| data_change | g_param | 0.95 (60) | invalid DSL: invalid scale change: {} should be non-empty |
| data_change (nl) | g_param | 0.95 (20) | result differs from reference |
| fixed_decision (nl) | combo | 0.95 (20) | invalid DSL: unknown table 'assign'; tables are ['customers', 'job_types', 'skills', 'technic |
| infeasible_request | i_commit | 0.95 (133) | result differs from reference |
| fixed_decision (nl) | f_fix_level | 0.96 (24) | result differs from reference |
| chained_scenario (nl) | c_undo | 0.97 (30) | result differs from reference |
| new_limit (nl) | g_floor_measure_scope | 0.97 (30) | result differs from reference |
| new_limit (nl) | combo | 0.97 (32) | invalid DSL: 'all' is not a location; known values: ['100 N WITCHDUCK RD', '1000 BELVOIR LA', |
| relative_rule (nl) | r_two_values | 0.97 (32) | invalid DSL: 'resource' is not a resource; known values: ['0', '1', '2', '3', '4', '5', '6'] |
| new_limit | g_floor_measure_scope | 0.98 (82) | invalid DSL: at_least is 15 but there are only 6 conditions |
| fixed_decision | f_force_one | 0.99 (67) | result differs from reference |
| fixed_decision | f_fix_level | 0.99 (85) | invalid DSL: '2' is not a resource; known values: ['0', '1', '2', '3', '4', '5', '6'] |
| data_change | g_set_column | 0.99 (86) | invalid DSL: measure 'pick' has dimensions ['player'], not 'position' |
| new_limit | g_cap_measure_scope | 0.99 (105) | invalid DSL: {'train': 'D'} is not valid under any of the given schemas: {'train': 'D'} is no |
| chained_scenario | c_revise | 1.00 (151) |  |
| chained_scenario (nl) | c_revise | 1.00 (40) |  |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (18) |  |
| data_change | g_remove_row | 1.00 (19) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |
| data_change (nl) | demand_set | 1.00 (2) |  |
| data_change (nl) | g_add_row | 1.00 (4) |  |
| data_change (nl) | g_remove_row | 1.00 (12) |  |
| data_change (nl) | g_set_column | 1.00 (20) |  |
| data_change (nl) | param | 1.00 (2) |  |
| new_limit | cap_store_month | 1.00 (4) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit (nl) | cap_store_month | 1.00 (2) |  |
| new_limit (nl) | cap_total_make | 1.00 (4) |  |
| new_limit (nl) | g_cap_measure_scope | 1.00 (20) |  |
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
| fixed_decision | f_fix_scope | 0.12 (67) | invalid DSL: unknown table 'rentals'; tables are ['days', 'demand', 'depots', 'rental_lengths |
| logical_rule | l_never_both | 0.12 (48) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| relax_remove | x_full | 0.12 (16) | result differs from reference |
| relative_rule | r_share_of_total | 0.13 (146) | invalid DSL: '4514' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| new_limit (nl) | g_cap_measure_total | 0.13 (30) | invalid DSL: invalid set change: {'aircraft': ['TranspCom#1', 'TranspCom#3', 'TranspCom#2', ' |
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
| new_limit (nl) | g_cap_measure_scope | 0.20 (20) | invalid DSL: unknown table 'operate'; tables are ['aircraft', 'airports', 'flights'] |
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
| new_limit (nl) | g_floor_measure_scope | 0.27 (30) | invalid DSL: no row of 'tasks' matches {"task": "worker_10"} |
| fixed_decision (nl) | f_fix_scope | 0.27 (22) | result differs from reference |
| objective_change | o_then_scoped | 0.29 (96) | result differs from reference |
| chained_scenario (nl) | c_undo | 0.30 (30) | invalid DSL: table 'hours' has no column 'soc'; columns are ['export_price', 'hour', 'import_ |
| chained_scenario | c_add | 0.31 (174) | result differs from reference |
| data_change | process_hours | 0.33 (3) | result differs from reference |
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
| data_change (nl) | g_scale_all_rows | 0.50 (26) | invalid DSL: no row of 'flights' matches {"flight": ["1", "2", "3", "4", "5", "6", "7", "8",  |
| data_change (nl) | margin_scale | 0.50 (2) | result differs from reference |
| new_limit | cap_two_products_month | 0.50 (2) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.54 (105) | invalid DSL: '1' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '104' |
| data_change (nl) | g_set_column | 0.55 (20) | result differs from reference |
| data_change | g_add_row | 0.56 (18) | invalid DSL: row is missing columns ['weight'] |
| new_limit | combo | 0.57 (86) | invalid DSL: '1' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '104' |
| data_change | g_remove_row | 0.58 (19) | result differs from reference |
| chained_scenario (nl) | c_revise | 0.60 (40) | result differs from reference |
| new_limit (nl) | combo | 0.62 (32) | invalid DSL: table 'flights' has no column 'operate'; columns are ['aircraft', 'arrival', 'de |
| data_change (nl) | g_scale_column | 0.67 (24) | result differs from reference |
| data_change | g_scale_all_rows | 0.69 (95) | invalid DSL: no row of 'flights' matches {"flight": ["1", "2", "3", "4", "5", "6", "7", "8",  |
| chained_scenario | c_revise | 0.70 (151) | result differs from reference |
| data_change | g_set_column | 0.71 (86) | result differs from reference |
| fixed_decision (nl) | combo | 0.75 (20) | invalid DSL: unknown table 'damaged_left'; tables are ['days', 'demand', 'depots', 'rental_le |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change (nl) | demand_set | 1.00 (2) |  |

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
| `ollama/gpt-oss:20b` | 301 | 161 | 20 | 217 | 0 | 0 |
| `ollama/qwen3:14b` | 682 | 587 | 3 | 3 | 0 | 0 |
| `ollama/qwen3:4b` | 2174 | 1279 | 3 | 3 | 0 | 1062 |
| `ollama/qwen3:4b-instruct-2507-q4_K_M` | 1078 | 1514 | 17 | 17 | 0 | 0 |
| `ollama/qwen3:8b` | 1079 | 787 | 6 | 6 | 0 | 0 |
