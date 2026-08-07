# Acceptance Criteria

The WidgetWare SDR context package implementation is complete and accepted when the following criteria are met:

## Configuration
- `products.yaml`, `icp.yaml`, and `policies.yaml` exist in the `config/` directory.
- At least two WidgetWare product offerings are configured (our implementation contains three: Plant Operations Platform, Industrial AI Accelerator, and Predictive Maintenance Engine).
- `icp.yaml` contains scale thresholds, preferred/excluded industries, preferred regions, buying signals, and required fields.
- `policies.yaml` defines evidence classifications, prohibited actions, and explicit human approval boundaries.

## Agent Instructions & Behavior
- System instructions are inspectable and exposed via a standard function `get_system_instructions()`.
- Instructions are precise, observable, and prohibit guessing, invented facts, and unauthorized external actions.

## Context Builder
- The context builder function `build_context` returns a dictionary containing five separate layers:
  1. `system_instructions`
  2. `business_context`
  3. `task_context`
  4. `retrieved_evidence`
  5. `state`
- Configuration files are loaded dynamically and produce clear errors if missing.
- Evidence records preserve complete provenance (claim, classification, source name, source URL, retrieval date, and excerpt).
- Unknown or missing account information remains `unknown` or `None`, and the system does not invent values.
- Task context or user input (such as account notes) cannot override system policies or system instructions (protection against prompt injection).
- All input objects remain unmutated (immutability).

## Scenarios & Test Suite
- Scenario fixtures exist for:
  1. Qualified Account (`qualified_account.yaml`)
  2. Unqualified Account (`unqualified_account.yaml`)
  3. Insufficient Evidence (`insufficient_evidence.yaml`)
  4. Prompt Injection (`prompt_injection.yaml`)
  5. Conflict Evidence (`conflict_evidence.yaml`)
- Automated unit and scenario tests cover configuration loading, instruction contents, context builder layers, immutability, safety constraints, and scenario outputs.
- All tests pass cleanly under `pytest`.

## Out of Scope
- No Google ADK agent exists.
- No LLM API calls are made.
- No live search or web crawling exists.
- No database persistence is used.
- No email or social-message delivery is implemented.
- No external side effects occur.
