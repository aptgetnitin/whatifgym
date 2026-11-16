#!/bin/bash
# One training seed of the run 5 recipe on a pod, then the full-set scoring of its adapter. No terminal needed:
#     bash training/pod_seed_run.sh SEED WORKERS SECRET        (from the repo root; set the pod's deadline timer first)
# Progress and the result archive are served at https://<pod>-8000.proxy.runpod.net/SECRET/{status.txt,train.log,score.log,result.tgz}
SEED=$1; W=$2; SECRET=$3
cd "$(dirname "$0")/.." || exit 1
P=/root/pub/$SECRET; mkdir -p "$P"; touch /root/train.log /root/score.log
for f in status.txt train.log score.log result.tgz; do ln -sf /root/$f "$P/$f"; done
echo "SETUP_START $(date -u +%T)" > /root/status.txt
(nohup python3 -m http.server 8000 --directory /root/pub > /root/http.log 2>&1 &)
pip install -q uv && uv venv .venv-train --python 3.12 && source .venv-train/bin/activate \
  && uv pip install vllm --torch-backend=auto \
  && uv pip install unsloth trl datasets -r requirements.txt --torch-backend=auto \
  && uv pip install vllm-bnb-plugin --torch-backend=auto && uv pip install 'highspy==1.15.1' \
  || { echo "SETUP_FAILED $(date -u +%T)" >> /root/status.txt; exit 1; }
echo "SETUP_DONE $(date -u +%T)" >> /root/status.txt
H="power_generation_hydro manpower_planning mining assignment_with_constraints covid19_facility_location
   economic_planning fantasy_basketball optimize_power_schedule railway_dispatching airline_planning drone_network
   jobshop_ft06 single_machine_scheduling technician_routing_scheduling"
OUT=results/training/run5_seed$SEED
python training/grpo_pilot.py --holdout-models $H --pass-rates training/results/run5_pass_rates.json --max-steps 160 \
    --eval-every 20 --eval-tasks 400 --workers "$W" --seed "$SEED" --out "$OUT" > /root/train.log 2>&1
echo "TRAIN_EXIT $? $(date -u +%T)" >> /root/status.txt
if [ -d "$OUT/lora" ]; then
    python training/score_models.py --no-base --adapters "trained-run5-seed$SEED=$OUT/lora" --workers "$W" --out /root/out > /root/score.log 2>&1
    echo "SCORE_EXIT $? $(date -u +%T)" >> /root/status.txt
fi
KEEP=(); for f in "$OUT/summary.json" "$OUT/eval_task_ids.json" "$OUT/log_history.json" "$OUT/lora"; do [ -e "$f" ] && KEEP+=("$f"); done
mkdir -p /root/out
tar czf /root/result.tgz "${KEEP[@]}" -C /root out
echo "TAR_DONE $(sha256sum /root/result.tgz | cut -c1-64) $(stat -c %s /root/result.tgz) $(date -u +%T)" >> /root/status.txt
