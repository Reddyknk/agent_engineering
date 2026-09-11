# Chapter 8 — Replace Prose with Typed Contracts

> **Status: outline.**

**Starting point:** V3 — reusable Skills
**Result:** V4 — typed, validated domain contracts

---

## 8.1 Current state and observed limitation

V3's qualification is a paragraph:

> *"Rockwell Automation appears to be a strong fit given their scale and
> recent emphasis on AI-enabled offerings, though I have some reservations
> about timing."*

A person reads that fine. Nothing else can. You cannot route on it, store it
in a column, compare it across runs, count how many accounts qualified, or
tell whether "some reservations" means the same thing this week as last.

Chapter 11 needs to branch on the decision. It cannot branch on a mood.

## 8.2 Engineering question

> Can another system act on this output without parsing English?

## 8.3 Architectural decision

Define **Pydantic contracts** for every domain object, produce them with
Claude's **native structured output**, and **validate at every node
boundary** with an explicit repair path on failure.

Six contracts: `ResearchResult`, `EvidenceItem`, `QualificationResult`,
`Draft`, `ReviewResult`, `Escalation`.

## 8.4 Two type systems, deliberately

A distinction that confuses people and is worth being firm about:

| | Used for | Why |
|---|---|---|
| **Pydantic models** | external requests/responses, domain objects | validation, coercion, JSON Schema generation, error messages |
| **TypedDict + reducers** | LangGraph internal state | LangGraph merges partial updates per key; a Pydantic model is a value, not a merge strategy |

Graph state *holds* Pydantic objects. It is not itself one. Getting this
backwards produces either state that cannot merge or contracts that cannot
validate.

## 8.5 Native structured output

```python
structured = model.with_structured_output(QualificationResult, method="json_schema")
```

`method="json_schema"` activates Anthropic's native structured output, which
validates names and argument types through constrained decoding
(ADR-000). This supersedes the older pattern of declaring one tool and
forcing the model to call it.

**Constrained decoding guarantees shape, not correctness.** A
`QualificationResult` with `decision="QUALIFIED"` and `confidence=0.9` is
schema-valid and may still be wrong. Validation at the boundary catches
malformed; only Chapter 12 catches mistaken.

## 8.6 Alternatives considered

**"Return JSON" in the prompt plus `json.loads`.** The common approach.
Rejected: no guarantee, and it fails by *sometimes* working — a stray
preamble breaks parsing in production having passed every test.

**Forced tool use.** Superseded by native structured output; see ADR-000.

**Instructor or a similar wrapper.** Adds a dependency to provide retry and
validation the provider now does natively and the brief asks us to write
visibly.

**One large `AccountBrief` contract** instead of six. Rejected — a single
object means every node depends on every field, and Chapter 11's typed
handoffs become impossible. Each node should publish only what the next
responsibility needs.

## 8.7 Trade-offs

Contracts are rigid where the domain is not. A company that half-fits gets
squeezed into an enum. The mitigation is the `INSUFFICIENT` decision and a
required `reasoning` field, not a looser schema.

Schema changes become breaking changes. `schema_version` is on every
contract from the start, and the chapter shows an additive migration.

## 8.8 Implementation walkthrough

- `app/contracts/evidence.py` — `EvidenceItem` carrying `evidence_id`,
  source, source location, retrieved passage, retrieval method, score,
  timestamp, content hash, `claim_type`, `support_type`. The Chapter 3
  policy becomes a type.
- `app/contracts/qualification.py` — `QualificationResult`: `decision`
  (`QUALIFIED` | `INSUFFICIENT` | `DISQUALIFIED`), `confidence`,
  `reasoning`, `criteria_assessments`, `evidence_refs`.
- `app/contracts/{research,draft,review,escalation}.py`.
- `app/nodes/validation.py` — boundary validation; on `ValidationError`,
  one repair attempt with the error fed back, then escalate.

The repair loop is bounded at one attempt and records why. An unbounded
repair loop is Chapter 1's runaway-loop failure pattern wearing a
respectable name.

## 8.9 Evidence references, not embedded evidence

`QualificationResult` carries `evidence_refs: list[str]`, not evidence
objects. Evidence lives once, in the Chapter 6 ledger. Embedding copies
means two versions of the same fact and no way to tell which was used.

## 8.10 Tests and evaluation

- Every contract round-trips through JSON.
- A malformed model response triggers exactly one repair, then escalation.
- `evidence_refs` resolve against the ledger; a dangling reference fails.
- `claim_type` and `support_type` are independently required.
- 100% structural validity across the thirteen accounts.

## 8.11 Failure demonstration

Force the model to return a decision outside the enum. Show the validation
error, the repair attempt with the error included, and — when repair fails —
a structured `Escalation` rather than a crash or a silently wrong answer.

## 8.12 Evidence of improvement

Structural validity: V3 unmeasurable → V4 100%. Qualification decisions
countable and comparable across runs for the first time.

## 8.13 Updated run manifest

`version_tag: "v4-contracts"`, contract schema versions.

## 8.14 What remains unresolved

The output has a guaranteed shape and no guaranteed truth. `evidence_refs`
can point at evidence the agent essentially invented, because nothing yet
requires a claim to come from a source that can be resolved and re-checked.

## 8.15 Exercises

1. Add a field to `QualificationResult` without breaking existing stored
   results. What made that possible?
2. Find a place in the contracts where an enum is hiding real ambiguity.
   Would a wider type or a required explanation serve better?
