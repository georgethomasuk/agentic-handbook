# Project plan — the handbook

**Status** plan — **binds the project, not the reader** · **Life** living · **Reader** George, and
anyone picking up a drafting session cold

> Working title: **Agentic Delivery Handbook**. The name is not settled. Written 2026-09-15.

---

## 1 · What we are making

A **reference handbook** for running a whole software engagement with agents — from first requirement
to shipped surface — documenting the setup as it actually stands.

Eight parts. **Each part is a folder, not a page** – a guide written for a person, a prompt written
for an agent, and templates for every file the process produces. Stable section anchors throughout, so
a blog post can link one level down instead of re-explaining the machinery.

It is generalised out of a live client build. The client is never named.

## 2 · The claim

Every stage of the work produces an artefact that declares **who it is for, what binds, and how it is
proved done**.

That is the same move at each altitude: a requirement with a fit criterion, a threat
finding with a treatment, a design part with a stated value, a plan leaf with a proof, a supervised
run with a gate.

**The agents run unattended because of that, not because the prompts are good.** That sentence is the
handbook's argument, and each part shows the move at one stage.

## 3 · Who it is for

Someone who already runs coding agents and has hit the ceiling — the work stalls on judgement,
design input and decisions, not on review capacity.

They are not looking for a prompt library. They are looking for what to write down, and where.

## 4 · What it is not

- **Not a starter kit.** There is nothing to install and nothing that runs. The templates are empty
  skeletons of documents – copy them and fill them in, or read them and write your own. **Revised 21
  September 2026:** this said *"not a repository to clone"* until Part 3 was drafted, and shipping
  copyable templates and an agent prompt is a clone of sorts. The distinction that survives is that
  the reader still has to do the thinking; the templates only say where to put it.
- **Not a product pitch.** No services page, no call to action. If it sells anything it does so by
  being useful.
- **Not a tutorial.** It assumes the reader has run agents and has opinions.
- **Not the blog voice.** See §7.

## 5 · The nine parts

| # | Part | The mechanism it carries |
|---|---|---|
| 0 | [What this is](docs/parts/00-what-this-is.md) | The claim, the assumptions, what is deliberately out |
| 1 | [Framing the work](docs/parts/01-framing-the-work/) | Testable requirements; exclusions written as deliberately as inclusions |
| 2 | [Designing the system](docs/parts/02-system-design/) | Zones as bulkheads; decisions recorded once; workflows interrogated for failure |
| 3 | [Attacking it before building it](docs/parts/03-threat-modelling/) | Two taxonomies over two different spines; one file per finding |
| 4 | [Designing the surfaces](docs/parts/04-design/) | IA by interview; a value lives in exactly one place; the handover spec |
| 5 | [Planning the delivery](docs/parts/05-delivery-planning/) | Four levels, each judged by who says it is done; the packet is the brief; naming the workflow a feature will run |
| 6 | [Managing the delivery](docs/parts/06-delivery-management/) | A workflow is columns with an entry, outputs and an exit; chosen by what could prove the work; a shared core plus slots filled per engagement |
| 7 | [Supervising the run](docs/parts/07-supervision/) | Running a workflow: the supervisor per build step; the unattended stretch; verification at source; escalation |
| 8 | [Keeping it honest](docs/parts/08-keeping-it-honest/) | Retros; the review panel; enforcement beats advice |
| 9 | [The machine](docs/parts/09-the-machine/) | The requirement first, then the box, the sessions, the network |

**Tooling is last on purpose.** The box is a consequence of needing to supervise several long-running
processes, not a starting choice. Leading with it would teach the wrong lesson.

## 6 · The shape of a part

**Rewritten 21 September 2026, from drafting Part 3.** The previous version specified five headings
that argued for an approach – *the problem · the mechanism · the rules that earned their place · what
it cost*. That is an **explanation**. What is actually wanted is a **how-to guide** somebody can
follow without having lived through the engagement. Part 3 was drafted twice against the old template
before this became clear, and both drafts were unusable by a reader coming in cold.

### A part is a folder

| File | Reader | What it carries |
|---|---|---|
| `README.md` | **A person** | The process, why it is shaped that way, and what good output looks like |
| `prompt.md` | **An agent** | The instruction set to paste into a session. Imperative, no justification |
| `templates/` | **Copied** | An empty skeleton for every file the process produces |

`prompt.md` and `templates/` appear when a part has a procedure an agent runs. Part 0 has neither and
stays a single page.

**The split is by reader, and it is the point.** A document that tries to explain to a person and
instruct an agent at the same time does neither.

### The guide's structure

| Section | What goes in it |
|---|---|
| **Context** | What you are producing · what you need before you start · what it costs · **who does what** · the shape of the work |
| **Numbered sections** | The procedure, in order. Decimal step numbers – `2.3` reads as *third step of the second section* |
| **Speeding it up** | Only where a real speed-up exists, and always with the signal that says it is safe yet. Never part of the numbered procedure |
| **Evaluating the quality** | Checks the operator runs on the agent's output. Never questions to ask the agent |
| **What's not solved yet** | The gaps, the proxies, the principles still unmet. Named, not apologised for |

### Four rules the guides follow

**Name the actor in every instruction.** Three roles – **you** the operator, **the agent**, **the
participant** who holds the knowledge. Every numbered step opens with a line saying who does what.
Without this a guide slides between addressing the reader and describing the agent, and it is never
clear which.

**Every step carries a worked example**, on [the example system](docs/reference/example-system.md).
Not a restatement of the rule. The actual question asked, the actual answer, the actual output. A step
that cannot be shown working has not been understood well enough to publish.

**One example across the whole handbook.** The reader meets one system, not a different one per part,
so the parts can refer to each other's analysis.

**State the terms.** A term like *holding* or *trust boundary* is defined where it is first needed, in
one sentence. Stripping the vocabulary out is what made the first two Part 3 drafts unreadable.

### What replaced "the smallest version that works"

That heading made the handbook reproducible without shipping anything. The templates do that job
better, so it is gone as a required heading. Where a part has a genuinely smaller first version worth
naming, it belongs in Context, under *what you need before you start*.

## 7 · Register

**The handbook is not written in the blog voice.** `my-voice/personal/voice/VOICE.md` governs posts
and LinkedIn — writing aimed at referrers. It would flatten this.

The handbook is written in the register George already uses in his own repository documentation:
declarative, rule-and-reason, the failure stated at the line, dated corrections left visible rather
than quietly restated. See `CLAUDE.md` in this repository for the rules.

The split is deliberate: **the handbook carries the mechanism, the posts carry the story, and the
posts link into the handbook** so they never have to explain the machinery twice.

## 8 · Sourcing and confidentiality

Two source estates, both private:

- The client platform repository — the specification, ADRs, design handovers, the plan tree, the
  supervisor playbook, the review skills.
- The engagement record — the threat model, governance, delivery plans, deep dives, the UX record.

**This repository is public.** Assume every commit is permanent. The full confidentiality rules,
the generalisation table and the publish gate are in `CLAUDE.md` — read them before extracting
anything. In summary:

1. **Never name a client, their end client, their sector, or anything that identifies it.** Where a
   detail is load-bearing, generalise it to the shape (*"a public write endpoint feeding a reviewed
   inbox"*), not to mush. **George Thomas** and **Redmoor Labs** are the only names that appear.
2. **Never publish a figure that has not been re-read from source.** Several of the source documents
   carry their own warnings that a stale measurement reads as current.
3. **Say "not measured" when it is not measured.** Three of the source documents do this and it is
   the most credible thing in them.
4. **Redact the same way the engagement record already did** when it moved documents across the
   client boundary: remove commercial posture, keep the method.
5. **Nothing commercial.** No prices, day rates, scope caps, contract posture or sign-off dates.
6. **Private source paths live in `<!-- DRAFTING ONLY -->` blocks** at the foot of each part, and are
   stripped before publishing.

**Enforced, not advised.** `scripts/check-sanitised.sh` fails the build on a denylisted term or a
leaked path. The denylist is confidential, so it lives at `.sanitise-denylist`, gitignored and never
committed; `.sanitise-denylist.example` shows the format. This is Part 8's own argument applied to
the handbook.

## 9 · Publishing

Own repository, public on GitHub, rendered with **MkDocs Material** to GitHub Pages.

Each part is a folder whose `README.md` is its landing page, so the structure reads correctly both on
the site and when browsing the repository on GitHub.

Why not Ghost: the handbook is nine cross-linked documents with anchors, not a blog feed. Why not a
folder in `my-voice`: that repository is a private working record, and this artefact is meant to be
shared.

The markdown stays plain enough to read directly on GitHub, so the repository itself is a usable
surface even for someone who never opens the site.

## 10 · Status and sequencing

Draft the parts that already have a method document behind them. Those are extraction-and-editing
jobs. The rest are written from George's own account, with the artefacts as evidence.

| # | Part | Source method doc exists? | Effort | Order |
|---|---|---|---|---|
| 3 | Threat modelling | **Yes** — the walk playbook and the approach note | extract | 1st |
| 5 | Delivery planning | **Yes** — the plan model | extract · **drafted 2026-10-02** | 2nd |
| 6 | Delivery management | **Yes** — the workflow files and workflow selection | extract | 3rd |
| 7 | Supervision | **Yes** — the supervisor playbook | extract | 4th |
| 4 | Design | **Partly** — IA method and handover spec yes; the design-system step no | extract + write | 5th |
| 8 | Keeping it honest | **Partly** — retro rules and panel composition yes | extract + write | 6th |
| 0 | What this is | n/a — written last, once the parts exist | write | 7th |
| 1 | Framing the work | **No** — excellent outputs, no recorded method | write | 8th |
| 2 | System design | **No** — same | write | 9th |
| 9 | The machine | **Partly** — the devbox document; two terms unresolved | write | 10th |

**Parts 3, 5, 6, 7 alone are a publishable handbook.** Ship in that state if the rest stalls.

## 11 · Open questions

| # | Question | Blocks |
|---|---|---|
| Q1 | The handbook's name and the repository's name | publishing |
| Q2 | "Coly" — the web interface over the session multiplexer? Transcription unresolved | Part 9 |
| Q3 | "Officialization" — visibility? observability? Transcription unresolved | Part 9 |
| Q4 | How the design system was actually produced from the IA. No method doc found | Part 4 |
| Q5 | How Parts 1 and 2 were actually run with agents. No method doc found | Parts 1, 2 |
| Q6 | What about the recent supervisor work is *not* already in the playbook §5a | Part 7 |
| Q7 | Diagrams — the source estate has almost none. Which parts need one? | all |
| Q8 | Whether parts without an agent procedure (0, and possibly 1) stay single pages or become folders for consistency | structure |

### Decided

| Date | Decision | Affects |
|---|---|---|
| 2026-09-23 | **"Slice" means the plan level only** – an integrated capability you can demonstrate. The source also uses it for the cut of one feature's build that a subagent runs; the handbook calls that a **build step**. One word with two meanings three parts apart is unreadable, and renaming one term is cheaper | Parts 5, 6 |
| 2026-09-23 | **Part 5 plans; Part 6 runs.** Part 5 covers the plan levels, the packet, choosing a workflow, and what a workflow's columns carry. Part 6 covers running one – the unattended stretch, subagents per build step, the review panel, the journal, cost per column. The source is about 9,500 lines and one part cannot carry both | Parts 5, 6 |
| 2026-09-24 | **The workflow templates are layered, and reusable across engagements.** Each workflow is method text plus a shared core file plus a slots file; the handbook publishes method and slots with the tooling described, and George's private copy fills the tooling slots. Eight source workflows become six: build in the repository · build in a browser (styling units fold in as a mode) · component library · contract change · change only the real environment can prove · acceptance (runtime and browser acceptance merge). Dated incidents leave the `why:` lines for the guide; each `why:` keeps the failure's shape. **Extracting the tooling itself into a runnable kit is deferred**, a separate project | Part 5, and every part that ships templates |
| 2026-10-02 | **Nine parts, not eight: managing the delivery is its own part.** Part 5 is planning – the plan levels and the packet. The new Part 6 is delivery management – the workflows, choosing one, and filling the slots for an engagement. Supervising the run moves from 6 to 7, keeping it honest from 7 to 8, the machine from 8 to 9. Workflows are how delivery is managed, not how it is planned; planning is the packets. **The three rows above use the old numbers**: where they say Part 6 they mean supervision, now Part 7, and the workflow templates they place in Part 5 are now in Part 6 | Parts 5 to 9, every index |
| 2026-10-02 | **Seven workflow templates, not six.** The source gained a ninth workflow on 2026-09-26, after the six were decided: one bounded part built against a registry that already declares it. It is lighter than `component-library` and has two columns nothing else has, so it is published as `single-part` rather than folded in. **`build-plan` and `build-execute` moved into the shared core**, because four of the seven use the same text; a workflow adds to them with `also:`. Two modes: `treatment-only` (of `build-in-browser`) and `draft-contract` (of `contract-change`, **not yet run**) | Part 6 |
| 2026-10-02 | **The kit lives in this repository, under `kit/`.** The row of 2026-09-24 deferred it as a separate project; George's decision on 2026-10-02 was one repository holding everything. It is written fresh against the published templates, not copied from the source tooling. **Slot values move out of `slots.yaml` into `values.yaml`**, so the definitions can be replaced without losing an engagement's answers. The repository is no longer writing-only: `scripts/test-kit.sh` is a third gate, and the sanitise check now reads code as well as prose | Part 6, `CLAUDE.md`, the publish gate |
| 2026-10-02 | **One worked plan, in `kit/example/tree/`, used by Parts 5 and 6.** A full plan on the example system: one mission, four milestones, six slices, 24 features, with packets and records. It lives with the kit, not under `docs/`, because it is a plan in a plan's layout and the kit's tests load it. Each part's worked examples are quoted from it. **The kit enforces what Part 5 teaches**: `## Where to err` on every packet, and every milestone criterion answered by a feature that builds it. `plan view` prints the census. The build order in file names, link checking and citation checking are in the source and not in the kit; Part 5 says so | Parts 5, 6, the kit |

## 12 · After the handbook

Posts sit on top of it, and link into it.

The candidate post catalogue is not written down yet. It belongs in `notes/post-candidates.md` in
this repository, or in `my-voice`, once the handbook's parts are settled enough to link to.
