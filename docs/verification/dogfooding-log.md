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

_No entries yet. Adding one entry per agent/skill is required for the Phase 6 acceptance criterion._

### Suggested first exercise

1. Open Copilot Chat in a fresh session.
2. Type `/` and confirm the 6 skills appear in the menu by name.
3. Open the agent picker and confirm the 4 agents appear by name.
4. Type "critique my plan" — confirm description-based routing surfaces **Socrates**.
5. Type "/breadcrumb" — confirm the skill loads without error.
6. Record the outcome here.
