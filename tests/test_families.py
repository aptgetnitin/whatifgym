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


def test_registry_has_both_families():
    assert set(FAMILIES) == {"data_change", "new_limit"}
    assert FAMILIES["data_change"] is DataChangeFamily and FAMILIES["new_limit"] is NewLimitFamily


def test_nice_rounding():
    assert nice(0) == 0
    assert nice(1234.4) == 1250 and nice(187.3) == 190 and nice(12.34) == 12 and nice(3.14159) == 3.1
    assert nice(0.123) == 0.12


@pytest.mark.parametrize("model_name", FAST_MODELS)
@pytest.mark.parametrize("family_name", sorted(FAMILIES))
def test_generate_small_batch(model_name, family_name):
    fam = FAMILIES[family_name](model_name)
    tasks = fam.generate(3, seed=1, max_seconds=120)
    if model_name == "bin_packing" and family_name == "new_limit":
        pass  # the bins-used objective rarely moves under a single rule; a short batch may legitimately be empty
    else:
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


def test_task_files_cover_every_model_and_both_families():
    files = _task_files()
    models_with_files = {p.parent.name for p in files}
    assert models_with_files == set(list_models())
    total = sum(1 for p in files for line in open(p, encoding="utf-8") if line.strip())
    assert total >= 200
    families = {p.stem.rsplit("_v0", 1)[0] for p in files}
    assert families == {"data_change", "new_limit"}


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
