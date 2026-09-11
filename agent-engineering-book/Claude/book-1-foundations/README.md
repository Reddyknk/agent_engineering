# Agent Engineering with Claude and Open Source

## Book 1 — Foundations

One prospect-intelligence agent, built in eleven deliberate steps.

This repository holds both the manuscript and the reference application it
builds. The application is a WidgetWare prospect-intelligence and
sales-development agent: it researches a company, collects attributable
evidence, retrieves grounded product knowledge, decides whether the company
fits an ideal customer profile, drafts outreach, reviews and revises that
draft, and escalates when the evidence will not support a conclusion.

It never contacts anyone. That boundary is structural — Book 1 builds no
send capability, and a test fails if one appears.

## The method

Every version in this book follows one cycle:

> **Observe → Ask → Decide → Change → Prove**

Observe the current system's behavior. Identify a specific weakness. Ask
what architectural capability is missing. Make one deliberate decision.
Change the system. Prove the improvement with tests, traces or evaluation
results.

No technology appears in this book because it exists. Each addition answers
a problem the previous version demonstrably has.

## Getting started

Requires Python 3.11 or newer and [uv](https://docs.astral.sh/uv/).

```bash
git clone <this-repository>
cd book-1-foundations

uv sync --extra dev
cp .env.example .env        # then add your Anthropic API key

uv run pytest
```

The test suite is green before you have written anything or supplied a key.
That is Chapter 4's point: the harness proves itself before there is an
agent to prove.

To record the environment a run was evaluated against:

```bash
uv run python -m app.manifest
```

## Reading order

Chapters 1 and 2 establish the vocabulary and the method. Chapter 3 scopes
the problem and Chapter 4 builds the harness — together they are V0, before
any agent exists. Chapter 5 builds the first one.

| Chapter | Version | What it adds |
|---:|:---:|---|
| 1. Agent Engineering as a Discipline | — | What an agent is, and when not to build one |
| 2. Observe, Ask, Decide, Change, Prove | — | The method and the evidence contract |
| 3. Scope the Agent and Bound Its Autonomy | V0 | Users, outcomes, risks, autonomy boundary, SLOs |
| 4. Build the Engineering Harness | V0 | Repository, environment, tests, run manifest |
| 5. Build the First Claude Agent with LangGraph | V1 | One graph: an agent node and a tool node |
| 6. Establish Trust Boundaries | V2 | Request context, tenant checks, tool policy, audit |
| 7. Package Expertise as Agent Skills | V3 | `SKILL.md` packages and a `SkillRegistry` |
| 8. Replace Prose with Typed Contracts | V4 | Pydantic contracts and structured output |
| 9. Connect External Capabilities through MCP | V5 | An MCP server and a LangGraph adapter |
| 10. Ground the Agent with RAG and Evidence | V6 | pgvector, full-text search, hybrid ranking |
| 11. Evolve from One Agent to an Explicit Workflow | V7 | Named nodes, routing, a parallel branch |
| 12. Evaluate Behavior before Adding Complexity | V8 | Golden and adversarial evaluation |
| 13. Improve Quality with a Bounded Review Loop | V9 | Generate → review → revise, with a stop reason |
| 14. Observe the Complete Agentic System | V10 | OpenTelemetry traces and Langfuse |
| 15. Assemble and Run the Reference Architecture | V10 | Checkpointing, FastAPI, Docker Compose |

Each version is a git tag (`v0-harness` through `v10-packaged`). Checking
one out gives you a repository that passes its own tests, so you can run any
stage of the system independently.

Four appendices are reference material — consult them, don't work through
them:

| | Appendix | Answers |
|---|---|---|
| A | Environment Setup and Troubleshooting | It won't install / it won't run |
| B | Contract, State and Tool Reference | What fields does this have, and who owns that state? |
| C | The Evidence Policy in Practice | Is this claim a fact, and is it supported? |
| D | Verified API Reference | What's the current call, and has it changed? |

`manuscript/00-index.md` indexes everything three ways — by chapter, by
concept, and by decision. The decision table is the book's argument on one
screen, and the place to disagree with it.

## What is in here

```text
manuscript/     the fifteen chapters
architecture/   decision records and per-version diagrams
app/            the application — one LangGraph graph and what surrounds it
config/         ICP, offering, proof points, voice, and their schemas
data/           the thirteen-account comparison set and offline fixtures
evals/          golden and adversarial cases
tests/          per-version test suites
scripts/        verification and corpus tooling
```

`app/contracts/evidence-policy.yaml` is worth reading before Chapter 3. It
holds the distinction the whole application rests on: a claim's *epistemic
status* (fact, inference, hypothesis) is tracked separately from how
strongly the cited evidence *supports* it. Most systems collapse these into
one confidence number and lose the ability to say "well-sourced guess."

## Claude Code is not part of the runtime

Claude Code is used to write, test and modify this repository. It is not a
dependency of the application, and no production code path invokes it. The
application reaches Claude through the Anthropic Messages API via
`langchain-anthropic`, and through nothing else.

## Versions

Dependencies are pinned exactly rather than floored, and the reasoning —
along with every version-sensitive API this book relies on, verified against
current documentation rather than recalled — is in
[`architecture/ADR-000`](architecture/ADR-000-verified-dependency-baseline.md).

Read it before filing a bug. Three of its findings contradict what most
material written before 2026 will tell you, including the widespread advice
to set `temperature=0` for reliability — current Claude models reject that
parameter outright.
