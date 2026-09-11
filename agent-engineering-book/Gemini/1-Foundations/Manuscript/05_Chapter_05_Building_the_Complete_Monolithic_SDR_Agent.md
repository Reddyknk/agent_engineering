# Chapter 5: Building the Complete Monolithic SDR Agent

*Proving the complete business outcome before adding topology*

## Chapter purpose

This chapter produces V1: the simplest complete WidgetWare SDR product. One broad
ADK `LlmAgent` receives a deliberately assembled context package, uses bounded
read-only capabilities, researches and qualifies one account, drafts outreach and
saves an approval package. The architecture is intentionally monolithic so later
complexity must improve a measured baseline.

## Product version

**Starting point:** V0 — scoped use case and reproducible harness  
**Result:** V1 — complete monolithic SDR agent

## Engineering question

> Can the simplest complete product deliver the SDR outcome end to end?

## Learning objectives

By the end of this chapter, the reader should be able to:

- configure one baseline model without optimizing prematurely;
- distinguish system instructions, business context, task context, and retrieved evidence;
- separate stable policy from dynamic data;
- design an evidence policy;
- identify context pollution and prompt-injection risks; and
- build and run one ADK `LlmAgent`;
- use sessions, events, state and bounded tools;
- produce a structured SDR approval package;
- capture a basic trace and run manifest; and
- test whether the complete product follows the intended scope.

## Seven-Step mapping

**Primary:** Build Context  
**Supporting:** Frame the Use Case; Evaluate & Govern

## The WidgetWare increment

Create one complete monolithic SDR agent with role, business rules, ideal-customer
profile, product facts, evidence policy, output expectations and prohibited
behavior. It must produce a saved account package but cannot send outreach or
write to production CRM.

## 5.1 Context is a designed operating environment

Chapter 3 defined the business boundary and Chapter 4 created the harness. Chapter
5 now asks what one complete but structurally simple agent can accomplish.

> What exactly should Gemini see when it is asked to reason about a target account?

That question matters because the model does not operate in a vacuum. A model is powerful, but it is also permissive. If the system supplies ambiguous rules, duplicated instructions, stale evidence, or uncontrolled notes, the model will still attempt to produce a plausible answer. Context engineering exists to prevent that drift.

For WidgetWare SDR, the model is not being asked to “know everything about sales.” It is being asked to perform one bounded task inside one bounded system:

- interpret a target account in light of WidgetWare’s ideal customer profile;
- consider approved business rules and exclusions;
- review evidence from permitted sources;
- represent uncertainty honestly; and
- return a structured result that the next step can inspect.

That means context is not a decorative prompt. It is part of the architecture. It determines what the model is allowed to consider, what it must ignore, what it must never claim without support, and how its answer will be judged.

A helpful mental model is this:

- **the model** provides probabilistic reasoning;
- **the harness** provides an engineered environment for development and testing;
- **context** provides the information boundary for each reasoning step.

If the boundary is sloppy, the model’s apparent intelligence quickly becomes operational ambiguity.

## 5.2 Model choice is an architectural decision

Different Gemini model configurations offer different tradeoffs in reasoning depth, response time, context capacity, and cost. Book 1 should begin with one supported Gemini model and keep the model identifier configurable.

Do not scatter model names throughout the code. Centralize model selection so that evaluation can compare alternatives later. In practice, that usually means one configuration file, one registry, or one factory function that resolves the model to use for a particular class of task.

The correct question is not “Which model is best?” It is:

> Which model provides sufficient quality for this task under the required latency and cost constraints?

That wording is important. It turns model selection from a branding discussion into an engineering discussion. For WidgetWare SDR, different activities may value different things:

- a quick account triage step may prioritize low latency and low cost;
- a qualification step may tolerate slightly more latency if it improves reliability;
- a long review step may require larger context capacity because it synthesizes multiple evidence items.

A common early mistake is to choose the largest or most capable model for every step. That often works in a prototype, but it hides two production questions:

1. Is the additional cost justified by measurable quality improvement?
2. Could a smaller or faster configuration produce sufficient quality for the same business decision?

Book 1 deliberately avoids premature optimization. The right first move is to choose one supported Gemini model, keep its identifier configurable, and build the evaluation and logging needed to compare alternatives later.

### Figure 5.1 — Model Selection as an Architectural Decision

<div class="figure-page landscape">
  <img src="figures/chapter3/model-selection-as-an-architectural-decision.png" alt="Figure 5.1 — Model Selection as an Architectural Decision" />
</div>

A practical model-selection policy for Book 1 is simple:

- use one supported Gemini model as the default for the chapter exercises;
- define the model identifier in configuration rather than inline in agent code;
- record quality, latency, and cost observations during evaluation; and
- defer model comparison until the surrounding context and contracts are stable.

In other words, avoid changing both the model and the surrounding system at the same time. If the context package is unstable, changing the model will tell you very little.

## 5.3 Layers of context

Use separate context layers rather than one undifferentiated prompt. This chapter uses five core layers and one output layer.

### System instructions

System instructions define stable behavioral rules:

- the agent’s role;
- scope;
- safety constraints;
- communication style;
- prohibited actions; and
- escalation requirements.

These should change rarely. They are not about the current target account. They define how the agent is expected to behave across many requests.

### Business context

Business context contains WidgetWare-specific knowledge:

- product definitions;
- ideal-customer profile;
- qualification rules;
- excluded industries;
- approved claims; and
- escalation rules.

This is still fairly stable, but it is domain-specific rather than universal.

### Task context

Task context contains the information specific to the current request:

- target account;
- user objective;
- current workflow stage;
- supplied notes; and
- requested deliverable.

Task context changes every run. It is not policy. It is the situation the agent is being asked to evaluate.

### Retrieved evidence

Retrieved evidence is tool or MCP output that supports the current decision. Evidence should include source identity, retrieval time, and a compact excerpt or normalized fact.

### State

State contains structured information from previous steps, such as an account identifier, research status, qualification status, or approval decision. State differs from evidence because it is produced by the workflow itself rather than fetched from external sources.

### Output expectations

The system must also define what the agent is expected to return:

- required fields;
- allowed decision values;
- how uncertainty is represented;
- when escalation is required; and
- what must never be omitted.

Many prompt failures are actually output-design failures. If the agent is expected to decide, explain, cite evidence, and identify uncertainty, those expectations must be explicit.

### Figure 5.2 — Layers of Context for WidgetWare SDR

<div class="figure-page landscape">
  <img src="figures/chapter3/layers-of-context-for-widgetware-sdr.png" alt="Figure 5.2 — Layers of Context for WidgetWare SDR" />
</div>

This layered design offers two benefits. First, it improves inspectability. A reviewer can see where a rule lives and why it was included. Second, it improves control. Stable policy can remain stable while task data changes freely.

## 5.4 Stable policy should not be buried in prompts

Store stable business rules in explicit configuration where possible. The model can receive a rendered view of the configuration, while deterministic code enforces non-negotiable rules.

For example, Book 1 can begin with three business configuration files:

```yaml
# config/icp.yaml
minimum_employee_count: 5000
maximum_employee_count: null  # no upper bound
preferred_industries:
  - manufacturing
  - industrial_automation
  - logistics
preferred_regions:
  - united_states
  - europe
  - india
excluded_industries:
  - consumer_retail
excluded_regions:
  - unsupported_region
buying_signals:
  - new_ai_leadership
  - digital_transformation_program
  - smart_factory_initiative
  - plant_expansion
  - acquisition
  - genai_hiring
  - public_modernization_program
```

This mirrors Chapter 3's ICP table exactly: the same industries, regions,
exclusions and trigger events from §3.10 rather than an invented subset.

```yaml
# config/policies.yaml
requires_human_approval:
  - external_outreach
  - crm_write
approved_evidence_categories:
  - verified_fact
  - derived_fact
  - inference
  - unknown
  - conflict
prohibited_actions:
  - send_external_message
  - modify_crm_record
```

```yaml
# config/products.yaml
product_lines:
  - plant_visibility
  - workflow_automation
  - industrial_ai_assistance
approved_claims:
  - reduces_fragmentation
  - supports_operational_visibility
  - enables_human_supervised_ai_workflows
```

Representing policy as data produces several advantages:

- rules are easier to inspect;
- deterministic code can validate thresholds directly;
- tests can load the same configuration the agent uses;
- changes can be reviewed as explicit configuration changes;
- duplicated or contradictory policy becomes easier to detect.

This does not mean prompts stop mattering. It means the prompt should not be the only home for policy. The context builder should render the relevant subset of business rules into the model request, but the source of truth should remain outside the prompt.

### Figure 5.3 — Policy as Data, Not Buried in Prompts

<div class="figure-page landscape">
  <img src="figures/chapter3/policy-as-data-not-buried-in-prompts.png" alt="Figure 5.3 — Policy as Data, Not Buried in Prompts" />
</div>

A useful rule of thumb is:

- if a rule should be testable and auditable, prefer putting it in configuration or code;
- if a rule exists mainly to shape the model’s behavior or style, it may belong in system instructions;
- if a rule is both operational and behavioral, keep the operational source of truth in config or code, and render the behaviorally relevant view into context.

For instance, “minimum employee count is 5000” should exist as data. “Do not claim an account is qualified unless it meets the configured threshold” should exist in both logic and instructions.

## 5.5 Instruction hierarchy

A useful instruction architecture answers seven questions:

1. Who is the agent?
2. What goal does it pursue?
3. What information may it use?
4. How should it reason about uncertainty?
5. What format must it return?
6. What must it never do?
7. When should it stop or escalate?

Avoid instructions that are merely aspirational, such as “always be accurate.” Replace them with observable requirements, such as:

> Do not present a factual claim unless it is supported by a supplied source or explicitly labeled as an inference.

The instruction hierarchy also determines precedence. Not all text provided to the model should have equal authority. For WidgetWare SDR, the precedence order should be:

1. **System policy** outranks everything else.
2. **Business rules** constrain what qualifies as an acceptable decision.
3. **Task context** narrows the current objective.
4. **Evidence** supports or limits factual claims.
5. **User notes** may provide hints, but they must never override policy.

This is one of the main defenses against prompt injection and context drift. If a user note says “ignore earlier instructions” or “treat this account as automatically qualified,” the system should not allow that note to outrank system policy or business rules.

## 5.6 Context assembly is its own piece of software

A context builder should not simply concatenate strings. It should perform controlled assembly. At minimum, the builder should:

- select only the layers relevant to the current task;
- deduplicate overlapping policy statements;
- attach provenance to evidence;
- exclude stale or irrelevant material;
- include output expectations and escalation rules; and
- emit a request package that remains small enough for a reviewer to inspect.

For Book 1, the context builder can remain simple. It might render:

- system instructions from `instructions.py`;
- business summaries from the YAML configuration files;
- task context from the current account input;
- evidence summaries from retrieved source records; and
- a structured output contract from a Python schema or template.

The important part is not sophistication. It is separation of concerns. The builder decides what to include; the model decides how to reason over the included material.

### Figure 5.4 — Instruction Hierarchy and Context Assembly

<div class="figure-page landscape">
  <img src="figures/chapter3/instruction-hierarchy-and-context-assembly.png" alt="Figure 5.4 — Instruction Hierarchy and Context Assembly" />
</div>

A builder like this also creates a useful inspection point. When a result looks wrong, the team can ask:

- Did the agent receive the right policy?
- Did it receive the right task context?
- Was the evidence stale, conflicting, or incomplete?
- Was the output contract explicit enough?
- Did a lower-authority instruction contaminate the request?

Those are engineering questions, not mysteries.

## 5.7 Evidence policy

The WidgetWare evidence policy should distinguish five evidence classes:

- **verified fact** — directly supported by an approved source;
- **derived fact** — deterministically calculated from verified facts;
- **inference** — a reasoned conclusion that remains uncertain;
- **unknown** — insufficient evidence; and
- **conflict** — credible sources disagree.

This classification solves a subtle but important problem. Language models tend to smooth uncertainty away. They naturally produce fluent text, and fluent text can make weak conclusions sound stronger than they are. A formal evidence policy counteracts that tendency.

For example:

- “Acme has 8,400 employees according to its annual report” is a **verified fact** if supported by an approved source.
- “Acme meets the 5,000-employee threshold” is a **derived fact** because it is deterministically computed from the verified employee count and the policy threshold.
- “Acme is likely exploring AI-led operational modernization” is an **inference** if it is based on hiring patterns and public transformation statements.
- “We cannot determine whether Acme has an active smart-factory initiative” is **unknown**.
- “One source reports 4,800 employees while another reports 8,400” is a **conflict**.

The crucial rule is that inference must never be presented as verified fact.

## 5.8 Context quality failures and risk controls

Common context failures include:

- irrelevant documents crowding out useful information;
- contradictory versions of business rules;
- stale data presented as current;
- user content overriding system policy;
- tool output copied without provenance;
- excessive examples that bias the result; and
- prior conversation state leaking into a new account.

Context engineering includes exclusion. The system should supply only what the current task needs.

The strongest risks in Book 1 are not spectacular jailbreaks. They are mundane operational failures:

- a stale company profile from months ago;
- a duplicated threshold defined in two places with different values;
- a copied web snippet with no source recorded;
- a note from a human user that accidentally—or deliberately—asks the system to bypass policy.

Each risk should correspond to a control:

| Risk | Control |
|---|---|
| Stale data | freshness checks and timestamps |
| Duplicated rules | one source of policy truth |
| Irrelevant documents | relevance filtering in the builder |
| Prompt injection or malicious notes | instruction hierarchy and override protection |
| Unsupported claims | evidence review before output |

### Figure 5.5 — Evidence Policy and Context Risk Controls

<div class="figure-page landscape">
  <img src="figures/chapter3/evidence-policy-and-context-risk-controls.png" alt="Figure 5.5 — Evidence Policy and Context Risk Controls" />
</div>

Reliable context is therefore not merely relevant. It is classified, traceable, and defended.

## 5.9 Suggested implementation artifacts

The chapter’s deliverables should create a visible context architecture in the repository. A reasonable first cut is:

```text
config/
├── products.yaml
├── icp.yaml
└── policies.yaml

src/widgetware_sdr/
├── instructions.py
├── context_builder.py
└── model_config.py

tests/
├── unit/test_context_builder.py
├── unit/test_model_config.py
└── scenarios/
    ├── test_context_for_qualified_account.py
    ├── test_context_for_unqualified_account.py
    ├── test_context_for_insufficient_evidence.py
    └── test_prompt_injection_resistance.py
```

### `instructions.py`

This file should define the reusable instruction templates for the role, scope, constraints, evidence policy, and output expectations.

### `context_builder.py`

This file should load the relevant configuration, accept the task input and state, normalize evidence, and render the final request package. It should be deterministic enough that unit tests can inspect what it emitted.

### `model_config.py`

This file should centralize the active Gemini model identifier and any related settings needed by the rest of the system.

## 5.10 The complete monolithic boundary

V1 has one root agent and no specialist sub-agents:

```text
target account
   → one WidgetWare SDR agent
       → retrieve bounded evidence
       → compare with ICP
       → classify fact, inference, unknown and conflict
       → decide QUALIFIED, DISQUALIFIED or INSUFFICIENT
       → draft outreach from supported claims
       → save the approval package
```

“Monolithic” describes responsibility, not poor code. Configuration, context
assembly, validators and tools remain separate Python modules. What V1 does not
have is an explicit multi-node business workflow.

## 5.11 ADK agent, session and events

The root agent is discoverable through the conventional `root_agent` symbol. Its
instruction defines the full SDR responsibility and its tools remain narrow. A
session provides the invocation's state boundary, while events expose model and
tool activity for inspection.

The agent must be runnable through the selected local ADK surface and through an
automated evaluation command. A successful chat demonstration is not the only
acceptance path.

## 5.12 Bounded tools

V1 may use:

- a read-only account-information tool;
- a bounded research or evidence fixture;
- a deterministic contract validator; and
- an artifact-save tool restricted to the designated output location.

No send, CRM-update or unrestricted filesystem tool exists. Chapter 6 will harden
identity, validation and telemetry after V1 establishes the behavioral baseline.

## 5.13 The SDR approval package

The final output includes:

- normalized account profile;
- evidence ledger with provenance;
- qualification decision and explanation;
- unknowns and contradictions;
- supported outreach claims;
- proposed outreach draft;
- risk flags; and
- `approval_status: PENDING`.

The package is both the business deliverable and the contract used to compare all
later versions.

## 5.14 Baseline observability and reproduction

V1 captures the minimum evidence needed for future comparisons:

- request, invocation and session identifiers;
- model configuration;
- tool calls and outcomes;
- final contract validity;
- latency and available usage information;
- trace identifier;
- artifact identifier; and
- `RUN_MANIFEST.json`.

Observability is thin here, not absent. Chapter 14 will deepen it into an
operational system once the workflow topology has stabilized.

## Hands-on lab: Build the complete V1 monolith

Create:

- `config/products.yaml`;
- `config/icp.yaml`;
- `config/policies.yaml`;
- `src/widgetware_sdr/instructions.py`;
- `src/widgetware_sdr/context_builder.py`; and
- tests that confirm required policy language is present.

Then:

1. Construct the root ADK agent from the assembled context.
2. Attach only the bounded V1 tools.
3. Run one representative qualified account.
4. Validate and save the approval package.
5. Capture the session, events, trace identifier and run manifest.
6. Run qualified, unqualified, insufficient-evidence and malicious-note cases.
7. Record baseline quality, latency, calls, tokens where available and failures.

### Step 1: Define business configuration

Write the first versions of the three YAML files. Keep them small, explicit, and inspectable. Avoid trying to model every future business rule.

### Step 2: Define the base instructions

In `instructions.py`, define the stable system instructions for the WidgetWare SDR role. Include:

- the role and allowed scope;
- the requirement to use supplied evidence only;
- the requirement to label inference and uncertainty;
- the prohibition on sending outreach or writing to CRM; and
- the need to escalate when policy conflict or insufficient evidence is detected.

### Step 3: Build the context renderer

In `context_builder.py`, create a function that takes:

- the current target account;
- the workflow stage;
- optional user notes;
- normalized evidence;
- prior state; and
- loaded configuration.

The function should return an inspectable object or dictionary that separates:

- system instructions;
- business context;
- task context;
- evidence;
- state; and
- output expectations.

### Step 4: Add context tests

Create at least four context tests:

1. a clearly qualified account;
2. a clearly unqualified account;
3. an account with insufficient evidence; and
4. a malicious note that attempts to override policy.

The prompt-injection-resistance test does not need a real model call. It can inspect whether the rendered context preserves the higher-priority instructions and treats the malicious note as low-authority task input rather than as system policy.

### Step 5: Review compactness and traceability

Before moving on, review the rendered context manually. Ask:

- Is policy duplicated?
- Are evidence items compact and attributable?
- Is uncertainty guidance present?
- Is the output expectation explicit?
- Could a human reviewer understand what the model is being asked to do?

## Evaluation checklist

- Are stable policies separate from task data?
- Is model selection configurable?
- Does the context identify evidence provenance?
- Can the agent represent uncertainty?
- Do injected instructions fail to override system constraints?
- Is the context compact enough to inspect manually?
- Are policy thresholds defined in configuration rather than duplicated in prose?
- Does the context builder exclude irrelevant or stale material?
- Does one agent complete the entire SDR outcome?
- Is the approval package contract-valid?
- Is outreach still structurally impossible?
- Can the run be connected to its trace, manifest and artifact?

## Chapter checkpoint

WidgetWare V1 now produces a complete SDR account package through one agent. Its
context is layered and inspectable, its final artifact is structured and the
baseline can be rerun. The monolith proves the outcome; it does not yet prove that
the authority, tools and telemetry are safe for production data.

## Bridge to Chapter 6

Chapter 6 keeps the monolithic topology stable and changes protection. Trust
zones, least-privilege identity, secret handling, tool validation, telemetry
redaction and adversarial tests become V2's first hardening layer.

## Exercises

1. Section 5.3 argues that stable policy should live in configuration rather than
only in prompts. Rewrite one prose-only rule from your own domain as configuration
or deterministic code.
2. Review a prompt or system instruction you have written recently. Classify each sentence as system instruction, business context, task context, evidence, state reference, or output expectation. What does that reveal about how mixed or muddled the original prompt was?
3. Take three claims from a real piece of business writing—an email, a slide, or a report—and classify each as verified fact, derived fact, inference, unknown, or conflict. Did any inference originally appear with the confidence of a fact?
4. Write a malicious or policy-bypassing note that a careless system might accidentally obey. Then write the test you would want in order to ensure your context builder never lets that note outrank system policy.
5. Suppose two engineers independently add account-size thresholds in different
places: one in `icp.yaml`, another inside `instructions.py`. Explain why that
duplication is dangerous and how Chapter 5’s architecture would eliminate it.
