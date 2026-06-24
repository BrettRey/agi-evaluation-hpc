# AGI Evaluation Metrics: Core Second-Pass Formalization

This is a narrower follow-up formalization target. Focus on the metrics that should be easiest to specify directly from the paper without getting bogged down in special-function details.

Use Lean 4 with Mathlib.

## 1. Basic helpers

Define:

- `inUnitInterval (x : ℝ) : Prop := 0 ≤ x ∧ x ≤ 1`
- `avg` for a finite nonempty index type:
  - `avg f = (∑ i, f i) / Fintype.card ι`
- `cappedRatio (x y : ℝ) = min 1 (x / y)`

Prove:

- If `∀ i, f i ∈ [0,1]`, then `avg f ∈ [0,1]`
- If `x ≥ 0` and `y > 0`, then `cappedRatio x y ∈ [0,1]`

## 2. Weighted score and level-shift metrics

Define:

- `weightedScore w a = ∑ i, w i * a i`

For:

- a finite nonempty domain type `ι`
- a finite nonempty perturbation type `P`
- baseline profile `a0 : ι → ℝ`
- perturbed profiles `ap : P → ι → ℝ`

define:

- `meanScore a = avg a`
- `levelShift a0 ap = avg (fun j => cappedRatio (meanScore (ap j)) (meanScore a0))`
- `weightedLevelShift w a0 ap = avg (fun j => cappedRatio (weightedScore w (ap j)) (weightedScore w a0))`

Prove:

- `weightedScore w a ∈ [0,1]` if all weights are nonnegative, the weights sum to `1`, and all scores are in `[0,1]`
- `levelShift a0 ap ∈ [0,1]` if all perturbed scores are nonnegative and `meanScore a0 > 0`
- `weightedLevelShift w a0 ap ∈ [0,1]` if all weights are nonnegative, the weights sum to `1`, all scores are in `[0,1]`, and `weightedScore w a0 > 0`

## 3. Direct dCSI

For:

- a finite nonempty item type `T`
- a finite nonempty delay type `D`
- `score0 : T → ℝ`
- `scoreDelay : T → D → ℝ`

define:

- `dcsi score0 scoreDelay = avg (fun t => avg (fun d => cappedRatio (scoreDelay t d) (score0 t)))`

Prove:

- `dcsi score0 scoreDelay ∈ [0,1]` if all delayed scores are nonnegative and all baseline scores are strictly positive

## 4. Raw error-sequence definitions for eCSI

Let `e : Fin (n + 2) → ℝ` represent an error sequence with at least two attempts.

Define:

- `positivePart x = max 0 x`
- `transitionDiff e k = e k.succ - e k.castSucc` for `k : Fin (n + 1)`
- `totalVariation e = ∑ k, |transitionDiff e k|`
- `backslidingNumerator e = ∑ k, positivePart (transitionDiff e k)`
- `backslidingRatio eps e = backslidingNumerator e / (totalVariation e + eps)`
- `improvement eps e = max 0 ((e 0 - e (Fin.last (n + 1))) / max (e 0) eps)`
- `ecsiFromErrors eps e = improvement eps e * (1 - min 1 (backslidingRatio eps e))`

Prove:

- `backslidingRatio eps e ∈ [0,1]` if `0 < eps`
- `improvement eps e ∈ [0,1]` if all error values lie in `[0,1]` and `0 < eps`
- `ecsiFromErrors eps e ∈ [0,1]` under the same conditions

## Constraints

- Keep the file compact.
- Prefer short robust proofs.
- Prioritize sections 3 and 4 if time is limited.
