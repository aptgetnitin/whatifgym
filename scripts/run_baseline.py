#!/usr/bin/env python3
"""Run an agent over a task file through the environment and score it.

    python scripts/run_baseline.py --tasks tasks/factory_planning/data_change_v0.jsonl --agent oracle
    python scripts/run_baseline.py --tasks ... --agent noop
    python scripts/run_baseline.py --tasks ... --agent anthropic --model claude-sonnet-5-5
    python scripts/run_baseline.py --tasks ... --agent ollama --model qwen3:8b --save-answers results/raw/qwen3-8b

Agents
  oracle            submits the hidden gold scenario (pipeline sanity check: every task must score 1.1)
  noop              submits an empty but valid scenario (scores the 0.1 validity bonus only)
  ask_then_oracle   asks an unnecessary question first, then the gold scenario (expects 0.9)
  anthropic         a frontier model through the Anthropic Messages API (needs ANTHROPIC_API_KEY and `pip install anthropic`)
  ollama            a local open-weight model served by Ollama (http://localhost:11434); the context window is
                    forced to --num-ctx (default 16384) because Ollama's default of 4096 silently truncates our
                    4-7k-token prompts, and JSON output mode is on unless --no-json-mode
  answers           replays answers collected elsewhere (one <task_id>.json per task) so any model can be scored here

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
        "# Rows that exist in each table (keys only; `set`/`scale`/`shift` need an existing row, `add` a new key)",
        json.dumps({t: [list(r.values()) for r in rows] for t, rows in obs["table_keys"].items()}, separators=(",", ":")),
        "# Parameter names", json.dumps(obs["params"]),
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


# USD per million tokens (input, output) from platform.claude.com/docs/en/models/overview, read 2026-10-02.
PRICES = {"claude-fable-5-1": (10.0, 50.0), "claude-opus-5-5": (4.0, 20.0), "claude-sonnet-5-5": (2.0, 10.0),
          "claude-haiku-4-5-20251001": (1.0, 5.0), "claude-haiku-4-5": (1.0, 5.0)}


def estimate_cost_usd(model_name: str, input_tokens: int, output_tokens: int) -> float | None:
    for key, (pin, pout) in PRICES.items():
        if model_name.startswith(key):
            return input_tokens / 1e6 * pin + output_tokens / 1e6 * pout
    return None


def make_anthropic_agent(model_name: str, max_tokens: int = 4000, retries: int = 3):
    try:
        import anthropic
    except ImportError as exc:
        raise SystemExit("pip install anthropic") from exc
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("set ANTHROPIC_API_KEY in the environment")
    client = anthropic.Anthropic()

    def agent(obs, task, state):
        t0 = time.perf_counter()
        for attempt in range(retries):
            try:
                resp = client.messages.create(model=model_name, max_tokens=max_tokens, system=SYSTEM_PROMPT,
                                              messages=[{"role": "user", "content": build_prompt(obs)}])
                break
            except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.InternalServerError) as exc:
                if attempt == retries - 1:
                    raise
                time.sleep(5 * (attempt + 1))
                state["retries"] = state.get("retries", 0) + 1
        text = "".join(getattr(b, "text", "") or "" for b in resp.content if getattr(b, "type", "") == "text")
        state["latency_s"] = state.get("latency_s", 0.0) + time.perf_counter() - t0
        state["input_tokens"] = state.get("input_tokens", 0) + resp.usage.input_tokens
        state["output_tokens"] = state.get("output_tokens", 0) + resp.usage.output_tokens
        state["model"] = model_name
        state["raw_output"] = text[:4000]
        try:
            scenario = _extract_json(text)
        except Exception:
            state["parse_error"] = text[:500]
            return {"type": "scenario", "scenario": {"version": "0.1", "note": "unparseable model output", "data_changes": []}}
        return {"type": "scenario", "scenario": scenario}

    return agent


def _save_answer(save_dir, task_id: str, text: str) -> None:
    if save_dir:
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        (Path(save_dir) / f"{task_id}.json").write_text(text, encoding="utf-8")


def _ollama_request(host: str, path: str, body: dict | None = None, timeout: float = 600.0) -> dict:
    import urllib.error
    import urllib.request

    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(host.rstrip("/") + path, data=data, method="POST" if body is not None else "GET",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"Ollama {path} returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"cannot reach Ollama at {host} ({exc.reason}); start it with `ollama serve` or the app") from exc


def make_ollama_agent(model_name: str, host: str = "http://localhost:11434", num_ctx: int = 16384, think: str = "off",
                      max_tokens: int = 2000, temperature: float = 0.0, json_mode: bool = True,
                      save_dir: str | None = None, timeout: float = 900.0, think_max_tokens: int = 8192):
    """A local open-weight model through Ollama's native /api/chat.

    Pre-flight: the server answers, the model is pulled, and its native context length is at least --num-ctx
    (Ollama's default window is 4096 tokens and it truncates silently; our prompts are 4-7k tokens, so every call
    sets `num_ctx` explicitly). Thinking is off by default for comparability and speed (`--think on`, or
    low|medium|high for gpt-oss); a model that does not support the `think` flag is retried without it.
    """
    tags = _ollama_request(host, "/api/tags", timeout=30)
    names = {m.get("name") for m in tags.get("models", [])} | {m.get("model") for m in tags.get("models", [])}
    if model_name not in names and f"{model_name}:latest" not in names:
        raise SystemExit(f"model {model_name!r} is not pulled; run `ollama pull {model_name}` (have: {sorted(n for n in names if n)})")
    show = _ollama_request(host, "/api/show", {"model": model_name}, timeout=60)
    native_ctx = next((v for k, v in (show.get("model_info") or {}).items() if k.endswith(".context_length")), None)
    if native_ctx and native_ctx < num_ctx:
        print(f"warning: {model_name} has a native context of {native_ctx} tokens, below --num-ctx {num_ctx}; prompts may be truncated")
    print(f"ollama: {model_name} ready (num_ctx={num_ctx}, think={think}, json_mode={json_mode}, native context={native_ctx})")

    think_value = {"off": False, "on": True}.get(think, think)
    send_think = {"value": True}
    # distinct label so a thinking run is not merged with the plain run (both share the Ollama model id)
    label = f"ollama/{model_name}" + ("" if think == "off" else f"+think={think}")
    # thinking tokens count against num_predict: give a thinking run room, or answers get cut off mid-JSON
    budget = max_tokens if think == "off" else max(max_tokens, think_max_tokens)

    def agent(obs, task, state):
        prompt = build_prompt(obs)
        body = {"model": model_name, "stream": False,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                "options": {"num_ctx": num_ctx, "temperature": temperature, "num_predict": budget, "seed": 0}}
        if json_mode:
            body["format"] = "json"
        if send_think["value"]:
            body["think"] = think_value
        t0 = time.perf_counter()
        try:
            resp = _ollama_request(host, "/api/chat", body, timeout=timeout)
        except RuntimeError as exc:
            if "think" in str(exc).lower() and send_think["value"]:
                send_think["value"] = False          # model has no thinking switch: resend without it, once for all
                body.pop("think", None)
                try:
                    resp = _ollama_request(host, "/api/chat", body, timeout=timeout)
                except RuntimeError as exc2:
                    exc = exc2
                    resp = None
            else:
                resp = None
            if resp is None:
                # a per-task server error (e.g. HTTP 500 "token repeat limit reached") must not abort the whole
                # run: record it, score it as a failed answer, and move to the next task.
                state["request_error"] = str(exc)[:300]
                state["latency_s"] = state.get("latency_s", 0.0) + time.perf_counter() - t0
                state["model"] = label
                _save_answer(save_dir, task.id, f"REQUEST_ERROR: {exc}")
                return {"type": "scenario", "scenario": {"version": "0.1", "note": "request error", "data_changes": []}}
        text = (resp.get("message") or {}).get("content", "")
        state["latency_s"] = state.get("latency_s", 0.0) + time.perf_counter() - t0
        state["input_tokens"] = state.get("input_tokens", 0) + int(resp.get("prompt_eval_count") or 0)
        state["output_tokens"] = state.get("output_tokens", 0) + int(resp.get("eval_count") or 0)
        state["model"] = label
        state["raw_output"] = text[:4000]
        if (resp.get("message") or {}).get("thinking"):
            state["thinking_chars"] = len(resp["message"]["thinking"])
        if int(resp.get("prompt_eval_count") or 0) >= num_ctx - budget:
            state["truncated"] = True
            print(f"warning: {task.id}: prompt filled the context window ({resp.get('prompt_eval_count')} tokens); raise --num-ctx")
        if resp.get("done_reason") == "length":
            state["cut_off"] = True
        state["turns"] = state.get("turns", 0) + 1   # a reply after a clarifying question must not overwrite the first
        _save_answer(save_dir, task.id if state["turns"] == 1 else f"{task.id}.turn{state['turns']}", text)
        try:
            scenario = _extract_json(text)
        except Exception:
            state["parse_error"] = text[:500]
            return {"type": "scenario", "scenario": {"version": "0.1", "note": "unparseable model output", "data_changes": []}}
        return {"type": "scenario", "scenario": scenario}

    return agent


def make_answers_agent(answers_dir: str, label: str):
    """Replay answers collected offline: one <task_id>.json (or .txt with JSON inside) per task.

    Used when the model is driven by something other than this script (another harness, a human, an API
    proxy): export the prompts with --export-prompts, collect the raw replies, then score them here so the
    environment, scorer and bookkeeping stay identical across agents.
    """
    folder = Path(answers_dir)

    def agent(obs, task, state):
        state["model"] = label
        for ext in (".json", ".txt"):
            f = folder / f"{task.id}{ext}"
            if f.exists():
                text = f.read_text(encoding="utf-8")
                state["raw_output"] = text[:4000]
                try:
                    return {"type": "scenario", "scenario": _extract_json(text)}
                except Exception:
                    state["parse_error"] = text[:500]
                    return {"type": "scenario", "scenario": {"version": "0.1", "note": "unparseable output", "data_changes": []}}
        state["missing_answer"] = True
        return {"type": "scenario", "scenario": {"version": "0.1", "note": "no answer collected", "data_changes": []}}

    return agent


def export_prompts(tasks, out_dir: Path) -> int:
    """Write the exact prompt each task would receive (system + user) so an external runner can answer it."""
    out_dir.mkdir(parents=True, exist_ok=True)
    env = WhatIfEnv(tasks)
    for task in tasks:
        obs = env.reset(task)
        (out_dir / f"{task.id}.txt").write_text("SYSTEM:\n" + SYSTEM_PROMPT + "\n\nUSER:\n" + build_prompt(obs), encoding="utf-8")
    return len(tasks)


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
               "reward": reward, **{k: info["score"][k] for k in ("correct", "valid_dsl", "asked", "route_correct", "ask_needed")},
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
        model_name = next((r["agent_state"].get("model") for r in records if r["agent_state"].get("model")), "")
        cost = estimate_cost_usd(model_name, tok_in, tok_out)
        lines.append(f"API tokens: {tok_in} in / {tok_out} out; mean latency {lat / n:.2f}s"
                     + (f"; estimated cost ${cost:.2f} ({model_name})" if cost is not None else ""))
    truncated = sum(1 for r in records if r["agent_state"].get("truncated"))
    cut_off = sum(1 for r in records if r["agent_state"].get("cut_off"))
    if truncated:
        lines.append(f"prompts that filled the context window (likely truncated): {truncated}")
    if cut_off:
        lines.append(f"answers cut off at max tokens: {cut_off}")
    request_errors = sum(1 for r in records if r["agent_state"].get("request_error"))
    if request_errors:
        lines.append(f"server/request errors (scored as wrong): {request_errors}")
    parse_errors = sum(1 for r in records if r["agent_state"].get("parse_error"))
    missing = sum(1 for r in records if r["agent_state"].get("missing_answer"))
    if parse_errors:
        lines.append(f"unparseable model outputs: {parse_errors}")
    if missing:
        lines.append(f"missing answers: {missing}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--split", default=None, help="train | dev | test (default: all)")
    ap.add_argument("--agent", default="oracle", choices=["oracle", "noop", "ask_then_oracle", "anthropic", "ollama", "answers"])
    ap.add_argument("--answers-dir", default=None, help="for --agent answers: folder of <task_id>.json replies")
    ap.add_argument("--label", default=None, help="for --agent answers: how to name the model in results")
    ap.add_argument("--export-prompts", default=None, metavar="DIR", help="write each task's full prompt to DIR and exit")
    ap.add_argument("--model", default="claude-sonnet-5-5", help="model id: Anthropic API id (see PRICES) or an Ollama tag such as qwen3:8b")
    ap.add_argument("--host", default=os.environ.get("OLLAMA_HOST", "http://localhost:11434"), help="Ollama server for --agent ollama")
    ap.add_argument("--num-ctx", type=int, default=16384, help="context window forced on Ollama calls (prompts are 4-7k tokens)")
    ap.add_argument("--think", default="off", help="Ollama thinking: off | on | low | medium | high (gpt-oss levels)")
    ap.add_argument("--no-json-mode", action="store_true", help="do not constrain Ollama output to JSON")
    ap.add_argument("--max-tokens", type=int, default=2000, help="max output tokens per answer")
    ap.add_argument("--think-max-tokens", type=int, default=8192, help="output budget when thinking is on (thinking tokens count against it)")
    ap.add_argument("--save-answers", default=None, metavar="DIR", help="save each raw model reply as DIR/<task_id>.json (re-score later with --agent answers)")
    ap.add_argument("--solver", default="highs")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    tasks = load_tasks(args.tasks, split=args.split)
    if args.limit:
        tasks = tasks[:args.limit]
    if args.export_prompts:
        n = export_prompts(tasks, Path(args.export_prompts))
        print(f"wrote {n} prompts to {args.export_prompts}")
        return 0
    agent = {"oracle": agent_oracle, "noop": agent_noop, "ask_then_oracle": agent_ask_then_oracle}.get(args.agent)
    if args.agent == "anthropic":
        agent = make_anthropic_agent(args.model, max_tokens=args.max_tokens)
    elif args.agent == "ollama":
        agent = make_ollama_agent(args.model, host=args.host, num_ctx=args.num_ctx, think=args.think, max_tokens=args.max_tokens,
                                  json_mode=not args.no_json_mode, save_dir=args.save_answers, think_max_tokens=args.think_max_tokens)
    elif args.agent == "answers":
        if not args.answers_dir:
            raise SystemExit("--agent answers needs --answers-dir")
        agent = make_answers_agent(args.answers_dir, args.label or Path(args.answers_dir).name)
    records = run(tasks, agent, solver=args.solver, verbose=args.verbose)
    if args.agent == "anthropic":
        suffix = "." + args.model
    elif args.agent == "ollama":
        suffix = "." + args.model.replace(":", "-").replace("/", "-")
    elif args.agent == "answers":
        suffix = "." + (args.label or Path(args.answers_dir).name)
    else:
        suffix = ""
    out = Path(args.out or ROOT / "results" / f"{Path(args.tasks).stem}.{args.agent}{suffix}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, default=str) + "\n")
    print(summarise(records))
    print(f"\nwrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
