**Status** reference – a worked plan, checked by the kit · **Life** living · **Reader** you, wanting to see a whole plan before writing one

# The example plan

A complete plan for [the example system](../../reference/example-system.md), from the mission down to
packets and records. Every worked example in [Part 5](./README.md) and
[Part 6](../06-delivery-management/README.md) is taken from it.

**It is in the repository, not on this site**, because it is a plan and not a page: 36 files in the
layout a real one has.
[`kit/example/tree/`](https://github.com/georgethomasuk/agentic-handbook/tree/main/kit/example/tree)

**It is fiction with a real shape.** Nothing in it was built. The six finished features carry records
because a record is something the guide has to show. No figure in it is evidence of anything.

**It is checked.** The kit's tests load it on every run, and `plan check` passes on it.

## Run it yourself

```
$ git init demo && cd demo
$ plan init . --example
$ plan check
$ plan work --all
$ plan view
$ plan prompt feature_report_inbox
```

`plan` is [the kit](../06-delivery-management/kit.md).

## The tree

```
mission_platform_build/
  milestone_incident_reporting_live/              G1 · target 16 October 2026
    feature_ci_and_full_gate                      done
    feature_reporting_acceptance_run              no-packet
    slice_supervisor_files_a_report/
      feature_report_intake_contract              done
      feature_report_intake_endpoint              done
      feature_report_form                         done
    slice_reports_arrive_translated/
      feature_translation_service_access          done
      feature_translate_on_intake                 in-progress
      feature_translation_label                   blocked
    slice_safety_team_triages_reports/
      feature_report_inbox                        ready
      feature_report_read_log                     design
  milestone_checkin_window_opens/                 G2 · target 2 November 2026
    feature_window_rehearsal                      no-packet
    slice_staff_complete_a_checkin/
      feature_anonymous_checkin_token             done
      feature_checkin_rate_limit                  ready
      feature_checkin_screens                     in-review
    slice_checkins_stay_anonymous/
      feature_checkin_log_scrub                   ready
      feature_invitation_send                     no-packet
  milestone_insurer_reads_trends/                 G3 · target 1 December 2026
    slice_insurer_sees_trends_by_site/
      feature_aggregate_store                     no-packet
      feature_small_cell_suppression              design
      feature_chart_parts                         no-packet
      feature_site_trend_chart                    no-packet
    slice_insurer_access_is_attributable/
      feature_insurer_named_accounts              no-packet
      feature_dashboard_read_log                  no-packet
  milestone_handover_accepted/                    G4 · no date agreed
    feature_deploy_runbook                        no-packet
    feature_operations_rehearsal                  no-packet
```

**The statuses in that listing are typed, and will drift.** They were true on 2 October 2026. The
plan's own answer is `plan work`.

## Where it stands

`plan view`, run on 2 October 2026:

```
The whole plan
  2 design · 10 no-packet · 3 ready · 1 blocked · 1 in-progress · 1 in-review · 6 done

Criteria · The check-in window can open
  G2.1  3 features, 1 done
  G2.2  3 features, 1 done
  G2.3  1 feature, 0 done  ← answered once
  left out of the count: feature_window_rehearsal traces every criterion

Criteria · The company runs it alone
  G4.1  1 feature, 0 done  ← answered once
  G4.2  1 feature, 0 done  ← answered once

Criteria · Incident reporting is live
  G1.1  3 features, 3 done
  G1.2  3 features, 1 done
  G1.3  1 feature, 0 done  ← answered once
  G1.4  1 feature, 0 done  ← answered once
  left out of the count: feature_reporting_acceptance_run traces every criterion

Criteria · The insurer reads trends
  G3.1  4 features, 0 done
  G3.2  1 feature, 0 done  ← answered once
  G3.3  2 features, 0 done

Longest chain still to run · 5
  feature_report_inbox → feature_aggregate_store → feature_small_cell_suppression → feature_chart_parts → feature_site_trend_chart

Most waited on · feature_report_inbox
  7 unfinished features cannot start until it lands
```

`plan check` passes with six warnings. Each is one of the *answered once* lines above.

## What each part of it shows

| Look at | To see |
|---|---|
| The mission's `README.md` | Boundaries that reach every feature. A *Reading* that says what the counts cannot |
| `milestone_incident_reporting_live` | Confirmation statements, each mapped to a node. A target date. A criterion resting on one undecided feature |
| `milestone_handover_accepted` | A milestone that is honestly unplanned: two one-line features, so its criteria have owners |
| `feature_ci_and_full_gate` | A feature hung from a milestone because it serves every slice. `traces: {gate: inherit}` |
| `feature_report_intake_contract` | A full packet and a full record. *Decisions taken* with what would make each wrong. *Carried forward* as a table |
| `feature_report_intake_endpoint` | A contract section that names one event and nothing else. A *Verification actually run* that changed how a later packet is written |
| `feature_translate_on_intake` | A feature in flight. An acceptance criterion that exists because of an upstream feature's *Carried forward*. A `## Blocked on` |
| `feature_translation_label` | `blocked`: a packet, waiting on two features |
| `feature_report_inbox` | `ready`, and the feature the most others wait on |
| `feature_report_read_log` · `feature_small_cell_suppression` | `design`: a decision that needs an owner, written as the question and its candidates |
| `feature_window_rehearsal` · `feature_reporting_acceptance_run` | Features that trace every criterion, and are left out of the coverage count |
| `feature_report_form` | A *Carried forward* with nothing depending on it, so its entry names an issue |

## The seven workflows, each bound once or more

| Workflow | Bound by |
|---|---|
| `build-in-repository` | `feature_report_intake_endpoint`, `feature_checkin_rate_limit`, and nine more |
| `build-in-browser` | `feature_report_form`, `feature_report_inbox`, `feature_translation_label`, `feature_checkin_screens` |
| `contract-change` | `feature_report_intake_contract` |
| `real-environment-change` | `feature_translation_service_access`, `feature_insurer_named_accounts` |
| `acceptance` | The two acceptance runs, and both handover features |
| `component-library` | `feature_chart_parts` |
| `single-part` | `feature_site_trend_chart` |

## What it leaves out

**No requirement or decision numbers.** Parts 1 and 2 are not written. Features trace to acceptance
criteria, findings, boundaries and holdings.

**No constitution.** Packets point at an `AGENTS.md` that the example does not include.

**No code.** Paths such as `reports/api.py` are named in packets and exist nowhere.
