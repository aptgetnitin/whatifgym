# Mining

**Domain:** production planning · **Type:** MILP · **Size:** 65 variables (40 binary), 71 constraints · **Sense:** maximise discounted profit

A mining company plans five years of operations for an area with four mines. Each year it may work at most three
of them. A mine that is kept open pays a yearly royalty whether or not it is worked; once a mine is closed it can
never reopen, and no more royalties are due. Each mine has a yearly extraction limit and an ore grade. The ore
extracted in a year is blended, and the blend must have exactly that year's target grade (grades mix linearly by
tonnage). Blended ore sells at a fixed price per ton, and revenue and royalties in later years are discounted at an
annual rate (10 %, so year *n* counts at 1.1^-(n-1)).

Decisions per year and mine: how many tons to **extract**, whether to **operate** (work) the mine, and whether to
keep it **open**; per year, the tons of **blend** sold.

Constraints: at most `max_mines` mines worked per year; blended grade equals the year's target; tons blended equal
tons extracted; a mine extracts only when worked, up to its capacity; a mine is worked only while open; a closed mine
stays closed.

Objective: discounted revenue from blended ore minus discounted royalties on open mines. The notebook's printed
formula multiplies royalties by tons extracted, but its problem statement and its code charge royalties per open
mine-year; the reference optimum comes from the code, which is what is modelled here.

Reference optimum (original Gurobi notebook): **146 861 974.36** USD. All four mines stay open in years 1–4 and
Mine4 closes after year 4; 26.09 million tons of blended ore are sold over the horizon.

Identifiers: `Mine1`–`Mine4` and `Year1`–`Year5` are the notebook's mines 1–4 and years 1–5. The notebook's
`Working` and `Available` variables are the `operate` and `open` measures here. The discount rate, hard-coded in
the notebook, is the parameter `discount_rate`; a year's discount exponent is its `order` minus 1.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `mines` | Mine1's royalty rises to 6 million a year. Mine3 can be expanded to 1.6 million tons a year. Mine2's ore grade drops to 0.6. Mine4 is not available at all (remove the row). A fifth mine with royalty 3 million, capacity 1 million tons and grade 1.2 becomes available (add a row). |
| `years` | The year-3 quality target is relaxed from 1.2 to 1.0. A sixth year with target 0.9 is added to the horizon. |
| `params` | The ore price falls to 9 USD per ton. Only two mines may be worked each year. The discount rate rises to 15 %. |

Decision rules also apply directly to the measures, for example "Mine4 must stay open through Year5"
(fix `open` for Mine4 in Year5 to 1) or "Mine3 may be worked in at most three years" (a rule on `operate` for
Mine3).

Source: Gurobi `modeling-examples/mining/mining.ipynb` (Apache-2.0), after H. P. Williams, *Model Building in
Mathematical Programming*, 5th ed., example 7. Re-implemented from the published data; no code copied.
