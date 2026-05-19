# Dogfooding log — agents and skills exercised in real Copilot sessions

Per the template-hardening plan, every agent and skill should be exercised end-to-end at least once before being marked "verified" in the README. Until then it carries the "experimental" label.

## Format

```
### YYYY-MM-DD — <agent or skill name>

- **Invoked as:** `@AgentName` or `/skill-name`
- **Task:** <one sentence>
- **Result:** worked | partially worked | did not work
- **Notes:** routing fired? frontmatter loaded? tool restrictions honoured? unexpected behaviour?
```

## Entries

### 2026-05-19 — First end-to-end exercise (fresh devcontainer, fresh Copilot session)

**Environment:** project bootstrapped from template via `gh repo create … --template`, opened in devcontainer, fresh Copilot Chat session.

**Picker visibility:**
- All 6 skills appear in the `/` menu by name. ✓
- All 4 agents appear in the chat mode picker by name. ✓

**Per-agent / per-skill:**

| Item | Invocation | Outcome | Notes |
|---|---|---|---|
| Planner | explicit | worked | Wrote a plan to `plans/cli-scripts.md`. |
| Implementer | explicit | worked | Ran lint + tests as part of work. |
| Socrates | explicit | worked | Tool restriction not directly tested but agent behaved as critic-only. |
| Socrates | description-routing ("critique my README") | **did not fire** | Default agent answered directly; never handed off. Explicit invocation works. |
| Project Flow | explicit | worked | Dispatched to subagents. **Action:** added a human approval gate between Socrates and Implementer (was implicit before). |
| `/experiment-logger` | description-routing ("I just trained a model and want to log it") | worked | Skill fired without explicit `/` invocation. ✓ |
| `/pr-writeup` | explicit | worked, but unclear | Wrote draft correctly, but tone didn't make clear it would NOT push. **Action:** strengthened constraint in SKILL.md to explicitly forbid `git push`/`git commit`/`gh pr create`. |
| `/breadcrumb`, `/architect-diagram`, `/slide-deck`, `/visualisation` | (not yet exercised) | — | Visible in picker; behaviour unverified. Remain "experimental". |

**Instruction file (`experiment-reminders`):**
- Fires on training-code edits (verified). ✓
- Stays quiet on non-DS file edits (verified). ✓

**Devcontainer:**
- `postAttachCommand` welcome message appears. ✓
- `make doctor` passes inside container. ✓
- `make init` second run correctly short-circuits with "Already bootstrapped". ✓
- **Bug found and fixed:** `make init` was prompting "replace venv?" before checking bootstrap state. Reordered to short-circuit first.

**Open items:**
- 4 skills still unverified (breadcrumb, architect-diagram, slide-deck, visualisation). Promote when exercised.
- Description-based auto-routing to agents (especially Socrates) is unreliable. Either accept explicit-invocation-only as the design, or sharpen agent descriptions to be more keyword-rich.
- User proposed a separate "code review" agent (post-implementation diff review, distinct from Socrates's pre-implementation idea critique). Open for future work.

### Suggested next exercise

Exercise the four remaining unverified skills (`/breadcrumb`, `/architect-diagram`, `/slide-deck`, `/visualisation`) and add a row per skill above.
