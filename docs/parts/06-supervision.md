**Status** scaffold — nothing here is drafted · **Life** living · **Reader** anyone who wants work to continue while they are asleep

# 6 · Supervising the run

> **Draft order: 3rd.** Documented in full. Extraction-and-editing job.

## The problem

Unattended does not mean unsupervised. Several agents working in parallel will collide, will report
success they cannot prove, and will stall silently on a decision that is not theirs to make.

## The mechanism

A **long-lived supervisor process, one per slice**, acting as a delivery manager. It writes the
packets, dispatches agents into their own worktrees, verifies at source, holds the collision map,
and routes decisions back to the owner.

The owner has a direct channel and interacts with the session running each packet.

## The rules that earned their place

- **The supervisor is the party who checks at source.** A report of success is not success.
- **Verification is a balance, not a rule.**
- **Dispatch through the tree's own commands, never a hand-authored brief.**
- **Name every agent, and make them message back.**
- **Silence is assent, once a deadline has been named and passed** — bounded three ways: the subject
  line must say a decision is being asked for; asking twice is not a window; and the deadline does not
  start until receipt is acknowledged.
- **The ledger is state, not story.**
- **A gate is cleared in words.** A relayed approval is not the exception where the gate exists
  because a human looked.
- **A relayed observation carries its observer, or it is not a finding.**
- **Do not touch their branch.**

## What it cost

Countable and needing re-reading: how long a slice runs unattended before it needs the owner, and
what fraction of escalations were genuine decisions versus avoidable.

Much of this is likely **not measured**. Say so.

## The smallest version that works

One process whose only job is to check other agents' claims against the source, and a written rule
about what it is allowed to decide on your behalf.

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

- **Q6** — what about the recent supervisor work is not already in the playbook. George flagged that
  the newest behaviour is not captured; the playbook appears to cover the owner channel. Needs an
  answer before drafting.
- Whether the fleet loop is a Part 6 mechanism or a Part 7 one.

<!-- END DRAFTING ONLY -->
