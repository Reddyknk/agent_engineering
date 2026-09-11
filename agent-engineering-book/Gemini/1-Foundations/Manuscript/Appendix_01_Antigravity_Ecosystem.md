# Appendix 01: The Google Antigravity Ecosystem

This appendix provides a concise, book-friendly overview of the Google Antigravity ecosystem. It is designed as a reader companion to the instructor deck, and it emphasizes architectural understanding rather than product marketing. The goal is to help the reader understand how Antigravity fits into modern Agent Engineering.

The source document used for grounding is the Google Antigravity overview page provided by the user. That overview identifies four product surfaces—Antigravity 2.0, CLI, SDK, and IDE—running on a shared agent harness powered by Gemini 3.5 Flash. It also highlights asynchronous subagents, visual artifacts, secure local execution, approval gates, and curated Google integrations.

---

## A1.1 What Is Google Antigravity?

Google Antigravity is best understood as an **ecosystem of product surfaces** rather than as a single application. The documentation presents four complementary interfaces:

- **Antigravity 2.0**: a desktop command center for projects, workspaces, and orchestration.
- **Antigravity CLI**: a lightweight, keyboard-centric terminal experience.
- **Antigravity SDK**: a Python framework for custom agent development.
- **Antigravity IDE**: a fully integrated developer environment with deep context awareness.

These surfaces are not isolated silos. They all sit on top of a common execution substrate: the **shared agent harness**.

The architectural point is more important than any one interface: each surface
uses the same governed execution substrate, so repositories, policies, review
artifacts and approval boundaries can remain consistent across working styles.

---

## A1.2 The Four Product Surfaces

The product surfaces are aimed at different working styles. The desktop surface is useful when the developer wants a visual command center and multiple long-running streams of work. The CLI is optimized for speed and locality, especially for developers who already live in the terminal. The SDK is for engineers who want to build and extend agents programmatically. The IDE is best when local code context is the center of gravity.

![Comparison of the four Antigravity surfaces.](figures/appendix/antigravity-surface-comparison.png)

*Figure A1.1 — A practical comparison of the four Antigravity product surfaces.*

### Antigravity 2.0

Antigravity 2.0 is described as a standalone desktop command center. It supports projects, multiple workspaces, worktrees, asynchronous task management, scheduled tasks, and voice transcription. This makes it especially appropriate for longer-lived, multi-step flows where visibility and management matter.

![Desktop workspace with projects, workspaces, worktrees, and orchestration capabilities.](figures/appendix/antigravity-desktop-project-model.png)

*Figure A1.2 — The desktop surface acts as a command center for larger workflows.*

### Antigravity CLI

The CLI is a terminal-first surface for fast developer interaction. The documentation emphasizes high-speed prompt shortcuts, custom keybindings, SSH compatibility, and parallel subagent management. The CLI is attractive because it minimizes interface friction.

![CLI path from prompt to agent execution and result.](figures/appendix/antigravity-cli-flow.png)

*Figure A1.3 — The CLI provides a short path from prompt to action.*

### Antigravity SDK

The SDK is a Python framework for researchers and developers who need deep programmatic control. The documentation describes custom agent creation, custom tool registration, lifecycle hooks, declarative safety policies, and programmatic subagent spawning.

![The SDK stack from developer code to artifacts and policies.](figures/appendix/antigravity-sdk-stack.png)

*Figure A1.4 — The SDK exposes the layers needed for explicit agent engineering.*

### Antigravity IDE

The IDE is positioned as a fully featured AI-powered development environment. It integrates coding agents, deep context awareness, MCP, and skills. For many developers, this is likely to be the most natural day-to-day interface because it keeps context, code, and agent support in one environment.

![The IDE context model links the codebase, context, agent, tools, and coding outcomes.](figures/appendix/antigravity-ide-context-model.png)

*Figure A1.5 — The IDE surface concentrates context around coding work.*

---

## A1.3 The Shared Agent Harness

The documentation states that every Antigravity surface runs on a shared, optimized agent harness. Architecturally, the harness can be understood as the operating environment that coordinates the model layer, tools, working context, policies, artifacts, and subagents.

This idea is important because it separates **surface** from **system**. The surface is what the user interacts with. The harness is what makes the behavior coherent across surfaces.

![A conceptual architecture showing surfaces feeding into the shared harness and then into planning, context, subagents, artifacts, and approvals.](figures/appendix/antigravity-shared-harness-architecture.png)

*Figure A1.6 — A conceptual view of the shared harness architecture.*

A useful way to think about the harness is that it is the **control plane for agent behavior**. It is not merely a wrapper around a model. It is the layer that makes planning, delegation, review, and tool use operationally meaningful.

---

## A1.4 The Agent Execution Lifecycle

A simple way to explain Antigravity’s execution behavior is to describe the lifecycle of a request:

1. Receive the user’s **intent**.
2. Create or refine a **plan**.
3. **Delegate** subwork if parallel execution is beneficial.
4. **Execute** tools and agent actions.
5. **Review** intermediate evidence and output.
6. **Respond** with a merged, user-facing result.

![A step-by-step request lifecycle from intent to response.](figures/appendix/antigravity-request-lifecycle.png)

*Figure A1.7 — A simple lifecycle for agent execution.*

This lifecycle is useful pedagogically because many agent failures can be diagnosed by asking which stage failed. Was the plan poor? Was delegation inappropriate? Were the tools wrong? Was review too weak? The lifecycle provides a structured debugging lens.

---

## A1.5 Asynchronous Subagents

One of the most important documented capabilities is **asynchronous subagents**. The overview describes the ability of the main agent to delegate parallel background tasks to concurrent subagents without blocking the user’s flow.

This is one of the defining traits of an agentic system. A simple conversational system answers sequentially. A more capable agent system can **multiply effort through structured delegation**.

![A main agent delegating work to multiple subagents.](figures/appendix/antigravity-asynchronous-subagents.png)

*Figure A1.8 — The main agent can spawn asynchronous background subagents.*

Subagents are particularly useful when work can be decomposed into relatively independent tasks. Examples include:

- running multiple repository analyses,
- examining several code areas in parallel,
- splitting research into topic-specific workstreams,
- generating documentation and tests in separate tracks.

The value of subagents is not only speed. It is also **separation of concerns**.

---

## A1.6 Visual Artifacts and Human Oversight

The overview highlights **visual artifacts** such as plans, code diffs, browser recordings, and reports. These artifacts are important because they make agent behavior inspectable.

![Artifacts feeding into a human review step.](figures/appendix/antigravity-artifact-review-loop.png)

*Figure A1.9 — Visual artifacts support inspection and human review.*

Artifacts support several important goals:

- **trust**: users can see what happened;
- **review**: humans can inspect changes before approval;
- **learning**: teams can study successful and unsuccessful runs;
- **governance**: artifact trails help document actions.

Without artifacts, agent systems become opaque. With artifacts, they become easier to understand and therefore easier to trust.

---

## A1.7 Security and Approval Gates

The documentation emphasizes **security by design**. It references secure local execution, safe defaults, local proxying, and granular tool approval gates.

![A security flow passing agent intent through policy checks and approval before action.](figures/appendix/antigravity-security-approval-flow.png)

*Figure A1.10 — Sensitive actions should pass through policy and approval gates.*

This is especially important in agent systems because autonomy increases both power and risk. A tool-enabled agent that can modify code, touch infrastructure, or interact with external systems needs more guardrails than a passive chatbot.

From an engineering point of view, approval gates are not a sign of weakness. They are a sign of **mature control design**.

---

## A1.8 Scheduled and Long-Running Work

The desktop surface includes scheduled tasks, and the ecosystem as a whole is oriented toward asynchronous execution. This means Antigravity is not limited to short interactive sessions. It can support **long-running and recurring work**.

Examples of scheduled or background-oriented tasks include:

- daily repository health summaries,
- recurring dependency checks,
- weekly prospect research,
- documentation freshness reviews,
- periodic test or quality reports.

This matters because it extends the platform from “an assistant that answers” to “an environment that carries forward useful work over time.”

---

## A1.9 Google Ecosystem Integrations

The overview describes several curated Google integrations:

- **Android** integrations and developer skills,
- **Firebase** skills for areas such as Firestore and Cloud Functions,
- **Web** integration via Chrome and Web MCP servers,
- **Science** skills for biology and chemistry workflows,
- **AGY SDK** skills that help developers build better agents.

A sixth integration matters enough to the WidgetWare build to get its own section: **Stitch**, the Gemini-powered design surface that produces the reviewer-facing screens and their design system. See A1.12.

![The Antigravity ecosystem connected to its documented Google integrations.](figures/appendix/antigravity-integrations-landscape.png)

*Figure A1.11 — Curated integrations increase real-world usefulness.*

The larger architectural point is that ecosystems win by reducing friction. Integrations are important because they help the platform meet users inside established workflows.

---

## A1.10 Antigravity and the Seven Steps to Agent Engineering

This appendix becomes more useful when it is placed into the broader framework of Agent Engineering.

The seven-step structure, as Chapter 2 states it, is:

1. Frame the Use Case  
2. Build Context  
3. Design Agent Capabilities  
4. Build the Harness  
5. Orchestrate Workflows  
6. Engineer Loops  
7. Evaluate & Govern

Antigravity fits most naturally at **Step 4, Build the Harness**, while also touching capability design, workflow orchestration, loops, and the governance half of Step 7.

![Seven-step mapping with Antigravity highlighted at the harness layer.](figures/appendix/antigravity-seven-steps-mapping.png)

*Figure A1.12 — Antigravity is best understood as the harness layer within a broader engineering framework.*

This framing is valuable because it prevents the reader from confusing Antigravity with the entire agent system. Antigravity is a powerful layer, but it still exists inside a larger design space.

---

## A1.11 WidgetWare SDR Example

The WidgetWare SDR case makes the architecture concrete. Imagine a workflow with the following stages:

1. Prospect intake  
2. Account research  
3. Outreach drafting  
4. Manager review  
5. CRM update  
6. Send and track

This is a natural candidate for an agent platform because it is multi-step, partially automatable, and benefits from both delegation and human approval.

![A conceptual WidgetWare SDR architecture showing surfaces, a shared harness, and several specialized agents.](figures/appendix/widgetware-sdr-architecture.png)

*Figure A1.13 — A possible Antigravity-based architecture for WidgetWare SDR.*

Different personas might prefer different surfaces:

- an SDR manager may prefer the **desktop** surface,
- a power user may prefer the **CLI**,
- an application developer may use the **IDE**,
- a platform engineer may use the **SDK**.

This illustrates one of the strengths of the ecosystem model: different users can participate through different surfaces while relying on the same underlying harness.

---

## A1.12 Designing the WidgetWare Front-End with Stitch

Two earlier sections describe something the SDR system cannot run without: **visual artifacts** a reviewer can inspect (A1.6) and an **approval gate** a human passes work through (A1.7). Both imply a screen. Neither says where that screen comes from.

**Stitch** is Google Labs' answer to that question. It is a free AI design surface at `stitch.withgoogle.com` that generates and iterates on user interfaces with Gemini. Standard mode runs on Gemini 2.5 Flash and experimental mode on Gemini 2.5 Pro, each with its own monthly generation allowance — roughly 350 and 50 at the time of writing. That is comfortable for a course and worth re-checking before a workshop depends on it.

### What goes in, and what comes out

Stitch accepts more than a prompt:

- a **prose description** of the screen and who uses it;
- an **image** — a screenshot, a wireframe, a photograph of a whiteboard;
- a **URL**, from which Stitch extracts an existing design system so that new screens match a product that already exists; and
- **voice**, for critique and revision while the canvas is open.

What it produces is the part that matters for this book:

- **multi-screen designs on an infinite canvas**, with follow-on screens generated from the interaction flows the first screen implies;
- **front-end code** — HTML and CSS, Tailwind, and framework targets including React, Vue, Angular, Flutter, and SwiftUI;
- a **paste into Figma**, for the point where a designer takes the work over;
- **`DESIGN.md`**, an agent-readable Markdown file carrying the design system — color, type, spacing, component rules — that can be exported to or imported from other tools; and
- an **MCP server and SDK**, so an agent can retrieve designs directly instead of waiting for a person to export them.

### Why a design tool belongs in an agent-engineering book

The last two outputs are the reason. `DESIGN.md` turns design intent into a text
artifact that lives in the same repository as the agent, is reviewed in the same
change and is read by Antigravity as context. The MCP server turns Stitch into a
controlled integration, following the tool and evidence principles in Chapters 6
and 9.

Design stops being a handoff document and becomes context. That is the same move
Chapter 5 makes with business rules and Chapter 9 makes with evidence, applied
to the interface layer.

### The three WidgetWare screens

The architecture in A1.11 needs precisely three human-facing screens:

1. **Prospect Queue** — what is waiting, how old it is, and what the agent already concluded.
2. **Research Dossier** — the qualification result with its evidence, every claim carrying a visible source.
3. **Outreach Review** — the drafted message beside that evidence, with the approval decision attached.

A workable starting prompt:

```
Design three screens for an internal sales tool used by an SDR manager.

Screen 1 - Prospect Queue: a dense table of accounts awaiting review, showing
company, industry, agent-assigned qualification score, evidence count, and how
long the item has been waiting. Sortable, scannable, no dashboard chrome.

Screen 2 - Research Dossier: one account in depth. Firmographics, the
qualification rationale, and a list of findings where every claim shows its
source link inline. Findings without a source are visibly marked as unsourced.

Screen 3 - Outreach Review: the drafted email on the left, the supporting
evidence on the right, and three actions: Approve, Edit and approve, and
Reject with a required reason.

Desktop web. Light and dark. Restrained enterprise styling, no marketing gloss.
```

From there the loop closes: export `DESIGN.md` into the repository, generate the
interface and use Antigravity to connect it to the agent. The Chapter 8
qualification contract populates the dossier; the rejection reason becomes input
to the Chapter 12 refinement route.

The design loop is therefore: prompt to screens, screens to reviewed design
artifacts and artifacts to implementation context. The exported interface is
still governed by the same repository tests, contracts and approval policy as
the agent runtime.

### Where Stitch fits in the Seven Steps

Stitch is not the harness, and it is not a surface in the sense A1.2 uses the word. It fits in two places:

- **Step 1, Frame the Use Case.** Designing the reviewer's screen forces a decision about what a human must see before approving an outbound message. That is an autonomy-boundary question wearing the costume of a styling question.
- **Step 5, Orchestrate Workflows.** The approval gate is a screen before it is a code path, and the screen determines what the gate can actually enforce.

There is a third, less obvious placement. A rejection with a written reason is a labeled evaluation example, and the review screen is the instrument that collects it. Designed well, the front-end is not only how humans supervise the agent — it is how the evaluation set in **Step 7** gets built.

### Cautions

- **Generated code is a first draft.** Review it before it merges, on the same principle this appendix applies to every other agent output.
- **A convincing screen can make a thin dossier look authoritative.** Insist on the citation slot, and render an unsourced claim as visibly unsourced. Design against the failure mode, not around it.
- **Stitch is a Labs product.** Modes, quotas, and export targets have changed more than once. Verify them before a class session depends on a specific one.

---

## A1.13 Choosing the Right Surface

A simple selection guide can help readers decide where to begin.

![A decision-oriented view that maps common developer needs to the most suitable surface.](figures/appendix/antigravity-surface-selection-guide.png)

*Figure A1.14 — A practical guide for choosing the most suitable product surface.*

A useful rule of thumb is:

- choose **Desktop** when visibility and orchestration matter,
- choose **CLI** when speed and terminal locality matter,
- choose **SDK** when programmatic control matters,
- choose **IDE** when code context matters most.

In practice, teams may use more than one surface. A developer might explore through the CLI, work daily in the IDE, and later move a repeatable pattern into the SDK.

---

## A1.14 Key Takeaways

Five final ideas capture the essence of the Antigravity ecosystem:

1. Antigravity is an **ecosystem of surfaces**, not a single interface.
2. The **shared harness** is the architectural center of gravity.
3. **Asynchronous subagents**, **visual artifacts**, and **approval gates** are core differentiators.
4. **Curated integrations** help the platform fit real workflows.
5. The most useful way to place Antigravity is inside a broader **Agent Engineering** framework.

For the book, this appendix should be read as a conceptual companion: it helps the reader understand where Antigravity fits, what makes it interesting, and how it can be connected to the larger practice of engineering reliable agent systems.
