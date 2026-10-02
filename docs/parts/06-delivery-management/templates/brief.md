# [feature title]

[mission › milestone › slice › feature, by name] · status [status] · packet written [date]

[the outward identifiers the feature declares – requirement, decision and finding numbers. Leave the line out if it declares none]

## Your task

**Start at column `[column]` – [n] of [N] in `[workflow]`.** [every column name in order, the current one in bold]

[`stage_protocol` from the resolved workflow, unchanged]

[only if the workflow names `unattended_from`] **From `[column]` on, this workflow runs unattended.**
Roll from column to column without a check-in. Stop only at a blocking human gate or on the stop list
in [where the stop list is kept]. Read that list before entering `[column]`.

**The goal**

[the feature's own Goal section, unchanged]

**The contract** is the packet reproduced under `## This feature` below. Its acceptance criteria are
the contract and its verification commands are the evidence. Its file is `[path from the repository
root]`. There is no second brief to find.

## Column · `[column]`

About the `[workflow]` workflow: [the workflow's `description`, unchanged]

[the column, from the resolved workflow, unchanged and in this order: `precondition`, `delegate`,
`review_each_step`, `entry`, `produces`, `exit`, `compact`]

### Standing constraints – every column, every time

[`standing_constraints` from the resolved workflow, unchanged]

## How to report back

[`report_back` from the resolved workflow, unchanged]

## The journal, and when to compact

[`compaction` from the resolved workflow, unchanged. Leave the whole section out if no column in this
brief carries `compact:`]

## Columns that send work to a worker

[`delegation` from the resolved workflow, unchanged. Leave the whole section out if no column in this
brief carries `delegate:`]

---

## Standing context

Everything below is assembled from the plan. It is the context for the task above, not a second set
of instructions, and it does not restate the column.

## Why this exists – the goal chain

### Mission · [title]

[its Goal section, unchanged]

### Milestone · [title]

[its Goal section, unchanged]

### Slice · [title]

[its Goal section, unchanged. Leave out a level the feature does not sit under]

## Boundaries inherited from above

These accumulate. A feature cannot widen a fence set above it. If the work starts reaching past one
of these, it has left its scope – stop.

### From the [level] · [title]

[its Boundaries section, unchanged. One block per level that has one]

## This feature

[the packet, in full and unchanged – everything in the feature file above `## Record`]

## Settled above – do not reopen

### From the [level] · [title]

[its Inherited context section, unchanged. Leave the whole section out if no level has one]

## Depends on

- `[feature]` – [title] · [done, or **its status – not yet met**]

## Carried forward from upstream work

Gaps and traps left deliberately by the features this one is built on, nearest dependency first. Each
was written for whoever came next. That is you. Nothing else in this brief repeats them.

### From `[feature]` · [title]

[its `### Carried forward` section, unchanged. One block per feature this one depends on, directly or
through another. Leave the whole section out if none of them wrote one]

## The rest of the workflow

The [n] columns after `[column]`, in order, exactly as the workflow states them. **Do not start any
of them now, and do not work from this copy.** It is here for reading ahead. Enter each column the
way the stage protocol says, and work from what that prints.

### `[column]` – [n] of [N]

[the column, from the resolved workflow, unchanged. One block per remaining column]
