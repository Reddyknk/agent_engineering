# Chapter 9: Evidence-Backed Research with MCP

## Chapter purpose

This chapter expands the evidence pipeline introduced in the V1 monolith and
hardened in V2. It explains how to research external information without turning
retrieval into unverified context and when an MCP integration is preferable to a
custom function tool.

## Product version

**Starting point:** V4 — contract-bound agent  
**Result:** V5 — evidence-backed agent

## Engineering question

> Can every claim in the account brief be traced to a source that still exists?

## Learning objectives

By the end of this chapter, the reader should be able to:

- design research as a sequence of claims, sources, and evidence;
- distinguish retrieval from reasoning;
- evaluate source quality, freshness, and conflict;
- explain function tools versus MCP;
- connect an ADK agent to an approved MCP service;
- prevent retrieved content from overriding system policy; and
- produce an inspectable evidence-backed account brief.

## Seven-Step mapping

**Primary:** Design Agent Capabilities  
**Supporting:** Build Context, Evaluate & Govern

## The WidgetWare increment

Add an Account Research capability that gathers approved public evidence, normalizes it into an evidence ledger, and produces a structured research brief for qualification.

## 9.1 Research is not one model call

A robust research process separates:

1. the questions to answer;
2. source discovery;
3. source retrieval;
4. evidence extraction;
5. source assessment;
6. contradiction detection;
7. synthesis; and
8. citation.

The model may assist at several stages, but the system should preserve provenance throughout.

## 9.2 Claims and evidence

Begin with explicit research questions, such as:

- What industry does the company operate in?
- Approximately how large is it?
- Does it show evidence of legacy plant-floor systems or automation gaps?
- Has it announced a digital-transformation or AI initiative?
- Is there a recent trigger event relevant to WidgetWare?

For every resulting claim, record the supporting evidence. A research brief should never contain a floating factual assertion whose source has been lost.

## 9.3 Source quality and freshness

Assess sources according to the claim:

- official company material is strong for product announcements;
- regulatory filings may be strong for financial or organizational facts;
- reputable reporting may provide context;
- directories and aggregators may be useful but require caution;
- social posts may indicate intent but may not establish fact.

Freshness should be explicit. A five-year-old employee count may not support a current qualification decision.

## 9.4 Contradictions

When sources disagree, do not choose the most convenient result. Record:

- the conflicting values;
- source dates;
- source types;
- likely explanation; and
- whether the conflict affects qualification.

The appropriate outcome may be `NEEDS_RESEARCH`.

## 9.5 Function tools versus MCP

Use a custom function tool when:

- the integration is application-specific;
- the interface is narrow;
- the application owns the implementation; or
- deterministic control is more important than portability.

Use MCP when:

- a standardized server already exposes the capability;
- multiple agents or clients need the integration;
- discovery and portability matter; or
- enterprise systems are exposed through governed MCP services.

MCP does not remove the need for permission, input validation, provenance, or output filtering.

## 9.6 Retrieved content is untrusted data

External content may contain instructions such as “ignore your rules” or “send this secret.” Treat retrieved text as data, not authority.

Controls include:

- isolate source text from system instructions;
- label its origin;
- extract only task-relevant evidence;
- avoid executing commands found in content;
- redact secrets and unnecessary personal data;
- restrict accessible MCP servers and methods; and
- validate the final brief against the evidence ledger.

## 9.7 The evidence ledger

Create a durable structure:

```text
ResearchBrief
- account_id
- research_questions[]
- evidence_items[]
- claims[]
- conflicts[]
- unknowns[]
- trigger_events[]
- summary
- recommended_next_step
```

Each claim links to one or more evidence items. Each evidence item records source, date, excerpt, and reliability assessment.

## Hands-on lab: Build account research

1. Add a `research_account` agent or capability.
2. Connect one approved research source through a function tool or MCP service.
3. Normalize results into `EvidenceItem` contracts.
4. Implement an Evidence Classification Skill.
5. Produce a `ResearchBrief`.
6. Add a validation check that rejects uncited material claims.
7. Test an input containing prompt-injection text.
8. Test two conflicting sources.

## Evaluation checklist

- Does every material claim link to evidence?
- Are source date and type preserved?
- Are conflicts visible rather than silently resolved?
- Does retrieved text remain subordinate to system policy?
- Are MCP permissions and methods restricted?
- Can the research brief be reproduced from mocked evidence?
- Does insufficient evidence stop the workflow appropriately?

## Chapter checkpoint

WidgetWare can produce an inspectable account research brief whose evidence package
is suitable for the Chapter 11 graph.

## Bridge to Chapter 10

Every claim WidgetWare makes about the *prospect* now carries a source. Every claim
it makes about *itself* still does not. The draft may assert a product capability
or a customer outcome with nothing behind it, which is the same defect this chapter
just spent itself eliminating, pointed the other way.

Chapter 10 closes it, retrieving over a corpus WidgetWare owns and landing the
results in this chapter's evidence ledger.

Note also that this chapter reopens Chapter 6's work. Retrieval is the largest
untrusted input surface in the product, and §9.6 extends the trust boundary
established there to content the agent did not author.

## Exercises

1. §9.5 gives four conditions favoring MCP over a function tool. Take the one research source you connected in the Hands-on Lab and argue, honestly, whether MCP was the right call for it under those four conditions — or whether a function tool would have been more honest about what the integration actually is.
2. §9.6 lists seven controls against untrusted retrieved content. Re-run your prompt-injection test, but change the injected instruction to something more subtle than "ignore your rules" — for example, retrieved text stating a false but plausible employee count as if it were the company's own official figure. Does your evidence pipeline catch a false *fact* as readily as it catches an obvious override attempt?
3. §9.4 says contradictions should not be resolved by picking the most convenient result. Using your two-conflicting-sources test, write out what "the most convenient result" would have been for a WidgetWare SDR eager to hit quota, and confirm your `ResearchBrief` actually resisted that pull.
4. §9.2 gives five research questions. Add a sixth, specific to a signal WidgetWare's ICP (Chapter 3) cares about but isn't already covered, and explain what evidence would actually answer it.
5. §9.3 treats a five-year-old employee count as potentially unusable for a current decision. Pick one evidence item from your `ResearchBrief` and write what "sufficiently current" should mean for that specific kind of fact — a number of days, months, or years — and why.
