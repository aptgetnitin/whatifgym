#!/usr/bin/env python3
"""Run an agent over a task file through the environment and score it.

    python scripts/run_baseline.py --tasks tasks/factory_planning/data_change_v0.jsonl --agent oracle
    python scripts/run_baseline.py --tasks ... --agent noop
    python scripts/run_baseline.py --tasks ... --split test --agent anthropic --model claude-sonnet-4-5

Agents
  oracle            submits the hidden gold scenario (pipeline sanity check: every task must score 1.1)
  noop              submits an empty but valid scenario (scores the 0.1 validity bonus only)
  ask_then_oracle   asks an unnecessary question first, then the gold scenario (expects 0.9)
  anthropic         a frontier model through the Anthropic Messages API (needs ANTHROPIC_API_KEY and `pip install anthropic`)

Writes one JSON line per episode to --out and prints a summary table.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from whatifgym.env import WhatIfEnv  # noqa: E402
from whatifgym.tasks import load_tasks  # noqa: E402


# ------------------------------------------------------------------------------------------------ agents
def agent_oracle(obs, task, _state):
    return {"type": "scenario", "scenario": task.scenario}


def agent_noop(obs, task, _state):
    return {"type": "scenario", "scenario": {"version": "0.1", "base_model": task.model, "data_changes": []}}


def agent_ask_then_oracle(obs, task, state):
    if not state.get("asked"):
        state["asked"] = True
        return {"type": "ask", "text": "Can you confirm the numbers?"}
    return {"type": "scenario", "scenario": task.scenario}


SYSTEM_PROMPT = """You are a planning analyst who turns a planner's what-if question into a machine-checkable
scenario for an existing optimization model. You never solve the model yourself. You answer with ONE JSON object
that validates against the scenario DSL schema you are given: either a scenario (data_changes, rules, objective,
fixed_decisions) or, only when the question cannot be made precise from the information available, {"ask": "..."}.
Use only table names, column names, parameter names, measure names and key values that appear in the model
schema and index sets. Output JSON only, no prose, no code fences."""


def _compact_schema(schema: dict) -> dict:
    tables = {t: {"key": s.get("key", []), "columns": {c: {k: v for k, v in cs.items() if k in ("type", "unit", "description")}
                                                        for c, cs in s.get("columns", {}).items()}}
              for t, s in schema.get("tables", {}).items()}
    return {"tables": tables, "params": schema.get("params", {}), "decision_variables": schema.get("decision_variables", {}),
            "constraints": schema.get("constraints", {})}


def build_prompt(obs: dict) -> str:
    parts = [
        f"# Base model: {obs['title']} (`{obs['model']}`)", obs["description"],
        "# Model schema (tables, columns, parameters)", json.dumps(_compact_schema(obs["schema"]), indent=1),
        "# Key values you may refer to", json.dumps(obs["index_sets"]),
        "# Decision measures for rules / fixed decisions / objective stages", json.dumps(obs["measures"]),
        "# Scenario DSL JSON Schema", json.dumps(obs["dsl_schema"], separators=(",", ":")),
        "# Worked examples",
    ]
    for ex in obs["examples"]:
        parts += [f"Question: {ex['question']}", json.dumps(ex["scenario"], indent=1)]
    if obs["dialogue"]:
        parts += ["# Dialogue so far", json.dumps(obs["dialogue"], indent=1)]
    parts += [f"# Planner's question\n{obs['question']}", "Answer with the JSON object only."]
    return "\n\n".join(parts)


def _extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start:end + 1])


def make_anthropic_agent(model_name: str, max_tokens: int = 2000):
    try:
        import anthropic
    except ImportError as exc:
        raise SystemExit("pip install anthropic") from exc
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("set ANTHROPIC_API_KEY in the environment")
    client = anthropic.Anthropic()

    def agent(obs, task, state):
        t0 = time.perf_counter()
        resp = client.messages.create(model=model_name, max_tokens=max_tokens, system=SYSTEM_PROMPT,
                                      messages=[{"role": "user", "content": build_prompt(obs)}])
        text = "".join(getattr(b, "text", "") for b in resp.content)
        state["latency_s"] = state.get("latency_s", 0.0) + time.perf_counter() - t0
        state["input_tokens"] = state.get("input_tokens", 0) + resp.usage.input_tokens
        state["output_tokens"] = state.get("output_tokens", 0) + resp.usage.output_tokens
        try:
            scenario = _extract_json(text)
        except Exception:
            state["parse_error"] = text[:500]
            return {"type": "scenario", "scenario": {"version": "0.1", "note": "unparseable model output", "data_changes": []}}
        return {"type": "scenario", "scenario": scenario}

    return agent


# ------------------------------------------------------------------------------------------------ driver
def run(tasks, agent, solver="highs", verbose=False):
    env = WhatIfEnv(tasks, solver=solver)
    records = []
    for task in tasks:
        obs = env.reset(task)
        state: dict = {}
        done, reward, info = False, 0.0, {}
        actions = []
        while not done:
            action = agent(obs, task, state)
            actions.append(action)
            obs, reward, done, info = env.step(action)
        rec = {"task_id": task.id, "template": task.template, "difficulty": task.difficulty, "split": task.split,
               "reward": reward, **{k: info["score"][k] for k in ("correct", "valid_dsl", "asked", "route_correct")},
               "notes": info["score"].get("notes", ""), "validation_errors": info.get("validation_errors", []),
               "final_action": actions[-1], "agent_state": state}
        if "result" in info:
            rec["candidate_objective"] = info["result"].get("objective")
            rec["reference_objective"] = task.reference.get("objective")
        records.append(rec)
        if verbose:
            print(f"{task.id} reward={reward:.2f} {rec['notes']}")
    return records


def summarise(records) -> str:
    n = len(records)
    if not n:
        return "no episodes"
    lines = [f"episodes: {n}", f"mean reward: {sum(r['reward'] for r in records) / n:.3f}",
             f"accuracy: {sum(r['correct'] for r in records) / n:.3f}",
             f"valid DSL: {sum(r['valid_dsl'] for r in records) / n:.3f}",
             f"route correct: {sum(r['route_correct'] for r in records) / n:.3f}"]
    by = collections.defaultdict(list)
    for r in records:
        by[("difficulty", r["difficulty"])].append(r["correct"])
        by[("template", r["template"])].append(r["correct"])
    lines.append("| group | n | accuracy |")
    lines.append("|---|---|---|")
    for (kind, key), vals in sorted(by.items()):
        lines.append(f"| {kind}={key} | {len(vals)} | {sum(vals) / len(vals):.2f} |")
    tok_in = sum(r["agent_state"].get("input_tokens", 0) for r in records)
    tok_out = sum(r["agent_state"].get("output_tokens", 0) for r in records)
    lat = sum(r["agent_state"].get("latency_s", 0.0) for r in records)
    if tok_in:
        lines.append(f"API tokens: {tok_in} in / {tok_out} out; mean latency {lat / n:.2f}s")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--split", default=None, help="train | dev | test (default: all)")
    ap.add_argument("--agent", default="oracle", choices=["oracle", "noop", "ask_then_oracle", "anthropic"])
    ap.add_argument("--model", default="claude-sonnet-4-5", help="API model name for --agent anthropic")
    ap.add_argument("--solver", default="highs")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    tasks = load_tasks(args.tasks, split=args.split)
    if args.limit:
        tasks = tasks[:args.limit]
    agent = {"oracle": agent_oracle, "noop": agent_noop, "ask_then_oracle": agent_ask_then_oracle}.get(args.agent)
    if agent is None:
        agent = make_anthropic_agent(args.model)
    records = run(tasks, agent, solver=args.solver, verbose=args.verbose)
    out = Path(args.out or ROOT / "results" / f"{Path(args.tasks).stem}.{args.agent}{'.' + args.model if args.agent == 'anthropic' else ''}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, default=str) + "\n")
    print(summarise(records))
    print(f"\nwrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
