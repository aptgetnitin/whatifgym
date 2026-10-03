"""Bin packing — put every item into a bin, using as few bins as possible (IP / CP-SAT).

Clean-room re-implementation of the public OR-Tools sample ``ortools/linear_solver/samples/bin_packing_mip.py``
(Apache-2.0). Only the published data values are reused (eleven item weights, bin capacity 100, one candidate
bin per item); the code here is new. The sample's single capacity is stored per bin in ``bins.csv`` so that a
what-if can resize one bin; with the shipped data (every bin 100) the model is exactly the original.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ...base import BaseModel, Source


class BinPacking(BaseModel):
    name = "bin_packing"
    title = "Bin packing (OR-Tools sample)"
    domain = "packing_assignment_covering"
    sense = "min"
    problem_type = "IP"
    source = Source(
        repo="google/or-tools",
        path="ortools/linear_solver/samples/bin_packing_mip.py",
        url="https://github.com/google/or-tools/blob/stable/ortools/linear_solver/samples/bin_packing_mip.py",
        license="Apache-2.0",
        notes="Data values from the sample (weights, capacity 100, one candidate bin per item); model re-implemented.",
    )
    DATA_DIR = Path(__file__).parent / "data"
    TABLES = ("items", "bins")
    HAS_PARAMS = False
    MEASURE_DIMS = {"x": ("item", "bin"), "y": ("bin",)}
    SCORING_KPIS = ["bins_used", "total_weight", "min_bins_by_weight"]  # KPIs that are unique at the optimum; the scorer compares these

    @staticmethod
    def _index(data: dict[str, Any]):
        items = [r["item"] for r in data["items"]]
        weight = {r["item"]: r["weight"] for r in data["items"]}
        bins = [r["bin"] for r in data["bins"]]
        capacity = {r["bin"]: r["capacity"] for r in data["bins"]}
        return items, weight, bins, capacity

    # ------------------------------------------------------------ PuLP (IP)
    def build(self, data: dict[str, Any]):
        import pulp

        items, weight, bins, capacity = self._index(data)
        prob = pulp.LpProblem("bin_packing", pulp.LpMinimize)
        x = {(i, b): pulp.LpVariable(f"x_{i}_{b}", cat=pulp.LpBinary) for i in items for b in bins}
        y = {b: pulp.LpVariable(f"y_{b}", cat=pulp.LpBinary) for b in bins}

        prob += pulp.lpSum(y[b] for b in bins), "bins_used"
        for i in items:  # every item is packed into exactly one bin
            prob += pulp.lpSum(x[i, b] for b in bins) == 1, f"assign_{i}"
        for b in bins:   # a bin holds at most its capacity, and nothing unless it is used
            prob += pulp.lpSum(weight[i] * x[i, b] for i in items) <= capacity[b] * y[b], f"capacity_{b}"

        prob._wig = {"x": x, "y": y}
        return prob

    def kpis(self, prob, data: dict[str, Any]) -> dict[str, Any]:
        items, weight, bins, capacity = self._index(data)
        x, y = prob._wig["x"], prob._wig["y"]
        placed = {i: b for (i, b), var in x.items() if (var.value() or 0) > 0.5}
        opened = [b for b in bins if (y[b].value() or 0) > 0.5]
        return self._kpis_from_solution(placed, opened, items, weight, bins, capacity)

    # ------------------------------------------------------------- CP-SAT
    def build_cpsat(self, data: dict[str, Any]):
        from ortools.sat.python import cp_model

        items, weight, bins, capacity = self._index(data)
        # CP-SAT is integer-only. Every capacity row reads weight * x <= capacity * y, so multiplying all weights
        # and capacities by one power of ten (needed only after a fractional what-if edit) changes nothing.
        f = self._integer_scale(list(weight.values()) + list(capacity.values()))
        w = {i: int(round(weight[i] * f)) for i in items}
        cap = {b: int(round(capacity[b] * f)) for b in bins}

        model = cp_model.CpModel()
        x = {(i, b): model.new_bool_var(f"x_{i}_{b}") for i in items for b in bins}
        y = {b: model.new_bool_var(f"y_{b}") for b in bins}
        for i in items:
            model.add_exactly_one(x[i, b] for b in bins)
        for b in bins:
            model.add(sum(w[i] * x[i, b] for i in items) <= cap[b] * y[b])
        model.minimize(sum(y[b] for b in bins))
        return model, {"x": x, "y": y}

    def kpis_cpsat(self, solver, variables, data: dict[str, Any]) -> dict[str, Any]:
        items, weight, bins, capacity = self._index(data)
        placed = {i: b for (i, b), var in variables["x"].items() if solver.value(var) > 0.5}
        opened = [b for b in bins if solver.value(variables["y"][b]) > 0.5]
        return self._kpis_from_solution(placed, opened, items, weight, bins, capacity)

    # ------------------------------------------------------------- shared
    @staticmethod
    def _integer_scale(values: list[float]) -> int:
        """Smallest power of ten (up to 10**6) that turns every value into an integer, within 1e-9."""
        for k in range(7):
            f = 10 ** k
            if all(abs(v * f - round(v * f)) <= 1e-9 * max(1.0, abs(v * f)) for v in values):
                return f
        raise ValueError("CP-SAT needs weights and capacities with at most six decimals")

    @staticmethod
    def _kpis_from_solution(placed, opened, items, weight, bins, capacity) -> dict[str, Any]:
        load = {b: 0 for b in bins}
        contents: dict[Any, list] = {b: [] for b in bins}
        for i in items:
            if i in placed:
                load[placed[i]] += weight[i]
                contents[placed[i]].append(i)
        shown = [b for b in bins if b in opened or contents[b]]
        packed = sum(weight[i] for i in placed)
        open_capacity = sum(capacity[b] for b in opened)
        # fewest bins whose combined capacity covers the total weight: a lower bound on bins_used
        min_bins, covered = 0, 0
        for c in sorted(capacity.values(), reverse=True):
            if covered >= packed - 1e-9:
                break
            covered += c
            min_bins += 1
        return {
            "bins_used": len(opened),
            "total_weight": round(packed, 4),
            "open_capacity": round(open_capacity, 4),
            "spare_capacity": round(open_capacity - packed, 4),
            "fill_rate": round(packed / open_capacity, 4) if open_capacity else None,
            "min_bins_by_weight": min_bins,
            "bin_load": {b: round(load[b], 4) for b in shown},
            "bin_items": {b: contents[b] for b in shown},
        }
