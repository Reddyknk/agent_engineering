# Chapter 13: Graph Loops and Controlled Refinement

## Chapter purpose

Version 4 can detect weak output, but detection alone does not improve the SDR
package. This chapter closes the feedback path with a bounded inner loop. The
system may revise only the rejected artifact, preserve accepted evidence and stop
for a reason it can name.

## Product version

**Starting point:** V8 — reliable graph with quality detection  
**Result:** V9 — controlled refinement loop

## Engineering question

> What should happen after the system detects a defect?

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish detection from correction;
- model generate-review-revise as graph routes;
- preserve accepted work across iterations;
- define deterministic termination conditions;
- enforce iteration, token, latency and tool budgets;
- stop on approval, exhaustion, non-retryable failure or human escalation; and
- evaluate whether the loop improves cost-adjusted quality.

## The WidgetWare increment

The V9 loop operates on one account package:

```text
generate or revise
  → review
  → route
      PASS       → continue to human approval
      REVISE     → revision node → review
      BLOCKED    → human escalation
      EXHAUSTED  → stop with best artifact and reasons
```

This is the **inner quality loop**. It must not be confused with Chapter 16's
outer loop, which selects and processes multiple accounts.

## 13.1 A loop needs a contract

`max_iterations` prevents infinity; it does not define success. The loop contract
must specify:

- artifact being improved;
- immutable inputs and accepted evidence;
- evaluator schema;
- allowed revision operations;
- pass threshold;
- blocking conditions;
- budgets; and
- terminal outcomes.

## 13.2 Structured reviewer output

The reviewer returns machine-actionable feedback:

```json
{
  "decision": "REVISE",
  "score": 0.76,
  "blocking_issues": ["unsupported ROI claim"],
  "preserve": ["qualification decision", "source list"],
  "revision_guidance": ["remove the ROI claim or attach evidence"]
}
```

The routing node validates this object and chooses the next edge. The reviewer
does not control routing by producing persuasive prose.

## 13.3 Preserve accepted work

The revision agent receives the current draft, explicit defects and a list of
content to preserve. It does not rerun account research unless the defect is
missing evidence. This reduces cost and prevents an accepted qualification from
changing accidentally while tone is revised.

## 13.4 Termination

The loop ends with one of five named outcomes:

1. **PASS** — quality gate met;
2. **BLOCKED** — evidence or policy prevents safe completion;
3. **ESCALATE** — human judgment is required;
4. **BUDGET_EXHAUSTED** — iteration, token, time or tool budget reached; or
5. **FAILED** — non-retryable technical error.

Each outcome becomes evidence in the run manifest and final artifact.

## 13.5 Graph loop versus `LoopAgent`

`LoopAgent` is useful for learning the iterative-refinement pattern and for a
compact fixed loop. The V9 product uses graph loop routes because the loop has
multiple terminal outcomes, deterministic budget checks and an explicit human
escalation path.

## Hands-on lab: Close the feedback path

1. Select V8 cases the evaluator rejects consistently.
2. Define the reviewer contract and pass threshold.
3. Add deterministic routing and budget nodes.
4. Implement a revision agent that preserves accepted fields.
5. Add pass, blocked, exhausted and escalation exits.
6. Trace every iteration and record its cost.
7. Prove the loop stops when the first revision passes.
8. Prove it stops at the hard limit when quality does not improve.
9. Compare V8 and V9 pass rate, variance, latency and cost.

## Evaluation checklist

- Is success defined independently of iteration count?
- Does the reviewer return structured feedback?
- Does deterministic code select the route?
- Is accepted evidence preserved?
- Are all budgets enforced?
- Is there a human escalation path?
- Can the final result explain why the loop stopped?
- Does improved pass rate justify the added latency and cost?

## Chapter checkpoint

WidgetWare V9 detects and corrects bounded quality defects. The loop earns its
place only if the unchanged evaluation set shows a worthwhile improvement. The
next question is whether all steps and iterations deserve the same model and the
same amount of context — and, before that, whether the product can even answer
that question with evidence rather than intuition.

## Bridge to Chapter 14

Chapter 14 makes the graph explain itself: per-node traces, logs, metrics and cost
attribution. Nothing about V9's behavior changes. What changes is that the next
two chapters can be argued from measurement instead of assertion.

