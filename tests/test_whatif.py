"""What-if scenarios are data edits: change a table, re-solve, compare KPIs. Smoke tests of that loop."""
import copy

import pytest

from whatifgym import get_model
from whatifgym.base import write_table
from whatifgym.solvers import available_solvers

SOLVER = "highs" if "highs" in available_solvers() else "scip"


def _edit(data, table, where, column, value):
    data = copy.deepcopy(data)
    for row in data[table]:
        if all(row[k] == v for k, v in where.items()):
            row[column] = value
    return data


def test_factory_planning_more_maintenance_cannot_raise_profit():
    m = get_model("factory_planning")
    base = m.solve(solver=SOLVER)
    worse = _edit(m.load_data(), "downtime", {"month": "Feb", "machine": "horiDrill"}, "machines_down", 3)
    hit = m.solve(worse, solver=SOLVER)
    assert hit.status == "optimal" and hit.objective <= base.objective + 1e-6
    assert hit.kpis != base.kpis, "the plan should change when a machine type is fully down for a month"


def test_factory_planning_demand_drop_changes_product_mix():
    m = get_model("factory_planning")
    data = m.load_data()
    base = m.solve(data, solver=SOLVER)
    scen = _edit(data, "max_sales", {"month": "May", "product": "Prod5"}, "max_sales", 500)
    res = m.solve(scen, solver=SOLVER)
    assert res.objective < base.objective
    assert res.kpis["units_sold_by_product"]["Prod5"] < base.kpis["units_sold_by_product"]["Prod5"]


def test_knapsack_extra_bin_raises_packed_value():
    m = get_model("multiple_knapsack")
    data = m.load_data()
    data["bins"].append({"bin": "bin5", "capacity": 100})
    res = m.solve(data, solver=SOLVER)
    # total item value is 430; one more 100-unit bin lifts the optimum from 395 to 420 but still cannot fit all 558 weight units
    assert res.status == "optimal" and 395 < res.objective <= 430 and res.kpis["bins_used"] == 6


def test_knapsack_total_value_is_an_upper_bound():
    m = get_model("multiple_knapsack")
    data = m.load_data()
    for b in data["bins"]:
        b["capacity"] = 1000
    res = m.solve(data, solver=SOLVER)
    assert res.status == "optimal" and res.objective == sum(r["value"] for r in data["items"]) == 430
    assert res.kpis["items_left_out"] == 0


def test_wedding_fewer_tables_is_infeasible():
    """17 guests do not fit on 4 tables of 4: the environment must report infeasibility, not a number."""
    m = get_model("wedding_seating")
    data = m.load_data()
    data["params"]["max_tables"] = 4
    res = m.solve(data, solver=SOLVER)
    assert res.status == "infeasible" and res.objective is None and res.kpis == {}


def test_wedding_bigger_tables_restore_feasibility():
    m = get_model("wedding_seating")
    data = m.load_data()
    data["params"]["max_tables"] = 4
    data["params"]["max_table_size"] = 5
    res = m.solve(data, solver=SOLVER)
    assert res.status == "optimal" and res.kpis["tables_used"] <= 4 and res.kpis["largest_table"] <= 5
    assert res.n_vars == 17 + 136 + 680 + 2380 + 6188  # all subsets of size 1..5 of 17 guests


def test_scenario_round_trips_through_csv(tmp_path):
    """A scenario materialised as a data directory loads and solves like the shipped data."""
    m = get_model("multiple_knapsack")
    data = m.load_data()
    for table in m.TABLES:
        write_table(tmp_path / f"{table}.csv", data[table])
    assert m.solve(m.load_data(tmp_path), solver=SOLVER).objective == 395
