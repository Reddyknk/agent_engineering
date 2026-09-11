# Course Conventions

Decided 2026-09-04. This file is the single source of truth for the environment
every class assumes. A class folder that disagrees with this file is wrong, not
an exception.

Read this before editing any class, and when propagating a change across the
course, work down the compliance checklist at the bottom.

---

## 1. One model path: Google Cloud

Every class runs Gemini through a **Google Cloud project** using Vertex AI —
renamed the **Gemini Enterprise Agent Platform** in 2026, though the API
(`aiplatform.googleapis.com`) and the environment variables are unchanged.

There is no second path. The Google AI Studio API-key route was removed from the
course on 2026-09-04. It produced two of everything — two `.env` templates, two
sets of instructions, two failure modes — and the observability, deployment, and
Agent Engine material from Class 02C onward only works on a real project anyway.

**Never reintroduce:**

- `GOOGLE_API_KEY` in a `.env`, a template, an example, or prose;
- `aistudio.google.com` sign-up instructions;
- "Option A / Option B" or "Vertex *or* API key" branching in any instruction;
- code that falls back to an API key when a project is absent.

A missing or misconfigured project is an error to report, not a condition to
route around.

## 2. Canonical environment

Every class's `.env` starts from exactly these four keys, in this order:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
MODEL=gemini-2.5-flash
```

- `GOOGLE_GENAI_USE_VERTEXAI` is always `TRUE`, spelled in capitals. It is never
  absent and never conditional.
- `GOOGLE_CLOUD_LOCATION` is always a real region. **Never `global`** — Agent
  Engine rejects it, and the failure surfaces much later than the mistake.
  `us-central1` unless a class has a stated reason to differ.
- A class may add its own keys after these four. It may not remove or rename one.

Credentials come from **Application Default Credentials**, never from a key file
committed or copied into the repository.

## 3. Shell: bash

- Every fenced command block is ```bash.
- Every script carries `#!/usr/bin/env bash` and is executed, not sourced —
  except a script that must change the caller's shell (activating a virtualenv),
  which documents `source` explicitly.
- Scripts are executed, so a student's login shell does not matter. macOS ships
  zsh; that is fine and no one needs to change it.
- A script intended to be sourced must work under both bash and zsh. Two traps,
  both found in `class-02C/package/class-02C-work/startup.sh`:
  - zsh does not field-split unquoted scalars. Use arrays: `for x in "${arr[@]}"`.
  - zsh sets `ZSH_EVAL_CONTEXT=toplevel:file` — match `*:file*`, not `*:file:*`,
    or a sourced script will `exit` and close the student's terminal.
- Never `set -e` in a script that may be sourced.

## 4. The project exists from Class 1

Students create their Google Cloud project during **Class 1**, following
`SETUP.md`. From Class 2 onward, every class assumes:

- a Google Cloud project exists and its ID is known;
- billing is enabled on it (the free trial counts);
- `gcloud` is installed and authenticated;
- ADC is present and its quota project matches the project in `.env`;
- Cloud Trace, Logging, Monitoring, and Agent Platform APIs are enabled.

No class re-teaches this. A class that needs it verified runs a pre-flight
script; `class-02C/package/class-02C-work/startup.sh` is the reference
implementation.

## 5. Compliance checklist

Propagating a change means walking this table. Status as of 2026-09-04.

| Location | Needs | Done |
| --- | --- | :-: |
| `SETUP.md` | Google Cloud sign-up, project creation, gcloud, ADC | ✅ |
| `CONVENTIONS.md` | this file | ✅ |
| `class-01/` | project-creation task; remove AI Studio prerequisite | ✅ |
| `README.md` (Classes) | remove API-key references | ☐ |
| `class-02A/` | `SETUP.md`, `TROUBLESHOOTING.md`, `.env.example`, `scripts/preflight.py` | ☐ |
| `class-02B/` | `Class_02B_Build_Instructions.md` | ☐ |
| `class-02C/package/` | delete `.env.api-key.example`, drop Option B from instructions, update `golden-source.sha256`, drop apikey mode from `startup.sh` and `start_*.sh`, rebuild zip | ☐ |
| `class-03/` … `class-10/` | `golden-solution/.env.example`, `app.py` docstring, `tests/integration/test_qualification_agent_live.py`, `README.md`, `KNOWN_FAILURE_CASES.md` | ☐ |

The eight golden solutions in Classes 03–10 are **byte-identical** for
`.env.example` and `app.py`, so those two edits are one change applied eight
times, not eight decisions.

## 6. Known inconsistency, not yet decided

The model is named `MODEL` in Class 02C and `WIDGETWARE_MODEL_ID` in Classes
03–10. Both are correct within their own class and neither is wrong enough to
churn every file over. Decide before the next edition; do not "fix" one side in
passing.
