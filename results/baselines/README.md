# Baseline runs

Every run goes through the same environment and scorer (`scripts/run_baseline.py`), so numbers are comparable
across models and over time. `summary.md` is regenerated from all files here by `scripts/summarise_results.py`;
`../trivial_baselines.md` holds the oracle / noop / ask-then-oracle checks that must be exact on every task file.

| run | tasks | model | result | where |
|---|---|---|---|---|
| 2026-10-02 | `factory_planning/data_change_v0` (60) | Claude Sonnet, Claude Opus (Cowork subagents, one fresh agent per task) | 59/60 and 60/60 correct, all valid DSL | `data_change_v0/` |
| 2026-10-03 | all 19 original files (399) | Qwen3 8B through Ollama, no thinking, JSON mode, 16k context, M4 Max | 314/399 = 78.7 %; data_change 86 %, new_limit 67 %; easy/medium/hard 77/86/67 %; valid DSL 89 %; 6 s/task, 40 min total | `local/qwen3-8b/` |

## Reading of the first local run (Qwen3 8B)

The gap to frontier models exists and is in the right places. On the one family where both were measured
(`factory_planning` data changes, planner-language questions) Sonnet scored 98 % and the 8B model 61 %; overall
the 8B model scored 79 %. Its 85 misses split into 45 invalid scenarios caught by the validator (a measure used as a
table name, a column used as a parameter, invented wildcards such as `"product": "*"`, `set` on a maintenance row
that does not exist instead of `add`) and 40 valid-but-wrong scenarios. The wrong ones have a clear structure:

* **a new constraint translated into an existing knob** — "no more than 180 units in stock in total at the end of
  May" became `set max_inventory 180`, "total sales capped at 6,450" became setting every market-limit cell to
  6,450, "at most 240 on short-time working in total" became the per-skill parameter (about a dozen cases);
* **arithmetic semantics** — "one of the 4 grinders is scrapped" became `scale installed by 0.8` instead of
  `shift −1`; "takes 1.4 hours per unit" became `scale by 1.4` instead of `set 1.4`; "320 machine hours a month"
  became `scale_param by 320`;
* **quantifier scope** — "never more than 420 in any single month" became one cap on the six-month total;
  "summed over everything" became a cap on a single depot pair;
* **two-part questions** — 16 of the 40; one part done, the rest padded with edits copied from the worked examples
  (`holding_cost ×2`, `max_inventory 150`, `store_target 0` appear verbatim).

Across base models the pattern is about language, not model size: 100 % on wedding seating, 93 % on food
manufacture, 92 % on bin packing (all generic, DSL-like question templates) against 61 % on factory planning
(hand-written planner language). That is the evidence behind the paraphrase stage (`scripts/paraphrase_tasks.py`)
and behind the four families added on 2026-10-03 (`relative_rule`, `objective_change`, `fixed_decision`,
`under_specified`), which target exactly the skills above.

Caveats: one model, temperature 0, one fixed prompt. A sentence in the system prompt on "a limit on a decision is a
rule, not a data edit" would move the number; the benchmark therefore keeps the prompt fixed and reports such
changes as ablations rather than tuning toward either outcome.

## Protocol notes

* Frontier numbers so far come from Cowork subagents reading the exact exported prompt, not from pinned API model
  ids; re-run with `--agent anthropic --model <id>` for the paper.
* Local models: `scripts/run_local_baselines.py --models <ollama tags>`; context is forced to 16k because Ollama's
  default of 4,096 tokens silently truncates the 4–7k-token prompts; thinking off unless `--think on`
  (`--label-suffix -think` keeps the two variants apart).
* Raw model replies are kept under `<run>/raw_answers/` so any file can be re-scored with `--agent answers`.
