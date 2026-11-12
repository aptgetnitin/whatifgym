# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question; on under-specified tasks an answer without a question scores 0. `route ok` = share of episodes where the agent asked exactly when it should have. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | route ok | chained_scenario | data_change | data_change (nl) | fixed_decision | infeasible_request | logical_rule | new_limit | new_limit (nl) | objective_change | relative_rule | relax_remove | under_specified | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/gpt-oss:20b` | 2368 | 0.888 | 0.981 | 0.95 | 0.98 | 0.97 (267) | 0.97 (320) | 1.00 (33) | 0.99 (235) | 0.89 (201) | 0.70 (238) | 0.98 (239) | 1.00 (45) | 0.96 (168) | 0.91 (258) | 1.00 (84) | 0.57 (280) | 0.97 (324) | 0.86 (1328) | 0.90 (716) | 14.2 |

## By base model

| base model | `ollama/gpt-oss:20b` |
|---|---|
| `battery_scheduling` | 0.83 (177) |
| `bin_packing` | 0.85 (82) |
| `car_rental` | 0.90 (177) |
| `car_rental_2` | 0.92 (194) |
| `factory_planning` | 0.89 (223) |
| `factory_planning_2` | 0.90 (180) |
| `farm_planning` | 0.88 (187) |
| `food_manufacture` | 0.90 (196) |
| `food_supply` | 0.78 (164) |
| `manpower_planning` | 0.90 (210) |
| `mining` | 0.90 (203) |
| `multiple_knapsack` | 0.95 (130) |
| `power_generation_hydro` | 0.91 (197) |
| `wedding_seating` | 0.92 (48) |

## By template (where the misses are)

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt | request errors |
|---|---|---|---|---|---|---|
| `ollama/gpt-oss:20b` | 141 | 124 | 16 | 100 | 0 | 0 |
