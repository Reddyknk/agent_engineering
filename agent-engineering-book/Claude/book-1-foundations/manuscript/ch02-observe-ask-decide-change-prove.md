# Chapter 2 — Observe, Ask, Decide, Change, Prove

## What this chapter establishes

The method every remaining chapter follows, and the evidence contract that
keeps it honest.

Chapter 1 ended on an unresolved question: what does it mean for a
capability to be *needed*? This chapter answers it, because without an
answer "add capability when needed" collapses into "add capability," which
is how agent systems become expensive, slow and unexplainable while
appearing to make progress.

---

## 2.1 The cycle

Every version of the system in this book is produced by one pass through
five steps.

> **Observe → Ask → Decide → Change → Prove**

**Observe.** Run the current version against the fixed account set. Look at
what it actually did, not what you think it does. Read the outputs. Read the
failures.

**Ask.** Name a specific weakness, and phrase it as an engineering question
about a missing capability — not a solution. "The system cannot tell me
which stage consumed the time" is a question. "We should add tracing" is a
solution wearing a question's clothes.

**Decide.** Choose the smallest change that answers the question. Record the
alternatives you considered and why you rejected them. This is the step
teams skip, and skipping it is why architectures accumulate technologies
nobody can justify a year later.

**Change.** Implement it. One capability per version.

**Prove.** Show the improvement with evidence: a passing test, a trace, an
evaluation score against the previous version. If you cannot prove it, you
have not finished — and you may have made things worse.

The cycle has a property worth stating explicitly: **it can conclude that a
change was not worth making.** A version that fails its proof step gets
reverted, and the book records that it was tried. An architecture where
every proposed addition was adopted is not an architecture that was
evaluated.

---

## 2.2 Why the order is what it is

The two most common inversions are worth naming.

**Deciding before observing.** You know LangGraph supports parallel
execution, so you parallelise. Later you discover the slow stage was a
single sequential database call and parallelism bought nothing. The
evidence was available before the work; you just did not look.

**Changing before asking.** Closely related and more subtle: you observe a
real problem, then immediately reach for the tool you already wanted to use.
The observation was genuine, the diagnosis was not. Forcing yourself to
phrase the question *as a capability gap* before choosing a mechanism is a
cheap defence.

There is a third, quieter one: **proving with the wrong evidence.** The
system feels better. The demo went well. A single account produced a nicer
draft. None of these are proof, because none of them would have detected a
regression on the other twelve accounts.

---

## 2.3 The evidence contract

For a comparison between two versions to mean anything, the things being
held constant have to actually be constant. This book fixes five:

**1. The account set.** The same thirteen companies in
`data/accounts.csv`, every version, unchanged. Adding an account changes
the score without changing the system.

**2. The output contract.** What a completed run produces — a company
profile, evidence items, a fit decision, a draft, a disposition. It gains
structure over time (Chapter 8 makes it typed) but never changes meaning.

**3. The evaluation dimensions.** The same questions asked of every
version: is the output structurally valid, is every factual claim sourced,
is the fit decision correct, is the draft free of unsupportable claims, did
the run terminate for a stated reason.

**4. The adversarial case.** At least one input designed to make the system
misbehave — a page containing an injected instruction. It appears in
Chapter 6 and is re-run against every version afterwards. A control that
worked in V2 and silently stopped working in V7 is worse than one that was
never built, because you believed you had it.

**5. The reproduction record.** `RUN_MANIFEST.json`: application version,
model identifier and parameters, pinned dependency versions, dataset
version, and from Chapter 7 the content hashes of the skills that ran. A
result you cannot attribute to specific inputs is an anecdote.

---

## 2.4 What counts as proof

Four kinds of evidence, in ascending order of cost and descending order of
frequency.

**A deterministic test.** Fastest and most reliable. Does the output
validate against the schema? Was the prohibited tool refused? Did the loop
stop at the configured limit? Most proofs in this book are of this kind,
and you should prefer them wherever the question can be phrased to admit
one.

**A trace.** Answers "where did the time and the tokens go" and "which
stage produced this." Chapter 14.

**A rubric evaluation.** For questions with no deterministic answer: is
this draft any good? A model judges against a written rubric, on a fixed
set of cases. Noisier than a test, and the only tool available for
questions of quality. Chapter 12 keeps deterministic assertions and rubric
judgements strictly separated, because averaging them produces a number
that means nothing.

**A human review.** The most expensive and the final word. Reserved for
whether the *product* is right, not whether the code works.

A claim proved by none of these is a claim this book does not make.

---

## 2.5 One capability per version

Thirteen versions could have been three. The book uses eleven (V0 through
V10) because each one isolates a single variable.

When V6 adds retrieval and the evaluation scores move, the movement is
attributable to retrieval. If V6 had added retrieval, typed contracts and a
graph together, the scores would still have moved and you would have learned
nothing about which change caused it — or worse, you would have learned that
the bundle helped while one of its three parts quietly made things worse.

This is slower to read and slower to build. It is also the only way the
word *prove* in the cycle name means anything.

A practical consequence: **the early versions are deliberately inadequate.**
The Chapter 5 agent is one broad prompt doing three jobs. It is not a
strawman — it is a real, working, genuinely useful system, and many teams
ship exactly it. It is also the version whose specific, observed failures
justify everything that follows. Watching it fail is the point.

---

## 2.6 The version ladder

| Version | Chapter | Capability added | The question it answers |
|:---:|:---:|---|---|
| V0 | 3–4 | Scope, boundary, harness, manifest | Can we build and measure anything at all? |
| V1 | 5 | One LangGraph agent | What does the naive version actually do? |
| V2 | 6 | Trust boundaries and policy | Can prohibited behaviour be blocked? |
| V3 | 7 | Agent Skills | Is judgment applied the same way every time? |
| V4 | 8 | Typed contracts | Can another system act on the output? |
| V5 | 9 | MCP integration | Can capabilities live outside the application? |
| V6 | 10 | RAG and grounding | Are our own product claims supportable? |
| V7 | 11 | Explicit workflow | Can we locate the responsibility that failed? |
| V8 | 12 | Evaluation gates | Is V7 actually better than V1? |
| V9 | 13 | Bounded review loop | Can quality improve without running forever? |
| V10 | 14–15 | Observability and packaging | Can we explain and reproduce a run? |

Two orderings in that table are deliberate and worth defending, because
both invert what a reader might expect.

**Evaluation (V8) comes after the graph (V7), not before.** You cannot
build a meaningful evaluation suite against a system whose stages are not
yet nameable. V7 creates the vocabulary — research, qualification,
drafting, review — that V8's dimensions are expressed in. The cost is that
V1 through V7 are proved by tests and inspection rather than scores, which
is honest about what those versions can support.

**Observability (V10) comes near the end, and the loop (V9) before it.**
This may look backwards: shouldn't you observe before you optimise? Yes —
and Book 1 does not optimise. Cost and latency work is deliberately out of
scope here, which removes the usual reason to front-load tracing. What V10's
traces are for is *explanation and reproduction*, which is a packaging
concern, and packaging comes last.

---

## 2.7 What this method costs

Honesty requires stating the downsides.

**It is slow.** Eleven versions with a proof step each is more work than
building the final architecture directly. If you already know the answer —
you have built this system three times before — the ceremony buys you
little.

**It can overfit to the evidence.** Optimising against thirteen accounts
and one adversarial case risks a system that is excellent on exactly those
and mediocre elsewhere. The defence is to treat the evaluation set as a
regression guard rather than a target, and to refresh it when the product
changes. This book cannot fully escape the problem, and you should not
believe anyone who claims their method does.

**It biases toward incrementalism.** Small justified steps rarely arrive at
an architecture that would have required a large jump. Some redesigns are
not reachable by local improvement. When the cycle keeps producing marginal
gains against a persistent problem, that is the signal to step back and
question the shape rather than continue climbing.

---

## 2.8 Exercises

1. Take a change made recently in a system you work on. Reconstruct it as
   Observe → Ask → Decide → Change → Prove. Which steps actually happened?
   The missing one is usually Decide or Prove.

2. For a system you maintain, write its evidence contract: what is held
   constant when you compare two versions? If nothing is, you have no way
   to know whether last quarter's work helped.

3. Phrase this as a capability question rather than a solution: *"our agent
   sometimes produces briefs with claims that aren't in any source."*
   Then list two mechanisms that could answer it and what would distinguish
   them.

---

## What remains unresolved

We have a method but nothing to apply it to. Applying Observe first
requires something to observe, and building something requires knowing what
it is for, who uses it, what it may not do, and how we will know if it is
working.

Chapter 3 answers those, and produces V0's specification.
