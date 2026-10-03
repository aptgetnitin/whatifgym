"""Factory Planning II: reference optimum on every open solver, original model sizes, measures and metadata."""
import copy
import math

import pytest

from whatifgym.models.factory_planning_2.model import FactoryPlanning2
from whatifgym.solvers import available_solvers, pulp_sizes

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = FactoryPlanning2()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis
    # every machine type gets exactly its required maintenance, whichever optimal calendar the solver picks
    required = {row["machine"]: row["machines_to_maintain"] for row in m.load_data()["maintenance"]}
    assert {mc: sum(plan.values()) for mc, plan in r.kpis["maintenance_plan"].items()} == required


def test_sizes_and_measures():
    m = FactoryPlanning2(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert pulp_sizes(prob) == (ref["n_vars"], ref["n_constraints"], ref["n_int_vars"])
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)


def test_schema_labels_and_measures():
    schema = FactoryPlanning2.schema()
    assert set(schema["tables"]) == set(FactoryPlanning2.TABLES)
    for table, spec in schema["tables"].items():
        assert spec.get("label"), table
        assert all(col.get("label") for col in spec["columns"].values()), table
    assert all(p.get("label") for p in schema["params"].values())
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == FactoryPlanning2.MEASURE_DIMS
    assert all(v.get("label") for v in schema["measures"].values())


def test_maintenance_requirement_is_data():
    """The maintenance table drives the model: skipping the planer service frees capacity, a third grinder is scheduled."""
    m = FactoryPlanning2()
    base = m.reference()["objective"]

    def solve_with(machine, n):
        data = copy.deepcopy(m.load_data())
        for row in data["maintenance"]:
            if row["machine"] == machine:
                row["machines_to_maintain"] = n
        r = m.solve(data, solver=SOLVERS[0], time_limit=60)
        assert r.status == "optimal", r.message
        return r

    no_planer = solve_with("planer", 0)
    # the same edit applied to the original notebook code (gurobipy) gives 111305
    assert math.isclose(no_planer.objective, 111305.0, rel_tol=1e-6) and no_planer.kpis["maintenance_plan"]["planer"] == {}
    third_grinder = solve_with("grinder", 3)  # more maintenance can never raise profit (here it is free: 108855)
    assert third_grinder.objective <= base + 1e-6
    assert sum(third_grinder.kpis["maintenance_plan"]["grinder"].values()) == 3
