# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

## Quick start

```bash
make init    # one-time: bootstrap, venv, deps, hooks
make test    # run pytest
make lint    # ruff + mypy --strict
```

That's it for the Python project. The rest of this README covers tooling and conventions.

> Bootstrapped from [{{TEMPLATE_UPSTREAM}}]({{TEMPLATE_UPSTREAM}}) — a Python 3.12 + VS Code + Copilot agent project template.

---

## What's in the box

| Concern        | Tool                                         | Config                                                              |
|----------------|----------------------------------------------|---------------------------------------------------------------------|
| Python         | 3.12                                         | [pyproject.toml](pyproject.toml)                                    |
| Package mgmt   | [`uv`](https://github.com/astral-sh/uv)      | [Makefile](Makefile)                                                |
| Lint + format  | `ruff` (88-char lines)                       | [pyproject.toml](pyproject.toml)                                    |
| Type check     | `mypy --strict` — see [docs/typing.md](docs/typing.md) for escape hatches | [pyproject.toml](pyproject.toml)        |
| Tests          | `pytest`                                     | [pyproject.toml](pyproject.toml)                                    |
| Pre-commit     | ruff + mypy + standard hooks                 | [.pre-commit-config.yaml](.pre-commit-config.yaml)                  |
| Dev container  | Python 3.12 + extensions                     | [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json)  |
| VS Code        | Format on save, ruff default, pytest wired   | [.vscode/settings.json](.vscode/settings.json)                      |
| AI workflow    | 4 agents + 6 skills (experimental)           | [docs/ai-workflow.md](docs/ai-workflow.md)                          |

## Development commands

```bash
make init     # first-time setup: bootstrap, venv, deps, .env, hooks
make install  # install/sync dependencies (assumes venv)
make test     # pytest
make lint     # ruff check + mypy --strict
make format   # ruff format + ruff --fix
make doctor   # validate repo conventions (skill names, frontmatter, slug pairing)
make clean    # remove caches and venv
make help     # list all targets
```

Pre-commit runs `ruff` + `mypy` + standard hygiene hooks on every commit. Mypy runs from the project venv (not a separate hook env), so it sees real dependency types.

### Non-interactive bootstrap (CI, devcontainer, scripted)

```bash
python scripts/bootstrap.py --non-interactive \
  --project-name "My Project" \
  --project-slug my_project \
  --project-description "Short description." \
  --author-name "Jane Doe" \
  --author-email "jane@example.com" \
  --template-upstream "https://github.com/you/template-repo"
  # add --no-attribution to drop the "Bootstrapped from" line
```

The bootstrap is atomic: changes are backed up to `.bootstrap-backup/` and restored on any failure mid-run.

## Directory layout

```
src/{{PROJECT_SLUG}}/   — package source
tests/                  — pytest tests (no __init__.py by design)
plans/                  — feature plans and workflow status
experiments/            — data science experiment write-ups + raw metrics
docs/
  ai-workflow.md        — agents, skills, and how to use them
  typing.md             — mypy --strict escape hatches
  architecture/         — Mermaid diagrams of systems/flows
  breadcrumbs/          — implementation logs (one per plan, treat as append-only)
  decks/                — Marp slide decks
  figures/              — generated charts (PNG/SVG)
  verification/         — evidence that customisations actually work
scripts/
  bootstrap.py          — template placeholder substitution
  doctor.py             — convention validator
  figures/              — source scripts for docs/figures/
.github/
  agents/               — Copilot custom agents (role-based personas)
  skills/               — Agent Skills (one-shot, portable, open standard)
  instructions/         — scoped Copilot instructions
  PULL_REQUEST_TEMPLATE.md
.devcontainer/          — devcontainer config
.vscode/                — workspace settings
```

## AI workflow (optional)

This template ships an experimental ecosystem of Copilot agents and skills for plan→implement→review workflows, breadcrumbs, architecture diagrams, experiment logging, and PR writeups. **They have not yet been exercised end-to-end against a real feature** — see [docs/verification/](docs/verification/) for status.

Full details in [docs/ai-workflow.md](docs/ai-workflow.md).

If you don't want any of this, delete `.github/agents/`, `.github/skills/`, and `.github/instructions/` — nothing else in the template depends on them.

## Updating the template

If improvements land upstream in [{{TEMPLATE_UPSTREAM}}]({{TEMPLATE_UPSTREAM}}) that you want to pull into this project, the agent files, instructions, and `make` targets are all self-contained — copy them across individually as needed.

## License

See [LICENSE](LICENSE).
