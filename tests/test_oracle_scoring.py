"""Oracle + scorer: equivalent spellings score identically; tolerance, status and KPI logic behave."""
import math

from whatifgym import get_model
from whatifgym.oracle import solve_scenario
from whatifgym.scoring import compare_results, score_episode

M = get_model("factory_planning")
KPIS = ["profit", "holding_cost", "sales_contribution"]


def test_same_scenario_two_spellings_scores_identical():
    scale = {"version": "0.1", "data_changes": [
        {"op": "scale", "table": "max_sales", "column": "max_sales", "where": {"product": "Prod5", "month": ["May", "Jun"]}, "factor": 0.8}]}
    explicit = {"version": "0.1", "data_changes": [
        {"op": "set", "table": "max_sales", "column": "max_sales", "where": {"product": "Prod5", "month": "May"}, "value": 800},
        {"op": "set", "table": "max_sales", "column": "max_sales", "where": {"product": "Prod5", "month": "Jun"}, "value": 880}]}
    a, b = solve_scenario(M, scale), solve_scenario(M, explicit)
    assert a.status == b.status == "optimal" and a.scenario_hash != b.scenario_hash
    assert compare_results(a.to_dict(), b.to_dict(), KPIS).match
    sa = score_episode(a.to_dict(), b.to_dict(), valid_dsl=True, asked=False, ask_needed=False, kpi_keys=KPIS)
    sb = score_episode(b.to_dict(), a.to_dict(), valid_dsl=True, asked=False, ask_needed=False, kpi_keys=KPIS)
    assert sa.reward == sb.reward == 1.1 and sa.correct and sb.correct


def test_rule_equivalent_to_data_edit():
    """'Sell at most 300 Prod4 in April' as a market-limit edit or as a rule on sell: same result."""
    edit = {"version": "0.1", "data_changes": [{"op": "set", "table": "max_sales", "column": "max_sales", "where": {"product": "Prod4", "month": "Apr"}, "value": 300}]}
    rule = {"version": "0.1", "rules": [{"measure": "sell", "scope": {"product": "Prod4", "month": "Apr"}, "sense": "<=", "value": 300}]}
    a, b = solve_scenario(M, edit), solve_scenario(M, rule)
    assert compare_results(a.to_dict(), b.to_dict(), KPIS).match


def test_tolerance_and_status_logic():
    base = solve_scenario(M, {"version": "0.1", "data_changes": []}).to_dict()
    near = dict(base, objective=base["objective"] * (1 + 5e-4), kpis=dict(base["kpis"], profit=base["kpis"]["profit"] * (1 + 5e-4)))
    far = dict(base, objective=base["objective"] * 1.01)
    assert compare_results(base, near, KPIS).match
    assert not compare_results(base, far, KPIS).objective_match
    infeasible = solve_scenario(M, {"version": "0.1", "rules": [{"measure": "sell", "scope": {"product": "Prod1"}, "sense": ">=", "value": 1e6}]}).to_dict()
    assert infeasible["status"] == "infeasible"
    assert compare_results(infeasible, infeasible, KPIS).match and not compare_results(infeasible, base, KPIS).status_match


def test_reward_rules():
    ref = solve_scenario(M, {"version": "0.1", "data_changes": []}).to_dict()
    assert score_episode(ref, ref, valid_dsl=True, asked=False, ask_needed=False).reward == 1.1
    assert score_episode(ref, ref, valid_dsl=True, asked=True, ask_needed=False).reward == 0.9
    assert score_episode(ref, None, valid_dsl=False, asked=False, ask_needed=False).reward == 0.0
    assert score_episode(ref, None, valid_dsl=True, asked=False, ask_needed=False).reward == 0.1
    s = score_episode(ref, ref, valid_dsl=True, asked=False, ask_needed=True)
    assert s.reward == 0.0 and not s.route_correct
    assert score_episode(ref, ref, valid_dsl=True, asked=True, ask_needed=True).reward == 1.1


def test_lexicographic_stages_hold_earlier_optimum():
    r = solve_scenario(M, {"version": "0.1", "objective": [{"sense": "max", "measure": "original"}, {"sense": "min", "measure": "store"}]})
    base = solve_scenario(M, {"version": "0.1", "data_changes": []})
    assert r.status == "optimal" and len(r.stage_values) == 2
    assert math.isclose(r.stage_values[0], base.objective, rel_tol=1e-9)
    assert math.isclose(r.kpis["profit"], base.objective, rel_tol=1e-5)


def test_invalid_and_ask_statuses():
    assert solve_scenario(M, {"version": "0.1", "rules": [{"measure": "nope", "sense": "<=", "value": 1}]}).status == "invalid"
    assert solve_scenario(M, {"version": "0.1", "ask": "Which product?"}).status == "ask"
