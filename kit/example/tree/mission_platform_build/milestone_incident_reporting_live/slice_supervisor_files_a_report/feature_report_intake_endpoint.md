---
title: The report intake endpoint
status: done
workflow: build-in-repository
blocked_by: [feature_report_intake_contract]
briefed: 2026-09-09
pr: 27
merged: 2026-09-12
traces:
  gate: [G1.1]
  holding: [H1, H6]
---

# Feature · The report intake endpoint

## Goal

A report that passes the contract is in the canonical store, once, with the contract version it was
accepted under. A report that does not pass is refused with a reason the form can show.

## Where to err

Toward refusing and saying why. A supervisor told "this was not filed, because…" files it again. A
supervisor told it was filed, when part of it was lost, does not.

## Done-when

A valid report posted to the endpoint is read back from the store unchanged, an invalid one writes
nothing, and neither leaves report content in a log.

## Context

- **Constitution:** `AGENTS.md`, data rules.
- **The contract:** `contracts/incident_report/` – the schema and the fixtures.
- **Pattern to mimic:** none yet.

## The contract to implement

- Accepts exactly what the intake contract defines.
- **Emits `report.accepted` once per stored report**, carrying the report's identifier and nothing
  from its content. `feature_translate_on_intake` listens for this by name.

## Scope

**In scope**
- The endpoint, the write to the canonical store, the event.

**Out of scope**
- Translation. Triggered by the event, built elsewhere.
- Who may file a report. Managed devices are authenticated upstream.

**Expected surface (not a limit)**
- `reports/api.py`, `reports/store.py`

**Do not touch**
- `checkin/`
- `contracts/` – a contract change is its own feature.

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN a valid report is posted THE SYSTEM SHALL store it unchanged with its contract version | post the canonical fixture, read the store |
| 2 | WHEN an invalid report is posted THE SYSTEM SHALL write nothing and return the contract's reason code | each invalid fixture |
| 3 | WHEN any report is posted THE SYSTEM SHALL write no report content to the logs (H6) | read the log after each |
| 4 | WHEN the same report is posted twice THE SYSTEM SHALL store it once | post, post again, count |

## Edge cases to handle

- The store is unavailable → refuse, and say the report was not filed. Never queue it out of sight.

## Verification

```bash
make check
```

Then against the local system: post each fixture, and read the store and the log back.

**Green means:** the store holds exactly the valid fixtures, and the log holds no fixture text.

## Boundaries

- 🚫 **Never:** report content in an error message, a log line or an event.

---

## Record

### Decisions taken

- **The request is bounded at the endpoint.** The contract carries no length limit (carried forward
  from `feature_report_intake_contract`), so the endpoint refuses a body over a configured size
  before parsing it.
- **A repeat is recognised by a key the form generates, not by comparing content.** Two supervisors
  can file identical words about one incident, and both reports are real.

### Carried forward

| Gap | Consequence | When it closes |
|---|---|---|
| `report.accepted` is emitted after the write, not with it | If the process stops between the two, a report is stored and nothing is told. A consumer must not assume every stored report had an event | `feature_translate_on_intake` – it needs a way to find reports it was never told about |
| The size limit refuses with a generic reason, not a contract code | The form shows "could not be filed" with no cause | issue #31 |

### Verification actually run

- Criterion 3 was checked by reading the log, and also by posting a fixture whose text is a marker
  string and searching every log stream for it. Reading the log by eye had passed while a debug
  stream nobody was looking at held the whole body.

### Lesson

"Nothing in the logs" is proved by searching for something you planted, in every stream, not by
reading the stream you expected.
