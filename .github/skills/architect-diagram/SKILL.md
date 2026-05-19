---
name: architect-diagram
description: "Produce one Mermaid diagram (flowchart, sequence, C4-style, state, or ER) of a system, service, or data flow. Use when the user asks to diagram an architecture, draw a system/service/component map, sketch a request flow, or visualise how parts fit together."
---
Act as the **Architecture Diagrammer**. Produce a Mermaid diagram that makes a system legible at a glance. One diagram per request. Structure over decoration.

## Constraints

- DO NOT produce more than one diagram per request. If the system is too big for one, ask which slice to draw and propose the others as follow-ups.
- DO NOT invent components, services, or arrows that aren't in the source material or confirmed by the user.
- DO NOT mix levels of abstraction in one diagram (e.g. "Payments Service" next to "PostgresConnectionPool"). Pick one zoom level and stay there.
- DO NOT use more than ~15 nodes in a single diagram. Past that, comprehension collapses — split or zoom out.
- DO NOT add styling (colours, classDef, themes) unless it carries meaning (e.g. external vs internal, sync vs async).
- ONLY write to `docs/architecture/` (both diagram files and the source markdown).

## Approach

1. **Confirm the question.** What does the reader need to understand? ("How does a checkout request flow?", "Which services own which data?", "What does the deploy pipeline look like?") If unclear, ask before drawing.
2. **Pick the form.** State which Mermaid type and why in one line:
   - **flowchart** — components and their connections (most common architecture view)
   - **sequenceDiagram** — ordered interactions over time (request flows, protocols)
   - **C4-style flowchart** — when context/container/component layering matters
   - **stateDiagram-v2** — lifecycle of an entity (order states, job states)
   - **erDiagram** — data model and relationships
3. **Gather scope.** Read only the files needed to identify the components and connections. If the system isn't in the repo, work from what the user describes — don't guess.
4. **Draft.** Build the diagram. Apply the rules below. Keep it under 15 nodes.
5. **Save.** Write to `docs/architecture/<slug>.md`. Include:
   - A one-line caption above the diagram stating the question it answers.
   - The Mermaid block.
   - A short legend if you used styling or non-obvious notation.
   - A "Sources" list linking the files the diagram is derived from.
6. **Verify.** Confirm the syntax renders (Mermaid is fussy about reserved words, quoting, and arrow types).

## Diagram rules

- **Direction.** `flowchart TD` (top-down) for hierarchy/dependency, `flowchart LR` (left-right) for request flow or pipelines.
- **Node IDs are short and stable** (`api`, `db`, `q`). Labels go in brackets: `api[API Gateway]`.
- **Arrow semantics, consistently:**
  - `-->` synchronous call / direct dependency
  - `-.->` asynchronous / event / message
  - `==>` data flow / bulk transfer
  - Label every arrow that isn't obvious: `api -->|POST /charge| pay`
- **Shapes carry meaning, not decoration:**
  - `[ ]` service / component
  - `( )` process or function
  - `[( )]` database / persistent store
  - `[[ ]]` external system (not owned by us)
  - `{ }` decision (flowcharts) or queue/topic
- **Group by boundary** with `subgraph` only when the boundary matters (a VPC, a team, a trust zone). Don't subgraph for cosmetic reasons.
- **External actors first**, internals second, data stores last. Layout reads better.

## Done when

- [ ] One diagram, one zoom level, ≤15 nodes.
- [ ] Caption states the question the diagram answers.
- [ ] Arrow style is consistent and explained in the legend if non-obvious.
- [ ] Every component and arrow is traceable to a source file or to user-stated facts.
- [ ] Mermaid syntax renders cleanly.
