---
title: No check-in content in the operational exhaust
status: ready
workflow: build-in-repository
blocked_by: [feature_anonymous_checkin_token]
briefed: 2026-09-30
traces:
  gate: [G2.2]
  finding: [F-51]
  holding: [H6]
---

# Feature · No check-in content in the operational exhaust

## Goal

A check-in is anonymous in the store. It also passes through logs, a queue of failed requests and
transient stores, and each of those keeps what it is given for 30 days. Anonymity that holds in the
store and fails in a log line does not hold.

## Where to err

Toward logging less. A request that cannot be debugged from its log line is an inconvenience during
the build. An answer or a token in a log is a check-in tied to a time and an address.

## Done-when

After a synthetic window, no log stream, failed-request queue or transient store holds an answer, a
token or anything derived from either.

## Context

- **Constitution:** `AGENTS.md`, data rules.
- **Threat model:** the workbook's row for H6 – exhaust is purged at 30 days while H1 is kept.
- **Pattern to mimic:** the marker-string search recorded in `feature_report_intake_endpoint`.

## The contract to implement

Nothing another feature depends on.

## Scope

**In scope**
- Every place a check-in request or its failure is written outside the canonical store.

**Out of scope**
- The report path. Reports are attributable and are logged by different rules.
- Retention periods. They are set, and this does not change them.

**Expected surface (not a limit)**
- `checkin/`, the logging configuration, the failed-request handler.

**Do not touch**
- `reports/`

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN a check-in succeeds, fails or is refused THE EXHAUST SHALL hold no answer and no token | marker strings planted in both, every stream searched |
| 2 | WHEN a check-in request fails THE FAILED-REQUEST QUEUE SHALL hold enough to count the failure and nothing to replay it | read the queue |
| 3 | WHEN a new log statement is added under `checkin/` THE BUILD SHALL fail if it logs the request body | a check in `make check` |

## Edge cases to handle

- An unhandled exception → the stack trace carries no request body.

## Verification

```bash
make check
```

Then a synthetic window against the local system, and every stream searched for the marker strings.

## Boundaries

- ⚠️ **Ask first:** dropping a log line the safety team's lead has said they rely on.
- 🚫 **Never:** a token, or a hash of one, anywhere outside the request that carries it.
