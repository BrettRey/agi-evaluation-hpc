# AGI Evaluation Metrics: Second-Pass Formalization Target

This is a second-pass Lean 4 formalization target for the paper's scoring framework.

The first-pass formalization already established some generic boundedness facts. This pass should formalize the actual averaged metrics more directly.

Use Lean 4 with Mathlib.

## 1. Basic helper definitions

Define:

- `inUnitInterval (x : ℝ) : Prop := 0 ≤ x ∧ x ≤ 1`
- `avg` for a finite nonempty index type:
  - for `f : ι → ℝ`, where `ι` is a `Fintype` and `Nonempty`,
  - `avg f = (∑ i, f i) / Fintype.card ι`

Prove:

- If `∀ i, f i ∈ [0,1]`, then `avg f ∈ [0,1]`.

## 2. Fisher-averaged profile stability (pCSI)

Formalize the paper’s Fisher-averaged profile stability more directly.

Define for a finite nonempty family of correlations `r : ι → ℝ`:

- `fisherZBar r = avg (fun i => Real.artanh (r i))`
- `fisherRBar r = Real.tanh (fisherZBar r)`
- `pcsiFisher r = (1 + fisherRBar r) / 2`

Use the smallest principled domain condition:

- assume `∀ i, r i ∈ Set.Ioo (-1 : ℝ) 1`

Prove:

- `pcsiFisher r ∈ [0,1]`

If useful, also prove:

- `fisherRBar r ∈ Set.Ioo (-1 : ℝ) 1`

## 3. Level-shift metrics

Define:

- `meanScore a = avg a` for a score vector `a : ι → ℝ`
- `weightedScore w a = ∑ i, w i * a i`

For a finite nonempty perturbation family `P` and score vectors:

- baseline `a0 : ι → ℝ`
- perturbed profiles `ap : P → ι → ℝ`

define:

- `levelShift a0 ap = avg (fun j => min 1 (meanScore (ap j) / meanScore a0))`

For weights `w : ι → ℝ`, define:

- `weightedLevelShift w a0 ap = avg (fun j => min 1 (weightedScore w (ap j) / weightedScore w a0))`

Prove:

- `weightedScore w a ∈ [0,1]` if all weights are nonnegative, sum to `1`, and all scores are in `[0,1]`
- `levelShift a0 ap ∈ [0,1]` if all perturbed scores are nonnegative and `meanScore a0 > 0`
- `weightedLevelShift w a0 ap ∈ [0,1]` if all weights are nonnegative, sum to `1`, all scores are in `[0,1]`, and `weightedScore w a0 > 0`

## 4. Direct dCSI

Formalize the paper’s direct dCSI.

Let:

- `T` be a finite nonempty item type
- `D` be a finite nonempty delay type
- `score0 : T → ℝ`
- `scoreDelay : T → D → ℝ`

Define:

- `dcsi score0 scoreDelay = avg (fun t => avg (fun d => min 1 (scoreDelay t d / score0 t)))`

Prove:

- `dcsi score0 scoreDelay ∈ [0,1]` if all delayed scores are nonnegative and all baseline scores are strictly positive

## 5. Raw eCSI ingredients from an error sequence

Formalize `B` and `I` from an actual finite error sequence, not just from already-bounded abstract inputs.

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

## 6. Optional but desirable strengthening for CSI interpretation

If time permits, define:

- `csiArithmetic eps p d e = (max eps p + max eps d + max eps e) / 3`

and prove:

- `csi eps p d e ≤ csiArithmetic eps p d e`

under the same `[0,1]` assumptions used for the existing CSI formalization.

## Constraints

- Keep the development compact and close to the paper’s formulas.
- Use stronger hypotheses only where mathematically necessary.
- If one target is too expensive, prioritize sections 2, 4, and 5.
