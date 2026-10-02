**Status** template – in draft · **Life** living · **Reader** you, setting up

# Templates

Copy both into the client repository, beside the plan. [The guide](../README.md) says what to do with
each. With [the kit](../kit.md), `plan init` copies the workflows for you, and the brief skeleton is
not needed.

| | What it is | State |
|---|---|---|
| [`workflows/`](./workflows/README.md) | The columns a feature moves through, from claimed to closed. The shared core, seven workflows and the slots file | Draft |
| [`brief.md`](./brief.md) | The skeleton of the brief a fresh session is handed for one feature. The ask first, the context after | Draft |

**The resulting layout:**

```
plan/
  values.yaml             your values for the slots
  kit.yaml                with the kit only – where things are, and how a claim lands
  workflows/
    core.yaml
    <workflow>.yaml       seven of them
    slots.yaml            what each slot needs – not edited
    resolved/
      <workflow>.yaml     by hand only – one per workflow you use, what the agent reads
  brief.md                by hand only
.work/
  <feature>/
    journal.md            working state – ignored by version control
    brief.md              the assembled brief for that feature
```

**Ignore `.work/` in version control.** The journal and the brief are working state for one feature.
The record that outlives them is written into the feature's own file at the `record` column.
