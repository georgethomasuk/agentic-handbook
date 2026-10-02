---
title: Platform build
---

# Mission · Platform build

## Goal

The safety team runs incident reporting and the yearly wellbeing check-in on one platform, the
insurer reads trends from it, and the company can operate it without the supplier.

It replaces a spreadsheet-and-forms process in which a report and its translation lived in different
places and nobody could say who had read either.

## Done-when

The company accepts the handover (boundary B4). Judged by the company, against the acceptance
schedule it agreed with the supplier.

| Gate | What | Milestone |
|---|---|---|
| G1 | Incident reporting is live | `milestone_incident_reporting_live` |
| G2 | The check-in window can open | `milestone_checkin_window_opens` |
| G3 | The insurer reads trends | `milestone_insurer_reads_trends` |
| G4 | The company runs it alone | `milestone_handover_accepted` |

The gates are not a sequence, except that G4 follows the other three.

## Boundaries

- No live personal data on a supplier machine (holding H4). Fixtures are synthetic.
- Nothing the insurer can read may identify a person. Small sites make small cells (holding H2).
- The supplier builds and hands over. It does not host the platform or hold the data.

## Inherited context

- Trust boundaries B1 to B7 and holdings H1 to H6 are fixed by the threat model. A feature names the
  ones it touches; it does not redraw them.
- Sensitivity is a property of a field, not of a store. Reports and check-ins converge in H1 and are
  never treated alike because they share it.

## Reading

**G2 is the gate with no slack.** The check-in window is two weeks, once a year, and its date was set
before the build started. Every other target can move by agreement. That one cannot.

**G4 is two placeholders.** Nothing under it has a packet. The tree gives it a node so that its
criteria have an owner, not because it is planned.
