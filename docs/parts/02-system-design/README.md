**Status** scaffold – not yet written · **Life** living · **Reader** you, about to design the system and record the decisions

# How to design the system and record the decisions

> **Not yet written.** This part is an outline. The finished part is
> [Part 3, threat modelling](../03-threat-modelling/README.md) – start there.

an architecture description, the zones and their boundaries, and one recorded decision per choice that was genuinely open

The worked example throughout is [the example system](../../reference/example-system.md).

## What is in this folder

| | |
|---|---|
| **This guide** | What the process is, why it is shaped this way, and what good output looks like. Written for you |
| [**`prompt.md`**](./prompt.md) | The instruction set to paste into an agent session. Written for the agent |
| [**`templates/`**](./templates/README.md) | Skeletons for every file the process produces. Copy the directory |

**Read this once. Use the prompt every time.**

> **Draft order: 8th.** See `PLAN.md` section 10.

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

- `platform/docs/spec/02_solution_design/` — `00_overview`, `01_building_blocks`, three zone
  documents, `05_crosscutting`, `05a_data_model`, `06_runtime`, `07_deployment`.
- `platform/docs/spec/04_workflows/` — fourteen workflows, each interrogated.
- `platform/docs/adr/` — the decision series.
- `platform/docs/architecture/` — zone crossings, drift detection, observability, CI verification
  identity, zone runtime.
- `redmoor_docs/deep_dives/` — ten dated research notes. The README line *"Not decisions — those
  graduate to ADRs"* is the rule worth lifting.
- `redmoor_docs/README.md` — the specification move, and the reason for it.

## Open

- [what has to be decided before this can be drafted]

<!-- END DRAFTING ONLY -->
