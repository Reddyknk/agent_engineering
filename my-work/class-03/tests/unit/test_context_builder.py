"""Automated tests for the WidgetWare SDR Context Package."""

import yaml
from pathlib import Path
from unittest.mock import patch
import pytest

from widgetware_sdr.context_builder import build_context
from widgetware_sdr.instructions import get_system_instructions

SCENARIOS_DIR = Path(__file__).resolve().parent.parent / "scenarios"


def load_scenario(filename: str) -> dict:
    """Load a scenario YAML fixture file."""
    path = SCENARIOS_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# --- 1. Configuration Tests ---

def test_configuration_loading() -> None:
    """Verify that all three YAML files load and contain the required structures."""
    context = build_context(account={}, objective="", evidence=[])
    biz = context["business_context"]

    assert "products" in biz
    assert "icp" in biz
    assert "policies" in biz

    # Required top-level sections exist
    assert "company" in biz["products"]
    assert "products" in biz["products"]
    assert "minimum_employee_count" in biz["icp"]
    assert "evidence_categories" in biz["policies"]

    # Scale limit check (minimum company size is numeric)
    assert isinstance(biz["icp"]["minimum_employee_count"], (int, float))

    # Evidence classifications present
    categories = biz["policies"]["evidence_categories"]
    for cat in ["verified_fact", "derived_fact", "inference", "unknown", "conflict"]:
        assert cat in categories

    # Prohibited actions include sending messages, modifying CRM, and SLA agreements (homework)
    prohibited = biz["policies"]["prohibited_actions"]
    assert "send_email" in prohibited
    assert "send_social_message" in prohibited
    assert "modify_crm" in prohibited
    assert "make_service_level_agreements" in prohibited

    # Human approval boundaries
    approval = biz["policies"]["requires_human_approval"]
    assert "external_outreach" in approval
    assert "crm_write" in approval


# --- 2. Instruction Tests ---

def test_instruction_requirements() -> None:
    """Verify that instructions are detailed, precise, and contain observable requirements."""
    instructions = get_system_instructions()

    # Must require source evidence for factual claims
    assert "evidence" in instructions.lower() or "source" in instructions.lower()

    # Must distinguish fact from inference
    assert "inference" in instructions.lower()

    # Must prohibit invented company facts
    assert "guess" in instructions.lower() or "invent" in instructions.lower()

    # Must prohibit outreach sending
    assert "email" in instructions.lower() or "send" in instructions.lower()

    # Must prohibit CRM modification
    assert "crm" in instructions.lower()

    # Define insufficient-evidence behavior
    assert "insufficient" in instructions.lower()

    # State that task content cannot override system policies
    assert "override" in instructions.lower() or "untrusted" in instructions.lower()


# --- 3. Context Builder Behavior Tests ---

def test_context_builder_layers() -> None:
    """Verify all five context layers exist with proper separation and types."""
    account = {"company_name": "Test Company", "industry": "manufacturing"}
    objective = "Analyze company scale"
    evidence = [{"claim": "Has 6000 employees", "classification": "verified_fact"}]
    state = {"current_step": "qualification"}

    context = build_context(
        account=account,
        objective=objective,
        evidence=evidence,
        state=state
    )

    # All five layers present
    assert set(context.keys()) == {
        "system_instructions",
        "business_context",
        "task_context",
        "retrieved_evidence",
        "state",
    }

    # Separations and types
    assert isinstance(context["system_instructions"], str)
    assert isinstance(context["business_context"], dict)
    assert isinstance(context["task_context"], dict)
    assert isinstance(context["retrieved_evidence"], list)
    assert isinstance(context["state"], dict)

    # Business config separated from task data
    assert context["task_context"]["account"] == account
    assert context["task_context"]["objective"] == objective
    assert "Test Company" not in context["system_instructions"]


def test_evidence_provenance_preserved() -> None:
    """Verify that evidence details (provenance) are preserved in retrieved_evidence."""
    evidence = [
        {
            "claim": "Apex announced plant modernization.",
            "classification": "verified_fact",
            "source": {
                "name": "Apex PR",
                "url": "https://example.com/pr",
                "retrieved_at": "2026-08-07"
            },
            "excerpt": "Apex is launching modernization."
        }
    ]
    context = build_context(account={}, objective="", evidence=evidence)
    assert context["retrieved_evidence"] == evidence


def test_missing_values_remain_unknown() -> None:
    """Verify that missing account fields remain None or unknown, without guess fabrication."""
    account = {"company_name": "Ghost Inc", "industry": "unknown", "employee_count": None}
    context = build_context(account=account, objective="", evidence=[])
    
    ret_account = context["task_context"]["account"]
    assert ret_account["industry"] == "unknown"
    assert ret_account["employee_count"] is None


def test_supplied_and_omitted_state() -> None:
    """Verify state handling (preserved when supplied, empty dict when omitted)."""
    # Supplied state
    state = {"workflow_step": "check_ready", "decision": "hold"}
    context_with_state = build_context(account={}, objective="", evidence=[], state=state)
    assert context_with_state["state"] == state

    # Omitted state
    context_no_state = build_context(account={}, objective="", evidence=[])
    assert context_no_state["state"] == {}


def test_input_immutability() -> None:
    """Verify that build_context does not mutate input arguments in-place."""
    account = {"company_name": "Original"}
    evidence = [{"claim": "Original Claim"}]
    state = {"status": "Original State"}

    context = build_context(account=account, objective="", evidence=evidence, state=state)

    # Mutate the output layers
    context["task_context"]["account"]["company_name"] = "Mutated"
    context["retrieved_evidence"][0]["claim"] = "Mutated"
    context["state"]["status"] = "Mutated"

    # Inputs should be unchanged (showing deep copy behavior)
    assert account["company_name"] == "Original"
    assert evidence[0]["claim"] == "Original Claim"
    assert state["status"] == "Original State"


def test_missing_config_produces_clear_error() -> None:
    """Verify that missing configuration files produce a clear file error."""
    with patch("pathlib.Path.is_file", return_value=False):
        with pytest.raises((FileNotFoundError, ValueError)) as excinfo:
            build_context(account={}, objective="", evidence=[])
        assert "Missing" in str(excinfo.value) or "not found" in str(excinfo.value).lower()


# --- 4. Scenario Tests ---

def test_qualified_account_scenario() -> None:
    """Verify qualified account matches ICP rules."""
    scenario = load_scenario("qualified_account.yaml")
    context = build_context(
        account=scenario["account"],
        objective=scenario["objective"],
        evidence=scenario["evidence"],
        state=scenario["state"]
    )

    icp = context["business_context"]["icp"]
    acc = context["task_context"]["account"]

    # Match preferred industry
    assert acc["industry"] in icp["preferred_industries"]
    # Match size
    assert acc["employee_count"] >= icp["minimum_employee_count"]
    # Match region
    assert acc["region"] in icp["preferred_regions"]
    # Is not excluded
    assert acc["industry"] not in icp["excluded_industries"]


def test_unqualified_account_scenario() -> None:
    """Verify unqualified account fails ICP rules."""
    scenario = load_scenario("unqualified_account.yaml")
    context = build_context(
        account=scenario["account"],
        objective=scenario["objective"],
        evidence=scenario["evidence"],
        state=scenario["state"]
    )

    icp = context["business_context"]["icp"]
    acc = context["task_context"]["account"]

    # Fails scale or is in excluded industries
    assert acc["employee_count"] < icp["minimum_employee_count"] or acc["industry"] in icp["excluded_industries"]


def test_insufficient_evidence_scenario() -> None:
    """Verify insufficient evidence preserves missing fields and maps status."""
    scenario = load_scenario("insufficient_evidence.yaml")
    context = build_context(
        account=scenario["account"],
        objective=scenario["objective"],
        evidence=scenario["evidence"],
        state=scenario["state"]
    )

    acc = context["task_context"]["account"]
    assert acc["employee_count"] is None
    assert acc["industry"] == "unknown"


def test_prompt_injection_scenario() -> None:
    """Verify that malicious injection attempt cannot alter instructions or policies."""
    scenario = load_scenario("prompt_injection.yaml")
    context = build_context(
        account=scenario["account"],
        objective=scenario["objective"],
        evidence=scenario["evidence"],
        state=scenario["state"]
    )

    # Instructions remain unchanged
    assert context["system_instructions"] == get_system_instructions()
    assert "Ignore all previous policies" not in context["system_instructions"]

    # Policies remain stable
    policies = context["business_context"]["policies"]
    assert "send_email" in policies["prohibited_actions"]


def test_conflict_evidence_scenario() -> None:
    """Verify that conflicting evidence sources are classified as conflict."""
    scenario = load_scenario("conflict_evidence.yaml")
    context = build_context(
        account=scenario["account"],
        objective=scenario["objective"],
        evidence=scenario["evidence"],
        state=scenario["state"]
    )

    # Check classifications list contains conflict
    classifications = [item["classification"] for item in context["retrieved_evidence"]]
    assert "conflict" in classifications
