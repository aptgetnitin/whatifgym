"""The two probe agents: nearest_example never copies the task itself; random_valid is valid and reproducible."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_baseline import agent_nearest_example, agent_random_valid  # noqa: E402
from whatifgym import get_model  # noqa: E402
from whatifgym.dsl import validate_scenario  # noqa: E402
from whatifgym.tasks import load_tasks  # noqa: E402

TASKS = load_tasks(ROOT / "tasks" / "factory_planning" / "data_change_v0.jsonl")


def test_nearest_example_never_copies_the_task_itself():
    for task in [t for t in TASKS if t.split == "train"][:10]:
        action = agent_nearest_example({}, task, {})
        assert action["scenario"] != task.scenario


def test_random_valid_is_valid_and_reproducible():
    model = get_model("factory_planning")
    data = model.load_data()
    for task in TASKS[:10]:
        a, b = agent_random_valid({}, task, {}), agent_random_valid({}, task, {})
        assert a == b
        assert validate_scenario(a["scenario"], model, data, raise_on_error=False) == []
