# Class 02C work area

These utilities observe the golden agent application without editing its source.

| File | Purpose |
|---|---|
| `start_api_server.sh` | Starts the golden agents with native Google Cloud OpenTelemetry export |
| `start_web_server.sh` | The same, but runs `adk web` so you can drive the agent in a browser |
| `run_and_record.sh` | Creates a session, runs two messages, and records session events to JSONL |
| `record_session.sh` | Records an existing session to JSONL without running the agent |
| `show_events.sh` | Displays a concise event table |
| `play_events.sh` | Plays the recorded event sequence at a chosen speed |
| `replay_events.py` | Reconstructs the JSONL recording as a new Google Cloud trace |
| `verify_golden_source.sh` | Verifies the golden source and configuration against the supplied manifest |

Generated files such as `sessions.db`, `events.jsonl`, `session.json`, and
`run-*.json` are written here and are ignored by Git.
