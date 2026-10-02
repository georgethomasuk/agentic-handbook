**Status** template – copy into an agent session · **Life** living · **Reader** the agent, not you

# The agent prompts

Two prompts, one per kind of session. Paste each one into a **fresh** agent session. Fill every
bracketed placeholder first.

| Prompt | Guide step | How often |
|---|---|---|
| [**A · Draft the tree**](#a-draft-the-tree) | 1.3 to 1.6 | Once per milestone, when its acceptance criteria are known |
| [**B · Draft a packet**](#b-draft-a-packet) | 2.3 to 2.5 | Once per feature, just before it is built |

**Neither prompt writes a goal you have not seen.** Both stop and show you a draft. The goal, the
*where to err* and the fence are yours – guide steps 2.2 and 2.4.

**There is no prompt for the record.** It is written by the session that did the work, at the
`record` column of its workflow. That is [Part 6](../06-delivery-management/README.md).

The human-readable account of why it is shaped this way is in [the guide](./README.md). The agent
does not need that; it needs this.

**Neither prompt has been run.** They are written from the guide.

---

## A · Draft the tree

Paste this with the plan folder created and the mission written.

```markdown
You are drafting part of a delivery plan. You propose; I decide. Write no code and start no feature.

The plan's tree: [path to plan/tree]
The mission: [path to its README.md]
The milestone to draft: [its name, and who accepts it]
The acceptance criteria it is judged by: [path, or pasted, with their own numbers]
The specification: [paths – requirements, decisions, threat model, design]
The two skeletons: [path to container.md and feature.md]

## What to read

Read the mission's README, the acceptance criteria and the specification. Read every existing node
under the tree, so you name nothing twice.

## What to draft, in this order

1. **Confirmation statements.** One plain sentence per acceptance criterion, saying what will be
   true. Keep the criterion's own number. Do not copy its wording.
2. **Slices.** Group the statements into capabilities somebody could watch working. For each, write
   a done-when that names what is demonstrated, and on what. If you cannot, it is not a slice – say
   so and leave the features on the milestone.
3. **Features.** For each slice, the features it needs. For each: a title, a goal of two or three
   sentences, a done-when, and which criteria it answers.
4. **Dependencies.** For each feature, every other feature it cannot start without. Only "cannot
   start". Give the reason in one clause.

Show me all four as tables before writing any file:

| Criterion | Confirmation statement | Answered by |
| Slice | Done-when |
| Feature | Under | Answers | Cannot start without | Why |

## Rules

- Name a slice for a capability, never for an area of the code. "Infrastructure" is not a slice.
- Name a feature for what it is. No numbers of your own.
- A feature that serves every slice hangs from the milestone, with `traces.gate: inherit`.
- Where the specification does not settle how a feature would be built, do not settle it. Mark the
  feature `design` and write the open question.
- Every criterion must be answered by at least one feature that builds it. A rehearsal or an
  acceptance run that answers all of them does not count. List any criterion left with nothing, or
  with one feature only.
- Do not estimate. No sizes, no dates, no order beyond the dependencies.

## Writing

Write nothing until I have replied to the tables. Then, for what I confirmed:

- The milestone and each slice: a folder with a `README.md`, from the container skeleton. Fill Goal,
  Done-when and the confirmation statements. Leave Boundaries as a list of questions for me – I
  write those.
- Each feature: a file from the feature skeleton, with the header, Goal and Done-when filled, status
  `no-packet` or `design`, and every section from `## Where to err` down removed.

You may write under the plan's tree. You may not edit the mission, any existing node, or anything
outside the tree.

## Report back

The nodes written, by path. Every criterion answered once or not at all. Every feature marked
`design`, with its question. Every dependency you were unsure of. Then, if the kit is installed, run
`plan check` and show me its output unchanged.
```

---

## B · Draft a packet

Paste this for one feature whose status is `no-packet`, with nothing it depends on still undesigned.

```markdown
You are drafting the packet for one feature – the brief another session will build from. You are
not building it. Write no code, and do not design the solution.

The feature: [path to its file]
The plan's tree: [path to plan/tree]
The specification: [paths]
The constitution: [path]
The feature skeleton: [path to feature.md]
Today's date: [YYYY-MM-DD]

## What to read

1. The feature's file, and the README of every level above it.
2. Every feature named in its `blocked_by`, and every feature those name. Read each one's
   `## Record`, and above all `### Carried forward`.
3. The parts of the specification its `traces:` point at.
4. The repository, where the feature will land. Read it. Do not infer it.

## What to draft

Fill the skeleton's sections from `## Context` to `## Verification`. Leave `## Goal` and
`## Done-when` as they are. Leave `## Where to err`, **Do not touch** and `## Boundaries` empty, each
with a one-line suggestion marked `SUGGESTION:` – those are mine to write.

**Context.** Paths and section names. Paste nothing from the specification. Name one existing file
whose shape to follow, or write "none yet".

**The contract to implement.** Only what another feature will depend on: a name, a field, an event,
an interface. Find these by reading the features that name this one in their `blocked_by`. If
nothing crosses, write "Nothing another feature depends on". Do not describe how the feature works
inside.

**Scope.** In scope, out of scope, and the expected surface. Head the surface
"Expected surface (not a limit)".

**Acceptance criteria.** A table: number, criterion, test. Write each criterion as
WHEN … THE … SHALL …, with a result somebody could observe. Each needs a test, or a named person
who judges it. Add a criterion for every upstream *Carried forward* entry that names this feature.

**Edge cases.** Each as: case → expected behaviour.

**Verification.** The commands that must pass, copied from the constitution, never invented. Then
what must be run and read back that a command cannot show. Then a "Green means" line.

## Rules

- State properties, not counts. Never write how many tests, files, fields or records there are. Name
  the thing to count.
- Every path, command and name you write must be one you read in the repository in this session.
  If you did not read it, do not write it.
- Do not restate a boundary from a level above.
- If the feature cannot be briefed without a design decision nobody has taken, stop. Write nothing,
  and tell me the decision.

## Writing

Show me the draft before writing it. Then write it into the feature's file, set `briefed:` to
today's date, and change nothing else in the header. I set the status.

You may edit that one file. You may not edit any other node, the specification or any source code.

## Report back

Which upstream *Carried forward* entries you used, and which you judged did not apply and why.
Everything the packet names that you could not find in the repository. Every place the
specification and the repository disagreed. The three sections left for me.
```
