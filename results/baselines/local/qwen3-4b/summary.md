# Results summary

Accuracy = share of episodes whose re-solved result matched the hidden reference (status, objective and scoring KPIs within 1e-3 relative). Mean reward adds +0.1 for a valid scenario and −0.2 for a needless clarifying question. Numbers in parentheses are episode counts. Trivial agents are left out; see `results/trivial_baselines.md` for them.

## By family and difficulty

| model | episodes | accuracy | mean reward | valid DSL | data_change | new_limit | easy | medium | hard | s/episode |
|---|---|---|---|---|---|---|---|---|---|---|
| `ollama/qwen3:4b` | 399 | 0.501 | 0.575 | 0.74 | 0.57 (240) | 0.40 (159) | 0.34 (131) | 0.57 (173) | 0.60 (95) | 2.4 |

## By base model

| base model | `ollama/qwen3:4b` |
|---|---|
| `bin_packing` | 0.42 (24) |
| `car_rental` | 0.35 (40) |
| `factory_planning` | 0.36 (80) |
| `factory_planning_2` | 0.53 (40) |
| `food_manufacture` | 0.65 (40) |
| `manpower_planning` | 0.40 (40) |
| `mining` | 0.62 (40) |
| `multiple_knapsack` | 0.77 (35) |
| `power_generation_hydro` | 0.55 (40) |
| `wedding_seating` | 0.50 (20) |

## By template (where the misses are)

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

## Failure modes

| model | wrong result | invalid DSL | unparseable | cut off at max tokens | truncated prompt |
|---|---|---|---|---|---|
| `ollama/qwen3:4b` | 96 | 103 | 1 | 1 | 0 |
