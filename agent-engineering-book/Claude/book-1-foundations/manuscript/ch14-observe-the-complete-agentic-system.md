# Chapter 14 — Observe the Complete Agentic System

> **Status: outline.**

**Starting point:** V9 — bounded review loop
**Result:** V10 (part 1) — instrumented and inspectable

---

## 14.1 Current state and observed limitation

A V9 run takes ninety seconds and forty thousand tokens across a dozen model
calls, two MCP tools, a retrieval query and up to three review iterations.

Ask any of these and the system cannot answer:

- Where did the ninety seconds go?
- Which node produced this evidence item?
- Why was this account routed `INSUFFICIENT`?
- What happened on the run that failed last Tuesday?

Tests prove behaviour under conditions we anticipated. **Observability
explains behaviour under conditions we did not.**

## 14.2 Engineering question

> Can a run be explained after the fact by someone who was not watching it?

## 14.3 Architectural decision

Instrument with **OpenTelemetry** as the standard and send traces to
**Langfuse** as the backend and inspection interface.

**Content capture is disabled by default.** Sanitised capture is
demonstrated explicitly, as a deliberate act with visible redaction — never
as a default that silently records everything.

## 14.4 What gets a span

The full inventory: complete invocation; each graph node; each model call;
each tool call; each MCP call; retrieval; policy decisions; route decisions;
review iterations; exceptions.

Route and policy decisions are the ones usually missed, and the ones that
answer "why did it do that." A trace showing *what ran* without *why the
route went left* explains the mechanics and not the behaviour.

## 14.5 Correlation identifiers

One run touches several identifier spaces, and a trace is only useful if
they join:

| Identifier | Scope |
|---|---|
| `request_id` | one inbound request |
| `thread_id` | one LangGraph thread (Chapter 15) |
| `account_id` | the company being researched |
| `evidence_id` | one evidence item, back to its source |
| `trace_id` | the OpenTelemetry trace |

Every audit event carries enough of these to be joined to a trace. The
Chapter 6 audit log and the trace answer different questions — *what was
permitted* versus *what took how long* — and neither substitutes for the
other.

## 14.6 The content-capture problem

The section this chapter exists for.

**OpenTelemetry LLM instrumentation and Langfuse both capture prompt and
response bodies by default.** For this application that means prospect
research, retrieved passages, drafts, and anything a tool returned — sent to
a trace backend and retained.

That is how personal data about real people at real companies ends up in a
system nobody classified as holding personal data. It is not a hypothetical:
it is the default behaviour of the standard tooling.

The chapter therefore:

1. turns content capture **off** in the default configuration;
2. shows what a trace looks like without it — structure, timing, token
   counts, decisions, all present and sufficient for most debugging;
3. implements a redaction layer;
4. turns on **sanitised** capture explicitly, showing what is kept, what is
   dropped, and where the setting lives;
5. states plainly that secrets, full sensitive payloads and unrestricted
   prompt content are never captured, in any mode.

A reader should leave knowing that the default in their own stack is
probably on, and how to check.

## 14.7 Alternatives considered

**Prometheus, Grafana and Loki.** Excluded by the brief and correctly so:
three services to operate for metrics and logs, when the question at this
stage is causal explanation of a single run rather than aggregate
monitoring. That is a Book 4 concern.

**Langfuse SDK alone, without OpenTelemetry.** Fewer layers. Rejected —
instrumentation would be tied to one backend, and OTel is the standard the
rest of the industry's tooling speaks.

**`print` and structured logs only.** Rejected: logs record events, traces
record causality and duration. "Which node was slow" is a trace question and
logs answer it badly.

**Sampling traces.** Premature at this volume, and it would undermine the
chapter's point — an unsampled trace of every run is what makes
reconstruction possible.

## 14.8 Trade-offs

Instrumentation is code in every node, and it is code that adds no
capability. The discipline is to instrument at boundaries — node entry and
exit, tool calls, model calls — rather than sprinkling spans through logic.

Tracing adds latency and a service.

Content capture off by default costs debugging convenience. The chapter is
explicit that this is a trade, and that turning it on for a debugging
session is legitimate — as a decision, with an expiry.

## 14.9 Implementation walkthrough

- `app/observability/tracing.py` — OTel setup, OTLP exporter to Langfuse,
  resource attributes carrying app version and model id from the manifest.
- `app/observability/spans.py` — node, tool, model and decision span
  helpers; a decorator applied at node boundaries.
- `app/observability/redaction.py` — field-level redaction; allowlist of
  what may be captured when capture is on.
- `app/config.py` — `capture_content: Literal["off", "sanitized", "full"]`,
  defaulting to `"off"`; `"full"` is rejected outside `app_env="local"`.

## 14.10 Tests and evaluation

- Every node emits a span with the expected attributes.
- Route decisions appear as spans with the deciding values.
- With capture off, no span attribute contains prompt or document text —
  asserted by scanning exported spans against fixture content.
- Redaction removes secrets in sanitised mode.
- `capture_content="full"` outside a local environment raises.

That third test is the important one, and it is written to fail loudly if a
future dependency upgrade re-enables capture by default.

## 14.11 Failure demonstration

Take the account that fails in Chapter 12's evaluation. Reconstruct from the
trace alone — without re-running — which node produced the weak evidence,
how long each stage took, why the route went where it did, and how many
review iterations ran.

Then enable full capture in a non-local environment and show the refusal.

## 14.12 Evidence of improvement

A run is explainable from its trace. Per-node latency and token attribution
available for the first time — which is also the input a later book needs
before optimising anything.

## 14.13 Updated run manifest

`version_tag: "v10-observed"`, trace id, capture mode, Langfuse project.

## 14.14 What remains unresolved

Runs are explainable and still ephemeral. State dies with the process, an
interrupted run starts over, and the only way to run the system is `pytest`.

## 14.15 Exercises

1. Check the default content-capture setting of the tracing stack in a
   system you work on. Were you expecting that answer?
2. Add a span for a decision that is currently invisible. Does the trace now
   answer a question it could not before? If not, remove it — an
   uninformative span is noise with a cost.
