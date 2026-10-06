"""Apply a validated scenario to a base model and solve it.

``apply_data_changes`` edits a deep copy of the model data; ``apply_scenario`` builds the model on the edited
data, removes relaxed constraints, adds rules, fixed decisions and logical rules as constraints, runs the
objective stages lexicographically and returns a plain dict (status, objective, stage values, decisions, KPIs,
sizes, timing). Solver libraries are imported lazily, as everywhere in whatifgym.
"""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import re
import time
from typing import Any

REL_TOL_STAGE = 1e-6  # how tightly earlier lexicographic stages are held
_ILLEGAL = re.compile(r"[-+\[\] >/]")  # characters PuLP replaces with "_" in constraint names (pulp.LpElement)


def constraint_families(model) -> dict[str, tuple[str, ...]]:
    """Constraint families of a base model and their index dimensions, from the ``constraints`` keys of its
    schema.json (``"capacity[month, machine]"`` -> ``{"capacity": ("month", "machine")}``)."""
    out: dict[str, tuple[str, ...]] = {}
    for key in model.schema().get("constraints", {}):
        family, _, rest = key.partition("[")
        out[family.strip()] = tuple(d.strip() for d in rest.rstrip("]").split(",") if d.strip())
    return out


def relax_targets(model, prob, data: dict[str, Any], relaxation: dict[str, Any]) -> list[str] | None:
    """Names of the constraints a relaxation removes, or ``None`` when the family cannot be resolved in this
    model (a dimension that is not a key column of the data). Constraint ``family[i, j]`` is named
    ``family_i_j`` by the base models (PuLP replaces ``-+[] ->/`` with ``_``)."""
    dims = constraint_families(model).get(relaxation["constraint"])
    if dims is None:
        return None
    index_sets = model.index_sets(data)
    if any(d not in index_sets for d in dims):
        return None
    scope = relaxation.get("scope") or {}
    values = []
    for d in dims:
        if d in scope:
            values.append(scope[d] if isinstance(scope[d], list) else [scope[d]])
        else:
            values.append(index_sets[d])
    names = (_ILLEGAL.sub("_", "_".join([relaxation["constraint"]] + [str(v) for v in combo]))
             for combo in itertools.product(*values))
    return [n for n in names if n in prob.constraints]


def scenario_hash(scenario: dict) -> str:
    """Stable identifier of a scenario (canonical JSON, sha256, 16 hex chars)."""
    canon = json.dumps(scenario, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


def _matches(row: dict, where: dict | None) -> bool:
    if not where:
        return True
    for col, val in where.items():
        allowed = set(val) if isinstance(val, list) else {val}
        if row.get(col) not in allowed:
            return False
    return True


def apply_data_changes(data: dict[str, Any], changes: list[dict[str, Any]]) -> dict[str, Any]:
    """Return a new data dict with every change applied in order (the input is not modified)."""
    out = copy.deepcopy(data)
    for ch in changes:
        op = ch["op"]
        if op == "set_param":
            out["params"][ch["name"]] = ch["value"]
        elif op == "scale_param":
            out["params"][ch["name"]] = out["params"][ch["name"]] * ch["factor"]
        elif op == "shift_param":
            out["params"][ch["name"]] = out["params"][ch["name"]] + ch["delta"]
        elif op in ("scale", "shift", "set"):
            col, where = ch["column"], ch.get("where")
            for row in out[ch["table"]]:
                if _matches(row, where):
                    if op == "set":
                        row[col] = ch["value"]
                    elif op == "scale":
                        row[col] = row[col] * ch["factor"]
                    else:
                        row[col] = row[col] + ch["delta"]
        elif op == "add":
            out[ch["table"]].extend(copy.deepcopy(r) for r in ch["rows"])
        elif op == "remove":
            out[ch["table"]] = [r for r in out[ch["table"]] if not _matches(r, ch["where"])]
        else:  # pragma: no cover - schema forbids
            raise ValueError(f"unknown op {op!r}")
    return out


def _sum(vars_: list):
    import pulp

    return pulp.lpSum(vars_) if vars_ else 0


def _add_rules(prob, measures: dict, rules: list[dict[str, Any]]) -> None:
    for i, rule in enumerate(rules):
        lhs = _sum(measures[rule["measure"]].select(rule.get("scope")))
        if "relative_to" in rule:
            rel = rule["relative_to"]
            rhs = rule["factor"] * _sum(measures[rel["measure"]].select(rel.get("scope")))
        else:
            rhs = rule["value"]
        name = rule.get("name") or f"rule_{i}"
        name = "".join(c if c.isalnum() or c in "_-" else "_" for c in name)[:60]
        if rule["sense"] == "<=":
            prob += (lhs <= rhs, name)
        elif rule["sense"] == ">=":
            prob += (lhs >= rhs, name)
        else:
            prob += (lhs == rhs, name)


def _fix_decisions(measures: dict, fixed: list[dict[str, Any]]) -> int:
    n = 0
    for fd in fixed:
        for var in measures[fd["measure"]].select(fd.get("scope")):
            var.lowBound = fd["value"]
            var.upBound = fd["value"]
            n += 1
    return n


def _relax(model, prob, data: dict[str, Any], relaxations: list[dict[str, Any]]) -> int:
    n = 0
    for rx in relaxations:
        names = relax_targets(model, prob, data, rx)
        if not names:
            raise ValueError(f"relaxation {rx} selects no constraint of {model.name}")
        for name in names:
            del prob.constraints[name]
            n += 1
    return n


def _lp_range(prob, expr, need_max: bool, need_min: bool, solver: str, time_limit: float | None):
    """Max and min of ``expr`` over the LP relaxation of ``prob`` as it stands. Every point of the MILP lies in
    the relaxation, so these bound ``expr`` validly for big-M. Returns ``None`` when the relaxation is infeasible
    (the scenario is infeasible anyway); raises when a needed side is unbounded.

    The bounds are a property of the LP, not of the solver, so they come from HiGHS whenever it is installed (PuLP's
    CBC interface fails on some re-targeted objectives with a KeyError while reading the solution back)."""
    import pulp

    from .. import solvers

    if "highs" in solvers.available_solvers():
        solver = "highs"

    saved_obj, saved_sense = prob.objective, prob.sense
    cats = {v.name: v.cat for v in prob.variables()}
    for v in prob.variables():
        v.cat = pulp.LpContinuous
    try:
        out = []
        for want, sense in ((need_max, pulp.LpMaximize), (need_min, pulp.LpMinimize)):
            if not want:
                out.append(None)
                continue
            prob.setObjective(expr)
            prob.sense = sense
            status, value, _, _ = solvers.solve_pulp(prob, solver, time_limit=time_limit)
            if status == "infeasible":
                return None
            if status != "optimal":
                raise ValueError(f"a logical condition has no finite {'upper' if sense == pulp.LpMaximize else 'lower'} "
                                 f"bound ({status}); bound the measure with a rule first")
            out.append(value)
        return out[0], out[1]
    finally:
        for v in prob.variables():
            if v.name in cats:
                v.cat = cats[v.name]
        prob.setObjective(saved_obj)
        prob.sense = saved_sense


def _add_logic(prob, measures: dict, logic: list[dict[str, Any]], solver: str, time_limit: float | None) -> int:
    """At least k of the conditions hold: one binary per condition, ``b = 1`` forces its condition, ``sum b >= k``.
    Big-M is the exact LP range of the condition's sum, so no feasible plan is cut off."""
    import pulp

    n = 0
    for i, lr in enumerate(logic):
        indicators = []
        for j, cond in enumerate(lr["of"]):
            expr = _sum(measures[cond["measure"]].select(cond.get("scope")))
            sense, v = cond["sense"], cond["value"]
            bounds = _lp_range(prob, expr, sense in ("<=", "=="), sense in (">=", "=="), solver, time_limit)
            if bounds is None:
                return n  # the scenario is infeasible before the logic; the solve will say so
            hi, lo = bounds
            b = pulp.LpVariable(f"logic_{i}_{j}", cat=pulp.LpBinary)
            indicators.append(b)
            if hi is not None:
                m_up = max(0.0, hi - v) * (1 + 1e-6) + 1e-6
                prob += (expr - v <= m_up * (1 - b), f"logic_{i}_{j}_le")
            if lo is not None:
                m_lo = max(0.0, v - lo) * (1 + 1e-6) + 1e-6
                prob += (v - expr <= m_lo * (1 - b), f"logic_{i}_{j}_ge")
        prob += (pulp.lpSum(indicators) >= lr["at_least"], f"logic_{i}_at_least")
        n += 1
    return n


def _stage_expression(measures: dict, stage: dict[str, Any], original):
    """``original`` = (expression, sense) of the model's own objective, captured before any stage replaced it."""
    if stage["measure"] == "original":
        return original
    return _sum(measures[stage["measure"]].select(stage.get("scope"))), stage["sense"]


def apply_scenario(model, scenario: dict[str, Any], data: dict[str, Any] | None = None,
                   solver: str = "highs", time_limit: float | None = None,
                   keep_decisions: bool = True) -> dict[str, Any]:
    """Apply ``scenario`` to ``model`` and solve. The scenario must already be validated."""
    import pulp

    from .. import solvers

    if "ask" in scenario:
        raise ValueError("an `ask` action cannot be solved; answer the question first")
    base = data if data is not None else model.load_data()
    t0 = time.perf_counter()
    new_data = apply_data_changes(base, scenario.get("data_changes", []))
    prob = model.build(new_data)
    measures = model.measures(prob)
    n_relaxed = _relax(model, prob, new_data, scenario.get("relax", []))
    _add_rules(prob, measures, scenario.get("rules", []))
    n_fixed = _fix_decisions(measures, scenario.get("fixed_decisions", []))
    n_logic = _add_logic(prob, measures, scenario.get("logic", []), solver, time_limit)

    stages = scenario.get("objective") or [{"sense": "original", "measure": "original"}]
    original = (prob.objective, "max" if prob.sense == pulp.LpMaximize else "min")   # before any stage replaces it
    stage_values: list[float] = []
    status, elapsed_solve, message = "not_solved", 0.0, ""
    for k, stage in enumerate(stages):
        expr, sense = _stage_expression(measures, stage, original)
        prob.setObjective(expr)
        prob.sense = pulp.LpMaximize if sense == "max" else pulp.LpMinimize
        status, value, dt, message = solvers.solve_pulp(prob, solver, time_limit=time_limit)
        elapsed_solve += dt
        if status != "optimal":
            break
        stage_values.append(value)
        if k < len(stages) - 1:  # hold this stage at its optimum for the next one
            tol = REL_TOL_STAGE * max(1.0, abs(value))
            if sense == "max":
                prob += (expr >= value - tol, f"lex_stage_{k}")
            else:
                prob += (expr <= value + tol, f"lex_stage_{k}")

    n_vars, n_cons, n_int = solvers.pulp_sizes(prob)
    result: dict[str, Any] = {
        "model": model.name, "solver": solver, "status": status,
        "objective": stage_values[-1] if status == "optimal" else None,
        "stage_values": stage_values,
        "kpis": model.kpis(prob, new_data) if status == "optimal" else {},
        "decisions": {}, "n_vars": n_vars, "n_constraints": n_cons, "n_int_vars": n_int,
        "n_fixed_vars": n_fixed, "n_rules": len(scenario.get("rules", [])),
        "n_relaxed_constraints": n_relaxed, "n_logical_rules": n_logic,
        "n_data_changes": len(scenario.get("data_changes", [])),
        "solve_time_s": elapsed_solve, "wall_time_s": time.perf_counter() - t0,
        "scenario_hash": scenario_hash(scenario), "message": message,
    }
    if status == "optimal" and keep_decisions:
        result["decisions"] = {v.name: round(v.value(), 9) for v in prob.variables()
                               if v.value() is not None and abs(v.value()) > 1e-9}
    return result
