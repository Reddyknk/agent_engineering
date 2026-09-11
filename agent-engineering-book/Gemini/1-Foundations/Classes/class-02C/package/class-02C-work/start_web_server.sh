#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$PACKAGE_ROOT"
PROJECT_ID="${1:-${PROJECT_ID:-${GOOGLE_CLOUD_PROJECT:-}}}"

if [[ ! -d "$PROJECT_ROOT" ]]; then
  echo "Missing $PROJECT_ROOT"
  exit 1
fi

if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
  echo "Missing $PROJECT_ROOT/.env"
  echo "Create it from a template first. See Task 2 of class_02C_instructions.md:"
  echo "  cp .env.vertex.example .env   # or: cp .env.api-key.example .env"
  exit 1
fi

if [[ ! -f "$PROJECT_ROOT/.venv/bin/activate" ]]; then
  echo "Missing project virtual environment."
  echo "See Task 1 of class_02C_instructions.md:"
  echo "  python3 -m venv .venv && source .venv/bin/activate && python -m pip install -e ."
  exit 1
fi

source "$PROJECT_ROOT/.venv/bin/activate"

set -a
source "$PROJECT_ROOT/.env"
set +a

if [[ -z "$PROJECT_ID" ]]; then
  PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-}"
fi

if [[ -z "$PROJECT_ID" ]]; then
  echo "Set PROJECT_ID, set GOOGLE_CLOUD_PROJECT in .env, or pass it as the first argument."
  echo "Example: ./start_web_server.sh my-project-id"
  exit 1
fi

export GOOGLE_CLOUD_PROJECT="$PROJECT_ID"
export OTEL_SERVICE_NAME="${OTEL_SERVICE_NAME:-class-02c-live}"
# service.instance.id is required: telemetry.googleapis.com maps this resource
# onto a prometheus_target, which rejects the whole metrics batch with
# "must have an instance specified" when it is absent. ADK only sets it on
# the Agent Engine path, so a local run has to supply it.
export OTEL_RESOURCE_ATTRIBUTES="${OTEL_RESOURCE_ATTRIBUTES:-deployment.environment=classroom,class.name=02C,service.instance.id=$(hostname -s)-$$,cloud.region=${GOOGLE_CLOUD_LOCATION:-us-central1}}"
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="${OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT:-NO_CONTENT}"

# Two independent content-capture knobs:
#   OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT governs the gen_ai.* attributes.
#   ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS governs ADK's own
#     gcp.vertex.agent.llm_request / llm_response attributes, and DEFAULTS ON.
# Left on deliberately so the lab can show what telemetry really captures.
# Set it to false and re-run to watch those attributes collapse to "{}".
export ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS="${ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS:-true}"

echo "Web UI:  http://127.0.0.1:${ADK_PORT:-8000}"
echo "Project: $PROJECT_ID"
echo "Traces:  service.name=$OTEL_SERVICE_NAME"

# SESSION_SERVICE_URI overrides where sessions live. Default is the local
# SQLite file. Point it at a deployed agent to browse its managed sessions:
#   SESSION_SERVICE_URI=agentengine://<engine-id> ./start_web_server.sh
# Note that new messages still execute this local code; only the session
# store is remote.
exec adk web \
  --otel_to_cloud \
  --no-reload \
  --port "${ADK_PORT:-8000}" \
  --session_service_uri="${SESSION_SERVICE_URI:-sqlite:///$SCRIPT_DIR/sessions.db}" \
  "$PROJECT_ROOT/adk_multiagent_systems"
