---
title: Access to the translation service, in region and without training
status: done
workflow: real-environment-change
blocked_by: [feature_ci_and_full_gate]
briefed: 2026-09-15
pr: 38
merged: 2026-09-19
traces:
  gate: [G1.2]
  boundary: [B1, B5]
---

# Feature · Access to the translation service, in region and without training

## Goal

Report text is about to leave the core store for a third party. Before any code sends it, the
platform has an identity that can reach the translation service, only that service, only in the
agreed region, with the service's use of the content for training switched off.

## Where to err

Toward the narrowest grant that works. A grant that is too narrow fails loudly on the first call. One
that is too wide works, and nobody finds out.

## Done-when

From the staging environment, the platform's identity translates a synthetic sentence, is refused in
any other region and on any other service, and the opt-out reads back as on.

## Context

- **Constitution:** `AGENTS.md`, data rules.
- **Threat model:** the workbook's row for B1 – report content leaving the core store.
- **Pattern to mimic:** none. This is the first change only a real environment can prove.

## The contract to implement

- **One identity, named `translation-caller`.** `feature_translate_on_intake` runs as it.

## Scope

**In scope**
- The identity, its grant, the region restriction, the training opt-out.

**Out of scope**
- Any code that calls the service.

**Expected surface (not a limit)**
- `infra/translation/`

**Do not touch**
- Any existing identity or grant.

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN `translation-caller` translates in the agreed region THE SERVICE SHALL answer | called from staging |
| 2 | WHEN it calls any other region or any other service THE CALL SHALL be refused | called from staging, each refusal read back |
| 3 | WHEN the opt-out is read from the service THE SERVICE SHALL report it as on | read back, not asserted from the configuration |

## Verification

Apply to staging, one unit at a time. After each: the call that should work, the call that should be
refused, and the setting read back from the service itself.

## Boundaries

- ⚠️ **Ask first:** anything applied to production.
- 🚫 **Never:** a real report as the test sentence.

---

## Record

### Decisions taken

- **The region restriction is on the identity, not in the calling code.** A restriction in code is a
  default the next change can override.

### Carried forward

| Gap | Consequence | When it closes |
|---|---|---|
| The service keeps request metadata at its own end for a period it sets | Not content, but it records that the platform translated something and when. It is the service's position, not a control here | the company declares it in its own records – accepted, never closed by the build |
| The opt-out is an account setting, not part of the grant | Somebody with access to the account can switch it off, and nothing in the repository would change | `feature_translate_on_intake` must not assume it; raised as issue #40 for a check that reads it back on a schedule |

### Verification actually run

- Criterion 3 was first "verified" by reading the configuration file that sets the opt-out. That
  shows what was asked for. The setting was then read back from the service, which is the only thing
  that shows what is true.

### Lesson

For a change only the real environment can prove, the evidence is what the environment says when
asked – never the file that was applied.
