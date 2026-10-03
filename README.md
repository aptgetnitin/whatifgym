# whatifgym

A clean-room benchmark and reinforcement-learning environment for **LLM what-if agents over optimization models**.

A planner who owns an optimization model (a production plan, a fleet plan, a generation schedule) asks questions
like *"what if demand for Prod5 drops 20 % in May?"*, *"what if we may never make more than 300 units of Prod1 in a
month?"* or *"what if guest K cancels?"*. Answering one of those by hand means finding the right table cell or the
right new constraint, editing the model, re-solving it and reading off the KPIs. whatifgym turns that job into a
machine-checkable task: the agent has to **translate the question into a formal scenario**; a solver, not the
agent, then re-solves the model, and the agent is rewarded only when the re-solved result matches the hidden
reference. Everything needed to generate such tasks, run agents on them and score them is in this repository.

This README is written for someone who sees only the code. It explains the idea, every concept and file, how to run
each piece, what the results so far mean, and how to extend it.

---

## Contents

1. [The idea in one picture](#1-the-idea-in-one-picture)
2. [Clean-room rule](#2-clean-room-rule)
3. [Glossary](#3-glossary)
4. [Repository layout](#4-repository-layout)
5. [Base models](#5-base-models)
6. [The scenario DSL](#6-the-scenario-dsl)
7. [Oracle and scoring](#7-oracle-and-scoring)
8. [The environment](#8-the-environment)
9. [Task families and the generated task files](#9-task-families-and-the-generated-task-files)
10. [Results so far](#10-results-so-far)
11. [Running everything](#11-running-everything)
12. [Extending: new model, new family, new template](#12-extending-new-model-new-family-new-template)
13. [Conventions and known gotchas](#13-conventions-and-known-gotchas)
14. [Status and roadmap](#14-status-and-roadmap)
15. [Licence](#15-licence)

---

## 1. The idea in one picture

```
 base model                      hidden gold scenario          reference result
 (CSV tables + build())  ──►  template picks an edit  ──►  oracle re-solves  ──►  {status, objective, KPIs}
        │                              │                                                  │
        │                              ▼                                                  │
        │                    natural-language question                                    │
        │                              │                                                  │
        ▼                              ▼                                                  ▼
 observation ──────────────────────► AGENT ──► scenario JSON (DSL) ──► oracle re-solves ──► compare ──► reward
 (description, schema, keys,          │
  measures, DSL schema, examples)     └──► or {"ask": "..."} ──► simulated planner answers ──► AGENT ...
```

A **base model** is an ordinary optimization model (LP, MILP or IP) written so that all of its numbers live in CSV
tables and a parameter list, and the model is rebuilt from those tables on every solve. A **task** is a question in
plain language plus a hidden **gold scenario**: a small JSON document in the **scenario DSL** that says exactly
which numbers change or which new constraint is added. The **oracle** applies a scenario to the data, rebuilds the
model, solves it with an open solver and returns status, objective and KPIs. The **scorer** compares the agent's
re-solved result with the reference result (never the JSON text, so any equivalent spelling of the same change is
correct). The **environment** wraps this as `reset()` / `step()` with two kinds of action: ask a clarifying
question, or submit a scenario. **Task families** are generators that produce questions and gold scenarios for any
registered model from its schema, filter out tasks that are trivial, duplicated or solver-dependent, and write
JSONL files that are frozen once results refer to them.

The agent is never asked to solve anything. Its whole job is the translation from words to a checkable scenario,
which is what a planner would otherwise do by hand in a spreadsheet or a notebook.

## 2. Clean-room rule

Every model, dataset and scenario in this repository comes from **public, permissively licensed sources**
(Apache-2.0, MIT, BSD) and is **rebuilt from scratch** here. No employer or client code, data, scenarios or names
are used, now or later. Each ported model records its source, licence and the reference optimum obtained by running
the original public implementation (`whatifgym/models/<name>/reference.json`); the full list with the notices the
licences require is `ATTRIBUTION.md`. Ten models are ported so far; the thirty-model shortlist they come from, with
links, licences and measured sizes, is `docs/base_models.md`.

## 3. Glossary

| term | meaning in this repository |
|---|---|
| **base model** | A class in `whatifgym/models/<name>/model.py` deriving from `BaseModel`, plus `data/*.csv`, `schema.json`, `description.md` and `reference.json`. It rebuilds a PuLP `LpProblem` from the data every time (`build(data)`), so scenarios are **data edits, not code edits**. |
| **data** | `model.load_data()`: a dict with one list of row-dicts per CSV table (`data["max_sales"] == [{"month": "Jan", "product": "Prod1", "max_sales": 500}, ...]`) and `data["params"]`, a dict of scalar parameters from `params.csv`. This is the entire editable surface. |
| **schema** | `schema.json`: for every table its key columns, each column's type, unit, description and human **label**, each parameter, each decision measure, and prose for decision variables and constraints. Labels drive the generic question templates; `"editable": false` marks structural columns that are never a what-if (an ordering, an initial state); `"min"`/`"max"` on a parameter bound what scenarios may set it to. |
| **measure** | A named family of decision variables with dimensions, e.g. `make[month, product]`. Declared in `MEASURE_DIMS` and returned by `model.measures(prob)`. Rules, fixed decisions and objective stages in the DSL refer to measures, never to raw solver variables. |
| **KPI** | Every model's `kpis(prob, data)` returns a dict of business numbers (profit, holding cost, bins used, ...). `SCORING_KPIS` lists the subset that is unique at the optimum; only those are compared when scoring, because models with degenerate optima have other KPIs that legitimately differ between solvers. |
| **scenario** | One JSON object in the scenario DSL (`whatifgym/dsl/SPEC.md`, `schema.json`): `data_changes`, `rules`, `objective` stages, `fixed_decisions`, or a lone `ask`. |
| **rule** | A new linear constraint on the sum of a measure over a scope: `{"measure": "make", "scope": {"product": "Prod1"}, "sense": "<=", "value": 1000}`; `relative_to` + `factor` express "at most 80 % of what we sell". |
| **oracle** | `whatifgym.oracle.solve_scenario(model, scenario, data, solver)`: validate → apply → build → solve → `ScenarioResult`. Used both to produce reference results and to evaluate what the agent submits. |
| **reference** | The oracle's result on the gold scenario, stored inside each task (`task.reference`). Generation guarantees that HiGHS and a second open solver agree on it. |
| **task** | `whatifgym.tasks.Task`: id, family, model, question, hidden `scenario`, `reference`, `kpi_keys`, difficulty, template, slots, split, optional `clarification`, tags. One JSON line per task in `tasks/<model>/<family>_v0.jsonl`. |
| **family** | A kind of what-if, implemented as a `TaskFamily` subclass in `whatifgym/families/`: `data_change` (edit numbers, add or remove rows, change a parameter) and `new_limit` (add rules). |
| **template** | One question pattern inside a family, a function `(rng, ctx) -> (question, scenario, slots, difficulty)` or `None`. *Specific* templates speak the language of one model (factory planning); *generic* templates work on any model from its schema labels. |
| **combo** | A two-part question made from two templates ("What if X, and at the same time Y?"); always `difficulty = hard`, capped at 30 % of a file. |
| **split** | `train` / `dev` / `test`, 70/15/15, decided by a hash of the task id, so regenerating never moves a task between splits. |
| **reward** | 1.0 if the re-solved result matches the reference (status; and for optimal results objective and scoring KPIs within relative 1e-3), +0.1 for a valid scenario even when wrong, −0.2 for an unnecessary clarifying question, 0 when a needed question was not asked. |
| **trivial agents** | `oracle` (submits the gold scenario, must score 1.1), `noop` (empty valid scenario, must score 0.1), `ask_then_oracle` (one needless question then the gold scenario, must score 0.9). They pin the reward scale and catch leaked or broken tasks. |
| **frontier baseline** | A large hosted model run through the same environment, either through the Anthropic API (`--agent anthropic`) or by replaying answers collected offline (`--agent answers`). |

## 4. Repository layout

```
whatifgym/                      the package (import whatifgym)
  base.py                       BaseModel contract, Source, SolveResult, Measure; CSV loading; solve() on any solver
  solvers.py                    open-solver access through PuLP (highs | scip | cbc), CP-SAT helpers, availability checks
  runner.py                     solve one (model, solver) pair in-process or in a subprocess; `python -m whatifgym.runner`
  registry.py                   list_models(), get_model(name): every ported model is registered here
  models/<name>/                one folder per base model (see section 5)
    model.py                    the class: TABLES, MEASURE_DIMS, SCORING_KPIS, build(), kpis(), measures(), [build_cpsat()]
    data/*.csv                  the tables and params.csv (name,value,description)
    schema.json                 tables, columns, labels, params, measures, decision variables, constraints in words
    description.md              what the model is, its what-if surface, where it comes from
    reference.json              the optimum of the original public implementation, reproduced by the port
  dsl/
    schema.json                 JSON Schema 2020-12 of the scenario DSL
    SPEC.md                     the DSL specification with semantics of every operation
    validate.py                 two-stage validation: syntax (JSON Schema), then semantics against a model's data
    apply.py                    apply data changes, add rules / fixed decisions, run objective stages, solve
    examples/01..10.json        worked examples (two are shown to the agent in every observation)
  oracle.py                     solve_scenario() -> ScenarioResult; save/load results
  scoring.py                    compare_results(), score() and the reward constants
  env.py                        WhatIfEnv: reset()/step(), observation, ask handling, 3 turns
  tasks.py                      Task dataclass, JSONL I/O, deterministic splits
  families/
    base.py                     FamilyContext (what templates may look at) and TaskFamily.generate() with its filters
    data_change.py              family 1: specific factory-planning templates + generic schema-driven templates
    new_limit.py                family 2: rule templates, specific and generic
scripts/
  verify_models.py              every model x every available solver vs reference.json (33/33 pairs match)
  build_base_model_table.py     regenerates docs/base_models.md and data/base_models.csv (the 30-model shortlist)
  make_tasks.py                 generates task files for one or all (family, model) pairs; respects tasks/frozen.txt
  run_baseline.py               runs an agent through the environment: oracle | noop | ask_then_oracle | anthropic | ollama | answers
  run_trivial_baselines.py      the three trivial agents on every task file -> results/trivial_baselines.md
  run_local_baselines.py        local Ollama models over every task file, resumable -> results/baselines/local/
  summarise_results.py          comparison tables across result files -> results/baselines/summary.md
tasks/
  <model>/data_change_v0.jsonl  generated tasks (question, hidden gold scenario, reference, split)
  <model>/new_limit_v0.jsonl
  frozen.txt                    task files that published results cite; make_tasks.py never overwrites them
results/
  trivial_baselines.md          oracle / noop / ask_then_oracle on all 19 task files
  baselines/summary.md          accuracy tables across every model run so far (regenerate with summarise_results.py)
  baselines/data_change_v0/     the first frontier baseline (Claude Sonnet and Opus on factory_planning data_change)
  baselines/local/<model>/      local open-weight model runs (created by run_local_baselines.py)
tests/                          pytest, 166 tests: models, DSL, oracle, scoring, env, families, task files
docs/
  base_models.md                the 30-model shortlist with sources, licences, measured sizes and what-if hooks
  PORTING_GUIDE.md              how to port a public model into whatifgym, step by step
data/base_models.csv            the same shortlist as CSV
ATTRIBUTION.md                  sources, licences and notices for every ported model
requirements.txt, setup.sh      pulp<4, highspy, pyscipopt, ortools, jsonschema, pytest; one-shot environment setup
```

## 5. Base models

Ten public models are ported so far, chosen from the shortlist in `docs/base_models.md` to cover several domains
and all three problem types. Each one reproduces the published optimum on HiGHS, SCIP and CBC
(`scripts/verify_models.py`: 33 of 33 model–solver pairs match); the pure-integer ones also have a native OR-Tools
CP-SAT formulation.

| model | origin (all re-implemented; data values only) | type | vars / cons / int | sense | reference optimum | scoring KPIs | measures |
|---|---|---|---|---|---|---|---|
| `factory_planning` | Gurobi modeling-examples, Factory Planning I (Williams ex. 3) | LP | 126 / 79 / 0 | max | 93 715.18 | profit, holding_cost, sales_contribution | make, store, sell |
| `factory_planning_2` | Gurobi, Factory Planning II: maintenance month is a decision | MILP | 156 / 84 / 30 | max | 108 855 | profit, sales_contribution, holding_cost | make, store, sell, repair |
| `food_manufacture` | Gurobi, Food Manufacture I: oil buying, blending, storage | LP | 96 / 70 / 0 | max | 107 842.59 | profit, revenue, food_produced | buy, consume, store, produce |
| `mining` | Gurobi, Mining: which mines to work each year, ore blending | MILP | 65 / 71 / 40 | max | 146 861 974.36 | profit, discounted_revenue, discounted_royalties, ore_sold_tons | extract, operate, open, blend |
| `manpower_planning` | Gurobi, Manpower Planning: recruit, retrain, downgrade, redundancy | LP | 72 / 30 / 0 | min | 841.80 | total_redundancy, redundancy_by_year, redundancy_by_skill | recruit, retrain, downgrade, redundant, short_time, overmanned, workforce |
| `power_generation_hydro` | Gurobi, Electrical Power Generation 2: thermal units + pumped hydro | MILP | 75 / 85 / 50 | min | 1 000 630 | total_cost | ngen, output, nstart, hydro_on, hydro_start, pump, reservoir_level |
| `car_rental` | Gurobi, Car Rental 1: fleet size, transfers, repairs over a week | LP | 289 / 97 / 0 | max | 121 160.21 | profit, rental_contribution, transfer_cost, fleet_cost, fleet_size | fleet_size, rentals, (un)damaged_stock, (un)damaged_left, (un)damaged_transfers, repairs |
| `multiple_knapsack` | OR-Tools samples, multiple knapsack | IP | 75 / 20 / 75 | max | 395 | packed_value | x |
| `bin_packing` | OR-Tools samples, bin packing | IP | 132 / 22 / 132 | min | 4 | bins_used, total_weight, min_bins_by_weight | x, y |
| `wedding_seating` | PuLP case study, set partitioning (every candidate table is a column) | IP | 3 213 / 18 / 3 213 | min | 12 | total_unhappiness | x |

Every model follows the same contract (`whatifgym/base.py`):

```python
class FactoryPlanning(BaseModel):
    name, title, domain, sense, problem_type, source   # identity and provenance
    DATA_DIR, TABLES                                    # which CSVs make up load_data()
    MEASURE_DIMS = {"make": ("month", "product"), ...}  # decision measures and their dimensions
    SCORING_KPIS = ["profit", "holding_cost", "sales_contribution"]   # KPIs unique at the optimum
    def build(self, data) -> pulp.LpProblem             # rebuild from data; keeps variable handles in prob._wig
    def kpis(self, prob, data) -> dict                  # business numbers read off the solved problem
    def measures(self, prob) -> dict[str, Measure]      # name -> Measure(dims, {index tuple: variable})
    def build_cpsat(self, data), kpis_cpsat(...)        # optional native CP-SAT formulation for IP models
```

`BaseModel` supplies `load_data()`, `schema()`, `description()`, `reference()`, `index_sets(data)` (the key values
per dimension), `table_keys(data)` (which rows exist, keys only) and `solve(data, solver, time_limit,
keep_variables)`. Solver libraries are imported lazily inside methods, never at module import (see section 13).

`docs/PORTING_GUIDE.md` is the step-by-step recipe that produced these ten; the remaining twenty shortlisted models
are the porting queue.

## 6. The scenario DSL

The DSL (`whatifgym/dsl/SPEC.md`, JSON Schema in `whatifgym/dsl/schema.json`, version `0.1`) is the only thing an
agent produces. A scenario is one JSON object with `version`, optionally `base_model`, and any of:

| part | what it does | example |
|---|---|---|
| `data_changes` | Ordered edits to the tables or parameters. Row ops: `scale` (multiply a column by `factor`), `shift` (add `delta`), `set` (assign `value`), each over the rows matching `where` (a key value or a list of them; no `where` means every row); `add` (new complete rows); `remove` (rows matching `where`). Parameter ops: `set_param`, `scale_param`, `shift_param`. | `{"op": "scale", "table": "max_sales", "column": "max_sales", "where": {"product": "Prod5", "month": ["May", "Jun"]}, "factor": 0.8}` |
| `rules` | New constraints: the sum of `measure` over `scope` is `<=`, `>=` or `==` an absolute `value`, or `factor` times the sum of another measure (`relative_to`). | `{"measure": "make", "scope": {"product": "Prod1"}, "sense": "<=", "value": 1000}` |
| `objective` | Up to three lexicographic stages, each `min` or `max` of `original` (the model's own objective) or of the sum of a measure over a scope; earlier stages are held within relative 1e-6 while later ones are optimised. | `[{"sense": "max", "measure": "original"}, {"sense": "min", "measure": "store"}]` |
| `fixed_decisions` | Fix every variable of a measure inside a scope to a value. | `{"measure": "make", "scope": {"month": "Jan", "product": "Prod3"}, "value": 100}` |
| `ask` | Instead of all of the above, one clarifying question to the planner. Must stand alone. | `{"version": "0.1", "ask": "Which product do you mean?"}` |

Validation (`validate.py`) has two stages so that errors are actionable: the JSON Schema catches shape errors
(unknown op, missing field, `ask` next to other parts), then the semantic pass checks against the actual model —
table and column exist, `where` names key columns with values that exist in the data, a `set` on a non-numeric
column is refused, `add` rows have exactly the table's columns and a new key, `remove` does not empty a table,
measures and scope dimensions exist, parameters exist. Each error is `{"path": "/data_changes/0/where/product",
"message": "..."}`. `whatifgym/dsl/examples/` holds ten valid worked examples and `tests/dsl_bad/` twenty-two
planted bad ones that must be rejected with the expected message.

## 7. Oracle and scoring

`solve_scenario()` returns a `ScenarioResult`: `status` (`optimal`, `infeasible`, `unbounded`, `not_solved`,
`time_limit`, `error`, `invalid`, `ask`), `objective`, `stage_values`, `kpis`, `decisions` (optional), model sizes,
timings, `scenario_hash` (sha256 of the canonical JSON, used for de-duplication) and `validation_errors`.

`scoring.compare_results(reference, candidate, kpi_keys)` matches when the statuses agree and, for optimal results,
the objective and every KPI in `kpi_keys` agree within relative tolerance `REL_TOL = 1e-3` (absolute 1e-6 near
zero; nested KPI dicts and lists are compared element-wise). `scoring.score()` turns that into the reward in the
glossary. Because results are compared and not text, `scale` by 0.8 and `set` to the resulting numbers score the
same, as do `set machines_down 0` and `remove` the row — the frontier baseline showed both in practice.

## 8. The environment

`WhatIfEnv(tasks)` implements the usual `reset(task) -> obs` and `step(action) -> (obs, reward, done, info)`.

The observation deliberately follows the OptiGuide stance: the agent sees **structure, not numbers**. It contains
the model title and `description.md`, the full `schema.json`, `index_sets` (the key values of every dimension),
`table_keys` (which rows exist in each table — keys only, so the agent can decide between `set` on an existing row
and `add` of a new one), the parameter names, the measures and their dimensions, the DSL JSON Schema, two worked
examples, the planner's question, the dialogue so far and `turns_left`. It never contains table values, so the
agent cannot shortcut the task by reading the answer off the data.

Actions are `{"type": "ask", "text": "..."}` — the simulated planner answers from the task's `clarification` if
the task is under-specified and otherwise says the question is clear — or `{"type": "scenario", "scenario":
{...}}`, which ends the episode: the oracle solves the scenario and the scorer compares it with the reference. A
bare DSL object is also accepted as an action. An episode lasts at most three turns. `info` carries the full score
breakdown (`correct`, `valid_dsl`, `asked`, `route_correct`, notes) and any validation errors, so a training loop
can give shaped feedback.

## 9. Task families and the generated task files

### How a family generates tasks

`TaskFamily.__init__` solves the base model once with decisions kept, so templates can read the base plan
(`ctx.measure_sum("make", {"product": "Prod1"})`, `ctx.dim_values(...)`), the data, the schema labels
(`ctx.label("column", "max_sales", "max_sales")` → "market limit (units)"), the editable numeric columns, the
numeric parameters and their bounds, and which tables are *entity* tables (see below). `generate(n, seed)` then
draws templates deterministically and keeps a candidate only if all of the following hold:

| filter | why |
|---|---|
| the gold scenario validates | a template bug must fail loudly, not produce unsolvable tasks |
| the model builds and solves to `optimal` | a model may reject edited data in `build()` (e.g. two skill levels with the same ordinal); such candidates are skipped and counted in `family.skipped` |
| the scoring KPIs move by more than 3 × REL_TOL versus the base plan | otherwise the empty "nothing changes" scenario would be scored correct — a leak the noop agent would exploit |
| the reference is identical on a second open solver (SCIP or CBC) | the reward must not depend on which solver the oracle happens to use |
| the scenario hash is new | no duplicates within a file |
| combos ≤ 30 % of the file | keeps the difficulty mix honest on models where single edits rarely change the objective |
| wall-time budget (`max_seconds`) | the column-enumerated wedding model needs seconds per solve |

Task ids are `<model>-<family>-<seed>-<index>`; the split is a hash of the id.

### Family 1: `data_change`

The planner changes one or two input numbers; the answer is the corresponding data edit. For `factory_planning`
there are eleven specific templates in natural planner language (demand up or down for some months, zero demand,
a market cap, extra machines down for maintenance, maintenance cancelled, buying or retiring a machine, a margin
change, a process-time change, parameter changes such as three shifts or no end-of-horizon stock). Every other
model uses six generic templates driven by the schema labels:

| template | example question |
|---|---|
| `g_scale_column` | What if the ore quality for mine Mine2 is 25% higher? |
| `g_set_column` | Assume the yearly royalty of mine Mine3 is now 8000000. |
| `g_scale_all_rows` | Every minimum output per unit in the thermal generator types table falls by 10%. Effect? |
| `g_param` | What if the oil storage cost is doubled? / Assume the storage limit becomes 200. |
| `g_remove_row` | Suppose guest P drops out entirely (delete that guest and re-plan). |
| `g_add_row` | What if a new item 'new_item' is added with item weight 36 and item value 45? |

Rows are only added or removed on **entity tables**: a single key that no other table uses or refers to, no
`order` column, no share column, at least three rows (items, bins, guests, mines, thermal generator types). Removing
a row of a fact table keyed by another table's entities ("delete the January market limit of Prod1") would have a
silent default semantics inside the model and is therefore never generated. Structural numeric columns are marked
`"editable": false` in the schema and never edited (a skill level's ordinal, the hours of a period that partition
the day, a unit's on/off state at the start of the day, a guest's rank). Parameters that are shares or rates stay
within [0, 1]; `"min"`/`"max"` hints in the schema keep e.g. the wedding table size at most six, because every
candidate table is a column.

### Family 2: `new_limit`

The planner adds a constraint the model never had; the answer is one or more rules. Values are taken from the base
plan so the limit binds: a cap below what the plan currently does, a floor above it (`CAP_FACTORS` 0.5–0.9,
`FLOOR_FACTORS` 1.1–1.5), rounded to numbers a planner would say (whole units for integer measures). Eight specific
templates exist for `factory_planning` (total production cap, cap over some months, sales floor, stock cap in a
month, total stock cap, per-month cap on every month, minimum run every month, two products together) and three
generic ones:

| template | example question |
|---|---|
| `g_cap_measure_scope` | Add a limit: the units sold, summed over everything with month = Feb, must stay at or below 1100. |
| `g_floor_measure_scope` | What if the total thermal output (MW) for period 09-15 must be at least 31600? |
| `g_cap_measure_total` | An overall cap of 1550 applies to the cars rented out in total. |

0/1 measures over thousands of enumerated columns (the wedding tables) are not planning quantities and are
excluded, which is why `wedding_seating` has no `new_limit` file; `bin_packing` has only four such tasks because
its objective, the number of bins used, almost never moves under a single rule.

### The task files

| file | tasks | easy / medium / hard | train / dev / test |
|---|---|---|---|
| `tasks/factory_planning/data_change_v0.jsonl` (**frozen**) | 60 | 28 / 16 / 16 | 48 / 5 / 7 |
| `tasks/factory_planning/new_limit_v0.jsonl` | 20 | 5 / 6 / 9 | 13 / 4 / 3 |
| `tasks/factory_planning_2/data_change_v0.jsonl` | 20 | 8 / 7 / 5 | 13 / 2 / 5 |
| `tasks/factory_planning_2/new_limit_v0.jsonl` | 20 | 8 / 9 / 3 | 16 / 2 / 2 |
| `tasks/food_manufacture/data_change_v0.jsonl` | 20 | 7 / 7 / 6 | 16 / 1 / 3 |
| `tasks/food_manufacture/new_limit_v0.jsonl` | 20 | 3 / 13 / 4 | 14 / 4 / 2 |
| `tasks/mining/data_change_v0.jsonl` | 20 | 5 / 11 / 4 | 13 / 6 / 1 |
| `tasks/mining/new_limit_v0.jsonl` | 20 | 8 / 8 / 4 | 15 / 2 / 3 |
| `tasks/manpower_planning/data_change_v0.jsonl` | 20 | 10 / 4 / 6 | 17 / 2 / 1 |
| `tasks/manpower_planning/new_limit_v0.jsonl` | 20 | 4 / 15 / 1 | 14 / 1 / 5 |
| `tasks/power_generation_hydro/data_change_v0.jsonl` | 20 | 4 / 11 / 5 | 12 / 4 / 4 |
| `tasks/power_generation_hydro/new_limit_v0.jsonl` | 20 | 8 / 6 / 6 | 17 / 1 / 2 |
| `tasks/car_rental/data_change_v0.jsonl` | 20 | 8 / 6 / 6 | 15 / 3 / 2 |
| `tasks/car_rental/new_limit_v0.jsonl` | 20 | 7 / 10 / 3 | 15 / 2 / 3 |
| `tasks/multiple_knapsack/data_change_v0.jsonl` | 20 | 5 / 11 / 4 | 10 / 4 / 6 |
| `tasks/multiple_knapsack/new_limit_v0.jsonl` | 15 | 6 / 3 / 6 | 11 / 0 / 4 |
| `tasks/bin_packing/data_change_v0.jsonl` | 20 | 2 / 12 / 6 | 13 / 2 / 5 |
| `tasks/bin_packing/new_limit_v0.jsonl` | 4 | 0 / 3 / 1 | 3 / 1 / 0 |
| `tasks/wedding_seating/data_change_v0.jsonl` | 20 | 5 / 15 / 0 | 14 / 0 / 6 |
| **total** | **399** | | |

All were generated with `python scripts/make_tasks.py --family all --model all --n 20 --seed 0`. The
`factory_planning` data-change file was generated earlier with `--n 60` and is listed in `tasks/frozen.txt`
because the frontier baseline in `results/baselines/data_change_v0/` refers to it; `make_tasks.py` refuses to
overwrite frozen files unless `--force-frozen` is given. Everything else can be regenerated identically from the
seed, and `--force` regenerates it.

## 10. Results so far

**Trivial agents** (`results/trivial_baselines.md`, `scripts/run_trivial_baselines.py`): on all 19 files and 399
tasks the oracle scores exactly 1.100, noop exactly 0.100 and ask_then_oracle exactly 0.900. Any other number would
mean a broken oracle, a broken scorer or a leaked task.

**Frontier models** (`results/baselines/data_change_v0/README.md`): on the 60 `factory_planning` data-change tasks,
Claude Sonnet answered 59/60 and Claude Opus 60/60 correctly, every answer a valid scenario, through the exact
prompt `run_baseline.py` builds (run as one fresh agent per task from exported prompt files; raw answers are in
`raw_answers/`). The single miss was a question whose wording ("maintenance is rescheduled") admitted a second
reading; the template now says "additional maintenance is scheduled", and the v0 file is kept frozen so the
published numbers stay reproducible.

What that means: the data-change family on a model whose schema is fully exposed is **saturated** for frontier
models. It is the floor check that the pipeline and the reward are sound. Difficulty has to come from the other
families (`new_limit` is the first; relative, logical and relax/remove rules, objective changes, fixed decisions,
infeasible requests, chained and under-specified questions are planned), from models held out at test time, and
from the small open models that are the eventual RL target. No frontier run has been made yet on the 339 new
tasks; `scripts/run_baseline.py --export-prompts` produces their prompts.

## 11. Running everything

### Setup

```bash
git clone https://github.com/aptgetnitin/whatifgym && cd whatifgym
./setup.sh                      # creates .venv, installs requirements.txt, runs the tests and verify_models.py
source .venv/bin/activate
```

`requirements.txt`: `pulp>=2.8,<4`, `highspy`, `pyscipopt`, `ortools`, `jsonschema`, `pytest`. Gurobi is optional
(`gurobipy` with a licence) and only ever used for cross-checks.

### Tests and verification

```bash
python -m pytest -q                       # 166 tests, about 30 s
python scripts/verify_models.py           # every model x every available solver vs reference.json (subprocess per pair)
```

### Solve a base model

```bash
python -m whatifgym.runner --model factory_planning --solver highs
python -m whatifgym.runner --model multiple_knapsack --solver cpsat
```

```python
from whatifgym import get_model

m = get_model("factory_planning")
data = m.load_data()                      # dict of CSV tables + params: the editable scenario surface
base = m.solve(data, solver="highs")      # SolveResult(status, objective, kpis, ...)
for row in data["downtime"]:              # what if every horizontal drill is down in February?
    if row["month"] == "Feb" and row["machine"] == "horiDrill":
        row["machines_down"] = 3
alt = m.solve(data, solver="highs")
print(base.objective - alt.objective, alt.kpis["machine_utilisation"])
```

### Solve a scenario, run the environment

```python
from whatifgym.oracle import solve_scenario
from whatifgym.env import WhatIfEnv
from whatifgym.tasks import load_tasks

r = solve_scenario("factory_planning", {"version": "0.1", "data_changes": [
    {"op": "scale", "table": "max_sales", "column": "max_sales",
     "where": {"product": "Prod5", "month": ["May", "Jun"]}, "factor": 0.8}]})
print(r.status, r.objective, r.kpis["profit"])

tasks = load_tasks("tasks/mining/new_limit_v0.jsonl", split="test")
env = WhatIfEnv(tasks)
obs = env.reset(tasks[0])                 # description, schema, index sets, table keys, measures, DSL schema, examples, question
obs, reward, done, info = env.step({"type": "scenario", "scenario": {"version": "0.1", "rules": [
    {"measure": "extract", "scope": {"year": "Year3"}, "sense": "<=", "value": 1950000}]}})
```

### Generate tasks

```bash
python scripts/make_tasks.py --family all --model all --n 20          # keeps existing files
python scripts/make_tasks.py --family new_limit --model mining --n 40 --seed 1 --force --check-solvers
python scripts/make_tasks.py --family data_change --model factory_planning --n 60 --force-frozen   # only if you mean it
```

The script prints the split and difficulty counts, the template mix and why candidates were dropped
(`no effect`, `infeasible`, `duplicate`, `solver disagreement`, `error: ...`, `no candidate`).

### Run agents

```bash
python scripts/run_trivial_baselines.py                                   # all files -> results/trivial_baselines.md
python scripts/run_baseline.py --tasks tasks/mining/new_limit_v0.jsonl --agent oracle   # 1.100
python scripts/run_baseline.py --tasks tasks/mining/new_limit_v0.jsonl --agent noop     # 0.100

# a frontier model through the Anthropic API (reads ANTHROPIC_API_KEY from the environment; prints token cost)
ANTHROPIC_API_KEY=... python scripts/run_baseline.py --tasks tasks/mining/new_limit_v0.jsonl --split test \
    --agent anthropic --model claude-sonnet-5-5

# the same evaluation with answers produced elsewhere: export the prompts, collect one JSON reply per task, replay
python scripts/run_baseline.py --tasks tasks/mining/new_limit_v0.jsonl --export-prompts /tmp/prompts
python scripts/run_baseline.py --tasks tasks/mining/new_limit_v0.jsonl --agent answers --answers-dir /tmp/answers --label my-model
```

`run_baseline.py` writes one JSON line per episode and prints accuracy, mean reward, validity, the share of
episodes that took the right route (ask vs. answer), accuracy by difficulty and by template, and for API runs the
token counts, latency and estimated cost.

### Local open-weight models (Ollama)

The small open models that are the eventual RL target run locally through [Ollama](https://ollama.com):

```bash
ollama pull qwen3:8b
python scripts/run_local_baselines.py --models qwen3:8b                      # every task file, resumable
python scripts/run_local_baselines.py --models qwen3:4b qwen3:14b qwen3:32b gpt-oss:20b --split test
python scripts/run_baseline.py --tasks tasks/mining/new_limit_v0.jsonl --agent ollama --model qwen3:8b --think on
```

Two things the runner enforces because they silently corrupt results otherwise: the context window is set to
`--num-ctx` (16384) on every call, since Ollama's default of 4096 tokens truncates our 4–7k-token prompts from
the front without any error; and JSON output mode is on (`--no-json-mode` to measure raw format compliance).
Thinking is off by default (`--think on`, or `low|medium|high` for gpt-oss) so runs are comparable and fast; a
model without a thinking switch is retried without the flag. Per-episode records land in
`results/baselines/local/<model>/`, raw replies in its `raw_answers/` (re-scorable with `--agent answers`), and
`scripts/summarise_results.py` builds the comparison tables — accuracy by family, difficulty, base model and
template, plus failure modes (wrong result, invalid DSL, unparseable, cut off, truncated) — in
`results/baselines/summary.md`. On an Apple-silicon laptop an 8B model takes roughly 20–40 s per task
(reading the prompt dominates), so the full 399 tasks is a few hours unattended.

## 12. Extending: new model, new family, new template

**A new base model** follows `docs/PORTING_GUIDE.md`: pick a public, permissively licensed model; put its numbers
in `data/*.csv` with a `params.csv`; write `model.py` with the class contract from section 5 (keep variable
handles in `prob._wig`, choose `SCORING_KPIS` that are unique at the optimum, declare `MEASURE_DIMS`); write
`schema.json` with labels on every table, column, parameter and measure (mark structural columns `"editable":
false`, give parameters `"min"`/`"max"` where a scenario must not go); record the original implementation's
optimum in `reference.json`; write `description.md`; register the class in `whatifgym/registry.py`; add the size
to `EXPECTED_SIZES` in `tests/test_models.py` and a `tests/test_model_<name>.py`; add a row to `ATTRIBUTION.md`
and mark the row `PORTED` in `scripts/build_base_model_table.py`. Run `scripts/verify_models.py` and
`make_tasks.py --model <name>`: the generic templates of both families work immediately from the labels.

**A new template** is a function `(rng, ctx) -> (question, scenario, slots, difficulty) | None` added to a
family's `specific_templates[model]` or `generic_templates`. `ctx` is a `FamilyContext` with the model, data,
schema, base result and helpers (`measure_sum`, `dim_values`, `label`, `dim_label`, `numeric_columns`,
`numeric_params`, `param_in_bounds`, `removable_tables`, `round_for`). Return `None` when the template does not
apply to this model; never produce a scenario that fails validation (generation raises on it, on purpose). The
question must be unambiguous given only the observation of section 8: name keys, never raw values the agent cannot
see.

**A new family** subclasses `TaskFamily` (`whatifgym/families/base.py`), sets `name`, `description`,
`specific_templates`, `generic_templates`, optionally `allow_infeasible`, overrides `combo()` for its own two-part
phrasing, and is added to `FAMILIES` in `whatifgym/families/__init__.py`. The filters in `generate()` apply
unchanged.

## 13. Conventions and known gotchas

**Lazy solver imports.** On Linux the `highspy` and `ortools` wheels both bundle `libhighs.so.1`; importing both
in one Python process fails with an `undefined symbol` error (seen with highspy 1.15.1 + ortools 9.15 on x86-64 and
arm64). whatifgym therefore never imports a solver at module level, and `whatifgym.runner.run_subprocess`,
`scripts/verify_models.py` and the CP-SAT tests run each solver family in its own interpreter. In one process use
either the PuLP solvers (HiGHS, SCIP, CBC) or CP-SAT, not both.

**PuLP is pinned to `<4`** because PuLP 4.0 (September 2026) changed the modelling API; the 3.x API is the one
most published model code uses.

**Results are compared, never text.** Any scenario that re-solves to the same status, objective and scoring KPIs
is correct. Do not add text matching to the scorer.

**Frozen task files.** A task file that a published result cites is listed in `tasks/frozen.txt` and is never
regenerated silently. New generations go to new files (`--version v1`) or to models that have none yet.

**Determinism.** Generation is seeded; splits are hashes of task ids; the trivial baselines are deterministic.
Rerunning `make_tasks.py` with the same seed reproduces a file byte for byte as long as the templates and the model
data are unchanged.

**Schema hints.** `"editable": false` on a column keeps it out of every data-change template; `"removable": false`
on a table keeps its rows from being added or removed; `"min"`/`"max"` on a parameter bound generated values;
`label` strings are what questions are built from, so keep them short noun phrases ("market limit (units)",
"number of machines installed"); measure labels of 0/1 measures should read as things that can be counted
("thermal units running").

**Scoring KPIs.** Only KPIs that are unique at the optimum belong in `SCORING_KPIS`. If `make_tasks.py` reports
`solver disagreement` often for a model, a listed KPI is probably not unique.

**Observation hides values.** `index_sets` and `table_keys` expose keys, not numbers; any new observation field must
keep that property or the data-change family becomes a look-up exercise.

## 14. Status and roadmap

| state | item |
|---|---|
| done | Repository with MIT licence and the clean-room rule; `setup.sh` installs HiGHS, SCIP (PySCIPOpt), OR-Tools |
| done | 30-model shortlist with sources, licences and measured sizes (`docs/base_models.md`) |
| done | 10 base models ported and verified on HiGHS, SCIP and CBC (33/33 pairs), 3 of them also on CP-SAT |
| done | Scenario DSL v0.1 with JSON Schema, two-stage validation, 10 worked examples, 22 planted bad scenarios |
| done | Oracle, scorer (relative 1e-3 on status, objective and scoring KPIs) and environment (ask + scenario, 3 turns) |
| done | Two task families (`data_change`, `new_limit`) with specific and schema-driven generic templates; 399 tasks in 19 files over all 10 models; trivial agents exact on every file |
| done | First frontier baseline on `factory_planning` data_change: Claude Sonnet 59/60, Claude Opus 60/60 |
| next | Small open models (Qwen3 4B–32B, gpt-oss 20B) on all 399 tasks through Ollama — the go/no-go measurement for the RL story: is there a gap to close? |
| next | Frontier baselines on the new files, through the API with pinned model ids |
| next | More families: relative rules, logical rules, relax/remove a constraint, objective change, fixed decisions, infeasible requests, chained and under-specified questions (the `ask` route is implemented; only `clarification` tasks are missing) |
| next | Port the remaining shortlisted models; hold some out for generalisation tests |
| next | Small open models as RL policies trained against the environment reward |

## 15. Licence

MIT (see `LICENSE`). Ported data values are reused under their sources' licences, listed in `ATTRIBUTION.md`.
