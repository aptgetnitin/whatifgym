# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | data_change | new_limit | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:14b` | 399 | 0.902 | 0.995 | 0.93 | 0.85 (240) | 0.97 (159) | 0.95 (131) | 0.93 (173) | 0.79 (95) | 3.7 |

## By base model

| base model | `ollama/qwen3:14b` |
|---|---|
| `bin_packing` | 1.00 (24) |
| `car_rental` | 0.95 (40) |
| `factory_planning` | 0.79 (80) |
| `factory_planning_2` | 0.97 (40) |
| `food_manufacture` | 0.88 (40) |
| `manpower_planning` | 0.78 (40) |
| `mining` | 1.00 (40) |
| `multiple_knapsack` | 0.94 (35) |
| `power_generation_hydro` | 0.93 (40) |
| `wedding_seating` | 1.00 (20) |

## By template (where the misses are)

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt |
|---|---|---|---|---|---|
| `ollama/qwen3:14b` | 12 | 27 | 0 | 0 | 0 |
