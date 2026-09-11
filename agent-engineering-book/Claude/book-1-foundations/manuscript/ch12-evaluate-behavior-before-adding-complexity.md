# Chapter 12 — Evaluate Behavior before Adding Complexity

> **Status: outline.**

**Starting point:** V7 — explicit workflow
**Result:** V8 — measured behaviour and a regression baseline

---

## 12.1 Current state and observed limitation

Seven versions. Every one claimed an improvement, and every claim rested on
a test of the thing that version changed: V6 proved product claims are
grounded, V7 proved failures are attributable.

**No version has been measured against another on the same dimensions.**

Chapter 2 named this: a system that *feels* better, demos well, and produces
one nicer draft is not a system that has been shown to be better. V7 may
have regressed something nothing tests.

## 12.2 Engineering question

> Is V7 actually better than V1 — and on which dimensions is it worse?

The second half is not rhetorical. An evaluation that can only find
improvement is not an evaluation.

## 12.3 Architectural decision

Build a **golden dataset**, a set of **deterministic assertions**, and a set
of **model-judged rubrics**, run by a **small evaluation runner owned by
this repository**, on top of `pytest`.

Keep deterministic and judged results **strictly separate**, reported side
by side and never averaged into one number.

Include **adversarial cases**: prompt injection, and poisoned retrieved
content.

## 12.4 Two kinds of question

| | Answers | Cost | Noise |
|---|---|---|---|
| **Deterministic assertion** | Is the contract valid? Was the right route taken? Did the loop stop? | ~0 | none |
| **Model-judged rubric** | Is this draft any good? Is the reasoning sound? | a model call | real |

Averaging a 1.0 schema-validity rate with a 0.72 draft-quality score
produces 0.86, which describes nothing. They are reported separately, and a
release gate may require both — different thresholds, different meanings.

## 12.5 Evaluation dimensions

Every dimension the brief requires, each mapped to its kind:

| Dimension | Kind |
|---|---|
| Contract validity | deterministic |
| Tool selection | deterministic |
| Tool arguments | deterministic |
| Route selection | deterministic |
| Evidence attribution | deterministic |
| Unsupported claims | deterministic (prohibited-claim list) |
| Qualification accuracy | deterministic vs. labelled expectation |
| Refusal and escalation behaviour | deterministic |
| Draft quality | judged |
| Loop termination | deterministic (from Ch. 13) |
| Regression vs. previous version | both, reported per dimension |

Nine of eleven are deterministic. That ratio is the chapter's quiet
argument: **most of what people reach for an LLM judge to answer can be
asserted.**

## 12.6 Alternatives considered

**Promptfoo, DeepEval and Langfuse datasets together.** Excluded by the
brief, correctly. Three evaluation systems means three places a case can
live and three reasons a result cannot be reproduced. One runner, in the
repository, readable.

**An LLM judge for everything.** Rejected — noisy, expensive, and it hides
the fact that most questions here have exact answers.

**Human evaluation only.** The gold standard and unscalable. Used in Book 1
for whether the *product* is right, not whether the code works.

**Evaluate from Chapter 5 onward.** Tempting, and it was considered. Rejected
because V1–V6 have no stable stage vocabulary to express route-selection or
per-node dimensions in — the evaluation would have been rewritten at V7
anyway, and a baseline that changes definition is not a baseline.

## 12.7 Trade-offs

Stated plainly: **an evaluation set is a target, and targets get overfit.**
Thirteen accounts and a handful of adversarial cases can be satisfied by a
system that is excellent on exactly those. The defences are partial —
treat the set as a regression guard rather than an optimisation objective,
refresh it when the product changes, and never tune a prompt against a
single failing case without asking what class it represents.

Judged scores drift when the judge model changes. The judge's model id goes
in the manifest, and a judge change invalidates comparison across versions.

## 12.8 Implementation walkthrough

- `evals/cases/golden_v1.yaml` — per account: expected facts, known signals,
  expected qualification decision with reasoning, prohibited claims,
  compliant and non-compliant draft examples.
- `evals/cases/adversarial.yaml` — injected instruction in a fetched page;
  poisoned corpus passage asserting a false product capability.
- `app/evaluation/runner.py` — executes cases, collects per-dimension
  results, writes a comparison report against a stored baseline.
- `app/evaluation/assertions.py` — the deterministic checks.
- `app/evaluation/rubrics.py` — written rubrics; the judge returns a typed
  `ReviewResult` (Chapter 8), because a judge with no contract is a judge
  whose output cannot be aggregated.
- `evals/baselines/` — one stored result per version tag.

## 12.9 The poisoned corpus case

Chapter 6 handled an instruction injected into a *fetched page*. This adds
the harder case: a passage in **our own corpus** asserting a capability
WidgetWare does not have.

Chapter 10's grounding will faithfully cite it. Retrieval cannot tell truth
from confident falsehood in a governed corpus — it can only tell you where
a claim came from. The defence is corpus governance, and the honest
statement is that **RAG moves the trust problem rather than solving it.**

## 12.10 Failure demonstration

Run the full evaluation across V1, V4, V6 and V7. Publish the table
including regressions. Expect V7 to be worse on at least one dimension —
likely latency, possibly draft fluency, since decomposition removes context
each node can see.

Reporting a regression the book then chooses to accept, with reasoning, is
more instructive than a table of green cells.

## 12.11 Evidence of improvement

The V1 → V7 comparison table, per dimension, with regressions named and
either fixed or explicitly accepted.

## 12.12 Updated run manifest

`version_tag: "v8-evaluated"`, dataset version and hash, judge model id,
per-dimension scores.

## 12.13 What remains unresolved

Evaluation now detects weak drafts. The system still emits them — detection
without correction just tells you sooner that the output was poor.

## 12.14 Exercises

1. Add a golden case for an account that should be `INSUFFICIENT` rather
   than qualified or disqualified. Does the system get it right? Most
   systems collapse `INSUFFICIENT` into `DISQUALIFIED`.
2. Change the judge model and re-run the judged dimensions. How much moved?
   What does that tell you about comparing scores across versions?
