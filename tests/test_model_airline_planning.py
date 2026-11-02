"""airline_planning: reference optimum on every open solver, original sizes, measures, two what-ifs."""
import math

import pytest

from whatifgym.dsl import apply_data_changes
from whatifgym.models.airline_planning.model import AirlinePlanning
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = AirlinePlanning()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis["passengers_carried"] == 6570 and r.kpis["revenue_flights_operated"] == 51
    assert math.isclose(r.kpis["revenue_kept"] + r.kpis["lost_revenue"], 1878476)


def test_sizes_and_measures():
    m = AirlinePlanning(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert set(m.schema()["measures"]) == set(m.MEASURE_DIMS)


@pytest.mark.parametrize("solver", SOLVERS[:1])
def test_whatifs(solver):
    m = AirlinePlanning(); base = m.reference()["objective"]
    full = apply_data_changes(m.load_data(), [{"op": "set", "table": "airports", "column": "capacity_share",
                                               "where": {"airport": a}, "value": 1.0} for a in ("ORY", "CDG", "LYS", "NCE")])
    r = m.solve(full, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    # even at full capacity 492,049.5 is lost: on the 4-airport cut many rotations cannot start or end where they must
    assert math.isclose(r.objective, 492049.5, abs_tol=1e-6) and r.objective < base
    closed = apply_data_changes(m.load_data(), [{"op": "set", "table": "airports", "column": "capacity_share",
                                                 "where": {"airport": "NCE"}, "value": 0}])
    r = m.solve(closed, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert r.objective > base
