"""Environment loop and the data-change task family."""
import json
from pathlib import Path

from whatifgym.env import WhatIfEnv
from whatifgym.families import DataChangeFamily
from whatifgym.tasks import Task, load_tasks

TASK_FILE = Path(__file__).resolve().parents[1] / "tasks" / "factory_planning" / "data_change_v0.jsonl"


def test_task_file_exists_and_is_consistent():
    tasks = load_tasks(TASK_FILE)
    assert len(tasks) == 60
    assert {t.split for t in tasks} <= {"train", "dev", "test"} and len({t.id for t in tasks}) == 60
    assert all(t.reference["status"] in ("optimal", "infeasible") for t in tasks)
    assert all(t.kpi_keys == ["profit", "holding_cost", "sales_contribution"] for t in tasks)


def test_generation_is_deterministic_and_no_task_is_a_noop():
    fam = DataChangeFamily("factory_planning")
    a = fam.generate(12, seed=7)
    b = fam.generate(12, seed=7)
    assert [t.question for t in a] == [t.question for t in b]
    base = fam.base_result.objective
    assert all(abs(t.reference["objective"] - base) > 1e-3 * base for t in a if t.reference["status"] == "optimal")


def test_env_oracle_scores_full_reward_and_observation_hides_raw_values():
    tasks = load_tasks(TASK_FILE)[:5]
    env = WhatIfEnv(tasks)
    for task in tasks:
        obs = env.reset(task)
        assert "index_sets" in obs and "max_sales" not in json.dumps(obs["index_sets"])
        assert {"month": "Jan", "machine": "grinder"} in obs["table_keys"]["downtime"]
        assert all(set(r) == {"month", "machine"} for r in obs["table_keys"]["downtime"])  # keys only, no values
        assert len(obs["examples"]) == 2 and obs["question"] == task.question
        _, reward, done, info = env.step({"type": "scenario", "scenario": task.scenario})
        assert done and reward == 1.1 and info["score"]["correct"]


def test_env_invalid_scenario_and_unneeded_ask():
    task = load_tasks(TASK_FILE)[0]
    env = WhatIfEnv([task])
    env.reset(task)
    _, reward, done, info = env.step({"type": "scenario", "scenario": {"version": "0.1", "rules": [{"measure": "ghost", "sense": "<=", "value": 1}]}})
    assert done and reward == 0.0 and info["validation_errors"]
    env.reset(task)
    obs, reward, done, info = env.step({"type": "ask", "text": "Which month?"})
    assert not done and reward == 0.0 and obs["dialogue"][-1]["role"] == "planner"
    _, reward, done, info = env.step({"type": "scenario", "scenario": task.scenario})
    assert done and reward == 0.9 and info["score"]["correct"] and not info["score"]["route_correct"]


def test_env_under_specified_task_requires_ask():
    base = load_tasks(TASK_FILE)[0]
    vague = Task(**{**base.to_dict(), "id": "vague-1", "question": "What if demand rises?",
                    "clarification": {"answer": "Prod5, 20% higher, in May and June."}})
    env = WhatIfEnv([vague])
    env.reset(vague)
    _, reward, done, info = env.step({"type": "scenario", "scenario": base.scenario})
    assert done and reward == 0.0 and info["score"]["notes"] == "needed clarification not asked"
    env.reset(vague)
    obs, _, _, info = env.step({"ask": "Which product, how much and when?", "version": "0.1"})
    assert info["answer"].startswith("Prod5")
    _, reward, done, _ = env.step(base.scenario)
    assert done and reward == 1.1


def test_env_non_numeric_param_is_invalid_not_a_crash():
    """qwen3:4b once set a numeric parameter to a word; that must score 0, not abort the run."""
    task = load_tasks("tasks/battery_scheduling/under_specified_v0.jsonl")[0]
    env = WhatIfEnv([task])
    env.reset(task)
    bad = {"version": "0.1", "base_model": "battery_scheduling",
           "data_changes": [{"op": "set_param", "name": "energy_capacity_kwh", "value": "upper_limit"}]}
    _, reward, done, info = env.step({"type": "scenario", "scenario": bad})
    assert done and reward == 0.0 and info["validation_errors"][0]["path"] == "/data_changes/0/value"


def test_env_ask_wrapped_as_scenario_is_a_question():
    """LLM agents return every parsed reply as a scenario; an ask-only reply must still open the dialogue."""
    vague = load_tasks("tasks/factory_planning/under_specified_v0.jsonl")[0]
    env = WhatIfEnv([vague])
    env.reset(vague)
    obs, reward, done, info = env.step({"type": "scenario", "scenario": {"version": "0.1", "ask": "By how much?"}})
    assert not done and info["action"] == "ask" and obs["dialogue"][-1]["role"] == "planner"
    _, reward, done, info = env.step({"type": "scenario", "scenario": vague.scenario})
    assert done and reward == 1.1 and info["score"]["route_correct"]


def test_infeasible_request_needs_the_same_conflict():
    """An impossible scenario that clashes with other constraints is valid but wrong (0.1), not correct."""
    from whatifgym.families import FAMILIES

    task = FAMILIES["infeasible_request"]("factory_planning").generate(1, seed=0)[0]
    env = WhatIfEnv([task])
    env.reset(task)
    _, reward, done, info = env.step({"type": "scenario", "scenario": task.scenario})
    assert done and reward == 1.1
    other = {"version": "0.1", "rules": [{"measure": "store", "scope": {"month": "Jan"}, "sense": ">=", "value": 10 ** 7}]}
    env.reset(task)
    _, reward, done, info = env.step({"type": "scenario", "scenario": other})
    assert done and reward == 0.1 and "conflict" in info["score"]["comparison"]["kpi_mismatches"]


def test_chained_task_shows_its_history_and_needs_it():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from run_baseline import build_prompt
    from whatifgym.families import FAMILIES

    tasks = FAMILIES["chained_scenario"]("factory_planning").generate(4, seed=0)
    task = tasks[0]
    env = WhatIfEnv([task])
    obs = env.reset(task)
    assert obs["history"] and "Earlier questions" in build_prompt(obs)
    _, reward, done, _ = env.step({"type": "scenario", "scenario": task.history[0]["scenario"]})
    assert done and reward == 0.1          # the earlier change alone is not the answer
    env.reset(task)
    _, reward, done, _ = env.step({"type": "scenario", "scenario": task.scenario})
    assert done and reward == 1.1
