# Trivial baselines

Mean reward of the three trivial agents on every task file (`scripts/run_trivial_baselines.py`). Expected on fully specified tasks: oracle 1.100 (gold scenario), noop 0.100 (valid but empty scenario: validity bonus only), ask_then_oracle 0.900 (gold scenario after one needless clarification). On `under_specified` files the expectations are 0.000 / 0.000 / 1.100, because answering without asking scores 0 there. Any other value is a bug or a leaked task.

| task file | tasks | oracle | noop | ask_then_oracle |
|---|---|---|---|---|
| `tasks/battery_scheduling/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/battery_scheduling/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/battery_scheduling/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/battery_scheduling/objective_change_v0.jsonl` | 16 | 1.100 | 0.100 | 0.900 |
| `tasks/battery_scheduling/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/battery_scheduling/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/bin_packing/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/bin_packing/new_limit_v0.jsonl` | 4 | 1.100 | 0.100 | 0.900 |
| `tasks/bin_packing/relative_rule_v0.jsonl` | 18 | 1.100 | 0.100 | 0.900 |
| `tasks/bin_packing/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/car_rental/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental/data_change_v0_nl.jsonl` | 6 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental/new_limit_v0_nl.jsonl` | 9 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental/objective_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/car_rental_2/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental_2/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental_2/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental_2/objective_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental_2/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/car_rental_2/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/factory_planning/data_change_v0.jsonl` | 60 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning/objective_change_v0.jsonl` | 3 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/factory_planning_2/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning_2/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning_2/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning_2/objective_change_v0.jsonl` | 13 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning_2/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/factory_planning_2/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/farm_planning/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/farm_planning/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/farm_planning/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/farm_planning/objective_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/farm_planning/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/farm_planning/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/food_manufacture/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_manufacture/data_change_v0_nl.jsonl` | 9 | 1.100 | 0.100 | 0.900 |
| `tasks/food_manufacture/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_manufacture/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_manufacture/new_limit_v0_nl.jsonl` | 6 | 1.100 | 0.100 | 0.900 |
| `tasks/food_manufacture/objective_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_manufacture/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_manufacture/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/food_supply/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_supply/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_supply/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_supply/objective_change_v0.jsonl` | 4 | 1.100 | 0.100 | 0.900 |
| `tasks/food_supply/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/food_supply/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/manpower_planning/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/manpower_planning/data_change_v0_nl.jsonl` | 3 | 1.100 | 0.100 | 0.900 |
| `tasks/manpower_planning/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/manpower_planning/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/manpower_planning/new_limit_v0_nl.jsonl` | 15 | 1.100 | 0.100 | 0.900 |
| `tasks/manpower_planning/objective_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/manpower_planning/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/manpower_planning/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/mining/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/mining/data_change_v0_nl.jsonl` | 3 | 1.100 | 0.100 | 0.900 |
| `tasks/mining/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/mining/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/mining/new_limit_v0_nl.jsonl` | 9 | 1.100 | 0.100 | 0.900 |
| `tasks/mining/objective_change_v0.jsonl` | 11 | 1.100 | 0.100 | 0.900 |
| `tasks/mining/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/mining/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/multiple_knapsack/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/multiple_knapsack/fixed_decision_v0.jsonl` | 15 | 1.100 | 0.100 | 0.900 |
| `tasks/multiple_knapsack/new_limit_v0.jsonl` | 15 | 1.100 | 0.100 | 0.900 |
| `tasks/multiple_knapsack/objective_change_v0.jsonl` | 1 | 1.100 | 0.100 | 0.900 |
| `tasks/multiple_knapsack/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/multiple_knapsack/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/power_generation_hydro/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/power_generation_hydro/data_change_v0_nl.jsonl` | 12 | 1.100 | 0.100 | 0.900 |
| `tasks/power_generation_hydro/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/power_generation_hydro/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/power_generation_hydro/new_limit_v0_nl.jsonl` | 6 | 1.100 | 0.100 | 0.900 |
| `tasks/power_generation_hydro/objective_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/power_generation_hydro/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/power_generation_hydro/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |
| `tasks/wedding_seating/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 |
| `tasks/wedding_seating/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 |

Total tasks: **1578** in 88 files.

No deviations from the expected rewards.
