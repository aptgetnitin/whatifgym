"""bin_packing: reference optimum on every open solver, original sizes, measures, CP-SAT agreement, one what-if."""
import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

from whatifgym.dsl import apply_data_changes
from whatifgym.models.bin_packing.model import BinPacking
from whatifgym.solvers import available_solvers

ROOT = Path(__file__).resolve().parents[1]
SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


def _check_packing(kpis, data):
    """Alternative optima pack differently; check the packing is valid rather than which bins are used."""
    capacity = {r["bin"]: r["capacity"] for r in data["bins"]}
    packed = sorted(i for items in kpis["bin_items"].values() for i in items)
    assert packed == sorted(r["item"] for r in data["items"])
    assert all(load <= capacity[b] for b, load in kpis["bin_load"].items())
    assert kpis["bins_used"] == len(kpis["bin_load"])


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = BinPacking()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis
    assert r.kpis["bins_used"] == 4 and r.kpis["total_weight"] == 370 and r.kpis["min_bins_by_weight"] == 4
    _check_packing(r.kpis, m.load_data())


def test_sizes_and_measures():
    m = BinPacking(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert set(m.schema()["measures"]) == set(m.MEASURE_DIMS)


@pytest.mark.skipif("cpsat" not in available_solvers(), reason="ortools not installed")
def test_cpsat_matches_reference():
    # own interpreter: highspy and ortools cannot share a Linux process
    code = ("import json; from whatifgym.models.bin_packing.model import BinPacking; "
            "print(json.dumps(BinPacking().solve_cpsat(time_limit=60).to_dict(), default=str))")
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=300, cwd=ROOT)
    assert proc.returncode == 0, proc.stderr[-2000:]
    r = json.loads(proc.stdout.strip().splitlines()[-1])
    ref = BinPacking.reference()
    assert r["status"] == "optimal", r["message"]
    assert math.isclose(r["objective"], ref["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert (r["n_vars"], r["n_constraints"]) == (ref["n_vars"], ref["n_constraints"])
    _check_packing(r["kpis"], BinPacking.load_data())


@pytest.mark.parametrize("solver", SOLVERS[:1])
def test_capacity_whatif(solver):
    # bins of 90 cannot hold 370 units in four bins: the weight bound rises to ceil(370 / 90) = 5
    m = BinPacking()
    data = apply_data_changes(m.load_data(), [{"op": "set", "table": "bins", "column": "capacity", "value": 90}])
    r = m.solve(data, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, 5.0) and r.kpis["min_bins_by_weight"] == 5
    _check_packing(r.kpis, data)
