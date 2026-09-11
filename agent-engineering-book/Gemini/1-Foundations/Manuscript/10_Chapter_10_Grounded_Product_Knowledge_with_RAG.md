# Chapter 10: Grounded Product Knowledge with RAG

## Chapter purpose

Chapter 9 established that no claim about the prospect may float without a source.
It left the other half of the message ungrounded. When WidgetWare's draft says
"we helped a similar manufacturer reduce unplanned downtime," nothing checks that
such a customer exists, that the number is current, or that the product still
works the way the sentence implies.

This chapter applies the same evidence discipline to WidgetWare's own knowledge,
using retrieval over a corpus the company owns rather than tools that fetch the
public web.

## Product version

**Starting point:** V5 — evidence-backed agent  
**Result:** V6 — grounded agent

## Engineering question

> Can the draft's claims about our own product be traced to a document, the way
> its claims about the prospect already are?

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish retrieval over an owned corpus from tool-based external research;
- assemble a small governed corpus and state what belongs in it;
- explain chunking, embedding and similarity retrieval without treating them as magic;
- return retrieved passages as evidence items rather than as prose;
- cite product claims in a draft the same way research claims are cited;
- recognize the two failure modes that matter — confident irrelevance and stale positioning; and
- measure grounding as a percentage rather than asserting it.

## Seven-Step mapping

**Primary:** Build Context  
**Supporting:** Design Agent Capabilities, Evaluate & Govern

## The WidgetWare increment

Index WidgetWare's product documentation, competitive positioning and prior
account histories. The outreach draft may assert a product capability, a customer
outcome or a differentiator only when a retrieved passage supports it.

## 10.1 Two kinds of evidence, one ledger

Chapter 9 answered questions about a company WidgetWare does not control, from
sources it does not own, fetched at the moment of asking. This chapter answers
questions about WidgetWare itself, from documents it does own, indexed in advance.

The differences are real and worth naming:

| | External research (Chapter 9) | Owned knowledge (this chapter) |
| --- | --- | --- |
| Subject | The prospect | WidgetWare |
| Corpus | Public, uncontrolled | Curated, governed |
| Timing | Fetched per request | Indexed ahead of time |
| Dominant risk | Untrusted input, staleness | Wrong passage retrieved confidently |
| Freshness control | Retrieval timestamp | Re-indexing policy |

What must not differ is where the answers land. Both produce **evidence items in
the same ledger**, carrying source, excerpt and retrieval time. A reviewer should
not have to learn two formats to audit one email, and the qualification contract
from Chapter 8 should not care which retrieval path produced a citation.

## 10.2 What belongs in the corpus

A corpus is a governed collection, not a folder. For WidgetWare, three categories
earn their place:

- **product documentation** — what the product does, in the words the company is
  willing to stand behind;
- **competitive positioning** — how WidgetWare differs from named alternatives; and
- **prior account histories** — what was sold, to whom, and what outcome followed.

Each document needs an owner, a review date and a statement of whether it may be
quoted to a customer. A case study cleared for publication and an internal
post-mortem describing the same account are both true and only one may be cited.

Marking that distinction is corpus governance, and it is the cheapest control in
this chapter. Skipping it is how an internal note reaches a prospect.

## 10.3 Chunking is a design decision

Retrieval does not return documents; it returns passages. How a document is split
determines what can be found and what can be cited.

Two failures bracket the choice. Chunks that are too small retrieve a sentence
with no context — a percentage with no idea what it measures. Chunks that are too
large retrieve a page to support one clause, and the model is free to draw on
material no one intended as support.

Prefer splitting on structure the document already has — sections, headings, table
rows — over splitting on a fixed character count. A chunk should be the smallest
passage that remains true when read alone.

Every chunk carries its document identifier, section, owner and review date. That
metadata is what makes a citation resolvable later.

## 10.4 Embeddings and retrieval, without mystique

An embedding maps text to a vector so that passages about similar things sit near
each other. Retrieval embeds the query, finds the nearest chunks, and returns them.

Two consequences follow, and both matter more than the mechanism:

- **Similarity is not relevance.** The nearest chunk is the nearest one that
  exists, whether or not anything in the corpus actually answers the question.
  Retrieval always returns something.
- **Similarity is not truth.** A retrieved passage may be outdated, superseded, or
  correct about a product tier the prospect is not buying.

On Google Cloud, Vertex AI RAG Engine provides ingestion, chunking, embedding and
retrieval as a managed service, which is the right default for this book. The
engineering that matters is not which service performs the search — it is what the
system does with a result that is near but wrong.

## 10.5 Confident irrelevance

This is the failure mode to design against.

A tool that cannot reach Wikipedia raises an error, and Chapter 9 taught the agent
to degrade honestly. A retriever that finds nothing relevant does not fail. It
returns its best three chunks with respectable similarity scores, and a model
handed three passages will use them.

Three defenses, in order of value:

1. **A relevance floor.** Below a similarity threshold, return no passages rather
   than the least bad ones. An empty result is a usable answer.
2. **An explicit unknown.** The research brief already has an `unknowns[]` field.
   Unsupported product claims belong there, not in the draft.
3. **Claim-level citation.** A draft sentence asserting a capability, a number or a
   customer outcome carries a chunk reference or it does not ship.

The third defense is what makes the failure visible. Without it, "grounded" is a
claim about the architecture rather than a property of the output.

## 10.6 Stale positioning

An external source is stale when the world moves. An owned corpus is stale when
*the company* moves — a repositioned product, a retired integration, a customer
who has since churned and may not be named.

Freshness here is a review policy, not a retrieval timestamp. Each document
carries a review date; retrieval surfaces it; the draft may not cite a passage
whose review date has lapsed. A citation to a case study about a lost customer is
worse than no citation at all, and no similarity score will catch it.

## 10.7 Extending the ledger

The `ResearchBrief` from §9.7 gains a second evidence source rather than a second
structure:

```text
EvidenceItem
- source_kind: EXTERNAL_RESEARCH | OWNED_KNOWLEDGE
- source_ref: URL, or document id + section
- excerpt
- retrieved_at
- review_date        (owned knowledge only)
- citable_externally (owned knowledge only)
- reliability
```

One field distinguishes the paths. Everything downstream — the qualification
contract, the reviewer interface, the evaluation set — reads one shape.

## Hands-on lab: Ground the outreach draft

1. Assemble a small corpus: three product documents, one competitive comparison
   and two prior account histories.
2. Mark each document with an owner, a review date and an external-citability flag.
3. Ingest and index the corpus.
4. Retrieve against three drafting questions, and read the returned chunks.
5. Ask one question the corpus cannot answer, and observe what comes back.
6. Add a relevance floor and confirm that same question now returns nothing.
7. Emit retrieved passages as `EvidenceItem` records with `source_kind: OWNED_KNOWLEDGE`.
8. Require every product claim in the draft to carry a chunk reference.
9. Route unsupported claims to `unknowns[]`.
10. Report the percentage of product claims that are grounded, across the golden
    accounts.

## Evaluation checklist

- Does every product claim in a draft carry a resolvable citation?
- Does a question the corpus cannot answer produce nothing rather than something?
- Are internal-only documents structurally prevented from being quoted externally?
- Do owned-knowledge evidence items share the ledger shape with external research?
- Is a lapsed review date treated as a blocking condition?
- Is grounding reported as a measured percentage rather than asserted?

## Chapter checkpoint

WidgetWare V6 can defend both halves of its message. Claims about the prospect
trace to external sources; claims about the product trace to owned documents; both
sit in one ledger a reviewer can audit in one pass.

The agent is now doing five jobs — applying Skills, honoring contracts, researching
externally, retrieving internally, and drafting — inside one prompt. Every
capability the product needs exists. Nothing organizes them.

## Bridge to Chapter 11

Chapter 11 stops adding capability and starts imposing structure. The five jobs
become nodes with typed handoffs and explicit routes, so that a failure in one is
diagnosable and recoverable without re-running the rest.

## Exercises

1. Take one sentence from a WidgetWare outreach draft that asserts a product
   capability. Write down what document would have to exist for that sentence to
   be citable, and whether it does.
2. §10.5 argues that retrieval returning nothing is a feature. Describe a case
   where returning the nearest-but-irrelevant passage would produce a worse
   business outcome than an empty result.
3. A case study is cleared for publication. Eighteen months later that customer
   churns. Using §10.6, state which control should prevent the case study from
   being cited, and at what point in the pipeline it acts.
4. §10.1 insists both retrieval paths share one ledger shape. Name one thing that
   becomes harder if they are allowed to diverge.
