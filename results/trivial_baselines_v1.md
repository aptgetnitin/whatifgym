# Trivial baselines

Mean reward of the three trivial agents on every task file (`scripts/run_trivial_baselines.py`). Expected on fully specified tasks: oracle 1.100 (gold scenario), noop 0.100 (valid but empty scenario: validity bonus only), ask_then_oracle 0.900 (gold scenario after one needless clarification). On `under_specified` files the expectations are 0.000 / 0.000 / 1.100, because answering without asking scores 0 there. Any other value is a bug or a leaked task.

The last two columns are *accuracy* (share of tasks answered correctly) of two probes without an exact expectation: `nearest_example` copies the gold scenario of the most similar training task on the same base model, `random_valid` submits a random valid scenario. Both must stay low; files above 0.10 are listed under Warnings.

| task file | tasks | oracle | noop | ask_then_oracle | nearest_example acc | random_valid acc |
|---|---|---|---|---|---|---|
| `tasks/battery_scheduling/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/battery_scheduling/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/battery_scheduling/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/battery_scheduling/infeasible_request_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/battery_scheduling/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/battery_scheduling/new_limit_v1.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/battery_scheduling/objective_change_v1.jsonl` | 8 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/battery_scheduling/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/battery_scheduling/relax_remove_v0.jsonl` | 1 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/battery_scheduling/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/bin_packing/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/bin_packing/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/bin_packing/new_limit_v1.jsonl` | 1 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/bin_packing/relative_rule_v1.jsonl` | 7 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/bin_packing/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/car_rental/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/car_rental/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/car_rental/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental/infeasible_request_v0.jsonl` | 2 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental/new_limit_v0_nl.jsonl` | 9 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental/objective_change_v1.jsonl` | 13 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/car_rental_2/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/car_rental_2/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/car_rental_2/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/car_rental_2/infeasible_request_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental_2/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental_2/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/car_rental_2/objective_change_v1.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental_2/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/car_rental_2/relax_remove_v0.jsonl` | 14 | 1.100 | 0.100 | 0.900 | 0.00 | 0.07 |
| `tasks/car_rental_2/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/factory_planning/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning/data_change_v0.jsonl` | 60 | 1.100 | 0.100 | 0.900 | 0.02 | 0.00 |
| `tasks/factory_planning/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning/infeasible_request_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning/objective_change_v0.jsonl` | 3 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning/relax_remove_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/factory_planning_2/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning_2/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning_2/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning_2/infeasible_request_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning_2/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning_2/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning_2/objective_change_v1.jsonl` | 7 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning_2/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning_2/relax_remove_v0.jsonl` | 7 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/factory_planning_2/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/farm_planning/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/farm_planning/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.05 |
| `tasks/farm_planning/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/farm_planning/infeasible_request_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/farm_planning/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/farm_planning/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/farm_planning/objective_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/farm_planning/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/farm_planning/relax_remove_v0.jsonl` | 7 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/farm_planning/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/food_manufacture/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_manufacture/data_change_v1.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_manufacture/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_manufacture/infeasible_request_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_manufacture/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_manufacture/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_manufacture/new_limit_v0_nl.jsonl` | 6 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_manufacture/objective_change_v1.jsonl` | 11 | 1.100 | 0.100 | 0.900 | 0.09 | 0.00 |
| `tasks/food_manufacture/relative_rule_v1.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_manufacture/relax_remove_v0.jsonl` | 1 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_manufacture/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/food_supply/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_supply/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/food_supply/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_supply/infeasible_request_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_supply/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_supply/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_supply/objective_change_v0.jsonl` | 4 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_supply/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/food_supply/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/manpower_planning/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/manpower_planning/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/manpower_planning/data_change_v0_nl.jsonl` | 3 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/manpower_planning/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/manpower_planning/infeasible_request_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/manpower_planning/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/manpower_planning/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/manpower_planning/new_limit_v0_nl.jsonl` | 15 | 1.100 | 0.100 | 0.900 | 0.07 | 0.00 |
| `tasks/manpower_planning/objective_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/manpower_planning/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/manpower_planning/relax_remove_v0.jsonl` | 12 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/manpower_planning/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/mining/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/mining/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/mining/data_change_v0_nl.jsonl` | 3 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/mining/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.05 |
| `tasks/mining/infeasible_request_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/mining/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/mining/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/mining/new_limit_v0_nl.jsonl` | 9 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/mining/objective_change_v1.jsonl` | 2 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/mining/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/mining/relax_remove_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/mining/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/multiple_knapsack/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/multiple_knapsack/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.05 | 0.00 |
| `tasks/multiple_knapsack/fixed_decision_v1.jsonl` | 2 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/multiple_knapsack/logical_rule_v0.jsonl` | 18 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/multiple_knapsack/new_limit_v1.jsonl` | 6 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/multiple_knapsack/objective_change_v0.jsonl` | 1 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/multiple_knapsack/relative_rule_v1.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/multiple_knapsack/relax_remove_v0.jsonl` | 1 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/multiple_knapsack/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/power_generation_hydro/chained_scenario_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/power_generation_hydro/data_change_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/power_generation_hydro/fixed_decision_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/power_generation_hydro/infeasible_request_v0.jsonl` | 19 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/power_generation_hydro/logical_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/power_generation_hydro/new_limit_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/power_generation_hydro/objective_change_v1.jsonl` | 14 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/power_generation_hydro/relative_rule_v0.jsonl` | 20 | 1.100 | 0.100 | 0.900 | 0.10 | 0.00 |
| `tasks/power_generation_hydro/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |
| `tasks/wedding_seating/chained_scenario_v0.jsonl` | 7 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/wedding_seating/data_change_v1.jsonl` | 5 | 1.100 | 0.100 | 0.900 | 0.20 | 0.00 |
| `tasks/wedding_seating/relax_remove_v0.jsonl` | 1 | 1.100 | 0.100 | 0.900 | 0.00 | 0.00 |
| `tasks/wedding_seating/under_specified_v0.jsonl` | 20 | 0.000 | 0.000 | 1.100 | 0.00 | 0.00 |

Total tasks: **2239** in 131 files. Overall accuracy: nearest_example **0.017**, random_valid **0.001**.

## Warnings

- tasks/wedding_seating/data_change_v1.jsonl / nearest_example: accuracy 0.20 (['wedding_seating-data_change-001-0001'])

No deviations from the expected rewards.
