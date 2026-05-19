# AI workflow ecosystem

> **Status:** experimental. The agents and skills described here have not yet been exercised end-to-end against a real feature. See [docs/verification/dogfooding-log.md](verification/dogfooding-log.md) for evidence as it accumulates.

This repo ships two kinds of Copilot customisation, split by what each one actually needs:

- **Agents** ([.github/agents/](../.github/agents/)) — role-based personas with **restricted tool access** and **persistence across a session**. Reserved for cases where the constraint is load-bearing (e.g. a critic that must not edit) or where multi-turn discipline matters.
- **Skills** ([.github/skills/](../.github/skills/)) — one-shot capabilities following the [open Agent Skills standard](https://agentskills.io/). Portable across Copilot in VS Code, Copilot CLI, and Copilot cloud agent. Each skill is a directory with a `SKILL.md` plus any supporting scripts or templates.

Both surface in the Copilot Chat picker and both auto-route via their `description` field when your phrasing matches.

## Agents (persistent personas, restricted tools)

| Agent              | Status | What it does                                              | Writes to                          |
|--------------------|--------|-----------------------------------------------------------|------------------------------------|
| **Planner**        | experimental | Break work into ordered, verifiable steps           | `plans/<slug>.md`                  |
| **Socrates**       | experimental | Stress-test plans, designs, arguments via probing critique | nothing (read-only)            |
| **Implementer**    | experimental | Execute a plan step; lint + test; log breadcrumbs as it goes | source + `docs/breadcrumbs/<slug>.md` |
| **Project Flow**   | experimental | Orchestrate Planner → Socrates → Implementer end-to-end   | `plans/_status.md`, `plans/<slug>-retro.md` |

## Skills (one-shot procedures)

| Skill                     | Status | What it does                                                  | Writes to                          |
|---------------------------|--------|---------------------------------------------------------------|------------------------------------|
| `/breadcrumb`             | experimental | Read the latest implementation log and brief the next session | nothing (read-only)        |
| `/architect-diagram`      | experimental | One Mermaid diagram per request                         | `docs/architecture/<slug>.md`      |
| `/slide-deck`             | experimental | Marp-compatible deck from a brief or source             | `docs/decks/<slug>.md`             |
| `/visualisation`          | experimental | One chart per request, reproducible                     | `docs/figures/` + `scripts/figures/`|
| `/experiment-logger`      | experimental | Rigorous write-up of a DS experiment                    | `experiments/<YYYY-MM-DD>-<slug>.md`|
| `/pr-writeup`             | experimental | Draft a review-focused PR description for AI-heavy diffs | `.pr-drafts/<slug>.md` (gitignored)|

There is also one scoped instruction file: [experiment-reminders.instructions.md](../.github/instructions/experiment-reminders.instructions.md) — applies in `experiments/`, `notebooks/`, and `train*.py` / `eval*.py` files; nudges Copilot to log experiments when training/eval language appears.

> Promote a "status" entry from **experimental** to **verified \<date\>** once you've successfully exercised it end-to-end and logged the result in [verification/dogfooding-log.md](verification/dogfooding-log.md).

## Invoking

- **Agent picker:** in Copilot Chat, click the agent dropdown → pick an agent by name.
- **Slash commands:** skills are invokable as `/breadcrumb`, `/pr-writeup`, etc. (the `name` in each `SKILL.md` matches its directory).
- **Auto-delegation:** the default agent reads each `description` and routes to the best match — so "plan the auth rewrite" tends to land in **Planner**, and "diagram the checkout flow" tends to invoke `/architect-diagram`, without explicit selection.
- **From another agent:** **Project Flow** dispatches Planner/Socrates/Implementer as subagents (declared in its `agents:` frontmatter).

## Typical workflows

### Build a feature
```
Project Flow → Planner (writes plans/feature.md)
            → Socrates (stress-tests the plan)
            → Implementer (executes step by step; appends to docs/breadcrumbs/feature.md)
            → Retro (plans/feature-retro.md)
```
Or manually: `/Planner` → review plan → `/Implementer` for each step.

### Resume after a break
`/breadcrumb` reads the latest implementation log, cross-checks `git status`, and tells you the single next action.

### Run an experiment
Mention training, evaluation, or comparison in chat → the [experiment-reminders instruction](../.github/instructions/experiment-reminders.instructions.md) nudges Copilot to offer `/experiment-logger` → answer 3 questions (hypothesis, primary metric, baseline) → log lands in `experiments/`. Negative results are logged with the same rigour as positive ones.

### Visualise / diagram
- **Data chart:** `/visualisation` — one chart, one insight, reproducible script under `scripts/figures/`.
- **System diagram:** `/architect-diagram` — one Mermaid diagram, ≤15 nodes, consistent arrow/shape semantics.

### Pressure-test an idea
`/Socrates` — steelmans your idea, attacks the load-bearing claims, ends with Keep / Sharpen / Drop. Read-only; never edits.

### Open a PR
`/pr-writeup` — reads the diff against `main`, builds a risk map, points the reviewer at the load-bearing parts and tells them what to skim. Writes a draft to `.pr-drafts/<slug>.md` (gitignored) for you to paste into GitHub or Azure DevOps. The committed [PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) follows the same structure so manual PRs stay consistent.

## Conventions (advisory, not enforced)

- **One slug, many artefacts.** A feature `auth-rewrite` has `plans/auth-rewrite.md`, `docs/breadcrumbs/auth-rewrite.md`, optionally `docs/architecture/auth-rewrite.md`. Same slug, predictable paths. Validated by `make doctor`.
- **Filenames lowercase + hyphen-separated.**
- **Treat breadcrumb and experiment logs as append-only by habit.** This is not enforced by tooling (a pre-commit hook for "additions only" in markdown is fiddly and noisy); it's a convention. The honest framing: corrections go in as new entries; only rewrite history if you also note why.
- **Generated artefacts are committed.** Figures and decks are the deliverable; they live in git.

## Validating the ecosystem

```
make doctor
```

Checks that skill names match their directories, agent/skill frontmatter parses, and plans have matching breadcrumbs where you'd expect them.
