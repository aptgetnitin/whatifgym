# Hand audit audit_v1: 200 tasks (seed 20261112)

For each task: does the gold scenario say what the question asks? Record `ok`, `wrong`, `ambiguous` or `wording` in `audit_v1.csv`. Made by `scripts/make_audit_pack.py`.

### 1. `airline_planning-chained_scenario-000-0012`

*airline_planning · chained_scenario · template `c_add` · medium*

**Earlier question:** What if the total number of flights operated for aircraft A320#22 may not exceed 3?

```json
{"version": "0.1", "base_model": "airline_planning", "rules": [{"measure": "operate", "scope": {"aircraft": "A320#22"}, "sense": "<=", "value": 3, "name": "cap_operate_A320#22"}]}
```

**Question:** Keep that change. In addition: What if the total number of flights operated, summed over everything, may not exceed 46?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "operate",
   "scope": {
    "aircraft": "A320#22"
   },
   "sense": "<=",
   "value": 3,
   "name": "cap_operate_A320#22"
  },
  {
   "measure": "operate",
   "scope": {},
   "sense": "<=",
   "value": 46,
   "name": "cap_operate_total"
  }
 ],
 "version": "0.1",
 "base_model": "airline_planning"
}
```

**Result:** objective 5.611e+05 → 6.214e+05; lost_revenue 6.214e+05, revenue_kept 1.257e+06, passengers_carried 6,193, revenue_flights_operated 46

### 2. `airline_planning-data_change-000-0016`

*airline_planning · data_change · template `g_scale_all_rows` · medium*

**Question:** What if the ticket revenue is 20% lower for every row of the planned flights table?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "flights",
   "column": "revenue",
   "factor": 0.8
  }
 ],
 "version": "0.1",
 "base_model": "airline_planning"
}
```

**Result:** objective 5.611e+05 → 4.489e+05; lost_revenue 4.489e+05, revenue_kept 1.054e+06, passengers_carried 6,570, revenue_flights_operated 51

### 3. `airline_planning-fixed_decision-000-0001`

*airline_planning · fixed_decision · template `f_fix_zero` · easy*

**Question:** Suppose we decide against aircraft A318#8, flight 3103: set its number of flights operated to 0 and re-plan.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "operate",
   "scope": {
    "aircraft": "A318#8",
    "flight": 3103
   },
   "value": 0
  }
 ],
 "version": "0.1",
 "base_model": "airline_planning"
}
```

**Result:** objective 5.611e+05 → 5.687e+05; lost_revenue 5.687e+05, revenue_kept 1.31e+06, passengers_carried 6,528, revenue_flights_operated 51

### 4. `airline_planning-new_limit-000-0009`

*airline_planning · new_limit · template `g_cap_measure_scope` · medium*

**Question:** Add a limit: the number of flights operated, summed over everything with aircraft = A320#22, must stay at or below 3.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "operate",
   "scope": {
    "aircraft": "A320#22"
   },
   "sense": "<=",
   "value": 3,
   "name": "cap_operate_A320#22"
  }
 ],
 "version": "0.1",
 "base_model": "airline_planning"
}
```

**Result:** objective 5.611e+05 → 5.655e+05; lost_revenue 5.655e+05, revenue_kept 1.313e+06, passengers_carried 6,432, revenue_flights_operated 51

### 5. `assignment_with_constraints-fixed_decision-000-0001`

*assignment_with_constraints · fixed_decision · template `f_fix_zero` · easy*

**Question:** Suppose we decide against team team_10_11: set its number of teams chosen to 0 and re-plan.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "team",
   "scope": {
    "team": "team_10_11"
   },
   "value": 0
  }
 ],
 "version": "0.1",
 "base_model": "assignment_with_constraints"
}
```

**Result:** objective 239 → 253; total_cost 253, assignments 6, workers_used 6, max_worker_load 15, extra_assignments 0

### 6. `assignment_with_constraints-fixed_decision-000-0013`

*assignment_with_constraints · fixed_decision · template `f_fix_zero` · easy*

**Question:** What if worker worker_1 is ruled out (the number of workers working there is fixed at 0)?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "works",
   "scope": {
    "worker": "worker_1"
   },
   "value": 0
  }
 ],
 "version": "0.1",
 "base_model": "assignment_with_constraints"
}
```

**Result:** objective 239 → 268; total_cost 268, assignments 6, workers_used 6, max_worker_load 15, extra_assignments 0

### 7. `assignment_with_constraints-logical_rule-000-0007`

*assignment_with_constraints · logical_rule · template `l_at_most_k` · hard*

**Question:** What if at most 1 of worker worker_10, worker_0, worker_11 and worker_1 may have a non-zero number of workers working?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 3,
   "of": [
    {
     "measure": "works",
     "scope": {
      "worker": "worker_10"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "works",
     "scope": {
      "worker": "worker_0"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "works",
     "scope": {
      "worker": "worker_11"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "works",
     "scope": {
      "worker": "worker_1"
     },
     "sense": "<=",
     "value": 0
    }
   ],
   "name": "at_most_1_works"
  }
 ],
 "version": "0.1",
 "base_model": "assignment_with_constraints"
}
```

**Result:** objective 239 → 280; total_cost 280, assignments 6, workers_used 6, max_worker_load 15, extra_assignments 0

### 8. `assignment_with_constraints-logical_rule-000-0013`

*assignment_with_constraints · logical_rule · template `l_at_most_k` · hard*

**Question:** What if at most 2 of worker worker_1, worker_0, worker_11 and worker_10 may have a non-zero number of workers working?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 2,
   "of": [
    {
     "measure": "works",
     "scope": {
      "worker": "worker_1"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "works",
     "scope": {
      "worker": "worker_0"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "works",
     "scope": {
      "worker": "worker_11"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "works",
     "scope": {
      "worker": "worker_10"
     },
     "sense": "<=",
     "value": 0
    }
   ],
   "name": "at_most_2_works"
  }
 ],
 "version": "0.1",
 "base_model": "assignment_with_constraints"
}
```

**Result:** objective 239 → 262; total_cost 262, assignments 6, workers_used 6, max_worker_load 15, extra_assignments 0

### 9. `assignment_with_constraints-new_limit-000-0001`

*assignment_with_constraints · new_limit · template `g_floor_measure_scope` · medium*

**Question:** What if the total number of task assignments for worker worker_10 must be at least 2?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "assign",
   "scope": {
    "worker": "worker_10"
   },
   "sense": ">=",
   "value": 2,
   "name": "floor_assign_worker_10"
  }
 ],
 "version": "0.1",
 "base_model": "assignment_with_constraints"
}
```

**Result:** objective 239 → 322; total_cost 322, assignments 7, workers_used 6, max_worker_load 15, extra_assignments 1

### 10. `assignment_with_constraints-new_limit-000-0004`

*assignment_with_constraints · new_limit · template `g_floor_measure_scope` · medium*

**Question:** Add a requirement: the number of task assignments, summed over everything with worker = worker_1, must be at least 2.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "assign",
   "scope": {
    "worker": "worker_1"
   },
   "sense": ">=",
   "value": 2,
   "name": "floor_assign_worker_1"
  }
 ],
 "version": "0.1",
 "base_model": "assignment_with_constraints"
}
```

**Result:** objective 239 → 274; total_cost 274, assignments 7, workers_used 6, max_worker_load 15, extra_assignments 1

### 11. `assignment_with_constraints-under_specified-000-0007`

*assignment_with_constraints · under_specified · template `ask_g_floor_measure_scope` · medium*

**Question:** What if we require a minimum number of task assignments?

**Planner's answer when asked:** The total number of task assignments for task task_2 must be at least 2.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "assign",
   "scope": {
    "task": "task_2"
   },
   "sense": ">=",
   "value": 2,
   "name": "floor_assign_task_2"
  }
 ],
 "version": "0.1",
 "base_model": "assignment_with_constraints"
}
```

**Result:** objective 239 → 292; total_cost 292, assignments 7, workers_used 6, max_worker_load 15, extra_assignments 1

### 12. `battery_scheduling-chained_scenario-000-0019`

*battery_scheduling · chained_scenario · template `c_revise` · hard*

**Earlier question:** Add a limit: the battery discharging power (kW), summed over everything with hour = 21-22, must stay at or below 3.5.

```json
{"version": "0.1", "base_model": "battery_scheduling", "rules": [{"measure": "discharge", "scope": {"hour": "21-22"}, "sense": "<=", "value": 3.5, "name": "cap_discharge_21-22"}]}
```

**Question:** Correction: make that limit 4.5, not 3.5.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "discharge",
   "scope": {
    "hour": "21-22"
   },
   "sense": "<=",
   "value": 4.5,
   "name": "cap_discharge_21-22"
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 1.516; profit 1.516, export_revenue 2.61, import_cost 1.094, energy_charged_kwh 7.812, energy_discharged_kwh 7.2

### 13. `battery_scheduling-data_change-000-0011`

*battery_scheduling · data_change · template `g_scale_column` · medium*

**Question:** What if the grid import price (EUR/kWh) for hour 16-17 is 25% lower?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "hours",
   "column": "import_price",
   "where": {
    "hour": "16-17"
   },
   "factor": 0.75
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 1.68; profit 1.68, export_revenue 3.674, import_cost 1.994, energy_charged_kwh 12.81, energy_discharged_kwh 11.81

### 14. `battery_scheduling-data_change-000-0015`

*battery_scheduling · data_change · template `g_scale_all_rows` · medium*

**Question:** Every grid import price (EUR/kWh) in the hourly prices table rises by 10%. Effect?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "hours",
   "column": "import_price",
   "factor": 1.1
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 1.457; profit 1.457, export_revenue 2.66, import_cost 1.203, energy_charged_kwh 7.812, energy_discharged_kwh 7.2

### 15. `battery_scheduling-fixed_decision-000-0015`

*battery_scheduling · fixed_decision · template `f_fix_level` · medium*

**Question:** What if the battery stored energy (kWh) for hour 22-23 is fixed at 4.5?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "soc",
   "scope": {
    "hour": "22-23"
   },
   "value": 4.5
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 1.467; profit 1.467, export_revenue 3.092, import_cost 1.625, energy_charged_kwh 9.375, energy_discharged_kwh 8.64

### 16. `battery_scheduling-infeasible_request-000-0012`

*battery_scheduling · infeasible_request · template `i_commit` · medium*

**Question:** We have promised 27 battery stored energy (kWh) for hour 05-06, no more and no less. Re-plan.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "soc",
   "scope": {
    "hour": "05-06"
   },
   "value": 27
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** infeasible; conflicting constraints: soc_balance_06_07

### 17. `battery_scheduling-logical_rule-000-0019`

*battery_scheduling · logical_rule · template `l_if_then` · hard*

**Question:** What if a non-zero battery stored energy (kWh) for hour 18-19 requires a total battery charging power (kW) of at least 5.6 for hour 02-03?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "soc",
     "scope": {
      "hour": "18-19"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "charge",
     "scope": {
      "hour": "02-03"
     },
     "sense": ">=",
     "value": 5.6
    }
   ],
   "name": "if_soc_then_charge"
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 0.1898; profit 0.1898, export_revenue 4.684, import_cost 4.494, energy_charged_kwh 17.81, energy_discharged_kwh 16.42

### 18. `battery_scheduling-new_limit-001-0011`

*battery_scheduling · new_limit · template `g_cap_measure_total` · easy*

**Question:** An overall cap of 140 applies to the battery stored energy (kWh), summed over everything.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "soc",
   "scope": {},
   "sense": "<=",
   "value": 140,
   "name": "cap_soc_total"
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 0.992; profit 0.992, export_revenue 3.214, import_cost 2.222, energy_charged_kwh 14.06, energy_discharged_kwh 12.96

### 19. `battery_scheduling-objective_change-001-0007`

*battery_scheduling · objective_change · template `o_then_scoped` · medium*

**Question:** What if we first make sure daily profit stays at its maximum and then make the battery stored energy (kWh) for hour 02-03 as large as possible?

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "max",
   "measure": "original"
  },
  {
   "sense": "max",
   "measure": "soc",
   "scope": {
    "hour": "02-03"
   }
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 10.8; profit 1.566, export_revenue 2.66, import_cost 1.094, energy_charged_kwh 7.812, energy_discharged_kwh 7.2

### 20. `battery_scheduling-relative_rule-000-0016`

*battery_scheduling · relative_rule · template `r_share_of_total` · medium*

**Question:** Suppose at most 60% of the total battery discharging power (kW) may go to hour 21-22.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "discharge",
   "scope": {
    "hour": "21-22"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "discharge",
    "scope": {}
   },
   "factor": 0.6,
   "name": "share_discharge_21-22"
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 1.528; profit 1.528, export_revenue 2.819, import_cost 1.291, energy_charged_kwh 9.042, energy_discharged_kwh 8.333

### 21. `battery_scheduling-under_specified-000-0013`

*battery_scheduling · under_specified · template `ask_g_cap_measure_total` · medium*

**Question:** There is going to be an upper limit on battery discharging power (kW). How does the plan change?

**Planner's answer when asked:** An overall cap of 6.5 applies to the battery discharging power (kW), summed over everything.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "discharge",
   "scope": {},
   "sense": "<=",
   "value": 6.5,
   "name": "cap_discharge_total"
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 1.463; profit 1.463, export_revenue 2.45, import_cost 0.9874, energy_charged_kwh 7.053, energy_discharged_kwh 6.5

### 22. `battery_scheduling-under_specified-000-0015`

*battery_scheduling · under_specified · template `ask_g_cap_measure_scope` · medium*

**Question:** There is going to be an upper limit on battery stored energy (kWh). How does the plan change?

**Planner's answer when asked:** The total battery stored energy (kWh) for hour 05-06 may not exceed 10.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "soc",
   "scope": {
    "hour": "05-06"
   },
   "sense": "<=",
   "value": 10,
   "name": "cap_soc_05-06"
  }
 ],
 "version": "0.1",
 "base_model": "battery_scheduling"
}
```

**Result:** objective 1.566 → 1.53; profit 1.53, export_revenue 2.66, import_cost 1.13, energy_charged_kwh 7.812, energy_discharged_kwh 7.2

### 23. `bin_packing-data_change-000-0009`

*bin_packing · data_change · template `g_scale_column` · medium*

**Question:** Suppose the item weight of item item2 (in the items to pack table) falls by 50%.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "items",
   "column": "weight",
   "where": {
    "item": "item2"
   },
   "factor": 0.5
  }
 ],
 "version": "0.1",
 "base_model": "bin_packing"
}
```

**Result:** objective 4 → 4; bins_used 4, total_weight 360.5, min_bins_by_weight 4

### 24. `bin_packing-data_change-000-0019`

*bin_packing · data_change · template `g_scale_column` · medium*

**Question:** What if the item weight for item item5 is 25% higher?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "items",
   "column": "weight",
   "where": {
    "item": "item5"
   },
   "factor": 1.25
  }
 ],
 "version": "0.1",
 "base_model": "bin_packing"
}
```

**Result:** objective 4 → 4; bins_used 4, total_weight 376.8, min_bins_by_weight 4

### 25. `car_rental-chained_scenario-000-0010`

*car_rental · chained_scenario · template `c_revise` · hard*

**Earlier question:** What if the total cars rented out, summed over everything, may not exceed 1350?

```json
{"version": "0.1", "base_model": "car_rental", "rules": [{"measure": "rentals", "scope": {}, "sense": "<=", "value": 1350, "name": "cap_rentals_total"}]}
```

**Question:** Correction: make that limit 1600, not 1350.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "rentals",
   "scope": {},
   "sense": "<=",
   "value": 1600,
   "name": "cap_rentals_total"
  }
 ],
 "version": "0.1",
 "base_model": "car_rental"
}
```

**Result:** objective 1.212e+05 → 1.014e+05; profit 1.014e+05, rental_contribution 1.103e+05, transfer_cost 1,469, fleet_cost 7,419, fleet_size 494.6

### 26. `car_rental-data_change-000-0013`

*car_rental · data_change · template `g_scale_column` · medium*

**Question:** Suppose the price, return to another depot of rental length 2 (in the rental-length mix and prices table) rises by 10%.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "rental_lengths",
   "column": "price_other_depot",
   "where": {
    "rental_days": 2
   },
   "factor": 1.1
  }
 ],
 "version": "0.1",
 "base_model": "car_rental"
}
```

**Result:** objective 1.212e+05 → 1.229e+05; profit 1.229e+05, rental_contribution 1.34e+05, transfer_cost 1,904, fleet_cost 9,250, fleet_size 616.7

### 27. `car_rental-fixed_decision-000-0003`

*car_rental · fixed_decision · template `f_fix_scope` · hard*

**Question:** What if the undamaged cars kept at the depot overnight for depot Manchester is fixed at 1.7 for every day?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "undamaged_left",
   "scope": {
    "depot": "Manchester"
   },
   "value": 1.7
  }
 ],
 "version": "0.1",
 "base_model": "car_rental"
}
```

**Result:** objective 1.212e+05 → 1.207e+05; profit 1.207e+05, rental_contribution 1.323e+05, transfer_cost 2,330, fleet_cost 9,259, fleet_size 617.3

### 28. `car_rental-fixed_decision-000-0013`

*car_rental · fixed_decision · template `combo` · hard*

**Question:** Two commitments at once: day Wednesday, origin depot Glasgow, destination depot Manchester gets 3.8 damaged cars transferred, no more and no less; and the cars rented out for depot Glasgow is fixed at 68 for every day. Optimise the rest.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "damaged_transfers",
   "scope": {
    "day": "Wednesday",
    "from_depot": "Glasgow",
    "to_depot": "Manchester"
   },
   "value": 3.8
  },
  {
   "measure": "rentals",
   "scope": {
    "depot": "Glasgow"
   },
   "value": 68
  }
 ],
 "version": "0.1",
 "base_model": "car_rental"
}
```

**Result:** objective 1.212e+05 → 1.211e+05; profit 1.211e+05, rental_contribution 1.323e+05, transfer_cost 1,918, fleet_cost 9,287, fleet_size 619.1

### 29. `car_rental-new_limit-000-0016`

*car_rental · new_limit · template `g_floor_measure_scope` · medium*

**Question:** What if the total undamaged cars at the depot in the morning for day Thursday must be at least 410?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "undamaged_stock",
   "scope": {
    "day": "Thursday"
   },
   "sense": ">=",
   "value": 410,
   "name": "floor_undamaged_stock_Thursday"
  }
 ],
 "version": "0.1",
 "base_model": "car_rental"
}
```

**Result:** objective 1.212e+05 → 1.209e+05; profit 1.209e+05, rental_contribution 1.323e+05, transfer_cost 1,904, fleet_cost 9,530, fleet_size 635.4

### 30. `car_rental-new_limit-000-0019`

*car_rental · new_limit · template `combo` · hard*

**Question:** What if the damaged cars kept at the depot overnight, summed over everything with day = Saturday, must be at least 1.9, and in addition the total damaged cars at the depot in the morning for depot Manchester may not exceed 67?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "damaged_left",
   "scope": {
    "day": "Saturday"
   },
   "sense": ">=",
   "value": 1.9,
   "name": "floor_damaged_left_Saturday"
  },
  {
   "measure": "damaged_stock",
   "scope": {
    "depot": "Manchester"
   },
   "sense": "<=",
   "value": 67,
   "name": "cap_damaged_stock_Manchester"
  }
 ],
 "version": "0.1",
 "base_model": "car_rental"
}
```

**Result:** objective 1.212e+05 → 1.18e+05; profit 1.18e+05, rental_contribution 1.289e+05, transfer_cost 1,885, fleet_cost 8,936, fleet_size 595.7

### 31. `car_rental_2-chained_scenario-000-0005`

*car_rental_2 · chained_scenario · template `c_undo` · hard*

**Earlier question:** Assume the marginal cost per rental of rental length 3 is now 60.

```json
{"version": "0.1", "base_model": "car_rental_2", "data_changes": [{"op": "set", "table": "rental_lengths", "column": "marginal_cost", "where": {"rental_days": 3}, "value": 60}]}
```

**Question:** Forget that change. Instead: Assume the price, return to same depot of rental length 2 is now 35.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "rental_lengths",
   "column": "price_same_depot",
   "where": {
    "rental_days": 2
   },
   "value": 35
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.219e+05; profit 1.219e+05, rental_contribution 1.638e+05, transfer_cost 4,121, fleet_cost 1.279e+04, fleet_size 852.4, expansion_cost 2.5e+04

### 32. `car_rental_2-chained_scenario-000-0006`

*car_rental_2 · chained_scenario · template `c_add` · medium*

**Earlier question:** An overall cap of 50 applies to the undamaged cars transferred, summed over everything.

```json
{"version": "0.1", "base_model": "car_rental_2", "rules": [{"measure": "undamaged_transfers", "scope": {}, "sense": "<=", "value": 50, "name": "cap_undamaged_transfers_total"}]}
```

**Question:** On top of that: Assume the rental demand of day Monday, depot Glasgow is now 80.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "demand",
   "column": "demand",
   "where": {
    "day": "Monday",
    "depot": "Glasgow"
   },
   "value": 80
  }
 ],
 "rules": [
  {
   "measure": "undamaged_transfers",
   "scope": {},
   "sense": "<=",
   "value": 50,
   "name": "cap_undamaged_transfers_total"
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.317e+05; profit 1.317e+05, rental_contribution 1.736e+05, transfer_cost 4,121, fleet_cost 1.281e+04, fleet_size 853.7, expansion_cost 2.5e+04

### 33. `car_rental_2-chained_scenario-000-0007`

*car_rental_2 · chained_scenario · template `c_revise` · hard*

**Earlier question:** What if the total cars rented out for depot Plymouth may not exceed 360?

```json
{"version": "0.1", "base_model": "car_rental_2", "rules": [{"measure": "rentals", "scope": {"depot": "Plymouth"}, "sense": "<=", "value": 360, "name": "cap_rentals_Plymouth"}]}
```

**Question:** Correction: make that limit 400, not 360.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "rentals",
   "scope": {
    "depot": "Plymouth"
   },
   "sense": "<=",
   "value": 400,
   "name": "cap_rentals_Plymouth"
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.323e+05; profit 1.323e+05, rental_contribution 1.943e+05, transfer_cost 3,292, fleet_cost 1.476e+04, fleet_size 983.7, expansion_cost 4.4e+04

### 34. `car_rental_2-chained_scenario-000-0018`

*car_rental_2 · chained_scenario · template `c_revise` · hard*

**Earlier question:** What if the total undamaged cars kept at the depot overnight, summed over everything, may not exceed 540?

```json
{"version": "0.1", "base_model": "car_rental_2", "rules": [{"measure": "undamaged_left", "scope": {}, "sense": "<=", "value": 540, "name": "cap_undamaged_left_total"}]}
```

**Question:** Correction: make that limit 590, not 540.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "undamaged_left",
   "scope": {},
   "sense": "<=",
   "value": 590,
   "name": "cap_undamaged_left_total"
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.322e+05; profit 1.322e+05, rental_contribution 1.943e+05, transfer_cost 3,546, fleet_cost 1.456e+04, fleet_size 970.4, expansion_cost 4.4e+04

### 35. `car_rental_2-data_change-000-0011`

*car_rental_2 · data_change · template `combo` · hard*

**Question:** Two things change together: every price, return to same depot in the rental-length mix and prices table falls by 10%; and the rental demand for day Tuesday, depot Manchester becomes 290. What happens to the plan?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "rental_lengths",
   "column": "price_same_depot",
   "factor": 0.9
  },
  {
   "op": "set",
   "table": "demand",
   "column": "demand",
   "where": {
    "day": "Tuesday",
    "depot": "Manchester"
   },
   "value": 290
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.217e+05; profit 1.217e+05, rental_contribution 1.636e+05, transfer_cost 4,121, fleet_cost 1.279e+04, fleet_size 852.4, expansion_cost 2.5e+04

### 36. `car_rental_2-infeasible_request-000-0017`

*car_rental_2 · infeasible_request · template `i_commit` · medium*

**Question:** We have promised 100 cars repaired for day Friday, depot Birmingham, no more and no less. Re-plan.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "repairs",
   "scope": {
    "day": "Friday",
    "depot": "Birmingham"
   },
   "value": 100
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** infeasible; conflicting constraints: repair_capacity_Friday_Birmingham

### 37. `car_rental_2-logical_rule-000-0001`

*car_rental_2 · logical_rule · template `l_none_or_batch` · medium*

**Question:** What if the total cars repaired for day Tuesday, depot Plymouth must be either zero or at least 12.5?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "repairs",
     "scope": {
      "day": "Tuesday",
      "depot": "Plymouth"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "repairs",
     "scope": {
      "day": "Tuesday",
      "depot": "Plymouth"
     },
     "sense": ">=",
     "value": 12.5
    }
   ],
   "name": "batch_repairs"
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.317e+05; profit 1.317e+05, rental_contribution 1.736e+05, transfer_cost 4,121, fleet_cost 1.279e+04, fleet_size 852.4, expansion_cost 2.5e+04

### 38. `car_rental_2-logical_rule-000-0009`

*car_rental_2 · logical_rule · template `l_none_or_batch` · medium*

**Question:** What if the total cars rented out for day Wednesday, depot Manchester must be either zero or at least 200?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "rentals",
     "scope": {
      "day": "Wednesday",
      "depot": "Manchester"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "rentals",
     "scope": {
      "day": "Wednesday",
      "depot": "Manchester"
     },
     "sense": ">=",
     "value": 200
    }
   ],
   "name": "batch_rentals"
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.315e+05; profit 1.315e+05, rental_contribution 1.736e+05, transfer_cost 3,716, fleet_cost 1.34e+04, fleet_size 893.5, expansion_cost 2.5e+04

### 39. `car_rental_2-objective_change-001-0018`

*car_rental_2 · objective_change · template `o_then_scoped` · medium*

**Question:** What if we first make sure weekly profit stays at its maximum and then make the undamaged cars kept at the depot overnight for depot Birmingham as small as possible?

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "max",
   "measure": "original"
  },
  {
   "sense": "min",
   "measure": "undamaged_left",
   "scope": {
    "depot": "Birmingham"
   }
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 427.1; profit 1.323e+05, rental_contribution 1.943e+05, transfer_cost 3,230, fleet_cost 1.475e+04, fleet_size 983.3, expansion_cost 4.4e+04

### 40. `car_rental_2-relative_rule-000-0016`

*car_rental_2 · relative_rule · template `r_share_of_total` · medium*

**Question:** Suppose at least 60% of the total damaged cars transferred must go to destination depot Manchester.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "damaged_transfers",
   "scope": {
    "to_depot": "Manchester"
   },
   "sense": ">=",
   "relative_to": {
    "measure": "damaged_transfers",
    "scope": {}
   },
   "factor": 0.6,
   "name": "share_damaged_transfers_Manchester"
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.25e+05; profit 1.25e+05, rental_contribution 1.854e+05, transfer_cost 2,413, fleet_cost 1.403e+04, fleet_size 935.6, expansion_cost 4.4e+04

### 41. `car_rental_2-relax_remove-000-0002`

*car_rental_2 · relax_remove · template `x_scoped` · hard*

**Question:** Suppose the daily repair-capacity limit is lifted for depot Manchester and Birmingham only. Effect on the plan?

**Gold scenario:**

```json
{
 "relax": [
  {
   "constraint": "repair_capacity",
   "scope": {
    "depot": [
     "Manchester",
     "Birmingham"
    ]
   }
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.976e+05; profit 1.976e+05, rental_contribution 2.249e+05, transfer_cost 9,748, fleet_cost 1.762e+04, fleet_size 1,175, expansion_cost 0

### 42. `car_rental_2-under_specified-000-0003`

*car_rental_2 · under_specified · template `ask_g_param` · medium*

**Question:** Suppose the damage excess charged changes. What happens to the plan?

**Planner's answer when asked:** The damage excess charged becomes 80.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set_param",
   "name": "damage_excess",
   "value": 80
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.267e+05; profit 1.267e+05, rental_contribution 1.887e+05, transfer_cost 3,230, fleet_cost 1.475e+04, fleet_size 983.4, expansion_cost 4.4e+04

### 43. `car_rental_2-under_specified-000-0018`

*car_rental_2 · under_specified · template `ask_g_scale_all_rows` · medium*

**Question:** What if the price, return to another depot changes across the board?

**Planner's answer when asked:** The price, return to another depot is 20% lower for every row of the rental-length mix and prices table.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "rental_lengths",
   "column": "price_other_depot",
   "factor": 0.8
  }
 ],
 "version": "0.1",
 "base_model": "car_rental_2"
}
```

**Result:** objective 1.323e+05 → 1.102e+05; profit 1.102e+05, rental_contribution 1.521e+05, transfer_cost 4,121, fleet_cost 1.279e+04, fleet_size 852.4, expansion_cost 2.5e+04

### 44. `covid19_facility_location-chained_scenario-000-0004`

*covid19_facility_location · chained_scenario · template `c_undo` · hard*

**Earlier question:** What if the cost of building a temporary facility is halved?

```json
{"version": "0.1", "base_model": "covid19_facility_location", "data_changes": [{"op": "scale_param", "name": "temporary_build_cost", "factor": 0.5}]}
```

**Question:** Forget that change. Instead: Add one more row to the counties table: county new_county, county centroid x coordinate 1, county centroid y coordinate 1 and forecast COVID-19 patients 317. Effect on the plan?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "add",
   "table": "counties",
   "rows": [
    {
     "county": "new_county",
     "x": 1,
     "y": 1,
     "demand": 317
    }
   ]
  }
 ],
 "version": "0.1",
 "base_model": "covid19_facility_location"
}
```

**Result:** objective 1.522e+06 → 3.026e+06; total_cost 3.026e+06, build_cost 3e+06, travel_cost 2.571e+04, temporary_built 6, extra_beds_added 0, patients_at_temporary 600

### 45. `covid19_facility_location-chained_scenario-000-0007`

*covid19_facility_location · chained_scenario · template `c_revise` · hard*

**Earlier question:** Suppose the forecast COVID-19 patients of county C3 (in the counties table) rises by 25%.

```json
{"version": "0.1", "base_model": "covid19_facility_location", "data_changes": [{"op": "scale", "table": "counties", "column": "demand", "where": {"county": "C3"}, "factor": 1.25}]}
```

**Question:** Correction: make that 10% higher, not 25% higher.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "counties",
   "column": "demand",
   "where": {
    "county": "C3"
   },
   "factor": 1.1
  }
 ],
 "version": "0.1",
 "base_model": "covid19_facility_location"
}
```

**Result:** objective 1.522e+06 → 2.021e+06; total_cost 2.021e+06, build_cost 2e+06, travel_cost 2.133e+04, temporary_built 4, extra_beds_added 0, patients_at_temporary 400

### 46. `covid19_facility_location-data_change-000-0002`

*covid19_facility_location · data_change · template `g_scale_all_rows` · medium*

**Question:** What if the forecast COVID-19 patients is 25% lower for every row of the counties table?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "counties",
   "column": "demand",
   "factor": 0.75
  }
 ],
 "version": "0.1",
 "base_model": "covid19_facility_location"
}
```

**Result:** objective 1.522e+06 → 1.265e+04; total_cost 1.265e+04, build_cost 0, travel_cost 1.265e+04, temporary_built 0, extra_beds_added 0, patients_at_temporary 0

### 47. `covid19_facility_location-data_change-000-0012`

*covid19_facility_location · data_change · template `g_scale_column` · medium*

**Question:** Suppose the facility capacity (beds) of facility E2 (in the healthcare facilities table) falls by 10%.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "facilities",
   "column": "capacity",
   "where": {
    "facility": "E2"
   },
   "factor": 0.9
  }
 ],
 "version": "0.1",
 "base_model": "covid19_facility_location"
}
```

**Result:** objective 1.522e+06 → 1.522e+06; total_cost 1.522e+06, build_cost 1.5e+06, travel_cost 2.214e+04, temporary_built 3, extra_beds_added 0, patients_at_temporary 300

### 48. `covid19_facility_location-infeasible_request-000-0009`

*covid19_facility_location · infeasible_request · template `i_commit` · medium*

**Question:** Commit to exactly 2810 patients assigned for county C5, facility E6, and plan the rest around it.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "assign",
   "scope": {
    "county": "C5",
    "facility": "E6"
   },
   "value": 2810
  }
 ],
 "version": "0.1",
 "base_model": "covid19_facility_location"
}
```

**Result:** infeasible; conflicting constraints: demand_C5

### 49. `covid19_facility_location-new_limit-000-0010`

*covid19_facility_location · new_limit · template `g_cap_measure_scope` · medium*

**Question:** Add a limit: the patients assigned, summed over everything with facility = E6, must stay at or below 210.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "assign",
   "scope": {
    "facility": "E6"
   },
   "sense": "<=",
   "value": 210,
   "name": "cap_assign_E6"
  }
 ],
 "version": "0.1",
 "base_model": "covid19_facility_location"
}
```

**Result:** objective 1.522e+06 → 2.021e+06; total_cost 2.021e+06, build_cost 2e+06, travel_cost 2.129e+04, temporary_built 4, extra_beds_added 0, patients_at_temporary 400

### 50. `covid19_facility_location-relax_remove-000-0002`

*covid19_facility_location · relax_remove · template `x_full` · easy*

**Question:** Suppose we drop the bed-capacity limit of the facilities. How does the plan change?

**Gold scenario:**

```json
{
 "relax": [
  {
   "constraint": "capacity"
  }
 ],
 "version": "0.1",
 "base_model": "covid19_facility_location"
}
```

**Result:** objective 1.522e+06 → 1.018e+04; total_cost 1.018e+04, build_cost 0, travel_cost 1.018e+04, temporary_built 0, extra_beds_added 0, patients_at_temporary 234

### 51. `covid19_facility_location-under_specified-000-0003`

*covid19_facility_location · under_specified · template `ask_g_param` · medium*

**Question:** Suppose the cost of building a temporary facility changes. What happens to the plan?

**Planner's answer when asked:** The cost of building a temporary facility changes by a factor of 0.75.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale_param",
   "name": "temporary_build_cost",
   "factor": 0.75
  }
 ],
 "version": "0.1",
 "base_model": "covid19_facility_location"
}
```

**Result:** objective 1.522e+06 → 1.147e+06; total_cost 1.147e+06, build_cost 1.125e+06, travel_cost 2.165e+04, temporary_built 3, extra_beds_added 0, patients_at_temporary 300

### 52. `covid19_facility_location-under_specified-000-0016`

*covid19_facility_location · under_specified · template `ask_g_set_column` · medium*

**Question:** What if the facility capacity (beds) for facility E1 changes?

**Planner's answer when asked:** The facility capacity (beds) of facility E1 is now 562.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "facilities",
   "column": "capacity",
   "where": {
    "facility": "E1"
   },
   "value": 562
  }
 ],
 "version": "0.1",
 "base_model": "covid19_facility_location"
}
```

**Result:** objective 1.522e+06 → 2.364e+04; total_cost 2.364e+04, build_cost 0, travel_cost 2.364e+04, temporary_built 0, extra_beds_added 0, patients_at_temporary 0

### 53. `drone_network-fixed_decision-000-0003`

*drone_network · fixed_decision · template `f_fix_zero` · easy*

**Question:** What if incident location 3800 JEFFERSON BL, drone base 3769 E. STRATFORD ROAD Rescue Squad is ruled out (the number of incident locations assigned to a base there is fixed at 0)?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "assign",
   "scope": {
    "location": "3800 JEFFERSON BL",
    "base": "3769 E. STRATFORD ROAD Rescue Squad"
   },
   "value": 0
  }
 ],
 "version": "0.1",
 "base_model": "drone_network"
}
```

**Result:** objective 37.32 → 38.31; response_objective 38.31, bases_opened 4, avg_wait_minutes 0.2576, avg_flight_minutes 2.299, max_base_utilization 0.0245

### 54. `drone_network-logical_rule-000-0013`

*drone_network · logical_rule · template `l_none_or_batch` · medium*

**Question:** Minimum batch: if the total queue load linked to an assigned location (hours) for incident location 1900 LANDSTOWN CENTRE WAY, drone base 21 MUNICIPAL CTR Fire Station is above zero, it must be at least 0.01.

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "linked_load",
     "scope": {
      "location": "1900 LANDSTOWN CENTRE WAY",
      "base": "21 MUNICIPAL CTR Fire Station"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "linked_load",
     "scope": {
      "location": "1900 LANDSTOWN CENTRE WAY",
      "base": "21 MUNICIPAL CTR Fire Station"
     },
     "sense": ">=",
     "value": 0.01
    }
   ],
   "name": "batch_linked_load"
  }
 ],
 "version": "0.1",
 "base_model": "drone_network"
}
```

**Result:** objective 37.32 → 37.93; response_objective 37.93, bases_opened 4, avg_wait_minutes 0.2666, avg_flight_minutes 2.276, max_base_utilization 0.0253

### 55. `drone_network-new_limit-000-0015`

*drone_network · new_limit · template `combo` · hard*

**Question:** Two new limits at once: the queue load linked to an assigned location (hours), summed over everything with drone base = 5145 RURITAN COURT Rescue Squad, must stay at or below 0.27; and the total queue load linked to an assigned location (hours) for drone base 800 VIRGINIA BEACH BLVD Fire Station must be at least 0.13.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "linked_load",
   "scope": {
    "base": "5145 RURITAN COURT Rescue Squad"
   },
   "sense": "<=",
   "value": 0.27,
   "name": "cap_linked_load_5145 RURITAN COURT Rescue Squad"
  },
  {
   "measure": "linked_load",
   "scope": {
    "base": "800 VIRGINIA BEACH BLVD Fire Station"
   },
   "sense": ">=",
   "value": 0.13,
   "name": "floor_linked_load_800 VIRGINIA BEACH BLVD Fire Station"
  }
 ],
 "version": "0.1",
 "base_model": "drone_network"
}
```

**Result:** objective 37.32 → 39.42; response_objective 39.42, bases_opened 4, avg_wait_minutes 0.1967, avg_flight_minutes 2.365, max_base_utilization 0.017

### 56. `drone_network-relative_rule-000-0008`

*drone_network · relative_rule · template `combo` · hard*

**Question:** Two relative limits at once: the queue load linked to an assigned location (hours) for incident location 5600 MEER ST must be at most 50% of the queue load linked to an assigned location (hours) for incident location 1700 VIRGINIA BEACH BL; and drone base 21 MUNICIPAL CTR Fire Station must account for at most 10% of the total number of drone bases opened.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "linked_load",
   "scope": {
    "location": "5600 MEER ST"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "linked_load",
    "scope": {
     "location": "1700 VIRGINIA BEACH BL"
    }
   },
   "factor": 0.5,
   "name": "rel_linked_load_5600 MEER ST_vs_1700 VIRGINIA BEACH BL"
  },
  {
   "measure": "open",
   "scope": {
    "base": "21 MUNICIPAL CTR Fire Station"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "open",
    "scope": {}
   },
   "factor": 0.1,
   "name": "share_open_21 MUNICIPAL CTR Fire Station"
  }
 ],
 "version": "0.1",
 "base_model": "drone_network"
}
```

**Result:** objective 37.32 → 40; response_objective 40, bases_opened 4, avg_wait_minutes 0.2523, avg_flight_minutes 2.4, max_base_utilization 0.0224

### 57. `drone_network-relative_rule-000-0016`

*drone_network · relative_rule · template `r_two_values` · medium*

**Question:** New policy: the base queue load (hours) for drone base 800 VIRGINIA BEACH BLVD Fire Station must be at least 2 times the base queue load (hours) for drone base 21 MUNICIPAL CTR Fire Station.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "queue_load",
   "scope": {
    "base": "800 VIRGINIA BEACH BLVD Fire Station"
   },
   "sense": ">=",
   "relative_to": {
    "measure": "queue_load",
    "scope": {
     "base": "21 MUNICIPAL CTR Fire Station"
    }
   },
   "factor": 2.0,
   "name": "rel_queue_load_800 VIRGINIA BEACH BLVD Fire Station_vs_21 MUNICIPAL CTR_0bc81bb1"
  }
 ],
 "version": "0.1",
 "base_model": "drone_network"
}
```

**Result:** objective 37.32 → 37.85; response_objective 37.85, bases_opened 4, avg_wait_minutes 0.2818, avg_flight_minutes 2.271, max_base_utilization 0.026

### 58. `economic_planning-data_change-000-0015`

*economic_planning · data_change · template `g_scale_all_rows` · medium*

**Question:** Every input per unit of output in the input-output coefficients table falls by 10%. Effect?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "input_output",
   "column": "input_per_unit_output",
   "factor": 0.9
  }
 ],
 "version": "0.1",
 "base_model": "economic_planning"
}
```

**Result:** objective 1,902 → 2,280; employment 2,280, production_employment 1,883, capacity_building_employment 397.6, total_production 4,198, capacity_built 993.9

### 59. `economic_planning-fixed_decision-000-0003`

*economic_planning · fixed_decision · template `f_fix_scope` · hard*

**Question:** What if the capacity built (million USD/year) for year 3 is fixed at 30 for every industry?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "extra_capacity",
   "scope": {
    "year": 3
   },
   "value": 30
  }
 ],
 "version": "0.1",
 "base_model": "economic_planning"
}
```

**Result:** objective 1,902 → 1,671; employment 1,671, production_employment 1,472, capacity_building_employment 198.8, total_production 3,373, capacity_built 534.4

### 60. `economic_planning-infeasible_request-000-0001`

*economic_planning · infeasible_request · template `i_commit` · medium*

**Question:** Commit to exactly 4810 output produced (million USD) for year 5, industry coal, and plan the rest around it.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "production",
   "scope": {
    "year": 5,
    "industry": "coal"
   },
   "value": 4810
  }
 ],
 "version": "0.1",
 "base_model": "economic_planning"
}
```

**Result:** infeasible; conflicting constraints: balance_1_coal, balance_1_steel, balance_1_transport, balance_2_coal, balance_2_steel, balance_2_transport, balance_3_coal, balance_3_steel, balance_3_transport, balance_4_steel, balance_4_transport

### 61. `economic_planning-infeasible_request-000-0008`

*economic_planning · infeasible_request · template `i_floor` · medium*

**Question:** Management wants at least 740 output produced (million USD) for year 3, industry coal. Is that possible?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "production",
   "scope": {
    "year": 3,
    "industry": "coal"
   },
   "sense": ">=",
   "value": 740,
   "name": "floor_production"
  }
 ],
 "version": "0.1",
 "base_model": "economic_planning"
}
```

**Result:** infeasible; conflicting constraints: balance_1_coal, balance_1_steel, balance_1_transport, balance_2_coal, balance_2_steel, balance_2_transport, balance_3_transport, capacity_3_coal

### 62. `economic_planning-infeasible_request-000-0009`

*economic_planning · infeasible_request · template `i_floor` · medium*

**Question:** What if we must reach 4200 output produced (million USD) for year 5?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "production",
   "scope": {
    "year": 5
   },
   "sense": ">=",
   "value": 4200,
   "name": "floor_production"
  }
 ],
 "version": "0.1",
 "base_model": "economic_planning"
}
```

**Result:** infeasible; conflicting constraints: balance_1_coal, balance_1_steel, balance_1_transport, balance_2_coal, balance_2_steel, balance_2_transport, balance_3_coal, balance_3_steel, balance_3_transport, balance_4_coal, balance_4_steel, balance_4_transport

### 63. `economic_planning-logical_rule-000-0003`

*economic_planning · logical_rule · template `l_none_or_batch` · medium*

**Question:** Minimum batch: if the total capacity built (million USD/year) for year 3, industry coal is above zero, it must be at least 213.

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "extra_capacity",
     "scope": {
      "year": 3,
      "industry": "coal"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "extra_capacity",
     "scope": {
      "year": 3,
      "industry": "coal"
     },
     "sense": ">=",
     "value": 213
    }
   ],
   "name": "batch_extra_capacity"
  }
 ],
 "version": "0.1",
 "base_model": "economic_planning"
}
```

**Result:** objective 1,902 → 1,850; employment 1,850, production_employment 1,598, capacity_building_employment 252.9, total_production 3,636, capacity_built 632.3

### 64. `economic_planning-new_limit-000-0010`

*economic_planning · new_limit · template `g_floor_measure_scope` · medium*

**Question:** Add a requirement: the output produced (million USD), summed over everything with industry = transport, must be at least 1110.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "production",
   "scope": {
    "industry": "transport"
   },
   "sense": ">=",
   "value": 1110,
   "name": "floor_production_transport"
  }
 ],
 "version": "0.1",
 "base_model": "economic_planning"
}
```

**Result:** objective 1,902 → 1,895; employment 1,895, production_employment 1,637, capacity_building_employment 258.4, total_production 3,742, capacity_built 646.1

### 65. `economic_planning-relative_rule-000-0009`

*economic_planning · relative_rule · template `combo` · hard*

**Question:** What if the output produced (million USD) for year 5 must be at most 25% of the output produced (million USD) for year 3, and in addition the total capacity built (million USD/year) must be at least 50% of the total output produced (million USD)?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "production",
   "scope": {
    "year": 5
   },
   "sense": "<=",
   "relative_to": {
    "measure": "production",
    "scope": {
     "year": 3
    }
   },
   "factor": 0.25,
   "name": "rel_production_5_vs_3"
  },
  {
   "measure": "extra_capacity",
   "scope": {},
   "sense": ">=",
   "relative_to": {
    "measure": "production",
    "scope": {}
   },
   "factor": 0.5,
   "name": "rel_extra_capacity_vs_production"
  }
 ],
 "version": "0.1",
 "base_model": "economic_planning"
}
```

**Result:** objective 1,902 → 1,337; employment 1,337, production_employment 843.8, capacity_building_employment 493.4, total_production 2,103, capacity_built 1,234

### 66. `economic_planning-relative_rule-000-0015`

*economic_planning · relative_rule · template `r_two_values` · medium*

**Question:** New policy: the output produced (million USD) for industry steel must be at least 1.25 times the output produced (million USD) for industry transport.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "production",
   "scope": {
    "industry": "steel"
   },
   "sense": ">=",
   "relative_to": {
    "measure": "production",
    "scope": {
     "industry": "transport"
    }
   },
   "factor": 1.25,
   "name": "rel_production_steel_vs_transport"
  }
 ],
 "version": "0.1",
 "base_model": "economic_planning"
}
```

**Result:** objective 1,902 → 1,901; employment 1,901, production_employment 1,639, capacity_building_employment 262.2, total_production 3,733, capacity_built 655.4

### 67. `factory_planning-chained_scenario-000-0001`

*factory_planning · chained_scenario · template `c_undo` · hard*

**Earlier question:** What if we retire one vertical drill?

```json
{"version": "0.1", "base_model": "factory_planning", "data_changes": [{"op": "shift", "table": "machines", "column": "installed", "where": {"machine": "vertDrill"}, "delta": -1}]}
```

**Question:** Drop the earlier change; consider only this: What if we never make more than 300 units of Prod4 in any single month?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "make",
   "scope": {
    "product": "Prod4",
    "month": "Jan"
   },
   "sense": "<=",
   "value": 300,
   "name": "cap_Prod4_Jan"
  },
  {
   "measure": "make",
   "scope": {
    "product": "Prod4",
    "month": "Feb"
   },
   "sense": "<=",
   "value": 300,
   "name": "cap_Prod4_Feb"
  },
  {
   "measure": "make",
   "scope": {
    "product": "Prod4",
    "month": "Mar"
   },
   "sense": "<=",
   "value": 300,
   "name": "cap_Prod4_Mar"
  },
  {
   "measure": "make",
   "scope": {
    "product": "Prod4",
    "month": "Apr"
   },
   "sense": "<=",
   "value": 300,
   "name": "cap_Prod4_Apr"
  },
  {
   "measure": "make",
   "scope": {
    "product": "Prod4",
    "month": "May"
   },
   "sense": "<=",
   "value": 300,
   "name": "cap_Prod4_May"
  },
  {
   "measure": "make",
   "scope": {
    "product": "Prod4",
    "month": "Jun"
   },
   "sense": "<=",
   "value": 300,
   "name": "cap_Prod4_Jun"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning"
}
```

**Result:** objective 9.372e+04 → 9.319e+04; profit 9.319e+04, sales_contribution 9.388e+04, holding_cost 691.2

### 68. `factory_planning-chained_scenario-000-0015`

*factory_planning · chained_scenario · template `c_add` · medium*

**Earlier question:** Suppose the market for Prod2 grows by 50% in June.

```json
{"version": "0.1", "base_model": "factory_planning", "data_changes": [{"op": "scale", "table": "max_sales", "column": "max_sales", "where": {"product": "Prod2", "month": "Jun"}, "factor": 1.5}]}
```

**Question:** Keep that change. In addition: What if Prod5 and Prod1 together may not exceed 600 units of production in February?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "max_sales",
   "column": "max_sales",
   "where": {
    "product": "Prod2",
    "month": "Jun"
   },
   "factor": 1.5
  }
 ],
 "rules": [
  {
   "measure": "make",
   "scope": {
    "product": [
     "Prod5",
     "Prod1"
    ],
    "month": "Feb"
   },
   "sense": "<=",
   "value": 600,
   "name": "cap_Prod5_Prod1_Feb"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning"
}
```

**Result:** objective 9.372e+04 → 9.052e+04; profit 9.052e+04, sales_contribution 9.11e+04, holding_cost 575

### 69. `factory_planning-data_change-000-0013`

*factory_planning · data_change · template `install` · easy*

**Question:** What if we install 1 more grinder?

**Gold scenario:**

```json
{
 "version": "0.1",
 "base_model": "factory_planning",
 "data_changes": [
  {
   "op": "shift",
   "table": "machines",
   "column": "installed",
   "where": {
    "machine": "grinder"
   },
   "delta": 1
  }
 ]
}
```

**Result:** objective 9.372e+04 → 9.468e+04; profit 9.468e+04, sales_contribution 9.525e+04, holding_cost 566.2

### 70. `factory_planning-data_change-000-0027`

*factory_planning · data_change · template `demand_set` · easy*

**Question:** Set the market limit for Prod1 sales in January to 600.

**Gold scenario:**

```json
{
 "version": "0.1",
 "base_model": "factory_planning",
 "data_changes": [
  {
   "op": "set",
   "table": "max_sales",
   "column": "max_sales",
   "where": {
    "product": "Prod1",
    "month": "Jan"
   },
   "value": 600
  }
 ]
}
```

**Result:** objective 9.372e+04 → 9.429e+04; profit 9.429e+04, sales_contribution 9.485e+04, holding_cost 566.2

### 71. `factory_planning-data_change-000-0045`

*factory_planning · data_change · template `margin_set` · easy*

**Question:** What if the profit contribution of Prod1 becomes 5 per unit?

**Gold scenario:**

```json
{
 "version": "0.1",
 "base_model": "factory_planning",
 "data_changes": [
  {
   "op": "set",
   "table": "products",
   "column": "profit_per_unit",
   "where": {
    "product": "Prod1"
   },
   "value": 5
  }
 ]
}
```

**Result:** objective 9.372e+04 → 8.422e+04; profit 8.422e+04, sales_contribution 8.478e+04, holding_cost 566.2

### 72. `factory_planning-data_change-000-0055`

*factory_planning · data_change · template `demand_scale` · medium*

**Question:** What if demand for Prod1 is 10% higher in January, February and March?

**Gold scenario:**

```json
{
 "version": "0.1",
 "base_model": "factory_planning",
 "data_changes": [
  {
   "op": "scale",
   "table": "max_sales",
   "column": "max_sales",
   "where": {
    "product": "Prod1",
    "month": [
     "Jan",
     "Feb",
     "Mar"
    ]
   },
   "factor": 1.1
  }
 ]
}
```

**Result:** objective 9.372e+04 → 9.459e+04; profit 9.459e+04, sales_contribution 9.517e+04, holding_cost 573.8

### 73. `factory_planning-infeasible_request-000-0003`

*factory_planning · infeasible_request · template `i_two_floors` · hard*

**Question:** Two requests arrive together: at least 2550 units made for month Apr, and at least 600 units made for month Mar. Can we do both?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "make",
   "scope": {
    "month": "Apr"
   },
   "sense": ">=",
   "value": 2550,
   "name": "floor_make_a"
  },
  {
   "measure": "make",
   "scope": {
    "month": "Mar"
   },
   "sense": ">=",
   "value": 600,
   "name": "floor_make_b"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning"
}
```

**Result:** infeasible; conflicting constraints: balance_Apr_Prod1, balance_Apr_Prod2, balance_Apr_Prod3, balance_Apr_Prod4, balance_Apr_Prod5, balance_Apr_Prod6, balance_Apr_Prod7

### 74. `factory_planning-new_limit-000-0007`

*factory_planning · new_limit · template `cap_two_products_month` · medium*

**Question:** In May, combined output of Prod2 and Prod6 is limited to 300 units.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "make",
   "scope": {
    "product": [
     "Prod2",
     "Prod6"
    ],
    "month": "May"
   },
   "sense": "<=",
   "value": 300,
   "name": "cap_Prod2_Prod6_May"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning"
}
```

**Result:** objective 9.372e+04 → 9.367e+04; profit 9.367e+04, sales_contribution 9.428e+04, holding_cost 616.2

### 75. `factory_planning-relative_rule-000-0004`

*factory_planning · relative_rule · template `combo` · hard*

**Question:** Two relative limits at once: product Prod5 must account for at least 75% of all units made; and we keep the total units sold at or below 2 times the total units in stock.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "make",
   "scope": {
    "product": "Prod5"
   },
   "sense": ">=",
   "relative_to": {
    "measure": "make",
    "scope": {}
   },
   "factor": 0.75,
   "name": "share_make_Prod5"
  },
  {
   "measure": "sell",
   "scope": {},
   "sense": "<=",
   "relative_to": {
    "measure": "store",
    "scope": {}
   },
   "factor": 2.0,
   "name": "rel_sell_vs_store"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning"
}
```

**Result:** objective 9.372e+04 → 3.294e+04; profit 3.294e+04, sales_contribution 3.372e+04, holding_cost 779.2

### 76. `factory_planning-relative_rule-000-0008`

*factory_planning · relative_rule · template `r_two_measures` · medium*

**Question:** What if the total units made may be at most 25% of the total units in stock?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "make",
   "scope": {},
   "sense": "<=",
   "relative_to": {
    "measure": "store",
    "scope": {}
   },
   "factor": 0.25,
   "name": "rel_make_vs_store"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning"
}
```

**Result:** objective 9.372e+04 → 3,512; profit 3,512, sales_contribution 5,438, holding_cost 1,925

### 77. `factory_planning-relax_remove-000-0004`

*factory_planning · relax_remove · template `x_full` · easy*

**Question:** What if the machine-hours limit did not apply?

**Gold scenario:**

```json
{
 "relax": [
  {
   "constraint": "capacity"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning"
}
```

**Result:** objective 9.372e+04 → 1.165e+05; profit 1.165e+05, sales_contribution 1.166e+05, holding_cost 175

### 78. `factory_planning-under_specified-000-0002`

*factory_planning · under_specified · template `ask_retire` · medium*

**Question:** Suppose the number of machines installed for machine type horiDrill moves. What does that do?

**Planner's answer when asked:** One of the 3 horizontal drills is scrapped for the whole horizon.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "shift",
   "table": "machines",
   "column": "installed",
   "where": {
    "machine": "horiDrill"
   },
   "delta": -1
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning"
}
```

**Result:** objective 9.372e+04 → 8.578e+04; profit 8.578e+04, sales_contribution 8.63e+04, holding_cost 525

### 79. `factory_planning_2-data_change-000-0015`

*factory_planning_2 · data_change · template `g_param` · easy*

**Question:** What if the storage limit is set to 200?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set_param",
   "name": "max_inventory",
   "value": 200
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** objective 1.089e+05 → 1.125e+05; profit 1.125e+05, sales_contribution 1.132e+05, holding_cost 725

### 80. `factory_planning_2-infeasible_request-000-0015`

*factory_planning_2 · infeasible_request · template `i_floor` · medium*

**Question:** Management wants at least 750 units made for month Feb, product Prod7. Is that possible?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "make",
   "scope": {
    "month": "Feb",
    "product": "Prod7"
   },
   "sense": ">=",
   "value": 750,
   "name": "floor_make"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** infeasible; conflicting constraints: balance_Feb_Prod7

### 81. `factory_planning_2-logical_rule-000-0000`

*factory_planning_2 · logical_rule · template `l_if_then` · hard*

**Question:** Suppose that if the units in stock for product Prod2 is above zero, the total units in stock for product Prod1 must be at least 300.

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "store",
     "scope": {
      "product": "Prod2"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "store",
     "scope": {
      "product": "Prod1"
     },
     "sense": ">=",
     "value": 300
    }
   ],
   "name": "if_store_then_store"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** objective 1.089e+05 → 1.088e+05; profit 1.088e+05, sales_contribution 1.093e+05, holding_cost 550

### 82. `factory_planning_2-logical_rule-000-0019`

*factory_planning_2 · logical_rule · template `l_at_most_k` · hard*

**Question:** What if at most 3 of month Feb, Mar, Jan and Apr may have a non-zero units sold?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "sell",
     "scope": {
      "month": "Feb"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "sell",
     "scope": {
      "month": "Mar"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "sell",
     "scope": {
      "month": "Jan"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "sell",
     "scope": {
      "month": "Apr"
     },
     "sense": "<=",
     "value": 0
    }
   ],
   "name": "at_most_3_sell"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** objective 1.089e+05 → 1.05e+05; profit 1.05e+05, sales_contribution 1.051e+05, holding_cost 175

### 83. `factory_planning_2-new_limit-000-0001`

*factory_planning_2 · new_limit · template `g_cap_measure_scope` · medium*

**Question:** What if the total units sold for product Prod1 may not exceed 1000?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "sell",
   "scope": {
    "product": "Prod1"
   },
   "sense": "<=",
   "value": 1000,
   "name": "cap_sell_Prod1"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** objective 1.089e+05 → 9.89e+04; profit 9.89e+04, sales_contribution 9.933e+04, holding_cost 425

### 84. `factory_planning_2-new_limit-000-0006`

*factory_planning_2 · new_limit · template `g_cap_measure_scope` · medium*

**Question:** Add a limit: the units made, summed over everything with product = Prod5, must stay at or below 2000.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "make",
   "scope": {
    "product": "Prod5"
   },
   "sense": "<=",
   "value": 2000,
   "name": "cap_make_Prod5"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** objective 1.089e+05 → 9.376e+04; profit 9.376e+04, sales_contribution 9.408e+04, holding_cost 325

### 85. `factory_planning_2-objective_change-001-0003`

*factory_planning_2 · objective_change · template `o_then_scoped` · medium*

**Question:** Keep profit at its maximum, then minimise the number of machines down for maintenance for month Jun.

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "max",
   "measure": "original"
  },
  {
   "sense": "min",
   "measure": "repair",
   "scope": {
    "month": "Jun"
   }
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** objective 1.089e+05 → 0; profit 1.089e+05, sales_contribution 1.093e+05, holding_cost 475

### 86. `factory_planning_2-relative_rule-000-0002`

*factory_planning_2 · relative_rule · template `r_two_measures` · medium*

**Question:** What if the total units made must be at least 2 times the total units sold?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "make",
   "scope": {},
   "sense": ">=",
   "relative_to": {
    "measure": "sell",
    "scope": {}
   },
   "factor": 2.0,
   "name": "rel_make_vs_sell"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** objective 1.089e+05 → 3,675; profit 3,675, sales_contribution 3,850, holding_cost 175

### 87. `factory_planning_2-under_specified-000-0008`

*factory_planning_2 · under_specified · template `ask_g_cap_measure_total` · medium*

**Question:** There is going to be an upper limit on units sold. How does the plan change?

**Planner's answer when asked:** The total units sold, summed over everything, may not exceed 6450.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "sell",
   "scope": {},
   "sense": "<=",
   "value": 6450,
   "name": "cap_sell_total"
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** objective 1.089e+05 → 6.758e+04; profit 6.758e+04, sales_contribution 6.785e+04, holding_cost 275

### 88. `factory_planning_2-under_specified-000-0011`

*factory_planning_2 · under_specified · template `ask_g_scale_all_rows` · medium*

**Question:** Suppose the market limit shifts for every row of the market limits table.

**Planner's answer when asked:** The market limit is 25% lower for every row of the market limits table.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "max_sales",
   "column": "max_sales",
   "factor": 0.75
  }
 ],
 "version": "0.1",
 "base_model": "factory_planning_2"
}
```

**Result:** objective 1.089e+05 → 8.251e+04; profit 8.251e+04, sales_contribution 8.297e+04, holding_cost 462.5

### 89. `fantasy_basketball-chained_scenario-000-0000`

*fantasy_basketball · chained_scenario · template `c_add` · medium*

**Earlier question:** Every player salary in the players table falls by 10%. Effect?

```json
{"version": "0.1", "base_model": "fantasy_basketball", "data_changes": [{"op": "scale", "table": "players", "column": "salary", "factor": 0.9}]}
```

**Question:** Keep that change. In addition: What if the salary cap is set to 60000?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "players",
   "column": "salary",
   "factor": 0.9
  },
  {
   "op": "set_param",
   "name": "salary_cap",
   "value": 60000
  }
 ],
 "version": "0.1",
 "base_model": "fantasy_basketball"
}
```

**Result:** objective 171.9 → 226.7; total_predicted_points 226.7, total_salary 4.158e+04, salary_cap_left 1.842e+04, players_selected 5

### 90. `fantasy_basketball-chained_scenario-000-0002`

*fantasy_basketball · chained_scenario · template `c_undo` · hard*

**Earlier question:** Assume the players required at the position of position C is now 0.

```json
{"version": "0.1", "base_model": "fantasy_basketball", "data_changes": [{"op": "set", "table": "positions", "column": "required", "where": {"position": "C"}, "value": 0}]}
```

**Question:** Forget that change. Instead: What if the predicted fantasy points for player Russell Westbrook becomes 66?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "players",
   "column": "predicted_points",
   "where": {
    "player": "Russell Westbrook"
   },
   "value": 66
  }
 ],
 "version": "0.1",
 "base_model": "fantasy_basketball"
}
```

**Result:** objective 171.9 → 177.5; total_predicted_points 177.5, total_salary 2.99e+04, salary_cap_left 100, players_selected 5

### 91. `fantasy_basketball-chained_scenario-000-0003`

*fantasy_basketball · chained_scenario · template `c_add` · medium*

**Earlier question:** The salary cap changes by a factor of 1.25.

```json
{"version": "0.1", "base_model": "fantasy_basketball", "data_changes": [{"op": "scale_param", "name": "salary_cap", "factor": 1.25}]}
```

**Question:** Keep that change. In addition: What if the player salary is 25% higher for every row of the players table?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale_param",
   "name": "salary_cap",
   "factor": 1.25
  },
  {
   "op": "scale",
   "table": "players",
   "column": "salary",
   "factor": 1.25
  }
 ],
 "version": "0.1",
 "base_model": "fantasy_basketball"
}
```

**Result:** objective 171.9 → 171.9; total_predicted_points 171.9, total_salary 3.712e+04, salary_cap_left 375, players_selected 5

### 92. `fantasy_basketball-data_change-000-0009`

*fantasy_basketball · data_change · template `g_param` · easy*

**Question:** The salary cap changes by a factor of 1.25.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale_param",
   "name": "salary_cap",
   "factor": 1.25
  }
 ],
 "version": "0.1",
 "base_model": "fantasy_basketball"
}
```

**Result:** objective 171.9 → 199.4; total_predicted_points 199.4, total_salary 3.74e+04, salary_cap_left 100, players_selected 5

### 93. `fantasy_basketball-fixed_decision-000-0019`

*fantasy_basketball · fixed_decision · template `f_force_one` · medium*

**Question:** What if player Russell Westbrook is forced (the number of players picked there is fixed at 1)?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "pick",
   "scope": {
    "player": "Russell Westbrook"
   },
   "value": 1
  }
 ],
 "version": "0.1",
 "base_model": "fantasy_basketball"
}
```

**Result:** objective 171.9 → 155.5; total_predicted_points 155.5, total_salary 2.99e+04, salary_cap_left 100, players_selected 5

### 94. `fantasy_basketball-under_specified-000-0007`

*fantasy_basketball · under_specified · template `ask_g_scale_all_rows` · medium*

**Question:** What if the player salary changes across the board?

**Planner's answer when asked:** The player salary is 25% lower for every row of the players table.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "players",
   "column": "salary",
   "factor": 0.75
  }
 ],
 "version": "0.1",
 "base_model": "fantasy_basketball"
}
```

**Result:** objective 171.9 → 206.3; total_predicted_points 206.3, total_salary 3e+04, salary_cap_left 0, players_selected 5

### 95. `fantasy_basketball-under_specified-000-0014`

*fantasy_basketball · under_specified · template `ask_g_param` · medium*

**Question:** We may have to revisit the salary cap. Effect?

**Planner's answer when asked:** The salary cap changes by a factor of 1.25.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale_param",
   "name": "salary_cap",
   "factor": 1.25
  }
 ],
 "version": "0.1",
 "base_model": "fantasy_basketball"
}
```

**Result:** objective 171.9 → 199.4; total_predicted_points 199.4, total_salary 3.74e+04, salary_cap_left 100, players_selected 5

### 96. `farm_planning-chained_scenario-000-0002`

*farm_planning · chained_scenario · template `c_revise` · hard*

**Earlier question:** What if the total heifer calves raised, summed over everything, may not exceed 17?

```json
{"version": "0.1", "base_model": "farm_planning", "rules": [{"measure": "raise_heifers", "scope": {}, "sense": "<=", "value": 17, "name": "cap_raise_heifers_total"}]}
```

**Question:** Correction: make that limit 19, not 17.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "raise_heifers",
   "scope": {},
   "sense": "<=",
   "value": 19,
   "name": "cap_raise_heifers_total"
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.212e+05; profit 1.212e+05, final_dairy_cows 78.92, extra_housing_places 0, overtime_hours 0

### 97. `farm_planning-chained_scenario-000-0012`

*farm_planning · chained_scenario · template `c_add` · medium*

**Earlier question:** Assume the sugar beet eaten per dairy cow per year (tons) becomes 1.4.

```json
{"version": "0.1", "base_model": "farm_planning", "data_changes": [{"op": "set_param", "name": "beet_per_cow", "value": 1.4}]}
```

**Question:** Keep that change. In addition: What if the grain-suitable acres for land group Group1 becomes 40?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set_param",
   "name": "beet_per_cow",
   "value": 1.4
  },
  {
   "op": "set",
   "table": "land_groups",
   "column": "area",
   "where": {
    "land_group": "Group1"
   },
   "value": 40
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.023e+05; profit 1.023e+05, final_dairy_cows 62.83, extra_housing_places 0, overtime_hours 0

### 98. `farm_planning-chained_scenario-000-0018`

*farm_planning · chained_scenario · template `c_add` · medium*

**Earlier question:** Assume land group Group1 is no longer part of the problem. What does the plan look like without it?

```json
{"version": "0.1", "base_model": "farm_planning", "data_changes": [{"op": "remove", "table": "land_groups", "where": {"land_group": "Group1"}}]}
```

**Question:** On top of that: What if the total tons of grain bought for year Year4 must be at least 60?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "remove",
   "table": "land_groups",
   "where": {
    "land_group": "Group1"
   }
  }
 ],
 "rules": [
  {
   "measure": "buy_grain",
   "scope": {
    "year": "Year4"
   },
   "sense": ">=",
   "value": 60,
   "name": "floor_buy_grain_Year4"
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.207e+05; profit 1.207e+05, final_dairy_cows 85.46, extra_housing_places 0, overtime_hours 0

### 99. `farm_planning-data_change-000-0004`

*farm_planning · data_change · template `g_scale_all_rows` · medium*

**Question:** What if the grain-suitable acres is 25% higher for every row of the land groups suitable for grain table?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "land_groups",
   "column": "area",
   "factor": 1.25
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.219e+05; profit 1.219e+05, final_dairy_cows 93.87, extra_housing_places 0, overtime_hours 0

### 100. `farm_planning-data_change-000-0008`

*farm_planning · data_change · template `g_scale_all_rows` · medium*

**Question:** What if the grain yield per acre is 25% higher for every row of the land groups suitable for grain table?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "land_groups",
   "column": "grain_yield",
   "factor": 1.25
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.252e+05; profit 1.252e+05, final_dairy_cows 91, extra_housing_places 0, overtime_hours 0

### 101. `farm_planning-fixed_decision-000-0014`

*farm_planning · fixed_decision · template `f_fix_zero` · easy*

**Question:** Fix the tons of grain grown for year Year1, land group Group1 at 0 and optimise the rest.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "grow_grain",
   "scope": {
    "year": "Year1",
    "land_group": "Group1"
   },
   "value": 0
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.215e+05; profit 1.215e+05, final_dairy_cows 92.46, extra_housing_places 0, overtime_hours 0

### 102. `farm_planning-infeasible_request-000-0002`

*farm_planning · infeasible_request · template `i_floor_total` · easy*

**Question:** The target is now 1170 head of cattle in total. Can the plan meet it?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "herd",
   "scope": {},
   "sense": ">=",
   "value": 1170,
   "name": "floor_total_herd"
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** infeasible; conflicting constraints: ageing_Year2_12, ageing_Year2_7, ageing_Year2_8, ageing_Year2_9, ageing_Year3_10, ageing_Year3_11, ageing_Year3_12, ageing_Year4_11, ageing_Year4_12, ageing_Year5_10, ageing_Year5_11, ageing_Year5_12, ageing_Year5_3, ageing_Year5_4, ageing_Year5_5, ageing_Year5_6, ageing_Year5_7, ageing_Year5_8, ageing_Year5_9, heifers_calve_Year2, heifers_calve_Year4, heifers_calve_Year5, initial_herd_1, initial_herd_10, initial_herd_11, initial_herd_12, initial_herd_2, initial_herd_3, initial_herd_4, initial_herd_5, initial_herd_6, initial_herd_7, initial_herd_8, initial_herd_9, land_Year2, land_Year3, land_Year4, land_Year5

### 103. `farm_planning-logical_rule-000-0001`

*farm_planning · logical_rule · template `l_none_or_batch` · medium*

**Question:** Minimum batch: if the total tons of sugar beet sold for year Year3 is above zero, it must be at least 49.

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "sell_beet",
     "scope": {
      "year": "Year3"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "sell_beet",
     "scope": {
      "year": "Year3"
     },
     "sense": ">=",
     "value": 49
    }
   ],
   "name": "batch_sell_beet"
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.215e+05; profit 1.215e+05, final_dairy_cows 92.46, extra_housing_places 0, overtime_hours 0

### 104. `farm_planning-relative_rule-000-0002`

*farm_planning · relative_rule · template `r_two_measures` · medium*

**Question:** Keep the total tons of grain bought at or below 25% of the total tons of sugar beet grown. Effect on the plan?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "buy_grain",
   "scope": {},
   "sense": "<=",
   "relative_to": {
    "measure": "grow_beet",
    "scope": {}
   },
   "factor": 0.25,
   "name": "rel_buy_grain_vs_grow_beet"
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.211e+05; profit 1.211e+05, final_dairy_cows 82.21, extra_housing_places 0, overtime_hours 0

### 105. `farm_planning-relative_rule-000-0004`

*farm_planning · relative_rule · template `r_two_values` · medium*

**Question:** What if the tons of grain grown for year Year2 must be at least 1.25 times the tons of grain grown for year Year5?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "grow_grain",
   "scope": {
    "year": "Year2"
   },
   "sense": ">=",
   "relative_to": {
    "measure": "grow_grain",
    "scope": {
     "year": "Year5"
    }
   },
   "factor": 1.25,
   "name": "rel_grow_grain_Year2_vs_Year5"
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.217e+05; profit 1.217e+05, final_dairy_cows 92.46, extra_housing_places 0, overtime_hours 0

### 106. `farm_planning-under_specified-000-0006`

*farm_planning · under_specified · template `ask_g_cap_measure_total` · medium*

**Question:** Suppose the tons of sugar beet sold gets capped.

**Planner's answer when asked:** An overall cap of 170 applies to the tons of sugar beet sold, summed over everything.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "sell_beet",
   "scope": {},
   "sense": "<=",
   "value": 170,
   "name": "cap_sell_beet_total"
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.217e+05; profit 1.217e+05, final_dairy_cows 93.68, extra_housing_places 0, overtime_hours 0

### 107. `farm_planning-under_specified-000-0009`

*farm_planning · under_specified · template `ask_g_scale_column` · medium*

**Question:** Suppose the grain yield per acre for land group Group1 moves. What does that do?

**Planner's answer when asked:** The grain yield per acre for land group Group1 is 10% lower.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "land_groups",
   "column": "grain_yield",
   "where": {
    "land_group": "Group1"
   },
   "factor": 0.9
  }
 ],
 "version": "0.1",
 "base_model": "farm_planning"
}
```

**Result:** objective 1.217e+05 → 1.209e+05; profit 1.209e+05, final_dairy_cows 85.46, extra_housing_places 0, overtime_hours 0

### 108. `food_manufacture-chained_scenario-000-0017`

*food_manufacture · chained_scenario · template `c_add` · medium*

**Earlier question:** Assume the oil hardness of oil VEG1 is now 17.6.

```json
{"version": "0.1", "base_model": "food_manufacture", "data_changes": [{"op": "set", "table": "oils", "column": "hardness", "where": {"oil": "VEG1"}, "value": 17.6}]}
```

**Question:** On top of that: An overall cap of 1350 applies to the tons of oil bought, summed over everything.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "oils",
   "column": "hardness",
   "where": {
    "oil": "VEG1"
   },
   "value": 17.6
  }
 ],
 "rules": [
  {
   "measure": "buy",
   "scope": {},
   "sense": "<=",
   "value": 1350,
   "name": "cap_buy_total"
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 3.132e+04; profit 3.132e+04, revenue 2.025e+05, food_produced 1,350

### 109. `food_manufacture-data_change-001-0002`

*food_manufacture · data_change · template `combo` · hard*

**Question:** Suppose every purchase price in the raw oil purchase prices table falls by 20%. On top of that, the oil hardness of oil VEG1 is now 13.2.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "purchase_prices",
   "column": "price",
   "factor": 0.8
  },
  {
   "op": "set",
   "table": "oils",
   "column": "hardness",
   "where": {
    "oil": "VEG1"
   },
   "value": 13.2
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 1.502e+05; profit 1.502e+05, revenue 4.05e+05, food_produced 2,700

### 110. `food_manufacture-data_change-001-0011`

*food_manufacture · data_change · template `g_scale_all_rows` · medium*

**Question:** What if the purchase price is 25% lower for every row of the raw oil purchase prices table?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "purchase_prices",
   "column": "price",
   "factor": 0.75
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 1.709e+05; profit 1.709e+05, revenue 4.05e+05, food_produced 2,700

### 111. `food_manufacture-fixed_decision-000-0001`

*food_manufacture · fixed_decision · template `combo` · hard*

**Question:** Two commitments at once: month Jun gets 220 tons of food produced, no more and no less; and the tons of oil refined for oil VEG1 is fixed at 110 for every month. Optimise the rest.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "produce",
   "scope": {
    "month": "Jun"
   },
   "value": 220
  },
  {
   "measure": "consume",
   "scope": {
    "oil": "VEG1"
   },
   "value": 110
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 9.03e+04; profit 9.03e+04, revenue 3.705e+05, food_produced 2,470

### 112. `food_manufacture-fixed_decision-000-0003`

*food_manufacture · fixed_decision · template `f_fix_scope` · hard*

**Question:** What if the tons of oil in storage for month Mar is fixed at 280 for every oil?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "store",
   "scope": {
    "month": "Mar"
   },
   "value": 280
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 9.918e+04; profit 9.918e+04, revenue 4.05e+05, food_produced 2,700

### 113. `food_manufacture-infeasible_request-000-0013`

*food_manufacture · infeasible_request · template `i_commit` · medium*

**Question:** We have promised 7500 tons of oil bought for month Jun, oil OIL2, no more and no less. Re-plan.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "buy",
   "scope": {
    "month": "Jun",
    "oil": "OIL2"
   },
   "value": 7500
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** infeasible; conflicting constraints: balance_Jun_OIL2, refining_nonveg_Jun

### 114. `food_manufacture-logical_rule-000-0016`

*food_manufacture · logical_rule · template `l_never_both` · medium*

**Question:** New rule: month Jun and month Apr cannot both have a non-zero tons of food produced. Re-plan.

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "produce",
     "scope": {
      "month": "Jun"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "produce",
     "scope": {
      "month": "Apr"
     },
     "sense": "<=",
     "value": 0
    }
   ],
   "name": "never_both_produce"
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 8.334e+04; profit 8.334e+04, revenue 3.375e+05, food_produced 2,250

### 115. `food_manufacture-new_limit-000-0011`

*food_manufacture · new_limit · template `g_floor_measure_scope` · medium*

**Question:** Add a requirement: the tons of oil bought, summed over everything with month = Feb, must be at least 940.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "buy",
   "scope": {
    "month": "Feb"
   },
   "sense": ">=",
   "value": 940,
   "name": "floor_buy_Feb"
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 1.021e+05; profit 1.021e+05, revenue 4.05e+05, food_produced 2,700

### 116. `food_manufacture-relative_rule-001-0001`

*food_manufacture · relative_rule · template `r_two_measures` · medium*

**Question:** What if the total tons of oil bought may be at most 25% of the total tons of oil refined?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "buy",
   "scope": {},
   "sense": "<=",
   "relative_to": {
    "measure": "consume",
    "scope": {}
   },
   "factor": 0.25,
   "name": "rel_buy_vs_consume"
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → -7.5e+04; profit -7.5e+04, revenue 0, food_produced 0

### 117. `food_manufacture-relative_rule-001-0010`

*food_manufacture · relative_rule · template `r_share_of_total` · medium*

**Question:** What if month May must account for at least 20% of all tons of oil in storage?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "store",
   "scope": {
    "month": "May"
   },
   "sense": ">=",
   "relative_to": {
    "measure": "store",
    "scope": {}
   },
   "factor": 0.2,
   "name": "share_store_May"
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 9.115e+04; profit 9.115e+04, revenue 4.05e+05, food_produced 2,700

### 118. `food_manufacture-relative_rule-001-0016`

*food_manufacture · relative_rule · template `r_share_of_total` · medium*

**Question:** What if month Jun must account for at least 75% of all tons of oil bought?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "buy",
   "scope": {
    "month": "Jun"
   },
   "sense": ">=",
   "relative_to": {
    "measure": "buy",
    "scope": {}
   },
   "factor": 0.75,
   "name": "share_buy_Jun"
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 1.06e+05; profit 1.06e+05, revenue 4.05e+05, food_produced 2,700

### 119. `food_manufacture-under_specified-000-0019`

*food_manufacture · under_specified · template `ask_g_set_column` · medium*

**Question:** What if the purchase price for month Apr, oil VEG2 changes?

**Planner's answer when asked:** The purchase price for month Apr, oil VEG2 becomes 60.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "purchase_prices",
   "column": "price",
   "where": {
    "month": "Apr",
    "oil": "VEG2"
   },
   "value": 60
  }
 ],
 "version": "0.1",
 "base_model": "food_manufacture"
}
```

**Result:** objective 1.078e+05 → 1.352e+05; profit 1.352e+05, revenue 4.05e+05, food_produced 2,700

### 120. `food_supply-data_change-000-0015`

*food_supply · data_change · template `g_scale_all_rows` · medium*

**Question:** Every minimum daily intake per person in the nutrient requirements table rises by 10%. Effect?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "nutrients",
   "column": "min_per_person",
   "factor": 1.1
  }
 ],
 "version": "0.1",
 "base_model": "food_supply"
}
```

**Result:** objective 4.008e+08 → 4.409e+08; total_cost 4.409e+08, procurement_cost 3.899e+08, transport_cost 5.099e+07, food_bought 3.568e+05

### 121. `food_supply-fixed_decision-000-0015`

*food_supply · fixed_decision · template `f_fix_scope` · hard*

**Question:** What if the food bought (units of 100 g a day) for food Oil is fixed at 2450 for every supplier?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "purchase",
   "scope": {
    "food": "Oil"
   },
   "value": 2450
  }
 ],
 "version": "0.1",
 "base_model": "food_supply"
}
```

**Result:** objective 4.008e+08 → 6.437e+08; total_cost 6.437e+08, procurement_cost 5.418e+08, transport_cost 1.019e+08, food_bought 3.728e+05

### 122. `food_supply-infeasible_request-000-0008`

*food_supply · infeasible_request · template `i_floor` · medium*

**Question:** Management wants at least 200550 food bought (units of 100 g a day) for food Oil, supplier Hassakeh. Is that possible?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "purchase",
   "scope": {
    "food": "Oil",
    "supplier": "Hassakeh"
   },
   "sense": ">=",
   "value": 200550,
   "name": "floor_purchase"
  }
 ],
 "version": "0.1",
 "base_model": "food_supply"
}
```

**Result:** infeasible; conflicting constraints: balance_Oil_Aleppo, balance_Oil_Ar_Raqqa, balance_Oil_As_Suweida, balance_Oil_Damascus, balance_Oil_Daraa, balance_Oil_Dayr_Az_Zor, balance_Oil_Hama, balance_Oil_Hassakeh, balance_Oil_Homs, balance_Oil_Idleb, balance_Oil_Jubb_al_Jarrah, balance_Oil_Qamishli, nutrition_Fat_g_Ar_Raqqa, nutrition_Fat_g_Daraa, nutrition_Fat_g_Dayr_Az_Zor, nutrition_Fat_g_Hassakeh, nutrition_Fat_g_Idleb, nutrition_Fat_g_Jubb_al_Jarrah, nutrition_Fat_g_Qamishli

### 123. `food_supply-logical_rule-000-0006`

*food_supply · logical_rule · template `l_if_then` · hard*

**Question:** Suppose that if the ration per person (units of 100 g a day) for food Oil, camp Idleb is above zero, the total food bought (units of 100 g a day) for supplier Amman must be at least 12050.

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "ration",
     "scope": {
      "food": "Oil",
      "camp": "Idleb"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "purchase",
     "scope": {
      "supplier": "Amman"
     },
     "sense": ">=",
     "value": 12050
    }
   ],
   "name": "if_ration_then_purchase"
  }
 ],
 "version": "0.1",
 "base_model": "food_supply"
}
```

**Result:** objective 4.008e+08 → 4.012e+08; total_cost 4.012e+08, procurement_cost 3.54e+08, transport_cost 4.716e+07, food_bought 3.244e+05

### 124. `food_supply-new_limit-000-0004`

*food_supply · new_limit · template `g_floor_measure_scope` · medium*

**Question:** What if the total ration per person (units of 100 g a day) for food Oil must be at least 6.7?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "ration",
   "scope": {
    "food": "Oil"
   },
   "sense": ">=",
   "value": 6.7,
   "name": "floor_ration_Oil"
  }
 ],
 "version": "0.1",
 "base_model": "food_supply"
}
```

**Result:** objective 4.008e+08 → 4.078e+08; total_cost 4.078e+08, procurement_cost 3.603e+08, transport_cost 4.754e+07, food_bought 3.222e+05

### 125. `food_supply-new_limit-000-0010`

*food_supply · new_limit · template `g_floor_measure_scope` · medium*

**Question:** Add a requirement: the food shipped (units of 100 g a day), summed over everything with food = Milk, must be at least 43800.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "flow",
   "scope": {
    "food": "Milk"
   },
   "sense": ">=",
   "value": 43800,
   "name": "floor_flow_Milk"
  }
 ],
 "version": "0.1",
 "base_model": "food_supply"
}
```

**Result:** objective 4.008e+08 → 4.008e+08; total_cost 4.008e+08, procurement_cost 3.492e+08, transport_cost 5.164e+07, food_bought 3.243e+05

### 126. `food_supply-relative_rule-000-0006`

*food_supply · relative_rule · template `combo` · hard*

**Question:** Two relative limits at once: the total food bought (units of 100 g a day) may be at most 75% of the total food shipped (units of 100 g a day); and the food shipped (units of 100 g a day) for origin city Amman may be at most 60% of the food shipped (units of 100 g a day) for origin city Gaziantep.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "purchase",
   "scope": {},
   "sense": "<=",
   "relative_to": {
    "measure": "flow",
    "scope": {}
   },
   "factor": 0.75,
   "name": "rel_purchase_vs_flow"
  },
  {
   "measure": "flow",
   "scope": {
    "from_city": "Amman"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "flow",
    "scope": {
     "from_city": "Gaziantep"
    }
   },
   "factor": 0.6,
   "name": "rel_flow_Amman_vs_Gaziantep"
  }
 ],
 "version": "0.1",
 "base_model": "food_supply"
}
```

**Result:** objective 4.008e+08 → 4.221e+08; total_cost 4.221e+08, procurement_cost 3.442e+08, transport_cost 7.786e+07, food_bought 3.243e+05

### 127. `food_supply-relative_rule-000-0008`

*food_supply · relative_rule · template `r_two_values` · medium*

**Question:** What if the food shipped (units of 100 g a day) for food Milk may be at most 25% of the food shipped (units of 100 g a day) for food Wheat?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "flow",
   "scope": {
    "food": "Milk"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "flow",
    "scope": {
     "food": "Wheat"
    }
   },
   "factor": 0.25,
   "name": "rel_flow_Milk_vs_Wheat"
  }
 ],
 "version": "0.1",
 "base_model": "food_supply"
}
```

**Result:** objective 4.008e+08 → 4.017e+08; total_cost 4.017e+08, procurement_cost 3.593e+08, transport_cost 4.244e+07, food_bought 3.244e+05

### 128. `food_supply-under_specified-000-0008`

*food_supply · under_specified · template `ask_g_scale_all_rows` · medium*

**Question:** What if the local price changes across the board?

**Planner's answer when asked:** The local price is 25% higher for every row of the local procurement prices table.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "local_prices",
   "column": "price",
   "factor": 1.25
  }
 ],
 "version": "0.1",
 "base_model": "food_supply"
}
```

**Result:** objective 4.008e+08 → 4.262e+08; total_cost 4.262e+08, procurement_cost 3.698e+08, transport_cost 5.638e+07, food_bought 3.244e+05

### 129. `jobshop_ft06-chained_scenario-000-0009`

*jobshop_ft06 · chained_scenario · template `c_add` · medium*

**Earlier question:** What if the total operation end time, summed over everything, may not exceed 1000?

```json
{"version": "0.1", "base_model": "jobshop_ft06", "rules": [{"measure": "end", "scope": {}, "sense": "<=", "value": 1000, "name": "cap_end_total"}]}
```

**Question:** On top of that: Suppose the processing time of job J1, routing step 2 (in the job operations (routing) table) rises by 25%.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "operations",
   "column": "duration",
   "where": {
    "job": "J1",
    "step": 2
   },
   "factor": 1.25
  }
 ],
 "rules": [
  {
   "measure": "end",
   "scope": {},
   "sense": "<=",
   "value": 1000,
   "name": "cap_end_total"
  }
 ],
 "version": "0.1",
 "base_model": "jobshop_ft06"
}
```

**Result:** objective 55 → 70; makespan 70, mean_utilisation 47.2

### 130. `jobshop_ft06-data_change-000-0004`

*jobshop_ft06 · data_change · template `combo` · hard*

**Question:** What if every job release time in the jobs table falls by 20%, and at the same time the processing time of job J0, routing step 2 is now 4.5?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "jobs",
   "column": "release_time",
   "factor": 0.8
  },
  {
   "op": "set",
   "table": "operations",
   "column": "duration",
   "where": {
    "job": "J0",
    "step": 2
   },
   "value": 4.5
  }
 ],
 "version": "0.1",
 "base_model": "jobshop_ft06"
}
```

**Result:** objective 55 → 55; makespan 55, mean_utilisation 60.15

### 131. `jobshop_ft06-data_change-000-0009`

*jobshop_ft06 · data_change · template `g_set_column` · easy*

**Question:** What if the processing time for job J1, routing step 6 becomes 8?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "operations",
   "column": "duration",
   "where": {
    "job": "J1",
    "step": 6
   },
   "value": 8
  }
 ],
 "version": "0.1",
 "base_model": "jobshop_ft06"
}
```

**Result:** objective 55 → 57; makespan 57, mean_utilisation 58.77

### 132. `jobshop_ft06-fixed_decision-000-0004`

*jobshop_ft06 · fixed_decision · template `f_fix_level` · medium*

**Question:** Management has decided: job J1, routing step 6 gets 60 operation start time, no more and no less. Re-plan everything else.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "start",
   "scope": {
    "job": "J1",
    "step": 6
   },
   "value": 60
  }
 ],
 "version": "0.1",
 "base_model": "jobshop_ft06"
}
```

**Result:** objective 55 → 64; makespan 64, mean_utilisation 51.3

### 133. `jobshop_ft06-fixed_decision-000-0006`

*jobshop_ft06 · fixed_decision · template `f_force_one` · medium*

**Question:** What if machine M1, job J2, other job J3 is forced (the number of job pairs where the job goes first on the machine there is fixed at 1)?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "goes_first",
   "scope": {
    "machine": "M1",
    "job": "J2",
    "other_job": "J3"
   },
   "value": 1
  }
 ],
 "version": "0.1",
 "base_model": "jobshop_ft06"
}
```

**Result:** objective 55 → 62; makespan 62, mean_utilisation 52.96

### 134. `jobshop_ft06-new_limit-000-0006`

*jobshop_ft06 · new_limit · template `g_floor_measure_scope` · medium*

**Question:** What if the total operation start time for routing step 5 must be at least 290?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "start",
   "scope": {
    "step": 5
   },
   "sense": ">=",
   "value": 290,
   "name": "floor_start_5"
  }
 ],
 "version": "0.1",
 "base_model": "jobshop_ft06"
}
```

**Result:** objective 55 → 62; makespan 62, mean_utilisation 52.96

### 135. `jobshop_ft06-objective_change-000-0005`

*jobshop_ft06 · objective_change · template `o_then_min` · medium*

**Question:** Keep makespan at its minimum, then minimise the total number of job pairs where the job goes first on the machine.

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "min",
   "measure": "original"
  },
  {
   "sense": "min",
   "measure": "goes_first"
  }
 ],
 "version": "0.1",
 "base_model": "jobshop_ft06"
}
```

**Result:** objective 55 → 45; makespan 55, mean_utilisation 59.7

### 136. `jobshop_ft06-objective_change-000-0017`

*jobshop_ft06 · objective_change · template `o_then_scoped` · medium*

**Question:** Keep makespan at its minimum, then maximise the operation end time for routing step 3.

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "min",
   "measure": "original"
  },
  {
   "sense": "max",
   "measure": "end",
   "scope": {
    "step": 3
   }
  }
 ],
 "version": "0.1",
 "base_model": "jobshop_ft06"
}
```

**Result:** objective 55 → 173; makespan 55, mean_utilisation 59.7

### 137. `jobshop_ft06-under_specified-000-0001`

*jobshop_ft06 · under_specified · template `ask_g_set_column` · medium*

**Question:** Suppose the processing time is different for one of the rows in the job operations (routing) table.

**Planner's answer when asked:** The processing time for job J3, routing step 2 becomes 2.5.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "operations",
   "column": "duration",
   "where": {
    "job": "J3",
    "step": 2
   },
   "value": 2.5
  }
 ],
 "version": "0.1",
 "base_model": "jobshop_ft06"
}
```

**Result:** objective 55 → 54.5; makespan 54.5, mean_utilisation 59.48

### 138. `manpower_planning-fixed_decision-000-0009`

*manpower_planning · fixed_decision · template `f_fix_zero` · easy*

**Question:** Fix the workers employed above requirement for year 2, skill level unskilled at 0 and optimise the rest.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "overmanned",
   "scope": {
    "year": 2,
    "skill": "unskilled"
   },
   "value": 0
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** objective 841.8 → 856.8; total_redundancy 856.8

### 139. `manpower_planning-infeasible_request-000-0010`

*manpower_planning · infeasible_request · template `i_floor_total` · easy*

**Question:** The target is now 2250 workers employed above requirement in total. Can the plan meet it?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "overmanned",
   "scope": {},
   "sense": ">=",
   "value": 2250,
   "name": "floor_total_overmanned"
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** infeasible; conflicting constraints: overmanning_1, overmanning_2, overmanning_3

### 140. `manpower_planning-logical_rule-000-0000`

*manpower_planning · logical_rule · template `l_if_then` · hard*

**Question:** What if a non-zero workers on short-time working for year 2, skill level unskilled requires a total workers employed above requirement of at least 220 for year 3?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "short_time",
     "scope": {
      "year": 2,
      "skill": "unskilled"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "overmanned",
     "scope": {
      "year": 3
     },
     "sense": ">=",
     "value": 220
    }
   ],
   "name": "if_short_time_then_overmanned"
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** objective 841.8 → 844.3; total_redundancy 844.3

### 141. `manpower_planning-logical_rule-000-0016`

*manpower_planning · logical_rule · template `l_none_or_batch` · medium*

**Question:** What if the total workers retrained to a higher skill level for year 3, from skill level unskilled, to skill level semi_skilled must be either zero or at least 400?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "retrain",
     "scope": {
      "year": 3,
      "from_skill": "unskilled",
      "to_skill": "semi_skilled"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "retrain",
     "scope": {
      "year": 3,
      "from_skill": "unskilled",
      "to_skill": "semi_skilled"
     },
     "sense": ">=",
     "value": 400
    }
   ],
   "name": "batch_retrain"
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** objective 841.8 → 1,046; total_redundancy 1,046

### 142. `manpower_planning-logical_rule-000-0019`

*manpower_planning · logical_rule · template `l_if_then` · hard*

**Question:** What if a non-zero workers employed above requirement for year 2, skill level unskilled requires a total workers downgraded to a lower skill level of at least 210 for year 1, from skill level skilled, to skill level semi_skilled?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "overmanned",
     "scope": {
      "year": 2,
      "skill": "unskilled"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "downgrade",
     "scope": {
      "year": 1,
      "from_skill": "skilled",
      "to_skill": "semi_skilled"
     },
     "sense": ">=",
     "value": 210
    }
   ],
   "name": "if_overmanned_then_downgrade"
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** objective 841.8 → 843.9; total_redundancy 843.9

### 143. `manpower_planning-new_limit-000-0008`

*manpower_planning · new_limit · template `g_cap_measure_total` · easy*

**Question:** What if the total workers on short-time working, summed over everything, may not exceed 240?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "short_time",
   "scope": {},
   "sense": "<=",
   "value": 240,
   "name": "cap_short_time_total"
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** objective 841.8 → 842.1; total_redundancy 842.1

### 144. `manpower_planning-objective_change-000-0016`

*manpower_planning · objective_change · template `o_then_max` · medium*

**Question:** What if, without giving up any total redundancy, we want the total workers recruited to be as high as possible?

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "min",
   "measure": "original"
  },
  {
   "sense": "max",
   "measure": "recruit"
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** objective 841.8 → 2,600; total_redundancy 841.8

### 145. `manpower_planning-relative_rule-000-0006`

*manpower_planning · relative_rule · template `r_two_values` · medium*

**Question:** What if the workers made redundant for year 1 may be at most 1.5 times the workers made redundant for year 2?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "redundant",
   "scope": {
    "year": 1
   },
   "sense": "<=",
   "relative_to": {
    "measure": "redundant",
    "scope": {
     "year": 2
    }
   },
   "factor": 1.5,
   "name": "rel_redundant_1_vs_2"
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** objective 841.8 → 854.7; total_redundancy 854.7

### 146. `manpower_planning-relax_remove-000-0005`

*manpower_planning · relax_remove · template `x_scoped` · medium*

**Question:** Suppose the limit on retraining is lifted for year 1 only. Effect on the plan?

**Gold scenario:**

```json
{
 "relax": [
  {
   "constraint": "retraining_limit",
   "scope": {
    "year": 1
   }
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** objective 841.8 → 257.5; total_redundancy 257.5

### 147. `manpower_planning-relax_remove-000-0008`

*manpower_planning · relax_remove · template `x_scoped` · medium*

**Question:** Suppose the limit on retraining is lifted for year 2 only. Effect on the plan?

**Gold scenario:**

```json
{
 "relax": [
  {
   "constraint": "retraining_limit",
   "scope": {
    "year": 2
   }
  }
 ],
 "version": "0.1",
 "base_model": "manpower_planning"
}
```

**Result:** objective 841.8 → 509; total_redundancy 509

### 148. `mining-data_change-000-0002`

*mining · data_change · template `g_scale_all_rows` · medium*

**Question:** What if the yearly royalty is 25% lower for every row of the mines table?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "mines",
   "column": "royalty",
   "factor": 0.75
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.648e+08; profit 1.648e+08, discounted_revenue 2.185e+08, discounted_royalties 5.373e+07, ore_sold_tons 2.609e+07

### 149. `mining-fixed_decision-000-0004`

*mining · fixed_decision · template `f_fix_level` · medium*

**Question:** Management has decided: year Year2 gets 3000000 tons of blended ore sold, no more and no less. Re-plan everything else.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "blend",
   "scope": {
    "year": "Year2"
   },
   "value": 3000000
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.196e+08; profit 1.196e+08, discounted_revenue 1.912e+08, discounted_royalties 7.164e+07, ore_sold_tons 2.309e+07

### 150. `mining-fixed_decision-000-0012`

*mining · fixed_decision · template `f_fix_level` · medium*

**Question:** What if the tons of blended ore sold for year Year5 is fixed at 4100000?

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "blend",
   "scope": {
    "year": "Year5"
   },
   "value": 4100000
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.375e+08; profit 1.375e+08, discounted_revenue 2.092e+08, discounted_royalties 7.164e+07, ore_sold_tons 2.472e+07

### 151. `mining-fixed_decision-000-0014`

*mining · fixed_decision · template `f_fix_zero` · easy*

**Question:** Suppose we decide against year Year1, mine Mine1: set its number of mine-years worked to 0 and re-plan.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "operate",
   "scope": {
    "year": "Year1",
    "mine": "Mine1"
   },
   "value": 0
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.344e+08; profit 1.344e+08, discounted_revenue 2.06e+08, discounted_royalties 7.164e+07, ore_sold_tons 2.484e+07

### 152. `mining-infeasible_request-000-0006`

*mining · infeasible_request · template `i_floor_total` · easy*

**Question:** Can we reach a total of at least 130458350 tons of ore extracted?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "extract",
   "scope": {},
   "sense": ">=",
   "value": 130458350,
   "name": "floor_total_extract"
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** infeasible; conflicting constraints: capacity_Year1_Mine1, capacity_Year1_Mine2, capacity_Year1_Mine3, capacity_Year1_Mine4, capacity_Year2_Mine1, capacity_Year2_Mine2, capacity_Year2_Mine3, capacity_Year2_Mine4, capacity_Year3_Mine1, capacity_Year3_Mine2, capacity_Year3_Mine3, capacity_Year3_Mine4, capacity_Year4_Mine1, capacity_Year4_Mine2, capacity_Year4_Mine3, capacity_Year4_Mine4, capacity_Year5_Mine1, capacity_Year5_Mine2, capacity_Year5_Mine3, capacity_Year5_Mine4

### 153. `mining-infeasible_request-000-0015`

*mining · infeasible_request · template `i_floor` · medium*

**Question:** Management wants at least 2600000 tons of ore extracted for year Year3, mine Mine3. Is that possible?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "extract",
   "scope": {
    "year": "Year3",
    "mine": "Mine3"
   },
   "sense": ">=",
   "value": 2600000,
   "name": "floor_extract"
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** infeasible; conflicting constraints: capacity_Year3_Mine3

### 154. `mining-infeasible_request-000-0019`

*mining · infeasible_request · template `i_two_floors` · hard*

**Question:** Two requests arrive together: at least 11500000 tons of ore extracted for year Year1, and at least 6500000 tons of ore extracted for year Year3. Can we do both?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "extract",
   "scope": {
    "year": "Year1"
   },
   "sense": ">=",
   "value": 11500000,
   "name": "floor_extract_a"
  },
  {
   "measure": "extract",
   "scope": {
    "year": "Year3"
   },
   "sense": ">=",
   "value": 6500000,
   "name": "floor_extract_b"
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** infeasible; conflicting constraints: capacity_Year1_Mine1, capacity_Year1_Mine2, capacity_Year1_Mine3, capacity_Year1_Mine4

### 155. `mining-logical_rule-000-0013`

*mining · logical_rule · template `l_none_or_batch` · medium*

**Question:** Minimum batch: if the total tons of ore extracted for year Year1, mine Mine1 is above zero, it must be at least 5000000.

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "extract",
     "scope": {
      "year": "Year1",
      "mine": "Mine1"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "extract",
     "scope": {
      "year": "Year1",
      "mine": "Mine1"
     },
     "sense": ">=",
     "value": 5000000
    }
   ],
   "name": "batch_extract"
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.344e+08; profit 1.344e+08, discounted_revenue 2.06e+08, discounted_royalties 7.164e+07, ore_sold_tons 2.484e+07

### 156. `mining-new_limit-000-0009`

*mining · new_limit · template `g_cap_measure_scope` · medium*

**Question:** What if the total tons of ore extracted for year Year2 may not exceed 5400000?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "extract",
   "scope": {
    "year": "Year2"
   },
   "sense": "<=",
   "value": 5400000,
   "name": "cap_extract_Year2"
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.414e+08; profit 1.414e+08, discounted_revenue 2.13e+08, discounted_royalties 7.164e+07, ore_sold_tons 2.549e+07

### 157. `mining-new_limit-000-0011`

*mining · new_limit · template `g_cap_measure_total` · easy*

**Question:** What if the total tons of ore extracted, summed over everything, may not exceed 23482500?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "extract",
   "scope": {},
   "sense": "<=",
   "value": 23482500,
   "name": "cap_extract_total"
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.389e+08; profit 1.389e+08, discounted_revenue 1.947e+08, discounted_royalties 5.579e+07, ore_sold_tons 2.285e+07

### 158. `mining-new_limit-000-0012`

*mining · new_limit · template `g_cap_measure_scope` · medium*

**Question:** What if the total number of mine-years kept open for year Year5 may not exceed 2?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "open",
   "scope": {
    "year": "Year5"
   },
   "sense": "<=",
   "value": 2,
   "name": "cap_open_Year5"
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.399e+08; profit 1.399e+08, discounted_revenue 2.043e+08, discounted_royalties 6.447e+07, ore_sold_tons 2.402e+07

### 159. `mining-relax_remove-000-0000`

*mining · relax_remove · template `x_scoped` · medium*

**Question:** What if the blend-quality target did not apply for year Year3?

**Gold scenario:**

```json
{
 "relax": [
  {
   "constraint": "quality",
   "scope": {
    "year": "Year3"
   }
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.82e+08; profit 1.82e+08, discounted_revenue 2.536e+08, discounted_royalties 7.164e+07, ore_sold_tons 3.034e+07

### 160. `mining-under_specified-000-0003`

*mining · under_specified · template `ask_g_add_row` · medium*

**Question:** Suppose a new mine joins the mines table.

**Planner's answer when asked:** A new mine 'new_mine' is added with yearly royalty 5000000, yearly extraction limit 2500000 and ore quality 1.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "add",
   "table": "mines",
   "rows": [
    {
     "mine": "new_mine",
     "royalty": 5000000,
     "capacity": 2500000,
     "quality": 1
    }
   ]
  }
 ],
 "version": "0.1",
 "base_model": "mining"
}
```

**Result:** objective 1.469e+08 → 1.644e+08; profit 1.644e+08, discounted_revenue 2.456e+08, discounted_royalties 8.119e+07, ore_sold_tons 2.909e+07

### 161. `multiple_knapsack-chained_scenario-000-0015`

*multiple_knapsack · chained_scenario · template `c_add` · medium*

**Earlier question:** Add one more row to the items table: item new_item, item weight 18 and item value 27. Effect on the plan?

```json
{"version": "0.1", "base_model": "multiple_knapsack", "data_changes": [{"op": "add", "table": "items", "rows": [{"item": "new_item", "weight": 18, "value": 27}]}]}
```

**Question:** On top of that: What if the item value for item item14 becomes 19?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "add",
   "table": "items",
   "rows": [
    {
     "item": "new_item",
     "weight": 18,
     "value": 27
    }
   ]
  },
  {
   "op": "set",
   "table": "items",
   "column": "value",
   "where": {
    "item": "item14"
   },
   "value": 19
  }
 ],
 "version": "0.1",
 "base_model": "multiple_knapsack"
}
```

**Result:** objective 395 → 416; packed_value 416

### 162. `multiple_knapsack-data_change-000-0016`

*multiple_knapsack · data_change · template `g_remove_row` · medium*

**Question:** Suppose bin bin2 drops out entirely (delete that bin and re-plan).

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "remove",
   "table": "bins",
   "where": {
    "bin": "bin2"
   }
  }
 ],
 "version": "0.1",
 "base_model": "multiple_knapsack"
}
```

**Result:** objective 395 → 350; packed_value 350

### 163. `multiple_knapsack-data_change-000-0017`

*multiple_knapsack · data_change · template `g_add_row` · medium*

**Question:** What if a new item 'new_item' is added with item weight 25 and item value 40?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "add",
   "table": "items",
   "rows": [
    {
     "item": "new_item",
     "weight": 25,
     "value": 40
    }
   ]
  }
 ],
 "version": "0.1",
 "base_model": "multiple_knapsack"
}
```

**Result:** objective 395 → 435; packed_value 435

### 164. `multiple_knapsack-logical_rule-000-0001`

*multiple_knapsack · logical_rule · template `l_at_most_k` · hard*

**Question:** Only 2 of these may have a non-zero number of item placements: bin bin2, bin1, bin4 and bin3. Re-plan.

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 2,
   "of": [
    {
     "measure": "x",
     "scope": {
      "bin": "bin2"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "x",
     "scope": {
      "bin": "bin1"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "x",
     "scope": {
      "bin": "bin4"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "x",
     "scope": {
      "bin": "bin3"
     },
     "sense": "<=",
     "value": 0
    }
   ],
   "name": "at_most_2_x"
  }
 ],
 "version": "0.1",
 "base_model": "multiple_knapsack"
}
```

**Result:** objective 395 → 295; packed_value 295

### 165. `multiple_knapsack-logical_rule-000-0004`

*multiple_knapsack · logical_rule · template `l_never_both` · medium*

**Question:** What if we may not have a non-zero number of item placements for both item item1 and item item8?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "x",
     "scope": {
      "item": "item1"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "x",
     "scope": {
      "item": "item8"
     },
     "sense": "<=",
     "value": 0
    }
   ],
   "name": "never_both_x"
  }
 ],
 "version": "0.1",
 "base_model": "multiple_knapsack"
}
```

**Result:** objective 395 → 380; packed_value 380

### 166. `multiple_knapsack-relative_rule-001-0009`

*multiple_knapsack · relative_rule · template `r_two_values` · medium*

**Question:** What if the number of item placements for item item12 may be at most 80% of the number of item placements for item item10?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "x",
   "scope": {
    "item": "item12"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "x",
    "scope": {
     "item": "item10"
    }
   },
   "factor": 0.8,
   "name": "rel_x_item12_vs_item10"
  }
 ],
 "version": "0.1",
 "base_model": "multiple_knapsack"
}
```

**Result:** objective 395 → 390; packed_value 390

### 167. `multiple_knapsack-under_specified-000-0005`

*multiple_knapsack · under_specified · template `ask_g_add_row` · medium*

**Question:** Suppose a new item joins the items table.

**Planner's answer when asked:** Add one more row to the items table: item new_item, item weight 29 and item value 30.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "add",
   "table": "items",
   "rows": [
    {
     "item": "new_item",
     "weight": 29,
     "value": 30
    }
   ]
  }
 ],
 "version": "0.1",
 "base_model": "multiple_knapsack"
}
```

**Result:** objective 395 → 415; packed_value 415

### 168. `optimize_power_schedule-chained_scenario-000-0009`

*optimize_power_schedule · chained_scenario · template `c_add` · medium*

**Earlier question:** Every fuel cost per MWh in the fuels table falls by 20%. Effect?

```json
{"version": "0.1", "base_model": "optimize_power_schedule", "data_changes": [{"op": "scale", "table": "fuels", "column": "fuel_cost", "factor": 0.8}]}
```

**Question:** On top of that: What if the fuel cost per MWh for fuel BLQ becomes 7?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "fuels",
   "column": "fuel_cost",
   "factor": 0.8
  },
  {
   "op": "set",
   "table": "fuels",
   "column": "fuel_cost",
   "where": {
    "fuel": "BLQ"
   },
   "value": 7
  }
 ],
 "version": "0.1",
 "base_model": "optimize_power_schedule"
}
```

**Result:** objective 4.495e+06 → 3.572e+06; total_cost 3.572e+06, fuel_cost 3.37e+06, health_cost 1.996e+05

### 169. `optimize_power_schedule-data_change-000-0015`

*optimize_power_schedule · data_change · template `g_set_column` · easy*

**Question:** Assume the fuel cost per MWh of fuel SUB is now 9.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "fuels",
   "column": "fuel_cost",
   "where": {
    "fuel": "SUB"
   },
   "value": 9
  }
 ],
 "version": "0.1",
 "base_model": "optimize_power_schedule"
}
```

**Result:** objective 4.495e+06 → 3.851e+06; total_cost 3.851e+06, fuel_cost 3.649e+06, health_cost 1.999e+05

### 170. `optimize_power_schedule-fixed_decision-000-0013`

*optimize_power_schedule · fixed_decision · template `f_fix_zero` · easy*

**Question:** Fix the power generated (MWh) for power plant OTHER COAL, hour 24 at 0 and optimise the rest.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "output",
   "scope": {
    "plant": "OTHER COAL",
    "hour": 24
   },
   "value": 0
  }
 ],
 "version": "0.1",
 "base_model": "optimize_power_schedule"
}
```

**Result:** objective 4.495e+06 → 4.627e+06; total_cost 4.627e+06, fuel_cost 4.293e+06, health_cost 3.311e+05

### 171. `optimize_power_schedule-fixed_decision-000-0015`

*optimize_power_schedule · fixed_decision · template `f_fix_scope` · hard*

**Question:** Level it out: power plant BIOMASS gets exactly 240 power generated (MWh) in each hour. Optimise the rest.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "output",
   "scope": {
    "plant": "BIOMASS"
   },
   "value": 240
  }
 ],
 "version": "0.1",
 "base_model": "optimize_power_schedule"
}
```

**Result:** objective 4.495e+06 → 4.608e+06; total_cost 4.608e+06, fuel_cost 4.406e+06, health_cost 1.999e+05

### 172. `optimize_power_schedule-new_limit-000-0003`

*optimize_power_schedule · new_limit · template `g_cap_measure_scope` · medium*

**Question:** What if the total number of plant-hours on for power plant Scherer may not exceed 22?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "on",
   "scope": {
    "plant": "Scherer"
   },
   "sense": "<=",
   "value": 22,
   "name": "cap_on_Scherer"
  }
 ],
 "version": "0.1",
 "base_model": "optimize_power_schedule"
}
```

**Result:** objective 4.495e+06 → 4.641e+06; total_cost 4.641e+06, fuel_cost 4.471e+06, health_cost 1.673e+05

### 173. `optimize_power_schedule-relative_rule-000-0013`

*optimize_power_schedule · relative_rule · template `r_share_of_total` · medium*

**Question:** Suppose at most 15% of the total power generated (MWh) may go to power plant Edwin I Hatch.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "output",
   "scope": {
    "plant": "Edwin I Hatch"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "output",
    "scope": {}
   },
   "factor": 0.15,
   "name": "share_output_Edwin I Hatch"
  }
 ],
 "version": "0.1",
 "base_model": "optimize_power_schedule"
}
```

**Result:** objective 4.495e+06 → 4.581e+06; total_cost 4.581e+06, fuel_cost 4.379e+06, health_cost 1.999e+05

### 174. `optimize_power_schedule-under_specified-000-0015`

*optimize_power_schedule · under_specified · template `ask_g_scale_all_rows` · medium*

**Question:** What if the fuel cost per MWh changes across the board?

**Planner's answer when asked:** The fuel cost per MWh is 25% lower for every row of the fuels table.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "fuels",
   "column": "fuel_cost",
   "factor": 0.75
  }
 ],
 "version": "0.1",
 "base_model": "optimize_power_schedule"
}
```

**Result:** objective 4.495e+06 → 3.422e+06; total_cost 3.422e+06, fuel_cost 3.22e+06, health_cost 1.996e+05

### 175. `power_generation_hydro-chained_scenario-000-0004`

*power_generation_hydro · chained_scenario · template `c_revise` · hard*

**Earlier question:** What if the units available is 20% higher for every row of the thermal generator types table?

```json
{"version": "0.1", "base_model": "power_generation_hydro", "data_changes": [{"op": "scale", "table": "thermal_types", "column": "units_available", "factor": 1.2}]}
```

**Question:** Correction: make that 10% higher, not 20% higher.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "thermal_types",
   "column": "units_available",
   "factor": 1.1
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** objective 1.001e+06 → 9.881e+05; total_cost 9.881e+05

### 176. `power_generation_hydro-chained_scenario-000-0006`

*power_generation_hydro · chained_scenario · template `c_add` · medium*

**Earlier question:** What if the total number of hydro unit start-ups for hydro unit HydroB must be at least 2?

```json
{"version": "0.1", "base_model": "power_generation_hydro", "rules": [{"measure": "hydro_start", "scope": {"hydro": "HydroB"}, "sense": ">=", "value": 2, "name": "floor_hydro_start_HydroB"}]}
```

**Question:** On top of that: Assume generator type Thermal1 is no longer part of the problem. What does the plan look like without it?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "remove",
   "table": "thermal_types",
   "where": {
    "type": "Thermal1"
   }
  }
 ],
 "rules": [
  {
   "measure": "hydro_start",
   "scope": {
    "hydro": "HydroB"
   },
   "sense": ">=",
   "value": 2,
   "name": "floor_hydro_start_HydroB"
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** objective 1.001e+06 → 1.061e+06; total_cost 1.061e+06

### 177. `power_generation_hydro-chained_scenario-000-0019`

*power_generation_hydro · chained_scenario · template `c_revise` · hard*

**Earlier question:** Suppose the maximum output per unit of generator type Thermal1 (in the thermal generator types table) rises by 10%.

```json
{"version": "0.1", "base_model": "power_generation_hydro", "data_changes": [{"op": "scale", "table": "thermal_types", "column": "max_output_mw", "where": {"type": "Thermal1"}, "factor": 1.1}]}
```

**Question:** Correction: make that 100% higher, not 10% higher.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "thermal_types",
   "column": "max_output_mw",
   "where": {
    "type": "Thermal1"
   },
   "factor": 2.0
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** objective 1.001e+06 → 8.946e+05; total_cost 8.946e+05

### 178. `power_generation_hydro-infeasible_request-000-0005`

*power_generation_hydro · infeasible_request · template `i_floor` · medium*

**Question:** Can the plan deliver at least 199700 thermal output (MW) for generator type Thermal0?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "output",
   "scope": {
    "type": "Thermal0"
   },
   "sense": ">=",
   "value": 199700,
   "name": "floor_output"
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** infeasible; conflicting constraints: available_00_06_Thermal0, available_06_09_Thermal0, available_09_15_Thermal0, available_15_18_Thermal0, available_18_24_Thermal0, max_output_00_06_Thermal0, max_output_06_09_Thermal0, max_output_09_15_Thermal0, max_output_15_18_Thermal0, max_output_18_24_Thermal0

### 179. `power_generation_hydro-infeasible_request-000-0013`

*power_generation_hydro · infeasible_request · template `i_commit` · medium*

**Question:** Commit to exactly 102000 thermal output (MW) for period 18-24, generator type Thermal0, and plan the rest around it.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "output",
   "scope": {
    "period": "18-24",
    "type": "Thermal0"
   },
   "value": 102000
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** infeasible; conflicting constraints: available_18_24_Thermal0, max_output_18_24_Thermal0

### 180. `power_generation_hydro-logical_rule-000-0003`

*power_generation_hydro · logical_rule · template `l_if_then` · hard*

**Question:** What if a non-zero number of thermal units running for period 00-06 requires a total number of thermal units started of at least 14 for period 00-06?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "ngen",
     "scope": {
      "period": "00-06"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "nstart",
     "scope": {
      "period": "00-06"
     },
     "sense": ">=",
     "value": 14
    }
   ],
   "name": "if_ngen_then_nstart"
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** objective 1.001e+06 → 1.004e+06; total_cost 1.004e+06

### 181. `power_generation_hydro-logical_rule-000-0008`

*power_generation_hydro · logical_rule · template `l_if_then` · hard*

**Question:** What if a non-zero number of thermal units running for period 00-06, generator type Thermal1 requires a total number of thermal units running of at least 14 for period 18-24, generator type Thermal1?

**Gold scenario:**

```json
{
 "logic": [
  {
   "at_least": 1,
   "of": [
    {
     "measure": "ngen",
     "scope": {
      "period": "00-06",
      "type": "Thermal1"
     },
     "sense": "<=",
     "value": 0
    },
    {
     "measure": "ngen",
     "scope": {
      "period": "18-24",
      "type": "Thermal1"
     },
     "sense": ">=",
     "value": 14
    }
   ],
   "name": "if_ngen_then_ngen"
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** objective 1.001e+06 → 1.007e+06; total_cost 1.007e+06

### 182. `power_generation_hydro-objective_change-001-0010`

*power_generation_hydro · objective_change · template `o_then_scoped` · medium*

**Question:** Keep total generating cost at its minimum, then minimise the reservoir level (m) for period 09-15.

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "min",
   "measure": "original"
  },
  {
   "sense": "min",
   "measure": "reservoir_level",
   "scope": {
    "period": "09-15"
   }
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** objective 1.001e+06 → 2.8; total_cost 1.001e+06

### 183. `power_generation_hydro-relative_rule-000-0006`

*power_generation_hydro · relative_rule · template `r_two_values` · medium*

**Question:** New policy: the thermal output (MW) for period 15-18 must not exceed the thermal output (MW) for period 00-06.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "output",
   "scope": {
    "period": "15-18"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "output",
    "scope": {
     "period": "00-06"
    }
   },
   "factor": 1.0,
   "name": "rel_output_15-18_vs_00-06"
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** objective 1.001e+06 → 1.189e+06; total_cost 1.189e+06

### 184. `power_generation_hydro-under_specified-000-0003`

*power_generation_hydro · under_specified · template `ask_g_add_row` · medium*

**Question:** What if we add another generator type?

**Planner's answer when asked:** Add one more row to the thermal generator types table: generator type new_type, units available 8, minimum output per unit 1000, maximum output per unit 1400, hourly running cost per unit 1550, cost per MWh above minimum 2, start-up cost per unit 1000 and units running at the start of the day 5.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "add",
   "table": "thermal_types",
   "rows": [
    {
     "type": "new_type",
     "units_available": 8,
     "min_output_mw": 1000,
     "max_output_mw": 1400,
     "cost_per_hour": 1550,
     "cost_per_mwh_above_min": 2,
     "startup_cost": 1000,
     "units_on_at_start": 5
    }
   ]
  }
 ],
 "version": "0.1",
 "base_model": "power_generation_hydro"
}
```

**Result:** objective 1.001e+06 → 9.452e+05; total_cost 9.452e+05

### 185. `railway_dispatching-objective_change-000-0008`

*railway_dispatching · objective_change · template `o_reorder` · medium*

**Question:** Minimise the total number of trains clearing a resource before another train enters it first; among those plans, take the one with the minimum total delay.

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "min",
   "measure": "goes_first"
  },
  {
   "sense": "min",
   "measure": "original"
  }
 ],
 "version": "0.1",
 "base_model": "railway_dispatching"
}
```

**Result:** objective 47 → 93; total_delay 93, trains_delayed 4

### 186. `railway_dispatching-objective_change-000-0013`

*railway_dispatching · objective_change · template `o_then_scoped` · medium*

**Question:** Keep total delay at its minimum, then minimise the entry time (minutes) for train B.

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "min",
   "measure": "original"
  },
  {
   "sense": "min",
   "measure": "entry_time",
   "scope": {
    "train": "B"
   }
  }
 ],
 "version": "0.1",
 "base_model": "railway_dispatching"
}
```

**Result:** objective 47 → 103; total_delay 47, trains_delayed 4

### 187. `railway_dispatching-relative_rule-000-0004`

*railway_dispatching · relative_rule · template `r_share_of_total` · medium*

**Question:** Suppose at least 40% of the total entry time (minutes) must go to train B.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "entry_time",
   "scope": {
    "train": "B"
   },
   "sense": ">=",
   "relative_to": {
    "measure": "entry_time",
    "scope": {}
   },
   "factor": 0.4,
   "name": "share_entry_time_B"
  }
 ],
 "version": "0.1",
 "base_model": "railway_dispatching"
}
```

**Result:** objective 47 → 71.25; total_delay 71.25, trains_delayed 5

### 188. `railway_dispatching-under_specified-000-0007`

*railway_dispatching · under_specified · template `ask_g_scale_column` · medium*

**Question:** What if one of the minimum time on the resource values changes?

**Planner's answer when asked:** The minimum time on the resource of resource 5 (in the stations and tracks table) falls by 30%.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "resources",
   "column": "duration",
   "where": {
    "resource": 5
   },
   "factor": 0.7
  }
 ],
 "version": "0.1",
 "base_model": "railway_dispatching"
}
```

**Result:** objective 47 → 48.5; total_delay 48.5, trains_delayed 4

### 189. `railway_dispatching-under_specified-000-0011`

*railway_dispatching · under_specified · template `ask_g_scale_all_rows` · medium*

**Question:** Suppose the minimum time on the resource shifts for every row of the stations and tracks table.

**Planner's answer when asked:** The minimum time on the resource is 10% higher for every row of the stations and tracks table.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "resources",
   "column": "duration",
   "factor": 1.1
  }
 ],
 "version": "0.1",
 "base_model": "railway_dispatching"
}
```

**Result:** objective 47 → 51.7; total_delay 51.7, trains_delayed 4

### 190. `single_machine_scheduling-new_limit-000-0001`

*single_machine_scheduling · new_limit · template `g_floor_measure_scope` · medium*

**Question:** Add a requirement: the end time, summed over everything with job = job_9, must be at least 118700.

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "end_time",
   "scope": {
    "job": "job_9"
   },
   "sense": ">=",
   "value": 118700,
   "name": "floor_end_time_job_9"
  }
 ],
 "version": "0.1",
 "base_model": "single_machine_scheduling"
}
```

**Result:** objective 1.126e+05 → 1.187e+05; makespan 1.187e+05

### 191. `single_machine_scheduling-objective_change-000-0003`

*single_machine_scheduling · objective_change · template `o_three_stages` · hard*

**Question:** Priorities in order: makespan at its minimum first, then the most total end time, and after that the least total number of job pairs where the first job runs earlier.

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "min",
   "measure": "original"
  },
  {
   "sense": "max",
   "measure": "end_time"
  },
  {
   "sense": "min",
   "measure": "runs_before"
  }
 ],
 "version": "0.1",
 "base_model": "single_machine_scheduling"
}
```

**Result:** objective 1.126e+05 → 76; makespan 1.126e+05

### 192. `single_machine_scheduling-objective_change-000-0007`

*single_machine_scheduling · objective_change · template `o_then_scoped` · medium*

**Question:** Keep makespan at its minimum, then minimise the start time for job job_6.

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "min",
   "measure": "original"
  },
  {
   "sense": "min",
   "measure": "start_time",
   "scope": {
    "job": "job_6"
   }
  }
 ],
 "version": "0.1",
 "base_model": "single_machine_scheduling"
}
```

**Result:** objective 1.126e+05 → 2.779e+04; makespan 1.126e+05

### 193. `technician_routing_scheduling-chained_scenario-000-0011`

*technician_routing_scheduling · chained_scenario · template `c_undo` · hard*

**Earlier question:** What if the daily working capacity (min) is 20% lower for every row of the technicians table?

```json
{"version": "0.1", "base_model": "technician_routing_scheduling", "data_changes": [{"op": "scale", "table": "technicians", "column": "capacity_min", "factor": 0.8}]}
```

**Question:** Forget that change. Instead: What if the time window end is 25% lower for every row of the customer jobs table?

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "customers",
   "column": "window_end",
   "factor": 0.75
  }
 ],
 "version": "0.1",
 "base_model": "technician_routing_scheduling"
}
```

**Result:** objective 1.241e+04 → 1.268e+04; total_penalty 1.268e+04, unfilled_penalty 1.22e+04, window_penalty 274.5, lateness_penalty 210, jobs_unfilled 1, lateness_minutes 105

### 194. `technician_routing_scheduling-fixed_decision-000-0004`

*technician_routing_scheduling · fixed_decision · template `combo` · hard*

**Question:** Two commitments at once: customer Customer5, technician Ed is forced (the number of jobs assigned there is fixed at 1); and the minutes late for customer Customer5 is fixed at 210. Optimise the rest.

**Gold scenario:**

```json
{
 "fixed_decisions": [
  {
   "measure": "assign",
   "scope": {
    "customer": "Customer5",
    "technician": "Ed"
   },
   "value": 1
  },
  {
   "measure": "lateness",
   "scope": {
    "customer": "Customer5"
   },
   "value": 210
  }
 ],
 "version": "0.1",
 "base_model": "technician_routing_scheduling"
}
```

**Result:** objective 1.241e+04 → 2.482e+04; total_penalty 2.482e+04, unfilled_penalty 2.44e+04, window_penalty 0, lateness_penalty 420, jobs_unfilled 2, lateness_minutes 210

### 195. `technician_routing_scheduling-objective_change-000-0000`

*technician_routing_scheduling · objective_change · template `o_reorder` · medium*

**Question:** What if the least possible total number of jobs assigned comes first and total penalty only second?

**Gold scenario:**

```json
{
 "objective": [
  {
   "sense": "min",
   "measure": "assign"
  },
  {
   "sense": "min",
   "measure": "original"
  }
 ],
 "version": "0.1",
 "base_model": "technician_routing_scheduling"
}
```

**Result:** objective 1.241e+04 → 9.772e+04; total_penalty 9.772e+04, unfilled_penalty 9.76e+04, window_penalty 0, lateness_penalty 120, jobs_unfilled 7, lateness_minutes 60

### 196. `technician_routing_scheduling-relative_rule-000-0013`

*technician_routing_scheduling · relative_rule · template `combo` · hard*

**Question:** What if location Loerrach must account for at most 20% of all service start time (min), and in addition we keep the total number of legs driven at or above 3 times the total number of technicians dispatched?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "start_time",
   "scope": {
    "location": "Loerrach"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "start_time",
    "scope": {}
   },
   "factor": 0.2,
   "name": "share_start_time_Loerrach"
  },
  {
   "measure": "route",
   "scope": {},
   "sense": ">=",
   "relative_to": {
    "measure": "use",
    "scope": {}
   },
   "factor": 3.0,
   "name": "rel_route_vs_use"
  }
 ],
 "version": "0.1",
 "base_model": "technician_routing_scheduling"
}
```

**Result:** objective 1.241e+04 → 1.278e+04; total_penalty 1.278e+04, unfilled_penalty 1.22e+04, window_penalty 0, lateness_penalty 579, jobs_unfilled 1, lateness_minutes 289.5

### 197. `technician_routing_scheduling-relative_rule-000-0015`

*technician_routing_scheduling · relative_rule · template `r_two_values` · medium*

**Question:** What if the number of jobs assigned for customer Customer5 may be at most 75% of the number of jobs assigned for customer Customer1?

**Gold scenario:**

```json
{
 "rules": [
  {
   "measure": "assign",
   "scope": {
    "customer": "Customer5"
   },
   "sense": "<=",
   "relative_to": {
    "measure": "assign",
    "scope": {
     "customer": "Customer1"
    }
   },
   "factor": 0.75,
   "name": "rel_assign_Customer5_vs_Customer1"
  }
 ],
 "version": "0.1",
 "base_model": "technician_routing_scheduling"
}
```

**Result:** objective 1.241e+04 → 2.452e+04; total_penalty 2.452e+04, unfilled_penalty 2.44e+04, window_penalty 0, lateness_penalty 120, jobs_unfilled 2, lateness_minutes 60

### 198. `technician_routing_scheduling-under_specified-000-0002`

*technician_routing_scheduling · under_specified · template `ask_g_scale_all_rows` · medium*

**Question:** What if the daily working capacity (min) changes across the board?

**Planner's answer when asked:** Every daily working capacity (min) in the technicians table rises by 25%.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "technicians",
   "column": "capacity_min",
   "factor": 1.25
  }
 ],
 "version": "0.1",
 "base_model": "technician_routing_scheduling"
}
```

**Result:** objective 1.241e+04 → 210; total_penalty 210, unfilled_penalty 0, window_penalty 0, lateness_penalty 210, jobs_unfilled 0, lateness_minutes 105

### 199. `technician_routing_scheduling-under_specified-000-0009`

*technician_routing_scheduling · under_specified · template `ask_g_scale_column` · medium*

**Question:** What if the job priority for job type Equipment Installation changes?

**Planner's answer when asked:** The job priority for job type Equipment Installation is 10% lower.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "scale",
   "table": "job_types",
   "column": "priority",
   "where": {
    "job_type": "Equipment Installation"
   },
   "factor": 0.9
  }
 ],
 "version": "0.1",
 "base_model": "technician_routing_scheduling"
}
```

**Result:** objective 1.241e+04 → 1.117e+04; total_penalty 1.117e+04, unfilled_penalty 1.098e+04, window_penalty 0, lateness_penalty 189, jobs_unfilled 1, lateness_minutes 105

### 200. `technician_routing_scheduling-under_specified-000-0019`

*technician_routing_scheduling · under_specified · template `ask_g_set_column` · medium*

**Question:** Suppose the job duration (min) for job type Equipment Installation moves. What does that do?

**Planner's answer when asked:** The job duration (min) of job type Equipment Installation is now 120.

**Gold scenario:**

```json
{
 "data_changes": [
  {
   "op": "set",
   "table": "job_types",
   "column": "duration_min",
   "where": {
    "job_type": "Equipment Installation"
   },
   "value": 120
  }
 ],
 "version": "0.1",
 "base_model": "technician_routing_scheduling"
}
```

**Result:** objective 1.241e+04 → 2.464e+04; total_penalty 2.464e+04, unfilled_penalty 2.44e+04, window_penalty 0, lateness_penalty 240, jobs_unfilled 2, lateness_minutes 120
