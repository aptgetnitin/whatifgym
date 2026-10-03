"""Manpower Planning — three-year recruitment, retraining, downgrading and redundancy plan (LP).

Clean-room re-implementation in PuLP of the public Gurobi modeling example
``manpower_planning/manpower_planning.ipynb`` (Apache-2.0), itself based on H. P. Williams,
*Model Building in Mathematical Programming*, 5th ed., example 5. Only the published data values
are reused; the code here is new.

``build`` minimises total redundancy (the notebook's first objective). The notebook's second objective,
total cost, is available as :meth:`ManpowerPlanning.cost_expression` and is reported as the ``total_cost`` KPI.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class ManpowerPlanning(BaseModel):
    name = "manpower_planning"
    title = "Manpower Planning (Williams, example 5)"
    domain = "scheduling"
    sense = "min"
    problem_type = "LP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="manpower_planning/manpower_planning.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/manpower_planning/manpower_planning.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook; model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("skills", "years", "requirements", "retraining", "costs")
    MEASURE_DIMS = {
        "recruit": ("year", "skill"),
        "retrain": ("year", "from_skill", "to_skill"),
        "downgrade": ("year", "from_skill", "to_skill"),
        "redundant": ("year", "skill"),
        "short_time": ("year", "skill"),
        "overmanned": ("year", "skill"),
        "workforce": ("year", "skill"),
    }
    SCORING_KPIS = ["total_redundancy", "redundancy_by_year", "redundancy_by_skill"]  # KPIs that are unique at the optimum; the scorer compares these
    COST_PARTS = ("retraining", "redundancy", "short_time", "overmanning")

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _index(data: dict[str, Any]) -> dict[str, Any]:
        rows = sorted(data["skills"], key=lambda r: r["level"])
        skills = [r["skill"] for r in rows]
        level = {r["skill"]: r["level"] for r in rows}
        if len(set(level.values())) != len(level):
            raise ValueError("skills.level must differ between skill levels: it decides which moves are "
                             "retraining (to a higher level) and which are downgrading (to a lower level)")
        known = set(skills)
        # A retraining row limits (and prices) one move between two different known skill levels.
        retraining = {(r["from_skill"], r["to_skill"]): r for r in data["retraining"]
                      if r["from_skill"] in known and r["to_skill"] in known and r["from_skill"] != r["to_skill"]}
        return {
            "skills": skills,
            "level": level,
            "years": sorted(r["year"] for r in data["years"]),
            "strength": {r["skill"]: r["current_strength"] for r in rows},
            "attrition_new": {r["skill"]: r["attrition_new"] for r in rows},
            "attrition_experienced": {r["skill"]: r["attrition_experienced"] for r in rows},
            "required": {(r["year"], r["skill"]): r["required"] for r in data["requirements"]},
            "max_recruit": {(r["year"], r["skill"]): r["max_recruit"] for r in data["requirements"]},
            "retraining": retraining,
            "costs": {r["skill"]: r for r in data["costs"]},
        }

    @staticmethod
    def _cost_terms(prob, ix: dict[str, Any]) -> list[tuple[float, Any, str]]:
        """(cost per worker, variable, cost part) for every priced decision of a built problem."""
        v = prob._wig
        move = {**v["retrain"], **v["downgrade"]}
        priced = (("redundancy_cost", "redundant", "redundancy"), ("short_time_cost", "short_time", "short_time"),
                  ("overmanning_cost", "overmanned", "overmanning"))
        terms = []
        for t in ix["years"]:
            for (a, b), row in ix["retraining"].items():
                if row["cost"]:
                    terms.append((row["cost"], move[t, a, b], "retraining"))
            for s in ix["skills"]:
                rates = ix["costs"].get(s, {})
                for column, measure, part in priced:
                    if rates.get(column):
                        terms.append((rates[column], v[measure][t, s], part))
        return terms

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        ix = self._index(data)
        years, skills, level = ix["years"], ix["skills"], ix["level"]
        P = data["params"]
        cells = [(t, s) for t in years for s in skills]

        prob = pulp.LpProblem("manpower_planning", pulp.LpMinimize)
        recruit = {(t, s): pulp.LpVariable(f"recruit_{t}_{s}", lowBound=0, upBound=ix["max_recruit"].get((t, s), 0))
                   for t, s in cells}
        short_time = {(t, s): pulp.LpVariable(f"short_time_{t}_{s}", lowBound=0, upBound=P["max_short_time"])
                      for t, s in cells}
        workforce = {(t, s): pulp.LpVariable(f"workforce_{t}_{s}", lowBound=0) for t, s in cells}
        redundant = {(t, s): pulp.LpVariable(f"redundant_{t}_{s}", lowBound=0) for t, s in cells}
        overmanned = {(t, s): pulp.LpVariable(f"overmanned_{t}_{s}", lowBound=0) for t, s in cells}
        # Moves between skill levels: up = retraining, down = downgrading. The notebook declares its move
        # variable over every (year, skill, skill), so it also has same-level columns that enter no constraint.
        # They are kept, inert and outside every measure, so the model has the original's 72 columns.
        retrain, downgrade, same_level = {}, {}, {}
        for t in years:
            for a in skills:
                for b in skills:
                    if a == b:
                        same_level[t, a] = pulp.LpVariable(f"same_level_{t}_{a}", lowBound=0)
                    elif level[b] > level[a]:
                        retrain[t, a, b] = pulp.LpVariable(f"retrain_{t}_{a}_{b}", lowBound=0)
                    else:
                        downgrade[t, a, b] = pulp.LpVariable(f"downgrade_{t}_{a}_{b}", lowBound=0)
        move = {**retrain, **downgrade}

        # Objective: total redundancies over the horizon. The inert same-level columns carry an explicit zero
        # cost (as in the original, where every column has an objective coefficient); this keeps them in the
        # problem for every PuLP backend (CBC cannot map back a column that is in neither objective nor rows).
        prob += pulp.LpAffineExpression([(x, 1) for x in redundant.values()]
                                        + [(x, 0) for x in same_level.values()]), "total_redundancy"

        # Workforce balance. Experienced staff (the year-1 opening strength, or last year's workforce) lose
        # attrition_experienced; recruits lose attrition_new; workers retrained in lose the destination
        # level's attrition_experienced; workers downgraded in lose downgrade_attrition.
        keep_downgraded = 1 - P["downgrade_attrition"]
        for i, t in enumerate(years):
            for s in skills:
                keep = 1 - ix["attrition_experienced"][s]
                previous = ix["strength"][s] if i == 0 else workforce[years[i - 1], s]
                flows = keep * previous + (1 - ix["attrition_new"][s]) * recruit[t, s]
                for o in skills:
                    if o != s:
                        kept = keep if level[o] < level[s] else keep_downgraded
                        flows += kept * move[t, o, s] - move[t, s, o]
                prob += workforce[t, s] == flows - redundant[t, s], f"balance_{t}_{s}"

        # Retraining limits: a fixed number of places plus a share of the destination level's workforce
        for (a, b), row in ix["retraining"].items():
            for t in years:
                limit = row["max_per_year"]
                if row["max_share_of_target"]:
                    limit = limit + row["max_share_of_target"] * workforce[t, b]
                prob += move[t, a, b] <= limit, f"retraining_limit_{t}_{a}_{b}"

        # Overmanning allowance per year, all skill levels together
        for t in years:
            prob += pulp.lpSum(overmanned[t, s] for s in skills) <= P["max_overmanned"], f"overmanning_{t}"

        # Requirements: employed = required + overmanned + output lost to short-time working
        lost_per_short_time = 1 - P["short_time_productivity"]
        for t, s in cells:
            prob += workforce[t, s] == ix["required"].get((t, s), 0) + overmanned[t, s] \
                + lost_per_short_time * short_time[t, s], f"requirement_{t}_{s}"

        prob._wig = {"recruit": recruit, "retrain": retrain, "downgrade": downgrade, "redundant": redundant,
                     "short_time": short_time, "overmanned": overmanned, "workforce": workforce,
                     "same_level": same_level}  # same_level: inert columns, deliberately not a measure
        return prob

    def cost_expression(self, prob, data: dict[str, Any]):
        """Total cost of the plan in ``prob`` (built by :meth:`build` from ``data``) as a PuLP expression.

        This is the notebook's second objective ("minimise cost"): retraining cost per move plus redundancy,
        short-time and overmanning cost per worker. Set it as the objective to solve that variant. Like the
        built objective it gives the inert same-level columns a zero coefficient, so no column drops out.
        """
        import pulp

        expr = pulp.lpSum(cost * var for cost, var, _ in self._cost_terms(prob, self._index(data)))
        for var in prob._wig["same_level"].values():
            expr.addterm(var, 0)
        return expr

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        ix = self._index(data)
        years, skills = ix["years"], ix["skills"]
        v = prob._wig
        val = lambda x: x.value() or 0.0  # noqa: E731
        total = lambda name: sum(val(x) for x in v[name].values())  # noqa: E731
        parts = dict.fromkeys(self.COST_PARTS, 0.0)
        for cost, var, part in self._cost_terms(prob, ix):
            parts[part] += cost * val(var)
        return {
            "total_redundancy": round(total("redundant"), 2),
            "redundancy_by_year": {t: round(sum(val(v["redundant"][t, s]) for s in skills), 1) for t in years},
            "redundancy_by_skill": {s: round(sum(val(v["redundant"][t, s]) for t in years), 1) for s in skills},
            "total_cost": round(sum(parts.values()), 2),
            "cost_breakdown": {k: round(x, 2) for k, x in parts.items()},
            "recruited": round(total("recruit"), 1),
            "retrained": round(total("retrain"), 1),
            "downgraded": round(total("downgrade"), 1),
        }
