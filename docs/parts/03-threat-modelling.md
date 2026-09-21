**Status** draft – figures verified 16 September 2026, re-verify before publishing · **Life** living · **Reader** anyone who wants an adversarial pass that agents can actually run

# 3 · Attacking it before building it

> **Quick reference, stated not explained.**
>
> **Shostack's four questions** – what are we working on · what can go wrong · what are we going to do about it · did we do a good job. ([Threat Modeling: Designing for Security](https://shostack.org/books/threat-modeling-book))
>
> **STRIDE** – Spoofing · Tampering · Repudiation · Information disclosure · Denial of service · Elevation of privilege.
>
> **LINDDUN GO** – Linking · Identifying · Non-repudiation · Detecting · Data disclosure · Unawareness · Non-compliance. ([linddun.org](https://linddun.org/go/))
>
> The four questions are the container. The two taxonomies fill the second one, and nothing else.

The worked example throughout is [the example system](../reference/example-system.md) – an internal
safety and wellbeing platform, with seven trust boundaries and seven data holdings.

## The problem

**At the start of an engagement there is nothing for an agent to analyse.**

No codebase. No running system. There are specifications, and specifications describe the system as
it is meant to be, which is not the same as how it works.

What exists instead is business context sitting in people's heads. How collection actually happens.
Who is allowed to ask for an account. What the team does when a record will not process. None of it
is in a repository, so there is nothing to grep.

**So the agent's job is elicitation, not analysis.** That inverts which parts of the workflow matter.
An agent reading a codebase can work alone. An agent with nothing to read cannot, and every rule
below follows from that.

### The output is usually the wrong shape

Threat modelling conventionally produces a document written to **close** things. Coverage statements,
declared gaps, a sign-off table.

That is an end-of-engagement assurance artefact. At the start of a build you need the opposite: a
document written to **open** things. *Here is how we looked, here is what we found, tell us what we
got wrong.*

The difference is not tone. It decides the file layout, the granularity, and whether anyone outside
the team can contribute to it.

## The mechanism

Eight steps. Steps 1 and 2 are done once. Steps 3 to 6 repeat per category. Steps 7 and 8 are how it
scales.

---

### Step 1 · Describe the system twice

Two lists, on two different spines, because the two taxonomies need different units.

**Trust boundaries** – the places where data moves between parties who trust each other differently.
Security threats cluster here, because each side relies on assumptions the other has not promised to
keep. The example system has seven.

**Data holdings** – each place personal data sits, treated as one thing for analysis. Not a database
table and not a server. A body of records about people that can be reasoned about as a unit. The
example system has seven.

**Do not reconcile the two lists.** They answer different questions and forcing one spine onto both
loses cells. The reason is specific: a boundary walk never sits you in front of two holdings at once,
and that is exactly where the sharpest questions live. *Can an incident report be linked to a
wellbeing check-in* is only visible with both holdings side by side.

---

### Step 2 · Split the holdings, using the fork test

Splitting a holding decides how long the walk takes, so it needs a rule.

**Split only where walking a holding as one forces two different answers.** Not where the data merely
differs.

On the example system the two intakes fork hard:

| | Holding | Can the person deny having said it? |
|---|---|---|
| **H3a** | Incident report, managed device | Attribution is **the control**. Losing it defeats the purpose of filing a report |
| **H3b** | Wellbeing check-in, personal phone | Attribution is **the harm**. Someone who cannot deny having reported that they are struggling has lost the thing that made the check-in safe to complete |

Same mechanism, opposite valence. Walking them as one holding forces a single answer onto two
questions, and it will be wrong for both.

**Different content is the symptom. Diverging analysis is the justification.** Hold that line or the
spine splits forever.

**Holdings outside the platform get no row.** Paper notes in a filing cabinet are real and are not
analysable here. Note them in the cell that raised them and move on.

---

### Step 3 · Pick one category and prepare it

Work one category at a time, all the way across the row. Six security categories against seven
boundaries is forty-two cells; seven privacy suits against seven holdings is forty-nine.

**Asking the same question seven times in a row is what catches the category you would otherwise
skim.** That repetition is the entire reason the pass exists.

Three things before the first question:

**Research the category.** What it covers, where it borders the adjacent ones, and its specific
pitfalls. Do this first, not in parallel with opening the interview.

**Read the existing record, including the contracts.** Proposing something already decided makes the
walk look like it is talking over earlier work rather than building on it. Contracts are easy to skip
because they read as commercial material, and they are often where obligations are actually specified.

**Write the disambiguation rules down before using them.** State the test that separates this category
from its neighbours as something answerable: *if authentication were perfect and the finding survives,
it is elevation of privilege, not spoofing.*

---

### Step 4 · Work the row, one cell at a time, by interview

This is where the elicitation happens. Four rules, each a consequence of the agent knowing nothing.

| Rule | Why |
|---|---|
| **Ask what happens before asking what goes wrong** | There is no model of the system yet, so a hypothesis-first question spends the whole exchange being reversed |
| **Ask in the system's own terms, not the taxonomy's** | Not *"is there a spoofing risk at B2"* but *"someone from the insurer logs in – could that be someone else, and how would you know?"* A cell answered in taxonomy vocabulary has usually not been thought about |
| **Lead with the plain question. Hold the scaffolding** | The analysis can be deep. The sentence handed over must be plain. Give the reasoning only if asked |
| **State the candidate finding in one sentence, get a yes, then write it up** | A finding that cannot be said in one sentence is not understood yet |

**Every one of these protects the human's attention**, because the human is the only source of truth
in the room. That cost multiplies across parallel sessions.

Two things to separate while listening:

**What exists, versus what is intended.** *"There'd be some mechanism where the form gets taken down"*
is an intention, not a control, and it arrives in the same breath as things that are actually built.
The threat goes in the finding. The intention becomes a requirement. The finding says plainly that the
control is not built.

**The good property, before the gap.** Name what the design gets right, then what it does not reach. A
gap framed as an edge on a sound design invites contribution. A bare gap invites defensiveness.

---

### Step 5 · Mark every cell

Three states. There is no fourth, and an unmarked row means the walk is incomplete.

| Mark | When |
|---|---|
| **Finding** | The prompt produced something. Write the entry now, not later |
| **Closed** | Considered and dismissed. **The reason is the deliverable** – *"n/a"* is not a reason |
| **Open** | Cannot be closed by you. Name what it waits on and who owns it |

**A dismissal is a result.** A category considered and dismissed on stated grounds is a decision. A
category never considered is a gap. Distinguishing those two is the only thing the coverage record is
for.

**Withdraw rather than defend.** When an interview kills a finding you already drafted, record the
withdrawal in the cell rather than deleting it. A walk that never retracts is not being told anything.

**If a cell produces something that is not a threat, give it a different number.** Contract gaps,
stale documents, undecided scope – real, actionable, not threats. A reader is entitled to assume every
finding describes a way the system can harm someone or be harmed, and one paperwork entry corrupts
that guarantee for every other line.

---

### Step 6 · Write each finding as its own file

One file per finding, named so they sort. An index table alongside. A one-line register entry
elsewhere.

**Write it in plain language the first time.** Not a compressed note to be translated later. The
finding is the thing that goes in front of the client, and a statement that cannot survive plain
English is one that is not yet understood.

---

### Step 7 · Run categories in parallel

Two agents, two categories, one operator moving between them.

**Parallelism is a throughput change, not a depth change.** Each session runs the full interview
procedure. The moment it starts proposing marks to save time, the pass stops being worth running.

Four rules make concurrent sessions safe:

| Rule | Why |
|---|---|
| **Allocate finding IDs in blocks before work starts** | Two sessions both taking *the next free number* collide, and the collision surfaces at merge, after both entries are written. Gaps in the numbering cost nothing |
| **Each session owns its own category table and its own finding files exclusively** | Never edit another session's table, even to fix an obvious typo |
| **Shared files are append-only, and re-read immediately before editing** | Not once at session start. An edit built on a stale read silently reverts the other session |
| **Do not commit unless asked** | A commit sweeps up half-finished work from the other session |

---

### Step 8 · Synthesise across categories, in one place

Cross-category judgements cannot be written by a session that has seen one category. The coverage
summary, the distribution check, the cross-cutting observations – these compare categories against
each other.

A session finishing its category says what looked cross-cutting. It does not write that into the
shared sections itself.

**Derive every count by script, not by hand.** A hand-kept tally drifts, and it drifts silently.

## The rules that earned their place

Each of these exists because something went wrong without it.

**Lead with the plain question; hold the scaffolding.** An agent that hands over its framing, its
reasoning and its severity split wrapped around the question forces the participant to say *simplify
that* before the actual question is visible. That cost lands on the participant and multiplies across
parallel sessions.

**State the candidate in one sentence before writing it up.** A finding built, framed and paragraphed
before the premise is confirmed collapses the moment the participant describes what actually happens.
The cost lands on the person who has to read three paragraphs to find the one wrong assumption
underneath.

**Separate what exists from what is intended.** A finding whose treatment credits an unbuilt control
has quietly become an assurance claim, which is the one thing this work must never produce.

**Name the good property before the finding.** It also keeps the record honest in the other
direction, because a dismissal that names the property it relies on is auditable.

**Things that are real, actionable and not threats get a separate series.** Otherwise the register
stops meaning what its readers assume it means.

**Derive every count by script.** A hand-kept tally will disagree with the grid it describes, and
nothing will announce it.

**Never imply independent review where there is none.** The output supports one claim: recognised
practice was followed and what it found was recorded. Not *reviewed*. Not *secure*. A declared gap is
defensible; an implied assurance is not.

### Failure modes worth naming before starting

- **Admiration for the problem.** A finding with no treatment decision is half a finding.
- **The tidy grid.** No open cells means the walk stopped asking. An open cell is a healthy state.
- **Findings that are really requirements.** *"The system should log exports"* is a control. The
  threat is *"an export cannot be traced to a person."*
- **Over-weighting the dramatic.** Frequency and severity are separate axes.

## What it cost

**What one full pass takes, measured 16 September 2026. Re-verify before publishing.**

| | |
|---|---|
| Cells to work | **91** across thirteen tables – 42 security, 49 privacy |
| Findings produced | **43**, taking a register of 16 to 62 |
| Findings file before it was split | **2,201 lines**, then one file per finding |

**Budget roughly double what you expect for the reference annexes, and hold the line on the document
people actually read.** Two annexes came in at about twice their target. The client-facing document
was budgeted at around 120 lines and landed at 350, and it is the one with a real constraint, because
it is the only one anybody reads end to end.

**A pass this size is not cheap.** The smallest version below exists because of that.

### Two results worth knowing before you start

**A category can produce nothing, and that is a result.** One privacy category was flagged in advance
with a specific fear, walked across all seven holdings, and closed every cell. The reason was recorded
rather than assumed. A pass that only reports its successful hypotheses is not evidence of anything.

**Running one taxonomy can make the system worse.** Four times, a property the security pass recorded
as a weakness turned out to be the thing protecting the subject. Unreliable records protect
deniability. Absent read-logging protects the people being logged. Each is a live trade-off, and
fixing the security finding erodes the privacy property.

## The smallest version that works

One security pass over your trust boundaries. One table per category. One file per finding. A rule
that anything dismissed is written down with its reason, and that *"n/a"* is not a reason.

The privacy spine can come later. The parallel sessions can come much later.

## What's not solved yet

**The agent interviews the supplier, not the client.** Somebody has to represent the client's
knowledge, and that is a proxy with a ceiling – the pass is only as accurate as what the proxy has
absorbed. The artefact shape compensates rather than fixes: the whole output is built to be handed
over with *tell us what we got wrong*.

**Running this with the client in the room is not designed yet.** It is the obvious next version.
Parallel sessions get harder immediately, because the knowledge sits with someone whose time cannot
be booked twice.

**Length is a design constraint and this method does not yet meet it.** Recorded that way rather than
restated downwards.

**Pace is deliberately unsolved.** The obvious speed-up – propose marks for every boundary at once and
interview only the live ones – was declined, on the grounds that optimising against a sample of one is
optimising against noise. It has not been revisited.

---

<!-- DRAFTING ONLY -->

## Source material

- `redmoor_docs/governance/security/threat_model/README.md` – the approach, the artefact table, the overrun note.
- `.../walk_playbook.md` – the working procedure: two spines, the fork test, the interview rules, the parallel-session mechanics, failure modes.
- `.../workbook.md` – §4.3 the two spines, §5.1 coverage, §5.2 what the grids added, §7 limits.
- `.../annex_a_grids.md` – the thirteen tables, the ID reservation table.
- `.../annex_b_findings.md` + `annex_b/` – the index and one file per finding.
- `.../adjacent_findings.md` – the separate series.
- `.../findings_register.csv` – the register, 64 rows.
- `.../design_review/` – the two superseded predecessors.

## Verification state

Counts re-read from source 16 September 2026, against `findings_register.csv` and `annex_b/` rather
than against the README, which has drifted. **Re-verify before publishing.** The README's artefact
table is stale on three lines and must not be quoted.

## Open

- Whether the client-facing front-door document is worth showing as a shape.
- How much of the governance mapping belongs here versus one line.

<!-- END DRAFTING ONLY -->
