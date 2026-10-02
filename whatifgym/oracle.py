"""Oracle: validate a scenario, apply it to a base model, re-solve, and keep the result.

The oracle is what produces reference solutions for tasks and what the environment runs on the agent's
scenario. The agent never solves anything itself.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .dsl import apply_scenario, validate_scenario
from .registry import get_model


@dataclass
class ScenarioResult:
    model: str
    solver: str
    status: str                      # optimal | infeasible | unbounded | not_solved | time_limit | error | invalid
    objective: float | None
    stage_values: list[float] = field(default_factory=list)
    kpis: dict[str, Any] = field(default_factory=dict)
    decisions: dict[str, float] = field(default_factory=dict)
    n_vars: int = 0
    n_constraints: int = 0
    n_int_vars: int = 0
    n_fixed_vars: int = 0
    n_rules: int = 0
    n_data_changes: int = 0
    solve_time_s: float = 0.0
    wall_time_s: float = 0.0
    scenario_hash: str = ""
    message: str = ""
    validation_errors: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ScenarioResult":
        known = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**known)


def solve_scenario(model_or_name, scenario: dict[str, Any], data: dict[str, Any] | None = None,
                   solver: str = "highs", time_limit: float | None = None,
                   keep_decisions: bool = True) -> ScenarioResult:
    """Validate then solve. Invalid scenarios return ``status == "invalid"`` with the error list."""
    model = get_model(model_or_name) if isinstance(model_or_name, str) else model_or_name
    base = data if data is not None else model.load_data()
    errors = validate_scenario(scenario, model, base, raise_on_error=False)
    if errors:
        return ScenarioResult(model=model.name, solver=solver, status="invalid", objective=None,
                              validation_errors=errors, message="; ".join(e["message"] for e in errors)[:500])
    if "ask" in scenario:
        return ScenarioResult(model=model.name, solver=solver, status="ask", objective=None, message=scenario["ask"])
    raw = apply_scenario(model, scenario, base, solver=solver, time_limit=time_limit, keep_decisions=keep_decisions)
    return ScenarioResult(**raw)


def save_result(result: ScenarioResult, path: str | Path) -> None:
    Path(path).write_text(json.dumps(result.to_dict(), indent=1, default=str), encoding="utf-8")


def load_result(path: str | Path) -> ScenarioResult:
    return ScenarioResult.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
