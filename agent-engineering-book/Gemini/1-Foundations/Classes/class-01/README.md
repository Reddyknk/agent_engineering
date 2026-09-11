# Class 1 — Agent Engineering Foundations and the Antigravity Repository Harness

**Manuscript source:** Book 1, Chapters 1 and 2
**Seven-Step mapping:** Primary: Frame the Use Case, Build the Harness / Supporting: Design Agent Capabilities, Evaluate & Govern
**Starting checkpoint:** none (first class)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 18 passed)

Class 1 merges the former Class 1 (charter) and Class 2 (repository harness) into one class. This is the first runnable, reproducible, known-good baseline in the course — not a documents-only checkpoint. See `golden-solution/docs/architecture-decisions/0003-repository-harness.md` for why.

## Prerequisites

The Class 1 build itself is fully offline — no model call happens until Class 3. But **Class 1 is where you create your Google Cloud project**, because every class from Class 2 onward assumes it already exists.

Follow the "Google Cloud" section of [`../SETUP.md`](../SETUP.md): start the free trial ($300 credit, 90 days; a payment method is required for identity verification and is not charged — a debit card is enough, and UPI works from India; prepaid and virtual cards do not), create a project, install `gcloud`, and run all four auth commands — including `gcloud auth application-default login`, which is the one people skip.

There is one model path in this course and it is Google Cloud. See [`../CONVENTIONS.md`](../CONVENTIONS.md).

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan: cadence, rationale, and section-by-section detail |
| [`common-mistakes.md`](common-mistakes.md) | 0:20–0:30 | Mistakes to watch for as participants draft the charter and stand up the harness for the first time |
| [`slides.md`](slides.md) | 0:30–0:55 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:55–1:05 | 8 quiz questions, Kahoot-ready, with answer key |
| [`golden-solution/`](golden-solution/) | reference throughout, comparison at 1:50–1:57 | The reference checkpoint: charter, architecture, agent rules, installable package, health check, one-command gate |
| [`homework.md`](homework.md) | 1:57–2:00 | The three-level homework assignment, submission spec, and constraints |
| [`BUILD.md`](BUILD.md) | self-paced track | Step-by-step instructions to build this checkpoint yourself with Antigravity |
| [`GRADING.md`](GRADING.md) | self-paced track (or facilitator supplement) | Class-specific LLM-judge criteria, used with `../GRADING-RUBRIC-TEMPLATE.md` |

## Running the golden solution

```bash
cd golden-solution
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expected: `verify_environment.py`, `ruff format --check`, `ruff check`, `mypy`, and `pytest` (18 tests) all pass — no Google credentials, no network access, no Gemini or ADK runtime involved.

## Class 1 exception — opening cadence

Class 1 has no previous homework and no previous golden solution to reveal. Use this opening instead of the standard 0:00–0:30:

|      Time | Segment |
| --------: | ------- |
| 0:00–0:10 | Introductions, course goals, participant expectations |
| 0:10–0:20 | Ten-class course architecture and the final outcome (the unattended batch loop) |
| 0:20–0:30 | WidgetWare SDR case study, repository structure, and the cumulative learning model |

From 0:30 onward, follow the standard cadence, adapted for this class's two-part build segment — see `lesson-plan.md`.

## Facilitator checklist

- [ ] Participants leave with their own committed `docs/acceptance-criteria.md`, drafted before seeing `golden-solution/`'s version
- [ ] All 8 Kahoot questions run, especially the one confirming participants understand real code now exists — a common early confusion carried over from the previous course structure
- [ ] Every participant's `./scripts/check.sh` passes before homework is assigned
- [ ] Homework's Required/Diagnostic/Extension levels explained, with the submission format stated explicitly
- [ ] Every participant has a Google Cloud project with billing enabled, and `gcloud auth application-default print-access-token` succeeds for it — the whole course depends on this and Class 3 is too late to discover it missing
