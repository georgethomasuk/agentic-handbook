---
title: The check-in screens on a personal phone
status: in-review
column: submit
workflow: build-in-browser
blocked_by: [feature_anonymous_checkin_token]
briefed: 2026-09-21
pr: 58
traces:
  gate: [G2.1]
  holding: [H3b]
---

# Feature · The check-in screens on a personal phone

## Goal

A member of staff opens the link on their own phone, on whatever connection they have, and finishes
the check-in in one go. Most will do it once and never see the screens again.

## Where to err

Toward the agreed wording, exactly. Where a line does not fit the narrowest phone, the layout gives
way and the words do not.

## Done-when

On the narrowest supported phone, the agreed question set is answered and submitted from an
invitation link, and every question reads exactly as agreed.

## Context

- **Design reference:** the design folder, the check-in flow's documents.
- **Content authority:** the agreed wellbeing check-in question set.
- **Pattern to mimic:** `web/report/` for a form read from generated types.

## The contract to implement

Nothing another feature depends on.

## Scope

**In scope**
- The screens, the submit, the confirmation, the refused state.

**Out of scope**
- Any change to a question, an answer option or their order.

**Expected surface (not a limit)**
- `web/checkin/`

**Do not touch**
- The question set's source file. It is copied from what was agreed and is not edited here.

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN a screen is rendered THE WORDING SHALL match the agreed question set character for character | compared against the source file |
| 2 | WHEN the phone is the narrowest supported THE SCREENS SHALL need no sideways scrolling | browser test at that viewport |
| 3 | WHEN the check-in is submitted THE PHONE SHALL keep nothing that shows a check-in was made | read browser storage afterwards |

## Verification

```bash
make check
make check-component C=checkin
```

Then in a browser over the built surface, at every supported viewport.

## Boundaries

- ⚠️ **Ask first:** any wording on a check-in screen that the question set does not supply.
- 🚫 **Never:** analytics, or any third-party script, on a check-in screen.
