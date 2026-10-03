# Food Manufacture I

**Domain:** production planning · **Type:** LP · **Size:** 96 variables, 70 constraints · **Sense:** maximise profit

A manufacturer buys five raw oils, refines them and blends them into one food product over six months (January to
June). Two oils are vegetable (VEG1, VEG2) and three are non-vegetable (OIL1, OIL2, OIL3). Purchase prices vary
by oil and by month. Vegetable and non-vegetable oils are refined on separate lines, which can process 200 and 250
tons a month. Refining loses no mass, so each month's food output equals the tons of oil refined. The product sells
for 150 USD/ton, and its hardness must lie between 3 and 6. Hardness blends linearly; the oils' hardness values are
VEG1 8.8, VEG2 6.1, OIL1 2.0, OIL2 4.2 and OIL3 5.0. Raw oil can be stored at 5 USD per ton per month, up to 1,000 tons
of each oil; refined oil and the food product cannot be stored. Each oil starts January with 500 tons in stock,
and the plan must end June with 500 tons of each.

Decisions: per month and oil, how much to **buy**, **consume** (refine into the blend) and **store**; per month,
how much food to **produce**.

Constraints:
* stock balance per oil and month (opening stock + purchases = oil refined + closing stock);
* end-of-horizon stock target;
* refining capacity per line and month;
* lower and upper hardness bounds on each month's blend;
* mass balance (oil refined = food produced);
* storage capacity (a bound on each storage variable).

The objective is sales revenue minus purchase cost minus storage cost. Stock held at the end of every month is
charged, including the closing stock in June.

Reference optimum (original Gurobi notebook): **107 842.59**. Every optimal plan runs both refining lines at
capacity in every month, making 450 tons of food a month (2,700 tons in total). Purchase timing and the OIL2/OIL3
mix have alternative optima, so the split between purchase cost and storage cost is not unique. The notebook says
so too.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `purchase_prices` | VEG1 costs 20 % more in June. All non-vegetable oils are 10 % cheaper in March. OIL2 cannot be bought in February (remove the row; a missing price means no purchase that month). |
| `oils` | A different VEG2 supply is harder (6.5). A new vegetable oil becomes available (add an `oils` row and its six `purchase_prices` rows; it inherits the per-oil stock parameters). |
| `months` | The horizon is extended or shortened (add or remove a month, with its prices). |
| `params` | The product price falls to 130. The vegetable line is upgraded to 250 tons a month. Storage cost doubles. The warehouse holds only 600 tons of each oil. The hardness band tightens to 4–5.5. We start with 600 tons of each oil, or may end June with no stock. |

Rules and fixed decisions address the measures `buy`, `consume` and `store` (by `month`, `oil`) and `produce`
(by `month`). Examples: "buy at most 500 tons of OIL2 over the horizon"; "make only 300 tons in January".

## Port notes

* **Same rows as the original.** The notebook generates its `Balance` constraints with `if month != month[0]`.
  The test was meant to be `months[0]`; as written it is always true. So the family also contains a January row
  for each oil: `store[Jun] + buy[Jan] = consume[Jan] + store[Jan]`. Combined with the initial balance, this row
  forces June's closing stock to equal the initial stock. The port keeps these five rows as `horizon_closure`,
  with right-hand side `final_stock - initial_stock`. That is 0 in the notebook data, so all 70 rows (278 nonzeros)
  are identical to the original's. Written this way, the rows are implied by `initial_balance` and `end_stock`
  for any data. Otherwise, a what-if that changes only the opening stock or only the closing target would be
  infeasible.
* **Storage limit.** The notebook's text gives a limit of 1,000 tons per oil, but its code omits it. The port
  imposes the limit as an upper bound on `store`. Bounds are not rows, and the limit does not bind at the optimum.
* **Purchase cost.** The notebook's written formulation charges purchase prices on `consume`, but its code charges
  them on `buy`. The port follows the code.
* **Missing data.** A `(month, oil)` pair with no purchase price cannot be bought in that month. An oil whose
  `category` is neither `veg` nor `nonveg` cannot be refined. `initial_stock`, `final_stock` and
  `storage_capacity` apply to every oil, including oils added in a scenario.

Source: Gurobi `modeling-examples/food_manufacturing/food_manufacture_1.ipynb` (Apache-2.0), after
H. P. Williams, *Model Building in Mathematical Programming*, 5th ed., example 1. Only the published data values
are reused; no code is copied.
