---
title: Incident reporting is live
target: 2026-10-16
traces:
  gate: [G1.1, G1.2, G1.3, G1.4]
---

# Milestone · Incident reporting is live

## Goal

A supervisor files an incident report at their site and the safety team reads it, in the company's
working language, the same day. The spreadsheet-and-forms process is switched off.

## Done-when

**The safety team's lead accepts criteria G1.1 to G1.4, on reports filed from two sites, by
16 October 2026.**

### The confirmation statements

Plain restatements of the acceptance schedule. The schedule's own wording is the authority and is not
reproduced here.

| | | Node |
|---|---|---|
| G1.1 | A supervisor files an incident report from a managed device at their site | `slice_supervisor_files_a_report` |
| G1.2 | A report written in another language reaches the safety team in the working language, labelled as machine-translated | `slice_reports_arrive_translated` |
| G1.3 | The safety team reads and triages every report in one inbox | `slice_safety_team_triages_reports` |
| G1.4 | Every read of a report is attributable to a named member of the safety team | `feature_report_read_log` |

## Boundaries

- **Nothing here touches the check-in.** Reports are named and attributable (H3a). Check-ins are
  anonymous (H3b). A part shared between them is a part that can leak one property into the other.
- **No report content in the aggregate store.** What the insurer sees is G3.
- **Translation is labelled, always.** A translated sentence shown as the supervisor's own words is a
  misattribution, and a report can be used in a disciplinary or an injury claim.

## Inherited context

- The original text is kept beside every translation. Whoever acts on a report must be able to quote
  the source.
- Report content leaves the core store in exactly one direction during this milestone: to the
  translation service (boundary B1).

## Reading

**G1.4 rests on one feature, and that feature is still a design question.** The safety team is three
people with the same access. A log they can all write to does not attribute anything. Until
`feature_report_read_log` has a design, G1.4 has a node and no answer.

**The acceptance run traces every criterion, so it is left out of the coverage count.** It proves the
milestone. It builds none of it.
