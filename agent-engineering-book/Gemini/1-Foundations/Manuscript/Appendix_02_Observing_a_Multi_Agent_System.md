# Appendix 02: Observing a Multi-Agent System

## What this appendix is

A field guide to reading the telemetry a multi-agent system produces — first from
an agent running on your own machine, then from the same agent deployed to
Google's Agent Platform.

Every number in this appendix was measured, not estimated. The subject is the
Class 02C movie-pitch application: a greeter hands off to a sequential team, a
bounded loop of researcher → screenwriter → critic drafts a plot, two agents
research box office and casting in parallel, and a file writer assembles the
pitch. It is small enough to hold in your head and rich enough that its trace
contains every shape you will meet in a real system.

The lessons transfer. The specific span names do not.

---

## A2.1 An event is not a span

The first confusion to clear up, because two different things both look like
"the list of what happened".

| | ADK Event | OpenTelemetry span |
|---|---|---|
| Produced by | the agent runtime | instrumentation |
| Represents | a unit of conversation or state change | a timed operation |
| Carries duration | **no** | yes |
| Carries parentage | ordering only | explicit parent |
| Where it lives | the session store | the trace backend |

One run of the movie-pitch application produced **22 ADK Events and 42 spans**.
Neither number is wrong. They are answers to different questions: the events say
*what the agents said and changed*, the spans say *what executed, nested inside
what, for how long*.

Keep the distinction sharp, because the most valuable finding in this appendix
comes from the gap between them.

---

## A2.2 Reading a local trace

The application ran with ADK's native OpenTelemetry export enabled, sending spans
straight to Cloud Trace with no collector in between.

### The shape

```text
invocation                                1m 5.111s
└── invoke_agent greeter                      1.562s
└── invoke_agent film_concept_team         1m 3.545s
    ├── invoke_agent writers_room             29.097s
    │   ├── invoke_agent researcher            7.578s
    │   │   └── execute_tool wikipedia         2.612s
    │   ├── invoke_agent screenwriter         13.890s
    │   └── invoke_agent critic                7.628s
    │       └── execute_tool exit_loop       373.000µs
    ├── invoke_agent preproduction_team       16.865s
    │   ├── invoke_agent box_office_researcher 16.864s
    │   └── invoke_agent casting_agent        11.992s
    └── invoke_agent file_writer              17.583s
        └── execute_tool write_file             2.100ms
```

Three readings matter.

### Parallelism is proved by arithmetic, not by layout

`preproduction_team` took **16.865s**. Its two children took 16.864s and 11.992s.
Run sequentially they would total 28.856s. The parent equals the *longer* child,
which is what concurrency looks like in a trace. A timeline view renders this as
two overlapping bars; the numbers say it even without the picture.

### The expensive span is not the one you expect

`file_writer` was the slowest stage at 17.583s — yet `execute_tool write_file`,
the actual file write, took **2.1ms**. The remaining 17.581s was one model call
assembling the text. A reader who assumes I/O is slow and inference is fast will
misread this trace completely.

### A loop that never loops still teaches something

Across three runs the critic approved on its first pass every time, so
researcher → screenwriter → critic executed exactly once. The interesting
artifact is not repetition but the **`execute_tool exit_loop`** span: the trace
shows the loop's *exit decision* as a discrete event. A bounded loop that
finishes early looks identical to one that never iterated, unless you know to
look for the escape hatch firing.

---

## A2.3 What an event recording loses

ADK session events can be exported as JSONL — one event per line, portable,
inspectable without any backend. It is a genuinely useful artifact. It is also a
lossy one, and the loss is not obvious.

In the recording of the run above, the two parallel agents appear like this:

```text
17  1788149463.042542  critic                 functionResponse
18  1788149463.050171  box_office_researcher  text, state_delta
19  1788149463.102871  casting_agent          text, state_delta
20  1788149479.919916  file_writer            functionCall
```

Events 17, 18 and 19 span **8 milliseconds**. Then a **16.85 second gap** before
event 20, with nothing recorded inside it.

Compare that to the trace: `preproduction_team` took 16.865s. The recording
stamps the parallel branches at **fan-out**, not completion, so the 16.86s during
which both agents actually worked is invisible. A reader with only the JSONL
would conclude the parallel stage was instantaneous and that something
unexplained happened afterwards.

> **The rule.** An event log tells you what happened and in what order. Only a
> trace tells you how long anything took, or what ran at the same time.

### Replaying a recording

Those recorded events can be reconstructed as a fresh trace without re-running
the agent — no model calls, no tool execution, no side effects. It is a cheap way
to inspect a past run, and its limits are instructive.

| Live trace | Replay trace |
|---|---|
| 42 spans, nested four deep | 23 spans: one root, 22 flat children |
| 1m 5.111s of real time | ~20s, being 80s of recording at 4× speed |
| `invoke_agent`, `call_llm`, `execute_tool` | `replay.event.<author>` only |
| Full prompt text in attributes | `recorded.*` metadata only |
| Parallel branches overlap | Every child 1ms, no overlap |

The replay reproduces the *story* faithfully and the *physics* not at all. It
cannot show duration or concurrency, because the recording never held them.

There is a sharper point hiding here, worth raising with anyone who treats
telemetry as evidence: **a replay is fabricated telemetry that is
indistinguishable from the real thing to anyone reading the backend.** Writing
convincing spans requires only permission to write spans. What a trace proves
depends entirely on who you trust to have produced it.

---

## A2.4 Content capture: two systems, opposite defaults

This section exists because the intuitive assumption is wrong in both directions.

Running locally, ADK has **two independent content-capture switches**, and
setting the well-known one does not do what its name implies:

| Variable | Governs | Default |
|---|---|---|
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | the `gen_ai.*` semantic-convention attributes | — |
| `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` | ADK's own `gcp.vertex.agent.llm_request` / `llm_response` | **on** |

Set the first to `NO_CONTENT` and the `gen_ai.*` attributes hold only metadata —
model name, finish reason, token counts. Meanwhile the second, untouched and
enabled by default, puts the **complete system instruction, the entire
conversation history, every tool result, and the full model output** into span
attributes, readable by anyone with trace-read permission on the project.

ADK's own source is candid about it: *"By default some ADK spans include
attributes with potential PII data."*

Deployed to Agent Platform, the same application behaves oppositely. The Session
view reports **"Prompt-response content collection is not enabled"** and offers an
**Enable in Service configuration** button. Logs show `{"content":"<elided>"}`.

| | Local | Deployed |
|---|---|---|
| Default | captured | **not** captured |
| Control | environment variable | console toggle |
| Discoverability | read the source | the UI tells you |

Same code, opposite postures. If you learn observability on a laptop and deploy
without re-checking, you will be wrong about what is being recorded — and the
direction of the error depends on which one you learned first.

---

## A2.5 The deployed picture

Deploying the identical application to Agent Platform produces the same
underlying trace — the console even links out to Cloud Trace — but frames it
through three views, and adds one capability that does not exist upstream.

Two naming differences to expect: the root span is **`invoke_workflow greeter`**
rather than `invocation`, and very short spans are collapsed into
**`execute_tool (merged)`**.

### Session view

A session groups the traces belonging to one conversation, with total duration
and total GenAI tokens. The unit of analysis moves up from the request to the
conversation — which is the right altitude for questions like *what did this user
cost us* or *where did this conversation go wrong*.

### Trace view

The familiar span tree, Graph or Timeline. The parallel overlap survives intact:
`preproduction_team` 13.992s containing `box_office_researcher` 13.991s and
`casting_agent` 7.391s.

### Span view: per-agent cost attribution

This is the capability that does not exist in a general-purpose trace explorer.
Every span carries a **type** — `Invoke Agent`, `Agent to Model`, `Agent to Tool`,
or unset for runtime internals — and every `invoke_agent` span carries a **token
count that rolls up its subtree**:

```text
researcher      4,507 ┐
screenwriter   12,233 ├─→ writers_room        22,853 ┐
critic          6,113 ┘                              │
box_office      7,194 ┐                              ├─→ film_concept_team  60,698
casting         6,193 ┴─→ preproduction_team  13,387 │
file_writer                                  24,458 ┘
greeter           451
```

The arithmetic is exact. 4,507 + 12,233 + 6,113 = 22,853. 7,194 + 6,193 = 13,387.
22,853 + 13,387 + 24,458 = 60,698. Adding the greeter's 451 gives 61,149, matching
the session total.

---

## A2.6 Why the last agent costs the most

Expanding to individual model calls turns the cost table into a finding.

```text
researcher       390 → 1,853 → 2,264      (3 calls)
screenwriter           5,629 → 6,604
critic                         6,113
box_office                     7,194
casting                        6,193
file_writer           12,196 → 12,262
```

Token cost **grows monotonically with position in the workflow**. The researcher's
first call costs 390 tokens. The file writer's costs 12,262 — thirty times more,
to produce one file.

The file writer is not expensive because it does more. It is expensive because it
runs **last**, and the accumulated conversation is re-sent on every call. It pays
for everything upstream. This is the same span that took 17.5s while writing a
file in 2.1ms: by both measures the cheapest-sounding stage is the most costly
one.

Three consequences for anyone designing a multi-agent system:

1. **Cost is positional, not proportional to work.** Adding a trivial agent at
   the end of a long workflow is not cheap.
2. **Summarise at hand-off.** The researcher passes a summary rather than the raw
   Wikipedia article, which is why the loop stays affordable. Every stage that
   forwards raw context taxes every stage after it.
3. **Parallel branches do not accumulate from each other.** `box_office` (7,194)
   and `casting` (6,193) each carry the shared prefix but not one another's
   output. Fan-out limits context growth as well as latency.

None of this is visible in a latency waterfall. It needs per-agent token
attribution, which is precisely what the deployed Span view provides.

---

## A2.7 Field notes

Findings from getting all of the above working. Each cost real time to diagnose.

**The `wikipedia` package is rate-limited by its own User-Agent.** Version 1.4.0
sends a User-Agent every installation shares, and Wikimedia returns **HTTP 429**
with a `text/plain` body. The library then calls `.json()` on it, so the symptom
is `JSONDecodeError: Expecting value: line 1 column 1` — no mention of rate
limiting anywhere. Under ADK the exception ends the entire invocation. Calling
`wikipedia.set_user_agent()` with a descriptive string turns 429 into 200.

**LangChain's `handle_tool_error` does nothing under ADK.** `LangchainTool` calls
`tool._run()` directly, bypassing `BaseTool.run()` where that setting is honoured.
A tool that looks guarded is not.

**Metrics export needs `service.instance.id`.** The telemetry endpoint maps the
OTel Resource onto a `prometheus_target`, which requires an `instance` label.
Without it every metrics batch is rejected — `"prometheus_target resource type
must have an instance specified"` — while traces succeed, so the failure hides in
a scrolling server log.

**Hand-built OTel providers need the project on the Resource.** Setting
`GOOGLE_CLOUD_PROJECT` is not enough; the exporter reads `gcp.project_id` from the
Resource, and a batch without it is rejected with a bare `400 Bad Request`.

**Export failures are logged, not raised.** `BatchSpanProcessor` records a failed
export and returns normally, so a tool that only watches for exceptions will
report success while writing nothing. Any exporter wrapper should check and exit
non-zero.

**In a managed lab project, `gcloud services enable` may always fail** with
`UREQ_TOS_NOT_ACCEPTED`, because the account cannot accept the cloud terms of
service — while the services are already enabled. Check before enabling.

**Deployment specifics** for `adk deploy agent_engine`, all four required:

1. `requirements.txt` must exist **in the agent folder**; `pyproject.toml` is
   ignored, and a generated file will omit your tool dependencies.
2. `--temp_folder` must point outside the package, or staging recurses into
   itself until `File name too long`.
3. `--extra_packages` needs an absolute path, because the deploy changes its
   working directory.
4. Clear `.adk/` and `__pycache__` first — the dev artifact store holds previous
   outputs and would be uploaded.

**Filesystem writes do not survive deployment.** A tool writing to a path relative
to the source tree works locally and silently loses its output in a container.
Saving through the artifact service works in both places; keep the local file as a
best-effort convenience, not the destination.

---

## A2.8 A reading checklist

For any trace from a multi-agent system:

- [ ] Does the parent's duration equal the **sum** of its children, or the
      **longest**? That distinguishes sequential from parallel.
- [ ] Which **leaf** span is slowest? Parents inherit; only leaves tell you where
      time went.
- [ ] Where is the gap with no span inside it? That is either untraced work or
      genuine waiting.
- [ ] Did the loop iterate, or exit on the first pass? Look for the exit tool.
- [ ] Which agent consumed the most tokens, and is that because of what it does
      or because of **where it sits**?
- [ ] Is prompt content in the attributes — and did you intend it to be?
- [ ] Are you reading a real execution, or a reconstruction of one?
