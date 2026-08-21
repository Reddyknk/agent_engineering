---
name: renewal-advisor
description: Helps WidgetWare teams analyze enterprise software contract renewals, discount approval routing, commercial process timelines, risk escalation criteria, and construct renewal briefs.
---

# Renewal Advisor

This skill guides the agent in analyzing WidgetWare enterprise software contract renewals, routing discounts, managing timeline escalations, and formatting renewal briefs. Policy details are maintained in L3 resources and must be loaded selectively.

## When to use

Use this skill when asked about:
- Discount approval routing paths for renewals.
- Renewal timelines, milestones, and commercial process rules.
- Churn risk escalation, auto-renewal removal requests, SLA commitments, or compliance reviews.
- Constructing or formatting an official renewal approval brief.
- Deterministic quote calculations for net ARR and dollar discount amounts.

## When not to use

Do not use this skill for:
- Product troubleshooting or technical support.
- General sales qualification for new business (non-renewals).
- Auditing internal SOC 2 controls, compliance checklists, or security certifications.
- Constructing custom contract language or legal terms not defined in the policies.

## Required inputs

To complete renewal analysis or briefs, the following inputs are required:
- Customer Name
- Current ARR / List Renewal ARR
- Requested Discount Percentage
- Renewal Date or Days Remaining
- Churn Risk Level (e.g., High, Low)
- Customer contract requests (e.g., auto-renewal removal, service-level commitments)

If any of these required inputs are missing, do not assume or invent values. Politely ask the CSM for the missing information.

## Procedure

1. **Analyze query**: Identify the query type (discount approval, timeline process, risk escalation, renewal brief, or calculation).
2. **Collect inputs**: Extract all provided customer details. If required inputs are missing, ask the user to provide them.
3. **Route and load minimum resources**: Identify and load only the minimum necessary L3 resource paths for the query type (see the Resource routing map below). Avoid loading irrelevant resources.
4. **Perform calculation (if applicable)**: If the query requests net ARR or dollar discount calculations, run `scripts/calculate_quote.py` using `--arr` and `--discount-percent` arguments.
5. **Formulate policy analysis**: Evaluate the commercial parameters against the loaded references. Cite every finding.
6. **Generate renewal brief (if requested)**: Use the format from `assets/renewal-brief-template.md` and fill it in based strictly on the loaded evidence.
7. **Draft the response**: Adhere to the output contract, including citations and clear status words.

## Resource routing map

To ensure selective loading, route queries to the exact file paths as follows:
- Discount approval bands and rules: Load `references/discount-policy.md`
- Renewal timelines, milestones, and commercial rules: Load `references/renewal-process.md`
- Churn risk escalation, auto-renewal terms, SLA/recovery time routing: Load `references/risk-escalation.md`
- Renewal brief formatting template: Load `assets/renewal-brief-template.md`
- Precise quote or discount calculations: Execute `scripts/calculate_quote.py`

## Output contract

1. **Minimum resource loading**: Verify in your execution trace that you loaded only the minimum L3 resources required for the query.
2. **Strict facts**: Never invent approvals, deadlines, control IDs, or exceptions. Keep status words strictly limited to **requested**, **routed**, or **approved**.
3. **Citations**: Cite every policy conclusion using its exact relative path in the format `[Source: references/discount-policy.md]`, `[Source: references/renewal-process.md]`, `[Source: references/risk-escalation.md]`, or `[Source: assets/renewal-brief-template.md]`.

## Unsupported and missing-source behavior

If the user asks a question that is unsupported by the provided resources (such as requesting specific SOC 2 control IDs, security audit reports, or specific SLA recovery times):
1. State clearly that the supplied sources do not support or establish the requested information.
2. Identify the proper escalation route (e.g. Legal, Security, Service Reliability, or Policy Owner) as specified in `references/risk-escalation.md` or `references/discount-policy.md`.
3. Stop and do not invent any details.

## Examples

### Positive

Query: `The renewal ARR is $92,000 and the requested discount is 12%. Which approval path is required?`
Action: Load `references/discount-policy.md`. Cite the path.
Output: VP Sales and Finance Business Partner approval is required [Source: references/discount-policy.md].

### Negative

Query: `My WidgetWare application is showing a database connection error. Can you help?`
Action: Refuse to answer since technical product troubleshooting is out of scope.
Output: I cannot help with application troubleshooting. Please contact IT support.

### Ambiguous

Query: `Is a 20% discount okay for our renewal?`
Action: Ask for the list renewal ARR and check if the discount has been approved, explaining that a 20% discount requires CRO and Finance Director approval [Source: references/discount-policy.md], but must not be called "approved" until authorized.
