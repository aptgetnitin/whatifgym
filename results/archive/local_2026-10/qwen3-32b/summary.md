# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | data_change | new_limit | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:32b` | 399 | 0.895 | 0.987 | 0.92 | 0.85 (240) | 0.96 (159) | 0.97 (131) | 0.90 (173) | 0.79 (95) | 8.5 |

## By base model

| base model | `ollama/qwen3:32b` |
|---|---|
| `bin_packing` | 0.92 (24) |
| `car_rental` | 0.93 (40) |
| `factory_planning` | 0.78 (80) |
| `factory_planning_2` | 0.93 (40) |
| `food_manufacture` | 0.95 (40) |
| `manpower_planning` | 0.93 (40) |
| `mining` | 0.93 (40) |
| `multiple_knapsack` | 0.89 (35) |
| `power_generation_hydro` | 0.90 (40) |
| `wedding_seating` | 1.00 (20) |

## By template (where the misses are)

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt |
|---|---|---|---|---|---|
| `ollama/qwen3:32b` | 11 | 31 | 0 | 0 | 0 |
