"""Deterministic context builder for WidgetWare SDR."""

import copy
import yaml
from pathlib import Path
from typing import Any

from widgetware_sdr.instructions import get_system_instructions

def build_context(
    account: dict[str, Any],
    objective: str,
    evidence: list[dict[str, Any]],
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble the five context layers deterministically from configuration and inputs.

    Args:
        account: Information about the target account (untrusted task data).
        objective: SDR research objective for the run.
        evidence: Retrieved or supplied evidence items with provenance.
        state: Prior execution workflow state, or None.

    Returns:
        A dictionary containing the five separate context layers.
    """
    # 1. Determine configuration directory
    project_root = Path(__file__).resolve().parent.parent.parent
    config_dir = project_root / "config"
    
    products_path = config_dir / "products.yaml"
    icp_path = config_dir / "icp.yaml"
    policies_path = config_dir / "policies.yaml"

    # 2. Validate configuration files exist
    if not products_path.is_file():
        raise FileNotFoundError(f"Missing products configuration: {products_path}")
    if not icp_path.is_file():
        raise FileNotFoundError(f"Missing ICP configuration: {icp_path}")
    if not policies_path.is_file():
        raise FileNotFoundError(f"Missing policies configuration: {policies_path}")

    # 3. Load configurations
    try:
        with open(products_path, "r", encoding="utf-8") as f:
            products_data = yaml.safe_load(f) or {}
    except Exception as e:
        raise ValueError(f"Failed to parse products.yaml: {e}")

    try:
        with open(icp_path, "r", encoding="utf-8") as f:
            icp_data = yaml.safe_load(f) or {}
    except Exception as e:
        raise ValueError(f"Failed to parse icp.yaml: {e}")

    try:
        with open(policies_path, "r", encoding="utf-8") as f:
            policies_data = yaml.safe_load(f) or {}
    except Exception as e:
        raise ValueError(f"Failed to parse policies.yaml: {e}")

    # 4. Prevent mutation of input parameters by deep copying them
    safe_account = copy.deepcopy(account)
    safe_evidence = copy.deepcopy(evidence)
    safe_state = copy.deepcopy(state) if state is not None else {}

    # 5. Build and return the five-layer context package
    return {
        "system_instructions": get_system_instructions(),
        "business_context": {
            "products": products_data,
            "icp": icp_data,
            "policies": policies_data,
        },
        "task_context": {
            "account": safe_account,
            "objective": objective,
        },
        "retrieved_evidence": safe_evidence,
        "state": safe_state,
    }
