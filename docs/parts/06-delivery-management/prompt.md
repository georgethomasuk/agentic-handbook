**Status** template – copy into an agent session · **Life** living · **Reader** the agent, not you

# The agent prompts

Three prompts, one per kind of session. Paste each one into a **fresh** agent session. Fill every
bracketed placeholder first.

**With [the kit](./kit.md) you need only prompt A.** `plan resolve` does what B does and `plan prompt`
does what C does. B and C are the by-hand route, and the only route for a workflow in a mode.

| Prompt | Guide step | How often |
|---|---|---|
| [**A · Fill the slots**](#a-fill-the-slots) | 1.2 | Once per engagement, and again when a new workflow is first used |
| [**B · Resolve a workflow**](#b-resolve-a-workflow) | 1.6, by hand | Once per workflow, and again whenever a source file changes |
| [**C · Assemble a brief**](#c-assemble-a-brief) | 2.2, by hand | Once per feature, and again to resume one at a later column |

Steps 1.3, 1.4 and 1.5 are yours. There is no prompt for agreeing the two lists, for filling your own
tooling slots, or for watching a check fail.

**There is no prompt for running a feature.** The brief that prompt C produces is that prompt.

The human-readable account of why it is shaped this way is in [the guide](./README.md). The agent does
not need that; it needs this.

---

## A · Fill the slots

Paste this with the templates already copied into the repository.

```markdown
You are proposing values for the engagement-specific slots a workflow needs. You will propose; I
decide. Do not start any feature work.

Workflow folder: [path to plan/workflows]
The values file: [path to plan/values.yaml]
The workflow being set up: [workflow name]
The constitution: [path]
The threat model's boundary table: [path]

## What to read

Read `core.yaml` and `[workflow name].yaml`. List every `{{project.*}}` slot either file uses. Those
are the only slots in scope. Ignore every `{{tooling.*}}` slot – those are mine.

Read each slot's entry in `slots.yaml`: `what` it needs, how to meet it `by_hand`, and the `example`.
The example is from a different system. Never copy it.

## What to propose

For each slot in scope, find the fact in this repository and propose a value. Show me a table:

| Slot | Proposed value | Taken from |

`Taken from` is a file path and the line you read. If the repository does not hold the fact, write
`not found` and what you looked for. Do not infer a value from what such a repository usually has.

Where the slot is a command, run it once and tell me the exit status. Do not run a command that
deploys, applies, pushes or deletes.

## Three slots you do not fill

`project.stop_list`, `project.decide_and_disclose_list` and `project.real_data_policy` are decisions,
not facts. List them as `for the operator` and propose nothing.

## Writing

Write nothing until I have replied to the table. Then write each value I confirmed into the values
file, under `project:`, keyed by the slot's name without its `project.` prefix. Write no other key.

You may edit the values file. You may not edit `slots.yaml`, `core.yaml`, any workflow file, the
constitution or any source code.

## Report back

When finished, tell me: how many slots were in scope, how many now have a value, which are still
unfilled and why, and every command you ran with its exit status.
```

---

## B · Resolve a workflow

Paste this once every slot the workflow uses has a value.

```markdown
You are joining three files into one. This is mechanical. Change no wording, make no judgement, and
improve nothing.

Workflow folder: [path to plan/workflows]
The workflow to resolve: [workflow name]
The mode, if any: [mode name, or none]
The values file: [path to plan/values.yaml]
My tooling values, if they are in a file of their own: [path, or none]

Write the result to `resolved/[workflow name].yaml`, or `resolved/[workflow name].[mode].yaml` for a
mode. Write no other file.

## The rules

Work down the workflow file's `columns` list in order.

1. A column with its own `name` and no `use:` is copied as it is.
2. `use: core.<name>` – copy that whole column from `core.yaml`.
3. `as: <name>` on that column – replace the copied column's `name`.
4. `also:` on that column – append each field under it to the field of the same name in the copied
   column. Text is appended as further paragraphs. A list gains the items at its end. A nested block
   such as `delegate` or `compact` is appended field by field in the same way. A field the copied
   column does not have is added.
5. `seeds:` on that column – keep it on the copied column as `seeds`.
6. Keep the workflow's `name`, `description`, `agreed_at`, `unattended_from` and `unit` at the top.
   Drop `uses`.
7. Copy `stage_protocol`, `exit_kinds`, `report_back`, `compaction` and `delegation` from `core.yaml`
   to the top of the result.
8. `standing_constraints` – the core's list first, then the workflow's own.
9. Replace every `{{project.x}}` and `{{tooling.x}}` with that slot's value, from the values file.
   Where both files give a value for one slot, the values file wins.
10. Leave `modes:` out. If I named a mode, apply its changes column by column after rule 9: replace
    or extend the entry of each column it names, remove each column it marks `skip`, add each column
    it defines, and use its own `agreed_at`, `unattended_from` and `standing_constraints`.

Open the result with one comment line: the three source files, today's date, and
`Do not edit – change the sources and resolve again.`

## If a slot has no value

Stop. Do not write the file. Tell me which slots are unfilled. Never substitute the slot's `example`.

## Check

Run both and show me the output. Each must print 0.

    grep -c '{{' resolved/[file]
    grep -c 'use: core' resolved/[file]

Then confirm the file parses as YAML, and list the column names in order.

## Report back

The path written, the column names in order, the two counts, and anything in the workflow file the
rules above did not cover. Do not resolve that part by guessing – name it and leave it.
```

---

## C · Assemble a brief

Paste this when a feature's packet is written and you have bound a workflow to it.

```markdown
You are assembling the brief for one feature. You are not doing the feature. Do not read the source
code, do not propose a design, and do not start the first column.

The feature: [path to the feature's file]
The plan's root: [path]
The resolved workflow: [path to resolved/<workflow>.yaml]
The brief skeleton: [path to brief.md]
The column to start at: [column name, or "first"]
Write the brief to: [path, e.g. .work/<feature>/brief.md]

## The rule that matters

Copy. Do not summarise, shorten, reorder or reword anything you take from the plan or the workflow.
The session that reads this brief re-reads its column later and must find the same text.

## Build it in the skeleton's order

Fill the skeleton from top to bottom. Each bracketed line says where its content comes from.

**The ask.**

1. The title, then one line: every level above the feature by name, the feature's status, and the
   date its packet was written.
2. The outward identifiers the feature declares. Leave the line out if there are none.
3. The column to start at, its position, and every column name in order with the current one in bold.
   If I wrote "first", say in that line that the column is assumed, not recorded.
4. `stage_protocol`, unchanged. Then the unattended line, only if the workflow has `unattended_from`.
5. The feature's Goal section, and the path to its file from the repository root.
6. The starting column, whole: `precondition`, `delegate`, `review_each_step`, `entry`, `produces`,
   `exit`, `compact`, in that order, leaving out any it does not have. Then `standing_constraints`.
7. `report_back`.
8. `compaction` – only if the starting column or any later one carries `compact:`.
9. `delegation` – only if the starting column or any later one carries `delegate:`.

**The context.**

10. The Goal section of every level above the feature, top down.
11. The Boundaries section of every level above the feature that has one, top down.
12. The feature in full – everything in its file above `## Record`.
13. The Inherited context section of every level above that has one.
14. Each feature this one depends on, with its status. Mark any that is not done.
15. From every feature this one depends on – directly, or through another – its `### Carried forward`
    section, found by that exact heading. Nearest dependency first. A heading spelled any other way
    is not lifted: list it in your report instead.
16. Every column after the starting one, whole, in order.

## What you may not do

Do not restate the starting column in the context, or the context in the ask. Do not add advice of
your own. Do not write to the plan, the workflow or the feature's file.

## Report back

Tell me: the path written; the number of words before the sentence that names the column; which
sections you left out and why; every dependency that is not done; and any record heading that looked
like `Carried forward` but was not spelled that way.
```
