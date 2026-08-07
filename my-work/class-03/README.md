# WidgetWare SDR Context Package (Class 3)

This project implements the WidgetWare SDR Context Package for Class 3 of the B2B Sales Agent engineering course. It constructs a structured, deterministic, and testable context environment that a future sales agent can consume.

## Setup Instructions

1. Ensure Python 3.11+ is installed.
2. From this directory (`my-work/class-03/`), install the package in editable mode:
   ```bash
   python -m pip install -e ".[dev]"
   ```

## Running Tests

Run the automated test suite to verify the configurations, instructions, behaviors, and scenarios:
```bash
python -m pytest -v
```

## The Five Context Layers

To ensure safe, deterministic, and bounded operation, the context is strictly divided into five separate layers:

1. **System Instructions**
   Stable, immutable behavioral instructions that govern the agent's core capabilities, constraints, and boundaries (e.g. role description, evidence classification rules, and human-in-the-loop triggers). These instructions are drawn from fixed code constants and can never be overridden by user inputs or retrieved content.

2. **Business Context**
   Stable, non-prose business parameters loaded from YAML configurations. This includes:
   - `products`: Product descriptions, target buyers, and approved claims.
   - `icp`: The Ideal Customer Profile scale thresholds, region/industry preferences, and required fields.
   - `policies`: Safety policies, prohibited actions, and human approval boundaries.

3. **Task Context**
   Dynamic parameters specifying the current assignment details. This contains:
   - `account`: The target company's current profile fields (e.g. name, industry, size, region).
   - `objective`: The specific SDR task target for the run (e.g. "Evaluate Apex scale fit").

4. **Retrieved Evidence**
   A structured list of facts and signals retrieved for the account, with strict source provenance (claim text, classification category, source name, URL, retrieval timestamp, and exact excerpts). This serves as the factual grounding material for the agent.

5. **Workflow State**
   Dynamic context representing the execution status of the SDR process (such as prior decisions, missing fields, or approval status). This separates the logic path from static data or instructions.

## Safety & Security Bounding
- **Immutability**: All input structures are deep-copied to prevent side-effect mutations.
- **Untrusted Account Notes**: Data in notes or retrieved text is strictly confined to the `retrieved_evidence` or `task_context` and cannot inject commands or override `system_instructions` or `policies`.
- **No LLM or External calls**: The package is deterministic and runs entirely locally.
