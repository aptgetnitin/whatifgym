"""railway_dispatching: reference optimum on every open solver, original sizes, measures, two what-ifs."""
import math

import pytest

from whatifgym.dsl import apply_data_changes
from whatifgym.models.railway_dispatching.model import RailwayDispatching
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = RailwayDispatching()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis["total_delay"] == 47 and r.kpis["trains_delayed"] == 4
    assert r.kpis["delay_by_train"]["C"] == 0 and r.kpis["delay_by_train"]["E"] == 6


def test_sizes_and_measures():
    m = RailwayDispatching(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert set(m.schema()["measures"]) == set(m.MEASURE_DIMS)


@pytest.mark.parametrize("solver", SOLVERS[:1])
def test_whatifs(solver):
    m = RailwayDispatching(); base = m.reference()["objective"]
    late = apply_data_changes(m.load_data(), [{"op": "set", "table": "trains", "column": "ready_time",
                                               "where": {"train": "E"}, "value": 10}])
    r = m.solve(late, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, 55, abs_tol=1e-6) and r.kpis["delay_by_train"]["E"] >= 10
    double = apply_data_changes(m.load_data(), [{"op": "set", "table": "resources", "column": "capacity",
                                                 "where": {"resource": 3}, "value": 2}])
    r = m.solve(double, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, 12, abs_tol=1e-6)  # a second track 2-4 removes most of the delay
