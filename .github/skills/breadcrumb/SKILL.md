---
name: breadcrumb
description: "Read the latest implementation breadcrumb log and brief the next session: what's done, where work stopped, the next concrete action, and any open blockers. Use when the user asks to resume, catch up, brief me, recap, or pick up where I left off."
---
Act as the **Breadcrumb** reader. You do not write breadcrumbs — the **Implementer** does that as it works. Your job is to read the log and give the next session a 30-second brief so they can resume immediately.

## Constraints

- DO NOT modify the breadcrumb log or any other file. You are read-only for this task.
- DO NOT summarise more than one log per invocation. If the user asks about several, brief the most recent and list the others.
- DO NOT exceed ~25 lines of output. The point is a fast brief, not a re-read.
- DO NOT include raw log lines verbatim unless quoting a `BLOCKED` or `DECISION` entry.
- DO NOT speculate about state the log doesn't record. If something is unclear, say "log doesn't say" rather than guessing.

## Approach

1. **Pick the log.**
   - If the user named a plan slug or file, use it.
   - Otherwise: list `docs/breadcrumbs/` and pick the most recently modified `*.md` (excluding `INDEX.md` if present).
   - If `docs/breadcrumbs/` doesn't exist or is empty, say so and stop.
2. **Read it.** Read the whole log file. Also read the linked plan file (`plans/<slug>.md`) if it exists, to map log entries to plan steps.
3. **Cross-check git state.** Run `git status --short` and `git log --oneline -n 3` to confirm the log isn't lying about uncommitted work.
4. **Brief.** Produce the output format below. Lead with the **Next action** — it's what the user opened this for.
5. **Flag drift.** If git state contradicts the log (uncommitted files the log doesn't mention, or log says committed but no commit exists), say so explicitly.

## Output format

```markdown
## Resume: <plan-slug>

**Next action:** <one-sentence concrete step, lifted from the latest `STOP` entry or inferred from the latest activity>

**Where you are in the plan:** Step <N> of <M> — <step title> (<state: doing / blocked / done>).

**Last activity:** <YYYY-MM-DD HH:MM> — <latest non-STOP entry, paraphrased>.

**Open blockers:**
- <BLOCKED entry, verbatim, if any>
- (or "None.")

**Recent decisions worth knowing:**
- <DECISION entry, paraphrased>
- (≤ 3 items; oldest first.)

**State check:**
- Branch: `<branch>`
- Uncommitted: <N files> — <"matches log" | "log doesn't mention X, Y">
- Last commit: `<sha> <subject>`

**Full log:** [docs/breadcrumbs/<slug>.md](../../docs/breadcrumbs/<slug>.md)
```

## Done when

- [ ] One brief, under ~25 lines.
- [ ] **Next action** is concrete and actionable in the next turn.
- [ ] Git drift (if any) is flagged.
- [ ] Brief links the full log so the user can dig deeper if they want.
