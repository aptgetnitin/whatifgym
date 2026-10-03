# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | data_change | new_limit | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/gpt-oss:20b` | 399 | 0.985 | 1.085 | 1.00 | 0.98 (240) | 0.99 (159) | 0.98 (131) | 0.99 (173) | 0.98 (95) | 9.3 |
| `ollama/qwen3:14b` | 399 | 0.902 | 0.995 | 0.93 | 0.85 (240) | 0.97 (159) | 0.95 (131) | 0.93 (173) | 0.79 (95) | 3.7 |
| `ollama/qwen3:32b` | 399 | 0.895 | 0.987 | 0.92 | 0.85 (240) | 0.96 (159) | 0.97 (131) | 0.90 (173) | 0.79 (95) | 8.5 |
| `ollama/qwen3:4b` | 399 | 0.501 | 0.575 | 0.74 | 0.57 (240) | 0.40 (159) | 0.34 (131) | 0.57 (173) | 0.60 (95) | 2.4 |
| `ollama/qwen3:8b` | 399 | 0.787 | 0.876 | 0.89 | 0.86 (240) | 0.67 (159) | 0.77 (131) | 0.86 (173) | 0.67 (95) | 6.0 |
| `ollama/qwen3:8b+think=on` | 399 | 0.895 | 0.993 | 0.98 | 0.93 (240) | 0.85 (159) | 0.89 (131) | 0.98 (173) | 0.75 (95) | 24.0 |

## By base model

| base model | `ollama/gpt-oss:20b` | `ollama/qwen3:14b` | `ollama/qwen3:32b` | `ollama/qwen3:4b` | `ollama/qwen3:8b` | `ollama/qwen3:8b+think=on` |
|---|---|---|---|---|---|---|
| `bin_packing` | 1.00 (24) | 1.00 (24) | 0.92 (24) | 0.42 (24) | 0.92 (24) | 1.00 (24) |
| `car_rental` | 0.97 (40) | 0.95 (40) | 0.93 (40) | 0.35 (40) | 0.88 (40) | 0.93 (40) |
| `factory_planning` | 0.95 (80) | 0.79 (80) | 0.78 (80) | 0.36 (80) | 0.61 (80) | 0.88 (80) |
| `factory_planning_2` | 1.00 (40) | 0.97 (40) | 0.93 (40) | 0.53 (40) | 0.75 (40) | 0.90 (40) |
| `food_manufacture` | 1.00 (40) | 0.88 (40) | 0.95 (40) | 0.65 (40) | 0.93 (40) | 0.90 (40) |
| `manpower_planning` | 0.97 (40) | 0.78 (40) | 0.93 (40) | 0.40 (40) | 0.68 (40) | 0.90 (40) |
| `mining` | 1.00 (40) | 1.00 (40) | 0.93 (40) | 0.62 (40) | 0.88 (40) | 0.88 (40) |
| `multiple_knapsack` | 1.00 (35) | 0.94 (35) | 0.89 (35) | 0.77 (35) | 0.74 (35) | 0.77 (35) |
| `power_generation_hydro` | 1.00 (40) | 0.93 (40) | 0.90 (40) | 0.55 (40) | 0.82 (40) | 0.93 (40) |
| `wedding_seating` | 1.00 (20) | 1.00 (20) | 1.00 (20) | 0.50 (20) | 1.00 (20) | 0.95 (20) |

## By template (where the misses are)

### `ollama/gpt-oss:20b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| data_change | demand_set | 0.50 (6) | result differs from reference |
| data_change | g_scale_all_rows | 0.96 (25) | result differs from reference |
| data_change | combo | 0.98 (58) | result differs from reference |
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
| data_change | outage | 1.00 (4) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |
| new_limit | cap_store_month | 1.00 (4) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit | combo | 1.00 (33) |  |
| new_limit | g_cap_measure_scope | 1.00 (44) |  |
| new_limit | g_cap_measure_total | 1.00 (44) |  |
| new_limit | g_floor_measure_scope | 1.00 (23) |  |

### `ollama/qwen3:14b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | install | 0.00 (1) | result differs from reference |
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| data_change | demand_set | 0.33 (6) | result differs from reference |
| data_change | combo | 0.67 (58) | invalid DSL: invalid scale change: {} should be non-empty |
| data_change | g_scale_all_rows | 0.76 (25) | result differs from reference |
| new_limit | g_cap_measure_total | 0.95 (44) | invalid DSL: 'unskilled' is not a from_skill; known values: ['semi_skilled', 'skilled'] |
| data_change | g_scale_column | 0.96 (23) | invalid DSL: unknown parameter 'startup_cost'; parameters are ['pump_mwh_per_m', 'reserve_mar |
| new_limit | g_cap_measure_scope | 0.98 (44) | invalid DSL: table 'costs' has no column 'max_short_time'; columns are ['overmanning_cost', ' |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_add_row | 1.00 (12) |  |
| data_change | g_param | 1.00 (33) |  |
| data_change | g_remove_row | 1.00 (24) |  |
| data_change | g_set_column | 1.00 (21) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | margin_set | 1.00 (6) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| data_change | param | 1.00 (5) |  |
| data_change | process_hours | 1.00 (3) |  |
| data_change | retire | 1.00 (3) |  |
| new_limit | cap_store_month | 1.00 (4) |  |
| new_limit | cap_total_make | 1.00 (5) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |
| new_limit | combo | 1.00 (33) |  |
| new_limit | g_floor_measure_scope | 1.00 (23) |  |

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
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | invalid DSL: unknown table 'params'; tables are ['downtime', 'machines', 'max_sales', 'months |
| new_limit | cap_total_make | 0.00 (5) | result differs from reference |
| new_limit | cap_two_products_month | 0.00 (2) | result differs from reference |
| new_limit | g_floor_measure_scope | 0.17 (23) | invalid DSL: unknown measure 'x[item, bin]'; measures are ['x', 'y'] |
| new_limit | g_cap_measure_total | 0.23 (44) | result differs from reference |
| data_change | g_param | 0.30 (33) | invalid DSL: unknown table 'params'; tables are ['days', 'demand', 'depots', 'rental_lengths' |
| data_change | process_hours | 0.33 (3) | result differs from reference |
| data_change | retire | 0.33 (3) | result differs from reference |
| new_limit | cap_total_store | 0.33 (3) | result differs from reference |
| data_change | outage_cancel | 0.50 (4) | result differs from reference |
| data_change | combo | 0.57 (58) | invalid DSL: row is missing columns ['weight'] |
| data_change | g_add_row | 0.58 (12) | invalid DSL: row is missing columns ['weight'] |
| new_limit | g_cap_measure_scope | 0.59 (44) | invalid DSL: unknown table 'undamaged_stock'; tables are ['days', 'demand', 'depots', 'rental |
| data_change | g_scale_column | 0.65 (23) | result differs from reference |
| data_change | g_remove_row | 0.67 (24) | result differs from reference |
| new_limit | combo | 0.70 (33) | invalid DSL: unknown measure 'x[item, bin]'; measures are ['x', 'y'] |
| data_change | g_set_column | 0.71 (21) | invalid DSL: unknown parameter 'price_other_depot'; parameters are ['cost_per_car', 'damage_e |
| data_change | demand_set | 0.83 (6) | result differs from reference |
| data_change | g_scale_all_rows | 0.84 (25) | result differs from reference |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | margin_scale | 1.00 (5) |  |

### `ollama/qwen3:8b`

| family | template | accuracy (n) | typical miss |
|---|---|---|---|
| data_change | outage | 0.00 (4) | invalid DSL: no row of 'downtime' matches {"month": "Feb", "machine": "planer"} |
| new_limit | cap_each_month | 0.00 (1) | result differs from reference |
| new_limit | cap_store_month | 0.00 (4) | result differs from reference |
| data_change | process_hours | 0.33 (3) | result differs from reference |
| data_change | retire | 0.33 (3) | result differs from reference |
| new_limit | combo | 0.52 (33) | result differs from reference |
| new_limit | g_cap_measure_total | 0.52 (44) | invalid DSL: unknown table 'rentals'; tables are ['days', 'demand', 'depots', 'rental_lengths |
| data_change | margin_set | 0.67 (6) | invalid DSL: unknown parameter 'profit_per_unit'; parameters are ['holding_cost', 'hours_per_ |
| data_change | combo | 0.76 (58) | invalid DSL: '*' is not a product; known values: ['Prod1', 'Prod2', 'Prod3', 'Prod4', 'Prod5' |
| data_change | param | 0.80 (5) | result differs from reference |
| new_limit | cap_total_make | 0.80 (5) | result differs from reference |
| new_limit | g_floor_measure_scope | 0.83 (23) | invalid DSL: row is missing columns ['required', 'max_recruit'] |
| data_change | g_scale_all_rows | 0.84 (25) | result differs from reference |
| new_limit | g_cap_measure_scope | 0.89 (44) | result differs from reference |
| data_change | g_set_column | 0.90 (21) | result differs from reference |
| data_change | g_add_row | 0.92 (12) | invalid DSL: '*' is not a bin; known values: ['bin0', 'bin1', 'bin10', 'bin2', 'bin3', 'bin4' |
| data_change | g_param | 0.97 (33) | invalid DSL: unknown table 'params'; tables are ['mines', 'years'] |
| data_change | demand_scale | 1.00 (5) |  |
| data_change | demand_set | 1.00 (6) |  |
| data_change | demand_zero | 1.00 (2) |  |
| data_change | g_remove_row | 1.00 (24) |  |
| data_change | g_scale_column | 1.00 (23) |  |
| data_change | install | 1.00 (1) |  |
| data_change | margin_scale | 1.00 (5) |  |
| data_change | outage_cancel | 1.00 (4) |  |
| new_limit | cap_total_store | 1.00 (3) |  |
| new_limit | cap_two_products_month | 1.00 (2) |  |

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

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt |
|---|---|---|---|---|---|
| `ollama/gpt-oss:20b` | 6 | 0 | 0 | 1 | 0 |
| `ollama/qwen3:14b` | 12 | 27 | 0 | 0 | 0 |
| `ollama/qwen3:32b` | 11 | 31 | 0 | 0 | 0 |
| `ollama/qwen3:4b` | 96 | 103 | 1 | 1 | 0 |
| `ollama/qwen3:8b` | 40 | 45 | 0 | 0 | 0 |
| `ollama/qwen3:8b+think=on` | 36 | 6 | 3 | 29 | 0 |
