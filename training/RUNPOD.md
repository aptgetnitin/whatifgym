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
| Pilot80 (8 prompts a step, eval on 200 test tasks) | Nov 1, 2026 | 80 | 54.3 | 0.28 (0.5 %) | 19.64 GB of 24 | test accuracy 0.515 → **0.560**; train reward steps 1–40: 0.553, 41–80: 0.652 | `max_prompt_length`, `warmup_ratio` |

Smoke: the pipeline works end to end, and the solver is not the bottleneck (the plan's limit is a quarter of each step). Five steps of 2 prompts each are too few to show learning. Peak memory is mostly vLLM's advance reservation (55 % of the card), so it does not yet say whether a 12 GB GPU fits. Both dropped options are harmless here: prompts are already filtered to 7,000 tokens, and warmup was 0.

Pilot: 823.9 s of training (the smoke run's 39.3 s/step included the first-step compile). The mean reward rose from 0.475 (steps 1–25) to 0.634 (steps 26–50), but the slope is +0.002 a step and a permutation test gives p = 0.29: not a real trend yet. Each step sees only 2 questions, so its reward mostly says how hard those two were (9 steps were near 0, 7 were 1.1). Answers were about 130 tokens and none hit the 768 limit. The training reward cannot show learning at this size; the next run needs a fixed evaluation set scored before and after training.

Per-step rewards: 0.688, 0.038, 0.562, 0.55, 0.55, 0.975, 0.7, 0.062, 0.6, 0.963, 0.05, 0.55, 0.562, 0.562, 0.013, 1.1, 0.55, 0.275, 0.3, 0.963, 0.55, 0.138, 0.025, 0.0, 0.55, 0.413, 1.1, 0.85, 0.0, 1.1, 1.1, 0.6, 1.1, 0.55, 0.55, 0.575, 1.1, 0.963, 0.825, 0.013, 0.175, 0.575, 0.038, 0.6, 0.963, 0.275, 0.575, 0.688, 1.1, 0.013.

Cost: RTX 4090 at $0.89/hr; smoke 196.6 s and pilot 823.9 s of training, plus installs and start-up.

Printing results: long pasted one-liners and heredocs broke in the web terminal (it wraps lines and indents pasted lines, so `EOF` is not seen). Print the summary with a short line: `cd results/training/pilot50 && python -c "import json;print(json.load(open('summary.json')))"`.

## Run 3: pilot80 with before/after evaluation (started by the agent through the Runpod MCP plugin)

The same steps as above, run as one start command, so nobody needs a terminal. Pod `hot6j5n75jxl6v`, `whatifgym-pilot80`: RTX 4090, 16 vCPU, EUR-IS-2, host CUDA 13.2, $0.89/hr, image `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404` (official template "Runpod Pytorch 2.8.0"), 50 GB container disk, no volume, no ports. Created 2026-11-01 21:53 UTC. The first create (EU-CZ-1, at least 8 vCPU) was refused for capacity; the second, with no data center or vCPU filter, placed.

```text
# what the pod runs at start (entrypoint /bin/bash -c); the same as steps 2, 4, 5 and 8 by hand
cd / && git clone --depth 1 https://github.com/aptgetnitin/whatifgym && cd whatifgym
pip install -q uv
uv venv .venv-train --python 3.12 && . .venv-train/bin/activate
uv pip install -q vllm --torch-backend=auto
uv pip install -q -r requirements.txt -r training/requirements.txt --torch-backend=auto
python training/check_gpu.py; nvidia-smi | head -4
python training/grpo_pilot.py --max-steps 80 --workers 6 --eval-tasks 200 --out results/training/pilot80
echo RUN_DONE; sleep infinity        # keeps the pod up so its log can be read; then terminate it
```

Timeline (UTC): 21:53 pod created; 21:55 install done (uv took about 2 min); 21:57:54 vLLM ready (100 s, of which 47 s compile); 21:58:23 datasets built (train 1,078 tasks; test 235 fit in 7,000 tokens, 200 drawn); 21:58:57 evaluation before training done (30 s for 200 prompts); 21:59 training started. Step 1 took 181 s (compile), steps 3–6 took 58, 88, 41, 60 s: about 62 s a step, so 80 steps take about 80 min.

**Before training** (200 test tasks, greedy): accuracy **0.515**, valid 0.73, mean reward 0.588. By family: fixed_decision 0.80, relax_remove 0.75, data_change 0.688, new_limit 0.667, infeasible_request 0.591, relative_rule 0.52, chained_scenario 0.44, objective_change 0.125, logical_rule 0.077.

Watch `frac_reward_zero_std` in the step logs: the share of question groups whose 4 answers all scored the same. Such a group teaches nothing. In steps 1–6 it was 0.375 to 0.875.

**Result** (23:12 UTC; pod terminated about 23:13, `list-pods` empty after; about 80 min of pod time, about $1.18):

| 200 test tasks, greedy | Before | After 80 steps | Change |
|---|---|---|---|
| **Accuracy** | **0.515** | **0.560** | **+4.5 points (+9 tasks)** |
| Valid scenario | 0.73 | 0.79 | +6 |
| Mean reward | 0.588 | 0.639 | +0.051 |
| data_change | 0.688 | 0.781 | +9.3 |
| infeasible_request | 0.591 | 0.727 | +13.6 |
| new_limit | 0.667 | 0.714 | +4.7 |
| relative_rule | 0.52 | 0.56 | +4 |
| logical_rule | 0.077 | 0.115 | +3.8 |
| fixed_decision, relax_remove, objective_change, chained_scenario | 0.80, 0.75, 0.125, 0.44 | the same | 0 |

No family went down. The training reward rose too: steps 1–40 mean 0.553, steps 41–80 mean 0.652 (by 20-step quarter 0.52, 0.586, 0.672, 0.632); slope +0.0021 a step, permutation p = 0.006. Training: 4,345.6 s, 54.3 s a step, solver 0.28 s a step (0.5 %), peak GPU 19.64 GB, `frac_reward_zero_std` 0.375–0.875 a step.

What it does and does not show: the direction is right and consistent (more valid scenarios, gains in 5 families, none lost), but it is one seed, 200 tasks and one 4-bit 4B model. +9 tasks of 200 is not yet a significant gain by itself; the per-task results were lost with the pod, so no paired test is possible for this run. `grpo_pilot.py` now stores them (`"correct"`, one character per task) for the next run.

Per-step training reward: 0.459, 0.503, 0.575, 0.562, 0.491, 0.206, 0.728, 0.7, 0.659, 0.725, 0.316, 0.622, 0.428, 0.159, 0.491, 0.603, 0.441, 0.378, 0.791, 0.562, 0.716, 0.587, 0.775, 0.338, 0.531, 0.656, 0.472, 0.622, 0.694, 0.284, 0.522, 0.894, 0.572, 0.641, 0.834, 0.319, 0.469, 0.156, 0.725, 0.906, 0.741, 0.794, 0.653, 0.513, 0.25, 0.659, 0.522, 0.581, 0.763, 0.812, 0.756, 0.566, 0.869, 0.828, 0.831, 0.584, 0.734, 0.597, 0.6, 0.781, 0.775, 0.419, 0.675, 0.553, 0.584, 0.641, 0.713, 0.669, 0.369, 0.963, 0.606, 0.472, 0.794, 0.587, 0.609, 0.756, 0.503, 0.697, 0.703, 0.559.

## Run 4 (planned): pass-rate filter, held-out base models, 3 seeds

Changes since run 3: the task set is cleaned (`_v1` files, `tasks/superseded.txt`, probe 1.7 %); three base models are held out of training (`power_generation_hydro`, `manpower_planning`, `mining`); training uses only tasks the untrained model solves 10–90 % of the time; every seed is scored on the same tasks, with per-task results saved.

```text
# on the pod, after steps 1–4 (install)
git pull                                                     # needs commit 1eed81c or later
H="--holdout-models power_generation_hydro manpower_planning mining"
# a) pass rates: 8 sampled answers per training task (also the plan's pass@8 number); no training
python training/grpo_pilot.py $H --measure-pass 8 --workers 14 --out results/training/pass8
# look for: PASS_RATES {...}  (pass@1, pass@8 and the share in [0.1, 0.9], by family)
# b) three seeds on the filtered tasks; each scores "test" (200, trained models) and "heldout_models" (200)
for s in 1 2 3; do
  python training/grpo_pilot.py $H --pass-rates results/training/pass8/pass_rates.json \
      --max-steps 80 --workers 14 --seed $s --out results/training/run4_seed$s
done
# look for: EVAL before training / EVAL after training, and SUMMARY, for each seed
```

Three base models (`food_supply`, `farm_planning`, `car_rental_2`) have no task whose prompt fits in 7,000 tokens, so no run trains or scores on them.

Started by the agent (MCP plugin), as one start command running a) and then b): pod `du2ke49fph6irm`, `whatifgym-run4`, RTX 4090, 16 vCPU, EU-RO-1, host CUDA 13.2, $0.89/hr, same image, 50 GB disk, no volume, no ports; code at `df92ff6`. Created 2026-11-02 00:14:30 UTC. Budget cap $4.50: terminate by 05:17 UTC whatever the state.

Timeline (UTC): 00:16:45 datasets (train 1,006 tasks fit in 7,000 tokens; after the 3 held-out models, 671); 00:17 sampling 8 answers for each of 671 tasks; 00:27:06 pass rates done (about 10 min); 00:27:12 seed 1 starts; 00:27:54 filter keeps 171 of 671; 00:28:56 evaluation before training done, training starts.

**Pass rates** (`--measure-pass 8`, temperature 1, 671 training tasks):

| Family | Tasks | pass@1 | pass@8 | In [0.1, 0.9] |
|---|---|---|---|---|
| all | 671 | 0.508 | 0.624 | **0.255 (171 kept)** |
| fixed_decision | 73 | 0.868 | 0.918 | 0.11 |
| data_change | 131 | 0.637 | 0.74 | 0.206 |
| new_limit | 77 | 0.631 | 0.792 | 0.364 |
| relax_remove | 24 | 0.604 | 0.667 | 0.208 |
| infeasible_request | 61 | 0.549 | 0.639 | 0.262 |
| chained_scenario | 108 | 0.544 | 0.667 | 0.25 |
| relative_rule | 86 | 0.314 | 0.535 | 0.465 |
| logical_rule | 79 | 0.15 | 0.266 | 0.253 |
| objective_change | 32 | **0.0** | **0.0** | 0.0 |

Three quarters of the training tasks are always or never solved. `objective_change`: 0 of 256 sampled answers correct on the training models; to check (the trivial agents are exact on these files, so the references hold). The full `pass_rates.json` stays on the pod: its one-line copy in the log is cut at 16,384 characters.

**Before training, seed 1** (greedy): test (training models) 131 tasks, accuracy **0.519**, valid 0.725; held-out models (power_generation_hydro, manpower_planning, mining) 200 tasks, accuracy **0.550**, valid 0.725. Only 131 test tasks of the training models fit in 7,000 tokens.

**Seed 1 result** (training 00:29–01:41 UTC; 54.0 s a step; solver 0.06 s a step; peak GPU 19.11 GB):

| Greedy, same tasks before and after | Before | After | Gained / lost tasks | Paired test (McNemar) | 95 % bootstrap CI of the change |
|---|---|---|---|---|---|
| **Held-out base models** (200 tasks; never trained on) | 0.550 | **0.680** | 29 / 3 | p = 2.6e-6 | +8.0 to +18.5 points |
| Test tasks of the training models (131) | 0.519 | **0.634** | 16 / 1 | p = 0.00027 | +6.1 to +17.6 points |
| Valid scenario, held-out / test | 0.725 / 0.725 | 0.87 / 0.84 | | | |

Held-out models by family, before → after: data_change 0.696 → 0.826, new_limit 0.704 → 0.852, relative_rule 0.52 → 0.80, chained 0.346 → 0.50, logical_rule 0.217 → 0.304, relax 0.444 → 0.611, fixed 0.88 → 0.92, infeasible 0.571 → 0.667, objective 0.5 → 0.5. Test tasks: infeasible 0.636 → 1.0, data_change 0.71 → 0.839, chained 0.471 → 0.588, new_limit 0.462 → 0.692, objective 0 → 0.

Training reward rose from 0.668 (mean of steps 1–10) to 0.979 (steps 71–80): the model learned its 171 tasks (3.8 passes), and the gain carried over to base models it never saw. Per-task results: `training/results/run4_seed1_correct.json`.

Per-step training reward: 0.641, 0.781, 0.769, 0.703, 0.453, 0.656, 0.675, 0.897, 0.45, 0.659, 0.694, 0.356, 0.812, 0.438, 0.728, 0.519, 0.378, 0.725, 0.641, 0.791, 0.863, 0.859, 0.622, 0.738, 0.7, 0.656, 0.528, 0.759, 0.778, 0.463, 0.966, 0.728, 0.631, 0.65, 0.969, 0.678, 0.725, 0.634, 0.931, 0.966, 0.897, 0.869, 1.003, 0.906, 0.731, 0.938, 0.966, 0.906, 0.975, 0.797, 0.875, 0.628, 0.772, 0.963, 0.812, 0.938, 1.003, 0.997, 0.825, 1.031, 0.997, 0.828, 0.797, 1.034, 1.1, 0.809, 0.897, 0.881, 0.634, 1.1, 1.066, 1.031, 0.791, 1.069, 0.963, 1.034, 1.069, 0.966, 0.941, 0.859.

Seed 2 started 01:41:57 UTC.

**Seed 2 result** (ended about 02:45 UTC; 43.7 s a step):

| Greedy, same tasks | Before | After | Gained / lost | McNemar | 95 % CI of the change |
|---|---|---|---|---|---|
| **Held-out base models** (200) | 0.560 | **0.670** | 23 / 1 | p = 3e-6 | +6.5 to +15.5 points |
| Test tasks of the training models (131) | 0.527 | **0.634** | 14 / 0 | p = 0.00012 | +6.1 to +16.0 points |
| Valid scenario, held-out / test | 0.71 / 0.733 | 0.85 / 0.855 | | | |

Training reward 0.627 (steps 1–10) to 0.948 (steps 71–80). The before-training scores differ slightly between seeds (held-out 0.550 vs 0.560) although the untrained model is the same: greedy decoding in vLLM is not bit-exact across batches. Per-task results: `training/results/run4_seed2_correct.json`. Seed 3 started about 02:45 UTC. **Stopped by the user at 02:46 UTC (6:46 PM Pacific): pod terminated, `list-pods` empty; seed 3 not run. Run 4 cost about $2.30 (about 2.6 h at $0.89/hr).** To finish later: one pod with the run 4 commands and `--seed 3` only (pass rates can be re-measured in about 10 min, or skipped by reusing the same filter step).

**Why `objective_change` is 0 % on the training models** (checked on the Mac with Ollama qwen3:4b, 24 tasks of the `_v1` files): the scenario language names the model's own objective `"measure": "original"`, but the model writes its natural name (`"profit"`), which the validator rejects (`unknown measure 'profit'`). All 9 answers that came back used `profit` instead of `original`; stage order, sense and the second measure were mostly right (15 others failed with a local Ollama request error, not related). `original` appears only inside the 20,000-character schema; neither worked example is an objective change; the validator's message does not mention it. So the 0 % is mostly a prompt artifact, and RL cannot learn it (no correct sample, so the filter drops all 32 tasks). Fix after run 4 (so all three seeds share one prompt): (1) the validator's message names `original`; (2) one line on `original` in the system prompt. Then re-run the untrained ladder on the current set. **Fixed Nov 1** (`whatifgym/dsl/validate.py`, `scripts/run_baseline.py`). Check with Ollama qwen3:4b on the same 24 tasks: 2 of the 9 answers that came back are now correct (before: 0 of 9), and 3 objective stages use `original` (before: 0); most still write `profit`, often for a stage that comes second ("minimize X, then the most profit"). The other 15 failed again with a local Ollama request error, to look into. Next step if needed: an objective-change worked example in the prompt.

## Problems hit, in order

1. `check_gpu.py` said `not sm_89` on the RTX 4090: a false alarm, fixed in `da6e3a8` (an `sm_86` build runs on `sm_89`).
2. `unsloth` and `vllm` did not import: mixed CUDA builds from `pip`. Fix: a fresh venv with `uv ... --torch-backend=auto`.
3. `RuntimeError: Unsloth: vLLM >= 0.28 moved bitsandbytes out of tree`: fix `uv pip install vllm-bnb-plugin`; in `training/requirements.txt` since `472daa5`.
4. `sessions should be nested with care`: already inside tmux; run the command there.
