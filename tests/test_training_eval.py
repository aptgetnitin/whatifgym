"""The GPU-free parts of training/grpo_pilot.py: the fixed evaluation draw, evaluate() and pass_rates()."""
import json
import multiprocessing
import sys
import types
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "training"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.modules.setdefault("vllm", types.SimpleNamespace(SamplingParams=lambda **k: k))  # stand-in: no GPU here

import grpo_pilot as g  # noqa: E402
from whatifgym.tasks import load_tasks  # noqa: E402


class Tok:  # one token per four characters: enough for the length filter
    def apply_chat_template(self, m, tokenize=True, add_generation_prompt=True):
        s = "".join(x["content"] for x in m)
        return list(s[: len(s) // 4]) if tokenize else s


class Model:
    """Answers the gold scenario for every other task, junk otherwise; n answers per prompt."""
    def __init__(self, gold, rows):
        self.answers = {r["task_id"]: json.dumps(gold[r["task_id"]]) if i % 2 == 0 else "not json"
                        for i, r in enumerate(rows)}

    def fast_generate(self, texts, sampling_params, lora_request=None):
        n = sampling_params.get("n", 1)
        return [types.SimpleNamespace(outputs=[types.SimpleNamespace(text=a)] * n) for a in self.answers.values()]


def test_evaluate_and_pass_rates_score_with_the_environment():
    files = g.task_files(("under_specified",))
    rows = g.build_rows(files, Tok(), 7000, 24, 0, split="test")
    assert rows == g.build_rows(files, Tok(), 7000, 24, 0, split="test")  # the same draw every time
    gold = {t.id: t.scenario for f in files for t in load_tasks(f)}
    model = Model(gold, rows)
    with ProcessPoolExecutor(4, initializer=g._init_worker, initargs=(files,),
                             mp_context=multiprocessing.get_context("spawn")) as pool:
        res = g.evaluate(model, Tok(), rows, pool, 768)
        rates = g.pass_rates(model, Tok(), rows, pool, 3, 768)
    assert res["accuracy"] == 0.5 and res["correct"] == "10" * 12
    assert [rates[r["task_id"]] for r in rows] == [1.0, 0.0] * 12
