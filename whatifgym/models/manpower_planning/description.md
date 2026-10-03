# Manpower Planning

**Domain:** scheduling · **Type:** LP · **Size:** 72 variables, 30 constraints · **Sense:** minimise redundancies

A company is reorganising. New machinery and an expected downturn reduce its need for unskilled labour and raise
its need for semi-skilled and skilled labour over the next three years. Today it employs 2 000 unskilled,
1 500 semi-skilled and 1 000 skilled workers, and it must cover a required headcount for each skill level in each
year. Workers leave naturally: 25 / 20 / 10 % of new recruits in their first year and 10 / 5 / 5 % of experienced
staff every year. Each year the company can recruit up to 500 / 800 / 500 workers, retrain up to 200 unskilled
workers to semi-skilled ($400 each) and semi-skilled workers to skilled up to a quarter of the skilled workforce
($500 each), and downgrade workers to a lower level (half of them then leave). It may also employ up to
150 workers in total above requirements (overmanning, $1 500 / 2 000 / 3 000 per worker-year), put up to 50
workers of each level on short-time working (half as productive; $500 / 400 / 400 per worker-year), or make
workers redundant ($200 per unskilled worker, $500 otherwise). Skill levels are `unskilled`, `semi_skilled` and
`skilled` (the notebook's s1, s2, s3); years are 1, 2, 3.

Decisions per year and skill level: how many workers to **recruit**, **retrain** (to a higher level),
**downgrade** (to a lower level), make **redundant**, put on **short_time** working and keep **overmanned**,
and the resulting **workforce**.

Constraints: a workforce balance per year and level (last year's workforce, or the opening strength in year 1,
net of attrition, plus recruits and workers retrained or downgraded into the level, minus workers moved out and
redundancies); retraining limits (a fixed number of places per year plus a share of the destination level's
workforce); the overmanning allowance per year; and the requirement per year and level (employed = required +
overmanned + the output lost to short-time working). Recruitment and short-time limits are variable bounds.

Objective: minimise total redundancies, the notebook's first objective. The notebook's second objective,
minimise total cost (retraining + redundancy + short-time + overmanning), is not the built objective. It is
available as `ManpowerPlanning.cost_expression(prob, data)` and is reported as the `total_cost` KPI.

Reference optimum (original Gurobi notebook): **841.80** redundancies (841.796875), all of them unskilled:
443.0 in year 1, 166.3 in year 2 and 232.5 in year 3. Alternative objective (minimum cost, same notebook):
**498 677.29**, with 1 423.7 redundancies.

The minimum redundancy is unique, and so is its split by year and by skill level. The rest of the plan is not.
Across alternative optima the plan's total cost ranges from 1 441 389.80 (the plan the notebook reports, which
is the cheapest) to 1 696 250.00, and recruitment, retraining, downgrading and short-time working vary too.
Cost rates enter neither the redundancy objective nor any constraint, so editing them changes only the cost
KPIs, never the optimum, unless the cost objective is used.

Formulation notes. The port has the original's columns and rows one for one, with three changes that leave the
feasible set and the optimum unchanged:
* The ban on retraining unskilled workers directly to skilled (`== 0` in the notebook) is the limit row
  `<= 0`, taken from the `retraining` table, so it can be relaxed as data.
* The requirement row counts short-time workers with coefficient `1 - short_time_productivity`, the output each
  one leaves uncovered. At the published productivity of 0.5 this is the notebook's coefficient of 0.5, and
  it stays correct when the productivity is edited.
* The notebook's move variable runs over every pair of skill levels, so 9 of its 72 columns are same-level moves
  (unskilled to unskilled, and so on) that enter no constraint. They are kept as inert `same_level` columns with a
  zero objective coefficient and are not part of any measure.

## What-if surface

| Table / param | Typical scenario questions |
|---|---|
| `requirements` | We need 2 200 skilled workers in year 3; 700 unskilled workers are still needed in year 2; we can recruit 1 000 semi-skilled workers a year. |
| `skills` | First-year attrition of unskilled recruits falls to 20 %; experienced skilled attrition doubles; we start with 200 more semi-skilled workers. |
| `retraining` | The training centre takes 300 unskilled trainees a year; semi-skilled-to-skilled retraining is capped at 20 % of the skilled workforce; allow 100 direct unskilled-to-skilled retrainings a year; retraining costs rise 10 %. |
| `costs` | Redundancy pay for skilled workers rises to $800; overmanning costs fall 25 % (cost KPIs only, unless the cost objective is used). |
| `years` | Plan only two years; add a fourth year (with its `requirements` rows). |
| `params` | The overmanning allowance is 250; up to 100 workers per level may go on short time; short-time workers are 60 % productive; only 30 % of downgraded workers leave. |

Measures for rules, fixed decisions and objective stages: `recruit`, `redundant`, `short_time`, `overmanned`,
`workforce` by (`year`, `skill`), and `retrain`, `downgrade` by (`year`, `from_skill`, `to_skill`). Examples:
no downgrading at all; at most 800 skilled recruits over the three years; minimise recruitment among the
minimum-redundancy plans.

Source: Gurobi `modeling-examples/manpower_planning/manpower_planning.ipynb` (Apache-2.0), after
H. P. Williams, *Model Building in Mathematical Programming*, 5th ed., example 5. Re-implemented from the
published data; no code copied.
