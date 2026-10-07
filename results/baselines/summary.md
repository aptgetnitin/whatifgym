# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | data_change | data_change (nl) | fixed_decision | infeasible_request | logical_rule | new_limit | new_limit (nl) | objective_change | relative_rule | relax_remove | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cowork-opus` | 60 | 1.000 | 1.100 | 1.00 | 1.00 | – | 1.00 (60) | – | – | – | – | – | – | – | – | – | – | 1.00 (28) | 1.00 (16) | 1.00 (16) | – |
| `cowork-sonnet` | 60 | 0.983 | 1.083 | 1.00 | 1.00 | – | 0.98 (60) | – | – | – | – | – | – | – | – | – | – | 1.00 (28) | 1.00 (16) | 0.94 (16) | – |
| `ollama/gpt-oss:20b` | 2368 | 0.888 | 0.981 | 0.95 | 0.98 | 0.97 (267) | 0.97 (320) | 1.00 (33) | 0.99 (235) | 0.89 (201) | 0.70 (238) | 0.98 (239) | 1.00 (45) | 0.96 (168) | 0.91 (258) | 1.00 (84) | 0.57 (280) | 0.97 (324) | 0.86 (1328) | 0.90 (716) | 14.2 |
| `ollama/qwen3:14b` | 2368 | 0.736 | 0.820 | 0.89 | 0.94 | 0.75 (267) | 0.84 (320) | 0.88 (33) | 0.91 (235) | 0.92 (201) | 0.30 (238) | 0.91 (239) | 0.93 (45) | 0.74 (168) | 0.81 (258) | 0.82 (84) | 0.41 (280) | 0.89 (324) | 0.72 (1328) | 0.70 (716) | 4.6 |
| `ollama/qwen3:32b` | 399 | 0.895 | 0.987 | 0.92 | 1.00 | – | 0.85 (240) | – | – | – | – | 0.96 (159) | – | – | – | – | – | 0.97 (131) | 0.90 (173) | 0.79 (95) | 8.5 |
| `ollama/qwen3:4b` | 2368 | 0.287 | 0.348 | 0.68 | 0.91 | 0.48 (267) | 0.57 (320) | 0.42 (33) | 0.28 (235) | 0.12 (201) | 0.18 (238) | 0.41 (239) | 0.22 (45) | 0.23 (168) | 0.26 (258) | 0.10 (84) | 0.01 (280) | 0.25 (324) | 0.24 (1328) | 0.39 (716) | 3.6 |
| `ollama/qwen3:8b` | 2368 | 0.582 | 0.659 | 0.81 | 0.95 | 0.70 (267) | 0.87 (320) | 0.79 (33) | 0.46 (235) | 0.69 (201) | 0.24 (238) | 0.67 (239) | 0.67 (45) | 0.45 (168) | 0.60 (258) | 0.56 (84) | 0.41 (280) | 0.65 (324) | 0.59 (1328) | 0.54 (716) | 4.6 |
| `ollama/qwen3:8b+think=on` | 399 | 0.895 | 0.993 | 0.98 | 1.00 | – | 0.93 (240) | – | – | – | – | 0.85 (159) | – | – | – | – | – | 0.89 (131) | 0.98 (173) | 0.75 (95) | 24.0 |

## By base model

| base model | `cowork-opus` | `cowork-sonnet` | `ollama/gpt-oss:20b` | `ollama/qwen3:14b` | `ollama/qwen3:32b` | `ollama/qwen3:4b` | `ollama/qwen3:8b` | `ollama/qwen3:8b+think=on` |
|---|---|---|---|---|---|---|---|---|
| `battery_scheduling` | – | – | 0.83 (177) | 0.62 (177) | – | 0.19 (177) | 0.67 (177) | – |
| `bin_packing` | – | – | 0.85 (82) | 0.62 (82) | 0.92 (24) | 0.29 (82) | 0.67 (82) | 1.00 (24) |
| `car_rental` | – | – | 0.90 (177) | 0.80 (177) | 0.93 (40) | 0.24 (177) | 0.55 (177) | 0.93 (40) |
| `car_rental_2` | – | – | 0.92 (194) | 0.72 (194) | – | 0.26 (194) | 0.51 (194) | – |
| `factory_planning` | 1.00 (60) | 0.98 (60) | 0.89 (223) | 0.77 (223) | 0.78 (80) | 0.27 (223) | 0.56 (223) | 0.88 (80) |
| `factory_planning_2` | – | – | 0.90 (180) | 0.76 (180) | 0.93 (40) | 0.28 (180) | 0.61 (180) | 0.90 (40) |
| `farm_planning` | – | – | 0.88 (187) | 0.73 (187) | – | 0.35 (187) | 0.50 (187) | – |
| `food_manufacture` | – | – | 0.90 (196) | 0.77 (196) | 0.95 (40) | 0.33 (196) | 0.68 (196) | 0.90 (40) |
| `food_supply` | – | – | 0.78 (164) | 0.63 (164) | – | 0.32 (164) | 0.49 (164) | – |
| `manpower_planning` | – | – | 0.90 (210) | 0.73 (210) | 0.93 (40) | 0.21 (210) | 0.53 (210) | 0.90 (40) |
| `mining` | – | – | 0.90 (203) | 0.80 (203) | 0.93 (40) | 0.27 (203) | 0.59 (203) | 0.88 (40) |
| `multiple_knapsack` | – | – | 0.95 (130) | 0.77 (130) | 0.89 (35) | 0.51 (130) | 0.65 (130) | 0.77 (35) |
| `power_generation_hydro` | – | – | 0.91 (197) | 0.82 (197) | 0.90 (40) | 0.30 (197) | 0.62 (197) | 0.93 (40) |
| `wedding_seating` | – | – | 0.92 (48) | 0.52 (48) | 1.00 (20) | 0.27 (48) | 0.52 (48) | 0.95 (20) |

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
| under_specified | ask_install | 0.00 (1) | invalid scenario |
| under_specified | ask_margin_set | 0.00 (1) | invalid scenario |
| under_specified | ask_outage_cancel | 0.00 (1) | invalid scenario |
| under_specified | ask_retire | 0.00 (2) | invalid scenario |
| under_specified | ask_g_set_column | 0.44 (36) | invalid scenario |
| data_change | demand_set | 0.50 (6) | result differs from reference |
| under_specified | ask_g_cap_measure_total | 0.50 (32) | invalid scenario |
| under_specified | ask_g_scale_column | 0.50 (34) | invalid scenario |
| under_specified | ask_g_param | 0.53 (30) | invalid scenario |
| under_specified | ask_g_cap_measure_scope | 0.56 (27) | invalid scenario |
| under_specified | ask_g_scale_all_rows | 0.61 (38) | result differs from reference |
| logical_rule | l_at_most_k | 0.63 (63) | unparseable output |
| logical_rule | l_if_then | 0.64 (75) | result differs from reference |
| under_specified | ask_g_add_row | 0.64 (14) | invalid scenario |
| under_specified | ask_demand_scale | 0.67 (3) | invalid scenario |
| logical_rule | l_never_both | 0.72 (29) | result differs from reference |
| under_specified | ask_g_floor_measure_scope | 0.73 (22) | invalid scenario |
| infeasible_request | i_floor_total | 0.79 (29) | result differs from reference |
| logical_rule | l_none_or_batch | 0.80 (71) | result differs from reference |
| under_specified | ask_g_remove_row | 0.85 (27) | invalid scenario |
| infeasible_request | i_commit | 0.88 (81) | result differs from reference |
| infeasible_request | i_two_floors | 0.89 (35) | result differs from reference |
| relative_rule | combo | 0.89 (54) | unparseable output |
| fixed_decision | f_force_one | 0.90 (20) | result differs from reference |
| relative_rule | r_share_of_total | 0.90 (81) | invalid scenario |
| relative_rule | r_two_values | 0.91 (80) | result differs from reference |
| objective_change | o_then_max | 0.92 (12) | result differs from reference |
| objective_change | o_reorder | 0.92 (37) | result differs from reference |
| chained_scenario | c_undo | 0.93 (87) | unparseable output |
| data_change | combo | 0.94 (69) | result differs from reference |
| objective_change | o_three_stages | 0.95 (43) | result differs from reference |
| infeasible_request | i_floor | 0.96 (56) | result differs from reference |
| new_limit | g_floor_measure_scope | 0.98 (43) | result differs from reference |
| relative_rule | r_two_measures | 0.98 (43) | invalid DSL: unknown measure 'y[bin]'; measures are ['x', 'y'] |
| fixed_decision | combo | 0.98 (46) | result differs from reference |
| data_change | g_scale_all_rows | 0.98 (49) | result differs from reference |
| new_limit | combo | 0.98 (52) | result differs from reference |
| new_limit | g_cap_measure_total | 0.98 (64) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.98 (65) | result differs from reference |
| objective_change | o_then_scoped | 0.99 (70) | result differs from reference |
| chained_scenario | c_add | 0.99 (99) | invalid DSL: '{' is not valid under any of the given schemas: '{' is not of type 'object' |
| chained_scenario | c_revise | 1.00 (81) |  |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (14) |  |
| data_change | g_param | 1.00 (47) |  |
| data_change | g_remove_row | 1.00 (26) |  |
| data_change | g_scale_column | 1.00 (34) |  |
| data_change | g_set_column | 1.00 (37) |  |
| data_change | install | 1.00 (1) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage | 1.00 (4) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |
| data_change (nl) | combo | 1.00 (3) |  |
| data_change (nl) | g_param | 1.00 (12) |  |
| data_change (nl) | g_scale_all_rows | 1.00 (3) |  |
| data_change (nl) | g_scale_column | 1.00 (6) |  |
| data_change (nl) | g_set_column | 1.00 (9) |  |
| fixed_decision | f_fix_level | 1.00 (54) |  |
| fixed_decision | f_fix_scope | 1.00 (51) |  |
| fixed_decision | f_fix_zero | 1.00 (64) |  |
| new_limit | cap_store_month | 1.00 (4) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit (nl) | combo | 1.00 (15) |  |
| new_limit (nl) | g_cap_measure_scope | 1.00 (3) |  |
| new_limit (nl) | g_cap_measure_total | 1.00 (15) |  |
| new_limit (nl) | g_floor_measure_scope | 1.00 (12) |  |
| objective_change | o_then_min | 1.00 (6) |  |
| relax_remove | combo | 1.00 (5) |  |
| relax_remove | x_full | 1.00 (14) |  |
| relax_remove | x_scoped | 1.00 (65) |  |
| under_specified | ask_cap_store_month | 1.00 (1) |  |
| under_specified | ask_cap_total_store | 1.00 (2) |  |
| under_specified | ask_cap_two_products_month | 1.00 (2) |  |
| under_specified | ask_demand_zero | 1.00 (1) |  |
| under_specified | ask_margin_scale | 1.00 (1) |  |
| under_specified | ask_outage | 1.00 (1) |  |

### `ollama/qwen3:14b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | result differs from reference |
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_store_month | 0.00 (1) | needed clarification not asked |
| under_specified | ask_demand_zero | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_remove_row | 0.00 (27) | needed clarification not asked |
| under_specified | ask_install | 0.00 (1) | result differs from reference |
| under_specified | ask_margin_set | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_cap_measure_total | 0.16 (32) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| logical_rule | l_at_most_k | 0.17 (63) | result differs from reference |
| logical_rule | l_if_then | 0.19 (75) | result differs from reference |
| data_change | demand_set | 0.33 (6) | result differs from reference |
| logical_rule | l_none_or_batch | 0.34 (71) | result differs from reference |
| under_specified | ask_g_scale_all_rows | 0.34 (38) | invalid DSL: invalid shift change: {} should be non-empty |
| under_specified | ask_g_floor_measure_scope | 0.41 (22) | needed clarification not asked |
| chained_scenario | c_add | 0.45 (99) | result differs from reference |
| under_specified | ask_g_cap_measure_scope | 0.48 (27) | needed clarification not asked |
| data_change (nl) | g_scale_column | 0.50 (6) | invalid DSL: unknown parameter 'startup_cost'; parameters are ['pump_mwh_per_m', 'reserve_mar |
| objective_change | o_then_max | 0.50 (12) | invalid DSL: {'hour': ['23-24']} is not valid under any of the given schemas: {'hour': ['23-2 |
| under_specified | ask_cap_total_store | 0.50 (2) | result differs from reference |
| under_specified | ask_g_add_row | 0.50 (14) | needed clarification not asked |
| under_specified | ask_g_param | 0.50 (30) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| under_specified | ask_retire | 0.50 (2) | result differs from reference |
| under_specified | ask_g_scale_column | 0.53 (34) | needed clarification not asked |
| data_change | combo | 0.62 (69) | invalid DSL: invalid scale change: {} should be non-empty |
| objective_change | o_three_stages | 0.63 (43) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| relative_rule | r_two_measures | 0.65 (43) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| objective_change | o_then_min | 0.67 (6) | result differs from reference |
| under_specified | ask_demand_scale | 0.67 (3) | needed clarification not asked |
| under_specified | ask_g_set_column | 0.67 (36) | needed clarification not asked |
| infeasible_request | i_floor_total | 0.69 (29) | invalid DSL: '=' is not one of ['<=', '>=', '=='] |
| data_change | g_scale_all_rows | 0.69 (49) | invalid DSL: invalid scale change: {} should be non-empty |
| objective_change | o_reorder | 0.70 (37) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| fixed_decision | f_fix_scope | 0.73 (51) | result differs from reference |
| logical_rule | l_never_both | 0.76 (29) | result differs from reference |
| relative_rule | combo | 0.76 (54) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| relative_rule | r_share_of_total | 0.78 (81) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| relax_remove | x_full | 0.79 (14) | invalid DSL: [] is not valid under any of the given schemas: [] should be non-empty |
| new_limit (nl) | g_cap_measure_total | 0.80 (15) | invalid DSL: 'unskilled' is not a from_skill; known values: ['semi_skilled', 'skilled'] |
| relax_remove | combo | 0.80 (5) | invalid DSL: unknown table 'params'; tables are ['mines', 'years'] |
| new_limit | g_cap_measure_total | 0.81 (64) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| infeasible_request | i_two_floors | 0.83 (35) | result differs from reference |
| relax_remove | x_scoped | 0.83 (65) | result differs from reference |
| chained_scenario | c_undo | 0.85 (87) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| objective_change | o_then_scoped | 0.87 (70) | invalid DSL: {'depot': ['Glasgow', 'Manchester', 'Birmingham', 'Plymouth']} is not valid unde |
| new_limit | combo | 0.88 (52) | invalid DSL: {'hour': ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08' |
| fixed_decision | combo | 0.89 (46) | result differs from reference |
| data_change (nl) | g_param | 0.92 (12) | invalid DSL: unknown table 'params'; tables are ['months', 'oils', 'purchase_prices'] |
| relative_rule | r_two_values | 0.96 (80) | invalid DSL: 'all' is not a product; known values: ['Prod1', 'Prod2', 'Prod3', 'Prod4', 'Prod |
| fixed_decision | f_fix_zero | 0.97 (64) | invalid DSL: unknown table 'grow_grain'; tables are ['ages', 'land_groups', 'years'] |
| new_limit | g_cap_measure_scope | 0.97 (65) | result differs from reference |
| data_change | g_scale_column | 0.97 (34) | invalid DSL: unknown parameter 'startup_cost'; parameters are ['pump_mwh_per_m', 'reserve_mar |
| infeasible_request | i_commit | 0.98 (81) | invalid DSL: unknown table 'grow_grain'; tables are ['ages', 'land_groups', 'years'] |
| new_limit | g_floor_measure_scope | 0.98 (43) | result differs from reference |
| data_change | g_param | 0.98 (47) | result differs from reference |
| fixed_decision | f_fix_level | 0.98 (54) | invalid DSL: unknown table 'undamaged_stock'; tables are ['days', 'demand', 'depots', 'rental |
| chained_scenario | c_revise | 1.00 (81) |  |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (14) |  |
| data_change | g_remove_row | 1.00 (26) |  |
| data_change | g_set_column | 1.00 (37) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |
| data_change (nl) | combo | 1.00 (3) |  |
| data_change (nl) | g_scale_all_rows | 1.00 (3) |  |
| data_change (nl) | g_set_column | 1.00 (9) |  |
| fixed_decision | f_force_one | 1.00 (20) |  |
| infeasible_request | i_floor | 1.00 (56) |  |
| new_limit | cap_store_month | 1.00 (4) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit (nl) | combo | 1.00 (15) |  |
| new_limit (nl) | g_cap_measure_scope | 1.00 (3) |  |
| new_limit (nl) | g_floor_measure_scope | 1.00 (12) |  |
| under_specified | ask_cap_make_months | 1.00 (1) |  |
| under_specified | ask_cap_total_make | 1.00 (2) |  |
| under_specified | ask_cap_two_products_month | 1.00 (2) |  |
| under_specified | ask_margin_scale | 1.00 (1) |  |
| under_specified | ask_outage | 1.00 (1) |  |
| under_specified | ask_outage_cancel | 1.00 (1) |  |

### `ollama/qwen3:32b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| data_change | demand_set | 0.33 (6) | result differs from reference |
| new_limit | cap_store_month | 0.50 (4) | result differs from reference |
| data_change | g_scale_all_rows | 0.52 (25) | invalid DSL: invalid scale change: {} should be non-empty |
| data_change | combo | 0.72 (58) | invalid DSL: invalid scale change: {} should be non-empty |
| new_limit | combo | 0.91 (33) | invalid DSL: 'all' is not a day; known values: ['Friday', 'Monday', 'Saturday', 'Thursday', ' |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (12) |  |
| data_change | g_param | 1.00 (33) |  |
| data_change | g_remove_row | 1.00 (24) |  |
| data_change | g_scale_column | 1.00 (23) |  |
| data_change | g_set_column | 1.00 (21) |  |
| data_change | install | 1.00 (1) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit | g_cap_measure_scope | 1.00 (44) |  |
| new_limit | g_cap_measure_total | 1.00 (44) |  |
| new_limit | g_floor_measure_scope | 1.00 (23) |  |

### `ollama/qwen3:4b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | demand_zero | 0.00 (2) | result differs from reference |
| data_change | install | 0.00 (1) | invalid DSL: row is missing columns ['installed'] |
| data_change | margin_set | 0.00 (6) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| data_change | outage | 0.00 (4) | invalid DSL: row is missing columns ['machines_down'] |
| data_change | param | 0.00 (5) | result differs from reference |
| infeasible_request | i_floor_total | 0.00 (29) | result differs from reference |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| new_limit | cap_total_make | 0.00 (5) | result differs from reference |
| new_limit | cap_two_products_month | 0.00 (2) | result differs from reference |
| objective_change | o_then_min | 0.00 (6) | result differs from reference |
| relax_remove | combo | 0.00 (5) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_cap_make_months | 0.00 (1) | needed clarification not asked |
| under_specified | ask_cap_store_month | 0.00 (1) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| under_specified | ask_cap_total_make | 0.00 (2) | needed clarification not asked |
| under_specified | ask_cap_total_store | 0.00 (2) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_cap_two_products_month | 0.00 (2) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_demand_scale | 0.00 (3) | needed clarification not asked |
| under_specified | ask_demand_zero | 0.00 (1) | needed clarification not asked |
| under_specified | ask_g_add_row | 0.00 (14) | needed clarification not asked |
| under_specified | ask_g_cap_measure_scope | 0.00 (27) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| under_specified | ask_g_cap_measure_total | 0.00 (32) | invalid DSL: parameter 'energy_capacity_kwh' is numeric; got 'upper_limit' |
| under_specified | ask_g_floor_measure_scope | 0.00 (22) | needed clarification not asked |
| under_specified | ask_g_param | 0.00 (30) | needed clarification not asked |
| under_specified | ask_g_remove_row | 0.00 (27) | needed clarification not asked |
| under_specified | ask_g_scale_all_rows | 0.00 (38) | needed clarification not asked |
| under_specified | ask_install | 0.00 (1) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_margin_scale | 0.00 (1) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_margin_set | 0.00 (1) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_outage | 0.00 (1) | needed clarification not asked |
| under_specified | ask_outage_cancel | 0.00 (1) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_retire | 0.00 (2) | invalid DSL: Additional properties are not allowed ('role', 'text' were unexpected) |
| under_specified | ask_g_set_column | 0.03 (36) | needed clarification not asked |
| under_specified | ask_g_scale_column | 0.03 (34) | needed clarification not asked |
| logical_rule | l_at_most_k | 0.03 (63) | invalid DSL: table 'hours' has no column 'soc'; columns are ['export_price', 'hour', 'import_ |
| new_limit (nl) | g_cap_measure_total | 0.07 (15) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| objective_change | o_reorder | 0.08 (37) | invalid DSL: unknown measure 'profit'; measures are ['charge', 'discharge', 'soc'] |
| data_change (nl) | g_param | 0.08 (12) | invalid DSL: unknown table 'params'; tables are ['days', 'demand', 'depots', 'rental_lengths' |
| infeasible_request | i_floor | 0.09 (56) | invalid DSL: [] should be non-empty |
| relax_remove | x_scoped | 0.09 (65) | result differs from reference |
| fixed_decision | f_fix_zero | 0.09 (64) | result differs from reference |
| infeasible_request | i_commit | 0.11 (81) | invalid DSL: table 'hours' has no column 'soc'; columns are ['export_price', 'hour', 'import_ |
| relative_rule | r_share_of_total | 0.11 (81) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| relative_rule | r_two_measures | 0.12 (43) | result differs from reference |
| relax_remove | x_full | 0.14 (14) | result differs from reference |
| fixed_decision | f_fix_scope | 0.18 (51) | invalid DSL: unknown table 'undamaged_left'; tables are ['days', 'demand', 'depots', 'rental_ |
| objective_change | o_then_scoped | 0.19 (70) | result differs from reference |
| logical_rule | l_if_then | 0.19 (75) | result differs from reference |
| fixed_decision | f_fix_level | 0.20 (54) | result differs from reference |
| logical_rule | l_never_both | 0.21 (29) | result differs from reference |
| new_limit | g_cap_measure_total | 0.23 (64) | result differs from reference |
| relative_rule | combo | 0.24 (54) | result differs from reference |
| objective_change | o_then_max | 0.25 (12) | result differs from reference |
| new_limit (nl) | combo | 0.27 (15) | invalid DSL: unknown measure 'profit'; measures are ['damaged_left', 'damaged_stock', 'damage |
| logical_rule | l_none_or_batch | 0.28 (71) | result differs from reference |
| infeasible_request | i_two_floors | 0.29 (35) | invalid DSL: unknown table 'soc'; tables are ['hours'] |
| chained_scenario | c_add | 0.29 (99) | result differs from reference |
| data_change | g_param | 0.30 (47) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| new_limit | g_floor_measure_scope | 0.30 (43) | invalid DSL: unknown measure 'profit'; measures are ['charge', 'discharge', 'soc'] |
| data_change | process_hours | 0.33 (3) | result differs from reference |
| data_change | retire | 0.33 (3) | result differs from reference |
| data_change (nl) | g_scale_all_rows | 0.33 (3) | invalid DSL: no row of 'requirements' matches {"year": ["1", "2", "3"], "skill": ["unskilled" |
| new_limit | cap_total_store | 0.33 (3) | result differs from reference |
| new_limit (nl) | g_cap_measure_scope | 0.33 (3) | invalid DSL: table 'retraining' has no column 'year'; columns are ['cost', 'from_skill', 'max |
| new_limit (nl) | g_floor_measure_scope | 0.33 (12) | invalid DSL: unknown table 'store'; tables are ['months', 'oils', 'purchase_prices'] |
| objective_change | o_three_stages | 0.44 (43) | invalid DSL: '*' is not a hour; known values: ['00-01', '01-02', '02-03', '03-04', '04-05', ' |
| data_change | outage_cancel | 0.50 (4) | result differs from reference |
| relative_rule | r_two_values | 0.50 (80) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| new_limit | g_cap_measure_scope | 0.54 (65) | invalid DSL: unknown table 'soc'; tables are ['hours'] |
| chained_scenario | c_undo | 0.54 (87) | result differs from reference |
| data_change | combo | 0.57 (69) | invalid DSL: row is missing columns ['weight'] |
| fixed_decision | combo | 0.57 (46) | result differs from reference |
| data_change | g_scale_column | 0.59 (34) | result differs from reference |
| chained_scenario | c_revise | 0.63 (81) | result differs from reference |
| new_limit | combo | 0.63 (52) | result differs from reference |
| data_change | g_add_row | 0.64 (14) | invalid DSL: row is missing columns ['weight'] |
| data_change (nl) | combo | 0.67 (3) | result differs from reference |
| data_change (nl) | g_scale_column | 0.67 (6) | result differs from reference |
| data_change (nl) | g_set_column | 0.67 (9) | invalid DSL: unknown parameter 'cost_per_mwh_above_min'; parameters are ['pump_mwh_per_m', 'r |
| data_change | g_remove_row | 0.69 (26) | result differs from reference |
| fixed_decision | f_force_one | 0.70 (20) | result differs from reference |
| data_change | g_set_column | 0.73 (37) | result differs from reference |
| data_change | g_scale_all_rows | 0.78 (49) | result differs from reference |
| data_change | demand_set | 0.83 (6) | result differs from reference |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | margin_scale | 1.00 (5) |  |

### `ollama/qwen3:8b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | result differs from reference |
| under_specified | ask_cap_each_month | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_make_months | 0.00 (1) | result differs from reference |
| under_specified | ask_cap_store_month | 0.00 (1) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| under_specified | ask_cap_total_store | 0.00 (2) | result differs from reference |
| under_specified | ask_cap_two_products_month | 0.00 (2) | invalid scenario |
| under_specified | ask_margin_scale | 0.00 (1) | invalid scenario |
| under_specified | ask_outage | 0.00 (1) | invalid DSL: row is missing columns ['machines_down'] |
| under_specified | ask_retire | 0.00 (2) | invalid scenario |
| logical_rule | l_at_most_k | 0.06 (63) | invalid DSL: '>' is not one of ['<=', '>=', '=='] |
| objective_change | o_reorder | 0.16 (37) | result differs from reference |
| objective_change | o_then_min | 0.17 (6) | invalid DSL: unknown measure 'weekly_profit'; measures are ['damaged_left', 'damaged_stock',  |
| under_specified | ask_g_param | 0.17 (30) | needed clarification not asked |
| logical_rule | l_if_then | 0.17 (75) | result differs from reference |
| relax_remove | combo | 0.20 (5) | invalid DSL: '*' is not a product; known values: ['Prod1', 'Prod2', 'Prod3', 'Prod4', 'Prod5' |
| under_specified | ask_g_remove_row | 0.22 (27) | needed clarification not asked |
| under_specified | ask_g_cap_measure_total | 0.25 (32) | result differs from reference |
| fixed_decision | f_fix_scope | 0.25 (51) | result differs from reference |
| under_specified | ask_g_cap_measure_scope | 0.30 (27) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| logical_rule | l_none_or_batch | 0.31 (71) | invalid DSL: a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), |
| fixed_decision | combo | 0.33 (46) | invalid DSL: table 'hours' has no column 'charge'; columns are ['export_price', 'hour', 'impo |
| data_change | process_hours | 0.33 (3) | result differs from reference |
| data_change | retire | 0.33 (3) | result differs from reference |
| chained_scenario | c_add | 0.35 (99) | invalid DSL: invalid set change: {} should be non-empty |
| relax_remove | x_full | 0.36 (14) | invalid DSL: constraint family 'terminal_soc' has dimensions [], not 'hour' |
| relative_rule | combo | 0.39 (54) | invalid DSL: '*' is not a hour; known values: ['00-01', '01-02', '02-03', '03-04', '04-05', ' |
| relative_rule | r_two_measures | 0.40 (43) | invalid DSL: 'all' is not a hour; known values: ['00-01', '01-02', '02-03', '03-04', '04-05', |
| under_specified | ask_g_floor_measure_scope | 0.41 (22) | needed clarification not asked |
| under_specified | ask_g_add_row | 0.43 (14) | needed clarification not asked |
| objective_change | o_three_stages | 0.47 (43) | invalid DSL: '*' is not a hour; known values: ['00-01', '01-02', '02-03', '03-04', '04-05', ' |
| infeasible_request | i_floor_total | 0.48 (29) | result differs from reference |
| fixed_decision | f_fix_zero | 0.48 (64) | invalid DSL: table 'hours' has no column 'max_discharge_kw'; columns are ['export_price', 'ho |
| objective_change | o_then_max | 0.50 (12) | invalid DSL: unknown measure 'weekly_profit'; measures are ['damaged_left', 'damaged_stock',  |
| under_specified | ask_cap_total_make | 0.50 (2) | result differs from reference |
| under_specified | ask_g_set_column | 0.50 (36) | needed clarification not asked |
| new_limit | combo | 0.52 (52) | result differs from reference |
| relative_rule | r_share_of_total | 0.53 (81) | result differs from reference |
| new_limit | g_cap_measure_total | 0.53 (64) | result differs from reference |
| new_limit (nl) | g_cap_measure_total | 0.53 (15) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| logical_rule | l_never_both | 0.59 (29) | result differs from reference |
| under_specified | ask_g_scale_column | 0.59 (34) | result differs from reference |
| objective_change | o_then_scoped | 0.60 (70) | invalid DSL: unknown measure 'weekly_profit'; measures are ['damaged_left', 'damaged_stock',  |
| fixed_decision | f_fix_level | 0.61 (54) | invalid DSL: table 'hours' has no column 'charge'; columns are ['export_price', 'hour', 'impo |
| infeasible_request | i_commit | 0.63 (81) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| relax_remove | x_scoped | 0.63 (65) | invalid DSL: '*' is not a depot; known values: ['Birmingham', 'Glasgow', 'Manchester', 'Plymo |
| data_change | margin_set | 0.67 (6) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| data_change (nl) | g_scale_column | 0.67 (6) | invalid DSL: invalid scale_param change: Additional properties are not allowed ('where' was u |
| new_limit (nl) | g_cap_measure_scope | 0.67 (3) | invalid DSL: table 'retraining' has no column 'year'; columns are ['cost', 'from_skill', 'max |
| under_specified | ask_demand_scale | 0.67 (3) | invalid scenario |
| under_specified | ask_g_scale_all_rows | 0.71 (38) | needed clarification not asked |
| new_limit (nl) | combo | 0.73 (15) | result differs from reference |
| data_change (nl) | g_param | 0.75 (12) | invalid DSL: unknown table 'params'; tables are ['months', 'oils', 'purchase_prices'] |
| new_limit (nl) | g_floor_measure_scope | 0.75 (12) | result differs from reference |
| data_change | combo | 0.75 (69) | result differs from reference |
| data_change (nl) | g_set_column | 0.78 (9) | result differs from reference |
| new_limit | g_floor_measure_scope | 0.79 (43) | result differs from reference |
| data_change | param | 0.80 (5) | result differs from reference |
| fixed_decision | f_force_one | 0.80 (20) | invalid DSL: table 'mines' has no column 'open'; columns are ['capacity', 'mine', 'quality',  |
| infeasible_request | i_two_floors | 0.80 (35) | invalid DSL: table 'hours' has no column 'soc'; columns are ['export_price', 'hour', 'import_ |
| new_limit | cap_total_make | 0.80 (5) | result differs from reference |
| infeasible_request | i_floor | 0.80 (56) | invalid DSL: unknown table 'damaged_transfers'; tables are ['days', 'demand', 'depots', 'rent |
| chained_scenario | c_undo | 0.84 (87) | invalid DSL: unknown table 'params'; tables are ['hours'] |
| new_limit | g_cap_measure_scope | 0.88 (65) | result differs from reference |
| data_change | g_scale_all_rows | 0.88 (49) | result differs from reference |
| data_change | g_set_column | 0.89 (37) | result differs from reference |
| data_change | g_add_row | 0.93 (14) | invalid DSL: '*' is not a bin; known values: ['bin0', 'bin1', 'bin10', 'bin2', 'bin3', 'bin4' |
| data_change | g_param | 0.94 (47) | invalid DSL: unknown table 'params'; tables are ['ages', 'land_groups', 'years'] |
| relative_rule | r_two_values | 0.94 (80) | invalid DSL: 'depot' is not a depot; known values: ['Birmingham', 'Glasgow', 'Manchester', 'P |
| chained_scenario | c_revise | 0.99 (81) | result differs from reference |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_remove_row | 1.00 (26) |  |
| data_change | g_scale_column | 1.00 (34) |  |
| data_change | install | 1.00 (1) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change (nl) | combo | 1.00 (3) |  |
| data_change (nl) | g_scale_all_rows | 1.00 (3) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| under_specified | ask_demand_zero | 1.00 (1) |  |
| under_specified | ask_install | 1.00 (1) |  |
| under_specified | ask_margin_set | 1.00 (1) |  |
| under_specified | ask_outage_cancel | 1.00 (1) |  |

### `ollama/qwen3:8b+think=on`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | result differs from reference |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | combo | 0.61 (33) | result differs from reference |
| new_limit | g_cap_measure_total | 0.80 (44) | invalid DSL: 'Glasmond' is not a to_depot; known values: ['Birmingham', 'Glasgow', 'Mancheste |
| data_change | combo | 0.83 (58) | result differs from reference |
| data_change | g_param | 0.88 (33) | invalid DSL: unknown table 'params'; tables are ['machines', 'maintenance', 'max_sales', 'mon |
| data_change | g_scale_all_rows | 0.88 (25) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.98 (44) | result differs from reference |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (12) |  |
| data_change | g_remove_row | 1.00 (24) |  |
| data_change | g_scale_column | 1.00 (23) |  |
| data_change | g_set_column | 1.00 (21) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage | 1.00 (4) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |
| new_limit | cap_store_month | 1.00 (4) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit | g_floor_measure_scope | 1.00 (23) |  |

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `cowork-opus` | 0 | 0 | 0 | 0 | 0 | 0 |
| `cowork-sonnet` | 1 | 0 | 0 | 0 | 0 | 0 |
| `ollama/gpt-oss:20b` | 141 | 124 | 16 | 100 | 0 | 0 |
| `ollama/qwen3:14b` | 371 | 255 | 0 | 0 | 0 | 0 |
| `ollama/qwen3:32b` | 11 | 31 | 0 | 0 | 0 | 0 |
| `ollama/qwen3:4b` | 920 | 769 | 2 | 2 | 0 | 392 |
| `ollama/qwen3:8b` | 541 | 450 | 2 | 2 | 0 | 0 |
| `ollama/qwen3:8b+think=on` | 36 | 6 | 3 | 29 | 0 | 0 |
