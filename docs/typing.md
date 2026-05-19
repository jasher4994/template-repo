# Working with `mypy --strict`

This project runs `mypy --strict` on every commit (via pre-commit) and in `make lint`. Strict mode catches whole categories of bugs early — but it can also block you when third-party libraries lack type stubs or when you're prototyping.

This page documents the escape hatches and when to reach for each one.

## When you legitimately need to silence a check

### Per-line: a specific error code

```python
result = legacy_call()  # type: ignore[no-untyped-call]
```

Always include the specific code in brackets. A bare `# type: ignore` silences every error on that line forever, hiding future bugs you'd want to know about.

### Per-module: a missing third-party stub

Most pain comes from libraries without typed stubs (e.g. older scientific packages). Add an override in `pyproject.toml`:

```toml
[[tool.mypy.overrides]]
module = ["scipy.*", "matplotlib.*"]
ignore_missing_imports = true
```

This says "I trust these imports exist; don't fail just because there are no stubs". It does NOT turn off type-checking in your own code that uses them.

### Per-function: an opaque external call

If you're calling into something dynamic (e.g. a `**kwargs` API) and you want to type the boundary cleanly:

```python
from typing import Any, cast

raw: Any = external_api(query)
result = cast(MyTypedDict, raw)
```

`cast` is a runtime no-op — it just tells mypy to trust you. Pay this cost at the boundary, then keep the rest of your code strict.

## Worked example: adding `pandas` without stubs

A first attempt to use pandas under `mypy --strict` usually surfaces:

```
error: Skipping analyzing "pandas": module is installed, but missing library stubs or py.typed marker
```

Two options:

1. **Install the stubs** (preferred):
   ```bash
   uv pip install pandas-stubs
   ```
   Then add to `pyproject.toml` dependencies:
   ```toml
   [project.optional-dependencies]
   dev = [..., "pandas-stubs"]
   ```

2. **Silence the import** (if stubs don't exist or are stale):
   ```toml
   [[tool.mypy.overrides]]
   module = ["pandas.*"]
   ignore_missing_imports = true
   ```

After either fix, your own functions still need explicit types:

```python
import pandas as pd

def load_users(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
```

## When to relax `--strict` entirely (don't)

Resist the urge. The cost of being strict from day one is small; the cost of retrofitting strictness onto a large untyped codebase is large. If you're feeling pressure to relax it everywhere, the right move is usually:

- Move the messy code into a single module
- Add `[[tool.mypy.overrides]]` for that one module with `disallow_untyped_defs = false`
- Keep the rest of the project strict

This contains the mess instead of spreading it.

## Quick reference

| Situation | Fix |
|---|---|
| One line, known code | `# type: ignore[code]` |
| Third-party import has no stubs | `[[tool.mypy.overrides]]` with `ignore_missing_imports` |
| Boundary to dynamic data | `cast(T, value)` |
| Whole module is unavoidably dynamic | Module-level overrides with `disallow_untyped_defs = false` |
| All my code feels strict | Good. Keep going. |
