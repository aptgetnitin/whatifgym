"""Mining (Gurobi modeling-examples): reference optimum on the open solvers, sizes, measures, one what-if."""
import math

import pytest

from whatifgym.models.mining.model import Mining
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = Mining()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis
    assert math.isclose(r.kpis["profit"], r.objective, rel_tol=1e-6)
    assert r.kpis["years_open_by_mine"] == {"Mine1": 5, "Mine2": 5, "Mine3": 5, "Mine4": 4}


def test_sizes_and_measures():
    m = Mining(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)


def test_schema_labels_and_types():
    schema = Mining.schema()
    assert set(schema["tables"]) == set(Mining.TABLES)
    for table in schema["tables"].values():
        assert table["label"] and all(col["label"] for col in table["columns"].values())
    assert set(schema["params"]) == set(Mining.load_data()["params"])
    assert all(p["label"] and p["type"] in ("number", "int") for p in schema["params"].values())
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == Mining.MEASURE_DIMS
    assert all(v["label"] for v in schema["measures"].values())


@pytest.mark.skipif(not SOLVERS, reason="no open MIP solver")
def test_what_if_moves_objective():
    m = Mining()
    base = m.solve(solver=SOLVERS[0], time_limit=60)
    data = m.load_data()
    data["params"]["max_mines"] = 2  # only two mines may be worked each year
    tighter = m.solve(data, solver=SOLVERS[0], time_limit=60)
    assert tighter.status == "optimal" and tighter.objective < base.objective - 1.0
    assert max(tighter.kpis["mines_worked_by_year"].values()) <= 2
