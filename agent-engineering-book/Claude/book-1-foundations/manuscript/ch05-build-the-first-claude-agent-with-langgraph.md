# Chapter 5 — Build the First Claude Agent with LangGraph

> **Status: outline.** Structure, decisions and alternatives are settled;
> prose and code walkthrough to be written.

**Starting point:** V0 — specification and harness
**Result:** V1 — one bounded agent, deliberately monolithic

---

## 5.1 Current state and observed limitation

V0 has a specification, a proven environment and no agent. The limitation is
epistemic rather than technical: **we do not know what a language model does
with these tools and this instruction.** Every architectural decision from
here — decomposition, contracts, retrieval — would be a guess made against
imagined failures.

Chapter 2's method starts with Observe. There is nothing to observe.

## 5.2 Engineering question

> What does the simplest capable agent actually produce for a real company,
> and how does it fail?

## 5.3 Architectural decision

Build one LangGraph `StateGraph` with two nodes — an agent node that calls
Claude with bound tools, and a tool node that executes what it asked for —
joined by a conditional edge that loops until the model stops requesting
tools.

The prompt is deliberately broad: research, qualification and drafting in one
instruction. **The monolith is the experiment, not a strawman.** Many teams
ship exactly this, it genuinely works, and its specific failures are what
earn every later version.

## 5.4 Alternatives considered

**A direct Messages API loop with no framework.** Fewer moving parts, and
honestly a fine way to build V1. Rejected because Chapter 11 would then
require replacing the runtime *and* decomposing the responsibilities in one
step, and the reader would be unable to tell which change produced which
improvement. Adopting LangGraph at V1 with a two-node graph costs almost
nothing and makes every later change additive.

**`create_agent` from `langchain.agents`.** One line instead of twenty.
Rejected on two grounds. It is a constructor, not a graph you assembled, and
a reader cannot reason about control flow they did not write — by Chapter 11
they would be modifying a structure they never understood. Separately,
ADR-000 records the `langgraph` / `langgraph-prebuilt` version coupling that
broke installs; taking no dependency on the prebuilt package avoids it.

**Three agents from the start** — researcher, qualifier, writer. Rejected as
a Chapter 2 violation: no observation yet justifies decomposition, and
starting decomposed means never learning why decomposition is worth its
cost.

## 5.5 Trade-offs

A two-node graph is more ceremony than a `while` loop for what V1 does. The
payment comes at Chapter 11, and a reader who stops at Chapter 5 will
reasonably feel over-served.

The broad prompt will produce results good enough to be tempting. Resist
shipping it — Chapters 6 through 9 exist because of what it does when
nobody is watching.

## 5.6 Architecture before and after

```text
Before:  (nothing)

After:   START → agent ⇄ tools → END
                    │
                    └─ conditional: tool call pending? tools : END
```

## 5.7 Implementation walkthrough

- `app/graph/state.py` — `SDRState(TypedDict)`: `messages` with the
  `add_messages` reducer, plus `account`, `brief`. First encounter with
  reducers: why `messages` accumulates and `account` overwrites.
- `app/nodes/agent.py` — builds `ChatAnthropic` from `Settings`, binds
  tools, returns `{"messages": [response]}`. No model id appears here; the
  V0 test enforces that.
- `app/tools/fetch_webpage.py`, `search_company_news.py` — every tool
  declares purpose, typed input, typed output, read/write class,
  authorization, failure modes, timeout and audit requirement. The
  declaration format introduced here is used for every tool in the book.
- `app/graph/build.py` — `StateGraph`, `add_node`, `add_conditional_edges`,
  `compile(checkpointer=InMemorySaver())`.

Offline by default: both tools resolve from `data/fixtures/` unless a live
flag is set, so the suite runs with no network.

## 5.8 The inner loop, named

The agent ⇄ tools cycle *is* the agent loop from Chapter 1's definition —
decide, act, observe, repeat. Naming it here matters because Chapter 13 adds
a second, outer loop, and readers who never learned to distinguish them will
conflate the two.

## 5.9 Tests and evaluation

Offline: the graph compiles; the conditional edge routes to `tools` when a
tool call is pending and to `END` otherwise, driven by a fake model; the
tool node executes and appends a tool message; the account set loads.

Live (`@pytest.mark.live`, deselected by default): one real run against
Rockwell Automation producing a brief.

## 5.10 Failure demonstration

Run V1 against three accounts and read the output carefully. Expect, and
record:

- claims with no source, stated as confidently as sourced ones;
- the ICP applied differently across accounts — different criteria weighted
  each time;
- a single opaque span: no way to say which responsibility consumed the
  time or produced the error;
- fetched page content treated as instruction rather than data.

Each becomes a later chapter's opening observation.

## 5.11 Evidence of improvement

There is no previous version to improve on. V1's deliverable is the
**baseline report** at `evals/baselines/v1.md`: what it produced per
account, model call count, token usage, elapsed time, and the four failure
classes above with examples.

## 5.12 Updated run manifest

`version_tag: "v1-monolith"`, plus per-run model call count and token usage.

## 5.13 What remains unresolved

The agent read a webpage and believed it. Nothing distinguishes text we
wrote from text it retrieved, and nothing constrains what a tool can do
regardless of what the model was persuaded to ask for.

## 5.14 Exercises

1. Add a third tool the agent does not need. Run again. Did it call it? What
   does that tell you about tool descriptions as an interface?
2. Change one sentence of the system prompt and re-run the same account.
   Compare the two briefs. How much of what you thought was capability was
   phrasing?
