#!/usr/bin/env bash
set -euo pipefail

# Record an ADK session's event history to JSONL without running the agent.
# Use this after driving the agent yourself in the `adk web` UI.
#
#   ./record_session.sh                 # newest session for APP_NAME/USER_ID
#   ./record_session.sh <session-id>    # a specific session

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
APP_NAME="${APP_NAME:-workflow_agents}"
USER_ID="${USER_ID:-user}"
SESSION_ID="${1:-${SESSION_ID:-}}"

for command in curl jq; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Required command not found: $command"
    exit 1
  fi
done

if [[ -z "$SESSION_ID" ]]; then
  echo "Looking up the newest session for $APP_NAME / $USER_ID"
  SESSION_ID="$(
    curl -fsS "$BASE_URL/apps/$APP_NAME/users/$USER_ID/sessions" \
      | jq -r 'sort_by(.lastUpdateTime) | last | .id // empty'
  )"
fi

if [[ -z "$SESSION_ID" ]]; then
  echo "No sessions found for $APP_NAME / $USER_ID at $BASE_URL"
  echo "The web UI stores sessions under user id 'user'."
  echo "Override with: USER_ID=class02c-user ./record_session.sh"
  exit 1
fi

echo "Recording session $SESSION_ID"

curl -fsS \
  "$BASE_URL/apps/$APP_NAME/users/$USER_ID/sessions/$SESSION_ID" \
  | tee "$SCRIPT_DIR/session.json" \
  | jq -c '.events[]' \
  > "$SCRIPT_DIR/events.jsonl"

cat > "$SCRIPT_DIR/last_session.env" <<INNER
BASE_URL=$BASE_URL
APP_NAME=$APP_NAME
USER_ID=$USER_ID
SESSION_ID=$SESSION_ID
INNER

echo "Recorded $(wc -l < "$SCRIPT_DIR/events.jsonl" | tr -d ' ') events"
echo "Recording: $SCRIPT_DIR/events.jsonl"
