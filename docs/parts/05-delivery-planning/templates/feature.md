---
title: "[what this is, in a few words]"
status: no-packet        # design · no-packet · ready · blocked · in-progress · in-review · done
workflow: "[the workflow this will run – Part 6]"
blocked_by: []           # hard dependencies only – "cannot start", not "would rather not"
briefed:                 # the day this packet is written – YYYY-MM-DD
pr:                      # written when the work is recorded – the change that closed this
merged:                  # written at close, after the merge – read from the code host, never typed
traces:
  gate: []               # the milestone criteria this answers – or the word inherit
  finding: []            # one line per kind of identifier somebody outside the build owns:
  decision: []           # a requirement, a decision, a finding, a boundary. Delete what is unused
---

<!--
  One feature. This file is the plan node and the agent's brief. There is no second document.

  Everything above `## Record` is the packet – written before the work, by whoever plans it.
  `## Record` is written after, by whoever did it.

  Point at the specification. Do not paste it.
  State properties, not counts. Name the thing to count and let the work count it.
  Delete each comment as you fill the section under it.
-->

# Feature · [short name]

## Goal

[The outcome and why it matters. Two or three sentences. Not a restatement of the criteria below –
this is what the agent falls back on when the criteria run out.]

## Where to err

[One sentence. The direction the work leans when a trade-off appears and you are not there to ask.
A direction, not a rule: "Toward … A … is …; a … is …."]

## Done-when

[The stop condition, in words. The plain summary of the acceptance criteria.]

## Blocked on

[Optional. Not the list – `blocked_by` holds that. Say why a dependency is hard: what this cannot
know until that one lands. Delete the heading if the list speaks for itself.]

## Context

[Pointers, with paths. Not paste.]

- **Constitution:** [path]
- **Specification, decisions, threat model:** [path and section]
- **Pattern to mimic:** [the one existing file whose shape to follow, or "none yet"]

## The contract to implement

[Only what another feature depends on: a name, a field, an event, an interface. Spell those out
exactly, because something else will match them literally. Leave everything that stays inside this
feature to the design column. Write "Nothing another feature depends on" if that is so.]

## Scope

**In scope**
- [the work, as a short list]

**Out of scope**
- [what a reasonable agent might pull in and must not – name it]

**Expected surface (not a limit)**
- [where this probably lands. A forecast. Reaching outside it needs no permission]

**Do not touch**
- [the fence. This half binds. A path that must not change goes here and nowhere else]

## Acceptance criteria

| # | Criterion | Test |
|---|---|---|
| 1 | WHEN [condition] THE [thing] SHALL [observable result] | [the test, or the person who judges it] |

## Edge cases to handle

- [case] → [expected behaviour]

## Verification

```bash
[the command that must pass]
```

[Anything a command cannot show: what is run against the local system or a real environment, and
what is read back.]

**Green means:** [what a pass has to include, so a partial run is not read as one]

## Boundaries

[Only what is specific to this feature. The levels above are assembled into the brief for you.]

- ⚠️ **Ask first:** [a decision this feature must hand back for]
- 🚫 **Never:** [the thing no trade-off justifies]

---

## Record

<!--
  Written after the work. Left empty on purpose: a heading with only a comment under it counts as
  nothing, and a done feature needs a filled-in Lesson plus Decisions taken or Carried forward.

  The headings are a closed set. Copy the spelling exactly – `Carried forward` is copied by that
  heading into the brief of every feature that depends on this one. Leave out a heading with nothing
  to say. Do not rename one.

  ### Decisions taken
  Choices the packet did not settle. What was chosen, over what, and what would make it wrong.

  ### Carried forward
  Gaps left on purpose, for whoever builds on this. A table reads well:
  | Gap | Consequence | When it closes |
  It reaches only features that depend on this one. Anything for anyone else names its destination
  in the entry: a feature, or `issue #N`.

  ### Verification actually run
  Where the packet's verification was not enough, and what was done instead. The difference only.

  ### Review
  What people said, as distinct from tests. Including what came back and changed nothing.

  ### Panel tally
  Pasted from the review panel's own output. Not counted by hand.

  ### Also fixed (not the feature)
  Repairs made along the way, so a later reader does not take them for part of the feature.

  ### Lesson
  The one thing that applies to work that is not this work. If it repeats an earlier feature's
  lesson, say which.
-->
