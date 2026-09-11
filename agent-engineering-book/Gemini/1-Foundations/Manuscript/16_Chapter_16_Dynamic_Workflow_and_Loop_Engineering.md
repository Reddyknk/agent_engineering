# Chapter 16: Dynamic Workflow and Loop Engineering

## Chapter purpose

This chapter takes the evaluated, observable, optimized and parallelized
single-account WidgetWare graph from Chapter 15 and turns it into a bounded process that works through a queue of
accounts. The reader learns that this is a distinct engineering discipline—Loop
Engineering—and implements it as an ADK dynamic workflow with explicit decisions,
automatic node checkpoints and controlled resume.

## Product version

**Starting point:** V11 — parallel, observable single-account graph  
**Result:** V12 — durable operational loop

## Engineering question

> Can the proven workflow process a queue without repeating settled work, losing
> progress or weakening human control?

## Learning objectives

By the end of this chapter, the reader should be able to:

- distinguish the inner agent loop ADK already runs from the outer engineered loop this chapter adds;
- explain why a working, evaluated workflow is still not a safe thing to run unattended;
- use an ADK dynamic workflow to express programmatic loops and conditions;
- explain node checkpoint and resume behavior;
- design durable session state that survives a restart without reprocessing settled work;
- represent a loop's control decision as one of five explicit outcomes; and
- build a loop-ready checklist and apply it honestly to their own implementation.

## Seven-Step mapping

**Primary:** Engineer Loops  
**Supporting:** Build the Harness, Evaluate & Govern

## The WidgetWare increment

Wrap the Chapter 11–15 single-account graph, unchanged, in a dynamic workflow that
reads a queue, processes one account at a time, checkpoints meaningful nodes and
stops with a named reason.

## 16.1 What the single-account graph did not answer

The graph answers one question well: given one account, produce one evaluated,
approved-or-rejected recommendation. A system meant to run WidgetWare's actual
sales-development motion must answer questions the single-account workflow was
not designed to answer:

- Where does the *next* account come from?
- Has this account already been processed in an earlier run?
- Should a failed research call be retried, and how many times before giving up?
- Should the system move on to another account, or stop entirely?
- When must a person intervene rather than the system deciding on its own?

None of these questions are about qualifying one account better. They concern
control around the workflow. Chapters 3–12 deliberately left them unanswered
until the single-account graph was secured, evaluated, optimized and observable.

## 16.2 The inner loop ADK already runs

Every ADK agent already executes an inner loop the moment it reasons: it observes the current input and state, decides whether to call a tool or respond, acts, and observes the result — repeating until it has enough to answer. This is real, it works, and Chapters 4 through 9 already built on top of it without needing to touch it directly.

```
Observe → Reason → Act → Observe
```

Chapter 13 already added a bounded inner quality loop. This chapter adds a different
loop around the complete account workflow.

## 16.3 The outer loop this chapter adds

The outer loop is what decides, across many separate invocations of the workflow, what to work on next and whether to keep going:

```
Trigger
   ↓
Discover work
   ↓
Select the next eligible account
   ↓
Invoke the single-account graph for that account
   ↓
Verify the outcome
   ↓
Persist state
   ↓
Continue, retry, stop, defer, or escalate
```

ADK gives this outer loop a durable home in a dynamic workflow. The orchestrator
uses ordinary Python conditions and iteration while invoking named workflow nodes.
Completed nodes are checkpointed; after interruption, the orchestrator can rerun
and obtain completed child results from checkpoints instead of executing them
again. The single-account graph remains unchanged inside this outer control layer.

## 16.4 A loop is not a `for` statement alone

It is tempting to write the smallest program that repeats the workflow:

```python
node(rerun_on_resume=True)
async def process_queue(ctx, queue):
    for account in queue[:50]:
        await ctx.run_node(single_account_workflow, account)
```

This can run. It is not yet an engineered loop. The iteration limit says nothing
about eligibility, settled work, verification, budgets or operator control:

- No work-selection policy — nothing says which account is next, or whether one was already handled.
- No durable state — an `InMemorySessionService` restart loses everything, including which accounts were already processed.
- No verification — a malformed or incomplete result is treated the same as a good one.
- No per-account attempt limit — one bad account can consume retries meant for the whole run.
- No cost or time budget — nothing bounds what the run actually costs.
- No escalation path — nothing routes an account the loop cannot resolve to a person.
- No recovery strategy — a restart has no way to resume, only to start over.

The principle worth carrying forward is unchanged: **repetition creates a loop.
State, verification, budgets and control make it an engineered loop.**

## 16.5 Durable state with SessionService

A `Session`'s state is not inherently durable — durability is a property of the `SessionService` backing it, not of the `Session` object itself. ADK's `Session` separates a record — its `state`, a scratchpad of serializable values — from the transient event stream of one conversation, but that record only outlives a restart if the `SessionService` implementation behind it is built to persist it. Which implementation backs a session decides whether the record survives a restart:

- `InMemorySessionService` — state lives in process memory. Fine for a single lab run; gone the moment the process exits.
- `DatabaseSessionService` (or `VertexAiSessionService` in a managed deployment) — state is written durably and reloaded on restart.

Book 1 uses the persistent option for the batch loop's own bookkeeping, and keeps that bookkeeping simple and inspectable — two small structures, not a schema the reader has to reverse-engineer:

Run-level state:

- `run_id`, `status`, `started_at`
- `accounts_processed`, `successes`, `failures`
- `current_account_id`
- `stop_reason`

Per-account state:

- `account_id`, `status`, `attempts`
- `research_status`, `qualification_result`
- `draft_status`, `approval_required`

"Which stage is this account in" should never be a sentence buried in a model's
response. It is one value from a small explicit set, following the deterministic-
versus-probabilistic boundary Chapter 3 already established. A model may recommend
a transition. Code decides whether it is allowed.

## 16.6 Explicit states and transitions

```
RECEIVED → RESEARCHING → RESEARCH_COMPLETE → QUALIFYING

QUALIFYING     → REVIEW_REQUIRED        (QualificationResult: QUALIFIED)
               → DISQUALIFIED, terminal (QualificationResult: NOT_QUALIFIED)
               → RESEARCHING, again     (QualificationResult: NEEDS_RESEARCH)
               → BLOCKED, terminal      (QualificationResult: BLOCKED)

REVIEW_REQUIRED → DRAFT_READY → AWAITING_APPROVAL

AWAITING_APPROVAL → APPROVED, terminal
                  → REJECTED, terminal
                  → DRAFT_READY, again  (revision requested)
                  → BLOCKED, terminal
```

This extends the single-account state machine introduced with the Chapter 11 graph
and refined in Chapter 13. The outer loop does not replace it; it adds two states
that make sense when accounts are processed as a queue:

- `RETRY_PENDING` — a recoverable failure occurred and attempts remain.
- `NEEDS_HUMAN_REVIEW` — the loop is not authorized to resolve this account on its own.

An account that has failed twice and has one attempt left is in a different, nameable condition from one that has failed permanently. The session state should say which, not leave it implied by the absence of a result.

## 16.7 Verification before advancing

Every stage the loop advances past should be checked deterministically before the
loop trusts it—the same contract principle used by the Chapter 11 graph:

- the workflow's output validates against its contract (Chapters 8 and 11);
- decisive claims carry evidence references (Chapters 9 and 10);
- this account has not already reached a settled status in an earlier run;
- the draft contains no claim the Evidence Reviewer did not approve (Chapter 12); and
- no external send action has occurred — Book 1 still contains no send tool.

A model-based judge may score whether the reasoning was useful, but deterministic
code still verifies shape and policy compliance, following Chapter 12's separation
of semantic judgment from hard requirements.

## 16.8 Budgets and the five-way decision

State every limit before the loop starts running, not after it has already spent the budget:

- maximum accounts per run;
- maximum attempts per account;
- maximum wall-clock runtime;
- maximum tool calls or estimated token cost; and
- maximum consecutive failures.

Any one of these being reached is a legitimate reason to stop, alongside simply running out of eligible accounts. After each account, the loop makes exactly one explicit decision — never an implicit fallthrough:

- **CONTINUE** — the account reached a state with no further automated work remaining (`APPROVED`, `REJECTED`, `DISQUALIFIED`, or `AWAITING_APPROVAL`); move to the next eligible account.
- **RETRY** — a recoverable failure occurred and attempts remain; requeue the account.
- **STOP** — a budget was reached, or no eligible accounts remain; end the run cleanly.
- **DEFER** — the account cannot proceed right now (a dependency is unavailable) but has not failed; leave it for the next run.
- **ESCALATE** — the account needs a decision the loop is not authorized to make; route it to `NEEDS_HUMAN_REVIEW` rather than retrying or discarding it.

**A case worth naming explicitly: reaching `AWAITING_APPROVAL` is a `CONTINUE`, not a `DEFER`.** The account has done everything the automated workflow can do — there is no further automated work waiting on it. The loop persists the approval package, removes that account from the automated work queue, and moves on to the next eligible account. Human approval happens asynchronously, outside the loop's own iteration; the loop does not wait for it, poll for it, or block other accounts on it. `DEFER` means something different: a dependency is temporarily unavailable and the account might become eligible again on a *later automated run* — not one waiting on a person. Because Book 1 has no send tool, there is nothing left to unblock once approval eventually arrives; the approval record itself is the terminal artifact for that account.

The dynamic workflow returns a structured control decision after each account.
Programmatic logic assigns the next action and records the reason. A template
`LoopAgent` and its escalation signal remain useful for compact fixed refinement
loops, as shown in Chapter 13, but the outer queue requires richer programmatic
selection, budgets, checkpoint-aware resume and multiple terminal outcomes.

## 16.9 Checkpoints and resume

A durable session is only useful if the loop actually writes to it at meaningful moments and actually reads it back on restart. Checkpoint after each of: an account being selected, research completing and passing verification, qualification completing, a draft being created, and the run's overall counters being updated. A process restarted against a `DatabaseSessionService`-backed session should read the last checkpoint and resume from there — it should not re-research a company whose profile is already saved, and it must not re-send anything, though Book 1 makes that guarantee structurally by never building a send tool in the first place rather than by trusting the loop to remember not to call one.

## 16.10 Human control does not change inside a loop

The autonomy boundary from Chapter 3 still applies inside a loop. The workflow
does not get to renegotiate approval merely because a person is not watching it:

| Action | Authority |
|---|---|
| Research an account | automatic |
| Summarize evidence | automatic |
| Recommend a qualification status | automatic |
| Draft outreach | automatic |
| Send outreach | human approval required |
| Modify a CRM record | human approval required |
| Delete a business record | prohibited |

Everything above the line can run across as many accounts as the budget allows.
Everything below it stops that account at `AWAITING_APPROVAL` until a person acts,
preserving the human-input boundary established in Chapter 11.

## 16.11 The loop-ready checklist

Before this loop is trusted to run unattended, it should answer yes to each of the following:

- Is there a defined goal for what the loop is trying to accomplish?
- Is there a clear source of work, and a policy for selecting from it?
- Is state durable — does it survive a restart?
- Are the states an account can be in explicit, not implied by prose?
- Does the loop checkpoint after meaningful stages, not only at the end?
- Is every stage verified deterministically before the loop trusts it?
- Is there an attempt limit per account?
- Are there time, cost, and tool-call budgets?
- Are there explicit stop conditions, checked every iteration?
- Is there a path to escalate to a person, distinct from simply failing?
- Does the run produce a report a person can audit after the fact?
- Is there a way for an operator to stop the loop from outside it?

A system that cannot answer yes to all twelve is not yet an engineered loop, whatever else it does well.

## Hands-on lab: Build the batch loop

Implement:

- `src/widgetware_sdr/loop/account_queue.py` — work discovery and the work-selection policy: the next account whose status is `RECEIVED` or `RETRY_PENDING`, never one already settled;
- `src/widgetware_sdr/loop/budget.py` — the budget dataclass and a stop-condition check run once per iteration, before any account is selected;
- `src/widgetware_sdr/loop/decision.py` — a function returning exactly one of `CONTINUE` / `RETRY` / `STOP` / `DEFER` / `ESCALATE`, given an account's state and the current budget check;
- `src/widgetware_sdr/loop/run_report.py` — a report every run produces, always including its `stop_reason` and per-status totals;
- a dynamic workflow node that invokes the Chapter 11–15 single-account graph and
  uses checkpoint-aware resume;
- a persistent `SessionService` for application session state; and
- a small seed queue of at least four accounts, at least one deliberately outside WidgetWare's ICP.

Add scenario tests for: a fresh account gets selected and a settled one doesn't; a recoverable failure retries up to the configured limit and no further; a restarted run resumes from saved session state instead of reprocessing; the loop stops at both the account limit and a budget limit; and every run's report names a stop reason.

## Evaluation checklist

- Does the loop select a new account and skip a settled one correctly?
- Does session state survive a simulated restart?
- Is every stage verified before the loop advances past it?
- Does a recoverable failure retry only up to its configured limit?
- Does the loop stop at every budget it declares, not only the account limit?
- Does every run produce a report naming its stop reason?
- Does anything in the loop send an external message automatically? (It must not.)

## Chapter checkpoint

WidgetWare V12 can now work through a queue of accounts within limits it states in
advance, resume from completed nodes and stop for a reason it can name. Nothing
about the single-account graph changed; this chapter added control around it.

## Bridge to Chapter 17

Chapter 17 packages the V12 system as a repeatable release. It connects code,
configuration, model, evidence, trace, recording and artifact lineage, then tests
deployment, replay, rollback and cleanup.

## Exercises

1. Using §16.4's list of things `max_iterations` alone doesn't give you, pick a repeating process you already run today — a script, a cron job, a manual routine — and score it against the same list. How many of the seven are actually present?
2. Using §16.8's five-way decision (CONTINUE, RETRY, STOP, DEFER, ESCALATE), write out, in plain language, what should happen to a WidgetWare account whose research completes successfully but whose qualification cannot be computed because the ICP configuration is missing a required field. Which decision applies, and why not one of the other four?
3. Run the batch loop from the Hands-on Lab to completion, then interrupt it mid-run on a fresh copy and restart it. Confirm from the session state itself, not from re-reading the code, exactly which accounts were re-processed and which were correctly skipped.
4. Using §16.10's authority table, audit the outer workflow: is outreach
structurally impossible without approval, as Chapter 11 required, or did the loop
introduce a new path around the control?
5. Using §16.11's twelve-item loop-ready checklist, audit your own Hands-on Lab implementation honestly. If you find one item it does not fully satisfy, what would closing that gap require?
6. §16.2 and §16.3 distinguish the inner agent loop, the Chapter 13 quality loop
and the outer operational loop. Before Book 2 introduces planning, predict whether
planning needs another loop or a new policy inside one of these existing layers.
