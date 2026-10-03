"""Farm Planning — five-year herd, crop and housing-finance plan for a dairy farm (LP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example ``farm_planning/farm_planning.ipynb``
(Apache-2.0), itself based on H. P. Williams, *Model Building in Mathematical Programming*, 5th ed., example 8.
Only the published data values are reused; the code here is new.

The herd is tracked by age. With the ages of ``ages.csv`` sorted, the youngest age holds the one-year-old heifers,
the oldest holds the cows sold that year, and every age in between is a dairy cow (ages 1, 12 and 2-11 in the
published data). Newborn heifer calves are either raised (they join the youngest age the next year) or sold.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class FarmPlanning(BaseModel):
    name = "farm_planning"
    title = "Farm Planning (Williams, example 8)"
    domain = "production_planning"
    sense = "max"
    problem_type = "LP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="farm_planning/farm_planning.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/farm_planning/farm_planning.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("years", "land_groups", "ages")
    MEASURE_DIMS = {
        "herd": ("year", "age"),
        "raise_heifers": ("year",),
        "sell_heifers": ("year",),
        "grow_grain": ("year", "land_group"),
        "grow_beet": ("year",),
        "buy_grain": ("year",),
        "sell_grain": ("year",),
        "buy_beet": ("year",),
        "sell_beet": ("year",),
        "overtime": ("year",),
        "extra_housing": ("year",),
        "yearly_profit": ("year",),
    }
    # KPIs that are unique at the optimum; the scorer compares these. Horizon totals only: the per-year breakdowns
    # (profit_by_year, dairy_cows_by_year) have alternative optima once a rule caps a total over several years.
    SCORING_KPIS = ["profit", "final_dairy_cows", "heifer_calves", "feed_trade_tons", "extra_housing_places",
                    "overtime_hours", "revenue", "costs"]
    REVENUE_PARTS = ("milk", "calves", "cull_cows", "crop_sales")
    COST_PARTS = ("feed_purchases", "labour", "herd_upkeep", "crop_growing", "housing_loan")

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]) -> dict[str, Any]:
        years = [r["year"] for r in sorted(data["years"], key=lambda r: r["order"])]
        lands = [r["land_group"] for r in data["land_groups"]]
        ages = sorted(r["age"] for r in data["ages"])
        if len(set(ages)) != len(ages) or len(ages) < 3:
            raise ValueError("ages.age must hold at least three different ages: the heifer age, one or more "
                             f"dairy-cow ages and the sale age; got {ages}")
        P = data["params"]
        # Tons of crop -> acres used. A crop that yields nothing occupies no land (and none of it is grown).
        beet_acres_per_ton = 1 / P["beet_yield"] if P["beet_yield"] > 0 else 0.0
        grain_acres_per_ton = {r["land_group"]: (1 / r["grain_yield"] if r["grain_yield"] > 0 else 0.0)
                               for r in data["land_groups"]}
        return {
            "years": years,
            "lands": lands,
            "ages": ages,
            "heifer_age": ages[0],
            "dairy_ages": ages[1:-1],
            "sale_age": ages[-1],
            "initial_head": {r["age"]: r["initial_head"] for r in data["ages"]},
            "grain_limit": {r["land_group"]: r["grain_yield"] * r["area"] for r in data["land_groups"]},
            "grain_acres_per_ton": grain_acres_per_ton,
            "beet_acres_per_ton": beet_acres_per_ton,
        }

    @staticmethod
    def _repayment_years(years: list, term: float) -> dict[Any, tuple[list, float]]:
        """For a housing outlay made in each year: the planning years in which an instalment is paid, and the
        number of instalments still due after the last planning year (charged to the plan in the objective)."""
        out = {}
        for i, d in enumerate(years):
            paid_in = [t for j, t in enumerate(years) if 0 <= j - i < term]
            out[d] = (paid_in, max(0.0, term - len(paid_in)))
        return out

    def _parts(self, prob, data: dict[str, Any], ix: dict[str, Any]) -> dict[str, dict[Any, Any]]:
        """Revenue and cost parts per year as PuLP expressions (yearly profit = revenue - cost), the loan repayments
        still due after the last year (``pending``, charged in the objective) and the herd and acre subtotals."""
        import pulp

        P = data["params"]
        v = prob._wig
        years, lands = ix["years"], ix["lands"]
        dairy = {t: pulp.lpSum(v["herd"][t, a] for a in ix["dairy_ages"]) for t in years}
        heifers = {t: v["raise_heifers"][t] + v["herd"][t, ix["heifer_age"]] for t in years}
        grain_acres = {t: pulp.lpSum(ix["grain_acres_per_ton"][l] * v["grow_grain"][t, l] for l in lands) for t in years}
        beet_acres = {t: ix["beet_acres_per_ton"] * v["grow_beet"][t] for t in years}
        repay = self._repayment_years(years, P["loan_term_years"])
        loan = {t: pulp.lpSum(P["housing_installment"] * v["extra_housing"][d]
                              for d in years if t in repay[d][0]) for t in years}
        pending = pulp.lpSum(P["housing_installment"] * repay[d][1] * v["extra_housing"][d] for d in years)
        calves_sold = P["bullock_price"] * P["calves_per_cow"] * (1 - P["heifer_calf_share"])
        parts = {
            "milk": {t: P["milk_revenue_per_cow"] * dairy[t] for t in years},
            "calves": {t: calves_sold * dairy[t] + P["heifer_calf_price"] * v["sell_heifers"][t] for t in years},
            "cull_cows": {t: P["cull_cow_price"] * v["herd"][t, ix["sale_age"]] for t in years},
            "crop_sales": {t: P["grain_sale_price"] * v["sell_grain"][t] + P["beet_sale_price"] * v["sell_beet"][t]
                           for t in years},
            "feed_purchases": {t: P["grain_purchase_price"] * v["buy_grain"][t]
                               + P["beet_purchase_price"] * v["buy_beet"][t] for t in years},
            "labour": {t: P["regular_labour_cost"] + P["overtime_cost"] * v["overtime"][t] for t in years},
            "herd_upkeep": {t: P["heifer_upkeep"] * heifers[t] + P["cow_upkeep"] * dairy[t] for t in years},
            "crop_growing": {t: P["grain_acre_cost"] * grain_acres[t] + P["beet_acre_cost"] * beet_acres[t]
                             for t in years},
            "housing_loan": loan,
        }
        return {"parts": parts, "pending": pending, "dairy": dairy, "heifers": heifers,
                "grain_acres": grain_acres, "beet_acres": beet_acres}

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        ix = self._index(data)
        P = data["params"]
        years, lands, ages = ix["years"], ix["lands"], ix["ages"]
        heifer_age, dairy_ages = ix["heifer_age"], ix["dairy_ages"]
        first, last = years[0], years[-1]

        prob = pulp.LpProblem("farm_planning", pulp.LpMaximize)

        def yearly(name: str, **bounds):
            return {t: pulp.LpVariable(f"{name}_{t}", **bounds) for t in years}

        # Sugar beet needs land to grow; if it yields nothing, none can be grown.
        grow_beet = yearly("grow_beet", lowBound=0, upBound=None if P["beet_yield"] > 0 else 0)
        buy_grain = yearly("buy_grain", lowBound=0)
        sell_grain = yearly("sell_grain", lowBound=0)
        buy_beet = yearly("buy_beet", lowBound=0)
        sell_beet = yearly("sell_beet", lowBound=0)
        overtime = yearly("overtime", lowBound=0)
        extra_housing = yearly("extra_housing", lowBound=0)
        sell_heifers = yearly("sell_heifers", lowBound=0)
        raise_heifers = yearly("raise_heifers", lowBound=0)
        # Yearly profit is the cash flow after loan repayments; its lower bound keeps every year out of the red.
        yearly_profit = yearly("yearly_profit", lowBound=P["min_yearly_profit"])
        grow_grain = {(t, l): pulp.LpVariable(f"grow_grain_{t}_{l}", lowBound=0) for t in years for l in lands}
        herd = {(t, a): pulp.LpVariable(f"herd_{t}_{a}", lowBound=0) for t in years for a in ages}
        # The final dairy herd must lie in [min, max]: one equality row with a bounded slack, which is how the
        # original's range constraint is stored (final dairy cows + headroom = max, 0 <= headroom <= max - min).
        headroom = pulp.LpVariable("final_dairy_cows_headroom", lowBound=0,
                                   upBound=P["max_final_dairy_cows"] - P["min_final_dairy_cows"])

        prob._wig = {"herd": herd, "raise_heifers": raise_heifers, "sell_heifers": sell_heifers,
                     "grow_grain": grow_grain, "grow_beet": grow_beet, "buy_grain": buy_grain,
                     "sell_grain": sell_grain, "buy_beet": buy_beet, "sell_beet": sell_beet, "overtime": overtime,
                     "extra_housing": extra_housing, "yearly_profit": yearly_profit,
                     "final_dairy_cows_headroom": headroom}  # the headroom slack is not a measure
        x = self._parts(prob, data, ix)
        dairy, heifers, grain_acres, beet_acres = x["dairy"], x["heifers"], x["grain_acres"], x["beet_acres"]

        # Objective: the yearly profits, less the loan repayments for extra housing still due after the horizon
        # (so that housing built late costs as much as housing built early).
        prob += pulp.lpSum(yearly_profit[t] for t in years) - x["pending"], "total_profit"

        # Housing: heifers (calves being raised and one-year-olds) and dairy cows fit the existing places plus
        # every place added so far.
        for t in years:
            built = pulp.lpSum(extra_housing[d] for d in years[:years.index(t) + 1])
            prob += heifers[t] + dairy[t] - built <= P["housing_capacity"], f"housing_{t}"

        # Feed: grain and sugar beet eaten by the dairy cows come from the farm's crop or from net purchases.
        for t in years:
            grown = pulp.lpSum(grow_grain[t, l] for l in lands)
            prob += P["grain_per_cow"] * dairy[t] <= buy_grain[t] - sell_grain[t] + grown, f"grain_feed_{t}"
        for t in years:
            prob += P["beet_per_cow"] * dairy[t] <= buy_beet[t] - sell_beet[t] + grow_beet[t], f"beet_feed_{t}"

        # Grain grows only on the suitable land groups, at most yield x area per group.
        for t in years:
            for l in lands:
                prob += grow_grain[t, l] <= ix["grain_limit"][l], f"grain_land_{t}_{l}"

        # Land: sugar beet, heifers, grain and dairy cows share the farm's acres.
        for t in years:
            prob += (beet_acres[t] + P["heifer_acres"] * heifers[t] + grain_acres[t] + P["cow_acres"] * dairy[t]
                     <= P["land_area"]), f"land_{t}"

        # Labour: hours needed by the herd and the crops, beyond the regular hours, are paid as overtime.
        for t in years:
            prob += (P["heifer_labour_hours"] * heifers[t] + P["cow_labour_hours"] * dairy[t]
                     + P["grain_labour_hours"] * grain_acres[t] + P["beet_labour_hours"] * beet_acres[t]
                     <= P["regular_labour_hours"] + overtime[t]), f"labour_{t}"

        # Ageing: calves raised last year become heifers, heifers become dairy cows (heifer death rate), and dairy
        # cows grow one year older (cow death rate) up to the sale age.
        heifer_survival, cow_survival = 1 - P["heifer_death_rate"], 1 - P["cow_death_rate"]
        for prev, t in zip(years, years[1:]):
            prob += herd[t, heifer_age] == heifer_survival * raise_heifers[prev], f"calves_raised_{t}"
        for prev, t in zip(years, years[1:]):
            prob += herd[t, ages[1]] == heifer_survival * herd[prev, heifer_age], f"heifers_calve_{t}"
        for prev, t in zip(years, years[1:]):
            for younger, older in zip(dairy_ages, ages[2:]):
                prob += herd[t, older] == cow_survival * herd[prev, younger], f"ageing_{t}_{older}"

        # Calving: the heifer calves born to the dairy cows are raised or sold (bullocks are sold at birth).
        for t in years:
            prob += (raise_heifers[t] + sell_heifers[t]
                     == P["calves_per_cow"] * P["heifer_calf_share"] * dairy[t]), f"calving_{t}"

        # Final dairy herd within [min_final_dairy_cows, max_final_dairy_cows] (range row, see headroom).
        prob += dairy[last] + headroom == P["max_final_dairy_cows"], "final_dairy_cows"

        # Initial herd in the first year.
        for a in ages:
            prob += herd[first, a] == ix["initial_head"][a], f"initial_herd_{a}"

        # Yearly profit = revenue - costs (the regular labour cost is fixed and appears as the constant).
        for t in years:
            revenue = pulp.lpSum(x["parts"][p][t] for p in self.REVENUE_PARTS)
            cost = pulp.lpSum(x["parts"][p][t] for p in self.COST_PARTS)
            prob += yearly_profit[t] == revenue - cost, f"profit_{t}"

        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        import pulp

        ix = self._index(data)
        years, last = ix["years"], ix["years"][-1]
        v = prob._wig
        val = lambda e: pulp.value(e) or 0.0  # noqa: E731
        x = self._parts(prob, data, ix)
        revenue = {p: sum(val(x["parts"][p][t]) for t in years) for p in self.REVENUE_PARTS}
        cost = {p: sum(val(x["parts"][p][t]) for t in years) for p in self.COST_PARTS}
        cost["housing_loan"] += val(x["pending"])
        total = lambda name: sum(val(e) for e in v[name].values())  # noqa: E731
        # Money to the cent; head, tons, places and hours to 4 decimals, so that solver noise rounds away near zero
        # and rounding never moves a value of 0.1 or more by the scorer's 1e-3 relative tolerance.
        qty = lambda z: round(z, 4)  # noqa: E731
        return {
            "profit": round(sum(revenue.values()) - sum(cost.values()), 2),
            "profit_by_year": {t: round(val(v["yearly_profit"][t]), 2) for t in years},
            "final_dairy_cows": qty(val(x["dairy"][last])),
            "dairy_cows_by_year": {t: qty(val(x["dairy"][t])) for t in years},
            "heifer_calves": {"raised": qty(total("raise_heifers")), "sold": qty(total("sell_heifers"))},
            "feed_trade_tons": {"grain_bought": qty(total("buy_grain")), "grain_sold": qty(total("sell_grain")),
                                "beet_bought": qty(total("buy_beet")), "beet_sold": qty(total("sell_beet"))},
            "extra_housing_places": qty(total("extra_housing")),
            "overtime_hours": qty(total("overtime")),
            "revenue": {p: round(z, 2) for p, z in revenue.items()},
            "costs": {p: round(z, 2) for p, z in cost.items()},
        }
