"""Solve a (model, solver) pair, optionally in a fresh subprocess.

Why a subprocess: ``highspy`` and ``ortools`` cannot share a Linux process (both bundle
``libhighs.so.1``), and an RL environment wants solver isolation and hard timeouts anyway.

CLI::

    python -m whatifgym.runner --model factory_planning --solver highs
    python -m whatifgym.runner --model multiple_knapsack --solver cpsat --json
    python -m whatifgym.runner --model wedding_seating --solver scip --data-dir scenarios/four_tables
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from .registry import get_model


def run(model: str, solver: str = "highs", data_dir: str | Path | None = None,
        time_limit: float | None = None, keep_variables: bool = False) -> dict[str, Any]:
    """Solve in the current process and return a JSON-serialisable dict."""
    m = get_model(model)
    data = m.load_data(data_dir)
    if solver == "cpsat":
        if not m.supports_cpsat:
            return {"model": model, "solver": solver, "status": "error",
                    "message": f"{model} has no CP-SAT formulation", "objective": None, "time_s": 0.0,
                    "n_vars": 0, "n_constraints": 0, "n_int_vars": 0, "kpis": {}, "variables": {}}
        result = m.solve_cpsat(data, time_limit=time_limit)
    else:
        result = m.solve(data, solver=solver, time_limit=time_limit, keep_variables=keep_variables)
    return result.to_dict()


def run_subprocess(model: str, solver: str = "highs", data_dir: str | Path | None = None,
                   time_limit: float | None = None, timeout: float = 300.0,
                   keep_variables: bool = False, python: str | None = None) -> dict[str, Any]:
    """Solve in a fresh interpreter (same Python as the caller by default) and return the result dict."""
    cmd = [python or sys.executable, "-m", "whatifgym.runner", "--model", model, "--solver", solver, "--json"]
    if data_dir is not None:
        cmd += ["--data-dir", str(data_dir)]
    if time_limit is not None:
        cmd += ["--time-limit", str(time_limit)]
    if keep_variables:
        cmd.append("--variables")
    root = Path(__file__).resolve().parents[1]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=root)
    except subprocess.TimeoutExpired:
        return {"model": model, "solver": solver, "status": "timeout", "objective": None,
                "time_s": timeout, "n_vars": 0, "n_constraints": 0, "n_int_vars": 0, "kpis": {},
                "variables": {}, "message": f"subprocess exceeded {timeout}s"}
    # The last stdout line is the JSON payload (solver libraries may print before it). A non-zero exit
    # code only means the status was not optimal; the payload is still there unless the process crashed.
    lines = proc.stdout.strip().splitlines()
    if lines:
        try:
            return json.loads(lines[-1])
        except json.JSONDecodeError:
            pass
    return {"model": model, "solver": solver, "status": "error", "objective": None, "time_s": 0.0,
            "n_vars": 0, "n_constraints": 0, "n_int_vars": 0, "kpis": {}, "variables": {},
            "message": (proc.stderr or proc.stdout).strip()[-2000:] or f"exit code {proc.returncode}"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Solve one whatifgym model with one solver.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--solver", default="highs", help="highs | scip | cbc | cpsat | gurobi")
    parser.add_argument("--data-dir", default=None, help="directory with the model's CSV tables (default: shipped data)")
    parser.add_argument("--time-limit", type=float, default=None)
    parser.add_argument("--variables", action="store_true", help="include non-zero variable values")
    parser.add_argument("--json", action="store_true", help="print a single JSON line (machine-readable)")
    args = parser.parse_args(argv)

    result = run(args.model, args.solver, args.data_dir, args.time_limit, keep_variables=args.variables)
    if args.json:
        print(json.dumps(result, default=str))
    else:
        print(f"{result['model']} / {result['solver']}: {result['status']}  objective={result['objective']}"
              f"  time={result['time_s']:.3f}s  vars={result['n_vars']} cons={result['n_constraints']}")
        for k, v in result.get("kpis", {}).items():
            print(f"  {k}: {v}")
        if result.get("message"):
            print("  " + result["message"])
    return 0 if result["status"] in ("optimal", "time_limit") else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
