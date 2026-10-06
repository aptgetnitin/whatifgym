"""The what-if environment: reset/step over tasks, with the oracle as the only solver.

Observation (the OptiGuide stance: structure and keys, never raw numbers):
    model, description, schema, index_sets, table_keys (which rows exist), params (names), measures,
    dsl_schema, examples, question, dialogue, turns_left
Actions:
    {"type": "ask", "text": "..."}                    one clarifying question (the simulator answers from the task)
    {"type": "scenario", "scenario": {...DSL...}}     ends the episode; the oracle solves and the scorer scores
A bare scenario dict (optionally with an `ask` key) is accepted as an action too.
The episode also ends after ``max_turns`` actions without a scenario (reward 0).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .dsl import SCHEMA, validate_scenario
from .oracle import solve_scenario
from .registry import get_model
from .scoring import score_episode
from .tasks import Task

EXAMPLES_DIR = Path(__file__).parent / "dsl" / "examples"


def worked_examples() -> list[dict[str, Any]]:
    out = []
    for p in sorted(EXAMPLES_DIR.glob("*.json")):
        ex = json.loads(p.read_text(encoding="utf-8"))
        if ex.get("_worked_example"):
            out.append({"question": ex.get("_question", ""), "scenario": {k: v for k, v in ex.items() if not k.startswith("_")}})
    return out


class WhatIfEnv:
    def __init__(self, tasks: list[Task], solver: str = "highs", max_turns: int = 3, time_limit: float | None = 60.0):
        if not tasks:
            raise ValueError("no tasks")
        self.tasks = tasks
        self.solver = solver
        self.max_turns = max_turns
        self.time_limit = time_limit
        self._models: dict[str, Any] = {}
        self._data: dict[str, Any] = {}
        self.task: Task | None = None
        self.dialogue: list[dict[str, str]] = []
        self.turn = 0
        self.asked = False
        self.done = True

    # ----------------------------------------------------------------- helpers
    def _model(self, name: str):
        if name not in self._models:
            self._models[name] = get_model(name)
            self._data[name] = self._models[name].load_data()
        return self._models[name], self._data[name]

    def observation(self) -> dict[str, Any]:
        assert self.task is not None
        model, data = self._model(self.task.model)
        return {
            "task_id": self.task.id,
            "model": model.name,
            "title": model.title,
            "description": model.description(),
            "schema": model.schema(),
            "index_sets": model.index_sets(data),
            "table_keys": model.table_keys(data),
            "params": sorted(data.get("params", {})) if isinstance(data.get("params"), dict) else [],
            "measures": {k: list(v) for k, v in model.MEASURE_DIMS.items()},
            "dsl_schema": SCHEMA,
            "examples": worked_examples(),
            "question": self.task.question,
            "dialogue": list(self.dialogue),
            "turns_left": self.max_turns - self.turn,
        }

    # ----------------------------------------------------------------- gym API
    def reset(self, task: Task | int | str | None = None) -> dict[str, Any]:
        if task is None:
            task = self.tasks[0]
        elif isinstance(task, int):
            task = self.tasks[task]
        elif isinstance(task, str):
            task = next(t for t in self.tasks if t.id == task)
        self.task = task
        self.dialogue = []
        self.turn = 0
        self.asked = False
        self.done = False
        return self.observation()

    def step(self, action: dict[str, Any]) -> tuple[dict[str, Any], float, bool, dict[str, Any]]:
        if self.done or self.task is None:
            raise RuntimeError("call reset() first")
        self.turn += 1
        kind, payload = self._parse(action)
        info: dict[str, Any] = {"action": kind, "turn": self.turn}

        if kind == "ask":
            self.asked = True
            answer = (self.task.clarification or {}).get("answer") or \
                "The question is fully specified; nothing to add."
            self.dialogue += [{"role": "agent", "text": payload}, {"role": "planner", "text": answer}]
            info["answer"] = answer
            if self.turn >= self.max_turns:
                return self._finish(None, valid_dsl=False, info=info)
            return self.observation(), 0.0, False, info

        if kind == "scenario":
            model, data = self._model(self.task.model)
            errors = validate_scenario(payload, model, data, raise_on_error=False)
            if errors:
                info["validation_errors"] = errors
                return self._finish(None, valid_dsl=False, info=info)
            try:
                result = solve_scenario(model, payload, data, solver=self.solver, time_limit=self.time_limit,
                                        keep_decisions=False)
            except Exception as exc:  # a scenario the validator missed must cost the episode, not the run
                info["error"] = f"{type(exc).__name__}: {exc}"
                return self._finish(None, valid_dsl=False, info=info)
            info["result"] = result.to_dict()
            return self._finish(result.to_dict(), valid_dsl=True, info=info)

        info["error"] = f"unknown action {kind!r}"
        if self.turn >= self.max_turns:
            return self._finish(None, valid_dsl=False, info=info)
        return self.observation(), 0.0, False, info

    # ----------------------------------------------------------------- internals
    @staticmethod
    def _parse(action: dict[str, Any]) -> tuple[str, Any]:
        if "type" in action:
            if action["type"] == "ask":
                return "ask", action.get("text", "")
            if action["type"] == "scenario":
                return "scenario", action.get("scenario", {})
            return action["type"], action
        if "ask" in action and len([k for k in action if k not in ("version", "base_model", "note")]) == 1:
            return "ask", action["ask"]
        return "scenario", action

    def _finish(self, candidate: dict[str, Any] | None, valid_dsl: bool, info: dict[str, Any]):
        assert self.task is not None
        score = score_episode(self.task.reference, candidate, valid_dsl=valid_dsl, asked=self.asked,
                              ask_needed=self.task.ask_needed, kpi_keys=self.task.kpi_keys)
        info["score"] = score.to_dict()
        info["reference"] = {k: self.task.reference.get(k) for k in ("status", "objective", "kpis")}
        self.done = True
        return self.observation(), score.reward, True, info
