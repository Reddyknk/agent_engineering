# Chapter 12: Evaluation and Quality Detection

## Chapter purpose

This chapter holds the V7 graph stable and adds two related capabilities. An
external evaluation harness measures the product without participating in the
workflow. An in-product reviewer inspects the generated SDR package and returns a
structured quality decision. The reviewer detects defects; it does not correct
them yet.

## Product version

**Starting point:** V7 — reliable single-account graph  
**Result:** V8 — graph with quality detection

## Engineering question

> How will weak output be recognized consistently?

## Learning objectives

By the end of this chapter, the reader should be able to:

- build a representative golden dataset;
- separate unit, contract, scenario, and semantic evaluation;
- evaluate tool trajectories and workflow state transitions;
- define pass criteria and version gates;
- build a structured reviewer contract;
- keep the external evaluator independent of the product; and
- demonstrate both successful detection and controlled failure.

## Seven-Step mapping

**Primary:** Evaluate & Govern  
**Supporting:** Build the Harness, Orchestrate Workflows

## The WidgetWare increment

Add a reviewer after the SDR package generator. It checks requirements, evidence,
qualification logic, outreach claims and safety boundaries, then returns `PASS`,
`REVISE` or `BLOCKED` with scores and reasons. The workflow records the result but
does not loop.

## 12.1 Evaluation is broader than the final answer

An agent can produce a plausible final message while using the wrong source, calling an unnecessary tool, ignoring an exclusion, or skipping approval. Evaluate the entire behavior:

- inputs;
- context assembly;
- model outputs;
- tool calls;
- contracts;
- state transitions;
- evidence usage;
- approval compliance; and
- final artifacts.

## 12.2 Evaluation layers

### Unit tests

Deterministic functions, validators, state transitions, and tools.

### Contract tests

Schema validity, required fields, enumerations, and invariants.

### Scenario tests

End-to-end behavior for representative business situations.

### Semantic evaluation

Whether research, qualification, reasoning, and drafting are useful and correct.

### Safety and boundary tests

Prompt injection, prohibited action requests, missing approval, secret exposure, and unsupported claims.

### Operational tests

Latency, dependency failure, retry behavior, logging, and deployment health.

## 12.3 Build the golden dataset

A useful Book 1 dataset should contain at least:

- clearly qualified accounts;
- clearly unqualified accounts;
- ambiguous accounts;
- missing data;
- contradictory sources;
- stale evidence;
- malicious retrieved instructions;
- unsupported outreach claims;
- approval rejection; and
- dependency failure.

Each case should define expected stable properties rather than one perfect paragraph.

## 12.4 Evaluation criteria

Possible metrics include:

- qualification accuracy;
- evidence coverage;
- unsupported-claim rate;
- contract-validity rate;
- correct workflow-transition rate;
- prohibited-action rate;
- approval-compliance rate;
- tool-selection accuracy;
- average latency; and
- cost per completed case.

Book 1 can begin with simple thresholds and human-reviewed rubrics. Book 2 will extend this into continuous evaluation.

## 12.5 LLM-as-a-judge with caution

A model-based evaluator can score relevance, clarity, grounding, or tone. It should use a specific rubric and structured output. It should not be the only authority for high-risk requirements.

Use deterministic checks for:

- schema validity;
- citations present;
- allowed state transition;
- approval recorded;
- prohibited tool not called; and
- secrets absent.

Use human review to calibrate judge behavior.

## 12.6 The external evaluator and product reviewer are different

The external evaluator measures the system from outside and remains stable across
versions. The product reviewer is an operational component whose output can route
later workflow behavior. Using the product's own reviewer as the only evidence of
quality would allow the system to grade itself.

The external harness should therefore verify whether the reviewer:

- catches known defects;
- avoids rejecting known-good packages;
- returns a valid contract;
- cites the failing dimensions; and
- never overrides deterministic safety requirements.

## 12.7 Generate and review

V8 implements the ADK generate-and-review pattern:

```text
qualification and outreach generator
  → quality reviewer
  → record PASS, REVISE or BLOCKED
  → stop
```

The deliberate stop matters. V8 proves detection before Chapter 13 adds correction.

The reviewer returns a structured object containing dimension scores, blocking
issues, evidence gaps, fields to preserve and revision guidance. Deterministic
code validates the object and records the outcome.

## 12.8 Basic observability

Capture:

- request and workflow identifiers;
- agent and stage names;
- model configuration;
- tool calls and outcomes;
- state transitions;
- validation failures;
- latency;
- token or usage information where available; and
- final status.

Avoid logging secrets, unnecessary personal data, or full sensitive payloads.

Tracing should make it possible to answer: “Why did the reviewer return
`BLOCKED`?” Chapter 14 develops complete AgentOps.

## 12.9 The V8 acceptance gate

V8 is accepted only when:

- all unit and contract tests pass;
- scenario pass rate meets the threshold;
- no test demonstrates autonomous external action;
- evidence coverage meets the threshold;
- known limitations are documented;
- reviewer precision and recall on seeded defects meet the target; and
- reviewer output is contract-valid.

## 12.10 The quality-detection demonstration

Demonstrate more than the happy path.

### Success case

A qualified account produces a research brief, supported qualification, reviewed outreach draft, and approval request.

### Insufficient-evidence case

The workflow stops and requests more research.

### Conflict case

Contradictory evidence remains visible and prevents an unjustified claim.

### Safety case

Retrieved prompt-injection text fails to override policy.

### Approval case

A rejected draft does not proceed.

A trustworthy demonstration shows how the system fails safely.

## Hands-on lab: Add quality detection

1. Build the golden dataset.
2. Run unit, contract, and scenario tests.
3. Add an evaluation command and report.
4. Define the reviewer rubric and structured output.
5. Add the reviewer after generation without a revision path.
6. Seed unsupported claims, weak personalization and missing citations.
7. Measure detection and false-rejection rates.
8. Record model, code, configuration, Skill and dataset versions.
9. Deliver the five-case quality-detection demonstration.

## Evaluation checklist

- Are quality claims backed by a dataset?
- Are workflow trajectories evaluated, not only final prose?
- Are deterministic requirements checked deterministically?
- Can failures be traced to a stage?
- Are secrets and sensitive payloads excluded from logs?
- Is the product reviewer evaluated externally?
- Does the demonstration include safe failure and false-positive analysis?

## Chapter checkpoint

WidgetWare V8 has an evaluated graph and an independent in-product reviewer. It
can identify weak output and explain the failing dimensions. It still stops after
detection; it does not decide how or whether to correct the defect.

## Bridge to Chapter 13

Chapter 13 closes the feedback path with a bounded graph loop. It preserves
accepted work, revises only the rejected artifact and stops on approval, blocking
conditions, budget exhaustion or human escalation.

## Exercises

1. §12.1 lists nine things evaluation should cover beyond the final answer. Pick one of your own past "it works" moments with an agent system, in this course or elsewhere, and check how many of the nine you actually verified versus simply assumed because the final output looked right.
2. §12.3 requires ten kinds of cases in the golden dataset. Look at your own dataset from the Hands-on Lab and identify which of the ten is currently thinnest or missing, and describe a specific WidgetWare account profile that would fill that gap.
3. §12.5 says an LLM-as-a-judge should never be the sole authority for high-risk requirements, listing six things that must stay deterministic instead. Pick one of the six and describe, concretely, what a judge model getting it "almost right" would look like — a plausible-sounding but wrong judgment a rubric alone might miss.
4. §12.9 lists V8 acceptance conditions. Under deadline pressure, which two would
you refuse to waive, and why?
5. §12.10's five-case demonstration includes success, insufficient evidence,
conflict, safety and approval. Which case should a skeptical buyer see first, and
what does it prove that the success case cannot?
