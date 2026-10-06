"""Compare two scenario results and turn the comparison into a reward.

Rules (from the paper plan):
* reward 1.0 when status matches (optimal or infeasible) and, for optimal, the objective and the task family's
  KPIs match the reference within relative tolerance 1e-3; for infeasible, the conflict (the base-model
  constraints the scenario clashes with) must match too; otherwise 0;
* a syntactically and semantically valid scenario adds 0.1 even when wrong;
* an unnecessary clarifying question costs 0.2; a needed question that was not asked scores 0;
* route correctness (ask vs. answer) is reported separately, never folded into the number silently.

Two equivalent scenarios spelled differently produce the same solve, so they earn the same reward — the
scorer looks only at results, never at the scenario text.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

REL_TOL = 1e-3
ABS_TOL = 1e-6
VALID_DSL_BONUS = 0.1
UNNEEDED_ASK_PENALTY = 0.2


def close(a: Any, b: Any, rel: float = REL_TOL, abs_tol: float = ABS_TOL) -> bool:
    if a is None or b is None:
        return a is b
    if isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str):
        return a == b
    try:
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=abs_tol)
    except (TypeError, ValueError):
        return a == b


def _flatten(d: Any, prefix: str = "") -> dict[str, Any]:
    """Flatten nested KPI dicts to dotted paths; lists are compared as sorted tuples of strings."""
    out: dict[str, Any] = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(_flatten(v, f"{prefix}{k}."))
    elif isinstance(d, list):
        out[prefix.rstrip(".")] = tuple(sorted(map(str, d)))
    else:
        out[prefix.rstrip(".")] = d
    return out


@dataclass
class Comparison:
    status_match: bool
    objective_match: bool
    kpi_mismatches: dict[str, tuple[Any, Any]] = field(default_factory=dict)
    kpi_checked: int = 0
    rel_tol: float = REL_TOL

    @property
    def match(self) -> bool:
        return self.status_match and self.objective_match and not self.kpi_mismatches


def compare_results(reference: dict[str, Any], candidate: dict[str, Any],
                    kpi_keys: list[str] | None = None, rel_tol: float = REL_TOL) -> Comparison:
    """``reference`` / ``candidate`` are ScenarioResult dicts. ``kpi_keys`` = the family's KPIs (None = all)."""
    status_match = reference["status"] == candidate["status"]
    if reference["status"] != "optimal":
        # an infeasible reference with a known conflict must be infeasible for the same reason: the same base-model
        # constraints (else any absurd impossible scenario would score)
        mismatches = {}
        if status_match and reference.get("conflict") and candidate.get("conflict") != reference["conflict"]:
            mismatches["conflict"] = (reference["conflict"], candidate.get("conflict"))
        return Comparison(status_match=status_match, objective_match=status_match, kpi_mismatches=mismatches,
                          kpi_checked=1 if reference.get("conflict") else 0, rel_tol=rel_tol)
    objective_match = status_match and close(reference.get("objective"), candidate.get("objective"), rel_tol)
    ref_k, cand_k = _flatten(reference.get("kpis", {})), _flatten(candidate.get("kpis", {}))
    keys = [k for k in ref_k if kpi_keys is None or any(k == kk or k.startswith(kk + ".") for kk in kpi_keys)]
    mismatches = {k: (ref_k[k], cand_k.get(k)) for k in keys if not close(ref_k[k], cand_k.get(k), rel_tol)}
    return Comparison(status_match=status_match, objective_match=objective_match,
                      kpi_mismatches=mismatches, kpi_checked=len(keys), rel_tol=rel_tol)


@dataclass
class Score:
    reward: float
    correct: bool
    valid_dsl: bool
    asked: bool
    ask_needed: bool
    route_correct: bool
    comparison: Comparison | None = None
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = {"reward": self.reward, "correct": self.correct, "valid_dsl": self.valid_dsl, "asked": self.asked,
             "ask_needed": self.ask_needed, "route_correct": self.route_correct, "notes": self.notes}
        if self.comparison is not None:
            d["comparison"] = {"status_match": self.comparison.status_match,
                               "objective_match": self.comparison.objective_match,
                               "kpi_checked": self.comparison.kpi_checked,
                               "kpi_mismatches": {k: list(v) for k, v in self.comparison.kpi_mismatches.items()}}
        return d


def score_episode(reference: dict[str, Any], candidate: dict[str, Any] | None, *, valid_dsl: bool,
                  asked: bool, ask_needed: bool, kpi_keys: list[str] | None = None) -> Score:
    """Score one finished episode.

    ``candidate`` is the oracle's result for the agent's final scenario (None when the agent never submitted one
    or its scenario was invalid). ``asked`` = the agent used its clarifying question; ``ask_needed`` = the task
    was under-specified and required one.
    """
    comparison = compare_results(reference, candidate, kpi_keys) if candidate is not None else None
    correct = bool(comparison and comparison.match)
    if ask_needed and not asked:
        return Score(reward=0.0, correct=False, valid_dsl=valid_dsl, asked=asked, ask_needed=ask_needed,
                     route_correct=False, comparison=comparison, notes="needed clarification not asked")
    reward = (1.0 if correct else 0.0) + (VALID_DSL_BONUS if valid_dsl else 0.0)
    if asked and not ask_needed:
        reward -= UNNEEDED_ASK_PENALTY
    reward = max(0.0, round(reward, 6))
    route_correct = asked == ask_needed
    notes = "" if correct else ("invalid scenario" if not valid_dsl else "result differs from reference")
    return Score(reward=reward, correct=correct, valid_dsl=valid_dsl, asked=asked, ask_needed=ask_needed,
                 route_correct=route_correct, comparison=comparison, notes=notes)
