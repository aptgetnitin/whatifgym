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
| `multiple_knapsack` | Google LLC — OR-Tools `ortools/sat/samples/multiple_knapsack_sat.py` and `ortools/linear_solver/samples/multiple_knapsack_mip.py` | Apache-2.0 (https://github.com/google/or-tools/blob/stable/LICENSE) | Copyright 2010-2025 Google LLC. Data values reused under Apache-2.0; code re-implemented. |
| `bin_packing` | Google LLC — OR-Tools `ortools/linear_solver/samples/bin_packing_mip.py` | Apache-2.0 (as above) | Copyright 2010-2025 Google LLC. Data values reused under Apache-2.0; code re-implemented. |
| `wedding_seating` | Stuart Mitchell — PuLP `examples/wedding.py`, case study "A Set Partitioning Problem" | MIT (https://github.com/coin-or/pulp/blob/master/LICENSE) | Copyright (c) 2002-2005 Jean-Sebastien Roy; modifications Copyright (c) 2007- Stuart Anthony Mitchell. Data values reused under MIT; code re-implemented. |

The shortlist in `docs/base_models.md` links each of the 30 candidate models to its source file and records the
licence found in that repository (Gurobi modeling-examples: Apache-2.0; Google OR-Tools: Apache-2.0; PuLP: MIT;
PyPSA: MIT code with CC-BY-4.0 notebook content).

Solvers and libraries used at run time, all open source: HiGHS (MIT), SCIP (Apache-2.0 since 9.0) via PySCIPOpt
(MIT), CBC (EPL-2.0) as bundled with PuLP, OR-Tools CP-SAT (Apache-2.0), PuLP (MIT), jsonschema (MIT). Gurobi is optional and only used for
cross-checking references when a licence is present on the machine.

Not used, by design: any Intel, C3 AI or other employer/client material; the OptiGuide repository's example
applications (Gurobi-copyrighted, evaluation only) and datasets whose licences forbid training use.
