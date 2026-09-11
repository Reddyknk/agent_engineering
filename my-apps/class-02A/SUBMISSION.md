# Class 02A Submission

## Student
- Name: Agentic Engineer
- GitHub: Reddyknk
- Branch / commit: main

---

# Test Results & Local Grader Summary

- **Total Score**: 98 / 98 (100% Pass)
- **Pytest Suite**: All tests passing cleanly (`python -m pytest -q`)
- **Preflight Check**: Offline and Live Online model checks passed (`python scripts/preflight.py --online`)

### Grader Breakdown Table
- No placeholder tasks remain in SKILL.md: `PASS` (10/10)
- L2 routes exact path `references/discount-policy.md`: `PASS` (6/6)
- L2 routes exact path `references/renewal-process.md`: `PASS` (6/6)
- L2 routes exact path `references/risk-escalation.md`: `PASS` (6/6)
- L2 routes exact path `assets/renewal-brief-template.md`: `PASS` (6/6)
- L2 routes exact path `scripts/calculate_quote.py`: `PASS` (6/6)
- L2 requires minimum-resource loading: `PASS` (8/8)
- L2 handles missing inputs: `PASS` (8/8)
- L2 requires citations: `PASS` (8/8)
- L2 handles unsupported questions: `PASS` (8/8)
- L2 preserves requested/routed/approved states: `PASS` (8/8)
- `submission.md` completed: `PASS` (10/10)
- Full pytest suite passes: `PASS` (8/8)

---

# Baseline observations

## L1
Initial L1 description was vague ("Helps with renewals."), which was too broad and failed to specify specific intent capabilities (discounting, timing, risk escalation, quotes, briefs) or product troubleshooting exclusions.

## L2
Initial L2 procedure body in SKILL.md was an unfinished placeholder, missing intent classification, explicit L3 resource paths, input validation rules, state language rules, citation rules, and refusal instructions.

## L3
Initial L3 loading behavior was unguided; the agent did not reliably target the minimum necessary reference file (`references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, or `scripts/calculate_quote.py`).

---

# Final trace evidence

## Case A
- Predicted L3: `references/discount-policy.md`
- Observed L1: Matched `renewal-advisor` skill via L1 description.
- Observed L2: Executed L2 procedure and selected `references/discount-policy.md`.
- Observed L3: Loaded `references/discount-policy.md` exclusively.
- Final result: Identified 12% requested discount falls in >10%–15% band, correctly routed to Customer Success Director with `requested` / `routed` state language.
- Unnecessary resources loaded: None (0 unnecessary resources loaded).

## Case B
- Predicted L3: `references/renewal-process.md`
- Observed L1: Matched `renewal-advisor` skill via L1 description.
- Observed L2: Executed L2 procedure and selected `references/renewal-process.md`.
- Observed L3: Loaded `references/renewal-process.md` exclusively.
- Final result: Identified 75 days to renewal falls in 60–89 day milestone window; advised CSM to validate commercial path, decision process, and auto-renewal notice requirements.
- Unnecessary resources loaded: None (0 unnecessary resources loaded).

## Case C
- Predicted L3: `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Observed L1: Matched `renewal-advisor` skill via L1 description.
- Observed L2: Executed L2 procedure and identified cross-resource intent requirements.
- Observed L3: Loaded `references/discount-policy.md`, `references/renewal-process.md`, and `references/risk-escalation.md`.
- Final result: Correctly addressed high churn risk (CS leadership), 10-day renewal urgency (0–29 days), 18% discount route (VP Customer Success), and auto-renewal removal request (Legal review path).
- Unnecessary resources loaded: None (0 unnecessary resources loaded).

## Case D
- Predicted L3: `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md`
- Observed L1: Matched `renewal-advisor` skill via L1 description.
- Observed L2: Executed L2 procedure for brief generation intent.
- Observed L3: Loaded `assets/renewal-brief-template.md`, `references/discount-policy.md`, and `references/renewal-process.md`.
- Final result: Generated structured renewal brief for Apex Manufacturing ($150k ARR, 15% discount routed to CS Director, 42 days remaining). Kept missing Executive Sponsor uninvented as requested.
- Unnecessary resources loaded: None (0 unnecessary resources loaded).

## Case E
- Predicted L3: `scripts/calculate_quote.py`, `references/discount-policy.md`
- Observed L1: Matched `renewal-advisor` skill via L1 description.
- Observed L2: Executed L2 procedure for deterministic math + discount routing intent.
- Observed L3: Executed `scripts/calculate_quote.py` and loaded `references/discount-policy.md`.
- Final result: Calculated exact discount amount ($11,040.00) and net ARR ($80,960.00) via script execution, and routed 12% discount to Customer Success Director.
- Unnecessary resources loaded: None (0 unnecessary resources loaded).

## Case F
- Predicted L3: `references/risk-escalation.md`
- Observed L1: Matched `renewal-advisor` skill via L1 description.
- Observed L2: Executed L2 procedure for unsupported compliance claim intent.
- Observed L3: Loaded `references/risk-escalation.md` exclusively.
- Final result: Applied safe abstention. Refused to invent SOC 2 control coverage claims, stated that supplied sources do not establish the claim, and escalated to Reliability/Security + Legal.
- Unnecessary resources loaded: None (0 unnecessary resources loaded).

---

# What I learned

## Skill vs resource
A **skill** provides the reusable logic, intent classification rules, and operating procedure for the agent (L2 in `SKILL.md`), whereas a **resource** provides the specific domain knowledge, document assets, or deterministic scripts (L3 files) loaded only when required for a specific task.

## L1 → L2 → L3 progressive disclosure
Progressive disclosure minimizes token usage and context clutter: L1 metadata allows the agent to discover the skill during initial routing; L2 instructions load the procedure when the skill is invoked; L3 resources load exact reference documents or scripts only when an intent specifically demands them.

## Why minimum-resource loading matters
Loading only the minimum required resource prevents context window bloat, reduces latency and LLM costs, and avoids confusing the model with irrelevant policy rules or competing constraints.

## Why deterministic math belongs in a script
LLMs can make arithmetic errors when performing multi-digit floating point operations in prose. Running deterministic math in Python scripts (`calculate_quote.py`) guarantees exact precision, reproducible quotes, and financial accuracy.

## Why safe abstention can be a correct answer
When customer requests ask for legal, security, or compliance commitments not supported by internal policy (such as unverified SOC 2 assurances), inventing an answer creates significant liability. Grounded refusal combined with human escalation is a correct and safe AI system outcome.

