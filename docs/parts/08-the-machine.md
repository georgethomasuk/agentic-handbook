**Status** scaffold — nothing here is drafted · **Life** living · **Reader** anyone about to buy hardware before they know what they need it for

# 8 · The machine

> **Draft order: 9th, and last on purpose.** The box is a consequence of needing to supervise several
> long-running processes, not a starting choice. Leading a handbook with the hardware teaches the
> wrong lesson.

## The problem

A laptop cannot hold several long-running agent sessions overnight, and the tooling that can is not
obvious. The requirement is not compute — it is **survivability and visibility**: processes that
outlive the client, reachable from wherever you are, with enough of a view to know which one needs you.

## The mechanism

- A single dedicated remote machine, provisioned from configuration rather than by hand.
- A terminal multiplexer running as a system service, pinned by checksum, with a memory ceiling, so
  sessions survive disconnection.
- A private network over WireGuard with a hosted control plane, the machine tagged so it cannot be
  exposed publicly. Reachable from laptop, tablet and phone.
- Agents run without per-action permission prompts, which is what makes unattended running possible
  and is the reason containment is a machine-level question.

## The rules that earned their place

- **Write the requirement before the shopping list.** The machine was sized against measured
  concurrent session counts, not a guess.
- **The non-root user buys test fidelity, not containment.** Passwordless sudo plus docker group is
  root with two keystrokes. **The containment lever is not the account — it is what the box is allowed
  to hold.**
- **The figure that belongs in a document is the one on the invoice.** This document carried a wrong
  price and a wrong disk specification for weeks, and the correction is recorded at the line with its
  date rather than quietly restated. **The invoice has still not been read into it.**
- Record what was rejected and why, not only what was chosen.

## What it cost

The machine's specification, its actual monthly cost **from the invoice** — which has not yet been
read — and the measured session concurrency it was sized against: median, ninetieth percentile and
peak. Re-read all of it. Do not publish the corrected-but-unverified price.

## The smallest version that works

Any always-on machine you can reach privately, running a multiplexer as a service. The specification
matters far less than the fact that the session does not die when you close the laptop.

## What's not solved yet

[the gaps, the proxies, the principles still unmet]

---

<!-- DRAFTING ONLY -->

## Source material

- `redmoor_infra/docs/devbox.md` — the specification, the sizing evidence, the containment argument,
  the rejected alternatives, and the price correction.
- `redmoor_infra/ansible/group_vars/devbox.yml` — the multiplexer version and pinning, the service
  definition, the memory ceiling, the network configuration.
- `redmoor_docs/deep_dives/20260815_CI_Cost_And_Remote_Development.md` — the research behind it.

## Open

- **Q2** — "Coly". A web interface over the multiplexer? Searched both estates and found nothing.
  Transcription unresolved; will not be written until George confirms the name.
- **Q3** — "Officialization". Read as visibility or observability. Unresolved.
- The tooling journey before this — the desktop app, the other harness — is story, and may belong in
  a post rather than here.

<!-- END DRAFTING ONLY -->
