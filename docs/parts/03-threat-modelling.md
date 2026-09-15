**Status** scaffold — nothing here is drafted · **Life** living · **Reader** anyone who wants an adversarial pass that agents can actually run

# 3 · Attacking it before building it

> **Draft order: 1st.** The method is fully documented in the source estate. This is an
> extraction-and-editing job, and it is the most novel part of the handbook — threat modelling run as
> an agentic workflow is not something anyone else appears to have written up.

## The problem

Threat modelling usually produces a document written to *close* things — coverage statements,
declared gaps, a sign-off table. That is an end-of-engagement assurance artefact, and at the start of
a build it is the wrong shape. What is needed is a document written to **open** things.

Separately: a single large findings file is the wrong shape for agents. Reading one finding should
not mean loading all of them, and parallel sessions writing into one file collide.

## The mechanism

- **Two taxonomies over two different spines, deliberately not reconciled.** STRIDE walks the trust
  boundaries, because security threats cluster where trust levels meet. LINDDUN GO walks the
  personal-data holdings, because a privacy threat attaches to a record about a person, not to an
  architecture element.
- **Work per-category, present per-category.** Take one category, ask it of every element in the row,
  record it in that category's own small table. Asking the same question seven times is what catches
  the category you would otherwise skim.
- **One table per category, not one matrix.** A small table has room to carry the reason in the row.
  A single large matrix pushes every explanation into notes underneath, which is how a coverage record
  becomes unreadable.
- **An index plus one file per finding.** Split out of a single large file mid-walk.
- **A separate series for things that are real and actionable but are not threats**, so no reader
  mistakes one for the other.
- **Raw elicitation transcripts are gitignored.** Candid liability content does not go in the tree.

## The rules that earned their place

- **Dialogue first, document second.** The goal is the client understanding and contributing to the
  security of the system, not the client receiving a report.
- **Show what was considered and dismissed**, not only what was found.
- **The fork test.** Split a data holding only where walking it as one forces two different answers.
  Different content is the symptom; diverging analysis is the justification. Otherwise the spine
  splits forever.
- **Route out-of-scope holdings in-cell; do not give them a row.**
- **Length is a design constraint.** A document nobody finishes is a document that failed.
- **Record the overrun rather than quietly restating the target.** Two artefacts ran to roughly double
  their budget; that is written at the line, with the date, and named as a live question.
- **Nothing implies independent review where there is none.**

## What it cost

Figures exist and must be re-read before publishing: the number of findings, the number of coverage
cells across how many tables, the line count the findings file reached before it was split, and the
two artefacts' target versus actual lengths. All dated.

## The smallest version that works

One STRIDE pass over your trust boundaries, one table per category, one line per finding, and a rule
that anything dismissed is written down with its reason. The privacy spine can come later.

---

<!-- DRAFTING ONLY -->

## Source material

- `redmoor_docs/governance/security/threat_model/README.md` — the approach, the artefact table, the
  overrun note.
- `.../walk_playbook.md` — the working procedure, including the two-spines decision and the fork test.
- `.../workbook.md`, `annex_a_grids.md`, `annex_b_findings.md` + `annex_b/` — the substance, the
  coverage record, the findings.
- `.../adjacent_findings.md` — the separate series.
- `.../design_review/` — the earlier session, kept as the signed historical record and explicitly
  superseded rather than deleted.
- `redmoor_docs/governance/security/` — posture, secure-by-design and SSDF mapping, Cyber Essentials.

## Open

- How much of the governance mapping belongs here versus being named in one line.
- Whether the client-facing front-door document is worth showing as a shape.

<!-- END DRAFTING ONLY -->
