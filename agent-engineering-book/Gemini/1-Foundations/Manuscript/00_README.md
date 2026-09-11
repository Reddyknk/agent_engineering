# Agent Engineering with Gemini, ADK & Antigravity

## Book 1: Foundations

### Evolve a Trustworthy SDR Agent on Google Cloud

This revised manuscript follows one evidence-driven product from a blank slate to
an observable, repeatable deployment. The reader does not begin with a finished
multi-agent diagram. WidgetWare SDR starts as one deliberately broad monolithic
agent. Each later version adds only the smallest change justified by evidence.

The governing cycle is:

> **Observe → Ask → Decide → Change → Prove**

## Reading order and product versions

| Chapter number | Name | Description of concept | Version number | Feature in the version | SDR improvement |
| ---: | --- | --- | :---: | --- | --- |
| 1 | Preface: Why Agent Engineering | Establishes the discipline, risk posture and case for progressive complexity. | — | Editorial and engineering principles. | Keeps business outcomes and human accountability ahead of novelty. |
| 2 | Introduction: Evolving an Agentic Product | Defines the Observe → Ask → Decide → Change → Prove method and the evidence contract. | V0 | Version ladder, acceptance gates and common comparison dataset. | Makes every SDR capability traceable to a measured need. |
| 3 | From Language Models to Agent Engineering | Frames the use case, autonomy boundary, SDR process, KPIs, SLOs and risks. | V0 | Scoped product contract and Google Cloud boundary. | Clarifies which accounts, artifacts and decisions the SDR workflow owns. |
| 4 | Building the Engineering Harness with Antigravity | Creates a reproducible environment for agent-assisted development. | V0 | Google Cloud project, governed repository, tests and manifests. | Reduces setup drift and makes SDR experiments comparable. |
| 5 | Building the Complete Monolithic SDR Agent | Starts with one broad agent so the team can observe real coupling before decomposing it. | V1 | One ADK agent completes research, qualification and draft generation. | Produces one reviewable account package end to end. |
| 6 | Securing the Agent and Its Tools | Moves controls outside prompt persuasion and constrains tool effects. | V2 | Trust boundaries, least privilege, policy enforcement and adversarial tests. | Protects customer data and prevents unauthorized outreach or CRM mutation. |
| 7 | Skills and Reusable Agent Capabilities | Turns the agent's repeatable judgment into an inspectable, versioned asset. | V3 | ICP Qualification and Evidence Classification Skills. | Applies the same qualification method to every account, and lets the method be reviewed and changed on its own. |
| 8 | Structured Outputs and Agent Contracts | Replaces prose answers with results another system can act on. | V4 | Validated `QualificationResult` schema, confidence and evidence references. | Makes a qualification decision routable, auditable and comparable across runs. |
| 9 | Evidence-Backed Research with MCP | Gives every claim a source that can be resolved and re-checked. | V5 | MCP research tools, evidence ledger, freshness and contradiction handling. | Produces account briefs a reviewer can trust without re-researching them. |
| 10 | Grounded Product Knowledge with RAG | Applies the evidence discipline to the company's own claims, not just the prospect's. | V6 | Governed corpus, chunking, retrieval, and product claims cited into the evidence ledger. | Stops outreach asserting capabilities and customer outcomes nothing can support. |
| 11 | Reliable Graph Workflows and Responsibility Boundaries | Replaces hidden prompt sequencing with explicit state and transitions. | V7 | ADK graph workflow, typed handoffs, routes and failure isolation. | Makes research, qualification, drafting and approval independently recoverable. |
| 12 | Evaluation and Quality Detection | Separates external product evaluation from runtime detection of weak work. | V8 | Golden datasets, rubric scoring and quality signals. | Detects unsupported claims, poor fit decisions and weak drafts before review. |
| 13 | Graph Loops and Controlled Refinement | Adds bounded correction only where evaluation shows it is worthwhile. | V9 | Generate–review–revise subgraph with exit and escalation conditions. | Improves low-quality drafts without silently retrying forever. |
| 14 | Observability and AgentOps | Makes each graph stage and business outcome explainable before anything is optimized. | V10 | Traces, logs, metrics, alerts and per-stage cost/latency attribution. | Shows where SDR packages fail, slow down or consume excess reviewer effort. |
| 15 | Cost and Latency Optimization | Spends the trace evidence twice: do less work, and wait less while doing it. | V11 | Model right-sizing, deterministic nodes, context budgets, parallel branches and join contracts. | Lowers cost and elapsed time while protecting evidence quality. |
| 16 | Dynamic Workflow and Loop Engineering | Adds a governed outer loop for repeated account processing. | V12 | ADK dynamic workflow with queue policy, checkpoint, resume and stop decisions. | Processes a campaign queue durably while preserving per-account approval. |
| 17 | Repeatable Deployment, Recording and Replay | Turns a working system into a controlled product release. | V13 | Release gates, Cloud Run deployment, lineage, replay and rollback. | Makes SDR outcomes reproducible, auditable and safely recoverable. |

The conclusion and Book 2 bridge follow Chapter 17.

## Measurement precedes optimization

Chapter 15 spends evidence twice: cost optimization needs per-node token and
latency attribution, and parallelization needs a critical path. Chapter 14 is where
that evidence is produced, which is why observability precedes optimization rather
than following it. No version in this book is optimized on intuition.

## Two rails run through every version

### Evidence rail

Every version uses the same representative accounts, output contract, evaluation
dimensions, adversarial case, SLO vocabulary and comparison report. A new
architecture is accepted only when the repeated evidence improves without an
unacceptable regression.

### Reproduction rail

Every run records the application version, prompt and policy versions, model
configuration, dataset version, Google Cloud project and region, session and trace
identifiers, tool versions, artifacts and evaluation result. Chapter 17 extends
this foundation into release manifests, recording, replay and rollback.

## Continuous lab

WidgetWare is a fictional software company. Its SDR system researches accounts,
tests fit against an Ideal Customer Profile, preserves evidence, drafts outreach
and requests human approval. It never sends an external message autonomously.

The lab evolves one product rather than presenting disconnected demos:

```text
V0 scope and harness
  → V1 complete monolith
  → V2 secured monolith
  → V3 reusable Skills
  → V4 typed contracts
  → V5 sourced evidence
  → V6 grounded product knowledge
  → V7 reliable graph
  → V8 quality detection
  → V9 controlled correction
  → V10 operational observability
  → V11 cost and latency optimization
  → V12 durable operational loop
  → V13 repeatable deployment and replay
```

## Appendices

1. `Appendix_01_Antigravity_Ecosystem.md`
2. `Appendix_02_Observing_a_Multi_Agent_System.md`
3. `Appendix_03_Google_Cloud_Project_Setup.md`
4. `Appendix_04_ADK_Workflow_Selection_Guide.md`

These are reference material, consulted rather than worked through. Skills,
contracts and evidence-backed research were appendices in an earlier draft; they
are Chapters 7, 8 and 9 now, because Chapter 11 cannot be built without them.

## Editorial standard

Every chapter identifies the current version, the evidence that creates the need
for change, the engineering question, the smallest justified modification, the
SDR improvement, the Google Cloud and ADK mechanisms, the proof required to
accept the version, a hands-on lab and a bridge to the next unanswered question.
