---
title: Label machine translation wherever it is shown
status: blocked
workflow: build-in-browser
blocked_by: [feature_translate_on_intake, feature_report_inbox]
briefed: 2026-09-30
traces:
  gate: [G1.2]
  holding: [H3a]
---

# Feature · Label machine translation wherever it is shown

## Goal

A report can end up in a disciplinary or an injury claim. Anyone reading a translated sentence must
know it is the machine's wording and be one action from the supervisor's own.

## Where to err

Toward the label being impossible to miss. A label that clutters the inbox is an annoyance. A
translated sentence quoted as the supervisor's words is a misattribution.

## Done-when

Everywhere the inbox shows translated text it is marked as machine-translated, the original is one
action away, and a report with no translation says which of the three states it is in.

## Blocked on

`feature_report_inbox` builds the surface this labels. `feature_translate_on_intake` settles what the
states are called – the label reads them by name.

## Context

- **Design reference:** the design folder, the inbox document, the translated-text part.
- **Pattern to mimic:** whatever `feature_report_inbox` uses for a row's secondary text.

## The contract to implement

Nothing another feature depends on.

## Scope

**In scope**
- The label, the route to the original, the three untranslated states.

**Out of scope**
- Requesting a new translation.

**Expected surface (not a limit)**
- `web/inbox/`

**Do not touch**
- `reports/translation/`

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN translated text is shown THE SCREEN SHALL mark it machine-translated in text, not by colour alone | browser test, and a person at `user-review` |
| 2 | WHEN a reader asks for the original THE SCREEN SHALL show it unchanged, in one action | browser test |
| 3 | WHEN a report is `pending`, `failed` or `not-needed` THE SCREEN SHALL say which | browser test per state |

## Verification

```bash
make check
make check-component C=inbox
```

Then in a browser over the built surface, at every supported viewport.

## Boundaries

- 🚫 **Never:** translated text copied to the clipboard without its label.
