# Car Rental 1

**Domain:** revenue / resource planning · **Type:** LP · **Size:** 289 variables, 97 constraints · **Sense:** maximise weekly profit

A car rental company rents one type of car from four depots (Glasgow, Manchester, Birmingham, Plymouth),
Monday to Saturday. Each depot has an estimated demand for every trading day, and the company does not have to
meet all of it. Rentals last one, two or three days (55 %, 20 % and 25 % of rentals). A car can be returned to any
depot: for each rental depot a fixed share of its cars comes back to each depot. The price depends on the rental
length and on whether the car comes back to the depot it left from, and every rental has a marginal cost.
Ten per cent of returned cars are damaged. The customer then pays a $100 excess, and the car goes to a repair
depot: one day in transit unless it is already there, then one day in repair, after which it can be rented the
next morning. Manchester can repair 12 cars a day and Birmingham 20; Glasgow and Plymouth have no workshop.
Undamaged cars can be moved between depots at a per-car cost and arrive the next morning. Owning a car costs
$15 a week. The plan is a weekly steady state, with the same number of cars at each depot on the same day of
every week, so the day before Monday is Saturday.

Decisions per day and depot: **rentals**, the undamaged and damaged cars at the depot in the morning
(**undamaged_stock**, **damaged_stock**), the cars kept there overnight (**undamaged_left**, **damaged_left**) and
**repairs**. Per day and lane: **undamaged_transfers** and **damaged_transfers**. Overall: the **fleet_size**.

Constraints:
* Undamaged-car balance at every depot and day: returns + arrivals + yesterday's repairs + cars kept overnight
  = rentals + transfers out + cars kept.
* Damaged-car balance: returns + cars kept overnight (+ arrivals, at a repair depot) = repairs + transfers out
  + cars kept.
* Repair capacity and demand, both as variable bounds.
* Fleet count: the cars still on rent plus all cars at the depots on Wednesday morning.

Reference optimum (original Gurobi notebook): **121 160.21** a week, with 616.69 cars (617 rounded) and 1 920
rentals a week (58.8 % of demand). Both repair depots work at capacity, which caps rentals at 1 920
(192 repairs a week ÷ 10 % damaged).

## Notes on the port

* The variables, constraints and coefficients are the original's, checked coefficient by coefficient. The repair
  variables of the depots without a workshop (upper bound 0) are also written into those depots' balance rows, so
  PuLP keeps them. The feasible set does not change.
* Values the original hard-codes are derived from the data:
  * Repair depots are the depots with positive repair capacity.
  * The fleet-count factors 0.25 and 0.45 come from the rental-length mix.
  * The expected damage fee of 10 per rental is `damaged_share × damage_excess`.
  * The undamaged share is `1 − damaged_share`.

  The original's same-depot transfer costs (0.001) are never used and are left out.
* Two damaged-car flows are kept as in the original. A damaged transfer out of a repair depot can only go to a depot
  without a workshop, and that depot does not receive it. A damaged transfer between two repair depots is
  received but never leaves the sender. Neither flow is used at the published optimum. A scenario with very
  unbalanced repair capacity may use them.
* Return shares and rental-length shares are used exactly as given and are not renormalised. When editing them,
  keep each set summing to 1.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `demand` | Saturday demand in Glasgow drops 20 %. A trade fair adds 50 rentals in Birmingham on Wednesday. |
| `depots` | Birmingham's workshop grows to 25 repairs a day. Glasgow opens a 10-car workshop and becomes a repair depot. Manchester's workshop closes. |
| `rental_lengths` | 3-day rentals rise to 30 % of the mix while 1-day rentals fall to 50 %. The one-way 2-day price rises to 110. The marginal cost of a 1-day rental rises to 25. |
| `return_shares` | 25 % of Glasgow rentals end in Manchester, and the share returned to Glasgow falls to 55 %. |
| `transfer_costs` | All transfer costs rise 20 %. The Glasgow–Plymouth lane closes. |
| `days` | The company opens on Sundays too (add the day and its demand rows). |
| `params` | Owning a car costs 20 a week. The damage rate rises to 15 %. The damage excess rises to 150. |

Measures for rules, fixed decisions and objective stages:
* `fleet_size` has no index.
* `rentals`, `undamaged_stock`, `damaged_stock`, `undamaged_left`, `damaged_left` and `repairs` are indexed by
  `day` and `depot`.
* `undamaged_transfers` and `damaged_transfers` are indexed by `day`, `from_depot` and `to_depot`.

For example, a scenario can cap the fleet at 550 cars or forbid undamaged transfers into Plymouth.

Source: Gurobi `modeling-examples/car_rental/car_rental_1.ipynb` (Apache-2.0), after H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 25. Re-implemented from the published data; no
code copied.
