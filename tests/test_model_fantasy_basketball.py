"""fantasy_basketball: reference optimum on every open solver, original sizes, measures, one what-if."""
import math

import pytest

from whatifgym.dsl import apply_data_changes
from whatifgym.models.fantasy_basketball.model import FantasyBasketball
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]
LINEUP = {"PG": ["Jarrett Jack"], "SG": ["Trevor Ariza"], "SF": ["Markieff Morris"], "PF": ["Dario Saric"], "C": ["Joel Embiid"]}


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = FantasyBasketball()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis["lineup"] == LINEUP and r.kpis["total_salary"] == 29700 and r.kpis["players_selected"] == 5


def test_sizes_and_measures():
    m = FantasyBasketball(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert set(m.schema()["measures"]) == set(m.MEASURE_DIMS)


@pytest.mark.parametrize("solver", SOLVERS[:1])
def test_salary_cap_whatif(solver):
    # a tighter cap can only lower the points and must be respected
    m = FantasyBasketball()
    data = apply_data_changes(m.load_data(), [{"op": "set_param", "name": "salary_cap", "value": 25000}])
    r = m.solve(data, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert r.objective < m.reference()["objective"] and r.kpis["total_salary"] <= 25000
