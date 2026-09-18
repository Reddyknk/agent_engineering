#!/usr/bin/env bash
# One documented command that runs every baseline check.
# Book 1 §2's Evaluation checklist requires this: "Can all baseline
# checks run with one documented command?"
set -euo pipefail

echo "==> ruff format --check"
ruff format --check .

echo "==> ruff check"
ruff check .

echo "==> pytest"
pytest

echo "==> All checks passed."
