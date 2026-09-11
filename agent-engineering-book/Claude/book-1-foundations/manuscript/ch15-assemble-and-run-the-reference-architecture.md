# Chapter 15 — Assemble and Run the Book 1 Reference Architecture

> **Status: outline.**

**Starting point:** V10 (part 1) — instrumented
**Result:** V10 — a running, restartable, reproducible system

---

## 15.1 Current state and observed limitation

Everything works under `pytest`. Nothing is a system anyone can run.

- State lives in `InMemorySaver`. An interrupted run starts over.
- There is no interface. The entry point is a test.
- There is no packaging. Running it means reproducing a developer's machine.
- Human approval — the boundary the whole book is built around — has no
  mechanism. The system prepares an approval package and stops.

## 15.2 Engineering question

> Can someone else run this, interrupt it, restart it, approve its output,
> and reconstruct afterwards what happened and why?

## 15.3 Architectural decision

Four additions, no new capability:

1. **`PostgresSaver` checkpointing** — thread-scoped execution state that
   survives a restart.
2. **A FastAPI boundary** — authentication, `RequestContext` construction,
   run submission, status, approval.
3. **`interrupt()` / `Command(resume=...)`** — the approval pause as a
   first-class graph mechanism.
4. **Docker Compose** — application and PostgreSQL, non-root, read-only
   root filesystem, secrets injected.

## 15.4 Six kinds of state, distinguished

The brief insists on this and it is worth a section, because conflating any
two produces a bug that looks like data loss.

| | Holds | Scope | Survives |
|---|---|---|---|
| **Checkpoint** | graph execution state mid-run | one thread | restart |
| **Conversation history** | messages in the current run | one thread | restart, as part of the checkpoint |
| **Application memory** | facts about an account across runs | cross-thread | indefinitely, in its own store |
| **Evidence store** | evidence items with provenance | global | indefinitely |
| **Artifacts** | generated briefs and drafts | per run | indefinitely |
| **Audit history** | who did what, permitted or refused | global, append-only | indefinitely |

**A checkpointer is not a memory system.** It resumes an interrupted run. It
does not remember that this account was researched last month — that is
application memory, it needs its own store, and Book 1 keeps it deliberately
minimal so the distinction stays visible.

## 15.5 The approval pause

```python
decision = interrupt({
    "account": state["account"],
    "draft": state["draft"],
    "evidence": state["evidence_refs"],
    "qualification": state["qualification"],
})
```

Execution suspends, state is checkpointed, and the graph waits. A reviewer
reads the package through the API and resumes with
`Command(resume=decision)`.

Approve, edit and reject are three different outcomes with three different
meanings, and the API models them distinctly rather than as a boolean. An
edit is a human authoring the final text; the system records that the text
it produced was not the text accepted, which is the signal that tells you
whether the drafting is actually good.

And the approval leads nowhere. Book 1 has no send tool — Chapter 3's
boundary, still holding at the last chapter. The approved package is
written, recorded and handed to a person.

## 15.6 Alternatives considered

**SQLite checkpointing.** Adequate and one less service — except PostgreSQL
is already required for retrieval and the ledger. One database beats two.

**A CLI instead of an API.** Simpler, and it cannot express the approval
pause, which needs a mechanism for a second actor to resume a suspended run.

**Kubernetes, or any orchestrated deployment.** Out of scope by the brief.
Compose is reproducible on one machine, which is what a book can honestly
promise.

**Storing approvals in the checkpoint.** Rejected — approvals are audit
records with independent lifetime. A checkpoint is deleted when a thread
completes; an approval must outlive it.

## 15.7 Trade-offs

The FastAPI layer is real code — auth, request validation, error mapping —
serving one workflow. Named as the cost of having a boundary at all.

`thread_id` must stay under 255 characters with `PostgresSaver` (ADR-000).
Thread naming is `{tenant}:{account}:{run}` with an explicit length
assertion, because discovering this limit in production is unpleasant.

Compose is not a deployment. High availability, migrations, secret rotation,
and rollback are Book 4's subject and are named in §15.11 rather than
half-built.

## 15.8 Implementation walkthrough

- `app/api/main.py` — `POST /runs`, `GET /runs/{id}`,
  `GET /runs/{id}/approval`, `POST /runs/{id}/approval`.
- `app/api/auth.py` — authenticate, then construct the trusted
  `RequestContext`. Chapter 6's rule holds: context comes from authenticated
  input, never from anything the model produced.
- `app/persistence/checkpointer.py` — `PostgresSaver.from_conn_string`,
  `setup()`, thread-id construction with the length assertion.
- `Dockerfile` — non-root user `10001`, read-only root filesystem, no
  secrets in any layer.
- `scripts/verify_clean_clone.sh` — clone, install, migrate, ingest, test.

## 15.9 Tests and evaluation

- A run interrupted mid-graph resumes from its checkpoint and does not
  re-execute completed nodes — asserted from the checkpoint, not by
  inspecting logs.
- Approve, edit and reject each produce distinct recorded outcomes.
- The audit history reconstructs a full run without the trace backend.
- The container runs as non-root with a read-only root filesystem.
- No secret appears in any image layer.
- `scripts/verify_clean_clone.sh` passes from a fresh clone.

## 15.10 The Book 1 reference architecture

The complete diagram: FastAPI boundary → `RequestContext` → LangGraph
(validate → parallel research → join → verify → qualify → route → ground →
draft → review loop → approval interrupt) with Skills, MCP tools, hybrid
retrieval, the policy gate, the evidence ledger, the audit log,
checkpointing and tracing around it.

Then the version ladder, each step with the observation that earned it —
the book's actual argument in one page.

## 15.11 Known limitations

Stated plainly, because a book that ends by claiming completeness has
mistaken its own scope for the world.

The evaluation set is small enough to overfit. Application memory is
minimal. The policy layer is application-level and not an identity system.
Corpus governance is a version field. There is no rate limiting, no cost
ceiling, no multi-tenancy beyond a validated identifier, no migration
strategy, no rollback, no SLO alerting, no threat model. Single instance,
single region.

Each names the later book that takes it up.

## 15.12 Acceptance criteria

The checklist the book is answerable to:

- [ ] Stands alone with no reference to another implementation
- [ ] LangGraph is the only orchestration framework
- [ ] Claude Code is separate from the application runtime
- [ ] Every component has a defined responsibility
- [ ] One reference application evolves through every version
- [ ] Each change begins with an observed need
- [ ] Each claimed improvement is supported by evidence
- [ ] Tools, Skills, MCP, RAG, state, memory and artifacts are distinguished
- [ ] The agent produces attributable evidence
- [ ] The review loop is bounded and testable
- [ ] Golden and adversarial evaluations run
- [ ] Traces make the execution path understandable
- [ ] It runs locally from a clean clone
- [ ] The architecture leads into the advanced books

## 15.13 What comes next

Book 2 takes the single-account graph and asks what changes when one system
serves many accounts, many tenants and many concurrent runs — memory that
persists, context that must be budgeted, planning, and collaboration between
agents.

The Book 1 system is the thing those books modify. It is deliberately
small enough to hold in your head, and complete enough to be worth
extending.

## 15.14 Exercises

1. Interrupt a run at each node in turn and resume. Is there a node where
   resumption repeats work? That is a checkpoint-granularity decision —
   was it the right one?
2. Pick three items from §15.11. For each, write the observation that would
   tell you it had stopped being acceptable.
