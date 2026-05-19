# docs/

Outputs and reference material produced by this project and its agents.

## Layout

| Path                  | Purpose                                            | Written by                      |
|-----------------------|----------------------------------------------------|---------------------------------|
| `architecture/`       | Mermaid diagrams of systems and flows              | `Architecture Diagrammer` agent |
| `breadcrumbs/`        | Append-only implementation logs (one per plan)     | `Implementer` agent             |
| `decks/`              | Marp-compatible slide decks                        | `Slide Deck Author` agent       |
| `decks/assets/`       | Images/media used in decks                         | `Slide Deck Author` agent       |
| `figures/`            | Generated charts (PNG/SVG) and mermaid data viz    | `Visualisation Specialist` agent|

Related folders at the repo root:

| Path              | Purpose                                            | Written by                      |
|-------------------|----------------------------------------------------|---------------------------------|
| `plans/`          | Feature plans, one per slug; orchestrator status   | `Planner`, `Project Flow`       |
| `scripts/figures/`| Source scripts for `docs/figures/` (reproducible)  | `Visualisation Specialist`      |

## Conventions

- One slug per piece of work. The same slug links plan, breadcrumb, and any artefacts:
  - `plans/oauth-login.md`
  - `docs/breadcrumbs/oauth-login.md`
  - `docs/architecture/oauth-login.md` (if applicable)
- Filenames are lowercase, hyphen-separated.
- Generated artefacts (figures, decks) are committed — they're the deliverable.
- Breadcrumb logs are append-only and grouped by date; never rewritten.
