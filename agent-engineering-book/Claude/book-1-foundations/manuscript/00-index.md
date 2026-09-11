# Book 1 — Index

Three ways in: by **chapter**, by **concept**, and by **decision**.

Status legend: **written** — prose complete. **outline** — structure,
decisions and alternatives settled; prose and code to be written.

---

## Chapters

| # | Chapter | Version | Tag | Status |
|---:|---|:---:|---|---|
| 1 | [Agent Engineering as a Discipline](ch01-agent-engineering-as-a-discipline.md) | — | — | written |
| 2 | [Observe, Ask, Decide, Change, Prove](ch02-observe-ask-decide-change-prove.md) | — | — | written |
| 3 | [Scope the Agent and Bound Its Autonomy](ch03-scope-the-agent-and-bound-its-autonomy.md) | V0 | `v0-harness` | written |
| 4 | [Build the Engineering Harness](ch04-build-the-engineering-harness.md) | V0 | `v0-harness` | written |
| 5 | [Build the First Claude Agent with LangGraph](ch05-build-the-first-claude-agent-with-langgraph.md) | V1 | `v1-monolith` | outline |
| 6 | [Establish Trust Boundaries](ch06-establish-trust-boundaries.md) | V2 | `v2-bounded` | outline |
| 7 | [Package Expertise as Agent Skills](ch07-package-expertise-as-agent-skills.md) | V3 | `v3-skills` | outline |
| 8 | [Replace Prose with Typed Contracts](ch08-replace-prose-with-typed-contracts.md) | V4 | `v4-contracts` | outline |
| 9 | [Connect External Capabilities through MCP](ch09-connect-external-capabilities-through-mcp.md) | V5 | `v5-mcp` | outline |
| 10 | [Ground the Agent with RAG and Evidence](ch10-ground-the-agent-with-rag-and-evidence.md) | V6 | `v6-grounded` | outline |
| 11 | [Evolve from One Agent to an Explicit Workflow](ch11-evolve-from-one-agent-to-an-explicit-workflow.md) | V7 | `v7-workflow` | outline |
| 12 | [Evaluate Behavior before Adding Complexity](ch12-evaluate-behavior-before-adding-complexity.md) | V8 | `v8-evaluated` | outline |
| 13 | [Improve Quality with a Bounded Review Loop](ch13-improve-quality-with-a-bounded-review-loop.md) | V9 | `v9-review-loop` | outline |
| 14 | [Observe the Complete Agentic System](ch14-observe-the-complete-agentic-system.md) | V10 | `v10-observed` | outline |
| 15 | [Assemble and Run the Reference Architecture](ch15-assemble-and-run-the-reference-architecture.md) | V10 | `v10-packaged` | outline |

---

## Appendices

Reference material — consulted, not worked through.

| | Appendix | Answers | Status |
|---|---|---|---|
| A | [Environment Setup and Troubleshooting](appendix-a-environment-setup-and-troubleshooting.md) | It will not install / it will not run | written |
| B | [Contract, State and Tool Reference](appendix-b-contract-state-and-tool-reference.md) | What fields does this have, and who owns that state? | outline |
| C | [The Evidence Policy in Practice](appendix-c-the-evidence-policy-in-practice.md) | Is this claim a fact, and is it supported? | written |
| D | [Verified API Reference](appendix-d-verified-api-reference.md) | What is the current call, and has it changed? | written |

Also: [ADR-000 — Verified Dependency Baseline](../architecture/ADR-000-verified-dependency-baseline.md),
which argues the pins Appendix D lists.

Appendix C is the one to read early — Chapter 3.8 introduces the
`claim_type` × `support_type` split, and C.3's fifteen worked examples are
where it becomes usable rather than agreeable.

---

## The version ladder

Each version answers one question, earned by an observation of the version
before it.

| Version | Question it answers | Observation that earned it |
|:---:|---|---|
| V0 | Can we build and measure anything at all? | Nothing exists |
| V1 | What does the naive version actually do? | No agent to observe |
| V2 | Can prohibited behaviour be blocked? | V1 obeyed a fetched page |
| V3 | Is judgment applied the same way each time? | V2's reasoning varied per run |
| V4 | Can another system act on the output? | V3 returned prose |
| V5 | Can capabilities live outside the app? | V4 had no provenance boundary |
| V6 | Are our own product claims supportable? | V5 invented WidgetWare claims |
| V7 | Can we locate the responsibility that failed? | V6 was one opaque span |
| V8 | Is V7 actually better than V1? | Seven versions, no measurement |
| V9 | Can quality improve without running forever? | V8 detected weak drafts, emitted them |
| V10 | Can a run be explained and reproduced? | V9 was ephemeral and unexplainable |

---

## Sections

**Chapter 1 — Agent Engineering as a Discipline**
1.1 A definition worth arguing with · 1.2 The autonomy spectrum ·
1.3 Deterministic and probabilistic parts, kept separate ·
1.4 When not to build an agent · 1.5 Five failure patterns to recognise now ·
1.6 The reference application · 1.7 What "engineering" adds ·
1.8 A caution about this book's own claims · 1.9 Exercises

**Chapter 2 — Observe, Ask, Decide, Change, Prove**
2.1 The cycle · 2.2 Why the order is what it is · 2.3 The evidence contract ·
2.4 What counts as proof · 2.5 One capability per version ·
2.6 The version ladder · 2.7 What this method costs · 2.8 Exercises

**Chapter 3 — Scope the Agent and Bound Its Autonomy**
3.1 Current state and observed limitation · 3.2 Engineering question ·
3.3 Architectural decision · 3.4 Alternatives considered · 3.5 Trade-offs ·
3.6 The specification · 3.7 What V0 produces ·
3.8 The evidence policy, and why it has two dimensions ·
3.9 Evidence of completion · 3.10 Updated run manifest ·
3.11 What remains unresolved · 3.12 Exercise

**Chapter 4 — Build the Engineering Harness**
4.1 Current state and observed limitation · 4.2 Engineering question ·
4.3 Architectural decision · 4.4 Alternatives considered ·
4.5 Architecture before and after · 4.6 Implementation walkthrough ·
4.7 Claude Code, and where it stops · 4.8 Evidence of improvement ·
4.9 Failure demonstration · 4.10 Updated run manifest ·
4.11 What remains unresolved · 4.12 Exercises

**Chapter 5 — Build the First Claude Agent with LangGraph**
5.1 Current state and observed limitation · 5.2 Engineering question ·
5.3 Architectural decision · 5.4 Alternatives considered · 5.5 Trade-offs ·
5.6 Architecture before and after · 5.7 Implementation walkthrough ·
5.8 The inner loop, named · 5.9 Tests and evaluation ·
5.10 Failure demonstration · 5.11 Evidence of improvement ·
5.12 Updated run manifest · 5.13 What remains unresolved · 5.14 Exercises

**Chapter 6 — Establish Trust Boundaries**
6.1 Current state and observed limitation · 6.2 Engineering question ·
6.3 Architectural decision · 6.4 Alternatives considered · 6.5 Trade-offs ·
6.6 Architecture before and after · 6.7 Implementation walkthrough ·
6.8 Prompt injection, demonstrated · 6.9 Tests and evaluation ·
6.10 Failure demonstration · 6.11 Evidence of improvement ·
6.12 Updated run manifest · 6.13 What remains unresolved · 6.14 Exercises

**Chapter 7 — Package Expertise as Agent Skills**
7.1 Current state and observed limitation · 7.2 Engineering question ·
7.3 Architectural decision · 7.4 What a Skill is not ·
7.5 Progressive disclosure, and why it is not just token thrift ·
7.6 Alternatives considered · 7.7 Trade-offs · 7.8 Implementation walkthrough ·
7.9 Tests and evaluation · 7.10 Failure demonstration ·
7.11 Evidence of improvement · 7.12 Updated run manifest ·
7.13 What remains unresolved · 7.14 Exercises

**Chapter 8 — Replace Prose with Typed Contracts**
8.1 Current state and observed limitation · 8.2 Engineering question ·
8.3 Architectural decision · 8.4 Two type systems, deliberately ·
8.5 Native structured output · 8.6 Alternatives considered · 8.7 Trade-offs ·
8.8 Implementation walkthrough · 8.9 Evidence references, not embedded evidence ·
8.10 Tests and evaluation · 8.11 Failure demonstration ·
8.12 Evidence of improvement · 8.13 Updated run manifest ·
8.14 What remains unresolved · 8.15 Exercises

**Chapter 9 — Connect External Capabilities through MCP**
9.1 Current state and observed limitation · 9.2 Engineering question ·
9.3 Architectural decision · 9.4 MCP, from zero · 9.5 Alternatives considered ·
9.6 Trade-offs · 9.7 Implementation walkthrough · 9.8 Failure handling ·
9.9 Tests and evaluation · 9.10 Failure demonstration ·
9.11 Evidence of improvement · 9.12 Updated run manifest ·
9.13 What remains unresolved · 9.14 Exercises

**Chapter 10 — Ground the Agent with RAG and Evidence**
10.1 Current state and observed limitation · 10.2 Engineering question ·
10.3 Architectural decision · 10.4 RAG, from zero · 10.5 Why hybrid, concretely ·
10.6 Alternatives considered · 10.7 Trade-offs · 10.8 Implementation walkthrough ·
10.9 Tests and evaluation · 10.10 Failure demonstration ·
10.11 Evidence of improvement · 10.12 Updated run manifest ·
10.13 What remains unresolved · 10.14 Exercises

**Chapter 11 — Evolve from One Agent to an Explicit Workflow**
11.1 Current state and observed limitation · 11.2 Engineering question ·
11.3 Architectural decision · 11.4 The V7 graph · 11.5 Choosing a node type ·
11.6 Typed handoffs and state ownership · 11.7 Parallel fan-out, honestly scoped ·
11.8 Alternatives considered · 11.9 Trade-offs · 11.10 Implementation walkthrough ·
11.11 Tests and evaluation · 11.12 Failure demonstration ·
11.13 Evidence of improvement · 11.14 Updated run manifest ·
11.15 What remains unresolved · 11.16 Exercises

**Chapter 12 — Evaluate Behavior before Adding Complexity**
12.1 Current state and observed limitation · 12.2 Engineering question ·
12.3 Architectural decision · 12.4 Two kinds of question ·
12.5 Evaluation dimensions · 12.6 Alternatives considered · 12.7 Trade-offs ·
12.8 Implementation walkthrough · 12.9 The poisoned corpus case ·
12.10 Failure demonstration · 12.11 Evidence of improvement ·
12.12 Updated run manifest · 12.13 What remains unresolved · 12.14 Exercises

**Chapter 13 — Improve Quality with a Bounded Review Loop**
13.1 Current state and observed limitation · 13.2 Engineering question ·
13.3 Architectural decision · 13.4 The subgraph · 13.5 Stop reasons, enumerated ·
13.6 Independence of the reviewer · 13.7 Preserving evidence across iterations ·
13.8 Alternatives considered · 13.9 Trade-offs · 13.10 Implementation walkthrough ·
13.11 Tests and evaluation · 13.12 Failure demonstration ·
13.13 Evidence of improvement · 13.14 Updated run manifest ·
13.15 What remains unresolved · 13.16 Exercises

**Chapter 14 — Observe the Complete Agentic System**
14.1 Current state and observed limitation · 14.2 Engineering question ·
14.3 Architectural decision · 14.4 What gets a span ·
14.5 Correlation identifiers · 14.6 The content-capture problem ·
14.7 Alternatives considered · 14.8 Trade-offs · 14.9 Implementation walkthrough ·
14.10 Tests and evaluation · 14.11 Failure demonstration ·
14.12 Evidence of improvement · 14.13 Updated run manifest ·
14.14 What remains unresolved · 14.15 Exercises

**Chapter 15 — Assemble and Run the Reference Architecture**
15.1 Current state and observed limitation · 15.2 Engineering question ·
15.3 Architectural decision · 15.4 Six kinds of state, distinguished ·
15.5 The approval pause · 15.6 Alternatives considered · 15.7 Trade-offs ·
15.8 Implementation walkthrough · 15.9 Tests and evaluation ·
15.10 The Book 1 reference architecture · 15.11 Known limitations ·
15.12 Acceptance criteria · 15.13 What comes next · 15.14 Exercises

---

## Concepts

Where each idea is introduced (**bold**) and where it is used again.

| Concept | Introduced | Also |
|---|---|---|
| Agent, definition of | **1.1** | 5.8 |
| Autonomy spectrum | **1.2** | 3.6 |
| Deterministic vs. probabilistic split | **1.3** | 11.5 |
| When not to build an agent | **1.4** | — |
| Confident fabrication | **1.5** | 9.1, 10.1 |
| Silent degradation | **1.5** | 12.1 |
| Runaway loop | **1.5** | 13.2, 13.8 |
| Unattributable failure | **1.5** | 11.1, 14.1 |
| Prompt injection | **1.5** | **6.8**, 12.9 |
| Observe → Ask → Decide → Change → Prove | **2.1** | every chapter |
| Evidence contract | **2.3** | 6.9, 12.3 |
| What counts as proof | **2.4** | 12.4 |
| One capability per version | **2.5** | — |
| Autonomy boundary | **3.6** | 4.9, 15.5 |
| `claim_type` × `support_type` | **3.8** | 7.3, 8.8 |
| Service level objective (SLO) | **3.6** | 14.12 |
| Run manifest | **4.6** | every chapter's penultimate section |
| Exact vs. floored pins | **4.4** | ADR-000 |
| Claude Code vs. the runtime | **4.7** | 7.6 |
| Sampling parameters, absence of | **4.6** | ADR-000 |
| `StateGraph` | **5.3** | 11.4 |
| Reducers | **5.7** | 8.4, 11.6, 13.7 |
| Tool declaration format | **5.7** | 6.7, 9.7 |
| Inner loop vs. outer loop | **5.8** | 13.3 |
| `RequestContext` | **6.3** | 15.8 |
| Read/write tool classification | **6.3** | 9.8 |
| Policy gate | **6.3** | 9.8 |
| Audit events | **6.3** | 14.5, 15.9 |
| Evidence ledger | **6.7** | 8.9, 9.7, 10.3 |
| Agent Skill | **7.3** | — |
| Skill vs. tool vs. agent vs. RAG | **7.4** | — |
| Progressive disclosure | **7.5** | — |
| Content hash | **4.6** | 7.8, 9.7, 10.8 |
| Pydantic vs. TypedDict | **8.4** | 11.6 |
| Native structured output | **8.5** | ADR-000 |
| Repair loop, bounded | **8.8** | 13.3 |
| Model Context Protocol (MCP) | **9.4** | — |
| Tools vs. resources vs. prompts | **9.4** | — |
| Graceful degradation | **9.8** | 11.7 |
| Retrieval-Augmented Generation (RAG) | **10.4** | — |
| Chunking | **10.4** | 10.14 |
| Hybrid ranking | **10.5** | — |
| Citation integrity | **10.8** | 12.5 |
| Node type selection | **11.5** | — |
| State ownership | **11.6** | 13.7 |
| Parallel fan-out and join | **11.7** | — |
| Conditional routing | **11.4** | 13.4 |
| Golden dataset | **12.3** | — |
| Deterministic vs. judged evaluation | **12.4** | 13.9 |
| Adversarial case | **12.3** | 6.8, 12.9 |
| Overfitting to an eval set | **12.7** | — |
| Bounded loop | **13.3** | — |
| Stop reason | **13.5** | 15.9 |
| Reviewer independence | **13.6** | — |
| OpenTelemetry | **14.3** | — |
| Content capture, disabled by default | **14.6** | — |
| Correlation identifiers | **14.5** | 15.4 |
| Checkpointing | **15.3** | ADR-000 |
| Six kinds of state | **15.4** | — |
| `interrupt()` / `Command(resume=)` | **15.5** | ADR-000 |
| Human approval | **15.5** | 1.2, 3.6 |
| Classifying a claim, worked | **C.3** | 3.8, 7.8 |
| Evidence by reference | **B.2** | 8.9 |
| State ownership table | **B.3** | 11.6 |
| Tool declaration fields | **B.4** | 5.7, 6.7 |
| Manifest fields by version | **B.6** | 4.10 |
| Re-verifying a pinned API | **D.7** | ADR-000 |

---

## Decisions

Every architectural decision, with the section that argues it and the
alternatives it rejected. Read this column to disagree with the book.

| Decision | Argued in | Rejected |
|---|---|---|
| Specification as data, not prompt | 3.3–3.4 | prompt-embedded ICP |
| Autonomy boundary as structure, not flag | 3.3–3.4 | feature flag; pre-send policy check |
| Harness before agent | 4.3–4.4 | agent first, tests later |
| Exact dependency pins | 4.4 | compatible-release specifiers |
| Manifest from pins, not environment | 4.4 | `pip freeze` |
| LangGraph from V1, two nodes | 5.3–5.4 | raw API loop; `create_agent`; three agents |
| Policy in code, not prompt | 6.3–6.4 | prompt defence; guardrail model; per-tool checks |
| Skills with an app-owned registry | 7.3–7.6 | `CLAUDE.md`; Python function; fine-tuning |
| Six contracts, not one | 8.3–8.6 | single `AccountBrief`; JSON-in-prompt; Instructor |
| Native structured output | 8.5 | forced tool use |
| Evidence by reference | 8.9 | embedded evidence objects |
| MCP for external capabilities only | 9.3–9.5 | in-process; `langchain-mcp-adapters`; HTTP service; MCP everywhere |
| Visible RAG pipeline | 10.3–10.6 | LlamaIndex; vector-only; dedicated vector DB |
| Delete unsupported claims, don't hedge | 10.8 | softening language |
| Decompose to four responsibilities | 11.3–11.8 | subagents; better prompt; full decomposition |
| Evaluation after the graph | 12.6 | evaluating from Ch. 5 |
| One owned evaluation runner | 12.3–12.6 | Promptfoo + DeepEval + Langfuse together |
| Deterministic and judged kept separate | 12.4 | a single blended score |
| Loop bounded by conditional edge | 13.3–13.8 | unbounded retry; single pass; self-critique |
| Independent reviewer node | 13.6 | critique in the generation call |
| OTel standard, Langfuse backend | 14.3–14.7 | Langfuse SDK alone; logs only; Prometheus stack |
| Content capture off by default | 14.6 | default-on instrumentation |
| PostgreSQL for everything | 15.6 | SQLite; separate vector DB |
| API boundary, not CLI | 15.6 | CLI (cannot express the approval pause) |

---

## Out of scope for Book 1

Named where relevant, implemented in later books: multiple orchestration
frameworks · adaptive workflow generation · multi-agent collaboration ·
dynamic model routing · model right-sizing · prompt-caching strategy ·
batch processing · distributed queues · high availability · advanced
checkpoint recovery · enterprise identity · policy engines · full threat
modelling · distributed metrics and logs · SLO dashboards and alerting ·
release lineage, replay and rollback · multi-region deployment.

Book 1's known limitations are enumerated in 15.11, each pointing at the
book that takes it up.
