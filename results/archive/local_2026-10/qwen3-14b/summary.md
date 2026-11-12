# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | data_change | data_change (nl) | fixed_decision | infeasible_request | logical_rule | new_limit | new_limit (nl) | objective_change | relative_rule | relax_remove | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:14b` | 2368 | 0.736 | 0.820 | 0.89 | 0.94 | 0.75 (267) | 0.84 (320) | 0.88 (33) | 0.91 (235) | 0.92 (201) | 0.30 (238) | 0.91 (239) | 0.93 (45) | 0.74 (168) | 0.81 (258) | 0.82 (84) | 0.41 (280) | 0.89 (324) | 0.72 (1328) | 0.70 (716) | 4.6 |

## By base model

| base model | `ollama/qwen3:14b` |
|---|---|
| `battery_scheduling` | 0.62 (177) |
| `bin_packing` | 0.62 (82) |
| `car_rental` | 0.80 (177) |
| `car_rental_2` | 0.72 (194) |
| `factory_planning` | 0.77 (223) |
| `factory_planning_2` | 0.76 (180) |
| `farm_planning` | 0.73 (187) |
| `food_manufacture` | 0.77 (196) |
| `food_supply` | 0.63 (164) |
| `manpower_planning` | 0.73 (210) |
| `mining` | 0.80 (203) |
| `multiple_knapsack` | 0.77 (130) |
| `power_generation_hydro` | 0.82 (197) |
| `wedding_seating` | 0.52 (48) |

## By template (where the misses are)

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/qwen3:14b` | 371 | 255 | 0 | 0 | 0 | 0 |
