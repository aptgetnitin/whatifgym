"""assignment_with_constraints: reference optimum on every open solver, port sizes, measures, unique plan, one what-if."""
import math

import pytest

from whatifgym.models.assignment_with_constraints.model import AssignmentWithConstraints
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]
PLAN = {"worker_0": ["task_4"], "worker_1": ["task_2"], "worker_5": ["task_5"], "worker_6": ["task_3"],
        "worker_10": ["task_0"], "worker_11": ["task_1"]}


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = AssignmentWithConstraints()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis["assignment"] == PLAN and r.kpis["teams_chosen"] == ["team_0_1", "team_10_11", "team_5_6"]
    assert set(m.SCORING_KPIS) <= set(r.kpis)


def test_sizes_and_measures():
    m = AssignmentWithConstraints(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert set(m.schema()["measures"]) == set(m.MEASURE_DIMS)


@pytest.mark.parametrize("solver", SOLVERS[:1])
def test_forbid_team_whatif(solver):
    # forbidding the chosen team 5+6 (removing its rows) can only raise the cost, and that pair must not work
    m = AssignmentWithConstraints()
    data = m.load_data()
    data["allowed_teams"] = [r for r in data["allowed_teams"] if r["team"] != "team_5_6"]
    r = m.solve(data, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert r.objective > m.reference()["objective"] and "team_5_6" not in r.kpis["teams_chosen"]
    assert not {"worker_5", "worker_6"} <= set(r.kpis["assignment"])
