# Chapter 17: Repeatable Deployment, Recording and Replay

## Chapter purpose

This chapter turns the evolved SDR workflow into a releasable product. It combines
deployment, release evidence, artifact lineage, event recording, replay, rollback
and cleanup. Repeatability does not mean that a probabilistic model produces
identical prose; it means that the system can reconstruct the conditions, evidence,
versions and decisions that produced a result.

## Product version

**Starting point:** V12 — durable operational loop  
**Result:** V13 — repeatable deployed SDR product

## Engineering question

> Can this version be deployed, audited, compared, reproduced and safely replaced?

## Learning objectives

By the end of this chapter, the reader should be able to:

- define a release manifest and lineage chain;
- choose a Google Cloud runtime deliberately;
- deploy with a least-privilege identity;
- configure health, logging, tracing and rollback;
- record ADK events and generated artifacts;
- explain what replay can and cannot prove;
- apply release gates to success and controlled failure; and
- remove resources safely when the learning environment ends.

## 17.1 The release unit

A release is more than a container image. The V12 release manifest records:

- source commit and application version;
- ADK and dependency versions;
- prompt, policy and Skill versions;
- graph and dynamic-workflow versions;
- model identifiers and configuration;
- evaluation dataset and rubric versions;
- infrastructure and region;
- service account identity;
- artifact and recording locations;
- release-gate report; and
- rollback target.

## 17.2 Runtime choice

Book 1 uses one documented deployment path and treats alternatives as explicit
substitutions. Cloud Run provides a transparent containerized application model.
A supported managed agent runtime can provide tighter agent lifecycle integration.
The choice is based on operational requirements, not on which service creates the
most impressive diagram.

The deployment must include authentication, environment-specific configuration,
least privilege, health checks, versioning, logging, tracing and rollback.

## 17.3 Artifact lineage

Every account package links to:

- the request and account identifier;
- accepted evidence package;
- qualification decision;
- review and loop decisions;
- human approval result;
- workflow and model versions;
- trace and session identifiers; and
- final artifact checksum or version.

This creates an evidence chain without embedding every sensitive payload in the
manifest.

## 17.4 Recording

ADK session events can be exported as a portable record of what agents produced
and changed. A recording is useful for review, teaching, regression investigation
and reconstructing the narrative of a run without new model calls or side effects.

Recordings must be governed like other operational data: access, retention,
redaction, tenant scope and deletion all matter.

## 17.5 Replay is not re-execution

Replaying recorded events can reconstruct a sequence for inspection. It cannot
recover timing, true parallel overlap, hidden tool execution or model physics that
the recording never captured. Replayed spans are reconstructed telemetry and must
be labeled accordingly.

For exact behavioral verification, rerun the released version against the same
test case under controlled configuration. For cheap narrative inspection, replay
the recording. The two answer different questions.

## 17.6 Release gates

V12 cannot be released unless:

- unit and contract tests pass;
- scenario and semantic evaluation meet thresholds;
- the adversarial case fails safely;
- approval cannot be bypassed;
- evidence coverage meets its target;
- latency and cost remain within budgets;
- deployment identity is least privilege;
- telemetry content has been reviewed;
- smoke tests pass; and
- rollback and cleanup have been exercised.

## 17.7 Demonstrate controlled failure

The final demonstration includes:

1. qualified account;
2. insufficient evidence;
3. contradictory evidence;
4. retrieved prompt injection;
5. rejected human approval;
6. partial enrichment failure;
7. loop budget exhaustion; and
8. resume after interruption.

A trustworthy demonstration shows both successful production and safe refusal.

## 17.8 Rollback and cleanup

Rollback identifies the previous known-good application and configuration, not
only the previous code commit. Cleanup removes deployed revisions and stored data
according to the lab's retention plan, while retaining any explicitly required
evaluation report or anonymized learning artifact.

## Hands-on lab: Release V12

1. Freeze the source and configuration versions.
2. Generate the release manifest.
3. Run the complete evaluation and security suite.
4. Build and deploy to the selected Google Cloud runtime.
5. Run authenticated smoke tests.
6. Verify logs, traces, metrics and artifact persistence.
7. Record one complete invocation.
8. Replay it and document the information lost in replay.
9. Exercise rollback to the prior version.
10. Run the cleanup procedure.

## Evaluation checklist

- Can every artifact be connected to its release and evidence?
- Is the runtime choice explained?
- Are deployment and local identities distinct?
- Can the release be recreated from versioned inputs?
- Is replay clearly distinguished from re-execution?
- Are release gates measurable?
- Does the demonstration include controlled failure?
- Have rollback and cleanup been tested?

## Chapter checkpoint

WidgetWare V12 is a bounded, secured, reliable, evaluated, optimized, observable
and repeatable SDR product. It can process a controlled queue of accounts, resume
after interruption, preserve evidence, request human approval and explain its
decisions. It remains intentionally limited to one application and one bounded
organizational context.

## Bridge to Book 2

An application is not yet an enterprise platform. Book 2 asks how multiple teams,
tenants, knowledge domains, agents, identities and workflows share infrastructure
without sharing authority or risk.

