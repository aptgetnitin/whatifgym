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


# ------------------------------------------------------------------ relax and logic
def _solve(model, **parts):
    from whatifgym.oracle import solve_scenario

    return solve_scenario(model, {"version": "0.1", **parts}, keep_decisions=False)


def _cond(measure, scope, sense, value):
    return {"measure": measure, "scope": scope, "sense": sense, "value": value}


@pytest.mark.parametrize("model_name,conds,k", [
    ("factory_planning", [_cond("make", {"month": "Jan", "product": "Prod1"}, "<=", 0),
                          _cond("make", {"month": "Jan", "product": "Prod2"}, "<=", 0)], 1),
    ("factory_planning", [_cond("sell", {"product": p}, "<=", 0) for p in ("Prod1", "Prod2", "Prod4")], 2),
    ("mining", [_cond("operate", {"year": "Year1", "mine": "Mine1"}, "<=", 0),
                _cond("operate", {"year": "Year1", "mine": "Mine3"}, "<=", 0)], 1),
    ("food_manufacture", [_cond("buy", {"month": "Jan"}, "<=", 0), _cond("buy", {"month": "Feb"}, "==", 300)], 1),
])
def test_logic_equals_the_best_branch(model_name, conds, k):
    """At least k of the conditions == the best of the scenarios that impose k of them as plain rules."""
    import itertools

    model = get_model(model_name)
    logic = _solve(model, logic=[{"at_least": k, "of": conds}])
    branches = [_solve(model, rules=list(c)) for c in itertools.combinations(conds, k)]
    values = [b.objective for b in branches if b.status == "optimal"]
    best = max(values) if model.sense == "max" else min(values)
    assert logic.status == "optimal" and abs(logic.objective - best) <= 1e-6 * max(1.0, abs(best))


def test_logic_is_infeasible_when_every_branch_is():
    model = get_model("factory_planning")   # Prod3 has an end-stock target, and 2,500 is beyond capacity
    r = _solve(model, logic=[{"at_least": 1, "of": [_cond("make", {"product": "Prod3"}, "<=", 0),
                                                     _cond("make", {"product": "Prod3"}, ">=", 2500)]}])
    assert r.status == "infeasible"


def test_relax_full_and_scoped():
    model = get_model("factory_planning")
    base = _solve(model, data_changes=[])
    full = _solve(model, relax=[{"constraint": "capacity"}])
    march = _solve(model, relax=[{"constraint": "capacity", "scope": {"month": "Mar"}}])
    assert full.n_relaxed_constraints == 30 and march.n_relaxed_constraints == 5
    assert full.objective > march.objective > base.objective


def test_relax_and_logic_semantic_errors():
    model = get_model("factory_planning")
    cases = {
        "unknown constraint family": {"relax": [{"constraint": "nope"}]},
        "has dimensions": {"relax": [{"constraint": "capacity", "scope": {"product": "Prod1"}}]},
        "is not a month": {"relax": [{"constraint": "capacity", "scope": {"month": "Smarch"}}]},
        "only 2 conditions": {"logic": [{"at_least": 3, "of": [_cond("make", {}, "<=", 0), _cond("sell", {}, "<=", 0)]}]},
        "unknown measure": {"logic": [{"at_least": 1, "of": [_cond("ghost", {}, "<=", 0), _cond("sell", {}, "<=", 0)]}]},
    }
    for needle, parts in cases.items():
        errors = validate_scenario({"version": "0.1", **parts}, model, raise_on_error=False)
        assert any(needle in e["message"] for e in errors), (needle, errors)
    unresolvable = validate_scenario({"version": "0.1", "relax": [{"constraint": "refining"}]},
                                     get_model("food_manufacture"), raise_on_error=False)
    assert "cannot be relaxed" in unresolvable[0]["message"]
