---
title: The check-in window can open
target: 2026-11-02
traces:
  gate: [G2.1, G2.2, G2.3]
---

# Milestone · The check-in window can open

## Goal

Every member of staff can be invited to the yearly check-in, and the two-week window can run once
without being repeated.

## Done-when

**The safety team's lead signs off a rehearsal window run against the staging environment, against
criteria G2.1 to G2.3, before the window opens on 2 November 2026.**

### The confirmation statements

| | | Node |
|---|---|---|
| G2.1 | A member of staff completes the check-in on their own phone, from the link they were sent | `slice_staff_complete_a_checkin` |
| G2.2 | Nothing stored or logged can tie a check-in to a person or a device | `slice_checkins_stay_anonymous` |
| G2.3 | A flood of requests during the window does not stop staff checking in | `feature_checkin_rate_limit` |

## Boundaries

- The window is two weeks and cannot be re-run. Anything that could lose check-ins inside it is in
  scope; anything that only matters after it closes is not.
- No reporting on check-ins here. What the insurer sees is G3.

## Reading

**G2.3 is answered by one feature.** The rate limit is the only thing between the public endpoint and
the window. The rehearsal proves it at load. It does not replace it.
