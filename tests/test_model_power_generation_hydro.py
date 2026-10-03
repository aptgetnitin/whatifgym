"""power_generation_hydro reproduces the original Gurobi notebook's optimum and size on the open solvers."""
import math

import pytest

from whatifgym.models.power_generation_hydro.model import PowerGenerationHydro
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = PowerGenerationHydro()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis
    assert math.isclose(r.kpis["total_cost"], r.objective, rel_tol=1e-6)


def test_sizes_and_measures():
    m = PowerGenerationHydro(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_peak_demand():
    from whatifgym.oracle import solve_scenario

    m = PowerGenerationHydro()
    scenario = {"version": "0.1", "base_model": m.name, "data_changes": [
        {"op": "scale", "table": "periods", "column": "demand_mw", "where": {"period": "15-18"}, "factor": 1.1}]}
    r = solve_scenario(m, scenario, solver=SOLVERS[0], time_limit=60, keep_decisions=False)
    assert r.status == "optimal", r.message
    assert r.objective > m.reference()["objective"] + 1.0
