# Agent vs skill — one-line rationale per customisation

Decision date: 2026-05-19. Per Socrates critique and frontmatter verification.

## Agents (4)

| Agent | Why an agent and not a skill |
|---|---|
| **Planner** | Needs persistent persona across multi-turn clarification (clarify → scope → decompose → persist). Tool restriction to `search, edit` is load-bearing: prevents accidental code edits while planning. |
| **Socrates** | Adversarial critique benefits from a sustained read-only stance across a long conversation; `tools: [search]` enforces this. A skill would lose the persona between invocations. |
| **Implementer** | Multi-turn execution: step → lint → test → log breadcrumb → next step. Skill would force re-loading context each turn. Tool list intentionally permissive (omitted) — Implementer needs the full tool set. |
| **Project Flow** | Requires `agents:` field to dispatch subagents (Planner, Socrates, Implementer). Skills cannot dispatch other agents — this is the load-bearing capability that makes this an agent. |

## Skills (6)

| Skill | Why a skill and not an agent |
|---|---|
| `breadcrumb` | One-shot: read latest log, brief next session. No persistence needed. |
| `architect-diagram` | One-shot: produce one Mermaid diagram. |
| `slide-deck` | One-shot: produce one deck. |
| `visualisation` | One-shot: produce one chart. |
| `experiment-logger` | One-shot: capture one experiment write-up. |
| `pr-writeup` | One-shot: produce one PR description. |

## Open question (deferred)

Could **Implementer** be a skill with `context: fork`? Possibly — the forked-context model would isolate per-step tool use. But the breadcrumb-logging discipline benefits from staying in the parent context so the user sees progress. Keep as agent for now.
