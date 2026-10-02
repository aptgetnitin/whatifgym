# Attribution

whatifgym re-implements public optimization models from scratch and reuses only their published data values.
The sources, their licences and the notices they require are listed here. Each ported model also carries its
source in `whatifgym/models/<name>/model.py` (`Source(...)`) and the reference optimum obtained by running the
original implementation in `reference.json`.

| whatifgym model | original | licence | notice |
|---|---|---|---|
| `factory_planning` | Gurobi Optimization, LLC — `modeling-examples/factory_planning/factory_planning_1.ipynb`, after H. P. Williams, *Model Building in Mathematical Programming*, 5th ed., example 3 | Apache-2.0 (https://github.com/Gurobi/modeling-examples/blob/master/LICENSE.txt) | Copyright © 2020 Gurobi Optimization, LLC. Data values reused under Apache-2.0; code re-implemented. |
| `multiple_knapsack` | Google LLC — OR-Tools `ortools/sat/samples/multiple_knapsack_sat.py` and `ortools/linear_solver/samples/multiple_knapsack_mip.py` | Apache-2.0 (https://github.com/google/or-tools/blob/stable/LICENSE) | Copyright 2010-2025 Google LLC. Data values reused under Apache-2.0; code re-implemented. |
| `wedding_seating` | Stuart Mitchell — PuLP `examples/wedding.py`, case study "A Set Partitioning Problem" | MIT (https://github.com/coin-or/pulp/blob/master/LICENSE) | Copyright (c) 2002-2005 Jean-Sebastien Roy; modifications Copyright (c) 2007- Stuart Anthony Mitchell. Data values reused under MIT; code re-implemented. |

The shortlist in `docs/base_models.md` links each of the 30 candidate models to its source file and records the
licence found in that repository (Gurobi modeling-examples: Apache-2.0; Google OR-Tools: Apache-2.0; PuLP: MIT;
PyPSA: MIT code with CC-BY-4.0 notebook content).

Not used, by design: any Intel, C3 AI or other employer/client material; the OptiGuide repository's example
applications (Gurobi-copyrighted, evaluation only) and datasets whose licences forbid training use.
