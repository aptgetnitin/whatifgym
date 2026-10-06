# Food Supply

**Domain:** supply chain logistics · **Type:** LP · **Size:** 1,397 variables, 437 constraints · **Sense:** minimise cost

A relief agency feeds 67,000 people in seven camps in Syria: Ar Raqqa, Daraa, Dayr_Az_Zor, Hassakeh, Idleb,
Jubb_al_Jarrah and Qamishli, with 2,000 to 25,000 people each. For each camp it chooses a daily ration from 24
foods. It buys the food in 11 supplier cities (eight in Syria, plus Amman, Beirut and Gaziantep) and trucks it
over 37 directed road links. Each ration must provide at least the daily minimum of 11 nutrients: energy,
protein, fat, calcium, iron, vitamin A, thiamine, riboflavin, niacin, folate and vitamin C. It may provide at
most twice each minimum. A Syrian supplier sells 13 of the foods at its own mean price from January 2017 to
October 2021. Every other supplier-food pair is priced at the food's international price. Each link has a
transport cost per unit shipped. The plan minimises purchase cost plus transport cost.

Decisions: the **ration** per person of each food in each camp, the food **purchase**d at each supplier, and the
**flow** of each food on each link.

Constraints:
* nutrition, per camp and nutrient: intake per person lies between the minimum and `max_nutrient_factor` (2)
  times the minimum;
* flow balance, per food and city: food arriving minus food leaving equals the food handed out at a camp
  (beneficiaries × ration) minus the food bought at a supplier. A city that is both does both, and food may pass
  through any city;
* a purchase limit per food and supplier (`max_purchase`, so large that it never binds).

**Units.** Nutrient contents are given per 100 g and requirements per person per day. Rations are therefore in
100-g units per person per day, and purchases and flows in 100-g units per day. Prices are the published
figures, which look like USD per metric ton. Link costs are also as published: about 2 per km of road. Like the
original, the model applies both per 100-g unit without conversion, so the objective matches. Read as per-ton
figures, the optimal plan costs about 40,081 USD a day, or 0.60 USD per person.

Reference optimum (original Gurobi notebook): **400,812,394.0**, of which procurement is 354,457,744.8 and
transport 46,354,649.2. The plan buys six foods: wheat, oil, corn-soya blend, milk, dried skim milk and maize
meal. It buys in eight of the 11 cities, mostly in the camp cities that are suppliers themselves
(Dayr_Az_Zor, Hassakeh and Daraa). Each person receives about 4.84 units (484 g) of food a day. Total cost, its
procurement/transport split and the food bought are unique at the optimum and are scored. Rations per camp and
purchases per supplier can tie in some what-ifs, so they are reported but not scored. Flows are not scored.

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `camps` | Idleb's population doubles to 10,000. The Qamishli camp closes (remove the row). A camp of 3,000 people opens in Homs (add a row; Homs is already on the network). |
| `local_prices` | Oil prices in Hassakeh fall 10 %. Hassakeh's market stops quoting a local price for oil (remove the row: the international price of 2,800 applies instead of 2,591.32). |
| `foods` | International prices rise 10 %. These apply to every supplier without a local price, so to all purchases in Amman, Beirut and Gaziantep and to the 11 foods that have no local price anywhere. |
| `arcs` | Fuel costs push all transport costs up 25 %. The road from Aleppo to Idleb closes (remove the link). A new road from Homs to Idleb (add a link). |
| `nutrients` | The energy requirement rises to 2,300 kcal a day. Every requirement falls 20 % (a reduced ration). Vitamin C is no longer required (remove the row; a minimum of 0 would also cap vitamin C at 0). |
| `food_nutrients` | The corn-soya blend is fortified with 25 % more vitamin C (raise the amount). |
| `suppliers` | Beirut stops selling (remove the supplier). Qamishli's market starts selling at international prices (add a supplier row). |
| `params` | Intake may reach three times the minimum (`max_nutrient_factor` = 3). No supplier can sell more than 20,000 units of a food (`max_purchase`). |

Rules and fixed decisions address the measures `ration` (by `food`, `camp`), `purchase` (by `food`, `supplier`)
and `flow` (by `food`, `from_city`, `to_city`). Examples: "buy at most 50,000 units in Hassakeh"; "nobody in Idleb
gets more than 0.5 units of oil a day"; "ship nothing out of Beirut".

## Port notes

* **Data.** The data are the six CSV files in `food_program/data`; the folder holds no others. Values are copied
  verbatim into tidy tables:
  * `suppliers` and `camps` come from the S and D node rows of `node_types.csv`;
  * `arcs` comes from `edge_costs.csv`;
  * `foods` comes from `food_nutrition.csv` and `food_internationalprice.csv`;
  * `nutrients` comes from `nutrient_requirements.csv`;
  * `food_nutrients` is `food_nutrition.csv` in long form;
  * `local_prices` is the `Mean` column of `food_costs.csv`.

  The model does not use the road distances and durations, the node-level link labels, the transit-hub (TS) node
  rows or the 58 monthly prices behind each mean, so they are left out.
* **Duplicate links.** `edge_costs.csv` repeats each city pair once per pair of node types (supplier, transit hub,
  camp): 84 rows for 37 city pairs. The notebook keys the costs by city pair, so the last row of a pair wins. Only
  Hama → Jubb_al_Jarrah conflicts, with 147.6 on the supplier rows and 148 on the transit rows. The port uses 148,
  as the notebook does.
* **Ranged rows.** The notebook states each nutrition bound pair as one ranged row. Gurobi stores a ranged row as
  an equality plus a bounded range column. That is why it reports 1,397 columns although the notebook counts 1,320
  decision variables. The port writes the same equality, intake − `nutrient_surplus` = minimum, with
  0 ≤ `nutrient_surplus` ≤ (`max_nutrient_factor` − 1) × minimum. Rows, columns, the 3,541 nonzeros and the 1,080
  nonzero objective coefficients all match. The upper limit is a multiple of the minimum, so a zero minimum also
  caps that nutrient at zero.
* **Hard-coded numbers.** The notebook's upper limit of twice the minimum and its purchase limit of 10,000,000 are
  the parameters `max_nutrient_factor` and `max_purchase`.
* **Transit cities.** The original writes balance rows only for suppliers and camps. A city that is only a transit
  hub would get none, and food could appear there for free. The port writes a balance row for every city that a
  supplier, camp or link names; where nothing is bought or handed out, inflow equals outflow. In the published
  data every city is a supplier or a camp, so the rows are identical. This matters for what-ifs that remove a
  supplier or a camp.
* **Self-links.** Daraa, Dayr_Az_Zor and Hassakeh each have a zero-cost link to themselves: the source's link from
  a city's supplier node to its camp node. Flow on such a link enters and leaves the same balance row, so it nets
  out. The 72 flow variables on these links (3 links × 24 foods) appear only in the objective with cost 0, as in
  the original. They are kept for the size but are not part of the `flow` measure, so a floor on shipments cannot
  be met by this inert flow.
* **Quirks kept as published.** The nutrient `NicacinB3(mg)` is niacin. Soya-fortified sorghum grits list 360 g
  of protein per 100 g; the optimum does not use them.
* **Missing data.** Every city named by a supplier, camp or link is part of the network, so a new camp needs
  a link that reaches it. Rows that name an unknown food or nutrient are ignored. A missing `food_nutrients` row
  counts as 0. A food with neither a local nor an international price cannot be bought at that supplier.

Source: Gurobi `modeling-examples/food_program/food_supply.ipynb` and its data folder (Apache-2.0), motivated by
the World Food Programme case studies of Peters et al. (INFORMS Journal on Optimization, 2021; INFORMS Journal on
Applied Analytics, 2022). Only the published data values are reused; no code or text is copied.
