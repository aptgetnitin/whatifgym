"""technician_routing_scheduling reproduces the original Gurobi notebook's Sce3 optimum and size on the open solvers."""
import math

import pytest

from whatifgym.models.technician_routing_scheduling.model import TechnicianRoutingScheduling
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = TechnicianRoutingScheduling()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    ref = m.reference()
    assert math.isclose(r.objective, ref["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert (r.n_vars, r.n_constraints, r.n_int_vars) == (ref["n_vars"], ref["n_constraints"], ref["n_int_vars"])
    k = r.kpis
    assert set(k) == set(m.schema()["kpis"]) and set(m.SCORING_KPIS) <= set(k)
    assert math.isclose(k["total_penalty"], r.objective, rel_tol=1e-6)
    # Customer4 unfilled (2 * 6100), Customer5 105 min late (2 * 105), as in the notebook run
    assert (k["unfilled_penalty"], k["jobs_unfilled"]) == (12200, 1)
    assert math.isclose(k["lateness_minutes"], 105, abs_tol=1e-4) and abs(k["window_penalty"]) < 1e-4


def test_sizes_and_measures():
    m = TechnicianRoutingScheduling(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)


def test_schema_matches_data_and_has_labels():
    m = TechnicianRoutingScheduling(); data = m.load_data(); schema = m.schema()
    assert set(schema["tables"]) == set(m.TABLES)
    assert set(schema["params"]) == set(data["params"])
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == m.MEASURE_DIMS
    assert all(v["label"] for v in schema["measures"].values())
    for table, spec in schema["tables"].items():
        assert spec["label"]
        assert set(spec["columns"]) == set(data[table][0]), table
        assert all(col["label"] for col in spec["columns"].values()), table


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_moves_objective():
    m = TechnicianRoutingScheduling(); data = m.load_data()
    # train Albert (Heidelberg, idle at the optimum) for installations: Customer4 can now be served
    for row in data["skills"]:
        if (row["technician"], row["job_type"]) == ("Albert", "Equipment Installation"):
            row["qualified"] = 1
    r = m.solve(data, solver=SOLVERS[0], time_limit=60)
    assert r.status == "optimal", r.message
    assert r.objective < m.reference()["objective"] - 1.0
