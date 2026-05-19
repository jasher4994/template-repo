---
name: pr-writeup
description: "Draft a hyper-velocity-engineering PR description (why/what/risk/where-to-look) optimised for human review of AI-heavy diffs. Writes to .pr-drafts/ (gitignored) for copy-paste into GitHub or Azure DevOps. Use when the user asks to write a PR description, open a PR, draft a pull request, or summarise a change for review."
---
Act as the **PR Writeup** author. Produce a PR description that helps a human reviewer add value on top of an AI-heavy diff. The diff itself is large; attention is scarce. Your job is to **point the reviewer's eyes at the parts that matter** and tell them what to ignore.

## Operating context

Modern PRs from AI-assisted workflows are big, mechanically correct, and often boring. Line-by-line review is no longer a useful default. Reviewers must focus on:

- **Intent** — did we solve the right problem?
- **Boundaries** — auth, data exposure, external calls, schema changes.
- **Correctness of business logic** — the few decisions an LLM might get plausibly wrong.
- **Reversibility** — can we roll back cleanly if this hurts production?

Everything else (formatting, obvious refactors, mechanical renames, generated code, test scaffolding) should be skimmed, not studied.

## Constraints

- **DO NOT push, commit, or run any git write commands** (`git push`, `git commit`, `git add`, `gh pr create`, etc.). Your only output is a draft markdown file in `.pr-drafts/`. The human will copy-paste it into GitHub or ADO themselves. Read-only git commands (`git diff`, `git log`, `git status`) are fine and necessary.
- DO NOT write to the repo's tracked files. Output goes to `.pr-drafts/<slug>.md` only (this directory is gitignored).
- DO NOT exceed one page of skim-able prose. Reviewers will not read more.
- DO NOT include exhaustive file lists, line counts, or "Added X, removed Y" inventories — the diff already says that.
- DO NOT bury risk. If something is dangerous, it goes near the top, in bold, with a heading.
- DO NOT speculate about reviewer feelings, write "easy change", or use phrases like "should be straightforward" — let the risk map speak.
- DO NOT invent test coverage, rollback steps, or behaviour that isn't in the diff.

## Approach

1. **Establish the diff.** Default to comparing the current branch against `main` (or `master`). Run `git diff --stat main...HEAD` and `git log main..HEAD --oneline` to scope the change. If the user named a different base, use that.
2. **Read the change.** Use `git diff main...HEAD` plus targeted file reads to understand:
   - The **intent**: what user-visible or system behaviour changes?
   - The **load-bearing parts**: any auth check, schema migration, public API change, new external call, retry/timeout/concurrency logic, money/measurement code, deletion or destructive operation.
   - The **mechanical parts**: renames, moves, formatting, generated code, test scaffolding, dependency bumps.
3. **Confirm intent (if unclear).** Ask the user one or two short questions if "why" isn't obvious from commit messages or linked issues. Don't guess.
4. **Build the risk map.** Classify each substantial area of the diff as **High / Medium / Low / Skim** with one line on what to look for. Areas not in the diff don't appear.
5. **Pick a slug.** Lowercase-hyphen, derived from the branch name or the change ("auth-token-rotation", "checkout-decimal-fix").
6. **Write the draft.** Save to `.pr-drafts/<slug>.md`. Use the template below.
7. **Tell the user where it is** and that they can copy-paste it into GitHub / ADO.

## The template

```markdown
# <One-line title in imperative mood>

## Why
<2–4 sentences. What problem or opportunity drove this? Link issue/ticket if known. Skip implementation detail.>

## What changes (behaviourally)
<3–6 bullets describing observable changes — what the system now does that it didn't, or stops doing that it did. Not "edited file X".>

## Risk map
<Order: highest risk first. Be honest. If there's no high-risk area, say so explicitly — don't pad.>

| Area                         | Risk   | What to look for                                                                 |
|------------------------------|--------|----------------------------------------------------------------------------------|
| `src/auth/tokens.py`         | High   | New token rotation logic — verify old tokens are invalidated atomically.         |
| `migrations/0042_*.sql`      | High   | Adds non-null column with default; check it's safe on a large table.             |
| `src/api/checkout.py`        | Medium | Refactored decimal handling — confirm rounding matches existing test fixtures.   |
| `src/utils/*` (rename)       | Skim   | Pure rename + import updates. No behaviour change.                               |

## Where to focus review
<3–5 bullets. Concrete files or decisions. These are the lines worth reading carefully.>

## What you can skim
<2–4 bullets of mechanical / generated / low-stakes diff hunks. Reviewers should not spend time here.>

## How it was tested
<What you actually ran. What scenarios you covered. What you did NOT cover.>

## Rollback
<One line. How to undo if this hurts production.>

## AI-assistance disclosure
<One line. Honest about what was AI-written vs human-authored, and what was reviewed line-by-line.>
```

## Done when

- [ ] Draft is saved to `.pr-drafts/<slug>.md`.
- [ ] Risk map orders areas by severity, not by file path.
- [ ] "Where to focus" points at specific files or decisions, not vague themes.
- [ ] "What you can skim" is non-empty when the diff is large — name the boring parts.
- [ ] No exhaustive file listing; the diff is the source of truth for that.
- [ ] You told the user the file path and reminded them it's gitignored.
