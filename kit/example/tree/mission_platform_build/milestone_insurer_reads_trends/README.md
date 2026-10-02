---
title: The insurer reads trends
target: 2026-12-01
traces:
  gate: [G3.1, G3.2, G3.3]
---

# Milestone · The insurer reads trends

## Goal

The insurer's analysts see safety and wellbeing trends by site, from aggregates, without the company
sending a spreadsheet. The company can say what the insurer saw and who saw it.

## Done-when

**The company's safety lead and the insurer's analyst lead accept criteria G3.1 to G3.3 on a
dashboard fed by one full month of reports, by 1 December 2026.**

### The confirmation statements

| | | Node |
|---|---|---|
| G3.1 | Each analyst signs in with an account of their own and sees trends broken down by site | `slice_insurer_sees_trends_by_site` |
| G3.2 | No figure the insurer can see describes fewer people than the agreed minimum | `feature_small_cell_suppression` |
| G3.3 | The company can say which analyst viewed which site, and when | `slice_insurer_access_is_attributable` |

## Boundaries

- **Aggregates only.** No report text, no check-in answer and no free text crosses boundary B2.
- The dashboard reads the aggregate store (H2) and nothing else.
- No export from the dashboard.

## Reading

**Nothing here has a packet.** The milestone was given nodes on 22 September 2026 so that its
criteria had owners. Two features are marked `design` because their answer changes what the others
build: what the minimum cell is, and what a suppressed cell shows.

**The chart work waits on the suppression design, and says so in `blocked_by`.** A chart built before
it would have to be rebuilt around whatever a suppressed cell turns out to be.
