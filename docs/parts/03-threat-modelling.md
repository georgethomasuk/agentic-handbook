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
> The four questions are the container. The two taxonomies plug into the second one, and nothing else.

## The problem

**At the start of an engagement there is nothing for an agent to analyse.**

No codebase. No running system. There are specifications, and the specifications are wrong in places
nobody has noticed yet. Three cells in this walk corrected the specification itself, each found by
asking what actually happens rather than reading what was written.

What exists instead is business context sitting in people's heads. How collection actually happens.
Who is allowed to ask for an account. What the team does when a record will not process. None of it
is in a repository, so there is nothing to grep.

**So the agent's job is elicitation, not analysis.** That inverts which parts of the workflow matter.
Most writing about agents and security assumes the agent is reading something. Here it reads almost
nothing and interviews almost entirely.

### The second problem: the usual output is the wrong shape

Threat modelling conventionally produces a document written to **close** things. Coverage statements,
declared gaps, a sign-off table.

That is an end-of-engagement assurance artefact. At the start of a build it is the wrong shape.

This engagement had two of them already, from an earlier session – 462 lines of internal working
record with dated addenda, and 788 lines of closing report. Both were good work. Neither was readable
by the client, and neither was the thing needed, which is a document written to **open** things: here
is how we looked, here is what we found, tell us what we got wrong.

## The mechanism

Three things. Everything else is detail.

### The worked example

The system described below is a stand-in. It carries the structure of a real engagement and none of
its content, and it is used across Parts 2, 3 and 5 so you meet one example rather than three.

> **An internal safety and wellbeing platform for a multi-site employer.** Supervisors file incident
> reports from managed devices, sometimes in another language, so reports are machine-translated on
> the way in. Once a year, for a two-week window, all staff are invited to complete an anonymous
> wellbeing check-in on their own phones. The company's insurer reads a dashboard of aggregate
> trends by site.

Every count in *What it cost* is real and comes from the actual engagement. The stand-in illustrates
shape; it never carries a finding, a figure or a quote.

### M1 · Two taxonomies, two spines, deliberately not reconciled

**STRIDE walks the trust boundaries.** Security threats cluster where trust levels meet, so the
boundary is the right unit. Six categories against seven boundaries is forty-two cells.

**The privacy taxonomy walks the personal-data holdings.** A privacy harm attaches to a record about
a person, not to an architecture element. *Can this person be re-identified* is a question about
data, not about a line on a diagram. Seven suits against seven holdings is forty-nine cells.

The first attempt walked both against the boundaries. It did not survive contact with the work.

**The reason it does not work is specific.** A boundary walk never sits you in front of two holdings
at once, and that is exactly where the sharp cells live. Linking an incident report to a check-in is
only visible with both holdings side by side.

#### The fork test

Splitting a holding is the decision that decides how long the walk takes, so it needs a rule.

**Split only where walking a holding as one forces two different answers.** Not where the data merely
differs.

On the stand-in, the two intakes fork hard:

| | Holding | Non-repudiation |
|---|---|---|
| **H3a** | Incident report, managed device | Attribution is **the control**. Losing it defeats the purpose of the report |
| **H3b** | Wellbeing check-in, personal phone | Attribution is **the harm**. Someone who cannot deny having reported that they are struggling has lost the thing that made the check-in safe to complete |

Same mechanism, opposite valence. Walking them together forces one answer onto two questions.

**Different content is the symptom. Diverging analysis is the justification.** Hold that line or the
spine splits forever.

Holdings outside the platform get no row at all. Route them in the cell that raised them and move on.

### M2 · The interview rules

This is where the elicitation happens, and it is the mechanism the whole method rests on.

Four rules. Each is a consequence of the agent knowing nothing.

| Rule | Why, given the agent knows nothing |
|---|---|
| **Ask what happens before asking what goes wrong** | There is no model of the system yet, so a hypothesis-first question spends the whole exchange being reversed |
| **Ask in the system's own terms, not the taxonomy's** | Not *"is there a spoofing risk at B2"* but *"someone from the insurer logs in – could that be someone else, and how would you know?"* A cell answered in taxonomy vocabulary has usually not been thought about |
| **Lead with the plain question. Hold the scaffolding** | The analysis can be deep. The sentence handed over must be plain. Give the reasoning only if asked |
| **State the candidate finding in one sentence, get a yes, then write it up** | A finding that cannot be said in one sentence is not understood yet |

**Every one of these is a rule about protecting the human's attention**, because the human is the
only source of truth in the room.

Two of them exist because of a specific failure, and those are in the next section.

### M3 · The artefact shape

Each of these was adopted for a machine reason. Each turned out to be what made the output something
a non-specialist could contribute to.

| Choice | Adopted because | Turned out to also mean |
|---|---|---|
| **One file per finding** | Reading one finding should not mean loading all of them, and parallel sessions writing into one file collide | A reader can be sent one finding rather than a document |
| **One small table per category, not one large matrix** | A category is worked in one pass, so it is written in one place | A small table has room to carry the reason in the row. A large matrix pushes every explanation into notes underneath |
| **Finding IDs allocated in blocks before work starts** | Two sessions both taking "the next free number" collide, and the collision surfaces at merge, after both entries are written | Gaps in the numbering are visible, and a gap is cheaper than a reconciliation pass |
| **Three marks, no fourth, and the reason is the deliverable** | An unmarked row means the walk is incomplete, which is the thing worth knowing | A category considered and dismissed on stated grounds is a decision. A category never considered is a gap |
| **Explicit ownership, per file** | Each session owns its category table exclusively and appends to the shared index, never rewriting it | The record says who wrote what |

Two agents worked two categories in parallel, with the operator moving between them. **Parallelism is
a throughput change, not a depth change** – each session runs the full interview procedure.

## The rules that earned their place

Each of these has a dated failure behind it.

**Lead with the plain question; hold the scaffolding.** On the first parallel test run, the
participant twice had to say *simplify that* before the actual question was visible underneath the
framing, the reasoning and the severity split wrapped around it. That cost lands on the participant,
and it multiplies across parallel sessions.

**State the candidate in one sentence before writing it up.** Three cells in one category had a whole
finding built, framed and paragraphed before the premise was confirmed. Each collapsed the moment the
participant described what actually happens. The cost lands on the person who has to read three
paragraphs to find the one wrong assumption underneath.

**Separate what exists from what is intended.** Describing a system slides into describing the system
as it is meant to be, and both are said in the same breath. *"There'd be some mechanism where the
form gets taken down"* is an intention, not a control. The threat goes in the finding, the intention
becomes a requirement, and the finding says plainly that the control is not yet built. A finding whose
treatment credits an unbuilt control has quietly become an assurance claim.

**Name the good property before the finding.** A gap framed as an edge on a sound design invites the
contribution the exercise exists for. A bare gap invites defensiveness. It also keeps the record
honest in the other direction, because a dismissal that names the property it relies on is auditable.

**Withdraw rather than defend.** Several findings were drafted and pulled back after interview, and
the withdrawals are recorded in the cells rather than deleted. A walk that never retracts is not being
told anything.

**Things that are real, actionable and not threats get a separate series.** The walk reliably turns up
contract clauses that do not cover a task that will certainly happen, documents describing an
architecture the design has moved away from, and scope decisions nobody has taken. They get an `ADJ-`
number, not an `F-` number. A reader is entitled to assume every finding line describes a way the
system can harm someone or be harmed, and one entry that is really a paperwork question corrupts that
guarantee for every other line.

**Derive every count by script, not by hand.** A hand-kept tally had already drifted – it recorded six
open cells when there were seven, because it counted its own rows instead of the marks.

**Never imply independent review where there is none.** The output supports one claim: recognised
practice was followed and what it found was recorded. Not *reviewed*. Not *secure*. A declared gap is
defensible; an implied assurance is not.

### Failure modes, named before starting

- **Admiration for the problem.** A finding with no treatment decision is half a finding.
- **The tidy grid.** No open cells means the walk stopped asking. An open cell is a healthy state.
- **Findings that are really requirements.** *"The system should log exports"* is a control. The
  threat is *"an export cannot be traced to a person."*
- **Over-weighting the dramatic.** Frequency and severity are separate axes.

## What it cost

**Figures from the real engagement, verified 16 September 2026.**

| | |
|---|---|
| Cells walked | **91** across thirteen tables – 42 security, 49 privacy |
| Register before the walk | **16 findings** |
| Register after | **62 findings**, 43 of them produced by this walk |
| Findings file before it was split | **2,201 lines**, then one file per finding |

**Two annexes came in at roughly double their line budget.** They were written down as overruns at the
line, with the date, rather than the targets being quietly restated.

**The front door came in at nearly triple.** It was budgeted at around 120 lines and landed at 350 –
and it is the one document with a real length constraint, because it is the only one the client
actually reads. The length principle still stands and is now unmet.

### A prediction made in advance, which failed

One privacy category went onto a watch-list before the walk started, flagged with a specific fear. It
was walked across all seven holdings and produced **nothing**. Every cell closed.

The reason was recorded rather than assumed. Nothing in the system could stop a person denying an
account attributed to them, because the record is a paraphrase with no verbatim original and no
confirmation step.

**A walk that only reports its successful hypotheses is not evidence of anything.**

### One result that only two taxonomies could find

Four times, a property the security pass recorded as a weakness turned out to be the thing protecting
the subject. Unreliable records protect deniability. Absent read-logging protects the people being
logged.

Each is a live trade-off rather than a defect, and **fixing the security finding would erode the
privacy property.** Running one taxonomy would have produced four confident recommendations that made
the system worse.

## The smallest version that works

One security pass over your trust boundaries. One table per category. One file per finding. A rule
that anything dismissed is written down with its reason, and that *"n/a"* is not a reason.

The privacy spine can come later. The parallel sessions can come much later.

## What's not solved yet

**The agent interviews me, and I represent the client's knowledge.** That is a proxy, and a proxy has
a ceiling – the walk is only as accurate as what I happen to have absorbed from prior conversations.
The artefact shape compensates for this rather than fixing it, because the whole output is built to be
handed over with *tell us what we got wrong*.

**How to run this with the client in the room is unsolved.** It is the obvious next version and it is
not designed yet. Parallel sessions get harder immediately, because the knowledge sits with someone
whose time cannot be booked twice.

**The length principle is unmet**, and it is recorded that way rather than restated downwards.

**Pace is deliberately unsolved.** The obvious speed-up – propose marks for every boundary at once and
interview only the live ones – was declined after a single cell, on the grounds that optimising
against a sample of one is optimising against noise. It has not been revisited since.

---

<!-- DRAFTING ONLY -->

## Source material

- `redmoor_docs/governance/security/threat_model/README.md` – the approach, the artefact table, the overrun note.
- `.../walk_playbook.md` – the working procedure: two spines, the fork test, the interview rules, the parallel-session mechanics, failure modes.
- `.../workbook.md` – §4.3 the two spines, §5.1 coverage, §5.2 what the grids added, §7 limits.
- `.../annex_a_grids.md` – the thirteen tables, the ID reservation table.
- `.../annex_b_findings.md` + `annex_b/` – the index and one file per finding.
- `.../adjacent_findings.md` – the `ADJ-` series.
- `.../findings_register.csv` – the register, 64 rows.
- `.../design_review/` – the two superseded predecessors, kept as the signed historical record.

## Verification state

Counts re-read from source 16 September 2026, against `findings_register.csv` and `annex_b/` rather
than against the README, which has drifted. **Re-verify before publishing.** The README's artefact
table is stale on three lines and must not be quoted.

## Open

- Whether the client-facing front-door document is worth showing as a shape.
- How much of the governance mapping belongs here versus one line.
- The stand-in system is introduced here but belongs in Part 2. Move it when Part 2 is drafted.

<!-- END DRAFTING ONLY -->
