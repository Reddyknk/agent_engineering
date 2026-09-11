# Book 1 Conclusion: An Agent Is a System

The WidgetWare SDR application began with a deliberately modest question: can an agent help research and qualify a prospective customer while remaining inspectable and under human control?

The answer is yes—but not because the model was given one extraordinary prompt.

The system became useful through layers:

- Gemini supplied interpretation, synthesis, and drafting.
- Context architecture supplied WidgetWare’s business knowledge and task-specific evidence.
- ADK supplied the agent application model, sessions, tools, workflows, and evaluation structure.
- Antigravity supplied the development harness for specification-driven, agent-assisted engineering.
- Skills captured reusable business procedures.
- Structured contracts converted probabilistic outputs into deterministic interfaces.
- Tools supplied controlled access to current data.
- MCP provided a standardized path to external capabilities.
- An ADK graph made routes, responsibilities, contracts and failure boundaries explicit.
- Generate-review-revise behavior detected and corrected bounded quality defects.
- Model right-sizing, deterministic nodes and context budgets reduced waste.
- Parallel graph routes reduced enrichment latency.
- Human approval retained control over external action.
- Evaluations supplied evidence that the system behaved as intended.
- Cloud Trace, Logging and Monitoring made behavior, latency, cost and failure inspectable.
- An ADK dynamic workflow turned one evaluated graph into a bounded process that works through many accounts, resumes from checkpoints and stops for a reason it can name.
- Release manifests, recordings and replay connected deployed behavior to its evidence.

This is the central lesson of Book 1:

> Agent Engineering is the discipline of placing model intelligence inside an engineered system of context, capabilities, structure, evidence, and boundaries.

## What the system can now do

The Book 1 system can:

1. Accept a target account.
2. Retrieve controlled internal information.
3. Research approved external evidence.
4. Preserve provenance.
5. Compare the account with WidgetWare’s ideal-customer profile.
6. Represent uncertainty and missing information.
7. Review the evidence supporting a recommendation.
8. Draft outreach from approved facts.
9. Stop for human approval.
10. Produce logs, tests, and evaluation results.
11. Work through a queue of accounts unattended, within stated budgets, and stop with a named reason.
12. Resume the queue without repeating completed nodes.
13. Reproduce the conditions and lineage of a released run.

## What the system still cannot do

It does not yet provide:

- durable memory across users and long time periods;
- enterprise-scale document ingestion and retrieval;
- multi-tenant platform services and operating model;
- adaptive planning over complex goals;
- loops that revise their own strategy, run across distributed workers, or recover from more than the failure modes this book anticipated;
- collaboration with independently deployed agents;
- centralized agent identity and registration;
- enterprise gateway enforcement;
- network-level containment;
- production-grade semantic safety controls;
- organization-wide model routing and chargeback; or
- continuous evaluation across many workflows and teams.

These are not omissions caused by an incomplete foundation. They are the next architectural layer.

## Five engineering habits to retain

### 1. Define the boundary before the behavior

A system should state what it may and may not do before implementation begins.

### 2. Prefer contracts over interpretation

Whenever software consumes an agent result, use typed structures and deterministic validation.

### 3. Preserve evidence

A conclusion is only as inspectable as the path from claim to source.

### 4. Use autonomy selectively

The ability to act does not justify permission to act. External actions require policy, identity, auditability, and often human approval.

### 5. Evaluate trajectories, not demonstrations

A polished result can conceal unsafe or inefficient behavior. Test the route the system took, not only the final words.

## The transition from application to platform

Book 1 proves that we can build the application. Book 2 develops the credibility
to advise an enterprise on platform strategy, operating model, knowledge,
identity, governance, economics and transformation. Each Book 2 chapter produces
both a technical implementation and a reusable consulting artifact.

Book 1 built one bounded application. Enterprise adoption raises broader questions:

- How do hundreds of users receive isolated memory?
- How is enterprise knowledge indexed and permissioned?
- How do agents plan and recover over long-running tasks?
- How can independently deployed agents discover and trust each other?
- Which identity does an agent use when accessing data?
- Where are agents registered and governed?
- How are prompts and responses screened?
- How do teams observe latency, quality, cost, and failures across the ecosystem?

Those questions define Book 2.
