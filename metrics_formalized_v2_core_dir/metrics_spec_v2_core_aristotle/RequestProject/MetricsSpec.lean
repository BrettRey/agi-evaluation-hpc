import Mathlib

open Finset BigOperators

noncomputable section

/-! # AGI Evaluation Metrics: Core Second-Pass Formalization

This file formalizes the core metrics from the AGI evaluation metrics specification,
including basic helpers, weighted scores, level-shift metrics, dCSI, and eCSI.
-/

-- ============================================================================
-- § 1. Basic helpers
-- ============================================================================

/-- A real number lies in the unit interval `[0, 1]`. -/
def inUnitInterval (x : ℝ) : Prop := 0 ≤ x ∧ x ≤ 1

/-- Average of `f` over a finite nonempty index type. -/
def avg {ι : Type*} [Fintype ι] [Nonempty ι] (f : ι → ℝ) : ℝ :=
  (∑ i, f i) / Fintype.card ι

/-- Capped ratio: `min 1 (x / y)`. -/
def cappedRatio (x y : ℝ) : ℝ := min 1 (x / y)

theorem avg_inUnitInterval {ι : Type*} [Fintype ι] [Nonempty ι] {f : ι → ℝ}
    (hf : ∀ i, inUnitInterval (f i)) : inUnitInterval (avg f) := by
  exact ⟨ div_nonneg ( Finset.sum_nonneg fun i _ => hf i |>.1 ) ( Nat.cast_nonneg _ ), div_le_one_of_le₀ ( le_trans ( Finset.sum_le_sum fun i _ => hf i |>.2 ) ( by simp ) ) ( Nat.cast_nonneg _ ) ⟩

theorem cappedRatio_inUnitInterval {x y : ℝ} (hx : 0 ≤ x) (hy : 0 < y) :
    inUnitInterval (cappedRatio x y) := by
  exact ⟨ by unfold cappedRatio; exact le_min zero_le_one ( div_nonneg hx hy.le ), by unfold cappedRatio; exact min_le_left _ _ ⟩

-- ============================================================================
-- § 2. Weighted score and level-shift metrics
-- ============================================================================

/-- Weighted score: `∑ i, w i * a i`. -/
def weightedScore {ι : Type*} [Fintype ι] (w a : ι → ℝ) : ℝ :=
  ∑ i, w i * a i

/-- Mean score is just the average. -/
def meanScore {ι : Type*} [Fintype ι] [Nonempty ι] (a : ι → ℝ) : ℝ := avg a

/-- Level shift metric. -/
def levelShift {ι P : Type*} [Fintype ι] [Nonempty ι] [Fintype P] [Nonempty P]
    (a0 : ι → ℝ) (ap : P → ι → ℝ) : ℝ :=
  avg (fun j => cappedRatio (meanScore (ap j)) (meanScore a0))

/-- Weighted level shift metric. -/
def weightedLevelShift {ι P : Type*} [Fintype ι] [Fintype P] [Nonempty P]
    (w : ι → ℝ) (a0 : ι → ℝ) (ap : P → ι → ℝ) : ℝ :=
  avg (fun j => cappedRatio (weightedScore w (ap j)) (weightedScore w a0))

theorem weightedScore_inUnitInterval {ι : Type*} [Fintype ι] {w a : ι → ℝ}
    (hw_nn : ∀ i, 0 ≤ w i) (hw_sum : ∑ i, w i = 1)
    (ha : ∀ i, inUnitInterval (a i)) : inUnitInterval (weightedScore w a) := by
  exact ⟨ Finset.sum_nonneg fun i _ => mul_nonneg ( hw_nn i ) ( ha i |>.1 ), hw_sum ▸ Finset.sum_le_sum fun i _ => mul_le_of_le_one_right ( hw_nn i ) ( ha i |>.2 ) ⟩

theorem levelShift_inUnitInterval {ι P : Type*} [Fintype ι] [Nonempty ι]
    [Fintype P] [Nonempty P]
    {a0 : ι → ℝ} {ap : P → ι → ℝ}
    (hap : ∀ j i, 0 ≤ ap j i)
    (h0 : 0 < meanScore a0) :
    inUnitInterval (levelShift a0 ap) := by
  refine' avg_inUnitInterval _;
  exact fun j => cappedRatio_inUnitInterval ( by exact div_nonneg ( Finset.sum_nonneg fun _ _ => hap _ _ ) ( Nat.cast_nonneg _ ) ) h0

theorem weightedLevelShift_inUnitInterval {ι P : Type*} [Fintype ι]
    [Fintype P] [Nonempty P]
    {w : ι → ℝ} {a0 : ι → ℝ} {ap : P → ι → ℝ}
    (hw_nn : ∀ i, 0 ≤ w i) (_hw_sum : ∑ i, w i = 1)
    (ha : ∀ j i, inUnitInterval (ap j i))
    (h0 : 0 < weightedScore w a0) :
    inUnitInterval (weightedLevelShift w a0 ap) := by
  apply_rules [ avg_inUnitInterval ];
  exact fun i => by rw [ inUnitInterval ] ; exact ⟨ by exact le_min zero_le_one ( div_nonneg ( by exact Finset.sum_nonneg fun _ _ => mul_nonneg ( hw_nn _ ) ( ha i _ |>.1 ) ) h0.le ), by exact min_le_left _ _ ⟩

-- ============================================================================
-- § 3. Direct dCSI
-- ============================================================================

/-- Direct dCSI metric. -/
def dcsi {T D : Type*} [Fintype T] [Nonempty T] [Fintype D] [Nonempty D]
    (score0 : T → ℝ) (scoreDelay : T → D → ℝ) : ℝ :=
  avg (fun t => avg (fun d => cappedRatio (scoreDelay t d) (score0 t)))

theorem dcsi_inUnitInterval {T D : Type*} [Fintype T] [Nonempty T]
    [Fintype D] [Nonempty D]
    {score0 : T → ℝ} {scoreDelay : T → D → ℝ}
    (hd : ∀ t d, 0 ≤ scoreDelay t d)
    (h0 : ∀ t, 0 < score0 t) :
    inUnitInterval (dcsi score0 scoreDelay) := by
  exact avg_inUnitInterval fun t => avg_inUnitInterval fun d => cappedRatio_inUnitInterval ( hd t d ) ( h0 t )

-- ============================================================================
-- § 4. Raw error-sequence definitions for eCSI
-- ============================================================================

/-- Positive part: `max 0 x`. -/
def positivePart (x : ℝ) : ℝ := max 0 x

/-- Transition difference of an error sequence. -/
def transitionDiff {n : ℕ} (e : Fin (n + 2) → ℝ) (k : Fin (n + 1)) : ℝ :=
  e k.succ - e k.castSucc

/-- Total variation of an error sequence. -/
def totalVariation {n : ℕ} (e : Fin (n + 2) → ℝ) : ℝ :=
  ∑ k, |transitionDiff e k|

/-- Backsliding numerator: sum of positive transition differences. -/
def backslidingNumerator {n : ℕ} (e : Fin (n + 2) → ℝ) : ℝ :=
  ∑ k, positivePart (transitionDiff e k)

/-- Backsliding ratio with smoothing parameter `eps`. -/
def backslidingRatio {n : ℕ} (eps : ℝ) (e : Fin (n + 2) → ℝ) : ℝ :=
  backslidingNumerator e / (totalVariation e + eps)

/-- Improvement metric with smoothing parameter `eps`. -/
def improvement {n : ℕ} (eps : ℝ) (e : Fin (n + 2) → ℝ) : ℝ :=
  max 0 ((e 0 - e (Fin.last (n + 1))) / max (e 0) eps)

/-- eCSI from error sequence. -/
def ecsiFromErrors {n : ℕ} (eps : ℝ) (e : Fin (n + 2) → ℝ) : ℝ :=
  improvement eps e * (1 - min 1 (backslidingRatio eps e))

theorem backslidingRatio_inUnitInterval {n : ℕ} {eps : ℝ} {e : Fin (n + 2) → ℝ}
    (heps : 0 < eps) :
    inUnitInterval (backslidingRatio eps e) := by
  constructor;
  · exact div_nonneg ( Finset.sum_nonneg fun _ _ => le_max_left _ _ ) ( add_nonneg ( Finset.sum_nonneg fun _ _ => abs_nonneg _ ) heps.le );
  · exact div_le_one_of_le₀ ( le_add_of_le_of_nonneg ( Finset.sum_le_sum fun _ _ => by cases max_cases 0 ( e ( Fin.succ ‹_› ) - e ( Fin.castSucc ‹_› ) ) <;> cases abs_cases ( e ( Fin.succ ‹_› ) - e ( Fin.castSucc ‹_› ) ) <;> linarith! ) heps.le ) ( add_nonneg ( Finset.sum_nonneg fun _ _ => abs_nonneg _ ) heps.le )

theorem improvement_inUnitInterval {n : ℕ} {eps : ℝ} {e : Fin (n + 2) → ℝ}
    (he : ∀ i, inUnitInterval (e i)) (heps : 0 < eps) :
    inUnitInterval (improvement eps e) := by
  refine' ⟨ _, _ ⟩;
  · exact le_max_left _ _;
  · refine' max_le_iff.mpr ⟨ _, _ ⟩;
    · norm_num;
    · rw [ div_le_iff₀ ] <;> cases max_cases ( e 0 ) eps <;> linarith [ he 0 |>.1, he 0 |>.2, he ( Fin.last ( n + 1 ) ) |>.1, he ( Fin.last ( n + 1 ) ) |>.2 ]

theorem ecsiFromErrors_inUnitInterval {n : ℕ} {eps : ℝ} {e : Fin (n + 2) → ℝ}
    (he : ∀ i, inUnitInterval (e i)) (heps : 0 < eps) :
    inUnitInterval (ecsiFromErrors eps e) := by
  constructor;
  · exact mul_nonneg ( improvement_inUnitInterval he heps |>.1 ) ( sub_nonneg.2 ( min_le_left _ _ ) );
  · refine' mul_le_one₀ _ _ _;
    · exact improvement_inUnitInterval he heps |>.2;
    · exact sub_nonneg.2 ( min_le_left _ _ );
    · exact sub_le_self _ ( le_min zero_le_one ( by exact ( backslidingRatio_inUnitInterval heps ) |>.1 ) )

end