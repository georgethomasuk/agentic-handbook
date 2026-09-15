**Status** scaffold — nothing here is drafted · **Life** living · **Reader** anyone who has to hand an agent an architecture it will not quietly reinterpret

# 2 · Designing the system

> **Draft order: 8th.** Outputs available in full, **method not recorded**. Written from George's own
> account.

## The problem

Agents reinterpret architecture. Without a written boundary, the same constraint gets re-derived
differently in every worktree, and the drift is only visible once two of them merge.

## The mechanism

- **arc42/C4 solution design**, split by concern: overview, building blocks, one document per zone,
  cross-cutting, data model, runtime, deployment.
- **Zones as bulkheads** — isolation stated as a property the design must hold, not an intention.
- **ADRs for the load-bearing calls.** The design points at them rather than restating them.
- **Every key workflow interrogated for failure modes** — a standing pre-mortem that feeds decisions,
  open items and acceptance tests, rather than a description of the happy path.
- **Deep dives are not decisions.** Exploratory research is kept separate; a conclusion graduates to
  an ADR or it does not count.

## The rules that earned their place

- **A decision is recorded once, and everything else points at it.**
- **An ADR outranks a picture.** Where a ruling and a drawing disagree, the ruling wins, and the rule
  saying so is written down.
- **The engineering record ships with the code.** The specification, the decisions and the plan tree
  live in the repository the client receives — because a citation that dies at handover means the
  deliverable shipped with no architecture record.
- **The boundary between records is content, not category.** Commercial posture stays private;
  engineering record ships. Applied file by file, not folder by folder.

## What it cost

**Not measured.** Counts available and worth citing once re-read: the number of ADRs, the number of
workflows walked, the date the specification moved repositories.

## The smallest version that works

One page naming your zones and what may cross between them, plus a decision log with one entry per
choice you would be annoyed to re-litigate. The full arc42 set is not the entry point.

---

<!-- DRAFTING ONLY -->

## Source material

- `platform/docs/spec/02_solution_design/` — `00_overview`, `01_building_blocks`, three zone
  documents, `05_crosscutting`, `05a_data_model`, `06_runtime`, `07_deployment`.
- `platform/docs/spec/04_workflows/` — fourteen workflows, each interrogated.
- `platform/docs/adr/` — the decision series.
- `platform/docs/architecture/` — zone crossings, drift detection, observability, CI verification
  identity, zone runtime.
- `redmoor_docs/deep_dives/` — ten dated research notes. The README line *"Not decisions — those
  graduate to ADRs"* is the rule worth lifting.
- `redmoor_docs/README.md` — the specification move, and the reason for it.

## Open

- **Q5** — method interview.
- **Q7** — this part probably needs the zone diagram. The source estate has one image and it is
  client-specific.

<!-- END DRAFTING ONLY -->
