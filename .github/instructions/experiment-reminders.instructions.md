---
description: "Nudge the user to log data-science experiments when training, evaluation, or comparison language appears in code or chat."
applyTo: "experiments/**,notebooks/**,**/*.ipynb,**/train*.py,**/eval*.py,**/*experiment*.py"
---
# Experiment logging discipline

This project treats experiments as first-class artefacts. When working in files matching this instruction:

- If the user runs, modifies, or discusses a **training run, evaluation, ablation, sweep, baseline comparison, or model benchmark**, and there is no matching recent entry under `experiments/`, offer to invoke the `/experiment-logger` skill.
- Do **not** silently capture results in the chat and move on. Either log it, or the user explicitly says "skip".
- Do **not** propose fixes to a failing experiment until it has been logged. The log is the cheapest version of the conversation "what did we actually run?".
- When the user references "the last run" or "previous experiment", read `experiments/INDEX.md` to identify what they mean before answering.

Trigger phrases (require co-occurrence with a DS context word — model, metric, dataset, checkpoint, loss, accuracy, F1, AUC, baseline run): *"trained the model"*, *"finetuned"*, *"got X% accuracy/F1"*, *"baseline run"*, *"swept hyperparameters"*, *"ablation"*, *"evaluated on <dataset>"*, *"vs. the previous run"*, *"loss went down/up"*, *"checkpoint <n>"*.

Intentionally NOT triggers (too ambiguous): bare *"evaluated"*, *"compared"*, *"tested"*, *"benchmarked"* without a model/metric/dataset object. Code review uses these constantly. Asking every time would train the user to ignore the nudge.

If you genuinely cannot tell whether something is a DS experiment, ask one clarifying question rather than firing the prompt.
