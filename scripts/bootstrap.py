#!/usr/bin/env python3
"""Bootstrap a fresh project from this template.

Replaces template placeholders across the repo and renames the placeholder
package directory. Idempotent: a no-op if already bootstrapped.

Supports interactive (TTY) and non-interactive (CI/devcontainer) modes.
Atomic: all changes happen in-memory first, then commit. On failure, restores
from .bootstrap-backup/.

Run via ``make init`` or directly:
    python scripts/bootstrap.py                   # interactive
    python scripts/bootstrap.py --non-interactive \\
        --project-name "My Project" \\
        --project-slug my_project \\
        --project-description "Description" \\
        --author-name "Jane Doe" \\
        --author-email "jane@example.com" \\
        [--template-upstream "https://github.com/you/template-repo"] \\
        [--no-attribution]
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER_DIR = ROOT / "src" / "_pkg_placeholder"
BACKUP_DIR = ROOT / ".bootstrap-backup"

PLACEHOLDERS = (
    "PROJECT_SLUG",
    "PROJECT_NAME",
    "PROJECT_DESCRIPTION",
    "AUTHOR_NAME",
    "AUTHOR_EMAIL",
    "TEMPLATE_UPSTREAM",
)

SCAN_GLOBS = (
    "pyproject.toml",
    "README.md",
    "LICENSE",
    "src/**/*.py",
    "tests/**/*.py",
)

SLUG_RE = re.compile(r"^[a-z][a-z0-9_]*$")
DEFAULT_UPSTREAM = "https://github.com/jasher4994/template-repo"


def prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix}: ").strip() or (default or "")
        if value:
            return value
        print("  (required)")


def git_config(key: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "config", "--get", key],
            capture_output=True, text=True, check=False,
        )
        return out.stdout.strip() or None
    except FileNotFoundError:
        return None


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()
    if s and s[0].isdigit():
        s = "_" + s
    return s or "app"


def already_bootstrapped() -> bool:
    pyproject = (ROOT / "pyproject.toml").read_text()
    return "{{PROJECT_SLUG}}" not in pyproject and not PLACEHOLDER_DIR.exists()


def collect_files() -> list[Path]:
    seen: set[Path] = set()
    for pattern in SCAN_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file():
                seen.add(path)
    return sorted(seen)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--non-interactive", action="store_true",
                   help="Fail rather than prompt for missing values.")
    p.add_argument("--project-name")
    p.add_argument("--project-slug")
    p.add_argument("--project-description")
    p.add_argument("--author-name")
    p.add_argument("--author-email")
    p.add_argument("--template-upstream",
                   help=f"Upstream template URL (default: {DEFAULT_UPSTREAM}). Ignored if --no-attribution.")
    p.add_argument("--no-attribution", action="store_true",
                   help="Strip the upstream-template attribution paragraph from README.")
    return p.parse_args()


def resolve_value(name: str, cli_value: str | None, default: str | None,
                  non_interactive: bool, label: str, required: bool = False) -> str:
    if cli_value:
        return cli_value
    if non_interactive:
        if required or not default:
            print(f"error: --non-interactive requires --{name.replace('_', '-')}",
                  file=sys.stderr)
            sys.exit(2)
        return default
    return prompt(label, default)


def stage_substitutions(values: dict[str, str], strip_attribution: bool) -> dict[Path, str]:
    """Build the new content for every file in-memory. No writes yet."""
    staged: dict[Path, str] = {}
    for path in collect_files():
        text = path.read_text()
        new = text
        for key in PLACEHOLDERS:
            new = new.replace("{{" + key + "}}", values.get(key, ""))
        if strip_attribution and path.name == "README.md":
            new = re.sub(
                r"\n> Bootstrapped from .*?\n\n---\n",
                "\n---\n",
                new,
                count=1,
                flags=re.DOTALL,
            )
        if new != text:
            staged[path] = new
    return staged


def backup_files(paths: list[Path]) -> None:
    if BACKUP_DIR.exists():
        print(f"error: {BACKUP_DIR} already exists. Inspect and remove it before re-running.",
              file=sys.stderr)
        sys.exit(1)
    BACKUP_DIR.mkdir()
    for path in paths:
        rel = path.relative_to(ROOT)
        dest = BACKUP_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def restore_from_backup() -> None:
    if not BACKUP_DIR.exists():
        return
    for src in BACKUP_DIR.rglob("*"):
        if src.is_file():
            rel = src.relative_to(BACKUP_DIR)
            dest = ROOT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
    # If the placeholder dir was renamed before failure, rename it back.
    if not PLACEHOLDER_DIR.exists():
        for candidate in (ROOT / "src").iterdir():
            if candidate.is_dir() and candidate.name != "_pkg_placeholder":
                if (candidate / "__init__.py").exists():
                    candidate.rename(PLACEHOLDER_DIR)
                    break


def main() -> int:
    args = parse_args()

    if already_bootstrapped():
        print("Already bootstrapped — nothing to do.")
        return 0

    if BACKUP_DIR.exists():
        print(f"error: {BACKUP_DIR} exists from a previous failed run. "
              f"Inspect and remove it before re-running.", file=sys.stderr)
        return 1

    non_interactive = args.non_interactive or not sys.stdin.isatty()
    if non_interactive and not args.non_interactive:
        print("note: stdin is not a TTY; running in non-interactive mode.",
              file=sys.stderr)

    print("Bootstrapping project from template.\n")

    project_name = resolve_value(
        "project_name", args.project_name, ROOT.name,
        non_interactive, "Project name", required=True)
    project_slug = resolve_value(
        "project_slug", args.project_slug, slugify(project_name),
        non_interactive, "Project slug (importable, lowercase)", required=True)
    if not SLUG_RE.match(project_slug):
        print(f"error: invalid slug: {project_slug!r}", file=sys.stderr)
        return 1
    project_desc = resolve_value(
        "project_description", args.project_description, "A Python project.",
        non_interactive, "Description")
    author_name = resolve_value(
        "author_name", args.author_name, git_config("user.name") or "Your Name",
        non_interactive, "Author name")
    author_email = resolve_value(
        "author_email", args.author_email,
        git_config("user.email") or "you@example.com",
        non_interactive, "Author email")
    template_upstream = args.template_upstream or DEFAULT_UPSTREAM

    values = {
        "PROJECT_SLUG": project_slug,
        "PROJECT_NAME": project_name,
        "PROJECT_DESCRIPTION": project_desc,
        "AUTHOR_NAME": author_name,
        "AUTHOR_EMAIL": author_email,
        "TEMPLATE_UPSTREAM": template_upstream,
    }

    target_dir = ROOT / "src" / project_slug
    if PLACEHOLDER_DIR.exists() and target_dir.exists() and target_dir != PLACEHOLDER_DIR:
        print(f"error: target {target_dir} already exists", file=sys.stderr)
        return 1

    # Back up everything we might touch BEFORE any mutation.
    candidates = collect_files()
    backup_files(candidates)

    try:
        # Rename first so file globs pick up the new path.
        if PLACEHOLDER_DIR.exists():
            PLACEHOLDER_DIR.rename(target_dir)
            print(f"  renamed src/_pkg_placeholder -> src/{project_slug}")
        # Stage substitutions AFTER rename, then write all-or-nothing.
        staged = stage_substitutions(values, strip_attribution=args.no_attribution)
        for path, new_text in staged.items():
            path.write_text(new_text)
            print(f"  updated {path.relative_to(ROOT)}")
    except Exception as exc:
        print(f"\nerror: bootstrap failed mid-run: {exc}", file=sys.stderr)
        print("Restoring from .bootstrap-backup/ ...", file=sys.stderr)
        restore_from_backup()
        print("Restore complete. Remove .bootstrap-backup/ to retry.", file=sys.stderr)
        return 1

    # Success — remove backup.
    shutil.rmtree(BACKUP_DIR)
    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
