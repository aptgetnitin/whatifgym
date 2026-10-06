"""Shared machinery for task families.

A family is a set of *templates*. A template is a function ``(rng, ctx) -> (question, scenario, slots, difficulty)``
or ``None`` when it cannot produce a task for this model. ``TaskFamily.generate`` draws templates, solves the gold
scenario with the oracle to get the reference, and keeps a task only when

* the reference solved (optimal, or infeasible for families that allow it),
* the scored KPIs moved clearly beyond the scoring tolerance (so "no change" is a wrong answer),
* the reference is identical on a second open solver (so the reward is solver-independent),
* the scenario is not a duplicate.

Model-specific templates (richer language) and generic schema-driven templates (work on any model with labels in its
schema.json) are both supported; a family lists which it has.
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from ..dsl.apply import scenario_hash
from ..oracle import ScenarioResult, solve_scenario
from ..registry import get_model
from ..scoring import REL_TOL, compare_results
from ..solvers import available_solvers
from ..tasks import Task, split_for

Template = Callable[[random.Random, "FamilyContext"], tuple[str, dict[str, Any], dict[str, Any], str] | None]


@dataclass
class FamilyContext:
    """Everything a template may look at: the model, its data, schema and the solved base plan."""

    model: Any
    data: dict[str, Any]
    schema: dict[str, Any]
    base: ScenarioResult                      # base plan solved with decisions kept
    measure_values: dict[str, dict[tuple, float]] = field(default_factory=dict)  # measure -> index tuple -> value
    measure_integral: dict[str, bool] = field(default_factory=dict)              # measure -> all variables integer/binary?

    # ---- helpers for templates
    def measure_sum(self, measure: str, scope: dict[str, Any] | None = None) -> float:
        dims = self.model.MEASURE_DIMS[measure]
        scope = scope or {}
        total = 0.0
        for key, val in self.measure_values.get(measure, {}).items():
            ok = True
            for dim, wanted in scope.items():
                allowed = set(wanted) if isinstance(wanted, (list, tuple, set)) else {wanted}
                if key[dims.index(dim)] not in allowed:
                    ok = False
                    break
            if ok:
                total += val
        return total

    def dim_values(self, measure: str, dim: str) -> list:
        dims = self.model.MEASURE_DIMS[measure]
        i = dims.index(dim)
        seen: dict = {}
        for key in self.measure_values.get(measure, {}):
            seen.setdefault(key[i], None)
        return list(seen)

    def label(self, kind: str, *path: str) -> str:
        """Human label from schema.json: ('table', t) | ('column', t, c) | ('param', p) | ('measure', m) | ('table_key', t)."""
        s = self.schema
        try:
            if kind == "table":
                return s["tables"][path[0]].get("label") or path[0].replace("_", " ")
            if kind == "column":
                return s["tables"][path[0]]["columns"][path[1]].get("label") or path[1].replace("_", " ")
            if kind == "param":
                return s["params"][path[0]].get("label") or path[0].replace("_", " ")
            if kind == "measure":
                return s.get("measures", {}).get(path[0], {}).get("label") or path[0].replace("_", " ")
        except KeyError:
            pass
        return path[-1].replace("_", " ")

    def dim_label(self, dim: str) -> str:
        """Label of a measure dimension: the label of the key column of the same name, when a table has one."""
        for t, ts in self.schema["tables"].items():
            if dim in ts.get("key", []):
                return self.label("column", t, dim)
        return dim.replace("_", " ")

    def numeric_columns(self, table: str) -> list[str]:
        """Editable numeric columns: not a key, not marked structural, not a share/fraction (those must sum to one)."""
        spec = self.schema["tables"][table]
        keys = set(spec.get("key", []))
        out = []
        for c, cs in spec["columns"].items():
            if c in keys or cs.get("editable") is False or cs.get("type") not in ("number", "int", "integer", "float"):
                continue
            text = f"{c} {cs.get('label', '')} {cs.get('description', '')}".lower()
            if any(w in text for w in ("share", "fraction", "probability", "proportion")):
                continue
            out.append(c)
        return out

    def round_for(self, measure: str, value: float, base: float | None = None):
        """Round a limit the way the measure is counted: whole units for integer measures, otherwise `nice`."""
        if self.measure_integral.get(measure):
            return max(1, int(round(value)))
        return nice(value, base)

    def numeric_params(self) -> list[str]:
        return [p for p, v in self.data.get("params", {}).items() if isinstance(v, (int, float)) and not isinstance(v, bool)]

    def param_in_bounds(self, name: str, value: float) -> bool:
        """Respect optional ``min``/``max`` hints on a parameter in schema.json (e.g. a size that explodes the model)."""
        spec = self.schema.get("params", {}).get(name, {})
        lo, hi = spec.get("min"), spec.get("max")
        return (lo is None or value >= lo) and (hi is None or value <= hi)

    def referenced_tables(self) -> set[str]:
        """Tables that some other table's column points at via ``ref: table.column`` (their rows must not be removed)."""
        out: set[str] = set()
        for t, ts in self.schema["tables"].items():
            for c, cs in ts["columns"].items():
                ref = cs.get("ref")
                if ref and "." in ref and ref.split(".", 1)[0] != t:
                    out.add(ref.split(".", 1)[0])
        return out

    def removable_tables(self, min_rows: int = 3) -> list[str]:
        """*Entity* tables whose rows can be added or removed as a what-if (an item, a guest, a mine, a generator
        type). A table qualifies when it has a single key that no other table uses or refers to (so dropping a row
        leaves no dangling references and no silent default), no ``ref`` column (a fact table keyed by another
        table's entities), no ``order`` column (an ordered horizon), no share/fraction column (those sum to one),
        and at least ``min_rows`` rows. ``"removable": false`` on the table opts out explicitly."""
        refd = self.referenced_tables()
        tables = self.schema["tables"]
        out = []
        for t, ts in tables.items():
            keys = ts.get("key", [])
            if t in refd or len(self.data.get(t, [])) < min_rows or len(keys) != 1 or ts.get("removable") is False:
                continue
            cols = ts["columns"]
            keys_elsewhere = {k for t2, ts2 in tables.items() if t2 != t for k in ts2.get("key", [])}
            if "order" in cols or keys[0] in keys_elsewhere or any(cs.get("ref") for cs in cols.values()):
                continue
            text = " ".join(f"{c} {cs.get('label', '')}" for c, cs in cols.items()).lower()
            if any(w in text for w in ("share", "fraction", "probability", "proportion")):
                continue
            out.append(t)
        return out


def nice(value: float, base: float | None = None) -> float:
    """Round a generated number to something a planner would say (keeps zero as zero)."""
    if value == 0:
        return 0
    mag = abs(base if base else value)
    if mag >= 1000:
        step = 50.0
    elif mag >= 100:
        step = 10.0
    elif mag >= 10:
        step = 1.0
    elif mag >= 1:
        step = 0.1
    else:
        step = 0.01
    out = round(value / step) * step
    return int(out) if float(out).is_integer() else round(out, 4)


def describe_key(ctx: FamilyContext, table: str, row: dict[str, Any]) -> str:
    keys = ctx.schema["tables"][table].get("key", [])
    return ", ".join(f"{ctx.label('column', table, k)} {row[k]}" for k in keys)


class TaskFamily:
    name: str = ""
    description: str = ""
    allow_infeasible: bool = False
    specific_templates: dict[str, dict[str, Template]] = {}   # model name -> {template name: fn}
    generic_templates: dict[str, Template] = {}
    combo_share: float = 0.15        # how often a two-part question is attempted
    check_all_solvers: bool = False  # cross-check references on every other open solver, not only the first
    distinct_outcomes: bool = False  # drop a candidate whose scored result equals an accepted task's (else one
                                     # answer fits several questions, which a copy-the-nearest agent exploits)
    max_combo_share: float = 0.3     # ... and the ceiling on two-part questions in a generated file

    def __init__(self, model_name: str, solver: str = "highs"):
        self.model = get_model(model_name)
        self.solver = solver
        self.skipped: dict[str, int] = {}   # why candidates were dropped in the last generate() call
        self.data = self.model.load_data()
        base = solve_scenario(self.model, {"version": "0.1", "data_changes": []}, self.data, solver=solver, keep_decisions=True)
        if base.status != "optimal":
            raise RuntimeError(f"base model {model_name} does not solve: {base.status}")
        prob = self.model.build(self.data)
        from .. import solvers  # lazy
        solvers.solve_pulp(prob, solver)
        measures = self.model.measures(prob)
        values = {name: {k: (v.value() or 0.0) for k, v in m.vars.items()} for name, m in measures.items()}
        integral = {name: all(getattr(v, "cat", "Continuous") in ("Integer", "Binary") for v in m.vars.values())
                    for name, m in measures.items()}
        self.ctx = FamilyContext(model=self.model, data=self.data, schema=self.model.schema(), base=base,
                                 measure_values=values, measure_integral=integral)

    @property
    def base_result(self) -> ScenarioResult:
        """The base plan's oracle result (what "no change" would score against)."""
        return self.ctx.base

    # ---- templates available for this model
    def templates(self) -> dict[str, Template]:
        out = dict(self.generic_templates)
        out.update(self.specific_templates.get(self.model.name, {}))
        return out

    def combo(self, rng: random.Random):
        """Two single templates in one question; override for family-specific phrasing."""
        return None

    def accept(self, scenario: dict[str, Any], ref: ScenarioResult) -> bool:
        """Family-specific acceptance beyond the common filters (override to drop degenerate candidates)."""
        return True

    # ---- generation
    solve_time_limit: float = 60.0   # seconds per oracle solve during generation; a candidate that needs more is dropped

    def _solve(self, scenario: dict[str, Any], solver: str) -> ScenarioResult | None:
        """Oracle call that never raises: a model may reject edited data in ``build`` (``ValueError`` on a
        structural inconsistency); such a candidate is simply skipped and counted in ``self.skipped``. Every solve
        carries a time limit, because a rule can turn an easy MILP into a hard one."""
        try:
            return solve_scenario(self.model, scenario, self.data, solver=solver, keep_decisions=False,
                                  time_limit=self.solve_time_limit)
        except Exception as exc:  # noqa: BLE001 - any model/solver failure just drops the candidate
            self.skipped[f"error: {type(exc).__name__}"] = self.skipped.get(f"error: {type(exc).__name__}", 0) + 1
            return None

    def generate(self, n: int, seed: int = 0, check_solvers: list[str] | None = None,
                 max_seconds: float | None = None) -> list[Task]:
        """Generate up to ``n`` tasks. Stops early after ``60 * n`` attempts or ``max_seconds`` of wall time
        (slow models such as column-enumerated set partitioning may legitimately yield fewer tasks)."""
        rng = random.Random(seed)
        t_start = time.time()
        templates = self.templates()
        self.skipped: dict[str, int] = {}
        if not templates:
            return []
        names = list(templates)
        tasks: list[Task] = []
        seen: set[str] = set()
        tried: set[str] = set()   # every candidate already solved: a repeat is skipped without solving again
        kpi_keys = self.model.SCORING_KPIS
        checkers = check_solvers if check_solvers is not None else \
            [s for s in available_solvers() if s in ("scip", "cbc") and s != self.solver][:None if self.check_all_solvers else 1]
        attempts = 0
        while len(tasks) < n and attempts < 60 * n:
            if max_seconds is not None and time.time() - t_start > max_seconds:
                self.skipped["time budget"] = attempts
                break
            attempts += 1
            tname, produced = None, None
            n_combo = sum(1 for t in tasks if t.template == "combo")
            if rng.random() < self.combo_share and n_combo < max(1, int(self.max_combo_share * n)):
                produced = self.combo(rng)
                tname = "combo"
            if produced is None:
                tname = names[len(tasks) % len(names)] if rng.random() < 0.6 else rng.choice(names)
                produced = templates[tname](rng, self.ctx)
            if produced is None:
                self.skipped["no candidate"] = self.skipped.get("no candidate", 0) + 1
                continue
            question, scenario, slots, difficulty = produced
            scenario.setdefault("version", "0.1")
            scenario.setdefault("base_model", self.model.name)
            h = scenario_hash(scenario)
            if h in tried:  # same candidate as before: it was accepted (a duplicate) or rejected for a stable reason
                self.skipped["duplicate"] = self.skipped.get("duplicate", 0) + 1
                continue
            tried.add(h)
            ref = self._solve(scenario, self.solver)
            if ref is None:
                continue
            if ref.status == "invalid":
                raise RuntimeError(f"template {tname} produced an invalid scenario: {ref.message}")
            if ref.status != "optimal" and not (self.allow_infeasible and ref.status == "infeasible"):
                self.skipped[ref.status] = self.skipped.get(ref.status, 0) + 1
                continue
            if ref.scenario_hash in seen:
                self.skipped["duplicate"] = self.skipped.get("duplicate", 0) + 1
                continue
            if ref.status == "optimal" and compare_results(self.ctx.base.to_dict(), ref.to_dict(), kpi_keys, rel_tol=3 * REL_TOL).match:
                self.skipped["no effect"] = self.skipped.get("no effect", 0) + 1
                continue  # "no change" would be accepted: not a task
            stable = True
            for s in checkers:
                other = self._solve(scenario, s)
                if other is None or not compare_results(ref.to_dict(), other.to_dict(), kpi_keys).match:
                    stable = False
                    break
            if not stable:
                self.skipped["solver disagreement"] = self.skipped.get("solver disagreement", 0) + 1
                continue
            if self.distinct_outcomes and any(compare_results(t.reference, ref.to_dict(), kpi_keys).match for t in tasks):
                self.skipped["same outcome as another task"] = self.skipped.get("same outcome as another task", 0) + 1
                continue
            if not self.accept(scenario, ref):
                self.skipped["family filter"] = self.skipped.get("family filter", 0) + 1
                continue
            seen.add(ref.scenario_hash)
            clarification = slots.pop("_clarification", None) if isinstance(slots, dict) else None
            history = slots.pop("_history", None) if isinstance(slots, dict) else None
            tid = f"{self.model.name}-{self.name}-{seed:03d}-{len(tasks):04d}"
            tasks.append(Task(id=tid, family=self.name, model=self.model.name, question=question, scenario=scenario,
                              reference=ref.to_dict(), kpi_keys=list(kpi_keys), difficulty=difficulty, template=tname,
                              slots=slots, split=split_for(tid), clarification=clarification, history=history,
                              tags=[tname, difficulty, ref.status] + (["ask"] if clarification else [])))
        return tasks
