# experiments/

One write-up per experiment, produced by the **Experiment Logger** agent.

## Files

- `<YYYY-MM-DD>-<slug>.md` — the log: hypothesis, setup, method, results, interpretation, decision.
- `INDEX.md` — single-line summary of every experiment, newest first.
- `raw/<slug>.json` (optional) — raw metrics dumped from the run. Logs link to these but never inline them.

## Conventions

- One experiment = one hypothesis (or one explicit `type: exploration`).
- Every number in a log cites the command or file that produced it.
- Dirty working trees are logged and flagged — they are not reproducible.
- Negative results are logged with the same rigour as positive ones.
- Logs are immutable once the experiment is done. New experiment = new file, with a `Related: previous run` link.
