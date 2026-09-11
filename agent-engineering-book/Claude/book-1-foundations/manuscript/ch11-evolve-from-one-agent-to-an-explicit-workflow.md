# Chapter 11 — Evolve from One Agent to an Explicit Workflow

> **Status: outline.**

**Starting point:** V6 — grounded, sourced, contracted single agent
**Result:** V7 — an explicit graph with named responsibilities

---

## 11.1 Current state and observed limitation

V6 is secured, skill-driven, contract-bound, sourced and grounded. One
prompt still controls four business responsibilities at once, and the
accumulated evidence shows four specific costs:

- **No attribution.** One span covers everything. Which responsibility
  consumed the ninety seconds is unanswerable.
- **Contamination.** A malformed research result flows into qualification
  and produces a confident decision about nothing.
- **No isolation.** A research failure discards completed qualification
  work, because there is no unit smaller than the whole run.
- **Order is requested, not enforced.** The prompt describes a sequence. The
  runtime does not enforce it, and under an unusual account the model
  reorders.

The fourth is the important one. Chapter 1 §1.3: *a prompt is a request, a
graph edge is a guarantee.*

## 11.2 Engineering question

> Can we locate, isolate and recover the responsibility that failed?

## 11.3 Architectural decision

Decompose the single agent node into **named nodes with typed state
ownership**, mixing model-backed reasoning with deterministic functions,
joined by **explicit edges and conditional routes**.

Add a **parallel research fan-out with a deterministic join** — taught here
as a workflow shape, not as performance optimisation.

## 11.4 The V7 graph

```text
START
  → validate_request           deterministic
  → ┌ profile_company          model + MCP tools   ┐ parallel
    └ find_signals             model + MCP tools   ┘
  → join_research              deterministic
  → verify_evidence            deterministic
  → qualify_account            model + Skill + contract
  → qualification_route        deterministic branch
       QUALIFIED     → ground_claims → draft_outreach
       INSUFFICIENT  → request_more_evidence
       DISQUALIFIED  → write_disposition
  → prepare_approval
  → END
```

Reasoning stays probabilistic inside selected nodes. Order, validation,
routing and prohibited transitions are code.

## 11.5 Choosing a node type

The heuristic, stated once and used for every node:

| Use | When |
|---|---|
| a model node | the step needs interpretation, synthesis or language |
| a function node | the answer follows a rule |
| a tool node | the step interacts with an external capability |
| a human node | progress requires a person's decision |

The architecture gets stronger every time inexpensive deterministic work
stops being disguised as intelligence. "Is the employee count within the ICP
band?" is a comparison, not a judgment — and V6 was paying a model to do it.

## 11.6 Typed handoffs and state ownership

Each node returns **only the keys it owns**. `profile_company` returns
`company_profile`; it does not touch `evidence` — that key has a reducer and
accumulates from several nodes.

The rule that makes this work: *if two nodes write the same key without a
reducer, one silently wins.* State ownership is documented per node and
tested.

## 11.7 Parallel fan-out, honestly scoped

`profile_company` and `find_signals` are independent, so they run
concurrently and `join_research` waits for both.

Taught here as **a workflow shape**: how a fan-out is expressed, what a join
contract is, and why the join must be deterministic. Latency measurement and
critical-path analysis belong to a later book — this chapter does not claim
a speedup it has not measured.

The join's real lesson is failure: what happens when one branch succeeds and
the other fails. The answer is an explicit partial-result contract, not an
exception.

## 11.8 Alternatives considered

**Subagent delegation** — a manager agent invoking worker agents. Rejected
as a second orchestration framework inside the first: control flow becomes
invisible, sitting in prompts rather than edges, which is the problem this
chapter exists to fix.

**A better single prompt.** Rejected — it cannot fix attribution or
isolation, which are structural, not linguistic.

**Full decomposition into every possible node.** Rejected. Nodes cost
serialisation and latency. Decompose where evidence shows a boundary is
needed, which here means four responsibilities, not eleven.

**Sequential research** rather than parallel. Defensible and simpler; the
fan-out is included because the join contract is a lesson, and one is enough
to teach it.

## 11.9 Trade-offs

More files, more state keys, more places to look. A reader debugging V7
navigates a graph rather than reading a prompt — better for a maintainer,
worse for a newcomer, and worth saying which.

Explicit routing means an account the router has no branch for stops.
Chapter 12 finds those; V7 escalates rather than guessing.

## 11.10 Implementation walkthrough

- `app/graph/state.py` — full `SDRState`, reducers, ownership table.
- `app/nodes/` — one module per node, each with a docstring naming the keys
  it reads and the keys it owns.
- `app/graph/routes.py` — `qualification_route` as a pure function of state.
  Testable without a model.
- `app/graph/build.py` — assembly; parallel edges; join.

## 11.11 Tests and evaluation

- Every route is exercised by a state fixture, with no model call.
- A node that writes a key it does not own fails a test.
- A failing research branch preserves qualification state.
- Malformed research is caught by `verify_evidence` and never reaches
  `qualify_account`.
- The join handles one-branch-failed with a partial-result contract.

## 11.12 Failure demonstration

Force `find_signals` to fail. In V6 the run dies and everything is lost. In
V7 the join records the partial result, `verify_evidence` marks evidence
insufficient, the route sends the account to `request_more_evidence`, and
the completed company profile survives.

## 11.13 Evidence of improvement

Failure attribution: V6 impossible → V7 per-node. Work preserved on partial
failure. Route coverage tested without model calls.

## 11.14 Updated run manifest

`version_tag: "v7-workflow"`, node inventory, graph topology hash.

## 11.15 What remains unresolved

Seven versions, and every claim of improvement so far rests on targeted
tests of the specific thing each version changed. **Nobody has measured
whether V7 is better than V1 overall.** It may have regressed something
nothing tests.

## 11.16 Exercises

1. Add a node and deliberately write a key another node owns. Read the
   failure. Why is this worth a test rather than a convention?
2. `qualification_route` is a pure function. Write three state fixtures that
   exercise all branches without touching a model. How long did that take
   compared with testing V6's equivalent?
