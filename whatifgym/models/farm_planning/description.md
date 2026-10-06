# Farm Planning

**Domain:** production planning · **Type:** LP · **Size:** 131 variables, 116 constraints · **Sense:** maximise profit

A farmer plans the next five years of a 200-acre dairy farm. Today the herd is 120 head, ten of each age from
newborn to 11 years: 20 heifers and 100 dairy cows. A dairy cow has 1.1 calves a year. Half of the calves are
bullocks, sold at birth for 30 each; the other half are heifer calves, sold for 40 or raised to join the dairy herd at
two. Cows are sold at 12 for 120. Every year 5 % of the heifers and 2 % of the dairy cows die. A dairy cow's milk
earns 370 a year.

Dairy cows eat 0.6 t of grain and 0.7 t of sugar beet a year. Sugar beet grows on any acre at 1.5 t/acre; grain
grows only on 80 acres in four land groups yielding 1.1, 0.9, 0.8 and 0.65 t/acre. Both crops can also be bought
(grain 90, sugar beet 70 a ton) or sold (75 and 58 a ton). A heifer needs two thirds of an acre and a dairy cow one
acre. Labour is 10 hours per heifer, 42 per dairy cow, 4 per acre of grain and 14 per acre of sugar beet a year; 5 500
regular hours cost 4 000 a year and overtime costs 1.20 an hour. Other yearly costs are 50 per heifer, 100 per dairy
cow, 15 per acre of grain and 10 per acre of sugar beet. Housing holds 130 animals; each extra place costs 200,
financed by a 10-year loan repaid at 39.71 a year. No year may make a loss, and at the end of the plan the dairy herd
must hold between 50 and 175 cows.

The herd is tracked by age. Age 1 holds the heifers, ages 2 to 11 the dairy cows, and age 12 the cows sold that year
(they need no housing, land, labour or feed). Year 1 starts from 9.5 head of ages 1 and 2 and 9.8 of each age from 3
to 12: today's herd, one year older and net of one year's deaths. Heifer calves raised in a year are one-year-old
heifers the next year. Identifiers: `Year1`–`Year5` and `Group1`–`Group4` are the notebook's years 1–5 and land
groups 1–4.

Decisions per year: how many heifer calves to **raise** and to **sell**, the **herd** by age, tons of **grain grown**
on each land group and of **sugar beet grown**, tons of grain and sugar beet **bought** and **sold**, **overtime**
hours, **extra housing** places, and the year's **profit**.

Constraints per year: housing (heifers and dairy cows fit the existing places plus all places added so far); grain
and sugar beet feed (eaten = grown + bought - sold, or less); grain per land group at most yield x area; land
(sugar beet acres + heifers + grain acres + dairy cows within the farm's acres); labour (hours needed within the
regular hours plus overtime); ageing (calves raised become heifers and heifers become dairy cows at the heifer death
rate; dairy cows age one year at the cow death rate); calving (heifer calves born = raised + sold); and the yearly
profit (milk, calves, cows sold and crops sold, less feed bought, labour, upkeep, crop costs and the loan repayments
due that year). Once: the dairy herd of the last year lies within the final limits, and the first year's herd equals
the initial herd. The yearly profit has the lower bound `min_yearly_profit` (0).

Objective: the sum of the yearly profits, less the loan repayments that will still be due after the last year for
the housing added during the plan, so that housing added late costs as much as housing added early. Housing added
in year t is repaid inside the plan in years t to 5, which leaves `loan_term_years - (6 - t)` repayments (the
notebook's t + 4).

Reference optimum (original Gurobi notebook): **121 719.17** (121 719.1728613383). The optimal plan is unique: no
extra housing and no overtime; 22.8 heifer calves raised in Year1 and 11.6 in Year2, none later, and 236.9 sold;
grain grown on Group1 at its 22 t limit every year (plus 2.8 t on Group2 in Year3) and 33 to 40 t bought a year;
91 to 131 t of sugar beet grown a year and the surplus sold; 92.5 dairy cows in Year5. Yearly profit: 21 906.06,
21 888.70, 25 816.06, 26 825.77 and 25 282.59.

Formulation notes. The port has the original's columns, rows (same order, senses and right-hand sides), bounds and
objective coefficients, 734 nonzeros, with these differences in representation:
* **Labour in hours.** The notebook counts labour in hundreds of hours. Here the labour rows are the original's
  times 100, and `overtime` is in hours at 1.20 an hour rather than in hundreds of hours at 120. The feasible set
  and the optimum are unchanged.
* **Final herd range.** The notebook adds the 50–175 limit as a Gurobi range constraint, which Gurobi stores as
  `final dairy cows + RgFinal_dairy_cows = 175` with the range variable in [0, 125]. The port writes the same row
  and column explicitly: `final_dairy_cows_headroom` (not a measure) is the 131st variable.
* **Hard-coded values made data.** These numbers are fixed in the notebook's code and are parameters here:
  1 acre per dairy cow (`cow_acres`), half the calves heifers (`heifer_calf_share`), the 10-year loan behind the
  objective's t + 4 (`loan_term_years`), and the zero lower bound on profit that forbids a loss-making year
  (`min_yearly_profit`).
* **Generalisations.** Neither changes the published model. A housing loan is repaid for `loan_term_years` years
  only (all five planning years here). A crop with zero yield occupies no land and none of it is grown, rather than
  dividing by zero.

Model behaviour inherited from the original, worth knowing before asking a what-if:
* Trading is unlimited. A sale price above the purchase price of the same crop (grain above 90, sugar beet above
  70 at the published prices) makes buying to resell pay without limit, and the LP is unbounded.
* The first year's herd is fixed. A farm too small for it is infeasible: at the published rates its 97.7 dairy
  cows and 9.5 heifers need 104.03 acres.
* `housing_installment` is the yearly repayment per place, given directly (the book's 39.71; the annuity formula at
  15 % over 10 years gives 39.85). It is not recomputed when `loan_term_years` changes.
* The yearly profit is a cash flow after loan repayments, so a cap on it can be met by wasting money in many
  ways. Such rules leave almost every plan KPI with alternative optima. The scored KPIs are horizon totals, which
  are otherwise unique. `profit_by_year` and `dairy_cows_by_year` are reported but not scored, because a rule that
  caps a total over several years lets the plan shift it between years at the same profit.

## What-if surface

| Table / param | Typical scenario questions |
|---|---|
| `land_groups` | Drainage lifts Group1 to 1.3 t/acre; Group2 can no longer grow grain (remove the row); 25 more acres become suitable for grain at 1.0 t/acre (add a row); a drought cuts every grain yield by 20 %. |
| `params`: prices | Milk earns 330 per cow; grain costs 110 a ton; heifer calves fetch 60; cows sold at 12 fetch 150; sugar beet sells for 50. |
| `params`: herd | Cow mortality doubles; 1.2 calves per cow; sexed semen makes 70 % of the calves heifers. |
| `params`: land, labour, housing | The farm leases 20 more acres; regular labour covers 6 000 hours; overtime costs 1.50 an hour; housing for 150 animals, or only 100, so that places must be added on loan; a cow needs 1.2 acres. |
| `params`: policy | The final dairy herd must hold at least 100 cows (or at most 90); every year must make at least 22 000. |
| `years`, `ages` | Structural: the horizon order and the initial herd are not what-if inputs. |

Measures for rules, fixed decisions and objective stages: `herd` by (`year`, `age`); `grow_grain` by (`year`,
`land_group`); `raise_heifers`, `sell_heifers`, `grow_beet`, `buy_grain`, `sell_grain`, `buy_beet`, `sell_beet`,
`overtime`, `extra_housing` and `yearly_profit` by `year`. Examples: raise at least 15 heifer calves every year;
buy at most 30 t of grain in any year; build no extra housing; grow no grain on Group4; at least 23 000 profit in
Year1.

Source: Gurobi `modeling-examples/farm_planning/farm_planning.ipynb` (Apache-2.0), after H. P. Williams, *Model
Building in Mathematical Programming*, 5th ed., example 8. Re-implemented from the published data; no code copied.
