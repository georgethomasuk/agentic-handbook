**Status** draft – tested, and not yet run on a real feature · **Life** living · **Reader** you, the operator, setting the kit up and running a feature with it

# The kit

The kit is one command, `plan`. It does the mechanical steps of [the guide](./README.md): it joins a
workflow, assembles a brief, prints a column when the agent enters it, and makes the two edits to the
plan that claim a feature and close it.

**It replaces prompts B and C, and the by-hand line of nine tooling slots.** It does not replace
any judgement. Choosing the workflow, agreeing the two lists and answering a gate are still yours.

**It has not run a real feature.** It has tests, and one walk through its commands on the example
plan. [What it has not proved](#what-it-has-not-proved) is the list to read before relying on it.

| | |
|---|---|
| Source | [`kit/` in the handbook's repository](https://github.com/georgethomasuk/agentic-handbook/tree/main/kit) |
| Needs | `git`. Either [`uv`](https://docs.astral.sh/uv/), or Python 3.11 or later with PyYAML. `gh`, only for `land: pr` |
| Licence | CC0, as the prompts and templates are |

---

## What it reads and what it writes

| | Where | The kit |
|---|---|---|
| The plan | `plan/tree/` | Reads it. Edits two things: the claim, and the close |
| The workflows | `plan/workflows/` | Reads them. Never edits them |
| Your slot values | `plan/values.yaml` | Reads it |
| Where things are | `plan/kit.yaml` | Reads it |
| Working state for one feature | `.work/<feature>/` | Writes it. Ignored by version control |
| Retros | `plan/retro/` | Creates one empty file per run |

**Everything it prints is worked out at that moment.** There is no resolved workflow on disk and no
stored brief the kit trusts. A stored copy is a copy that can fall behind its sources.

---

## 1 · Install it

> **You** do this once per machine.

Clone the handbook and put its `kit/` folder on your path.

```
$ git clone https://github.com/georgethomasuk/agentic-handbook.git ~/tools/agentic-handbook
$ export PATH="$HOME/tools/agentic-handbook/kit:$PATH"
$ plan --help
```

**Add the folder to the path. Do not link the script into another folder.** `plan` finds its Python
file and the workflow templates from where it sits, and a link moves it.

With `uv` installed there is nothing else to set up. Without it, `plan` runs under `python3`, which
needs PyYAML.

---

## 2 · Write a plan directory

> **You** run one command in the client repository.

```
$ plan init .
wrote plan – the workflows, kit.yaml and values.yaml. Fill values.yaml, write the tree, then run `plan check`.
```

It copies the workflow templates, writes `kit.yaml` and an empty `values.yaml` with one line per
`project.*` slot, and adds `.work/` to `.gitignore`. It refuses if `plan/kit.yaml` already exists.

**To try the kit before you have a plan,** add `--example`. That also copies [the example plan](../05-delivery-planning/example-plan.md) – 24 features on
[the example system](../../reference/example-system.md) – and fills every project slot from the slot's
own example.

**Then set how a claim reaches the main branch.** One line in `kit.yaml`:

| `land:` | A claim or a close is | Use it when |
|---|---|---|
| `pr` | A pull request holding only the plan edit, merged when its checks pass | The main branch is protected. This is the default |
| `push` | Pushed straight to the main branch | Nothing protects the main branch |
| `none` | Made in your working copy and nowhere else | You land it yourself |

**Worked example.** On the example system the main branch is protected, so `land: pr` stays.

---

## 3 · Fill the values

> **You** fill `plan/values.yaml`. Guide steps 1.2 to 1.4 say how to decide each one.

```yaml
project:
  constitution: "AGENTS.md"
  full_gate: "make check"
```

**The tooling slots are already filled.** The kit carries a value for all 24, in `kit/tooling.yaml`.
To change one – the three model tiers at least – write a file of the same shape and name it in
`kit.yaml` under `tooling_values`, or in `PLAN_TOOLING_VALUES`.

Three places can hold a value. The first that has it wins.

| Order | File | Holds |
|---|---|---|
| 1 | `plan/values.yaml` | The engagement's values. `tooling:` entries here win too |
| 2 | Your own tooling file | How you work, on every engagement |
| 3 | `kit/tooling.yaml` | The kit's own commands |

**A slot with no value stops the command and is named.** The kit never falls back to the slot's
example, which describes another system.

```
$ plan check
error  workflow `build-in-repository` is bound by a feature and slot `project.full_gate` has no value

1 error, 0 warnings.
```

`plan check` asks only for the slots of workflows a feature has bound. You do not fill 77 slots to
run one workflow.

---

## 4 · Run one feature

> **You** start it. **The agent** runs every command from `plan enter` on.

The worked example is the guide's: the rate limit on the public check-in endpoint. Every block below
is output from runs on 2 October 2026, against a local repository with `land: push`. The archive
path is shortened, and the queue is cut to its ready features.

**See what can start.** A feature is listed as ready only when everything it depends on is done.

```
$ plan work
2 design · 10 no-packet · 3 ready · 1 blocked · 1 in-progress · 1 in-review · 6 done
…
Ready
  feature_checkin_log_scrub – No check-in content in the operational exhaust
    build-in-repository · wave 3
    plan prompt feature_checkin_log_scrub
  feature_checkin_rate_limit – Rate limit on the public check-in endpoint
    build-in-repository · wave 3
    plan prompt feature_checkin_rate_limit
  feature_report_inbox – The report inbox
    build-in-browser · wave 4
    plan prompt feature_report_inbox
…
```

A **wave** is the earliest point a feature could start, counted from the dependencies alone.
Features in one wave do not depend on each other.

**Assemble the brief.** The kit prints the count the guide tells you to check.

```
$ plan prompt feature_checkin_rate_limit -o .work/feature_checkin_rate_limit/brief.md
wrote .work/feature_checkin_rate_limit/brief.md – 10321 words, 47 before the sentence naming the column.
```

Hand that file to a fresh session. From here the agent runs the commands, because the brief and
every column tell it to.

**The agent enters a column, and the column is printed.** Entering is the command that prints the
instructions. There is no separate "mark the stage" step to forget.

```
$ plan enter feature_checkin_rate_limit check
Column `check` – 1 of 12 in `build-in-repository`. **`check`** → `open` → `frame` → …

Say which column this is, then restate in your own words what it asks and what ends it, from the text
below. Stop at its exit conditions.
…
```

**The agent claims the feature.** The claim is two lines in the feature's file: `status: in-progress`
and the column the work will be in. It is made in a throwaway copy of the main branch, never in the
working branch, so the claim lands on its own.

```
$ plan claim feature_checkin_rate_limit --land
landed on origin/main, and this branch now contains it.
$ plan claim-check feature_checkin_rate_limit; echo $?
0
```

The commit on the main branch reads `plan(open): claim Rate limit on the public check-in endpoint`.

**Each column's first exit checks the column was entered.** It passes only for the most recent one.

```
$ plan enter-check feature_checkin_rate_limit check
plan: the most recent column entered for feature_checkin_rate_limit is `open`, not `check`
```

**After the merge, the agent closes, archives and releases, in that order.**

```
$ plan close feature_checkin_rate_limit --pr 12 --land
landed on origin/main.
$ plan retro feature_checkin_rate_limit
wrote plan/retro/2026-10-02-feature_checkin_rate_limit.md – five labelled lines, …
$ plan archive feature_checkin_rate_limit
archived .work/feature_checkin_rate_limit/journal.md to …/feature_checkin_rate_limit.md – 6 lines, read back.
$ plan release feature_checkin_rate_limit
released .work/feature_checkin_rate_limit.
```

**`release` refuses until the journal is archived and the copy matches.** Run before the archive, it
printed this and exited 1:

```
$ plan release feature_checkin_rate_limit
plan: PLAN_JOURNAL_ARCHIVE is not set – nothing archived. An archive step that succeeds having
copied nothing leaves you believing there is an archive.
```

The destination is an environment variable because it is your own records, outside the client's
repository. Guide step 1.5 has the failure this guards against.

---

## The commands

| Command | Who runs it | What it does |
|---|---|---|
| `plan init <dir> [--example]` | You | Writes a plan directory |
| `plan check` | You, and the agent at `record` | Checks the templates, the plan and the retros. Exits 1 on any error |
| `plan work [--all]` | You | Unfinished features by state, with the command that briefs each |
| `plan view [node]` | You | The census for one node or the whole plan: counts by status, each criterion and what points at it, the longest chain, the feature most others wait on. Computed, never stored |
| `plan show <feature> [--field f]` | Either | The feature's header fields, or one of them |
| `plan resolve <workflow> [-o file]` | You | One workflow, joined and filled, to read |
| `plan prompt <feature> [--column c] [--column-only] [-o file]` | You | The brief. `--column` starts it at a later column |
| `plan enter <feature> <column>` | The agent | Records the column, then prints it |
| `plan enter-check <feature> <column>` | The agent | Passes if that column was the last one entered |
| `plan claim <feature> [--land]` | The agent | `ready` to `in-progress`, with the column |
| `plan claim-check <feature>` | The agent | Passes if the claim is on the main branch and in this branch |
| `plan close <feature> --pr N [--merged date] [--land]` | The agent | `done`, the column removed, the merge date written |
| `plan close-check <feature>` | The agent | Passes if the feature reads done on the main branch |
| `plan retro <feature>` | The agent | Creates the run's retro file, five labels |
| `plan archive <feature>` | The agent | Copies the journal to `PLAN_JOURNAL_ARCHIVE` and reads it back |
| `plan release <feature>` | The agent | Removes `.work/<feature>/`, once the journal is archived |

A feature is named by its file name without `.md`, or by its path under `plan/tree/`.

Three environment variables: `PLAN_ROOT` names the plan directory where the kit cannot find it by
walking up, `PLAN_TOOLING_VALUES` names your tooling file, `PLAN_JOURNAL_ARCHIVE` is where journals
go.

---

## What `plan check` checks

| In | It fails on |
|---|---|
| The templates | A slot used and not defined · a slot with no `what`, `by_hand` or `example` · a bound workflow with an unfilled slot · a column marked to compact both ways · a human gate that does not block inside an unattended stretch |
| The plan | A level in the wrong place · a missing title, goal or done-when · a container with no boundaries · a `blocked_by` that names nothing · a dependency loop · a status that contradicts its blockers · a `ready` feature with no packet or no workflow · a packet with no `## Where to err` · a milestone criterion no feature traces to · a feature tracing a criterion its milestone does not declare · a date on anything but a milestone · a column the workflow does not have · a record heading outside the closed set · a done feature with no record or no lesson |
| The retros | A file over 60 lines · a missing label |

It warns, without failing, on a slot nothing uses, a done feature with no merge date, a feature in
flight with no column, a criterion answered by one feature only, and a *Carried forward* note that
no later feature will read.

**It found a defect in the published templates on its first run**, on 2 October 2026. One column
was marked both to offer compaction and never to compact. The template is fixed.

---

## What the plan must look like

[Part 5](../05-delivery-planning/README.md) is the guide to writing one, and
[the example plan](../05-delivery-planning/example-plan.md) is a whole one. This is the short form of
what the kit reads.

**A level is a folder with a `README.md`. A feature is a file.** The name's prefix says the level:
`mission_`, `milestone_`, `slice_`, `feature_`.

A feature's header:

```yaml
---
title: Rate limit on the public check-in endpoint
status: ready
workflow: build-in-repository
blocked_by: [feature_anonymous_checkin_token]
briefed: 2026-09-28
traces:
  gate: [G2.3]
  finding: [F-51]
  boundary: [B3]
---
```

| Section | On | The kit |
|---|---|---|
| `## Goal` · `## Done-when` | Every node | Requires both. Copies the goal of every level into the brief |
| `## Boundaries` | Every level above a feature | Requires it. Copies each into the brief |
| `## Inherited context` | Any level above a feature | Copies it into the brief |
| `## Acceptance criteria` · `## Verification` | A feature | Together these are what makes a feature *briefed* |
| `## Where to err` | A briefed feature | Requires it |
| `## Record` | A done feature | Requires a filled-in *Lesson*, and *Decisions taken* or *Carried forward* |

Everything in a feature's file above `## Record` is copied into its brief unchanged.

**The record's headings are a closed set:** Decisions taken · Carried forward · Verification actually
run · Review · Panel tally · Also fixed (not the feature) · Lesson. *Carried forward* is copied by
that exact heading into the brief of every feature that depends on this one, directly or through
another. A heading spelled another way is not copied, so the check rejects it.

**The seven statuses:** `design` · `no-packet` · `ready` · `blocked` · `in-progress` · `in-review` ·
`done`. The kit moves a feature from `ready` to `in-progress` and to `done`. Every other change is
yours.

**A milestone may declare criteria**, as `traces: {gate: […]}`. Every feature under it then says
which it answers, or `inherit`.

---

## What it has not proved

**No feature has been built with it.** The walk above runs every command. It does not run a session
through twelve columns.

**`land: pr` has only met a stand-in.** The tests run it against a script that plays the code host.
Raising a real pull request, waiting on real checks and merging it are untested.

**Modes are refused.** `plan resolve --mode` exits with an error, and a feature with `mode:` gets a
warning and the full workflow. Resolve a mode by hand, with prompt B.

**It does not run a review panel.** `panel_runner` is the by-hand line, so `panel` needs you present.

**Left in the tooling it was extracted from, and not rebuilt here:**

| Not in the kit | By hand instead |
|---|---|
| A panel runner | One fresh session per seat. You paste the findings back |
| A cost-per-column report | Not measured. The column markers in `.work/<feature>/stages.jsonl` are the raw material |
| A journal scaffold per build step | The agent writes the journal's headings itself |
| A picture of the whole plan | `plan view` prints the census. Nothing draws the levels against the build order |
| The build order written into file names | `plan work` prints each feature's wave. A folder listing still sorts alphabetically |
| Checks that a packet's links resolve, and that an identifier its text cites is in its header | Read them yourself |

---

## Changing the kit

```
$ scripts/test-kit.sh
```

It runs the kit's tests, then `plan check` on a fresh copy of the example plan. Every test builds its
own repository in a temporary folder, with a local remote, so nothing touches a real one.
