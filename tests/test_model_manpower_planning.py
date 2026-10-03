"""manpower_planning: reference optimum and size of the original Gurobi notebook, on every open LP solver."""
import math
import subprocess
import sys
from pathlib import Path

import pytest

from whatifgym.base import read_table
from whatifgym.models.manpower_planning.model import ManpowerPlanning
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]
ROOT = Path(__file__).resolve().parents[1]
# The notebook's second objective (minimum total cost), from the same gurobipy run as reference.json (see its notes).
COST_OPTIMUM = 498677.2853185595


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = ManpowerPlanning()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis
    assert math.isclose(r.kpis["total_redundancy"], r.objective, abs_tol=0.01)
    assert r.kpis["redundancy_by_year"] == {1: 443.0, 2: 166.3, 3: 232.5}  # unique across alternative optima


def test_sizes_and_measures():
    m = ManpowerPlanning(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat != "Continuous") == ref["n_int_vars"] == 0
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    # retrain / downgrade hold the 3 upward / 3 downward moves per year; the inert same-level columns are in no measure
    assert len(ms["retrain"].vars) == len(ms["downgrade"].vars) == 9
    in_measures = {id(v) for meas in ms.values() for v in meas.vars.values()}
    assert not any(id(v) in in_measures for v in prob._wig["same_level"].values())


@pytest.mark.parametrize("solver", SOLVERS)
def test_alternative_cost_objective(solver):
    from whatifgym import solvers

    m = ManpowerPlanning(); data = m.load_data(); prob = m.build(data)
    prob.setObjective(m.cost_expression(prob, data))
    status, objective, _, message = solvers.solve_pulp(prob, solver, time_limit=60)
    assert status == "optimal", message
    assert math.isclose(objective, COST_OPTIMUM, rel_tol=1e-6)
    ref = m.reference()
    assert solvers.pulp_sizes(prob) == (ref["n_vars"], ref["n_constraints"], ref["n_int_vars"])
    assert math.isclose(m.kpis(prob, data)["total_cost"], COST_OPTIMUM, abs_tol=0.01)


def test_schema_covers_data_with_labels():
    m = ManpowerPlanning(); schema = m.schema(); data = m.load_data()
    assert set(schema["tables"]) == set(m.TABLES)
    for table, spec in schema["tables"].items():
        assert spec.get("label"), table
        header = list(read_table(m.DATA_DIR / f"{table}.csv")[0])
        assert set(header) == set(spec["columns"]), table
        assert set(spec["key"]) <= set(header)
        for col, cspec in spec["columns"].items():
            assert cspec.get("label") and cspec.get("description"), (table, col)
            if col not in spec["key"]:
                assert cspec["type"] in ("number", "int"), (table, col)
                assert all(isinstance(r[col], (int, float)) for r in data[table]), (table, col)
    assert set(schema["params"]) == set(data["params"])
    assert all(p.get("label") and p["type"] in ("number", "int") for p in schema["params"].values())
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == m.MEASURE_DIMS
    assert all(v.get("label") for v in schema["measures"].values())


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver")
def test_what_if_more_retraining_places_cuts_redundancy():
    m = ManpowerPlanning(); data = m.load_data()
    for row in data["retraining"]:
        if (row["from_skill"], row["to_skill"]) == ("unskilled", "semi_skilled"):
            row["max_per_year"] = 300
    r = m.solve(data, solver=SOLVERS[0], time_limit=60)
    assert r.status == "optimal", r.message
    assert r.objective < m.reference()["objective"] - 100


def test_no_solver_import_at_module_level():
    code = ("import sys, whatifgym.models.manpower_planning.model; "
            "print(sorted(m for m in ('pulp', 'highspy', 'pyscipopt', 'ortools', 'gurobipy') if m in sys.modules))")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=ROOT, check=True)
    assert out.stdout.strip() == "[]"
