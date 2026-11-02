# Attribution

whatifgym re-implements public optimization models from scratch and reuses only their published data values.
The sources, their licences and the notices they require are listed here. Each ported model also carries its
source in `whatifgym/models/<name>/model.py` (`Source(...)`) and the reference optimum obtained by running the
original implementation in `reference.json`.

Gurobi's `modeling-examples` notebooks are themselves worked versions of examples from H. P. Williams, *Model
Building in Mathematical Programming* (5th ed., Wiley); the example number is given for each. The book's text is
not reproduced anywhere in this repository — only the numeric data as published in the Apache-2.0 notebooks.

| whatifgym model | original | licence | notice |
|---|---|---|---|
| `factory_planning` | Gurobi Optimization, LLC — `modeling-examples/factory_planning/factory_planning_1.ipynb` (Williams, example 3) | Apache-2.0 (https://github.com/Gurobi/modeling-examples/blob/master/LICENSE.txt) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `factory_planning_2` | Gurobi Optimization, LLC — `modeling-examples/factory_planning/factory_planning_2.ipynb` (Williams, example 4) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `food_manufacture` | Gurobi Optimization, LLC — `modeling-examples/food_manufacturing/food_manufacture_1.ipynb` (Williams, example 1) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `mining` | Gurobi Optimization, LLC — `modeling-examples/mining/mining.ipynb` (Williams, example 7) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `manpower_planning` | Gurobi Optimization, LLC — `modeling-examples/manpower_planning/manpower_planning.ipynb` (Williams, example 5) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `power_generation_hydro` | Gurobi Optimization, LLC — `modeling-examples/electrical_power_generation/electrical_power_2.ipynb` (Williams, example 16) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `car_rental` | Gurobi Optimization, LLC — `modeling-examples/car_rental/car_rental_1.ipynb` (Williams, example 25) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `farm_planning` | Gurobi Optimization, LLC — `modeling-examples/farm_planning/farm_planning.ipynb` (Williams, example 8) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `battery_scheduling` | Gurobi Optimization, LLC — `modeling-examples/battery_scheduling/battery_scheduling.ipynb` (variant S) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `car_rental_2` | Gurobi Optimization, LLC — `modeling-examples/car_rental/car_rental_2.ipynb` (Williams, example 26) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `food_supply` | Gurobi Optimization, LLC — `modeling-examples/food_program/food_supply.ipynb` and its six CSV files (World Food Programme case) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `economic_planning` | Gurobi Optimization, LLC — `modeling-examples/economic_planning/economic_planning.ipynb` (Williams, example 9, as the notebook states) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `fantasy_basketball` | Gurobi Optimization, LLC — `modeling-examples/fantasy_basketball/fantasy_basketball_part1.ipynb` and its `results_target_advanced.csv` | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Player names, positions, salaries and predicted points reused under Apache-2.0; code re-implemented; the regression that predicts points is not reproduced. The notebook states that the salaries and positions come from the Kaggle dataset "daily-fantasy-basketball-draftkings" (alandu20) and the box scores from "nba-enhanced-stats" (pablote); those datasets' own licences were not checked. |
| `assignment_with_constraints` | Google LLC — OR-Tools `examples/python/assignment_with_constraints_sat.py` | Apache-2.0 (https://github.com/google/or-tools/blob/stable/LICENSE) | Copyright 2010-2025 Google LLC. Data values reused under Apache-2.0; the CP-SAT model is re-implemented as a 0-1 integer program. |
| `covid19_facility_location` | Gurobi Optimization, LLC — `modeling-examples/covid19_facility_location/covid19_facility_location.ipynb` (base scenario) | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `railway_dispatching` | Gurobi Optimization, LLC — `modeling-examples/railway_dispatching/railway_dispatching.ipynb` | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `optimize_power_schedule` | Gurobi Optimization, LLC — `modeling-examples/power_generation/optimize_power_schedule.ipynb` and its CSV files | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `technician_routing_scheduling` | Gurobi Optimization, LLC — `modeling-examples/technician_routing_scheduling/technician_routing_scheduling.ipynb` and its `data-Sce3.xlsx` workbook | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values (fictional) reused under Apache-2.0; code re-implemented. |
| `drone_network` | Gurobi Optimization, LLC — `modeling-examples/drone_network/drone_network.ipynb` and its three CSV files | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. The data comes from Custodio & Lejeune (2022), INFORMS Journal on Computing, repository INFORMSJoC/2020.1022 (MIT): public 911 cardiac-arrest incidents in Virginia Beach, at street-block level. |
| `airline_planning` | Gurobi Optimization, LLC — `modeling-examples/aviation_planning/airlineplanning.ipynb` and its CSV files | Apache-2.0 (as above) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0 as redistributed by Gurobi; code re-implemented. The flight data derives from the ROADEF/EURO 2009 challenge (Amadeus); its original terms were not checked. |
| `multiple_knapsack` | Google LLC — OR-Tools `ortools/sat/samples/multiple_knapsack_sat.py` and `ortools/linear_solver/samples/multiple_knapsack_mip.py` | Apache-2.0 (https://github.com/google/or-tools/blob/stable/LICENSE) | Copyright 2010-2025 Google LLC. Data values reused under Apache-2.0; code re-implemented. |
| `bin_packing` | Google LLC — OR-Tools `ortools/linear_solver/samples/bin_packing_mip.py` | Apache-2.0 (as above) | Copyright 2010-2025 Google LLC. Data values reused under Apache-2.0; code re-implemented. |
| `jobshop_ft06` | Google LLC — OR-Tools `examples/python/jobshop_ft06_sat.py` | Apache-2.0 (as above) | Copyright 2010-2025 Google LLC. The ft06 instance (Fisher & Thompson, 1963) reused; the CP-SAT model is re-implemented as a big-M MILP. |
| `single_machine_scheduling` | Google LLC — OR-Tools `examples/python/single_machine_scheduling_with_setup_release_due_dates_sat.py` | Apache-2.0 (as above) | Copyright 2010-2025 Google LLC. Data values reused under Apache-2.0; the CP-SAT model is re-implemented as a strengthened MILP. |
| `wedding_seating` | Stuart Mitchell — PuLP `examples/wedding.py`, case study "A Set Partitioning Problem" | MIT (https://github.com/coin-or/pulp/blob/master/LICENSE) | Copyright (c) 2002-2005 Jean-Sebastien Roy; modifications Copyright (c) 2007- Stuart Anthony Mitchell. Data values reused under MIT; code re-implemented. |

The shortlist in `docs/base_models.md` links each of the 30 candidate models to its source file and records the
licence found in that repository (Gurobi modeling-examples: Apache-2.0; Google OR-Tools: Apache-2.0; PuLP: MIT;
PyPSA: MIT code with CC-BY-4.0 notebook content).

Solvers and libraries used at run time, all open source: HiGHS (MIT), SCIP (Apache-2.0 since 9.0) via PySCIPOpt
(MIT), CBC (EPL-2.0) as bundled with PuLP, OR-Tools CP-SAT (Apache-2.0), PuLP (MIT), jsonschema (MIT). Gurobi is optional and only used for
cross-checking references when a licence is present on the machine.

Not used, by design: any Intel, C3 AI or other employer/client material; the OptiGuide repository's example
applications (Gurobi-copyrighted, evaluation only) and datasets whose licences forbid training use.
