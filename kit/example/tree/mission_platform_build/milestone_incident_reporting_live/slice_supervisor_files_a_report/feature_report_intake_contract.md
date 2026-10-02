---
title: The incident-report intake contract
status: done
workflow: contract-change
blocked_by: [feature_ci_and_full_gate]
briefed: 2026-09-04
pr: 19
merged: 2026-09-09
traces:
  gate: [G1.1]
  boundary: [B1]
  holding: [H1, H3a]
---

# Feature · The incident-report intake contract

## Goal

A report is defined once. The form that collects it, the endpoint that accepts it and the store that
keeps it all answer to the same definition, so a field cannot exist in one and be missing from
another.

## Where to err

Toward a narrow contract that refuses. A field the contract does not name is rejected at intake, not
stored in case it is useful. An incident report is evidence, and a store holding fields nobody
defined cannot say what it holds.

## Done-when

The contract is published as version 1, a canonical valid report and a set of invalid ones exist as
fixtures, and both the browser and the server reject every invalid one for the same stated reason.

## Context

- **Constitution:** `AGENTS.md`, data rules.
- **Threat model:** the workbook's rows for H1 and H3a – what a report holds and who may be named.
- **Pattern to mimic:** none yet. This is the first contract.

## The contract to implement

The contract itself is the deliverable, so only its edges are fixed here:

- It carries a **version**, and a stored report records the version it was accepted under.
- Free text carries the **language it was written in**, as declared by the supervisor.
- A field is **marked sensitive in the contract**, not in the code that handles it.

Later features read these three by name.

## Scope

**In scope**
- The specification, the schema, the canonical fixtures, the generated types for both stacks.

**Out of scope**
- The form and the endpoint. Each is its own feature and consumes this.
- The check-in. It has its own contract and shares nothing with this one.

**Expected surface (not a limit)**
- `contracts/incident_report/`

**Do not touch**
- `checkin/`

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN a report carries a field the contract does not define THE CHECK SHALL reject it, naming the field | the invalid fixtures |
| 2 | WHEN the same invalid report is checked in the browser and on the server BOTH SHALL give the same reason | one fixture set, run in both stacks |
| 3 | WHEN the contract changes THE GENERATED TYPES SHALL fail the build until regenerated | change the schema, run `make check` |

## Edge cases to handle

- Free text in a script the working language does not use → accepted, unchanged, byte for byte.
- A report with no language declared → rejected. The language is not guessed.

## Verification

```bash
make check
make check-component C=contracts
```

**Green means:** every fixture gives its expected verdict in both stacks.

## Boundaries

- ⚠️ **Ask first:** adding a field that names a third person. That is a new holding of personal data.
- 🚫 **Never:** a fixture built from a real report.

---

## Record

### Decisions taken

- **Unknown fields are rejected, not dropped.** Chosen over silently dropping them, which the first
  design did. A dropped field tells the supervisor the report was filed when part of it was thrown
  away. Wrong if the form and the contract are ever released separately – then a newer form would be
  refused by an older server.
- **Language is declared by the supervisor, never detected.** Detection is wrong on short text, and a
  wrong language label sends the text through the wrong translation.

### Carried forward

| Gap | Consequence | When it closes |
|---|---|---|
| Free text has no length limit in version 1 | One report can be arbitrarily large. The endpoint must bound the request itself, because the contract will not | `feature_report_intake_endpoint`, or a contract version that adds a limit |
| "Sensitive" is one flag, not a scale | Every sensitive field is handled alike. Fine for version 1, wrong the day one field needs stricter handling than another | accepted until a second level is needed |

### Verification actually run

- The fixtures were run in both stacks from one directory. The brief asked for "the same reason"; the
  first run gave the same verdict with differently worded reasons. The reason is now a code from the
  contract, and the wording is each stack's own.

### Review

- The panel's contract seat asked what an old stored report means after version 2. Answered in the
  specification: a stored report is read under the version it was accepted under. No change to the
  build.

### Lesson

A contract's first job is to refuse. Decide what is rejected, and how the rejection reads, before
deciding what is accepted.
