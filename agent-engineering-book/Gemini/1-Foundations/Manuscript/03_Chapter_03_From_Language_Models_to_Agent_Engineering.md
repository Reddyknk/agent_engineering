# Chapter 3: From Language Models to Agent Engineering

*Understanding the WidgetWare SDR System*

## Product version

**V0 — problem framing and system boundary**

This chapter turns a broad SDR ambition into a scoped agent-engineering problem. V0 does not automate production work yet; it defines the user, outcome, constraints, evidence requirements and Google Cloud boundary that every later version must preserve.

## Engineering question

**What must be true before an SDR assistant is safe and specific enough to build?**

## Chapter purpose

This chapter establishes V0's conceptual and business foundation. The reader
learns why a language model is a capability rather than a complete system, when
agent behavior is justified, how autonomy should be bounded and where Sales
Development Representatives fit within a formal business-to-business sales
process.

Chapter 3 does not reveal or implement the final architecture. It defines the
problem, authority boundary, expected artifacts, risks, unknown targets and
evidence contract. Architecture will emerge later from observed need.

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish a model, assistant, workflow, agent, and agentic system;
- identify work that should remain deterministic rather than be delegated to an agent;
- explain the seven-level autonomy spectrum and select an appropriate level for a business system;
- describe the Seven Steps to Agent Engineering and map them to WidgetWare SDR;
- explain the formal B2B sales lifecycle and the role of an SDR within it;
- distinguish pre-contact account qualification from full opportunity qualification;
- describe the Book 1 WidgetWare workflow, artifacts, and approval boundary;
- identify the minimum Google Cloud capabilities required to begin safely;
- define a version-neutral evidence and reproduction contract; and
- write measurable business, quality, safety, and operational acceptance criteria.

## Seven-Step mapping

**Primary:** Frame the Use Case  
**Supporting:** Build Context; Build the Harness; Evaluate & Govern

## The WidgetWare increment

Create the V0 product and evidence brief for the WidgetWare SDR system:

- business objective;
- intended users and stakeholders;
- sales-process position;
- inputs, outputs, and intermediate artifacts;
- tasks assigned to model reasoning;
- tasks enforced by deterministic software;
- actions reserved for human authority;
- initial Google Cloud project boundary;
- KPIs, SLOs, risks, assumptions and `NEEDS TARGET` items;
- explicit exclusions and prohibited capabilities; and
- measurable acceptance criteria.

No agent code is required in this chapter.

---

## A Monday morning at WidgetWare

At 9:00 a.m. on Monday, WidgetWare’s sales manager gives an SDR a list of 200 manufacturing companies. One of them, Acme Manufacturing, appears promising. It has approximately 22,000 employees, operates plants in several countries, and recently announced an initiative involving artificial intelligence and manufacturing modernization.

The account looks attractive, but the SDR cannot act on impressions alone. Before investing time or contacting anyone, the SDR must answer several questions:

- Does Acme match WidgetWare’s ideal customer profile?
- Which company facts are current and verified?
- Is the announced initiative genuinely relevant to WidgetWare’s products?
- What is known, what is inferred, and what remains unknown?
- Are there exclusion criteria that make the account unsuitable?
- Is the evidence sufficient to justify outreach?
- Which buyer role would most likely care about the problem?
- What could WidgetWare truthfully say in a first message?
- Who must review the message before any external communication occurs?

Gemini can help interpret announcements, compare several weak signals, summarize evidence, and draft a concise message. But Gemini should not decide by itself which sources are approved, whether mandatory evidence is present, whether an exclusion rule applies, whether a workflow stage has completed, or whether an external message may be sent.

That difference is the subject of this book.

> **A model produces possible intelligence. An engineered system assigns responsibility, evidence, and boundaries to that intelligence.**

---

## 3.1 A model is a capability, not a system

A language model can summarize, classify, compare, draft, infer, extract, and reason. Those capabilities are powerful, but they do not constitute a dependable business system.

A model does not inherently know the current business objective, which source is authoritative, what customer data it may access, which output contract downstream software expects, which state transition is legal, whether approval exists, or how success will be measured. Those responsibilities belong to the engineered system around it.

| Requirement | Model contribution | Engineered system responsibility |
|---|---|---|
| Interpret an ambiguous announcement | Relates language to possible business meaning | Supplies bounded context and records uncertainty |
| Retrieve current account data | Chooses when information may be useful | Calls a narrow, permissioned tool |
| Determine whether a source is approved | May describe the source | Enforces source and provenance policy |
| Return a stable qualification status | Recommends a status | Validates a typed contract and business invariants |
| Remember workflow state | Uses supplied history | Persists state outside the model |
| Prevent unauthorized outreach | May follow an instruction | Removes the capability or enforces an external gate |
| Explain a decision | Generates a rationale | Preserves evidence and execution history |
| Measure improvement | Cannot judge itself objectively | Uses tests, datasets, metrics, and human review |

A system can fail even when the final prose sounds good:

- **Plausible but unsupported:** the model invents an employee count.
- **Correct answer, unsafe route:** the draft is accurate, but the workflow bypasses evidence review.
- **Valid output, wrong decision:** the schema passes, but an exclusion criterion is ignored.

The design pattern for Book 1 is therefore:

- let the model interpret, synthesize, compare, and draft;
- let deterministic software validate, authorize, persist, route, count, and enforce; and
- let people retain authority over consequential external actions.

## 3.2 Models, assistants, workflows, agents, and agentic systems

Agent terminology is often used loosely. Precise vocabulary improves architecture because different system types require different controls.

| Term | Primary characteristic | WidgetWare example |
|---|---|---|
| **Model** | Supplies language and reasoning capability | Gemini compares evidence with an ICP |
| **Assistant** | Responds to a user inside an interaction | A chat interface explains why an account may fit |
| **Workflow** | Executes a predefined sequence | Research → qualify → review → draft → approval |
| **Agent** | Selects or adapts actions in pursuit of a goal | A research agent decides which approved tool to call next |
| **Agentic system** | Combines agents with context, tools, state, policies, workflows, evaluation, and oversight | The complete WidgetWare SDR application |

A workflow and an agent are not opposites. A well-designed system can place agent reasoning inside a deterministic workflow. The workflow defines the permitted stages and state transitions; an agent contributes judgment within a stage.

For example, the WidgetWare workflow determines that evidence review must occur before outreach drafting. Within the research stage, an agent may decide that an official company announcement is more relevant than a directory listing. The agent has discretion, but only inside a larger structure.

Likewise, multiple agents do not automatically create a better system. Specialization is useful when responsibilities have different goals, context, tools, permissions, output contracts, or evaluation criteria. Splitting one simple task into many named agents merely creates more handoffs and more places for failure.

The objective is not to maximize the number of agents. The objective is to assign each kind of work to the component best suited to perform and control it.

---

## 3.3 When not to use an agent

Agent Engineering includes the judgment to avoid agents when ordinary software is sufficient.

Use deterministic software when the behavior is known, repeatable, and mechanically verifiable. Consider agent reasoning when interpretation, synthesis, adaptive selection, or judgment is necessary.

| Task characteristic | Prefer deterministic software | Consider bounded agent reasoning |
|---|---|---|
| Rules are complete and stable | Yes | Usually unnecessary |
| Inputs are structured and predictable | Yes | Only if interpretation remains necessary |
| Exact repeatability is required | Yes | Only in a supporting role |
| Correctness can be mechanically verified | Yes | Agent may add little value |
| Natural-language interpretation is required | Limited | Yes |
| Several weak signals must be combined | Difficult | Yes |
| Evidence must be synthesized | Difficult | Yes |
| Several reasonable approaches exist | Limited | Yes |
| The action has significant consequences | Deterministic authorization | Agent may recommend or prepare |
| Quality requires domain judgment | Limited | Yes, with evaluation |

Apply the distinction to WidgetWare:

- Checking whether `employee_count >= minimum_employee_count` is deterministic.
- Normalizing `USA`, `United States`, and `US` can be deterministic.
- Validating that a qualification status belongs to an enumeration is deterministic.
- Confirming that approval exists before an external action is deterministic.
- Interpreting whether an announcement signals a genuine modernization initiative may require model reasoning.
- Comparing several incomplete signals and explaining uncertainty may require model reasoning.
- Drafting a concise message from approved facts benefits from model reasoning.

A useful architectural question is:

> **If the required behavior can be stated completely as rules and tested mechanically, what does an agent add besides variability?**

Sometimes the honest answer is: nothing.

---

## 3.4 Autonomy is an engineering decision

Autonomy should be selected deliberately rather than inherited from a tool’s maximum capabilities.

A practical spectrum is:

| Level | Capability | WidgetWare example |
|---:|---|---|
| 1 | **Answer** | Explain whether an industry is generally relevant |
| 2 | **Recommend** | Recommend whether an account merits research |
| 3 | **Draft** | Draft an account summary or outreach message |
| 4 | **Prepare** | Assemble a complete approval package for a person |
| 5 | **Execute with approval** | Send only after an authorized person approves |
| 6 | **Execute within policy** | Send automatically inside narrow, preapproved limits |
| 7 | **Open-ended autonomy** | Select targets, strategies, channels, and actions broadly |

Book 1 implements **Level 4: Prepare**. It performs research, recommends a qualification status, drafts outreach, creates an approval package, and records an approval or rejection decision. It deliberately does **not** implement message delivery.

This distinction matters. A system cannot truthfully claim Level 5 merely because it displays an Approve button. Level 5 requires an executable external action that becomes available only after valid approval. Book 1 constructs the approval boundary needed for such a future capability, but the send tool itself is absent.

The absence is structural, not rhetorical. The system is safe from autonomous outreach because there is no external communication capability for the model or workflow to invoke.

A higher autonomy level is not necessarily more advanced. It is more consequential. The correct level depends on:

- reversibility of the action;
- cost of an incorrect action;
- sensitivity of the data;
- maturity of evaluation;
- clarity of policy;
- strength of identity and authorization;
- quality of monitoring and audit trails; and
- availability of a responsible human owner.

For WidgetWare, research and drafting are reversible. Sending a misleading message to a real prospect is not. The system therefore automates preparation and preserves human control over communication.

---

## 3.5 The Seven Steps to Agent Engineering

The Seven Steps are the series' vendor-independent vocabulary for the kinds of work an agent system requires, across Gemini, ADK, Antigravity, tools, Skills, workflows, loops, and Google Cloud services. The technologies are implementations; the steps describe the engineering work. They do not, by themselves, say which work to do next — that is what the Observe → Ask → Decide → Change → Prove cycle in Chapter 2 decides, and it is the cycle that determines this book's chapter order.

### Figure 3.1 — The Seven Steps to Agent Engineering

<div class="figure-page landscape">
  <img src="figures/chapter1/the-seven-steps-to-agent-engineering.png" alt="Figure 3.1 — The Seven Steps to Agent Engineering" />
</div>

| Step | Engineering question | WidgetWare result |
|---|---|---|
| **1. Frame the Use Case** | What outcome, users, boundaries, and autonomy level are allowed? | SDR charter, sales-process position, scope, exclusions, and approval boundary |
| **2. Build Context** | What information may Gemini reason over? | Product facts, ICP, policy, account data, task state, and retrieved evidence |
| **3. Design Agent Capabilities** | Which reusable procedures and controlled actions are required? | Skills, typed contracts, internal tools, and MCP-enabled research |
| **4. Build the Harness** | Where is the system specified, built, tested, and run? | Antigravity workspace, repository conventions, ADK runtime, permissions, and tests |
| **5. Orchestrate Workflows** | In what order does work occur, and which transitions are legal? | Research → qualify → review → draft → approval |
| **6. Engineer Loops** | How does the system process repeated work safely? | Account queue, durable state, checkpoints, budgets, retries, stopping, and escalation |
| **7. Evaluate & Govern** | How do we know the system is useful and remains within its boundaries? | Golden dataset, release gates, traces, policies, least privilege, and human control |

The numbered steps are not a rigid chapter order. Chapter 4 builds the development
harness before Chapter 5 completes the monolithic agent and its context because
the reader needs a disciplined workspace in which to place business rules.

Evaluation and governance appear as Step 7 because they provide the evidence
required to release and improve the system. They are cross-cutting disciplines.
We define acceptance criteria in Chapter 3, write tests while building the harness,
preserve evidence during research, enforce approval during orchestration, verify
progress inside loops and perform integrated evaluation before release.

A useful mental model is:

> **The Seven Steps form a lifecycle, but evaluation and governance form the feedback system around that lifecycle.**

---

## 3.6 Understanding B2B sales and the SDR role

WidgetWare sells software to other businesses. This is a business-to-business, or **B2B**, sales environment. B2B purchases often involve multiple stakeholders, longer decision cycles, technical validation, procurement, security review, and formal approval.

**SDR** stands for **Sales Development Representative**. An SDR usually works near the beginning of the sales process. Depending on the company, the role may focus on inbound lead qualification, outbound prospecting, or a combination of both. Some organizations use **Business Development Representative (BDR)** for outbound work and SDR for inbound work; others use the terms interchangeably. Account Executives, or **AEs**, generally accept qualified prospects, conduct deeper discovery, develop opportunities, propose solutions, negotiate, and close business.[^sales-roles]

For this book, *WidgetWare SDR* is an umbrella term for the early-stage research and qualification function. The system helps a human sales-development team:

- understand a target account;
- compare the account with the Ideal Customer Profile;
- collect and classify supporting evidence;
- identify relevant business signals;
- explain fit and uncertainty;
- draft evidence-backed outreach; and
- prepare a controlled handoff for human review.

It is important to distinguish **account qualification** from **full sales qualification**.

Before contact, WidgetWare can estimate whether a company appears to fit the target profile and whether there is a plausible reason to engage. It cannot confirm a prospect’s budget, decision authority, purchase timeline, internal priorities, or willingness to change. Those facts usually require a conversation with the customer.

Therefore, WidgetWare produces a **pre-contact qualification recommendation**, not a final declaration that a sale is real. A human SDR and later an Account Executive remain responsible for validating need, authority, budget, timing, decision criteria, and the buying process.

---

## 3.7 The formal B2B sales process

A sales process is the defined sequence through which a company identifies potential customers, determines whether a genuine opportunity exists, develops a solution, reaches a commercial decision, and manages the relationship after the sale. The exact stages vary, but commonly span research, prospecting or lead generation, qualification, sales conversations, closing, and relationship building.[^sales-process]

### Figure 3.2 — End-to-end B2B sales lifecycle

<div class="figure-page landscape">
  <img src="figures/chapter1/end-to-end-b2b-sales-lifecycle.png" alt="Figure 3.2 — End-to-End B2B Sales Cycle" />
</div>

| Stage | Typical owner | Primary artifact |
|---|---|---|
| Define ICP and campaigns | Marketing and sales leadership | ICP, buyer roles, target criteria |
| Generate or capture leads | Marketing, partners, outbound teams | Lead or target-account record |
| Research and initial qualification | SDR or BDR | Account brief and recommendation |
| Discovery and opportunity | Account Executive | Discovery notes and opportunity record |
| Technical validation | Solutions consultant or architect | Demonstration, architecture, or POC |
| Proposal and negotiation | AE, legal, procurement | Proposal, approvals, and contract |
| Adoption and expansion | Delivery, customer success, account management | Success plan, renewal, expansion |

A formal process uses **stage gates**. A company name is not a qualified lead; sending an email does not create an opportunity; a demonstration does not prove need; and enthusiasm is not a signed contract. Work advances because evidence exists, not merely because a seller—or an agent—completed an activity.

A **sales process** defines *what stages occur*. A **sales methodology** defines *how people execute them*. WidgetWare supports evidence-based account research and pre-contact qualification; it does not automate human discovery, negotiation, or relationship judgment.

## 3.8 The SDR operating process

The SDR portion of the sales lifecycle can itself be represented as a controlled workflow.

### Figure 3.3 — Human SDR operating process

<div class="figure-page landscape">
  <img src="figures/chapter1/the-sdr-operating-process.png" alt="Figure 3.3 — The SDR Operating Process" />
</div>

The diagram describes a human sales-development process. Book 1 automates selected preparation stages, not the entire sales function.

| SDR activity | Book 1 treatment |
|---|---|
| Accept a supplied target account | Implemented |
| Retrieve approved internal account data | Implemented |
| Research permitted external sources | Implemented |
| Evaluate ICP fit | Implemented |
| Identify missing or conflicting evidence | Implemented |
| Produce a structured qualification result | Implemented |
| Identify likely buyer roles at a role level | Supported as analysis, not personal-data enrichment |
| Draft account-level outreach | Implemented |
| Review factual support | Implemented |
| Prepare an approval package | Implemented |
| Record approval, rejection, or revision | Implemented |
| Discover or scrape personal contact information | Not a primary Book 1 capability |
| Conduct a qualification call | Human responsibility |
| Create or modify a CRM opportunity | Outside Book 1 |
| Send email or social messages | Deliberately absent |

The boundary prevents a common category error. Research evidence that an account resembles WidgetWare’s customers is not evidence that an individual has agreed to speak, has budget, or can authorize a purchase. The system may recommend an account for human attention; it must not manufacture customer intent.

---

## 3.9 Why SDR is an effective Agent Engineering case

WidgetWare SDR is not merely a convenient demonstration. It is a compact representation of the tensions found in many enterprise agent systems.

| Engineering concern | SDR manifestation |
|---|---|
| Ambiguous information | Announcements rarely state a customer need directly |
| Dynamic context | Company size, leadership, strategy, and initiatives change |
| Evidence requirements | Qualification and outreach claims must be traceable |
| Deterministic and probabilistic work | Thresholds are deterministic; interpreting signals requires judgment |
| Controlled tools | Internal account records and external research sources have different permissions |
| Reusable Skills | Qualification and evidence classification are repeatable procedures |
| Structured contracts | Research briefs and qualification results feed later stages |
| Multi-agent specialization | Research, qualification, review, drafting, and coordination differ |
| Human authority | External communication is consequential |
| Evaluation | Representative accounts can test useful and unsafe behavior |
| Loops | Many accounts must be processed without repeating settled work |

The case is also understandable to readers who are not sales professionals. Almost everyone can recognize the difference between researching a company, recommending a next step, drafting a message, and sending it. That progression makes autonomy and approval concrete.

Most importantly, the use case rewards disciplined engineering. A one-prompt demonstration can appear impressive, but it quickly fails when asked to preserve provenance, handle contradictions, enforce exclusions, return machine-readable results, recover from partial failure, or prove that no unauthorized communication occurred.

---

## 3.10 The WidgetWare business brief

WidgetWare is a fictional B2B software company. It sells a configurable platform that helps manufacturing and industrial organizations connect fragmented plant systems, digitize manual workflows, improve operational visibility, and introduce AI-assisted decisions without replacing every legacy investment at once.

### Initial Ideal Customer Profile

An **Ideal Customer Profile (ICP)** describes the type of organization most likely to benefit from the offering. It differs from a buyer persona, which describes a role inside that organization.

| Dimension | Initial WidgetWare criterion |
|---|---|
| Industry | Manufacturing, industrial automation, logistics, or related industrial operations |
| Size | Mid-market to large enterprise; thresholds become configurable in Chapter 5 |
| Geography | United States, Europe, and India |
| Operating environment | Multiple plants, fragmented systems, legacy operational technology, or manual workflows |
| Strategic signal | Digital transformation, smart-factory, AI modernization, or efficiency initiative |
| Exclusions | Very small firms, purely consumer businesses, unsupported regions, or companies without relevant industrial operations |

Likely buyer or influencer roles include operations, digital, information-technology, manufacturing-technology, industrial-automation, enterprise-architecture, and operational-excellence leaders.

Relevant trigger events include a new transformation leader, smart-factory initiative, plant expansion, acquisition, industrial-AI hiring, or a public modernization program. A trigger is not proof of need; it is a reason for focused research.

WidgetWare classifies information as:

- **verified fact** — directly supported by an approved source;
- **derived fact** — deterministically calculated from verified facts;
- **inference** — a reasoned but uncertain conclusion;
- **unknown** — insufficient evidence;
- **conflict** — credible sources disagree; or
- **prohibited claim** — a statement the system may not make.

Later Skills, contracts, and evaluation cases use this vocabulary consistently.

## 3.11 The Book 1 business workflow and artifacts

The completed Book 1 system transforms a supplied target account into an inspectable approval package.

### Figure 3.4 — WidgetWare information and artifact flow

<div class="figure-page landscape">
  <img src="figures/chapter1/widgetware-sdr-information-and-artifact-flow.png" alt="Figure 3.4 — WidgetWare SDR Information & Artifact Flow" />
</div>

The flow introduces an important architectural principle:

> **Agents exchange structured business artifacts, not complete conversation transcripts.**

Each artifact exists for a reason:

- `AccountProfile` normalizes the supplied account and approved internal facts.
- The **Evidence Ledger** preserves source identity, date, excerpt, reliability, and the claims supported.
- `ResearchBrief` summarizes relevant evidence, contradictions, unknowns, and trigger events.
- `QualificationResult` records the decision, score, matched criteria, exclusions, missing information, and next step.
- `EvidenceReview` identifies which claims may be used in outreach.
- `OutreachDraft` contains a proposed message based only on reviewed facts.
- `ApprovalPackage` brings the decision, evidence, draft, and risk flags together for a person.
- `ApprovalRecord` records approve, reject, or revise without creating an external side effect.

The workflow uses model reasoning to produce and interpret artifacts. Deterministic code validates contracts, enforces state transitions, and ensures that unreviewed evidence cannot silently enter a later stage.

---

## 3.12 The V0 Google Cloud boundary

V0 chooses a Google Cloud project, region and identity boundary without pretending
to know the final topology. The first environment needs only enough capability to:

- authenticate a developer and later a runtime identity;
- call the configured Gemini model through the project;
- write deliberate logs and traces;
- store bounded evaluation and artifact evidence; and
- attribute resources and cost to the learning workload.

The final runtime, workflow shape, storage services and deployment topology remain
open decisions. They will be selected when the product produces evidence about
security, reliability, latency, cost and durability.

### The evidence contract

Every later version must retain:

| Evidence | Purpose |
| --- | --- |
| Representative accounts | Compare the same business situations |
| Output contract | Compare stable required properties |
| SLO vocabulary | Define acceptable quality, latency and cost |
| Adversarial case | Verify that protection does not regress |
| Run manifest | Record code, prompt, model, data and environment versions |
| Trace and artifact IDs | Connect behavior to operational evidence |

Unknown values are written as `NEEDS TARGET`; they are not silently invented.

## 3.13 System boundaries and human control

A system boundary states what the system can do and what it must remain unable to do.

### In scope

- accept a supplied target account;
- retrieve approved internal data and permitted external evidence;
- preserve provenance and represent uncertainty;
- compare an account with configured ICP criteria;
- produce structured research, qualification, review, and draft artifacts;
- assemble and record an approval decision;
- process a bounded queue with checkpoints, budgets, and named stopping reasons; and
- produce evaluation and run reports.

### Out of scope

- uncontrolled autonomous prospect discovery or indiscriminate scraping;
- collection of unnecessary personal data;
- autonomous email, social, or message delivery;
- CRM writes, opportunity creation, pricing, or contractual commitments;
- bypassing authentication or source restrictions;
- presenting inferred intent as customer fact; and
- self-modifying policies, permissions, or budgets.

These items are not all excluded for the same reason. External message delivery — the second item above — is structurally absent from Book 1: there is no send tool, with or without approval, and no later chapter adds one. CRM writes, opportunity creation, pricing, and contractual commitments are different: Book 1 simply does not build them yet, and a future system could add them behind the same kind of approval gate this book already builds for outreach. The remaining items — uncontrolled scraping, unnecessary personal data, bypassing authentication, and presenting inference as fact — are not scope decisions at all; approval would not make any of them acceptable, in Book 1 or any later system.

| Responsibility | Model | Deterministic software | Human |
|---|---:|---:|---:|
| Interpret evidence | Primary | Supplies bounded context | Reviews uncertainty |
| Enforce hard thresholds | Explains | Primary | Defines policy |
| Select approved tools | Bounded | Enforces allowlist | Approves integrations |
| Recommend qualification | Primary | Enforces invariants | Accepts or challenges |
| Draft outreach | Primary | Restricts inputs to reviewed facts | Reviews wording |
| Record workflow state | No | Primary | Explicit override only |
| Approve outreach | No | Records the decision | Primary |
| Send outreach | No capability | No capability in Book 1 | Outside Book 1 |

Human-in-the-loop control is not a polite prompt instruction. It is expressed through missing capabilities, authorization rules, state transitions, audit records, and interfaces.

## 3.14 Define success before implementation

“Produces a good answer” is not a sufficient acceptance criterion. Success must be stated in terms that can later be tested.

### Business success

- A representative target account can be evaluated from supplied and retrieved information.
- The result explains why the account does or does not appear to fit.
- The approval package reduces manual preparation while remaining understandable to an SDR.
- The handoff gives a human enough context to decide what should happen next.

### Quality success

- Every qualification conforms to its contract.
- Every decisive factual claim links to evidence.
- Missing information is explicit.
- Contradictory evidence remains visible.
- Inference is never presented as verified fact.
- Outreach uses only claims approved by evidence review.

### Safety and control success

- Retrieved instructions cannot override system policy.
- External communication is structurally unavailable.
- Approval cannot be inferred from natural-language text.
- Tool permissions are narrower than the underlying platform account.
- Secrets and unnecessary personal data are absent from outputs and logs.
- Policy or parsing failure produces a safe blocked state rather than a guessed result.

### Operational success

- Another learner can run the project from documented instructions.
- Failures produce named states and actionable next steps.
- A case can be traced across agents, tools, contracts, and state transitions.
- A restarted process resumes from persisted checkpoints.
- A batch run stops at declared limits and reports a named reason.
- The deployed version can be rolled back.

These criteria will evolve into tests, evaluation cases, release gates, and operational checks throughout the book.

---

## Hands-on lab: Frame the WidgetWare SDR system

Create the initial repository artifacts:

```text
README.md
SPEC.md

docs/
├── widgetware-business-brief.md
├── sales-process.md
├── sdr-workflow.md
├── autonomy-boundary.md
├── google-cloud-boundary.md
├── evidence-contract.md
├── version-map.md
├── acceptance-criteria.md
└── architecture-decisions/
    ├── ADR-001-use-an-agent.md
    ├── ADR-002-human-approval.md
    └── ADR-003-defer-final-topology.md

tests/
└── scenarios/
    ├── qualified-account.md
    ├── unqualified-account.md
    ├── insufficient-evidence.md
    ├── conflicting-evidence.md
    └── prohibited-send-request.md
```

Complete the following tasks:

1. State the business objective in one paragraph.
2. Identify the primary user, decision-maker, reviewer, and downstream Account Executive.
3. Place WidgetWare within the end-to-end sales lifecycle.
4. Draw the SDR workflow and mark which stages Book 1 automates.
5. Classify every activity as model reasoning, deterministic software, or human authority.
6. Select the Book 1 autonomy level and justify why the next level is not implemented.
7. Define the expected artifacts from `AccountProfile` through `ApprovalRecord`.
8. Mark every known external system and trust boundary without choosing the final topology.
9. Write measurable acceptance criteria under business, quality, safety, and operational headings.
10. Confirm that no external send capability appears in the specification, architecture, tools, or tests.

Do not implement an ADK agent yet.

## Evaluation checklist

- Is the business objective explicit and tied to the sales process?
- Is the difference between account fit and full sales qualification clear?
- Are model, software, and human responsibilities separated?
- Is Book 1 correctly positioned at autonomy Level 4?
- Are external actions clearly bounded?
- Is human approval represented as state and authority rather than prompt wording?
- Does every initial Google Cloud capability have a required V0 responsibility?
- Have final architectural decisions been left open until evidence exists?
- Are evidence and inference treated differently?
- Can every acceptance criterion be tested or reviewed without asking the author what it means?
- Does the architecture avoid using an agent where deterministic logic is sufficient?
- Is message delivery structurally absent?

## Chapter checkpoint

The repository now contains a clear business definition, formal sales-process
position, autonomy boundary and measurable success criteria for WidgetWare SDR.

The reader should be able to explain:

- what the system will do;
- what it will not do;
- which work requires model reasoning;
- which decisions remain deterministic;
- which authority remains human;
- what the initial Google Cloud boundary must provide; and
- what evidence will demonstrate success.

## Bridge to Chapter 4

The next chapter builds the engineering harness in Google Antigravity. Before
giving Gemini or ADK more capability, we create the workspace, repository
conventions, specifications, permissions, test discipline, version directories
and review cycle that will keep evolution inspectable.

## Exercises

1. **Choose the correct system type.** Describe one task as a deterministic program, workflow, and agent. Which representation is justified, and why?

2. **Apply the autonomy spectrum.** Select the highest level you would permit for that task today. What evidence or control is required before allowing the next level?

3. **Separate account fit from opportunity qualification.** List three facts WidgetWare can establish before contact and three that require a customer conversation.

4. **Design a stage gate.** Choose one SDR transition and specify its entry criteria, exit criteria, required artifact, and failure state.

5. **Find the deterministic core.** For three WidgetWare activities, state what the model may decide and what software must never let it decide alone.

6. **Write a prohibited-action test.** Define the expected output, workflow state, tool trajectory, and audit evidence when a user asks the system to send outreach immediately.

## References

[^sales-process]: Salesforce Trailhead, [“Learn About the Sales Process”](https://trailhead.salesforce.com/content/learn/modules/build-a-sales-process/learn-about-the-sales-process), describing research, lead generation, sales call and close, and relationship building as core stages that organizations adapt to their context.

[^sales-roles]: Salesforce Trailhead, [“Optimize Your Business Pipeline for Success”](https://trailhead.salesforce.com/content/learn/modules/business-pipeline-quick-look/build-your-pipeline-engine), illustrating how SDR, BDR, and Account Executive responsibilities can be divided. Terminology varies across organizations.

[^gcp-reference-architecture]: Google Cloud Architecture Center, [“Single-agent AI system using ADK and Cloud Run”](https://docs.cloud.google.com/architecture/single-agent-ai-system-adk-cloud-run), reference architecture using ADK, Cloud Run, MCP integrations, and Google Cloud Observability.

[^adk-components]: Google Cloud Architecture Center, [“Choose your agentic AI architecture components”](https://docs.cloud.google.com/architecture/choose-agentic-ai-architecture-components), describing ADK as a modular framework for simple through multi-agent workflows.

[^antigravity]: Google Antigravity, [“Antigravity IDE”](https://antigravity.google/product/antigravity-ide), describing the editor, agent operation across editor, terminal, and browser, and artifact-based review.

[^scheduled-jobs]: Google Cloud Documentation, [“Execute jobs on a schedule”](https://docs.cloud.google.com/run/docs/execute/jobs-on-schedule), documenting authenticated scheduling of Cloud Run jobs through Cloud Scheduler.
