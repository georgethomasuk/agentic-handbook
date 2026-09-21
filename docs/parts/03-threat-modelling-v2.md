**Status** alternative draft – a how-to rewrite for comparison · **Life** draft · **Reader** you, about to run a threat-modelling pass with an agent

# How to run a threat-modelling pass with agents

This is a procedure. Follow it in order.

It produces a coverage record, a set of findings, and a document your client can argue with. It works
at the design stage, before there is any code to analyse.

The worked example throughout is [the example system](../reference/example-system.md).

---

# Context

## What you are producing

**A document written to open the conversation, not close it.** *Here is how we looked, here is what we
found, tell us what we got wrong.*

If you find yourself writing a coverage statement and a sign-off table, you are building the wrong
artefact. That is an end-of-engagement assurance document, and you are at the start.

## What you need before you start

| | |
|---|---|
| **A system description** | Architecture, data flows, who the users are. Draft quality is fine. It will be wrong in places, and finding that out is part of the work |
| **A person who knows the business** | Not the architecture – the business. What actually happens when a record fails to process. The agent has no way to obtain this except by asking |
| **A repository** | Everything is written to files as you go. Nothing lives in the conversation |
| **Days, not an afternoon** | A full pass over both taxonomies is around ninety cells |

## What it costs

**Figures from one full pass, measured 16 September 2026.**

| | |
|---|---|
| Cells worked | 91, across thirteen tables |
| Findings produced | 43, taking a register from 16 to 62 |
| Findings file before it was split into one file per finding | 2,201 lines |

**Budget roughly double what you expect for the reference annexes.** Two came in at about twice
target. Hold the line on the client-facing document instead – it is the only one anybody reads end to
end, and it is the one that overran worst.

## Who does what

Three roles. They are referred to by name throughout, so it is always clear who is acting.

| | | |
|---|---|---|
| **You** | the operator | Direct the agent. Decide when a step is done. Make the calls the agent cannot: what counts as a boundary, whether a split is justified, when the work is finished |
| **The agent** | | Research the category. Ask the questions. Draft findings. Write every file. It starts knowing nothing about the system |
| **The participant** | | Hold the business knowledge and answer the questions. What actually happens, as opposed to what the specification says |

**You and the participant may be the same person.** Today they usually are – the operator represents
the client's knowledge from prior conversations. That is a limitation rather than a design, and it is
in *What's not solved yet*.

**Never let the agent be the participant.** If it starts answering its own questions from the
specification, the pass is producing a summary of a document rather than a model of a system.

## The shape of the work

You run **two passes**, not one.

| | Pass 2 · Security | Pass 3 · Privacy |
|---|---|---|
| **Taxonomy** | STRIDE, 6 categories | LINDDUN GO, 7 suits |
| **Walked against** | Your trust boundaries | Your data holdings |
| **Asks** | How does an attacker break this? | How does this harm people when it works as designed? |

Six categories × seven boundaries = 42 cells. Seven suits × seven holdings = 49 cells. **Ninety-one
cells, each one either a finding or a written reason.**

**Do not reconcile the two spines.** They answer different questions about different units. Forcing
one spine onto both loses cells.

**Work through it sequentially.** One category at a time, one cell at a time, start to finish. There
is a section on speeding it up at the end, and it is deliberately not part of the procedure.

| Section | Steps | What happens |
|---|---|---|
| **1 · Set up** | 1.1 – 1.4 | Describe the system on both spines. Create the files |
| **2 · The security pass** | 2.1 – 2.5 | Six categories, walked across your boundaries |
| **3 · The privacy pass** | 3.1 – 3.3 | Seven suits, walked across your holdings |
| **4 · Bringing it together** | 4.1 – 4.2 | Compare the passes, then synthesise |
| **Speeding it up** | – | Only once the signals below are present |
| **Evaluating the quality** | – | Checks to run before calling it done |

---

# 1 · Set up

Describe the system on **both** spines before either pass starts, because step 1.3 needs them side by
side.

## 1.1 · List your trust boundaries

> **Agent** drafts from the system description · **You** check and decide the final list.

A **trust boundary** is where data moves between two parties who trust each other differently.

The agent works through the system description asking *where does something cross from one party's
control into another's?* Each answer is a boundary. Number them.

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

**Aim for five to nine.** Fewer and the agent is describing zones, not boundaries. More and it is
describing components. This is your call to make, not its.

---

## 1.2 · List your data holdings

> **Agent** drafts from the system description · **You** check and decide the final list.

A **holding** is one place personal data sits, treated as a single thing for analysis. Not a database
table. Not a server. A body of records about people you can reason about as a unit.

The agent asks *where does personal data come to rest?* It must include the places nobody controls –
the client's own exports, the supplier's own machines.

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
analysable here. The agent notes them in the cell that raises them and moves on.

---

## 1.3 · Split holdings with the fork test

> **Agent** proposes candidate splits · **Participant** answers the forking question · **You** decide.

Some holdings hide two different analyses inside one row. Split those, and only those.

The agent proposes a split. You decide whether to take it, because an over-eager split is what makes
the pass unfinishable.

**The test: split only where walking the holding as one forces two different answers.** Not where the
data merely differs.

**Worked example.** H3, intake, looks like one holding. The agent puts one privacy question to the
participant:

> *Can the person deny having said this?*

| | Answer |
|---|---|
| **Incident report** from a supervisor's managed device | Attribution is **the control**. A report nobody can be held to is worthless |
| **Wellbeing check-in** from a member of staff's own phone | Attribution is **the harm**. Someone who cannot deny having reported that they are struggling has lost the thing that made the check-in safe to fill in |

Same question, opposite answers. **H3 splits into H3a and H3b.**

The agent then tests H6, operational exhaust, the same way. Its retention answer differs from H1 – exhaust is
purged at thirty days while the canonical store is kept. That is a diverging answer, so H6 stays
separate.

**Different content is the symptom. Diverging analysis is the justification.** Hold the agent to that
test, or the spine splits forever and the pass never finishes.

You now have seven holdings: H1, H2, H3a, H3b, H4, H5, H6.

---

## 1.4 · Set up the files before the first question

> **You** create the files and reserve the ID blocks. **Agent** writes into them from here on.

Three files and one directory. Create them now, empty, before the agent is given any task.

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

# 2 · The security pass

**The agent is walking your trust boundaries.** Holdings are not used in this section at all.

Six categories × seven boundaries = **42 cells**.

## 2.1 · Pick one category and prepare it

> **You** choose the category · **Agent** does all three preparation tasks and writes the rules down.

One category is worked all the way across every boundary before the next one starts. Asking the same
question at seven different boundaries is what catches the category the agent would otherwise skim.

**The six STRIDE categories:**

| | Category | The question |
|---|---|---|
| **S** | Spoofing | Can someone pretend to be someone they are not? |
| **T** | Tampering | Can data or code be changed by someone who should not? |
| **R** | Repudiation | Can someone do something and deny it? |
| **I** | Information disclosure | Can data reach someone who should not see it? |
| **D** | Denial of service | Can the system be made unavailable? |
| **E** | Elevation of privilege | Can someone gain rights they were not granted? |

Before the agent puts its first question, it does three things. None is optional, and each produces
something written down that you can check.

**Research the category.** What it covers, where it borders its neighbours, its specific pitfalls.
This happens first, not while the interview is open.

**Read what already exists, including the contracts.** Contracts are easy for an agent to skip because
they read as commercial material, and they are often where security obligations are actually written
down. Proposing a control that is already a contractual deliverable wastes the participant's time.

**Write the disambiguation rules down before using them.** Each is stated as something answerable, so
that when a cell is borderline there is a test rather than an opinion. Read them before the pass
starts – this is the cheapest place to catch an agent that has misunderstood the category.

**Worked example, preparing Repudiation:**

| Against | Test |
|---|---|
| **vs Spoofing** | Assume authentication is perfect. Does the finding survive? If it vanishes it was Spoofing |
| **vs Tampering** | Ask who benefits. If the log can be altered by the person whose conduct it records, it is Repudiation with Tampering as the mechanism |
| **vs Information disclosure** | Under-logging is Repudiation. Over-logging is Information disclosure |

---

## 2.2 · Work the category across every boundary, by interview

> **Agent** asks · **Participant** answers · **You** move things on when a cell is settled.

The agent takes the boundaries in order – on the example system, B1 through B7 from 1.1 – and asks the
category's question at each one.

One cell is **one category at one boundary.** Repudiation at B2, for instance.

The agent runs four moves per cell. Watch for it skipping move 1.

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

**Lead with the plain question. Hold the scaffolding.** The agent's analysis can be deep. The sentence
it hands over must be plain, and the reasoning comes only if the participant asks for it.

> **Agent:** So: the dashboard can't say which person at the insurer saw which site's data, and a
> shared login means it couldn't even narrow it to a person. Finding, or accept?
>
> **Participant:** Finding. Though I'd want to say that not logging reads is partly deliberate –
> we're not trying to surveil the insurer's staff.

**A finding that cannot be said in one sentence is not understood yet.** No entry gets written before
this lands.

### Move 4 · Separate what exists from what is intended

Descriptions slide into intentions, and both arrive in the same breath.

> **Participant:** There'd be some mechanism where each analyst gets their own account.

That is an intention, not a control. The agent splits it three ways:

- the **threat** goes in the finding;
- the **intention** becomes a requirement, written as a requirement;
- the finding's treatment says plainly that the control is **not built**.

A finding whose treatment credits an unbuilt control has become an assurance claim.

### Two habits that change the output

**Name the good property before the gap.** *"Aggregates-only is the right property here; what it does
not cover is…"* A gap framed as an edge on a sound design invites contribution. A bare gap invites
defensiveness.

**Withdraw rather than defend.** When the interview kills a finding the agent already drafted, the
withdrawal is recorded in the cell rather than deleted. A pass that never retracts is not being told
anything.

---

## 2.3 · Mark the cell

> **Agent** writes the row, using the answer the participant already confirmed in 2.2.

Three marks. There is no fourth. An unmarked row means the pass is incomplete.

| Mark | When |
|---|---|
| `✅ F-n` | Produced a finding. Write the entry **now**, not later |
| `➖` | Considered and closed. **The reason is the deliverable** – *"n/a"* is not a reason |
| `⚠️` | Cannot be closed by anyone in the room. Name what it waits on and who owns it |

**Worked example**, the row written for the cell above, in the Repudiation table:

| Boundary | Mark | Finding or reason |
|---|---|---|
| **B2** The insurer logging in | `✅ F-48` | The dashboard records nothing – no sign-in event, no view event – so *"which analyst saw this site?"* has no answer. A shared login removes even account-level attribution. **Treatment splits:** sign-in visibility is the insurer's own account governance and is achievable today; content-read logging is **designed for and not built**, because a record of which analyst read which site is surveillance of the insurer's own staff. Recorded as a decision so the absence does not later read as an oversight |

Note what that row carries: the finding, the mechanism, the split treatment, and the reason a control
was deliberately not taken. **That is why there is one table per category.** A single large matrix has
no room for a cell like this and pushes every explanation into notes underneath.

---

## 2.4 · Write the finding as its own file

> **Agent** writes the file, the index row and the register line, before moving to the next cell.

The agent writes it in plain language the first time. Not a compressed note to be expanded later. The
finding is the thing that goes in front of the client, and a statement that cannot survive plain
English is one that is not yet understood.

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

Then one row goes into the index in `annex_b_findings.md`, and one line into the register. All three
before the next cell is opened – an agent that batches them will lose them on a context reset.

### If it is not a threat, give it a different number

Contract gaps, stale documents, scope nobody has decided – real, actionable, not threats.

These go in a separate series, `ADJ-n`. **A reader is entitled to assume every `F-` line describes a
way the system can harm someone or be harmed.** One paperwork entry in the register corrupts that
guarantee for every other line.

The test: *does this describe something going wrong with the system, or something wrong with the
paperwork about the system?*

---

## 2.5 · Repeat for the remaining five categories

> **You** decide the order and when to start the next category.

Six categories, seven boundaries, one table each. When all six tables are full, the security pass is
done.

---

# 3 · The privacy pass

**The agent is now walking your data holdings.** Boundaries are not used in this section at all.

Seven suits × seven holdings = **49 cells**.

**The mechanics are identical to the security pass.** Same four interview moves (2.2), same three
marks (2.3), same one file per finding (2.4). Only the unit and the question bank change, so what
follows covers only what differs.

## 3.1 · Pick one suit and prepare it

> **You** choose the suit · **Agent** prepares it, and reads the real data before the first question.

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

**Non-repudiation is the one that catches agents out.** In security it is a property you want. In
privacy it is a threat – a person who cannot deny having said something has lost something. Check the
agent has this the right way round before it starts.

**One extra preparation step for this pass: the agent reads the real data first.** Before the first
suit, give it the actual form output. Not the specification of it – the real columns, the real
metadata, the real free-text fields. Privacy questions are answered against what data exists, and the
specification will have left things out.

**The agent adds one disambiguation test specific to this pass:**

| Against | Test |
|---|---|
| **vs STRIDE Repudiation** | Ask whether the actor is **staff acting in role**, where attribution is a control, or a **data subject**, where attribution may be the harm. The same log line can answer both ways. Record both |

---

## 3.2 · Work the suit across every holding, by interview

> **Agent** asks · **Participant** answers · **You** move things on when a cell is settled.

The agent takes the holdings in order – on the example system, H1, H2, H3a, H3b, H4, H5, H6 from 1.2
and 1.3.

One cell is **one suit at one holding.** Detecting at H3b, for instance.

Same four moves as 2.2. What changes is the shape of the question: it is about a body of records, not
about a crossing point.

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

## 3.3 · Repeat for the remaining six suits

> **You** decide the order and when to start the next suit.

When all seven tables are full, the privacy pass is done.

---

# 4 · Bringing it together

## 4.1 · Compare the two passes against each other

> **Agent** proposes the pairs · **You** confirm them and decide what goes to the client.

**This is the output you can only get by running both, and it is easy to skip.**

The agent reads both passes' findings looking for the same mechanism appearing twice with opposite
signs. A control in one, a harm in the other.

**Worked example.** The security pass recorded *the dashboard logs no reads* as an accountability gap.
The privacy pass, at the same mechanism, recorded that logging reads would be surveillance of the
insurer's own staff.

**Same absence. One pass calls it a weakness, the other calls it protection.**

These are written up as a set rather than left in their separate findings. Each is a live trade-off,
not a defect, and **fixing the security finding erodes the privacy property**. The client has to
decide which way it goes, and they can only do that if both readings are on the same page. Neither you
nor the agent resolves one of these quietly.

---

## 4.2 · Synthesise, in one place

> **You** choose one session to do this. **Agent** writes it, having read every category table.

Cross-category judgements cannot be written by an agent that has seen one category. Give this to a
session that reads all thirteen tables from the files.

A session finishing its own category **tells you** what looked cross-cutting. It does not write that
into the shared sections itself.

**Have the agent derive every count by script, not by hand.** A short script that reads the mark column
of every table and reports totals plus any unmarked row. A hand-kept tally drifts, and it drifts
silently – so the script is the answer, not the agent's arithmetic.

The synthesis session then writes four things:

1. **Coverage** – rows are the thirteen categories and suits, not the boundaries or holdings. The
   question is *was this taxonomy actually walked?*
2. **What the pass added** – the narrative. This is the part anyone reads.
3. **Accepted risks** – as a signable list, in plain English, because someone has to sign it.
4. **Limits** – what was deliberately not walked, and what the work does not support being claimed.

---

# Speeding it up

The procedure above is slow on purpose. This section is how to make it faster **and how to know when
you have earned the right to.** Every judgement here is yours – the agent cannot tell you whether it
has become reliable.

## The signal that it is safe

**You can predict the agent's mark for a cell before it runs the interview, and you are usually
right.**

That is the whole test. It means the shape of a live question in this system is now known, and the
cells that genuinely need an interview can be told apart from the ones that can be proposed and
confirmed.

Four things to check before you believe it:

| | |
|---|---|
| **At least two full categories are finished, sequentially** | One is a sample of one. Optimising against a sample of one is optimising against noise |
| **The agent's disambiguation rules stopped changing mid-category** | If it is still rewriting the test that separates this category from its neighbour, it does not yet know the category |
| **No finding has been withdrawn for the same reason twice** | A repeated withdrawal means a wrong assumption is still in play |
| **The participant has stopped correcting the agent's description of the system** | While the specification is still being falsified, nobody knows the system well enough to guess at cells |

**If any of those is not true, keep going sequentially.** It will feel slow. That is the price of the
calibration.

## Two ways to go faster

**Propose and confirm, instead of interviewing.** For cells you have told the agent it may call, it
puts the proposed mark and its reason to the participant in one sentence and asks for a yes or no. The
full interview stays in place for every other cell. **You decide which cells qualify, not the agent** –
an agent asked to judge its own reliability will say yes.

**Run two categories at once.** Two agent sessions, two categories, you moving between them as the
single participant.

**Parallelism is a throughput change, not a depth change.** Each session still runs the full interview
on the cells that need it. The moment a session starts proposing marks it has not earned, the pass
stops being worth running.

**The ceiling is you.** Two sessions is what one participant can hold. A third does not fail loudly –
it fails by getting shallower answers from a person who is now context-switching.

## Four rules that make concurrent sessions safe

| | |
|---|---|
| **Each session owns its own files exclusively** | Its category table, its finding files. It never edits another session's table, even to fix an obvious typo |
| **Shared files are append-only** | A session adds its index row. It does not regenerate the table |
| **Re-read immediately before editing a shared file** | Not once at session start. An edit built on a stale read silently reverts the other session |
| **No session commits unless you ask it to** | A commit sweeps up half-finished work from the other session |

Finding-ID blocks (1.4) exist for exactly this. Two sessions both taking *the next free number* will
collide, and the collision surfaces at merge, after both entries are written. Give each session its
block when you start it.

## What not to speed up

**The descriptive question.** Move 1 of the interview – *walk me through what actually happens* – is
where specifications get corrected. An agent under time pressure drops it first, and that is how a
pass ends up analysing a system that does not exist.

**Cross-category synthesis.** It cannot be done by a session that has seen one category, and it cannot
be split across two.

---

# Evaluating the quality

**These are yours to run, on the agent's output.** Do not ask the agent whether its own pass was good
– it will tell you it was. Each check below is cheap and reads the files rather than the conversation.

**The mark distribution varies by category.** If every category comes back all-findings, the agent is
marking generously rather than analysing. A category pointed at part of a design that genuinely works
should come back mostly closed, with reasons.

**There are open cells.** A grid with nothing open, in a system that depends on facts held by other
people, means the pass stopped asking. An open cell is a healthy state.

**Every closed cell has a reason you could defend out loud.** Grep the tables for *"n/a"* and for
one-word reasons. Each one is a cell the agent did not work.

**At least one finding was withdrawn.** A pass that never retracts is not being told anything – it is
an agent confirming its own first guesses.

**Nothing claims more than it can.** The work supports one sentence: *recognised practice was followed
and what it found was recorded.* Not *reviewed*. Not *secure*. A declared gap is defensible; an
implied assurance is not.

## Four failure modes to watch for

| | |
|---|---|
| **Admiration for the problem** | A finding with no treatment decision is half a finding |
| **The tidy grid** | No open cells means the pass stopped asking |
| **Findings that are really requirements** | *"The system should log exports"* is a control. The threat is *"an export cannot be traced to a person"* |
| **Over-weighting the dramatic** | The rare severe case is not the design centre. Frequency and severity are separate axes |

---

# What's not solved yet

**The operator is usually also the participant.** One person both directs the agent and answers its
questions, representing the client's knowledge from prior conversations. That is a proxy with a
ceiling, and the two roles pull against each other – the person checking the agent's work is the same
person whose answers produced it. The artefact shape compensates rather than fixes it: the whole
output is built to be handed over with *tell us what we got wrong*.

**Running this with the client as the participant is not designed yet.** It would separate the two
roles properly. It also makes parallel sessions much harder, because the knowledge then sits with
someone whose time cannot be booked twice.

**The signals in *Speeding it up* are proposed, not validated.** The speed-up was declined early, on
the grounds that optimising against a sample of one is optimising against noise, and it has not been
revisited since. The four checks are a considered guess at what readiness looks like. Nobody has yet
run a pass that used them and then measured whether the faster cells held up.

**Length is a design constraint and this method does not meet it.** Recorded that way rather than
restated downwards.
