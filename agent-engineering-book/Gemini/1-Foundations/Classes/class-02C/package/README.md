# Class 02C — Observe, Record, Play, and Replay an ADK Agent

This is one self-contained package. It contains a **completed golden** ADK
multi-agent application plus the Class 02C observability utilities.

You do not need to complete any earlier class. You are not expected to edit or
rebuild the agent source — it is the system you will observe.

## Contents

```text
class-02C/
├── adk_multiagent_systems/       # Completed golden agent applications
├── movie_pitches/                # Generated movie-pitch files
├── scripts/                      # Package validation utilities
├── class-02C-work/               # Telemetry helpers and generated evidence
│   └── startup.sh                # Environment setup — source this before every session
├── pyproject.toml
├── .env.api-key.example
├── .env.vertex.example
└── class_02C_instructions.md     # The Class 02C observability lab — start here
```

No nested archive is required.

## Start

```bash
unzip class-02C.zip
cd class-02C
less class_02C_instructions.md
```

Create the environment and install the project:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Confirm you have the golden source before starting the lab:

```bash
python scripts/validate_package.py
python scripts/check_progress.py
```

Every progress line must report `PASS`.

## Startup — run this before every session

One command sets up the environment and proves it is actually set up:

```bash
source ./class-02C-work/startup.sh
```

To switch to a different Google Cloud project, pass it as the first argument.
The region is the optional second argument and defaults to `us-central1`:

```bash
source ./class-02C-work/startup.sh qwiklabs-gcp-01-abc123def456
source ./class-02C-work/startup.sh qwiklabs-gcp-01-abc123def456 us-central1
```

With no arguments it uses whatever `.env` already names.

**Use `source`, not `./`.** A script runs in its own shell and cannot activate a
virtual environment in yours. Run it as `./class-02C-work/startup.sh` and
everything else still happens — you are just left outside `.venv`, and the
script says so.

To see what it would do without changing anything, add `--check`:

```bash
./class-02C-work/startup.sh --check
```

It must report `READY` before you start a server.

### What it does

| # | Step | Why it is here |
| --: | --- | --- |
| 1 | Finds the package root | Works from any directory inside the package |
| 2 | Creates `.venv` and installs the project if missing | Task 1, done for you |
| 3 | Writes the project and region into `.env` | The two values that change between lab instances |
| 4 | Points `gcloud` at that project | `gcloud` and `.env` disagreeing is silent and confusing |
| 5 | Refreshes Application Default Credentials if they do not match | The one everyone misses — see below |
| 6 | Confirms Trace, Logging, Monitoring, and Agent Platform are enabled | Missing APIs surface as unrelated-looking export errors |
| 7 | Stops a stale ADK server from an earlier project | A server reads `.env` once, at startup |
| 8 | Deactivates any other venv and activates this one | Only possible when the script is sourced |

Step 5 opens a browser when it has work to do. Everything else is silent unless
it finds a problem.

### The step that exists because of one specific mistake

`gcloud auth login` and `gcloud auth application-default login` are two
different credentials. The first authenticates the `gcloud` command. The second
writes Application Default Credentials, and **ADC is what the agent and the
Cloud Trace exporter actually use.**

So after switching projects, running only `gcloud auth login` leaves the lab
pointed at the old project. Nothing announces this. Model calls fail with
permission errors that read like quota problems, or — worse — they succeed, and
the traces land in a project you are not looking at.

Step 5 compares the project recorded inside the ADC file against the one in
`.env`, and re-runs the login when they disagree. The equivalent by hand is:

```bash
export PROJECT_ID=your_new_project_id
gcloud config set project "$PROJECT_ID"
gcloud auth application-default login
gcloud auth application-default set-quota-project "$PROJECT_ID"
```

### A note on lab accounts

A new lab instance issues a new project **and** a new student account. If
`startup.sh` warns that your account number and project number disagree, check
whether step 6 could still list the enabled services. If it could, the old
account still has access and the warning is harmless. If it could not, switch
accounts:

```bash
gcloud auth list
gcloud config set account <the account for this lab>
```
