**Status** scaffold – nothing here is drafted · **Life** living · **Reader** you, about to turn a brief into testable requirements

# How to turn a brief into testable requirements

a requirement set with a fit criterion on every line, and exclusions written as deliberately as inclusions

The worked example throughout is [the example system](../../reference/example-system.md).

## What is in this folder

| | |
|---|---|
| **This guide** | What the process is, why it is shaped this way, and what good output looks like. Written for you |
| [**`prompt.md`**](./prompt.md) | The instruction set to paste into an agent session. Written for the agent |
| [**`templates/`**](./templates/README.md) | Skeletons for every file the process produces. Copy the directory |

**Read this once. Use the prompt every time.**

> **Draft order: 7th.** See `PLAN.md` section 10.

---

# Context

## What you are producing

[the artefact, and what it is for. If it is a document written to open a conversation rather than
close one, say so here]

## What you need before you start

| | |
|---|---|
| | |

## What it costs

[figures, dated, re-read from source. Or *"not measured"* said plainly]

## Who does what

| | | |
|---|---|---|
| **You** | the operator | |
| **The agent** | | |
| **The participant** | | |

## The shape of the work

[the sections, as a map, with what happens in each]

---

# 1 · Set up

## 1.1 · [step]

> **Agent** … · **You** …

[what to do]

**Worked example.**

[the actual thing, on the example system]

---

# 2 · [the process]

## 2.1 · [step]

> **Agent** … · **Participant** … · **You** …

---

# Evaluating the quality

**These are yours to run, on the agent's output.** Do not ask the agent whether its own work was good.

---

# What's not solved yet

[the gaps, the proxies, the principles still unmet]

---

<!-- DRAFTING ONLY -->

## Source material

- `platform/docs/spec/README.md` — the four-document chain and the work-package table.
- `platform/docs/spec/00_frame.md` — purpose, goals with testable success criteria, constraints,
  assumptions, exclusions.
- `platform/docs/spec/01_requirements.md` — the EARS register, functional then ISO 25010 non-functional.
- `platform/docs/spec/03_scope_acceptance.md` — the requirement → scope → acceptance-test chain.
- `platform/docs/adr/` — where the load-bearing decisions went instead of into the requirements.

Good worked examples to generalise: the requirement whose mechanism was withdrawn and replaced with
the obligation left intact; the discovery that an assumed integration did not exist, recorded at the
line with its date, after a watcher had been built against it and withdrawn.

## Open

- [what has to be decided before this can be drafted]

<!-- END DRAFTING ONLY -->
