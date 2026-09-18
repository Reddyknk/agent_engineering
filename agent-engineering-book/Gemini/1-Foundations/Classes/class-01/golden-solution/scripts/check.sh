#!/usr/bin/env bash
# One documented command that runs every baseline check, in order, failing
# on the first error. Book 1 §2's Evaluation checklist requires this:
# "Can all baseline checks run with one documented command?"
set -euo pipefail

echo "==> verify_environment.py"
python3 scripts/verify_environment.py

echo "==> ruff format --check"
ruff format --check .

echo "==> ruff check"
ruff check .

echo "==> mypy"
mypy src tests scripts

echo "==> pytest"
pytest -q

echo "==> All checks passed."
