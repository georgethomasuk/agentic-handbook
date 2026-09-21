**Status** scaffold — nothing here is drafted · **Life** living · **Reader** anyone briefing agents at more than one at a time

# 5 · Planning the delivery

> **Draft order: 2nd.** Documented in full. Extraction-and-editing job.

## The problem

A hand-written kickoff brief silently omits things. Status held in four places disagrees the day
anyone reconciles it. And a plan that grows a rung every time something feels big stops meaning
anything.

## The mechanism

- **Two rungs that matter: the slice and the feature.** Higher rungs exist for reporting, not for
  work. **A level is not a size — it is defined by who says it is done.**
- **Path is identity.** No minted IDs. Keep the identifiers an outside authority owns; drop the ones
  you minted for yourself.
- **Leaves are authored, summaries are derived.** Doneness does not roll up.
- **A workflow is chosen by where the truth lives**, not by what the work is about. A real cloud
  account means apply and read back. A rendered surface means a browser. The repository means tests.
- **Columns inside a workflow**: check, frame, build-plan, build-execute, prove, panel, record, close.
  Each column can declare what model it delegates to, what it sends, what it keeps, and what it
  escalates.
- **The plan node is the brief.** Assembling the packet from the tree renders protocol blocks a
  hand-written kickoff omits.
- **Status lives once, in the tree.** The delivery documents hold knowledge, which is what they are
  good at.
- **The ID chain is load-bearing** — every task traces to a requirement and a gate criterion, so
  nothing is orphaned and coverage is checkable at a glance.

## The rules that earned their place

- **Do not add a rung below the feature.**
- **Do not maintain status in more than one place.** Four hand-maintained copies disagreed the day
  they were reconciled.
- **Never hand-author a brief where the tree can assemble one.**
- **A rule stated more broadly than its evidence gets obeyed at its width.** A withdrawn delegation
  rule fenced off a large share of all spend because it was phrased more generally than the
  measurement behind it.
- **Delivery documents point, they do not paste.**

## What it cost

This is the part with real numbers, and every one must be re-read from source before publishing:

- The per-column delegation measurement — units, turns and average context before and after, per
  column, including the column where delegation was **flat at best** and the one that has **not run
  since** and is therefore unmeasured.
- The cache-read share of weighted spend and the read-to-write ratio.
- The single column that accounted for the largest share of all spend, across how many turns and at
  what average context.
- **The delegation floor** — cheap-model delegation has one, and it is somewhere above thirty turns.
- The sliced-versus-batch comparison, which is **inconclusive**, on badly unmatched sample sizes.
  Publish it as inconclusive or not at all.

## The smallest version that works

One file per unit of work, holding what it is, how it will be proved, and what state it is in. Pick
the workflow by asking what could prove it. Nothing else here is needed for the benefit.

## What's not solved yet

[the gaps, the proxies, the principles still unmet]

---

<!-- DRAFTING ONLY -->

## Source material

- `platform/plan/README.md` — the delivery record, and the workflow-selection table.
- `platform/plan/model.md` — the rungs, the who-says-it-is-done definition, and the delegation
  measurement.
- `platform/plan/workflows/*.yaml` — the templates, with per-column delegation blocks, entry, produces,
  exit and human gates.
- `platform/plan/tree/` — the leaves.
- `redmoor_docs/delivery/README.md` — the sprint docs, the ID chain, and the note about four
  disagreeing copies.
- `redmoor_docs/delivery/journals/` — per-feature delivery journals.

## Open

- Whether the column list is generalisable or too specific to this estate.
- **Q7** — a rendered plan map would carry this part better than prose.

<!-- END DRAFTING ONLY -->
