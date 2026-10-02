#!/usr/bin/env bash
# Create .venv for this platform, install the open solvers, run the tests and the verification table.
# Works on macOS (arm64/x86-64) and Linux. Re-run it if .venv was created on another platform.
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
if [ -d .venv ] && ! .venv/bin/python -c "import sys" >/dev/null 2>&1; then
  echo "Existing .venv does not run on this platform; recreating it."
  rm -rf .venv
fi
if [ ! -d .venv ]; then
  if command -v uv >/dev/null 2>&1; then uv venv --python "$PY" .venv; else "$PY" -m venv .venv; fi
fi
if command -v uv >/dev/null 2>&1; then
  uv pip install --python .venv/bin/python -r requirements.txt
else
  .venv/bin/python -m pip install --upgrade pip >/dev/null
  .venv/bin/python -m pip install -r requirements.txt
fi

echo
.venv/bin/python - <<'PY'
import importlib.util as u
for mod in ("highspy", "pyscipopt", "ortools", "pulp"):
    print(f"{mod:10} {'ok' if u.find_spec(mod) else 'MISSING'}")
PY
.venv/bin/python -c "import highspy; print('HiGHS', highspy.Highs().version())"
.venv/bin/python -c "import pyscipopt; print('SCIP', pyscipopt.Model().version())"
.venv/bin/python -c "import ortools; print('OR-Tools', ortools.__version__)"
echo
.venv/bin/python -m pytest -q -W ignore
echo
.venv/bin/python scripts/verify_models.py
