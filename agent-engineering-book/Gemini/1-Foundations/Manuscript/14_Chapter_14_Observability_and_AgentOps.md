# Chapter 14: Observability and AgentOps

## Chapter purpose

Basic trace and run identifiers have existed since the monolith. This chapter
deepens them into an operational system, now that the workflow topology is stable
enough to produce meaningful per-stage evidence. The objective is to explain
behavior, not merely accumulate logs — and to produce the per-node cost, latency
and dependency evidence that the next two chapters spend.

## Product version

**Starting point:** V9 — controlled refinement loop  
**Result:** V10 — operationally observable graph

## Engineering question

> Can an operator explain what happened, why it happened, what it cost and what
> should happen next?

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish ADK events from OpenTelemetry spans;
- correlate request, invocation, session, account and artifact identifiers;
- read sequential, parallel and loop shapes from traces;
- attribute latency, tokens, calls and failures by node;
- design useful structured logs and metrics;
- build SLO-oriented dashboards and alerts;
- protect sensitive content in telemetry; and
- separate live traces from replayed operational narratives.

## 14.1 Events and spans answer different questions

ADK events describe conversation and state changes. Spans describe timed,
parented execution. Events can show what an agent produced; traces show what ran,
for how long and inside which parent operation.

Operators need both, connected by stable identifiers.

## 14.2 Correlation contract

Every run records:

- `request_id`;
- `invocation_id`;
- `session_id`;
- `account_id`;
- `workflow_version`;
- `manifest_id`;
- `trace_id`; and
- output artifact identifier.

The identifiers allow an evaluation failure to lead to the exact trace, manifest,
configuration and artifact without searching by prompt text.

## 14.3 Reading workflow shapes

For a sequential parent, duration tends toward the sum of children. For a parallel
parent, it tends toward the longest child. A loop trace must make iteration number,
review result and exit decision visible. A human-input pause should not appear as
unexplained model latency.

Appendix 02 provides a measured multi-agent example and a detailed reading
checklist.

## 14.4 Logs

Structured logs capture decisions and boundaries:

- node started and completed;
- validation result;
- route selected;
- tool outcome classification;
- retry and budget decisions;
- review decision;
- human approval state; and
- final status.

Do not log secrets, complete sensitive payloads or unrestricted prompt content.

## 14.5 Metrics and SLOs

Useful measures include:

- successful account packages;
- qualification contract-validity rate;
- evidence-coverage rate;
- unsupported-claim rate;
- approval-compliance rate;
- p50 and p95 completion latency;
- cost per successful package;
- loop iterations;
- tool failure rate; and
- deferred or escalated accounts.

An alert should correspond to an action. A dashboard is not an operating model by
itself.

## 14.6 Content capture and access

Telemetry is a data product with readers, retention and risk. Capture full model
content only when justified and authorized. Prefer bounded attributes and artifact
references. Trace-write permission does not prove that the writer executed the
real workflow, so replayed or synthetic telemetry must be labeled.

## 14.7 Per-agent economics

Token attribution often reveals that a late, apparently simple node is expensive
because it receives accumulated context. This is the finding Chapter 15 acts on,
both when it sets context budgets and when it uses the same per-node timing
evidence to decide which work is genuinely independent.

## Hands-on lab: Operate the complete graph

1. Instrument the V9 invocation and every material node.
2. Add stable correlation identifiers.
3. Emit structured decision logs.
4. Export traces to Cloud Trace.
5. Create metrics for SLOs and business outcomes.
6. Build a minimal Cloud Monitoring dashboard.
7. Add one actionable alert.
8. Run success, partial-failure, loop-exhaustion and approval cases.
9. Explain each outcome from telemetry without reading the code.

## Evaluation checklist

- Can an operator trace a failed evaluation to one invocation?
- Can the trace distinguish sequential, parallel and loop work?
- Are route and exit decisions visible?
- Are latency, tokens and calls attributable by node?
- Are sensitive contents intentionally excluded?
- Does each alert name an operator response?
- Are replayed traces labeled as reconstructed evidence?

## Chapter checkpoint

WidgetWare V10 can be operated and explained. Every node now reports what it cost,
how long it took and what it decided. That evidence is not an end in itself: it is
the input to the next two chapters, which are the first in the book that may not
be worth doing at all if the measurements say otherwise.

## Bridge to Chapter 15

Chapter 15 spends this evidence. With per-node token and latency attribution in
hand, it removes unnecessary model work, right-sizes intelligence and shortens
context — and can prove the result rather than assert it.

