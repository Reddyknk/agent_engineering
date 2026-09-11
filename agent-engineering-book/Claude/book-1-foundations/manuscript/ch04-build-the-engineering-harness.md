# Chapter 4 — Build the Engineering Harness

**Starting point:** V0 — a specification
**Result:** V0 — a specification that runs, tests and records itself

---

## 4.1 Current state and observed limitation

Chapter 3 produced a specification. Nothing runs it.

Concretely, three things are missing, and each has a characteristic failure
mode you will recognise:

- **No reproducible environment.** "Works on my machine" is not a joke in
  agent work, it is the default state. Model client libraries move fast, and
  a version skew between two developers produces different behaviour from
  identical code.
- **No test harness.** Without one, every claim in this book about whether a
  version improved on the last is a matter of opinion.
- **No record of what produced a result.** A good run you cannot attribute
  to specific inputs teaches you nothing.

## 4.2 Engineering question

> Can two people, on different machines, get the same result from the same
> inputs — and prove it?

## 4.3 Architectural decision

Build the harness **before the agent**, and make it prove itself with tests
that require no API key, no database and no network.

Pin every dependency **exactly**, not with a compatible-release specifier.

Generate a **run manifest** from the repository's own pins rather than from
the installed environment.

## 4.4 Alternatives considered

**Build the agent first, add tests when there is something to test.** The
overwhelmingly common choice, and it is why so many agent codebases have a
test suite that only runs against a live API. Rejected: by the time you want
the harness you have a system whose behaviour you cannot pin down, and
writing tests for it means first discovering what it does.

**Floor dependencies (`langgraph>=1.2`).** Standard practice for
applications, and wrong here. The concrete argument is in ADR-000: a
documented version-mismatch between `langgraph` and `langgraph-prebuilt` in
early 2026 broke installs, and a compatible-release specifier would have
happily accepted the broken combination. A book whose code stops working for
readers six months after publication has failed at its main job.

**Generate the manifest from the installed environment** (`pip freeze`).
Rejected, and the distinction is subtle enough to be worth stating: the
installed set answers *what is on this machine*; the pins answer *what was
this evaluated against*. Only the second is reproducible. A manifest built
from `pip freeze` on a machine with a stale virtualenv records the staleness
as though it were the specification.

**Require Docker from Chapter 4.** Rejected as premature. There is no
database until Chapter 10 and no service until Chapter 15. Making a reader
run a container to execute four tests that read YAML files teaches them that
the setup instructions are heavier than the work.

## 4.5 Architecture before and after

**Before:** files in a directory.

**After:**

```text
book-1-foundations/
├── manuscript/            prose
├── architecture/          decision records — ADR-000 is the dependency baseline
├── app/
│   ├── config.py          settings; the only place a model id appears
│   ├── manifest.py        the reproduction record
│   ├── contracts/         evidence-policy.yaml lives here
│   └── {graph,nodes,policies,tools,mcp,skills,
│        retrieval,persistence,observability,evaluation,api}/
│                          empty packages — the shape of what is coming
├── config/                the business specification (Ch. 3)
├── data/                  accounts.csv, offline fixtures
├── evals/cases/           golden cases (Ch. 12)
├── tests/
├── pyproject.toml         exact pins
├── .env.example
├── docker-compose.yml     unused until Ch. 15
└── RUN_MANIFEST.json      generated, committed
```

The empty packages are deliberate. A reader can see the intended shape of
the system from the directory listing, and a test asserts the listing
matches the architecture — so the two cannot drift apart silently.

## 4.6 Implementation walkthrough

### Settings, and the parameter that is missing

`app/config.py` holds the model identifier, because the architecture must
survive a model change and a model id inside a node will be missed when the
default moves. A test enforces this: no module below `config.py` may contain
the string `claude-`.

More interesting is what `Settings` deliberately does **not** expose:

```python
# Deliberately absent: temperature, top_p, top_k.
#
# Current Claude models reject non-default sampling parameters — setting
# them returns HTTP 400 rather than tuning anything (architecture/ADR-000).
```

This is worth dwelling on, because it contradicts advice you will find
almost everywhere. The standard guidance for making model output reliable is
`temperature=0`. On current Claude models that is not a conservative default
— it is an error response you have no obvious way to interpret.

The advice was never quite right anyway. `temperature=0` does not buy
determinism; it buys *lower variance*, and teams routinely mistake the two
and then build on an assumption that does not hold. This book's answer to
reliability is typed contracts (Chapter 8), validation at node boundaries
(Chapter 11) and measurement (Chapter 12). Those work, and they work for
reasons you can inspect.

`Settings.model_parameters()` therefore reports sampling as
`"model defaults (temperature/top_p/top_k not set)"` — a string, not a
number, because reporting `temperature: null` would suggest a value we
chose rather than a knob that does not exist for us.

### The manifest

`app/manifest.py` records: application version and git revision, model
parameters, Python and platform, every pinned dependency, and the autonomy
boundary.

It parses pins out of `pyproject.toml` directly. That parser had a bug worth
showing, because it is the kind that survives a passing test:

```python
# Strip the trailing comment first — several pins carry one naming
# the version that introduces them — then the TOML list punctuation.
line = raw.split("#", 1)[0].strip().rstrip(",").strip().strip('"')
```

The original stripped punctuation before comments, so a line reading
`"mcp==2.1.1",           # V5, Chapter 9` produced the version string
`2.1.1",`. The test passed, because it checked only that the version began
with a digit.

The fix was in two places, and the second matters more:

```python
assert re.fullmatch(r"\d+(\.\d+)*", version), (
    f"{name} pinned to a malformed version: {version!r}"
)
```

A test that checks the first character of a value is a test that will let
almost anything through. When a bug survives a test, the test is part of the
bug.

### Tests that need nothing

The V0 suite runs with no API key, no database and no network:

- the repository layout matches the architecture;
- no `.env` is committed, and `.env.example` holds no real key;
- no outbound-messaging capability exists anywhere in `app/`;
- no model identifier appears outside `config.py`;
- `Settings` exposes no sampling parameter;
- the manifest records what reproduction needs, and every pin is exact;
- every `config/` file parses and has a schema;
- the evidence policy keeps `claim_type` and `support_type` separate;
- the account set is large enough and every row has a stated fit reason.

Seventeen tests. A reader who cannot get them green has an environment
problem, and finding that out now is much cheaper than finding it out in
Chapter 5 while also debugging their first graph.

## 4.7 Claude Code, and where it stops

Claude Code is the harness used to write, test and modify this repository.
It is not part of the application.

The distinction is not stylistic. Claude Code is an interactive development
tool: it reads your files, runs your tests, and edits code under your
supervision. An application is a service that runs unattended and is
accountable to a contract. Building the second out of the first produces a
system that cannot be deployed, cannot be tested without a human in the
loop, and has no defined behaviour when nobody is watching.

So: the application reaches Claude through the Anthropic Messages API via
`langchain-anthropic`, and through nothing else. No production code path
invokes Claude Code, and `pyproject.toml` does not depend on it.

Use it freely for the work in this book. Just do not let it end up inside
the thing you are building.

## 4.8 Evidence of improvement

```bash
uv sync --extra dev
uv run pytest -q
# 17 passed
```

From a clean clone, with no key configured. That is the proof V0 owes: the
harness works, and it works before there is anything to run in it.

```bash
uv run python -m app.manifest
```

produces `RUN_MANIFEST.json` recording twenty-one exact pins, the model
configuration, the runtime, and the autonomy boundary.

## 4.9 Failure demonstration

Worth doing by hand, because the failures are the point of the tests.

Add `import smtplib` to any file under `app/`. Run the suite:

```text
FAILED test_no_send_capability_exists_anywhere
Outbound-messaging capability found in the application:
  app/tools/__init__.py: smtplib
Book 1 never builds a send tool (Chapter 3).
```

Then put `model = "claude-sonnet-5"` in a node:

```text
FAILED test_model_id_is_configuration_not_code
Hard-coded model identifier(s) outside app/config.py: app/nodes/research.py:14
```

Both failures name what to do, not merely what happened. An assertion
message is documentation that runs.

## 4.10 Updated run manifest

`RUN_MANIFEST.json` now exists, at `version_tag: "v0-harness"`. It will gain
fields as versions earn them — skill hashes in Chapter 7, dataset version in
Chapter 12, trace identifiers in Chapter 14 — and never gains a field
speculatively. A manifest field that is always `null` trains readers to stop
reading the manifest.

## 4.11 What remains unresolved

There is a specification, an environment and a proof that both work. There
is no agent.

We do not yet know what a language model, given these tools and this
instruction, actually does with a real company — and until we know, every
architectural decision after this point would be a guess.

Chapter 5 builds the smallest thing that can be observed.

## 4.12 Exercises

1. Run the suite, then break each test deliberately and read its failure
   message. If any message tells you only that an assertion failed, rewrite
   it to say what to do about it.

2. `test_no_send_capability_exists_anywhere` is a tripwire, not a security
   control — it greps for library names. Write down two ways a contributor
   could add send capability without tripping it. Then decide whether that
   makes the test worthless, or worth having anyway, and why.

3. Regenerate the manifest on your machine and diff it against the committed
   one. Every field that differs is a field that is about *your environment*
   rather than *the specification*. Should each one be in there?
