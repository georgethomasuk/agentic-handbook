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

## Glossary

Every term the handbook uses in a special sense. Each part also defines a term where it first needs it.

### The three roles

| Term | Meaning |
|---|---|
| **You** · the operator | The person running the agent sessions. You direct the work and make the calls the agent cannot |
| **The agent** | The coding agent in a session. It starts knowing nothing about the system that is not in the files |
| **The participant** | The person who holds the business knowledge and answers the agent's questions. Often also you |

### Threat modelling – Part 3

| Term | Meaning |
|---|---|
| **Trust boundary** | A place where data moves between two parties who trust each other differently. Numbered B1, B2, … |
| **Holding** | One place personal data comes to rest, treated as a single thing for analysis. Numbered H1, H2, … |
| **Element** | Either a trust boundary or a holding – whichever the current pass is walking |
| **Spine** | The list of elements a pass walks. The security pass walks the boundaries; the privacy pass walks the holdings |
| **Taxonomy** | The fixed list of questions a pass asks. STRIDE for security, LINDDUN GO for privacy |
| **Category** | One question in STRIDE, such as Repudiation |
| **Suit** | One question in LINDDUN GO, such as Detecting. LINDDUN GO is published as a deck of cards, hence the name |
| **Cell** | One category or suit asked at one element. Repudiation at B2 is one cell |
| **Mark** | The result recorded for a cell: `✅` a finding, `➖` closed with a reason, `⚠️` open and waiting on someone |
| **Finding** | A way the system can harm someone or be harmed, written up with a treatment. Numbered F-1, F-2, … |
| **Adjacent finding** | Something real and actionable that is not a threat – a contract gap, a stale document. Numbered ADJ-1, ADJ-2, … |
| **Treatment** | What is decided about a finding: mitigate, accept, share, investigate, or refine the specification |
| **Residual** | What is still true about a finding after its treatment is carried out |
| **Fork test** | Split a holding only when one question gets opposite answers for different records in it |
| **Register** | The one-line-per-finding list in the workbook |
| **Workbook** | The formal record of a threat-modelling pass. Written to be checked, not read through |
| **Front door** | The short document the client reads first. It points into the workbook rather than repeating it |

### The status line

Every page opens with a line such as **Status** draft · **Life** living · **Reader** you.

| Field | Meaning |
|---|---|
| **Status** | How far the page has got – *scaffold* (not written), *draft*, *reference*, *template*, *index* |
| **Life** | *Living* means it will still change. *Closed* means it will not |
| **Reader** | Who the page is written for – you, or an agent
