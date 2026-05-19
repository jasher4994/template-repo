# Copilot custom-agent frontmatter — verification matrix

Verified against [Custom agents in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents) on 2026-05-19.

## Fields used in `.github/agents/*.agent.md`

| Field | Status | Notes |
|---|---|---|
| `name` | **Supported** | Optional. Falls back to filename if omitted. |
| `description` | **Supported** | Shown as placeholder in chat input. Used for auto-routing. |
| `argument-hint` | **Supported** | Hint text in chat input. |
| `tools` | **Supported, but values must match real tool names** | List of tool / tool set names. **Invalid names are silently ignored** (see "Note: If a given tool is not available when using the custom agent, it is ignored"). Predefined tool sets confirmed in docs: `search`, `edit`. Other tool names should be discovered via the chat tools picker (`#` in chat input) since the docs don't enumerate a complete list. |
| `agents` | **Supported** | List of subagent names. `*` for all, `[]` for none. **Requires `agent` tool in the `tools` array** to dispatch them. |
| `model` | **Supported** | String or priority array. Format: `Model Name (vendor)`, e.g. `Claude Sonnet 4.5 (copilot)`. |
| `user-invocable` | **Supported** | Default `true`. `false` hides from agent picker. |
| `disable-model-invocation` | **Supported** | Default `false`. `true` prevents subagent invocation. |
| `handoffs` | **Supported** | Not currently used in this repo. Worth considering for Planner→Implementer flow. |
| `target` | **Supported** | Not currently used. Values: `vscode`, `github-copilot`. |
| `mcp-servers` | **Supported** | Not currently used. |
| `hooks` | **Supported (Preview)** | Not currently used. |

## Original Socrates concern — confirmed and rejected (partially)

**Claim:** "`tools` may not be enforced; the field may be Claude-only fiction."

**Reality:** The field IS real and IS enforced — BUT the original `.agent.md` files in this repo used Claude-format tool names (`read`, `execute`, `todo`) which do not match VS Code's tool registry. The docs say unknown tool names are silently ignored, which means the restrictions were effectively no-ops. The agents had unrestricted tool access despite appearing to be sandboxed.

**Fix applied:** Tool names rewritten to use only documented values (`search`, `edit`, `agent`). For agents that legitimately need broader access (Implementer), `tools` is omitted entirely so the agent inherits the default tool set rather than appearing restricted-but-not-actually.

## Skills frontmatter — separately verified

Skills under `.github/skills/<name>/SKILL.md` use a different schema verified against the [Agent Skills doc](https://code.visualstudio.com/docs/copilot/customization/agent-skills):

| Field | Status |
|---|---|
| `name` | **Required.** Must match parent directory name. Lowercase + hyphens + digits only. Max 64 chars. Invalid names silently fail to load. |
| `description` | **Required.** Max 1024 chars. Used for auto-routing. |
| `argument-hint`, `user-invocable`, `disable-model-invocation`, `context: fork` | Optional, all supported. |

Current skills in this repo all conform.
