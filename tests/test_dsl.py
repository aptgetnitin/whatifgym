"""DSL v0: every example validates (syntax and semantics); every planted bad scenario is rejected."""
import json
from pathlib import Path

import pytest

from whatifgym import get_model
from whatifgym.dsl import validate_scenario, validate_syntax
from whatifgym.dsl.apply import apply_data_changes

EXAMPLES = sorted((Path(__file__).resolve().parents[1] / "whatifgym" / "dsl" / "examples").glob("*.json"))
BAD = sorted((Path(__file__).resolve().parent / "dsl_bad").glob("*.json"))


def _load(path):
    ex = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in ex.items() if not k.startswith("_")}


@pytest.mark.parametrize("path", EXAMPLES, ids=[p.stem for p in EXAMPLES])
def test_examples_are_valid(path):
    scenario = _load(path)
    model = get_model(scenario["base_model"])
    assert validate_scenario(scenario, model, raise_on_error=False) == []


def test_at_least_twenty_bad_examples_all_rejected():
    assert len(BAD) >= 20
    for path in BAD:
        errors = validate_syntax(json.loads(path.read_text(encoding="utf-8")))
        assert errors, f"{path.name} should be rejected"
        assert all(e["path"].startswith("/") and e["message"] for e in errors)


def test_semantic_errors_name_the_problem():
    model = get_model("factory_planning")
    bad = {"version": "0.1", "data_changes": [
        {"op": "scale", "table": "max_sales", "column": "max_sales", "where": {"product": "Prod9"}, "factor": 0.8},
        {"op": "set", "table": "nope", "column": "x", "value": 1},
        {"op": "set", "table": "products", "column": "product", "where": {"product": "Prod1"}, "value": "P1"},
        {"op": "set_param", "name": "overtime_cap", "value": 1}],
        "rules": [{"measure": "produce", "sense": "<=", "value": 3},
                  {"measure": "make", "scope": {"line": "A"}, "sense": "<=", "value": 3},
                  {"measure": "make", "scope": {"month": "Sep"}, "sense": "<=", "value": 3}]}
    errors = validate_scenario(bad, model, raise_on_error=False)
    paths = {e["path"] for e in errors}
    assert {"/data_changes/0/where", "/data_changes/1/table", "/data_changes/2/column", "/data_changes/3/name",
            "/rules/0/measure", "/rules/1/scope/line", "/rules/2/scope/month"} <= paths


def test_add_then_select_sees_new_row_and_duplicate_key_is_rejected():
    model = get_model("factory_planning")
    ok = {"version": "0.1", "data_changes": [
        {"op": "add", "table": "downtime", "rows": [{"month": "Feb", "machine": "borer", "machines_down": 1}]},
        {"op": "set", "table": "downtime", "column": "machines_down", "where": {"month": "Feb", "machine": "borer"}, "value": 1}]}
    assert validate_scenario(ok, model, raise_on_error=False) == []
    dup = {"version": "0.1", "data_changes": [
        {"op": "add", "table": "downtime", "rows": [{"month": "Jan", "machine": "grinder", "machines_down": 2}]}]}
    assert any("already exists" in e["message"] for e in validate_scenario(dup, model, raise_on_error=False))


def test_apply_data_changes_is_pure_and_ordered():
    model = get_model("factory_planning")
    data = model.load_data()
    before = json.dumps(data, sort_keys=True)
    new = apply_data_changes(data, [
        {"op": "scale", "table": "max_sales", "column": "max_sales", "where": {"product": "Prod1"}, "factor": 2},
        {"op": "shift", "table": "max_sales", "column": "max_sales", "where": {"product": "Prod1", "month": "Jan"}, "delta": 7},
        {"op": "scale_param", "name": "holding_cost", "factor": 4}])
    assert json.dumps(data, sort_keys=True) == before
    jan = next(r for r in new["max_sales"] if r["product"] == "Prod1" and r["month"] == "Jan")
    assert jan["max_sales"] == 500 * 2 + 7 and new["params"]["holding_cost"] == 2.0
