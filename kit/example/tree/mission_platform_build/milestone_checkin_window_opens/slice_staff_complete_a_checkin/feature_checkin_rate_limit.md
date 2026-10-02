---
title: Rate limit on the public check-in endpoint
status: ready
workflow: build-in-repository
blocked_by: [feature_anonymous_checkin_token]
briefed: 2026-09-28
traces:
  finding: [F-51]
  boundary: [B3]
---

# Feature · Rate limit on the public check-in endpoint

## Goal

The check-in window lasts two weeks and cannot be repeated. A flood of requests in that window must
cost the sender, not the staff trying to check in.

## Where to err

Toward letting a real member of staff through. A limit that sometimes admits a flood is a worse
dashboard; a limit that refuses a real check-in is a check-in that is never made.

## Done-when

Requests over the limit are refused, a refused request leaves nothing behind, and the limit can be
changed without a release.

## Context

The check-in endpoint is public by design (boundary B3): anyone with the link can write to it. Staff
at one site often share one outbound address on the site's wifi.

## Acceptance criteria

1. Requests over the limit get a refusal the check-in screen can show.
2. A refused request writes nothing to the canonical store (H1), and no check-in content to the logs
   (H6).
3. The limit is set in configuration, not in code.

## Verification

- `make check`
- Requests fired past the limit at the local system, from two invitations behind one address. Then
  the store and the log read back.

## Boundaries

- No new wording on a check-in screen. The refusal uses a line of copy that already exists.
- The limit does not remember a device.
