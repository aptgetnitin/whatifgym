# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | data_change | data_change (nl) | fixed_decision | infeasible_request | logical_rule | new_limit | new_limit (nl) | objective_change | relative_rule | relax_remove | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:4b` | 2368 | 0.287 | 0.348 | 0.68 | 0.91 | 0.48 (267) | 0.57 (320) | 0.42 (33) | 0.28 (235) | 0.12 (201) | 0.18 (238) | 0.41 (239) | 0.22 (45) | 0.23 (168) | 0.26 (258) | 0.10 (84) | 0.01 (280) | 0.25 (324) | 0.24 (1328) | 0.39 (716) | 3.6 |

## By base model

| base model | `ollama/qwen3:4b` |
|---|---|
| `battery_scheduling` | 0.19 (177) |
| `bin_packing` | 0.29 (82) |
| `car_rental` | 0.24 (177) |
| `car_rental_2` | 0.26 (194) |
| `factory_planning` | 0.27 (223) |
| `factory_planning_2` | 0.28 (180) |
| `farm_planning` | 0.35 (187) |
| `food_manufacture` | 0.33 (196) |
| `food_supply` | 0.32 (164) |
| `manpower_planning` | 0.21 (210) |
| `mining` | 0.27 (203) |
| `multiple_knapsack` | 0.51 (130) |
| `power_generation_hydro` | 0.30 (197) |
| `wedding_seating` | 0.27 (48) |

## By template (where the misses are)

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/qwen3:4b` | 920 | 769 | 2 | 2 | 0 | 392 |
