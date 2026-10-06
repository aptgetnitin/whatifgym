"""Every base model solves to its reference optimum on the open MIP/LP solvers (in-process via PuLP)."""
import math

import pytest

from whatifgym import get_model, list_models
from whatifgym.solvers import available_solvers

PULP_SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]
EXPECTED_SIZES = {"factory_planning": (126, 79, 0), "multiple_knapsack": (75, 20, 75), "wedding_seating": (3213, 18, 3213),
                  "factory_planning_2": (156, 84, 30), "food_manufacture": (96, 70, 0), "mining": (65, 71, 40),
                  "manpower_planning": (72, 30, 0), "power_generation_hydro": (75, 85, 50), "bin_packing": (132, 22, 132),
                  "car_rental": (289, 97, 0), "farm_planning": (131, 116, 0), "battery_scheduling": (72, 25, 0),
                  "car_rental_2": (294, 118, 5), "food_supply": (1397, 437, 0)}


@pytest.mark.parametrize("solver", PULP_SOLVERS)
@pytest.mark.parametrize("name", list_models())
def test_reference_objective(name, solver):
    model = get_model(name)
    result = model.solve(solver=solver, time_limit=60)
    if result.status == "error" and "not available" in result.message:
        pytest.skip(result.message)
    assert result.status == "optimal", result.message
    assert math.isclose(result.objective, model.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert result.kpis, "kpis() must return something for an optimal solve"


@pytest.mark.parametrize("name", list_models())
def test_sizes_and_metadata(name):
    model = get_model(name)
    prob = model.build(model.load_data())
    n_vars, n_cons, n_int = len(prob.variables()), len(prob.constraints), sum(
        1 for v in prob.variables() if v.cat in ("Integer", "Binary"))
    assert (n_vars, n_cons, n_int) == EXPECTED_SIZES[name]
    assert model.source is not None and model.source.license in ("Apache-2.0", "MIT", "BSD-3-Clause")
    assert model.description().strip() and model.schema()["model"] == name
    assert 50 <= n_vars <= 5000, "base models must have 50 to 5000 variables"
