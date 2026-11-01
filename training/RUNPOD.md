# GRPO smoke test on Runpod

The setup that worked on Nov 1, 2026: an RTX 4090 (24 GB) on Secure Cloud at $0.89/hr, Runpod PyTorch template, host driver 595.91.07 with CUDA 13.2.

Versions that worked together: torch 2.13.0+cu132, vllm 0.32.0, unsloth 2026.10.11, trl 1.15.0, datasets 4.8.5, pulp 3.3.2.

```text
# ---- 0. Runpod console (browser, no commands) ----
# Sign up with a personal email; add $10 credit; auto-pay OFF       -> the most you can spend is $10
# Pods -> Deploy -> Secure Cloud, CUDA >= 12.8 filter, RTX 4090      -> Community Cloud had no cheap GPUs in stock
# Template: Runpod PyTorch; container disk 50 GB; volume disk 0 GB   -> no storage that bills after the pod is gone
# Deploy On-Demand (not Spot)                                         -> Spot pods can be shut down mid-run
# Connect -> Web Terminal                                             -> a shell inside the pod

# ---- 1. Keep the session alive ----
apt-get update && apt-get install -y tmux      # a terminal that survives a closed browser tab
tmux new -s pilot                              # open a session named "pilot"
# tmux attach -t pilot                         # (later) reconnect after the tab closes

# ---- 2. Get the code ----
git clone https://github.com/aptgetnitin/whatifgym && cd whatifgym   # the public repo

# ---- 3. Check the driver's CUDA version ----
nvidia-smi | head -4                           # top right, "CUDA Version: 13.2" -> uv picks the matching builds below

# ---- 4. Python environment with matching builds ----
pip install uv                                 # a fast installer that resolves all packages together
uv venv .venv-train --python 3.12              # an isolated Python 3.12 environment
source .venv-train/bin/activate                # use it in this shell
uv pip install vllm --torch-backend=auto       # "auto" reads the driver and picks the torch build for it
uv pip install unsloth trl datasets -r requirements.txt --torch-backend=auto   # training libraries + WhatIfGym's own
uv pip install vllm-bnb-plugin --torch-backend=auto   # vLLM >= 0.28 needs it for 4-bit loading (else: RuntimeError at model load)

# ---- 5. Verify ----
python training/check_gpu.py                   # expect the torch build, "matmul ok", all 6 libraries, READY
uv pip freeze > training/env-lock.txt          # exact versions, for the paper's compute report

# ---- 6. Smoke test ----
python training/grpo_pilot.py --smoke --workers 6   # 5 GRPO steps on 20 tasks; --workers = pod vCPUs - 2
cat results/training/pilot/summary.json             # the results

# ---- 7. Pilot, 50 steps (same pod: no second install) ----
# Already inside tmux? Run it there. "tmux new" inside tmux says "sessions should be nested with care".
python training/grpo_pilot.py --max-steps 50 --workers 6 --out results/training/pilot50   # --out keeps the smoke results
# Ctrl+b then d: leave it running; "tmux attach": come back
cat results/training/pilot50/summary.json

# ---- 8. Pilot with a before/after evaluation (the gate measure) ----
# The training reward cannot show learning (each step sees new questions). This run scores the same 200 test
# tasks, greedy, before and after training; 8 questions per step (--grad-accum 8, now the default).
git pull                                        # needs the commit with --eval-tasks
python training/grpo_pilot.py --max-steps 80 --workers 6 --eval-tasks 200 --out results/training/pilot80
# look for two lines: "EVAL before training: {...}" and "EVAL after training: {...}"
grep -h "^SUMMARY" -r results/ 2>/dev/null || true   # (the one-line summary is also printed at the end)

# ---- 9. When done ----
# Console -> pod menu -> Terminate; check that Pods is empty         -> "Stop" alone still bills for the disk
```

**What did not work.** `pip install torch --index-url .../cu128` followed by `pip install -r ...` mixed builds: pip took the CUDA 13 vLLM and torchvision from PyPI over a CUDA 12.8 torch, and `unsloth` and `vllm` did not import. Use `uv ... --torch-backend=auto` and let it choose all three.

Set `--workers` from the vCPU count on the pod page, not from `nproc`: inside a container, `nproc` can show the CPUs of the whole host.

## Results

| Run | Date | Steps | s/step | Solver s/step | Peak GPU | Reward by step | Dropped TRL options |
|---|---|---|---|---|---|---|---|
| Smoke (`--smoke`, 20 tasks) | Nov 1, 2026 | 5 | 39.3 | 0.25 (0.6 %) | 20.16 GB of 24 | 0.688, 0.975, 0.05, 1.1, 0.55 | `max_prompt_length`, `warmup_ratio` |
| Pilot (`--max-steps 50`, 1,078 tasks) | Nov 1, 2026 | 50 | 16.5 | 0.12 (0.7 %) | 18.19 GB of 24 | mean 0.554; steps 1–25: 0.475, steps 26–50: 0.634 | `max_prompt_length`, `warmup_ratio` |

Smoke: the pipeline works end to end, and the solver is not the bottleneck (the plan's limit is a quarter of each step). Five steps of 2 prompts each are too few to show learning. Peak memory is mostly vLLM's advance reservation (55 % of the card), so it does not yet say whether a 12 GB GPU fits. Both dropped options are harmless here: prompts are already filtered to 7,000 tokens, and warmup was 0.

Pilot: 823.9 s of training (the smoke run's 39.3 s/step included the first-step compile). The mean reward rose from 0.475 (steps 1–25) to 0.634 (steps 26–50), but the slope is +0.002 a step and a permutation test gives p = 0.29: not a real trend yet. Each step sees only 2 questions, so its reward mostly says how hard those two were (9 steps were near 0, 7 were 1.1). Answers were about 130 tokens and none hit the 768 limit. The training reward cannot show learning at this size; the next run needs a fixed evaluation set scored before and after training.

Per-step rewards: 0.688, 0.038, 0.562, 0.55, 0.55, 0.975, 0.7, 0.062, 0.6, 0.963, 0.05, 0.55, 0.562, 0.562, 0.013, 1.1, 0.55, 0.275, 0.3, 0.963, 0.55, 0.138, 0.025, 0.0, 0.55, 0.413, 1.1, 0.85, 0.0, 1.1, 1.1, 0.6, 1.1, 0.55, 0.55, 0.575, 1.1, 0.963, 0.825, 0.013, 0.175, 0.575, 0.038, 0.6, 0.963, 0.275, 0.575, 0.688, 1.1, 0.013.

Cost: RTX 4090 at $0.89/hr; smoke 196.6 s and pilot 823.9 s of training, plus installs and start-up.

Printing results: long pasted one-liners and heredocs broke in the web terminal (it wraps lines and indents pasted lines, so `EOF` is not seen). Print the summary with a short line: `cd results/training/pilot50 && python -c "import json;print(json.load(open('summary.json')))"`.

## Problems hit, in order

1. `check_gpu.py` said `not sm_89` on the RTX 4090: a false alarm, fixed in `da6e3a8` (an `sm_86` build runs on `sm_89`).
2. `unsloth` and `vllm` did not import: mixed CUDA builds from `pip`. Fix: a fresh venv with `uv ... --torch-backend=auto`.
3. `RuntimeError: Unsloth: vLLM >= 0.28 moved bitsandbytes out of tree`: fix `uv pip install vllm-bnb-plugin`; in `training/requirements.txt` since `472daa5`.
4. `sessions should be nested with care`: already inside tmux; run the command there.
