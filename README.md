# whatifgym

Clean-room benchmark and RL environment for LLM what-if agents over optimization models.

A planner asks "what if demand for Prod5 drops 20 % in May?" or "what if we add a sixth bin?". The agent has to turn
that question into a *verified* change to an existing optimization model, re-solve it, and report the KPIs. whatifgym
provides the pieces needed to train and evaluate such agents: base models with named data tables, a common solve
interface on open solvers, reference optima, and (coming) scenario tasks with solver-verified rewards.

## Clean-room rule

Every model, dataset and scenario in this repository comes from **public, permissively licensed sources**
(Apache-2.0, MIT, BSD) and is **rebuilt from scratch** here. No employer or client code, data, scenarios or names
are used, now or later. Each ported model records its source, licence and the reference optimum obtained by running
the original public implementation (`whatifgym/models/<name>/reference.json`); see `ATTRIBUTION.md`.

## Status (Phase 1)

| Done | Item |
|---|---|
| yes | Repository created with LICENSE and README only in the first commit |
| yes | HiGHS, SCIP (PySCIPOpt) and OR-Tools installed and verified (`setup.sh`, `requirements.txt`) |
| yes | One model each ported from the Gurobi examples, the OR-Tools examples and the PuLP case studies; all three solve on open solvers with objectives matching the originals (`scripts/verify_models.py`) |
| yes | 30 base models chosen (at least 4 per domain, 50 to 5 000 variables, open-solver time under 2 s) with source, licence and measured size: `docs/base_models.md`, `data/base_models.csv` |
| yes | Scenario DSL v0.1 with a JSON Schema: 10 worked examples validate, 22 planted bad scenarios are rejected with actionable errors (`whatifgym/dsl/SPEC.md`) |
| yes | Oracle and scorer: a scenario is validated, applied, re-solved and compared within relative tolerance 1e-3; the same change spelled two ways scores identically |
| started | Task families: `data_change` over `factory_planning` (60 tasks with reference solutions, `tasks/factory_planning/data_change_v0.jsonl`); `new_limit` and the other 9 models are next |
| started | Environment (`reset`/`step`, ask + scenario actions, 3 turns) and baseline runner; trivial agents verified (oracle 1.10, noop 0.10, unneeded ask 0.90); the frontier-API agent is wired up (`--agent anthropic`) but has not been run yet |

## Ported models

| model | source | type | vars / cons | reference optimum | verified on |
|---|---|---|---|---|---|
| `factory_planning` | Gurobi modeling-examples, Factory Planning I (Apache-2.0) | LP | 126 / 79 | 93 715.18 | HiGHS, SCIP, CBC, Gurobi |
| `multiple_knapsack` | OR-Tools samples, multiple knapsack (Apache-2.0) | IP | 75 / 20 | 395 | HiGHS, SCIP, CBC, CP-SAT, Gurobi |
| `wedding_seating` | PuLP case study, set partitioning (MIT) | IP | 3 213 / 18 | 12 | HiGHS, SCIP, CBC, CP-SAT |

## Quick start

```bash
git clone https://github.com/aptgetnitin/whatifgym && cd whatifgym
./setup.sh                      # creates .venv, installs solvers, runs the tests and the verification table
source .venv/bin/activate

python -m whatifgym.runner --model factory_planning --solver highs
python -m whatifgym.runner --model multiple_knapsack --solver cpsat
python scripts/verify_models.py # every model x every available open solver vs. the reference optimum
```

```python
from whatifgym import get_model

m = get_model("factory_planning")
data = m.load_data()                      # dict of CSV tables + params: the editable scenario surface
base = m.solve(data, solver="highs")      # SolveResult(status, objective, kpis, ...)

# What if the horizontal drills are all down in February?
for row in data["downtime"]:
    if row["month"] == "Feb" and row["machine"] == "horiDrill":
        row["machines_down"] = 3
scenario = m.solve(data, solver="highs")
print(base.objective - scenario.objective, scenario.kpis["machine_utilisation"])
```

## Scenario DSL, oracle, environment

A what-if question is answered with one JSON object in the scenario DSL (`whatifgym/dsl/SPEC.md`): data
changes (`scale`, `shift`, `set`, `add`, `remove` rows; parameter edits), rules (limits on sums of decision
measures, absolute or relative), lexicographic objective stages, fixed decisions, or a single `ask`. The oracle
validates it (JSON Schema, then semantics against the model's tables, keys and measures), applies it, re-solves on
an open solver and returns status, objective, KPIs and decisions. The scorer compares results, never text.

```python
from whatifgym.oracle import solve_scenario
from whatifgym.env import WhatIfEnv
from whatifgym.tasks import load_tasks

r = solve_scenario("factory_planning", {"version": "0.1", "data_changes": [
    {"op": "scale", "table": "max_sales", "column": "max_sales",
     "where": {"product": "Prod5", "month": ["May", "Jun"]}, "factor": 0.8}]})
print(r.status, r.objective, r.kpis["profit"])

tasks = load_tasks("tasks/factory_planning/data_change_v0.jsonl", split="test")
env = WhatIfEnv(tasks)
obs = env.reset(tasks[0])          # description, schema, index sets, measures, DSL schema, 2 worked examples, question
obs, reward, done, info = env.step({"type": "scenario", "scenario": {...}})
```

```bash
python scripts/make_tasks.py --family data_change --model factory_planning --n 60 --check-solvers
python scripts/run_baseline.py --tasks tasks/factory_planning/data_change_v0.jsonl --agent oracle   # 1.10
python scripts/run_baseline.py --tasks tasks/factory_planning/data_change_v0.jsonl --agent noop     # 0.10
ANTHROPIC_API_KEY=... python scripts/run_baseline.py --tasks tasks/factory_planning/data_change_v0.jsonl --split test --agent anthropic --model <model>
```

Reward: 1.0 when status, objective and the family's KPIs match the hidden reference within 1e-3 relative, plus
0.1 for a valid scenario, minus 0.2 for an unnecessary clarifying question; a needed question not asked scores 0.
Every task is generated so that "no change" is clearly wrong under that tolerance, and every reference is checked
to be identical on HiGHS, SCIP and CBC.

## Layout

```
whatifgym/
  base.py          BaseModel interface, SolveResult, CSV helpers
  solvers.py       open-solver access through PuLP (highs | scip | cbc) and availability checks
  runner.py        solve one (model, solver) pair in-process or in a subprocess; CLI
  registry.py      model registry
  models/<name>/   model.py, description.md, schema.json, reference.json, data/*.csv
  dsl/             schema.json, SPEC.md, validate.py, apply.py, examples/
  oracle.py        validate + apply + solve -> ScenarioResult
  scoring.py       compare results (rel 1e-3), reward rules
  env.py           WhatIfEnv: reset / step, ask + scenario actions
  tasks.py         Task records, JSONL I/O, deterministic splits
  families/        task-family generators (data_change)
scripts/
  verify_models.py           cross-solver verification against reference optima
  build_base_model_table.py  regenerates docs/base_models.md and data/base_models.csv
  make_tasks.py              generates a task file with oracle references (+ cross-solver stability check)
  run_baseline.py            runs an agent (oracle | noop | ask_then_oracle | anthropic) through the environment
tasks/<model>/<family>_v0.jsonl   generated tasks with hidden gold scenarios and references
tests/             pytest (47 tests): models, DSL, oracle, scoring, environment, families
docs/base_models.md, data/base_models.csv   the 30-model shortlist with sources, licences and measured sizes
```

Each model exposes `load_data()`, `build(data) -> pulp.LpProblem`, `kpis(prob, data) -> dict`, and for integer
models `build_cpsat(data)`. Scenarios are **data edits**, not code edits: change a CSV table or a parameter, re-solve,
compare KPIs. That is what makes a scenario checkable.

## Solvers

| name | backend | notes |
|---|---|---|
| `highs` | HiGHS via `highspy` (`pulp.HiGHS`) | default LP/MILP solver |
| `scip` | SCIP via `pyscipopt` (`pulp.SCIP_PY`) | second opinion for every MILP |
| `cbc` | CBC binary shipped with PuLP | available on most platforms |
| `cpsat` | OR-Tools CP-SAT | integer models that implement `build_cpsat` |
| `gurobi` | `gurobipy` (optional) | cross-checks only; never required |

**Known issue.** On Linux the `highspy` and `ortools` wheels both bundle `libhighs.so.1`, so importing both in one
Python process fails with an `undefined symbol` error (seen with highspy 1.15.1 + ortools 9.15 on x86-64 and arm64).
whatifgym therefore never imports a solver at module level, and `whatifgym.runner.run_subprocess` / `scripts/verify_models.py`
run each (model, solver) pair in its own interpreter. Use `runner.run(...)` in-process only when a single solver family
is needed.

PuLP is pinned to `<4` because PuLP 4.0 (September 2026) changed the modelling API; the 3.x API is the one most
published model code uses.

## Licence

MIT for the code in this repository. Ported models reuse only published data values from Apache-2.0 and MIT
sources; attribution and the original notices are in `ATTRIBUTION.md`.
