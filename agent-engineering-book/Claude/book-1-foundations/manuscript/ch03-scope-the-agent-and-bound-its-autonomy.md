# Chapter 3 — Scope the Agent and Bound Its Autonomy

**Starting point:** nothing
**Result:** V0 — a specification and a bounded problem

---

## 3.1 Current state and observed limitation

There is no system. The limitation is that we cannot begin: "build an agent
that helps with sales development" does not constrain anything. It does not
say who uses the output, what a good result looks like, what the system is
forbidden to do, or how we would know it was working.

Starting to build here is the most common way agent projects go wrong. Not
because the code is bad — because six weeks in, nobody can answer whether
the thing works, and there is no shared definition of *works* to appeal to.

## 3.2 Engineering question

> What is this system for, who is accountable for its output, and what must
> it never be able to do?

## 3.3 Architectural decision

Write the specification as **data in the repository**, not prose in a
document, and make the autonomy boundary **structural rather than
configured**.

Two parts, both deliberate.

**Specification as data.** The ideal customer profile, product offering,
proof points and voice go in `config/` as YAML with JSON Schemas attached.
They are business decisions, they change on a different cadence from the
code, and the people who own them do not read Python. Putting them in a
prompt string makes them invisible to their owners and untestable by us.

**Boundary as structure.** The system must never contact a prospect. The
weak way to guarantee that is a configuration flag. The strong way is to
never build the capability, and to add a test that fails if anyone does.

## 3.4 Alternatives considered

**Specification in the system prompt.** Simplest, and what most tutorials
do. Rejected: an ICP buried in a prompt cannot be reviewed by the sales
lead who owns it, cannot be versioned independently, and cannot be
validated. When it drifts from what the business actually targets — and it
will — nothing detects the drift.

**Boundary as a feature flag (`ALLOW_SEND=false`).** Rejected. A flag
guarantees nothing about a system under development by several people over
several months. It can be flipped in an environment file, defaulted wrong in
a new deployment, or bypassed by a code path added later. The absence of a
capability cannot be flipped.

**Boundary as a policy check before sending.** Better than a flag, and what
you would build if sending were genuinely required. Rejected here because it
is strictly more machinery to protect against a risk we can eliminate by
construction. Chapter 6 builds policy enforcement for the actions that *do*
exist.

**No explicit SLOs at V0.** Tempting — there is no system to measure. But
service level objectives written after you have performance data are
written to match the data. Writing them now, from what the business needs,
means Chapter 14 can report whether we met them rather than describing what
we achieved.

## 3.5 Trade-offs

Making the boundary structural costs us the ability to demonstrate a
complete send-and-approve flow, which is a real pedagogical loss — human
approval of a consequential action is an important pattern, and we can only
show its shape (Chapter 13's escalation path) rather than the thing itself.

We accept it because a book whose example repository contains working
outbound-messaging code is a book whose readers will run that code.

Specification-as-data costs indirection: a reader tracing why the agent
disqualified a company has to open a YAML file rather than read the prompt.
That is the correct trade — the alternative hides a business rule inside an
implementation detail.

## 3.6 The specification

### Users and accountability

| Role | Uses the system to | Accountable for |
|---|---|---|
| Sales development representative | Get a researched account package instead of doing the research | The decision to act on it; every message actually sent |
| Sales lead | Define and adjust the ICP, offering and proof points | Whether the targeting is right |
| Agent engineer | Build, evaluate and operate the system | Whether it does what it claims, and whether that is measurable |

The accountability column is the important one. The system produces a
recommendation. A person is accountable for every consequence. No output of
this system reaches a prospect without a human having read it — and in Book
1, without a human having copied it out by hand.

### Desired outcomes

1. A representative spends less time on research and more on conversations.
2. Every claim in a brief is traceable to a source that can be re-checked.
3. Fit decisions are consistent — the same company assessed twice gets the
   same answer for the same reasons.
4. A weak or unsupportable brief is flagged by the system, not discovered by
   the representative.

Note what is absent: no outcome mentions volume. A system that produces
forty briefs an hour that nobody trusts has negative value.

### The autonomy boundary

The system **may**:
read public web pages; search public news; read `config/` and the product
corpus; compute a fit assessment; draft a message; review and revise its own
draft; write briefs and drafts to local storage; record audit events;
escalate to a human.

The system **may not**:
send email or any external message; write to a CRM or any external system of
record; contact a person by any channel; spend money; act on any account not
explicitly supplied to it.

The second list is enforced by there being no code that could do any of it.
`tests/test_v0_harness.py::test_no_send_capability_exists_anywhere` scans
the application for outbound-messaging imports and fails if it finds one.

That test is a blunt instrument — it catches `smtplib` and `twilio`, not a
determined author using `httpx` against a mail API. It is not a security
control and Chapter 6 does not treat it as one. It is a **tripwire against
drift**, which is the realistic threat: not sabotage, but a well-meaning
contributor in month four adding a send tool because it seemed like the
obvious next feature.

### Risks

| Risk | Consequence | Where addressed |
|---|---|---|
| Fabricated facts about a prospect | Embarrassing or damaging outreach | Ch. 9, 10 — sourced evidence |
| Unsupportable claims about WidgetWare | Misrepresentation | Ch. 10 — grounded product knowledge |
| Injected instructions in fetched content | Agent manipulated by its input | Ch. 6, 12 — tool policy, adversarial tests |
| Inconsistent fit decisions | Targeting nobody can rely on | Ch. 7 — skills |
| Unbounded retry | Cost with no ceiling | Ch. 13 — bounded loop |
| Stale evidence presented as current | Outreach referencing dead news | Ch. 9 — freshness in the evidence record |
| Silent quality decline | Trust erodes before anyone measures | Ch. 12 — regression evaluation |

### Success metrics and initial SLOs

Written now, from business need, before any measurement exists.

| Metric | Target | Measured by |
|---|---|---|
| Brief structural validity | 100% | Schema validation (Ch. 8) |
| Factual claims carrying a resolvable source | 100% | Evidence policy check (Ch. 9) |
| Fit decisions matching human judgment | ≥ 85% | Golden dataset (Ch. 12) |
| Drafts containing a prohibited claim | 0% | Deterministic assertion (Ch. 12) |
| Runs terminating with a recorded stop reason | 100% | Loop instrumentation (Ch. 13) |
| End-to-end latency per account, p95 | ≤ 90 s | Traces (Ch. 14) |

Two of these are absolutes. 100% structural validity and 0% prohibited
claims are achievable because both are deterministically checkable and
enforceable at a boundary — the system can refuse to emit an invalid brief.
The 85% fit-decision target is not an absolute because human judgment is
itself inconsistent, and a target of 100% would be a target to overfit to.

The latency figure is a placeholder pending real data, and Chapter 14 will
say whether it was reasonable. Recording it now means we find out; setting
it in Chapter 14 would mean setting it to whatever we got.

### Unit-cost assumptions

Recorded now so Chapter 14's measurements can be compared against an
expectation rather than merely reported.

Assume, per account, roughly: three to six model calls, three to eight
thousand input tokens and one to two thousand output tokens per call, one to
three web fetches. At current pricing this is small change per account — a
few cents — and the reason to track it is not the per-account cost but the
shape: if a version triples the call count, that shows up in the manifest
before it shows up in a bill.

Book 1 does not optimise cost. It records it so that a later book can.

## 3.7 What V0 produces

No agent. Four things:

1. `config/icp.yaml`, `offering.yaml`, `proof-points.yaml`, `voice.yaml`
   with schemas — the business specification as validated data.
2. `app/contracts/evidence-policy.yaml` — the evidence rules, discussed
   below.
3. `data/accounts.csv` — the thirteen-account comparison set.
4. The autonomy boundary, enforced by a test.

Chapter 4 adds the harness that runs and proves them.

## 3.8 The evidence policy, and why it has two dimensions

Read `app/contracts/evidence-policy.yaml` before continuing. It is the
single most consequential file in the repository, and it makes a
distinction most systems miss.

Every factual claim carries both:

- **`claim_type`** — the *epistemic status* of the statement.
  `fact` (directly verifiable as stated), `inference` (reasoned from facts,
  not asserted by any source), or `hypothesis` (a proposition worth testing).
- **`support_type`** — how strongly the cited evidence *backs it*.
  `direct` (the source says this), `derived` (the source supports it via a
  step of reasoning), or `unsupported` (nothing cited establishes it).

These are independent, and the independence is the point. A hypothesis can
rest on directly-stated facts and remain a hypothesis. A fact can be
badly under-evidenced. The common design — one `confidence: 0.8` float —
collapses both into a number that cannot distinguish *"a well-sourced
guess"* from *"a poorly-sourced certainty."* Those two failures need
different responses: the first is fine to show a human with a caveat, the
second must not reach the output at all.

Every version from Chapter 6 onward depends on the split holding, and a test
asserts it does.

## 3.9 Evidence of completion

```bash
uv run pytest -k "domain_config or evidence_policy or account_set or send_capability"
```

Passing means: the specification parses, every config has a schema, the
evidence policy keeps its two dimensions separate, the account set is usable
as a fixed comparison basis, and no outbound-messaging capability exists.

## 3.10 Updated run manifest

`RUN_MANIFEST.json` gains its `autonomy_boundary` block, recording
`external_send_enabled: false` — with a note stating plainly that the
manifest *records* the boundary and does not enforce it. The enforcement is
the absence of the tool. A manifest that implied otherwise would be
documentation that lies.

## 3.11 What remains unresolved

We have a specification and no way to run anything. There is no environment,
no test harness anyone else can reproduce, and no way to record what
produced a result.

Chapter 4 builds all three, and proves them before there is an agent.

## 3.12 Exercise

Write the autonomy boundary for a system you would actually build — the two
lists, *may* and *may not*. Then, for each item on the *may not* list, ask:
is this enforced by structure, by policy, or by hope? Move at least one item
from hope to structure.
