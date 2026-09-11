# Chapter 13 — Improve Quality with a Bounded Review Loop

> **Status: outline.**

**Starting point:** V8 — measured behaviour
**Result:** V9 — bounded generate → review → revise

---

## 13.1 Current state and observed limitation

Chapter 12's evaluation gives a draft-quality distribution. Some drafts
score well. A meaningful tail does not — generic openings, a proof point
that does not match the signal, a claim technically supported but
overstated.

The system emits all of them identically. **Detection without correction
tells you sooner that the output was poor.**

The reviewer already exists: Chapter 12 built a rubric judge. V8 uses it to
score after the fact. V9 puts it in the loop.

## 13.2 Engineering question

> Can draft quality improve without the system running forever?

Both halves are the requirement. "Improve quality" alone is satisfied by an
unbounded retry, which is Chapter 1's runaway-loop failure pattern.

## 13.3 Architectural decision

Add a **generate → review → revise cycle** in the graph, with:

- an explicit **maximum iteration count**;
- a **quality threshold** for exit;
- a **recorded stop reason** on every path;
- an **escalation path** when the threshold is not reached;
- **prior evidence preserved** across iterations.

The exit condition is a conditional edge — visible code, testable without a
model. This is the argument for expressing the loop in the graph rather than
as a loop construct with a limit parameter: *the termination logic is the
part most likely to be wrong, so it should be the part most easily read.*

## 13.4 The subgraph

```text
draft_outreach → review_draft → review_route
                                   │
   ┌───────────────────────────────┼──────────────────────────┐
   │                               │                          │
   ▼                               ▼                          ▼
revise_draft                  prepare_approval            escalate
(→ review_draft)              threshold_met          max_iterations |
                                                     no_improvement
```

## 13.5 Stop reasons, enumerated

Every run records exactly one:

| Stop reason | Meaning |
|---|---|
| `threshold_met` | Score reached the exit threshold |
| `max_iterations` | Iteration limit hit; best draft escalated |
| `no_improvement` | Score failed to improve; further iterations are waste |
| `escalated` | Reviewer found an unfixable problem — an unsupported claim |

`no_improvement` deserves emphasis. A loop that stops only at its iteration
limit will burn its full budget on a draft the second pass already told you
would not get better. Detecting stagnation is separate from bounding
iteration, and most implementations conflate them.

## 13.6 Independence of the reviewer

The reviewer is a **separate node with its own contract**, not a
self-critique appended to the generation call.

Asking a model to critique text in the same call that produced it yields
agreeable critique — it has already committed to the output. A separate node
with a `ReviewResult` contract, a written rubric and no access to the
generator's reasoning produces findings that are actually actionable.

Cost: an extra model call per iteration. Named, accepted, measured.

## 13.7 Preserving evidence across iterations

A revision must not lose the evidence the original was built on. The
reducer on `evidence` accumulates; `revise_draft` reads the full set and
receives the reviewer's findings, and may not introduce a claim without a
resolvable `evidence_id`.

Without this, revision degrades into rewriting — each pass drifting further
from what the sources support while scoring better on fluency. That failure
is subtle, common, and exactly what an evaluation measuring only quality
will reward.

## 13.8 Alternatives considered

**Unbounded retry until the threshold.** Rejected: Chapter 1's failure
pattern. It terminates via your bill.

**A single fixed revision pass.** Simpler, no termination logic, and worth
measuring — Chapter 12's data will show whether pass two carries most of the
gain. If it does, say so and keep the loop anyway for the escalation path,
or drop it. Let the evidence decide, and record which way it went.

**Self-critique in the generation call.** Rejected per §13.6.

**Raising the bar in the generation prompt instead.** Tried first, and
should be. If a better prompt closes the gap, no loop is needed — the cheapest
change that works. The loop is justified only by the residual tail.

## 13.9 Trade-offs

Latency and cost scale with iterations: a three-iteration cap can nearly
triple the drafting stage. The threshold is a business decision — how good
is good enough — and belongs in configuration, reviewable by the sales lead,
not in code.

A quality threshold is a proxy. Optimising against a judge produces drafts
the judge likes.

## 13.10 Implementation walkthrough

- `app/nodes/review_draft.py` — rubric-based reviewer returning
  `ReviewResult` with score, findings and `is_fixable`.
- `app/nodes/revise_draft.py` — regenerates from findings plus preserved
  evidence.
- `app/graph/routes.py` — `review_route`, a pure function of
  `(score, iteration, previous_score, is_fixable)`. Every branch testable
  with no model call.
- `config/review.yaml` — threshold, max iterations, stagnation delta.

## 13.11 Tests and evaluation

- Termination on every case, including adversarial. **No path runs forever.**
- Each stop reason is reachable and is recorded exactly once.
- A draft below threshold with `is_fixable=false` escalates immediately
  rather than consuming iterations.
- Evidence set is non-decreasing across iterations.
- A revision introducing an unsupported claim is rejected.
- Draft-quality distribution improves against the V8 baseline.

## 13.12 Failure demonstration

Construct a draft that cannot reach the threshold — an account with genuinely
thin evidence. Show the loop stopping at `max_iterations`, escalating the
best attempt with its findings attached, and **not** silently emitting the
failing draft as though it had passed.

Then break the stagnation check and re-run to show budget consumed for
nothing.

## 13.13 Evidence of improvement

Draft-quality distribution V8 → V9, with the tail specifically. Termination
100%. Iteration count distribution, and cost per account as the price paid.

## 13.14 Updated run manifest

`version_tag: "v9-review-loop"`, threshold, max iterations, per-run
iteration count and stop reason.

## 13.15 What remains unresolved

The system produces good, sourced, grounded, reviewed briefs — and nobody
can explain a single run after the fact. There is no trace, state dies with
the process, and the only way to run it is `pytest`.

## 13.16 Exercises

1. Set max iterations to 1 and re-run. How much of the improvement came from
   the first revision? Was the loop worth building?
2. Remove the evidence-preservation rule and run five iterations on one
   account. Read the final draft against the original sources.
