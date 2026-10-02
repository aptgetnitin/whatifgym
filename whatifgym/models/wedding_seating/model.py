"""Wedding seating — a set-partitioning model (IP / CP-SAT).

Clean-room re-implementation of the PuLP case study "A Set Partitioning Problem" (``examples/wedding.py``,
MIT, Stuart Mitchell 2009). Every feasible table (any subset of guests up to ``max_table_size``) is a
column; choose at most ``max_tables`` of them so that every guest sits at exactly one table and total
"unhappiness" is minimal. Unhappiness of a table = rank spread between its first and last guest, exactly as
in the original (which used letter codes), so the reference optimum of 12 is reproduced.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class WeddingSeating(BaseModel):
    name = "wedding_seating"
    title = "Wedding seating as set partitioning (PuLP case study)"
    domain = "packing_assignment_covering"
    sense = "min"
    problem_type = "IP"
    source = Source(
        repo="coin-or/pulp",
        path="examples/wedding.py",
        url="https://github.com/coin-or/pulp/blob/master/examples/wedding.py",
        license="MIT",
        notes="Documented in doc/source/CaseStudies/a_set_partitioning_problem.rst; model re-implemented.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("guests",)
    MEASURE_DIMS = {"x": ("table",)}

    def measures(self, prob):
        from ...base import Measure

        x = prob._wig["x"]
        return {"x": Measure("x", ("table",), {("".join(t),): var for t, var in x.items()})}

    # ----------------------------------------------------------------- helpers
    @staticmethod
    def _tables(data: dict[str, Any]):
        guests = [r["guest"] for r in data["guests"]]
        rank = {r["guest"]: r["rank"] for r in data["guests"]}
        max_size = int(data["params"]["max_table_size"])
        tables = [c for size in range(1, max_size + 1) for c in combinations(guests, size)]
        unhappiness = {t: abs(rank[t[-1]] - rank[t[0]]) for t in tables}
        return guests, tables, unhappiness

    # ------------------------------------------------------------------- model
    def build(self, data: dict[str, Any]):
        import pulp

        guests, tables, unhappiness = self._tables(data)
        prob = pulp.LpProblem("wedding_seating", pulp.LpMinimize)
        x = {t: pulp.LpVariable("table_" + "_".join(t), cat=pulp.LpBinary) for t in tables}

        prob += pulp.lpSum(unhappiness[t] * x[t] for t in tables), "total_unhappiness"
        prob += pulp.lpSum(x[t] for t in tables) <= int(data["params"]["max_tables"]), "max_tables"
        for g in guests:
            prob += pulp.lpSum(x[t] for t in tables if g in t) == 1, f"seat_{g}"

        prob._wig = {"x": x, "unhappiness": unhappiness}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        x, unhappiness = prob._wig["x"], prob._wig["unhappiness"]
        chosen = [t for t, var in x.items() if (var.value() or 0) > 0.5]
        return self._kpis_from_tables(chosen, unhappiness)

    # ------------------------------------------------------------------ CP-SAT
    def build_cpsat(self, data: dict[str, Any]):
        from ortools.sat.python import cp_model

        guests, tables, unhappiness = self._tables(data)
        model = cp_model.CpModel()
        x = {t: model.new_bool_var("table_" + "_".join(t)) for t in tables}
        model.add(sum(x.values()) <= int(data["params"]["max_tables"]))
        for g in guests:
            model.add_exactly_one(x[t] for t in tables if g in t)
        model.minimize(sum(int(unhappiness[t]) * x[t] for t in tables))
        return model, {"x": x, "unhappiness": unhappiness}

    def kpis_cpsat(self, solver, variables, data: dict[str, Any]) -> dict[str, Any]:
        chosen = [t for t, var in variables["x"].items() if solver.value(var) > 0.5]
        return self._kpis_from_tables(chosen, variables["unhappiness"])

    @staticmethod
    def _kpis_from_tables(chosen, unhappiness) -> dict[str, Any]:
        return {
            "total_unhappiness": sum(unhappiness[t] for t in chosen),
            "tables_used": len(chosen),
            "largest_table": max((len(t) for t in chosen), default=0),
            "worst_table_unhappiness": max((unhappiness[t] for t in chosen), default=0),
            "tables": ["".join(t) for t in sorted(chosen)],
        }
