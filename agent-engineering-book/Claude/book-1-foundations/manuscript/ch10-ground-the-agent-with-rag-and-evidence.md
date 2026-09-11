# Chapter 10 — Ground the Agent with RAG and Evidence

> **Status: outline.**

**Starting point:** V5 — sourced external research
**Result:** V6 — grounded product knowledge with citations

---

## 10.1 Current state and observed limitation

Read V5's drafts. Every claim about the prospect carries a source. Every
claim about WidgetWare does not:

> *"Our platform typically delivers 30% reduction in unplanned downtime for
> manufacturers of your scale."*

Nothing in `config/offering.yaml` says that. The model produced a
plausible-sounding number because outreach messages contain
plausible-sounding numbers.

This is worse than an unsourced claim about the prospect. An error about the
prospect is embarrassing. **An invented claim about your own product is a
misrepresentation your company made in writing.**

## 10.2 Engineering question

> Can our own claims be held to the same evidence standard we already apply
> to the prospect's?

## 10.3 Architectural decision

Build a governed WidgetWare corpus and retrieve from it, using **PostgreSQL
with `pgvector` for vector search and PostgreSQL full-text search for
keyword search**, combined by a **small, visible hybrid-ranking function**,
with a **pinned open embedding model** via SentenceTransformers.

Retrieved passages become `EvidenceItem`s in the Chapter 6 ledger, with
stable citation identifiers. A product claim without a resolvable citation
does not reach a draft.

## 10.4 RAG, from zero

For readers meeting it for the first time. Retrieval-Augmented Generation
means: before asking the model to write, find the relevant documents and put
them in its context, so it answers from them rather than from memory.

The pipeline, each stage with a decision:

1. **Ingest** — what is in the corpus, and who governs it.
2. **Chunk** — how a document is split. Too large dilutes; too small loses
   context. Proof points are chunked as whole units because splitting a
   customer outcome from its qualifying conditions is how a caveat gets
   lost.
3. **Embed** — text to vector, with a pinned model.
4. **Retrieve** — vector similarity, keyword match, or both.
5. **Rank** — combine and order.
6. **Cite** — carry identifiers through so a claim resolves to a passage.

Stage 6 is the one most tutorials skip and the one this chapter is for.

## 10.5 Why hybrid, concretely

Vector search finds *"reduces machine failures"* for a query about
*"unplanned downtime."* It also cheerfully returns the wrong product line,
because product names are precisely where semantic similarity fails —
"WidgetWare Fleet" and "WidgetWare Flow" embed almost identically.

Keyword search gets exact product names right and misses every paraphrase.

Hybrid, via a readable reciprocal-rank-fusion function of about fifteen
lines, gets both. The book shows the function rather than importing it,
because a reader who cannot see how results are ranked cannot debug why the
wrong passage was cited.

## 10.6 Alternatives considered

**LlamaIndex or LangChain retrievers.** Excluded by the brief, and the
reasoning is sound for a foundations book: they collapse stages 1–5 into a
few calls, and a reader who has not seen chunking decided cannot make one.

**Vector-only retrieval.** Rejected for the product-name failure above,
which is not an edge case here — product names are the most important terms
in the corpus.

**A dedicated vector database.** Rejected: PostgreSQL is already needed for
checkpointing (Chapter 15) and the ledger, and one service the reader can
run locally beats two.

**Retrieve for prospect research too.** Rejected as scope creep. Prospect
facts come from live sources via MCP; a stale cached copy of a company's
website is a worse source than the site.

## 10.7 Trade-offs

The corpus becomes an asset requiring governance: who adds a proof point,
who removes a stale one, what happens when a claim is retracted. The chapter
names this and implements only a version field and an ingestion script —
adequate for a book, inadequate for a company, and said plainly.

Retrieval adds latency and a database dependency to a system that ran with
neither.

Embedding models drift. The model is pinned in `pyproject.toml` and recorded
in the manifest, because re-embedding with a different model silently
changes every retrieval result.

## 10.8 Implementation walkthrough

- `app/retrieval/schema.sql` — `documents`, `chunks` (with `vector` column
  and a generated `tsvector`), indexes.
- `app/retrieval/ingest.py` — corpus from `config/offering.yaml`,
  `proof-points.yaml` and `data/corpus/`; chunking with proof points kept
  whole; content hash per chunk.
- `app/retrieval/embed.py` — pinned SentenceTransformers model, batched.
- `app/retrieval/search.py` — `vector_search`, `keyword_search`,
  `hybrid_search` with the fusion function inline and commented.
- `app/nodes/ground_claims.py` — retrieve for each product claim; a claim
  with no supporting passage is marked `unsupported` and removed from the
  draft rather than softened.

That last decision is the chapter's spine: **the response to an unsupported
claim is deletion, not hedging.** "May help reduce downtime" is the same
misrepresentation with a modal verb in front of it.

## 10.9 Tests and evaluation

- A labelled query set: for each query, the expected passage is retrieved in
  the top *k*. Reported per method — vector, keyword, hybrid — so the hybrid
  claim is demonstrated rather than asserted.
- Product-name queries: keyword and hybrid succeed, vector-only fails. This
  test exists to make §10.5 checkable.
- Every product claim in a V6 draft resolves to a real `evidence_id`.
- A claim with no support is absent from the draft, not softened.
- Re-ingestion is idempotent by content hash.

## 10.10 Failure demonstration

Ask for outreach mentioning a capability WidgetWare does not have. V5
invents supporting detail. V6 finds nothing, marks it unsupported, and the
draft omits it — visibly, with the omission recorded so a reviewer can see
what was dropped and why.

## 10.11 Evidence of improvement

Unsupported product claims per draft: V5 baseline → V6 zero. Retrieval
quality per method on the labelled set.

## 10.12 Updated run manifest

`version_tag: "v6-grounded"`, corpus version and hash, embedding model id and
dimension, retrieval parameters.

## 10.13 What remains unresolved

Every claim is now sourced and every product claim grounded — and one prompt
still performs research, qualification and drafting together. When a run
produces a bad brief there is no way to say *which responsibility* failed,
and a research failure discards completed qualification work.

## 10.14 Exercises

1. Halve the chunk size and re-run the labelled query set. Which queries got
   worse, and can you explain why from the chunks themselves?
2. Add a proof point with a qualifying condition ("for plants over 500
   staff"). Does retrieval keep the condition attached to the claim? If not,
   that is a chunking bug with legal consequences.
