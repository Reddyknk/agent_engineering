# Revision Notes

## Governing change

The earlier manuscript was organized mainly as a sequence of technical subjects.
This edition reorganizes the learning journey around the evolution of one SDR
product. Technical concepts appear when evidence shows why the product needs
them.

## Principal structural changes

- Preface and Introduction are Chapters 1 and 2.
- The substantive journey is Chapters 3–14.
- The finished architecture is no longer revealed as the starting point.
- Chapter 5 creates a complete monolithic baseline before decomposition.
- Security is the first hardening increment.
- Evaluation and minimal telemetry begin before optimization.
- ADK 2.x graph workflows become the primary implementation for deterministic
  process control.
- Template workflow agents remain useful teaching comparisons, but they are not
  the final architecture.
- The inner quality loop and outer operational loop are separate chapters.
- Parallelism is introduced only after traces identify independent work.
- Skills, contract design and MCP research remain as detailed appendices and are
  integrated into the relevant product versions.
- Book 2 is repositioned as an enterprise agent-platform consulting book.

## Concepts moved to Book 2

- multi-tenant platform architecture;
- enterprise memory and state services;
- access-aware enterprise RAG;
- collaborative and hierarchical teams at scale;
- distributed agents and A2A;
- per-agent enterprise identity;
- organization-wide governance and containment;
- platform AgentOps and chargeback; and
- continuous evaluation across many workflows and teams.

## Compatibility note

The manuscript teaches sequential, parallel and loop execution as enduring
workflow patterns. For the primary Python ADK 2.x implementation, those patterns
are expressed through graph routes and dynamic workflows. The corresponding
template workflow agents are retained as compact comparisons for readers working
with earlier or mixed ADK codebases.

