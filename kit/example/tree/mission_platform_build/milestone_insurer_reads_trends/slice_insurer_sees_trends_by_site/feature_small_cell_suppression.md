---
title: Suppress any figure that describes too few people
status: design
workflow: build-in-repository
blocked_by: [feature_aggregate_store]
traces:
  gate: [G3.2]
  finding: [F-104]
  holding: [H2]
---

# Feature · Suppress any figure that describes too few people

## Goal

A small site makes a small cell. A wellbeing score for a site of four people, set beside last
month's, describes individuals. No figure the insurer sees may do that.

## Done-when

No cell in the aggregate store describes fewer people than the agreed minimum, and no pair of cells
lets a suppressed one be worked out from the others.

## Status – needs design

Three things are undecided, and each changes what the charts are handed:

- What the minimum is. That is the company's figure, agreed with the insurer.
- What a suppressed cell shows – nothing, a marker, or the site folded into a group.
- Whether a total is suppressed when one of its parts is, since a total minus the visible parts
  gives the hidden one back.
