"""Fantasy basketball — pick a line-up that maximises predicted fantasy points under a salary cap (IP).

Clean-room re-implementation of the optimisation part of the Gurobi modeling-examples notebook
``fantasy_basketball/fantasy_basketball_part1.ipynb`` (Apache-2.0). Only published data values are reused: the
96 players, positions and salaries of ``target_games.csv``, the predicted fantasy points the notebook's regression
produces (published in ``results_target_advanced.csv``), the 30,000 salary cap and one player per position.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class FantasyBasketball(BaseModel):
    name = "fantasy_basketball"
    title = "Fantasy basketball line-up under a salary cap (Gurobi modeling-examples)"
    domain = "revenue_resource_planning"
    sense = "max"
    problem_type = "IP"
    source = Source(
        repo="Gurobi/modeling-examples",
        path="fantasy_basketball/fantasy_basketball_part1.ipynb",
        url="https://github.com/Gurobi/modeling-examples/blob/master/fantasy_basketball/fantasy_basketball_part1.ipynb",
        license="Apache-2.0",
        notes="Data values from the notebook's CSVs (predicted points frozen, ML step not reproduced); model re-implemented in PuLP.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("players", "positions")
    HAS_PARAMS = True
    MEASURE_DIMS = {"pick": ("player",)}
    SCORING_KPIS = ["total_predicted_points", "total_salary", "salary_cap_left", "players_selected"]

    @staticmethod
    def _index(data: dict[str, Any]):
        players = [r["player"] for r in data["players"]]
        pos = {r["player"]: r["position"] for r in data["players"]}
        salary = {r["player"]: r["salary"] for r in data["players"]}
        points = {r["player"]: r["predicted_points"] for r in data["players"]}
        required = {r["position"]: r["required"] for r in data["positions"]}
        return players, pos, salary, points, required

    def build(self, data: dict[str, Any]):
        import pulp

        players, pos, salary, points, required = self._index(data)
        tag = {p: re.sub(r"\W", "_", p) for p in players}
        prob = pulp.LpProblem("fantasy_basketball", pulp.LpMaximize)
        pick = {p: pulp.LpVariable(f"pick_{tag[p]}", cat=pulp.LpBinary) for p in players}

        prob += pulp.lpSum(points[p] * pick[p] for p in players), "predicted_points"
        # Like the original, one position row per player (rows of players sharing a position are duplicates),
        # which keeps its 97 rows. shortcut: a position left with no players gets no row, so its requirement is dropped.
        for p in players:
            prob += (pulp.lpSum(pick[q] for q in players if pos[q] == pos[p]) == required.get(pos[p], 0),
                     f"position_{tag[p]}")
        prob += pulp.lpSum(salary[p] * pick[p] for p in players) <= data["params"]["salary_cap"], "salary_cap"

        prob._wig = {"pick": pick}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        players, pos, salary, points, required = self._index(data)
        chosen = [p for p, v in prob._wig["pick"].items() if (v.value() or 0) > 0.5]
        total_salary = sum(salary[p] for p in chosen)
        total_points = sum(points[p] for p in chosen)
        return {
            "total_predicted_points": round(total_points, 4),
            "total_salary": total_salary,
            "salary_cap_left": data["params"]["salary_cap"] - total_salary,
            "players_selected": len(chosen),
            "points_per_1000_salary": round(1000 * total_points / total_salary, 4) if total_salary else None,
            "lineup": {k: [p for p in chosen if pos[p] == k] for k in required},
        }
