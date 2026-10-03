"""Food Manufacture I: reference optimum and size of the original notebook, schema labels, what-if behaviour."""
import math

import pytest

from whatifgym.models.food_manufacture.model import FoodManufacture
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = FoodManufacture()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    ref = m.reference()
    assert math.isclose(r.objective, ref["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert (r.n_vars, r.n_constraints, r.n_int_vars) == (ref["n_vars"], ref["n_constraints"], ref["n_int_vars"])
    assert r.kpis
    assert math.isclose(r.kpis["profit"], r.objective, abs_tol=0.01)
    # unique at the optimum (both refining lines full every month); the purchase/storage split is not
    assert math.isclose(r.kpis["food_produced"], 2700.0, abs_tol=0.1)
    assert math.isclose(r.kpis["revenue"], 405000.0, abs_tol=1.0)


def test_sizes_and_measures():
    m = FoodManufacture(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)


def test_schema_matches_data_and_has_labels():
    m = FoodManufacture(); data = m.load_data(); schema = m.schema()
    assert set(schema["tables"]) == set(m.TABLES)
    assert set(schema["params"]) == set(data["params"])
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == m.MEASURE_DIMS
    for table, spec in schema["tables"].items():
        assert spec["label"]
        assert set(spec["columns"]) == set(data[table][0]), table
        assert all(col["label"] for col in spec["columns"].values()), table
    assert all(p["label"] for p in schema["params"].values())
    assert all(v["label"] for v in schema["measures"].values())


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_moves_objective():
    from whatifgym.oracle import solve_scenario

    m = FoodManufacture(); data = m.load_data(); solver = SOLVERS[0]
    base = m.reference()["objective"]

    dearer = {"version": "0.1", "base_model": m.name, "data_changes": [
        {"op": "scale", "table": "purchase_prices", "column": "price", "where": {"oil": "VEG1", "month": "Jun"},
         "factor": 1.2}]}
    r = solve_scenario(m, dearer, data, solver=solver, keep_decisions=False)
    assert r.status == "optimal", r.message
    assert r.objective < base - 1.0

    # the closing-stock target alone can change: the wrap-around rows stay redundant (no typo-induced infeasibility)
    less_stock = {"version": "0.1", "base_model": m.name, "data_changes": [
        {"op": "set_param", "name": "final_stock", "value": 300}]}
    r = solve_scenario(m, less_stock, data, solver=solver, keep_decisions=False)
    assert r.status == "optimal", r.message
    assert r.objective > base + 1.0

    capped = {"version": "0.1", "base_model": m.name, "rules": [
        {"measure": "buy", "scope": {"oil": "OIL2"}, "sense": "<=", "value": 500}]}
    r = solve_scenario(m, capped, data, solver=solver, keep_decisions=False)
    assert r.status == "optimal", r.message
    assert r.objective < base - 1.0
