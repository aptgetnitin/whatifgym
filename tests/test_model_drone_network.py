"""drone_network: reference objective on every open solver, original sizes, measures, one what-if."""
import math

import pytest

from whatifgym.dsl import apply_data_changes
from whatifgym.models.drone_network.model import DroneNetwork
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]
OPENED = ["21 MUNICIPAL CTR Fire Station", "800 VIRGINIA BEACH BLVD Fire Station",
          "3769 E. STRATFORD ROAD Rescue Squad", "5145 RURITAN COURT Rescue Squad"]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = DroneNetwork()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    k = r.kpis
    assert k["bases_selected"] == OPENED and k["bases_opened"] == 4
    assert math.isclose(k["avg_flight_minutes"], 2.2391, abs_tol=1e-3)
    assert set(m.SCORING_KPIS) <= set(k)


def test_sizes_and_measures():
    m = DroneNetwork(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert set(m.schema()["measures"]) == set(m.MEASURE_DIMS)


@pytest.mark.parametrize("solver", SOLVERS[:1])
def test_fewer_drones_whatif(solver):
    # fewer drones can only lengthen the expected response
    m = DroneNetwork()
    data = apply_data_changes(m.load_data(), [{"op": "set_param", "name": "max_bases", "value": 3}])
    r = m.solve(data, solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert r.objective > m.reference()["objective"] and r.kpis["bases_opened"] == 3
