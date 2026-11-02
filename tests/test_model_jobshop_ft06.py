"""jobshop_ft06: reference optimum on every open solver, port sizes, measures, one what-if."""
import math

import pytest

from whatifgym.dsl import apply_data_changes
from whatifgym.models.jobshop_ft06.model import JobshopFt06
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = JobshopFt06()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis["makespan"] == 55 and r.kpis["idle_by_machine"]["M5"] == 12 and r.kpis["mean_utilisation"] == 59.7
    assert max(r.kpis["completion_by_job"].values()) == 55
    assert set(m.SCORING_KPIS) <= set(r.kpis)


def test_sizes_and_measures():
    m = JobshopFt06(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    assert 50 <= ref["n_vars"] <= 5000
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert set(m.schema()["measures"]) == set(m.MEASURE_DIMS)


@pytest.mark.parametrize("solver", SOLVERS[:1])
def test_release_whatif(solver):
    m = JobshopFt06()
    late = apply_data_changes(m.load_data(), [{"op": "set", "table": "jobs", "column": "release_time",
                                               "where": {"job": "J5"}, "value": 30}])
    r = m.solve(late, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert r.objective >= 55 - 1e-6 and r.kpis["completion_by_job"]["J5"] >= 30 + 30  # J5's processing totals 30
