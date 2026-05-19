"""Tests for scripts/doctor.py.

Builds tiny fixture repos in ``tmp_path`` and asserts the doctor's outcomes.
Keeps the doctor honest about its own conventions.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import doctor  # noqa: E402


# --- frontmatter parser -----------------------------------------------------

def test_split_frontmatter_happy() -> None:
    fm, body = doctor.split_frontmatter("---\nname: foo\n---\nbody text\n")
    assert fm == "name: foo"
    assert body == "body text\n"


def test_split_frontmatter_missing() -> None:
    fm, body = doctor.split_frontmatter("no frontmatter here\n")
    assert fm is None
    assert body == "no frontmatter here\n"


def test_split_frontmatter_crlf() -> None:
    """Windows line endings must parse identically to LF."""
    fm, body = doctor.split_frontmatter("---\r\nname: foo\r\n---\r\nbody\r\n")
    assert fm == "name: foo"
    assert "body" in body


def test_parse_simple_frontmatter_basic() -> None:
    fields = doctor.parse_simple_frontmatter('name: foo\ndescription: "a thing"')
    assert fields == {"name": "foo", "description": "a thing"}


def test_parse_simple_frontmatter_colon_in_value() -> None:
    """Values containing colons (URLs, ratios) must round-trip."""
    fields = doctor.parse_simple_frontmatter("url: https://example.com/x")
    assert fields["url"] == "https://example.com/x"


def test_parse_simple_frontmatter_ignores_indented_and_comments() -> None:
    fm = "name: foo\n# a comment\n  indented: ignored\nother: bar"
    fields = doctor.parse_simple_frontmatter(fm)
    assert fields == {"name": "foo", "other": "bar"}


def test_parse_simple_frontmatter_strips_matching_quotes_only() -> None:
    # Mismatched quotes left intact rather than silently mangled.
    fields = doctor.parse_simple_frontmatter("a: \"unclosed\nb: 'ok'")
    assert fields["a"] == '"unclosed'
    assert fields["b"] == "ok"


# --- helpers ----------------------------------------------------------------

def _write_skill(root: Path, dir_name: str, frontmatter: str | None) -> None:
    d = root / ".github" / "skills" / dir_name
    d.mkdir(parents=True)
    content = f"---\n{frontmatter}\n---\nbody\n" if frontmatter is not None else "body\n"
    (d / "SKILL.md").write_text(content)


def _write_agent(root: Path, file_name: str, frontmatter: str) -> None:
    d = root / ".github" / "agents"
    d.mkdir(parents=True, exist_ok=True)
    (d / file_name).write_text(f"---\n{frontmatter}\n---\nbody\n")


# --- check_skills -----------------------------------------------------------

def test_check_skills_happy(tmp_path: Path) -> None:
    _write_skill(tmp_path, "foo", 'name: foo\ndescription: "does foo"')
    report = doctor.Report(verbose=False)
    doctor.check_skills(tmp_path, report)
    assert report.errors == []


def test_check_skills_name_mismatch(tmp_path: Path) -> None:
    _write_skill(tmp_path, "foo", 'name: bar\ndescription: "x"')
    report = doctor.Report(verbose=False)
    doctor.check_skills(tmp_path, report)
    assert any("does not match directory" in e for e in report.errors)


def test_check_skills_missing_name(tmp_path: Path) -> None:
    _write_skill(tmp_path, "foo", 'description: "x"')
    report = doctor.Report(verbose=False)
    doctor.check_skills(tmp_path, report)
    assert any("missing required 'name'" in e for e in report.errors)


def test_check_skills_missing_description(tmp_path: Path) -> None:
    _write_skill(tmp_path, "foo", "name: foo")
    report = doctor.Report(verbose=False)
    doctor.check_skills(tmp_path, report)
    assert any("missing required 'description'" in e for e in report.errors)


def test_check_skills_missing_skill_md(tmp_path: Path) -> None:
    (tmp_path / ".github" / "skills" / "foo").mkdir(parents=True)
    report = doctor.Report(verbose=False)
    doctor.check_skills(tmp_path, report)
    assert any("missing SKILL.md" in e for e in report.errors)


def test_check_skills_no_frontmatter(tmp_path: Path) -> None:
    _write_skill(tmp_path, "foo", None)
    report = doctor.Report(verbose=False)
    doctor.check_skills(tmp_path, report)
    assert any("no YAML frontmatter" in e for e in report.errors)


def test_check_skills_missing_directory_is_warning(tmp_path: Path) -> None:
    report = doctor.Report(verbose=False)
    doctor.check_skills(tmp_path, report)
    assert report.errors == []
    assert any("does not exist" in w for w in report.warnings)


# --- check_agents -----------------------------------------------------------

def test_check_agents_happy(tmp_path: Path) -> None:
    _write_agent(tmp_path, "p.agent.md", 'description: "a planner"\ntools: [search, edit]')
    report = doctor.Report(verbose=False)
    doctor.check_agents(tmp_path, report)
    assert report.errors == []


def test_check_agents_missing_description(tmp_path: Path) -> None:
    _write_agent(tmp_path, "p.agent.md", "tools: [search]")
    report = doctor.Report(verbose=False)
    doctor.check_agents(tmp_path, report)
    assert any("missing required 'description'" in e for e in report.errors)


def test_check_agents_subagent_dispatch_requires_agent_tool(tmp_path: Path) -> None:
    """Declaring agents: without 'agent' in tools: is silently broken in VS Code."""
    _write_agent(
        tmp_path,
        "orch.agent.md",
        'description: "x"\ntools: [search, edit]\nagents: [Planner]',
    )
    report = doctor.Report(verbose=False)
    doctor.check_agents(tmp_path, report)
    assert any("lacks 'agent'" in e for e in report.errors)


def test_check_agents_subagent_dispatch_ok_when_agent_in_tools(tmp_path: Path) -> None:
    _write_agent(
        tmp_path,
        "orch.agent.md",
        'description: "x"\ntools: [search, edit, agent]\nagents: [Planner]',
    )
    report = doctor.Report(verbose=False)
    doctor.check_agents(tmp_path, report)
    assert report.errors == []


# --- check_plan_breadcrumb_pairing ------------------------------------------

def test_check_plans_warns_on_missing_breadcrumb(tmp_path: Path) -> None:
    (tmp_path / "plans").mkdir()
    (tmp_path / "plans" / "feature-x.md").write_text("# plan\n")
    (tmp_path / "docs" / "breadcrumbs").mkdir(parents=True)
    report = doctor.Report(verbose=False)
    doctor.check_plan_breadcrumb_pairing(tmp_path, report)
    assert any("feature-x.md" in w for w in report.warnings)
    assert report.errors == []


def test_check_plans_no_warning_when_breadcrumb_exists(tmp_path: Path) -> None:
    (tmp_path / "plans").mkdir()
    (tmp_path / "plans" / "feature-x.md").write_text("# plan\n")
    bc = tmp_path / "docs" / "breadcrumbs"
    bc.mkdir(parents=True)
    (bc / "feature-x.md").write_text("# crumbs\n")
    report = doctor.Report(verbose=False)
    doctor.check_plan_breadcrumb_pairing(tmp_path, report)
    assert report.warnings == []


def test_check_plans_skips_meta_files(tmp_path: Path) -> None:
    (tmp_path / "plans").mkdir()
    for name in ("README.md", "_status.md", "feature-x-retro.md"):
        (tmp_path / "plans" / name).write_text("# x\n")
    (tmp_path / "docs" / "breadcrumbs").mkdir(parents=True)
    report = doctor.Report(verbose=False)
    doctor.check_plan_breadcrumb_pairing(tmp_path, report)
    assert report.warnings == []


def test_check_plans_silent_without_breadcrumbs_dir(tmp_path: Path) -> None:
    """If no breadcrumbs convention is in use, don't nag."""
    (tmp_path / "plans").mkdir()
    (tmp_path / "plans" / "feature-x.md").write_text("# plan\n")
    report = doctor.Report(verbose=False)
    doctor.check_plan_breadcrumb_pairing(tmp_path, report)
    assert report.warnings == []


# --- end-to-end -------------------------------------------------------------

def test_run_clean_repo_returns_no_errors(tmp_path: Path) -> None:
    _write_skill(tmp_path, "foo", 'name: foo\ndescription: "x"')
    _write_agent(tmp_path, "p.agent.md", 'description: "a"')
    report = doctor.run(tmp_path, verbose=False)
    assert report.errors == []


def test_run_dirty_repo_reports_errors(tmp_path: Path) -> None:
    _write_skill(tmp_path, "foo", "name: wrong")  # mismatch + missing desc
    report = doctor.run(tmp_path, verbose=False)
    assert len(report.errors) >= 2
