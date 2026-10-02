"""Multiple knapsack — pack items into capacity-limited bins to maximise packed value (MILP / CP-SAT).

Clean-room re-implementation of the public OR-Tools samples ``multiple_knapsack_mip.py`` and
``multiple_knapsack_sat.py`` (Apache-2.0). Only the published data values are reused.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class MultipleKnapsack(BaseModel):
    name = "multiple_knapsack"
    title = "Multiple knapsack (OR-Tools sample)"
    domain = "packing_assignment_covering"
    sense = "max"
    problem_type = "IP"
    source = Source(
        repo="google/or-tools",
        path="ortools/sat/samples/multiple_knapsack_sat.py",
        url="https://github.com/google/or-tools/blob/stable/ortools/sat/samples/multiple_knapsack_sat.py",
        license="Apache-2.0",
        notes="Same data as ortools/linear_solver/samples/multiple_knapsack_mip.py; model re-implemented.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("items", "bins")
    HAS_PARAMS = False
    MEASURE_DIMS = {"x": ("item", "bin")}

    @staticmethod
    def _index(data: dict[str, Any]):
        items = [r["item"] for r in data["items"]]
        weight = {r["item"]: r["weight"] for r in data["items"]}
        value = {r["item"]: r["value"] for r in data["items"]}
        bins = [r["bin"] for r in data["bins"]]
        capacity = {r["bin"]: r["capacity"] for r in data["bins"]}
        return items, weight, value, bins, capacity

    # ------------------------------------------------------------ PuLP (MILP)
    def build(self, data: dict[str, Any]):
        import pulp

        items, weight, value, bins, capacity = self._index(data)
        prob = pulp.LpProblem("multiple_knapsack", pulp.LpMaximize)
        x = {(i, b): pulp.LpVariable(f"x_{i}_{b}", cat=pulp.LpBinary) for i in items for b in bins}

        prob += pulp.lpSum(value[i] * x[i, b] for i in items for b in bins), "packed_value"
        for i in items:
            prob += pulp.lpSum(x[i, b] for b in bins) <= 1, f"assign_once_{i}"
        for b in bins:
            prob += pulp.lpSum(weight[i] * x[i, b] for i in items) <= capacity[b], f"capacity_{b}"

        prob._wig = {"x": x}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        items, weight, value, bins, capacity = self._index(data)
        x = prob._wig["x"]
        chosen = {(i, b) for (i, b), var in x.items() if (var.value() or 0) > 0.5}
        return self._kpis_from_assignment(chosen, items, weight, value, bins, capacity)

    # ------------------------------------------------------------- CP-SAT
    def build_cpsat(self, data: dict[str, Any]):
        from ortools.sat.python import cp_model

        items, weight, value, bins, capacity = self._index(data)
        for name, table in (("weight", weight), ("value", value), ("capacity", capacity)):
            if any(int(v) != v for v in table.values()):
                raise ValueError(f"CP-SAT needs integer {name}s")
        model = cp_model.CpModel()
        x = {(i, b): model.new_bool_var(f"x_{i}_{b}") for i in items for b in bins}
        for i in items:
            model.add_at_most_one(x[i, b] for b in bins)
        for b in bins:
            model.add(sum(int(weight[i]) * x[i, b] for i in items) <= int(capacity[b]))
        model.maximize(sum(int(value[i]) * x[i, b] for i in items for b in bins))
        return model, {"x": x}

    def kpis_cpsat(self, solver, variables, data: dict[str, Any]) -> dict[str, Any]:
        items, weight, value, bins, capacity = self._index(data)
        chosen = {(i, b) for (i, b), var in variables["x"].items() if solver.value(var) > 0.5}
        return self._kpis_from_assignment(chosen, items, weight, value, bins, capacity)

    # ------------------------------------------------------------- shared
    @staticmethod
    def _kpis_from_assignment(chosen, items, weight, value, bins, capacity) -> dict[str, Any]:
        packed_value = sum(value[i] for i, _ in chosen)
        packed_weight = sum(weight[i] for i, _ in chosen)
        per_bin = {b: sum(weight[i] for i, bb in chosen if bb == b) for b in bins}
        return {
            "packed_value": packed_value,
            "packed_weight": packed_weight,
            "items_packed": len(chosen),
            "items_left_out": len(items) - len(chosen),
            "value_left_out": sum(value.values()) - packed_value,
            "bin_utilisation": {b: round(per_bin[b] / capacity[b], 4) if capacity[b] else None for b in bins},
            "bins_used": sum(1 for b in bins if per_bin[b] > 0),
        }
