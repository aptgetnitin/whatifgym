"""Economic Planning: reference optimum and size of the original notebook, schema labels, what-if behaviour."""
import math

import pytest

from whatifgym.models.economic_planning.model import EconomicPlanning, _steady_state
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = EconomicPlanning()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    ref = m.reference()
    assert math.isclose(r.objective, ref["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert (r.n_vars, r.n_constraints, r.n_int_vars) == (ref["n_vars"], ref["n_constraints"], ref["n_int_vars"])
    assert math.isclose(r.kpis["employment"], r.objective, abs_tol=0.01)
    # unique at the optimum (min/max over the optimal face agree)
    assert math.isclose(r.kpis["total_production"], 3724.90, abs_tol=0.01)
    assert math.isclose(r.kpis["capacity_built"], 661.06, abs_tol=0.01)


def test_steady_state_matches_static_model():
    m = EconomicPlanning(); data = m.load_data()
    io = {(r["supplier"], r["user"]): r["input_per_unit_output"] for r in data["input_output"]}
    x = _steady_state([r["industry"] for r in data["industries"]], io,
                      {r["industry"]: r["external_demand"] for r in data["industries"]})
    # static_prod values from the original notebook's StaticModel
    assert x == pytest.approx({"coal": 166.39676113, "steel": 105.66801619, "transport": 92.30769231})


def test_sizes_and_measures():
    m = EconomicPlanning(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)


def test_schema_matches_data_and_has_labels():
    m = EconomicPlanning(); data = m.load_data(); schema = m.schema()
    assert set(schema["tables"]) == set(m.TABLES)
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == m.MEASURE_DIMS
    for table, spec in schema["tables"].items():
        assert spec["label"]
        assert set(spec["columns"]) == set(data[table][0]), table
        assert all(col["label"] for col in spec["columns"].values()), table
    assert all(v["label"] for v in schema["measures"].values())


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_moves_objective():
    from whatifgym.oracle import solve_scenario

    m = EconomicPlanning(); data = m.load_data(); solver = SOLVERS[0]
    base = m.reference()["objective"]

    no_coal_capacity = {"version": "0.1", "base_model": m.name, "rules": [
        {"measure": "extra_capacity", "scope": {"industry": "coal"}, "sense": "<=", "value": 0}]}
    r = solve_scenario(m, no_coal_capacity, data, solver=solver, keep_decisions=False)
    assert r.status == "optimal", r.message
    assert r.objective < base - 1.0

    less_stock = {"version": "0.1", "base_model": m.name, "data_changes": [
        {"op": "scale", "table": "industries", "column": "initial_stock", "where": {"industry": "coal"},
         "factor": 0.8}]}
    r = solve_scenario(m, less_stock, data, solver=solver, keep_decisions=False)
    assert r.status == "optimal", r.message
    assert r.objective < base - 1.0
