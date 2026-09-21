**Status** scaffold — nothing here is drafted · **Life** living · **Reader** anyone starting an engagement with agents rather than a codebase

# 1 · Framing the work

> **Draft order: 7th.** The outputs are excellent and fully available. **The method is not recorded
> anywhere** — this part is written from George's own account, with the artefacts as evidence.

## The problem

An agent given a loose requirement produces confident work against the wrong target. The failure is
invisible until acceptance, because nothing in the brief could have caught it.

## The mechanism

Four documents, read in order, each answering one question:

| # | Document | Answers |
|---|---|---|
| 00 | Frame | Why, for whom, within what limits and exclusions |
| 01 | Requirements | What it must do and how well — each one testable |
| 02 | Solution design | How it is built to satisfy that → Part 2 |
| 03 | Scope and acceptance | What is in, and how done is proved |
| 04 | Workflows | Each key workflow interrogated for failure modes → Part 2 |

Requirements are EARS-phrased, MoSCoW-tagged, and traced to a work package. The load-bearing move is
that **every requirement carries a fit criterion** — no untestable obligations.

## The rules that earned their place

- **Every requirement has a fit criterion.** A requirement an agent cannot prove it met is a
  requirement it will claim to have met.
- **Exclusions are written as deliberately as inclusions.** A deferred feature gets a decision record,
  not silence.
- **Open confirmations are named and parked, not resolved by invention.** They get a work-package tag
  and settle before build.
- **Dates are absolute.** Cross-references use anchors, never bare numbers.
- **Requirements change visibly.** The register's status line carries a dated list of what moved and
  what withdrew it.

## What it cost

**Not measured.** No figure exists for how long the framing took or what it saved. Do not invent one.

## The smallest version that works

A single requirements table with three columns: the requirement, the reason, and how you would prove
it. Nothing else in this part is necessary to get the benefit.

## What's not solved yet

[the gaps, the proxies, the principles still unmet]

---

<!-- DRAFTING ONLY -->

## Source material

- `platform/docs/spec/README.md` — the four-document chain and the work-package table.
- `platform/docs/spec/00_frame.md` — purpose, goals with testable success criteria, constraints,
  assumptions, exclusions.
- `platform/docs/spec/01_requirements.md` — the EARS register, functional then ISO 25010 non-functional.
- `platform/docs/spec/03_scope_acceptance.md` — the requirement → scope → acceptance-test chain.
- `platform/docs/adr/` — where the load-bearing decisions went instead of into the requirements.

Good worked examples to generalise: the requirement whose mechanism was withdrawn and replaced with
the obligation left intact; the discovery that an assumed integration did not exist, recorded at the
line with its date, after a watcher had been built against it and withdrawn.

## Open

- **Q5** — how this was actually produced with agents. Interview needed.
- Whether the ISO 25010 walk is worth its own section or one paragraph.

<!-- END DRAFTING ONLY -->
