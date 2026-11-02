# COVID-19 healthcare facility capacity

**Domain:** supply chain / logistics · **Type:** MILP · **Size:** 225 variables (9 binary), 32 constraints · **Sense:** minimise cost

Nine counties on a map have forecast COVID-19 patient demand (3,539 in total). Fourteen existing facilities
(always open, fixed bed capacity) and nine candidate temporary sites (100 beds each if built) can treat them.
Every patient of every county must be assigned to some facility. Cost = travel (cost per patient per unit of
Euclidean distance between county centroid and facility) + a fixed cost per temporary facility built + a very
large penalty per extra bed added at a temporary site beyond its capacity.

Decisions: `build[t]` (open temporary site t), `assign[county, facility]` (patients sent), `extra_beds[t]`.

Reference optimum (original notebook, Gurobi): **1,521,653.42** — build T15, T17, T18 (1,500,000), travel
21,653.42 (the notebook prints 21,645 because it rounds each term), no extra beds.

Quirks kept from the original: the travel cost (5) is described as per 10 miles but applied to the raw map
distance; extra beds are not tied to building the site. Base scenario only (the notebook's +20% demand rerun
is a what-if: scale `counties.demand` by 1.2).

## What-if surface

| Table | Typical scenario questions |
|---|---|
| `counties` | Demand rises 20% everywhere; county C6 forecast doubles. |
| `facilities` | E7 closes; E12 adds 50 beds; temporary sites get 150 beds; T15 is unavailable. |
| `params` | Building a temporary facility costs 300,000; travel cost doubles; a cheaper extra-bed penalty. |

Source: Gurobi modeling-examples `covid19_facility_location/covid19_facility_location.ipynb` (Apache-2.0;
fictional data, after Klise & Bynum, SAND2020-4693R). Re-implemented from the published data.
