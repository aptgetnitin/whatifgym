"""car_rental_2 (Gurobi modeling-examples car_rental_2): reference optimum on every open solver, original model
sizes, measures, the expansion plan the notebook reports, and the expansion options as scenario data."""
import copy
import math

import pytest

from whatifgym.models.car_rental_2.model import CarRental2
from whatifgym.oracle import solve_scenario
from whatifgym.solvers import available_solvers, pulp_sizes

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]

# What the original notebook reports at its optimum: Manchester expanded twice and Plymouth once, Birmingham not at
# all (3 of at most 3 options, 20000 + 5000 + 19000 a week), 983 cars, profit $132,341.47.
NOTEBOOK_PLAN = {"Glasgow": 0, "Manchester": 10, "Birmingham": 0, "Plymouth": 5}
NOTEBOOK_OPTIONS = {"expand_Manchester_1", "expand_Manchester_2", "expand_Plymouth_1"}


def isclose(a, b):
    return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-6)


def solve_with(edit, solver=None):
    m = CarRental2()
    data = copy.deepcopy(m.load_data())
    edit(data)
    r = m.solve(data, solver=solver or SOLVERS[0], time_limit=60)
    assert r.status == "optimal", r.message
    return r


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = CarRental2()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    assert math.isclose(r.objective, m.reference()["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert r.kpis
    assert all(k in r.kpis for k in m.SCORING_KPIS)


@pytest.mark.parametrize("solver", SOLVERS)
def test_expansion_plan_matches_notebook(solver):
    """Every solver finds the notebook's expansions: Manchester both steps and Plymouth, not Birmingham."""
    r = CarRental2().solve(solver=solver, time_limit=60, keep_variables=True)
    assert r.status == "optimal", r.message
    chosen = {name for name, value in r.variables.items() if name.startswith("expand_") and value > 0.5}
    assert chosen == NOTEBOOK_OPTIONS
    assert r.kpis["capacity_added"] == NOTEBOOK_PLAN
    assert r.kpis["expansion_cost"] == 44000
    assert round(r.kpis["fleet_size"]) == 983
    assert math.isclose(r.kpis["profit"], 132341.47, abs_tol=0.02)
    assert r.kpis["cars_rented"] == 2820.0  # 282 repairs a week (22 + 20 + 5 cars a day) = 10% of rentals
    assert r.kpis["repair_utilisation"] == {"Manchester": 1.0, "Birmingham": 1.0, "Plymouth": 1.0}


def test_sizes_and_measures():
    m = CarRental2(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"]) == (294, 118)
    assert pulp_sizes(prob) == (ref["n_vars"], ref["n_constraints"], ref["n_int_vars"]) == (294, 118, 5)
    assert sum(1 for v in prob.variables() if v.cat in ("Integer", "Binary")) == ref["n_int_vars"]
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert all(len(key) == len(ms[name].dims) for name in ms for key in ms[name].vars)
    assert len(ms["expand"].vars) == 5 and ms["expand"].dims == ("depot", "step")
    assert m.schema()["model"] == m.name and m.index_sets(data)


def test_schema_matches_data_and_carries_labels():
    m = CarRental2(); data = m.load_data(); schema = m.schema()
    assert set(schema["tables"]) == set(m.TABLES) and set(schema["params"]) == set(data["params"])
    assert all(set(spec["columns"]) == set(data[t][0]) for t, spec in schema["tables"].items())
    assert all(spec["label"] for spec in schema["tables"].values())
    assert all(c["label"] for spec in schema["tables"].values() for c in spec["columns"].values())
    assert all(p["label"] for p in schema["params"].values())
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == m.MEASURE_DIMS
    assert all(v["label"] for v in schema["measures"].values())
    # structural numbers are not what-ifs; key columns that point at another table say so
    assert schema["tables"]["days"]["columns"]["order"]["editable"] is False
    assert schema["tables"]["expansion_options"]["columns"]["step"]["editable"] is False
    assert schema["tables"]["expansion_options"]["columns"]["depot"]["ref"] == "depots.depot"
    assert schema["tables"]["expansion_options"]["key"] == ["depot", "step"]


def test_published_expansion_data():
    """The five options and the limit as the notebook gives them."""
    data = CarRental2().load_data()
    options = {(r["depot"], r["step"]): (r["added_capacity"], r["weekly_cost"]) for r in data["expansion_options"]}
    assert options == {("Birmingham", 1): (5, 18000), ("Birmingham", 2): (5, 8000), ("Manchester", 1): (5, 20000),
                       ("Manchester", 2): (5, 5000), ("Plymouth", 1): (5, 19000)}
    assert data["params"]["max_expansions"] == 3
    assert {r["depot"]: r["repair_capacity"] for r in data["depots"]} == {"Glasgow": 0, "Manchester": 12, "Birmingham": 20, "Plymouth": 0}
    assert sum(r["demand"] for r in data["demand"]) == 3266


def test_repair_depots_follow_the_data():
    """Repair depots are derived: a workshop today or an expansion option that adds capacity (Plymouth)."""
    m = CarRental2(); data = m.load_data()
    assert m._index(data)["repair_depots"] == ["Manchester", "Birmingham", "Plymouth"]
    no_option = copy.deepcopy(data)
    no_option["expansion_options"] = [r for r in no_option["expansion_options"] if r["depot"] != "Plymouth"]
    assert m._index(no_option)["repair_depots"] == ["Manchester", "Birmingham"]
    zero_gain = copy.deepcopy(data)
    for r in zero_gain["expansion_options"]:
        if r["depot"] == "Plymouth":
            r["added_capacity"] = 0
    assert m._index(zero_gain)["repair_depots"] == ["Manchester", "Birmingham"]
    # a depot that is not a repair depot cannot repair: its repair variables are pinned to zero
    prob = m.build(data)
    assert all(v.upBound == 0 for (t, d), v in prob._wig["repairs"].items() if d == "Glasgow")
    assert all(v.upBound is None for (t, d), v in prob._wig["repairs"].items() if d != "Glasgow")


def test_dearer_plymouth_expansion_drops_out():
    """At 25000 a week Plymouth's option no longer pays: the plan falls back to Manchester's two options."""
    def edit(data):
        for r in data["expansion_options"]:
            if (r["depot"], r["step"]) == ("Plymouth", 1):
                r["weekly_cost"] = 25000
    r = solve_with(edit)
    assert isclose(r.objective, 131725.3688) and r.kpis["capacity_added"]["Plymouth"] == 0
    assert r.kpis["capacity_added"] == {"Glasgow": 0, "Manchester": 10, "Birmingham": 0, "Plymouth": 0}
    assert r.kpis["expansion_cost"] == 25000


def test_expansion_limit_is_data():
    """Zero expansions allowed: no cost, no extra capacity, rentals fall to what the base workshops can repair;
    one more option than the notebook allows moves the plan to both Manchester and Birmingham steps."""
    none = solve_with(lambda d: d["params"].__setitem__("max_expansions", 0))
    assert isclose(none.objective, 120067.6039)
    assert none.kpis["expansion_cost"] == 0 and sum(none.kpis["capacity_added"].values()) == 0
    assert none.kpis["cars_rented"] == 1920.0  # 32 repairs a day for 6 days = 10% of rentals
    four = solve_with(lambda d: d["params"].__setitem__("max_expansions", 4))
    assert isclose(four.objective, 138102.8205) and four.objective > 132341.47
    assert four.kpis["capacity_added"] == {"Glasgow": 0, "Manchester": 10, "Birmingham": 10, "Plymouth": 0}
    assert four.kpis["expansion_cost"] == 51000


def test_further_expansion_needs_the_first():
    """Forcing Birmingham's step 2 through the scenario DSL brings step 1 along (and costs both steps)."""
    scenario = {"version": "0.1", "fixed_decisions": [{"measure": "expand", "scope": {"depot": "Birmingham", "step": 2}, "value": 1}]}
    r = solve_scenario(CarRental2(), scenario, solver=SOLVERS[0])
    assert r.status == "optimal", r.message
    assert r.kpis["capacity_added"]["Birmingham"] == 10 and r.kpis["expansion_cost"] == 18000 + 8000 + 19000
    assert isclose(r.objective, 129568.7843)
    # a rule on the measure works through the same dimensions: at most one expansion at Manchester
    rule = {"version": "0.1", "rules": [{"measure": "expand", "scope": {"depot": "Manchester"}, "sense": "<=", "value": 1}]}
    r2 = solve_scenario(CarRental2(), rule, solver=SOLVERS[0])
    assert r2.status == "optimal" and r2.kpis["capacity_added"]["Manchester"] <= 5
    assert r2.objective < 132341.47


def test_matches_car_rental_1_when_no_expansion_is_possible():
    """No Plymouth option (Plymouth is then a depot without workshop, as in Car Rental 1) and no expansion allowed:
    the same data and flows as Car Rental 1, whose reference optimum is 121160.20722480546."""
    def edit(data):
        data["params"]["max_expansions"] = 0
        data["expansion_options"] = [r for r in data["expansion_options"] if r["depot"] != "Plymouth"]
    r = solve_with(edit)
    assert math.isclose(r.objective, 121160.20722480546, rel_tol=1e-6)
    assert round(r.kpis["fleet_size"]) == 617 and r.kpis["cars_rented"] == 1920.0


def test_option_at_unknown_depot_is_ignored():
    m = CarRental2(); data = copy.deepcopy(m.load_data())
    data["expansion_options"].append({"depot": "Nowhere", "step": 1, "added_capacity": 5, "weekly_cost": 1})
    prob = m.build(data)
    assert (len(prob.variables()), len(prob.constraints)) == (294, 118)
    r = m.solve(data, solver=SOLVERS[0], time_limit=60)
    assert r.status == "optimal" and isclose(r.objective, m.reference()["objective"])
