#!/usr/bin/env python3
"""Validate repo conventions: skill name/dir match, agent/skill frontmatter
parses, plan/breadcrumb slug pairing.

Exit 0 if clean, 1 if any check fails. Run via ``make doctor``.

No external dependencies. YAML frontmatter is parsed by a minimal hand-rolled
scanner sufficient for the simple field types used in this repo.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GREEN = "\033[32m" if sys.stdout.isatty() else ""
RED = "\033[31m" if sys.stdout.isatty() else ""
YELLOW = "\033[33m" if sys.stdout.isatty() else ""
RESET = "\033[0m" if sys.stdout.isatty() else ""

class Report:
    """Collects pass/warn/fail outcomes. ``verbose`` controls stdout printing."""

    def __init__(self, verbose: bool = True) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.verbose = verbose

    def err(self, msg: str) -> None:
        self.errors.append(msg)
        if self.verbose:
            print(f"{RED}FAIL{RESET} {msg}")

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)
        if self.verbose:
            print(f"{YELLOW}WARN{RESET} {msg}")

    def ok(self, msg: str) -> None:
        if self.verbose:
            print(f"{GREEN} OK {RESET} {msg}")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    # Normalise CRLF/CR to LF so Windows-authored files parse identically.
    normalised = text.replace("\r\n", "\n").replace("\r", "\n")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", normalised, re.DOTALL)
    if not m:
        return None, normalised
    return m.group(1), m.group(2)


def parse_simple_frontmatter(fm: str) -> dict[str, str]:
    """Parse the subset of YAML used by agent/skill frontmatter.

    Supports ``key: value`` and ``key: "value"`` on a single line. Indented
    continuation lines and block scalars (``>``/``|``) are not supported -- the
    parser intentionally stays small. Any non-conforming line is ignored.
    """
    out: dict[str, str] = {}
    for line in fm.splitlines():
        if not line or line[:1] in (" ", "\t", "#"):
            continue
        m = re.match(r"^([a-zA-Z][a-zA-Z0-9_-]*):\s*(.*)$", line)
        if m:
            value = m.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            out[m.group(1)] = value
    return out


def check_skills(root: Path, report: Report) -> None:
    skills_dir = root / ".github" / "skills"
    if not skills_dir.is_dir():
        report.warn(f"{skills_dir.relative_to(root)} does not exist")
        return
    for d in sorted(skills_dir.iterdir()):
        if not d.is_dir():
            continue
        skill_file = d / "SKILL.md"
        if not skill_file.exists():
            report.err(f"skill {d.name}: missing SKILL.md")
            continue
        fm, _ = split_frontmatter(skill_file.read_text())
        if fm is None:
            report.err(f"skill {d.name}: SKILL.md has no YAML frontmatter")
            continue
        fields = parse_simple_frontmatter(fm)
        name = fields.get("name")
        if not name:
            report.err(f"skill {d.name}: missing required 'name' field")
        elif name != d.name:
            report.err(
                f"skill {d.name}: name={name!r} does not match directory {d.name!r}"
            )
        if not fields.get("description"):
            report.err(f"skill {d.name}: missing required 'description' field")
        if name == d.name and fields.get("description"):
            report.ok(f"skill {d.name}: valid")


def check_agents(root: Path, report: Report) -> None:
    agents_dir = root / ".github" / "agents"
    if not agents_dir.is_dir():
        report.warn(f"{agents_dir.relative_to(root)} does not exist")
        return
    for f in sorted(agents_dir.glob("*.agent.md")):
        text = f.read_text()
        fm, _ = split_frontmatter(text)
        if fm is None:
            report.err(f"agent {f.name}: no YAML frontmatter")
            continue
        fields = parse_simple_frontmatter(fm)
        if not fields.get("description"):
            report.err(f"agent {f.name}: missing required 'description' field")
            continue
        fm_lines = fm.splitlines()
        agents_field = next((ln for ln in fm_lines if ln.startswith("agents:")), None)
        tools_field = next((ln for ln in fm_lines if ln.startswith("tools:")), None)
        if agents_field and tools_field and "agent" not in tools_field:
            report.err(f"agent {f.name}: declares 'agents:' but 'tools:' lacks 'agent'")
            continue
        report.ok(f"agent {f.name}: valid")


def check_plan_breadcrumb_pairing(root: Path, report: Report) -> None:
    plans_dir = root / "plans"
    breadcrumbs_dir = root / "docs" / "breadcrumbs"
    if not plans_dir.is_dir():
        return
    for plan in sorted(plans_dir.glob("*.md")):
        if plan.name in {"README.md", "_status.md"} or plan.name.endswith("-retro.md"):
            continue
        slug = plan.stem
        bc = breadcrumbs_dir / f"{slug}.md"
        if breadcrumbs_dir.exists() and not bc.exists():
            report.warn(
                f"plan {plan.name}: no matching docs/breadcrumbs/{slug}.md "
                "(fine for un-started work)"
            )


def run(root: Path, verbose: bool = True) -> Report:
    report = Report(verbose=verbose)
    if verbose:
        print("Doctor: validating repo conventions\n")
    check_skills(root, report)
    check_agents(root, report)
    check_plan_breadcrumb_pairing(root, report)
    if verbose:
        print()
        if report.errors:
            print(
                f"{RED}{len(report.errors)} error(s){RESET}, "
                f"{len(report.warnings)} warning(s)"
            )
        else:
            print(
                f"{GREEN}All checks passed{RESET} "
                f"({len(report.warnings)} warning(s))"
            )
    return report


def main() -> int:
    report = run(ROOT, verbose=True)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
