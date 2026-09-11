# Chapter 15: Cost and Latency Optimization

## Chapter purpose

The V10 workflow is reliable enough to optimize and — since Chapter 14 —
instrumented enough to prove that an optimization worked. This chapter spends that
evidence twice. Cost optimization asks the workflow to do less work; parallel
execution asks it to wait less while doing the same work. Both are answered from
the same traces, tested against the same golden dataset, and accepted only under
the same quality gate.

They are one chapter because they are one discipline: measure, change one thing,
rerun, and keep the change only if the proof holds.

## Product version

**Starting point:** V10 — operationally observable graph  
**Result:** V11 — cost- and latency-optimized graph

## Engineering question

> Which work truly requires expensive intelligence, and which of what remains is
> genuinely ordered?

## Learning objectives

By the end of this chapter, the reader should be able to:

- calculate cost per attempted and successful account package;
- attribute model calls and tokens to workflow nodes;
- replace deterministic model work with code;
- choose models by task SLO rather than status;
- reduce accumulated context at handoffs;
- set node and workflow budgets; and
- prove optimization without accepting a quality regression;
- identify independent work from critical-path evidence rather than intuition;
- fan out and join with explicit state isolation and a partial-result policy; and
- prove concurrency from a trace rather than from the shape of the code.

## 15.1 Optimize the successful outcome

Cost per invocation can be misleading when cheap runs fail more often. The
primary measure is:

```text
total cost of evaluated runs / number of runs meeting the release gate
```

Track latency, quality and safety alongside cost. A cheaper workflow that creates
more human rework may be more expensive operationally.

## 15.2 Model right-sizing

Use a stronger model for ambiguous qualification, evidence synthesis and nuanced
outreach. Begin with a lower-cost model for extraction, classification, routing,
formatting or first-pass review when it meets the task SLO. Escalate only under a
measured condition.

Model choice is recorded per node in the manifest so a result can be reproduced.

## 15.3 Deterministic nodes

The workflow does not need a model to:

- validate schemas;
- calculate scores from fixed rules;
- enforce budgets;
- route known enumerations;
- verify required citations are present;
- format file paths; or
- assemble a stable JSON manifest.

Moving these tasks into functions improves predictability while reducing calls.

## 15.4 Context is positional cost

Later agents often receive everything produced earlier. A final formatter can
become the most expensive node because it pays for the accumulated conversation.
V10 replaces raw handoffs with typed summaries and artifact references.

Each node should receive:

- the business rules it needs;
- the accepted evidence it may cite;
- the immediate task contract; and
- the minimum state required to complete that task.

It should not receive an entire session simply because the runtime can provide it.

## 15.5 Compression, caching and reuse

Context compression and model context caching can reduce repeated processing when
the input is stable and eligible. They do not replace data freshness rules. A
cached research result must still carry source, retrieval time, tenant, policy and
invalidation conditions.

Book 1 introduces controlled reuse; Book 2 develops enterprise cache ownership,
cross-session knowledge and multi-tenant isolation.

## 15.6 Optimization experiment

Change one material variable at a time:

1. baseline V9;
2. replace one deterministic model step;
3. rerun the same cases;
4. right-size one model;
5. rerun;
6. shorten one handoff;
7. rerun; and
8. accept only changes that meet quality, safety and latency gates.

## 15.7 The candidate branches

For a validated account request, these enrichment tasks can often begin from the
same input:

- company and product research;
- contact and role research;
- competitive signals;
- technology-stack signals; and
- recent intent or event signals.

Qualification must wait for the join because it depends on the combined evidence.
Drafting must wait for qualification and approved claims. Human approval must wait
for the final draft.

## 15.8 Fan-out and join

```text
validated account
   ├── company research ──────┐
   ├── contact research ──────┤
   ├── competitor research ───┼→ evidence join → validate → qualify
   ├── technology research ───┤
   └── intent signals ────────┘
```

The V10 graph uses parallel routes rather than asking one coordinator to invent
concurrency. The join receives typed outputs and records missing or failed branches.

## 15.9 State isolation

Every branch writes a distinct output. Parallel agents must not append to the same
unprotected collection or overwrite a shared key. The join owns the combined
evidence package.

This rule makes race conditions visible during design instead of intermittent in
production.

## 15.10 Partial failure

A failed optional branch may produce `UNAVAILABLE` and allow qualification to
continue with reduced evidence. A failed required branch routes to retry, defer or
human review. The policy is deterministic and recorded in the artifact.

Parallelism must not turn missing evidence into invisible absence.

## 15.11 Proving concurrency

Do not infer concurrency from the diagram. In the trace, the parallel parent
duration should approximate the longest child, not the sum of all children.
Compare:

- critical-path duration;
- branch durations;
- join duration;
- aggregate tokens and model calls;
- error rate; and
- final evaluation score.

Concurrency usually reduces elapsed time without reducing token cost. It can also
increase burst demand and rate-limit risk.

## 15.12 Graph routes versus `ParallelAgent`

`ParallelAgent` is a compact representation of fan-out. The V10 product uses graph
parallel routes because it also needs typed branch outputs, explicit join behavior,
conditional handling of missing branches and later composition with human input
and loops.

## Hands-on lab: Spend less, and wait less

Work the halves in order. The second is only answerable once the first is done.

**Reduce cost**

1. Read per-node token, call and latency totals from the Chapter 14 traces.
2. Rank nodes by cost contribution.
3. Identify one deterministic model call.
4. Replace it with a function node.
5. Introduce a lower-cost model for one bounded task.
6. Summarize one oversized handoff.
7. Set iteration and token budgets.

**Reduce elapsed time**

1. Capture the V9 trace and identify the critical path.
2. Mark data dependencies between enrichment tasks.
3. Choose at least two independent branches.
4. Give every branch a typed output and distinct state ownership.
5. Add the fan-out and join routes.
6. Simulate one branch failure.
7. Verify required and optional failure policies.
8. Compare sequential and parallel traces.
9. Rerun the golden evaluation set.

**Prove both**

1. Run the unchanged golden dataset.
2. Report cost per successful SDR package, elapsed time, and any regression.

## Evaluation checklist

- Is cost attributed by node and by successful result?
- Are model choices tied to task SLOs?
- Did deterministic code replace suitable model work?
- Are handoffs smaller and typed?
- Are caches tenant-safe and freshness-aware?
- Are budgets visible and enforced?
- Is every parallel branch genuinely independent?
- Does each branch have separate state ownership?
- Is the join explicit and validated?
- Are missing branches visible?
- Is partial failure policy deterministic?
- Does trace arithmetic prove overlap?
- Did p50 and p95 latency improve?
- Did quality, cost or rate-limit behavior regress?
- Did the same evaluation cases continue to pass?

## Chapter checkpoint

WidgetWare V11 spends intelligence selectively and waits only where waiting is
required. Chapter 14's instrumentation carries over unchanged: the trace shows
genuine concurrency, the join is visible rather than inferred, and every cut is
attributable to a measurement rather than a preference.

The product is fast, measured and correct for one account at a time. It has never
been asked to work through many.

## Bridge to Chapter 16

Chapter 16 wraps the unchanged, evaluated single-account graph inside a dynamic
outer workflow with durable decisions, checkpoints and resume.
