"""Two-stage validation of a scenario: JSON Schema (syntax) then semantics against the base model.

Semantic checks catch what a schema cannot: an unknown table or column, a selector that matches no row
(a hallucinated entity), a measure or dimension the model does not expose, a scope value that is not a key,
a row added without every column, a parameter that does not exist, a non-numeric scale target, a constraint
family the model does not have.
Every problem is reported with a JSON-pointer-like path so an agent can repair its own output.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .apply import constraint_families, relax_targets

SCHEMA_PATH = Path(__file__).with_name("schema.json")
SCHEMA: dict[str, Any] = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

_NUMERIC_TYPES = {"number", "int", "integer", "float"}


class ValidationError(ValueError):
    """Raised by :func:`validate_scenario`; ``errors`` is a list of ``{"path", "message"}``."""

    def __init__(self, errors: list[dict[str, str]]):
        self.errors = errors
        super().__init__("; ".join(f"{e['path']}: {e['message']}" for e in errors))


def validate_syntax(scenario: Any) -> list[dict[str, str]]:
    """JSON Schema validation. Returns a list of errors (empty when valid)."""
    try:
        import jsonschema
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("pip install jsonschema") from exc
    validator = jsonschema.Draft202012Validator(SCHEMA)
    errors = []
    for err in sorted(validator.iter_errors(scenario), key=lambda e: list(e.path)):
        path = "/" + "/".join(str(p) for p in err.path)
        errors.append({"path": path or "/", "message": _explain(err)})
    return errors


def _explain(err) -> str:
    """Turn a jsonschema error into one sentence an agent can act on (oneOf branches are untangled)."""
    inst = err.instance
    if err.validator != "oneOf":
        return err.message
    if not err.path:  # root: ask vs. scenario
        if isinstance(inst, dict) and "ask" in inst:
            return "an `ask` must stand alone: remove data_changes, rules, objective, fixed_decisions, relax and logic, or remove `ask`"
        return "a scenario needs at least one of data_changes, rules, objective, fixed_decisions, relax or logic (or a single `ask`)"
    branches = err.schema.get("oneOf", [])
    if isinstance(inst, dict) and "op" in inst:  # data_change branches are keyed by op
        idx = next((i for i, b in enumerate(branches)
                    if b.get("properties", {}).get("op", {}).get("const") == inst["op"]), None)
        if idx is None:
            ops = [b.get("properties", {}).get("op", {}).get("const") for b in branches]
            return f"unknown op {inst['op']!r}; ops are {ops}"
        subs = [c.message for c in err.context if list(c.relative_schema_path)[:1] == [idx]]
        return f"invalid {inst['op']} change: " + ("; ".join(subs) or err.message)
    if isinstance(inst, dict) and "sense" in inst and ("value" in inst or "relative_to" in inst or "measure" in inst):
        return "a rule carries either `value` (absolute) or `relative_to` + `factor` (relative), not both and not neither"
    if isinstance(inst, dict) and "op" not in inst and err.schema.get("$ref", "").endswith("data_change"):
        return "a data change needs an `op` (scale | shift | set | add | remove | set_param | scale_param | shift_param)"
    best = min(err.context, key=lambda c: (len(list(c.path)), len(c.message))) if err.context else None
    return f"{err.message[:120]}" + (f": {best.message}" if best else "")


def _matches(row: dict, where: dict) -> bool:
    for col, val in where.items():
        allowed = set(val) if isinstance(val, list) else {val}
        if row.get(col) not in allowed:
            return False
    return True


def _column_type(schema: dict, table: str, column: str) -> str | None:
    return schema["tables"].get(table, {}).get("columns", {}).get(column, {}).get("type")


def validate_semantics(scenario: dict, model, data: dict) -> list[dict[str, str]]:
    """Check a syntactically valid scenario against the model's schema, data and measures."""
    errors: list[dict[str, str]] = []
    if "ask" in scenario:
        return errors
    if scenario.get("base_model") not in (None, model.name):
        errors.append({"path": "/base_model", "message": f"scenario is for {scenario['base_model']!r}, environment model is {model.name!r}"})

    schema = model.schema()
    tables = schema.get("tables", {})
    params = schema.get("params", {})

    # ---- data changes, applied in order on a shadow copy so later selectors see earlier adds/removes
    shadow = {t: [dict(r) for r in rows] for t, rows in data.items() if t != "params"}
    for i, ch in enumerate(scenario.get("data_changes", [])):
        p = f"/data_changes/{i}"
        op = ch["op"]
        if op in ("set_param", "scale_param", "shift_param"):
            if ch["name"] not in params and ch["name"] not in data.get("params", {}):
                errors.append({"path": p + "/name", "message": f"unknown parameter {ch['name']!r}; parameters are {sorted(params) or sorted(data.get('params', {}))}"})
            elif op != "set_param" and not isinstance(data["params"].get(ch["name"]), (int, float)):
                errors.append({"path": p + "/name", "message": f"parameter {ch['name']!r} is not numeric"})
            elif op == "set_param" and isinstance(data.get("params", {}).get(ch["name"]), (int, float)) \
                    and not isinstance(data["params"][ch["name"]], bool) \
                    and (isinstance(ch.get("value"), bool) or not isinstance(ch.get("value"), (int, float))):
                errors.append({"path": p + "/value", "message": f"parameter {ch['name']!r} is numeric; got {ch.get('value')!r}"})
            continue
        table = ch["table"]
        if table not in tables:
            errors.append({"path": p + "/table", "message": f"unknown table {table!r}; tables are {sorted(tables)}"})
            continue
        cols = tables[table].get("columns", {})
        where = ch.get("where")
        if where:
            for col in where:
                if col not in cols:
                    errors.append({"path": f"{p}/where/{col}", "message": f"table {table!r} has no column {col!r}; columns are {sorted(cols)}"})
            if not any(_matches(r, where) for r in shadow.get(table, [])):
                errors.append({"path": p + "/where", "message": f"no row of {table!r} matches {json.dumps(where)}"})
        if op in ("scale", "shift", "set"):
            col = ch["column"]
            if col not in cols:
                errors.append({"path": p + "/column", "message": f"table {table!r} has no column {col!r}; columns are {sorted(cols)}"})
            else:
                if col in tables[table].get("key", []):
                    errors.append({"path": p + "/column", "message": f"{col!r} is a key column of {table!r}; keys cannot be edited (remove and add rows instead)"})
                if op in ("scale", "shift") and (_column_type(schema, table, col) or "number") not in _NUMERIC_TYPES:
                    errors.append({"path": p + "/column", "message": f"column {col!r} is not numeric"})
                if op == "set" and (_column_type(schema, table, col) in _NUMERIC_TYPES) and not isinstance(ch["value"], (int, float)):
                    errors.append({"path": p + "/value", "message": f"column {col!r} is numeric; got {ch['value']!r}"})
            # shadow update
            for r in shadow.get(table, []):
                if not where or _matches(r, where):
                    if op == "set":
                        r[col] = ch["value"]
                    elif isinstance(r.get(col), (int, float)):
                        r[col] = r[col] * ch["factor"] if op == "scale" else r[col] + ch["delta"]
        elif op == "add":
            keys = tables[table].get("key", [])
            for j, row in enumerate(ch["rows"]):
                missing = [c for c in cols if c not in row]
                extra = [c for c in row if c not in cols]
                if missing:
                    errors.append({"path": f"{p}/rows/{j}", "message": f"row is missing columns {missing}"})
                if extra:
                    errors.append({"path": f"{p}/rows/{j}", "message": f"row has unknown columns {extra}"})
                if keys and any(all(r.get(k) == row.get(k) for k in keys) for r in shadow.get(table, [])):
                    errors.append({"path": f"{p}/rows/{j}", "message": f"a row with key {[row.get(k) for k in keys]} already exists in {table!r}"})
                shadow.setdefault(table, []).append(dict(row))
        elif op == "remove":
            shadow[table] = [r for r in shadow.get(table, []) if not _matches(r, where)]
            if not shadow[table]:
                errors.append({"path": p, "message": f"removing these rows empties table {table!r}"})

    # ---- measures (rules, objective, fixed decisions, logic) and relaxations need a built model for the index values
    needs_measures = scenario.get("rules") or scenario.get("fixed_decisions") or scenario.get("logic") \
        or scenario.get("relax") or any(st["measure"] != "original" for st in scenario.get("objective", []))
    measures, prob = {}, None
    if needs_measures:
        try:
            prob = model.build(data)
            measures = model.measures(prob)
        except Exception as exc:  # pragma: no cover - defensive
            errors.append({"path": "/", "message": f"could not build the base model to inspect measures: {exc}"})
            return errors

    def check_scope(path: str, measure_name: str, scope: dict | None) -> None:
        if measure_name not in measures:
            errors.append({"path": path + "/measure", "message": f"unknown measure {measure_name!r}; measures are {sorted(model.MEASURE_DIMS)}"})
            return
        m = measures[measure_name]
        n_before = len(errors)
        for dim, val in (scope or {}).items():
            if dim not in m.dims:
                errors.append({"path": f"{path}/scope/{dim}", "message": f"measure {measure_name!r} has dimensions {list(m.dims)}, not {dim!r}"})
                continue
            known = set(m.values(dim))
            for v in (val if isinstance(val, list) else [val]):
                if v not in known:
                    errors.append({"path": f"{path}/scope/{dim}", "message": f"{v!r} is not a {dim}; known values: {sorted(map(str, known))[:12]}"})
        if len(errors) == n_before and not m.select(scope or {}):
            errors.append({"path": path + "/scope", "message": "scope selects no variable"})

    for i, rule in enumerate(scenario.get("rules", [])):
        check_scope(f"/rules/{i}", rule["measure"], rule.get("scope"))
        if "relative_to" in rule:
            check_scope(f"/rules/{i}/relative_to", rule["relative_to"]["measure"], rule["relative_to"].get("scope"))
    for i, st in enumerate(scenario.get("objective", [])):
        if st["measure"] != "original":
            check_scope(f"/objective/{i}", st["measure"], st.get("scope"))
        elif st.get("scope"):
            errors.append({"path": f"/objective/{i}/scope", "message": "the original objective takes no scope"})
    for i, fd in enumerate(scenario.get("fixed_decisions", [])):
        check_scope(f"/fixed_decisions/{i}", fd["measure"], fd.get("scope"))
    for i, lr in enumerate(scenario.get("logic", [])):
        if lr["at_least"] > len(lr["of"]):
            errors.append({"path": f"/logic/{i}/at_least", "message": f"at_least is {lr['at_least']} but there are only {len(lr['of'])} conditions"})
        for j, cond in enumerate(lr["of"]):
            check_scope(f"/logic/{i}/of/{j}", cond["measure"], cond.get("scope"))

    families = constraint_families(model) if scenario.get("relax") else {}
    index_sets = model.index_sets(data) if scenario.get("relax") else {}
    for i, rx in enumerate(scenario.get("relax", [])):
        p = f"/relax/{i}"
        if rx["constraint"] not in families:
            errors.append({"path": p + "/constraint", "message": f"unknown constraint family {rx['constraint']!r}; families are {sorted(families)}"})
            continue
        dims = families[rx["constraint"]]
        n_before = len(errors)
        for dim, val in (rx.get("scope") or {}).items():
            if dim not in dims:
                errors.append({"path": f"{p}/scope/{dim}", "message": f"constraint family {rx['constraint']!r} has dimensions {list(dims)}, not {dim!r}"})
                continue
            known = set(index_sets.get(dim, []))
            for v in (val if isinstance(val, list) else [val]):
                if v not in known:
                    errors.append({"path": f"{p}/scope/{dim}", "message": f"{v!r} is not a {dim}; known values: {sorted(map(str, known))[:12]}"})
        if len(errors) == n_before:
            targets = relax_targets(model, prob, data, rx)
            if targets is None:
                errors.append({"path": p + "/constraint", "message": f"constraint family {rx['constraint']!r} cannot be relaxed in this model; change the data or add a rule instead"})
            elif not targets:
                errors.append({"path": p + "/scope", "message": "scope selects no constraint"})
    return errors


def validate_scenario(scenario: Any, model=None, data: dict | None = None, raise_on_error: bool = True) -> list[dict[str, str]]:
    """Syntax, then (when ``model`` is given) semantics. Returns the error list or raises :class:`ValidationError`."""
    errors = validate_syntax(scenario)
    if not errors and model is not None:
        errors = validate_semantics(scenario, model, data if data is not None else model.load_data())
    if errors and raise_on_error:
        raise ValidationError(errors)
    return errors
