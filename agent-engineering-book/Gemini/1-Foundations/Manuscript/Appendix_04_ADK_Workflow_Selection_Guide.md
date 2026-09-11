# Appendix 04: ADK Workflow Selection Guide

## A4.1 Begin with the least structure that can prove the outcome

WidgetWare starts with one `LlmAgent` because the first question is whether a
complete SDR outcome can be delivered. It adopts an explicit workflow only after
the monolith exposes problems in order, validation, diagnosis or recovery.

## A4.2 Workflow families

| ADK approach | Best fit | WidgetWare use |
| --- | --- | --- |
| Single `LlmAgent` | One bounded conversational task or an early complete baseline | V1 monolith |
| Graph workflow | Explicit routes combining agents, functions, tools and human input | V6–V11 single-account workflow |
| Dynamic workflow | Programmatic conditions, loops and durable orchestration | V12 account-queue loop |
| Collaborative team | Coordinator delegates less-structured tasks to specialists | Book 2 exploratory and advisory work |
| Template workflow agents | Compact fixed sequential, parallel or loop pattern | Teaching comparison and compatibility |
| Experimental routed agent | A/B selection, fallback or complexity routing where supported | Deferred until stable and required |

## A4.3 Pattern selection

| Pattern | Use when | Do not use merely because |
| --- | --- | --- |
| Sequential pipeline | A later step depends on validated earlier output | The business process was written as a list |
| Parallel fan-out and join | Branches share input and do not depend on one another | Several agents exist |
| Generate and review | Independent inspection catches material defects | More model calls feel more reliable |
| Iterative refinement | Feedback can produce a bounded, measurable correction | `max_iterations` is available |
| Human in the loop | Authority, ambiguity or risk requires a person | A prompt says “ask a human” |
| Coordinator and dispatcher | Users present multiple intents requiring different capabilities | Deterministic routing would be clearer |
| Hierarchical decomposition | A complex goal genuinely benefits from multiple levels | A flat design looks too simple |

## A4.4 WidgetWare decision sequence

```text
Can one agent deliver the complete outcome?
  No  → fix the product contract before adding topology
  Yes → does prompt-controlled order cause material failure?
          No  → keep the monolith
          Yes → introduce an explicit graph

Does weak output escape detection?
  Yes → add generate-and-review

Can structured feedback correct the defect economically?
  Yes → add a bounded loop
  No  → escalate to a human

Does the trace show independent work on the critical path?
  Yes → add parallel routes and an explicit join

Must the proven workflow process a durable queue?
  Yes → wrap it in a dynamic outer workflow
```

## A4.5 Book 1 versus Book 2

Book 1 teaches one explicit graph, one bounded dynamic loop and one human-control
path. Book 2 expands into collaborative and hierarchical teams, distributed
agents, A2A, enterprise memory, multi-tenancy, per-agent identities, platform
governance and continuous evaluation across many workflows.

## A4.6 Sources

- ADK workflow overview: <https://adk.dev/workflows/>
- Graph workflows: <https://adk.dev/graphs/>
- Graph routes: <https://adk.dev/graphs/routes/>
- Dynamic workflows: <https://adk.dev/graphs/dynamic/>
- Human input: <https://adk.dev/graphs/human-input/>
- Workflow patterns: <https://adk.dev/workflows/patterns/>
- Collaborative workflows: <https://adk.dev/workflows/collaboration/>
- Template workflow agents: <https://adk.dev/agents/workflow-agents/>
- Experimental agent routing: <https://adk.dev/agents/routing/>

