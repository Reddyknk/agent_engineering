---
name: renewal-advisor
description: "Helps with WidgetWare customer success renewal work including renewal discount approval routing, renewal timing and milestones, risk escalation for churn, legal, security, and regulated customers, deterministic quote calculations, and approval-ready renewal briefs. Excludes product troubleshooting or non-renewal technical support."
---

# Renewal Advisor Skill

Operating procedure for WidgetWare customer success renewal analysis, approval routing, financial calculations, and risk escalation.

## Scope & Intent Classification

Use this skill when helping Customer Success Managers (CSMs) with renewal tasks.
Do **not** use this skill for general product troubleshooting, feature requests, or non-renewal technical support.

Classify the user request into one of the following intents and load **only** the minimum resource required:

1. **Discount Approval & Routing**:
   - Intent: User asks about discount approval thresholds or approval routing.
   - Resource: Load `references/discount-policy.md`.

2. **Renewal Timing & Auto-Renewal**:
   - Intent: User asks about renewal timing, timeline milestones, or auto-renewal process.
   - Resource: Load `references/renewal-process.md`.

3. **Risk Escalation, Legal, Security & Regulated Customers**:
   - Intent: User asks about high churn risk, regulated customer compliance, SOC 2 claims, security, or legal contract language.
   - Resource: Load `references/risk-escalation.md`.

4. **Approval-Ready Brief**:
   - Intent: User requests an approval brief or renewal brief for a customer.
   - Resource: Load `assets/renewal-brief-template.md` along with any relevant policy references (`references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`).

5. **Dollar Discount & Net ARR Math**:
   - Intent: User asks for dollar discount amounts or net ARR calculations.
   - Resource: Execute `scripts/calculate_quote.py` with `--arr` and `--discount-pct`. Combine with `references/discount-policy.md` if approval routing is also requested.

---

## Operating Rules & Safety Boundaries

### Minimum Resource Rule
- Load **only** the minimum resource file needed for the user's specific intent.
- Do not load unnecessary references or scripts.

### Missing Input Rule
- If ARR, discount percentage, or other required input is missing for calculations or routing, ask the user for the missing input before performing calculations.

### State Language Rule
- Strictly preserve commercial state distinction:
  - Use `requested` for requested commercial changes or discounts.
  - Use `routed to <role>` after identifying the approval authority.
  - Use `approved` ONLY when explicit approval evidence is present in context. Never invent approval status.

### Citations Rule
- Cite exact source file paths (e.g. `references/discount-policy.md`) for all policy rules and threshold guidance provided in your response.

### Unsupported Questions & Refusals Rule
- If the user asks for unsupported compliance assurances (e.g. SOC 2 control coverage claims not established by policy) or unsupported commitments, state clearly that provided sources do not establish the claim.
- Use `references/risk-escalation.md` and route/escalate the request to the appropriate team (Legal, Security/Reliability, or CS Leadership).

### Missing Resource Fallback Rule
- If a named resource file cannot be loaded, notify the user which exact resource file is missing and escalate to Customer Success leadership.

