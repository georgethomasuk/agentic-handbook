---
title: Anonymous check-in token
status: done
workflow: build-in-repository
blocked_by: []
briefed: 2026-09-14
pr: 41
merged: 2026-09-18
traces:
  finding: [F-51]
  boundary: [B3]
---

# Feature · Anonymous check-in token

## Goal

An invitation link carries a token that proves it was issued by the platform, and says nothing about
who it was issued to.

## Done-when

A check-in is accepted only with a token the platform issued, and no stored field links a check-in
to a person.

## Acceptance criteria

1. A request with no token, or a token the platform did not issue, is refused.
2. A stored check-in carries no field derived from the token.

## Verification

- `make check`
- A check-in submitted against the local system, then read back from the store.

## Record

### Decisions taken

- The token is issued per invitation, not per person. One invitation, one token.

### Carried forward

- The token identifies an invitation, not a person, and is not rotated inside the window. A leaked
  link stays usable until the window closes. Closes when something bounds what one token can do.

### Lesson

Proving a request came from an invitation and proving who sent it are different properties. Only the
first was wanted.
