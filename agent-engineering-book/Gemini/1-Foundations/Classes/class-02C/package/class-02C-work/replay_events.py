#!/usr/bin/env python3
"""Replay an ADK JSONL event recording as a fresh Google Cloud trace."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any


def load_events(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"Line {line_number} is not a JSON object")
            records.append(value)
    return records


def event_types(event: dict[str, Any]) -> str:
    kinds: list[str] = []
    for part in (event.get("content") or {}).get("parts") or []:
        if not isinstance(part, dict):
            continue
        if "text" in part:
            kinds.append("text")
        if "functionCall" in part:
            kinds.append("function_call")
        if "functionResponse" in part:
            kinds.append("function_response")
        if "inlineData" in part:
            kinds.append("inline_data")
    state_delta = ((event.get("actions") or {}).get("stateDelta") or {})
    if state_delta:
        kinds.append("state_delta")
    return ",".join(dict.fromkeys(kinds)) or "event"


def attributes(event: dict[str, Any], sequence: int) -> dict[str, Any]:
    actions = event.get("actions") or {}
    state_delta = actions.get("stateDelta") or {}
    return {
        "replay.telemetry_only": True,
        "recorded.event.sequence": sequence,
        "recorded.event.id": str(event.get("id") or ""),
        "recorded.event.author": str(event.get("author") or "unknown"),
        "recorded.event.type": event_types(event),
        "recorded.invocation_id": str(event.get("invocationId") or ""),
        "recorded.state_delta.keys": ",".join(sorted(state_delta)),
    }


def planned_timestamps(events: list[dict[str, Any]], speed: float) -> list[int]:
    raw = [float(event.get("timestamp") or 0.0) for event in events]
    first = raw[0]
    relative = [max(0.0, timestamp - first) / speed for timestamp in raw]
    anchor = time.time_ns() - int(relative[-1] * 1_000_000_000) - 1_000_000_000
    return [anchor + int(delta * 1_000_000_000) for delta in relative]


class _ExportFailureWatcher(logging.Handler):
    """Collects OpenTelemetry export failures.

    A failed export is not an exception. BatchSpanProcessor writes a log record
    and returns normally, so a caller that only watches for exceptions cannot
    tell "wrote every span" from "Cloud Trace rejected the batch". This handler
    captures those records so the exit status can reflect what really happened.
    """

    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self.failures: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        if record.name.startswith("opentelemetry"):
            self.failures.append(record.getMessage())


def emit(events: list[dict[str, Any]], project_id: str, speed: float) -> list[str]:
    watcher = _ExportFailureWatcher()
    logging.getLogger().addHandler(watcher)

    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["OTEL_SERVICE_NAME"] = "class-02c-replay"
    os.environ["OTEL_RESOURCE_ATTRIBUTES"] = (
        "deployment.environment=classroom,class.name=02C,replay.mode=telemetry_only"
    )

    from google.adk.telemetry.google_cloud import get_gcp_exporters
    from google.adk.telemetry.google_cloud import get_gcp_resource
    from google.adk.telemetry.setup import maybe_set_otel_providers
    from opentelemetry import trace

    exporters = get_gcp_exporters(enable_cloud_tracing=True)
    # telemetry.googleapis.com rejects any batch whose Resource lacks
    # gcp.project_id. get_gcp_resource() takes the project as an argument and
    # does not read the environment, so setting GOOGLE_CLOUD_PROJECT is not
    # enough -- the resource has to be built and passed explicitly.
    maybe_set_otel_providers(
        [exporters], otel_resource=get_gcp_resource(project_id)
    )

    provider = trace.get_tracer_provider()
    tracer = trace.get_tracer("class-02c.event-replay")
    timestamps = planned_timestamps(events, speed)

    root = tracer.start_span(
        "replay.adk.session",
        start_time=timestamps[0],
        attributes={
            "replay.telemetry_only": True,
            "replay.event_count": len(events),
            "replay.source_invocation_id": str(events[0].get("invocationId") or ""),
        },
    )
    parent_context = trace.set_span_in_context(root)

    try:
        for sequence, (event, start_time) in enumerate(
            zip(events, timestamps, strict=True), start=1
        ):
            event_attributes = attributes(event, sequence)
            author = event_attributes["recorded.event.author"]
            span = tracer.start_span(
                f"replay.event.{author}",
                context=parent_context,
                start_time=start_time,
                attributes=event_attributes,
            )
            span.add_event(
                "recorded.adk.event",
                attributes=event_attributes,
                timestamp=start_time,
            )
            span.end(end_time=start_time + 1_000_000)
    finally:
        root.end(end_time=timestamps[-1] + 10_000_000)
        force_flush = getattr(provider, "force_flush", None)
        if callable(force_flush) and force_flush() is False:
            watcher.failures.append(
                "force_flush() timed out before every span was exported"
            )
        shutdown = getattr(provider, "shutdown", None)
        if callable(shutdown):
            shutdown()
        logging.getLogger().removeHandler(watcher)

    return watcher.failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("recording", type=Path, nargs="?", default=Path(__file__).with_name("events.jsonl"))
    parser.add_argument("--project-id", default=os.getenv("GOOGLE_CLOUD_PROJECT"))
    parser.add_argument("--speed", type=float, default=4.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--debug",
        action="store_true",
        help=(
            "Log the exporter's own diagnostics, including the full body of a "
            "rejected export."
        ),
    )
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.speed <= 0:
        parser.error("--speed must be greater than zero")

    events = load_events(args.recording)
    if not events:
        raise SystemExit("The recording contains no events")

    if args.dry_run:
        print(f"Would replay {len(events)} events")
        for sequence, event in enumerate(events, start=1):
            print(
                f"{sequence:03d} "
                f"{event.get('author', 'unknown')}: "
                f"{event_types(event)}"
            )
        return

    if not args.project_id:
        raise SystemExit("Set GOOGLE_CLOUD_PROJECT or pass --project-id")

    failures = emit(events, args.project_id, args.speed)
    if failures:
        print(
            f"Export FAILED for project {args.project_id}: at least one span "
            f"batch was rejected, so the replay trace is missing or incomplete.",
            file=sys.stderr,
        )
        for failure in dict.fromkeys(failures):
            print(f"  {failure}", file=sys.stderr)
        print(
            "  Re-run with --debug for the exporter's full error body.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    print(
        f"Replayed {len(events)} events to Google Cloud Trace "
        f"in project {args.project_id}"
    )


if __name__ == "__main__":
    main()
