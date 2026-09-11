# Chapter 9 — Connect External Capabilities through MCP

> **Status: outline.**

**Starting point:** V4 — typed contracts
**Result:** V5 — research capabilities behind the Model Context Protocol

---

## 9.1 Current state and observed limitation

V4's research tools are functions inside the application. Two consequences,
and the second is the one that matters.

The visible one: the tools cannot be shared with another application,
versioned independently, deployed separately, or replaced without a release
of the whole system.

The deeper one: **there is no boundary at which provenance is recorded.**
`fetch_webpage` returns a string. Whether that string was retrieved just now
or is a plausible summary the model produced is not distinguishable
downstream. Chapter 8 gave `EvidenceItem` a place to record source and
retrieval method; nothing populates it honestly, because nothing sits at a
boundary where it must.

## 9.2 Engineering question

> Can a capability live outside the application — with its own lifecycle and
> a provenance-bearing contract — without changing the workflow?

## 9.3 Architectural decision

Move external research behind a **Model Context Protocol (MCP)** server
using the official Python SDK, reached through a **thin MCP-to-LangGraph
adapter** the book writes and the reader can read.

MCP owns interoperability: tool discovery, schemas, invocation, resource
access, lifecycle. **MCP does not orchestrate.** The graph stays in
LangGraph.

## 9.4 MCP, from zero

For readers meeting it for the first time. MCP is an open protocol for
exposing capabilities to models across a process boundary. Three concepts:

- **Tools** — functions the model may call, with JSON Schema arguments.
- **Resources** — file-like data a client may read, addressed by URI.
- **Prompts** — reusable templates a server offers. Not used in Book 1;
  named so readers recognise them.

Transport is stdio here — the server is a subprocess. HTTP transports exist
and matter for independently deployed servers; the boundary is the lesson,
and stdio makes it demonstrable on one machine.

Verified against the current SDK (ADR-000): the server class is
`from mcp.server import MCPServer`, tools are declared with `@mcp.tool()`,
and the server runs via `mcp.run(transport="stdio")`. Material written for
the 1.x SDK will show `FastMCP`; that is the older name.

## 9.5 Alternatives considered

**Keep the tools in-process.** Simpler, and defensible for a system this
size. Rejected because the provenance boundary is the point — and because a
reader who never crosses a process boundary will not recognise the failure
modes when they later must.

**`langchain-mcp-adapters`.** Would work in one line. Rejected per the
brief's visibility constraint: the adapter is ~60 lines, and a reader who
has read it understands what MCP actually exchanges. This is a book, not a
race.

**A plain HTTP microservice.** Rejected — it reinvents discovery, schema
description and lifecycle, which is what the protocol already standardises.

**Move *all* tools behind MCP.** Rejected. Tools owned by the application
and used only by it stay ordinary Python. MCP is for capabilities that are
external or independently deployable; using it everywhere makes a boundary
meaningless by making it universal.

## 9.6 Trade-offs

A process boundary adds failure modes that did not exist: startup failure,
timeout, protocol mismatch, a server that dies mid-run. The chapter treats
these as first-class rather than as an appendix — a failing MCP server must
degrade one node, not the run.

Debugging is harder. A stack trace stops at the boundary.

## 9.7 Implementation walkthrough

- `app/mcp/server.py` — `MCPServer("widgetware-research")` exposing
  `fetch_page` and `search_news` as tools, and the ICP and offering as
  **resources** (they are data to read, not functions to call — the
  distinction is worth demonstrating rather than asserting).
- `app/mcp/adapter.py` — connect, list tools, convert MCP schemas to
  LangChain tool objects, invoke, and map results into `EvidenceItem` with
  source, retrieval method and timestamp populated **at the boundary**.
- `app/mcp/lifecycle.py` — startup, health, timeout, graceful degradation.

Every returned passage gets a content hash and a retrieval timestamp here.
Evidence freshness becomes checkable because the boundary records when.

## 9.8 Failure handling

Enumerated and tested: server fails to start; server dies mid-run; tool
times out; tool returns a schema-invalid result; server offers a tool the
allowlist forbids (Chapter 6's gate still applies — MCP is a source of
tools, not an authority over policy).

Each maps to a defined behaviour: degrade the node, record the failure in
the audit log, and escalate rather than fabricate.

## 9.9 Tests and evaluation

- The graph is byte-for-byte unchanged by the move; only tool construction
  differs. This is the chapter's central claim and its central test.
- Every evidence item from MCP carries source, method, timestamp and hash.
- Each failure mode above produces its defined behaviour.
- The Chapter 6 policy gate still refuses forbidden tools offered by MCP.

## 9.10 Failure demonstration

Kill the MCP server mid-run. Show the research node degrading, the audit
record, and the run completing with an `Escalation` — not a crash, and not a
brief with invented content where research should have been.

## 9.11 Evidence of improvement

Evidence items with resolvable provenance: V4 unenforced → V5 100%.
Workflow architecture unchanged, demonstrating the boundary was clean.

## 9.12 Updated run manifest

`version_tag: "v5-mcp"`, MCP server name and version, tool inventory.

## 9.13 What remains unresolved

Claims about the *prospect* are now sourced. Claims about *WidgetWare* — our
capabilities, our customer outcomes — are still whatever the model believes,
and drafts assert them confidently.

## 9.14 Exercises

1. Add a tool to the MCP server without touching the graph. What did you
   have to change? What does that tell you about the boundary?
2. Make the server return a schema-invalid result deliberately. Where is it
   caught — the adapter, the node, or the contract? Should it be earlier?
