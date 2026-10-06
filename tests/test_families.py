"""Task families over every registered model: generation, filters, and the published task files."""
import json
from pathlib import Path

import pytest

from whatifgym.dsl import validate_scenario
from whatifgym.families import FAMILIES, DataChangeFamily, NewLimitFamily
from whatifgym.families.base import nice
from whatifgym.oracle import solve_scenario
from whatifgym.registry import get_model, list_models
from whatifgym.scoring import REL_TOL, compare_results
from whatifgym.tasks import load_tasks

ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "tasks"
# wedding_seating enumerates 3 213 candidate tables; a scenario solve takes seconds, so it is tested separately
FAST_MODELS = [m for m in list_models() if m != "wedding_seating"]


def test_registry_has_all_families():
    assert set(FAMILIES) == {"data_change", "new_limit", "relative_rule", "objective_change", "fixed_decision", "under_specified"}
    assert FAMILIES["data_change"] is DataChangeFamily and FAMILIES["new_limit"] is NewLimitFamily


def test_nice_rounding():
    assert nice(0) == 0
    assert nice(1234.4) == 1250 and nice(187.3) == 190 and nice(12.34) == 12 and nice(3.14159) == 3.1
    assert nice(0.123) == 0.12


# objective_change re-solves every candidate up to three times and the degenerate LPs/MILPs below need many
# candidates before one is accepted; they are covered by the task-file tests instead of a live generation here
SLOW_PAIRS = {("objective_change", m) for m in ("mining", "food_supply", "power_generation_hydro", "multiple_knapsack",
                                                "bin_packing", "manpower_planning", "car_rental_2")}
# bin packing's objective (bins used) is robust to almost everything; several families legitimately yield nothing
MAY_BE_EMPTY = {("bin_packing", f) for f in ("new_limit", "fixed_decision", "objective_change", "relative_rule")}


@pytest.mark.parametrize("model_name", FAST_MODELS)
@pytest.mark.parametrize("family_name", sorted(FAMILIES))
def test_generate_small_batch(model_name, family_name):
    if (family_name, model_name) in SLOW_PAIRS:
        pytest.skip("slow degenerate pair; covered by the task-file tests")
    fam = FAMILIES[family_name](model_name)
    tasks = fam.generate(3, seed=1, max_seconds=120)
    if (model_name, family_name) not in MAY_BE_EMPTY:
        assert tasks, f"{family_name} produced nothing on {model_name}: skipped={fam.skipped}"
    model = get_model(model_name)
    data = model.load_data()
    base = fam.base_result.to_dict()
    for t in tasks:
        assert t.family == family_name and t.model == model_name and t.split in ("train", "dev", "test")
        assert validate_scenario(t.scenario, model, data, raise_on_error=False) == []
        assert t.reference["status"] == "optimal"
        assert t.kpi_keys == model.SCORING_KPIS
        # the "no change" answer must not be accepted
        assert not compare_results(base, t.reference, t.kpi_keys, rel_tol=3 * REL_TOL).match
        assert t.question and t.question[0].isupper()
        if family_name == "under_specified":
            assert t.clarification and t.clarification["answer"].endswith(".") and "ask" in t.tags
        else:
            assert t.clarification is None
    assert len({t.id for t in tasks}) == len(tasks)


def test_generation_is_deterministic():
    fam = NewLimitFamily("factory_planning")
    a = [t.question for t in fam.generate(6, seed=3)]
    b = [t.question for t in fam.generate(6, seed=3)]
    assert a == b and len(a) == 6


def test_structural_columns_are_not_edited():
    fam = DataChangeFamily("manpower_planning")
    assert "level" not in fam.ctx.numeric_columns("skills")
    fam2 = DataChangeFamily("power_generation_hydro")
    assert "hours" not in fam2.ctx.numeric_columns("periods")
    assert "units_on_at_start" not in fam2.ctx.numeric_columns("thermal_types")


def test_rows_are_only_added_or_removed_on_entity_tables():
    assert DataChangeFamily("factory_planning").ctx.removable_tables() == []      # every table is referenced or ordered
    assert set(DataChangeFamily("bin_packing").ctx.removable_tables()) == {"items", "bins"}
    assert DataChangeFamily("mining").ctx.removable_tables() == ["mines"]
    # hydro_units has only two rows, below the three-row minimum for add/remove templates
    assert DataChangeFamily("power_generation_hydro").ctx.removable_tables() == ["thermal_types"]
    assert DataChangeFamily("manpower_planning").ctx.removable_tables() == []    # costs/requirements are keyed by skill
    assert DataChangeFamily("car_rental").ctx.removable_tables() == []


def test_build_errors_skip_the_candidate_instead_of_aborting():
    fam = DataChangeFamily("manpower_planning")
    # a scenario that the model rejects in build(): two skill levels with the same ordinal
    bad = {"version": "0.1", "data_changes": [{"op": "set", "table": "skills", "column": "level", "value": 1}]}
    assert fam._solve(bad, "highs") is None
    assert any(k.startswith("error:") for k in fam.skipped)


def test_combo_share_is_capped():
    fam = DataChangeFamily("bin_packing")
    tasks = fam.generate(20, seed=0)
    assert sum(t.template == "combo" for t in tasks) <= 6


# ------------------------------------------------------------------ the published task files
def _task_files():
    return sorted(p for p in TASK_DIR.glob("*/*_v0.jsonl"))


def test_task_files_cover_every_model_and_every_family():
    files = _task_files()
    models_with_files = {p.parent.name for p in files}
    assert models_with_files == set(list_models())
    total = sum(1 for p in files for line in open(p, encoding="utf-8") if line.strip())
    assert total >= 200
    families = {p.stem.rsplit("_v0", 1)[0] for p in files}
    assert families == set(FAMILIES)


def test_under_specified_tasks_need_the_ask_route():
    from whatifgym.env import WhatIfEnv

    path = TASK_DIR / "factory_planning" / "under_specified_v0.jsonl"
    tasks = load_tasks(path)[:3]
    env = WhatIfEnv(tasks)
    for t in tasks:
        env.reset(t)
        _, reward, done, info = env.step({"type": "scenario", "scenario": t.scenario})   # right answer, wrong route
        assert done and reward == 0.0 and info["score"]["notes"] == "needed clarification not asked"
        env.reset(t)
        obs, reward, done, info = env.step({"type": "ask", "text": "Which one, and by how much?"})
        assert not done and info["answer"] == t.clarification["answer"] and obs["dialogue"][-1]["text"] == t.clarification["answer"]
        _, reward, done, info = env.step({"type": "scenario", "scenario": t.scenario})
        assert done and reward == 1.1 and info["score"]["route_correct"]


def test_lexicographic_original_objective_in_a_later_stage():
    """`original` in stage two must mean the model's own objective, not the stage-one expression."""
    model = get_model("factory_planning")
    ref = solve_scenario(model, {"version": "0.1", "objective": [{"sense": "min", "measure": "make"},
                                                                 {"sense": "max", "measure": "original"}]})
    assert ref.status == "optimal" and len(ref.stage_values) == 2
    assert abs(ref.stage_values[0] - 350.0) < 1e-6                     # 7 products x 50 units of closing stock
    assert abs(ref.stage_values[1] - ref.kpis["profit"]) < 0.01        # stage two really optimised profit
    for s in ("scip", "cbc"):
        other = solve_scenario(model, {"version": "0.1", "objective": [{"sense": "min", "measure": "make"},
                                                                       {"sense": "max", "measure": "original"}]}, solver=s)
        assert compare_results(ref.to_dict(), other.to_dict(), model.SCORING_KPIS).match


@pytest.mark.parametrize("path", _task_files(), ids=lambda p: f"{p.parent.name}/{p.name}")
def test_task_file_is_consistent(path):
    tasks = load_tasks(path)
    assert tasks
    model = get_model(path.parent.name)
    data = model.load_data()
    assert len({t.id for t in tasks}) == len(tasks)
    for t in tasks:
        assert t.model == model.name and t.family == path.stem.rsplit("_v0", 1)[0]
        assert t.kpi_keys == model.SCORING_KPIS
        assert t.reference["status"] in ("optimal", "infeasible")
        assert validate_scenario(t.scenario, model, data, raise_on_error=False) == []
        json.dumps(t.to_dict())  # serialisable
    # the reference is reproduced by the oracle today (first two tasks keep slow models cheap)
    for t in tasks[:2]:
        ref = solve_scenario(model, t.scenario, data, solver="highs", keep_decisions=False)
        assert compare_results(t.reference, ref.to_dict(), t.kpi_keys).match
