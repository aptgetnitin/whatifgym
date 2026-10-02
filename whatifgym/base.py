"""Common interface for every base model in whatifgym.

Design rules
------------
* Data is the scenario surface. Everything a planner might change lives in ``data/*.csv``; the Python
  code only turns records into a model. A what-if scenario is therefore a *data edit*, which can be
  validated, diffed and audited, instead of a code edit.
* No solver library is imported at module level (see ``whatifgym/__init__.py`` for why).
* ``load_data`` returns plain ``list[dict]`` records and a ``params`` dict so that models have no
  pandas dependency and so that LLM-written scenario code has as little surface as possible.
"""
from __future__ import annotations

import csv
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Source:
    """Where the model and its data were taken from (for attribution and licence tracking)."""

    repo: str
    path: str
    url: str
    license: str
    notes: str = ""


@dataclass
class SolveResult:
    model: str
    solver: str
    status: str                       # optimal | infeasible | unbounded | not_solved | time_limit | error
    objective: float | None
    time_s: float
    n_vars: int
    n_constraints: int
    n_int_vars: int
    kpis: dict[str, Any] = field(default_factory=dict)
    variables: dict[str, float] = field(default_factory=dict)
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Measure:
    """A family of decision variables exposed to the scenario DSL (e.g. ``make[month, product]``)."""

    name: str
    dims: tuple[str, ...]
    vars: dict[tuple, Any]  # index tuple (aligned with dims) -> solver variable

    def values(self, dim: str) -> list:
        i = self.dims.index(dim)
        seen: dict = {}
        for key in self.vars:
            seen.setdefault(key[i], None)
        return list(seen)

    def select(self, scope: dict[str, Any] | None) -> list:
        """Variables whose index matches ``scope`` (dimension -> value or list of values; missing = all)."""
        scope = scope or {}
        wanted = {}
        for dim, val in scope.items():
            if dim not in self.dims:
                raise KeyError(f"measure {self.name!r} has no dimension {dim!r}; dimensions are {list(self.dims)}")
            wanted[self.dims.index(dim)] = set(val) if isinstance(val, (list, tuple, set)) else {val}
        return [v for key, v in self.vars.items() if all(key[i] in allowed for i, allowed in wanted.items())]


def _coerce(value: str) -> Any:
    """Turn CSV strings into int/float/bool where they obviously are one; keep text otherwise."""
    s = value.strip()
    if s == "":
        return None
    low = s.lower()
    if low in ("true", "false"):
        return low == "true"
    try:
        if s.lstrip("+-").isdigit():
            return int(s)
        return float(s)
    except ValueError:
        return s


def read_table(path: Path) -> list[dict[str, Any]]:
    """Read a CSV into a list of records with numeric coercion."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return [{k: _coerce(v) for k, v in row.items()} for row in rows]


def read_params(path: Path) -> dict[str, Any]:
    """Read a ``name,value,description`` CSV into ``{name: value}``."""
    out: dict[str, Any] = {}
    for row in read_table(path):
        out[row["name"]] = row["value"]
    return out


def write_table(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write records back to CSV (used to materialise what-if scenarios on disk)."""
    if not rows:
        raise ValueError("refusing to write an empty table")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


class BaseModel:
    """Subclass this for every base model.

    Subclasses must set the class attributes below and implement :meth:`build` and :meth:`kpis`.
    Integer models may also implement :meth:`build_cpsat` / :meth:`kpis_cpsat` for OR-Tools CP-SAT.
    """

    name: str = ""
    title: str = ""
    domain: str = ""
    sense: str = "min"           # "min" or "max"
    problem_type: str = ""       # LP | MILP | IP
    source: Source | None = None
    DATA_DIR: Path | None = None  # set in each subclass: Path(__file__).parent / "data"
    TABLES: tuple[str, ...] = ()  # CSV table names (without .csv) expected in DATA_DIR
    HAS_PARAMS: bool = True       # whether data/params.csv exists
    MEASURE_DIMS: dict[str, tuple[str, ...]] = {}  # decision measure -> its index dimensions (for the DSL)

    # ------------------------------------------------------------------ data
    @classmethod
    def load_data(cls, data_dir: str | Path | None = None) -> dict[str, Any]:
        """Load every table in ``TABLES`` plus ``params`` from ``data_dir`` (default: the shipped data)."""
        base = Path(data_dir) if data_dir is not None else cls.DATA_DIR
        if base is None:
            raise ValueError(f"{cls.__name__} has no DATA_DIR")
        data: dict[str, Any] = {}
        for table in cls.TABLES:
            data[table] = read_table(base / f"{table}.csv")
        if cls.HAS_PARAMS:
            data["params"] = read_params(base / "params.csv")
        return data

    @classmethod
    def schema(cls) -> dict[str, Any]:
        with open(cls.DATA_DIR.parent / "schema.json", encoding="utf-8") as fh:  # type: ignore[union-attr]
            return json.load(fh)

    @classmethod
    def description(cls) -> str:
        return (cls.DATA_DIR.parent / "description.md").read_text(encoding="utf-8")  # type: ignore[union-attr]

    @classmethod
    def reference(cls) -> dict[str, Any]:
        """Reference objective obtained by running the *original* public implementation."""
        with open(cls.DATA_DIR.parent / "reference.json", encoding="utf-8") as fh:  # type: ignore[union-attr]
            return json.load(fh)

    # ----------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        """Return a ``pulp.LpProblem`` for ``data``."""
        raise NotImplementedError

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        """Planner-facing numbers from a solved PuLP problem."""
        raise NotImplementedError

    def build_cpsat(self, data: dict[str, Any]):
        """Return ``(cp_model.CpModel, variables_dict)``; only for integer models."""
        raise NotImplementedError(f"{self.name} has no CP-SAT formulation")

    def kpis_cpsat(self, solver, variables, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError(f"{self.name} has no CP-SAT formulation")

    def measures(self, prob) -> dict[str, Measure]:
        """Decision measures of a built PuLP problem, keyed by name (see ``MEASURE_DIMS``)."""
        handles = getattr(prob, "_wig", {})
        out: dict[str, Measure] = {}
        for name, dims in self.MEASURE_DIMS.items():
            variables = handles[name]
            out[name] = Measure(name, tuple(dims),
                                {(k if isinstance(k, tuple) else (k,)): v for k, v in variables.items()})
        return out

    @classmethod
    def index_sets(cls, data: dict[str, Any]) -> dict[str, list]:
        """Key values per key column across all tables (what an agent may name; never raw numbers)."""
        schema = cls.schema()
        out: dict[str, list] = {}
        for table, spec in schema.get("tables", {}).items():
            for col in spec.get("key", []):
                vals = out.setdefault(col, [])
                for row in data.get(table, []):
                    if row.get(col) is not None and row[col] not in vals:
                        vals.append(row[col])
        return out

    @property
    def supports_cpsat(self) -> bool:
        return type(self).build_cpsat is not BaseModel.build_cpsat

    # ----------------------------------------------------------------- solve
    def solve(self, data: dict[str, Any] | None = None, solver: str = "highs",
              time_limit: float | None = None, keep_variables: bool = False) -> SolveResult:
        """Build and solve in-process with a PuLP-backed open solver (``highs`` | ``scip`` | ``cbc``).

        For ``cpsat`` use :func:`whatifgym.runner.run` or :func:`whatifgym.runner.run_subprocess`.
        """
        from . import solvers  # lazy: pulls in pulp/highspy

        if data is None:
            data = self.load_data()
        prob = self.build(data)
        status, objective, elapsed, message = solvers.solve_pulp(prob, solver, time_limit=time_limit)
        n_vars, n_cons, n_int = solvers.pulp_sizes(prob)
        kpis = self.kpis(prob, data) if status == "optimal" else {}
        variables = {}
        if keep_variables and status == "optimal":
            variables = {v.name: v.value() for v in prob.variables() if v.value() not in (None, 0)}
        return SolveResult(model=self.name, solver=solver, status=status, objective=objective,
                           time_s=elapsed, n_vars=n_vars, n_constraints=n_cons, n_int_vars=n_int,
                           kpis=kpis, variables=variables, message=message)

    def solve_cpsat(self, data: dict[str, Any] | None = None, time_limit: float | None = None,
                    workers: int = 8) -> SolveResult:
        """Build and solve in-process with OR-Tools CP-SAT (do not call from a process that imported pulp)."""
        from ortools.sat.python import cp_model  # lazy

        if data is None:
            data = self.load_data()
        model, variables = self.build_cpsat(data)
        solver = cp_model.CpSolver()
        if time_limit:
            solver.parameters.max_time_in_seconds = float(time_limit)
        solver.parameters.num_workers = workers
        t0 = time.perf_counter()
        status_code = solver.solve(model)
        elapsed = time.perf_counter() - t0
        status = {cp_model.OPTIMAL: "optimal", cp_model.FEASIBLE: "time_limit",
                  cp_model.INFEASIBLE: "infeasible", cp_model.MODEL_INVALID: "error",
                  cp_model.UNKNOWN: "not_solved"}[status_code]
        proto = model.proto if hasattr(model, "proto") else model.Proto()
        objective = solver.objective_value if status in ("optimal", "time_limit") else None
        kpis = self.kpis_cpsat(solver, variables, data) if status == "optimal" else {}
        return SolveResult(model=self.name, solver="cpsat", status=status, objective=objective,
                           time_s=elapsed, n_vars=len(proto.variables), n_constraints=len(proto.constraints),
                           n_int_vars=len(proto.variables), kpis=kpis, message=solver.status_name(status_code))
