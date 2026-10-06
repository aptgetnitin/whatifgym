"""Car Rental 2 — weekly fleet plan with repair-capacity expansion decisions (MILP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``car_rental/car_rental_2.ipynb`` (Apache-2.0), itself based on H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 26. It is Car Rental 1 (weekly steady-state fleet
plan of a rental company with four depots) plus an investment decision: which repair workshops to expand, and
by how many cars a day, when every expansion is an all-or-nothing option with a fixed weekly cost. Only the
published data values are reused; the code here is new.

The trading days form a cycle (the company is closed on Sunday, so a car due back on Sunday comes back on
Monday morning) and the plan is a steady state: every week looks the same, so the day before the first day
is the last day. Each morning a depot receives the cars returned that day (a fixed share of them damaged),
the undamaged cars transferred to it the day before, the cars it repaired the day before and the cars it
kept overnight. It then rents cars out, transfers undamaged cars and keeps the rest. Damaged cars at a depot
without a workshop are sent to a repair depot (one day in transit); a repair depot repairs up to its daily
capacity, and a repaired car can be rented from the next morning. A repair depot is a depot that has a
workshop or may get one; its daily capacity is the base capacity plus the capacity of the expansion options
that are carried out.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source

# The fleet is counted at the start of the third trading day of the cycle (Wednesday in the published data),
# the day the original counts it on. Structural, not data: in a steady state every day gives the same count.
FLEET_COUNT_DAY = 2


class CarRental2(BaseModel):
    name = "car_rental_2"
    title = "Car Rental 2 (Williams, example 26)"
    domain = "revenue_resource_planning"
    sense = "max"
    problem_type = "MILP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="car_rental/car_rental_2.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/car_rental/car_rental_2.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("depots", "days", "demand", "rental_lengths", "return_shares", "transfer_costs", "expansion_options")
    HAS_PARAMS = True
    MEASURE_DIMS = {
        "fleet_size": (),
        "rentals": ("day", "depot"),
        "undamaged_stock": ("day", "depot"),
        "damaged_stock": ("day", "depot"),
        "undamaged_left": ("day", "depot"),
        "damaged_left": ("day", "depot"),
        "undamaged_transfers": ("day", "from_depot", "to_depot"),
        "damaged_transfers": ("day", "from_depot", "to_depot"),
        "repairs": ("day", "depot"),
        "expand": ("depot", "step"),
    }
    # KPIs that are unique at the optimum (the expansion plan included); the scorer compares these
    SCORING_KPIS = ["profit", "rental_contribution", "transfer_cost", "fleet_cost", "fleet_size",
                    "expansion_cost", "capacity_added"]

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]) -> dict[str, Any]:
        """Sets and coefficients derived from the tables (rows naming an unknown depot or day are ignored)."""
        P = data["params"]
        days = [r["day"] for r in sorted(data["days"], key=lambda r: r["order"])]
        depots = [r["depot"] for r in data["depots"]]
        known_day, known_depot = set(days), set(depots)
        capacity = {r["depot"]: r["repair_capacity"] or 0 for r in data["depots"]}
        demand = {(r["day"], r["depot"]): r["demand"] or 0 for r in data["demand"]
                  if r["day"] in known_day and r["depot"] in known_depot}
        mix = {int(r["rental_days"]): r for r in data["rental_lengths"] if int(r["rental_days"]) >= 1}
        returns = {(r["from_depot"], r["to_depot"]): r["share"] for r in data["return_shares"]
                   if r["from_depot"] in known_depot and r["to_depot"] in known_depot and r["share"]}
        transfer_cost = {(r["from_depot"], r["to_depot"]): r["cost"] or 0 for r in data["transfer_costs"]
                         if r["from_depot"] in known_depot and r["to_depot"] in known_depot
                         and r["from_depot"] != r["to_depot"]}

        # Expansion options, one per (depot, step). Steps at a depot are taken in increasing order and each
        # step can only be carried out when the previous step at that depot is ("a further expansion").
        options: dict[tuple, dict[str, float]] = {}
        steps: dict[str, list] = {d: [] for d in depots}
        for r in data["expansion_options"]:
            if r["depot"] in known_depot and r["step"] is not None:
                key = (r["depot"], r["step"])
                if key not in options:
                    steps[r["depot"]].append(r["step"])
                options[key] = {"added": r["added_capacity"] or 0, "cost": r["weekly_cost"] or 0}
        prerequisite: dict[tuple, tuple] = {}
        for d, ordered in steps.items():
            ordered.sort()
            for earlier, later in zip(ordered, ordered[1:]):
                prerequisite[d, later] = (d, earlier)

        damaged = P["damaged_share"]
        fee = damaged * P["damage_excess"]  # expected damage excess earned per rental
        # contribution of one rental at depot d: over return depots and rental lengths,
        # return share * length share * (price for that return - marginal cost + expected excess)
        margin = {d: 0.0 for d in depots}
        for (d, d2), share in returns.items():
            price = "price_same_depot" if d == d2 else "price_other_depot"
            for row in mix.values():
                margin[d] += share * row["share"] * (row[price] - row["marginal_cost"] + fee)

        # share of a day's rentals still out at the start of the count day: a car rented for r days on
        # day s is away on the mornings s+1 .. s+r-1 and is back (and counted at a depot) on morning s+r
        n_days = len(days)
        count_pos = min(FLEET_COUNT_DAY, n_days - 1)
        on_rent: dict[int, float] = {}
        for r, row in mix.items():
            for k in range(1, r):
                pos = (count_pos - k) % n_days
                on_rent[pos] = on_rent.get(pos, 0) + row["share"]

        return {
            "days": days, "depots": depots, "capacity": capacity, "demand": demand,
            # a repair depot has a workshop now or can get one through an expansion option
            "repair_depots": [d for d in depots
                              if capacity[d] > 0 or any(options[d, k]["added"] > 0 for k in steps[d])],
            "options": options, "prerequisite": prerequisite,
            "mix_share": {r: row["share"] for r, row in mix.items()},
            "returns": returns, "transfer_cost": transfer_cost,
            "damaged": damaged, "undamaged": 1 - damaged, "margin": margin,
            "count_pos": count_pos, "on_rent": on_rent,
        }

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        ix = self._index(data)
        P = data["params"]
        days, depots = ix["days"], ix["depots"]
        n_days = len(days)
        repair_depots = set(ix["repair_depots"])
        lanes = list(ix["transfer_cost"])
        undamaged, damaged = ix["undamaged"], ix["damaged"]
        options = ix["options"]

        prob = pulp.LpProblem("car_rental_2", pulp.LpMaximize)
        cell = [(t, d) for t in days for d in depots]
        fleet = pulp.LpVariable("fleet_size", lowBound=0)
        rent = {(t, d): pulp.LpVariable(f"rentals_{t}_{d}", lowBound=0, upBound=ix["demand"].get((t, d), 0))
                for t, d in cell}
        ud_stock = {(t, d): pulp.LpVariable(f"undamaged_stock_{t}_{d}", lowBound=0) for t, d in cell}
        dm_stock = {(t, d): pulp.LpVariable(f"damaged_stock_{t}_{d}", lowBound=0) for t, d in cell}
        ud_left = {(t, d): pulp.LpVariable(f"undamaged_left_{t}_{d}", lowBound=0) for t, d in cell}
        dm_left = {(t, d): pulp.LpVariable(f"damaged_left_{t}_{d}", lowBound=0) for t, d in cell}
        ud_move = {(t, a, b): pulp.LpVariable(f"undamaged_transfer_{t}_{a}_{b}", lowBound=0)
                   for t in days for a, b in lanes}
        dm_move = {(t, a, b): pulp.LpVariable(f"damaged_transfer_{t}_{a}_{b}", lowBound=0)
                   for t in days for a, b in lanes}
        # every depot has a repair variable. A repair depot is limited by its capacity rows below (base capacity
        # plus the expansions carried out); a depot that has no workshop and no option is pinned to 0 repairs
        repair = {(t, d): pulp.LpVariable(f"repairs_{t}_{d}", lowBound=0, upBound=None if d in repair_depots else 0)
                  for t, d in cell}
        # 0/1: carry out the expansion option (depot, step)
        expand = {key: pulp.LpVariable(f"expand_{key[0]}_{key[1]}", cat=pulp.LpBinary) for key in options}

        # Objective: rental contribution - transfer costs (damaged or not) - weekly cost of the fleet
        # - weekly fixed cost of the expansions carried out
        prob += (pulp.lpSum(ix["margin"][d] * rent[t, d] for t, d in cell)
                 - pulp.lpSum(ix["transfer_cost"][a, b] * (ud_move[t, a, b] + dm_move[t, a, b])
                              for t in days for a, b in lanes)
                 - P["cost_per_car"] * fleet
                 - pulp.lpSum(opt["cost"] * expand[key] for key, opt in options.items())), "profit"

        arriving = {d: [a for a, b in lanes if b == d] for d in depots}
        leaving = {d: [b for a, b in lanes if a == d] for d in depots}
        for i, t in enumerate(days):
            prev = days[(i - 1) % n_days]
            for d in depots:
                # cars due back at d this morning: rented at d2 r days ago and returned to d
                back = [(ix["returns"][d2, d], p, rent[days[(i - r) % n_days], d2])
                        for d2 in depots if (d2, d) in ix["returns"] for r, p in ix["mix_share"].items()]

                # undamaged cars: what arrives this morning = what is rented, sent away or kept
                prob += (pulp.lpSum(undamaged * s * p * x for s, p, x in back)
                         + pulp.lpSum(ud_move[prev, a, d] for a in arriving[d])
                         + repair[prev, d] + ud_left[prev, d] == ud_stock[t, d]), f"undamaged_in_{t}_{d}"
                prob += (rent[t, d] + pulp.lpSum(ud_move[t, d, b] for b in leaving[d])
                         + ud_left[t, d] == ud_stock[t, d]), f"undamaged_out_{t}_{d}"

                # damaged cars. As in the original: a depot without a workshop sends damaged cars to repair
                # depots; a repair depot receives them from every other depot and its own outgoing damaged
                # transfers go to the depots without a workshop.
                if d in repair_depots:
                    dm_in = (pulp.lpSum(damaged * s * p * x for s, p, x in back)
                             + pulp.lpSum(dm_move[prev, a, d] for a in arriving[d]) + dm_left[prev, d])
                    dm_out = (repair[t, d] + pulp.lpSum(dm_move[t, d, b] for b in leaving[d] if b not in repair_depots)
                              + dm_left[t, d])
                else:
                    dm_in = pulp.lpSum(damaged * s * p * x for s, p, x in back) + dm_left[prev, d]
                    dm_out = (repair[t, d] + pulp.lpSum(dm_move[t, d, b] for b in leaving[d] if b in repair_depots)
                              + dm_left[t, d])
                prob += dm_in == dm_stock[t, d], f"damaged_in_{t}_{d}"
                prob += dm_out == dm_stock[t, d], f"damaged_out_{t}_{d}"

        # Fleet size: cars still on rent at the start of the count day + every car at a depot that morning
        w = days[ix["count_pos"]]
        prob += (pulp.lpSum(c * rent[days[pos], d] for pos, c in ix["on_rent"].items() for d in depots)
                 + pulp.lpSum(ud_stock[w, d] + dm_stock[w, d] for d in depots) == fleet), "fleet_count"

        # Repair capacity of a repair depot each day: base capacity + capacity of the expansions carried out
        for d in ix["repair_depots"]:
            gain = pulp.lpSum(opt["added"] * expand[key] for key, opt in options.items() if key[0] == d)
            for t in days:
                prob += repair[t, d] <= ix["capacity"][d] + gain, f"repair_capacity_{t}_{d}"

        # A further expansion at a depot needs the previous expansion there; at most `max_expansions` in total
        for key, earlier in ix["prerequisite"].items():
            prob += expand[key] <= expand[earlier], f"expansion_order_{key[0]}_{key[1]}"
        if options:
            prob += pulp.lpSum(expand.values()) <= P["max_expansions"], "expansion_limit"

        prob._wig = {  # handles for kpis() and the DSL, keys aligned with MEASURE_DIMS
            "fleet_size": {(): fleet}, "rentals": rent,
            "undamaged_stock": ud_stock, "damaged_stock": dm_stock,
            "undamaged_left": ud_left, "damaged_left": dm_left,
            "undamaged_transfers": ud_move, "damaged_transfers": dm_move, "repairs": repair,
            "expand": expand,
        }
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        ix = self._index(data)
        P = data["params"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        days = ix["days"]
        rented = sum(val(x) for x in v["rentals"].values())
        contribution = sum(ix["margin"][d] * val(x) for (t, d), x in v["rentals"].items())
        transfer = sum(cost * (val(v["undamaged_transfers"][t, a, b]) + val(v["damaged_transfers"][t, a, b]))
                       for (a, b), cost in ix["transfer_cost"].items() for t in days)
        fleet = val(v["fleet_size"][()])
        fleet_cost = P["cost_per_car"] * fleet
        demand = sum(ix["demand"].values())

        built = [key for key, x in v["expand"].items() if val(x) > 0.5]
        expansion_cost = sum(ix["options"][key]["cost"] for key in built)
        added = {d: sum(ix["options"][key]["added"] for key in built if key[0] == d) for d in ix["depots"]}

        utilisation = {}  # share of the repair capacity in place (base + expansions carried out) that is used
        for d in ix["repair_depots"]:
            weekly = (ix["capacity"][d] + added[d]) * len(days)
            if weekly > 0:
                utilisation[d] = round(sum(val(v["repairs"][t, d]) for t in days) / weekly, 4)
        return {
            "profit": round(contribution - transfer - fleet_cost - expansion_cost, 2),
            "rental_contribution": round(contribution, 2),
            "transfer_cost": round(transfer, 2),
            "fleet_cost": round(fleet_cost, 2),
            "fleet_size": round(fleet, 2),
            "expansion_cost": round(expansion_cost, 2),
            "capacity_added": {d: round(added[d], 2) for d in ix["depots"]},  # repair cars/day added per depot
            "cars_rented": round(rented, 2),
            "demand_fill_rate": round(rented / demand, 4) if demand else None,
            "repair_utilisation": utilisation,
        }
