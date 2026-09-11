# Chapter 8: Structured Outputs and Agent Contracts

## Chapter purpose

This chapter designs the contracts the rest of the product depends on. Structured contracts allow
probabilistic reasoning to participate safely in deterministic graph workflows.

## Product version

**Starting point:** V3 — skill-driven agent  
**Result:** V4 — contract-bound agent

## Engineering question

> Can another system act on this agent's output without a human reading it first?

## Learning objectives

By the end of this chapter, the reader should be able to:

- explain why free-form prose is an unsafe integration boundary;
- design typed output schemas;
- represent confidence, uncertainty, evidence, and errors explicitly;
- validate and reject malformed responses;
- distinguish semantic evaluation from schema validation; and
- create typed handoffs for later multi-agent workflows.

## Seven-Step mapping

**Primary:** Design Agent Capabilities  
**Supporting:** Orchestrate Workflows, Evaluate & Govern

## The WidgetWare increment

Replace the qualification assistant’s prose-only result with a validated `QualificationResult` contract.

## 8.1 Prose is for people; contracts are for systems

A response such as “Acme looks like a strong opportunity” may be understandable to a person, but software cannot reliably determine:

- the final status;
- the decisive criteria;
- which evidence supports the decision;
- what information is missing;
- whether confidence is sufficient; or
- what the next workflow step should be.

A contract makes those elements explicit.

## 8.2 Designing the qualification schema

A useful result may contain:

```text
QualificationResult
- account_id
- status
- score
- rationale
- matched_criteria[]
- exclusion_reasons[]
- evidence_refs[]
- missing_information[]
- confidence
- recommended_next_step
- errors[]
```

Use enumerations for stable states:

- `QUALIFIED`
- `NOT_QUALIFIED`
- `NEEDS_RESEARCH`
- `BLOCKED`

These values replace casual prose recommendations from the V1 monolith. From V3
forward, only the validated enumeration is a qualification status.

Do not encode workflow state in arbitrary prose.

## 8.3 Confidence is not probability

A model-provided confidence value is a self-assessment, not a calibrated probability. It can still be useful when combined with rules:

- low confidence always routes to research or review;
- missing decisive evidence prevents qualification;
- explicit exclusions override confidence; and
- evaluation measures whether confidence correlates with correctness.

Do not treat `0.92` as scientific certainty merely because it contains decimals.

## 8.4 Evidence references

The result should refer to evidence by stable identifiers rather than copying large passages. An evidence object may include:

```text
EvidenceItem
- evidence_id
- source_type
- source_uri or source_name
- retrieved_at
- claim
- excerpt
- freshness
- reliability
```

The qualification result then lists the evidence identifiers that support each decisive claim.

## 8.5 Validation and repair

A structured-output pipeline should:

1. request the expected schema;
2. parse the response;
3. validate types and required fields;
4. enforce deterministic business rules;
5. optionally request a bounded repair for format errors; and
6. fail safely if the contract remains invalid.

Never silently coerce a materially ambiguous status.

## 8.6 Semantic correctness remains separate

Schema validation can prove that `status` contains an allowed value. It cannot prove that the chosen value is justified.

Use two layers:

- **contract tests** for format, required fields, and invariants;
- **evaluation cases** for reasoning quality, evidence use, and business correctness.

Both are required.

## 8.7 Designing for handoffs

Contracts should be designed for the next component. The future research agent needs a list of missing questions. The outreach agent needs approved facts and positioning angles. The approval interface needs the draft, evidence, and risk flags.

A handoff contract should be sufficient but not bloated. Passing an entire conversation history increases coupling and context noise.

## Hands-on lab: Add typed contracts

Create:

- `src/widgetware_sdr/contracts/evidence.py`;
- `src/widgetware_sdr/contracts/qualification.py`;
- schema validation tests;
- business invariant tests; and
- a serialization format for chapter checkpoints.

Add deterministic rules such as:

- `NOT_QUALIFIED` requires at least one exclusion or failed criterion;
- `QUALIFIED` requires at least one evidence reference;
- `NEEDS_RESEARCH` requires at least one missing-information item; and
- any parsing or policy failure produces `BLOCKED` rather than a guessed result.

## Evaluation checklist

- Can downstream code consume the result without parsing prose?
- Are all workflow states enumerated?
- Are uncertainty and missing information explicit?
- Do decisive claims reference evidence?
- Are deterministic invariants enforced after model output?
- Does invalid output fail safely?

## Chapter checkpoint

The WidgetWare qualification agent now produces a machine-validated result that remains readable to a person. This contract will become the interface between agents and workflow stages.

## Bridge to Chapter 9

The contract states what a qualification decision looks like. It does not make the
claims inside it true. Chapter 9 gives every claim a source, so the evidence
reference in this schema points at something real.

These schemas return throughout the book: Chapter 11 uses them as typed graph-node
inputs and outputs, Chapter 12 adds the reviewer contract, and Chapter 16 uses
explicit control decisions for the outer queue.

## Exercises

1. Take the prose result "Acme looks like a strong opportunity" from §8.1 and write out the six things §8.1 says software cannot reliably determine from it. Now look at your own `QualificationResult` output from the Hands-on Lab — does it actually answer all six?
2. §8.3 warns that a confidence value is a self-assessment, not a calibrated probability. Design one deterministic rule, in plain language, that would prevent your system from treating a 0.95 confidence score as sufficient justification on its own, mirroring the four rules in §8.3.
3. §8.5 lists six pipeline steps ending in "fail safely if the contract remains invalid." Deliberately feed your qualification agent an account likely to produce a borderline or malformed result. Does it reach `BLOCKED`, or does it silently produce something plausible-looking instead?
4. Using §8.7's handoff-design principle—sufficient but not bloated—identify one
field a downstream graph node needs and one field that no later node uses.
5. §8.6 requires two separate layers: contract tests and evaluation cases. Write one evaluation case, in plain language — the account, the expected reasoning — that a contract test could never catch, because the schema would validate a wrong answer just as easily as a right one.
