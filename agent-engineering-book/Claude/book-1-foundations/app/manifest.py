"""The run manifest: what it takes to reproduce a run.

A result that cannot be traced back to the exact inputs that produced it is
an anecdote. This module builds the record that turns one into evidence.

The manifest grows across versions. V0 records the harness; later versions
add the pieces they introduce — skills and their content hashes (V3),
dataset version (V8), trace identifiers (V10). Nothing is added
speculatively: a field appears in the version that can actually populate it.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import Settings, get_settings

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "RUN_MANIFEST.json"


def content_hash(path: Path) -> str:
    """Stable identity for a file whose content must be reproducible.

    Used for skills (V3), policies (V2) and evaluation datasets (V8) — the
    inputs a reader would otherwise have to take on trust.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def _git_revision() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None if result.returncode == 0 else None


def _pinned_dependencies() -> dict[str, str]:
    """Read the exact pins from pyproject rather than the installed set.

    The installed set answers "what is on this machine"; the pins answer
    "what was this evaluated against", which is the reproducible question.
    """
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    pins: dict[str, str] = {}
    for raw in text.splitlines():
        # Strip the trailing comment first — several pins carry one naming
        # the version that introduces them — then the TOML list punctuation.
        line = raw.split("#", 1)[0].strip().rstrip(",").strip().strip('"')
        if "==" not in line:
            continue
        name, _, version = line.partition("==")
        name, version = name.strip(), version.strip()
        if name and version:
            pins[name] = version
    return pins


def build_manifest(
    settings: Settings | None = None,
    *,
    version_tag: str = "v0-harness",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    settings = settings or get_settings()
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version_tag": version_tag,
        "application": {
            "version": settings.app_version,
            "environment": settings.app_env,
            "git_revision": _git_revision(),
        },
        "model": settings.model_parameters(),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.system().lower(),
        },
        "dependencies": _pinned_dependencies(),
        "autonomy_boundary": {
            "external_send_enabled": settings.allow_external_send,
            "note": "Book 1 builds no send tool. This records the boundary, "
            "it does not enforce it — the enforcement is the absence of the tool.",
        },
    }
    if extra:
        manifest.update(extra)
    return manifest


def write_manifest(manifest: dict[str, Any] | None = None) -> Path:
    payload = manifest or build_manifest()
    MANIFEST_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )
    return MANIFEST_PATH


if __name__ == "__main__":
    path = write_manifest()
    print(f"wrote {path.relative_to(REPO_ROOT)}")
