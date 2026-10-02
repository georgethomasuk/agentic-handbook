---
title: Check-ins stay anonymous
traces:
  gate: [G2.2]
---

# Slice · Check-ins stay anonymous

## Goal

A member of staff answers honestly only if the answer cannot come back to them. Anonymity has to
hold in the places nobody designed: the logs, the queue of failed requests, the invitation list.

## Done-when

Demonstrated by reading back every store a check-in passes through after a synthetic window, and
finding no field that links an answer to a person, an invitation or a device.

## Boundaries

- **The fix for a flood is never to remember who sent it.** Finding F-51 names the tension: the gap
  and the protection are the same property.
- Operational exhaust is purged at 30 days while the canonical store is kept (H6). A field removed
  from one is not thereby removed from the other.
