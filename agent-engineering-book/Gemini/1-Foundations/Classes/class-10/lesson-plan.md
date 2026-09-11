# Class 10 — Loop Engineering with ADK

**Manuscript source:** Book 1, Chapter 11 — Loop Engineering with ADK
**Seven-Step mapping:** Primary: Engineer Loops / Supporting: Orchestrate Workflows, Evaluate & Govern
**Golden solution produced:** `class-10/golden-solution/`
**Starting checkpoint:** `class-09/golden-solution/`

This class closes Book 1. Everything the loop touches today — the single-account workflow, its contracts, its release gate — is unchanged from Class 9. The loop wraps that proven system; it does not modify it.

## 0:00–0:20 — Homework review, common mistakes, golden solution reveal

- **Review homework:** ask participants to walk through their extra golden-dataset case and show it actually changing the release gate's outcome when deliberately broken.
- **Common mistakes to flag:** release gates that stop reporting after the first failure; golden-dataset cases that are technically present but don't cover a real failure mode.
- **Golden solution reveal:** run Class 9's release gate live against the Class 9 checkpoint and watch it pass, then ask: "This proves one run, for one account at a time, on request, is trustworthy. What happens the moment WidgetWare hands you a hundred accounts and goes home for the night?"

## Slide outline (0:20–0:45)

1. Current WidgetWare state: a single-account workflow that's proven good enough to ship, run once, on request
2. Today's dependency: nothing about `run_workflow` changes today — the loop wraps it, unchanged, exactly as Class 9 left it
3. Business objective: run the same proven workflow unattended, across a queue, safely and within stated budgets
4. Core concept: a loop is not `max_iterations` alone (§11.4) — it needs work selection, durable state, verification, and budgets
5. Terminology: the inner ADK reasoning loop vs. the outer engineered loop this chapter adds (§11.2–11.3)
6. Architecture: the five-way per-account decision (§11.8) — CONTINUE, RETRY, STOP, DEFER, ESCALATE
7. Seven Steps mapping: Engineer Loops — the final primary step of Book 1
8. Gemini vs. deterministic code: the workflow's reasoning is unchanged; everything new today — budget checks, decisions, queue selection — is deterministic
9. Security: human approval authority does not change inside a loop (§11.10) — an account processed at 3am unattended gets exactly the same scrutiny as one processed live
10. Today's increment: `loop/budget.py`, `loop/decision.py`, `loop/account_queue.py`, `loop/run_report.py`, `loop/batch_runner.py`, plus two new workflow states
11. Lab architecture: verification before advancing (§11.7) — trust only the state the workflow actually reached, never an agent's own unverified claim
12. Acceptance criteria: the loop stops for a reason it can name, every time

## Kahoot (8 questions)

- Terminology: What are the five outcomes of the loop's per-account decision (§11.8)?
- Terminology: What's the difference between the inner agent loop ADK already runs and the outer loop this chapter adds (§11.2–11.3)?
- Architecture: Why is `max_iterations` alone not an engineered loop (§11.4)?
- Architecture: Why does the state machine need `RETRY_PENDING` and `NEEDS_HUMAN_REVIEW` added, and why is `BLOCKED` no longer terminal once they exist?
- Failure analysis: A restarted batch run re-researches an account it already finished — what's missing?
- Security/governance: Does an account processed inside an unattended batch loop get less approval scrutiny than one processed on request? What does §11.10 say?
- WidgetWare scenario: The loop hits its maximum-attempts limit for one account — CONTINUE, RETRY, STOP, DEFER, or ESCALATE?
- Connecting back: How does the loop's verification-before-advancing step (§11.7) reuse Class 5's contracts and Class 8's state machine?

## Build together (0:55–1:35)

- extend `workflow/state_machine.py` with `RETRY_PENDING` and `NEEDS_HUMAN_REVIEW`, updating `BLOCKED` to route to either instead of being terminal
- `loop/budget.py` — the budget dataclass and stop-condition check
- `loop/decision.py` — the five-way decision function
- `loop/account_queue.py` — work discovery and selection policy
- `loop/run_report.py` — a report every run produces, with `stop_reason`
- `loop/batch_runner.py`'s `run_batch()`, accepting `qualify`/`review`/`draft` as injected callables, exactly like Class 8's `run_workflow`
- wire a `LoopAgent` to the Class 8 workflow

## Test and diagnose (1:35–1:50)

1. Run the loop's scenario tests: a fresh account gets selected, a settled one doesn't.
2. Trigger a failure: restart the process mid-batch and confirm the loop resumes from saved session state instead of reprocessing.
3. Inspect the run report's `stop_reason` and per-status totals.
4. Diagnose: a restart that reprocesses a settled account is almost always a **workflow state** or missing-**permissions**-to-persist issue (an `InMemorySessionService` used where a durable one was needed).
5. Apply the smallest fix — usually swapping in the persistent `SessionService` or fixing what gets checkpointed.
6. Confirm the tool-call budget stop actually fires — this is a real bug class, not a hypothetical: verify the counter that tracks usage against the budget is actually incremented somewhere in the loop.
7. Re-run the full scenario suite.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | The batch loop processes a four-account seed queue (at least one account outside WidgetWare's ICP) and produces a run report naming its `stop_reason` |
| **Diagnostic** | The provided budget test suite currently verifies a single account's retries count against its own attempt limit correctly, but does not verify that one badly-behaved account's retries don't quietly consume the run's `max_consecutive_failures` budget in a way that stops the whole batch prematurely for everyone else. Write a test with one account that fails twice, followed by three healthy accounts, and confirm all three still get processed |
| **Extension** | Add a fifth account to the seed queue specifically designed to trigger `DEFER` — wire a `dependency_available=False` path into `run_batch` for at least one realistic condition, and confirm the deferred account is not discarded and would be eligible again on a subsequent run |

- **Starting checkpoint:** `class-09/golden-solution/`
- **Files participants may modify:** `src/widgetware_sdr/workflow/state_machine.py`, `src/widgetware_sdr/loop/`, `tests/`
- **Expected behavior:** the same proven single-account workflow runs unattended across a queue, within stated budgets, stopping for a nameable reason
- **Tests that must pass:** the loop scenario tests (fresh-account selection, settled-account skip, restart-resume, budget stop, attempt-limit stop)
- **Submission:** one full batch-loop run report (`stop_reason` and status totals)
- **Constraints:** nothing about the single-account workflow (`run_workflow`) changes in this chapter — the loop wraps it, it does not modify it; still no send tool anywhere in the codebase

## Golden solution: `class-10/`

Adds the extended state machine and the full batch loop on top of `class-09/` without changing the single-account workflow. README closes Book 1 with its own conclusion framing: the system now works "for one account at a time, run on request," **and** across a bounded, unattended batch — but still cannot decompose its own goals, collaborate with agents it doesn't own, or prove continuously (not just once) that it still behaves. That gap is Book 2.

## Bridge to Book 2

Book 1 is complete. Book 2 begins its own ten-class course, with its own Class 1 — the same WidgetWare system, now asked to serve many users, remember across time, draw on enterprise knowledge, plan over ambiguous goals, and collaborate with agents it doesn't own. See `../../../2-Enterprise-Agent-Platform/Manuscript/` for the manuscript; Book 2's course companion is built separately.
