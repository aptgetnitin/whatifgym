# Economic Planning

**Domain:** revenue / resource planning · **Type:** LP · **Size:** 51 variables, 33 constraints · **Sense:** maximise employment

An economy has three interdependent industries: coal, steel and transport. Each unit of output (million USD) needs
inputs from all three industries in the previous year (the `input_per_unit_output` coefficients). New productive
capacity needs inputs from all three industries two years before it becomes available (`input_per_unit_capacity`).
Every year each industry must also meet an exogenous consumption demand (coal 60, steel 60, transport 30).
Output can be stocked from one year to the next. At the start, stocks are coal 250, steel 180 and transport 200;
capacities are 300, 350 and 280.

The plan covers years 1–5. Year 6 stands for the steady state beyond the horizon. In year 6, each industry must
produce at least its static Leontief level, which solves x = A x + demand (coal 166.40, steel 105.67, transport
92.31). Nothing is produced in year 1, so year-1 needs come from the initial stock. Capacity can first become
available in year 3 and is not built in year 6. Output in years 1–5 cannot exceed the initial capacity plus the
capacity built so far.

Decisions: per year and industry, **production**, end-of-year **stock** and **extra_capacity** (capacity becoming
available that year).

The objective is total manpower over years 1–5: manpower per unit of output (coal 0.6, steel 0.3, transport 0.2)
times production, plus manpower per unit of capacity built (0.4, 0.2, 0.1) times extra capacity.

Reference optimum (original Gurobi notebook): **1 902.22**. Coal capacity grows to 961 (built in years 3 and 5);
steel and transport build none. Total output over years 1–5 is 3 724.90. The year-by-year split of output has
alternative optima.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `industries` | Steel demand rises to 80. Transport starts with 150 in stock. Coal capacity is 250. Coal needs less manpower per unit (0.5). |
| `input_output` | Steel needs 20 % less coal per unit of output. Building transport capacity needs 0.7 coal per unit instead of 0.9. |
| `years` | The horizon is extended by a year (add a year; the last year remains the steady-state year). |

Rules and fixed decisions address `production`, `stock` and `extra_capacity` (by `year`, `industry`). Examples:
"build no steel capacity"; "produce at most 400 coal in year 5".

## Port notes

* **Objective.** The notebook maximises employment, so the port does too (`data/base_models.csv` says total
  production).
* **No output bound.** The notebook passes `ub=capacity0`, which is keyed by industry, to variables keyed by
  (industry, year). Gurobi therefore applies no bound. The port leaves production unbounded too; the capacity
  rows still limit years 1–5.
* **Steady state.** The notebook gets the year-6 levels from a separate static LP. The port solves the same
  3×3 linear system inside `build`, so the levels follow changes to demand and coefficients. The rows and bounds
  are otherwise the original's.

Source: Gurobi `modeling-examples/economic_planning/economic_planning.ipynb` (Apache-2.0), after H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 9. Only the published data values are reused; no
code is copied.
