"""covid19_facility_location: reference optimum on every open solver, original sizes, measures, one what-if."""
import math

import pytest

from whatifgym.dsl import apply_data_changes
from whatifgym.models.covid19_facility_location.model import Covid19FacilityLocation
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = Covid19FacilityLocation()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    k = r.kpis
    assert k["temporary_sites_built"] == ["T15", "T17", "T18"] and k["build_cost"] == 1500000
    assert math.isclose(k["travel_cost"], 21653.42, abs_tol=0.02) and k["extra_beds_added"] < 1e-6
    assert set(m.SCORING_KPIS) <= set(k)


def test_sizes_and_measures():
    m = Covid19FacilityLocation(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert set(m.schema()["measures"]) == set(m.MEASURE_DIMS)


@pytest.mark.parametrize("solver", SOLVERS[:1])
def test_cheaper_build_whatif(solver):
    # a cheaper temporary facility can only lower the cost
    m = Covid19FacilityLocation()
    data = apply_data_changes(m.load_data(), [{"op": "set_param", "name": "temporary_build_cost", "value": 100000}])
    r = m.solve(data, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert r.objective < m.reference()["objective"]
