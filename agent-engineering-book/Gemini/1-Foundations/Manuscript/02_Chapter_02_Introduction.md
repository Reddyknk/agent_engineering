# Chapter 2: Introduction — Evolving an Agentic Product

## Product version

**V0 — evolution method and evidence contract**

V0 defines how the product will change before implementation begins. Each later
version must start with observed evidence, make one justified architectural move
and prove that the move improved the SDR outcome without weakening control.

## Engineering question

**How will we decide whether additional agent complexity has earned its place?**

## Why this book exists

The easiest way to build an agent demonstration is to connect a model to a prompt and a few tools. The easiest way to misunderstand agent engineering is to assume that the demonstration is the system.

A production-minded agent application must answer questions that a prompt alone cannot answer:

- What business objective is the agent responsible for?
- Which decisions may the model make?
- Which actions must remain deterministic?
- What information should be placed in context?
- Which tools may be used, and with what permissions?
- How are outputs validated before downstream systems consume them?
- How do multiple agents divide work and exchange results?
- When must a human approve the next step?
- How do we test a system whose outputs are not always identical?
- How do we observe, deploy, and improve it?

This book develops a practical answer through a cumulative system.

## The reference system: WidgetWare SDR

WidgetWare is a fictional business-to-business software company. It needs help identifying and researching prospective customers. A human Sales Development Representative typically performs several related jobs:

1. Understand the company’s products and ideal customer profile.
2. Identify a target account.
3. Research recent, relevant evidence about that account.
4. Determine whether the account appears qualified.
5. Explain the qualification decision.
6. Draft a personalized outreach message.
7. Obtain approval before contacting the prospect.

These activities are well suited to Agent Engineering because they contain both predictable steps and judgment-intensive work. Research and synthesis benefit from model reasoning. Validation, permissions, state transitions, and approval gates benefit from deterministic software.

The goal is not to replace every human activity. The goal is to construct a system in which the model performs the work it is good at while software and people retain control over high-risk decisions.

## The method this book runs on

Book 1 is organized around one product and one recurring decision cycle:

> **Observe → Ask → Decide → Change → Prove**

Every version begins with evidence from the current system. The reader names the
material concern, states a measurable hypothesis, implements the smallest useful
change and reruns the same cases. If the proof is weak, the added complexity has
not earned its place.

This is the book's structure, not a slogan. It is why the chapters are ordered as
they are. The book deliberately starts with a broad monolithic agent, complete in
business scope but simple in topology. Security is the first hardening layer.
Explicit graph control follows only after the monolith reveals problems in order,
diagnosis, contracts or recovery. Review detects weak output; a later loop corrects
it. The workflow is made to explain itself before anything is optimized — cost
reduction and parallelism are both spent against measured evidence, never
intuition. A durable outer loop appears only after the single-account workflow is
evaluated, observable and fast.

## The Seven Steps, and where this book performs them

The series uses a seven-step framework across every technology it covers. Gemini,
ADK and Antigravity are this edition's implementation; the steps themselves are
vendor-independent, because they describe engineering activities rather than
product features.

The Seven Steps and the evolution cycle are not competing frameworks, and it is
worth being precise about the difference. **The Seven Steps name the kinds of work
an agent system requires. The evolution cycle governs when each kind of work is
justified.** A reader who knows the seven steps still does not know which to do
next; that is what the cycle decides. This book is structured by the cycle and
draws its vocabulary from the steps.

Every step is performed in Book 1, but not in a single pass and not in numbered
order — most are revisited as the product earns the right to more of them:

| Step | What it names | Where Book 1 performs it |
| --- | --- | --- |
| 1. Frame the Use Case | Objective, users, boundaries and permitted autonomy, settled before code | Chapter 3 — the WidgetWare charter and acceptance criteria (V0) |
| 2. Build Context | Instructions, business rules, ICP data, evidence and task state, kept separable | Chapter 5 assembles it (V1); Chapters 9 and 10 source it (V5, V6); Chapter 15 puts it on a budget (V11) |
| 3. Design Agent Capabilities | Skills, typed contracts and tools — what the system can actually invoke | Chapter 7 Skills (V3), Chapter 8 contracts (V4), Chapter 9 evidence tools (V5), Chapter 10 retrieval (V6) |
| 4. Build the Harness | The development and execution environment the agent runs inside | Chapter 4 — Antigravity and the ADK runtime (V0) |
| 5. Orchestrate Workflows | Explicit sequencing, state transitions and approval gates | Chapter 11 makes control explicit (V7); Chapter 15 makes it concurrent (V11) |
| 6. Engineer Loops | Bounded processes that decide whether to continue, retry, stop, defer or escalate | Chapter 13's inner quality loop (V9); Chapter 16's outer operational loop (V12) |
| 7. Evaluate & Govern | Measuring whether the system is good, and keeping it inside its boundaries | Chapter 12 evaluates (V8), Chapter 14 observes (V10), Chapter 17 releases and replays (V13) |

Step 7 is where the two books divide. Book 1 builds evaluation, observability and
release evidence for one product. Organization-wide governance, continuous
evaluation across many workflows, and platform AgentOps belong to Book 2.

## How Book 1 progresses

- Chapters 2–4 establish V0: the method, business contract, Google Cloud project
  and engineering harness.
- Chapter 5 produces V1: one complete monolithic SDR agent.
- Chapter 6 produces V2: the same product with explicit security boundaries.
- Chapter 7 produces V3: qualification judgment extracted into a reusable Skill.
- Chapter 8 produces V4: a validated output contract other systems can act on.
- Chapter 9 produces V5: research whose every claim carries a resolvable source.
- Chapter 10 produces V6: product claims grounded in retrieved, owned knowledge.
- Chapter 11 produces V7: a reliable ADK graph with typed nodes and routes.
- Chapter 12 produces V8: external evaluation and in-product quality detection.
- Chapter 13 produces V9: bounded generate-review-revise behavior.
- Chapter 14 produces V10: operational observability and AgentOps.
- Chapter 15 produces V11: cost and latency optimization, proved from the trace.
- Chapter 16 produces V12: a durable dynamic workflow for an account queue.
- Chapter 17 produces V13: repeatable deployment, lineage, recording and replay.

Every chapter leaves the repository in a usable state. The same golden cases,
output contract, SLO vocabulary and run manifest make versions comparable.

## What Book 1 deliberately does not do

Book 1 introduces production thinking without attempting to solve every enterprise concern. It does not deeply implement:

- long-term memory;
- production-scale retrieval-augmented generation;
- distributed Agent-to-Agent collaboration;
- enterprise Agent Registry and Gateway governance;
- network containment;
- comprehensive Model Armor policies;
- model-routing economics;
- production-scale observability; or
- continuous online evaluation.

These topics belong in Book 2 because they are easier to understand after the reader has built and evaluated one complete agent application.

## A principle for the entire series

The book repeatedly asks a simple question:

> Is this behavior better expressed as model reasoning or deterministic software?

Use deterministic software when the required behavior is known. Use model reasoning when interpretation, synthesis, or adaptive judgment is required. Connect the two through typed contracts, explicit state, narrow tools, and measurable evaluation.

That balance is the foundation of inspectable agents.
