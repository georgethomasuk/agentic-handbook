**Status** draft · **Life** living · **Reader** you, about to set up how features move from claimed to closed

# How to manage delivery with workflows

This is a procedure. Follow it in order.

It produces three things: a set of workflows fitted to one engagement, a brief for each feature, and
a way of moving a session from one column to the next without it losing its place.

A **workflow** is the fixed sequence of columns one feature moves through, from claimed to closed. A
**column** is one stage of that sequence. It says what it needs on entry, what it leaves behind, and
what ends it.

**Planning is not here.** What to build, in what order, and the packet that briefs each feature are
[Part 5](../05-delivery-planning/README.md). **Supervising a session while it runs is not here
either.** The unattended stretch, workers, the review panel and what each column costs are
[Part 7](../07-supervision/README.md). This part is what sits between them: the workflow a feature is
bound to, the brief built for it, and the rules for moving through it.

The worked example throughout is [the example system](../../reference/example-system.md). The feature
is **a rate limit on the public check-in endpoint**, boundary B3.

## What is in this folder

| | |
|---|---|
| **This guide** | What the process is, why it is shaped this way, and what good output looks like. Written for you |
| [**`prompt.md`**](./prompt.md) | Three instruction sets to paste into agent sessions – filling the slots, resolving a workflow, assembling a brief. Written for the agent |
| [**`templates/`**](./templates/README.md) | The shared core, seven workflows, the slots file and the brief skeleton. Copy the directory |

**Read this once. Use the prompts every time.**

## The procedure on one screen

For when you come back to it.

| Step | Who | What |
|---|---|---|
| 1.1 | You | Copy the templates into the client repository |
| 1.2 | Agent drafts, you decide | Fill the `project.*` slots the first workflow uses |
| 1.3 | Participant answers, you decide | Agree the stop list and the decide-and-disclose list |
| 1.4 | You | Fill the `tooling.*` slots, by hand where you have no tooling |
| 1.5 | You | Make every command slot fail once, and read the exit status |
| 1.6 | Agent resolves, you check | Flatten the core, one workflow and the slots into one file |
| 2.1 | You | Bind a workflow to the feature, by what has to run to prove it |
| 2.2 | Agent assembles, you check | Build the brief – the ask first, the context after |
| 2.3 | You | Hand the brief to a fresh session |
| 3.1 | Agent | Enter each column by printing it, and work from what was printed |
| 3.2 | You | Know which exits are yours |
| 3.3 | Agent hands back, you answer | Numbered decisions, lettered options, one-line reply |
| 3.4 | Agent offers, you decide | Compact only at a marked boundary, after the journal is written |
| 3.5 | You merge, agent closes | Nothing merges the feature but you |
| 4.1 – 4.2 | You | Put a fix in the right layer, then resolve again |

---

# Context

## What you are producing

| | For | What it is |
|---|---|---|
| **The filled slots** | The client's reviewers, and you | Every engagement-specific fact the workflows need, in one file. The stack, the data rules, the two lists that say what an unattended run may decide |
| **A resolved workflow** | The agent | One flat file per workflow you use. The shared core, the workflow and the slots joined, with no placeholder left in it |
| **A brief** | The agent, once per feature | The task and the column to start at, then everything the plan knows that bears on it |

**The brief is the point of the plan.** A plan that only displays status is a tracker. One that can
assemble a session's context from where a feature sits is what stops a fresh session drifting off the
goal.

## What you need before you start

| | |
|---|---|
| **A plan with packets** | Features, each with a goal, acceptance criteria, verification commands and its dependencies named. Part 5 covers writing them and is not yet written |
| **A constitution** | The one document every session reads first. The slots point at it |
| **The trust boundaries** | From [Part 3](../03-threat-modelling/README.md). Two slots are filled from that table |
| **A code host with pull requests and CI** | Every workflow ends in a pull request a person merges |
| **Someone on the client side who will read two lists** | The stop list and the decide-and-disclose list are theirs to disagree with |

**A feature with no packet does not enter a workflow.** Its next stage is a packet. The first column
of every workflow verifies inputs, and none of them does design discovery.

## What it costs

**Setup time is not measured.** The templates were extracted from one engagement and have not yet
been set up on a second.

**Counted from the templates on 2 October 2026:**

| | |
|---|---|
| Slots in all | 77 – 53 `project.*`, 24 `tooling.*` |
| Slots `build-in-repository` uses | 39 – 17 `project.*`, 22 `tooling.*` |
| Columns in `build-in-repository` | 12 |
| Its exits, by kind | 9 commands · 18 attests · 7 human gates, 4 of them blocking |
| Where you are stopped | `frame`, `build-plan` and `merge` |

**One figure from the engagement these were extracted from**, read from its design record on 2
October 2026. The first real brief assembled by walking the plan from the top was 5,501 words, and
5,064 of them came before the sentence naming the column. Step 2.2 exists because of that brief.

**What a column costs to run is Part 7's subject**, not this one's.

## Who does what

| | | |
|---|---|---|
| **You** | the operator | Fill the slots. Bind a workflow to each feature. Answer the human gates. Merge |
| **The agent** | | Draft the slot fillings from the repository. Resolve the workflow. Assemble the brief. Work the columns, one at a time |
| **The participant** | | Hold what the repository cannot say – what the client will not have decided for them. During setup this is the client's lead. During a feature it is whoever answers the design gate |

**You and the participant are often the same person during a feature.** They should not be during
step 1.3. The two lists decide what an agent may do to the client's system without asking, and a
supplier who writes both lists alone has agreed them with nobody.

## The shape of the work

| Section | How often | What happens |
|---|---|---|
| **1 · Set up** | Once per engagement | Fill the slots, prove the checks, resolve a workflow |
| **2 · Start a feature** | Once per feature | Bind a workflow, assemble the brief, hand it over |
| **3 · Move through the columns** | Every column | Enter, exit, hand back, compact, merge |
| **4 · Change a workflow** | When a run shows the method is wrong | Put the fix in the right layer |

**Every step works with no tooling.** Each slot has a by-hand filling, and each of the three agent
prompts stands in for a script that is not published. *What's not solved yet* says what that costs.

---

# 1 · Set up

Once per engagement, before the first feature is claimed.

## 1.1 · Copy the templates

> **You** copy the folder.

Copy [`templates/workflows/`](./templates/workflows/README.md) and
[`templates/brief.md`](./templates/brief.md) into the client repository, beside the plan.

**Do not edit `core.yaml` or the workflow files during setup.** Everything that differs between
engagements has already been taken out and left as a named hole – a **slot**. A workflow edited to
fit one client is a workflow that has to be read line by line before it can be used for the next.
That reading is what these templates were extracted to save.

**Worked example.**

```
plan/
  workflows/
    core.yaml
    build-in-repository.yaml
    …six more
    slots.yaml
    resolved/            written in step 1.6
  brief.md
```

---

## 1.2 · Fill the project slots

> **Agent** drafts from the repository · **You** decide every value.

A `{{project.*}}` slot is a fact about this engagement – the full check command, the lockfile, the
boundaries. Each slot in `slots.yaml` says what it needs, how to meet it by hand, and gives an
example. You add a `value:` line.

**Fill what the first workflow uses, not all 77.** `build-in-repository` uses 39. The slots for
browser work, contract changes and real environments can wait until a feature needs them.

The agent reads the repository and proposes a value for each slot, quoting the file it took it from.
Use [prompt A](./prompt.md#a-fill-the-slots). **It leaves three slots for step 1.3** –
`stop_list`, `decide_and_disclose_list` and `real_data_policy`. Those are decisions, not facts, and
the repository does not hold them.

**Worked example.** Four of the seventeen, filled.

```yaml
project:
  constitution:
    value: "AGENTS.md"
  boundaries:
    value: "the seven trust boundaries in threat_model/workbook.md §2.6, B1 to B7"
  sensitive_boundaries:
    value: "authentication, checkin/ (B3), anything writing to the aggregate store (H2)"
  full_gate:
    value: "make check"
```

The agent proposed `make test` for `full_gate`, quoting the README. You corrected it. The slot asks
for everything CI runs, CI also runs the linter and the type check, and `make check` is the command
that runs all three.

---

## 1.3 · Agree the two lists

> **You** draft · **The participant** – the client's lead – answers · **You** write the result down.

Two slots decide what a session may do without asking, once the design is agreed.

| Slot | Means |
|---|---|
| `project.stop_list` | Decisions an unattended run **hands back** for |
| `project.decide_and_disclose_list` | Decisions it **takes**, and names in the pull request under *Decided without asking* |

**Anything on neither list is a stop.**

**Keep both lists in the constitution, once.** The slots point at them. In the engagement these were
extracted from, the stop list lived in one document and was deliberately not copied into the
workflows, because a list copied into every workflow is that many lists to keep in step.

**Read both aloud to the participant, item by item.** Put each item as a question: *may a session do
this without asking you?*

**Worked example.** Your draft put copy wording on the decide-and-disclose list. You put it to the
safety team's lead.

> *Where the design is silent, may a session choose the wording on a check-in screen and tell you
> afterwards?*
>
> *Not on the check-in. The question set was agreed outside the build and I would have to take a
> change back to the people who agreed it. Anywhere else, yes.*

The lists as agreed:

```yaml
project:
  stop_list:
    value: >
      AGENTS.md §6 – anything that changes what crosses a trust boundary · a new holding of
      personal data · a change to what the insurer can see · any wording on a check-in screen ·
      a migration that cannot be reversed · a new dependency
  decide_and_disclose_list:
    value: >
      AGENTS.md §6 – naming, file placement, test structure · a refactor inside the files the
      feature already touches · copy wording outside the check-in, where the design is silent
  real_data_policy:
    value: "Never. The supplier's machines are holding H4."
```

**The lists exist because of what the gates had become.** In the source engagement, most of the
human gates after the build was agreed were checks the agent had already done, which a person was
then asked to confirm and confirmed without reading. Those became attests. What was left for a
person is these two lists and a handful of blocking gates.

---

## 1.4 · Fill the tooling slots

> **You** fill them. They are yours, not the engagement's.

A `{{tooling.*}}` slot is how *you* work – how you claim a feature, where the journal goes, how you
run a review panel. The same answers travel with you to the next engagement.

**Use the `by_hand` line wherever you have no tooling.** Every slot has one. Tooling makes a column
cheaper. It never makes a column possible.

**Worked example.** Four of the twenty-two, filled by hand.

```yaml
tooling:
  journal_file:
    value: ".work/<feature>/journal.md"
  enter_column:
    value: >
      append the column name and the time to the journal, then print that column from
      plan/workflows/resolved/<workflow>.yaml and work from what was printed
  panel_runner:
    value: >
      one fresh session per seat, each given its profile and the diff, read-only. The operator
      opens them and pastes the findings back
  archive_journal:
    value: "cp .work/<feature>/journal.md \"${JOURNAL_ARCHIVE:?unset}/<feature>.md\""
```

**A value that names you goes in the environment, not in the file.** The archive destination is your
own records, outside the client repository. Written into `slots.yaml` it would put the supplier's
name in a tree the client is handed. So the slot holds a variable, and the variable is set on your
machine.

**That by-hand panel runner needs you present.** The session cannot open fresh sessions for itself,
so `panel` stops being unattended. That is the cost of having no runner, and it is the right cost –
a panel that cannot run apart from the working session falls back to that session reviewing its own
work.

---

## 1.5 · Make every command slot fail

> **You** run each one against a missing input and read the exit status.

A slot whose value is a command is a check. **A check that skips when its input is missing reads as
a pass.** So before any workflow relies on one, see it fail.

Point each command at something that is not there – an unset variable, a missing file, a branch that
does not contain the main branch – and read the exit status. Zero is a defect in the slot.

**Worked example.** `archive_journal`, with the destination unset.

```
$ unset JOURNAL_ARCHIVE
$ cp .work/rate-limit/journal.md "${JOURNAL_ARCHIVE:?unset}/rate-limit.md"
bash: JOURNAL_ARCHIVE: unset
$ echo $?
1
```

That is the slot working. The filling you did not use:

```
$ cp .work/rate-limit/journal.md "$JOURNAL_ARCHIVE/rate-limit.md"
```

With the variable unset this one tries to write to the root of the disk. On the machine this was run
on, that failed because the root is read-only. On a machine where it is not, the command reports
success and there is no archive.

**Nothing downstream catches this one.** `close` archives the journal and then releases the working
copy the journal lives in. An archive that quietly copied nothing is found out when somebody wants
the evidence behind a record, which is after the only copy is gone.

---

## 1.6 · Resolve the workflow into one file

> **Agent** resolves · **You** run two checks on the result.

A workflow file is not runnable as written. It pulls columns from the core with `use:`, adds to them
with `also:`, and is full of slots. **Resolving** joins the core, one workflow and the filled slots
into one flat file with nothing left to look up.

**The agent works from the resolved file and never from the three sources.** The layers exist so
that you make each fix in one place. The agent needs each column whole, in one place, at the moment
it enters it.

Use [prompt B](./prompt.md#b-resolve-a-workflow). The rules it follows:

| In the workflow file | In the resolved file |
|---|---|
| `use: core.<name>` | The whole column, copied from `core.yaml` |
| `also:` | Each field appended to the same field of the copied column. Text becomes further paragraphs. A list gains items at the end. A nested block is appended field by field |
| `as: <name>` | The copied column's `name`, replaced |
| `seeds:` | Kept on the copied `panel` column, as its `seeds` list |
| `standing_constraints:` | The core's list first, then the workflow's |
| *nothing – these are in the core only* | `stage_protocol`, `exit_kinds`, `report_back`, `compaction` and `delegation`, copied to the top |
| `{{project.x}}` · `{{tooling.x}}` | The slot's `value` |
| `modes:` | Left out. A mode is resolved into a file of its own, `<workflow>.<mode>.yaml`, with its changes applied column by column |

**Then run two checks.** Both must print `0`.

```
$ grep -c '{{' plan/workflows/resolved/build-in-repository.yaml
0
$ grep -c 'use: core' plan/workflows/resolved/build-in-repository.yaml
0
```

A placeholder left in a resolved file is an instruction with a hole in it.

**Worked example.** The `panel` column in `build-in-repository.yaml` is short:

```yaml
  - use: core.panel
    seeds:
      - "Where the change moves data: … what leaves {{project.boundaries}} in a response, a log line or an error."
      - "Where it owns state: the ownership agreed at `frame`, and whether the code honours it."
      - …
```

Resolved, it is the whole of the core's `panel` column – its precondition, entry, five exits and
compaction block – with those seeds attached and every slot filled:

```yaml
  - name: panel
    precondition:
      - command: git fetch -q origin main && git merge-base --is-ancestor origin/main HEAD
        why: the panel reviews the diff it is handed. …
    entry: >
      Choose the reviewers from what this change can get wrong. …
      Fill each seat from .review/profiles/ by reuse first, …
    seeds:
      - "Where the change moves data: … what leaves the seven trust boundaries in
        threat_model/workbook.md §2.6, B1 to B7 in a response, a log line or an error."
```

**Checked on 2 October 2026:** all seven workflows resolve by these rules against the core, and each
leaves no placeholder when every slot it uses has a value. That was a trial resolution by script, on
the example fillings. It shows the files join. It does not show a resolved workflow has been run –
see *What's not solved yet*.

**Resolve again whenever a source changes**, and never edit a resolved file. An edit made there is
lost at the next resolve.

---

# 2 · Start a feature

Once per feature, when its packet is written and its dependencies have merged.

## 2.1 · Bind a workflow

> **You** choose. The choice is written on the feature.

Choose by **where the truth of the work lives** – what has to run for the change to be proved. The
[choosing table](./templates/workflows/README.md#choosing-a-workflow) lists the seven.

**Never choose by what the work is about.** A set of workflows named by subject produces the question
*"is a command-line task front end or infrastructure?"*, which has no answer. *"What would have to
run to prove this?"* always has one.

Write the workflow's name in the feature's own file, in the field Part 5 gives it. No other plan
level binds a workflow, because no other level is executed.

**Worked example.** The rate limit on the check-in endpoint.

| Ask | Answer |
|---|---|
| What has to run to prove it? | Tests, and requests fired at a local system |
| Does it need a deployed environment? | No |
| Does a person have to look at a built surface? | No. The refusal message is one line of existing copy |

So: `build-in-repository`.

**The same limit, enforced at the network edge instead, is a different workflow.** A rule in the
firewall in front of B3 cannot be proved by any test in the repository. Only the real environment
refuses a real request. That feature binds `real-environment-change`, and the subject – rate limiting
– has not changed at all.

---

## 2.2 · Assemble the brief

> **Agent** assembles, in a session of its own · **You** check it.

The **brief** is the single document a fresh session is handed for a feature. It is built from the
plan and the resolved workflow in a fixed order. Nothing in it is written from memory.

Use [prompt C](./prompt.md#c-assemble-a-brief) and the [brief skeleton](./templates/brief.md).

**The ask comes first. The context comes after.**

| | Section | Taken from |
|---|---|---|
| **The ask** | Where the feature sits, its status, the date its packet was written | The plan |
| | The outward identifiers it declares | The feature |
| | The column to start at, its position, the whole chain of columns, and the stage protocol | The resolved workflow |
| | The feature's goal | The feature |
| | Where the contract is | The feature's path |
| | The current column in full, and the standing constraints | The resolved workflow |
| | How to report back | The resolved workflow |
| | The journal and compaction protocol, the worker protocol | The resolved workflow – **only if a column in this brief uses them** |
| **The context** | The goal chain, from the top of the plan down | Every level above the feature |
| | Boundaries, accumulated down that chain | Every level above the feature |
| | The feature in full – the packet | The feature |
| | What the levels above have settled | Every level above the feature |
| | What it depends on, and whether each has landed | The dependency list |
| | *Carried forward* from every feature it depends on | Their records |
| | The rest of the workflow – every later column, in full | The resolved workflow |

Two rules in that order have a recorded failure behind them.

**The task goes above everything the session needs to know.** A brief built by walking the plan from
the top opens at the widest goal and reaches the instruction last. The first real one did exactly
that – 5,064 of its 5,501 words came before the sentence naming the column. The packet in between
reads as an instruction to build. So a session briefed for a planning column had every reason to
start writing configuration.

**Lift *Carried forward* along the dependency graph, by its exact heading.** Everything else a
feature inherits comes from the levels above it. This one comes from whatever it was built on, which
is usually somewhere else in the plan entirely. In the source engagement two features hit the same
failure a day apart, and the second recorded it as the first one's lesson repeating exactly. The
first had written it down. Nothing carried it.

**That lift reaches a feature only through its declared dependencies.** A note addressed to work that
depends on nothing is read by nobody, and the file looks written, filed and delivered. Three features
in the source engagement were each told to record a gap for a later piece of work that no feature
declared a dependency on. The notes were right. They had no route.

**Three more things about the order are how the source builds its briefs.** No failure was recorded
for them, so they are described here and not ruled.

| | The source's reasoning |
|---|---|
| Each thing is stated once | The ask does not restate the column, and the context does not restate the ask. The one deliberate repeat is the feature's goal, which is both the task and part of the packet |
| The whole workflow is carried, later columns last and copied whole | A session normally walks several columns, and by `prove` the instructions for `prove` are in the brief or nowhere. They go last because a column three stages away is neither what to do now nor what to know now |
| A protocol no column in the brief uses is left out | A page about compaction in a brief with no marked boundary is standing text for a rule that never fires |

**Worked example.** The brief for the rate limit, in outline. Every line below the headings is the
real text of that section, shortened.

```markdown
# Rate limit on the public check-in endpoint

Platform build › The check-in window can open › Staff complete a check-in on their own
phone › this feature · status ready · packet written 28 September

Traces: finding F-51 · boundary B3

## Your task

**Start at column `check` – 1 of 12 in `build-in-repository`.** **`check`** → `open` →
`frame` → `build-plan` → `build-execute` → `prove` → `panel` → `prepare-pr` → `submit` →
`record` → `merge` → `close`

Enter every column with: append the column name and the time to the journal, then print
that column from plan/workflows/resolved/build-in-repository.yaml …

**From `build-execute` on, this workflow runs unattended.** … the stop list in AGENTS.md §6.

**The goal**
The check-in window lasts two weeks and cannot be repeated. A flood of requests in that
window must cost the sender, not the staff trying to check in.

**The contract** is the packet under `## This feature` below. Its file is
`plan/…/feature_checkin_rate_limit.md`.

## Column · `check`
…the delegate block, the entry, what it produces, its one human gate…

### Standing constraints – every column, every time
…

## How to report back
…

## The journal, and when to compact
…

## Columns that send work to a worker
…

---

## Standing context

## Why this exists – the goal chain
### Mission · Platform build
### Milestone · The check-in window can open
### Slice · Staff complete a check-in on their own phone

## Boundaries inherited from above
### From the slice · Staff complete a check-in on their own phone
Nothing built for the check-in may make a check-in attributable to a person or a device.

## This feature
…the packet, whole…

## Depends on
- `feature_anonymous_checkin_token` – Anonymous check-in token · done

## Carried forward from upstream work
### From `feature_anonymous_checkin_token` · Anonymous check-in token
The token identifies an invitation, not a person, and is not rotated inside the window.
A leaked link stays usable until the window closes. Closes when something bounds what one
token can do.

## The rest of the workflow
### `open` – 2 of 12
…eleven columns, each whole…
```

Two things in that brief did not come from the packet. The slice's boundary rules out the obvious
design – remembering the device – before the session proposes it. And the upstream note is why the
agreed design in `frame` keys the limit on the token. Neither was remembered by anybody. Both were
lifted.

**Your check on a brief is one count.** How many words come before the sentence that names the
column? If the answer is more than a screen, the order is wrong.

---

## 2.3 · Hand the brief to a fresh session

> **You** paste it. **The agent** starts at the column the brief names.

Start a new session for every feature and paste the brief as its first message.

**The brief is a kickoff, not a resume.** It names one column to start at. To pick a feature up
partway through, assemble a new brief that starts at the column the work has reached.

**Take that column from the journal, not from the plan.** The plan records which column a feature is
in only twice – when the feature is claimed and when it is closed. That is deliberate. The plan lives
in the repository, so its state reaches the main branch only when a change does, and tracking every
move would cost a plan-only pull request per column. So read the plan's column as *which loop this
feature is in*, never as where it has got to.

**If the brief does not say which column, it must say that it is guessing.** A brief that silently
defaults to the first column tells the reader the work has not started, about a feature that may be
five columns in.

**Worked example.** The rate limit was handed back at `build-plan` on Thursday and you return to it
on Monday. The plan says `open` – the column written when it was claimed. The journal's last entry
says `build-plan`, with the cut agreed. The new brief starts at `build-execute`, 5 of 12.

---

# 3 · Move through the columns

Every column, every feature. This section is what you watch for. The instructions the agent follows
are in the resolved workflow.

## 3.1 · Entering a column

> **The agent** enters each column by printing it.

The agent runs `tooling.enter_column`. That records the column in the journal and prints the
column's instructions. Then, before doing anything:

1. It says which column it is entering and its position.
2. It restates what the column asks and what ends it, **from what was just printed** – not from the
   brief.
3. It works to the exit conditions and stops there.

**Entering a column has to be how the column's text is obtained.** That sentence took four attempts
in the source engagement, and the first three were instructions.

| Attempt | What it was | What happened |
|---|---|---|
| 1 | Stated once, at the top of the brief | Invisible by the fifth column. Three features missed exactly one column each – never the one anybody dreaded, always the one entered in the same breath as finishing the last |
| 2 | Written into every column | Still missed |
| 3 | Made an exit condition on every column | Honest, one column too late. It turned a silent miss into a flagged one and recovered nothing |
| 4 | Made the command that **prints** the column | Skipping it now means not having the instructions |

*Read from the source's design record on 2 October 2026:* thirteen recorded entries note a late or
missing entry marker across those attempts, three of them after attempt 2. The last two features
before attempt 4 each attributed about 84% of their cost to one build column, because every later
column had been entered without a marker.

**What that evidence shows, and what it does not.** The recorded failure is the marker – the record
of which column the work was in. That a column worked from memory also skips its exit conditions is
the source's stated reason for re-reading, and no count of it was kept.

**Worked example.** The session finishes `open` and enters `frame`.

> *Entering `frame` – 3 of 12 in `build-in-repository`.*
>
> *It asks me to state the observable behaviour of the limit, what owns its state and for how long,
> and to resolve every choice the packet leaves open. I am to search for how the approach fails
> before agreeing it. No code is edited in this column.*
>
> *It ends on one blocking human gate: design and ownership agreed. I will hand back there.*

If that restatement is missing, or reads like the brief rather than the column, the session is
working from memory. Ask it to enter the column again.

---

## 3.2 · Which exits are yours

> **You** answer human gates. **The agent** answers everything else.

Every exit is one of three kinds.

| Kind | Who answers | What the session does |
|---|---|---|
| `command` | The shell | Runs it. Exit status 0 passes |
| `attest` | The agent | Checks the property, writes the evidence in the journal, continues |
| `human_gate` | A named person | Asks. If the gate is `blocking: true`, stops and hands back |

**An exit that cannot be a command must be written as a human gate.** That is what keeps the queue
of work waiting on a person visible rather than implied.

**An attest is not a weaker gate.** It names where the answer comes from. The evidence still has to
exist, in the journal, where you can read it.

**From the workflow's `unattended_from` column onward, the session stops for two things only** – a
blocking human gate, and an item on the stop list. Inside that stretch every human gate is blocking.
A gate that neither stops the run nor is an attest is the ambiguous middle, and a session told to
*stop at its exit conditions* reads the ambiguous middle as a stop.

**Worked example.** Where the rate limit needs you.

| Column | Your exits |
|---|---|
| `check` | One gate, not blocking – blockers verified. Answered at the next hand-back |
| `frame` | **Blocking** – design and ownership agreed |
| `build-plan` | **Blocking** – the cut agreed. **Blocking** – the panel run authorised. Two more, not blocking, answered in the same reply |
| `build-execute` to `record` | None. Twenty-two exits, all commands and attests |
| `merge` | **Blocking** – you merge |
| `close` | None |

You are stopped three times. Between `build-plan` and `merge` the session runs alone, and how you
supervise that is [Part 7](../07-supervision/README.md).

**With the by-hand panel runner from step 1.4, `panel` needs you as well** – to open the fresh
sessions and paste the findings back.

---

## 3.3 · Answering a hand-back

> **The agent** hands back in a fixed shape · **You** reply in one line.

Whoever reads a hand-back has not read the brief and last looked at the feature days ago. That
reader is you.

**A hand-back that needs decisions is a numbered list, one decision per block.** Each block carries
the fact that makes it a choice, lettered options, and a recommendation that says what would make it
wrong.

**The test is your reply.** If `1B, 2A, 3 – your call` would not be a complete answer, the block is
not a decision yet. Send it back.

In the source engagement the shape had to be asked for repeatedly before it was written into every
brief. Left unsaid, a hand-back opens on the first item of the column's checklist, and a set of four
open calls arrives as a paragraph that has to be turned back into questions before it can be
answered.

Three things make a set unanswerable, and each feels like diligence to the session writing it: one
decision cross-referencing another, a caveat folded into a recommendation, and a loose question on
the end.

**Worked example.** The hand-back at `frame`.

> *This is the rate limit on the public check-in endpoint. I have finished designing it and edited
> no code. Two calls are open.*
>
> **1 · What the limit counts against**
>
> *Staff at one site share one outbound address on the site's wifi. The library's default counts
> per address.*
>
> *A – per address. One line of configuration. One busy site throttles everyone on it.*
> *B – per check-in token. A small custom key. A leaked link is bounded; a site is not.*
>
> *I recommend B. It is wrong if tokens turn out to be shared between people, which the upstream
> feature's record says they are not.*
>
> **2 · What a refused request is told**
>
> *The check-in screen can show one line of existing copy, or the refusal can be silent.*
>
> *A – show "Please try again in a minute". Uses copy already on the screen for a network error.*
> *B – a new message naming the limit. New wording on a check-in screen is on the stop list.*
>
> *I recommend A. It is wrong if the existing line was agreed only for network errors.*

Your reply: `1B, 2A`.

---

## 3.4 · Compaction offers

> **The agent** offers · **You** decide.

A session that walks a whole workflow accumulates context it stops needing – a read sweep whose
conclusions are three sentences, a build whose value is the diff. A column may mark the boundary at
its exit as safe to **compact**: to have the session's context summarised and the detail dropped.

A boundary is safe on one condition: **what the next column needs is in files, not in the
conversation.**

| The column carries | Means |
|---|---|
| `compact:` with `offer` and `carry` | Safe. The agent writes every `carry` item to the journal, then offers, then waits |
| `compact:` with `never` | Something load-bearing exists only in this conversation. No offer |
| Nothing | No offer. Silence is not permission |

**Offering is the agent's job. Compacting is yours.** Never mid-column, and never on the agent's own
initiative.

**Read the journal before you accept.** Open it and find each `carry` item. In the source engagement
one boundary was being compacted before it was marked. The drop was taken on judgement, and what
survived was whatever the session happened to remember.

**Worked example.** The offer at the end of `frame`, after your `1B, 2A`.

> *`frame` is agreed. Everything up to here was reading – the constitution, the token feature's
> record, the library's documentation. `build-plan` needs the agreement, not the sources.*
>
> *The journal at `.work/rate-limit/journal.md` now holds: the agreed design with its state table,
> what owns the counter and for how long, the two decisions and why, the packet drift from `check`,
> and what the research found against the per-address default.*
>
> *Compacting now drops the sources. Your call.*

You open the journal, find the six items the `frame` column lists under `carry`, and compact.

---

## 3.5 · Merge and close

> **You** merge the feature · **The agent** closes it.

**Nothing merges the feature but you.** The session hands back once with the pull request, its CI
result, what it decided without asking, and what was not proved. Then it waits on the pull request's
state – not on a reply.

**`close` runs the moment the pull request reads merged.** It marks the feature done, archives the
journal, and releases the working copy, in that order.

**Closing is a column because nothing moves a feature's status when it merges.** In the source
engagement the plan reported two features in flight that had both already merged, one of them nine
days earlier. Every queue and dependency check downstream was reading a stale line.

**Worked example.** You merge the rate limit's pull request and say nothing. The session reads the
state, enters `close`, and reports:

> *Closed. Status done, merge date read from the pull request. Journal archived – the copy at the
> archive is 214 lines, the same as the working copy. Working copy released.*

---

# 4 · Change a workflow

When a run shows the method is wrong, not before.

## 4.1 · Where a fix goes

> **You** decide the layer. Then resolve again, step 1.6.

The input is the **retro** – the five-line note on what the workflow itself cost, written at
`record`. Its last line, *Fix*, names where a fix belongs or says `none: one-off`.

| The fix | Goes in |
|---|---|
| Differs from one engagement to the next | A slot. Change its `value` |
| Is true of every workflow | `core.yaml` |
| Is true of one kind of work | That workflow – its own column, or an `also:` on a shared one |
| Is a lighter path for a narrow case | A `modes:` entry on the workflow |
| Is a kind of work whose proof lives somewhere no workflow reaches | A new workflow file |

**Never restate a shared column to change it.** In the workflows these were extracted from, the
shared columns were repeated in every file. Each repetition was one more place a fix had to be made.

**Worked example.** Three features in a row had CI fail on generated types that nobody regenerated.
Each retro's *Fix* line named the build column.

The fix is true of this engagement's build and of one workflow. It goes on `build-in-repository`, as
an addition to the shared column, using a slot that already exists:

```yaml
  - use: core.build-execute
    also:
      exit:
        - command: "{{project.regenerate}}"
          why: >
            generated types left stale pass the local gate and fail CI, which is found out two
            columns later at `submit`.
```

Then resolve again. The resolved `build-execute` gains a sixth exit.

---

## 4.2 · Writing a column

> **You** write it. These are the four things a column must have.

**An `entry` that says what to do.** Where the column only plans, it says so – no edits.

**A `produces` list of things that exist.** Three to six bullets, each a file, a decision, a
measurement or a merged change – never an activity. `produces` and `exit` are different lists. An
exit says when a column is finished. A gate can pass on a column that left nothing durable: *review
passed* is true of a review whose findings live only in a conversation.

It is a list on purpose. In the source engagement, where an obligation was a list item, sessions
reproduced the items as their own headings, in order, without being asked. Where the same obligation
was a sentence in the entry, they did not.

**An `exit` list where every item is one of the three kinds, each with a `why:`.** The `why:` names
the failure the exit prevents. An exit nobody can name a failure for is tidiness, and every future
run pays for it.

**A name for how the work is proved.** The same rule as a workflow's own name, and as a reviewer's
seat.

**Worked example.** A column that would fail review, and the same column repaired.

```yaml
  - name: security-review            # named for a subject
    entry: Review the change for security problems.
    produces:
      - security reviewed            # an activity
    exit:
      - human_gate: looks fine       # no why, and no failure it prevents
```

```yaml
  - name: read-back
    entry: >
      Fire one refused request and read H1 and the log. Do not rely on the response code.
    produces:
      - the rows written to H1 by the refused request – expected none
      - every log line the refused request produced, quoted
    exit:
      - attest: a refused request wrote nothing to H1 and no check-in content to the log
        why: >
          a refusal that returns the right status and still writes the body to the log has
          moved check-in content into H6, which is kept on a different retention rule.
```

---

# Evaluating the quality

**These are yours to run, on files.** Do not ask the agent whether its own setup was good.

**Every command slot has been seen to fail.** Step 1.5, written down per slot. A slot with no
recorded failure is a slot nobody tested.

**No resolved file contains a placeholder.** The two `grep` checks in step 1.6, run on every file in
`resolved/`.

**A brief names its column within the first screen.** Count the words before that sentence.

**The journal has an entry line for every column the session has passed.** Compare it against the
chain in the brief. A missing line means a column was worked from the brief's tail rather than
entered.

**Every hand-back with decisions could be answered in one line.** If you had to ask what a block
meant, the shape failed, and that is worth a retro line.

**You read what you were asked to confirm.** If you answered a human gate without reading the
evidence, the gate is in the wrong kind. Make it an attest, or make it a command.

**Every *Carried forward* entry has a reader.** For each finished feature, either another feature
depends on it, or the entry names its destination – an issue by number, a named feature.

## Four failure modes to watch for

| | |
|---|---|
| **The edited template** | A workflow file changed to fit this client. The next engagement inherits the client |
| **The gate confirmed unread** | A human gate you answer without looking. It is costing a round trip and proving nothing |
| **The column entered from memory** | No restatement, or one that paraphrases the brief. Its exits are being skipped |
| **The note with no route** | A *Carried forward* entry addressed to "whoever comes next" |

---

# What's not solved yet

**There is no published tool.** Resolving a workflow, assembling a brief and entering a column are
done here by an agent following a prompt, or by hand. All three are mechanical, and mechanical work
wants a script. The engagement this was extracted from has one. It is not yet separable from that
engagement.

**By hand, nothing forces column entry.** The source's fix was to make entry the command that prints
the column. The by-hand filling of `tooling.enter_column` is an instruction again – the kind that
failed three times before the fix.

**The layered templates have not been run.** The workflows these were extracted from are whole
files. Splitting them into a core, a workflow and slots – `use:`, `also:`, `as:` – was done during
extraction. The trial resolution in step 1.6 shows the layers join. No feature has yet been run from
a file resolved this way.

**The templates have been set up on one engagement.** The 77 slots are the holes that engagement
left. A second one will find holes that are missing and slots that are really one slot.

**A resolved file can drift from its sources.** It is a generated copy kept in the repository because
by-hand column entry reads it there. Nothing checks it against the three files it was built from.

**`draft-contract` has not been run**, and `single-part` may yet fold into `component-library`. Both
are marked in their files.

**Setup cost is not measured.** Neither the hours to fill the slots nor the size of a resolved brief
on a second engagement.

**Part 5 is not written.** This guide assumes a packet with a goal, acceptance criteria, verification
commands and named dependencies, and a plan with levels above the feature. The handbook does not yet
say how to write either.

---

<!-- DRAFTING ONLY -->

## Source material

- `platform/plan/model.md` – §9 (workflow templates, the column field, the bracket, the unattended
  stretch), §10 (prompt assembly, the ask before the context, one session many columns, reporting
  back, the journal), §11c (the record and Carried forward). Re-read 2026-10-02.
- `platform/plan/tools/plan.py` – `build_prompt`, `ask_block`, `column_body`, `enter_column`,
  `stage_protocol`, and the protocol text blocks. Re-read 2026-10-02.
- `platform/plan/workflows/*.yaml` – the nine source workflows.
- `notes/workflow-generalisation-analysis.md` – the layer analysis the templates were cut from.
- `notes/handover-2026-10-02.md` – state before this guide was drafted.

## Figures and where each was read

- 5,064 of 5,501 words – `model.md` §10a.
- Thirteen recorded late or missing markers; three after the per-column rendering; about 84% billed
  to the build column on the last two features – `model.md` §9c and the 2026-08-13 decisions row.
- Two features in flight that had merged, one nine days earlier – `model.md` §9b.
- Two features, same failure a day apart; three notes with no route – `model.md` §11c.
- Slot, column and exit counts – counted by script from this repository's templates, 2026-10-02.

## Open

- Whether `single-part` stays a workflow of its own (see PLAN §11, 2026-10-02).
- The by-hand `enter_column` filling has not been run. Neither has prompt B or prompt C.
- The worked example's plan levels and field names must be reconciled with Part 5 when it is written.

<!-- END DRAFTING ONLY -->
