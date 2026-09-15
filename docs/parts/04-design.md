**Status** scaffold — nothing here is drafted · **Life** living · **Reader** anyone whose agents build surfaces that are nearly right

# 4 · Designing the surfaces

> **Draft order: 4th.** The IA method and the handover spec are documented in full. **How the design
> system was produced from the IA is not recorded** — that step is written from George's own account.

## The problem

New product development is not a software factory. The work needs real design input, and an agent
handed a picture will build something that looks close and is wrong in six places at once — because
nobody stated which parts of the picture bind.

Worse: the same control gets built three times, privately, slightly differently, because no document
named it as one part.

## The mechanism

**The chain.** Each link answers one question and no link may answer another's:

```
spec/            WHAT the system must do
  ↓
ux/              WHERE it goes                 information architecture
  ↓
design/          HOW it looks and behaves      handovers, per area
  ↓
adr/             WHICH WAY we build it
  ↓
design-tokens/   what every VALUE is
  ↓
*-ui/            the PARTS
  ↓
storybook/       what a part LOOKS LIKE        plus the tests that hold it
```

**Read downward to build, upward to argue.**

**The IA method** — an interview, not a one-shot draft. Ground in the real source material first;
bring the acceptance criteria in at the start rather than the end; sketch rough screens to react
against; write it plain; reconcile as you go, upward as well as across; keep a running open list,
which is the closing instrument.

**The handover spec** — a shape, not a style guide. It states at the top what binds and what is a
picture; every file declares its status, life and reader in the first five lines; identifiers are
stable and never renumbered; the inventory is of parts, not screens.

## The rules that earned their place

- **State, at the top, what binds and what is a picture.** Silence is what a reader cannot notice.
- **A value lives in exactly one place.** Where a name exists twice with different values, the
  computed value wins over the name.
- **Values are stated as text, never only drawn.** The tool that recovers values by reading computed
  styles exists only because handovers did not state them. A handover that passes its checks makes
  that tool unnecessary.
- **Content variants are not variants.** The inventory is of parts.
- **Stable IDs are never renumbered.** A parallel rebase shifted a register's rows, and roughly forty
  shipped code comments now cite numbers that moved. Cite by anchor, never a bare number.
- **A file past roughly 400 lines is doing two jobs.**
- **Ground before you sketch.** Ranks were invented once when the real roles were sitting in the
  source form.
- **Talk first, fork to close.** A structured either/or offered too early forecloses the owner's own
  framing. It is a closing tool, not an opening one.
- **Log model gaps and keep moving.** The UX decides the shape; the field follows later.
- **Flag silent divergence as a reconciliation.** Do not quietly change the spec by building past it.
- **An area that redirects already-shipped code is a different artefact from a from-nothing handover**,
  and says so at its own top, so nobody reads it as a second template.

## What it cost

The countable things: how many areas have been handed over and on what dates; how many times the
bordered control was independently rebuilt before the parts inventory existed; the console spec's
line count against the 400-line rule. Re-read each before publishing.

**What the design system cost to produce is not measured.**

## The smallest version that works

One page per surface that says what binds, one token file where every value lives once, and a rule
that a value stated in a picture and not in text does not exist.

---

<!-- DRAFTING ONLY -->

## Source material

- `platform/docs/ux/ia_method.md` — the loop, the habits, the anti-patterns.
- `platform/docs/ux/` — the area deep dives and the master map.
- `platform/docs/DESIGN.md` — the chain, the six places, and the landing note admitting fourteen of
  its own citations resolved to nothing for a month.
- `platform/docs/design/design-handover-spec.md` — the shape every handover is written against.
- `platform/docs/design/README.md` — the delivered areas, and the redirect exception.
- `platform/docs/design/console-*.md` — the flat files that predate the spec, and the rule that a
  second handover must not land beside them.
- `platform/packages/design-tokens/`, `*-ui/`, `storybook/`.
- `platform/tools/design-diff/` — the recovery tool, and why it should not need to exist.
- `redmoor_docs/prototypes/` — the working prototype the domain model came from.

## Open

- **Q4** — how the design system was actually produced from the IA. The only trace found is a plan
  leaf for the console design spec. Interview needed.
- Where the prototype sits in the chain. It is upstream of the spec, not downstream of the IA, and
  the chain diagram does not show it.
- **Q7** — this part needs the chain diagram at minimum.

<!-- END DRAFTING ONLY -->
