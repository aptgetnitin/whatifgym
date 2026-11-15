# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | chained_scenario (nl) | data_change | data_change (nl) | fixed_decision | fixed_decision (nl) | infeasible_request | infeasible_request (nl) | logical_rule | logical_rule (nl) | new_limit | new_limit (nl) | objective_change | objective_change (nl) | relative_rule | relative_rule (nl) | relax_remove | relax_remove (nl) | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/gpt-oss:20b` | 4636 | 0.900 | 0.995 | 0.97 | 0.99 | 0.97 (469) | 0.97 (132) | 0.95 (512) | 0.97 (150) | 0.94 (423) | 0.93 (116) | 0.93 (324) | 0.94 (82) | 0.78 (381) | 0.79 (126) | 0.98 (375) | 0.97 (118) | 0.91 (217) | 0.94 (50) | 0.91 (427) | 0.90 (110) | 0.98 (108) | 0.97 (30) | 0.68 (486) | 0.96 (575) | 0.88 (2647) | 0.90 (1414) | 10.7 |

## By base model

| base model | `ollama/gpt-oss:20b` |
|---|---|
| `airline_planning` | 0.84 (181) |
| `assignment_with_constraints` | 0.87 (148) |
| `battery_scheduling` | 0.88 (217) |
| `bin_packing` | 0.94 (86) |
| `car_rental` | 0.94 (191) |
| `car_rental_2` | 0.91 (250) |
| `covid19_facility_location` | 0.91 (219) |
| `drone_network` | 0.83 (183) |
| `economic_planning` | 0.87 (220) |
| `factory_planning` | 0.92 (275) |
| `factory_planning_2` | 0.94 (216) |
| `fantasy_basketball` | 0.92 (105) |
| `farm_planning` | 0.91 (226) |
| `food_manufacture` | 0.95 (210) |
| `food_supply` | 0.80 (196) |
| `jobshop_ft06` | 0.84 (195) |
| `manpower_planning` | 0.91 (258) |
| `mining` | 0.93 (223) |
| `multiple_knapsack` | 0.96 (132) |
| `optimize_power_schedule` | 0.93 (182) |
| `power_generation_hydro` | 0.95 (220) |
| `railway_dispatching` | 0.85 (217) |
| `single_machine_scheduling` | 0.95 (55) |
| `technician_routing_scheduling` | 0.90 (196) |
| `wedding_seating` | 0.86 (35) |

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/gpt-oss:20b` | 301 | 161 | 20 | 217 | 0 | 0 |
