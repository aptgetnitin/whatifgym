"""optimize_power_schedule reproduces the original Gurobi notebook's optimum and size on the open solvers."""
import math

import pytest

from whatifgym.models.optimize_power_schedule.model import OptimizePowerSchedule
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = OptimizePowerSchedule()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    ref = m.reference()
    assert math.isclose(r.objective, ref["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert (r.n_vars, r.n_constraints, r.n_int_vars) == (ref["n_vars"], ref["n_constraints"], ref["n_int_vars"])
    k = r.kpis
    assert set(k) == set(m.schema()["kpis"]) and set(m.SCORING_KPIS) <= set(k)
    assert math.isclose(k["total_cost"], r.objective, rel_tol=1e-6)
    # breakdown printed by the original notebook run (gurobipy, zero gap)
    assert math.isclose(k["fuel_cost"], 4293478.55, rel_tol=1e-6)
    assert math.isclose(k["health_cost"], 199614.18, rel_tol=1e-6)
    assert k["startup_cost"] == k["shutdown_cost"] == 219


def test_sizes_and_measures():
    m = OptimizePowerSchedule(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)


def test_schema_matches_data_and_has_labels():
    m = OptimizePowerSchedule(); data = m.load_data(); schema = m.schema()
    assert set(schema["tables"]) == set(m.TABLES)
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == m.MEASURE_DIMS
    for table, spec in schema["tables"].items():
        assert spec["label"]
        assert set(spec["columns"]) == set(data[table][0]), table
        assert all(col["label"] for col in spec["columns"].values()), table


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_moves_objective():
    from whatifgym.oracle import solve_scenario

    m = OptimizePowerSchedule(); base = m.reference()["objective"]
    gas_up = {"version": "0.1", "base_model": m.name, "data_changes": [
        {"op": "scale", "table": "fuels", "column": "fuel_cost", "where": {"fuel": "NG"}, "factor": 1.5}]}
    r = solve_scenario(m, gas_up, solver=SOLVERS[0], time_limit=60, keep_decisions=False)
    assert r.status == "optimal", r.message
    assert r.objective > base + 1.0
    no_must_run = {"version": "0.1", "base_model": m.name, "relax": [{"constraint": "must_run"}]}
    r = solve_scenario(m, no_must_run, solver=SOLVERS[0], time_limit=60, keep_decisions=False)
    assert r.status == "optimal", r.message
    assert r.objective <= base + 1e-6
