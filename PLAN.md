# Project plan — the handbook

**Status** plan — **binds the project, not the reader** · **Life** living · **Reader** George, and
anyone picking up a drafting session cold

> Working title: **Agentic Delivery Handbook**. The name is not settled. Written 2026-09-15.

---

## 1 · What we are making

A **reference handbook** for running a whole software engagement with agents — from first requirement
to shipped surface — documenting the setup as it actually stands.

Eight parts. One published page per part, each with stable section anchors, so a blog post or a
LinkedIn post can link one level down instead of re-explaining the machinery.

It is generalised out of a live client build. The client is never named.

## 2 · The claim

Every stage of the work produces an artefact that declares **who it is for, what binds, and how it is
proved done**.

That is the same move at eight different altitudes: a requirement with a fit criterion, a threat
finding with a treatment, a design part with a stated value, a plan leaf with a proof, a supervised
run with a gate.

**The agents run unattended because of that, not because the prompts are good.** That sentence is the
handbook's argument, and each part shows the move at one stage.

## 3 · Who it is for

Someone who already runs coding agents and has hit the ceiling — the work stalls on judgement,
design input and decisions, not on review capacity.

They are not looking for a prompt library. They are looking for what to write down, and where.

## 4 · What it is not

- **Not a repository to clone.** No starter kit, no template repo. Every part ends with *the smallest
  version that works*, so the reader builds their own.
- **Not a product pitch.** No services page, no call to action. If it sells anything it does so by
  being useful.
- **Not a tutorial.** It assumes the reader has run agents and has opinions.
- **Not the blog voice.** See §7.

## 5 · The eight parts

| # | Part | The mechanism it carries |
|---|---|---|
| 0 | [What this is](docs/parts/00-what-this-is.md) | The claim, the assumptions, what is deliberately out |
| 1 | [Framing the work](docs/parts/01-framing-the-work.md) | Testable requirements; exclusions written as deliberately as inclusions |
| 2 | [Designing the system](docs/parts/02-system-design.md) | Zones as bulkheads; decisions recorded once; workflows interrogated for failure |
| 3 | [Attacking it before building it](docs/parts/03-threat-modelling.md) | Two taxonomies over two different spines; one file per finding |
| 4 | [Designing the surfaces](docs/parts/04-design.md) | IA by interview; a value lives in exactly one place; the handover spec |
| 5 | [Planning the delivery](docs/parts/05-delivery-planning.md) | Two rungs; workflow chosen by what could prove it; the packet is the brief |
| 6 | [Supervising the run](docs/parts/06-supervision.md) | The per-slice supervisor; verification at source; escalation |
| 7 | [Keeping it honest](docs/parts/07-keeping-it-honest.md) | Retros; the review panel; enforcement beats advice |
| 8 | [The machine](docs/parts/08-the-machine.md) | The requirement first, then the box, the sessions, the network |

**Tooling is last on purpose.** The box is a consequence of needing to supervise several long-running
processes, not a starting choice. Leading with it would teach the wrong lesson.

## 6 · The per-part template

**Superseded for Part 3, 21 September 2026.** Part 3 is now a folder – a human-readable guide, an
agent prompt, and templates for every output file. The five-heading shape below described an
*explanation* of an approach; what is actually wanted is a *how-to guide* somebody can follow. The
other parts have not been converted yet. See `docs/parts/03-threat-modelling/` for the shape that
replaces it.

Every part, the same six headings, in this order. No part may add a seventh at the top level.

| Heading | What goes in it |
|---|---|
| **The problem** | What breaks without this. Concrete, from the build. |
| **The mechanism** | What is actually done. The artefacts, their shape, their reader. |
| **The rules that earned their place** | Each rule, and the failure behind it. A rule with no failure behind it does not go in. |
| **What it cost** | The measurement, dated — or *"not measured"* said plainly. Never an estimate dressed as a figure. |
| **The smallest version that works** | The 20% a reader can build this week without adopting any of the rest. |
| **What's not solved yet** | The gaps, the proxies, the principles still unmet. Named, not apologised for. |

*The smallest version that works* is the heading that makes the handbook reproducible without being a
repository to clone.

*What's not solved yet* is what keeps it honest. Added 21 September 2026. Every part carries one, so
work-in-progress is a property of each document rather than a disclaimer at the top of the site — and
so there is an obvious home for the things that would otherwise be quietly omitted.

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
committed; `.sanitise-denylist.example` shows the format. This is Part 7's own argument applied to
the handbook.

## 9 · Publishing

Own repository, public on GitHub, rendered with **MkDocs Material** to GitHub Pages.

Why not Ghost: the handbook is eight cross-linked documents with anchors, not a blog feed. Why not a
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
| 5 | Delivery planning | **Yes** — the plan model and workflow selection | extract | 2nd |
| 6 | Supervision | **Yes** — the supervisor playbook | extract | 3rd |
| 4 | Design | **Partly** — IA method and handover spec yes; the design-system step no | extract + write | 4th |
| 7 | Keeping it honest | **Partly** — retro rules and panel composition yes | extract + write | 5th |
| 0 | What this is | n/a — written last, once the parts exist | write | 6th |
| 1 | Framing the work | **No** — excellent outputs, no recorded method | write | 7th |
| 2 | System design | **No** — same | write | 8th |
| 8 | The machine | **Partly** — the devbox document; two terms unresolved | write | 9th |

**Parts 3, 5, 6 alone are a publishable handbook.** Ship in that state if the rest stalls.

## 11 · Open questions

| # | Question | Blocks |
|---|---|---|
| Q1 | The handbook's name and the repository's name | publishing |
| Q2 | "Coly" — the web interface over the session multiplexer? Transcription unresolved | Part 8 |
| Q3 | "Officialization" — visibility? observability? Transcription unresolved | Part 8 |
| Q4 | How the design system was actually produced from the IA. No method doc found | Part 4 |
| Q5 | How Parts 1 and 2 were actually run with agents. No method doc found | Parts 1, 2 |
| Q6 | What about the recent supervisor work is *not* already in the playbook §5a | Part 6 |
| Q7 | Diagrams — the source estate has almost none. Which parts need one? | all |

## 12 · After the handbook

Posts sit on top of it, and link into it.

The candidate post catalogue is not written down yet. It belongs in `notes/post-candidates.md` in
this repository, or in `my-voice`, once the handbook's parts are settled enough to link to.
