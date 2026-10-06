# Scenario DSL v0.1

A scenario is one JSON object. It is the agent's whole answer to a what-if question: the environment validates
it, applies it to the base model, re-solves with an open solver and scores the result against a hidden
reference. The agent never solves anything. The machine-readable grammar is `schema.json` (JSON Schema
2020-12); this page gives the semantics and the worked examples in `examples/`.

## Shape

```json
{
  "version": "0.1",
  "base_model": "factory_planning",
  "data_changes": [ ... ],      // edits to the input tables and parameters
  "rules": [ ... ],             // new linear limits on sums of decision measures
  "objective": [ ... ],         // ordered objective stages (lexicographic)
  "fixed_decisions": [ ... ],   // decisions pinned to a value
  "relax": [ ... ],             // constraints of the base model that no longer apply
  "logic": [ ... ],             // either-or rules: at least k of several conditions hold
  "note": "free text, ignored"
}
```

A scenario must carry at least one of `data_changes`, `rules`, `objective`, `fixed_decisions`, `relax`, `logic`. The only
alternative is a clarifying question, which stands alone:

```json
{"version": "0.1", "ask": "Which product's demand rises, by how much, and in which months?"}
```

## Selectors

Two selector shapes recur. `where` picks **rows of a table** by column values; `scope` picks **variables of a
decision measure** by index dimension. In both, a value may be a scalar or a list (membership); a `where` must
name at least one column; an omitted `scope` dimension means "all".

```json
"where": {"product": "Prod5", "month": ["May", "Jun"]}
"scope": {"product": "Prod1", "month": ["Feb", "Mar"]}
```

The validator rejects a selector that matches nothing (a hallucinated entity) and a key column edited in place.

## Data changes (applied in order)

| op | fields | meaning |
|---|---|---|
| `scale` | table, column, where?, factor ≥ 0 | multiply the column of the matching rows |
| `shift` | table, column, where?, delta | add a constant to the column of the matching rows |
| `set` | table, column, where?, value | assign the value |
| `add` | table, rows | append complete rows (every column present, key not already used) |
| `remove` | table, where | delete the matching rows (the table may not become empty) |
| `set_param` / `scale_param` / `shift_param` | name, value / factor / delta | the same three edits on a scalar parameter |

Changes are validated against the model's `schema.json` (table, column and parameter names, numeric types) and
against the data as it stands after the earlier changes in the same scenario.

## Rules

A rule bounds the **sum** of a decision measure over a scope. Measures are the model's variable families
(`factory_planning`: `make`, `store`, `sell`, each indexed by `month` and `product`).

```json
{"measure": "make", "scope": {"product": "Prod1", "month": ["Feb", "Mar"]}, "sense": "<=", "value": 500}
{"measure": "sell", "scope": {"product": "Prod2"}, "sense": ">=",
 "relative_to": {"measure": "sell", "scope": {"product": "Prod1"}}, "factor": 1.0}
```

The first reads `make[Feb,Prod1] + make[Mar,Prod1] <= 500`; the second `sum sell[.,Prod2] >= 1.0 * sum sell[.,Prod1]`.
`sense` is one of `<=`, `>=`, `==`. A rule carries either `value` or `relative_to` + `factor`, never both.

## Objective stages

`objective` is an ordered list of up to three stages. Stage 1 is optimised first; each later stage is optimised
with every earlier stage held at its optimum (relative tolerance 1e-6). `"measure": "original"` is the model's
own objective; any other measure means the sum of that measure over the scope.

```json
"objective": [{"sense": "max", "measure": "original"}, {"sense": "min", "measure": "store"}]
```

The result's `objective` is the value of the last stage; `stage_values` lists all of them.

## Fixed decisions

```json
{"measure": "make", "scope": {"product": "Prod3", "month": "Jan"}, "value": 100}
```

Every variable of the measure inside the scope is fixed to the value (lower and upper bound). To pin a *sum*
instead, use a rule with `==`.

## Relaxations

A relaxation removes constraints of the base model. `constraint` names a constraint family from the model
schema (`factory_planning`: `balance[month, product]`, `end_stock[product]`, `capacity[month, machine]`); `scope`
picks members of the family by its index dimensions, and an omitted dimension means "all".

```json
"relax": [{"constraint": "capacity", "scope": {"month": "Mar"}}]
```

This lifts the machine-hours limit for every machine in March only. The validator rejects an unknown family, a
dimension the family does not have, a value that is not a key, and a scope that selects no constraint. A family
whose dimensions are not key columns of the data cannot be relaxed; change the data or add a rule instead.

## Logical rules

A logical rule says that at least `at_least` of the conditions in `of` hold. A condition bounds the **sum** of a
decision measure over a scope, like a rule with an absolute `value`. Negations are written out:

| planner says | logic |
|---|---|
| A or B (either-or) | `at_least` 1 of [A, B] |
| never both A and B | `at_least` 1 of [not A, not B], e.g. `make <= 0` for "no production" |
| make none, or at least q | `at_least` 1 of [`sum <= 0`, `sum >= q`] |
| if A then B | `at_least` 1 of [not A, B] |
| at most k of n may be active | `at_least` n − k of [`x_i <= 0`] |

```json
"logic": [{"at_least": 1, "of": [
  {"measure": "make", "scope": {"product": "Prod1", "month": "Mar"}, "sense": "<=", "value": 0},
  {"measure": "make", "scope": {"product": "Prod1", "month": "Mar"}, "sense": ">=", "value": 300}]}]
```

The oracle adds one binary per condition and a big-M constraint whose M is the exact range of the condition's
sum over the LP relaxation of the scenario, so no feasible plan is cut off. A condition whose sum has no finite
bound is an error: bound the measure with a rule first.

## Results and scoring

The oracle returns `status` (optimal | infeasible | unbounded | not_solved | time_limit | invalid | ask),
`objective`, `stage_values`, `kpis` (the model's planner-facing numbers), `decisions` (non-zero variables) and
sizes. The scorer compares status, objective and the task family's KPIs within relative tolerance 1e-3, so two
scenarios that spell the same change differently (`scale` by 0.8 versus `set` to the resulting numbers) earn
the same reward. Validation errors come back as `{"path", "message"}` pairs an agent can act on.

## Worked examples

`examples/01_demand_scale.json` and `examples/02_new_limit_rule.json` are the two shown to agents in the
environment observation; the remaining files cover every construct and are all validated in the test suite,
together with 26 planted invalid scenarios in `tests/dsl_bad/` that the schema must reject.
