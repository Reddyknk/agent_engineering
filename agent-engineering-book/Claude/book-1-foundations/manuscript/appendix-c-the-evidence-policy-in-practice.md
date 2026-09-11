# Appendix C — The Evidence Policy in Practice

The policy is in `app/contracts/evidence-policy.yaml` and argued in Chapter
3.8. This appendix is the part that cannot be argued, only practised:
classifying real claims.

Readers get this wrong in a consistent direction — they treat the two
dimensions as one, and label anything well-sourced a `fact`. The examples
below are chosen to make that collapse impossible to sustain.

---

## C.1 The two dimensions

**`claim_type`** — what *kind of statement* this is.

| | |
|---|---|
| `fact` | Directly verifiable as stated; not contingent on further reasoning |
| `inference` | A reasoned conclusion from facts, not asserted by any source |
| `hypothesis` | A proposition offered for testing; explicitly speculative |

**`support_type`** — how the cited evidence *backs it*.

| | |
|---|---|
| `direct` | The source states this, in these or equivalent words |
| `derived` | Reasoned from one or more cited sources |
| `unsupported` | Nothing cited establishes it |

They are independent. That is the whole point, and §C.3 is where it becomes
obvious.

## C.2 The grid

Nine combinations. Five are legal, four are rejected.

| | `direct` | `derived` | `unsupported` |
|---|:---:|:---:|:---:|
| **`fact`** | ✅ ideal | ✅ legal, rare | ❌ rejected |
| **`inference`** | ⚠️ suspect | ✅ the common case | ❌ rejected |
| **`hypothesis`** | ⚠️ suspect | ✅ legal | ✅ legal, must be labelled |

**`fact` + `unsupported`** and **`inference` + `unsupported`** are the two
rejections that matter. They are exactly the confident fabrication from
Chapter 1.5 — a statement presented as established with nothing behind it.

**`fact` + `direct`** is what research should mostly produce.

**`fact` + `derived`** is legal but should make you look twice. A fact
assembled from two sources is often really an inference. Example: source A
says the company has 12 plants, source B says each employs about 400 —
"roughly 4,800 plant staff" is arithmetic on cited numbers, so `fact` /
`derived` holds. But "the company is scaling its plant workforce" from the
same two sources is an `inference`, not a fact, and mislabelling it is the
most common error in the corpus.

**`hypothesis` + `unsupported`** is the one case where a claim with no
source is allowed — and only when it is labelled as speculation and reaches
the reviewer as such.

## C.3 Worked examples

Fifteen claims about Rockwell Automation, an account in `data/accounts.csv`.

### Correctly classified

**1.** *"Rockwell Automation describes itself as an industrial automation
and digital transformation company."*
→ `fact` / `direct` · Source: rockwellautomation.com/about, retrieved
2026-09-01. The source says this in these words.

**2.** *"Rockwell Automation employs approximately 27,000 people."*
→ `fact` / `direct` · Source: 2025 annual report. Verifiable as stated.

**3.** *"Rockwell falls within the WidgetWare ICP employee band."*
→ `fact` / `derived` · Sources: claim 2, plus `config/icp.yaml`
(minimum 5,000). A comparison of two cited numbers. Note this is
arithmetic, not judgment — Chapter 11.5 moves it to a function node.

**4.** *"Rockwell is emphasising AI-enabled offerings across its automation
portfolio."*
→ `fact` / `direct` · Source: product-launch press release, 2026-06-12.
The company asserts this about itself.

**5.** *"Rockwell's AI emphasis suggests active investment in data platform
modernisation."*
→ `inference` / `derived` · Source: claim 4. Reasonable, and no source
says it. Labelling this a `fact` is the error this appendix exists to
prevent.

**6.** *"Rockwell may be evaluating vendors for industrial data
integration."*
→ `hypothesis` / `unsupported` · No source. Legal because it is labelled
speculative and goes to a human to validate in conversation.

**7.** *"Rockwell's plant operations leaders are a relevant buying centre
for WidgetWare."*
→ `inference` / `derived` · Sources: `config/icp.yaml` target roles, plus
claim 1.

**8.** *"WidgetWare's platform integrates with ERP and MES systems."*
→ `fact` / `direct` · Source: `config/offering.yaml`, retrieved via
Chapter 10 grounding. A claim about *our own* product still needs a
citation — Chapter 10.1's central argument.

### Rejected, and why

**9.** *"Rockwell has budget allocated for a data platform purchase this
quarter."*
→ ❌ `fact` / `unsupported`. Presented as established, nothing behind it.
Rejected by the first condition in `rejection_conditions`.
**Repair:** demote to `hypothesis` / `unsupported`, or find a source.

**10.** *"Rockwell's CIO is Jane Smith."*
→ ❌ Rejected by *"claim states a person's identity or role without direct
evidence linking them to it."* Personnel claims decay fastest and embarrass
most. A LinkedIn search result is not direct evidence linking a named
person to a current role.

**11.** *"We spoke with your team about automation challenges last
quarter."*
→ ❌ Rejected by *"claim implies prior contact or familiarity with the
recipient."* The system has never spoken with anyone. This is the failure
mode of a model imitating the register of sales copy, and it is why the
rejection condition is explicit rather than left to judgment.

**12.** *"Rockwell announced a major restructuring."* Source dated
2024-03-01.
→ ❌ Rejected by staleness — 180 days in the policy, and this is well past
it. **Repair:** either drop it, or keep it with an explicit note on why an
older event remains relevant.

**13.** *"WidgetWare typically delivers a 30% reduction in unplanned
downtime for manufacturers of Rockwell's scale."*
→ ❌ `fact` / `unsupported`. Nothing in `proof-points.yaml` supports it.
This is Chapter 10.1's opening example, and the correct response is
**deletion, not hedging** (Chapter 10.8). "May help reduce downtime" is the
same misrepresentation with a modal verb attached.

**14.** *"Rockwell is likely to be receptive to outreach."*
→ ❌ `inference` / `unsupported`. Wishful reasoning with no premise. There
is no source and no cited fact it follows from. **Repair:** none — remove
it. Not every claim has a valid form.

**15.** *"Rockwell operates in industrial automation."* No source recorded.
→ ❌ Rejected by *"claim has no source"* — even though the statement is
true and claim 1 establishes it. **The policy checks provenance, not
truth.** An unsourced true claim is indistinguishable at the boundary from
an unsourced false one, and a system that lets true-sounding claims through
unsourced has no policy at all.

Claim 15 is the one worth sitting with. It feels pedantic and it is the
whole discipline.

## C.4 The distinctions people get wrong

**Confidence is not `support_type`.** `confidence: 0.9` on an
`unsupported` claim means the model is very sure about something nothing
backs. That combination is a red flag, not a strong claim — and it is why
collapsing both dimensions into one confidence float (Chapter 3.8) destroys
the information needed to catch it.

**`derived` is not weaker than `direct`.** It says *how the claim was
reached*, not how good it is. Claim 3 is derived and about as certain as
anything in the corpus.

**A `hypothesis` is not a hedge.** It is a proposition someone will test in
a conversation. Rewriting a rejected `fact` as a hypothesis to sneak it past
the policy — claim 13 becoming *"we hypothesise 30% downtime reduction"* —
is laundering, and Chapter 12's prohibited-claims assertion catches it.

**Our own claims need sources too.** Claim 8 is about WidgetWare and still
carries a citation. Chapter 10 exists because V5 treated the product as
common knowledge.

## C.5 Classifying, as a procedure

The `evidence-classification` Skill (Chapter 7) implements this:

1. What is being asserted? State it in one sentence.
2. Does a source say this, in these or equivalent words? → `direct`.
3. Does it follow from cited sources by a stated step? → `derived`.
4. Neither? → `unsupported`.
5. Is it verifiable as stated (`fact`), reasoned from facts
   (`inference`), or speculative (`hypothesis`)?
6. Check the grid in §C.2. If rejected, repair or remove.
7. Check `rejection_conditions` for the specific rules — personnel,
   implied contact, staleness.

Step 1 is the one people skip, and it is where most misclassification comes
from: a sentence asserting two things at once gets one label, and the
weaker half rides along on the stronger half's citation.

## C.6 Where this is enforced

| Stage | Chapter | What happens |
|---|---|---|
| Classification | 7 | The Skill assigns both dimensions |
| Type validation | 8 | `EvidenceItem` requires both fields |
| Provenance capture | 9 | Source and retrieval method recorded at the MCP boundary |
| Grounding | 10 | Product claims resolved against the corpus |
| Verification | 11 | `verify_evidence` node applies `rejection_conditions` |
| Detection | 12 | Prohibited claims asserted across the golden set |
| Preservation | 13 | Revisions may not introduce unsourced claims |

Seven chapters touch this policy. It is the most load-bearing file in the
repository, which is why Chapter 3.8 introduces it before any code exists.
