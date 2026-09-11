# Appendix A — Environment Setup and Troubleshooting

Reference material. Consult it; do not work through it.

Chapter 4 argues for a harness. This appendix is the installation detail
that would have buried that argument.

---

## A.1 Prerequisites

| Tool | Version | Needed from |
|---|---|---|
| Python | 3.11 or newer | Chapter 4 |
| [uv](https://docs.astral.sh/uv/) | recent | Chapter 4 |
| Git | any recent | Chapter 4 |
| Docker Desktop or Docker Engine | recent | Chapter 10 |

Nothing else is required, and nothing before Chapter 10 needs Docker. If
you are working through Chapters 1–9, Python and uv are enough.

An Anthropic API key is needed from Chapter 5. Chapters 1–4 run without one.

```bash
python3 --version     # 3.11+
uv --version
git --version
docker --version      # from Chapter 10
```

## A.2 First run

```bash
git clone <repository>
cd book-1-foundations

uv sync --extra dev
uv run pytest -q
```

Expect a green run before you have configured anything. That is Chapter
4.8's proof.

Then:

```bash
cp .env.example .env
```

and put your key in `.env`. Never commit it —
`tests/test_v0_harness.py::test_secrets_are_not_committed` fails loudly if
you do, which is the point.

## A.3 Dependency extras

Dependencies are grouped so a reader in Chapter 5 is not obliged to install
a database driver and a 2 GB embedding model.

| Extra | Install from | Adds |
|---|---|---|
| *(base)* | Chapter 5 | LangGraph, langchain-anthropic, Pydantic |
| `dev` | Chapter 4 | pytest, jsonschema, ruff |
| `mcp` | Chapter 9 | MCP Python SDK |
| `retrieval` | Chapter 10 | psycopg, pgvector, sentence-transformers |
| `serve` | Chapter 14 | FastAPI, uvicorn, checkpointer, OTel, Langfuse |

```bash
uv sync --extra dev                          # Chapters 1-8
uv sync --extra dev --extra mcp              # Chapter 9
uv sync --extra dev --extra mcp --extra retrieval   # Chapters 10-13
uv sync --all-extras                         # Chapters 14-15
```

## A.4 Services

From Chapter 10:

```bash
docker compose up -d postgres
docker compose ps                    # postgres should be healthy
uv run python -m app.retrieval.ingest
```

From Chapter 15, the whole stack:

```bash
export ANTHROPIC_API_KEY=...          # compose refuses to start without it
docker compose up --build
```

The application container runs as UID 10001 with a read-only root
filesystem. That is Chapter 6's security architecture, not deployment
polish, and it will surface any code that assumes it can write next to
itself.

## A.5 Running a specific version

Every version is a tag. Checking one out gives a repository that passes its
own tests.

```bash
git checkout v6-grounded
uv sync --extra dev --extra mcp --extra retrieval
uv run pytest -q
```

| Tag | Chapter | Extras needed |
|---|---|---|
| `v0-harness` | 3–4 | `dev` |
| `v1-monolith` | 5 | `dev` |
| `v2-bounded` | 6 | `dev` |
| `v3-skills` | 7 | `dev` |
| `v4-contracts` | 8 | `dev` |
| `v5-mcp` | 9 | `dev`, `mcp` |
| `v6-grounded` | 10 | `dev`, `mcp`, `retrieval` |
| `v7-workflow` | 11 | `dev`, `mcp`, `retrieval` |
| `v8-evaluated` | 12 | `dev`, `mcp`, `retrieval` |
| `v9-review-loop` | 13 | `dev`, `mcp`, `retrieval` |
| `v10-observed` | 14 | all |
| `v10-packaged` | 15 | all |

Return with `git checkout main`.

## A.6 Test selection

```bash
uv run pytest -q                       # everything offline
uv run pytest -m "not live"            # explicit: no API calls
uv run pytest -m live                  # real model calls, costs money
uv run pytest -m db                    # requires postgres running
uv run pytest tests/test_v7_workflow.py -k route
```

Tests are offline by default. Tools resolve from `data/fixtures/` unless a
live flag is set, so the suite runs on a plane.

## A.7 Troubleshooting

**`ModuleNotFoundError: No module named 'app'`**
Run through uv from the repository root: `uv run pytest`, not `pytest`.
`pyproject.toml` sets `pythonpath = ["."]` for pytest only.

**Tests pass locally, fail in CI**
Usually an extra that is installed locally and not in CI. Compare
`uv sync` invocations. This is also why the manifest records pins rather
than the installed environment (Chapter 4.4).

**`400 Bad Request` mentioning `temperature`, `top_p` or `top_k`**
You have added a sampling parameter. Current Claude models reject
non-default values (ADR-000, Appendix D.2). Remove it. If you added it to
`Settings`, `test_sampling_parameters_are_not_configurable` should have
caught it first.

**`ValueError: thread_id too long`**
`PostgresSaver` requires under 255 characters. Chapter 15.7. Shorten the
account or tenant component.

**`connection refused` on port 5432**
`docker compose up -d postgres`, then wait for `healthy` in
`docker compose ps`. The healthcheck exists because Postgres accepts TCP
before it accepts queries.

**`extension "vector" does not exist`**
You are running stock `postgres`, not `pgvector/pgvector`. Check the image
in `docker-compose.yml`; pgvector is not something you install into a
running stock image.

**Sentence-transformers downloads a model on first run**
Expected — a few hundred megabytes, cached afterwards. The model is pinned
and recorded in the manifest; re-embedding with a different one silently
changes every retrieval result (Chapter 10.7).

**MCP server fails to start**
Run it directly to see its output: `uv run python -m app.mcp.server`.
Over stdio, a server that crashes on import looks identical to one that is
merely slow.

**Traces are empty in Langfuse**
Check `LANGFUSE_HOST` and both keys. If spans appear but carry no prompt or
document text, that is correct — content capture is off by default
(Chapter 14.6).

**A permission error writing inside the container**
The root filesystem is read-only by design. Write to `/tmp`, which is
mounted as tmpfs, or reconsider whether the code should be writing at all.

## A.8 Cleaning up

```bash
docker compose down            # stop services, keep data
docker compose down -v         # stop and delete the database volume
rm -rf .venv .pytest_cache .ruff_cache
```

`docker compose down -v` discards the ingested corpus. Re-ingest with
`uv run python -m app.retrieval.ingest`.

## A.9 Cost

Chapters 1–4 cost nothing. From Chapter 5, live runs cost money.

Per account, expect roughly three to six model calls in early versions and
more once the review loop exists — small change per account (Chapter 3.6).
The whole book, run end to end a few times, is a few dollars rather than a
few hundred.

Two habits that keep it that way: leave tests offline by default, and use
`-m live` deliberately rather than running the full suite against the API
out of momentum.
