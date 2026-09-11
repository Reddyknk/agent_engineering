# Agent Engineering with Gemini, ADK & Antigravity — Instructor Course (Book 1)

A ten-class, cumulative delivery of the Gemini edition's **Book 1** — two hours per class, one per Book 1 chapter, same instructional rhythm every class, one running WidgetWare SDR Lab codebase from Class 1 through the close of Book 1.

Book 2 is its own separate ten-class program (one per Book 2 chapter), continuing the same WidgetWare system into enterprise-platform territory. It is not part of this directory's numbering — see [`../../2-Enterprise-Agent-Platform/Manuscript/`](../../2-Enterprise-Agent-Platform/Manuscript/) for the manuscript; its own `Classes/` companion follows the same pattern as this one once built.

This directory is the instructor's companion to the manuscript in [`../Manuscript/`](../Manuscript/). It does not replace the book — it sequences it into a live, cohort-paced program with a fixed classroom cadence, a golden-solution checkpoint per class, and a three-level homework pattern.

## Two tracks, one set of golden solutions

This course exists in two forms, built from the same manuscript and the same `class-0N/golden-solution/` checkpoints:

- **Classroom track** (this README, `00_Course_Framework.md`) — live, instructor-led, two-hour cadence.
- **Self-paced track** (`SETUP.md`, `HOW-TO-WORK-A-CLASS.md`, `GRADING-RUBRIC-TEMPLATE.md`, and each class's `BUILD.md`/`GRADING.md`) — work through the same material alone, building each checkpoint yourself with Antigravity and grading your own submission with an LLM judge before moving on. Modeled on the Claude edition's course infrastructure at `../../../Claude/book-1-foundations/course/`.

Neither track is the "real" one — pick whichever fits how you're actually delivering or taking the course.

## Start here

- **Classroom facilitators:** [`00_Course_Framework.md`](00_Course_Framework.md) — the fixed cadence, the learning loop, the golden-solution specification, the homework pattern, and the slide/Kahoot/testing cadences that apply to every class without exception.
- **Self-paced learners:** [`SETUP.md`](SETUP.md), then [`HOW-TO-WORK-A-CLASS.md`](HOW-TO-WORK-A-CLASS.md).

## The ten classes (Book 1, one chapter each)

| Class | Manuscript source | Main capability | Golden solution |
| ----: | ------------------ | ---------------------------------------------------------- | --- |
| [1](class-01/) | Book 1, Ch. 1–2 | Foundations, the WidgetWare specification, and the Antigravity repository harness (folds in course orientation) | ✅ verified — 18 passed |
| [2](class-02/) | Book 1, Ch. 3 | Gemini context and instruction architecture | ✅ verified — 8 passed |
| [3](class-03/) | Book 1, Ch. 4 | First ADK agent (embedded procedure, no Skills yet) | ✅ verified — 18 passed, 3 skipped |
| [4](class-04/) | Book 1, Ch. 5 | Skills and reusable agent capabilities | ✅ verified — 17 passed, 3 skipped |
| [5](class-05/) | Book 1, Ch. 6 | Structured outputs and agent contracts | ✅ verified — 29 passed, 3 skipped |
| [6](class-06/) | Book 1, Ch. 7 | Tool engineering | ✅ verified — 44 passed, 3 skipped |
| [7](class-07/) | Book 1, Ch. 8 | MCP and evidence-backed research | ✅ verified — 60 passed, 3 skipped |
| [8](class-08/) | Book 1, Ch. 9 | Multi-agent workflow and human approval | ✅ verified — 90 passed, 3 skipped |
| [9](class-09/) | Book 1, Ch. 10 | Evaluate, deploy, and demonstrate (no loop yet) | ✅ verified — 109 passed, 3 skipped |
| [10](class-10/) | Book 1, Ch. 11 | Loop engineering with ADK — closes Book 1 | ✅ verified — 140 passed, 3 skipped |

"Passed"/"skipped" counts are from `pytest` run with no live Gemini credentials in the environment — the skipped tests are the semantic, live-model scenario tests in `tests/integration/`, which require `GOOGLE_API_KEY` or a configured Vertex AI project to actually run. Every checkpoint is cumulative: `class-0N/golden-solution/` contains everything from `class-0(N-1)/` plus that chapter's own increment, verified by actually running its own test suite from a clean install, not by inspection.

Each class folder contains: the narrative lesson plan, slides, Kahoot questions, homework, a facilitator "common mistakes" briefing (Class 2 onward), the golden-solution checkpoint with its own `KNOWN_FAILURE_CASES.md` and completion checklist, and the self-paced track's `BUILD.md`/`GRADING.md`.

## What you need before Class 1

- The manuscript itself (Book 1), for reference during lecture prep.
- Kahoot (or an equivalent live-quiz tool) set up for the 0:55–1:05 segment.
- A shared conventions document for participants: Python version, package manager, how `.env.example` works, and how to submit homework artifacts.
- Nothing to seed for Class 1 itself — `classes/class-01/golden-solution/` is the from-scratch starting point, and each subsequent class's golden solution builds on the previous one cumulatively.
- (Self-paced track only) Follow `SETUP.md` instead — it covers forking the repository and tool installation, which the classroom track's facilitator handles once for the whole cohort instead.
- Starting Class 3, a way to actually call Gemini (`GOOGLE_API_KEY` or a Vertex AI project) is needed to run the live-model tests and see the agents reason for real — not required to build or gate-test any checkpoint.

## Grading, in either track

`GRADING-RUBRIC-TEMPLATE.md` plus each class's `GRADING.md` give a repeatable way to have Antigravity (or Gemini directly) judge a submission qualitatively — on top of, not instead of, the deterministic `pytest` gate check every class from Class 2 onward already has. Self-paced learners use this as a required step (`HOW-TO-WORK-A-CLASS.md` step 10); classroom facilitators can use it as a supplement to the informal homework review already built into the 0:00–0:10 segment.

## A note on scope

This program does not invent a different pedagogy from the manuscript — it applies the manuscript's own "probabilistic reasoning inside deterministic boundaries" discipline to the classroom itself. The cadence is deterministic and fixed; what participants build with it is where the reasoning happens.
