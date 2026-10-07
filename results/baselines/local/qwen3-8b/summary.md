# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | data_change | data_change (nl) | fixed_decision | infeasible_request | logical_rule | new_limit | new_limit (nl) | objective_change | relative_rule | relax_remove | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:8b` | 2368 | 0.582 | 0.659 | 0.81 | 0.95 | 0.70 (267) | 0.87 (320) | 0.79 (33) | 0.46 (235) | 0.69 (201) | 0.24 (238) | 0.67 (239) | 0.67 (45) | 0.45 (168) | 0.60 (258) | 0.56 (84) | 0.41 (280) | 0.65 (324) | 0.59 (1328) | 0.54 (716) | 4.6 |

## By base model

| base model | `ollama/qwen3:8b` |
|---|---|
| `battery_scheduling` | 0.67 (177) |
| `bin_packing` | 0.67 (82) |
| `car_rental` | 0.55 (177) |
| `car_rental_2` | 0.51 (194) |
| `factory_planning` | 0.56 (223) |
| `factory_planning_2` | 0.61 (180) |
| `farm_planning` | 0.50 (187) |
| `food_manufacture` | 0.68 (196) |
| `food_supply` | 0.49 (164) |
| `manpower_planning` | 0.53 (210) |
| `mining` | 0.59 (203) |
| `multiple_knapsack` | 0.65 (130) |
| `power_generation_hydro` | 0.62 (197) |
| `wedding_seating` | 0.52 (48) |

## By template (where the misses are)

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/qwen3:8b` | 541 | 450 | 2 | 2 | 0 | 0 |
