"""Open-solver access through PuLP (HiGHS, SCIP, CBC) plus availability checks.

Solver names used across whatifgym:

======  =====================================  ==========================
name    backend                                 licence
======  =====================================  ==========================
highs   HiGHS via ``highspy`` (``pulp.HiGHS``)  MIT
scip    SCIP via ``pyscipopt`` (``pulp.SCIP_PY``) Apache-2.0 (SCIP >= 9)
cbc     COIN-OR CBC binary shipped with PuLP     EPL-2.0
cpsat   OR-Tools CP-SAT (integer models only)    Apache-2.0
gurobi  Gurobi via ``gurobipy`` — cross-checks only, never required
======  =====================================  ==========================
"""
from __future__ import annotations

import importlib.util
import time

OPEN_SOLVERS = ("highs", "scip", "cbc", "cpsat")
_PULP_NAMES = {"highs": "HiGHS", "scip": "SCIP_PY", "cbc": "PULP_CBC_CMD", "gurobi": "GUROBI"}


def available_solvers(include_gurobi: bool = False) -> list[str]:
    """Return the solver names usable on this machine, in preferred order.

    Only checks for installed packages (no heavy imports), so it is safe to call from any process.
    """
    found: list[str] = []
    if importlib.util.find_spec("pulp") is not None:
        if importlib.util.find_spec("highspy") is not None:
            found.append("highs")
        if importlib.util.find_spec("pyscipopt") is not None:
            found.append("scip")
        found.append("cbc")  # PuLP ships a CBC binary on most platforms; verified lazily when used
    if importlib.util.find_spec("ortools") is not None:
        found.append("cpsat")
    if include_gurobi and importlib.util.find_spec("gurobipy") is not None:
        found.append("gurobi")
    return found


def pulp_solver(name: str, time_limit: float | None = None, msg: bool = False):
    """Instantiate the PuLP solver object for ``name``."""
    import pulp  # lazy

    if name not in _PULP_NAMES:
        raise ValueError(f"unknown PuLP-backed solver {name!r}; choose from {sorted(_PULP_NAMES)}")
    cls = getattr(pulp, _PULP_NAMES[name])
    kwargs = {"msg": msg}
    if time_limit is not None:
        kwargs["timeLimit"] = float(time_limit)
    solver = cls(**kwargs)
    if not solver.available():
        raise RuntimeError(f"solver {name!r} ({_PULP_NAMES[name]}) is not available in this environment")
    return solver


def pulp_status(prob) -> str:
    import pulp  # lazy

    raw = pulp.LpStatus[prob.status]
    return {"Optimal": "optimal", "Infeasible": "infeasible", "Unbounded": "unbounded",
            "Not Solved": "not_solved", "Undefined": "undefined"}.get(raw, raw.lower())


def pulp_sizes(prob) -> tuple[int, int, int]:
    import pulp  # lazy

    variables = prob.variables()
    n_int = sum(1 for v in variables if v.cat in (pulp.LpInteger, pulp.LpBinary))
    return len(variables), len(prob.constraints), n_int


def solve_pulp(prob, solver: str = "highs", time_limit: float | None = None, msg: bool = False):
    """Solve a PuLP problem. Returns ``(status, objective, wall_time_s, message)``."""
    import pulp  # lazy

    try:
        s = pulp_solver(solver, time_limit=time_limit, msg=msg)
    except Exception as exc:  # solver missing
        return "error", None, 0.0, str(exc)
    t0 = time.perf_counter()
    try:
        prob.solve(s)
    except Exception as exc:
        return "error", None, time.perf_counter() - t0, f"{type(exc).__name__}: {exc}"
    elapsed = time.perf_counter() - t0
    status = pulp_status(prob)
    objective = pulp.value(prob.objective) if status == "optimal" else None
    # PuLP reports a time-limited incumbent as "Optimal" for some backends; flag it if a limit was hit.
    if time_limit is not None and elapsed >= time_limit and status == "optimal":
        status = "time_limit"
    return status, objective, elapsed, ""
