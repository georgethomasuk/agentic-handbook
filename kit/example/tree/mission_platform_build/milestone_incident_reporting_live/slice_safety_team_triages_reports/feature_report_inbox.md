---
title: The report inbox
status: ready
workflow: build-in-browser
blocked_by: [feature_report_intake_endpoint]
briefed: 2026-10-01
traces:
  gate: [G1.3]
  holding: [H1, H3a]
---

# Feature · The report inbox

## Goal

The safety team works from one list. Each of them can see what is new, what a colleague has picked
up and what is closed, so no report is read by nobody and none is handled twice.

## Where to err

Toward showing a report twice. A report two people both pick up costs a conversation. A report
nobody saw is the failure the platform exists to end.

## Done-when

Two members of the safety team are signed in at once, one picks a report up, and the other sees it as
taken without refreshing. Every stored report appears in the list.

## Context

- **Design reference:** the design folder, the inbox document.
- **Pattern to mimic:** `web/report/` for how a screen reads the generated types.

## The contract to implement

- **A report has a triage state of `new`, `taken` or `closed`**, held beside the report and never in
  it. `feature_report_read_log` and the dashboard's aggregates read these three names.

## Scope

**In scope**
- The list, the three states, picking up and closing a report.

**Out of scope**
- Translation labels. That is `feature_translation_label`.
- Recording who read a report. That is `feature_report_read_log`, and it is still a design question.
- Export.

**Expected surface (not a limit)**
- `web/inbox/`, `reports/triage.py`

**Do not touch**
- `contracts/` – triage state is not part of a report.

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN a report is stored THE INBOX SHALL list it as `new` | post a fixture, read the list |
| 2 | WHEN one member takes a report THE OTHER'S INBOX SHALL show it as taken without a refresh | two browser sessions |
| 3 | WHEN two members take the same report at once THE SYSTEM SHALL give it to one and tell the other | two browser sessions, simultaneous |
| 4 | WHEN the list is filtered THE INBOX SHALL never hide a `new` report without saying a filter is on | browser test |

## Edge cases to handle

- A report whose translation is `pending` or `failed` → listed like any other.

## Verification

```bash
make check
make check-component C=inbox
```

Then in a browser over the built surface, with two sessions.

## Boundaries

- ⚠️ **Ask first:** any state beyond the three.
- 🚫 **Never:** a copy of a report held by the inbox. It reads the canonical store.
