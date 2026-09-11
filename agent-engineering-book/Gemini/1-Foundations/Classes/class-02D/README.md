# Class 02D — Deploying to Agent Platform (planning notes)

> **Status: planning, not a student-facing lab.** Nothing here has been built or
> tested. This file records the scope, the decisions already taken, and the
> obstacles found while testing Class 02C on 2026-09-01, so none of it has to be
> rediscovered.

---

## Why this is a separate class

Class 02C runs ADK on the student's own machine and exports OpenTelemetry spans
to Cloud Trace. That is deliberate and it stays that way. But it means the whole
Agent Platform console — Agent Registry, Sessions services, Deployments, Memory
Bank, Evaluation — is empty for a 02C student, because every one of those pages
lists resources *deployed to* Agent Platform.

That console is where the industry conversation is, and students ask about it. It
deserves its own class rather than three tasks bolted onto a lab that already has
twelve.

---

## What 02D teaches

1. Deploy the Class 02C golden application to Agent Engine.
2. Read the same agent's telemetry from the **Agent Registry → Traces** tab
   (Session / Trace / Span views) rather than from Trace Explorer.
3. Use the managed **Sessions service** instead of a local SQLite file.
4. Compare local-versus-deployed observability: what each surface shows, what it
   hides, and which questions each one can answer.
5. **Diagnose a failed invocation from its spans alone** — see below.

The entry point is a single command:

```bash
adk deploy agent_engine \
  --project=<project> \
  --region=<region> \
  --display_name=<name> \
  --otel_to_cloud \
  <agent>
```

`--staging_bucket` is deprecated in ADK 2.6.0, so the old GCS setup step is gone.
`--session_service_uri agentengine://<id>` is what populates the managed Sessions
page.

---

## The failure-diagnosis exercise

This is the strongest exercise idea to come out of testing 02C, and it belongs
here rather than in 02C's Task 7.

**The idea.** Students spend the whole of 02C reading healthy traces. Reading a
*failed* trace is a different and more useful skill: find the invocation that
went wrong, follow the span tree to the failing leaf, and explain the failure
from the spans without reading application logs.

**Where it came from.** During 02C testing, one run died on a Wikipedia HTTP 429
and left five `Error`-status spans sitting beside two successful invocations in
the same project. Reading that trace against the healthy ones was more
instructive than any exercise in the lab.

**The problem to solve first.** That failure is no longer reproducible. 02C's
Wikipedia tool was hardened to catch the exception and return
`{"status": "unavailable", ...}`, so the tool now degrades gracefully and the
span carries **no error status at all**. The very fix that made 02C reliable
removed the failure this exercise depends on. Any induced failure must therefore
be deliberate and separate from the hardened tool.

**Candidate ways to induce a failure**, in order of preference:

| Method | How | Why it is good or bad |
|---|---|---|
| Invalid model name | `MODEL=gemini-does-not-exist` | One env var, no source edit, reversible, fails fast at `call_llm`. Best candidate. |
| Region without the model | `GOOGLE_CLOUD_LOCATION=<region lacking the model>` | Also one env var; produces a `NOT_FOUND` on the model call. Needs a region confirmed not to serve the model. |
| Revoked permission | remove `roles/aiplatform.user` | Realistic, but needs admin rights a student will not have in a lab project. |
| A deliberately failing tool | add a tool that raises | Fully reliable, but requires editing the golden source, which the course promises not to do. |

**Complication found 2026-09-01.** The deployed container has no `MODEL`
environment variable — `.env` is not deployed, so it falls through to the
`os.getenv("MODEL", "gemini-2.5-flash")` default. Inducing a bad model on a
*deployed* agent therefore requires `env_vars` in `.agent_engine_config.json`,
and whether Agent Platform honours that is **unverified**. Test the mechanism
locally first (it is free), then confirm it survives deployment.

Both preferred methods work through `.env` or a single-run override, which fits
how 02C already teaches `MODEL`. Whichever is chosen must be verified to produce
a genuine `Error` span status, not a silently handled result.

**Questions the exercise should ask.** Which span failed, and which succeeded
before it? What did the parent do when the child failed? How far up did the
failure propagate? What can you tell about the cause from the span alone, and
what needs the logs? Why did the agents that ran before the failure still leave
successful spans?

---

## Proven on 2026-09-01

A first deployment of the 02C golden application succeeded end to end from a
Qwiklabs student account, so the class is viable. What it took:

```bash
adk deploy agent_engine \
  --project="$PROJECT_ID" \
  --region=us-central1 \
  --display_name="Class 02C Movie Pitch" \
  --otel_to_cloud \
  --temp_folder /tmp/adk-deploy-02c \
  --extra_packages "$PWD/adk_multiagent_systems" \
  adk_multiagent_systems/workflow_agents
```

Four things are non-obvious and all four are required:

1. **`requirements.txt` must exist in the agent folder.** `adk deploy
   agent_engine` reads `adk_multiagent_systems/workflow_agents/requirements.txt`
   and ignores `pyproject.toml` entirely. With no such file ADK writes one
   containing only `google-adk`, and the container fails on the Wikipedia
   import. ADK appends its own pins to this file at deploy time, which is why it
   must stay out of `golden-source.sha256`.
2. **`--temp_folder` must point outside the package.** The deploy switches its
   working directory into `adk_multiagent_systems` and stages into a temp folder
   there by default; `--extra_packages` then copies that directory into itself,
   recursing until `[Errno 63] File name too long`.
3. **`--extra_packages` needs an absolute path**, because of that same working
   directory switch.
4. **Clean `.adk/` and `__pycache__` before deploying.** The dev artifact store
   under the agent folder holds the full text of previously generated pitches
   and would otherwise be uploaded.

Confirmed working in the deployed container: the `shared` package import, both
tool dependencies, the full sequential/loop/parallel workflow, and `write_file`
saving an artifact while its local-copy fallback logs and continues.

### Local versus deployed: the content-capture contrast

This is the strongest teaching material the deployment produced, and it settles
the open question at the end of this file.

| | Local (02C) | Deployed |
|---|---|---|
| Default | prompts and responses **captured** | **not** captured |
| Control | `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` env var | **Enable in Service configuration**, a console toggle |
| Discoverability | none; you have to read ADK's source | the Session view says so and offers the button |
| Logs | full text in span attributes | `{"content":"<elided>"}` |

Same application, opposite defaults. Build a task around toggling the service
configuration and re-running, so students see the Session conversation appear —
and ask them which default they would choose and for whom.

### What Agent Platform Traces adds over Trace Explorer

It is the **same trace data** — the detail pane carries a `View in Cloud Trace`
link. Confirmed identical in shape: 41 spans, the loop under `writers_room`, and
`preproduction_team` at 13.992s containing `box_office_researcher` 13.991s and
`casting_agent` 7.391s, so the parallel overlap is preserved.

What it adds is a layer *above* the trace, and one thing Trace Explorer cannot do
at all.

**Per-agent token attribution (Span view).** Every `invoke_agent` span carries a
token count, and the counts roll up the agent hierarchy exactly. Measured on the
first deployed run:

```text
researcher      4,507 ┐
screenwriter   12,233 ├─→ writers_room        22,853 ┐
critic          6,113 ┘                              │
box_office      7,194 ┐                              ├─→ film_concept_team  60,698
casting         6,193 ┴─→ preproduction_team  13,387 │
file_writer                                  24,458 ┘
greeter           451
```

4,507 + 12,233 + 6,113 = 22,853. 7,194 + 6,193 = 13,387. 22,853 + 13,387 +
24,458 = 60,698. With greeter, 61,149 — matching the session header.

**Build the cost lesson on `file_writer`.** It is the most expensive agent in the
application at 24,458 tokens, roughly 40% of the invocation and more than the
entire writers' room loop, despite running one model call and a 2ms file write.
It receives the plot outline and both reports and re-emits the whole pitch. This
also matches 02C's finding that `file_writer` was the slowest span. Students will
not predict this from the topology diagram, which is exactly why it is worth
asking them to.

**Why file_writer is expensive — the lesson to actually teach.** Span view with
"Show all types" gives per-call token counts, and they grow monotonically with
position in the workflow:

```text
researcher     390 -> 1,853 -> 2,264     (3 model calls)
screenwriter          5,629 -> 6,604
critic                         6,113
box_office                     7,194
casting                        6,193
file_writer          12,196 -> 12,262
```

Each `invoke_agent` rollup is the sum of its model calls (390 + 1,853 + 2,264 =
4,507 for the researcher). The accumulated conversation is re-sent on every call,
so `file_writer` is not expensive because it does more work — it is expensive
because it runs **last** and pays for everything upstream. This is invisible in
02C and is the single best argument for the class.

**A semantic type taxonomy** Cloud Trace does not have: `Invoke Agent`,
`Agent to Model`, `Agent to Tool`, and an unset type for ADK internals
(`call_llm`, `invoke_workflow`). Students can reason about span *kinds* instead
of pattern-matching on names.

**Input / Output columns** showing `<elided>` on exactly the `Agent to Model`
rows — a precise picture of where content would be captured if collection were
enabled, which sets up the Service configuration exercise above.

Also useful: a **Show only invoke agent type / Show all types** toggle, giving
agent-level filtering directly, where Cloud Trace requires ticking span-name
facets by hand.

Sessions additionally group traces, carry duration and token totals, and gain an
**Evaluation** tab. So 02D is about the session and the agent as units of
analysis — and about cost — not about re-teaching spans.

Naming differs from local and the instructions must say so:

- root span is `invoke_workflow greeter`, not `invocation`;
- very short spans are collapsed into `execute_tool (merged)`.

### Browsing deployed sessions in the ADK dev UI

`agentengine://` is a registered session-service scheme for the local CLI, so the
familiar dev UI — graph view, Events, State, Artifacts — can read the managed
sessions a deployed agent creates:

```bash
SESSION_SERVICE_URI=agentengine://<engine-id> ./class-02C-work/start_web_server.sh
```

Both 02C start scripts honour `SESSION_SERVICE_URI` for this. **Caveat to teach
explicitly:** sending a new message from that UI runs the *local* agent code
against remote session storage. It views the deployed agent's history; it does
not invoke the deployed container.

The CLI prints a `console.cloud.google.com/vertex-ai/agents/agent-engines/…`
link, but the live console is at `console.cloud.google.com/agent-platform/…`.
Use the latter in the instructions.

---

## Known obstacles

Recorded while testing 02C. None of these is solved.

1. ~~**`file_writer` writes to the local filesystem.**~~ Solved 2026-09-01:
   `write_file` now saves an ADK artifact and treats the local file as a
   best-effort extra. The same code works on a laptop and in the container.
   Original problem, for context: The golden application's
   final step writes `movie_pitches/<title>.txt`. On Agent Engine that lands in
   an ephemeral container and disappears, so the lab's tangible artifact is lost.
   Either the agent moves to the artifact service
   (`--artifact_service_uri gs://<bucket>`) or the deployed version has no
   visible output. **This is a design change, not a flag, and it gates whether a
   deployed agent is demonstrable at all.** Solve it before building anything
   else.

2. ~~Qwiklabs permissions are unverified.~~ Solved 2026-09-01: a student account
   created `reasoningEngines/1706835121715281920` in `us-central1`. It is still a
   billable resource that keeps running, so the class needs a teardown step.

   **Scaling decided 2026-09-01: each student deploys in their own project.** No
   shared quota, no naming collisions, and teardown is each student's own
   billing. Teardown is therefore mandatory in the instructions, not optional.

   Useful: `--agent_engine_id <id>` updates an existing instance in place, so
   exercises that redeploy do not leave a student with several live engines.

3. **Region.** Now handled: both 02C `.env` templates ship
   `GOOGLE_CLOUD_LOCATION=us-central1` as of 2026-09-01, because Agent Engine
   requires a real region and rejects `global`.

---

## Carried over from 02C

Fixes made in 02C that this class inherits and must not regress:

- `wikipedia.set_user_agent(...)` — the package default is rate-limited to HTTP
  429 by Wikimedia, which surfaces as a bare `JSONDecodeError`.
- `service.instance.id` in `OTEL_RESOURCE_ATTRIBUTES` — without it,
  `telemetry.googleapis.com` rejects every metrics batch with
  "prometheus_target resource type must have an instance specified".
- `get_gcp_resource(project_id)` must be passed explicitly when setting up OTel
  providers by hand; setting `GOOGLE_CLOUD_PROJECT` is not enough.
- `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` defaults **on** and is a separate knob
  from `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`. 02C leaves it on
  deliberately and teaches it. Decide whether a deployed agent should do the
  same — the exposure is larger when the agent is not on a student's laptop.


---

## Decided: no replay in 02D

Telemetry replay stays in 02C. It is not carried into this class.

**Why.** `replay_events.py` emits spans carrying only `recorded.*` attributes —
no token counts, no `Agent to Model` / `Agent to Tool` classification, no agent
hierarchy. In Span view every replayed row would show a blank Token usage and an
unset Type. The two capabilities that justify this class are precisely the two a
replay cannot reconstruct. There is also plumbing cost: `record_session.sh` curls
`localhost`, while deployed sessions live in the managed session service.

In 02C replay earns its place, because the contrast is live-versus-replay on one
surface and the payoff is discovering that `events.jsonl` stamps the parallel
branches at fan-out and loses 16.86s of real work.

**Carry over one idea, as discussion rather than a task.** Replay proves
telemetry can be *fabricated*: anyone with trace-write permission can inject
spans that look like agent activity. Under the governance pillar, beside "who may
enable prompt collection" and "who may read these traces", ask what a trace
actually proves and who must be trusted for it to prove anything.

**Unverified prediction worth a cheap check:** a replay trace writes service
`class-02c-replay` with no association to a reasoningEngine, so it should appear
in Trace Explorer but **not** in Agent Registry → Traces — reinforcing that
Agent Platform surfaces list deployed resources only.
