# The kit

One command, `plan`. It does the mechanical steps of
[Part 6, managing the delivery](../docs/parts/06-delivery-management/README.md): it joins a workflow,
assembles a brief, prints a column when the agent enters it, and claims and closes a feature in the
plan.

**How to use it is in [the kit's page](../docs/parts/06-delivery-management/kit.md).** This file is
for somebody changing it.

## What is here

| File | What it is |
|---|---|
| `plan` | The command. A shell wrapper that runs `plan.py` under `uv`, or under `python3` where there is no `uv` |
| `plan.py` | The whole kit, one file. Its only dependency is PyYAML |
| `tooling.yaml` | The kit's own values for the `tooling.*` slots |
| `example/tree/` | A five-node plan on the example system. `plan init --example` copies it |
| `test_plan.py` | The tests |

**The kit reads the workflow templates where they are published**, in
`docs/parts/06-delivery-management/templates/workflows/`. There is no second copy here. So a change
to a template is a change to the kit, and the tests must be run after one.

## Run the tests

```
scripts/test-kit.sh
```

It runs the tests, then runs `plan check` on a fresh copy of the example plan. Every test builds its
own repository in a temporary folder with a local remote. The pull-request path is tested against a
script that stands in for `gh`, and against nothing else.

## Three rules the code keeps

**Nothing derived is stored.** A workflow is joined and a brief is assembled when a command asks for
one. A stored copy can fall behind the three files it came from, and nothing would check it.

**A check that cannot run fails.** An unset archive destination, an unfilled slot and a missing
tooling file each stop the command with a non-zero exit. A check that skips when its input is missing
reads as a pass.

**The plan is edited by line, not rewritten.** A claim changes one line and adds one. Loading the
header and writing it back would reformat lines nobody asked it to touch, and the claim would stop
being readable as a diff.

## Not done

Listed on [the kit's page](../docs/parts/06-delivery-management/kit.md#what-it-has-not-proved).
