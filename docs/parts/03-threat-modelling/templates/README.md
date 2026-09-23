**Status** templates – copy these into your own repository · **Life** living · **Reader** you, setting up a pass

# Templates

Copy this whole directory into your threat-model folder and fill it in. The structure matters more
than the wording – it is what lets several agent sessions work at once without colliding.

| File | What it is |
|---|---|
| [`front_door.md`](./front_door.md) | The short document the client reads first. Written last |
| [`workbook.md`](./workbook.md) | The formal record. System, scope, method, synthesis. §6.1 is the findings register |
| [`annex_a_grids.md`](./annex_a_grids.md) | The coverage record. One small table per category |
| [`annex_b_findings.md`](./annex_b_findings.md) | The findings index. One row per finding |
| [`finding.md`](./finding.md) | One finding. Copy per finding into `annex_b/` |
| [`adjacent_findings.md`](./adjacent_findings.md) | Real, actionable, not threats. A separate series |

**The resulting layout:**

```
threat_model/
  front_door.md
  workbook.md
  annex_a_grids.md
  annex_b_findings.md
  annex_b/
    F-001-<slug>.md
    F-002-<slug>.md
  adjacent_findings.md
  sources/              raw transcripts – gitignore this
```

**Gitignore `sources/`.** Elicitation transcripts contain candid commercial and liability content
that should not be in a tracked tree.
