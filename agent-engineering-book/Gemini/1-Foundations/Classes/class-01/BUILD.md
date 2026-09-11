# Building Class 01 with Antigravity

Goal: a merged charter-and-harness checkpoint — the five charter documents, plus an installable `widgetware_sdr` package, a deterministic health check, and one command that verifies the environment, then formats, lints, type-checks, and tests everything. `golden-solution/` in this folder is the reference; build your own copy in a separate directory first, then diff.

## Prerequisites

- **`../SETUP.md` complete** — Antigravity, Git, Python 3.11+, `gcloud`, and a Google Cloud project with billing enabled. One-time, done once.
- **Your Google Cloud project exists before you finish this class.** Nothing in Class 1 calls a model, so it is tempting to defer. Don't: Class 2 onward assumes the project, the `gcloud` install, and working Application Default Credentials. Confirm with `gcloud auth application-default print-access-token >/dev/null && echo OK`.
- You've read Book 1, Chapters 1 and 2 (`../../Manuscript/03_Chapter_01_From_Language_Models_to_Agent_Engineering.md` and `../../Manuscript/04_Chapter_02_Building_with_Antigravity.md`).

## Part 1: The charter

1. Open a working directory and start Antigravity.

2. Before writing anything, work the framework question through conversation. Paste the chapter's WidgetWare increment and ask:

   > "WidgetWare sells software that helps manufacturing and industrial-automation companies modernize plant operations and adopt AI-enabled automation. Its SDR process needs to research a target company, evaluate fit, and draft outreach. Using the distinctions between a model, an assistant, a workflow, an agent, and an agentic system — which is this task, and why? Where does it sit on the seven-level autonomy spectrum (answer-only, recommend, draft, prepare, execute-with-approval, execute-within-policy, open-ended)?"

3. Push back on the first answer. Ask Antigravity to argue the *other* side: "Make the case this should be a fixed deterministic workflow instead of an agent." A good answer concedes real tradeoffs — cost, latency, the value of adaptability.

4. Draft `docs/acceptance-criteria.md` yourself, in your own words, before looking at `golden-solution/docs/acceptance-criteria.md` — the point of this class is having your own opinion about what "success" means. Split it into two sections from the start: what this checkpoint can prove today, and what the finished product will need later. Each criterion in the first section should be something a person (or a test) could check mechanically.

5. Write `README.md`, `SPEC.md`, `docs/widgetware-business-brief.md`, and the three scenario descriptions under `tests/scenarios/` (a clearly qualifying account, a clearly disqualifying account, and a genuinely ambiguous one). Structure each scenario as a fixture pair too: `tests/fixtures/accounts/<id>.yaml` and `tests/fixtures/expected/<id>.yaml` — Class 2 needs this shape, and doing it now is good practice.

## Part 2: The harness

6. Give Antigravity a deliberately bad task first, and watch what happens:

   > "Set up the project."

7. Now give it the properly scoped version, following Book 1 §2.2's disciplined cycle (state objective, provide spec, ask for a plan, review, permit bounded implementation, inspect the diff, run tests, accept/revise/revert):

   > "Set up a Python package workspace for WidgetWare SDR Lab, following the repository structure in `SPEC.md`. I need: `pyproject.toml` with `pytest`, `ruff`, and `mypy` as dev dependencies; a `src/widgetware_sdr` package with an `__init__.py` and a deterministic `health_check()` function returning a status payload (no network call, no model call); a matching test in `tests/unit/`; `config/`, `docs/`, and `tests/{unit,contracts,scenarios,fixtures}` directories; a `.env.example` documenting `GOOGLE_CLOUD_PROJECT` and `WIDGETWARE_MODEL_ID` with no real values; a `.gitignore` covering `.venv/`, `__pycache__/`, `.env`, and generated caches; `scripts/verify_environment.py` checking Python version, required files, package importability, and the absence of a committed `.env`; and `scripts/check.sh` running verification, `ruff format --check`, `ruff check`, `mypy`, and `pytest` in that order, failing on the first error."

8. Compare what Antigravity produced for step 6 against step 7 — number of files touched, assumptions made, whether it added anything you didn't ask for. This comparison is Book 1 §2.6's actual lesson.

9. Ask Antigravity to inspect the project and produce a gap report against `SPEC.md`:

   > "Compare the current repository state against SPEC.md and docs/acceptance-criteria.md Section A. What's missing or inconsistent?"

   It will surface at least one real gap. Fix it before moving on.

10. Write `.agents/rules/engineering.md`, `.agents/rules/security.md`, `.agents/workflows/baseline-check.md`, `CONTRIBUTING.md`, and `SECURITY.md` — short, concrete, and specific to this repository, not generic advice. `golden-solution/`'s versions are a reasonable model for length and tone.

11. Write `docs/architecture.md` and at least the three architecture decision records in `docs/architecture-decisions/` — why autonomy stops at "Prepare," why no send capability exists in code, why the harness is part of Class 1 now. An ADR should explain the reasoning behind a decision, not just restate the decision.

12. Run the check script. Fix anything that fails.

13. Make your first commit.

## Verify

```
cd my-work/gemini-book-1/class-01
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expect `verify_environment.py`, `ruff format --check`, `ruff check`, `mypy`, and `pytest` to all pass — 18 tests in the reference solution, though yours may have a different count if you wrote additional tests. No live-model tests exist at this checkpoint; nothing here should ever need Google Cloud credentials, even though you have them by now.

## Compare against the reference

`golden-solution/tests/unit/test_repository_contract.py` is the reference for what "the checkpoint itself is verified" means at this stage — not just that code runs, but that the boundary holds (no Gemini or ADK import, no send-capable function, no committed credential, fixture pairs structurally consistent). If your own tests check materially less than this, add what's missing.

## Grade it

Passing `./scripts/check.sh` proves the harness works. It doesn't prove your charter is well-scoped, your acceptance criteria are genuinely testable, or your architecture decisions explain real reasoning rather than restating the decision. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md`.
