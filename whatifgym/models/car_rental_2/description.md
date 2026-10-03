# Car Rental 2

**Domain:** revenue / resource planning · **Type:** MILP · **Size:** 294 variables (5 binary), 118 constraints · **Sense:** maximise weekly profit

This is Car Rental 1 with an investment decision on top. A car rental company rents one type of car from four
depots (Glasgow, Manchester, Birmingham, Plymouth), Monday to Saturday. Each depot has an estimated demand for every
trading day, and the company does not have to meet all of it. Rentals last one, two or three days (55 %, 20 % and
25 % of rentals). A car can be returned to any depot: for each rental depot a fixed share of its cars comes back to
each depot. The price depends on the rental length and on whether the car comes back to the depot it left from, and
every rental has a marginal cost. Ten per cent of returned cars are damaged. The customer then pays a $100 excess,
and the car goes to a repair depot: one day in transit unless it is already there, then one day in repair, after
which it can be rented the next morning. Manchester can repair 12 cars a day and Birmingham 20; Glasgow and
Plymouth have no workshop today. Undamaged cars can be moved between depots at a per-car cost and arrive the next
morning. Owning a car costs $15 a week. The plan is a weekly steady state, with the same number of cars at each depot
on the same day of every week, so the day before Monday is Saturday.

Repair capacity is the binding resource, because every rental brings back a damaged car with probability 10 %. The
company can therefore expand its workshops. There are five all-or-nothing options of 5 cars a day each, with a fixed
weekly cost that includes the loan interest: Birmingham +5 for 18 000 and a further +5 for 8 000; Manchester +5 for
20 000 and a further +5 for 5 000; and Plymouth, which has no workshop, +5 for 19 000. A further expansion needs the
one before it at the same depot, and at most three options in total may be carried out. The model chooses the
expansions, the fleet size and where the cars are each morning.

Decisions per day and depot: **rentals**, the undamaged and damaged cars at the depot in the morning
(**undamaged_stock**, **damaged_stock**), the cars kept there overnight (**undamaged_left**, **damaged_left**) and
**repairs**. Per day and lane: **undamaged_transfers** and **damaged_transfers**. Overall: the **fleet_size**. Per
expansion option (depot and step): the 0/1 decision **expand**.

Constraints:
* Undamaged-car balance at every depot and day: returns + arrivals + yesterday's repairs + cars kept overnight
  = rentals + transfers out + cars kept.
* Damaged-car balance: returns + cars kept overnight (+ arrivals, at a repair depot) = repairs + transfers out
  + cars kept.
* Repair capacity at a repair depot each day: repairs at most the base capacity plus the capacity added by every
  expansion option carried out there.
* A further expansion needs the expansion before it; at most `max_expansions` options in total.
* Demand, as a variable bound.
* Fleet count: the cars still on rent plus all cars at the depots on Wednesday morning.

Reference optimum (original Gurobi notebook): **132 341.47** a week, with 983.35 cars (983 rounded) and 2 820
rentals a week (86.3 % of demand). The plan expands Manchester twice (+10 cars a day, 25 000 a week) and Plymouth once
(+5, 19 000 a week), and leaves Birmingham alone: three options, which is the limit, at 44 000 a week. All three
workshops then work at capacity, which caps rentals at 2 820 (282 repairs a week ÷ 10 % damaged). The next best plan
is Manchester's two expansions alone, 616 a week lower. Without any expansion the plan earns 120 067.60. With a limit
of four options the company would add Birmingham's two options instead of Plymouth's and earn 138 102.82.

## Notes on the port

* The variables, constraints and coefficients are the original's. All 118 rows, the 174 objective coefficients, the
  bounds and the five binaries were compared with the LP file that the original notebook code writes. The repair
  variables of the depot without a workshop and without an option (Glasgow, upper bound 0) are also written into
  its balance rows, so PuLP keeps them. The feasible set does not change.
* Values the original hard-codes are derived from the data:
  * A repair depot is a depot with a positive base repair capacity or an expansion option that adds capacity. The
    original names Manchester, Birmingham and Plymouth. A depot that is neither (Glasgow) has its repairs fixed at 0.
  * The fleet-count factors 0.25 and 0.45 come from the rental-length mix.
  * The expected damage fee of 10 per rental is `damaged_share × damage_excess`.
  * The undamaged share is `1 − damaged_share`.
  * The expansion options are rows of `expansion_options` (depot and step). The original's two orderings
    (Birmingham 2 needs Birmingham 1, Manchester 2 needs Manchester 1) follow from the step order. An option whose
    depot is missing from `depots` is ignored.

  The original's same-depot transfer costs (0.001) are never used and are left out.
* Two damaged-car flows are kept as in the original, and unlike in Car Rental 1 the optimum uses both. A damaged
  transfer out of a repair depot can only go to a depot that is not a repair depot, and that depot does not receive
  it, so the cars leave the plan. A damaged transfer between two repair depots is received but never leaves the
  sender, so the cars appear. Plymouth counts as a repair depot because it has an option, even though it cannot repair
  anything until it is expanded, so its damaged cars cannot be forwarded to Manchester or Birmingham. At the optimum
  11.46 damaged cars a week leave through Plymouth to Glasgow and the same number appear at Birmingham through the
  Manchester to Birmingham lane. This is also why the no-expansion plan (120 067.60) is worth less than Car Rental 1
  (121 160.21), where Plymouth is a depot without a workshop. With Plymouth's option removed and no expansion
  allowed, this model reproduces Car Rental 1 exactly.
* Because the original's damaged-car flows depend on which depots are repair depots, an edit that changes that set
  changes the flows and can move profit the "wrong" way. Withdrawing Plymouth's option turns Plymouth into a depot
  without a workshop and raises profit to 133 136.73. Giving Glasgow a workshop or an option lowers profit (129 548.17
  with a 10-car workshop, 92 607.52 with a declinable option) because Glasgow is then no longer the one depot that can
  hand damaged cars on. Edits to capacities, costs and the other tables do not have this effect.
* The optimum and the expansion plan are unique. All 14 allowed combinations of options were solved with the
  expansions fixed. The daily plan has alternative optima, but profit, rental contribution, transfer cost, fleet size,
  expansion cost and the capacity added at each depot are the same in every optimal plan.
* Return shares and rental-length shares are used exactly as given and are not renormalised. When editing them,
  keep each set summing to 1.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `expansion_options` | Birmingham's first expansion costs 14 000 a week. Plymouth's option adds 8 cars a day. Every expansion becomes 20 % cheaper. Manchester's further expansion is withdrawn (remove the row). |
| `params` | At most 4 expansions are allowed, or only 2 (`max_expansions`). Owning a car costs 20 a week. The damage rate rises to 15 %. The damage excess rises to 150. |
| `depots` | Birmingham's workshop grows to 25 repairs a day (the expansions there are then not needed). Manchester's workshop is cut to 8 repairs a day. |
| `demand` | Saturday demand in Glasgow drops 20 %. A trade fair adds 50 rentals in Birmingham on Wednesday. |
| `rental_lengths` | 3-day rentals rise to 30 % of the mix while 1-day rentals fall to 50 %. The one-way 2-day price rises to 110. The marginal cost of a 1-day rental rises to 25. |
| `return_shares` | 25 % of Glasgow rentals end in Manchester, and the share returned to Glasgow falls to 55 %. |
| `transfer_costs` | All transfer costs rise 20 %. The Glasgow–Plymouth lane closes. |
| `days` | The company opens on Sundays too (add the day and its demand rows). |

Measures for rules, fixed decisions and objective stages:
* `fleet_size` has no index.
* `rentals`, `undamaged_stock`, `damaged_stock`, `undamaged_left`, `damaged_left` and `repairs` are indexed by
  `day` and `depot`.
* `undamaged_transfers` and `damaged_transfers` are indexed by `day`, `from_depot` and `to_depot`.
* `expand` is indexed by `depot` and `step` and takes the values 0 and 1.

For example, a scenario can rule out any expansion at Plymouth (fix `expand` for Plymouth at 0), force both
Birmingham expansions (fix `expand` for Birmingham at 1), allow at most two options in total, or cap the fleet at
900 cars.

Source: Gurobi `modeling-examples/car_rental/car_rental_2.ipynb` (Apache-2.0), after H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 26. Re-implemented from the published data; no
code copied.
