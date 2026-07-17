import Mathlib

noncomputable section

open Finset BigOperators

set_option autoImplicit false

namespace Formalization

/-!
# Algebraic estimands for projectibility-first evaluation

This module formalizes only elementary definitions and range properties.  In
particular, the theorems below do not establish that an empirical estimate is
reliable, that a chosen projection target is valid, or that behavioural
stability identifies a mechanism.
-/

def inUnitInterval (x : ℝ) : Prop := 0 ≤ x ∧ x ≤ 1

def inSignedUnitInterval (x : ℝ) : Prop := -1 ≤ x ∧ x ≤ 1

def avg {ι : Type*} [Fintype ι] [Nonempty ι] (f : ι → ℝ) : ℝ :=
  (∑ i, f i) / Fintype.card ι

theorem avg_mem_interval {ι : Type*} [Fintype ι] [Nonempty ι]
    {lo hi : ℝ} {f : ι → ℝ} (hf : ∀ i, lo ≤ f i ∧ f i ≤ hi) :
    lo ≤ avg f ∧ avg f ≤ hi := by
  have hcard : 0 < (Fintype.card ι : ℝ) := by
    exact_mod_cast Fintype.card_pos
  unfold avg
  constructor
  · rw [le_div_iff₀ hcard]
    simpa [mul_comm] using
      (Finset.sum_le_sum fun i (_hi : i ∈ Finset.univ) => (hf i).1)
  · rw [div_le_iff₀ hcard]
    simpa [mul_comm] using
      (Finset.sum_le_sum fun i (_hi : i ∈ Finset.univ) => (hf i).2)

theorem avg_inUnitInterval {ι : Type*} [Fintype ι] [Nonempty ι] {f : ι → ℝ}
    (hf : ∀ i, inUnitInterval (f i)) : inUnitInterval (avg f) := by
  exact avg_mem_interval hf

theorem avg_inSignedUnitInterval {ι : Type*} [Fintype ι] [Nonempty ι]
    {f : ι → ℝ} (hf : ∀ i, inSignedUnitInterval (f i)) :
    inSignedUnitInterval (avg f) := by
  exact avg_mem_interval hf

/-! ## Profile-shape similarity -/

/-- Map an admissible correlation from `[-1,1]` to `[0,1]`. -/
def profileShapeSimilarity (r : ℝ) : ℝ := (1 + r) / 2

theorem profileShapeSimilarity_inUnitInterval {r : ℝ}
    (hr : inSignedUnitInterval r) :
    inUnitInterval (profileShapeSimilarity r) := by
  unfold profileShapeSimilarity inUnitInterval inSignedUnitInterval at *
  constructor <;> linarith

/-! ## Signed and absolute change -/

def scoreDelta {ι : Type*} (baseline perturbed : ι → ℝ) (i : ι) : ℝ :=
  perturbed i - baseline i

/-- Mean signed level change. Improvements and losses may cancel by design. -/
def signedChange {ι : Type*} [Fintype ι] [Nonempty ι]
    (baseline perturbed : ι → ℝ) : ℝ :=
  avg (scoreDelta baseline perturbed)

/-- Mean absolute item change, called INS in the paper. -/
def meanAbsoluteChange {ι : Type*} [Fintype ι] [Nonempty ι]
    (baseline perturbed : ι → ℝ) : ℝ :=
  avg (fun i => |scoreDelta baseline perturbed i|)

abbrev ins := @meanAbsoluteChange

theorem scoreDelta_inSignedUnitInterval {ι : Type*} {baseline perturbed : ι → ℝ}
    (hbaseline : ∀ i, inUnitInterval (baseline i))
    (hperturbed : ∀ i, inUnitInterval (perturbed i)) (i : ι) :
    inSignedUnitInterval (scoreDelta baseline perturbed i) := by
  unfold scoreDelta inSignedUnitInterval inUnitInterval at *
  constructor <;> linarith [(hbaseline i).1, (hbaseline i).2,
    (hperturbed i).1, (hperturbed i).2]

theorem signedChange_inSignedUnitInterval {ι : Type*} [Fintype ι] [Nonempty ι]
    {baseline perturbed : ι → ℝ}
    (hbaseline : ∀ i, inUnitInterval (baseline i))
    (hperturbed : ∀ i, inUnitInterval (perturbed i)) :
    inSignedUnitInterval (signedChange baseline perturbed) := by
  exact avg_inSignedUnitInterval
    (scoreDelta_inSignedUnitInterval hbaseline hperturbed)

theorem meanAbsoluteChange_inUnitInterval {ι : Type*} [Fintype ι] [Nonempty ι]
    {baseline perturbed : ι → ℝ}
    (hbaseline : ∀ i, inUnitInterval (baseline i))
    (hperturbed : ∀ i, inUnitInterval (perturbed i)) :
    inUnitInterval (meanAbsoluteChange baseline perturbed) := by
  apply avg_inUnitInterval
  intro i
  constructor
  · exact abs_nonneg _
  · rw [abs_le]
    exact scoreDelta_inSignedUnitInterval hbaseline hperturbed i

/--
Mean signed change on an externally selected tail.  The selector is an input:
this definition does not formalize, or validate, the procedure used to choose
the tail.
-/
def selectedTailMeanChange {ι τ : Type*} [Fintype τ] [Nonempty τ]
    (select : τ → ι) (baseline perturbed : ι → ℝ) : ℝ :=
  avg (fun j => scoreDelta baseline perturbed (select j))

theorem selectedTailMeanChange_inSignedUnitInterval
    {ι τ : Type*} [Fintype τ] [Nonempty τ]
    {select : τ → ι} {baseline perturbed : ι → ℝ}
    (hbaseline : ∀ i, inUnitInterval (baseline i))
    (hperturbed : ∀ i, inUnitInterval (perturbed i)) :
    inSignedUnitInterval (selectedTailMeanChange select baseline perturbed) := by
  apply avg_inSignedUnitInterval
  intro j
  exact scoreDelta_inSignedUnitInterval hbaseline hperturbed (select j)

/--
Worst-tail degradation (WTD) for an externally selected tail.  Negating the
tail's mean signed change makes score losses positive.
-/
def worstTailDegradation {ι τ : Type*} [Fintype τ] [Nonempty τ]
    (select : τ → ι) (baseline perturbed : ι → ℝ) : ℝ :=
  -selectedTailMeanChange select baseline perturbed

theorem worstTailDegradation_inSignedUnitInterval
    {ι τ : Type*} [Fintype τ] [Nonempty τ]
    {select : τ → ι} {baseline perturbed : ι → ℝ}
    (hbaseline : ∀ i, inUnitInterval (baseline i))
    (hperturbed : ∀ i, inUnitInterval (perturbed i)) :
    inSignedUnitInterval (worstTailDegradation select baseline perturbed) := by
  have htail := selectedTailMeanChange_inSignedUnitInterval
    (select := select) hbaseline hperturbed
  unfold worstTailDegradation inSignedUnitInterval
  constructor <;> linarith [htail.1, htail.2]

/-! ## Delayed retention -/

/--
Retained mass at one specified delay.  Scores are compared item by item before
summing, so no per-item division by a zero baseline is required.
-/
def retainedMass {ι : Type*} [Fintype ι]
    (baseline delayed : ι → ℝ) : ℝ :=
  (∑ i, min (baseline i) (delayed i)) / ∑ i, baseline i

theorem retainedMass_inUnitInterval {ι : Type*} [Fintype ι]
    {baseline delayed : ι → ℝ}
    (hbaseline : ∀ i, 0 ≤ baseline i)
    (hdelayed : ∀ i, 0 ≤ delayed i)
    (hdenom : 0 < ∑ i, baseline i) :
    inUnitInterval (retainedMass baseline delayed) := by
  unfold retainedMass inUnitInterval
  constructor
  · exact div_nonneg
      (Finset.sum_nonneg fun i _ => le_min (hbaseline i) (hdelayed i))
      hdenom.le
  · exact div_le_one_of_le₀
      (Finset.sum_le_sum fun i _ => min_le_left (baseline i) (delayed i))
      hdenom.le

/-! ## Feedback trajectories -/

/-- Reduction in error between the initial and final feedback rounds. -/
def endpointGain (initialError finalError : ℝ) : ℝ :=
  initialError - finalError

theorem endpointGain_inSignedUnitInterval {initialError finalError : ℝ}
    (hinitial : inUnitInterval initialError)
    (hfinal : inUnitInterval finalError) :
    inSignedUnitInterval (endpointGain initialError finalError) := by
  unfold endpointGain inSignedUnitInterval inUnitInterval at *
  constructor <;> linarith

def positivePart (x : ℝ) : ℝ := max 0 x

def transitionDiff {n : ℕ} (errors : Fin (n + 2) → ℝ)
    (k : Fin (n + 1)) : ℝ :=
  errors k.succ - errors k.castSucc

def totalVariation {n : ℕ} (errors : Fin (n + 2) → ℝ) : ℝ :=
  ∑ k, |transitionDiff errors k|

def backslidingNumerator {n : ℕ} (errors : Fin (n + 2) → ℝ) : ℝ :=
  ∑ k, positivePart (transitionDiff errors k)

/--
Exact share of error-path variation due to error-increasing transitions.  A
constant trajectory has no transition variation and is assigned value zero.
-/
def backslidingFraction {n : ℕ} (errors : Fin (n + 2) → ℝ) : ℝ :=
  if totalVariation errors = 0 then 0
  else backslidingNumerator errors / totalVariation errors

theorem backslidingFraction_inUnitInterval {n : ℕ}
    {errors : Fin (n + 2) → ℝ} :
    inUnitInterval (backslidingFraction errors) := by
  have hvariation_nonneg : 0 ≤ totalVariation errors :=
    Finset.sum_nonneg fun _ _ => abs_nonneg _
  have hnumerator_nonneg : 0 ≤ backslidingNumerator errors :=
    Finset.sum_nonneg fun _ _ => le_max_left _ _
  have hnumerator_le : backslidingNumerator errors ≤ totalVariation errors :=
    Finset.sum_le_sum fun _ _ => by
      cases max_cases 0
          (errors (Fin.succ ‹_›) - errors (Fin.castSucc ‹_›)) <;>
      cases abs_cases
          (errors (Fin.succ ‹_›) - errors (Fin.castSucc ‹_›)) <;>
      linarith!
  unfold backslidingFraction
  split_ifs with hzero
  · exact ⟨le_rfl, zero_le_one⟩
  · exact ⟨div_nonneg hnumerator_nonneg hvariation_nonneg,
      div_le_one_of_le₀ hnumerator_le hvariation_nonneg⟩

end Formalization
