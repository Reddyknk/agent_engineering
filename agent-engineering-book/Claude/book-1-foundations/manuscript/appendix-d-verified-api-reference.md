# Appendix D — Verified API Reference

Every version-sensitive call this book depends on, verified against current
official documentation on **2026-09-05** rather than recalled.

This appendix will age. §D.7 is how you check whether it has.

The reasoning behind the pins is in
[`architecture/ADR-000`](../architecture/ADR-000-verified-dependency-baseline.md);
this is the lookup surface.

---

## D.1 Pinned versions

| Package | Version | Introduced |
|---|---|---|
| `langgraph` | 1.2.11 | Ch. 5 |
| `langchain-anthropic` | 1.7.1 | Ch. 5 |
| `langchain-core` | 1.6.2 | Ch. 5 |
| `anthropic` | 1.4.0 | Ch. 5 |
| `pydantic` | 2.13.5 | Ch. 8 |
| `pydantic-settings` | 2.15.0 | Ch. 4 |
| `mcp` | 2.1.1 | Ch. 9 |
| `psycopg[binary]` | 3.3.5 | Ch. 10 |
| `pgvector` | 0.5.0 | Ch. 10 |
| `sentence-transformers` | 6.0.1 | Ch. 10 |
| `fastapi` | 0.141.1 | Ch. 15 |
| `uvicorn[standard]` | 0.52.4 | Ch. 15 |
| `langgraph-checkpoint-postgres` | 3.1.2 | Ch. 15 |
| `opentelemetry-sdk` | 1.44.0 | Ch. 14 |
| `opentelemetry-exporter-otlp-proto-http` | 1.44.0 | Ch. 14 |
| `langfuse` | 4.15.1 | Ch. 14 |
| `pytest` | 9.1.1 | Ch. 4 |
| `pytest-asyncio` | 1.4.0 | Ch. 9 |
| `jsonschema` | 4.26.0 | Ch. 4 |
| `pyyaml` | 6.0.3 | Ch. 3 |
| `ruff` | 0.16.6 | Ch. 4 |

All twenty-one resolve together — verified with `uv pip compile`, producing
115 packages with no conflicts.

**`langgraph-prebuilt` is deliberately not a dependency.** See §D.3.

## D.2 Model

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model=settings.model_id,       # from config; never inline
    max_tokens=settings.max_tokens,
)
```

**Sampling parameters are omitted, not set to defaults.** Current Claude
models — `claude-opus-5`, `claude-sonnet-5` and their siblings — reject
non-default `temperature`, `top_p` and `top_k` with HTTP 400.

This invalidates the widespread advice to set `temperature=0` for
reliability. Chapter 4.6 covers the substitute: typed contracts, boundary
validation and measurement.

Tool binding and structured output:

```python
model_with_tools = model.bind_tools([fetch_page, search_news])
model_with_tools = model.bind_tools([fetch_page], strict=True)   # strict validation

structured = model.with_structured_output(
    QualificationResult,
    method="json_schema",      # native structured output, constrained decoding
)
```

`method="json_schema"` guarantees **shape, not correctness** (Chapter 8.5).

## D.3 Graph

Core graph API is unchanged across the 1.0 boundary. Code written against
0.x `StateGraph` still applies.

```python
from typing import Annotated
from typing_extensions import TypedDict
from operator import add
from langgraph.graph import StateGraph, START, END

class SDRState(TypedDict):
    evidence: Annotated[list[EvidenceItem], add]   # reducer: accumulate
    qualification: QualificationResult | None      # no reducer: overwrite

builder = StateGraph(SDRState)
builder.add_node("qualify", qualify_node)
builder.add_edge(START, "qualify")
builder.add_conditional_edges("qualify", qualification_route)
builder.add_edge("draft", END)

graph = builder.compile(checkpointer=checkpointer)   # compile is mandatory
```

A key with no reducer is overwritten by each update. A key with a reducer
merges. Two nodes writing the same un-reduced key means one silently wins
(Chapter 11.6).

**Deprecated:** `create_react_agent` in `langgraph.prebuilt`, superseded by
`create_agent` in `langchain.agents`. This book uses neither — it assembles
`StateGraph` explicitly (Chapter 5.4), which also avoids the documented
`langgraph` / `langgraph-prebuilt` version coupling that broke installs in
early 2026.

## D.4 Persistence

```python
from langgraph.checkpoint.memory import InMemorySaver          # Ch. 5-14
from langgraph.checkpoint.postgres import PostgresSaver        # Ch. 15

checkpointer = PostgresSaver.from_conn_string(settings.database_url)
checkpointer.setup()                    # creates tables and indexes

graph.invoke(payload, {"configurable": {"thread_id": thread_id}})
```

Resuming means invoking with the same `thread_id`; prior checkpoints are
loaded and execution continues.

**Constraint:** `thread_id` must stay under 255 characters with
`PostgresSaver`. Chapter 15.7 asserts this at construction.

## D.5 Human-in-the-loop

```python
from langgraph.types import interrupt, Command

def approval_node(state: SDRState):
    decision = interrupt({
        "draft": state["draft"],
        "evidence": state["evidence_refs"],
    })
    return {"approval": decision}
```

`interrupt()` suspends execution, checkpoints state, and waits
indefinitely. Resume with:

```python
graph.stream(Command(resume=decision), config=config)
```

The value passed to `Command(resume=...)` becomes the return value of the
`interrupt()` call.

Requires a checkpointer — interrupt without one has nowhere to save the
suspended state.

## D.6 MCP

```python
from mcp.server import MCPServer

mcp = MCPServer("widgetware-research")

@mcp.tool()
async def fetch_page(url: str) -> str:
    """Fetch a public web page.

    Args:
        url: absolute http(s) URL
    """
    ...

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**The server class is `MCPServer`, imported from `mcp.server`.** Material
written for the 1.x SDK shows `FastMCP` from `mcp.server.fastmcp`; that is
the older name and will not import against `mcp==2.1.1`.

The SDK depends on `httpx2`. Spec revision `2026-07-28`.

## D.7 Re-verification

Everything above is a snapshot. Before a new edition, or when something
stops working:

```bash
for p in langgraph langchain-anthropic langchain-core anthropic mcp \
         pydantic fastapi pgvector sentence-transformers langfuse \
         opentelemetry-sdk psycopg; do
  curl -s "https://pypi.org/pypi/$p/json" \
    | python3 -c "import sys,json; d=json.load(sys.stdin)['info']; print(f\"{d['name']:<34} {d['version']}\")"
done
```

**Use the PyPI JSON API, not `pip index versions`.** During the writing of
this book `pip index` returned `langgraph 0.6.11` from a stale mirror when
the current release was `1.2.11` — a difference of a major version. A
baseline built on that would have been wrong from the first page.

Then confirm the set still resolves:

```bash
uv pip compile requirements.in --python-version 3.11 -o resolved.lock
```

## D.8 What changed from pre-2026 material

If you are carrying knowledge from older tutorials, these four are the ones
that will bite:

| Older material says | Current |
|---|---|
| `temperature=0` for reliable output | Rejected with HTTP 400; omit sampling parameters |
| Force a single tool call for structured output | `with_structured_output(..., method="json_schema")` |
| `create_react_agent` from `langgraph.prebuilt` | Deprecated; `create_agent` in `langchain.agents`, or assemble the graph |
| `FastMCP` from `mcp.server.fastmcp` | `MCPServer` from `mcp.server` |

The graph API itself — `StateGraph`, `Annotated` reducers, `START`/`END`,
`add_conditional_edges`, `compile()` — is unchanged, which is why most
LangGraph material still reads correctly.
