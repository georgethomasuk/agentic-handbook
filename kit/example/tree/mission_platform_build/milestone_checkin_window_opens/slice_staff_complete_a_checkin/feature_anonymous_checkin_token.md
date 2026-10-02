---
title: Anonymous check-in token
status: done
workflow: build-in-repository
blocked_by: [feature_ci_and_full_gate]
briefed: 2026-09-14
pr: 41
merged: 2026-09-18
traces:
  gate: [G2.1, G2.2]
  finding: [F-51]
  boundary: [B3]
  holding: [H3b]
---

# Feature · Anonymous check-in token

## Goal

An invitation link carries a token that proves it was issued by the platform, and says nothing about
who it was issued to. Staff answer honestly only if the answer cannot come back to them.

## Where to err

Toward anonymity. Where proving a request is genuine and keeping it anonymous pull apart, anonymity
wins, and the gap that leaves is written down for the next feature.

## Done-when

A check-in is accepted only with a token the platform issued, and no stored field links a check-in
to a person.

## Context

- **Constitution:** `AGENTS.md`, data rules.
- **Threat model:** finding F-51 – nothing ties a check-in to whoever sent it, and the obvious fix
  removes the anonymity the check-in depends on.
- **Pattern to mimic:** none yet. This is the first check-in feature.

## The contract to implement

- **A token identifies an invitation, never a person.** Every later check-in feature relies on this
  and may key on a token for that reason.

## Scope

**In scope**
- Issuing a token per invitation, and checking one on a check-in request.

**Out of scope**
- Sending invitations.
- Limiting how often a token is used. That is `feature_checkin_rate_limit`.

**Expected surface (not a limit)**
- `checkin/`

**Do not touch**
- `reports/` – reports are attributable and check-ins are not. They share nothing.

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN a request has no token, or one the platform did not issue THE SYSTEM SHALL refuse it | unit tests, and requests at the local system |
| 2 | WHEN a check-in is stored THE RECORD SHALL carry no field derived from the token | read the store back |

## Verification

```bash
make check
```

Then a check-in submitted against the local system, and the stored record read back.

## Boundaries

- 🚫 **Never:** a stored link between a token and a member of staff, even a hashed one.

---

## Record

### Decisions taken

- **The token is issued per invitation, not per person.** One invitation, one token.
- **The check-in view moved from `checkin/views.py` to `checkin/api.py`.** The token check and the
  view were one function. Split so the check can be tested without a request.

### Carried forward

- The token identifies an invitation, not a person, and is not rotated inside the window. A leaked
  link stays usable until the window closes. Closes when something bounds what one token can do.

### Lesson

Proving a request came from an invitation and proving who sent it are different properties. Only the
first was wanted.
