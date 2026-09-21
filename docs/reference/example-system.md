**Status** reference – the worked example used throughout · **Life** living · **Reader** anyone reading any part of the handbook

# The example system

Every part of this handbook works against the same example. You meet one system rather than a
different one per chapter, and the parts can refer to each other's analysis.

It is a stand-in. It carries the **structure** of real engagements and none of their content.

## The system

**An internal safety and wellbeing platform for a multi-site employer.**

Supervisors file incident reports from managed devices at each site. Reports are sometimes written in
a language other than the company's working language, so they are machine-translated on the way in.

Separately, once a year for a two-week window, all staff are invited to complete an anonymous
wellbeing check-in on their own phones.

The company's insurer reads a dashboard of aggregate safety and wellbeing trends, broken down by site.

A small internal safety team administers the whole thing. An external supplier builds it.

## Trust boundaries

A **trust boundary** is a place where data moves between two parties who trust each other differently.
It is where security problems cluster, because each side is relying on assumptions the other side has
not promised to keep.

| | Boundary |
|---|---|
| **B1** | Report content leaving the core store |
| **B2** | The insurer logging in to the dashboard |
| **B3** | The public check-in endpoint |
| **B4** | Handover from the supplier to the company |
| **B5** | The infrastructure underneath |
| **B6** | The supplier's own handling during the build |
| **B7** | The company's own handling |

## Data holdings

A **holding** is one place personal data sits, treated as a single thing for analysis. Not a database
table and not a server – a body of records about people that can be reasoned about as a unit.

The distinction matters because privacy harms attach to a record about a person, not to a line on an
architecture diagram.

| | Holding | What is in it |
|---|---|---|
| **H1** | Canonical record store | Reports and check-ins converge here. Sensitivity is a property of a field, not of the store |
| **H2** | Aggregate store | What the insurer reads. Small sites make small cells |
| **H3a** | Incident report · managed device | Named, attributable, used in disciplinary and injury claims |
| **H3b** | Wellbeing check-in · personal phone | Anonymous by design, self-selected reference |
| **H4** | The supplier's own processing | Live data on a development machine during the build |
| **H5** | The company's own handling | Exports to spreadsheets, board packs |
| **H6** | Operational exhaust | Logs, dead-letter queue, transient stores. Purged at 30 days while H1 is kept |

## Why these properties are here

Each one exists because some part of the handbook needs it. They are not decoration.

| Property | What needs it |
|---|---|
| A public write endpoint anyone with the link can reach | Boundary analysis; denial of service |
| **Two intakes that fork on attribution** | **The fork test**, [Part 3](../parts/03-threat-modelling/README.md) |
| A store where both intakes converge | Sensitivity as a field property |
| Aggregates read by a different organisation | Re-identification in small groups; the read-logging trade-off |
| A supplier holding live data during the build | The development-machine problem |
| Client handling beyond the platform edge | Exports, where controls stop following the data |
| Exhaust with its own retention answer | The second fork-test case |
| A collection window that cannot be repeated | Denial of service against an unrepeatable event |
| A team too small for separation of duties | Attribution resting on a log alone |
| A third party processing free text | An undeclared position rather than a missing control |

## How it is used

**It carries shape, never substance.** Where a part quotes a figure, that figure is real and comes
from work actually done. The example illustrates how the method behaves; it never supplies evidence
that it worked.
