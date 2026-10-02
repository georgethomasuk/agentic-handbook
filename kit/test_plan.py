"""Tests for the kit. Run with `scripts/test-kit.sh`, or `python -m unittest` from this directory.

Every test builds its own plan in a temporary directory from the shipped templates and the example
plan, so nothing here depends on the state of a repository – a fresh checkout passes.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan  # noqa: E402

RATE_LIMIT = "feature_checkin_rate_limit"
TOKEN = "feature_anonymous_checkin_token"
SLICE = ("plan/tree/mission_platform_build/milestone_checkin_window_opens/"
         "slice_staff_complete_a_checkin")

GIT_ENV = {
    "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
}

# A stand-in for the code host's command line. It records every call, and `pr merge` does what a
# merge does – puts the branch on the main branch – so the commands after it see a real result.
FAKE_GH = """#!/usr/bin/env bash
echo "$*" | tr '\\n' ' ' >> "$GH_LOG"
echo >> "$GH_LOG"
case "$1 $2" in
  "pr create") exit 0 ;;
  "pr checks") [ -n "$GH_NO_CHECKS" ] && { echo "no checks reported on the branch" >&2; exit 1; }
               exit "${GH_CHECKS_EXIT:-0}" ;;
  "pr merge")  git push -q origin "HEAD:main" ;;
  "pr view")   if [ -n "$GH_VIEW" ]; then echo "$GH_VIEW"
               else echo '{"state":"MERGED","mergedAt":"2026-10-01T10:00:00Z"}'; fi ;;
esac
"""


def sh(*args: str, cwd: Path) -> str:
    done = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if done.returncode != 0:
        raise AssertionError(f"{' '.join(args)} failed: {done.stderr}")
    return done.stdout.strip()


def quiet(function, *args, **kwargs):
    """Call a kit function, returning (result, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        result = function(*args, **kwargs)
    return result, out.getvalue(), err.getvalue()


class PlanCase(unittest.TestCase):
    """A repository holding the example plan, with a bare remote behind it."""

    land = "none"

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name).resolve()
        self._environ = dict(os.environ)
        self.addCleanup(self._restore_environ)
        os.environ.update(GIT_ENV)
        os.environ.pop("PLAN_ROOT", None)
        os.environ.pop("PLAN_TOOLING_VALUES", None)
        os.environ.pop("PLAN_JOURNAL_ARCHIVE", None)

        self.remote = self.base / "remote.git"
        self.repo = self.base / "repo"
        sh("git", "init", "-q", "--bare", "-b", "main", str(self.remote), cwd=self.base)
        sh("git", "clone", "-q", str(self.remote), str(self.repo), cwd=self.base)
        quiet(plan.init, self.repo, True)
        config = self.repo / "plan" / "kit.yaml"
        config.write_text(config.read_text().replace("land: pr", f"land: {self.land}"))
        sh("git", "add", "-A", cwd=self.repo)
        sh("git", "commit", "-q", "-m", "the plan", cwd=self.repo)
        sh("git", "push", "-q", "-u", "origin", "main", cwd=self.repo)
        self.kit = plan.Kit.load(self.repo / "plan")

    def _restore_environ(self) -> None:
        os.environ.clear()
        os.environ.update(self._environ)

    def load(self) -> tuple[plan.Tree, plan.Graph]:
        tree = plan.load_tree(self.kit)
        return tree, plan.Graph(tree)

    def node(self, key: str) -> plan.Node:
        return plan.resolve_node(self.load()[0], key)

    def feature_path(self, key: str) -> Path:
        return self.repo / SLICE / f"{key}.md"

    def edit(self, key: str, old: str, new: str) -> None:
        path = self.feature_path(key)
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new))

    def brief(self, key: str = RATE_LIMIT, column: str | None = None, only: bool = False) -> str:
        tree, graph = self.load()
        return plan.build_brief(self.kit, tree, graph, plan.resolve_node(tree, key), column, only)

    def tree_findings(self) -> tuple[list[str], list[str]]:
        tree, graph = self.load()
        return plan.check_tree(self.kit, tree, graph)


class ResolveTests(PlanCase):
    def test_every_workflow_resolves_with_nothing_left_to_look_up(self) -> None:
        names = plan.workflow_names(self.kit)
        self.assertEqual(len(names), 7)
        for name in names:
            resolved = plan.resolve_workflow(self.kit, name, RATE_LIMIT)
            text = json.dumps(resolved)
            self.assertNotIn("{{", text, name)
            self.assertNotIn("<feature>", text, name)
            self.assertFalse([c for c in resolved["columns"] if "use" in c], name)
            columns = plan.column_names(resolved)
            self.assertEqual(len(columns), len(set(columns)), name)
            for protocol in plan.PROTOCOLS:
                self.assertIn(protocol, resolved, name)

    def test_use_copies_the_shared_column_whole(self) -> None:
        core = plan.load_yaml(self.kit.workflows_dir / "core.yaml")
        shared = next(c for c in core["columns"] if c["name"] == "open")
        joined = plan.join_workflow(self.kit, "build-in-repository")
        self.assertEqual(next(c for c in joined["columns"] if c["name"] == "open"), shared)

    def test_also_appends_text_and_exits_to_the_shared_column(self) -> None:
        core = plan.load_yaml(self.kit.workflows_dir / "core.yaml")
        shared = next(c for c in core["columns"] if c["name"] == "build-plan")
        joined = plan.join_workflow(self.kit, "contract-change")
        column = next(c for c in joined["columns"] if c["name"] == "build-plan")
        self.assertTrue(column["entry"].startswith(shared["entry"].rstrip()))
        self.assertIn("Cutting matters most on this workflow", column["entry"])
        self.assertGreater(len(column["exit"]), len(shared["exit"]))
        self.assertEqual(column["exit"][: len(shared["exit"])], shared["exit"])

    def test_as_runs_a_shared_column_under_another_name(self) -> None:
        columns = plan.column_names(plan.join_workflow(self.kit, "contract-change"))
        self.assertIn("proposal-review", columns)
        self.assertIn("implementation-review", columns)
        self.assertNotIn("panel", columns)

    def test_seeds_stay_on_the_panel(self) -> None:
        joined = plan.join_workflow(self.kit, "build-in-repository")
        panel = next(c for c in joined["columns"] if c["name"] == "panel")
        self.assertEqual(len(panel["seeds"]), 4)

    def test_standing_constraints_are_the_cores_then_the_workflows(self) -> None:
        core = plan.load_yaml(self.kit.workflows_dir / "core.yaml")["standing_constraints"]
        joined = plan.join_workflow(self.kit, "acceptance")["standing_constraints"]
        self.assertEqual(joined[: len(core)], core)
        self.assertGreater(len(joined), len(core))

    def test_an_unfilled_slot_stops_the_resolve_and_is_named(self) -> None:
        values = self.repo / "plan" / "values.yaml"
        kept = [line for line in values.read_text().splitlines()
                if not line.startswith("  full_gate:")]
        values.write_text("\n".join(kept) + "\n")
        with self.assertRaises(SystemExit) as raised:
            plan.resolve_workflow(self.kit, "build-in-repository")
        self.assertIn("project.full_gate", str(raised.exception))
        self.assertNotIn("make check", str(raised.exception))

    def test_the_plans_values_win_over_the_kits(self) -> None:
        values = self.repo / "plan" / "values.yaml"
        values.write_text(values.read_text() + "tooling:\n  reading_tier: the cheapest tier\n")
        resolved = plan.resolve_workflow(self.kit, "build-in-repository")
        check = next(c for c in resolved["columns"] if c["name"] == "check")
        self.assertEqual(check["delegate"]["model"], "the cheapest tier")


class TemplateCheckTests(PlanCase):
    def test_the_shipped_templates_are_clean(self) -> None:
        errors, warnings = plan.check_templates(self.kit, set(plan.workflow_names(self.kit)))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def sound(self) -> dict:
        return {
            "unattended_from": "build",
            "columns": [
                {"name": "frame", "entry": "e", "produces": ["p"],
                 "exit": [{"human_gate": "agreed", "blocking": True}]},
                {"name": "build", "entry": "e", "produces": ["p"], "exit": [{"attest": "done"}]},
            ],
        }

    def problems(self, mutate) -> str:
        workflow = self.sound()
        mutate(workflow)
        return "\n".join(plan.check_workflow("w", workflow))

    def test_a_sound_workflow_has_no_problems(self) -> None:
        self.assertEqual(self.problems(lambda w: None), "")

    def test_a_human_gate_in_the_unattended_stretch_must_be_blocking(self) -> None:
        def mutate(w):
            w["columns"][1]["exit"] = [{"human_gate": "looks fine"}]
        self.assertIn("non-blocking human gate in the unattended stretch", self.problems(mutate))

    def test_the_same_gate_before_the_stretch_is_allowed(self) -> None:
        def mutate(w):
            w["columns"][0]["exit"] = [{"human_gate": "looks fine"}]
        self.assertEqual(self.problems(mutate), "")

    def test_an_exit_carries_exactly_one_kind(self) -> None:
        def mutate(w):
            w["columns"][1]["exit"] = [{"attest": "a", "command": "true"}]
        self.assertIn("exactly one of", self.problems(mutate))

    def test_an_attest_cannot_block(self) -> None:
        def mutate(w):
            w["columns"][1]["exit"] = [{"attest": "a", "blocking": True}]
        self.assertIn("`attest` is marked blocking", self.problems(mutate))

    def test_compaction_says_which_kind_of_boundary(self) -> None:
        def both(w):
            w["columns"][0]["compact"] = {"offer": "o", "carry": ["c"], "never": "n"}
        self.assertIn("both ways", self.problems(both))

        def no_carry(w):
            w["columns"][0]["compact"] = {"offer": "o"}
        self.assertIn("no `carry`", self.problems(no_carry))

        def typo(w):
            w["columns"][0]["compact"] = {"nver": "n"}
        self.assertIn("unknown nver", self.problems(typo))

    def test_delegation_must_say_what_is_kept(self) -> None:
        def mutate(w):
            w["columns"][1]["delegate"] = {"model": "m", "send": "s", "escalate": "e"}
        self.assertIn("`delegate` has no `keep`", self.problems(mutate))

    def test_a_per_unit_review_needs_a_unit(self) -> None:
        def mutate(w):
            w["columns"][1]["review_each_step"] = {"suspicion": "s", "escalate": "e"}
        self.assertIn("does not delegate", self.problems(mutate))

    def test_a_column_must_say_what_it_leaves_behind(self) -> None:
        def mutate(w):
            del w["columns"][1]["produces"]
        self.assertIn("no `produces`", self.problems(mutate))

    def test_unattended_from_must_name_a_column(self) -> None:
        def mutate(w):
            w["unattended_from"] = "nowhere"
        self.assertIn("is not a column", self.problems(mutate))

    def test_a_slot_no_workflow_defines_is_an_error(self) -> None:
        path = self.kit.workflows_dir / "build-in-repository.yaml"
        path.write_text(path.read_text().replace("{{project.lockfile}}", "{{project.lokfile}}"))
        errors, _ = plan.check_templates(self.kit, set())
        self.assertTrue(any("project.lokfile" in e for e in errors))

    def test_a_slot_nothing_uses_is_a_warning(self) -> None:
        path = self.kit.workflows_dir / "slots.yaml"
        path.write_text(path.read_text() + "\n  spare:\n    what: w\n    by_hand: b\n    example: e\n")
        errors, warnings = plan.check_templates(self.kit, set())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, ["slot `tooling.spare` is defined and no workflow uses it"])

    def test_a_bound_workflow_with_an_unfilled_slot_is_an_error(self) -> None:
        values = self.repo / "plan" / "values.yaml"
        values.write_text("\n".join(line for line in values.read_text().splitlines()
                                    if not line.startswith("  full_gate:")) + "\n")
        bound, _ = plan.check_templates(self.kit, {"build-in-repository"})
        self.assertTrue(any("slot `project.full_gate` has no value" in e for e in bound))
        self.assertEqual(plan.check_templates(self.kit, set())[0], [])


class TreeCheckTests(PlanCase):
    def test_the_example_plan_is_clean(self) -> None:
        self.assertEqual(self.tree_findings(), ([], []))
        result, out, _ = quiet(plan.check, self.kit)
        self.assertEqual(result, 0)
        self.assertIn("plan ok", out)

    def errors(self) -> str:
        return "\n".join(self.tree_findings()[0])

    def test_ready_while_a_blocker_is_unfinished(self) -> None:
        self.edit(TOKEN, "status: done", "status: in-progress")
        self.assertIn(f"status is `ready` while waiting on {TOKEN}", self.errors())

    def test_a_dependency_that_names_nothing(self) -> None:
        self.edit(RATE_LIMIT, f"blocked_by: [{TOKEN}]", "blocked_by: [feature_nowhere]")
        self.assertIn("`blocked_by: feature_nowhere` resolves to no node", self.errors())

    def test_ready_needs_a_packet(self) -> None:
        self.edit(RATE_LIMIT, "## Acceptance criteria", "## Criteria")
        self.assertIn("status is `ready` with no packet", self.errors())

    def test_the_record_headings_are_closed(self) -> None:
        self.edit(TOKEN, "### Carried forward", "### Carried forwards")
        self.assertIn("`### Carried forwards` is not a record heading", self.errors())

    def test_done_needs_a_lesson(self) -> None:
        self.edit(TOKEN, "### Lesson", "### Review")
        self.assertIn("no filled-in `### Lesson`", self.errors())

    def test_a_record_section_holding_only_a_comment_is_empty(self) -> None:
        text = self.feature_path(TOKEN).read_text()
        head, _, _ = text.partition("### Lesson")
        self.feature_path(TOKEN).write_text(head + "### Lesson\n\n<!-- the one thing -->\n")
        self.assertIn("no filled-in `### Lesson`", self.errors())

    def test_a_column_the_workflow_does_not_have(self) -> None:
        self.edit(RATE_LIMIT, "status: ready", "status: ready\ncolumn: nowhere")
        self.assertIn("`column: nowhere` is not a column of `build-in-repository`", self.errors())

    def test_status_belongs_to_features_only(self) -> None:
        readme = self.repo / SLICE / "README.md"
        readme.write_text(readme.read_text().replace("---\ntitle", "---\nstatus: ready\ntitle", 1))
        self.assertIn("`status` on a slice", self.errors())

    def test_a_level_in_the_wrong_place(self) -> None:
        (self.repo / SLICE / "milestone_misplaced").mkdir()
        (self.repo / SLICE / "milestone_misplaced" / "README.md").write_text("---\ntitle: x\n---\n")
        self.assertIn("a milestone cannot sit inside a slice", self.errors())

    def test_carried_forward_with_no_reader_warns(self) -> None:
        self.edit(RATE_LIMIT, f"blocked_by: [{TOKEN}]", "blocked_by: []")
        warnings = "\n".join(self.tree_findings()[1])
        self.assertIn("`### Carried forward` has no reader", warnings)

    def test_carried_forward_naming_an_issue_has_a_reader(self) -> None:
        self.edit(RATE_LIMIT, f"blocked_by: [{TOKEN}]", "blocked_by: []")
        self.edit(TOKEN, "Closes when something bounds", "Raised as issue #12. Closes when something bounds")
        self.assertEqual(self.tree_findings()[1], [])

    def test_a_bare_number_is_not_a_destination(self) -> None:
        self.edit(RATE_LIMIT, f"blocked_by: [{TOKEN}]", "blocked_by: []")
        self.edit(TOKEN, "Closes when something bounds", "See #12. Closes when something bounds")
        self.assertEqual(len(self.tree_findings()[1]), 1)


class BriefTests(PlanCase):
    def test_the_task_comes_before_the_context(self) -> None:
        brief = self.brief()
        task = brief.index("**Start at column `check` – 1 of 12 in `build-in-repository`.**")
        column = brief.index("## Column · `check`")
        context = brief.index("## Standing context")
        tail = brief.index("## The rest of the workflow")
        self.assertLess(task, column)
        self.assertLess(column, context)
        self.assertLess(context, brief.index("\n## This feature\n"))
        self.assertLess(brief.index("\n## This feature\n"), tail)
        self.assertLess(plan.words_before_column(brief), 100)

    def test_carried_forward_is_lifted_from_what_the_feature_depends_on(self) -> None:
        brief = self.brief()
        self.assertIn(f"### From `{TOKEN}` · Anonymous check-in token", brief)
        self.assertIn("A leaked\n  link stays usable until the window closes", brief)

    def test_it_is_lifted_through_a_dependency_of_a_dependency_nearest_first(self) -> None:
        far = self.feature_path("feature_invitation_list")
        far.write_text(self.feature_path(TOKEN).read_text()
                       .replace("Anonymous check-in token", "Invitation list")
                       .replace("The token identifies an invitation", "The list is rebuilt nightly"))
        self.edit(TOKEN, "blocked_by: []", "blocked_by: [feature_invitation_list]")
        brief = self.brief()
        near = brief.index(f"### From `{TOKEN}`")
        self.assertLess(near, brief.index("### From `feature_invitation_list`"))
        self.assertIn("The list is rebuilt nightly", brief)

    def test_a_heading_spelled_any_other_way_is_not_lifted(self) -> None:
        self.edit(TOKEN, "### Carried forward", "### Carried forwards")
        self.assertNotIn("## Carried forward from upstream work", self.brief())

    def test_only_the_record_s_carried_forward_travels(self) -> None:
        brief = self.brief()
        self.assertNotIn("Proving a request came from an invitation", brief)
        self.assertNotIn("The token is issued per invitation", brief)

    def test_boundaries_accumulate_from_every_level_above(self) -> None:
        brief = self.brief()
        for level in ("mission", "milestone", "slice"):
            self.assertIn(f"### From the {level} · ", brief)
        self.assertIn("attributable to a person or a device", brief)

    def test_each_later_column_appears_once_and_the_current_one_is_not_repeated(self) -> None:
        brief = self.brief()
        self.assertNotIn("### `check` – 1 of 12", brief)
        names = plan.column_names(plan.join_workflow(self.kit, "build-in-repository"))
        for position, name in enumerate(names[1:], 2):
            self.assertEqual(brief.count(f"### `{name}` – {position} of 12"), 1, name)

    def test_a_later_start_drops_the_columns_behind_it(self) -> None:
        brief = self.brief(column="prove")
        self.assertIn("**Start at column `prove` – 6 of 12", brief)
        self.assertNotIn("### `frame` –", brief)
        self.assertIn("### `panel` – 7 of 12", brief)

    def test_one_column_alone_carries_no_protocol_it_does_not_use(self) -> None:
        brief = self.brief(column="open", only=True)
        self.assertNotIn("## The rest of the workflow", brief)
        self.assertNotIn("## The journal, and when to compact", brief)
        self.assertNotIn("## Columns that send work to a worker", brief)
        self.assertIn("This brief covers **one** column", brief)
        with_both = self.brief(column="build-execute", only=True)
        self.assertIn("## The journal, and when to compact", with_both)
        self.assertIn("## Columns that send work to a worker", with_both)

    def test_a_column_is_the_same_text_in_the_brief_and_when_entered(self) -> None:
        brief = self.brief()
        entered = plan.enter_column(self.kit, self.node(RATE_LIMIT), "frame")
        body = entered.split("**Entered by:**", 1)[1].split("### Standing constraints", 1)[0]
        self.assertIn(body.strip(), brief)

    def test_an_unclaimed_feature_starts_at_the_first_column_as_a_fact(self) -> None:
        self.assertNotIn("This is assumed", self.brief())

    def test_a_feature_in_flight_with_no_column_says_it_is_guessing(self) -> None:
        self.edit(RATE_LIMIT, "status: ready", "status: in-progress")
        self.assertIn("**This is assumed.**", self.brief())

    def test_the_recorded_column_is_where_a_brief_starts(self) -> None:
        self.edit(RATE_LIMIT, "status: ready", "status: in-progress\ncolumn: frame")
        brief = self.brief()
        self.assertIn("**Start at column `frame` – 3 of 12", brief)
        self.assertNotIn("This is assumed", brief)

    def test_a_feature_with_no_packet_has_no_brief(self) -> None:
        self.edit(RATE_LIMIT, "status: ready", "status: no-packet")
        with self.assertRaises(SystemExit) as raised:
            self.brief()
        self.assertIn("write the packet first", str(raised.exception))

    def test_a_column_the_workflow_does_not_have_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            self.brief(column="nowhere")

    def test_lists_in_a_column_survive(self) -> None:
        brief = self.brief(column="submit", only=True)
        self.assertIn("\n- why the change was needed, and what changed\n- decisions", brief)


class EnterTests(PlanCase):
    def test_entering_records_the_column_then_prints_it(self) -> None:
        text = plan.enter_column(self.kit, self.node(RATE_LIMIT), "frame")
        self.assertTrue(text.startswith("Column `frame` – 3 of 12 in `build-in-repository`."))
        self.assertIn("**Human gate:** design and ownership agreed · **blocking", text)
        self.assertIn("### Standing constraints", text)
        recorded = plan.markers(self.kit, RATE_LIMIT)
        self.assertEqual([m["column"] for m in recorded], ["frame"])
        journal = (self.kit.work(RATE_LIMIT) / "journal.md").read_text()
        self.assertIn("## Column `frame` – entered ", journal)

    def test_the_journal_is_appended_never_rewritten(self) -> None:
        node = self.node(RATE_LIMIT)
        plan.enter_column(self.kit, node, "check")
        journal = self.kit.work(RATE_LIMIT) / "journal.md"
        journal.write_text(journal.read_text() + "\nblockers verified\n")
        plan.enter_column(self.kit, node, "open")
        text = journal.read_text()
        self.assertIn("blockers verified", text)
        self.assertLess(text.index("`check`"), text.index("`open`"))
        self.assertEqual(text.count("# Journal ·"), 1)

    def test_an_unknown_column_is_refused_before_anything_is_written(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            plan.enter_column(self.kit, self.node(RATE_LIMIT), "nowhere")
        self.assertIn("nothing recorded", str(raised.exception))
        self.assertFalse(self.kit.work(RATE_LIMIT).exists())

    def test_the_entry_check_compares_against_the_most_recent_column(self) -> None:
        node = self.node(RATE_LIMIT)
        self.assertEqual(quiet(plan.enter_check, self.kit, node, "check")[0], 1)
        plan.enter_column(self.kit, node, "check")
        self.assertEqual(quiet(plan.enter_check, self.kit, node, "check")[0], 0)
        plan.enter_column(self.kit, node, "open")
        self.assertEqual(quiet(plan.enter_check, self.kit, node, "check")[0], 1)
        self.assertEqual(quiet(plan.enter_check, self.kit, node, "open")[0], 0)

    def test_every_rendered_column_opens_its_exits_with_the_entry_check(self) -> None:
        text = plan.enter_column(self.kit, self.node(RATE_LIMIT), "prove")
        exits = text.split("**This column is finished when:**", 1)[1]
        self.assertTrue(exits.strip().startswith(
            f"- **Command must exit 0:** `plan enter-check {RATE_LIMIT} prove`"))


class ClaimEditTests(PlanCase):
    def test_a_claim_changes_two_lines_and_nothing_else(self) -> None:
        path = self.feature_path(RATE_LIMIT)
        before = path.read_text().splitlines()
        plan.apply_claim(path, "frame")
        after = path.read_text().splitlines()
        self.assertEqual(len(after), len(before) + 1)
        changed = [line for line in after if line not in before]
        self.assertEqual(changed, ["status: in-progress", "column: frame"])

    def test_the_claim_names_the_column_after_open(self) -> None:
        quiet(plan.claim, self.kit, self.node(RATE_LIMIT), False)
        self.assertEqual(self.node(RATE_LIMIT).frontmatter["column"], "frame")
        self.assertEqual(self.tree_findings()[0], [])

    def test_a_feature_that_is_not_ready_is_not_claimed(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            plan.apply_claim(self.feature_path(TOKEN), "frame")
        self.assertIn("status is `done`, expected `ready`", str(raised.exception))

    def test_a_second_claim_is_refused(self) -> None:
        path = self.feature_path(RATE_LIMIT)
        plan.apply_claim(path, "frame")
        with self.assertRaises(SystemExit):
            plan.apply_claim(path, "frame")

    def test_a_close_makes_three_changes(self) -> None:
        path = self.feature_path(RATE_LIMIT)
        plan.apply_claim(path, "frame")
        body_before = path.read_text().split("\n---\n", 1)[1]
        plan.apply_close(path, 57, "2026-10-01")
        frontmatter = self.node(RATE_LIMIT).frontmatter
        self.assertEqual(frontmatter["status"], "done")
        self.assertEqual(frontmatter["pr"], 57)
        self.assertEqual(str(frontmatter["merged"]), "2026-10-01")
        self.assertNotIn("column", frontmatter)
        self.assertEqual(path.read_text().split("\n---\n", 1)[1], body_before)

    def test_a_close_against_a_different_pull_request_is_refused(self) -> None:
        path = self.feature_path(RATE_LIMIT)
        plan.apply_claim(path, "frame")
        path.write_text(path.read_text().replace("column: frame\n", "column: frame\npr: 12\n"))
        with self.assertRaises(SystemExit) as raised:
            plan.apply_close(path, 57, "2026-10-01")
        self.assertIn("`pr:` reads 12, not 57", str(raised.exception))

    def test_a_feature_that_was_never_claimed_is_not_closed(self) -> None:
        with self.assertRaises(SystemExit):
            plan.apply_close(self.feature_path(RATE_LIMIT), 57, "2026-10-01")


class LandByPushTests(PlanCase):
    land = "push"

    def start_feature_branch(self) -> None:
        sh("git", "checkout", "-q", "-b", "feat/rate-limit", cwd=self.repo)

    def on_main(self) -> dict:
        sh("git", "fetch", "-q", "origin", "main", cwd=self.repo)
        shown = sh("git", "show", f"origin/main:{SLICE}/{RATE_LIMIT}.md", cwd=self.repo)
        return plan.parse_document(shown + "\n")[0]

    def test_a_claim_reaches_main_and_the_working_branch_contains_it(self) -> None:
        self.start_feature_branch()
        quiet(plan.claim, self.kit, self.node(RATE_LIMIT), True)
        self.assertEqual(self.on_main()["status"], "in-progress")
        self.assertEqual(self.on_main()["column"], "frame")
        self.assertEqual(self.node(RATE_LIMIT).status, "in-progress")
        self.assertEqual(sh("git", "branch", "--show-current", cwd=self.repo), "feat/rate-limit")
        self.assertEqual(quiet(plan.claim_check, self.kit, self.node(RATE_LIMIT))[0], 0)
        subject = sh("git", "log", "-1", "--format=%s", "origin/main", cwd=self.repo)
        self.assertEqual(subject, "plan(open): claim Rate limit on the public check-in endpoint")
        self.assertEqual(sh("git", "diff", "--name-only", "origin/main~1", "origin/main",
                            cwd=self.repo), f"{SLICE}/{RATE_LIMIT}.md")
        self.assertEqual(sh("git", "worktree", "list", cwd=self.repo).count("\n"), 0)

    def test_the_claim_check_fails_before_the_claim(self) -> None:
        result, _, err = quiet(plan.claim_check, self.kit, self.node(RATE_LIMIT))
        self.assertEqual(result, 1)
        self.assertIn("the claim is not there", err)

    def test_the_claim_check_fails_on_a_branch_that_does_not_contain_main(self) -> None:
        self.start_feature_branch()
        quiet(plan.claim, self.kit, self.node(RATE_LIMIT), True)
        other = self.base / "other"
        sh("git", "clone", "-q", str(self.remote), str(other), cwd=self.base)
        (other / "note.txt").write_text("landed meanwhile\n")
        sh("git", "add", "-A", cwd=other)
        sh("git", "commit", "-q", "-m", "something else", cwd=other)
        sh("git", "push", "-q", "origin", "main", cwd=other)
        result, _, err = quiet(plan.claim_check, self.kit, self.node(RATE_LIMIT))
        self.assertEqual(result, 1)
        self.assertIn("1 commit behind origin/main", err)

    def test_a_working_copy_with_uncommitted_changes_is_not_rebased(self) -> None:
        self.start_feature_branch()
        (self.repo / "plan" / "kit.yaml").write_text(
            (self.repo / "plan" / "kit.yaml").read_text() + "# a local edit\n")
        _, out, _ = quiet(plan.claim, self.kit, self.node(RATE_LIMIT), True)
        self.assertIn("was not rebased", out)
        self.assertEqual(self.on_main()["status"], "in-progress")

    def test_a_close_reaches_main(self) -> None:
        self.start_feature_branch()
        quiet(plan.claim, self.kit, self.node(RATE_LIMIT), True)
        self.assertEqual(quiet(plan.close_check, self.kit, self.node(RATE_LIMIT))[0], 1)
        quiet(plan.close, self.kit, self.node(RATE_LIMIT), 57, "2026-10-01", True)
        there = self.on_main()
        self.assertEqual((there["status"], there["pr"], str(there["merged"])),
                         ("done", 57, "2026-10-01"))
        self.assertNotIn("column", there)
        self.assertEqual(quiet(plan.close_check, self.kit, self.node(RATE_LIMIT))[0], 0)

    def test_a_refused_claim_leaves_main_and_the_working_copy_alone(self) -> None:
        self.start_feature_branch()
        before = sh("git", "rev-parse", "origin/main", cwd=self.repo)
        with self.assertRaises(SystemExit):
            quiet(plan.claim, self.kit, self.node(TOKEN), True)
        sh("git", "fetch", "-q", "origin", "main", cwd=self.repo)
        self.assertEqual(sh("git", "rev-parse", "origin/main", cwd=self.repo), before)
        self.assertEqual(sh("git", "worktree", "list", cwd=self.repo).count("\n"), 0)
        self.assertEqual(sh("git", "status", "--porcelain", cwd=self.repo), "")


class LandByPullRequestTests(PlanCase):
    land = "pr"

    def setUp(self) -> None:
        super().setUp()
        bin_dir = self.base / "bin"
        bin_dir.mkdir()
        fake = bin_dir / "gh"
        fake.write_text(FAKE_GH)
        fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
        self.log = self.base / "gh.log"
        os.environ["PATH"] = f"{bin_dir}{os.pathsep}{os.environ['PATH']}"
        os.environ["GH_LOG"] = str(self.log)
        sh("git", "checkout", "-q", "-b", "feat/rate-limit", cwd=self.repo)

    def calls(self) -> list[str]:
        return [" ".join(line.split()[:2]) for line in self.log.read_text().splitlines()]

    def main_status(self) -> str:
        sh("git", "fetch", "-q", "origin", "main", cwd=self.repo)
        shown = sh("git", "show", f"origin/main:{SLICE}/{RATE_LIMIT}.md", cwd=self.repo)
        return plan.parse_document(shown + "\n")[0]["status"]

    def test_a_claim_is_raised_checked_and_merged_in_that_order(self) -> None:
        quiet(plan.claim, self.kit, self.node(RATE_LIMIT), True)
        self.assertEqual(self.calls(), ["pr create", "pr checks", "pr merge"])
        self.assertIn("--match-head-commit", self.log.read_text())
        self.assertEqual(self.main_status(), "in-progress")
        self.assertEqual(quiet(plan.claim_check, self.kit, self.node(RATE_LIMIT))[0], 0)

    def test_a_red_check_stops_the_merge(self) -> None:
        os.environ["GH_CHECKS_EXIT"] = "1"
        with self.assertRaises(SystemExit) as raised:
            quiet(plan.claim, self.kit, self.node(RATE_LIMIT), True)
        self.assertIn("nothing merged", str(raised.exception))
        self.assertEqual(self.calls(), ["pr create", "pr checks"])
        self.assertEqual(self.main_status(), "ready")

    def test_a_repository_with_no_checks_still_merges(self) -> None:
        os.environ["GH_NO_CHECKS"] = "1"
        quiet(plan.claim, self.kit, self.node(RATE_LIMIT), True)
        self.assertEqual(self.calls(), ["pr create", "pr checks", "pr merge"])
        self.assertEqual(self.main_status(), "in-progress")

    def test_the_merge_date_is_read_from_the_code_host(self) -> None:
        quiet(plan.claim, self.kit, self.node(RATE_LIMIT), True)
        quiet(plan.close, self.kit, self.node(RATE_LIMIT), 57, None, True)
        self.assertEqual(str(self.node(RATE_LIMIT).frontmatter.get("merged", "")), "")
        sh("git", "rebase", "-q", "origin/main", cwd=self.repo)
        self.assertEqual(str(self.node(RATE_LIMIT).frontmatter["merged"]), "2026-10-01")

    def test_an_unmerged_pull_request_is_not_closed(self) -> None:
        quiet(plan.claim, self.kit, self.node(RATE_LIMIT), True)
        os.environ["GH_VIEW"] = '{"state":"OPEN","mergedAt":null}'
        with self.assertRaises(SystemExit) as raised:
            quiet(plan.close, self.kit, self.node(RATE_LIMIT), 57, None, True)
        self.assertIn("is OPEN, not MERGED", str(raised.exception))
        self.assertEqual(self.main_status(), "in-progress")


class JournalAfterlifeTests(PlanCase):
    def setUp(self) -> None:
        super().setUp()
        plan.enter_column(self.kit, self.node(RATE_LIMIT), "close")
        self.journal = self.kit.work(RATE_LIMIT) / "journal.md"
        self.archive = self.base / "archive"
        self.archive.mkdir()

    def test_an_unset_destination_fails_rather_than_skipping(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            plan.archive(self.kit, self.node(RATE_LIMIT))
        self.assertIn("PLAN_JOURNAL_ARCHIVE is not set", str(raised.exception))

    def test_a_destination_that_does_not_exist_fails(self) -> None:
        os.environ["PLAN_JOURNAL_ARCHIVE"] = str(self.base / "nowhere")
        with self.assertRaises(SystemExit):
            plan.archive(self.kit, self.node(RATE_LIMIT))

    def test_an_empty_journal_is_a_finding_not_a_success(self) -> None:
        os.environ["PLAN_JOURNAL_ARCHIVE"] = str(self.archive)
        self.journal.write_text("\n")
        with self.assertRaises(SystemExit) as raised:
            plan.archive(self.kit, self.node(RATE_LIMIT))
        self.assertIn("missing or empty", str(raised.exception))

    def test_the_archive_is_a_copy_that_was_read_back(self) -> None:
        os.environ["PLAN_JOURNAL_ARCHIVE"] = str(self.archive)
        result, out, _ = quiet(plan.archive, self.kit, self.node(RATE_LIMIT))
        self.assertEqual(result, 0)
        self.assertEqual((self.archive / f"{RATE_LIMIT}.md").read_text(), self.journal.read_text())
        self.assertIn("read back", out)

    def test_nothing_is_released_before_the_journal_is_archived(self) -> None:
        os.environ["PLAN_JOURNAL_ARCHIVE"] = str(self.archive)
        with self.assertRaises(SystemExit) as raised:
            plan.release(self.kit, self.node(RATE_LIMIT))
        self.assertIn("has not been archived", str(raised.exception))
        self.assertTrue(self.journal.exists())

    def test_a_journal_changed_since_the_archive_is_not_released(self) -> None:
        os.environ["PLAN_JOURNAL_ARCHIVE"] = str(self.archive)
        quiet(plan.archive, self.kit, self.node(RATE_LIMIT))
        self.journal.write_text(self.journal.read_text() + "one more line\n")
        with self.assertRaises(SystemExit):
            plan.release(self.kit, self.node(RATE_LIMIT))
        self.assertTrue(self.journal.exists())

    def test_release_follows_the_archive(self) -> None:
        os.environ["PLAN_JOURNAL_ARCHIVE"] = str(self.archive)
        quiet(plan.archive, self.kit, self.node(RATE_LIMIT))
        quiet(plan.release, self.kit, self.node(RATE_LIMIT))
        self.assertFalse(self.kit.work(RATE_LIMIT).exists())
        self.assertTrue((self.archive / f"{RATE_LIMIT}.md").exists())


class RetroTests(PlanCase):
    def retro_file(self) -> Path:
        return next(self.kit.retro_dir.glob(f"*-{RATE_LIMIT}.md"))

    def test_a_retro_is_one_new_file_with_the_five_labels(self) -> None:
        quiet(plan.retro, self.kit, self.node(RATE_LIMIT))
        text = self.retro_file().read_text()
        for label in plan.RETRO_LABELS:
            self.assertIn(f"**{label}.**", text)
        self.assertEqual(plan.check_retros(self.kit), [])

    def test_a_second_retro_for_the_same_feature_is_refused(self) -> None:
        quiet(plan.retro, self.kit, self.node(RATE_LIMIT))
        with self.assertRaises(SystemExit):
            plan.retro(self.kit, self.node(RATE_LIMIT))

    def test_a_missing_label_fails_the_check(self) -> None:
        quiet(plan.retro, self.kit, self.node(RATE_LIMIT))
        path = self.retro_file()
        path.write_text(path.read_text().replace("**Faster.**", ""))
        self.assertEqual(len(plan.check_retros(self.kit)), 1)
        self.assertIn("no **Faster** line", plan.check_retros(self.kit)[0])

    def test_the_ceiling_is_enforced(self) -> None:
        quiet(plan.retro, self.kit, self.node(RATE_LIMIT))
        path = self.retro_file()
        path.write_text(path.read_text() + "more\n" * plan.RETRO_CEILING)
        self.assertIn("over the ceiling", "\n".join(plan.check_retros(self.kit)))


class CommandLineTests(PlanCase):
    def run_plan(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(Path(plan.__file__)), *args], cwd=self.repo,
                              capture_output=True, text=True)

    def test_the_plan_is_found_from_anywhere_inside_the_repository(self) -> None:
        done = subprocess.run([sys.executable, str(Path(plan.__file__)), "check"],
                              cwd=self.repo / "plan" / "tree", capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_work_lists_the_ready_feature_with_its_command(self) -> None:
        done = self.run_plan("work")
        self.assertIn("1 ready · 1 done", done.stdout)
        self.assertIn(f"plan prompt {RATE_LIMIT}", done.stdout)

    def test_show_prints_one_field(self) -> None:
        self.assertEqual(self.run_plan("show", RATE_LIMIT, "--field", "status").stdout.strip(),
                         "ready")
        self.assertEqual(self.run_plan("show", RATE_LIMIT, "--field", "merged").returncode, 1)

    def test_prompt_reports_the_words_before_the_column(self) -> None:
        done = self.run_plan("prompt", RATE_LIMIT, "-o", ".work/brief.md")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertRegex(done.stdout, r"\d+ words, \d+ before the sentence naming the column")

    def test_a_mode_is_refused_rather_than_ignored(self) -> None:
        done = self.run_plan("resolve", "build-in-browser", "--mode", "treatment-only")
        self.assertEqual(done.returncode, 1)
        self.assertIn("modes are not applied by the kit yet", done.stderr)

    def test_resolve_prints_yaml_that_parses_with_no_placeholder(self) -> None:
        done = self.run_plan("resolve", "real-environment-change")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertNotIn("{{", done.stdout)
        self.assertEqual(len(plan.yaml.safe_load(done.stdout)["columns"]), 12)

    def test_init_refuses_to_write_over_a_plan(self) -> None:
        done = self.run_plan("init", ".")
        self.assertEqual(done.returncode, 1)
        self.assertIn("already holds a plan", done.stderr)


if __name__ == "__main__":
    unittest.main()
