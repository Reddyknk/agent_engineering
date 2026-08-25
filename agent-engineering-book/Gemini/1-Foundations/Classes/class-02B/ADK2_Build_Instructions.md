# Google ADK 2.x: Clean Local Build Instructions

This package is a finished, runnable teaching project for Google Agent Development Kit (ADK) 2.x. It is pinned to `google-adk[gcp]==2.6.0` and demonstrates:

- a single LLM agent;
- a parent agent with specialist sub-agents;
- session-state tools;
- a sequential workflow;
- a bounded research–write–critique loop;
- parallel preproduction agents; and
- a final file-writing agent.

The two authentication choices are included as separate templates. Choose one and copy it to the single project-level `.env` file.

## 1. Prerequisites

Install:

- Python 3.11 or 3.12;
- a terminal; and
- either a Google AI Studio API key or a Google Cloud project with Vertex AI access.

Verify Python:

```bash
python3 --version
```

On Windows, use `py --version` if `python3` is unavailable.

## 2. Expand the ZIP

### macOS or Linux

```bash
unzip class-02B-adk2-clean.zip
cd class-02B-adk2-clean
```

### Windows PowerShell

```powershell
Expand-Archive -Path .\class-02B-adk2-clean.zip -DestinationPath .
Set-Location .\class-02B-adk2-clean
```

After expanding, this directory should contain:

```text
class-02B-adk2-clean/
├── .env.api-key.example
├── .env.vertex.example
├── .gitignore
├── README.md
├── pyproject.toml
├── adk_multiagent_systems/
│   ├── parent_and_subagents/
│   │   └── agent.py
│   ├── shared/
│   │   ├── callbacks.py
│   │   ├── plugins.py
│   │   └── runtime.py
│   └── workflow_agents/
│       └── agent.py
├── movie_pitches/
└── scripts/
    └── validate_install.py
```

## 3. Create and activate a virtual environment

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Your prompt should now show `(.venv)`.

## 4. Install ADK 2.x and the project

Run from the expanded project root:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Confirm the installed ADK version:

```bash
python -c "import google.adk; print(google.adk.__version__)"
```

Expected version:

```text
2.6.0
```

The editable installation makes `adk_multiagent_systems` importable and installs the `adk` command in the active virtual environment.

## 5. Configure authentication

Use exactly one of the following options. Both produce one root file named `.env`.

### Option A — Google AI Studio API key

Create a key at [Google AI Studio](https://aistudio.google.com/app/apikey).

Copy the API-key template:

```bash
cp .env.api-key.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.api-key.example .env
```

Edit `.env`:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=replace_with_your_google_ai_studio_api_key
MODEL=gemini-2.5-flash
MAX_WRITING_ITERATIONS=3
```

Do not commit or share `.env`. It is already listed in `.gitignore`.

### Option B — Vertex AI

Copy the Vertex template:

```bash
cp .env.vertex.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.vertex.example .env
```

Edit `.env`:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your_google_cloud_project_id
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini-2.5-flash
MAX_WRITING_ITERATIONS=3
```

The exact ADK variable is `GOOGLE_GENAI_USE_VERTEXAI=TRUE`. Do not use `VERTEX_AI=true` or `vertex_Ai=true`.

Then authenticate Application Default Credentials and enable Vertex AI:

```bash
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com --project=your_google_cloud_project_id
```

Your Google identity also needs permission to use Vertex AI in that project, such as the Vertex AI User role.

## 6. Validate the local installation

Run this before starting the UI:

```bash
python scripts/validate_install.py
```

Expected final line:

```text
Validation passed. No model API call was made.
```

This test imports both apps, constructs every agent, and tests the ADK 2.x error-plugin hook. It does not send a request to Gemini.

## 7. Run the parent/sub-agent example

Move to the directory that contains the two ADK agent folders:

```bash
cd adk_multiagent_systems
```

Start the terminal runner:

```bash
adk run parent_and_subagents
```

Try these prompts:

```text
I want an art-focused trip, but I have not selected a country.
```

```text
Plan attractions for a first trip to Japan.
```

What to observe:

1. `steering` receives the request.
2. It transfers to `travel_brainstormer` or `attractions_planner`.
3. The attraction tool saves `country` and `attractions` in session state.
4. The parent summarizes the specialist's result.

Stop the runner with `Ctrl+C`.

## 8. Run the sequential, loop, and parallel workflow

From `adk_multiagent_systems`:

```bash
adk run workflow_agents
```

Example input:

```text
Create an inspiring historical drama about Ada Lovelace with a modern, energetic tone.
```

The workflow is:

1. `greeter` records the request in `PROMPT`.
2. `film_concept_team` runs its stages in sequence.
3. `writers_room` loops through `researcher`, `screenwriter`, and `critic`.
4. The critic calls `exit_loop` when the draft is ready; otherwise the loop stops at `MAX_WRITING_ITERATIONS`.
5. `preproduction_team` runs the box-office and casting agents in parallel.
6. `file_writer` gathers the state and writes the final pitch to `movie_pitches/`.

Stop the runner with `Ctrl+C`.

## 9. Use the ADK web interface

From `adk_multiagent_systems`:

```bash
adk web --port 8000
```

Open the URL printed by ADK, normally:

```text
http://127.0.0.1:8000
```

Select either `parent_and_subagents` or `workflow_agents`, enter a prompt, and inspect the events and session state in the developer UI.

The web interface is intended for local development. Do not expose it directly as a public production service.

## 10. Understand the code

| File | Purpose |
|---|---|
| `parent_and_subagents/agent.py` | Parent routing, specialist delegation, and session-state storage |
| `workflow_agents/agent.py` | Sequential, loop, and parallel agents plus safe file output |
| `shared/runtime.py` | Loads the one root `.env`, configures logging, and defines the model/retry settings |
| `shared/callbacks.py` | Logs model inputs, outputs, and tool calls |
| `shared/plugins.py` | Implements the current ADK 2.x `on_model_error_callback` hook for quota errors |
| `scripts/validate_install.py` | Performs a local no-network construction test |

The code imports `App` from `google.adk.apps` and `LangchainTool` from `google.adk.integrations.langchain`, avoiding older internal or deprecated paths.

## 11. Common fixes

### `adk: command not found`

Activate the virtual environment again, then confirm:

```bash
python -m pip show google-adk
which adk
```

On Windows, use `Get-Command adk` instead of `which adk`.

### `ModuleNotFoundError: adk_multiagent_systems`

Return to the extracted project root and reinstall:

```bash
python -m pip install -e .
```

### API-key authentication error

Confirm `.env` contains:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_real_key
```

Remove accidental quotes or trailing spaces.

### Vertex authentication error

Run:

```bash
gcloud auth application-default login
gcloud auth application-default print-access-token
```

Also verify the project ID, Vertex AI API, billing, and IAM permissions.

### `429` or `RESOURCE_EXHAUSTED`

The included plugin returns a readable fallback, but it cannot create additional quota. Wait and retry, reduce request frequency, or review quota for the selected authentication method.

### Wikipedia tool error

Confirm the environment is active and reinstall the project:

```bash
python -m pip install -e .
```

The workflow can still surface a handled tool error if Wikipedia is temporarily unavailable.

## 12. Reset or remove the local installation

Delete generated pitches if desired:

```bash
rm movie_pitches/*.txt
```

Windows PowerShell:

```powershell
Remove-Item .\movie_pitches\*.txt
```

To remove the virtual environment, deactivate it and delete only this project's `.venv` directory.

## Official references

- [ADK 2.0 migration and overview](https://google.github.io/adk-docs/2.0/)
- [ADK Python quickstart](https://google.github.io/adk-docs/get-started/python/)
- [Sequential agents](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
- [Loop agents](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
- [Parallel agents](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)

