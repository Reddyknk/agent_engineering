# Class 02D — Deploy an ADK Agent and Read Its Telemetry on Agent Platform

> **Draft.** Tasks 9, 10 and 12 are marked **UNVERIFIED** where the behaviour has
> not yet been tested end to end. Everything else was measured on a real
> deployment on 1 September 2026. Do not run this with a class until the marked
> tasks are confirmed.

## Purpose

Class 02C ran a multi-agent application on your own machine and exported its
OpenTelemetry spans to Cloud Trace. This class deploys **the same application,
unchanged**, to Google's Agent Platform, and reads its telemetry from the surface
built for deployed agents.

The point is not that deployment is difficult. It is that a deployed agent can be
asked questions a local one cannot:

1. **What does each agent cost?** Not the invocation — each agent, individually.
2. **Who decides what gets recorded?** Local and deployed default in opposite
   directions.
3. **What happened when it broke?** Reading a failed trace is a different skill
   from reading a healthy one.

By the end you can deploy an ADK agent, attribute token cost per agent, explain
why cost grows through a workflow, govern content capture deliberately, diagnose
a failed invocation from spans, and tear the deployment down.

---

## What you need before starting

**You do not download a new package.** This class uses the Class 02C package.

- The extracted `class-02C` directory with its `.venv` and a working `.env`.
- `GOOGLE_CLOUD_LOCATION=us-central1` in that `.env`. Agent Engine rejects
  `global`. The 02C template already ships `us-central1`.
- **Your own Google Cloud project**, with billing you control. Every student
  deploys into their own project. A deployment is a running, billable resource,
  and Task 12 removes it.

If you have not done 02C, download `class-02C.zip` from `Classes/class-02C/` and
complete its Tasks 1 and 2 (install and authentication) before continuing.

---

## Learning objectives

By the end of this lab you can:

- deploy an ADK agent to Agent Platform with `adk deploy agent_engine`;
- explain the four packaging requirements that are not obvious from the command;
- navigate the Session, Trace and Span views and say what each answers;
- read per-agent token attribution and explain why it rolls up;
- explain why cost grows with position in a workflow, and what to do about it;
- compare local and deployed defaults for prompt-content capture, and choose;
- diagnose a failed invocation from its spans; and
- tear down a deployment and confirm it is gone.

---

## Task 1 — Confirm your package is deployment-ready

The 02C package ships ready to deploy. Check three things:

```bash
cd class-02C
source .venv/bin/activate
cat adk_multiagent_systems/workflow_agents/requirements.txt
grep GOOGLE_CLOUD_LOCATION .env
grep -n "save_artifact" adk_multiagent_systems/workflow_agents/agent.py
```

You should see the tool dependencies listed, `us-central1`, and a
`save_artifact` call in `write_file`.

Each of those exists for a reason you will meet in Task 3.

---

## Task 2 — Confirm you can reach Agent Platform

```bash
export PROJECT_ID=your_project_id
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/us-central1/reasoningEngines"
```

`200` means the API is reachable and you can list deployments. A `403` means your
account lacks Agent Platform permissions; stop and resolve that first.

> **Naming note.** Vertex AI was renamed the **Gemini Enterprise Agent Platform**
> in 2026. The API is still `aiplatform.googleapis.com` and the environment
> variable is still `GOOGLE_GENAI_USE_VERTEXAI`, but the console says Agent
> Platform. Both names refer to the same product.

---

## Task 3 — Deploy

```bash
adk deploy agent_engine \
  --project="$PROJECT_ID" \
  --region=us-central1 \
  --display_name="Class 02D Movie Pitch" \
  --otel_to_cloud \
  --temp_folder /tmp/adk-deploy-02d \
  --extra_packages "$PWD/adk_multiagent_systems" \
  adk_multiagent_systems/workflow_agents
```

This takes several minutes and builds a container. Expected final output:

```text
Created a new instance: projects/<number>/locations/us-central1/reasoningEngines/<id>
Deployed to Agent Platform: projects/<number>/locations/us-central1/reasoningEngines/<id>
```

**Record the numeric engine ID. You need it in Tasks 11 and 12.**

```bash
export ENGINE_ID=paste_the_numeric_id_here
```

### Four requirements, none of them obvious

| Requirement | What happens without it |
|---|---|
| `requirements.txt` **in the agent folder** | `pyproject.toml` is ignored. ADK generates a file containing only `google-adk`, and the container fails on the Wikipedia import. |
| `--temp_folder` **outside the package** | Deploy switches its working directory into the package and stages there; `--extra_packages` then copies that directory into itself until `[Errno 63] File name too long`. |
| `--extra_packages` as an **absolute path** | Same working-directory switch resolves a relative path one level too deep. |
| Clear `.adk/` and `__pycache__` first | The dev artifact store holds previously generated pitches and would be uploaded. |

```bash
rm -rf adk_multiagent_systems/workflow_agents/.adk
find adk_multiagent_systems -name __pycache__ -type d -exec rm -rf {} +
```

### Why `write_file` still works

The deployed container's filesystem is ephemeral, and the path `write_file` used
in 02C does not resolve the same way inside it. The tool saves an **artifact**
and treats the local file as a best-effort extra, so the same code works in both
places. A tool that writes only to disk would appear to succeed and silently lose
its output.

---

## Task 4 — Run the deployed agent

Open the deployment in the console:

**Agent Platform → Deployments → Class 02D Movie Pitch → Playground**

Send `Hello`, then a historical figure. The full workflow runs — greeter,
research, the writers' room loop, the parallel preproduction pair, and the file
writer — exactly as it did locally.

Confirm the final response names a saved pitch file.

---

## Task 5 — Session view

**Traces → Session view.** Open your session.

A session groups every trace belonging to one conversation and carries total
duration and total GenAI tokens. Record:

| | Value |
|---|---|
| Session ID | |
| Duration | |
| Traces in session | |
| Tokens in / out | |

The unit of analysis has moved up. In 02C you asked *how long did this request
take*. Here you can ask *what did this conversation cost*.

---

## Task 6 — Trace view, against your local trace

**Traces → Trace view**, open the trace, switch between **Graph** and
**Timeline**.

Find the same structures you found in 02C: the greeter handing off, the loop, the
two parallel preproduction branches, the final file writer.

Two names differ from your local trace, and the difference is cosmetic:

- the root span is **`invoke_workflow greeter`**, not `invocation`;
- very short spans are collapsed into **`execute_tool (merged)`**.

Confirm the parallel stage still behaves as it did locally: the parent's duration
should equal its **longer** child, not the sum of both.

There is a **View in Cloud Trace** link in the detail pane. Follow it. This is the
same trace data you read in 02C — Agent Platform is a different lens on it, not a
different recording.

---

## Task 7 — Span view and per-agent cost

**Traces → Span view**, with **Show only invoke agent type** selected.

Every agent span carries a token count, and the counts roll up the agent
hierarchy. From a measured run:

```text
researcher      4,507 ┐
screenwriter   12,233 ├─→ writers_room        22,853 ┐
critic          6,113 ┘                              │
box_office      7,194 ┐                              ├─→ film_concept_team  60,698
casting         6,193 ┴─→ preproduction_team  13,387 │
file_writer                                  24,458 ┘
greeter           451
```

Check the arithmetic on your own run: each parent should equal the sum of its
children exactly, and the root plus the greeter should equal the session total
from Task 5.

Now switch to **Show all types**. Every span gains a type — `Invoke Agent`,
`Agent to Model`, `Agent to Tool`, or unset for runtime internals — and `Input`
and `Output` columns appear. Note where they read `<elided>`: only on
`Agent to Model` rows, which is exactly where prompt content would live.

---

## Task 8 — Why the last agent costs the most

With **Show all types**, read the token count on each individual model call in
workflow order. A measured run:

```text
researcher       390 → 1,853 → 2,264
screenwriter           5,629 → 6,604
critic                         6,113
box_office                     7,194
casting                        6,193
file_writer           12,196 → 12,262
```

Answer these:

1. Which agent consumed the most tokens?
2. That agent runs one model call and writes a file in about 2 milliseconds. Why
   is it the most expensive?
3. The researcher's three calls cost 390, then 1,853, then 2,264. What is growing?
4. Why do the two parallel agents cost roughly the same as each other, rather than
   the second costing more than the first?
5. Your team wants to add a one-line "format the output" agent at the end of the
   workflow. Estimate its cost, and justify your estimate from this trace.
6. The researcher writes a *summary* into state rather than the raw article. What
   would change if it stored the raw article instead?

> The answer to 2 is the lesson of this class: cost is **positional**. Each call
> re-sends the accumulated conversation, so an agent pays for everything upstream
> of it. The file writer is not expensive because it does more work — it is
> expensive because it goes last.

---

## Task 9 — Content collection *(UNVERIFIED)*

> **Not yet tested.** The toggle exists and the default state is confirmed. What
> has not been confirmed is what appears after enabling it. Verify before
> teaching.

Open the Session view for your run. It reports:

```text
Prompt-response content collection is not enabled
```

**A deployed agent does not record prompt or response content by default.** In
02C, running the identical application locally, the opposite was true:
`ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` defaults **on**, and the full system
instruction, conversation history, tool results and model output were readable in
span attributes.

| | Local (02C) | Deployed (02D) |
|---|---|---|
| Default | captured | **not** captured |
| Control | environment variable | console toggle |
| Discoverability | read the ADK source | the UI states it |

Now enable it deliberately, and understand what you are agreeing to first: this
sends your prompts and the model's output to your project's telemetry, readable
by anyone with trace-read permission on that project.

1. **Service configuration** → enable prompt-response content collection.
2. Start a **New Session** in the Playground and run the workflow again.
3. Return to **Session view** and open the new session.

Record what changed:

- Does the Session conversation panel now show the exchange?
- Do the `Input` / `Output` columns in Span view still read `<elided>`?
- Do the spans now carry `gcp.vertex.agent.llm_request`, as they did locally?

Then answer: which default would you choose for a production agent handling
customer data, and which for a development environment? What would you need to
tell your users in each case?

---

## Task 10 — Diagnose a failed invocation *(UNVERIFIED)*

> **Not yet tested.** The deployed container has no `MODEL` environment variable —
> it falls through to the `gemini-2.5-flash` default — so inducing this failure
> requires `env_vars` in `.agent_engine_config.json`, and Agent Platform support
> for that is unconfirmed. Verify before teaching.

Everything so far has been a healthy trace. Reading a broken one is a separate
skill, and the one you will actually need.

Redeploy the same agent with a model that does not exist, updating the existing
instance rather than creating a second one:

```bash
cat > adk_multiagent_systems/workflow_agents/.agent_engine_config.json <<'JSON'
{ "env_vars": { "MODEL": "gemini-does-not-exist" } }
JSON

adk deploy agent_engine \
  --project="$PROJECT_ID" \
  --region=us-central1 \
  --agent_engine_id "$ENGINE_ID" \
  --otel_to_cloud \
  --temp_folder /tmp/adk-deploy-02d \
  --extra_packages "$PWD/adk_multiagent_systems" \
  adk_multiagent_systems/workflow_agents
```

Run the agent in the Playground. It should fail.

Now diagnose it **from the spans alone**, without reading the application logs:

1. Which span carries an `Error` status?
2. Which spans succeeded before it? What does that tell you about how far the
   invocation got?
3. What did the failing span's parent do — did it fail too, or handle it?
4. How far up the tree did the failure propagate?
5. What can you determine about the cause from the span alone, and what would
   require the logs?
6. The agents that ran before the failure still left successful spans. Why does
   that matter when someone reports "the agent is broken"?

Then restore the working configuration:

```bash
rm adk_multiagent_systems/workflow_agents/.agent_engine_config.json
```

and redeploy with the same `--agent_engine_id`.

---

## Task 11 — Browse deployed sessions in the ADK dev UI

The ADK web UI you used in 02C can read the **managed** sessions your deployed
agent creates:

```bash
SESSION_SERVICE_URI=agentengine://$ENGINE_ID ./class-02C-work/start_web_server.sh
```

Open <http://127.0.0.1:8000>, choose `workflow_agents`, and find your deployed
session. You get the graph view, the Events panel, State, and Artifacts over a
run that executed in the cloud.

> **Understand what this is.** Sending a *new* message from this UI runs the agent
> code **on your machine**, storing the session in the managed service. It views
> the deployed agent's history; it does not invoke the deployed container.

Drop the environment variable to return to your local SQLite sessions.

---

## Task 12 — Tear down *(UNVERIFIED — but mandatory)*

> **Command not yet confirmed.** Verify it works before teaching this class. A
> class that deploys without a working teardown leaves every student paying for a
> running agent.

A deployment is a live, billable resource. Remove it:

```bash
gcloud beta ai reasoning-engines delete "$ENGINE_ID" \
  --region=us-central1 --project="$PROJECT_ID"
```

Confirm it is gone:

```bash
curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/us-central1/reasoningEngines" | jq .
```

The response should no longer list your engine.

---

## What this class does not cover

**Telemetry replay stays in Class 02C.** A replayed trace carries only
`recorded.*` attributes — no token counts, no span types, no agent hierarchy — so
in Span view it would show blank costs and unset types. The two capabilities that
justify this class are the two a replay cannot reconstruct.

One idea does carry over, as a discussion. In 02C you reconstructed a convincing
trace from a JSONL file without running anything. That trace is indistinguishable
from a real one to anyone reading the backend. Writing convincing telemetry needs
only permission to write telemetry. So: what does a trace actually prove, and who
must you trust for it to prove anything?

---

## Success criteria

- [ ] The agent is deployed and answers in the Playground.
- [ ] Session, Trace and Span views all show your run.
- [ ] Per-agent token counts reconcile: children sum to parents, and the total
      matches the session.
- [ ] You can explain why the file writer is the most expensive agent.
- [ ] You have compared local and deployed content-capture defaults and stated a
      preference with a reason.
- [ ] You have diagnosed a failed invocation from its spans.
- [ ] **The deployment is deleted and confirmed gone.**
