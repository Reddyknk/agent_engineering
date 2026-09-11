# Agent Engineering with Gemini, ADK & Antigravity

## Book 2: From Agent Application to Enterprise Agent Platform

### Turn a Working Agent Into a Governed Enterprise Platform

Book 2 transforms WidgetWare SDR from a bounded application into an enterprise
agent platform. It also changes the reader's altitude — from application builder
to enterprise architect and transformation consultant.

**The source of truth for this book's structure is Book 1's
`19_Introduction_to_Book_2.md`.** The chapter list, the ten architectural
questions and the expanded Seven Steps are defined there. When the two disagree,
Book 1's introduction wins and this manuscript is wrong.

The previous Book 2 manuscript, titled *Advanced Architectures*, was written
against an earlier Book 1 and was retired on 2026-09-04. It remains in git
history at commit `243470c` if any of its prose is worth recovering.

## Prerequisite

Book 2 assumes the completed Book 1 system: a WidgetWare SDR application that
researches accounts with sourced evidence, qualifies against an ICP, drafts
outreach and stops for human approval. An explicit ADK graph controls the
single-account process; a dynamic outer workflow processes a bounded queue with
checkpoints and named stopping decisions. The application is secured, evaluated,
optimized, observable, repeatable and deployed.

Every chapter here extends that system in place. Nothing in Book 2 asks the
reader to start over.

## Reading order

1. `01_Introduction.md`
2. `02_Chapter_01_Enterprise_Agent_Platform_Strategy.md`
3. `03_Chapter_02_Platform_Reference_Architecture_and_Operating_Model.md`
4. `04_Chapter_03_Sessions_State_Memory_and_Durable_Execution.md`
5. `05_Chapter_04_Enterprise_Knowledge_and_Access_Aware_RAG.md`
6. `06_Chapter_05_Context_Engineering_and_Skills_at_Scale.md`
7. `07_Chapter_06_Goals_Planning_and_Advanced_Dynamic_Workflows.md`
8. `08_Chapter_07_Collaborative_Hierarchical_and_Distributed_Agents.md`
9. `09_Chapter_08_Agent_Identity_and_Secure_Tool_Access.md`
10. `10_Chapter_09_Governance_Policy_and_Containment.md`
11. `11_Chapter_10_Enterprise_AgentOps_Economics_and_Continuous_Evaluation.md`
12. `12_Book_2_Conclusion.md`

The introduction and conclusion are not numbered as chapters.

## Editorial standard for every chapter

Book 2's altitude is different from Book 1's, and so is its chapter template.
Every chapter answers four questions and produces one reusable, client-facing
artifact:

| Question | What it settles |
| --- | --- |
| **Business** | Why the enterprise should care, in outcomes rather than capabilities |
| **Architecture** | What is built, on which plane, with which Google Cloud services |
| **Operating model** | Who owns, funds, secures and runs it once it exists |
| **Proof** | What evidence shows it works, and keeps showing it after release |

Each chapter also states its relationship to the Seven Steps, a conceptual
narrative, an implementation and lab outline, evaluation criteria, a checkpoint
and a bridge to the next chapter.

## The continuous lab

Book 1 proved the system could research, qualify, draft and stop for approval —
for one account, and for a bounded queue run on request. Book 2 asks what changes
when the same system must serve many users, remember across long time periods,
draw on enterprise-scale knowledge, plan over ambiguous goals, collaborate with
independently deployed agents, and prove — continuously, not once at release —
that it still behaves inside its boundaries.

## A note on Google Cloud product names

Book 2 names specific Google Cloud products and features throughout — Memory
Bank, RAG Engine, Agent Registry, Agent Gateway, Model Armor, Agent Identity and
others. Product names, capabilities and GA/Preview status change faster than a
book's release cycle. Treat every named product as this series treats a specific
ADK class: correct in spirit and current as of this edition's writing, but worth
confirming against Google's own documentation before it anchors a production
decision.

## The principle that carries forward

Book 2 adds scale and sophistication, but it does not abandon the Book 1
discipline. The platform must remain inspectable. Memory must remain scoped.
Retrieval must preserve evidence. Plans must remain bounded. Collaboration must
use explicit contracts. Tools must remain least privilege. Governance must exist
outside model persuasion. Evaluation must remain tied to business outcomes.

> Is this behavior better expressed as model reasoning or deterministic software?

Scale does not change that question. It raises the cost of answering it wrong.

The objective is not maximal autonomy. The objective is an enterprise system in
which intelligent behavior can expand without control becoming weaker.
