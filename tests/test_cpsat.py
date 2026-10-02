"""CP-SAT formulations agree with the MIP formulations. Runs in a subprocess because highspy and ortools
cannot be loaded in the same Linux process."""
import math

import pytest

from whatifgym import get_model, list_models
from whatifgym.runner import run_subprocess
from whatifgym.solvers import available_solvers

pytestmark = pytest.mark.skipif("cpsat" not in available_solvers(), reason="ortools not installed")


@pytest.mark.parametrize("name", [n for n in list_models() if get_model(n).supports_cpsat])
def test_cpsat_matches_reference(name):
    model = get_model(name)
    result = run_subprocess(name, "cpsat", time_limit=120, timeout=300)
    assert result["status"] == "optimal", result.get("message")
    assert math.isclose(result["objective"], model.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert result["n_vars"] == model.reference()["n_vars"]


def test_cpsat_refused_for_continuous_model():
    result = run_subprocess("factory_planning", "cpsat")
    assert result["status"] == "error" and "no CP-SAT" in result["message"]
