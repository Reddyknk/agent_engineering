# Chapter 11: Reliable Graph Workflows and Responsibility Boundaries

## Chapter purpose

The V6 agent is complete, secured, skill-driven, contract-bound and evidence-backed,
but a long prompt still controls several
business responsibilities at once. This chapter uses observed failure and trace
evidence to replace implicit prompt order with an explicit ADK graph. The graph
combines model reasoning with deterministic validation, routes and typed data
contracts.

## Product version

**Starting point:** V6 — evidence-backed single agent  
**Result:** V7 — reliable graph workflow

## Engineering question

> Can we locate, isolate and recover the responsibility that failed?

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish a business responsibility from an agent;
- justify decomposition with evidence rather than feature availability;
- define ADK graph nodes and edges;
- mix LLM agents, functions and tools in one controlled flow;
- design typed node inputs and outputs;
- use explicit branches for business decisions;
- assign state ownership and artifact ownership; and
- compare graph workflows with template workflow agents.

## Evidence that earns the change

The V6 baseline exposes at least four problems:

- one trace span hides which responsibility consumed time;
- malformed intermediate output contaminates later work;
- a research failure forces qualification and drafting to repeat; and
- the prompt describes order, but the runtime does not enforce the business
  state machine independently of the model.

The smallest useful response is not "many agents." It is an explicit process with
named boundaries.

## The WidgetWare V7 graph

```text
START
  → validate_request            deterministic function
  → research_account            LLM agent plus read-only tools
  → validate_evidence           deterministic function
  → qualify_account             LLM agent with structured output
  → qualification_route         deterministic branch
      QUALIFIED   → draft_outreach
      INSUFFICIENT→ request_more_evidence
      DISQUALIFIED→ write_disposition
  → prepare_approval_or_artifact
  → END
```

The graph is predictable without pretending that every node is deterministic.
Reasoning remains probabilistic inside selected nodes. Order, validation, routing
and prohibited transitions are expressed in code.

## 11.1 Node selection

Use a model-backed agent when the step requires interpretation, synthesis or
language generation. Use a function node when the answer follows a deterministic
rule. Use a tool node when the workflow must interact with an external capability.
Use a human-input node when progress requires a person's decision.

The architecture becomes stronger when inexpensive deterministic work stops being
disguised as intelligence.

## 11.2 Typed handoffs

Each node publishes a contract that includes only what the next responsibility
needs. The research node returns an evidence package, not an unrestricted transcript.
The qualification node returns a decision, reasons, confidence label and evidence
references. The drafting node receives approved claims rather than every raw page.

Typed handoffs provide:

- validation at the boundary;
- smaller context;
- clearer ownership;
- stable tests;
- safer retries; and
- independent model selection later.

Detailed contract design is Chapter 8's subject.

## 11.3 Skills become reusable procedures

The qualification rubric, evidence-review procedure and outreach-quality criteria
become versioned Skills. A Skill is not an additional agent. It is a reusable,
testable capability definition that can be applied by one or more nodes. Appendix
04 provides the complete Skill anatomy and evaluation checklist.

## 11.4 State ownership

V7 assigns clear keys and owners:

| State or artifact | Writer | Readers |
| --- | --- | --- |
| `request` | validator | research |
| `evidence_package` | research | evidence validator, qualifier |
| `qualification` | qualifier | route, drafter, artifact writer |
| `outreach_draft` | drafter | later reviewer and human approver |
| `disposition` | route | artifact writer |

Parallel writers never share a key. A later chapter will depend on this rule.

## 11.5 Failure boundaries

Every node declares expected failures and whether they are retryable. Validation
errors stop before model execution. A temporary research-tool failure may retry
within a budget. Insufficient evidence is a business result, not an exception.
Invalid structured output can be repaired once, then escalated.

V7 does not yet add a quality critic. First it proves that the system can explain
which responsibility executed, failed or produced an invalid contract.

## 11.6 Human approval in the graph

A human-input node records approval, rejection or requested revision. The workflow
pauses instead of simulating approval. After resume, the decision becomes typed
input to the next node. No external-action path exists before an affirmative,
auditable decision.

## 11.7 Template agents as a comparison

`SequentialAgent` remains a compact way to teach fixed-order execution, just as
`ParallelAgent` and `LoopAgent` express familiar patterns. The V7 product uses an
ADK 2.x graph because it needs typed node flow, explicit branches, deterministic
functions and a path that can evolve without placing all control in shared state.

The lesson is not that one API is universally superior. It is that the product's
requirements now justify the graph.

## Hands-on lab: Replace prompt order with a graph

1. Capture a failing or ambiguous V6 trace.
2. Identify responsibilities and state transitions.
3. Define typed input and output models.
4. Create deterministic validation and routing nodes.
5. Wrap research, qualification and drafting as bounded agents.
6. Add the human-approval interruption.
7. Inject a research failure and verify the failing node is visible.
8. Resume without rerunning accepted work where the runtime permits.
9. Run the unchanged golden dataset.
10. Compare V6 and V7 quality, latency, cost and trace clarity.

## Evaluation checklist

- Does every node have one primary responsibility?
- Is required order enforced outside a prompt?
- Are business branches explicit?
- Are handoffs typed and minimal?
- Does each state key have one writer?
- Is insufficient evidence represented as a valid outcome?
- Can a failing responsibility be named from evidence?
- Is human approval a real interruption?
- Did decomposition improve control without lowering quality?

## Chapter checkpoint

WidgetWare V7 is no longer one opaque monolith. It is an explicit graph whose
responsibilities, contracts, state and failure boundaries can be tested. Better
structure, however, does not prove better answers. The next question is whether
the system can recognize weak output consistently.

## Bridge to Chapter 12

Chapter 12 holds the architecture stable and adds quality detection. An evaluator
must identify failures in grounding, qualification, requirements and outreach
without being allowed to silently rewrite the product's answer.

