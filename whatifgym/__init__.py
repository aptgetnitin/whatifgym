"""whatifgym: clean-room benchmark and RL environment for LLM what-if agents over optimization models.

Every base model lives in ``whatifgym/models/<name>/`` and exposes the same interface:

* ``load_data()``   -> dict of plain Python records read from ``data/*.csv`` (the editable scenario surface)
* ``build(data)``   -> a ``pulp.LpProblem`` (and, where the model is integer, ``build_cpsat(data)`` -> OR-Tools CP-SAT)
* ``kpis(prob, data)`` -> dict of planner-facing numbers computed from the solved model
* ``description.md`` / ``schema.json`` -> what the model is and what each table/column means

Solver libraries are imported lazily inside functions, never at module import time: on Linux the
``highspy`` and ``ortools`` wheels both bundle ``libhighs.so.1`` and cannot be loaded in one process.
Use :func:`whatifgym.runner.run_subprocess` to solve with any solver from any process.
"""

__version__ = "0.1.0"

from .base import BaseModel, SolveResult, Source  # noqa: E402,F401
from .registry import get_model, list_models  # noqa: E402,F401
