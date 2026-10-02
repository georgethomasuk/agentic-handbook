**Status** template – in draft · **Life** living · **Reader** you, setting up a plan

# Templates

Two skeletons. Every node in a plan is one or the other. [The guide](../README.md) says how to fill
each.

| | What it is | Saved as |
|---|---|---|
| [`container.md`](./container.md) | A mission, a milestone or a slice. Goal, done-when, boundaries | `README.md` in a folder named for the level |
| [`feature.md`](./feature.md) | One feature. The packet above the line, the record below it | `feature_<name>.md` |

**The resulting layout:**

```
plan/
  tree/
    mission_<name>/
      README.md
      milestone_<name>/
        README.md
        feature_<name>.md           work that serves the whole milestone
        slice_<name>/
          README.md
          feature_<name>.md
          feature_<name>.md
```

**Neither skeleton opens with a status line.** Each is copied into a plan, where the first lines are
the node's own header.

**A worked plan built from these is in the repository**, at
[`kit/example/tree/`](https://github.com/georgethomasuk/agentic-handbook/tree/main/kit/example/tree):
one mission, four milestones, six slices and 24 features on
[the example system](../../../reference/example-system.md). [The example plan](../example-plan.md)
is the map of it.

**The workflow a feature names is not here.** Workflows are in
[Part 6, managing the delivery](../../06-delivery-management/templates/workflows/README.md).
