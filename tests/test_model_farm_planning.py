"""Farm Planning (Gurobi modeling-examples): reference optimum on the open solvers, sizes, schema, KPIs, what-ifs."""
import math
import subprocess
import sys
from pathlib import Path

import pytest

from whatifgym.base import read_table
from whatifgym.models.farm_planning.model import FarmPlanning
from whatifgym.oracle import solve_scenario
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]
ROOT = Path(__file__).resolve().parents[1]
YEARS = ["Year1", "Year2", "Year3", "Year4", "Year5"]

# The plan tables printed by the notebook (one decimal; zero entries omitted). The optimal plan is unique.
NOTEBOOK_PLAN = {
    "yearly_profit": [21906.1, 21888.7, 25816.1, 26825.8, 25282.6],
    "buy_grain": [36.6, 35.1, 37.8, 40.1, 33.5],
    "grow_beet": [91.1, 94.0, 97.7, 114.6, 131.3],
    "sell_beet": [22.8, 27.4, 24.6, 42.1, 66.6],
    "sell_heifers": [30.9, 40.8, 57.4, 57.0, 50.9],
    "raise_heifers": [22.8, 11.6, 0.0, 0.0, 0.0],
    "grow_grain_Group1": [22.0, 22.0, 22.0, 22.0, 22.0],
    "grow_grain_Group2": [0.0, 0.0, 2.8, 0.0, 0.0],
}


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = FarmPlanning()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert round(r.objective, 2) == 121719.17  # the notebook's printed optimum
    assert r.kpis
    assert math.isclose(r.kpis["profit"], r.objective, abs_tol=0.01)
    assert r.kpis["extra_housing_places"] == 0 and r.kpis["overtime_hours"] == 0
    assert math.isclose(r.kpis["final_dairy_cows"], 92.4608, abs_tol=1e-3)


@pytest.mark.parametrize("solver", SOLVERS)
def test_plan_matches_the_notebook_tables(solver):
    r = FarmPlanning().solve(solver=solver, time_limit=60, keep_variables=True)
    assert r.status == "optimal", r.message
    for family, printed in NOTEBOOK_PLAN.items():
        for year, want in zip(YEARS, printed):
            name = f"grow_grain_{year}_{family.rsplit('_', 1)[1]}" if family.startswith("grow_grain") else f"{family}_{year}"
            got = r.variables.get(name, 0.0)
            assert abs(got - want) <= 0.05 + 1e-6, (name, got, want)
    # no extra housing, no overtime, no sugar beet bought and no grain sold in any year
    assert all(abs(x) <= 1e-6 for n, x in r.variables.items()
               if n.startswith(("extra_housing", "overtime", "buy_beet", "sell_grain")))


def test_sizes_and_measures():
    m = FarmPlanning(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"]) == (131, 116)
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"] == 0
    assert sum(len(c) for c in prob.constraints.values()) == 734  # nonzeros, as in the original
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert len(ms["herd"].vars) == 5 * 12 and len(ms["grow_grain"].vars) == 5 * 4
    # the range slack of the final-herd row is the 131st column, but not a measure
    in_measures = {id(v) for meas in ms.values() for v in meas.vars.values()}
    assert len(in_measures) == 130 and id(prob._wig["final_dairy_cows_headroom"]) not in in_measures
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert m.index_sets(data) == {"year": YEARS, "land_group": ["Group1", "Group2", "Group3", "Group4"],
                                  "age": list(range(1, 13))}
    keys = m.table_keys(data)
    assert set(keys) == set(m.TABLES) and {"land_group": "Group4"} in keys["land_groups"]


def test_objective_charges_the_notebooks_pending_repayments():
    m = FarmPlanning(); data = m.load_data(); prob = m.build(data)
    coef = {v.name: c for v, c in prob.objective.items()}
    # 39.71 per place for each of the (t + 4) yearly repayments still due after year t of the plan
    assert [round(coef[f"extra_housing_{t}"], 6) for t in YEARS] == [-198.55, -238.26, -277.97, -317.68, -357.39]
    # a 3-year loan is repaid inside the plan for housing added up to Year3; later housing leaves 1 or 2 repayments
    data["params"]["loan_term_years"] = 3
    prob = m.build(data)
    coef = {v.name: c for v, c in prob.objective.items()}
    assert [round(coef.get(f"extra_housing_{t}", 0.0), 6) for t in YEARS] == [0, 0, 0, -39.71, -79.42]
    row = {v.name: c for v, c in prob.constraints["profit_Year4"].items()}
    assert "extra_housing_Year1" not in row and row["extra_housing_Year2"] == pytest.approx(39.71)


def test_schema_labels_and_types():
    m = FarmPlanning(); schema = m.schema(); data = m.load_data()
    assert set(schema["tables"]) == set(m.TABLES)
    for table, spec in schema["tables"].items():
        assert spec.get("label"), table
        header = list(read_table(m.DATA_DIR / f"{table}.csv")[0])
        assert set(header) == set(spec["columns"]) and set(spec["key"]) <= set(header), table
        for col, cspec in spec["columns"].items():
            assert cspec.get("label") and cspec.get("description"), (table, col)
            if col not in spec["key"]:
                assert cspec["type"] in ("number", "int"), (table, col)
                assert all(isinstance(r[col], (int, float)) for r in data[table]), (table, col)
    # structural numbers stay out of the data-change templates
    assert schema["tables"]["years"]["columns"]["order"]["editable"] is False
    assert schema["tables"]["ages"]["columns"]["initial_head"]["editable"] is False
    assert schema["tables"]["ages"]["removable"] is False
    assert set(schema["params"]) == set(data["params"])
    assert all(p.get("label") and p.get("description") and p["type"] in ("number", "int")
               for p in schema["params"].values())
    for name in ("heifer_death_rate", "cow_death_rate", "heifer_calf_share"):
        assert (schema["params"][name]["min"], schema["params"][name]["max"]) == (0, 1)
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == m.MEASURE_DIMS
    assert all(v.get("label") for v in schema["measures"].values())


def test_kpis_are_consistent():
    m = FarmPlanning(); data = m.load_data(); P = data["params"]
    k = m.solve(data, solver=SOLVERS[0], time_limit=60).kpis
    assert set(k) == set(m.schema()["kpis"]) and set(m.SCORING_KPIS) <= set(k)
    assert math.isclose(sum(k["revenue"].values()) - sum(k["costs"].values()), k["profit"], abs_tol=0.05)
    assert math.isclose(sum(k["profit_by_year"].values()), k["profit"], abs_tol=0.05)  # no housing loan due later
    cow_years = sum(k["dairy_cows_by_year"].values())
    assert k["dairy_cows_by_year"]["Year5"] == k["final_dairy_cows"]
    assert math.isclose(k["dairy_cows_by_year"]["Year1"], 97.7, abs_tol=1e-6)  # fixed by the initial herd
    born = P["calves_per_cow"] * P["heifer_calf_share"] * cow_years
    assert math.isclose(k["heifer_calves"]["raised"] + k["heifer_calves"]["sold"], born, rel_tol=1e-5)
    assert math.isclose(k["revenue"]["milk"], P["milk_revenue_per_cow"] * cow_years, rel_tol=1e-5)
    assert k["costs"]["labour"] == 5 * P["regular_labour_cost"] and k["costs"]["housing_loan"] == 0


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver")
def test_what_ifs_through_the_oracle():
    m = FarmPlanning()
    base = solve_scenario(m, {"version": "0.1", "data_changes": []}, solver=SOLVERS[0])
    assert base.status == "optimal" and math.isclose(base.objective, m.reference()["objective"], rel_tol=1e-6)
    # every year must make at least 22 000 (Year1 and Year2 make less in the base plan)
    floor = solve_scenario(m, {"version": "0.1", "data_changes": [
        {"op": "set_param", "name": "min_yearly_profit", "value": 22000}]}, solver=SOLVERS[0])
    assert floor.status == "optimal" and floor.objective < base.objective - 10
    assert min(floor.kpis["profit_by_year"].values()) >= 22000 - 0.01
    # housing for only 100 animals: places are added on loan, repayments due after Year5 are charged
    small = solve_scenario(m, {"version": "0.1", "data_changes": [
        {"op": "set_param", "name": "housing_capacity", "value": 100}]}, solver=SOLVERS[0])
    assert small.status == "optimal" and small.objective < base.objective - 1000
    assert small.kpis["extra_housing_places"] > 1 and small.kpis["costs"]["housing_loan"] > 0
    # a rule and a fixed decision on the measures
    rule = solve_scenario(m, {"version": "0.1", "rules": [
        {"measure": "raise_heifers", "scope": {"year": "Year3"}, "sense": ">=", "value": 10}],
        "fixed_decisions": [{"measure": "grow_grain", "scope": {"land_group": "Group2"}, "value": 0}]},
        solver=SOLVERS[0])
    assert rule.status == "optimal" and rule.objective < base.objective - 1
    assert rule.decisions["raise_heifers_Year3"] >= 10 - 1e-6
    assert all(abs(rule.decisions.get(f"grow_grain_{t}_Group2", 0.0)) <= 1e-9 for t in YEARS)
    # a fifth land group of grain land
    more_land = solve_scenario(m, {"version": "0.1", "data_changes": [
        {"op": "add", "table": "land_groups", "rows": [{"land_group": "Group5", "area": 25, "grain_yield": 1.0}]}]},
        solver=SOLVERS[0])
    assert more_land.status == "optimal" and more_land.objective > base.objective + 1


def test_no_solver_import_at_module_level():
    code = ("import sys, whatifgym.models.farm_planning.model; "
            "print(sorted(m for m in ('pulp', 'highspy', 'pyscipopt', 'ortools', 'gurobipy') if m in sys.modules))")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=ROOT, check=True)
    assert out.stdout.strip() == "[]"
