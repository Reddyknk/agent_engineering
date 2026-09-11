"""V0 — the harness proves itself before there is an agent to prove.

These tests run with no API key, no database and no network. That is the
point: a reader who cannot get a green run here has an environment problem,
and finding that out now is cheaper than finding it out in Chapter 5 while
also debugging their first graph.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from app.config import Settings
from app.manifest import build_manifest, content_hash

REPO_ROOT = Path(__file__).resolve().parent.parent


# --- the environment itself ------------------------------------------------


def test_repository_layout_matches_the_architecture():
    """Every directory named in the architecture exists and is importable.

    A layout that drifts from the documented one is how a reader ends up
    following instructions that no longer describe the repository.
    """
    for package in [
        "api", "graph", "nodes", "policies", "contracts",
        "tools", "mcp", "skills", "retrieval", "persistence",
        "observability", "evaluation",
    ]:
        path = REPO_ROOT / "app" / package
        assert path.is_dir(), f"missing app/{package}/"
        assert (path / "__init__.py").exists(), f"app/{package}/ is not a package"


def test_secrets_are_not_committed():
    assert not (REPO_ROOT / ".env").exists(), (
        ".env is present in the repository. It is gitignored, but this test "
        "fails loudly because a committed .env is the single most common way "
        "a key leaks from a book repository."
    )
    assert (REPO_ROOT / ".env.example").exists()


def test_env_example_names_no_real_key():
    text = (REPO_ROOT / ".env.example").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("ANTHROPIC_API_KEY="):
            value = line.partition("=")[2].strip()
            assert value.startswith("sk-ant-replace"), (
                "ANTHROPIC_API_KEY in .env.example looks like a real value"
            )


# --- the autonomy boundary (Chapter 3) -------------------------------------


def test_no_send_capability_exists_anywhere():
    """The autonomy boundary is structural, not configured.

    Book 1's guarantee that the agent never contacts a prospect rests on
    there being no code that could. This test is what makes that a
    guarantee rather than an intention — it fails the moment someone adds
    the capability, regardless of whether a flag would have gated it.
    """
    forbidden = ("smtplib", "sendgrid", "boto3.client(\"ses\"", "twilio")
    offenders = []
    for path in (REPO_ROOT / "app").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in text:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: {token}")
    assert not offenders, (
        "Outbound-messaging capability found in the application:\n  "
        + "\n  ".join(offenders)
        + "\nBook 1 never builds a send tool (Chapter 3)."
    )


def test_settings_default_to_no_external_send():
    assert Settings(anthropic_api_key="test").allow_external_send is False


# --- model configuration ---------------------------------------------------


def test_model_id_is_configuration_not_code():
    """No module below config.py may name a Claude model.

    The architecture has to survive a model change. If a model id appears in
    a node, it will be missed when the default moves.
    """
    offenders = []
    for path in (REPO_ROOT / "app").rglob("*.py"):
        if path.name == "config.py":
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue  # prose about models is fine; a value is not
            if "claude-" in stripped:
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{number}")
    assert not offenders, (
        "Hard-coded model identifier(s) outside app/config.py: " + ", ".join(offenders)
    )


def test_sampling_parameters_are_not_configurable():
    """Current Claude models reject non-default sampling parameters (ADR-000).

    Offering the knob would invite a reader to set it and receive an HTTP
    400 they have no way to interpret.
    """
    settings = Settings(anthropic_api_key="test")
    for parameter in ("temperature", "top_p", "top_k"):
        assert not hasattr(settings, parameter), (
            f"Settings exposes {parameter}; current models reject it (ADR-000)."
        )
    assert "model defaults" in settings.model_parameters()["sampling"]


# --- the run manifest ------------------------------------------------------


def test_manifest_records_what_reproduction_needs():
    manifest = build_manifest(Settings(anthropic_api_key="test"))
    assert manifest["version_tag"] == "v0-harness"
    assert manifest["model"]["model_id"]
    assert manifest["runtime"]["python"]
    assert manifest["application"]["version"]


def test_manifest_pins_are_exact_not_floored():
    """A floored dependency makes a run unreproducible by design.

    See ADR-000: the langgraph / langgraph-prebuilt incident is what this
    test is defending against.
    """
    manifest = build_manifest(Settings(anthropic_api_key="test"))
    pins = manifest["dependencies"]
    assert pins, "no pinned dependencies parsed from pyproject.toml"
    assert "langgraph" in pins, f"langgraph not pinned; found {sorted(pins)}"
    for name, version in pins.items():
        # A version is digits and dots and nothing else. Checking only the
        # first character let TOML punctuation ("2.1.1\",") through once.
        assert re.fullmatch(r"\d+(\.\d+)*", version), (
            f"{name} pinned to a malformed version: {version!r}"
        )
        assert not re.search(r"[\"',#]", name), f"malformed package name: {name!r}"


def test_manifest_is_json_serializable():
    json.dumps(build_manifest(Settings(anthropic_api_key="test")))


def test_content_hash_changes_when_content_changes(tmp_path):
    """V3 records a skill's hash so a reader can tell which version ran."""
    target = tmp_path / "skill.md"
    target.write_text("procedure", encoding="utf-8")
    before = content_hash(target)
    assert content_hash(target) == before, "hash is not stable for identical content"

    target.write_text("procedure, revised", encoding="utf-8")
    assert content_hash(target) != before, "hash did not change when content changed"


# --- the domain material carried into V0 -----------------------------------


@pytest.mark.parametrize(
    "name", ["icp", "offering", "proof-points", "voice"]
)
def test_domain_config_parses_and_has_a_schema(name):
    config = REPO_ROOT / "config" / f"{name}.yaml"
    schema = REPO_ROOT / "config" / "schemas" / f"{name}.schema.json"
    assert config.exists(), f"missing config/{name}.yaml"
    assert schema.exists(), f"missing schema for {name}"
    assert yaml.safe_load(config.read_text(encoding="utf-8"))
    json.loads(schema.read_text(encoding="utf-8"))


def test_evidence_policy_keeps_claim_type_and_support_type_separate():
    """The distinction this application is built on.

    claim_type is the epistemic status of a statement; support_type is how
    strongly the cited evidence backs it. Collapsing them into one
    "confidence" number is the mistake this policy exists to prevent, and
    every later version depends on the split holding.
    """
    policy = yaml.safe_load(
        (REPO_ROOT / "app" / "contracts" / "evidence-policy.yaml").read_text(encoding="utf-8")
    )
    required = policy["required_fields_per_claim"]
    assert "claim_type" in required
    assert "support_type" in required
    assert set(policy["claim_types"]) == {"fact", "inference", "hypothesis"}


def test_account_set_is_usable_as_a_comparison_dataset():
    """Every version is measured against the same accounts.

    Chapter 2's evidence contract requires it: a comparison across versions
    is meaningless if the inputs move.
    """
    import csv

    with (REPO_ROOT / "data" / "accounts.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) >= 10, "too few accounts to compare versions meaningfully"
    for row in rows:
        assert row["company_name"].strip()
        assert row["website"].startswith("http")
        assert row["fit_reason"].strip(), f"{row['company_name']} has no stated fit reason"
