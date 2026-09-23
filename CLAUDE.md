# agentic-handbook

The **Agentic Delivery Handbook** — a reference handbook on running a whole software engagement with
agents. Public artefact. Read [`PLAN.md`](./PLAN.md) before doing anything in here.

This is a **writing** repository. No build, no tests. The only tooling is MkDocs for the published
site.

## Hard rules

**Read `PLAN.md` in full before drafting.** It carries the claim, the shape of a part, the extraction
rules and the open questions. Do not invent a structure.

**A part is a how-to guide, not an explanation of an approach.** The reader is doing the task, not
trying to understand your reasoning. Do not write a document that argues for the method – write one
somebody can follow without having lived through the engagement.

**Never name the client, their end client, or their sector.** Generalise to the shape of the thing,
never to mush. If a detail cannot be generalised without losing its point, ask — do not publish it
and do not quietly drop it.

**Never publish a number that has not been re-read from source in the current session.** Several
source documents warn that a stale measurement reads as current. Cite what you read, and date it.

**Say "not measured" when it is not measured.** Do not estimate, round, or infer a figure. An
admitted gap is worth more than a plausible number.

**A rule only goes in a guide if there is a real failure behind it.** Name the failure at the line. A
rule invented for tidiness is the thing this handbook argues against.

**Name the actor in every instruction.** Three roles: **you** the operator, **the agent**, and **the
participant** who holds the knowledge. Never write an instruction where it is unclear which one acts.
A guide that slides between addressing the reader and describing the agent is unusable, and it is the
single failure mode that has cost the most drafting time here.

**Every step carries a worked example**, on the example system in `docs/reference/example-system.md`.
The actual question, the actual answer, the actual output – not a restatement of the rule. A step that
cannot be shown working has not been understood well enough to publish.

**Do not strip the vocabulary.** Define a term where it is first needed, in one sentence, and give the
reference material a home rather than removing it. Two Part 3 drafts were unreadable because the
taxonomies were generalised away and nothing replaced them.

**Do not apply `my-voice/personal/voice/VOICE.md` here.** That constitution governs George's
referrer-facing posts. This is a different genre with a different reader. See §Register below.

## Register

Write like George's own repository documentation, because that is what this is extracted from and it
is already good in this genre.

- Declarative. The claim first, then what earns it.
- One idea per paragraph. Short sentences.
- **Rule-and-reason.** Never state a rule without the failure that produced it.
- Corrections stay visible and dated — "said X until 2026-08-19; the figure that belongs here is on
  the invoice, which has not been read into this document yet". Do not quietly restate.
- Tables for anything with more than three parallel cases.
- Second person is allowed for the reader ("you will hit this at about the third slice"). First
  person plural is not — there is no "we".
- No hedging stacks. No "it depends". No throat-clearing openers.
- Spaced en dash ( – ) or a full stop. Not em dashes.

## Every file declares itself

First five lines of every document under `docs/`, before the H1:

```
**Status** scaffold | draft | reference | template | index – how far it has got · **Life** living | closed · **Reader** who this is for
```

The values are defined for readers in the glossary on `docs/reference/example-system.md`. Change them
there too if they change here. Said `normative | index | note` until 2026-09-23, which no page used.

This is the same convention the source estate uses. It is also, conveniently, a demonstration of the
handbook's own claim.

## Confidentiality — this repository is public

Assume every commit is public and permanent. A client name pushed once and reverted is still in the
history and still in anyone's fork.

**Never appears, anywhere, including commit messages and file paths:**

- Any client's name, trading name, or abbreviation. Any client's **end client**.
- The **sector or domain** of a client's work, or any detail that identifies it — a country, a
  programme, a named capability, a regulator, a specific cohort of people.
- Product names, internal service names, repository names, account identifiers, hostnames, or URLs
  belonging to a client estate.
- Anything commercial: prices, day rates, contract posture, scope caps, sign-off dates, statements
  of work.
- Anything about a named individual, on any side.

**Generalise to the shape, never to mush.** A worked example keeps its teeth if you keep the
mechanism and drop the subject:

| Do not write | Write |
|---|---|
| a named client's polling platform | a platform with a public write endpoint feeding a reviewed inbox |
| a named end client's training mission | the organisation the reports are produced for |
| the named form product they migrated off | the spreadsheet-and-forms process it replaced |
| war-crimes testimony | a data holding where non-repudiation is catastrophic |

If a detail cannot be generalised without losing its point, **ask** — do not publish it and do not
quietly drop it.

**Who may be named:** **George Thomas**, and **Redmoor Labs** (Redmoor Labs Ltd). Both are the
author. Nobody else.

**Source paths are private.** The `## Source material` block at the foot of each part cites private
repositories. It is drafting scaffolding and is stripped before publishing — see below.

## The publish gate

Advice does not hold. This repository enforces its own rule, which is also Part 7's argument.

```
scripts/check-sanitised.sh
```

It fails if a published file contains a denylisted term or a drafting-only block. Run it before any
push and before any site build.

**And build the site before pushing:**

```
scripts/build-site.sh
```

The publish workflow runs MkDocs in **strict mode**, so a link to a file that is not in `docs/` fails
the build rather than warning. That has already broken `main` once – a part was converted to a folder
and `index.md` still linked the old page. The script creates `.venv` on first run and then builds the
same way the workflow does.

**The denylist cannot live in a public repository**, because the denylist *is* the confidential list.
It lives at `.sanitise-denylist` in the working copy, is gitignored, and is never committed. The
repository ships `.sanitise-denylist.example` showing the format only.

Drafting scaffolding is wrapped so the check can find it:

```
<!-- DRAFTING ONLY -->
... source pointers, private paths, working notes ...
<!-- END DRAFTING ONLY -->
```

## Layout

```
PLAN.md          The project plan. The thing to read first.
docs/parts/      The eight parts. One folder each.
docs/reference/  The example system, used by every part.
notes/           Working notes, extraction scratch, post candidates. Gitignored – local only.
mkdocs.yml       Site config.
```

**Each part is a folder, split by reader:**

```
docs/parts/NN-name/
  README.md      the guide — written for a person
  prompt.md      the instruction set to paste into a session — written for an agent
  templates/     empty skeletons for every file the process produces — to copy
```

`prompt.md` and `templates/` exist where a part has a procedure an agent runs. Part 0 has neither.

**Never write one document that both explains to a person and instructs an agent.** It does neither.
That split is the structure, not a convenience.

`notes/` is **gitignored and local only**. It holds unsanitised extraction scratch, so it must never
be committed — the publish gate does not scan it. Nothing in it is published or written to the register.
