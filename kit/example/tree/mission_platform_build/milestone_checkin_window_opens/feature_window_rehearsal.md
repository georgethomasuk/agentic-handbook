---
title: Rehearse the check-in window on staging
status: no-packet
workflow: acceptance
blocked_by: [feature_checkin_rate_limit, feature_checkin_screens, feature_checkin_log_scrub, feature_invitation_send]
traces:
  gate: [G2.1, G2.2, G2.3]
---

# Feature · Rehearse the check-in window on staging

## Goal

The real window cannot be repeated, so the rehearsal is the only time the whole of it runs before it
matters: invitations out, check-ins in at the expected load, and every store read back.

## Done-when

Each of G2.1 to G2.3 has a row in the acceptance matrix with evidence read back from staging, and the
safety team's lead has signed it.

## Status – no packet

Written once the four features it waits on are in review. The expected load is the company's figure
to supply, and it has not been asked for yet.
