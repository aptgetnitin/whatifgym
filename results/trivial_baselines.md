# Trivial baselines

Mean reward of the three trivial agents on every task file (`scripts/run_trivial_baselines.py`). Expected: oracle 1.100 (gold scenario), noop 0.100 (valid but empty scenario: validity bonus only), ask_then_oracle 0.900 (gold scenario after one needless clarification). Any other value is a bug or a leaked task.

| task file | tasks | oracle | noop | ask_then_oracle |
|---|---|---|---|---|
| `tasks/bin_packing/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/bin_packing/new_limit_v0.jsonl` | 4 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning/data_change_v0.jsonl` | 60 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning_2/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning_2/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_manufacture/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_manufacture/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/manpower_planning/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/manpower_planning/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/mining/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/mining/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/multiple_knapsack/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/multiple_knapsack/new_limit_v0.jsonl` | 15 | 1.100 | 0.100 | 0.900 |
| `tasks/power_generation_hydro/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/power_generation_hydro/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/wedding_seating/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |

Total tasks: **399** in 19 files.

No deviations from the expected rewards.
