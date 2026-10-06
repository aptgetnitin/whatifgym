"""Task records: a question, a hidden reference scenario, and the oracle's reference result."""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass
class Task:
    id: str
    family: str
    model: str
    question: str
    scenario: dict[str, Any]                  # hidden gold scenario (DSL)
    reference: dict[str, Any]                 # oracle result for the gold scenario (status, objective, kpis, ...)
    kpi_keys: list[str]                       # the family's KPIs used for scoring
    difficulty: str = "easy"                  # easy | medium | hard
    template: str = ""
    slots: dict[str, Any] = field(default_factory=dict)
    split: str = "train"                      # train | dev | test
    clarification: dict[str, Any] | None = None  # {"question_hint", "answer"} for under-specified tasks
    history: list[dict[str, Any]] | None = None   # chained tasks: earlier [{question, scenario}] already applied
    tags: list[str] = field(default_factory=list)

    @property
    def ask_needed(self) -> bool:
        return self.clarification is not None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Task":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


def split_for(task_id: str, train: float = 0.7, dev: float = 0.15) -> str:
    """Deterministic split from the task id (so regenerating never moves a task between splits)."""
    h = int(hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:8], 16) / 0xFFFFFFFF
    return "train" if h < train else ("dev" if h < train + dev else "test")


def save_tasks(tasks: Iterable[Task], path: str | Path) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(path, "w", encoding="utf-8") as fh:
        for t in tasks:
            fh.write(json.dumps(t.to_dict(), default=str) + "\n")
            n += 1
    return n


def load_tasks(path: str | Path, split: str | None = None) -> list[Task]:
    tasks = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                t = Task.from_dict(json.loads(line))
                if split is None or t.split == split:
                    tasks.append(t)
    return tasks
