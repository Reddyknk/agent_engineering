#!/usr/bin/env python3
"""Verify the repository baseline is set up correctly, offline.

This script proves the checkpoint is *ready to check*, before
``scripts/check.sh`` runs formatting, linting, typing, and tests. It makes
no network calls and requires no credentials — that is the whole point: a
learner should be able to tell the difference between "my environment is
broken" and "my code is broken" without ever touching the internet.

It does not, and must not, check for a local Antigravity GUI installation.
Whether Antigravity is installed and authenticated on a given machine is
not a portable repository contract — that's the kind of thing a
facilitator confirms once for a room full of laptops, not something a
committed Python script can verify for everyone who ever clones this repo.
"""

from __future__ import annotations

import importlib.util
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIN_PYTHON = (3, 11)

REQUIRED_PATHS = [
    "pyproject.toml",
    "README.md",
    "SPEC.md",
    "docs/widgetware-business-brief.md",
    "docs/acceptance-criteria.md",
    "docs/architecture.md",
    ".agents/rules/engineering.md",
    ".agents/rules/security.md",
    ".agents/workflows/baseline-check.md",
    ".env.example",
    "src/widgetware_sdr/__init__.py",
    "src/widgetware_sdr/health.py",
    "tests/unit/test_health.py",
    "tests/unit/test_repository_contract.py",
]


class VerificationError(Exception):
    """Raised when a single verification check fails."""


def check_python_version() -> None:
    if sys.version_info[:2] < MIN_PYTHON:
        got = ".".join(str(part) for part in sys.version_info[:2])
        want = ".".join(str(part) for part in MIN_PYTHON)
        raise VerificationError(f"Python {want}+ required, found {got}.")


def check_required_paths() -> None:
    missing = [p for p in REQUIRED_PATHS if not (REPO_ROOT / p).exists()]
    if missing:
        joined = "\n  - ".join(missing)
        raise VerificationError(f"Missing required files:\n  - {joined}")


def check_package_importable() -> None:
    spec = importlib.util.find_spec("widgetware_sdr")
    if spec is None:
        raise VerificationError(
            'widgetware_sdr is not importable. Run `pip install -e ".[dev]"` first.'
        )


def check_version_readable() -> None:
    pyproject_path = REPO_ROOT / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)
    version = data.get("project", {}).get("version")
    if not version or not isinstance(version, str):
        raise VerificationError("pyproject.toml has no readable [project.version].")

    import widgetware_sdr

    if widgetware_sdr.__version__ != version:
        raise VerificationError(
            f"Package __version__ ({widgetware_sdr.__version__}) does not match "
            f"pyproject.toml's project.version ({version})."
        )


def check_no_committed_env() -> None:
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        raise VerificationError(
            ".env exists in the repository root. Copy it to a value outside version "
            "control, or confirm it is listed in .gitignore and was never committed."
        )


CHECKS = [
    ("Python version", check_python_version),
    ("Required files present", check_required_paths),
    ("Package importable", check_package_importable),
    ("Package version readable", check_version_readable),
    ("No committed .env", check_no_committed_env),
]


def main() -> int:
    failures = 0
    for name, check in CHECKS:
        try:
            check()
        except VerificationError as exc:
            print(f"[FAIL] {name}: {exc}")
            failures += 1
        else:
            print(f"[ OK ] {name}")

    if failures:
        print(f"\n{failures} check(s) failed.")
        return 1

    print("\nEnvironment verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
