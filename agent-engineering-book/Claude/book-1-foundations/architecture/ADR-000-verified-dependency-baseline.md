# ADR-000 — Verified Dependency Baseline

**Status:** Accepted
**Date:** 2026-09-05
**Applies from:** V0

## Context

Every version-sensitive API in this book was verified against current
official documentation and the PyPI release index on the date above, not
recalled from memory. This record exists because three of the findings
contradict what a reasonable engineer would have written from familiarity
with earlier releases, and because a reader running this code six months
from now needs to know exactly what was true when it was written.

`pip index versions` was consulted first and returned stale data from a
mirror — it reported `langgraph 0.6.11` when the current release is
`1.2.11`. The PyPI JSON API (`https://pypi.org/pypi/<name>/json`) was used
instead and is what the versions below come from.

## Pinned baseline

| Package | Version | Role |
|---|---|---|
| `langgraph` | 1.2.11 | The only orchestration framework |
| `langgraph-checkpoint-postgres` | 3.1.2 | Durable checkpointing (V10) |
| `langchain-anthropic` | 1.7.1 | Provider adapter to the Messages API |
| `langchain-core` | 1.6.2 | Message and tool primitives |
| `anthropic` | 1.4.0 | Underlying SDK |
| `mcp` | 2.1.1 | Model Context Protocol SDK (V5) |
| `pydantic` | 2.13.5 | External and domain contracts |
| `fastapi` | 0.141.1 | Application boundary (V10) |
| `psycopg` | 3.3.5 | PostgreSQL driver |
| `pgvector` | 0.5.0 | Vector column type (V6) |
| `sentence-transformers` | 6.0.1 | Embedding model host (V6) |
| `opentelemetry-sdk` | 1.44.0 | Instrumentation standard (V10) |
| `langfuse` | 4.15.1 | Trace backend (V10) |

## Findings that change the design

### 1. Newer Claude models reject non-default sampling parameters

Setting `temperature`, `top_p` or `top_k` to a non-default value on
`claude-opus-5` or `claude-sonnet-5` returns HTTP 400. The official
guidance is to omit them, or pass defaults only.

**Consequence.** This book must not teach `temperature=0` as the lever for
making agent output reliable — the conventional advice, and on these models
an error rather than a tuning choice. Reliability comes from typed
contracts (V4), validation nodes (V7) and evaluation (V8) instead. The run
manifest records that sampling parameters are at model defaults rather than
recording a temperature value.

This is a better lesson than the one it replaces. Determinism was never
what `temperature=0` bought, and the book is stronger for not being able to
pretend otherwise.

### 2. Native structured output supersedes forced tool use

`ChatAnthropic.with_structured_output(Model, method="json_schema")`
activates Anthropic's native structured output, which validates tool names
and argument types through constrained decoding.

**Consequence.** V4 uses this directly rather than the older pattern of
declaring a single tool and forcing the model to call it. The Pydantic
model is still the contract and validation at the node boundary is still
required — constrained decoding guarantees shape, not correctness.

### 3. `langgraph.prebuilt.create_react_agent` is deprecated

Superseded by `create_agent` in `langchain.agents`. There is also a
documented version-mismatch hazard between `langgraph` and
`langgraph-prebuilt` that broke installs in early 2026.

**Consequence.** This book builds its graph explicitly with `StateGraph`
from V1 onward and uses no prebuilt agent constructor. That was already the
pedagogically correct choice — a reader cannot learn to reason about a
graph they did not assemble — and it also avoids the prebuilt package's
release coupling entirely. `langgraph-prebuilt` is not a dependency of this
project.

### 4. The MCP Python SDK server class was renamed

The current server entry point is `from mcp.server import MCPServer`, not
the `FastMCP` class familiar from the 1.x SDK. Tools are declared with
`@mcp.tool()` and the server runs via `mcp.run(transport="stdio")`. The SDK
depends on `httpx2`. Spec revision `2026-07-28`.

## Verified API surface

These are the exact signatures V1–V10 are built on.

```python
# State and graph — unchanged across the 1.0 boundary
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    evidence: Annotated[list[EvidenceItem], add]   # explicit reducer
    qualification: QualificationResult | None      # default: overwrite

builder = StateGraph(State)
builder.add_node("qualify", qualify_node)
builder.add_edge(START, "qualify")
builder.add_conditional_edges("qualify", route_on_qualification)
graph = builder.compile(checkpointer=checkpointer)

# Persistence
from langgraph.checkpoint.memory import InMemorySaver          # V1–V9
from langgraph.checkpoint.postgres import PostgresSaver        # V10
checkpointer = PostgresSaver.from_conn_string(DSN)
checkpointer.setup()
graph.invoke(payload, {"configurable": {"thread_id": thread_id}})

# Human-in-the-loop
from langgraph.types import interrupt, Command
decision = interrupt("Approve this outreach draft?")
graph.stream(Command(resume=decision), config=config)

# Model
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model=settings.model_id, max_tokens=4096)  # no temperature
structured = model.with_structured_output(QualificationResult, method="json_schema")
```

## Constraints this places on the book

- `thread_id` must stay under 255 characters when `PostgresSaver` is in
  use. The account-scoped thread naming in V10 respects this.
- Model identifiers live in configuration and in `RUN_MANIFEST.json`, never
  inline in a node. The architecture must not depend on which Claude model
  is selected.
- Dependencies are pinned exactly, not floored. The `langgraph` /
  `langgraph-prebuilt` incident is the argument: a compatible-release
  specifier would have accepted the broken combination.

## Re-verification

Anything in this file may age. Re-check before a new edition:

```bash
for p in langgraph langchain-anthropic mcp pydantic fastapi; do
  curl -s "https://pypi.org/pypi/$p/json" \
    | python3 -c "import sys,json; d=json.load(sys.stdin)['info']; print(d['name'], d['version'])"
done
```
