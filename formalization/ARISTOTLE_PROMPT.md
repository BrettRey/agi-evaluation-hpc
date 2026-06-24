This Lean project formalizes the scoring layer of a paper on AGI evaluation.

Work only inside this package. Do not add unrelated abstractions. The target file is `Formalization/Metrics.lean`.

Task:

1. Replace the `sorry` proofs in `Formalization/Metrics.lean` with valid Lean 4 proofs.
2. Keep the existing definitions unless a tiny refactor is necessary to make the proofs go through cleanly.
3. Preserve the intended interpretation of the definitions:
   - `priorWeight` is the pointwise weight from Eq. (prior_weights)
   - `sum_priorWeights_eq_one` should show normalization is preserved if both input weight families sum to 1
   - `pcsi` maps a similarity score in `[-1,1]` into `[0,1]`
   - `cappedRatio` is the generic `min 1 (x / y)` pattern used in the dCSI and level-shift formulas
   - `ecsi` is bounded in `[0,1]` when improvement is in `[0,1]` and backsliding is nonnegative
   - `csiCore` and `csi` should both be shown to lie in `[0,1]` when all inputs are in `[0,1]`
4. Prefer short, robust proofs using Mathlib lemmas and `nlinarith` where appropriate.
5. Do not weaken the theorem statements unless strictly necessary. If one statement truly needs a stronger hypothesis, make the smallest principled change and explain it in the summary.

Goal: the package should build cleanly with these proofs completed.
