# Appendix B — Contract, State and Tool Reference

> **Status: outline.** Field tables are filled in as Chapters 8–13 define
> them. The structure and the rules below are settled.

The lookup surface: every domain contract, every graph state key with its
owner, and every tool with its declaration. Chapters argue; this appendix
is what you keep open while writing code.

---

## B.1 Domain contracts

Six Pydantic models, introduced in Chapter 8. Each carries
`schema_version` so additions do not break readers of stored results.

| Contract | Chapter | Produced by | Consumed by |
|---|:---:|---|---|
| `ResearchResult` | 8 | `profile_company`, `find_signals` | `join_research`, `verify_evidence` |
| `EvidenceItem` | 8 | research, MCP boundary, retrieval | everything downstream |
| `QualificationResult` | 8 | `qualify_account` | `qualification_route`, `draft_outreach` |
| `Draft` | 8 | `draft_outreach`, `revise_draft` | `review_draft`, `prepare_approval` |
| `ReviewResult` | 8 | `review_draft`, evaluation judge | `review_route`, `revise_draft` |
| `Escalation` | 8 | any node that cannot proceed | `prepare_approval` |

**To fill in per contract:** field name, type, required, constraint, and the
section that introduces it.

### `EvidenceItem` — the shape that matters most

Referenced by every other contract and by seven chapters. Fields follow
`app/contracts/evidence-policy.yaml` (Appendix C):

`evidence_id` · `source` · `source_location` · `source_date` ·
`retrieval_date` · `retrieval_method` · `retrieval_score` ·
`evidence_text` · `content_hash` · `claim_type` · `support_type` ·
`confidence`

`claim_type` and `support_type` are independently required. Chapter 3.8
argues why; Appendix C.4 shows what goes wrong when they are collapsed.

### `QualificationResult`

`decision` is the enum the graph routes on:
`QUALIFIED` | `INSUFFICIENT` | `DISQUALIFIED`.

Carries `evidence_refs: list[str]` — **identifiers, not embedded objects**
(Chapter 8.9). Evidence lives once, in the ledger.

## B.2 Evidence by reference, everywhere

The rule, stated once for the whole book:

> A contract referring to evidence carries `evidence_id` strings. It never
> embeds `EvidenceItem` objects.

Embedding creates a second copy that can diverge from the ledger, and
makes it impossible to say which version of a fact a decision was based on.
A dangling reference fails validation (Chapter 8.10).

## B.3 Graph state

`SDRState`, a `TypedDict` — **not** a Pydantic model (Chapter 8.4).
Pydantic validates values; LangGraph merges partial updates per key, which
is a different job.

**To fill in:** the full ownership table.

| Key | Type | Reducer | Owned by | Read by |
|---|---|---|---|---|
| `messages` | `list` | `add_messages` | agent nodes | agent nodes |
| `evidence` | `list[EvidenceItem]` | `add` | research, retrieval | verify, qualify, draft |
| `company_profile` | `ResearchResult \| None` | — | `profile_company` | join, qualify |
| `signals` | `ResearchResult \| None` | — | `find_signals` | join, qualify |
| `qualification` | `QualificationResult \| None` | — | `qualify_account` | route, draft |
| `draft` | `Draft \| None` | — | `draft_outreach`, `revise_draft` | review, approval |
| `review` | `ReviewResult \| None` | — | `review_draft` | route, revise |
| `iteration` | `int` | — | `revise_draft` | `review_route` |
| `stop_reason` | `str \| None` | — | `review_route` | manifest, approval |
| `escalation` | `Escalation \| None` | — | any node | `prepare_approval` |

Two rules, both tested (Chapter 11.11):

1. **A node returns only keys it owns.** A node writing another's key fails
   a test.
2. **Two nodes writing the same key need a reducer**, or one silently wins.
   `evidence` accumulates from several sources, which is why it has one.

## B.4 Tool declarations

Every tool declares all eight, introduced in Chapter 5.7 and enforced from
Chapter 6.

| Field | Meaning |
|---|---|
| Purpose | What it does, in one sentence the model reads |
| Typed input | Pydantic model or annotated signature |
| Typed output | Contract returned |
| Read or write | Classification the policy gate enforces |
| Authorization | What the `RequestContext` must permit |
| Failure modes | Enumerated, each with defined behaviour |
| Timeout | Explicit; no unbounded call |
| Audit | What is recorded on invocation and refusal |

A tool missing a policy declaration fails a test (Chapter 6.9). That is the
mechanism preventing enforcement from being something each tool remembers
to do.

### Inventory

**To fill in as each is built.**

| Tool | Chapter | Class | Transport | Notes |
|---|:---:|:---:|---|---|
| `fetch_webpage` | 5 | read | in-process → MCP (Ch. 9) | Offline via fixtures by default |
| `search_company_news` | 5 | read | in-process → MCP (Ch. 9) | Offline via fixtures by default |
| `hybrid_search` | 10 | read | in-process | Corpus only; never external |

Book 1 has **no write-classified tool**. The classification exists because
the policy gate needs it from the first tool, and because a reader adding
one must confront the classification rather than inherit a default.

There is no send tool, in any chapter (Chapter 3.6).

## B.5 The six kinds of state, distinguished

Expanded in Chapter 15.4; repeated here because conflating any two produces
a bug that looks like data loss.

| | Scope | Survives restart | Store |
|---|---|:---:|---|
| Checkpoint | one thread | yes | `PostgresSaver` |
| Conversation history | one thread | yes, within the checkpoint | `messages` |
| Application memory | cross-thread | yes | own repository |
| Evidence | global | yes | evidence ledger |
| Artifacts | per run | yes | filesystem |
| Audit history | global, append-only | yes | audit log |

**A checkpointer is not a memory system.** It resumes an interrupted run.
It does not remember that this account was researched last month.

## B.6 Manifest fields by version

`RUN_MANIFEST.json` grows as versions earn fields. A field appears in the
version that can populate it — never speculatively, because a field that is
always `null` trains readers to stop reading the manifest.

| Field | From |
|---|:---:|
| `schema_version`, `recorded_at`, `version_tag` | V0 |
| `application`, `runtime`, `dependencies` | V0 |
| `model` | V0 |
| `autonomy_boundary` | V0 |
| `policies` (content hash) | V2 |
| `skills` (name, version, hash) | V3 |
| `contracts` (schema versions) | V4 |
| `mcp` (server name, version, tool inventory) | V5 |
| `corpus` (version, hash, embedding model, dimension) | V6 |
| `graph` (node inventory, topology hash) | V7 |
| `evaluation` (dataset version, judge model, scores) | V8 |
| `review_loop` (threshold, max iterations, stop reason) | V9 |
| `trace` (trace id, capture mode) | V10 |

## B.7 Stop reasons

Every run records exactly one (Chapter 13.5).

| Value | Meaning |
|---|---|
| `threshold_met` | Review score reached the exit threshold |
| `max_iterations` | Iteration limit reached; best draft escalated |
| `no_improvement` | Score stagnated; further iterations are waste |
| `escalated` | Unfixable problem — typically an unsupported claim |

`no_improvement` is separate from `max_iterations` deliberately. Conflating
them burns the full budget on a draft the second pass already showed would
not improve.

## B.8 Route decisions

Pure functions of state, testable without a model (Chapter 11.10).

| Route | Reads | Branches |
|---|---|---|
| `qualification_route` | `qualification.decision` | `QUALIFIED` → ground+draft · `INSUFFICIENT` → request more · `DISQUALIFIED` → disposition |
| `review_route` | `review.score`, `iteration`, previous score, `review.is_fixable` | revise · approve · escalate |
| `agent_route` (V1) | pending tool call | tools · `END` |

Every branch is exercised by a state fixture with no model call. Chapter
11.16's exercise is to notice how much faster that is than testing the V6
equivalent.
