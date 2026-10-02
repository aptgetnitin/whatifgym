# Baseline: data_change_v0 on factory_planning (60 tasks), run 2026-10-02

| agent | episodes | accuracy | mean reward | valid DSL | route correct |
|---|---|---|---|---|---|
| oracle (gold scenario) | 60 | 1.000 | 1.100 | 1.00 | 1.00 |
| noop (empty valid scenario) | 60 | 0.000 | 0.100 | 1.00 | 1.00 |
| ask_then_oracle (one unneeded question) | 60 | 1.000 | 0.900 | 1.00 | 0.00 |
| **Claude Sonnet, via Cowork subagents** | 60 | **0.983** | 1.083 | 1.00 | 1.00 |
| **Claude Opus, via Cowork subagents** | 60 | **1.000** | 1.100 | 1.00 | 1.00 |

## Protocol

* Prompts: exactly what `scripts/run_baseline.py --agent anthropic` sends — the system prompt plus the
  observation (model description, schema, key values, table keys, parameter names, measures, DSL JSON Schema,
  two worked examples, the question); exported with `--export-prompts` and read by each agent from a file.
* Models: the Sonnet and Opus models available to the Claude Cowork session that ran this, one fresh subagent per
  task, no conversation history, no tools other than one `Read` of its own prompt file (every episode's
  tool-use count was checked; 0 of 120 used anything else). The harness adds its own system prompt around the
  benchmark prompt, and the exact model version IDs are not exposed, so these numbers are a preliminary
  "current frontier Claude" reading rather than a pinned API result. Re-run with
  `scripts/run_baseline.py --agent anthropic --model claude-sonnet-5-5` / `claude-opus-5-5` for pinned IDs.
* Scoring: `whatifgym.env.WhatIfEnv` + `whatifgym.scoring` (status, objective and the family KPIs
  `profit`, `holding_cost`, `sales_contribution` within 1e-3 relative; +0.1 valid DSL). Raw model outputs are in
  `raw_answers/<agent>/<task_id>.json`; per-episode scores in `cowork-<agent>.jsonl`.

## Reading

The data-change family is saturated for frontier models when the observation exposes table keys and two worked
examples: 59/60 and 60/60. The one Sonnet miss (`factory_planning-data_change-000-0038`, "Maintenance is
rescheduled so that 1 borer will be unavailable in January") read "rescheduled" as moving the existing March
borer outage to January, which is a defensible reading of an ambiguous question; the template now says
"Additional maintenance is scheduled" for future generations (v0 is kept frozen so these numbers stay reproducible).
Several answers also showed that equivalent spellings score identically in practice (`shift -1` vs `set 1`,
`set machines_down 0` vs `remove` the row).

What this means for the plan: the headline difficulty has to come from the other families (new limit, relative
rule, logical rule, relax/remove, objective change, fixed decision, infeasible request, chained, under-specified),
from held-out base models, and from the small open models that are the RL target; the data-change family is the
floor check that the pipeline and the reward are sound.
