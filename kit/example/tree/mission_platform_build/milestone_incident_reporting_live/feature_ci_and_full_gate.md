---
title: One command runs everything CI runs
status: done
workflow: build-in-repository
blocked_by: []
briefed: 2026-09-01
pr: 12
merged: 2026-09-04
traces:
  gate: inherit
---

# Feature · One command runs everything CI runs

## Goal

Every feature after this one is closed by a command passing. That only means something if the
command on a developer's machine and the command in CI are the same command.

## Where to err

Toward one slow command that is complete. A fast command that leaves a check out teaches every later
feature to trust a green that CI will turn red.

## Done-when

`make check` runs the tests, the linter and the type check, CI runs `make check` and nothing else,
and a failure in any of the three fails both.

## Context

- **Constitution:** `AGENTS.md`, the build rules.
- **Pattern to mimic:** none yet. This is the first feature.

## The contract to implement

Two names that every later packet will quote:

- `make check` – everything CI runs.
- `make check-component C=<name>` – the same checks, scoped to one component.

## Scope

**In scope**
- The two make targets, and the CI job that calls the first.

**Out of scope**
- Deployment. No environment exists yet.

**Expected surface (not a limit)**
- `Makefile`, the CI configuration.

**Do not touch**
- Nothing yet exists to protect.

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN a test, a lint rule or a type check fails THE COMMAND SHALL exit non-zero | each broken on purpose, once |
| 2 | WHEN CI runs THE JOB SHALL call `make check` and add no check of its own | read from the CI configuration |

## Verification

```bash
make check
```

**Green means:** all three kinds of check ran and passed. Read the output for all three names.

## Boundaries

- 🚫 **Never:** a check that is skipped when its tool is missing. A missing tool is a failure.

---

## Record

### Decisions taken

- **CI calls `make check` and nothing else.** Chosen over separate CI steps per check, which read
  better in the CI log. Separate steps are a second list of checks, and two lists drift. Wrong if a
  check ever needs a secret only CI holds.
- **The type check is not optional locally.** It adds most of the run time. It stays in because the
  first thing a slow optional check does is stop being run.

### Verification actually run

- Each of the three checks was broken on purpose and `make check` read back as failing, locally and
  in CI. `make check` being green shows the checks pass. It does not show all three ran, which is
  why each was broken once.

### Lesson

A gate is defined by what it fails on. Prove each failure once, at the start, before anything relies
on the green.
