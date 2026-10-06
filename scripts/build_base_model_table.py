#!/usr/bin/env python3
"""Write data/base_models.csv and docs/base_models.md from the curated shortlist below.

Every number in the shortlist was measured on 2026-10-02 by running the original public implementation
(Gurobi notebooks under a size-limited gurobipy licence, OR-Tools sample scripts, PuLP examples, PyPSA
notebooks) and then timing an open solver on the same model: HiGHS 1.15.1 on the exported LP for the
Gurobi notebooks, CP-SAT (8 workers) for OR-Tools CP-SAT examples, SCIP via pywraplp for OR-Tools MIP
samples, HiGHS/SCIP via PuLP for PuLP examples, HiGHS via linopy for PyPSA. Times are wall-clock seconds
of the solve call on one sandbox CPU and are indicative only; "open solver" names the solver timed.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = "https://github.com/Gurobi/modeling-examples/blob/master/"
O = "https://github.com/google/or-tools/blob/stable/"

ROWS = [
    # ---------------------------------------------------------------- supply chain & logistics
    dict(id="gurobi_covid19_facility_location", title="COVID-19 healthcare facility capacity optimization",
         domain="supply_chain_logistics", type="MILP", repo="Gurobi/modeling-examples",
         url=G + "covid19_facility_location/covid19_facility_location.ipynb", license="Apache-2.0",
         n_vars=225, n_cons=32, n_int=9, open_solver="HiGHS", open_time_s=0.180, reference_objective=1521653.42,
         hooks="County demand forecasts, existing facility capacities, candidate temporary facility fixed costs and capacities, cost per mile (notebook also runs a +20% demand scenario)",
         notes="Base scenario (solve 1 of 2 in the notebook)."),
    dict(id="gurobi_customer_assignment", title="Customer assignment (facility location with clustered demand)",
         domain="supply_chain_logistics", type="IP", repo="Gurobi/modeling-examples",
         url=G + "customer_assignment/customer_assignment.ipynb", license="Apache-2.0",
         n_vars=993, n_cons=1024, n_int=993, open_solver="HiGHS", open_time_s=0.022, reference_objective=5815.04,
         hooks="Customer locations (pre-clustered with k-means), candidate facility sites, maximum facilities to open, distance threshold",
         notes="Customer coordinates are generated with a fixed seed; the k-means preprocessing (scikit-learn) must be frozen into the data tables when porting."),
    dict(id="gurobi_drone_network", title="Drone-network design for out-of-hospital cardiac arrests",
         domain="supply_chain_logistics", type="MILP", repo="Gurobi/modeling-examples",
         url=G + "drone_network/drone_network.ipynb", license="Apache-2.0",
         n_vars=966, n_cons=1987, n_int=483, open_solver="HiGHS", open_time_s=0.048, reference_objective=37.3232,
         hooks="Candidate drone bases, demand points and base-to-demand distances, response-time threshold, number of drones/bases to deploy",
         notes="Reads three CSV files shipped in the example folder."),
    dict(id="gurobi_food_supply", title="Food supply chain for humanitarian aid (World Food Programme case)",
         domain="supply_chain_logistics", type="LP", repo="Gurobi/modeling-examples",
         url=G + "food_program/food_supply.ipynb", license="Apache-2.0",
         n_vars=1397, n_cons=437, n_int=0, open_solver="HiGHS", open_time_s=0.025, reference_objective=400812394.0,
         hooks="Nutrient requirements, commodity nutritional values, procurement prices per supplier, transport cost per arc, beneficiaries per city",
         notes="PORTED: whatifgym/models/food_supply (verified on HiGHS, SCIP, CBC; original re-run on Gurobi 13). Reads six CSV files shipped in the example folder."),
    # ---------------------------------------------------------------- production planning
    dict(id="gurobi_factory_planning_1", title="Factory Planning I", domain="production_planning", type="LP",
         repo="Gurobi/modeling-examples", url=G + "factory_planning/factory_planning_1.ipynb", license="Apache-2.0",
         n_vars=126, n_cons=79, n_int=0, open_solver="HiGHS", open_time_s=0.003, reference_objective=93715.18,
         hooks="Monthly market limits per product, machine hours per product, maintenance (machines down) table, profit contributions, storage cost, end stock target",
         notes="PORTED: whatifgym/models/factory_planning (verified on HiGHS, SCIP, CBC, Gurobi)."),
    dict(id="gurobi_factory_planning_2", title="Factory Planning II (maintenance schedule as a decision)",
         domain="production_planning", type="MILP", repo="Gurobi/modeling-examples",
         url=G + "factory_planning/factory_planning_2.ipynb", license="Apache-2.0",
         n_vars=156, n_cons=84, n_int=30, open_solver="HiGHS", open_time_s=0.017, reference_objective=108855.0,
         hooks="Same tables as Factory Planning I plus the number of machines of each type that must undergo maintenance in the horizon",
         notes="PORTED: whatifgym/models/factory_planning_2 (verified on HiGHS, SCIP, CBC)."),
    dict(id="gurobi_food_manufacture_1", title="Food Manufacture I (oil blending and purchasing)",
         domain="production_planning", type="LP", repo="Gurobi/modeling-examples",
         url=G + "food_manufacturing/food_manufacture_1.ipynb", license="Apache-2.0",
         n_vars=96, n_cons=70, n_int=0, open_solver="HiGHS", open_time_s=0.002, reference_objective=107842.59,
         hooks="Monthly oil purchase prices, hardness values, refining capacities, storage capacity and cost, product price, hardness bounds",
         notes="PORTED: whatifgym/models/food_manufacture (verified on HiGHS, SCIP, CBC). Food Manufacture II adds logical (indicator) constraints; port directly if wanted."),
    dict(id="gurobi_farm_planning", title="Farm Planning (multi-year herd, crop and capital plan)",
         domain="production_planning", type="LP", repo="Gurobi/modeling-examples",
         url=G + "farm_planning/farm_planning.ipynb", license="Apache-2.0",
         n_vars=131, n_cons=116, n_int=0, open_solver="HiGHS", open_time_s=0.002, reference_objective=121719.17,
         hooks="Land area, herd dynamics, yields and prices, labour hours per activity, capital and loan limits, housing capacity",
         notes="PORTED: whatifgym/models/farm_planning (verified on HiGHS, SCIP, CBC; original re-run on Gurobi 13)."),
    dict(id="gurobi_mining", title="Mining (multi-year mine operation and blending)",
         domain="production_planning", type="MILP", repo="Gurobi/modeling-examples",
         url=G + "mining/mining.ipynb", license="Apache-2.0",
         n_vars=65, n_cons=71, n_int=40, open_solver="HiGHS", open_time_s=0.123, reference_objective=146861974.36,
         hooks="Per-mine royalty, extraction capacity and ore quality, yearly blended-quality targets, selling price, discount rate, maximum mines operated per year",
         notes="PORTED: whatifgym/models/mining (verified on HiGHS, SCIP, CBC)."),
    # ---------------------------------------------------------------- scheduling (workforce, machines, projects)
    dict(id="gurobi_manpower_planning", title="Manpower Planning (recruitment, retraining, redundancy over 3 years)",
         domain="scheduling", type="LP", repo="Gurobi/modeling-examples",
         url=G + "manpower_planning/manpower_planning.ipynb", license="Apache-2.0",
         n_vars=72, n_cons=30, n_int=0, open_solver="HiGHS", open_time_s=0.001, reference_objective=841.80,
         hooks="Yearly manpower requirements per skill level, attrition rates, recruitment caps, retraining capacities and costs, redundancy/overmanning/short-time costs",
         notes="PORTED: whatifgym/models/manpower_planning (verified on HiGHS, SCIP, CBC). Objective is minimum redundancy (the notebook's first objective); `cost_expression()` gives the second."),
    dict(id="ortools_jobshop_ft06_sat", title="Job-shop scheduling, Fisher-Thompson 6x6 instance",
         domain="scheduling", type="CP-SAT", repo="google/or-tools",
         url=O + "examples/python/jobshop_ft06_sat.py", license="Apache-2.0",
         n_vars=73, n_cons=73, n_int=73, open_solver="CP-SAT", open_time_s=0.021, reference_objective=55.0,
         hooks="Job routings, processing times, machine availability; makespan objective",
         notes="Interval/no-overlap model; a MIP port needs disjunctive big-M constraints."),
    dict(id="ortools_flexible_job_shop_sat", title="Flexible job-shop scheduling",
         domain="scheduling", type="CP-SAT", repo="google/or-tools",
         url=O + "examples/python/flexible_job_shop_sat.py", license="Apache-2.0",
         n_vars=109, n_cons=136, n_int=109, open_solver="CP-SAT", open_time_s=0.029, reference_objective=6.0,
         hooks="Alternative machines per task with different durations, job routings; makespan objective",
         notes=""),
    dict(id="ortools_single_machine_scheduling_sat", title="Single machine scheduling with setup times, release and due dates",
         domain="scheduling", type="CP-SAT", repo="google/or-tools",
         url=O + "examples/python/single_machine_scheduling_with_setup_release_due_dates_sat.py", license="Apache-2.0",
         n_vars=271, n_cons=245, n_int=271, open_solver="CP-SAT", open_time_s=0.271, reference_objective=112605.0,
         hooks="Job durations, release dates, due dates, sequence-dependent setup matrix; weighted lateness objective",
         notes="Run with the script's default flags."),
    dict(id="ortools_task_allocation_sat", title="Task allocation to time slots with capacity",
         domain="scheduling", type="CP-SAT", repo="google/or-tools",
         url=O + "examples/python/task_allocation_sat.py", license="Apache-2.0",
         n_vars=2552, n_cons=2651, n_int=2552, open_solver="CP-SAT", open_time_s=0.938, reference_objective=17.0,
         hooks="Task-to-slot eligibility table, per-slot capacity; minimise number of slots used",
         notes="Largest CP-SAT model in the shortlist; still under one second."),
    # ---------------------------------------------------------------- energy & power
    dict(id="gurobi_battery_scheduling", title="Battery scheduling against hourly prices with PV and load",
         domain="energy_power", type="LP", repo="Gurobi/modeling-examples",
         url=G + "battery_scheduling/battery_scheduling.ipynb", license="Apache-2.0",
         n_vars=72, n_cons=25, n_int=0, open_solver="HiGHS", open_time_s=0.001, reference_objective=1.56625,
         hooks="Hourly import/export prices, load and PV profiles, battery energy capacity, charge/discharge limits and efficiencies, cycling cost",
         notes="PORTED: whatifgym/models/battery_scheduling (verified on HiGHS, SCIP, CBC; original re-run on Gurobi 13). Default variant 'S'; the 'LGS' variant adds load/PV variables and a power-law cycling cost (nonlinear), not ported."),
    dict(id="gurobi_electrical_power_2", title="Electrical Power Generation 2 (thermal units plus pumped hydro)",
         domain="energy_power", type="MILP", repo="Gurobi/modeling-examples",
         url=G + "electrical_power_generation/electrical_power_2.ipynb", license="Apache-2.0",
         n_vars=75, n_cons=85, n_int=50, open_solver="HiGHS", open_time_s=0.155, reference_objective=1000630.0,
         hooks="Demand per period, generator min/max output, running and startup costs, hydro output and reservoir depletion, pumping efficiency",
         notes="PORTED: whatifgym/models/power_generation_hydro (verified on HiGHS, SCIP, CBC). Part 1 (45 variables) is just below the size floor."),
    dict(id="gurobi_optimize_power_schedule", title="Power generation schedule (unit commitment with startup and health costs)",
         domain="energy_power", type="MILP", repo="Gurobi/modeling-examples",
         url=G + "power_generation/optimize_power_schedule.ipynb", license="Apache-2.0",
         n_vars=960, n_cons=1722, n_int=720, open_solver="HiGHS", open_time_s=0.047, reference_objective=4495153.46,
         hooks="Hourly demand curve, plant capacities, fuel, operating, startup and health-cost tables (small_plant_data/; a large variant ships too)",
         notes="Reads CSV files from the example folder."),
    dict(id="pypsa_unit_commitment", title="PyPSA unit commitment example (two generators, 30 snapshots)",
         domain="energy_power", type="MILP", repo="PyPSA/PyPSA",
         url="https://github.com/PyPSA/PyPSA/blob/master/docs/examples/unit-commitment.ipynb", license="MIT (code); CC-BY-4.0 (notebook)",
         n_vars=240, n_cons=598, n_int=180, open_solver="HiGHS (linopy)", open_time_s=0.013, reference_objective=2227450.0,
         hooks="Load profile, generator marginal and startup costs, min up/down times, ramp limits, minimum stable output",
         notes="Data is inline in the notebook; the 4-snapshot variant is too small (32 variables)."),
    # ---------------------------------------------------------------- packing, assignment & covering
    dict(id="ortools_multiple_knapsack", title="Multiple knapsack", domain="packing_assignment_covering", type="IP",
         repo="google/or-tools", url=O + "ortools/sat/samples/multiple_knapsack_sat.py", license="Apache-2.0",
         n_vars=75, n_cons=20, n_int=75, open_solver="HiGHS / CP-SAT", open_time_s=0.064, reference_objective=395.0,
         hooks="Item weights and values, bin capacities, number of bins",
         notes="PORTED: whatifgym/models/multiple_knapsack (verified on HiGHS, SCIP, CBC, CP-SAT, Gurobi)."),
    dict(id="ortools_bin_packing_mip", title="Bin packing (minimise bins used)", domain="packing_assignment_covering", type="IP",
         repo="google/or-tools", url=O + "ortools/linear_solver/samples/bin_packing_mip.py", license="Apache-2.0",
         n_vars=132, n_cons=22, n_int=132, open_solver="SCIP (pywraplp)", open_time_s=0.005, reference_objective=4.0,
         hooks="Item weights, bin capacity, number of candidate bins",
         notes="PORTED: whatifgym/models/bin_packing (verified on HiGHS, SCIP, CBC, CP-SAT)."),
    dict(id="pulp_wedding_seating", title="Wedding seating as set partitioning", domain="packing_assignment_covering", type="IP",
         repo="coin-or/pulp", url="https://github.com/coin-or/pulp/blob/master/examples/wedding.py", license="MIT",
         n_vars=3213, n_cons=18, n_int=3213, open_solver="HiGHS", open_time_s=0.334, reference_objective=12.0,
         hooks="Guest list and ranks, maximum tables, maximum table size",
         notes="PORTED: whatifgym/models/wedding_seating (verified on HiGHS, SCIP, CBC, CP-SAT)."),
    dict(id="ortools_assignment_with_constraints_sat", title="Assignment with group constraints",
         domain="packing_assignment_covering", type="CP-SAT", repo="google/or-tools",
         url=O + "examples/python/assignment_with_constraints_sat.py", license="Apache-2.0",
         n_vars=84, n_cons=33, n_int=84, open_solver="CP-SAT", open_time_s=0.027, reference_objective=239.0,
         hooks="Worker-task cost matrix, allowed group combinations (table constraints), tasks per worker",
         notes="Uses table constraints; a MIP port enumerates the allowed combinations."),
    # ---------------------------------------------------------------- network & routing
    dict(id="gurobi_technician_routing_scheduling", title="Technician routing and scheduling",
         domain="network_routing", type="MILP", repo="Gurobi/modeling-examples",
         url=G + "technician_routing_scheduling/technician_routing_scheduling.ipynb", license="Apache-2.0",
         n_vars=660, n_cons=217, n_int=630, open_solver="HiGHS", open_time_s=0.092, reference_objective=12410.0,
         hooks="Technician skills, capacities and depots; job durations, priorities and time windows; distance matrix (Excel scenarios Sce0/Sce3)",
         notes="Objective for scenario Sce3 (Sce0 has objective 0). Data is an Excel workbook in the example folder."),
    dict(id="gurobi_railway_dispatching", title="Railway dispatching (rescheduling trains after a delay)",
         domain="network_routing", type="MILP", repo="Gurobi/modeling-examples",
         url=G + "railway_dispatching/railway_dispatching.ipynb", license="Apache-2.0",
         n_vars=218, n_cons=367, n_int=180, open_solver="HiGHS", open_time_s=0.562, reference_objective=47.0,
         hooks="Train timetable, track-segment occupancy, minimum headways, delay scenario", notes=""),
    dict(id="gurobi_airline_planning", title="Airline planning after flight disruption",
         domain="network_routing", type="IP", repo="Gurobi/modeling-examples",
         url=G + "aviation_planning/airlineplanning.ipynb", license="Apache-2.0",
         n_vars=1930, n_cons=536, n_int=1930, open_solver="HiGHS", open_time_s=0.027, reference_objective=561087.0,
         hooks="Flight rotation schedule, aircraft start/end positions, itinerary revenues (CSV files in data/)",
         notes="Notebook needs a one-line pandas-3 compatibility patch (groupby().apply(list))."),
    dict(id="ortools_tsp_sat", title="Travelling salesman with the circuit constraint (40 cities)",
         domain="network_routing", type="CP-SAT", repo="google/or-tools",
         url=O + "examples/python/tsp_sat.py", license="Apache-2.0",
         n_vars=1560, n_cons=1, n_int=1560, open_solver="CP-SAT", open_time_s=0.582, reference_objective=216449.0,
         hooks="Distance matrix (fixed in the script); forbid or force arcs, add cities",
         notes="Gurobi's tsp.ipynb uses lazy subtour cuts and is deferred until a cut loop exists on open solvers."),
    # ---------------------------------------------------------------- revenue & resource planning
    dict(id="gurobi_economic_planning", title="Economic Planning (input-output model with capacity building)",
         domain="revenue_resource_planning", type="LP", repo="Gurobi/modeling-examples",
         url=G + "economic_planning/economic_planning.ipynb", license="Apache-2.0",
         n_vars=51, n_cons=33, n_int=0, open_solver="HiGHS", open_time_s=0.001, reference_objective=1902.22,
         hooks="Input-output coefficients between industries, capacity-building coefficients, exogenous demand, initial stocks and capacities, manpower limits",
         notes="Objective of the notebook's second model (maximise total production); the first model is 3 variables."),
    dict(id="gurobi_fantasy_basketball_1", title="Fantasy basketball line-up under a salary cap (part 1)",
         domain="revenue_resource_planning", type="IP", repo="Gurobi/modeling-examples",
         url=G + "fantasy_basketball/fantasy_basketball_part1.ipynb", license="Apache-2.0",
         n_vars=96, n_cons=97, n_int=96, open_solver="HiGHS", open_time_s=0.017, reference_objective=171.92,
         hooks="Predicted points per player, salaries, salary cap, position requirements",
         notes="Predicted points come from a regression step in the notebook; freeze them into the data table when porting."),
    dict(id="gurobi_car_rental_1", title="Car Rental 1 (fleet positioning, transfers and repairs)",
         domain="revenue_resource_planning", type="LP", repo="Gurobi/modeling-examples",
         url=G + "car_rental/car_rental_1.ipynb", license="Apache-2.0",
         n_vars=289, n_cons=97, n_int=0, open_solver="HiGHS", open_time_s=0.003, reference_objective=121160.21,
         hooks="Daily rental demand per depot, price by rental length, return-depot shares, damage rates and repair capacities, transfer costs",
         notes="PORTED: whatifgym/models/car_rental (verified on HiGHS, SCIP, CBC)."),
    dict(id="gurobi_car_rental_2", title="Car Rental 2 (adds repair-capacity expansion decisions)",
         domain="revenue_resource_planning", type="MILP", repo="Gurobi/modeling-examples",
         url=G + "car_rental/car_rental_2.ipynb", license="Apache-2.0",
         n_vars=294, n_cons=118, n_int=5, open_solver="HiGHS", open_time_s=0.020, reference_objective=132341.47,
         hooks="Same tables as Car Rental 1 plus repair-capacity expansion options and costs",
         notes="PORTED: whatifgym/models/car_rental_2 (verified on HiGHS, SCIP, CBC; original re-run on Gurobi 13)."),
]

# Candidates that did not make the strict cut but are worth knowing about.
DEFERRED = [
    ("gurobi_supply_network_design_2", "49 variables (one below the floor); otherwise ideal S&OP model", G + "supply_network_design/supply_network_design_2.ipynb"),
    ("gurobi_workforce_scheduling", "hierarchical two-objective model; needs a lexicographic two-solve port before timing on open solvers", G + "workforce/workforce_scheduling.ipynb"),
    ("gurobi_tsp", "1128 binaries; lazy subtour cuts via callback; needs a DFJ cut loop on open solvers", G + "traveling_salesman/tsp.ipynb"),
    ("gurobi_milk_collection", "442 binaries; same lazy-cut issue as tsp", G + "milk_collection/milk_collection.ipynb"),
    ("gurobi_lost_luggage_distribution", "1747 binaries; hierarchical objectives", G + "lost_luggage_distribution/lost_luggage_distribution.ipynb"),
    ("ortools_shift_scheduling_sat", "1462 booleans; CP-SAT 2.8 s with 8 workers (just over the 2 s bar)", O + "examples/python/shift_scheduling_sat.py"),
    ("ortools_wedding_optimal_chart_sat", "901 booleans, 1.0 s; near-duplicate of pulp_wedding_seating", O + "examples/python/wedding_optimal_chart_sat.py"),
    ("egret_tiny_uc_2", "BSD-3; 1203 variables; SCIP 0.7 s but HiGHS 2.0 s; needs the Egret package", "https://github.com/grid-parity-exchange/Egret/blob/main/egret/models/tests/uc_test_instances/tiny_uc_2.json"),
    ("switch_3zone_toy", "Apache-2.0; 618 variables, 0.009 s; needs the Switch package and its input-directory format", "https://github.com/switch-model/switch/tree/master/examples/3zone_toy"),
    ("pso_economic_dispatch_24h", "600 variables, 0.003 s; course material under CC-BY-4.0 (data) and MIT (code)", "https://github.com/east-winds/power-systems-optimization/blob/master/Notebooks/04-Economic-Dispatch.ipynb"),
]

DOMAIN_LABELS = {
    "supply_chain_logistics": "Supply chain & logistics",
    "production_planning": "Production planning",
    "scheduling": "Scheduling (workforce, machines, projects)",
    "energy_power": "Energy & power",
    "packing_assignment_covering": "Packing, assignment & covering",
    "network_routing": "Network & routing",
    "revenue_resource_planning": "Revenue & resource planning",
}


def main() -> None:
    assert len(ROWS) == 30, len(ROWS)
    for r in ROWS:
        assert 50 <= r["n_vars"] <= 5000, r["id"]
        assert r["open_time_s"] < 2.0, r["id"]
        assert r["url"].startswith("https://"), r["id"]
    counts = {}
    for r in ROWS:
        counts[r["domain"]] = counts.get(r["domain"], 0) + 1
    assert all(c >= 4 for c in counts.values()), counts

    fields = ["id", "title", "domain", "type", "repo", "url", "license", "n_vars", "n_cons", "n_int",
              "open_solver", "open_time_s", "reference_objective", "hooks", "notes"]
    (ROOT / "data").mkdir(exist_ok=True)
    with open(ROOT / "data" / "base_models.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in ROWS:
            w.writerow({k: r.get(k, "") for k in fields})

    lines = ["# Base models (30)", "",
             "Public, permissively licensed optimization models with named data tables, 50 to 5 000 variables and an "
             "open-solver solve time under 2 s. Every number was **measured** on 2026-10-02 by running the original "
             "public implementation and then timing an open solver on the same model (see `scripts/build_base_model_table.py` "
             "for the exact method per source). Times are single-run wall-clock seconds on one sandbox CPU core and are "
             "indicative only. Fourteen models are already ported into `whatifgym/models/` (marked **(ported)**); the rest are the Phase 1-2 porting queue.", "",
             f"Domains: {', '.join(f'{DOMAIN_LABELS[d]} ({c})' for d, c in counts.items())}.", ""]
    for domain, label in DOMAIN_LABELS.items():
        lines += [f"## {label}", "",
                  "| # | model | type | vars | cons | int | open solver | time (s) | reference objective | licence | what-if hooks |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in ROWS:
            if r["domain"] != domain:
                continue
            idx = ROWS.index(r) + 1
            ported = " **(ported)**" if r["notes"].startswith("PORTED") else ""
            lines.append(f"| {idx} | [{r['title']}]({r['url']})<br>`{r['id']}`{ported} | {r['type']} | {r['n_vars']} | {r['n_cons']} | "
                         f"{r['n_int']} | {r['open_solver']} | {r['open_time_s']:.3f} | {r['reference_objective']:,.6g} | "
                         f"{r['license']} | {r['hooks']} |")
        lines.append("")
    lines += ["## Notes per model", ""]
    for i, r in enumerate(ROWS, 1):
        if r["notes"]:
            lines.append(f"{i}. `{r['id']}` — {r['notes']}")
    lines += ["", "## Deferred candidates", "",
              "Measured but kept out of the 30 for the stated reason; several are one fix away.", "",
              "| id | why deferred | source |", "|---|---|---|"]
    for cid, why, url in DEFERRED:
        lines.append(f"| `{cid}` | {why} | [link]({url}) |")
    lines += ["", "## Licences", "",
              "Gurobi modeling-examples and Google OR-Tools: Apache-2.0. PuLP: MIT. PyPSA: MIT code, CC-BY-4.0 notebook content. "
              "The what-if benchmark reuses only published data values and re-implements each model; see `ATTRIBUTION.md`.", ""]
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "base_models.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {len(ROWS)} rows; domains: {counts}")


if __name__ == "__main__":
    main()
