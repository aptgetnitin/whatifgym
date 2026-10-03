"""Food Supply: reference optimum and size of the original notebook, tidy data, schema labels, what-if behaviour."""
import math

import pytest

from whatifgym.models.food_supply.model import FoodSupply
from whatifgym.solvers import available_solvers

SOLVERS = [s for s in available_solvers() if s in ("highs", "scip", "cbc")]


@pytest.mark.parametrize("solver", SOLVERS)
def test_reference_objective(solver):
    m = FoodSupply()
    r = m.solve(solver=solver, time_limit=60)
    assert r.status == "optimal", r.message
    ref = m.reference()
    assert math.isclose(r.objective, ref["objective"], rel_tol=1e-6, abs_tol=1e-6)
    assert abs(r.objective - 400812394.0) < 0.05  # the notebook prints 4.008123940e+08
    assert (r.n_vars, r.n_constraints, r.n_int_vars) == (ref["n_vars"], ref["n_constraints"], ref["n_int_vars"])
    assert r.kpis
    assert math.isclose(r.kpis["total_cost"], r.objective, abs_tol=0.01)
    # unique at the optimum (min/max over the optimal face); flows, per-camp rations and per-supplier purchases
    # are not scored
    assert math.isclose(r.kpis["procurement_cost"], 354457744.76, abs_tol=1.0)
    assert math.isclose(r.kpis["transport_cost"], 46354649.24, abs_tol=1.0)
    assert math.isclose(r.kpis["food_bought"], 324391.38, abs_tol=0.1)


def test_sizes_and_measures():
    m = FoodSupply(); data = m.load_data(); prob = m.build(data)
    ref = m.reference()
    assert (len(prob.variables()), len(prob.constraints)) == (ref["n_vars"], ref["n_constraints"])
    # the original's matrix: 3541 nonzeros and 1080 nonzero objective coefficients (Gurobi's counts)
    assert sum(1 for c in prob.constraints.values() for a in c.values() if a != 0) == 3541
    assert sum(1 for a in prob.objective.values() if a != 0) == 1080
    ms = m.measures(prob)
    assert set(ms) == set(m.MEASURE_DIMS) and all(len(v.vars) > 0 for v in ms.values())
    assert m.schema()["model"] == m.name and m.index_sets(data)
    # 24 foods x (7 camps, 11 suppliers, 34 links between different cities); the inert self-link flows and the
    # range variables of the nutrition rows are in no measure
    assert (len(ms["ration"].vars), len(ms["purchase"].vars), len(ms["flow"].vars)) == (168, 264, 816)
    in_measures = {id(v) for meas in ms.values() for v in meas.vars.values()}
    inert = [*prob._wig["local_flow"].values(), *prob._wig["nutrient_surplus"].values()]
    assert len(inert) == 72 + 77 and not any(id(v) in in_measures for v in inert)


def test_tidy_data_reproduces_notebook_inputs():
    ix = FoodSupply._index(FoodSupply.load_data())
    sizes = tuple(len(ix[k]) for k in ("foods", "nutrients", "suppliers", "camps", "arcs", "cities"))
    assert sizes == (24, 11, 11, 7, 37, 15)
    assert sum(ix["beneficiaries"].values()) == 67000 and len(ix["content"]) == 200
    assert len(ix["price"]) == 264 and None not in ix["price"].values()
    assert ix["price"]["Aleppo", "Beans"] == 2781.6      # local mean price
    assert ix["price"]["Amman", "Beans"] == 1000         # international price where there is no local one
    assert ix["transport"]["Hama", "Jubb_al_Jarrah"] == 148  # the notebook keeps the last of the repeated rows
    assert ix["minimum"]["Energy(kcal)"] == 2100


def test_schema_matches_data_and_has_labels():
    m = FoodSupply(); data = m.load_data(); schema = m.schema()
    assert set(schema["tables"]) == set(m.TABLES)
    assert set(schema["params"]) == set(data["params"])
    assert {k: tuple(v["dims"]) for k, v in schema["measures"].items()} == m.MEASURE_DIMS
    for table, spec in schema["tables"].items():
        assert spec["label"]
        assert set(spec["columns"]) == set(data[table][0]), table
        assert all(col["label"] for col in spec["columns"].values()), table
        keys = [tuple(r[k] for k in spec["key"]) for r in data[table]]
        assert len(keys) == len(set(keys)), table
        for col, cs in spec["columns"].items():
            if "ref" in cs:  # a reference names another table's key and every value exists there
                t, c = cs["ref"].split(".")
                assert c in schema["tables"][t]["key"], (table, col)
                assert {r[col] for r in data[table]} <= {r[c] for r in data[t]}, (table, col)
    assert all(p["label"] for p in schema["params"].values())
    assert all(v["label"] for v in schema["measures"].values())


@pytest.mark.skipif(not SOLVERS, reason="no PuLP-backed solver available")
def test_what_if_moves_objective():
    from whatifgym.oracle import solve_scenario

    m = FoodSupply(); data = m.load_data(); solver = SOLVERS[0]
    base = m.reference()["objective"]

    def solve(**scenario):
        r = solve_scenario(m, {"version": "0.1", "base_model": m.name, **scenario}, data, solver=solver,
                           keep_decisions=False)
        assert r.status == "optimal", r.message
        return r

    more_people = solve(data_changes=[{"op": "set", "table": "camps", "column": "beneficiaries",
                                       "where": {"camp": "Idleb"}, "value": 10000}])
    assert more_people.objective > base + 1.0

    camp_closes = solve(data_changes=[{"op": "remove", "table": "camps", "where": {"camp": "Qamishli"}}])
    assert camp_closes.objective < base - 1.0

    # Homs stops selling but stays on the road network as a pure transit city: food is conserved there (the
    # original would write no balance row for it)
    transit = solve(data_changes=[{"op": "remove", "table": "suppliers", "where": {"supplier": "Homs"}}])
    assert transit.objective > base + 1.0
    people = {r["camp"]: r["beneficiaries"] for r in data["camps"]}
    handed_out = sum(people[j] * q for j, q in transit.kpis["ration_per_person"].items())
    assert math.isclose(handed_out, transit.kpis["food_bought"], rel_tol=1e-4)

    capped = solve(rules=[{"measure": "purchase", "scope": {"supplier": "Hassakeh"}, "sense": "<=", "value": 50000}])
    assert capped.objective > base + 1.0

    # a shipment floor cannot be met by the inert Daraa -> Daraa link: it is not part of the flow measure
    shipped = solve(rules=[{"measure": "flow", "scope": {"from_city": "Daraa"}, "sense": ">=", "value": 1000}])
    assert shipped.objective > base + 1.0
