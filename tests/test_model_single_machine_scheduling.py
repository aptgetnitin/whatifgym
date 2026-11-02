"""single_machine_scheduling: reference optimum on every open solver, port sizes, measures, one what-if."""
import math

import pytest

from whatifgym.dsl import apply_data_changes
from whatifgym.models.single_machine_scheduling.model import SingleMachineScheduling
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = SingleMachineScheduling()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    k = r.kpis
    assert k["makespan"] == 112605 and k["last_job"] == "job_13" and len(k["sequence"]) == 15
    assert math.isclose(k["total_idle_time"] + k["total_setup_time"] + 83552, 112605, abs_tol=1e-3)
    assert k["min_deadline_slack"] >= 0 and set(m.SCORING_KPIS) <= set(k)


def test_sizes_and_measures():
    m = SingleMachineScheduling(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert 50 <= len(prob.variables()) <= 5000
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert set(m.schema()["measures"]) == set(m.MEASURE_DIMS)


@pytest.mark.parametrize("solver", SOLVERS[:1])
def test_later_release_whatif(solver):
    # releasing job_13 (always last) later than the current makespan pushes the makespan to release + duration
    m = SingleMachineScheduling()
    data = apply_data_changes(m.load_data(), [{"op": "set", "table": "jobs", "column": "release_date",
                                               "where": {"job": "job_13"}, "value": 120000}])
    r = m.solve(data, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, 127860, abs_tol=1e-6) and r.kpis["last_job"] == "job_13"
