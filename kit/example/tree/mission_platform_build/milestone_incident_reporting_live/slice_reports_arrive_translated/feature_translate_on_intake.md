---
title: Translate a report when it is accepted
status: in-progress
column: frame
workflow: build-in-repository
blocked_by: [feature_report_intake_endpoint, feature_translation_service_access]
briefed: 2026-09-29
traces:
  gate: [G1.2]
  boundary: [B1]
  holding: [H1, H6]
---

# Feature · Translate a report when it is accepted

## Goal

A report filed in another language is readable by the whole safety team within minutes, without
anybody asking for a translation. The original stays beside it, because whoever acts on the report
has to be able to quote what was written.

## Where to err

Toward delivering the report untranslated. A report that arrives late, or in its original language
with a note saying so, is still a report. One held back until translation works is an incident
nobody has read.

## Done-when

A synthetic report in a second language, accepted by the endpoint, has a working-language
translation stored beside its original, marked as machine-translated, and a report whose translation
fails is still visible and says it is untranslated.

## Blocked on

`feature_report_intake_endpoint` emits the event this listens for. Its record says the event can be
missing for a stored report, which decides more of this design than the happy path does.

## Context

- **Constitution:** `AGENTS.md`, data rules.
- **The contract:** `contracts/incident_report/` – the declared language of each free-text field.
- **Pattern to mimic:** `reports/store.py` for writes to the canonical store.

## The contract to implement

- Listens for `report.accepted`.
- **Stores a translation with three things beside it: the original untouched, the label
  `machine-translated`, and the time.** `feature_translation_label` reads the label by that name.
- **A report with no translation carries a `translation_state`** of `pending`, `failed` or
  `not-needed`. The inbox reads it.

## Scope

**In scope**
- The listener, the call as `translation-caller`, the stored translation and its state.
- Finding stored reports that never had an event.

**Out of scope**
- How a translation is shown. That is `feature_translation_label`.
- Re-translating on request.

**Expected surface (not a limit)**
- `reports/translation/`

**Do not touch**
- `contracts/` – a new field on the report is a contract change, and its own feature.
- `infra/translation/` – the grant is settled.

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN a report in another language is accepted THE SYSTEM SHALL store a translation beside the unchanged original, labelled `machine-translated` | synthetic report, read the store |
| 2 | WHEN the service fails or refuses THE SYSTEM SHALL leave the report readable with `translation_state: failed` | service stubbed to fail |
| 3 | WHEN a stored report had no event THE SYSTEM SHALL still translate it | store a report with the event suppressed |
| 4 | WHEN a report is translated THE SYSTEM SHALL write no report text to the logs (H6) | marker string, searched in every stream |
| 5 | WHEN a report is already in the working language THE SYSTEM SHALL send nothing to the service | read the call log |

## Edge cases to handle

- A field whose declared language the service does not support → `failed`, never a guess.

## Verification

```bash
make check
```

Then against the local system with the service stubbed, and once against staging with a synthetic
report.

## Boundaries

- ⚠️ **Ask first:** sending any field the contract marks sensitive beyond the free text itself.
- 🚫 **Never:** a real report sent to the service from a supplier machine (H4).
