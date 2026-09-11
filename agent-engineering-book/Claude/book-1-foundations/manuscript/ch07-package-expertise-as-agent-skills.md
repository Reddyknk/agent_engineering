# Chapter 7 — Package Expertise as Agent Skills

> **Status: outline.**

**Starting point:** V2 — bounded agent
**Result:** V3 — qualification judgment as a reviewable, versioned asset

---

## 7.1 Current state and observed limitation

Run V2 against the same company twice. The fit decisions may agree; the
*reasoning* will not. One run weights employee count heavily, the next
weights buying signals, a third invents a criterion that appears nowhere in
`config/icp.yaml`.

The cause is visible in the prompt: qualification method is three sentences
inside a nine-paragraph instruction that also covers research and drafting.
It has no owner, no version, and no way to be reviewed by the sales lead
whose expertise it is supposed to encode.

## 7.2 Engineering question

> Can repeatable judgment be extracted, versioned and reviewed on its own —
> without becoming another agent?

## 7.3 Architectural decision

Package the method as an **Agent Skill**: a directory containing `SKILL.md`
with metadata frontmatter and a written procedure, plus supporting
references and examples.

Load it through an **application-owned `SkillRegistry`** that discovers skill
directories, validates metadata, exposes only names and descriptions
initially, loads full instructions when a skill is selected, provides
controlled access to references and assets, and records each skill's name,
version and content hash in the run manifest.

Two skills: `icp-qualification` and `evidence-classification`.

## 7.4 What a Skill is not

Taught explicitly, because every one of these confusions is common:

| A Skill is not | Because |
|---|---|
| an agent | it has no loop, no tools and makes no decisions about control flow |
| a tool | it is procedural knowledge, not an executable capability with typed I/O |
| a prompt | it is versioned, discoverable, selectively loaded, and owned by a domain expert |
| a RAG collection | it is procedure the model *follows*, not facts it *retrieves* |
| a folder of docs | it has validated metadata and a defined loading contract |

The one-sentence test: **a Skill answers "how do we do this here."** If it
answers "what is true about the world," it is retrieval. If it answers "do
this thing," it is a tool.

## 7.5 Progressive disclosure, and why it is not just token thrift

The registry exposes name and description first; full instructions load only
on selection.

Token economy is the obvious motivation and the least interesting one. The
real reason is **attention**: a model given four full procedures reasons
worse about which applies than one given four descriptions and then the
chosen procedure. Loading everything makes the selection decision harder,
not easier.

## 7.6 Alternatives considered

**Put the method in `CLAUDE.md`.** Rejected on the brief's central
constraint: `CLAUDE.md` configures Claude Code, the *authoring harness*. The
application must not depend on it. A method the running system needs cannot
live in a file only an interactive tool reads.

**Implement qualification as a Python function.** Right answer if
qualification were a rule. It is not — it weighs partial evidence about
messy companies against a profile with soft edges. Chapter 11 does move the
genuinely deterministic parts (does the employee count fall in band?) into
code, which is a better division than either extreme.

**Fine-tune a model on past qualifications.** Wrong tool: the ICP changes
faster than a fine-tune cycle, and the result would be unreviewable by the
person who owns it.

**Let the model select skills freely from all available.** Rejected — the
registry decides what is offered. Selection is an application decision.

## 7.7 Trade-offs

Indirection: the reasoning is no longer visible in one prompt. A reader
debugging a qualification must open a skill file.

Skills can rot. A procedure that no longer matches how the business
qualifies is worse than no procedure, because it is applied consistently.
The manifest hash makes drift *detectable*, not impossible.

## 7.8 Implementation walkthrough

- `app/skills/registry.py` — discovery, frontmatter validation
  (`name`, `description`, `version` required), `list_available()` returning
  name and description only, `load(name)` returning the full procedure,
  scoped access to `references/` and `examples/`.
- `app/skills/icp-qualification/SKILL.md` — the procedure, written against
  `config/icp.yaml` rather than restating it.
- `app/skills/evidence-classification/SKILL.md` — applying the Chapter 3
  `claim_type` × `support_type` split to a specific claim.
- Manifest: `skills: [{name, version, content_hash}]`.

Skills are written fresh here. The procedure text is the deliverable of this
chapter and should read as something a sales lead could correct.

## 7.9 Tests and evaluation

- Discovery finds both skills; malformed frontmatter fails loudly.
- `list_available()` leaks no procedure body.
- A selected skill's hash appears in the manifest.
- Same account, five runs: the criteria cited are stable.
- An unknown skill name raises rather than silently returning nothing.

## 7.10 Failure demonstration

Edit `icp-qualification/SKILL.md` to contradict `config/icp.yaml` — say,
lower the employee floor. Re-run. The agent follows the skill. The manifest
hash changes.

The lesson is uncomfortable and worth stating: **a skill is authority.**
Consistency is only a virtue when the thing being applied consistently is
correct, which is exactly why it must be reviewable.

## 7.11 Evidence of improvement

Criteria-citation stability across five runs per account, V2 versus V3.
Qualification reasoning now traceable to a named, hashed artifact.

## 7.12 Updated run manifest

`version_tag: "v3-skills"`, plus the skills block.

## 7.13 What remains unresolved

Judgment is repeatable, but its output is still a paragraph of English.
Nothing downstream can route on it, store it, or compare it across runs
without parsing prose.

## 7.14 Exercises

1. Write a third skill for a judgment your own team makes inconsistently.
   Give it to a colleague and ask whether they would apply it the same way.
2. Argue the opposite case: when is a long prompt genuinely better than a
   skill registry? Name the conditions.
