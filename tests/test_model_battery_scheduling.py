"""battery_scheduling reproduces the original Gurobi notebook's optimum and size on the open solvers."""
import math

import pytest

from whatifgym.models.battery_scheduling.model import BatteryScheduling
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]

# the base plan: buy 7.8125 kWh in the two cheapest hours, sell 7.2 kWh in the evening
BASE_TOTALS = {"profit": 1.56625, "export_revenue": 2.66, "import_cost": 1.09375,
               "energy_charged_kwh": 7.8125, "energy_discharged_kwh": 7.2}


def _what_if(changes=None, rules=None, solver=None):
    from whatifgym.oracle import solve_scenario

    m = BatteryScheduling()
    scenario = {"version": "0.1", "base_model": m.name, "data_changes": changes or []}
    if rules:
        scenario["rules"] = rules
    return solve_scenario(m, scenario, solver=solver or SOLVERS[0], time_limit=60, keep_decisions=False)


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = BatteryScheduling()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis
    assert math.isclose(r.kpis["profit"], r.objective, abs_tol=1e-6)
    for key, expected in BASE_TOTALS.items():  # the scored totals are the same on every solver
        assert math.isclose(r.kpis[key], expected, rel_tol=1e-6, abs_tol=1e-6), key
    assert r.kpis["peak_soc_kwh"] == pytest.approx(13.5)  # the battery is filled to capacity


def test_sizes_and_measures():
    m = BatteryScheduling(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"]) == (72, 25)
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"] == 0
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    hours = [r["hour"] for r in data["hours"]]
    assert len(hours) == 24 and all(v.dims == ("hour",) and len(v.vars) == 24 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    assert m.index_sets(data)["hour"] == hours and m.table_keys(data)["hours"] == [{"hour": h} for h in hours]


def test_schema_describes_the_data():
    m = BatteryScheduling(); data = m.load_data(); schema = m.schema()
    hours = schema["tables"]["hours"]
    assert set(hours["columns"]) == set(data["hours"][0]) and hours["key"] == ["hour"]
    assert set(schema["params"]) == set(data["params"])
    labelled = [hours, *hours["columns"].values(), *schema["params"].values(), *schema["measures"].values()]
    assert all(spec.get("label") for spec in labelled)
    # structural numbers are not what-ifs
    assert hours["columns"]["order"]["editable"] is False and hours["columns"]["step_hours"]["editable"] is False
    assert all(c.get("editable") is not False for c in (hours["columns"]["import_price"], hours["columns"]["export_price"]))
    # efficiencies stay in (0, 1]
    for name in ("charge_efficiency", "discharge_efficiency"):
        assert 0 < schema["params"][name]["min"] < schema["params"][name]["max"] <= 1
        assert schema["params"][name]["min"] <= data["params"][name] <= schema["params"][name]["max"]
    assert set(schema["measures"]) == set(m.MEASURE_DIMS)
    assert all(tuple(spec["dims"]) == m.MEASURE_DIMS[name] for name, spec in schema["measures"].items())


@pytest.mark.parametrize("solver", SOLVERS)
def test_scoring_kpis_are_reported(solver):
    m = BatteryScheduling()
    r = m.solve(solver=solver, time_limit=60)
    assert m.SCORING_KPIS and set(m.SCORING_KPIS) <= set(r.kpis)
    assert all(isinstance(r.kpis[k], float) for k in m.SCORING_KPIS)
    assert set(r.kpis) <= set(m.schema()["kpis"])


def test_energy_accounting():
    """Energy bought = energy sold + change in stored energy + conversion losses."""
    from whatifgym import solvers

    m = BatteryScheduling(); data = m.load_data()
    data["params"]["charge_efficiency"], data["params"]["discharge_efficiency"] = 0.9, 0.85
    prob = m.build(data)
    status, *_ = solvers.solve_pulp(prob, SOLVERS[0])
    assert status == "optimal"
    k = m.kpis(prob, data)
    last = data["hours"][-1]["hour"]
    stored_change = prob._wig["soc"][last].value() - data["params"]["initial_soc_kwh"]
    assert k["energy_charged_kwh"] - k["energy_discharged_kwh"] - stored_change == pytest.approx(k["conversion_losses_kwh"], abs=1e-5)
    assert k["full_cycles"] == pytest.approx(k["energy_discharged_kwh"] / 0.85 / data["params"]["energy_capacity_kwh"], abs=1e-5)


@pytest.mark.skipif("highs" not in SOLVERS, reason="needs HiGHS")
def test_scored_kpis_are_unique_but_the_hourly_plan_is_not():
    """Over the optimal face the scored KPIs have a single value; the hourly split of the plan does not."""
    import pulp

    m = BatteryScheduling(); data = m.load_data()
    prob = m.build(data)
    pulp.LpProblem.solve(prob, pulp.HiGHS(msg=False))
    opt = pulp.value(prob.objective)
    assert math.isclose(opt, m.reference()["objective"], rel_tol=1e-6)
    hours = [r["hour"] for r in data["hours"]]
    buy = {r["hour"]: r["import_price"] for r in data["hours"]}
    sell = {r["hour"]: r["export_price"] for r in data["hours"]}
    c, d = prob._wig["charge"], prob._wig["discharge"]
    exprs = {  # one hour per step, so kW = kWh
        "profit": prob.objective.copy(),
        "export_revenue": pulp.lpSum(sell[h] * d[h] for h in hours),
        "import_cost": pulp.lpSum(buy[h] * c[h] for h in hours),
        "energy_charged_kwh": pulp.lpSum(c[h] for h in hours),
        "energy_discharged_kwh": pulp.lpSum(d[h] for h in hours),
    }
    assert set(m.SCORING_KPIS) <= set(exprs)
    hourly = {"charge 02-03": c["02-03"] * 1, "discharge 19-20": d["19-20"] * 1}

    def span(expr):
        values = []
        for sense in (pulp.LpMinimize, pulp.LpMaximize):
            prob.setObjective(expr)
            prob.sense = sense
            pulp.LpProblem.solve(prob, pulp.HiGHS(msg=False))
            assert pulp.LpStatus[prob.status] == "Optimal"
            values.append(pulp.value(prob.objective))
        return values

    face = exprs["profit"]
    prob += (face >= opt - 1e-9, "optimal_face")
    for key in m.SCORING_KPIS:
        lo, hi = span(exprs[key])
        assert hi - lo < 1e-5, f"{key} is not unique at the optimum: [{lo}, {hi}]"
    for name, expr in hourly.items():
        lo, hi = span(expr)
        assert hi - lo > 1.0, f"{name} was expected to have alternative optima"


@pytest.mark.skipif(len(SOLVERS) < 2, reason="needs two open solvers")
@pytest.mark.parametrize("what_if", [
    {"changes": [{"op": "scale", "table": "hours", "column": "import_price", "factor": 0.8}]},
    {"changes": [{"op": "set_param", "name": "energy_capacity_kwh", "value": 20}]},
    {"changes": [{"op": "set_param", "name": "charge_efficiency", "value": 0.8}]},
    {"changes": [], "rules": [{"measure": "charge", "scope": {"hour": ["02-03", "03-04"]}, "sense": "<=", "value": 4}]},
], ids=["cheaper_imports", "bigger_battery", "worse_charger", "night_charging_cap"])
def test_scored_kpis_agree_across_solvers(what_if):
    results = {s: _what_if(solver=s, **what_if) for s in SOLVERS}
    assert all(r.status == "optimal" for r in results.values()), {s: r.message for s, r in results.items()}
    ref = results[SOLVERS[0]]
    for r in results.values():
        assert math.isclose(r.objective, ref.objective, rel_tol=1e-6, abs_tol=1e-6)
        for key in BatteryScheduling.SCORING_KPIS:
            assert math.isclose(r.kpis[key], ref.kpis[key], rel_tol=1e-6, abs_tol=1e-6), (r.solver, key)


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_peak_export_price_falls():
    # 5 kW are still sold in 21-22, now at 0.35 instead of 0.40: profit falls by 5 * 0.05
    r = _what_if([{"op": "set", "table": "hours", "column": "export_price", "where": {"hour": "21-22"}, "value": 0.35}])
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, 1.56625 - 0.25, abs_tol=1e-6)
    assert math.isclose(r.kpis["energy_discharged_kwh"], 7.2, abs_tol=1e-6)


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_rule_on_a_measure():
    # at most 3 kW exported in 21-22: 3 * 0.40 + 4.2 * 0.30 - 1.09375
    rule = {"measure": "discharge", "scope": {"hour": "21-22"}, "sense": "<=", "value": 3}
    r = _what_if(rules=[rule])
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, 1.36625, abs_tol=1e-6)


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_battery_starts_full_or_the_day_is_worthless():
    # starting full, nothing needs buying: profit is the sale of 7.2 kWh alone
    r = _what_if([{"op": "set_param", "name": "initial_soc_kwh", "value": 13.5}])
    assert r.status == "optimal" and math.isclose(r.objective, 2.66, abs_tol=1e-6)
    assert math.isclose(r.kpis["energy_charged_kwh"], 0.0, abs_tol=1e-6)
    # nothing is paid for exports: the battery stays idle at its starting charge
    r = _what_if([{"op": "set", "table": "hours", "column": "export_price", "value": 0}])
    assert r.status == "optimal" and math.isclose(r.objective, 0.0, abs_tol=1e-9)
    assert r.kpis["energy_charged_kwh"] == 0 and r.kpis["energy_discharged_kwh"] == 0
    assert r.kpis["charge_kw_by_hour"] == {} and r.kpis["peak_soc_kwh"] == pytest.approx(6.0)


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_battery_size_and_required_charge():
    profit = {cap: _what_if([{"op": "set_param", "name": "energy_capacity_kwh", "value": cap}]).objective
              for cap in (6, 13.5, 20, 27)}
    assert profit[6] < profit[13.5] < profit[20] < profit[27]
    assert math.isclose(profit[13.5], 1.56625, abs_tol=1e-6)
    # a required closing charge above the capacity cannot be met
    r = _what_if([{"op": "set_param", "name": "terminal_soc_kwh", "value": 20}])
    assert r.status == "infeasible"


def test_efficiency_outside_zero_one_is_rejected():
    m = BatteryScheduling()
    for name, bad in (("charge_efficiency", 0), ("discharge_efficiency", 1.2), ("charge_efficiency", -0.5)):
        data = m.load_data()
        data["params"][name] = bad
        with pytest.raises(ValueError, match=name):
            m.build(data)
    data = m.load_data()
    data["params"]["energy_capacity_kwh"] = None
    with pytest.raises(ValueError, match="energy_capacity_kwh"):
        m.build(data)
    data = m.load_data()
    data["hours"] = []
    with pytest.raises(ValueError, match="at least one hour"):
        m.build(data)


def test_generic_task_templates_work(monkeypatch):
    """The schema-driven families can build tasks for this model (the registry is patched until it is registered)."""
    import whatifgym.registry as registry
    from whatifgym.families import DataChangeFamily, NewLimitFamily

    original = registry._registry
    monkeypatch.setattr(registry, "_registry", lambda: {**original(), BatteryScheduling.name: BatteryScheduling})
    data_change = DataChangeFamily(BatteryScheduling.name)
    # only the two prices can be edited in the table; the hour order and the step length are structural
    assert data_change.ctx.numeric_columns("hours") == ["import_price", "export_price"]
    assert data_change.ctx.removable_tables() == []
    for family in (data_change, NewLimitFamily(BatteryScheduling.name)):
        tasks = family.generate(3, seed=1, max_seconds=120)
        assert tasks, family.skipped
        assert all(t.kpi_keys == BatteryScheduling.SCORING_KPIS and t.reference["status"] == "optimal" for t in tasks)
