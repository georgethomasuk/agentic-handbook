# Adjacent findings – real, actionable, not threats

> The pass will surface things that are worth acting on and are **not threats.** A contract clause
> that does not cover a task that will certainly happen. A document describing an architecture the
> design has moved away from. A scope decision nobody has taken.
>
> Forcing these into the findings register corrupts it – a reader is entitled to assume every `F-`
> line describes a way the system can harm someone or be harmed. Dropping them loses work the pass
> paid for. So they land here, as `ADJ-n`, a separate series.

## What belongs here

| | |
|---|---|
| **Contract and scope** | A task the work requires that the agreements do not cleanly authorise |
| **Document drift** | Two documents describing the same thing differently, where one is stale |
| **Spec gaps** | A design decision the pass assumed was made, and finds was not |

**What does not belong here.** Anything describing a way the system can harm someone or be harmed.
That is a finding, however awkward its category.

## How these resolve

Not by being fixed here. **Each entry names where it goes to die** – a document to amend, a decision
to take, a conversation to have. An entry with no route out is not finished.

---

## ADJ-1 · <title>

*Raised* \<date\>, \<cell\> · *Status* open · *Route out* \<the specific thing that closes this\>

**What happens.** \<the situation, plainly\>

**Why it is a question.** \<what is ambiguous or missing, with references\>

**Why it matters.** \<the consequence of leaving it\>

**Options, recorded rather than decided.**

| | |
|---|---|
| \<option\> | \<what it costs\> |
| **\<recommended option\>** | *Recommended.* \<why\> |
