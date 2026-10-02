---
title: The report form on a managed device
status: done
workflow: build-in-browser
blocked_by: [feature_report_intake_contract, feature_report_intake_endpoint]
briefed: 2026-09-12
pr: 34
merged: 2026-09-17
traces:
  gate: [G1.1]
  holding: [H3a]
---

# Feature · The report form on a managed device

## Goal

A supervisor who has just dealt with an incident can file it in one sitting, in their own language,
on the device at their site, and knows when they leave the screen whether it was filed.

## Where to err

Toward keeping what the supervisor typed. Losing a half-written report to a validation error or a
dropped connection costs more than any other failure this form can have.

## Done-when

On the site's managed device, a supervisor files a report in a second language, sees it confirmed,
and a refused report shows the contract's reason beside the field that caused it.

## Context

- **Design reference:** the design folder, the report form's document.
- **The contract:** `contracts/incident_report/` – the generated types and the reason codes.
- **Pattern to mimic:** none yet. This is the first screen.

## The contract to implement

Nothing another feature depends on. The form consumes the intake contract and the endpoint.

## Scope

**In scope**
- The form, its validation from the generated types, the confirmation and refusal states.

**Out of scope**
- Editing a filed report. A report is evidence and is not edited after filing.

**Expected surface (not a limit)**
- `web/report/`

**Do not touch**
- `web/checkin/`

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN a field is invalid THE FORM SHALL show the contract's reason beside that field and keep everything typed | browser test per reason code |
| 2 | WHEN the connection drops during filing THE FORM SHALL keep the text and say the report was not filed | browser test, network cut |
| 3 | WHEN a report is accepted THE FORM SHALL show a confirmation that cannot be mistaken for a draft | a person, at `user-review` |

## Verification

```bash
make check
make check-component C=report
```

Then in a browser over the built surface, on the managed device's viewport.

## Boundaries

- 🚫 **Never:** report text in browser storage that outlives the session. The device is shared.

---

## Record

### Decisions taken

- **A half-written report is kept in memory only.** Chosen over saving a draft to the device, which
  survives a closed tab. The device is shared between supervisors, and a saved draft is one
  supervisor's report on the next one's screen.

### Carried forward

- A supervisor who closes the tab loses the report. Accepted for this milestone, and raised as
  issue #36 so the safety team can decide whether a draft tied to a sign-in is wanted.

### Review

- At `user-review` the safety team's lead read the confirmation state as "saved as draft". Reworded
  to "Filed", with the time. Criterion 3 exists for this and a browser test could not have caught it.

### Lesson

A confirmation is judged by the person it is for. Put that judgement in the criteria as a person's
check, not as a test.
