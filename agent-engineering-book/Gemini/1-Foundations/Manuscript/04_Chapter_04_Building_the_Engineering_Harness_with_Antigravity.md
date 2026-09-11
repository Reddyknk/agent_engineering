# Chapter 4: Building the Engineering Harness with Google Antigravity

*Creating the Engineering Harness for WidgetWare SDR*

## Product version

**V0 — reproducible engineering harness**

The product is still pre-production, but the work now becomes repeatable: a governed repository, explicit configuration, testable interfaces and a deployment path into the Google Cloud project.

## Engineering question

**How do we make every later change inspectable, testable and reproducible before the agent grows more capable?**

## Chapter purpose

Chapter 3 defined what WidgetWare SDR is allowed to do, where it fits in the
sales process and which decisions belong to models, software and people. It
deliberately left the final architecture unknown. This chapter turns the V0
contract into an inspectable development workspace capable of comparing every
later version.

Google Antigravity is treated here not as a magic code generator, but as an agent-assisted engineering environment. Its agent can inspect files, propose plans, edit code, run commands, use a browser, and produce reviewable artifacts. Those capabilities are valuable only when they operate inside repository rules, explicit specifications, bounded tasks, permissions, tests, version control, and human review.

The central idea is simple:

> **A coding agent becomes an engineering partner only when the environment around it makes work inspectable, controllable, reproducible, and recoverable.**

Chapter 4 does not build the WidgetWare business agent. It builds the harness in
which the V1 monolith and every later increment will be created safely.

## Learning objectives

By the end of this chapter, the reader should be able to:

- explain the role of an agent-assisted development harness;
- distinguish the coding agent from the controls surrounding it;
- create and inspect an Antigravity Project for the WidgetWare repository;
- use specification-driven planning and review artifacts;
- organize documentation, source code, configuration, tests, scripts, and generated evidence;
- distinguish `README.md`, `SPEC.md`, architecture decisions, rules, and workflows;
- write bounded engineering tasks with explicit completion contracts;
- apply least privilege to files, commands, browser access, dependencies, and secrets;
- review plans, diffs, command output, and test evidence before accepting changes;
- establish deterministic baseline quality gates; and
- use Git checkpoints and isolated experiments to make agent-assisted change recoverable.

## Seven-Step mapping

**Primary:** Build the Harness  
**Supporting:** Frame the Use Case; Design Agent Capabilities; Evaluate & Govern

## The WidgetWare increment

Create a reproducible Google Antigravity workspace containing:

- the Book 1 business and system specification;
- repository and documentation conventions;
- project-level rules and security boundaries;
- a minimal Python package;
- environment and dependency configuration;
- baseline formatting, linting, type-checking, and test commands;
- a deterministic health check;
- an initial Git checkpoint; and
- a versioned product-evolution structure;
- a shared golden evaluation set;
- a `RUN_MANIFEST.json` contract; and
- a repeatable cycle for planning, implementing, reviewing, verifying, and accepting change.

No Gemini-powered WidgetWare agent is implemented yet.

---

## From a product contract to a working repository

Chapter 3 did not present the completed architecture. That is deliberate. A
common mistake is to ask a coding agent to generate the imagined final system at
once. It may respond with hundreds of files, several frameworks, inferred
requirements, placeholder security and a project that appears complete but is
difficult to verify.

WidgetWare begins differently. The first implementation increment contains almost no business intelligence. It creates a package that imports, a health check that returns a deterministic result, a test that proves the result, and documented commands that another learner can run.

That modest beginning establishes several important facts:

- the repository has a known structure;
- the Python environment can be recreated;
- source and tests are discoverable;
- quality commands work;
- secrets are not required for baseline verification;
- the agent can follow repository conventions; and
- every later change has a stable point of comparison.

The first objective is not to make WidgetWare smart. It is to make WidgetWare
buildable, comparable and reversible.

The repository establishes a stable evolution spine:

```text
versions/        runnable V0–V9 checkpoints or release references
evals/           shared cases, rubrics and comparison reports
manifests/       run and release lineage
tests/           unit, contract, scenario and safety checks
infra/           Google Cloud configuration and deployment definitions
observability/   trace, metric and dashboard configuration
artifacts/       generated evidence excluded or retained by policy
```

Each chapter changes one material concern and reruns the same evidence.

## 4.1 The harness is part of the system

A development harness is the collection of structures and controls that turns intent into repeatable engineering work. It includes more than the integrated development environment.

For WidgetWare, the harness includes:

- the business specification and system boundary;
- repository structure and naming conventions;
- contributor and coding instructions;
- the Antigravity Project and its settings;
- source, configuration, and dependency management;
- environment-variable and secret-handling rules;
- formatting, linting, type-checking, and tests;
- permissions for files, commands, browser access, and tools;
- planning and implementation artifacts;
- Git history, branches, worktrees, and rollback points; and
- human review practices.

The coding agent sits inside this environment. It does not define the environment by itself.

### Figure 4.1 — The Agent Engineering Harness

<div class="figure-page landscape">
  <img src="figures/chapter2/the-agent-engineering-harness.png" alt="Figure 4.1 — The Agent Engineering Harness" />
</div>

Each part of the harness prevents a different class of failure.

| Harness element | Failure it helps prevent |
|---|---|
| Business specification | Building the wrong capability correctly |
| Repository instructions | Inconsistent style and hidden assumptions |
| Bounded task definition | Scope drift and unrelated changes |
| Dependency policy | Unnecessary packages and supply-chain risk |
| Secret handling | Credentials entering source control or logs |
| Tests and quality gates | Plausible code that does not meet stable requirements |
| Permission controls | The agent acting outside the intended trust zone |
| Review artifacts | Accepting work without understanding the plan or evidence |
| Version control | Losing a known-good state or being unable to revert |

A weak harness forces every engineer and every coding agent to rediscover expectations. A strong harness makes expectations executable or at least inspectable.

This is why the harness belongs to the system design. The quality of an agent-assisted codebase depends partly on model capability, but also on what the environment makes easy, difficult, visible, and impossible.

## 4.2 Antigravity as an engineering partner

Google Antigravity provides an environment in which agents can work across the editor, terminal, and browser. A Project can associate one or more local folders or Git repositories and maintain project-specific settings and security policies. The environment also produces artifacts such as task lists and implementation plans that can be reviewed before or during implementation.[^antigravity-overview]

These capabilities change the interaction model. A traditional code assistant primarily completes text near the cursor. An agentic development environment can inspect multiple files, trace dependencies, create a plan, edit several modules, run commands, observe failures, and propose follow-up changes.

That broader reach is useful, but it also increases the cost of vague instructions.

Consider two requests:

> Build the WidgetWare SDR application.

and:

> Create the initial Python package and a deterministic health-check function. Work only in `src/widgetware_sdr/health.py`, `tests/unit/test_health.py`, and the setup instructions in `README.md`. Do not add ADK, Gemini, Cloud Run, external integrations, or new runtime dependencies. The task is complete when the package imports and the documented test command passes.

The first request requires the agent to invent architecture, scope, sequencing, and completion criteria. The second provides a bounded engineering decision.

Antigravity should be used as a partner that can reason about implementation, not as the authority that defines the product.

A useful division of responsibility is:

| Human responsibility | Antigravity contribution |
|---|---|
| Define business outcome and authority boundary | Interpret the relevant specification |
| Decide acceptable architecture and risk | Propose an implementation plan |
| Approve scope and consequential actions | Execute bounded edits and commands |
| Judge whether evidence is sufficient | Return artifacts, diffs, logs, and test results |
| Accept, revise, or reject the change | Respond to feedback and repair failures |

The agent can be proactive within the task. The human remains accountable for whether the task should exist and whether the resulting change is acceptable.

### Figure 4.2 — The Antigravity Engineering Cycle

<div class="figure-page landscape">
  <img src="figures/chapter2/the-antigravity-engineering-cycle.png" alt="Figure 4.2 — The Antigravity Engineering Cycle" />
</div>

## 4.3 The Antigravity engineering cycle

Agent-assisted development should follow a repeatable cycle rather than an open-ended conversation.

### 1. Define the objective

State one outcome that matters. The objective should describe a change in the repository, not a vague aspiration.

Weak objective:

> Improve the project.

Stronger objective:

> Establish a minimal importable package and health check so later chapters have a reproducible baseline.

### 2. Load the relevant specification

Point the agent to the documents and files that govern the task. More context is not always better. The agent needs the authoritative context for this change, not the entire future architecture on every invocation.

For the health-check task, relevant context includes:

- `SPEC.md`;
- repository development instructions;
- `pyproject.toml`;
- the package directory; and
- baseline acceptance criteria.

It does not need Chapter 9's full MCP research contract.

### 3. Create a plan

Ask Antigravity to state:

- files to create or modify;
- behavior to implement;
- tests to add;
- commands to run;
- dependencies, if any;
- assumptions; and
- risks or open questions.

The plan is the first inspectable prediction of what the agent intends to do.

### 4. Review artifacts

Antigravity artifacts are not decoration. They externalize reasoning into reviewable objects. An implementation plan can reveal that the agent intends to add an unnecessary framework, modify a file outside scope, or interpret an ambiguous requirement incorrectly before those decisions become code.[^antigravity-artifacts]

Reviewing a plan is cheaper than reviewing a large incorrect diff.

### 5. Authorize bounded work

Approval should apply to the stated task, not to unlimited future action. If the plan broadens scope, revise it before execution.

### 6. Inspect changes

Read the diff. Do not treat successful generation as proof of correctness. Look for:

- unrelated refactoring;
- hidden behavior changes;
- duplicated logic;
- disabled tests;
- hard-coded values;
- secret exposure;
- new dependencies;
- vague error handling; and
- comments or documentation that claim more than the code provides.

### 7. Run quality gates

Execute the documented commands in a clean or known environment. A passing test suite is necessary evidence, not complete evidence. Verify that the right tests exist and that the agent did not weaken them to obtain a pass.

### 8. Accept, revise, or revert

There are three legitimate outcomes:

- **Accept** when the change meets the task contract.
- **Revise** when the approach is sound but evidence or implementation is incomplete.
- **Revert** when the change violates the boundary, introduces unjustified complexity, or is harder to repair than to replace.

Reversion is not failure. It is part of controlled experimentation.

## 4.4 Projects, workspaces, and isolated experiments

In Antigravity, a Project groups the folders or repositories an agent may work with and allows project-level settings and permissions. This creates a useful boundary: WidgetWare’s agent context should be tied to the WidgetWare repository, not to every directory on the workstation.[^antigravity-projects]

For routine changes, the Project may point to the normal local checkout. For risky or exploratory tasks, use isolation:

- create a throwaway branch;
- use a separate Git worktree;
- copy a small reproduction into an experiment directory; or
- restrict the task to a minimal test fixture.

Isolation reduces the consequences of a mistaken command or broad edit. It also improves review because the resulting diff contains only the experiment.

The repository remains the durable source of truth. Antigravity conversations and generated artifacts support the work, but important decisions must be reflected in versioned documents, code, configuration, tests, or architecture decision records.

A useful rule is:

> **If a future contributor must know it, it cannot exist only in a conversation.**

## 4.5 Repository architecture

Repository structure is an architectural control. It tells humans and agents where a type of truth belongs.

### Figure 4.3 — WidgetWare Repository Architecture

<div class="figure-page landscape">
  <img src="figures/chapter2/widgetware-repository-architecture.png" alt="Figure 4.3 — WidgetWare Repository Architecture" />
</div>

The initial WidgetWare repository should resemble:

```text
widgetware-sdr/
├── README.md
├── SPEC.md
├── CONTRIBUTING.md
├── SECURITY.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── .agents/
│   ├── rules/
│   └── workflows/
│
├── docs/
│   ├── widgetware-business-brief.md
│   ├── architecture.md
│   ├── acceptance-criteria.md
│   └── architecture-decisions/
│
├── config/
│   └── README.md
│
├── src/
│   └── widgetware_sdr/
│       ├── __init__.py
│       └── health.py
│
├── tests/
│   ├── unit/
│   │   └── test_health.py
│   ├── contracts/
│   └── scenarios/
│
├── scripts/
│   ├── check.sh
│   └── verify_environment.py
│
└── artifacts/
    └── .gitkeep
```

### Core documentation

- `README.md` helps a reader understand and run the project.
- `SPEC.md` defines required and prohibited system behavior.
- `CONTRIBUTING.md` defines how changes are proposed and verified.
- `SECURITY.md` states how secrets, permissions, vulnerabilities, and sensitive failures are handled.

### Business and architecture documents

The `docs/` directory preserves domain intent separately from code. Later code can load selected business configuration, but the business explanation should remain understandable to a person.

Architecture decision records capture consequential choices such as:

- why Book 1 stops at autonomy Level 4;
- why external sending is absent;
- why Cloud Run is the initial runtime target; and
- why persistent state is externalized.

### Configuration

The `config/` directory will hold product, ICP and policy files beginning in
Chapter 5. In Chapter 4, a `README.md` can define what belongs there and prohibit
credentials.

### Source

The package begins with only a deterministic health check. Future agents, tools, contracts, workflows, and loop components will appear under `src/widgetware_sdr/` in later chapters.

### Tests and evaluation

Different tests answer different questions:

- unit tests verify deterministic functions;
- contract tests verify typed interfaces and invariants;
- scenario tests verify end-to-end business behavior;
- later evaluation datasets judge semantic quality.

Separating them prevents an LLM-backed scenario from being mistaken for a unit test.

### Scripts and artifacts

Scripts provide one-command verification and repeatable utilities. The `artifacts/` directory can hold generated reports during development, but teams must decide which artifacts belong in Git and which should be ignored because they are large, transient, sensitive, or reproducible.

### Secrets excluded

Real credentials, tokens, private keys, and production configuration never belong in the repository. `.env.example` documents required variable names using safe placeholders. `.gitignore` excludes local secret files.

The structure is intentionally more explicit than a tiny demonstration requires. It teaches the repository how to grow without collapsing business policy, prompts, code, tests, and generated output into one directory.

## 4.6 README, SPEC, and architecture decisions

These documents solve different problems.

### `README.md`: how to enter the project

The README should answer:

- What is WidgetWare SDR?
- What can the current checkpoint do?
- What prerequisites are required?
- How is the environment created?
- Which commands run formatting, linting, typing, and tests?
- Where are the business brief and specification?
- What limitations apply at this stage?

The README describes the current usable state. It should not promise future capabilities as if they already exist.

### `SPEC.md`: what the system must mean

The specification should define:

- required behavior;
- prohibited behavior;
- inputs and outputs;
- authority and approval rules;
- state vocabulary;
- failure behavior;
- evidence requirements;
- completion criteria; and
- non-negotiable invariants.

The specification should be technology-aware without encoding incidental implementation detail.

Prefer:

> Qualification output must validate against a typed contract and fail safely when required fields are missing.

over:

> Qualification must use a specific Python class named `QualificationResultV1`.

The first preserves the architectural requirement. The second may become obsolete during a harmless refactor.

### Architecture decision records: why a consequential choice was made

A specification says what must be true. An ADR records why the team selected one durable approach over alternatives.

A concise ADR includes:

- context;
- decision;
- alternatives considered;
- consequences;
- status; and
- date or version.

This is especially valuable for coding agents. Without the decision history, an agent may repeatedly “improve” the project by reintroducing an alternative the team already rejected.

## 4.7 Repository instructions, rules, and workflows

The project should contain concise instructions for both human contributors and coding agents.

Recommended standing rules include:

- use clear, conventional Python;
- prefer explicit types and small functions;
- avoid unnecessary asynchronous code, decorators, or metaprogramming;
- write or update tests with every behavior change;
- preserve evidence identifiers across transformations;
- do not broaden tool or network permissions without review;
- never place credentials in source, prompts, fixtures, logs, or committed artifacts;
- do not implement external message sending in Book 1;
- keep business policy out of arbitrary source-code constants when configuration is appropriate;
- update documentation when behavior or commands change; and
- do not claim completion without returning verification evidence.

Antigravity workspace rules can be stored under `.agents/rules/`, with activation scoped to the relevant workspace and task. Reusable workflows can capture repeatable procedures such as reviewing a task, running baseline checks, or producing a gap report.[^antigravity-rules]

Rules should be short enough to follow. A giant instruction file becomes context noise and hides priorities. Separate:

- always-on non-negotiable rules;
- language or directory-specific conventions;
- task-specific requirements; and
- optional procedures invoked only when needed.

A strong rule is observable:

> Run `scripts/check.sh` and report each command’s result before declaring the task complete.

A weak rule is aspirational:

> Produce high-quality code.

## 4.8 Anatomy of a specification-driven task

A specification-driven task converts one approved objective into a bounded unit of work.

### Figure 4.4 — Anatomy of a Specification-Driven Task

<div class="figure-page landscape">
  <img src="figures/chapter2/anatomy-of-a-specification-driven-task.png" alt="Figure 4.4 — Anatomy of a Specification-Driven Task" />
</div>

A useful task contains nine elements.

### 1. Objective

One concrete repository outcome.

### 2. Business reason

Why the change exists and what later work depends on it.

### 3. In-scope files or modules

The area the agent may modify. The list can allow reasonable implementation files without authorizing repository-wide cleanup.

### 4. Required behavior

What the system must do after the change.

### 5. Explicit exclusions

What must not be added or changed. Exclusions prevent enthusiastic overreach.

### 6. Acceptance criteria

Stable properties that can be verified.

### 7. Commands to run

The exact checks expected before completion.

### 8. Evidence to return

A plan summary, changed-file list, diff summary, command output, test results, and open questions.

### 9. Completion condition

A task is not complete when code exists. It is complete when its acceptance criteria are met and the reviewer can verify the evidence.

The Chapter 4 health-check task can be written as follows:

> **Objective:** Create the initial importable Python package and deterministic health check.  
> **Business reason:** Establish a reproducible baseline before adding ADK, Gemini, tools, or deployment.  
> **In scope:** `pyproject.toml`, `src/widgetware_sdr/__init__.py`, `src/widgetware_sdr/health.py`, `tests/unit/test_health.py`, and setup commands in `README.md`.  
> **Required behavior:** Calling the health-check function returns a stable structure containing an `ok` status and package version.  
> **Exclusions:** Do not add ADK, model calls, Cloud Run files, network access, environment secrets, or external dependencies that are not required for testing.  
> **Acceptance criteria:** The package imports in a clean environment; the health test passes; the result is deterministic; documented commands are accurate.  
> **Commands:** Run the documented baseline quality command.  
> **Evidence:** Return the implementation plan, changed-file list, command results, and any assumptions.  
> **Completion:** Stop after the criteria pass. Do not begin Chapter 5 work.

This task gives the agent meaningful freedom over implementation details while preserving the limits of authority.

## 4.9 Task sizing and change budgets

Even a well-written task can be too large.

A task is probably oversized when it:

- spans several architectural layers;
- requires many unrelated dependencies;
- changes business rules and infrastructure together;
- cannot be reviewed in one coherent diff;
- has multiple independent definitions of done;
- would be difficult to revert without losing useful work; or
- asks the agent to continue until the entire product “works.”

Split work at stable interfaces. For example:

1. Create the package and health check.
2. Add configuration loading.
3. Add context assembly.
4. Add the complete V1 ADK agent.
5. Add a typed output contract.

Each step should leave the repository usable.

A change budget makes scope visible. A task may state:

- maximum number of modules expected to change;
- no dependency additions;
- no public-interface changes;
- no modification outside a named directory; or
- stop and ask before changing the specification.

The budget is not a rigid line-count target. It is a signal that the agent should pause when the implementation requires a qualitatively broader decision than the one authorized.

## 4.10 Trust, permissions, and change-acceptance gates

A development agent can read files, modify code, run commands, access browser-based information, and sometimes connect to additional tools. These actions do not have equal risk.

### Figure 4.5 — Trust, Permissions, and Change-Acceptance Gates

<div class="figure-page landscape">
  <img src="figures/chapter2/trust-permissions-and-change-acceptance-gates.png" alt="Figure 4.5 — Trust, Permissions, and Change-Acceptance Gates" />
</div>

Antigravity supports project-scoped permissions, and its settings allow permission decisions to be accumulated and managed at the project level. The CLI also exposes fine-grained permission controls. These mechanisms should reflect the actual needs of the task rather than granting broad access for convenience.[^antigravity-permissions]

A practical policy for Chapter 4 is:

| Action | Default treatment | Reason |
|---|---|---|
| Read files inside the WidgetWare workspace | Allowed | Required for repository understanding |
| Modify explicitly in-scope files | Allowed with diff review | Core task capability |
| Modify unrelated workspace files | Stop or request approval | Possible scope drift |
| Run known formatting and test commands | Allowed or reviewed once | Repeatable and low impact |
| Run a novel shell command | Review required | Command may alter environment or data |
| Add a new dependency | Elevated review | Security, maintenance, and reproducibility impact |
| Access the browser or external developer tool | Review and allowlist | Crosses the local workspace trust boundary |
| Read credentials or local secret files | Restricted | Not required for Chapter 4 |
| Commit, push, deploy, publish, or release | Human-controlled | Consequential external action |

Least privilege should be applied to the development environment just as it will later be applied to WidgetWare’s runtime tools.

### Separate trust zones

Treat these as different zones:

- versioned workspace files;
- generated local artifacts;
- terminal commands;
- browser and external URLs;
- package registries;
- credentials and secret stores;
- remote Git repositories; and
- cloud deployment environments.

Permission in one zone should not imply permission in all others.

### Browser access

External content can be useful for documentation and diagnosis, but it is untrusted input. Antigravity supports URL access controls, including allowlist and denylist mechanisms. Restrict browser access to necessary, approved documentation and services.[^antigravity-browser]

### Dependencies

A dependency addition deserves explicit review because it changes:

- the software supply chain;
- installation and build behavior;
- security exposure;
- licensing obligations;
- runtime size; and
- long-term maintenance.

The agent should explain why the standard library or existing dependencies are insufficient.

### Secrets

Chapter 4 requires no production secrets. If a tool asks for one, treat that as a
design warning. Use placeholders in `.env.example`, local ignored files for later
development credentials, and managed secret storage in deployed environments.

Permission is not merely a convenience setting. It is part of the engineering control system.

## 4.11 Reviewing changes and evidence

Review is not one action. It occurs at several levels.

### Review the plan

Ask whether the proposed implementation matches the task. Look for missing tests, scope expansion, and unjustified dependencies.

### Review the diff

Read both additions and deletions. Pay special attention to:

- changes to tests;
- changes to security or configuration;
- exception handling that suppresses failures;
- broad formatting changes that hide behavior edits;
- comments claiming guarantees not enforced by code; and
- generated files that should not be committed.

### Review command evidence

A statement such as “tests pass” is weaker than captured command output. The agent should report:

- command executed;
- environment assumptions;
- exit status;
- number of tests collected and passed;
- warnings; and
- checks that were not run.

### Review behavior directly

Run the health check yourself. Inspect the returned structure. Confirm that repeated calls are identical. Remove a required file or introduce a deliberate failure and verify that the quality command detects it.

### Review the absence of prohibited change

Some acceptance criteria are negative:

- no ADK dependency exists;
- no network call occurs;
- no secret file is committed;
- no send capability appears;
- no unrelated module changed.

Negative criteria require explicit inspection. A passing unit test may not prove them.

## 4.12 Environment, dependency, and secret management

A reproducible environment should make the project’s assumptions visible.

`pyproject.toml` should define:

- package name and version;
- supported Python range;
- build system;
- runtime dependencies;
- development dependencies or optional groups;
- formatter and linter configuration where appropriate;
- type-checker settings; and
- test configuration.

Avoid scattering tool configuration across many files unless a tool requires it. Central configuration makes it easier for both people and agents to inspect the development contract.

`verify_environment.py` can check stable prerequisites, such as:

- supported Python version;
- package import;
- expected directory presence; and
- absence of required runtime secrets for the baseline test.

`.env.example` documents names, not values. For example:

```text
# Added in later chapters; never place real values in this file.
GOOGLE_CLOUD_PROJECT=
GOOGLE_CLOUD_LOCATION=
WIDGETWARE_MODEL=
```

At the end of Chapter 4, these variables may remain unused. Documenting them early
is acceptable if the README distinguishes future setup from current requirements.

## 4.13 Baseline quality gates

A learner should be able to verify the repository with one documented command.

For example:

```bash
./scripts/check.sh
```

The script may run:

1. environment verification;
2. formatting check;
3. linting;
4. static type checking; and
5. tests.

The exact tools may change, but the contract should remain stable: one command provides a clear baseline signal.

A quality gate should:

- stop on failure;
- return a nonzero exit code;
- print which stage failed;
- avoid modifying source during a check-only run;
- work from a clean checkout; and
- be suitable for later CI execution.

Do not confuse more tools with more quality. Every tool should protect a meaningful property. A formatter protects consistency. A linter catches selected defects. A type checker verifies declared interfaces. Tests verify behavior. None replaces architectural review.

The health-check test should be deterministic and fast. It proves the harness, not the intelligence of the future agent.

## 4.14 Version control, checkpoints, and rollback

Git provides the recovery layer for agent-assisted development.

Before authorizing a meaningful task:

- begin from a clean working tree;
- record or commit the known-good state;
- create a task-specific branch or worktree when appropriate; and
- confirm that generated or secret files are ignored.

After the task:

- inspect `git status`;
- review the complete diff;
- run the quality gates;
- commit only accepted files; and
- write a commit message that states the behavior established.

A useful Chapter 4 checkpoint might be:

> `chapter-02: establish reproducible workspace and health-check baseline`

The checkpoint gives every later chapter a known starting point. A learner who
joins at Chapter 5 should be able to reproduce the same verification result.

Rollback should be practiced before it is needed. On a throwaway branch, ask Antigravity to make a harmless experimental change, inspect it, and then revert it. Recovery confidence is part of the harness.

---

## Hands-on lab: Build and verify the workspace

### Part 1: Create the Antigravity Project

1. Create a new Antigravity Project.
2. Associate only the WidgetWare repository or workspace folder.
3. Review the Project’s permissions and security settings.
4. Keep non-workspace access disabled unless a task explicitly requires it.
5. Configure artifact review so plans remain visible for review.

### Part 2: Create the repository structure

Create the directories and baseline files shown in Section 4.5. Copy the Chapter 3
business brief, authority boundary and acceptance criteria into `docs/`.

### Part 3: Add repository instructions

Create:

- contributor instructions;
- security and secret-handling rules;
- coding conventions;
- a rule prohibiting external message delivery; and
- a workflow for running and reporting baseline checks.

### Part 4: Create the minimal package

Add:

- `pyproject.toml`;
- `src/widgetware_sdr/__init__.py`;
- `src/widgetware_sdr/health.py`; and
- `tests/unit/test_health.py`.

The health check should return a deterministic result such as:

```python
{
    "status": "ok",
    "service": "widgetware-sdr",
    "version": "0.1.0",
}
```

No model call, network access, asynchronous runtime, or environment secret is required.

### Part 5: Add reproducible quality commands

Create `scripts/check.sh` and `scripts/verify_environment.py`. Document the exact setup and verification commands in the README.

### Part 6: Give Antigravity a bounded task

Use the task contract from Section 4.8. Ask for a plan before implementation.
Review the plan and remove unjustified dependencies or out-of-scope changes.

### Part 7: Review the implementation

Inspect:

- the plan artifact;
- changed files;
- dependency changes;
- diff;
- command output;
- test result; and
- open assumptions.

### Part 8: Produce a gap report

Ask Antigravity to compare the repository against `SPEC.md` and the Chapter 4
acceptance criteria. The report must distinguish:

- requirements satisfied now;
- capabilities intentionally deferred;
- gaps that block Chapter 5; and
- observations that are merely optional improvements.

Do not allow the agent to implement the deferred capabilities during the gap analysis.

### Part 9: Create the checkpoint

Run the baseline command from a clean state. Commit the accepted Chapter 4 files
and record the checkpoint identifier.

## Evaluation checklist

### Workspace and documentation

- Can another learner clone and understand the repository?
- Is the current checkpoint accurately described?
- Are business rules and architecture intent separated from implementation?
- Are `README.md`, `SPEC.md`, and ADR responsibilities distinct?
- Are standing agent rules concise and observable?

### Task control

- Does every agent task have one bounded objective?
- Are in-scope files and explicit exclusions stated?
- Are completion criteria verifiable?
- Does the agent stop when the task is complete?
- Are plans reviewed before broad implementation?

### Security and permissions

- Is the Antigravity Project limited to the required workspace?
- Are browser and non-workspace permissions restricted?
- Are novel commands and dependencies reviewed?
- Are real secrets excluded from source, fixtures, logs, and artifacts?
- Are push, deployment, and publication human-controlled?

### Quality and recovery

- Can all baseline checks run with one documented command?
- Does the check command fail clearly when a test fails?
- Is the health check deterministic?
- Does the repository contain a clean rollback point?
- Can an experimental change be reverted without damaging accepted work?

## Chapter checkpoint

The WidgetWare project now has an inspectable engineering harness.

The repository contains:

- a clear specification and architecture record;
- an Antigravity Project with bounded access;
- repository-level rules and review practices;
- an importable Python package;
- a deterministic health check;
- baseline tests and quality gates;
- documented environment and secret handling;
- an accepted Chapter 4 Git checkpoint; and
- a repeatable engineering cycle for future agent-assisted changes.

No sales qualification intelligence has been added yet. That is intentional. The project is now ready to receive business context without losing control over where that context belongs or how changes are verified.

## Bridge to Chapter 5

Chapter 5 defines how Gemini receives instructions and WidgetWare business
knowledge, then uses that context to build the complete V1 monolith.

The Chapter 4 harness makes that work possible. The repository now has a place
for configuration, a specification that defines evidence and authority, tests
that protect required behavior and a reviewable development cycle.

## Exercises

1. **Compare unrestricted and bounded work.** On a throwaway branch, give
Antigravity the instruction “build the entire application.” Do not accept the
changes. Record the plan, files touched, assumptions and review effort. Then use
the bounded health-check task from Section 4.8 and compare inspectability.

2. **Audit project truth.** Choose a project you maintain. Identify one important requirement that exists only in your memory, a chat, or a code comment. Decide whether it belongs in the README, specification, standing rules, or an ADR, and write the missing entry.

3. **Design a change budget.** Write a task that allows useful implementation freedom but requires the agent to stop before adding a dependency, changing a public interface, or editing outside a named directory.

4. **Review a deceptive pass.** Modify a test so it passes without checking meaningful behavior. Ask Antigravity to review the diff. What evidence would distinguish “the tests pass” from “the right behavior is tested”?

5. **Map trust zones.** List the files, terminal, browser, package registry, credentials, Git remote, and cloud account used by one of your projects. For each, state whether an agent may access it automatically, after review, or not at all.

6. **Practice rollback.** Make a harmless experimental change, run the checks,
inspect the diff and revert to the Chapter 4 checkpoint. Record the evidence.

7. **Predict repository growth.** Using the repository architecture in Section
4.5, predict where Chapters 5 through 8 will place business configuration,
context assembly, agent definitions, Skills, contracts and tests.

## References

[^antigravity-overview]: Google Antigravity, [“Antigravity IDE”](https://antigravity.google/product/antigravity-ide), and Google Developers, [“Getting Started with Google Antigravity”](https://codelabs.developers.google.com/getting-started-google-antigravity), describing agent operation across the editor, terminal, and browser and reviewable planning artifacts.

[^antigravity-artifacts]: Google Antigravity Documentation, [“Artifacts”](https://antigravity.google/docs/artifacts), describing task lists, implementation plans, walkthroughs, and other artifacts generated during agent work.

[^antigravity-projects]: Google Antigravity Documentation, [“Workspace vs. Projects”](https://antigravity.google/docs/projects), describing Projects, associated folders or repositories, inherited permissions, and project-level settings.

[^antigravity-rules]: Google Antigravity Documentation, [“Rules and Workflows”](https://antigravity.google/docs/rules-workflows), documenting workspace rules under `.agents/rules` and reusable workflows.

[^antigravity-permissions]: Google Antigravity Documentation, [“Antigravity 2.0 Settings”](https://antigravity.google/docs/settings), [“Antigravity 2.0 Features”](https://antigravity.google/docs/features), and [“CLI Permissions”](https://antigravity.google/docs/cli-permissions), describing project-scoped and fine-grained permissions.

[^antigravity-browser]: Google Antigravity Documentation, [“Allowlist and Denylist”](https://www.antigravity.google/docs/allowlist-denylist), describing URL access controls for browser activity.
