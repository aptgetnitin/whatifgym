# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | data_change | new_limit | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:8b` | 399 | 0.787 | 0.876 | 0.89 | 0.86 (240) | 0.67 (159) | 0.77 (131) | 0.86 (173) | 0.67 (95) | 6.0 |

## By base model

| base model | `ollama/qwen3:8b` |
|---|---|
| `bin_packing` | 0.92 (24) |
| `car_rental` | 0.88 (40) |
| `factory_planning` | 0.61 (80) |
| `factory_planning_2` | 0.75 (40) |
| `food_manufacture` | 0.93 (40) |
| `manpower_planning` | 0.68 (40) |
| `mining` | 0.88 (40) |
| `multiple_knapsack` | 0.74 (35) |
| `power_generation_hydro` | 0.82 (40) |
| `wedding_seating` | 1.00 (20) |

## By template (where the misses are)

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt |
|---|---|---|---|---|---|
| `ollama/qwen3:8b` | 40 | 45 | 0 | 0 | 0 |
