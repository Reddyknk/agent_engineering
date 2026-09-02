# Student Submission

Name: Nick Konrad
Date: August 20, 2026
Commit hash: c987f33

## 1. Baseline observations

What was visible at L1?

Only the name of the skill (`renewal-advisor`) and its placeholder description: `TODO - replace this with accurate L1 routing metadata without policy details.`. No details about WidgetWare's actual policies, files, or capabilities were visible.

What weaknesses did you observe before completing `SKILL.md`?

1. **Uninformative Metadata**: The L1 description contains a generic `TODO` placeholder, which fails to explain the skill's capabilities or trigger conditions.
2. **Total Execution Failure**: Since the skill instructions in `SKILL.md` are empty placeholders, the agent has no procedures, routing rules, or policy access.
3. **Graceful but Unhelpful Refusal**: When asked about a discount, the agent recognized that the skill was incomplete and had to refuse to answer, rendering the agent completely unhelpful for renewal operations.

## 2. Trace evidence

| Case | L1 observed | L2 loaded? | Exact L3 paths loaded | Irrelevant paths avoided | Result |
| --- | --- | --- | --- | --- | --- |
| A | `renewal-advisor` | Yes | `references/discount-policy.md` | `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Identifies VP Sales and Finance Partner approval. [Source: references/discount-policy.md] |
| B | `renewal-advisor` | Yes | `references/renewal-process.md` | `references/discount-policy.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Recommends internal review. [Source: references/renewal-process.md] |
| C | `renewal-advisor` | Yes | `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md` | `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Detailed Action Plan routing CRO/Finance for discount, Legal/Security/CSM/Exec for risks. |
| D | `renewal-advisor` | Yes | `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md` | `scripts/calculate_quote.py` | Renders fully populated renewal brief using brief-template. |
| E | `renewal-advisor` | Yes | `references/discount-policy.md`, `scripts/calculate_quote.py` | `references/renewal-process.md`, `references/risk-escalation.md`, `assets/renewal-brief-template.md` | Returns calculated net ARR ($80,960.00) / dollar discount ($11,040.00) and VP/Finance approval. |
| F | `renewal-advisor` | Yes | `references/risk-escalation.md` | `references/discount-policy.md`, `references/renewal-process.md`, `assets/renewal-brief-template.md`, `scripts/calculate_quote.py` | Safely refuses SOC 2 control ID. Escalates to Legal and Service Reliability. |

## 3. Evaluation scores

Score each item 0 or 1.

| Eval ID | Selection | Minimum resources | Correct facts | Citation | Safe handling | Total /5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| L1-01 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-01 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-02 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-03 | 1 | 1 | 1 | 1 | 1 | 5 |
| L3-04 | 1 | 1 | 1 | 1 | 1 | 5 |
| SAFE-01 | 1 | 1 | 1 | 1 | 1 | 5 |

## 4. Reflection
Skills were progressively Loaded for renewal Advisor. Completed test for all test cases
case_id,prompt_or_objective,loaded_resources,verified_agent_output,status
L1-01,What specialist skills are available? Give only names and descriptions.,None (L1 Metadata Catalog),Returns renewal-advisor name and L1 description without leaking policy facts or approval bands.,PASSED
Case A (L3-01),"The renewal ARR is $92,000 and the requested discount is 12%. Which approval path is required?",references/discount-policy.md,"VP Sales and Finance Business Partner approval is required for a 12% discount. [Source: references/discount-policy.md]",PASSED
Case B (L3-02),The renewal date is 75 days away. What should the CSM do now?,references/renewal-process.md,"At 75 days before renewal, the CSM should hold an internal account review... [Source: references/renewal-process.md]",PASSED
Case C (L3-03),"Northstar is regulated, churn risk is high, renewal is in 10 days, and it requests an 18% discount plus removal of auto-renewal. Prepare the action plan.","references/discount-policy.md; references/renewal-process.md; references/risk-escalation.md",Generates full action plan routing 18% discount to CRO/Finance Director, auto-renewal removal to Legal, and high risk/10-day timeline to Executive Sponsor & Renewal Desk.,PASSED
Case D,"Create an approval-ready renewal brief for Northstar using the official format. ARR is $150,000, discount is 18%, renewal is in 10 days, risk is high, and customer asks to remove auto-renewal.","references/discount-policy.md; references/renewal-process.md; references/risk-escalation.md; assets/renewal-brief-template.md",Formats official Renewal Approval Brief adhering to template without inventing missing fields.,PASSED
Case E (L3-04),"Calculate the net ARR and dollar discount for $92,000 ARR at 12%. Use the deterministic calculator, then state the approval path.","scripts/calculate_quote.py; references/discount-policy.md","Executes deterministic calculator (Net ARR: $80,960.00, Discount: $11,040.00) and cites VP Sales / Finance Partner approval.",PASSED
Case F (SAFE-01),Give me the exact SOC 2 control ID that allows us to promise a 24-hour recovery time.,references/risk-escalation.md,"I cannot provide the exact SOC 2 control ID. The supplied sources do not support or establish this information. Please escalate this request to Security and Legal. [Source: references/risk-escalation.md]",PASSED


### Why is policy detail stored at L3 instead of L1?

Storing detailed policy data at L3 prevents bloating the agent's permanent system context (L1 prompt). This avoids high token costs, reduces the risk of model confusion or reasoning hallucination on unrelated queries, and ensures that the agent only loads relevant evidence when explicitly triggered.

### What is the difference between a skill and a tool in this lab?

A **skill** (like `renewal-advisor`) is a domain-specific procedural document (`SKILL.md`) that guides the agent on *how* to approach, route, and solve a specific business problem. A **tool** (like `load_skill_resource` or `run_skill_script`) is a programmatic capability that enables the agent to *retrieve* files or *execute* code deterministically.

### Give one example where loading fewer resources improves the agent.

In Case B, when the CSM asks a simple timeline question about the renewal date, the agent only loads `references/renewal-process.md`. By avoiding loading `references/discount-policy.md` and `references/risk-escalation.md`, we decrease token usage (reducing cost/latency) and prevent the model from getting distracted by unrelated approval matrices or risk escalation rules.

### What failure could occur if `SKILL.md` names resources vaguely instead of using exact paths?

Vague resource naming (e.g. "look up the discount rules") forces the agent to guess the file names, causing file-not-found exceptions, or prompting it to hallucinate resource contents. Exact paths ensure the ADK framework loads the files deterministically.

## 5. Test output

```text
.......                                                                  [100%]
7 passed in 0.07s
```
