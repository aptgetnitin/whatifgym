# Porting a base model into whatifgym

Every base model is a self-contained package under `whatifgym/models/<name>/`. `factory_planning` is the
reference implementation; copy its shape exactly.

## Clean-room rule

Use only the **published data values** of a public, permissively licensed source (Apache-2.0, MIT, BSD) and write
the model code yourself. Do not copy code from the source. Record the source file, its licence and the reference
optimum you obtained by running the original implementation. Nothing from any employer or client.

## Files

```
whatifgym/models/<name>/
  __init__.py          empty
  model.py             class <CamelName>(BaseModel)
  description.md       what the model is, sizes, reference optimum, a "What-if surface" table (table -> typical questions), source + licence
  schema.json          tables (key, columns: type/unit/description/label), params, decision_variables, constraints, kpis, measures
  reference.json       {"objective", "source_solver", "n_vars", "n_constraints", "n_int_vars", "notes"}
  data/<table>.csv     one CSV per table, plus data/params.csv with columns name,value,description (if the model has scalar parameters)
tests/test_model_<name>.py
```

## model.py contract

```python
from pathlib import Path
from ...base import BaseModel, Source

class CamelName(BaseModel):
    name = "<name>"                     # snake_case, == directory name
    title = "..."                       # human title, with the source family in parentheses
    domain = "production_planning"      # supply_chain_logistics | production_planning | scheduling | energy_power | packing_assignment_covering | network_routing | revenue_resource_planning
    sense = "max"                       # or "min"
    problem_type = "LP"                 # LP | MILP | IP
    source = Source(repo="Gurobi/modeling-examples", path="<folder>/<file>.ipynb", url="https://github.com/.../blob/master/<folder>/<file>.ipynb", license="Apache-2.0", notes="Data values from the notebook; model re-implemented in PuLP.")
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("table_a", "table_b")     # CSV names without .csv; load_data() reads them into list[dict]
    HAS_PARAMS = True                   # False when there is no params.csv
    MEASURE_DIMS = {"make": ("month", "product")}   # every decision family the DSL may address -> its index dimensions

    def build(self, data):              # -> pulp.LpProblem; import pulp INSIDE the method (never at module level)
        ...
        prob._wig = {"make": make, ...} # dict of variable dicts keyed by tuples aligned with MEASURE_DIMS (a 1-dim measure may use plain keys)
        return prob

    def kpis(self, prob, data):         # -> dict of planner-facing numbers from the solved problem (use prob._wig)
        ...
```

Rules:
* **Lazy solver imports.** `import pulp` inside `build`/`kpis`. Never import highspy or ortools at module level.
* **Data is the scenario surface.** Every number a planner might change must live in a CSV table or `params.csv`, keyed by
  the index columns listed under `"key"` in `schema.json`. Nothing numeric may be hard-coded in `model.py` except
  structural constants that are not data (e.g. the first month has zero opening stock).
* **Same formulation, same size.** Reproduce the original model's variables and constraints so `n_vars`/`n_constraints`
  match the original where PuLP allows it. If the original uses a feature PuLP lacks (indicator constraints, SOS,
  piecewise), reformulate linearly and say so in `reference.json["notes"]` and `description.md`.
* **Measures.** `MEASURE_DIMS` lists every decision family (name -> dimension names). Keys of each `_wig` entry must be
  tuples in that dimension order (or plain values for a single dimension). The DSL uses them for rules, fixed decisions
  and objective stages.
* **KPIs.** Return 4–8 numbers a planner reads: the objective decomposition (revenue, cost parts), volumes, utilisation,
  fill rates. Use plain floats/ints/dicts; round sensibly.
* **Variable names.** Give every PuLP variable a unique readable name, e.g. `f"make_{m}_{p}"`.

## schema.json

```json
{"model": "<name>", "sense": "max", "objective": "<one line>",
 "tables": {"<table>": {"key": ["col"], "label": "<human label>", "columns": {"col": {"type": "string|int|number", "unit": "...", "description": "...", "label": "<short human label>"}}}},
 "params": {"<name>": {"type": "number", "unit": "...", "description": "...", "label": "..."}},
 "decision_variables": {"make[month, product]": "..."},
 "constraints": {"balance[month, product]": "..."},
 "kpis": ["..."],
 "measures": {"make": {"dims": ["month", "product"], "label": "units made"}}}
```
`type` of a numeric column must be `number` or `int` (the DSL validator uses it). Key columns are never edited.

The task families read the schema, so a few optional hints matter for the questions they generate:

* `"label"` on every table, column, parameter and measure is the noun phrase questions are built from
  ("market limit (units)", "number of machines installed", "tons of ore extracted"). Measure labels of 0/1
  measures should name countable things ("thermal units running"); the rule templates prefix "number of".
* `"editable": false` on a column keeps it out of every data-change template. Use it for structural numbers that
  are not a what-if: an `order` column of a horizon table, an ordinal such as a skill level, an initial state such
  as units on at the start of the day, a guest's rank.
* `"removable": false` on a table stops rows from being added or removed even if the table looks like an entity
  table (single key, not referenced elsewhere). Fact tables keyed by another table's entities are excluded
  automatically; declare `"ref": "<table>.<column>"` on such key columns so the relationship is explicit.
* `"min"` / `"max"` on a parameter bound the values scenarios may set (the wedding `max_table_size` is capped at
  6 because every candidate table is enumerated as a column).
* Columns whose name or label contains share / fraction / probability / proportion are never scaled, because they
  are expected to sum to one; share-like parameters are kept within [0, 1].

## reference.json

Run the **original** implementation (the Gurobi notebook's code cells with gurobipy, or the OR-Tools script) in a
subprocess and record the objective, `NumVars`, `NumConstrs`, `NumIntVars` (or the OR-Tools equivalents) and the
solver/version used, with the date. The pip gurobipy licence handles up to 2000 variables and constraints.

## Tests (`tests/test_model_<name>.py`)

```python
import math, pytest
from whatifgym.models.<name>.model import CamelName
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]

@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = CamelName()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis

def test_sizes_and_measures():
    m = CamelName(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
```

Run `python -m pytest -q tests/test_model_<name>.py` from the repo root (the repo root is on `sys.path` via `tests/conftest.py`).

## Registering

Add the class to `whatifgym/registry.py` (one import + one list entry). When several models are being ported in
parallel, leave the registry to the integrator and say so in your report.
