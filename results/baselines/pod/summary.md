# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | chained_scenario (nl) | data_change | data_change (nl) | fixed_decision | fixed_decision (nl) | infeasible_request | infeasible_request (nl) | logical_rule | logical_rule (nl) | new_limit | new_limit (nl) | objective_change | objective_change (nl) | relative_rule | relative_rule (nl) | relax_remove | relax_remove (nl) | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `vllm/trained-run5-seed1` | 4636 | 0.635 | 0.715 | 0.87 | 0.92 | 0.70 (469) | 0.59 (132) | 0.80 (512) | 0.81 (150) | 0.86 (423) | 0.86 (116) | 0.75 (324) | 0.73 (82) | 0.22 (381) | 0.18 (126) | 0.82 (375) | 0.72 (118) | 0.70 (217) | 0.56 (50) | 0.71 (427) | 0.71 (110) | 0.71 (108) | 0.70 (30) | 0.16 (486) | 0.79 (575) | 0.61 (2647) | 0.62 (1414) | – |
| `vllm/trained-run5-seed2` | 4636 | 0.632 | 0.712 | 0.87 | 0.92 | 0.70 (469) | 0.59 (132) | 0.78 (512) | 0.81 (150) | 0.86 (423) | 0.84 (116) | 0.74 (324) | 0.74 (82) | 0.21 (381) | 0.18 (126) | 0.84 (375) | 0.77 (118) | 0.70 (217) | 0.54 (50) | 0.74 (427) | 0.74 (110) | 0.69 (108) | 0.70 (30) | 0.13 (486) | 0.79 (575) | 0.60 (2647) | 0.62 (1414) | – |
| `vllm/trained-run5-seed3` | 4636 | 0.629 | 0.709 | 0.88 | 0.92 | 0.70 (469) | 0.59 (132) | 0.79 (512) | 0.81 (150) | 0.84 (423) | 0.84 (116) | 0.74 (324) | 0.74 (82) | 0.20 (381) | 0.19 (126) | 0.84 (375) | 0.74 (118) | 0.68 (217) | 0.54 (50) | 0.72 (427) | 0.72 (110) | 0.72 (108) | 0.70 (30) | 0.14 (486) | 0.80 (575) | 0.60 (2647) | 0.62 (1414) | – |
| `vllm/training-base` | 4636 | 0.500 | 0.567 | 0.73 | 0.93 | 0.62 (469) | 0.52 (132) | 0.68 (512) | 0.73 (150) | 0.78 (423) | 0.78 (116) | 0.53 (324) | 0.52 (82) | 0.16 (381) | 0.14 (126) | 0.68 (375) | 0.58 (118) | 0.46 (217) | 0.36 (50) | 0.34 (427) | 0.36 (110) | 0.56 (108) | 0.70 (30) | 0.16 (486) | 0.66 (575) | 0.47 (2647) | 0.49 (1414) | – |

## By base model

| base model | `vllm/trained-run5-seed1` | `vllm/trained-run5-seed2` | `vllm/trained-run5-seed3` | `vllm/training-base` |
|---|---|---|---|---|
| `airline_planning` | 0.50 (181) | 0.48 (181) | 0.45 (181) | 0.41 (181) |
| `assignment_with_constraints` | 0.73 (148) | 0.74 (148) | 0.72 (148) | 0.56 (148) |
| `battery_scheduling` | 0.69 (217) | 0.69 (217) | 0.70 (217) | 0.53 (217) |
| `bin_packing` | 0.62 (86) | 0.62 (86) | 0.62 (86) | 0.47 (86) |
| `car_rental` | 0.66 (191) | 0.65 (191) | 0.67 (191) | 0.47 (191) |
| `car_rental_2` | 0.65 (250) | 0.64 (250) | 0.64 (250) | 0.49 (250) |
| `covid19_facility_location` | 0.61 (219) | 0.61 (219) | 0.60 (219) | 0.48 (219) |
| `drone_network` | 0.58 (183) | 0.59 (183) | 0.57 (183) | 0.49 (183) |
| `economic_planning` | 0.63 (220) | 0.60 (220) | 0.60 (220) | 0.50 (220) |
| `factory_planning` | 0.62 (275) | 0.61 (275) | 0.64 (275) | 0.48 (275) |
| `factory_planning_2` | 0.63 (216) | 0.64 (216) | 0.63 (216) | 0.47 (216) |
| `fantasy_basketball` | 0.68 (105) | 0.63 (105) | 0.61 (105) | 0.58 (105) |
| `farm_planning` | 0.62 (226) | 0.64 (226) | 0.63 (226) | 0.56 (226) |
| `food_manufacture` | 0.79 (210) | 0.78 (210) | 0.78 (210) | 0.61 (210) |
| `food_supply` | 0.69 (196) | 0.69 (196) | 0.68 (196) | 0.57 (196) |
| `jobshop_ft06` | 0.62 (195) | 0.62 (195) | 0.62 (195) | 0.50 (195) |
| `manpower_planning` | 0.58 (258) | 0.58 (258) | 0.57 (258) | 0.50 (258) |
| `mining` | 0.62 (223) | 0.61 (223) | 0.62 (223) | 0.52 (223) |
| `multiple_knapsack` | 0.61 (132) | 0.60 (132) | 0.58 (132) | 0.43 (132) |
| `optimize_power_schedule` | 0.67 (182) | 0.67 (182) | 0.66 (182) | 0.51 (182) |
| `power_generation_hydro` | 0.73 (220) | 0.74 (220) | 0.73 (220) | 0.60 (220) |
| `railway_dispatching` | 0.59 (217) | 0.58 (217) | 0.56 (217) | 0.40 (217) |
| `single_machine_scheduling` | 0.71 (55) | 0.73 (55) | 0.71 (55) | 0.56 (55) |
| `technician_routing_scheduling` | 0.54 (196) | 0.58 (196) | 0.57 (196) | 0.37 (196) |
| `wedding_seating` | 0.37 (35) | 0.37 (35) | 0.37 (35) | 0.37 (35) |

## By template (where the misses are)

### `vllm/trained-run5-seed1`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | result differs from reference |
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| data_change (nl) | outage | 0.00 (2) | invalid DSL: invalid set change: 'column' is a required property |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| new_limit | cap_total_make | 0.00 (5) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_store_month | 0.00 (1) | needed clarification not asked |
| under_specified | ask_cap_total_store | 0.00 (2) | result differs from reference |
| under_specified | ask_cap_two_products_month | 0.00 (2) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| under_specified | ask_demand_scale | 0.00 (3) | needed clarification not asked |
| under_specified | ask_demand_zero | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_param | 0.00 (41) | needed clarification not asked |
| under_specified | ask_g_remove_row | 0.00 (33) | needed clarification not asked |
| under_specified | ask_install | 0.00 (1) | needed clarification not asked |
| under_specified | ask_margin_scale | 0.00 (1) | invalid scenario |
| under_specified | ask_outage | 0.00 (1) | invalid DSL: row is missing columns ['machines_down'] |
| under_specified | ask_outage_cancel | 0.00 (1) | result differs from reference |
| logical_rule | l_if_then | 0.08 (103) | result differs from reference |
| logical_rule (nl) | l_if_then | 0.13 (38) | result differs from reference |
| under_specified | ask_g_set_column | 0.14 (84) | needed clarification not asked |
| under_specified | ask_g_scale_all_rows | 0.16 (77) | unparseable output |
| logical_rule (nl) | l_at_most_k | 0.16 (32) | result differs from reference |
| logical_rule | l_at_most_k | 0.19 (108) | result differs from reference |
| logical_rule (nl) | l_none_or_batch | 0.19 (42) | result differs from reference |
| under_specified | ask_g_scale_column | 0.19 (77) | needed clarification not asked |
| under_specified | ask_g_cap_measure_total | 0.20 (45) | invalid DSL: [] is not valid under any of the given schemas: [] should be non-empty |
| under_specified | ask_g_cap_measure_scope | 0.23 (48) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| new_limit (nl) | cap_total_make | 0.25 (4) | result differs from reference |
| objective_change (nl) | o_reorder | 0.25 (4) | invalid DSL: unknown measure 'response_objective'; measures are ['assign', 'linked_load', 'op |
| relax_remove (nl) | combo | 0.25 (4) | invalid DSL: unknown table 'params'; tables are ['ages', 'land_groups', 'years'] |
| under_specified | ask_g_floor_measure_scope | 0.25 (44) | needed clarification not asked |
| logical_rule | l_never_both | 0.27 (48) | invalid DSL: 'any' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| objective_change (nl) | o_then_max | 0.29 (14) | result differs from reference |
| chained_scenario (nl) | c_add | 0.29 (62) | result differs from reference |
| under_specified | ask_g_add_row | 0.29 (17) | needed clarification not asked |
| objective_change | o_then_min | 0.30 (10) | result differs from reference |
| objective_change | o_then_max | 0.30 (23) | result differs from reference |
| logical_rule | l_none_or_batch | 0.34 (122) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| chained_scenario | c_add | 0.36 (174) | result differs from reference |
| logical_rule (nl) | l_never_both | 0.36 (14) | invalid DSL: scope selects no variable |
| infeasible_request (nl) | i_floor_total | 0.38 (8) | result differs from reference |
| infeasible_request (nl) | i_two_floors | 0.42 (12) | result differs from reference |
| new_limit | cap_two_products_month | 0.50 (2) | invalid DSL: unknown table 'make'; tables are ['downtime', 'machines', 'max_sales', 'months', |
| new_limit (nl) | cap_store_month | 0.50 (2) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| objective_change | o_three_stages | 0.50 (40) | invalid DSL: 'hour' is not of type 'object' |
| under_specified | ask_retire | 0.50 (2) | needed clarification not asked |
| infeasible_request | i_floor_total | 0.51 (45) | invalid DSL: 'all' is not a base; known values: ['21 MUNICIPAL CTR Fire Station', '2837 SHORE |
| relative_rule (nl) | combo | 0.54 (28) | invalid DSL: '4513' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| relative_rule | combo | 0.55 (93) | invalid DSL: '4564' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| objective_change (nl) | o_three_stages | 0.60 (10) | invalid DSL: 'J5' is not a job; known values: ['J0', 'J1', 'J2', 'J3', 'J4'] |
| data_change | combo | 0.62 (114) | result differs from reference |
| new_limit (nl) | combo | 0.62 (32) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| infeasible_request | i_two_floors | 0.64 (58) | invalid DSL: 'all' is not a county; known values: ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',  |
| data_change (nl) | combo | 0.64 (36) | invalid DSL: unknown measure 'min_workers'; measures are ['assign', 'team', 'works'] |
| data_change | retire | 0.67 (3) | result differs from reference |
| new_limit | cap_total_store | 0.67 (3) | invalid DSL: "The total unit-months of stock is the sum of store[month, product] over all mon |
| new_limit (nl) | g_cap_measure_total | 0.67 (30) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| relax_remove | combo | 0.67 (6) | invalid DSL: unknown constraint family 'max_operating[year]'; families are ['capacity', 'mass |
| relax_remove (nl) | x_full | 0.67 (6) | result differs from reference |
| infeasible_request | i_floor | 0.67 (88) | invalid DSL: 'any' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| relax_remove | x_full | 0.69 (16) | result differs from reference |
| relative_rule | r_share_of_total | 0.70 (146) | invalid DSL: '4514' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| chained_scenario (nl) | c_undo | 0.70 (30) | invalid DSL: table 'process_hours' has no column 'month'; columns are ['hours_per_unit', 'mac |
| data_change | g_param | 0.72 (60) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| relax_remove | x_scoped | 0.72 (86) | invalid DSL: unknown measure 'capacity'; measures are ['assign', 'build', 'extra_beds'] |
| relative_rule (nl) | r_share_of_total | 0.72 (40) | invalid DSL: '4564' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| infeasible_request (nl) | i_floor | 0.73 (26) | invalid DSL: '=' is not one of ['<=', '>=', '=='] |
| fixed_decision | f_fix_scope | 0.75 (67) | invalid DSL: '=' is not one of ['<=', '>=', '=='] |
| data_change (nl) | g_set_column | 0.75 (20) | result differs from reference |
| fixed_decision (nl) | combo | 0.75 (20) | result differs from reference |
| objective_change (nl) | o_then_min | 0.75 (4) | result differs from reference |
| new_limit | combo | 0.76 (86) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| relative_rule | r_two_measures | 0.77 (52) | unparseable output |
| objective_change (nl) | o_then_scoped | 0.78 (18) | result differs from reference |
| data_change | g_scale_all_rows | 0.78 (95) | unparseable output |
| new_limit | g_cap_measure_total | 0.79 (87) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| data_change | param | 0.80 (5) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| new_limit (nl) | g_floor_measure_scope | 0.80 (30) | result differs from reference |
| relative_rule (nl) | r_two_measures | 0.80 (10) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| relax_remove (nl) | x_scoped | 0.80 (20) | invalid DSL: table 'depots' has no column 'day'; columns are ['depot', 'repair_capacity'] |
| fixed_decision | combo | 0.80 (82) | invalid DSL: constraint family 'one_team' has dimensions ['group'], not 'team' |
| objective_change | o_reorder | 0.81 (48) | invalid DSL: unknown measure 'sum(expand, depot, step)'; measures are ['damaged_left', 'damag |
| relative_rule (nl) | r_two_values | 0.81 (32) | invalid DSL: '4572' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| relative_rule | r_two_values | 0.82 (136) | invalid DSL: '4572' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| fixed_decision (nl) | f_fix_scope | 0.82 (22) | result differs from reference |
| chained_scenario | c_undo | 0.83 (144) | result differs from reference |
| fixed_decision | f_force_one | 0.84 (67) | invalid DSL: '3076' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| data_change (nl) | g_param | 0.85 (20) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| objective_change | o_then_scoped | 0.85 (96) | result differs from reference |
| new_limit | g_floor_measure_scope | 0.88 (82) | result differs from reference |
| fixed_decision (nl) | f_fix_zero | 0.88 (34) | invalid DSL: '4273' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| data_change (nl) | g_scale_all_rows | 0.88 (26) | unparseable output |
| data_change | g_set_column | 0.90 (86) | result differs from reference |
| data_change | g_scale_column | 0.91 (76) | result differs from reference |
| data_change (nl) | g_scale_column | 0.92 (24) | result differs from reference |
| fixed_decision (nl) | f_fix_level | 0.92 (24) | result differs from reference |
| infeasible_request (nl) | i_commit | 0.92 (36) | result differs from reference |
| fixed_decision | f_fix_zero | 0.92 (122) | invalid DSL: '3103' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| fixed_decision (nl) | f_force_one | 0.94 (16) | result differs from reference |
| infeasible_request | i_commit | 0.94 (133) | result differs from reference |
| fixed_decision | f_fix_level | 0.94 (85) | result differs from reference |
| new_limit (nl) | g_cap_measure_scope | 0.95 (20) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| new_limit | g_cap_measure_scope | 0.95 (105) | invalid DSL: 'J0' is not a other_job; known values: ['J1', 'J2', 'J3', 'J4', 'J5'] |
| chained_scenario | c_revise | 0.97 (151) | result differs from reference |
| chained_scenario (nl) | c_revise | 0.97 (40) | invalid DSL: [] should be non-empty |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (18) |  |
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
| under_specified | ask_cap_make_months | 1.00 (1) |  |
| under_specified | ask_cap_total_make | 1.00 (2) |  |
| under_specified | ask_margin_set | 1.00 (1) |  |

### `vllm/trained-run5-seed2`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | result differs from reference |
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| data_change (nl) | outage | 0.00 (2) | invalid DSL: invalid set change: 'column' is a required property |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| new_limit | cap_total_make | 0.00 (5) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_store_month | 0.00 (1) | needed clarification not asked |
| under_specified | ask_cap_total_store | 0.00 (2) | result differs from reference |
| under_specified | ask_cap_two_products_month | 0.00 (2) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| under_specified | ask_demand_scale | 0.00 (3) | needed clarification not asked |
| under_specified | ask_demand_zero | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_param | 0.00 (41) | needed clarification not asked |
| under_specified | ask_g_remove_row | 0.00 (33) | needed clarification not asked |
| under_specified | ask_install | 0.00 (1) | needed clarification not asked |
| under_specified | ask_margin_scale | 0.00 (1) | invalid scenario |
| under_specified | ask_margin_set | 0.00 (1) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| under_specified | ask_outage | 0.00 (1) | invalid DSL: row is missing columns ['machines_down'] |
| under_specified | ask_outage_cancel | 0.00 (1) | result differs from reference |
| under_specified | ask_g_scale_all_rows | 0.08 (77) | unparseable output |
| under_specified | ask_g_cap_measure_total | 0.09 (45) | invalid DSL: [] is not valid under any of the given schemas: [] should be non-empty |
| logical_rule | l_if_then | 0.10 (103) | result differs from reference |
| logical_rule (nl) | l_if_then | 0.11 (38) | result differs from reference |
| under_specified | ask_g_set_column | 0.13 (84) | needed clarification not asked |
| under_specified | ask_g_scale_column | 0.16 (77) | needed clarification not asked |
| logical_rule (nl) | l_at_most_k | 0.16 (32) | result differs from reference |
| logical_rule | l_at_most_k | 0.18 (108) | invalid DSL: '4265' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| logical_rule (nl) | l_none_or_batch | 0.21 (42) | result differs from reference |
| logical_rule | l_never_both | 0.23 (48) | invalid DSL: 'any' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| new_limit (nl) | cap_total_make | 0.25 (4) | result differs from reference |
| objective_change (nl) | o_reorder | 0.25 (4) | invalid DSL: unknown measure 'response_objective'; measures are ['assign', 'linked_load', 'op |
| relax_remove (nl) | combo | 0.25 (4) | invalid DSL: unknown table 'params'; tables are ['ages', 'land_groups', 'years'] |
| under_specified | ask_g_cap_measure_scope | 0.25 (48) | needed clarification not asked |
| under_specified | ask_g_floor_measure_scope | 0.25 (44) | needed clarification not asked |
| chained_scenario (nl) | c_add | 0.27 (62) | result differs from reference |
| under_specified | ask_g_add_row | 0.29 (17) | needed clarification not asked |
| objective_change | o_then_min | 0.30 (10) | result differs from reference |
| objective_change | o_then_max | 0.30 (23) | result differs from reference |
| logical_rule | l_none_or_batch | 0.32 (122) | result differs from reference |
| chained_scenario | c_add | 0.36 (174) | result differs from reference |
| logical_rule (nl) | l_never_both | 0.36 (14) | invalid DSL: scope selects no variable |
| objective_change (nl) | o_then_max | 0.36 (14) | result differs from reference |
| objective_change (nl) | o_three_stages | 0.40 (10) | invalid DSL: 'hour' is not of type 'object' |
| infeasible_request | i_floor_total | 0.49 (45) | invalid DSL: 'all' is not a base; known values: ['21 MUNICIPAL CTR Fire Station', '2837 SHORE |
| infeasible_request (nl) | i_floor_total | 0.50 (8) | invalid scenario |
| infeasible_request (nl) | i_two_floors | 0.50 (12) | result differs from reference |
| new_limit | cap_two_products_month | 0.50 (2) | invalid DSL: unknown table 'make'; tables are ['downtime', 'machines', 'max_sales', 'months', |
| new_limit (nl) | cap_store_month | 0.50 (2) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| objective_change | o_three_stages | 0.50 (40) | invalid DSL: 'hour' is not of type 'object' |
| under_specified | ask_cap_total_make | 0.50 (2) | invalid scenario |
| under_specified | ask_retire | 0.50 (2) | needed clarification not asked |
| relative_rule (nl) | combo | 0.54 (28) | invalid DSL: '4513' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| data_change | combo | 0.58 (114) | result differs from reference |
| relative_rule | combo | 0.59 (93) | result differs from reference |
| infeasible_request | i_two_floors | 0.64 (58) | invalid DSL: '*' is not a county; known values: ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C |
| data_change (nl) | combo | 0.64 (36) | result differs from reference |
| infeasible_request | i_floor | 0.65 (88) | invalid DSL: 'any' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| data_change | retire | 0.67 (3) | result differs from reference |
| new_limit | cap_total_store | 0.67 (3) | unparseable output |
| relax_remove | combo | 0.67 (6) | invalid DSL: unknown constraint family 'max_operating[year]'; families are ['capacity', 'mass |
| relax_remove (nl) | x_full | 0.67 (6) | result differs from reference |
| relax_remove | x_scoped | 0.69 (86) | result differs from reference |
| relax_remove | x_full | 0.69 (16) | result differs from reference |
| infeasible_request (nl) | i_floor | 0.69 (26) | invalid DSL: '=' is not one of ['<=', '>=', '=='] |
| new_limit (nl) | g_cap_measure_total | 0.70 (30) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| new_limit (nl) | combo | 0.72 (32) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| chained_scenario (nl) | c_undo | 0.73 (30) | invalid DSL: table 'process_hours' has no column 'month'; columns are ['hours_per_unit', 'mac |
| data_change | g_param | 0.73 (60) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| fixed_decision | f_fix_scope | 0.75 (67) | invalid DSL: '=' is not one of ['<=', '>=', '=='] |
| relative_rule | r_share_of_total | 0.75 (146) | invalid DSL: '4514' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| data_change | g_scale_all_rows | 0.75 (95) | unparseable output |
| data_change (nl) | g_set_column | 0.75 (20) | result differs from reference |
| objective_change (nl) | o_then_min | 0.75 (4) | result differs from reference |
| relative_rule (nl) | r_share_of_total | 0.75 (40) | invalid DSL: '4564' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| new_limit | combo | 0.77 (86) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| fixed_decision (nl) | f_fix_scope | 0.77 (22) | result differs from reference |
| objective_change (nl) | o_then_scoped | 0.78 (18) | result differs from reference |
| objective_change | o_reorder | 0.79 (48) | invalid DSL: unknown measure 'sum(expand, depot, step)'; measures are ['damaged_left', 'damag |
| data_change | param | 0.80 (5) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| fixed_decision (nl) | combo | 0.80 (20) | result differs from reference |
| relax_remove (nl) | x_scoped | 0.80 (20) | invalid DSL: table 'depots' has no column 'day'; columns are ['depot', 'repair_capacity'] |
| relative_rule | r_two_values | 0.80 (136) | invalid DSL: '4572' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| fixed_decision | combo | 0.80 (82) | invalid DSL: constraint family 'one_team' has dimensions ['group'], not 'team' |
| relative_rule | r_two_measures | 0.81 (52) | invalid DSL: [] is not valid under any of the given schemas: [] should be non-empty |
| new_limit | g_cap_measure_total | 0.83 (87) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| fixed_decision | f_force_one | 0.84 (67) | invalid DSL: '3076' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| chained_scenario | c_undo | 0.84 (144) | result differs from reference |
| relative_rule (nl) | r_two_values | 0.84 (32) | invalid DSL: '4572' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| data_change (nl) | g_param | 0.85 (20) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| fixed_decision (nl) | f_fix_zero | 0.85 (34) | invalid DSL: '4273' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| objective_change | o_then_scoped | 0.86 (96) | result differs from reference |
| new_limit (nl) | g_floor_measure_scope | 0.87 (30) | result differs from reference |
| data_change (nl) | g_scale_column | 0.88 (24) | invalid DSL: unknown parameter 'thermal_types.startup_cost'; parameters are ['pump_mwh_per_m' |
| fixed_decision (nl) | f_fix_level | 0.88 (24) | result differs from reference |
| new_limit | g_floor_measure_scope | 0.88 (82) | invalid DSL: [{'measure': 'goes_first', 'scope': {'machine': 'M0'}, 'sense': '>=', 'value': 1 |
| data_change (nl) | g_scale_all_rows | 0.88 (26) | unparseable output |
| data_change | g_scale_column | 0.89 (76) | result differs from reference |
| relative_rule (nl) | r_two_measures | 0.90 (10) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| fixed_decision | f_fix_zero | 0.90 (122) | invalid DSL: '4265' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| data_change | g_set_column | 0.91 (86) | result differs from reference |
| infeasible_request (nl) | i_commit | 0.92 (36) | result differs from reference |
| infeasible_request | i_commit | 0.93 (133) | result differs from reference |
| fixed_decision (nl) | f_force_one | 0.94 (16) | result differs from reference |
| new_limit (nl) | g_cap_measure_scope | 0.95 (20) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| fixed_decision | f_fix_level | 0.95 (85) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.96 (105) | invalid DSL: 'J0' is not a other_job; known values: ['J1', 'J2', 'J3', 'J4', 'J5'] |
| chained_scenario | c_revise | 0.97 (151) | result differs from reference |
| chained_scenario (nl) | c_revise | 0.97 (40) | invalid DSL: [] should be non-empty |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (18) |  |
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
| under_specified | ask_cap_make_months | 1.00 (1) |  |

### `vllm/trained-run5-seed3`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | result differs from reference |
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| data_change (nl) | outage | 0.00 (2) | invalid DSL: invalid set change: 'column' is a required property |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_make_months | 0.00 (1) | needed clarification not asked |
| under_specified | ask_cap_store_month | 0.00 (1) | needed clarification not asked |
| under_specified | ask_cap_total_make | 0.00 (2) | needed clarification not asked |
| under_specified | ask_cap_total_store | 0.00 (2) | result differs from reference |
| under_specified | ask_cap_two_products_month | 0.00 (2) | result differs from reference |
| under_specified | ask_demand_zero | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_remove_row | 0.00 (33) | needed clarification not asked |
| under_specified | ask_install | 0.00 (1) | needed clarification not asked |
| under_specified | ask_margin_scale | 0.00 (1) | invalid scenario |
| under_specified | ask_outage | 0.00 (1) | invalid DSL: row is missing columns ['machines_down'] |
| under_specified | ask_outage_cancel | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_param | 0.02 (41) | needed clarification not asked |
| under_specified | ask_g_cap_measure_total | 0.07 (45) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| logical_rule | l_if_then | 0.08 (103) | result differs from reference |
| logical_rule (nl) | l_at_most_k | 0.12 (32) | result differs from reference |
| under_specified | ask_g_scale_all_rows | 0.13 (77) | unparseable output |
| under_specified | ask_g_set_column | 0.13 (84) | needed clarification not asked |
| logical_rule (nl) | l_if_then | 0.13 (38) | result differs from reference |
| logical_rule | l_at_most_k | 0.15 (108) | invalid DSL: '4265' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| under_specified | ask_g_scale_column | 0.17 (77) | needed clarification not asked |
| new_limit | cap_total_make | 0.20 (5) | result differs from reference |
| objective_change | o_then_min | 0.20 (10) | result differs from reference |
| logical_rule (nl) | l_none_or_batch | 0.24 (42) | result differs from reference |
| logical_rule | l_never_both | 0.25 (48) | invalid DSL: 'any' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| new_limit (nl) | cap_total_make | 0.25 (4) | result differs from reference |
| objective_change (nl) | o_reorder | 0.25 (4) | invalid DSL: unknown measure 'response_objective'; measures are ['assign', 'linked_load', 'op |
| relax_remove (nl) | combo | 0.25 (4) | invalid DSL: unknown table 'params'; tables are ['ages', 'land_groups', 'years'] |
| under_specified | ask_g_floor_measure_scope | 0.25 (44) | needed clarification not asked |
| chained_scenario (nl) | c_add | 0.26 (62) | result differs from reference |
| objective_change | o_then_max | 0.26 (23) | result differs from reference |
| under_specified | ask_g_cap_measure_scope | 0.27 (48) | needed clarification not asked |
| objective_change (nl) | o_then_max | 0.29 (14) | result differs from reference |
| under_specified | ask_g_add_row | 0.29 (17) | needed clarification not asked |
| logical_rule | l_none_or_batch | 0.32 (122) | result differs from reference |
| chained_scenario | c_add | 0.33 (174) | unparseable output |
| under_specified | ask_demand_scale | 0.33 (3) | needed clarification not asked |
| logical_rule (nl) | l_never_both | 0.36 (14) | invalid DSL: scope selects no variable |
| infeasible_request (nl) | i_two_floors | 0.42 (12) | result differs from reference |
| infeasible_request | i_floor_total | 0.49 (45) | result differs from reference |
| infeasible_request (nl) | i_floor_total | 0.50 (8) | invalid scenario |
| new_limit | cap_two_products_month | 0.50 (2) | invalid DSL: unknown table 'make'; tables are ['downtime', 'machines', 'max_sales', 'months', |
| new_limit (nl) | cap_store_month | 0.50 (2) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| objective_change | o_three_stages | 0.50 (40) | invalid DSL: 'hour' is not of type 'object' |
| under_specified | ask_retire | 0.50 (2) | needed clarification not asked |
| relative_rule (nl) | combo | 0.57 (28) | invalid DSL: '4513' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| objective_change (nl) | o_three_stages | 0.60 (10) | invalid DSL: 'J5' is not a job; known values: ['J0', 'J1', 'J2', 'J3', 'J4'] |
| data_change (nl) | combo | 0.61 (36) | result differs from reference |
| relative_rule | combo | 0.61 (93) | result differs from reference |
| data_change | combo | 0.61 (114) | result differs from reference |
| infeasible_request | i_two_floors | 0.64 (58) | invalid DSL: '*' is not a county; known values: ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C |
| infeasible_request | i_floor | 0.65 (88) | invalid DSL: 'any' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| fixed_decision | f_fix_scope | 0.66 (67) | invalid DSL: '=' is not one of ['<=', '>=', '=='] |
| data_change | retire | 0.67 (3) | result differs from reference |
| new_limit (nl) | g_cap_measure_total | 0.67 (30) | unparseable output |
| relax_remove | combo | 0.67 (6) | invalid DSL: unknown constraint family 'max_operating[year]'; families are ['capacity', 'mass |
| relax_remove (nl) | x_full | 0.67 (6) | result differs from reference |
| new_limit (nl) | combo | 0.69 (32) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| relax_remove | x_full | 0.69 (16) | result differs from reference |
| relative_rule | r_share_of_total | 0.72 (146) | invalid DSL: '4514' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| objective_change (nl) | o_then_scoped | 0.72 (18) | result differs from reference |
| relative_rule (nl) | r_share_of_total | 0.72 (40) | invalid DSL: '4564' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| infeasible_request (nl) | i_floor | 0.73 (26) | invalid DSL: '=' is not one of ['<=', '>=', '=='] |
| relax_remove | x_scoped | 0.73 (86) | result differs from reference |
| chained_scenario (nl) | c_undo | 0.73 (30) | result differs from reference |
| data_change | g_param | 0.75 (60) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| data_change (nl) | g_set_column | 0.75 (20) | result differs from reference |
| objective_change (nl) | o_then_min | 0.75 (4) | result differs from reference |
| relative_rule | r_two_values | 0.75 (136) | invalid DSL: '4572' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| new_limit | combo | 0.76 (86) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| data_change | g_scale_all_rows | 0.76 (95) | unparseable output |
| fixed_decision (nl) | f_fix_scope | 0.77 (22) | result differs from reference |
| relative_rule (nl) | r_two_values | 0.78 (32) | invalid DSL: '4572' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| objective_change | o_reorder | 0.79 (48) | invalid DSL: unknown measure 'sum(expand, depot, step)'; measures are ['damaged_left', 'damag |
| fixed_decision | combo | 0.79 (82) | invalid DSL: constraint family 'one_team' has dimensions ['group'], not 'team' |
| data_change | param | 0.80 (5) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| fixed_decision (nl) | combo | 0.80 (20) | result differs from reference |
| new_limit (nl) | g_floor_measure_scope | 0.80 (30) | result differs from reference |
| relax_remove (nl) | x_scoped | 0.80 (20) | invalid DSL: table 'depots' has no column 'day'; columns are ['depot', 'repair_capacity'] |
| fixed_decision | f_force_one | 0.84 (67) | invalid DSL: '3076' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| new_limit | g_cap_measure_total | 0.84 (87) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| objective_change | o_then_scoped | 0.84 (96) | result differs from reference |
| chained_scenario | c_undo | 0.85 (144) | unparseable output |
| data_change (nl) | g_param | 0.85 (20) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| fixed_decision (nl) | f_fix_zero | 0.85 (34) | invalid DSL: '4273' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| new_limit | g_floor_measure_scope | 0.85 (82) | result differs from reference |
| relative_rule | r_two_measures | 0.87 (52) | invalid DSL: [] is not valid under any of the given schemas: [] should be non-empty |
| data_change | g_scale_column | 0.87 (76) | result differs from reference |
| data_change (nl) | g_scale_column | 0.88 (24) | invalid DSL: unknown parameter 'thermal_types.startup_cost'; parameters are ['pump_mwh_per_m' |
| fixed_decision (nl) | f_fix_level | 0.88 (24) | result differs from reference |
| data_change | g_set_column | 0.90 (86) | result differs from reference |
| relative_rule (nl) | r_two_measures | 0.90 (10) | invalid scenario |
| fixed_decision | f_fix_zero | 0.91 (122) | invalid DSL: '3103' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| infeasible_request (nl) | i_commit | 0.92 (36) | result differs from reference |
| data_change (nl) | g_scale_all_rows | 0.92 (26) | unparseable output |
| infeasible_request | i_commit | 0.92 (133) | result differs from reference |
| fixed_decision (nl) | f_force_one | 0.94 (16) | result differs from reference |
| fixed_decision | f_fix_level | 0.94 (85) | result differs from reference |
| new_limit (nl) | g_cap_measure_scope | 0.95 (20) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| new_limit | g_cap_measure_scope | 0.96 (105) | invalid DSL: 'J0' is not a other_job; known values: ['J1', 'J2', 'J3', 'J4', 'J5'] |
| chained_scenario | c_revise | 0.97 (151) | result differs from reference |
| chained_scenario (nl) | c_revise | 1.00 (40) |  |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (18) |  |
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
| new_limit | cap_total_store | 1.00 (3) |  |
| under_specified | ask_margin_set | 1.00 (1) |  |

### `vllm/training-base`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | result differs from reference |
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| data_change (nl) | outage | 0.00 (2) | invalid DSL: no row of 'downtime' matches {"month": "Jan", "machine": "vertDrill"} |
| infeasible_request (nl) | i_floor_total | 0.00 (8) | invalid scenario |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| new_limit | cap_total_make | 0.00 (5) | result differs from reference |
| new_limit | cap_total_store | 0.00 (3) | unparseable output |
| new_limit (nl) | cap_total_make | 0.00 (4) | invalid DSL: unknown table 'make'; tables are ['downtime', 'machines', 'max_sales', 'months', |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_store_month | 0.00 (1) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| under_specified | ask_cap_total_store | 0.00 (2) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| under_specified | ask_cap_two_products_month | 0.00 (2) | result differs from reference |
| under_specified | ask_demand_scale | 0.00 (3) | needed clarification not asked |
| under_specified | ask_demand_zero | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_remove_row | 0.00 (33) | needed clarification not asked |
| under_specified | ask_install | 0.00 (1) | invalid scenario |
| under_specified | ask_margin_scale | 0.00 (1) | invalid scenario |
| under_specified | ask_outage | 0.00 (1) | invalid DSL: row is missing columns ['machines_down'] |
| under_specified | ask_outage_cancel | 0.00 (1) | needed clarification not asked |
| infeasible_request | i_floor_total | 0.04 (45) | invalid scenario |
| under_specified | ask_g_param | 0.05 (41) | needed clarification not asked |
| logical_rule | l_if_then | 0.08 (103) | result differs from reference |
| under_specified | ask_g_scale_column | 0.08 (77) | needed clarification not asked |
| infeasible_request (nl) | i_two_floors | 0.08 (12) | unparseable output |
| logical_rule (nl) | l_at_most_k | 0.09 (32) | result differs from reference |
| objective_change | o_then_min | 0.10 (10) | result differs from reference |
| logical_rule (nl) | l_if_then | 0.11 (38) | result differs from reference |
| logical_rule | l_never_both | 0.12 (48) | invalid DSL: 'any' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| under_specified | ask_g_set_column | 0.13 (84) | needed clarification not asked |
| relative_rule (nl) | combo | 0.14 (28) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| logical_rule | l_at_most_k | 0.15 (108) | invalid DSL: '3074' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| under_specified | ask_g_scale_all_rows | 0.16 (77) | invalid DSL: invalid scale change: [] is not valid under any of the given schemas |
| logical_rule (nl) | l_none_or_batch | 0.17 (42) | unparseable output |
| objective_change | o_then_max | 0.17 (23) | result differs from reference |
| relative_rule | combo | 0.19 (93) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| data_change | margin_scale | 0.20 (5) | invalid DSL: invalid scale_param change: Additional properties are not allowed ('where' was u |
| chained_scenario (nl) | c_add | 0.23 (62) | result differs from reference |
| relative_rule | r_two_measures | 0.23 (52) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| under_specified | ask_g_cap_measure_total | 0.24 (45) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| logical_rule | l_none_or_batch | 0.25 (122) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| objective_change (nl) | o_reorder | 0.25 (4) | invalid DSL: 'all' is not a base; known values: ['21 MUNICIPAL CTR Fire Station', '2837 SHORE |
| relax_remove (nl) | combo | 0.25 (4) | invalid DSL: invalid shift change: Additional properties are not allowed ('name' was unexpect |
| under_specified | ask_g_floor_measure_scope | 0.27 (44) | unparseable output |
| relative_rule (nl) | r_share_of_total | 0.28 (40) | invalid DSL: '4564' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| chained_scenario | c_add | 0.28 (174) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| logical_rule (nl) | l_never_both | 0.29 (14) | invalid DSL: scope selects no variable |
| objective_change (nl) | o_then_max | 0.29 (14) | result differs from reference |
| under_specified | ask_g_cap_measure_scope | 0.29 (48) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| under_specified | ask_g_add_row | 0.29 (17) | invalid DSL: row is missing columns ['weight'] |
| infeasible_request | i_floor | 0.30 (88) | invalid DSL: 'all' is not a depot; known values: ['Birmingham', 'Glasgow', 'Manchester', 'Ply |
| objective_change (nl) | o_three_stages | 0.30 (10) | invalid DSL: 'hour' is not of type 'object' |
| relative_rule (nl) | r_two_measures | 0.30 (10) | invalid DSL: 'all' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| relative_rule | r_share_of_total | 0.30 (146) | invalid DSL: '4514' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| data_change | retire | 0.33 (3) | result differs from reference |
| infeasible_request (nl) | i_floor | 0.35 (26) | invalid DSL: '=' is not one of ['<=', '>=', '=='] |
| relax_remove | x_full | 0.38 (16) | invalid DSL: constraint family 'one_team' cannot be relaxed in this model; change the data or |
| objective_change (nl) | o_then_scoped | 0.39 (18) | result differs from reference |
| infeasible_request | i_two_floors | 0.40 (58) | invalid DSL: 'any' is not a depot; known values: ['Birmingham', 'Glasgow', 'Manchester', 'Ply |
| objective_change | o_three_stages | 0.40 (40) | unparseable output |
| data_change | combo | 0.42 (114) | invalid DSL: invalid scale change: {} should be non-empty |
| data_change (nl) | combo | 0.44 (36) | result differs from reference |
| new_limit (nl) | g_cap_measure_total | 0.47 (30) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| new_limit (nl) | combo | 0.47 (32) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| new_limit | cap_two_products_month | 0.50 (2) | invalid DSL: unknown table 'make'; tables are ['downtime', 'machines', 'max_sales', 'months', |
| new_limit (nl) | cap_store_month | 0.50 (2) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| relax_remove | combo | 0.50 (6) | invalid DSL: 'team_pattern[worker]' is not of type 'object' |
| under_specified | ask_cap_total_make | 0.50 (2) | invalid scenario |
| under_specified | ask_retire | 0.50 (2) | invalid scenario |
| objective_change | o_then_scoped | 0.51 (96) | result differs from reference |
| relative_rule | r_two_values | 0.53 (136) | invalid DSL: 'aircraft' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318 |
| data_change | g_scale_all_rows | 0.58 (95) | invalid DSL: invalid scale change: [] is not valid under any of the given schemas |
| fixed_decision | f_fix_scope | 0.58 (67) | invalid DSL: 'all' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| new_limit | g_cap_measure_total | 0.59 (87) | invalid DSL: '*' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8', 'A |
| data_change | param | 0.60 (5) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| objective_change | o_reorder | 0.60 (48) | invalid DSL: 'all' is not a hour; known values: ['00-01', '01-02', '02-03', '03-04', '04-05', |
| relax_remove | x_scoped | 0.60 (86) | result differs from reference |
| new_limit | combo | 0.62 (86) | invalid DSL: 'all' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318#8',  |
| new_limit (nl) | g_floor_measure_scope | 0.63 (30) | result differs from reference |
| data_change (nl) | g_param | 0.65 (20) | invalid DSL: invalid set change: Additional properties are not allowed ('name' was unexpected |
| chained_scenario (nl) | c_undo | 0.67 (30) | invalid DSL: '*' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', 'Tu |
| relax_remove (nl) | x_full | 0.67 (6) | invalid DSL: [] should be non-empty |
| fixed_decision (nl) | f_fix_scope | 0.68 (22) | invalid DSL: 'all' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| relative_rule (nl) | r_two_values | 0.69 (32) | invalid DSL: 'aircraft' is not a aircraft; known values: ['A318#4', 'A318#5', 'A318#7', 'A318 |
| fixed_decision | combo | 0.70 (82) | invalid DSL: constraint family 'one_team' has dimensions ['group'], not 'team' |
| data_change | g_param | 0.70 (60) | invalid DSL: invalid scale change: Additional properties are not allowed ('name' was unexpect |
| new_limit | g_floor_measure_scope | 0.71 (82) | result differs from reference |
| chained_scenario | c_undo | 0.74 (144) | invalid DSL: invalid scale change: {} should be non-empty |
| fixed_decision (nl) | combo | 0.75 (20) | result differs from reference |
| fixed_decision (nl) | f_fix_level | 0.75 (24) | invalid DSL: '=' is not one of ['<=', '>=', '=='] |
| objective_change (nl) | o_then_min | 0.75 (4) | invalid DSL: 'all' is not a period; known values: ['00-06', '06-09', '09-15', '15-18', '18-24 |
| data_change | g_scale_column | 0.76 (76) | result differs from reference |
| data_change (nl) | g_scale_all_rows | 0.77 (26) | unparseable output |
| fixed_decision | f_force_one | 0.79 (67) | invalid DSL: '3076' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| fixed_decision (nl) | f_fix_zero | 0.79 (34) | invalid DSL: invalid set change: Additional properties are not allowed ('scope' was unexpecte |
| relax_remove (nl) | x_scoped | 0.80 (20) | invalid DSL: table 'depots' has no column 'day'; columns are ['depot', 'repair_capacity'] |
| fixed_decision | f_fix_zero | 0.83 (122) | invalid DSL: '4265' is not a flight; known values: ['1', '10', '100', '101', '102', '103', '1 |
| data_change (nl) | g_set_column | 0.85 (20) | invalid DSL: invalid set_param change: {'rental_days': 3, 'share': 0.3, 'price_same_depot': 6 |
| chained_scenario (nl) | c_revise | 0.88 (40) | unparseable output |
| new_limit | g_cap_measure_scope | 0.88 (105) | result differs from reference |
| data_change | g_set_column | 0.88 (86) | result differs from reference |
| chained_scenario | c_revise | 0.91 (151) | unparseable output |
| data_change (nl) | g_scale_column | 0.92 (24) | result differs from reference |
| infeasible_request (nl) | i_commit | 0.92 (36) | result differs from reference |
| infeasible_request | i_commit | 0.92 (133) | result differs from reference |
| fixed_decision | f_fix_level | 0.93 (85) | result differs from reference |
| fixed_decision (nl) | f_force_one | 0.94 (16) | result differs from reference |
| data_change | g_add_row | 0.94 (18) | invalid DSL: row is missing columns ['capacity'] |
| new_limit (nl) | g_cap_measure_scope | 0.95 (20) | invalid DSL: '*' is not a county; known values: ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_remove_row | 1.00 (19) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change (nl) | demand_set | 1.00 (2) |  |
| data_change (nl) | g_add_row | 1.00 (4) |  |
| data_change (nl) | g_remove_row | 1.00 (12) |  |
| data_change (nl) | margin_scale | 1.00 (2) |  |
| data_change (nl) | param | 1.00 (2) |  |
| under_specified | ask_cap_make_months | 1.00 (1) |  |
| under_specified | ask_margin_set | 1.00 (1) |  |

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `vllm/trained-run5-seed1` | 1100 | 592 | 52 | 0 | 0 | 0 |
| `vllm/trained-run5-seed2` | 1109 | 595 | 50 | 0 | 0 | 0 |
| `vllm/trained-run5-seed3` | 1142 | 579 | 52 | 0 | 0 | 0 |
| `vllm/training-base` | 1062 | 1258 | 75 | 0 | 0 | 0 |
