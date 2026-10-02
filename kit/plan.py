#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""plan – resolve workflows, assemble briefs, and move a feature through its columns.

The kit reads three things from a plan directory: the plan tree (one markdown file per node), the
workflow templates (a shared core, one file per workflow, and the slot definitions), and the values
that fill the slots. It writes working state for one feature under the work directory, and it edits
exactly two things in the tree: the claim when a feature is opened, and the close when it has merged.

Everything it prints is derived. Nothing it prints is stored, except where a command says so.
"""

from __future__ import annotations

import argparse
import copy
import filecmp
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

KIT_DIR = Path(__file__).resolve().parent
TEMPLATES = KIT_DIR.parent / "docs" / "parts" / "06-delivery-management" / "templates"

# A level is defined by who says it is done, not by size. Only a feature is executed, so only a
# feature binds a workflow, carries a status, and has a record.
LEVELS = ("mission", "milestone", "slice", "feature")
MAY_CONTAIN = {
    None: ("mission",),
    "mission": ("milestone", "feature"),
    "milestone": ("slice", "feature"),
    "slice": ("feature",),
    "feature": (),
}
NODE_NAME = re.compile(rf"^({'|'.join(LEVELS)})_[a-z0-9][a-z0-9_]*$")

STATUSES = ("design", "no-packet", "ready", "blocked", "in-progress", "in-review", "done")
IN_FLIGHT = ("in-progress", "in-review")
# These two sit before any workflow: the next stage is a design or a packet, not a column.
PRE_WORKFLOW = {
    "no-packet": "write the packet first – no column applies",
    "design": "needs design, not a workflow column",
}
CLAIM_STATUS = "in-progress"
OPEN_COLUMN = "open"

# The record's headings are closed because `Carried forward` is lifted by its exact heading into the
# brief of every feature that depends on the writer. Renamed, it reaches nobody.
CARRIED_FORWARD = "Carried forward"
RECORD_HEADINGS = (
    "Decisions taken",
    CARRIED_FORWARD,
    "Verification actually run",
    "Review",
    "Panel tally",
    "Also fixed (not the feature)",
    "Lesson",
)
PACKET_HEADINGS = ("Acceptance criteria", "Verification")
# The direction to lean when the criteria are silent. Its own heading because, as a clause inside
# the goal, it was the clause an author under time pressure did not write.
TIE_BREAKER = "Where to err"
INHERIT = "inherit"

EXIT_KINDS = ("command", "attest", "human_gate")
COMPACT_KEYS = {"offer", "carry", "never"}
DELEGATE_KEYS = {"model", "send", "keep", "escalate"}
REVIEW_KEYS = {"seat", "suspicion", "escalate"}
USE_KEYS = {"use", "as", "also", "seeds"}
PROTOCOLS = ("stage_protocol", "exit_kinds", "report_back", "compaction", "delegation")

RETRO_LABELS = ("Friction", "Worked", "Cheaper", "Faster", "Fix")
RETRO_CEILING = 60

SLOT = re.compile(r"\{\{(project|tooling)\.([a-z0-9_]+)\}\}")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def fail(message: str) -> "SystemExit":
    return SystemExit(f"plan: {message}")


def plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def as_text(value) -> str:
    """Block text, kept as written – paragraphs and lists intact."""
    return str(value).strip()


def inline(value) -> str:
    """One item on one line – a list entry, an exit, a slot value."""
    return " ".join(str(value).split())


# ──────────────────────────────────────────────────────────────────────────────
# Where things are
# ──────────────────────────────────────────────────────────────────────────────

DEFAULTS = {
    "tree": "tree",
    "workflows": "workflows",
    "values": "values.yaml",
    "retro": "retro",
    "work_dir": ".work",
    "remote": "origin",
    "main": "main",
    "land": "pr",
    "tooling_values": None,
}
LAND_MODES = ("pr", "push", "none")


@dataclass
class Kit:
    """One plan directory and the repository it sits in."""

    root: Path
    config: dict

    @classmethod
    def find(cls, start: Path | None = None) -> "Kit":
        if env := os.environ.get("PLAN_ROOT"):
            root = Path(env).resolve()
            if not (root / "kit.yaml").exists():
                raise fail(f"PLAN_ROOT is {root}, which has no kit.yaml")
            return cls.load(root)
        here = (start or Path.cwd()).resolve()
        for directory in (here, *here.parents):
            if (directory / "plan" / "kit.yaml").exists():
                return cls.load(directory / "plan")
            if (directory / "kit.yaml").exists() and (directory / "workflows").is_dir():
                return cls.load(directory)
        raise fail("no plan found – run `plan init <directory>`, or set PLAN_ROOT")

    @classmethod
    def load(cls, root: Path) -> "Kit":
        loaded = yaml.safe_load((root / "kit.yaml").read_text(encoding="utf-8")) or {}
        if unknown := sorted(set(loaded) - set(DEFAULTS)):
            raise fail(f"{root / 'kit.yaml'}: unknown key {', '.join(unknown)}")
        config = {**DEFAULTS, **loaded}
        if config["land"] not in LAND_MODES:
            raise fail(f"{root / 'kit.yaml'}: `land` must be one of {' · '.join(LAND_MODES)}")
        return cls(root=root, config=config)

    @cached_property
    def repo(self) -> Path:
        done = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True,
        )
        return Path(done.stdout.strip()).resolve() if done.returncode == 0 else self.root.parent

    @property
    def tree_dir(self) -> Path:
        return self.root / self.config["tree"]

    @property
    def workflows_dir(self) -> Path:
        return self.root / self.config["workflows"]

    @property
    def retro_dir(self) -> Path:
        return self.root / self.config["retro"]

    @property
    def remote_main(self) -> str:
        return f"{self.config['remote']}/{self.config['main']}"

    def work(self, key: str) -> Path:
        """Working state for one feature. Keyed on the feature rather than the working copy,
        because a working copy gets reused across features."""
        return self.repo / self.config["work_dir"] / key

    def show(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.repo))
        except ValueError:
            return str(path)


# ──────────────────────────────────────────────────────────────────────────────
# The plan tree
# ──────────────────────────────────────────────────────────────────────────────


@dataclass
class Node:
    file: Path
    slug: str
    level: str
    frontmatter: dict
    body: str
    rel: str
    parent: "Node | None" = None
    children: list["Node"] = field(default_factory=list)

    @property
    def key(self) -> str:
        return self.slug

    @property
    def is_leaf(self) -> bool:
        return not self.children

    @property
    def status(self) -> str | None:
        return self.frontmatter.get("status")

    @property
    def workflow(self) -> str | None:
        return self.frontmatter.get("workflow")

    @property
    def title(self) -> str:
        return str(self.frontmatter.get("title") or self.slug)

    @property
    def features(self) -> list["Node"]:
        """Every feature at or under this node."""
        if self.level == "feature":
            return [self]
        return [feature for child in self.children for feature in child.features]

    @property
    def milestone(self) -> "Node | None":
        return next((n for n in self.ancestry if n.level == "milestone"), None)

    @property
    def ancestry(self) -> list["Node"]:
        """Top of the plan first, this node last."""
        chain, cursor = [], self
        while cursor:
            chain.append(cursor)
            cursor = cursor.parent
        return list(reversed(chain))


@dataclass
class Tree:
    nodes: list[Node]
    errors: list[str]

    def by_key(self) -> dict[str, list[Node]]:
        out: dict[str, list[Node]] = defaultdict(list)
        for node in self.nodes:
            out[node.key].append(node)
        return out


def parse_document(text: str) -> tuple[dict, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    loaded = yaml.safe_load(match.group(1)) or {}
    if not isinstance(loaded, dict):
        raise ValueError("frontmatter is not a mapping")
    return loaded, text[match.end():]


def load_tree(kit: Kit) -> Tree:
    errors: list[str] = []
    nodes: list[Node] = []
    base = kit.tree_dir

    def make(file: Path, slug: str, parent: Node | None) -> Node:
        try:
            frontmatter, body = parse_document(file.read_text(encoding="utf-8"))
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{kit.show(file)}: {exc}")
            frontmatter, body = {}, ""
        anchor = file.parent if file.name == "README.md" else file.with_suffix("")
        node = Node(file=file, slug=slug, level=slug.split("_", 1)[0], frontmatter=frontmatter,
                    body=body, rel=str(anchor.relative_to(base)), parent=parent)
        nodes.append(node)
        return node

    def walk(directory: Path, parent: Node | None) -> list[Node]:
        found: list[Node] = []
        for entry in sorted(directory.iterdir()):
            if entry.name.startswith(".") or entry.name == "README.md":
                continue
            slug = entry.name if entry.is_dir() else entry.stem
            if not entry.is_dir() and entry.suffix != ".md":
                continue
            if not NODE_NAME.match(slug):
                errors.append(f"{kit.show(entry)}: name is not <level>_<slug> – everything under "
                              f"the tree is a node")
                continue
            if entry.is_dir():
                readme = entry / "README.md"
                if not readme.exists():
                    errors.append(f"{kit.show(entry)}: a node directory needs a README.md")
                    continue
                node = make(readme, slug, parent)
                node.children = walk(entry, node)
            else:
                node = make(entry, slug, parent)
            allowed = MAY_CONTAIN[parent.level if parent else None]
            if node.level not in allowed:
                where = f"inside a {parent.level}" if parent else "at the top of the tree"
                errors.append(f"{kit.show(entry)}: a {node.level} cannot sit {where}")
            found.append(node)
        return found

    if not base.is_dir():
        return Tree(nodes=[], errors=[f"{kit.show(base)} does not exist"])
    walk(base, None)
    return Tree(nodes=nodes, errors=errors)


def resolve_node(tree: Tree, spec: str) -> Node:
    wanted = spec.strip("/").removesuffix(".md").removesuffix("/README")
    matches = [n for n in tree.nodes if n.key == wanted or n.rel == wanted
               or n.rel.endswith("/" + wanted)]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise fail(f"no node matches {spec!r}")
    raise fail(f"{spec!r} matches {len(matches)} nodes – use the path: "
               + ", ".join(n.rel for n in matches))


def section(body: str, heading: str, level: int = 2) -> str | None:
    """The text under one heading, up to the next heading of the same or a higher level."""
    marks = "#" * level
    match = re.search(rf"^{marks} {re.escape(heading)}[ \t]*\n", body, re.M)
    if not match:
        return None
    rest = body[match.end():]
    stop = re.search(rf"^#{{1,{level}}} ", rest, re.M)
    return (rest[: stop.start()] if stop else rest).strip("\n")


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()


def record_parts(node: Node) -> dict[str, str]:
    """Each `###` section of the record, by heading. A section holding only a comment is empty."""
    record = section(node.body, "Record")
    if record is None:
        return {}
    parts: dict[str, str] = {}
    for match in re.finditer(r"^### (.+?)[ \t]*\n", record, re.M):
        parts[match.group(1)] = strip_comments(section(record, match.group(1), level=3) or "")
    return parts


def authored_brief(node: Node) -> str:
    """Everything written before the work – the node's body above `## Record`."""
    cut = re.search(r"^## Record[ \t]*$", node.body, re.M)
    brief = (node.body[: cut.start()] if cut else node.body).strip()
    # The file's own title is already the brief's title.
    return re.sub(r"\A# .*\n+", "", brief)


def is_briefed(node: Node) -> bool:
    return all(section(node.body, heading) is not None for heading in PACKET_HEADINGS)


def gate_criteria(node: Node) -> list[str]:
    """The criteria somebody outside the build will judge a milestone by, as it declares them."""
    declared = (node.frontmatter.get("traces") or {}).get("gate")
    return [str(c) for c in declared] if isinstance(declared, list) else []


def traced_gates(node: Node) -> list[str] | str | None:
    """What a feature says it answers: a list of criteria, `inherit`, or nothing at all."""
    declared = (node.frontmatter.get("traces") or {}).get("gate")
    if isinstance(declared, list):
        return [str(c) for c in declared]
    return INHERIT if declared == INHERIT else None


def coverage(milestone: Node) -> tuple[dict[str, list[Node]], list[Node]]:
    """Which features point at each criterion, and the features left out of the count. A feature
    that traces every criterion – a rehearsal, a final acceptance run – answers all of them by
    definition, so counting it makes each one look answered whether or not anything builds it."""
    criteria = gate_criteria(milestone)
    answered: dict[str, list[Node]] = {criterion: [] for criterion in criteria}
    blanket: list[Node] = []
    for feature in milestone.features:
        traced = traced_gates(feature)
        if not isinstance(traced, list):
            continue
        if len(criteria) > 1 and set(criteria) <= set(traced):
            blanket.append(feature)
            continue
        for criterion in traced:
            if criterion in answered:
                answered[criterion].append(feature)
    return answered, blanket


def demote(markdown: str, levels: int) -> str:
    return re.sub(r"^(#+) ", lambda m: "#" * (len(m.group(1)) + levels) + " ", markdown, flags=re.M)


class Graph:
    """`blocked_by` resolved to nodes, and what follows from the whole graph."""

    def __init__(self, tree: Tree) -> None:
        self.tree = tree
        by_key = tree.by_key()
        self.blockers: dict[str, list[Node]] = {}
        self.unresolved: list[tuple[Node, str]] = []
        for node in tree.nodes:
            resolved: list[Node] = []
            for ref in node.frontmatter.get("blocked_by") or []:
                targets = by_key.get(str(ref), [])
                if len(targets) == 1:
                    resolved.append(targets[0])
                else:
                    self.unresolved.append((node, str(ref)))
            self.blockers[node.rel] = resolved

    def unmet(self, node: Node) -> list[Node]:
        return [b for b in self.blockers[node.rel] if b.status != "done"]

    def upstream(self, node: Node) -> list[Node]:
        """Everything `node` depends on, directly or through another, nearest first."""
        seen, order, queue = {node.rel}, [], list(self.blockers[node.rel])
        while queue:
            current = queue.pop(0)
            if current.rel in seen:
                continue
            seen.add(current.rel)
            order.append(current)
            queue.extend(self.blockers[current.rel])
        return order

    def has_dependent(self, node: Node) -> bool:
        return any(node in blockers for blockers in self.blockers.values())

    def waiting_on(self, node: Node) -> list[Node]:
        """Every unfinished feature that cannot start until `node` lands, directly or through
        another."""
        return [other for other in self.tree.nodes
                if other.is_leaf and other.status != "done" and node in self.upstream(other)]

    def longest_chain(self, among: list[Node]) -> list[Node]:
        """The longest run of unfinished features in which each waits on the one before."""
        if self.cycles():
            return []
        inside = {n.rel for n in among if n.status != "done"}
        best: dict[str, list[Node]] = {}

        def chain(node: Node) -> list[Node]:
            if node.rel not in best:
                before = [chain(b) for b in self.blockers[node.rel] if b.status != "done"]
                best[node.rel] = max(before, key=len, default=[]) + [node]
            return best[node.rel]

        return max((chain(n) for n in among if n.rel in inside), key=len, default=[])

    def cycles(self) -> list[list[str]]:
        colour: dict[str, int] = {}
        found: list[list[str]] = []

        def visit(node: Node, path: list[str]) -> None:
            colour[node.rel] = 1
            for blocker in self.blockers[node.rel]:
                if colour.get(blocker.rel) == 1:
                    found.append(path[path.index(blocker.rel):] + [blocker.rel])
                elif colour.get(blocker.rel) is None:
                    visit(blocker, path + [blocker.rel])
            colour[node.rel] = 2

        for node in self.tree.nodes:
            if colour.get(node.rel) is None:
                visit(node, [node.rel])
        return found

    def waves(self) -> dict[str, int]:
        """The earliest point each feature could start, from the graph alone. Status is ignored on
        purpose: an order that moves when work finishes is not an order anyone can plan against."""
        if self.cycles():
            return {}
        depth: dict[str, int] = {}

        def resolve(node: Node) -> int:
            if node.rel not in depth:
                depth[node.rel] = 1 + max((resolve(b) for b in self.blockers[node.rel]), default=0)
            return depth[node.rel]

        return {n.rel: resolve(n) for n in self.tree.nodes if n.is_leaf}


# ──────────────────────────────────────────────────────────────────────────────
# Workflows – the core, one workflow and the slot values, joined
# ──────────────────────────────────────────────────────────────────────────────


def load_yaml(path: Path) -> dict:
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise fail(f"{path}: does not parse – {exc}") from None
    if not isinstance(loaded, dict):
        raise fail(f"{path}: expected a mapping at the top")
    return loaded


def workflow_names(kit: Kit) -> list[str]:
    return sorted(p.stem for p in kit.workflows_dir.glob("*.yaml")
                  if p.stem not in ("core", "slots"))


def slot_definitions(kit: Kit) -> dict[str, dict]:
    raw = load_yaml(kit.workflows_dir / "slots.yaml")
    return {f"{space}.{name}": body or {}
            for space in ("project", "tooling") for name, body in (raw.get(space) or {}).items()}


def slot_values(kit: Kit) -> dict[str, str]:
    """Later sources win: the kit's own tooling values, then the operator's, then the plan's."""
    values: dict[str, str] = {}

    def take(path: Path) -> None:
        raw = load_yaml(path)
        for space in ("project", "tooling"):
            for name, value in (raw.get(space) or {}).items():
                if value is not None and inline(value):
                    values[f"{space}.{name}"] = inline(value)

    take(KIT_DIR / "tooling.yaml")
    operator = os.environ.get("PLAN_TOOLING_VALUES") or kit.config["tooling_values"]
    if operator:
        path = Path(os.path.expanduser(operator))
        path = path if path.is_absolute() else kit.root / path
        if not path.exists():
            raise fail(f"tooling values file {path} does not exist")
        take(path)
    plan_values = kit.root / kit.config["values"]
    if plan_values.exists():
        take(plan_values)
    return values


def append_into(base: dict, extra: dict) -> None:
    """`also:` – each field is appended to the field of the same name. Text gains paragraphs, a
    list gains items, a nested block is appended field by field."""
    for key, value in extra.items():
        if key not in base:
            base[key] = copy.deepcopy(value)
        elif isinstance(value, dict) and isinstance(base[key], dict):
            append_into(base[key], value)
        elif isinstance(value, list) and isinstance(base[key], list):
            base[key] = base[key] + copy.deepcopy(value)
        elif isinstance(value, str) and isinstance(base[key], str):
            base[key] = base[key].rstrip() + "\n\n" + value
        else:
            raise fail(f"`also:` cannot append {type(value).__name__} `{key}` to "
                       f"{type(base[key]).__name__}")


def slots_in(value) -> set[str]:
    return {f"{m.group(1)}.{m.group(2)}" for m in SLOT.finditer(json.dumps(value))}


def substitute(value, replace):
    if isinstance(value, str):
        return replace(value)
    if isinstance(value, list):
        return [substitute(item, replace) for item in value]
    if isinstance(value, dict):
        return {key: substitute(item, replace) for key, item in value.items()}
    return value


def join_workflow(kit: Kit, name: str) -> dict:
    """The core and one workflow joined, with every slot still a placeholder."""
    path = kit.workflows_dir / f"{name}.yaml"
    if not path.exists():
        raise fail(f"no workflow `{name}` – {kit.show(path)} does not exist")
    workflow = load_yaml(path)
    core = load_yaml(kit.workflows_dir / "core.yaml")
    shared = {c["name"]: c for c in core.get("columns") or []}

    columns = []
    for entry in workflow.get("columns") or []:
        if "use" not in entry:
            columns.append(copy.deepcopy(entry))
            continue
        if unknown := sorted(set(entry) - USE_KEYS):
            raise fail(f"{name}: a `use:` column carries {', '.join(unknown)} – only "
                       f"{' · '.join(sorted(USE_KEYS))} are read")
        source = str(entry["use"]).removeprefix("core.")
        if source not in shared:
            raise fail(f"{name}: `use: {entry['use']}` names no column in core.yaml")
        column = copy.deepcopy(shared[source])
        if entry.get("as"):
            column["name"] = entry["as"]
        if entry.get("also"):
            append_into(column, entry["also"])
        if entry.get("seeds"):
            column["seeds"] = copy.deepcopy(entry["seeds"])
        columns.append(column)

    joined = {key: workflow[key] for key in ("name", "description", "agreed_at", "unattended_from",
                                             "unit") if key in workflow}
    for key in PROTOCOLS:
        if key in core:
            joined[key] = core[key]
    joined["standing_constraints"] = (core.get("standing_constraints") or []) + (
        workflow.get("standing_constraints") or [])
    joined["columns"] = columns
    if workflow.get("modes"):
        joined["modes"] = workflow["modes"]
    return joined


def resolve_workflow(kit: Kit, name: str, feature: str | None = None) -> dict:
    """The joined workflow with every slot filled. An unfilled slot stops it: an instruction with a
    hole in it is worse than no instruction, and the slot's example is from another system."""
    joined = join_workflow(kit, name)
    modes = joined.pop("modes", None)
    values = slot_values(kit)
    if missing := sorted(slots_in(joined) - set(values)):
        raise fail(f"`{name}` cannot be resolved – {plural(len(missing), 'slot')} with no value: "
                   + ", ".join(missing) + f". Add them to {kit.show(kit.root / kit.config['values'])}")

    def replace(text: str) -> str:
        text = SLOT.sub(lambda m: values[f"{m.group(1)}.{m.group(2)}"], text)
        text = text.replace("<workflow>", name)
        return text.replace("<feature>", feature) if feature else text

    resolved = substitute(joined, replace)
    if modes:
        resolved["modes_not_applied"] = [m.get("name") for m in modes]
    return resolved


def column_names(workflow: dict) -> list[str]:
    return [str(c.get("name")) for c in workflow.get("columns") or []]


def unattended_columns(workflow: dict) -> set[str]:
    names, start = column_names(workflow), workflow.get("unattended_from")
    return set(names[names.index(start):]) if start in names else set()


def review_block(column: dict) -> tuple[str, dict] | None:
    for key, value in column.items():
        if key.startswith("review_each_"):
            return key.removeprefix("review_each_"), value
    return None


# ──────────────────────────────────────────────────────────────────────────────
# Rendering – a column, and the brief around it
# ──────────────────────────────────────────────────────────────────────────────


def enter_command(key: str, column: str) -> str:
    return f"plan enter {key} {column}"


def render_exit(entry: dict) -> str:
    if "command" in entry:
        line = f"- **Command must exit 0:** `{inline(entry['command'])}`"
    elif "attest" in entry:
        line = (f"- **Attest, then continue:** {inline(entry['attest'])} · check it yourself and "
                f"write the evidence in the journal – not a hand-back")
    else:
        stop = " · **blocking – hand back, do not proceed**" if entry.get("blocking") else ""
        line = f"- **Human gate:** {inline(entry.get('human_gate', '?'))}{stop}"
    if entry.get("why"):
        line += f"\n  - {inline(entry['why'])}"
    return line


def render_column(column: dict, key: str, journal: str, unattended: bool) -> list[str]:
    """One column, rendered the same way wherever it appears, so that re-reading it later is reading
    the same text rather than a summary of it."""
    name = str(column.get("name"))
    out = [f"**Entered by:** `{enter_command(key, name)}` – it records the column and prints this "
           f"text. Work from what it prints."]
    if unattended:
        out.append("**Unattended column.** When its exits pass, enter the next column – no "
                   "check-in, no summary-and-wait. Stop only at a blocking human gate or on the "
                   "stop list. Everything else is decided here and disclosed in the pull request.")
    if preconditions := column.get("precondition") or []:
        out.append("**Before anything else, these must pass:**")
        out.append("\n".join(render_exit(p) for p in preconditions))
    if isinstance(delegate := column.get("delegate"), dict):
        out.append(f"**Send part of this column to a worker, at {inline(delegate.get('model'))}.**")
        out.append("**Send:** " + as_text(delegate.get("send", "")))
        out.append("**Keep in this session:** " + as_text(delegate.get("keep", "")))
        out.append("**Raise the tier if:** " + as_text(delegate.get("escalate", "")))
    if review := review_block(column):
        unit, block = review
        out.append(f"**Review every {unit} before the next one starts** – one reviewer, on that "
                   f"{unit}'s own diff. This is not a panel.")
        out.append(f"**Suspicion – what a {unit} here gets wrong:** "
                   + as_text(block.get("suspicion", "")))
        out.append(f"**Bring to the operator rather than the next {unit}:** "
                   + as_text(block.get("escalate", "")))
    if column.get("entry"):
        out.append("**Do this:**")
        out.append(as_text(column["entry"]))
    if seeds := column.get("seeds") or []:
        out.append("**Start the panel from these suspicions:**")
        out.append("\n".join(f"- {inline(s)}" for s in seeds))
    if produces := column.get("produces") or []:
        out.append("**When this column closes, these exist:**")
        out.append("\n".join(f"- {inline(p)}" for p in produces))
    # The entry check goes first because it is the only exit already wrong by the time it is read.
    # A column worked from the tail of the brief instead of entered leaves no trace otherwise.
    exits = [{"command": f"plan enter-check {key} {name}",
              "why": "the most recent column entered is this one. If it fails, the column was "
                     "worked without being entered – enter it now and say so in the record."}]
    exits.extend(column.get("exit") or [])
    out.append("**This column is finished when:**")
    out.append("\n".join(render_exit(e) for e in exits))
    if isinstance(compact := column.get("compact"), dict):
        if compact.get("never"):
            out.append("**Do not offer a compaction at this boundary.** " + as_text(compact["never"]))
        else:
            out.append("**A compaction point – offer it, do not take it.** "
                       + as_text(compact.get("offer", "")))
            out.append(f"Write the journal first. Append to `{journal}`:")
            out.append("\n".join(f"- {inline(c)}" for c in compact.get("carry") or []))
            out.append("Then hand back with the offer: say the journal is written, name what "
                       "would be dropped, and wait.")
    return out


def column_chain(names: list[str], chosen: str) -> str:
    return " → ".join(f"**`{n}`**" if n == chosen else f"`{n}`" for n in names)


def journal_path(kit: Kit, node: Node) -> str:
    return kit.show(kit.work(node.key) / "journal.md")


def choose_column(node: Node, names: list[str], asked: str | None) -> tuple[str, bool]:
    """Which column a brief starts at, and whether that is recorded or assumed. A guess presented as
    a position reads as "this has not started" about a feature that may be several columns in."""
    chosen = asked or node.frontmatter.get("column")
    if chosen and chosen not in names:
        raise fail(f"column {chosen!r} is not in workflow `{node.workflow}` ({', '.join(names)})")
    if chosen:
        return str(chosen), True
    if not names:
        raise fail(f"workflow `{node.workflow}` has no columns")
    # A feature nobody has claimed starts at the first column, and that is a fact. One already in
    # flight with no column recorded is a guess, and the brief has to say so.
    return names[0], node.status not in IN_FLIGHT


def identity_line(node: Node) -> str:
    chain = " › ".join(n.title for n in node.ancestry[:-1]) or "top of the plan"
    line = f"{chain} › this feature · status {node.status or 'unset'}"
    if briefed := node.frontmatter.get("briefed"):
        line += f" · packet written {briefed}"
    return line


def traces_line(node: Node) -> str | None:
    traces = node.frontmatter.get("traces")
    if not isinstance(traces, dict):
        return None
    parts = []
    for family, value in traces.items():
        items = value if isinstance(value, list) else [value]
        if items := [str(i) for i in items if i]:
            parts.append(f"{family} {', '.join(items)}")
    return "Traces: " + " · ".join(parts) if parts else None


def build_brief(kit: Kit, tree: Tree, graph: Graph, node: Node, asked: str | None,
                column_only: bool = False) -> str:
    """The brief for one feature. The ask first, then the context: a brief assembled by walking the
    plan from the top reaches the instruction last, and the packet above it reads as an order to
    build."""
    if not node.is_leaf or node.level != "feature":
        raise fail(f"{node.rel} is a {node.level} – only a feature is executed, so only a feature "
                   f"has a brief")
    if node.status in PRE_WORKFLOW:
        raise fail(f"{node.rel}: status is `{node.status}` – {PRE_WORKFLOW[node.status]}")
    if not node.workflow:
        raise fail(f"{node.rel}: no `workflow:` – bind one before assembling a brief")

    workflow = resolve_workflow(kit, node.workflow, node.key)
    names = column_names(workflow)
    chosen, recorded = choose_column(node, names, asked)
    columns = {str(c.get("name")): c for c in workflow["columns"]}
    unattended = unattended_columns(workflow)
    journal = journal_path(kit, node)
    here = kit.show(node.file)
    after = [] if column_only else names[names.index(chosen) + 1:]
    visible = [columns[n] for n in [chosen, *after]]

    out = [f"# {node.title}", identity_line(node)]
    if traces := traces_line(node):
        out.append(traces)

    out.append("## Your task")
    position = f"{names.index(chosen) + 1} of {len(names)}"
    start = "Column" if column_only else "Start at column"
    assumed = "" if recorded else (" **This is assumed.** The feature is in flight, no column was "
                                   "given and the plan records none. Read the journal for how far "
                                   "it has got before doing anything.")
    out.append(f"**{start} `{chosen}` – {position} in `{node.workflow}`.**{assumed} "
               f"{column_chain(names, chosen)}")
    out.append(as_text(workflow.get("stage_protocol", "")))
    if column_only:
        out.append("This brief covers **one** column. Do what it asks, stop at its exit "
                   "conditions, and do not run ahead into a later one.")
    elif (start_unattended := workflow.get("unattended_from")) in names:
        out.append(f"**From `{start_unattended}` on, this workflow runs unattended.** Roll from "
                   f"column to column without a check-in. Stop only at a blocking human gate or on "
                   f"the stop list in the standing constraints below. Read that list before "
                   f"entering `{start_unattended}`.")
    if goal := section(node.body, "Goal"):
        out.append("**The goal**\n\n" + goal.strip())
    if is_briefed(node):
        out.append(f"**The contract** is the packet reproduced under `## This feature` below. Its "
                   f"acceptance criteria are the contract and its verification commands are the "
                   f"evidence. Its file is `{here}`. There is no second brief to find.")
    else:
        out.append(f"**There is no packet.** `{here}` carries no acceptance criteria and no "
                   f"verification, so the first job is to write them – not to start building.")

    out.append(f"## Column · `{chosen}`")
    if workflow.get("description"):
        out.append(f"About the `{node.workflow}` workflow: " + inline(workflow["description"]))
    out.extend(render_column(columns[chosen], node.key, journal, chosen in unattended))
    if constraints := workflow.get("standing_constraints") or []:
        out.append("### Standing constraints – every column, every time")
        out.append("\n".join(f"- {inline(c)}" for c in constraints))

    out.append("## How to report back")
    out.append(as_text(workflow.get("report_back", "")))
    # A protocol no column in this brief uses is left out. Standing text for a rule that never
    # fires is the standing text a session learns to skim.
    if any(c.get("compact") for c in visible) and workflow.get("compaction"):
        out.append("## The journal, and when to compact")
        out.append(as_text(workflow["compaction"]))
    if any(c.get("delegate") for c in visible) and workflow.get("delegation"):
        out.append("## Columns that send work to a worker")
        out.append(as_text(workflow["delegation"]))

    out.append("---")
    out.append("## Standing context")
    out.append("Everything below is assembled from the plan. It is the context for the task above, "
               "not a second set of instructions, and it does not restate the column.")

    ancestors = node.ancestry[:-1]
    goals = [(a, section(a.body, "Goal")) for a in ancestors]
    if any(text for _, text in goals):
        out.append("## Why this exists – the goal chain")
        for ancestor, text in goals:
            if text:
                out.append(f"### {ancestor.level.title()} · {ancestor.title}")
                out.append(demote(text.strip(), 2))

    fences = [(a, section(a.body, "Boundaries")) for a in ancestors]
    if any(text for _, text in fences):
        out.append("## Boundaries inherited from above")
        out.append("These accumulate. A feature cannot widen a fence set above it. If the work "
                   "starts reaching past one of these, it has left its scope – stop.")
        for ancestor, text in fences:
            if text:
                out.append(f"### From the {ancestor.level} · {ancestor.title}")
                out.append(demote(text.strip(), 2))

    out.append("## This feature")
    out.append(demote(authored_brief(node), 1))

    settled = [(a, section(a.body, "Inherited context")) for a in ancestors]
    if any(text for _, text in settled):
        out.append("## Settled above – do not reopen")
        for ancestor, text in settled:
            if text:
                out.append(f"### From the {ancestor.level} · {ancestor.title}")
                out.append(demote(text.strip(), 2))

    if blockers := graph.blockers[node.rel]:
        out.append("## Depends on")
        out.append("\n".join(
            f"- `{b.key}` – {b.title} · "
            + ("done" if b.status == "done" else f"**{b.status} – not yet met**")
            for b in blockers))

    # The one section that flows along the dependency graph rather than down the tree. What a
    # feature inherits from above comes from its ancestors; what was left for it comes from whatever
    # it was built on, which is usually somewhere else in the plan.
    carried = [(n, record_parts(n).get(CARRIED_FORWARD)) for n in graph.upstream(node)]
    if carried := [(n, text) for n, text in carried if text]:
        out.append("## Carried forward from upstream work")
        out.append("Gaps and traps left deliberately by the features this one is built on, nearest "
                   "dependency first. Each was written for whoever came next. That is you. Nothing "
                   "else in this brief repeats them.")
        for source, text in carried:
            out.append(f"### From `{source.key}` · {source.title}")
            out.append(demote(text, 1))

    if after:
        out.append("## The rest of the workflow")
        out.append(f"The {plural(len(after), 'column')} after `{chosen}`, in order, exactly as the "
                   f"workflow states them. **Do not start any of them now, and do not work from "
                   f"this copy.** It is here for reading ahead. Enter each column with its "
                   f"`plan enter` line, and work from what that prints.")
        for name in after:
            out.append(f"### `{name}` – {names.index(name) + 1} of {len(names)}")
            out.extend(render_column(columns[name], node.key, journal, name in unattended))

    return "\n\n".join(part for part in out if part).rstrip() + "\n"


def words_before_column(brief: str) -> int:
    """How many words come before the sentence that names the column – the one check on a brief's
    order that needs no judgement."""
    marker = re.search(r"^\*\*(Start at column|Column) `", brief, re.M)
    return len(brief[: marker.start()].split()) if marker else -1


# ──────────────────────────────────────────────────────────────────────────────
# Entering a column
# ──────────────────────────────────────────────────────────────────────────────


def current_branch(kit: Kit) -> str:
    done = subprocess.run(["git", "-C", str(kit.repo), "branch", "--show-current"],
                          capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else ""


def markers(kit: Kit, key: str) -> list[dict]:
    path = kit.work(key) / "stages.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def enter_column(kit: Kit, node: Node, column_name: str) -> str:
    """Record entry to a column and return its instructions – in that order, as one command.

    Entering is how the column's text is obtained. As a separate step it was an instruction, and an
    instruction that costs nothing to skip gets skipped hardest when several columns are worked in
    one push. A column name that is not in the workflow raises before anything is written, because
    a marker naming a column that does not exist is worse than no marker.
    """
    if not node.workflow:
        raise fail(f"{node.rel} binds no workflow, so there is no column to enter")
    workflow = resolve_workflow(kit, node.workflow, node.key)
    names = column_names(workflow)
    if column_name not in names:
        raise fail(f"column {column_name!r} is not in workflow `{node.workflow}` "
                   f"({', '.join(names)}) – nothing recorded")

    work = kit.work(node.key)
    work.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with (work / "stages.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"time": now, "column": column_name,
                                 "branch": current_branch(kit)}) + "\n")
    journal = work / "journal.md"
    opening = "" if journal.exists() else f"# Journal · {node.title}\n"
    with journal.open("a", encoding="utf-8") as handle:
        handle.write(f"{opening}\n## Column `{column_name}` – entered {now}\n")

    column = next(c for c in workflow["columns"] if c.get("name") == column_name)
    out = [f"Column `{column_name}` – {names.index(column_name) + 1} of {len(names)} in "
           f"`{node.workflow}`. {column_chain(names, column_name)}",
           "Say which column this is, then restate in your own words what it asks and what ends "
           "it, from the text below. Stop at its exit conditions."]
    out.extend(render_column(column, node.key, kit.show(journal),
                             column_name in unattended_columns(workflow)))
    if constraints := workflow.get("standing_constraints") or []:
        out.append("### Standing constraints – every column, every time")
        out.append("\n".join(f"- {inline(c)}" for c in constraints))
    return "\n\n".join(out) + "\n"


def enter_check(kit: Kit, node: Node, column_name: str) -> int:
    recorded = markers(kit, node.key)
    if not recorded:
        print(f"plan: no column has been entered for {node.key}", file=sys.stderr)
        return 1
    last = recorded[-1]["column"]
    if last != column_name:
        print(f"plan: the most recent column entered for {node.key} is `{last}`, not "
              f"`{column_name}`", file=sys.stderr)
        return 1
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# The claim and the close – the only two edits the kit makes to the tree
# ──────────────────────────────────────────────────────────────────────────────


def frontmatter_span(lines: list[str], what: str) -> int:
    if not lines or lines[0].rstrip("\n") != "---":
        raise fail(f"{what}: no frontmatter")
    for index, line in enumerate(lines[1:], 1):
        if line.rstrip("\n") == "---":
            return index
    raise fail(f"{what}: frontmatter is not closed")


def field_lines(lines: list[str], end: int, name: str) -> list[int]:
    return [i for i in range(1, end) if lines[i].startswith(f"{name}:")]


def field_value(line: str) -> str:
    return line.split(":", 1)[1].split("#")[0].strip()


def apply_claim(path: Path, column: str) -> None:
    """Set `status:` and add `column:` after it, editing lines rather than re-dumping YAML. A dumper
    would reformat frontmatter nobody asked it to touch, and the claim would stop being a change
    anyone can read at a glance."""
    lines = path.read_text(encoding="utf-8").splitlines(True)
    end = frontmatter_span(lines, path.name)
    status = field_lines(lines, end, "status")
    if len(status) != 1:
        raise fail(f"{path.name}: expected exactly one `status:` line, found {len(status)}")
    if field_value(lines[status[0]]) != "ready":
        raise fail(f"{path.name}: status is `{field_value(lines[status[0]])}`, expected `ready`. "
                   f"A claim on a feature that is not ready is a second claim or a resurrected "
                   f"feature. Both want a person, not a command.")
    if field_lines(lines, end, "column"):
        raise fail(f"{path.name}: `column:` is already set – this feature is claimed, or a close "
                   f"did not remove it")
    lines[status[0]] = f"status: {CLAIM_STATUS}\n"
    lines.insert(status[0] + 1, f"column: {column}\n")
    path.write_text("".join(lines), encoding="utf-8")


def apply_close(path: Path, pr: int, merged: str) -> None:
    """Three changes: status done, the column removed, the merge date written. No prose."""
    lines = path.read_text(encoding="utf-8").splitlines(True)
    end = frontmatter_span(lines, path.name)
    at = {name: field_lines(lines, end, name) for name in ("status", "column", "pr", "merged")}
    if len(at["status"]) != 1:
        raise fail(f"{path.name}: expected exactly one `status:` line")
    if field_value(lines[at["status"][0]]) != CLAIM_STATUS:
        raise fail(f"{path.name}: status is `{field_value(lines[at['status'][0]])}`, expected "
                   f"`{CLAIM_STATUS}`")
    if any(field_value(lines[i]) for i in at["merged"]):
        raise fail(f"{path.name}: `merged:` is already set – this feature is already closed")
    recorded = [field_value(lines[i]) for i in at["pr"] if field_value(lines[i])]
    if recorded and recorded[0] != str(pr):
        raise fail(f"{path.name}: `pr:` reads {recorded[0]}, not {pr}. Closing against a different "
                   f"pull request is a person's call.")
    lines[at["status"][0]] = f"status: done\npr: {pr}\nmerged: {merged}\n"
    for index in at["column"] + at["pr"] + at["merged"]:
        lines[index] = ""
    path.write_text("".join(lines), encoding="utf-8")


def git(kit: Kit, *args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    done = subprocess.run(["git", "-C", str(cwd or kit.repo), *args], capture_output=True, text=True)
    if check and done.returncode != 0:
        raise fail(f"git {' '.join(args)} failed:\n{(done.stderr or done.stdout).strip()}")
    return done


def gh(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    done = subprocess.run(["gh", *args], cwd=str(cwd), capture_output=True, text=True)
    if check and done.returncode != 0:
        raise fail(f"gh {' '.join(args)} failed:\n{(done.stderr or done.stdout).strip()}")
    return done


def on_main(kit: Kit, node: Node) -> dict:
    """The feature's frontmatter as the main branch has it – the only place anyone else looks."""
    git(kit, "fetch", "-q", kit.config["remote"], kit.config["main"])
    shown = git(kit, "show", f"{kit.remote_main}:{kit.show(node.file)}", check=False)
    if shown.returncode != 0:
        raise fail(f"{kit.show(node.file)} is not on {kit.remote_main}")
    return parse_document(shown.stdout)[0]


def land(kit: Kit, node: Node, verb: str, subject: str, body: str, edit,
         rebase: bool = True) -> None:
    """Make one plan-only change on the main branch, from a throwaway working copy.

    The change is made against the main branch as it is now, not against the working branch, so it
    cannot carry anything else with it. Afterwards the working branch is brought up to the new main:
    a base that still holds the old status would silently revert the change when the feature merges.
    """
    mode = kit.config["land"]
    if mode == "none":
        edit(node.file)
        print(f"edited {kit.show(node.file)} in this working copy. `land: none` – getting it onto "
              f"{kit.config['main']} is yours.\n\nsuggested subject: {subject}")
        return

    remote, main = kit.config["remote"], kit.config["main"]
    branch = f"plan/{verb}-{node.key.removeprefix('feature_').replace('_', '-')}"
    relative = kit.show(node.file)
    git(kit, "fetch", "-q", remote, main)
    scratch = Path(tempfile.mkdtemp(prefix="plan-land-"))
    git(kit, "worktree", "add", "-q", "-B", branch, str(scratch), kit.remote_main)
    try:
        edit(scratch / relative)
        git(kit, "add", relative, cwd=scratch)
        git(kit, "commit", "-q", "-m", subject, "-m", body, cwd=scratch)
        head = git(kit, "rev-parse", "HEAD", cwd=scratch).stdout.strip()
        if mode == "push":
            git(kit, "push", "-q", remote, f"HEAD:{main}", cwd=scratch)
        else:
            git(kit, "push", "-q", "--force-with-lease", "-u", remote, branch, cwd=scratch)
            gh("pr", "create", "--base", main, "--head", branch, "--title", subject,
               "--body", body, cwd=scratch)
            checks = gh("pr", "checks", branch, "--watch", "--fail-fast", cwd=scratch, check=False)
            report = (checks.stdout + checks.stderr).lower()
            if checks.returncode != 0 and "no checks reported" not in report:
                raise fail(f"checks did not pass on {branch} – nothing merged:\n"
                           + (checks.stdout or checks.stderr).strip())
            gh("pr", "merge", branch, "--squash", "--match-head-commit", head, cwd=scratch)
    finally:
        git(kit, "worktree", "remove", "--force", str(scratch), check=False)
        shutil.rmtree(scratch, ignore_errors=True)
        git(kit, "branch", "-D", branch, check=False)

    git(kit, "fetch", "-q", remote, main)
    if not rebase:
        print(f"landed on {kit.remote_main}.")
        return
    dirty = git(kit, "status", "--porcelain", "--untracked-files=no").stdout.strip()
    if dirty:
        print(f"landed on {kit.remote_main}. This working copy has uncommitted changes, so it was "
              f"not rebased – run `git rebase {kit.remote_main}` once they are committed.")
        return
    git(kit, "rebase", "-q", kit.remote_main)
    print(f"landed on {kit.remote_main}, and this branch now contains it.")


def claim(kit: Kit, node: Node, do_land: bool) -> int:
    if not node.is_leaf or node.level != "feature":
        raise fail(f"{node.rel} is not a feature – only a feature carries a claim")
    workflow = join_workflow(kit, node.workflow) if node.workflow else None
    if workflow is None:
        raise fail(f"{node.rel}: no `workflow:` – nothing says which column follows `{OPEN_COLUMN}`")
    names = column_names(workflow)
    if OPEN_COLUMN not in names or names.index(OPEN_COLUMN) + 1 >= len(names):
        raise fail(f"{node.rel}: workflow `{node.workflow}` has no column after `{OPEN_COLUMN}`")
    column = names[names.index(OPEN_COLUMN) + 1]
    subject = f"plan(open): claim {node.title}"
    body = (f"Marks `{node.key}` in flight on `{kit.config['main']}` before the work starts, so "
            f"the plan stops offering it to the next session that looks.\n\n"
            f"`status: {CLAIM_STATUS}`, `column: {column}` ({node.workflow}, "
            f"{names.index(column) + 1} of {len(names)}). No code, no packet edits.")
    if do_land:
        land(kit, node, "open", subject, body, lambda path: apply_claim(path, column))
    else:
        apply_claim(node.file, column)
        print(f"claimed {node.key} in this working copy – `column: {column}`. Nothing was pushed; "
              f"`plan claim {node.key} --land` puts it on {kit.config['main']}.")
    return 0


def claim_check(kit: Kit, node: Node) -> int:
    """The property, not a report of it: the claim is on the main branch, and this branch contains
    the main branch. A claim that landed on a base the branch does not contain looks identical to
    one that worked, until the feature merges and quietly un-claims itself."""
    there = on_main(kit, node)
    problems = []
    if there.get("status") != CLAIM_STATUS or not there.get("column"):
        problems.append(f"{kit.remote_main} reads status `{there.get('status')}`, column "
                        f"`{there.get('column')}` – the claim is not there")
    behind = git(kit, "rev-list", "--count", f"HEAD..{kit.remote_main}").stdout.strip()
    if behind != "0":
        problems.append(f"this branch is {plural(int(behind), 'commit')} behind {kit.remote_main} "
                        f"– rebase before starting")
    here = parse_document(node.file.read_text(encoding="utf-8"))[0]
    if here.get("status") != CLAIM_STATUS:
        problems.append(f"the working copy reads status `{here.get('status')}`")
    for problem in problems:
        print(f"plan: {problem}", file=sys.stderr)
    return 1 if problems else 0


def merged_date(kit: Kit, pr: int) -> str:
    """The merge date, read from the code host. Never typed: a date typed before the merge is a
    guess, and one typed after it is a copy somebody has to get right."""
    done = gh("pr", "view", str(pr), "--json", "state,mergedAt", cwd=kit.repo)
    answer = json.loads(done.stdout)
    if answer.get("state") != "MERGED" or not answer.get("mergedAt"):
        raise fail(f"pull request {pr} is {answer.get('state')}, not MERGED – nothing closed")
    return str(answer["mergedAt"])[:10]


def close(kit: Kit, node: Node, pr: int, merged: str | None, do_land: bool) -> int:
    if not node.is_leaf or node.level != "feature":
        raise fail(f"{node.rel} is not a feature – only a feature is closed")
    when = merged or merged_date(kit, pr)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", when):
        raise fail(f"the merge date must be YYYY-MM-DD, got {when!r}")
    subject = f"plan(close): {node.title} is done"
    body = (f"Moves `{node.key}` to `done` on `{kit.config['main']}` now that pull request {pr} "
            f"has merged.\n\n`status: done`, `column:` removed, `merged: {when}`. No code, no "
            f"packet edits.")
    if do_land:
        # No rebase here: the feature branch has merged, and its working copy is about to go.
        land(kit, node, "close", subject, body, lambda path: apply_close(path, pr, when),
             rebase=False)
    else:
        apply_close(node.file, pr, when)
        print(f"closed {node.key} in this working copy. Nothing was pushed; "
              f"`plan close {node.key} --pr {pr} --land` puts it on {kit.config['main']}.")
    return 0


def close_check(kit: Kit, node: Node) -> int:
    there = on_main(kit, node)
    if there.get("status") == "done" and there.get("merged") and not there.get("column"):
        return 0
    print(f"plan: {kit.remote_main} reads status `{there.get('status')}`, merged "
          f"`{there.get('merged')}`, column `{there.get('column')}` – not closed", file=sys.stderr)
    return 1


# ──────────────────────────────────────────────────────────────────────────────
# The journal's afterlife, and the retro
# ──────────────────────────────────────────────────────────────────────────────


def archive_target(key: str) -> Path:
    destination = os.environ.get("PLAN_JOURNAL_ARCHIVE")
    if not destination:
        raise fail("PLAN_JOURNAL_ARCHIVE is not set – nothing archived. An archive step that "
                   "succeeds having copied nothing leaves you believing there is an archive.")
    directory = Path(os.path.expanduser(destination))
    if not directory.is_dir():
        raise fail(f"PLAN_JOURNAL_ARCHIVE is {directory}, which is not a directory – nothing "
                   f"archived")
    return directory / f"{key}.md"


def archive(kit: Kit, node: Node) -> int:
    journal = kit.work(node.key) / "journal.md"
    if not journal.exists() or not journal.read_text(encoding="utf-8").strip():
        raise fail(f"{kit.show(journal)} is missing or empty – there is nothing to archive, which "
                   f"is a finding, not a success")
    target = archive_target(node.key)
    shutil.copyfile(journal, target)
    if not filecmp.cmp(journal, target, shallow=False):
        raise fail(f"the copy at {target} does not match {kit.show(journal)}")
    print(f"archived {kit.show(journal)} to {target} – "
          f"{plural(len(target.read_text(encoding='utf-8').splitlines()), 'line')}, read back.")
    return 0


def release(kit: Kit, node: Node) -> int:
    """Remove the feature's working state – and only after the journal is safely elsewhere. The
    journal lives in the working state, so releasing first destroys the only evidence behind every
    "verification actually run" line the record has just made."""
    work = kit.work(node.key)
    journal = work / "journal.md"
    if journal.exists():
        target = archive_target(node.key)
        if not target.exists() or not filecmp.cmp(journal, target, shallow=False):
            raise fail(f"{kit.show(journal)} has not been archived, or has changed since – run "
                       f"`plan archive {node.key}` first. Nothing released.")
    if work.exists():
        shutil.rmtree(work)
    print(f"released {kit.show(work)}.")
    return 0


def retro(kit: Kit, node: Node) -> int:
    """Create this run's retro file. One file per run, and the author does not read the others: a
    shared file drifts longer with every author who reads the entries above before writing."""
    kit.retro_dir.mkdir(parents=True, exist_ok=True)
    path = kit.retro_dir / f"{date.today().isoformat()}-{node.key}.md"
    if any(kit.retro_dir.glob(f"*-{node.key}.md")):
        raise fail(f"a retro for {node.key} already exists in {kit.show(kit.retro_dir)}")
    path.write_text(
        f"# Retro · {node.title}\n\n"
        + "".join(f"**{label}.** \n\n" for label in RETRO_LABELS).rstrip() + "\n",
        encoding="utf-8")
    print(f"wrote {kit.show(path)} – five labelled lines, about what the workflow cost, not what "
          f"the feature did. Do not read the other entries first. `nothing` is a real answer to "
          f"Cheaper and Faster; `none: one-off` is a real answer to Fix.")
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Checks
# ──────────────────────────────────────────────────────────────────────────────


def check_workflow(name: str, workflow: dict) -> list[str]:
    problems: list[str] = []
    names = column_names(workflow)
    for duplicate in sorted({n for n in names if names.count(n) > 1}):
        problems.append(f"column `{duplicate}` appears more than once – run a shared column twice "
                        f"with `as:`")
    for key in ("unattended_from", "agreed_at"):
        if workflow.get(key) is not None and workflow[key] not in names:
            problems.append(f"`{key}` names {workflow[key]!r}, which is not a column")
    unattended = unattended_columns(workflow)

    for column in workflow.get("columns") or []:
        where = f"column `{column.get('name')}`"
        if not column.get("entry"):
            problems.append(f"{where} has no `entry`")
        if not column.get("produces"):
            problems.append(f"{where} has no `produces` – a gate can pass on a column that left "
                            f"nothing durable")
        if not column.get("exit"):
            problems.append(f"{where} has no `exit` – nothing says when it is finished")
        for entry in (column.get("exit") or []) + (column.get("precondition") or []):
            kinds = [k for k in EXIT_KINDS if k in (entry or {})]
            if len(kinds) != 1:
                problems.append(f"{where}: exit {entry!r} must carry exactly one of "
                                f"{' · '.join(EXIT_KINDS)}")
                continue
            if kinds == ["attest"] and entry.get("blocking"):
                problems.append(f"{where}: an `attest` is marked blocking – an exit a person must "
                                f"answer is a `human_gate`")
            if (kinds == ["human_gate"] and column.get("name") in unattended
                    and not entry.get("blocking")):
                problems.append(f"{where}: a non-blocking human gate in the unattended stretch – "
                                f"make it `blocking: true` or an `attest`: {entry['human_gate']!r}")
        for entry in column.get("precondition") or []:
            if "command" not in (entry or {}):
                problems.append(f"{where}: a `precondition` must be a command")

        compact = column.get("compact")
        if compact is not None:
            if not isinstance(compact, dict):
                problems.append(f"{where}: `compact` must be `offer` + `carry`, or `never`")
            else:
                if unknown := sorted(set(compact) - COMPACT_KEYS):
                    problems.append(f"{where}: `compact` carries unknown {', '.join(unknown)}")
                if "never" in compact and ("offer" in compact or "carry" in compact):
                    problems.append(f"{where}: `compact` marks the boundary both ways")
                elif "never" not in compact:
                    for needed in ("offer", "carry"):
                        if not compact.get(needed):
                            problems.append(f"{where}: `compact` has no `{needed}`")

        delegate = column.get("delegate")
        if delegate is not None:
            if not isinstance(delegate, dict):
                problems.append(f"{where}: `delegate` must be a mapping")
            else:
                if unknown := sorted(set(delegate) - DELEGATE_KEYS):
                    problems.append(f"{where}: `delegate` carries unknown {', '.join(unknown)}")
                for needed in sorted(DELEGATE_KEYS):
                    if not delegate.get(needed):
                        problems.append(f"{where}: `delegate` has no `{needed}`")

        if review := review_block(column):
            _, block = review
            if not isinstance(block, dict):
                problems.append(f"{where}: the per-unit review must be a mapping")
            else:
                if unknown := sorted(set(block) - REVIEW_KEYS):
                    problems.append(f"{where}: the per-unit review carries unknown "
                                    f"{', '.join(unknown)}")
                for needed in ("suspicion", "escalate"):
                    if not block.get(needed):
                        problems.append(f"{where}: the per-unit review has no `{needed}`")
            if delegate is None:
                problems.append(f"{where}: reviews each unit but does not delegate – a review of "
                                f"a unit needs a unit")
    return [f"workflow `{name}`: {p}" for p in problems]


def check_templates(kit: Kit, bound: set[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    definitions = slot_definitions(kit)
    values = slot_values(kit)
    used: set[str] = set()

    for name, body in definitions.items():
        for needed in ("what", "by_hand", "example"):
            if not body.get(needed):
                errors.append(f"slot `{name}` has no `{needed}`")

    for name in workflow_names(kit):
        try:
            joined = join_workflow(kit, name)
        except SystemExit as exc:
            errors.append(str(exc))
            continue
        # A mode is not applied by the kit, but the slots it uses are still used.
        used |= slots_in(joined.pop("modes", None))
        errors.extend(check_workflow(name, joined))
        needs = slots_in(joined)
        used |= needs
        for slot in sorted(needs - set(definitions)):
            errors.append(f"workflow `{name}` uses `{{{{{slot}}}}}`, which slots.yaml does not define")
        if name in bound:
            for slot in sorted((needs & set(definitions)) - set(values)):
                errors.append(f"workflow `{name}` is bound by a feature and slot `{slot}` has no "
                              f"value")

    for slot in sorted(set(definitions) - used):
        warnings.append(f"slot `{slot}` is defined and no workflow uses it")
    for slot in sorted(set(values) - set(definitions)):
        warnings.append(f"a value is given for `{slot}`, which slots.yaml does not define")
    return errors, warnings


def names_a_destination(text: str, keys: set[str]) -> bool:
    """A note addressed to nobody in particular has no route. A bare `#12` does not count: issues
    and pull requests share one sequence, so it cannot be told from a merged change."""
    if re.search(r"issue #\d+|/issues/\d+", text):
        return True
    return any(key in text for key in keys)


def check_tree(kit: Kit, tree: Tree, graph: Graph) -> tuple[list[str], list[str]]:
    errors = list(tree.errors)
    warnings: list[str] = []
    known = set(workflow_names(kit))
    joined: dict[str, dict] = {}

    def err(node: Node, message: str) -> None:
        errors.append(f"{node.rel}: {message}")

    def warn(node: Node, message: str) -> None:
        warnings.append(f"{node.rel}: {message}")

    for key, nodes in tree.by_key().items():
        if len(nodes) > 1:
            errors.append(f"`{key}` names {len(nodes)} nodes – `blocked_by` resolves by name: "
                          + ", ".join(n.rel for n in nodes))
    for node, ref in graph.unresolved:
        err(node, f"`blocked_by: {ref}` resolves to no node, or to more than one")
    for cycle in graph.cycles():
        errors.append("a `blocked_by` cycle: " + " → ".join(cycle))

    all_keys = {n.key for n in tree.nodes}
    for node in tree.nodes:
        if not node.frontmatter.get("title"):
            err(node, "no `title`")
        if section(node.body, "Goal") is None:
            err(node, "no `## Goal`")
        if section(node.body, "Done-when") is None:
            err(node, "no `## Done-when`")

        if node.level != "feature":
            if node.is_leaf:
                err(node, f"a {node.level} with nothing under it")
            if section(node.body, "Boundaries") is None:
                err(node, "no `## Boundaries` – where this stops is invisible without it")
            for forbidden in ("status", "workflow", "column"):
                if forbidden in node.frontmatter:
                    err(node, f"`{forbidden}` on a {node.level} – only a feature carries one. "
                              f"Everything above a feature is derived")
            if section(node.body, "Record") is not None:
                err(node, "`## Record` on a container – only a feature is executed")
            if "target" in node.frontmatter and node.level != "milestone":
                err(node, f"`target:` on a {node.level} – only a milestone has an acceptance date. "
                          f"A timebox is not a node")
            if node.level == "milestone" and gate_criteria(node):
                answered, _ = coverage(node)
                for criterion, features in answered.items():
                    if not features:
                        err(node, f"criterion `{criterion}` has no feature tracing to it")
                    elif len(features) == 1:
                        warn(node, f"criterion `{criterion}` is answered by one feature, "
                                   f"{features[0].key} – one slip there is a slip of the milestone")
            continue

        if not node.is_leaf:
            err(node, "a feature with nodes under it")
        status = node.status
        if status not in STATUSES:
            err(node, f"status {status!r} is not one of {' · '.join(STATUSES)}")
            continue

        unmet = graph.unmet(node)
        blockers = graph.blockers[node.rel]
        if status == "blocked" and blockers and not unmet:
            err(node, "status is `blocked` and every blocker is done")
        if status in ("ready", "in-progress") and unmet:
            err(node, f"status is `{status}` while waiting on "
                      + ", ".join(b.key for b in unmet))
        if status in ("ready", "blocked") and not is_briefed(node):
            err(node, f"status is `{status}` with no packet – it needs `## Acceptance criteria` "
                      f"and `## Verification`, or the status `no-packet`")
        if is_briefed(node) and section(node.body, TIE_BREAKER) is None:
            err(node, f"a packet with no `## {TIE_BREAKER}` – the direction to lean when the "
                      f"criteria are silent")
        if "target" in node.frontmatter:
            err(node, "`target:` on a feature – only a milestone has an acceptance date")

        milestone = node.milestone
        declared = gate_criteria(milestone) if milestone else []
        if declared:
            traced = traced_gates(node)
            if traced is None or traced == []:
                err(node, f"`traces.gate` is neither a list nor `{INHERIT}` – {milestone.key} "
                          f"declares criteria, so say which this answers, or that it serves its "
                          f"parent's")
            elif isinstance(traced, list):
                for criterion in traced:
                    if criterion not in declared:
                        err(node, f"traces gate `{criterion}`, which {milestone.key} does not "
                                  f"declare")

        workflow, column = node.workflow, node.frontmatter.get("column")
        if not workflow and status not in PRE_WORKFLOW:
            err(node, "no `workflow:`")
        if workflow and workflow not in known:
            warn(node, f"workflow `{workflow}` has no template yet")
        if node.frontmatter.get("mode"):
            warn(node, "`mode:` is not applied by the kit yet – the full workflow is what runs")
        if status in PRE_WORKFLOW and column:
            err(node, f"`column:` on a `{status}` feature – that status sits before the workflow")
        if column and workflow in known:
            if workflow not in joined:
                try:
                    joined[workflow] = join_workflow(kit, workflow)
                except SystemExit:
                    joined[workflow] = {}
            if column not in column_names(joined[workflow]):
                err(node, f"`column: {column}` is not a column of `{workflow}`")
        if status in IN_FLIGHT and not column:
            warn(node, "in flight with no `column:` – the claim did not record which loop this "
                       "is running")
        if status == "done" and column:
            warn(node, "`column:` on a finished feature – the close did not remove it")

        parts = record_parts(node)
        has_record = section(node.body, "Record") is not None
        for heading in parts:
            if heading not in RECORD_HEADINGS:
                err(node, f"`### {heading}` is not a record heading – the set is closed: "
                          + " · ".join(RECORD_HEADINGS))
        if status == "done":
            if not has_record:
                err(node, "done with no `## Record`")
            else:
                if not parts.get("Lesson"):
                    err(node, "the record has no filled-in `### Lesson`")
                if not (parts.get("Decisions taken") or parts.get(CARRIED_FORWARD)):
                    err(node, "the record has neither `### Decisions taken` nor "
                              f"`### {CARRIED_FORWARD}` filled in – say so in one of them if "
                              "there was nothing")
            if not node.frontmatter.get("merged"):
                warn(node, "done with no `merged:` date")
            carried = parts.get(CARRIED_FORWARD)
            if (carried and not graph.has_dependent(node)
                    and not names_a_destination(carried, all_keys - {node.key})):
                warn(node, f"`### {CARRIED_FORWARD}` has no reader – no feature depends on this "
                           f"one and no entry names an issue or a feature")
    return errors, warnings


def check_retros(kit: Kit) -> list[str]:
    problems = []
    if not kit.retro_dir.is_dir():
        return problems
    for path in sorted(kit.retro_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        lines = len(text.splitlines())
        if lines > RETRO_CEILING:
            problems.append(f"{kit.show(path)}: {lines} lines, over the ceiling of "
                            f"{RETRO_CEILING} – name where the rest belongs instead")
        for label in RETRO_LABELS:
            if not re.search(rf"\*\*{label}\.?\*\*", text):
                problems.append(f"{kit.show(path)}: no **{label}** line")
    return problems


def check(kit: Kit) -> int:
    tree = load_tree(kit)
    graph = Graph(tree)
    bound = {n.workflow for n in tree.nodes if n.workflow and n.status not in PRE_WORKFLOW}
    template_errors, template_warnings = check_templates(kit, bound)
    tree_errors, tree_warnings = check_tree(kit, tree, graph)
    errors = template_errors + tree_errors + check_retros(kit)
    warnings = template_warnings + tree_warnings
    for warning in warnings:
        print(f"warn   {warning}", file=sys.stderr)
    for error in errors:
        print(f"error  {error}", file=sys.stderr)
    features = [n for n in tree.nodes if n.level == "feature"]
    if errors:
        print(f"\n{plural(len(errors), 'error')}, {plural(len(warnings), 'warning')}.",
              file=sys.stderr)
        return 1
    print(f"plan ok – {plural(len(tree.nodes), 'node')}, {plural(len(features), 'feature')}, "
          f"{plural(len(workflow_names(kit)), 'workflow')}, {plural(len(warnings), 'warning')}.")
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# The queue – position, never priority
# ──────────────────────────────────────────────────────────────────────────────


def work(kit: Kit, tree: Tree, graph: Graph, show_all: bool) -> int:
    features = [n for n in tree.nodes if n.level == "feature"]
    counts = defaultdict(int)
    for node in features:
        counts[node.status or "unset"] += 1
    print(" · ".join(f"{counts[s]} {s}" for s in STATUSES if counts[s]) or "no features")
    waves = graph.waves()

    def position(node: Node) -> str:
        column = node.frontmatter.get("column")
        if not (node.workflow and column):
            return node.workflow or "no workflow"
        try:
            names = column_names(join_workflow(kit, node.workflow))
        except SystemExit:
            return f"{node.workflow} · {column}"
        where = f"{names.index(column) + 1}/{len(names)}" if column in names else "?"
        return f"{node.workflow} · {column} {where}"

    def group(title: str, nodes: list[Node], line) -> None:
        if not nodes:
            return
        print(f"\n{title}")
        for node in sorted(nodes, key=lambda n: (waves.get(n.rel, 0), n.rel)):
            print(f"  {node.key} – {node.title}")
            print(f"    {line(node)}")

    group("In flight", [n for n in features if n.status in IN_FLIGHT],
          lambda n: f"{position(n)} · the journal says how far it has got\n"
                    f"    plan prompt {n.key} --column <column>")
    group("Ready", [n for n in features if n.status == "ready"],
          lambda n: f"{position(n)} · wave {waves.get(n.rel, '?')}\n    plan prompt {n.key}")
    group("Needs design", [n for n in features if n.status == "design"],
          lambda n: PRE_WORKFLOW["design"])
    group("Blocked", [n for n in features if n.status == "blocked"],
          lambda n: "waits on " + (", ".join(b.key for b in graph.unmet(n)) or "nothing – stale"))
    if show_all:
        group("No packet", [n for n in features if n.status == "no-packet"],
              lambda n: PRE_WORKFLOW["no-packet"])
    return 0


def view(tree: Tree, graph: Graph, node: Node | None) -> int:
    """The census for one node, or for the whole plan. Facts a program can compute from the
    features, and no judgement: no percentage, no verdict, nothing stored."""
    features = node.features if node else [n for n in tree.nodes if n.level == "feature"]
    print(f"{node.level.capitalize()} · {node.title}" if node else "The whole plan")
    counts = defaultdict(int)
    for feature in features:
        counts[feature.status or "unset"] += 1
    print("  " + (" · ".join(f"{counts[s]} {s}" for s in STATUSES if counts[s]) or "no features"))

    below = node.features if node else None
    milestones = [n for n in tree.nodes if n.level == "milestone" and gate_criteria(n)
                  and (node is None or n in node.ancestry or n in _under(node))]
    for milestone in milestones:
        answered, blanket = coverage(milestone)
        print(f"\nCriteria · {milestone.title}")
        for criterion, tracing in answered.items():
            if below is not None:
                tracing = [f for f in tracing if f in below]
            done = sum(1 for f in tracing if f.status == "done")
            note = ("  ← nothing points at it" if not tracing
                    else "  ← answered once" if len(tracing) == 1 else "")
            print(f"  {criterion}  {plural(len(tracing), 'feature')}, {done} done{note}")
        for feature in blanket:
            print(f"  left out of the count: {feature.key} traces every criterion")

    chain = graph.longest_chain(features)
    if len(chain) > 1:
        print(f"\nLongest chain still to run · {len(chain)}")
        print("  " + " → ".join(f.key for f in chain))
    waited = [(len(graph.waiting_on(f)), f) for f in features if f.status != "done"]
    most = max(waited, key=lambda pair: pair[0], default=(0, None))
    if most[0]:
        print(f"\nMost waited on · {most[1].key}")
        print(f"  {plural(most[0], 'unfinished feature')} cannot start until it lands")
    return 0


def _under(node: Node) -> list[Node]:
    return [child for direct in node.children for child in [direct, *_under(direct)]]


# ──────────────────────────────────────────────────────────────────────────────
# Setting up
# ──────────────────────────────────────────────────────────────────────────────

KIT_YAML = """\
# Where the kit finds things. Every path is relative to this file's directory, except `work_dir`,
# which is relative to the repository root.
tree: tree
workflows: workflows
values: values.yaml
retro: retro
work_dir: .work
remote: origin
main: main

# How a claim or a close reaches the main branch.
#   pr    a plan-only pull request, merged when its checks pass
#   push  pushed straight to the main branch – for a repository with no protection on it
#   none  edited in the working copy only; landing it is yours
land: pr

# Your own tooling values, if they are not the kit's. A path, or set PLAN_TOOLING_VALUES.
tooling_values:
"""

VALUES_HEADER = """\
# Your values for the slots the workflows use. Each slot is defined in workflows/slots.yaml, with
# what it needs, how to meet it by hand, and an example from another system.
#
# Fill what the first workflow uses. `plan check` names every slot a bound workflow still needs.
# A value that names you – an archive destination, an account – is written as an environment
# variable, never as the name itself.
"""


def init(target: Path, example: bool) -> int:
    plan = target / "plan"
    if (plan / "kit.yaml").exists():
        raise fail(f"{plan} already holds a plan – nothing written")
    if not (TEMPLATES / "workflows" / "core.yaml").exists():
        raise fail(f"the workflow templates are not at {TEMPLATES}")
    (plan / "tree").mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATES / "workflows", plan / "workflows",
                    ignore=shutil.ignore_patterns("README.md"))
    (plan / "kit.yaml").write_text(KIT_YAML, encoding="utf-8")

    slots = yaml.safe_load((plan / "workflows" / "slots.yaml").read_text(encoding="utf-8"))
    project = slots.get("project") or {}
    if example:
        shutil.copytree(KIT_DIR / "example" / "tree", plan / "tree", dirs_exist_ok=True)
        body = {"project": {name: inline(slot["example"]) for name, slot in project.items()}}
        text = VALUES_HEADER + "\n" + yaml.safe_dump(body, sort_keys=False, width=100,
                                                     allow_unicode=True)
    else:
        text = VALUES_HEADER + "\nproject:\n" + "".join(
            f"  # {inline(slot.get('what', ''))}\n  {name}:\n" for name, slot in project.items())
    (plan / "values.yaml").write_text(text, encoding="utf-8")

    ignore = target / ".gitignore"
    present = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
    if ".work/" not in present:
        ignore.write_text(present + ("" if not present or present.endswith("\n") else "\n")
                          + ".work/\n", encoding="utf-8")
    print(f"wrote {plan} – the workflows, kit.yaml and values.yaml"
          + (", with the example plan and example values." if example else
             ". Fill values.yaml, write the tree, then run `plan check`."))
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Command line
# ──────────────────────────────────────────────────────────────────────────────


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="plan", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    def feature_command(name: str, help_text: str) -> argparse.ArgumentParser:
        command = sub.add_parser(name, help=help_text)
        command.add_argument("feature", help="a feature's name, or its path under the tree")
        return command

    setup = sub.add_parser("init", help="write a plan directory into a repository")
    setup.add_argument("directory", type=Path)
    setup.add_argument("--example", action="store_true",
                       help="also write the example plan, with every project slot filled from "
                            "its example")

    sub.add_parser("check", help="the templates, the tree and the retros – fails on any error")

    queue = sub.add_parser("work", help="unfinished features, and the command that briefs each")
    queue.add_argument("--all", action="store_true", dest="show_all",
                       help="also list features with no packet")

    census = sub.add_parser("view", help="the census for one node, or the whole plan – computed, "
                                         "never stored")
    census.add_argument("node", nargs="?", help="a node's name or path (default: the whole plan)")

    shown = feature_command("show", "one feature's frontmatter")
    shown.add_argument("--field", help="print one field's value and nothing else")

    resolved = sub.add_parser("resolve", help="one workflow, joined and filled, as YAML")
    resolved.add_argument("workflow")
    resolved.add_argument("--mode", help="not applied yet – see the kit's README")
    resolved.add_argument("-o", "--output", type=Path)

    brief = feature_command("prompt", "assemble the brief for a feature")
    brief.add_argument("--column", help="the column to start at (default: the plan's, else the first)")
    brief.add_argument("--column-only", action="store_true",
                       help="that column alone, without the columns after it")
    brief.add_argument("-o", "--output", type=Path)

    entered = feature_command("enter", "enter a column – record it, then print it")
    entered.add_argument("column")
    checked = feature_command("enter-check", "pass if this is the most recent column entered")
    checked.add_argument("column")

    claimed = feature_command("claim", "mark a ready feature in progress")
    claimed.add_argument("--land", action="store_true", help="put the claim on the main branch")
    feature_command("claim-check", "pass if the claim is on the main branch and in this branch")

    closed = feature_command("close", "mark a merged feature done")
    closed.add_argument("--pr", type=int, required=True, help="the merged pull request")
    closed.add_argument("--merged", help="the merge date, where there is no code host to read it "
                                         "from")
    closed.add_argument("--land", action="store_true", help="put the close on the main branch")
    feature_command("close-check", "pass if the feature reads done on the main branch")

    feature_command("retro", "create this run's retro file")
    feature_command("archive", "copy the journal to PLAN_JOURNAL_ARCHIVE, and read it back")
    feature_command("release", "remove the feature's working state, once the journal is archived")

    args = parser.parse_args(argv)
    if args.command == "init":
        return init(args.directory.resolve(), args.example)

    kit = Kit.find()
    if args.command == "check":
        return check(kit)
    if args.command == "resolve":
        if args.mode:
            raise fail(f"modes are not applied by the kit yet – `{args.mode}` is resolved by hand, "
                       f"from the mode's own block in the workflow file")
        text = (f"# Resolved from core.yaml, {args.workflow}.yaml and the slot values on "
                f"{date.today().isoformat()}.\n# Do not edit – change the sources and resolve "
                f"again.\n"
                + yaml.safe_dump(resolve_workflow(kit, args.workflow), sort_keys=False, width=100,
                                 allow_unicode=True))
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
            print(f"wrote {args.output}")
        else:
            sys.stdout.write(text)
        return 0

    tree = load_tree(kit)
    if tree.errors:
        for error in tree.errors:
            print(f"error  {error}", file=sys.stderr)
        raise fail("the tree has structural errors – fix those first")
    graph = Graph(tree)
    if args.command == "work":
        return work(kit, tree, graph, args.show_all)
    if args.command == "view":
        return view(tree, graph, resolve_node(tree, args.node) if args.node else None)

    node = resolve_node(tree, args.feature)
    if args.command == "show":
        if args.field:
            value = node.frontmatter.get(args.field)
            if value is None:
                return 1
            print(value)
        else:
            sys.stdout.write(yaml.safe_dump(node.frontmatter, sort_keys=False, allow_unicode=True))
        return 0
    if args.command == "prompt":
        text = build_brief(kit, tree, graph, node, args.column, args.column_only)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
            print(f"wrote {args.output} – {plural(len(text.split()), 'word')}, "
                  f"{words_before_column(text)} before the sentence naming the column.")
        else:
            sys.stdout.write(text)
        return 0
    if args.command == "enter":
        sys.stdout.write(enter_column(kit, node, args.column))
        return 0
    if args.command == "enter-check":
        return enter_check(kit, node, args.column)
    if args.command == "claim":
        return claim(kit, node, args.land)
    if args.command == "claim-check":
        return claim_check(kit, node)
    if args.command == "close":
        return close(kit, node, args.pr, args.merged, args.land)
    if args.command == "close-check":
        return close_check(kit, node)
    if args.command == "retro":
        return retro(kit, node)
    if args.command == "archive":
        return archive(kit, node)
    if args.command == "release":
        return release(kit, node)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
