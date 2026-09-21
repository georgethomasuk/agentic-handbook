**Status** scaffold – nothing here is drafted · **Life** living · **Reader** you, about to supervise an agent run

# How to supervise an agent run

a per-slice supervisor, verification taken at source rather than reported, and an escalation route that reaches a person

The worked example throughout is [the example system](../../reference/example-system.md).

## What is in this folder

| | |
|---|---|
| **This guide** | What the process is, why it is shaped this way, and what good output looks like. Written for you |
| [**`prompt.md`**](./prompt.md) | The instruction set to paste into an agent session. Written for the agent |
| [**`templates/`**](./templates/) | Skeletons for every file the process produces. Copy the directory |

**Read this once. Use the prompt every time.**

> **Draft order: 3rd.** See `PLAN.md` section 10.

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

- `platform/docs/supervisor-playbook.md` — all nine sections. Written 2026-08-27, direct owner
  channel added the following day.
- `platform/plan/workflows/*.yaml` — where a workflow declares the point from which it runs unattended.
- `platform/tools/fleet/` — the adjacent pattern: parallel resolvers in their own worktrees, each
  checked by a reviewer, with **a shell script and not a model holding the loop**. Decide whether this
  belongs here or in Part 7.

## Open

- [what has to be decided before this can be drafted]

<!-- END DRAFTING ONLY -->
