**Status** alternative draft – a how-to rewrite for comparison · **Life** draft · **Reader** you, about to run a threat-modelling pass with an agent

# How to run a threat-modelling pass with agents

This is a procedure. Follow it in order.

It produces a coverage record, a set of findings, and a document your client can argue with. It works
at the design stage, before there is any code to analyse.

The worked example throughout is [the example system](../reference/example-system.md).

## Before you start

**You need four things.**

| | |
|---|---|
| **A system description** | Architecture, data flows, who the users are. Draft quality is fine. It will be wrong in places, and finding that out is part of the work |
| **A person who knows the business** | Not the architecture – the business. What actually happens when a record fails to process. The agent has no way to obtain this except by asking |
| **A repository** | Everything is written to files as you go. Nothing lives in the conversation |
| **Two to four sessions of a few hours** | A full pass over both taxonomies is roughly ninety cells. Plan for days, not an afternoon |

**Know what you are producing before you start.** A document written to **open** the conversation, not
close it: *here is how we looked, here is what we found, tell us what we got wrong.* If you find
yourself writing a coverage statement and a sign-off table, you are building the wrong artefact.

## The shape of the work

You run **two passes**, not one.

| | Security pass | Privacy pass |
|---|---|---|
| **Taxonomy** | STRIDE, 6 categories | LINDDUN GO, 7 suits |
| **Walked against** | Your trust boundaries | Your data holdings |
| **Asks** | How does an attacker break this? | How does this harm people when it works as designed? |

Seven boundaries × 6 = 42 cells. Seven holdings × 7 = 49 cells. **Ninety-one cells, each one either a
finding or a written reason.**

**Do not reconcile the two spines.** They answer different questions on different units. Forcing one
spine onto both loses cells.

**The procedure below runs in four phases.**

| Phase | Steps | What happens |
|---|---|---|
| **Set up** | 1–4 | Describe the system on both spines. Create the files |
| **Pass 1 · Security** | 5–9 | Six categories, walked across your boundaries |
| **Pass 2 · Privacy** | 10–12 | Seven suits, walked across your holdings |
| **Finish** | 13–15 | Compare the passes, parallelise, synthesise |

---

# Set up

You describe the system on **both** spines before either pass starts, because Step 3 needs them side
by side.

## Step 1 · List your trust boundaries

A **trust boundary** is where data moves between two parties who trust each other differently.

Ask of the system: *where does something cross from one party's control into another's?* Each answer
is a boundary. Number them.

**Worked example.**

| | Boundary | Why it is separate |
|---|---|---|
| **B1** | Report content leaving the core store | The core is the highest-trust zone. Anything leaving it is a controlled release |
| **B2** | The insurer logging in to the dashboard | A different organisation, reading data about the company's staff |
| **B3** | The public check-in endpoint | Anyone with the link can write to it. No authentication by design |
| **B4** | Handover from the supplier to the company | Control of the system changes hands |
| **B5** | The infrastructure underneath | The cloud account, the database, the people with administrative access |
| **B6** | The supplier's own handling during the build | Live data on machines the client does not control |
| **B7** | The company's own handling | Exports, spreadsheets, board packs. Where the platform stops being able to help |

**Aim for five to nine.** Fewer and you are describing zones, not boundaries. More and you are
describing components.

---

## Step 2 · List your data holdings

A **holding** is one place personal data sits, treated as a single thing for analysis. Not a database
table. Not a server. A body of records about people you can reason about as a unit.

Ask: *where does personal data come to rest?* Include the places you do not control.

**Worked example.**

| | Holding | What is in it |
|---|---|---|
| **H1** | Canonical record store | Reports and check-ins converge here |
| **H2** | Aggregate store | What the insurer reads, broken down by site |
| **H3** | Intake | Everything as it is first captured |
| **H4** | The supplier's own processing | Live data on a development machine during the build |
| **H5** | The company's own handling | Exports to spreadsheets, board packs |
| **H6** | Operational exhaust | Logs, dead-letter queue, transient stores |

**Holdings outside the platform get no row.** Paper notes in a filing cabinet are real and are not
analysable here. Note them in the cell that raises them and move on.

---

## Step 3 · Split holdings with the fork test

Some holdings hide two different analyses inside one row. Split those, and only those.

**The test: split only where walking the holding as one forces two different answers.** Not where the
data merely differs.

**Worked example.** H3, intake, looks like one holding. Apply one privacy question to it:

> *Can the person deny having said this?*

| | Answer |
|---|---|
| **Incident report** from a supervisor's managed device | Attribution is **the control**. A report nobody can be held to is worthless |
| **Wellbeing check-in** from a member of staff's own phone | Attribution is **the harm**. Someone who cannot deny having reported that they are struggling has lost the thing that made the check-in safe to fill in |

Same question, opposite answers. **H3 splits into H3a and H3b.**

Now test H6, operational exhaust, the same way. Its retention answer differs from H1 – exhaust is
purged at thirty days while the canonical store is kept. That is a diverging answer, so H6 stays
separate.

**Different content is the symptom. Diverging analysis is the justification.** Apply the test
strictly, or the spine splits forever and the pass never finishes.

You now have seven holdings: H1, H2, H3a, H3b, H4, H5, H6.

---

## Step 4 · Set up the files before the first question

Three files and one directory. Create them now, empty.

```
threat_model/
  workbook.md            the system, scope, assumptions, method, synthesis
  annex_a_grids.md       thirteen tables – one per category and suit
  annex_b_findings.md    an index table
  annex_b/               one file per finding, F-<nnn>-<slug>.md
```

**One file per finding is not optional.** Reading one finding should not mean loading all of them, and
two agents writing into one file will collide.

**Reserve finding-ID blocks before any work starts.** Put this table at the top of `annex_a_grids.md`:

| Block | Category | Claimed | Used |
|---|---|---|---|
| F-1 … F-20 | Spoofing | | |
| F-21 … F-40 | Tampering | | |
| F-41 … F-60 | Repudiation | | |

Two sessions both taking *the next free number* will collide, and the collision surfaces at merge,
after both entries are written. **Gaps in the numbering cost nothing.** Do not compact them.

---

# Pass 1 · The security pass

**You are walking your seven trust boundaries.** Holdings are not used in this pass at all.

Six categories × seven boundaries = **42 cells**.

## Step 5 · Pick one category and prepare it

Work one category all the way across every boundary before starting the next. Asking the same
question at seven different boundaries is what catches the category you would otherwise skim.

**The six STRIDE categories:**

| | Category | The question |
|---|---|---|
| **S** | Spoofing | Can someone pretend to be someone they are not? |
| **T** | Tampering | Can data or code be changed by someone who should not? |
| **R** | Repudiation | Can someone do something and deny it? |
| **I** | Information disclosure | Can data reach someone who should not see it? |
| **D** | Denial of service | Can the system be made unavailable? |
| **E** | Elevation of privilege | Can someone gain rights they were not granted? |

Before the first question, do three things.

**Research the category.** What it covers, where it borders its neighbours, its specific pitfalls. Do
this first, not while the interview is open.

**Read what already exists, including the contracts.** Contracts are easy to skip because they read as
commercial material, and they are often where security obligations are actually written down.
Proposing a control that is already a contractual deliverable wastes the session.

**Write the disambiguation rules down before using them.** State each as something answerable, so that
when a cell is borderline you have a test rather than an opinion.

**Worked example, preparing Repudiation:**

| Against | Test |
|---|---|
| **vs Spoofing** | Assume authentication is perfect. Does the finding survive? If it vanishes it was Spoofing |
| **vs Tampering** | Ask who benefits. If the log can be altered by the person whose conduct it records, it is Repudiation with Tampering as the mechanism |
| **vs Information disclosure** | Under-logging is Repudiation. Over-logging is Information disclosure |

---

## Step 6 · Work the category across every boundary, by interview

Take your boundaries in order – on the example system, B1 through B7 from Step 1 – and ask the
category's question at each one.

You are now working one cell: **one category at one boundary.** Repudiation at B2, for instance.

The agent runs four moves per cell.

### Move 1 · Ask what happens, before asking what goes wrong

The agent has no model of the system. A hypothesis-first question spends the whole exchange being
reversed.

> **Agent:** Walk me through what happens when someone from the insurer opens the dashboard. Who are
> they, how do they get an account, and what do they see?

### Move 2 · Ask the threat question in the system's own terms

Not *"is there a repudiation risk at B2."* A cell answered in taxonomy vocabulary has usually not been
thought about.

> **Agent:** If someone later asked *which analyst at the insurer looked at the Northern site's
> figures in March*, could you answer that?
>
> **Participant:** No. The dashboard doesn't log reads. We'd know the account, maybe, if they each had
> one. I think they share one.

### Move 3 · State the candidate in one sentence, and get a yes

**Lead with the plain question. Hold the scaffolding.** The analysis can be deep. The sentence handed
over must be plain. Give the reasoning only if asked.

> **Agent:** So: the dashboard can't say which person at the insurer saw which site's data, and a
> shared login means it couldn't even narrow it to a person. Finding, or accept?
>
> **Participant:** Finding. Though I'd want to say that not logging reads is partly deliberate –
> we're not trying to surveil the insurer's staff.

**A finding that cannot be said in one sentence is not understood yet.** Do not write the entry before
this lands.

### Move 4 · Separate what exists from what is intended

Descriptions slide into intentions, and both arrive in the same breath.

> **Participant:** There'd be some mechanism where each analyst gets their own account.

That is an intention, not a control. Split it three ways:

- the **threat** goes in the finding;
- the **intention** becomes a requirement, written as a requirement;
- the finding's treatment says plainly that the control is **not built**.

A finding whose treatment credits an unbuilt control has become an assurance claim.

### Two habits that change the output

**Name the good property before the gap.** *"Aggregates-only is the right property here; what it does
not cover is…"* A gap framed as an edge on a sound design invites contribution. A bare gap invites
defensiveness.

**Withdraw rather than defend.** When the interview kills a finding you already drafted, record the
withdrawal in the cell. A pass that never retracts is not being told anything.

---

## Step 7 · Mark the cell

Three marks. There is no fourth. An unmarked row means the pass is incomplete.

| Mark | When |
|---|---|
| `✅ F-n` | Produced a finding. Write the entry **now**, not later |
| `➖` | Considered and closed. **The reason is the deliverable** – *"n/a"* is not a reason |
| `⚠️` | Cannot be closed by you. Name what it waits on and who owns it |

**Worked example**, the row written for the cell above, in the Repudiation table:

| Boundary | Mark | Finding or reason |
|---|---|---|
| **B2** The insurer logging in | `✅ F-48` | The dashboard records nothing – no sign-in event, no view event – so *"which analyst saw this site?"* has no answer. A shared login removes even account-level attribution. **Treatment splits:** sign-in visibility is the insurer's own account governance and is achievable today; content-read logging is **designed for and not built**, because a record of which analyst read which site is surveillance of the insurer's own staff. Recorded as a decision so the absence does not later read as an oversight |

Note what that row carries: the finding, the mechanism, the split treatment, and the reason a control
was deliberately not taken. **That is why there is one table per category.** A single large matrix has
no room for a cell like this and pushes every explanation into notes underneath.

---

## Step 8 · Write the finding as its own file

Write it in plain language the first time. Not a compressed note to be expanded later. The finding is
the thing that goes in front of the client, and a statement that cannot survive plain English is one
that is not yet understood.

**Worked example**, `annex_b/F-048-dashboard-records-no-reads.md`:

```markdown
# F-48 · The dashboard cannot say who read what

> **Finding** F-48 · **Origin** STRIDE Repudiation · B2 · **Raised** 12 March

*What it is.* The dashboard records no sign-in events and no view events. Analysts at the
insurer are understood to share a login. If asked which person saw a given site's figures on
a given day, the system has no answer and no way to reconstruct one.

*Why it matters.* Aggregates are small for small sites. A read record is the only thing that
could narrow who held that data on screen. Export is disabled, so the realistic route out is
a screen capture, which is untraceable by nature.

*What was considered and set aside.* Content-read logging was designed for and is not built.
A record of which analyst read which site is surveillance of the insurer's own staff, which
is out of scope. Recorded as a decision, not an oversight.

*Treatment.* Mitigate in part – individual accounts rather than a shared login, which is the
insurer's own account governance and achievable now. Content-read logging: accept, disclosed.

*Residual.* After individual logins, the system can say who had access, never who looked.
```

Then add one row to the index in `annex_b_findings.md`, and one line to the register.

### If it is not a threat, give it a different number

Contract gaps, stale documents, scope nobody has decided – real, actionable, not threats.

Use a separate series, `ADJ-n`. **A reader is entitled to assume every `F-` line describes a way the
system can harm someone or be harmed.** One paperwork entry in the register corrupts that guarantee
for every other line.

The test: *does this describe something going wrong with the system, or something wrong with the
paperwork about the system?*

---

## Step 9 · Repeat for the remaining five categories

Six categories, seven boundaries, one table each. When all six tables are full, the security pass is
done.

---

# Pass 2 · The privacy pass

**You are now walking your seven data holdings.** Boundaries are not used in this pass at all.

Seven suits × seven holdings = **49 cells**.

**Everything about the mechanics is the same as Pass 1.** Same four interview moves, same three marks,
same one-file-per-finding. Only the unit and the question bank change, so the steps below cover only
what differs.

## Step 10 · Pick one suit and prepare it

**The seven LINDDUN GO suits:**

| | Suit | The question |
|---|---|---|
| **L** | Linking | Can separate records be connected to the same person? |
| **I** | Identifying | Can someone be named from data not meant to name them? |
| **N** | Non-repudiation | Can a person be prevented from denying something? |
| **D** | Detecting | Is the fact someone participated observable, even without content? |
| **D** | Data disclosure | Is more collected, kept or shared than is needed? |
| **U** | Unawareness | Do people not understand what happens to their data? |
| **N** | Non-compliance | Does the handling breach law, policy or consent? |

**Non-repudiation is the one that catches people out.** In security it is a property you want. In
privacy it is a threat – a person who cannot deny having said something has lost something.

**One extra preparation step for this pass: read the real data first.** Before the first suit, open
the actual form output. Not the specification of it – the real columns, the real metadata, the real
free-text fields. Privacy questions are answered against what data exists, and the specification will
have left things out.

**Add one disambiguation test specific to this pass:**

| Against | Test |
|---|---|
| **vs STRIDE Repudiation** | Ask whether the actor is **staff acting in role**, where attribution is a control, or a **data subject**, where attribution may be the harm. The same log line can answer both ways. Record both |

---

## Step 11 · Work the suit across every holding, by interview

Take your holdings in order – on the example system, H1, H2, H3a, H3b, H4, H5, H6 from Steps 2 and 3.

One cell is **one suit at one holding.** Detecting at H3b, for instance.

Use the same four moves from Step 6. What changes is the shape of the question: you are asking about a
body of records, not about a crossing point.

**Worked example**, Detecting at H3b, the wellbeing check-in:

> **Agent:** The check-in is anonymous. Setting aside what people write in it – can anyone tell
> whether a particular person completed one at all?
>
> **Participant:** Not from the submission. But the safety team know the headcount per site, and they
> can see how many came in.
>
> **Agent:** So at a site with six staff where five respond, is the sixth person identifiable as a
> non-respondent?
>
> **Participant:** In principle, yes. Someone could work it out.
>
> **Agent:** So: participation itself carries no signal, but **non**-participation does, and it gets
> sharper the smaller the site. Finding, or accept?
>
> **Participant:** Finding. Though a lot of people just submit something empty rather than skip it,
> which sort of solves it.

**Note the last line.** That is the participant handing over a real mitigation that is not in any
specification, and it is the kind of thing only an interview produces. It also inverts: the junk
submission is the opt-out the platform never designed.

**Expect more open cells in this pass than in the security one.** Unawareness and Non-compliance run
straight at things that are somebody else's to decide – what people were told, whether consent covers
it. A cell that lands *open, waiting on the client* is the correct result there, not a stall.

---

## Step 12 · Repeat for the remaining six suits

When all seven tables are full, the privacy pass is done.

---

# After both passes

## Step 13 · Compare the two passes against each other

**This is the output you can only get by running both, and it is easy to skip.**

Go through the findings from each pass looking for the same mechanism appearing twice with opposite
signs. A control in one, a harm in the other.

**Worked example.** The security pass recorded *the dashboard logs no reads* as an accountability gap.
The privacy pass, at the same mechanism, recorded that logging reads would be surveillance of the
insurer's own staff.

**Same absence. One pass calls it a weakness, the other calls it protection.**

Write these up as a set rather than leaving them in their separate findings. Each is a live trade-off,
not a defect, and **fixing the security finding erodes the privacy property**. Somebody has to decide
which way it goes, and they can only do that if the two readings are on the same page.

---

## Step 14 · Run categories in parallel, once the method is settled

Two agents, two categories, one operator moving between them.

**Parallelism is a throughput change, not a depth change.** Each session runs the full interview. The
moment a session starts proposing marks to save time, the pass stops being worth running.

Four rules make concurrent sessions safe:

| | |
|---|---|
| **Own your own files exclusively** | Your category table, your finding files. Never edit another session's table, even to fix an obvious typo |
| **Append to shared files, never rewrite them** | Add your index row. Do not regenerate the table |
| **Re-read immediately before editing a shared file** | Not once at session start. An edit built on a stale read silently reverts the other session |
| **Do not commit unless asked** | A commit sweeps up half-finished work from the other session |

**Do not start here.** Run at least one category single-threaded first, or you will parallelise a
procedure you have not yet learned.

---

## Step 15 · Synthesise, in one place

Cross-category judgements cannot be written by a session that has seen one category.

A session finishing its category **says** what looked cross-cutting. It does not write that into the
shared sections itself.

**Derive every count by script, not by hand.** Write something that reads the mark column of every
table and reports totals plus any unmarked row. A hand-kept tally drifts, and it drifts silently.

Then write four things:

1. **Coverage** – rows are the thirteen categories and suits, not the boundaries or holdings. The
   question is *was this taxonomy actually walked?*
2. **What the pass added** – the narrative. This is the part anyone reads.
3. **Accepted risks** – as a signable list, in plain English, because someone has to sign it.
4. **Limits** – what was deliberately not walked, and what the work does not support being claimed.

---

## What good looks like

Check these before you call it done.

**The mark distribution varies by category.** If every category comes back all-findings, you are
marking generously rather than analysing. A category pointed at part of a design that genuinely works
should come back mostly closed, with reasons.

**There are open cells.** A grid with nothing open, in a system that depends on facts held by other
people, means the pass stopped asking. An open cell is a healthy state.

**Every closed cell has a reason you could defend out loud.** Search your tables for *"n/a"* and for
one-word reasons. Each is a cell that was not worked.

**At least one finding was withdrawn.** A pass that never retracts is not being told anything.

**Nothing claims more than it can.** The work supports one sentence: *recognised practice was followed
and what it found was recorded.* Not *reviewed*. Not *secure*. A declared gap is defensible; an
implied assurance is not.

### Four failure modes to watch for

| | |
|---|---|
| **Admiration for the problem** | A finding with no treatment decision is half a finding |
| **The tidy grid** | No open cells means the pass stopped asking |
| **Findings that are really requirements** | *"The system should log exports"* is a control. The threat is *"an export cannot be traced to a person"* |
| **Over-weighting the dramatic** | The rare severe case is not the design centre. Frequency and severity are separate axes |

---

## What to expect it to cost

**Figures from one full pass, measured 16 September 2026.**

| | |
|---|---|
| Cells worked | 91, across thirteen tables |
| Findings produced | 43, taking a register from 16 to 62 |
| Findings file before it was split into one file per finding | 2,201 lines |

**Budget roughly double what you expect for the reference annexes.** Two came in at about twice
target. Hold the line on the client-facing document instead – it is the only one anybody reads end to
end, and it is the one that overran worst.

**A category can produce nothing, and that is a result.** One privacy suit was flagged in advance with
a specific fear, walked across all seven holdings, and closed every cell with a recorded reason.

---

## What's not solved yet

**The agent interviews the supplier, not the client.** Somebody has to represent the client's
knowledge, and that is a proxy with a ceiling. The artefact shape compensates rather than fixes it:
the whole output is built to be handed over with *tell us what we got wrong*.

**Running this with the client in the room is not designed yet.** Parallel sessions get harder
immediately, because the knowledge sits with someone whose time cannot be booked twice.

**Pace is unsolved on purpose.** The obvious speed-up – propose marks for every boundary at once and
interview only the live ones – was declined, because optimising against a sample of one is optimising
against noise. It has not been revisited.

**Length is a design constraint and this method does not meet it.** Recorded that way rather than
restated downwards.
