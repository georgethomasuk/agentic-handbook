---
title: Platform build
---

# Mission · Platform build

## Goal

The safety team runs incident reporting and the yearly wellbeing check-in on one platform, and the
company can operate it without the supplier.

## Done-when

The company accepts the handover (boundary B4): its own staff deploy a change and run a check-in
window without the supplier present.

## Boundaries

- No live personal data on a supplier machine (holding H4). Fixtures are synthetic.
- Nothing the insurer can read may identify a person. Small sites make small cells (holding H2).

## Inherited context

- Trust boundaries B1 to B7 and holdings H1 to H6 are fixed by the threat model. A feature names the
  ones it touches; it does not redraw them.
