**Status** draft – extracted, with a worked plan · **Life** living · **Reader** you, about to plan delivery so an agent can be handed a brief

# How to plan delivery so an agent can be handed a brief

A plan in which every piece of work says what it is for, how it is known to be done, and where it
stops – and in which the smallest piece is a file an agent can be given as its whole brief.

This part ends where a feature is ready to start. Running it is
[Part 6](../06-delivery-management/README.md).

The worked example throughout is [the example system](../../reference/example-system.md), and
[the example plan](./example-plan.md) built on it: one mission, four milestones, six slices, 24
features.

## What is in this folder

| | |
|---|---|
| **This guide** | The process, why it is shaped this way, and what good output looks like. Written for you |
| [**`prompt.md`**](./prompt.md) | Two instruction sets to paste into an agent session. Written for the agent |
| [**`templates/`**](./templates/README.md) | The two skeletons every node is made from. Copy them |
| [**The example plan**](./example-plan.md) | A whole plan on the example system, with packets and records, checked by the kit |

**Read this once. Use the prompts every time.**

---

# Context

## What you are producing

| | For | What it is |
|---|---|---|
| **A plan tree** | You, and the client's lead | One folder per level, one file per feature. It answers four questions at any point: what is this for, how is it known to be done, where does it stop, where has it got to |
| **A packet** | The agent | The part of a feature's file written before the work. It is the brief. There is no second document |
| **A record** | Whoever comes back to the feature, and whoever builds on it | The part of the same file written after the work. What it decided, and what it left |

## The four levels

**A level is not a size. A level is defined by who says it is done.**

| Level | Done when | Judged by |
|---|---|---|
| **Mission** | The engagement's scope is delivered and accepted | The client's outcome |
| **Milestone** | An acceptance holds | Somebody outside the build |
| **Slice** | A capability can be demonstrated, end to end | You, watching it work |
| **Feature** | A verification command passes and the change merges | A machine |

Three things follow from that table.

**There is no level below a feature.** Nothing has authority below "a command passes". The source
model defined a task level and dropped it for that reason.

**A container is not a level.** A sprint, a campaign of styling work and a client relationship all
lack a done-when. They are labels on a node, never nodes.

**Doneness does not add up.** Each level answers to a different authority. A machine passing nine
times is not a demonstration. Nine demonstrations are not an acceptance.

## What you need before you start

| | |
|---|---|
| **The criteria the work will be accepted against** | Whatever the client will hold you to, as they number it. A milestone is built from these |
| **A specification** | Requirements, design decisions, the threat model's findings. A packet points at these. Parts 1 to 4 |
| **The client's lead, for an hour** | To confirm what each criterion means in plain words. Step 1.3 |
| **The workflow templates** | A packet names the workflow its feature will run. [Part 6](../06-delivery-management/templates/workflows/README.md) |

**The kit is optional and does the checking.** `plan check` enforces most of the rules below. Without
it, each rule is yours to hold. See [the kit](../06-delivery-management/kit.md).

## What it costs

**Not measured.** The source engagement did not record the hours spent planning.

**One figure of scale**, read from the source plan on 2 October 2026. It held 379 features under one
mission, three milestones and 34 slices. 325 were done.

**And one figure about packets**, from the source's design record, measured across 72 finished
features. The median time from a packet being written to its feature merging was one day, and the
longest was three. Packets were written just ahead of the work, not in bulk. Step 2.1 is why.

## Who does what

| | | |
|---|---|---|
| **You** | the operator | Decide the levels and the slices. Write every goal and every *where to err*. Bind the workflow. Set the status |
| **The agent** | | Drafts the tree from the acceptance criteria. Drafts a packet from the specification. Runs the check |
| **The participant** | the client's lead | Says what each acceptance criterion means, and who accepts a milestone |

## The shape of the work

| | | |
|---|---|---|
| **1** | **Lay out the tree** | Mission, milestones, slices, and every feature as one line. Dependencies declared. Once per engagement, then as the plan changes |
| **2** | **Write a packet** | One feature at a time, just before it is built |
| **3** | **Keep the plan true** | Status on features only. A record when one finishes. What is left over sent to somebody who will read it |

---

# 1 · Lay out the tree

## 1.1 · Make the folders

> **You** create the tree, or run one command.

A node with something under it is a folder holding a `README.md`. A feature is a file. The name's
prefix is the level: `mission_`, `milestone_`, `slice_`, `feature_`.

**The path is the identity. Do not mint numbers.** A ticket or epic number is your own bookkeeping.
Nothing outside the tracker refers to it, and it is a relic the day the tracker changes shape. A
feature is named for what it is.

**Keep the identifiers somebody outside the build owns.** A criterion in the acceptance schedule, a
requirement, a decision, a finding. A third party can quote these back at you. They go in a
feature's header under `traces:`, where they can be searched.

**With the kit:** `plan init .`

**Worked example.**

```
plan/tree/
  mission_platform_build/
    README.md
    milestone_incident_reporting_live/
      README.md
      feature_ci_and_full_gate.md               serves the whole milestone – no slice
      slice_supervisor_files_a_report/
        README.md
        feature_report_intake_contract.md
        feature_report_intake_endpoint.md
        feature_report_form.md
```

A feature may hang from any level. `feature_ci_and_full_gate` serves every slice under the
milestone, so it hangs from the milestone. Forcing it into one slice would say it belongs to that
capability, and it does not.

---

## 1.2 · Write the mission

> **You** write it. Copy [`container.md`](./templates/container.md).

Every node carries three things, at every level.

| Section | Holds |
|---|---|
| **Goal** | The outcome, and why it matters. What a reader falls back on when the detail runs out. Not a restatement of the checklist |
| **Done-when** | The acceptance, in that level's own terms – a sign-off, a demonstration, a command |
| **Boundaries** | Where it stops. What a reasonable reader would pull in and must not |

**Boundaries set at a level bind everything under it.** The brief for a feature is assembled with
the boundaries of every level above. So write a boundary once, at the highest level it is true of.

A fourth section, **Inherited context**, is optional: what is already settled and not to be
reopened.

**Worked example.** The mission, in full, is
[in the example plan](https://github.com/georgethomasuk/agentic-handbook/blob/main/kit/example/tree/mission_platform_build/README.md).
Its boundaries:

```markdown
## Boundaries

- No live personal data on a supplier machine (holding H4). Fixtures are synthetic.
- Nothing the insurer can read may identify a person. Small sites make small cells (holding H2).
- The supplier builds and hands over. It does not host the platform or hold the data.
```

Those three lines reach every one of the 24 features without being typed again.

---

## 1.3 · Write a milestone for each outside judgement

> **Agent** drafts from the acceptance criteria · **The participant** says what each one means ·
> **You** write the result.

A milestone exists where somebody outside the build accepts something. Its header lists the criteria
it will be judged by, numbered as their owner numbers them.

```yaml
---
title: Incident reporting is live
target: 2026-10-16
traces:
  gate: [G1.1, G1.2, G1.3, G1.4]
---
```

**A milestone is the only node that carries a date.** `target:` is its own acceptance date. The plan
is not a schedule, and a timebox is not a node.

**Restate each criterion in one plain sentence, and name the node that answers it.** These are the
**confirmation statements**. The owner's wording stays wherever the owner keeps it. The plain
sentence is what you and the participant agree it means.

**Read each statement to the participant and ask who would say it is true.** Use
[prompt A](./prompt.md#a-draft-the-tree) for the draft. The conversation is yours.

**Worked example.** The acceptance schedule's fourth criterion for incident reporting says reads of a
report must be *attributable*. You put the draft statement to the safety team's lead.

> *"Every read of a report is recorded." Is that what G1.4 asks for?*
>
> *No. Recorded isn't the point. I have to be able to say which of the three of us opened a report,
> if the person it names ever asks. And the three of us all have the same access, so it can't be a
> record any of us could tidy up.*

The statement as agreed:

| | | Node |
|---|---|---|
| G1.4 | Every read of a report is attributable to a named member of the safety team | `feature_report_read_log` |

That answer also changed the feature. It went from a line of logging to an open design question,
and its status says so – step 1.5.

---

## 1.4 · Cut slices from outcomes

> **You** decide the slices.

A slice is a capability you can watch working. **Cut slices from the confirmation statements, not
from the areas of the code.**

In the source engagement the first cut followed the technical areas. Infrastructure was a slice. It
was removed, because infrastructure is how a capability is achieved and is not one. Nobody can
demonstrate "infrastructure". The slices were rebuilt from the plain-language statements of what
would be accepted.

**The test of a slice is its done-when.** If it cannot be written as something demonstrated, on a
named device or dataset, it is not a slice.

**Worked example.** The three slices under *Incident reporting is live*:

| Slice | Done-when |
|---|---|
| `slice_supervisor_files_a_report` | Demonstrated on a managed device at one site: a report filed in a language other than the working language, then read back from the store with its language recorded and its text unchanged |
| `slice_reports_arrive_translated` | Demonstrated on a synthetic report in a second language: the working-language text appears in the inbox, marked as machine-translated, with the original one action away |
| `slice_safety_team_triages_reports` | Demonstrated with two members of the safety team signed in at once: one picks a report up, and the other sees it as taken without refreshing |

The translation-service access grant is in the second slice, not in a slice called "infrastructure".
It is there because that slice cannot be demonstrated without it.

---

## 1.5 · List the features, one line each

> **Agent** drafts the list · **You** cut it and set each status.

Write every feature you can name as a file with a header, a goal and a done-when. **Do not write its
packet yet.**

A feature carries a status. Nothing above a feature does.

| Status | Means |
|---|---|
| `design` | Needs a design decision before it can be briefed. Not ready for an agent |
| `no-packet` | Agreed work, a goal and a done-when, no packet yet |
| `ready` | A packet exists and nothing it depends on is unfinished |
| `blocked` | A packet exists and it is waiting on another feature |
| `in-progress` | Claimed. Part 6 writes this |
| `in-review` | A pull request is open |
| `done` | Merged and closed. Part 6 writes this |

**`no-packet` is not `blocked`.** One is short of design time and the other is waiting on a
dependency. Collapse them and the longest queue in the plan – work nobody has briefed – is hidden
inside the other. Where a feature has no packet and also waits on something, it is `no-packet`. Its
dependencies stay visible in `blocked_by`.

**`design` is for a decision, not for a build.** A workflow runs something already decided. A feature whose answer changes what its neighbours build needs an owner and a decision
before it gets a packet.

**Say what each feature answers.** Under a milestone that declares criteria, a feature's
`traces.gate` is either a list of them or the word `inherit`. `inherit` is a stated choice: this
feature serves its parent's capability and answers no criterion of its own.

**Worked example.** `feature_report_read_log`, after the conversation in step 1.3:

```markdown
---
title: Who read which report
status: design
workflow: build-in-repository
blocked_by: [feature_report_inbox]
traces:
  gate: [G1.4]
  holding: [H1]
---

## Status – needs design

The team is three people with the same access. A log they can all write to attributes nothing: each
can add or remove a line. The design question is where the record lives so that the people it
describes cannot change it, in an organisation too small to separate those duties.
```

And `feature_ci_and_full_gate`, which answers no criterion: `traces: {gate: inherit}`.

---

## 1.6 · Declare every hard dependency

> **You** declare them. **The agent** may propose them.

`blocked_by` names the features this one cannot start without.

**Hard dependencies only, and all of them.** *Cannot start*, not *would rather not start*. A
preference goes in prose.

**A dependency kept in prose is a dependency the plan does not have.** In the source engagement,
seven real "cannot start" edges were written in sentences and not in the field. The longest chain
the plan reported was three deep. It was five. The feature it named as the one most others waited on
was the wrong one.

**Say why a dependency is hard, where that is not obvious.** The list says what. An optional
`## Blocked on` section says what this feature cannot know until the other lands. Four features in
the source invented that same heading independently before it was given a name.

**With the kit:** `plan view` prints the longest chain and the feature most others wait on.

**Worked example.** The example plan, as written:

```
$ plan view
…
Longest chain still to run · 5
  feature_report_inbox → feature_aggregate_store → feature_small_cell_suppression → feature_chart_parts → feature_site_trend_chart

Most waited on · feature_report_inbox
  7 unfinished features cannot start until it lands
```

The chart parts wait on the suppression design, because every part has to draw a suppressed cell.
Move that one dependency out of the field and into a sentence, and run it again:

```
Longest chain still to run · 3
  feature_checkin_rate_limit → feature_window_rehearsal → feature_operations_rehearsal

Most waited on · feature_report_inbox
  6 unfinished features cannot start until it lands
```

The plan now reports a different chain, two features shorter, in a different milestone. Nothing
about the work changed. Both runs are from 2 October 2026.

---

## 1.7 · Check it, and read where it stands

> **The agent** or **you** run the check · **You** read the census.

**Only a feature's status is kept by hand. Everything above a feature is computed.** The source
engagement started with three hand-kept status tables that could disagree, and did. A fourth copy
turned up during the move to a tree. On that day it was the only accurate one: three features had
merged that the other three showed as ready, blocked or in review.

**A computed view is not stored.** The source wrote its summary into every level's file for a week.
Every pull request that touched the plan rewrote it, and two features opened and closed in the same
week conflicted on a 118-line table neither had a reason to touch. It is now computed when asked for.

**No percentage, anywhere.** A percent-complete implies a schedule the plan cannot support.

What rolls up is a count:

- features by status
- each criterion, and how many features point at it
- the longest chain, and the feature most others wait on

**A feature that traces every criterion is left out of the count.** A rehearsal or a final
acceptance run answers all of them by definition. Counted, it makes each criterion look answered
whether or not anything builds it.

**"Answered" and "answered once" are different risks.** One feature behind a criterion means one
slip there is a slip of the milestone.

**With the kit:** `plan check`, then `plan view`. By hand, the checks are under *Evaluating the
quality*.

**Worked example.**

```
$ plan view milestone_incident_reporting_live
Milestone · Incident reporting is live
  1 design · 1 no-packet · 1 ready · 1 blocked · 1 in-progress · 5 done

Criteria · Incident reporting is live
  G1.1  3 features, 3 done
  G1.2  3 features, 1 done
  G1.3  1 feature, 0 done  ← answered once
  G1.4  1 feature, 0 done  ← answered once
  left out of the count: feature_reporting_acceptance_run traces every criterion
```

Five of ten done reads as half way. The criteria say otherwise: G1.4 rests on one feature, and that
feature is the open design question from step 1.3.

---

# 2 · Write a packet

A **packet** is everything in a feature's file above `## Record`. Copy
[`feature.md`](./templates/feature.md).

**The packet lives in the feature's file, not beside it.** The source began with packets in a
separate folder and plan nodes pointing at them. Moving ten of them into their nodes found three
features the plan called ready or needing design that had already merged, and two references to the
wrong design decision. A goal in one file and an intent in another say the same thing in different
words, and nothing checks they still agree.

**So "briefed" is a property of the file.** A feature has a packet when it has acceptance criteria
and verification. A pointer only ever proved a file existed somewhere.

## 2.1 · Choose what to brief next

> **You** choose.

Brief a feature just before it is built. **Do not write packets in bulk.**

A packet is a snapshot. Every path, command and name in it was true on the day it was written and is
a hypothesis afterwards. In the source, six packets were written in one sitting and sat unbuilt. One
described a script as broken that had been fixed the day after the packet was written.

**So a packet carries the date it was written**, as `briefed:`. Whoever picks it up re-checks what it
names against the repository, and reports what has moved as a finding against the packet. The first
column of a workflow asks for exactly that.

**With the kit:** `plan work --all` lists what has no packet. `plan view` says which of those the
most work waits on.

**Worked example.** Ten features have no packet. `feature_report_inbox` is the one seven others wait
on, so it was briefed on 1 October. `feature_site_trend_chart` waits, through the chart parts, on a
design decision nobody has taken. A packet for it today would describe a suppressed cell that does
not exist yet.

---

## 2.2 · Write the goal, the tie-breaker and the stop

> **You** write these three. They are the part an agent cannot draft from the specification.

| Section | Holds |
|---|---|
| `## Goal` | The outcome and why it matters, in two or three sentences |
| `## Where to err` | One sentence. The direction to lean when a trade-off appears and you are not there to ask |
| `## Done-when` | The stop condition, in words |

**`Where to err` is a heading of its own, and it is required.** In the source it began as an optional
clause inside the goal. It was the clause an author under time pressure did not write.

**It is also the part of a packet that survives the work.** The source measured what its packets got
wrong, across its first 129 finished features. 76 records named something the packet specified and
the work overrode. 21 named something the packet left out. What was overridden was almost all
mechanism. What held was the direction and the fence.

Write it as a direction, not a rule: *toward this, because that failure is worse than the other.*

**Worked example.** `feature_report_inbox`:

```markdown
## Where to err

Toward showing a report twice. A report two people both pick up costs a conversation. A report
nobody saw is the failure the platform exists to end.
```

No acceptance criterion says what to do when two members take one report in the same instant and the
update is slow. That sentence does.

---

## 2.3 · Point at the context, and spell out only what crosses

> **Agent** drafts from the specification · **You** cut.

`## Context` is **pointers, not paste**. A path and a section. The specification is not copied into
the packet, because the copy is the one that goes stale.

`## The contract to implement` holds **only what another feature depends on** – a name, a field, an
event. Spell those out exactly. Something else will match them literally.

**Leave everything that stays inside the feature to the design column.** This is the same
measurement as step 2.2. The cost of a prescribed mechanism is not the one that gets overridden –
that is cheap. It is the one that gets **obeyed**. In the source, one packet stated how many fields
a screen made editable and cited a specification number beside it. It read as settled. It survived
eight of fourteen columns, and was first seen to be wrong by the operator, in a screenshot.

Use [prompt B](./prompt.md#b-draft-a-packet) for the draft.

**Worked example.** `feature_report_intake_endpoint` names one thing:

```markdown
## The contract to implement

- Accepts exactly what the intake contract defines.
- **Emits `report.accepted` once per stored report**, carrying the report's identifier and nothing
  from its content. `feature_translate_on_intake` listens for this by name.
```

It does not say how a repeated report is recognised. That stayed inside the feature, was settled at
its design column, and is in its record.

---

## 2.4 · Draw the surface and the fence

> **You** write the fence. **The agent** may propose the surface.

`## Scope` has four parts. Two of them look alike and are opposites.

| Part | Binds? |
|---|---|
| **In scope** · **Out of scope** | Out of scope names what a reasonable agent would pull in and must not |
| **Expected surface (not a limit)** | **No.** A forecast of where the work lands. Reaching outside it needs no permission |
| **Do not touch** | **Yes.** A path that must not change goes here and nowhere else |

**They are separate because one section was doing both jobs.** The source had a single *files in
scope* list. Seven features declared a deviation from it and one had a criterion's file list struck
out. The fence beside it held nearly everywhere. A list that is wrong more often than right reads as
a fence to everyone downstream of it, and the real fence is lost in it.

**Worked example.** `feature_translate_on_intake`:

```markdown
**Expected surface (not a limit)**
- `reports/translation/`

**Do not touch**
- `contracts/` – a new field on the report is a contract change, and its own feature.
- `infra/translation/` – the grant is settled.
```

If the build finds it needs a new field on the report, the fence stops it. That is a different
feature, proved a different way, by a different workflow.

---

## 2.5 · Write the acceptance criteria and the verification

> **Agent** drafts · **You** check each one could fail.

`## Acceptance criteria` is the contract. Each row has a condition, an observable result, and the
test or the person that judges it.

`## Verification` is the evidence: the commands that must pass, and what is run and read back where
a command cannot show it.

**State properties, not counts.** "No report text reaches a log" is a property. "The suite is 291
tests" is a measurement, and in the source that one was 413. In the measurement behind step 2.2, 59% of
records named a packet claim that was false. Those packets were a day old at the median. The counts
had not gone stale. They had never been checked. Name the thing to count and let the work count it.

**Say what a pass has to include.** A green command shows the checks passed. It does not show they
all ran.

**Worked example.** From `feature_report_intake_endpoint`:

| # | Criterion | Test |
|---|---|---|
| 3 | WHEN any report is posted THE SYSTEM SHALL write no report content to the logs (H6) | read the log after each |

And what its record says the test turned out to need:

> Criterion 3 was checked by reading the log, and also by posting a fixture whose text is a marker
> string and searching every log stream for it. Reading the log by eye had passed while a debug
> stream nobody was looking at held the whole body.

The later packet for `feature_checkin_log_scrub` names the marker-string search in its criterion.
That is the record doing its job.

---

## 2.6 · Add only this feature's boundaries

> **You** write them.

`## Boundaries` holds what is specific to this feature. **Do not restate a level above.** The brief
is assembled with every boundary from the mission down.

Two kinds of line:

- ⚠️ **Ask first** – a decision this feature must hand back for. It halts an unattended run, so each
  one costs a stop. The engagement's standing stop list is in the constitution, not here.
- 🚫 **Never** – what no trade-off justifies.

**Worked example.** `feature_checkin_screens`:

```markdown
- ⚠️ **Ask first:** any wording on a check-in screen that the question set does not supply.
- 🚫 **Never:** analytics, or any third-party script, on a check-in screen.
```

The slice above it already says the questions' wording is agreed outside the build. The feature adds
the one case the slice does not cover: a line the question set does not supply at all.

---

## 2.7 · Bind a workflow and set the status

> **You** choose the workflow and change the status.

Name the workflow in the header. Choose it by **what has to run for the change to be proved**, not
by what the work is about. The table is in
[Part 6](../06-delivery-management/templates/workflows/README.md#choosing-a-workflow).

**Read every binding once against that table before the first feature starts.** In the source, every
unstarted feature was re-read on 6 August 2026 and 17 were rebound. The commonest error was the
repository workflow used as a catch-all: nine features whose proof needed a running environment, and
six that were pages a browser had to be pointed at.

Then set `briefed:` to today, and the status to `ready`, or to `blocked` if `blocked_by` names
anything unfinished.

**With the kit:** `plan check` refuses `ready` or `blocked` without a packet, `ready` while a
dependency is unfinished, and a packet with no `## Where to err`.

**Worked example.** Marking the design question from step 1.5 as ready:

```
$ plan check
error  …/feature_report_read_log: status is `ready` while waiting on feature_report_inbox
error  …/feature_report_read_log: status is `ready` with no packet – it needs `## Acceptance criteria` and `## Verification`, or the status `no-packet`

2 errors, 6 warnings.
```

---

# 3 · Keep the plan true

## 3.1 · Change status on the feature, and nowhere else

> **The agent** writes `in-progress` and `done`, in Part 6's `open` and `close` columns · **You**
> write every other change.

Three fields on a feature are kept by hand: `status`, `blocked_by`, and the `column` Part 6 writes
when a feature is claimed. Nothing else in the plan is a statement of where the work has got to.

**If a table of status exists anywhere outside the features, delete it.** It will disagree, and
step 1.7 has what that cost.

**Worked example.** No node above a feature in the example plan has a status, a count or a tick.
`plan work` on 2 October 2026:

```
2 design · 10 no-packet · 3 ready · 1 blocked · 1 in-progress · 1 in-review · 6 done
```

---

## 3.2 · Check the record when a feature finishes

> **The agent** writes the record at Part 6's `record` column · **You** read it before the merge.

Below the packet, a finished feature carries `## Record`. Its headings are a closed set.

| Heading | Holds |
|---|---|
| **Decisions taken** | Choices the packet did not settle. What was chosen, over what, and what would make it wrong |
| **Carried forward** | Gaps left on purpose, each with its consequence and what closes it. **This one travels** |
| **Verification actually run** | Where the packet's verification was not enough, and what was done instead |
| **Review** | What people said, as distinct from tests. Including what came back and changed nothing |
| **Panel tally** | The review panel's own count, pasted, not hand-counted |
| **Also fixed (not the feature)** | Repairs made on the way, so a later reader does not take them for the feature |
| **Lesson** | The one thing that applies to other work |

**It exists because the records were being written anyway, somewhere the plan could not see.** In
the source, two streams of work produced 126 durable records – 92 decisions taken in flight and 34
gaps left on purpose – and filed them in two documents outside the plan.

**The headings are closed because three authors invented three.** *Known trap, carried forward.
Known gap, carried deliberately. Open against this feature.* The template had no place for the idea,
so each made one.

**A done feature needs a Lesson, and either Decisions taken or Carried forward, with something in
them.** The first version of the check asked only whether the heading was there. The skeleton
shipped the heading with a comment under it. A feature could finish with the stub untouched and the
plan stayed green.

**Worked example.** `feature_report_intake_contract`:

```markdown
### Decisions taken

- **Unknown fields are rejected, not dropped.** Chosen over silently dropping them, which the first
  design did. A dropped field tells the supervisor the report was filed when part of it was thrown
  away. Wrong if the form and the contract are ever released separately – then a newer form would be
  refused by an older server.
```

*What would make it wrong* is the part to look for. Without it, the next person either re-argues the
decision or reverses it without knowing what it was for.

---

## 3.3 · Send what is left to somebody who will read it

> **The agent** writes it · **You** check each entry has a reader.

**Carried forward is the one part of a record written for somebody else.** It is copied, by its
exact heading, into the brief of every feature that depends on the writer – directly, or through
another feature.

In the source, two pieces of styling work hit the identical failure one day apart. The second
recorded it as the first one's lesson *"repeating exactly"*. The first had written it down. Nothing
carried it.

**It travels along dependencies and nowhere else.** A note for anybody the graph does not connect is
read zero times, and nothing about the file says so. Three features in the source were each told to
record a gap *so it reaches whoever builds* a later capability. No feature depended on any of the
three. The notes were right. They had no route.

So every entry has one of three readers:

| The entry is for | It goes |
|---|---|
| A feature that depends on this one | In *Carried forward*. Nothing more to do |
| A feature that does not, or work with no node yet | In *Carried forward*, **naming the destination in the entry** – a feature, or an issue |
| Nobody yet | An issue on the code host, cited as `issue #N` |

**"Whoever comes next" is not a destination.**

**A real finding that is not this feature goes to an issue when it is found**, not at the end. A
finding held for six columns is a finding dropped.

**Write `issue #31`, never a bare `#31`.** The code host numbers issues and pull requests in one
sequence. The source's first check accepted the bare form, and cleared three features whose only
match was a merged pull request.

**With the kit:** `plan check` warns when a done feature carries a *Carried forward*, nothing
depends on it, and no entry names a feature or an issue.

**Worked example.** `feature_report_intake_endpoint` left this:

| Gap | Consequence | When it closes |
|---|---|---|
| `report.accepted` is emitted after the write, not with it | If the process stops between the two, a report is stored and nothing is told. A consumer must not assume every stored report had an event | `feature_translate_on_intake` – it needs a way to find reports it was never told about |
| The size limit refuses with a generic reason, not a contract code | The form shows "could not be filed" with no cause | issue #31 |

`feature_translate_on_intake` depends on the endpoint. Its brief, assembled by the kit on 2 October
2026, carries that table under *Carried forward from upstream work*, along with the tables of the
two other features it is built on. Its third acceptance criterion – *when a stored report had no
event, the system shall still translate it* – exists because of the first row.

---

## 3.4 · Write your reading beside the census

> **You** write it.

A count cannot say that a milestone is unplanned, or that one date has no slack. You can. That goes
in a `## Reading` section in the level's own file.

**The test for which side a statement belongs on: could a program compute it from the features?**
If it could, it is computed and must not be typed. If it could not, it is your reading and belongs in
the file.

The split was found by building the source's generator. The first hand-written summaries mixed
counts with judgement, and the generator would have deleted the half it could not produce.

**Worked example.** The mission's reading:

```markdown
## Reading

**G2 is the gate with no slack.** The check-in window is two weeks, once a year, and its date was set
before the build started. Every other target can move by agreement. That one cannot.

**G4 is two placeholders.** Nothing under it has a packet. The tree gives it a node so that its
criteria have an owner, not because it is planned.
```

Nothing in `plan view` says either.

---

# Evaluating the quality

**These are yours to run, on the plan.** Do not ask the agent whether its own plan is good.

**The check is clean.** `plan check` exits 0. By hand: every `blocked_by` names exactly one feature,
no feature is `ready` while a dependency is unfinished, and no level above a feature carries a
status.

**Every criterion has a feature that builds it.** Read each milestone's criteria against
`plan view`. A criterion pointed at only by the rehearsal is not answered.

**Every slice's done-when is a demonstration.** Read each one and ask what you would watch. A
done-when that lists features is a checklist, and the slice is a folder.

**Read one packet as a stranger.** Take a `ready` feature. Without opening anything it does not
point at, say what is built, which way to lean, and what must not be touched. If you cannot, the
agent cannot.

**Search the packets for numbers.** Every count in a packet is a claim nobody checked. Each one
should be a property, or the name of the thing to count.

**Find each *Carried forward* entry's reader.** For each done feature, name the feature or the issue
every entry reaches.

**Read a dependency you kept in prose.** Search the packets for *after*, *once*, *depends on* and
*waits for*. Each is either a preference or a missing `blocked_by`.

---

# What's not solved yet

**This procedure has not been run from nothing.** The source plan was not laid out top down. It was
ported in one day from an existing backlog, and grew from there. Section 1's order – mission,
milestones, slices, features – is the model's order, not a recorded sequence of work.

**The kit and the source differ, and the guide follows the kit.** The differences:

| The source has | The kit |
|---|---|
| The build order written into each feature's file name, regenerated from the dependency graph | Computes the same order and prints it in `plan work`. A folder listing still sorts alphabetically |
| A check that every path a packet points at resolves | Does not check links |
| A warning when a packet's text cites an identifier its header does not carry | Does not read the text for identifiers |
| Labels for sprints, tracks and sizes | Ignores any header field it does not know |

**The example plan has never been built.** Its six finished features have records because a record
is what the guide has to show. They were written for the example, not produced by a run.

**Requirement and decision numbers are missing from the example.** Parts 1 and 2 are not written, so
the example's features trace to criteria, findings, boundaries and holdings only.

**Nothing here plans time.** The model refuses a schedule on purpose. If the client needs dates below
a milestone, they are kept somewhere else, and this guide does not say where.

**The planning cost is not measured.**

**The prompts have not been run.**

---

<!-- DRAFTING ONLY -->

## Source material

- `platform/plan/model.md` – the levels, what every node carries, identity, status vocabulary,
  derived views, the packet, the record, issues, non-goals, and the decisions log.
- `platform/plan/README.md` – the workflow-selection table and the rebinding of 6 August 2026.
- `platform/plan/templates/feature.md` – the packet skeleton.
- `platform/plan/tree/` – read for shape only. No content from it is published.

## Where each figure was read – all on 2026-10-02

| Figure | Source |
|---|---|
| 379 features, 325 done, three milestones, 34 slices | counted from `tree/` – 417 files, 38 of them `README.md`; `status:` lines tallied |
| Median one day briefed to merged across 72 features, maximum three; 59% of records name a false packet claim; 291 that was 413 | `model.md` §13, row of 2026-08-11 |
| 76 overridden against 21 left out, across the first 129 finished features; eight of fourteen columns | same row |
| Seven features declared a deviation from the file list; one criterion's list struck | same row |
| Seven "cannot start" edges in prose; chain 3 reported, 5 real; wrong chokepoint | `model.md` §13, row of 2026-07-29 on `blocked_by` |
| Three hand-kept tables; a fourth copy the only accurate one; three features merged | `README.md` §Why this exists; `model.md` §13, row of 2026-07-29 on the fourth copy |
| A 118-line table; one week; two features conflicting | `model.md` §8b |
| Ten packets migrated; three already merged; two wrong decision references | `model.md` §11b |
| Six packets in one sitting; one script fixed the next day | `model.md` §6, `briefed:` |
| 126 records: 56 + 36 decisions, 34 gaps | `model.md` §11c table |
| Three invented headings, quoted | `model.md` §11c |
| Four features invented `Blocked on` | `model.md` §7 |
| Two pieces of work a day apart, "repeating exactly" | `model.md` §11c |
| Three features with no route | `model.md` §11c |
| Bare number cleared three features | `model.md` §11c |
| 17 rebound on 6 August 2026; nine and six | `README.md` §Status of the port |
| Infrastructure ceased to be a slice | `model.md` §13, row of 2026-07-29 on slices |

## Generalised, not dropped

- The source's `traces.gate` criteria are numbered by a contract annex. Published as "the acceptance
  schedule", numbered `G1.1`.
- "Styling units" became "pieces of styling work". The named later capability in the no-route
  failure became "a later capability".
- The obeyed-prescription failure named a screen and a field count. Published as "how many fields a
  screen made editable".

## Open

- Whether the kit should write the build order into file names, as the source does.
- Parts 1 and 2 will introduce requirement and decision numbers. The example plan's `traces:` should
  gain them then.

<!-- END DRAFTING ONLY -->
