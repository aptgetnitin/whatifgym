# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | data_change | new_limit | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:8b` | 399 | 0.895 | 0.993 | 0.98 | 0.93 (240) | 0.85 (159) | 0.89 (131) | 0.98 (173) | 0.75 (95) | 24.0 |

## By base model

| base model | `ollama/qwen3:8b` |
|---|---|
| `bin_packing` | 1.00 (24) |
| `car_rental` | 0.93 (40) |
| `factory_planning` | 0.88 (80) |
| `factory_planning_2` | 0.90 (40) |
| `food_manufacture` | 0.90 (40) |
| `manpower_planning` | 0.90 (40) |
| `mining` | 0.88 (40) |
| `multiple_knapsack` | 0.77 (35) |
| `power_generation_hydro` | 0.93 (40) |
| `wedding_seating` | 0.95 (20) |

## By template (where the misses are)

### `ollama/qwen3:8b`

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
| `ollama/qwen3:8b` | 36 | 6 | 3 | 29 | 0 |
