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

# ---- 7. When done ----
# Console -> pod menu -> Terminate; check that Pods is empty         -> "Stop" alone still bills for the disk
```

**What did not work.** `pip install torch --index-url .../cu128` followed by `pip install -r ...` mixed builds: pip took the CUDA 13 vLLM and torchvision from PyPI over a CUDA 12.8 torch, and `unsloth` and `vllm` did not import. Use `uv ... --torch-backend=auto` and let it choose all three.

Set `--workers` from the vCPU count on the pod page, not from `nproc`: inside a container, `nproc` can show the CPUs of the whole host.
