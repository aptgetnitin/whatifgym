"""car_rental (Gurobi modeling-examples car_rental_1): reference optimum on the open solvers, sizes, measures."""
import math

import pytest

from whatifgym.models.car_rental.model import CarRental
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = CarRental()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis


def test_sizes_and_measures():
    m = CarRental(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert all(len(key) == len(ms[name].dims) for name in ms for key in ms[name].vars)
    assert m.schema()["model"] == m.name and m.index_sets(data)


def test_schema_matches_data_and_carries_labels():
    m = CarRental(); data = m.load_data(); schema = m.schema()
    assert set(schema["tables"]) == set(m.TABLES) and set(schema["params"]) == set(data["params"])
    assert all(set(spec["columns"]) == set(data[t][0]) for t, spec in schema["tables"].items())
    assert all(spec["label"] for spec in schema["tables"].values())
    assert all(c["label"] for spec in schema["tables"].values() for c in spec["columns"].values())
    assert all(p["label"] for p in schema["params"].values())
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == m.MEASURE_DIMS
    assert all(v["label"] for v in schema["measures"].values())


def test_more_repair_capacity_raises_profit():
    """Repair capacity is the binding resource: 10% of rentals come back damaged and must be repaired."""
    m = CarRental()
    data = m.load_data()
    base = m.solve(data, solver=SOLVERS[0])
    for row in data["depots"]:
        if row["depot"] == "Birmingham":
            row["repair_capacity"] = 25
    more = m.solve(data, solver=SOLVERS[0])
    assert base.kpis["repair_utilisation"] == {"Manchester": 1.0, "Birmingham": 1.0}
    assert more.status == "optimal" and more.objective > base.objective
    assert more.kpis["cars_rented"] > base.kpis["cars_rented"] == 1920.0
