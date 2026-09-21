# agentic-handbook

The **Agentic Delivery Handbook** — a reference handbook on running a whole software engagement with
agents. Public artefact. Read [`PLAN.md`](./PLAN.md) before doing anything in here.

This is a **writing** repository. No build, no tests. The only tooling is MkDocs for the published
site.

## Hard rules

**Read `PLAN.md` in full before drafting.** It carries the claim, the part template, the extraction
rules and the open questions. Do not invent a structure.

**Never name the client, their end client, or their sector.** Generalise to the shape of the thing,
never to mush. If a detail cannot be generalised without losing its point, ask — do not publish it
and do not quietly drop it.

**Never publish a number that has not been re-read from source in the current session.** Several
source documents warn that a stale measurement reads as current. Cite what you read, and date it.

**Say "not measured" when it is not measured.** Do not estimate, round, or infer a figure. An
admitted gap is worth more than a plausible number.

**A rule only goes in "the rules that earned their place" if there is a real failure behind it.**
Name the failure at the line. A rule invented for tidiness is the thing this handbook argues against.

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
**Status** normative | index | note — what binds · **Life** living | closed · **Reader** who this is for
```

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
docs/parts/      The eight parts. One published page each.
notes/           Working notes, extraction scratch, post candidates. Gitignored — local only.
mkdocs.yml       Site config.
```

`notes/` is **gitignored and local only**. It holds unsanitised extraction scratch, so it must never
be committed — the publish gate does not scan it. Nothing in it is published or written to the register.
