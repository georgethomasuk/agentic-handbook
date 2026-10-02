**Status** template – copy into your own repository and fill the slots · **Life** living · **Reader** you, setting up the workflows for an engagement

# Workflow templates

A **workflow** is the fixed sequence of columns one feature moves through, from claimed to closed. Each
column says what it needs on entry, what it produces, and what ends it. The agent works one column at a
time and stops where the column says to stop.

These files are the method with everything client-specific taken out. What was taken out left a named
hole – a **slot** – which you fill once per engagement, or once for yourself.

## The files

| File | What it is | Who edits it |
|---|---|---|
| [`core.yaml`](./core.yaml) | The columns and rules every workflow shares – claim, cut the build, run the build steps, review panel, pull request, record, merge, close – and the protocols for entering a column, reporting back, compacting and sending work to a worker | Nobody. Copy as is |
| The seven workflow files, listed under [Choosing a workflow](#choosing-a-workflow) | One workflow each. A workflow writes its own distinctive columns and pulls the rest from the core | Nobody. Copy as is |
| [`slots.yaml`](./slots.yaml) | Every hole in the files above, with what it needs, how to do it by hand, and an example | You – `project.*` once per engagement, `tooling.*` once for yourself |

**The core exists because the shared columns were duplicated.** In the workflows these were extracted
from, the claim, panel, pull request, record and close columns were repeated in every workflow file.
Each repetition is one more place a fix has to be made. One copy is one place.

**How a workflow uses the core.** Three keys do all of it.

| Key | What it does | Example |
|---|---|---|
| `use: core.<name>` | Runs the shared column, unchanged | `use: core.open` |
| `also:` | Appends to the shared column. Shaped like the column: `also: {entry: …, exit: […]}` | The contract workflow adds a coexistence gate to `core.build-plan` |
| `as: <name>` | Runs the shared column under another name | The contract workflow runs `core.panel` twice, as `proposal-review` and `implementation-review` |

A workflow may also end with **`modes:`** – a lighter or narrower variant, stated as what it changes
column by column. Everything a mode does not mention is unchanged.

## The two kinds of slot

**`{{project.*}}` belongs to the engagement.** The stack, the data rules, the trust boundaries, the list
of decisions an unattended run must hand back. It lives in the client's repository, because the client's
reviewers need to read it.

**`{{tooling.*}}` belongs to you.** How you claim work, where the journal goes, how you run a review
panel. It travels with you from one engagement to the next.

**Keep them apart.** A workflow where the two were written together could not be moved to a second
client without reading every line to find out which was which. That reading is what these templates
were extracted to save.

**Every slot has a by-hand filling.** You can run these workflows with no tooling at all: a markdown
journal, a code host, and fresh sessions for the panel. Tooling makes a column cheaper. It never makes a
column possible.

## Choosing a workflow

Choose by **where the truth of the work lives** – what has to run for the change to be proved.

| The change is proved by | Workflow | Distinctive columns |
|---|---|---|
| Tests, and running it locally against a real system | [`build-in-repository`](./build-in-repository.yaml) | `frame` · `prove` |
| A browser over the built surface, and a person judging it | [`build-in-browser`](./build-in-browser.yaml) | `recon` · `user-review` · `browser-sweep` |
| Each part measured against a design reference until nothing differs | [`component-library`](./component-library.yaml) | `survey` · `behaviour` · `decompose` · `measure` · `compose` |
| A registry's own check, for one part it already declares | [`single-part`](./single-part.yaml) | `frame` in a live scratch page · `behaviour` after the build |
| Every producer and consumer of an interface agreeing | [`contract-change`](./contract-change.yaml) | `impact-map` · two panels |
| Only the real environment – an access grant, a network rule | [`real-environment-change`](./real-environment-change.yaml) | panel before apply · `prove` one apply at a time |
| Running the deployed thing and reading the effect back | [`acceptance`](./acceptance.yaml) | `prepare` a matrix · `deploy` · `result-review` |

**Two modes.**

| Mode | Of | Use it when |
|---|---|---|
| `treatment-only` | `build-in-browser` | The parts exist and only how they look moves |
| `draft-contract` | `contract-change` | Nothing is released, stored or deployed under the contract. **Not yet run** – see the file |

**All seven share one spine.** Verify the inputs, claim the work, agree a design with a person, build,
prove, review with a panel, write the record, merge, release the claim. What differs is the middle:
what "prove" has to mean for that kind of work.

## Setting up

**You** do this once per engagement, before the first feature is claimed. [The guide](../../README.md)
walks each step with a worked example; this is the short form.

1. Copy this folder into the client repository, next to the plan.
2. Add a `value:` to every `project.*` slot the first workflow uses. Use the `by_hand` line where the
   engagement has no tooling for it yet.
3. Read the stop list and the decide-and-disclose list aloud to the client's lead. These two lists
   decide what an unattended run may do without asking. They are the slots most worth disagreeing
   about early.
4. Add a `value:` to every `tooling.*` slot from your own copy. If you have none, use the `by_hand`
   lines.
5. Check that every command slot fails when it cannot run. Point it at a missing file and read the exit
   status.
6. Resolve each workflow you will use into one flat file – the core, the workflow and the slots joined,
   with no `use:` and no placeholder left. The agent works from that file, never from these.

**Step 5 exists because a check that skips reads as a pass.** An archive step that exits cleanly having
copied nothing leaves you believing there is an archive – and `close` releases the working copy, where
the journal lives, straight after it.

## Worked example

On the example system, the feature is **a rate limit on the public check-in endpoint (B3)**. The
endpoint is reachable by anyone with the link, and the collection window cannot be repeated.

**Choosing.** It is proved by tests and by firing requests at a local system. Nothing needs a deployed
environment. So: `build-in-repository`.

**At `check`**, the agent reports one piece of packet drift: *"The packet names the check-in view in
`checkin/views.py`. It moved to `checkin/api.py` when the anonymous token was split out. Designing
against the new location."* You confirm at the gate.

**At `frame`**, the agent's research finds the rate-limiting library it would have used keys on client
address by default. It brings back what it found against that: staff on one site's wifi share one outbound
address, so one busy site throttles everyone on it. The agreed design keys on the
check-in token instead, and names the library and its version from the lockfile.

**At `build-plan`**, the cut is three build steps:

| Step | Makes true | Tier | Closes |
|---|---|---|---|
| 1 | Requests over the limit, per token, get a refusal the check-in screen can show | mid | criterion 1 |
| 2 | A refused request writes nothing to H1, and no check-in content to the logs (H6) | top – touches B3, which is on `sensitive_boundaries` | criterion 2 |
| 3 | The limit is set in configuration, not in code | mid | criterion 3 |

The fixture line reads: *"Stands in for check-ins across all sites during the window. Omits: many
phones behind one site's address, which is the case that broke the default key."*

**At `prove`**, the agent opens with *"Application behaviour – exercised against the local system."* It
fires requests past the limit from two tokens behind one address, then reads the store and the log
back. It does not stop at the response codes.

## Adding a workflow

Add a new workflow file only when the truth of the work lives somewhere none of the existing ones
reach. Pull every shared column from the core with `use:`. Add to it with `also:` or `seeds:`, and
never restate it. Give every exit a `why:` that names the failure it prevents. An exit
nobody can name a failure for is tidiness, and it costs every future run.
