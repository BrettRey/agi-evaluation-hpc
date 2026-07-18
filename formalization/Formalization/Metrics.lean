import Mathlib

noncomputable section

open Finset BigOperators

set_option autoImplicit false

namespace Formalization

/-!
# Algebraic estimands for target-indexed evaluation

This module formalizes the compact algebraic core of `metrics_spec_v3.md`.
It proves raw-estimand identities and bounds only. Tail membership remains an
external selector, and no theorem addresses sampling, noise correction,
holdout validity, transport, construct validity, or mechanism.
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

theorem avg_add {ι : Type*} [Fintype ι] [Nonempty ι] (f g : ι → ℝ) :
    avg (fun i => f i + g i) = avg f + avg g := by
  unfold avg
  rw [Finset.sum_add_distrib]
  ring

theorem avg_sub {ι : Type*} [Fintype ι] [Nonempty ι] (f g : ι → ℝ) :
    avg (fun i => f i - g i) = avg f - avg g := by
  unfold avg
  rw [Finset.sum_sub_distrib]
  ring

theorem abs_avg_le_avg_abs {ι : Type*} [Fintype ι] [Nonempty ι]
    (f : ι → ℝ) : |avg f| ≤ avg (fun i => |f i|) := by
  have hcard : 0 < (Fintype.card ι : ℝ) := by
    exact_mod_cast Fintype.card_pos
  unfold avg
  rw [abs_div, abs_of_nonneg hcard.le]
  exact div_le_div_of_nonneg_right
    (by simpa using Finset.abs_sum_le_sum_abs f Finset.univ) hcard.le

/-! ## Positive parts, signed change, INS, and directional components -/

def positivePart (x : ℝ) : ℝ := max 0 x

theorem positivePart_nonneg (x : ℝ) : 0 ≤ positivePart x := by
  exact le_max_left 0 x

theorem positivePart_sub_positivePart_neg (x : ℝ) :
    positivePart x - positivePart (-x) = x := by
  by_cases hx : 0 ≤ x
  · simp [positivePart, max_eq_right hx, max_eq_left (neg_nonpos.mpr hx)]
  · have hx' : x ≤ 0 := le_of_not_ge hx
    simp [positivePart, max_eq_left hx', max_eq_right (neg_nonneg.mpr hx')]

theorem positivePart_add_positivePart_neg (x : ℝ) :
    positivePart x + positivePart (-x) = |x| := by
  by_cases hx : 0 ≤ x
  · simp [positivePart, max_eq_right hx, max_eq_left (neg_nonpos.mpr hx),
      abs_of_nonneg hx]
  · have hx' : x ≤ 0 := le_of_not_ge hx
    simp [positivePart, max_eq_left hx', max_eq_right (neg_nonneg.mpr hx'),
      abs_of_nonpos hx']

theorem positivePart_inUnitInterval {x : ℝ} (hx : inSignedUnitInterval x) :
    inUnitInterval (positivePart x) := by
  constructor
  · exact positivePart_nonneg x
  · exact max_le zero_le_one hx.2

def scoreDelta {ι : Type*} (baseline perturbed : ι → ℝ) (i : ι) : ℝ :=
  perturbed i - baseline i

/-- Mean signed level change. Improvements and losses may cancel by design. -/
def signedChange {ι : Type*} [Fintype ι] [Nonempty ι]
    (baseline perturbed : ι → ℝ) : ℝ :=
  avg (scoreDelta baseline perturbed)

/-- Mean absolute paired item change, called INS in the specification. -/
def meanAbsoluteChange {ι : Type*} [Fintype ι] [Nonempty ι]
    (baseline perturbed : ι → ℝ) : ℝ :=
  avg (fun i => |scoreDelta baseline perturbed i|)

abbrev ins := @meanAbsoluteChange

def positiveFlow {ι : Type*} [Fintype ι] [Nonempty ι]
    (baseline perturbed : ι → ℝ) : ℝ :=
  avg (fun i => positivePart (scoreDelta baseline perturbed i))

def negativeFlow {ι : Type*} [Fintype ι] [Nonempty ι]
    (baseline perturbed : ι → ℝ) : ℝ :=
  avg (fun i => positivePart (-scoreDelta baseline perturbed i))

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

theorem abs_signedChange_le_meanAbsoluteChange
    {ι : Type*} [Fintype ι] [Nonempty ι]
    (baseline perturbed : ι → ℝ) :
    |signedChange baseline perturbed| ≤ meanAbsoluteChange baseline perturbed := by
  exact abs_avg_le_avg_abs (scoreDelta baseline perturbed)

theorem signedChange_eq_positiveFlow_sub_negativeFlow
    {ι : Type*} [Fintype ι] [Nonempty ι]
    (baseline perturbed : ι → ℝ) :
    signedChange baseline perturbed =
      positiveFlow baseline perturbed - negativeFlow baseline perturbed := by
  unfold signedChange positiveFlow negativeFlow
  rw [← avg_sub]
  apply congrArg avg
  funext i
  exact (positivePart_sub_positivePart_neg
    (scoreDelta baseline perturbed i)).symm

theorem meanAbsoluteChange_eq_positiveFlow_add_negativeFlow
    {ι : Type*} [Fintype ι] [Nonempty ι]
    (baseline perturbed : ι → ℝ) :
    meanAbsoluteChange baseline perturbed =
      positiveFlow baseline perturbed + negativeFlow baseline perturbed := by
  unfold meanAbsoluteChange positiveFlow negativeFlow
  rw [← avg_add]
  apply congrArg avg
  funext i
  exact (positivePart_add_positivePart_neg
    (scoreDelta baseline perturbed i)).symm

/-! ## Externally selected tails -/

/--
Mean signed change on an externally selected tail. The selector is an input;
this definition does not formalize sorting, noisy selection, or cross-fitting.
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

/-- Signed WTD for an externally selected lower tail. -/
def worstTailDegradation {ι τ : Type*} [Fintype τ] [Nonempty τ]
    (select : τ → ι) (baseline perturbed : ι → ℝ) : ℝ :=
  -selectedTailMeanChange select baseline perturbed

abbrev wtd := @worstTailDegradation

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

/-- Target-specific WTL for an externally selected high-loss tail. -/
def worstTailLoss {ι τ : Type*} [Fintype τ] [Nonempty τ]
    (select : τ → ι) (loss : ι → ℝ) : ℝ :=
  avg (fun j => loss (select j))

abbrev wtl := @worstTailLoss

theorem worstTailLoss_inUnitInterval
    {ι τ : Type*} [Fintype τ] [Nonempty τ]
    {select : τ → ι} {loss : ι → ℝ}
    (hloss : ∀ i, inUnitInterval (loss i)) :
    inUnitInterval (worstTailLoss select loss) := by
  exact avg_inUnitInterval fun j => hloss (select j)

/-! ## Retention of above-pretest gain -/

def abovePretestGain {ι : Type*} (pre later : ι → ℝ) (i : ι) : ℝ :=
  positivePart (scoreDelta pre later i)

theorem abovePretestGain_inUnitInterval {ι : Type*} {pre later : ι → ℝ}
    (hpre : ∀ i, inUnitInterval (pre i))
    (hlater : ∀ i, inUnitInterval (later i)) (i : ι) :
    inUnitInterval (abovePretestGain pre later i) := by
  exact positivePart_inUnitInterval
    (scoreDelta_inSignedUnitInterval hpre hlater i)

def retainedGain {ι : Type*} [Fintype ι]
    (pre immediate delayed : ι → ℝ) : ℝ :=
  (∑ i, min (abovePretestGain pre immediate i)
      (abovePretestGain pre delayed i)) /
    ∑ i, abovePretestGain pre immediate i

theorem retainedGain_inUnitInterval {ι : Type*} [Fintype ι]
    {pre immediate delayed : ι → ℝ}
    (hdenom : 0 < ∑ i, abovePretestGain pre immediate i) :
    inUnitInterval (retainedGain pre immediate delayed) := by
  unfold retainedGain inUnitInterval
  constructor
  · exact div_nonneg
      (Finset.sum_nonneg fun i _ =>
        le_min (positivePart_nonneg _) (positivePart_nonneg _))
      hdenom.le
  · exact div_le_one_of_le₀
      (Finset.sum_le_sum fun i _ => min_le_left
        (abovePretestGain pre immediate i) (abovePretestGain pre delayed i))
      hdenom.le

theorem retainedGain_inUnitInterval_of_avg_threshold
    {ι : Type*} [Fintype ι] [Nonempty ι]
    {pre immediate delayed : ι → ℝ} {γ : ℝ}
    (hγ : 0 < γ)
    (hthreshold : γ ≤ avg (abovePretestGain pre immediate)) :
    inUnitInterval (retainedGain pre immediate delayed) := by
  have havgpos : 0 < avg (abovePretestGain pre immediate) :=
    lt_of_lt_of_le hγ hthreshold
  have hcard : 0 < (Fintype.card ι : ℝ) := by
    exact_mod_cast Fintype.card_pos
  unfold avg at havgpos
  have hdenom : 0 < ∑ i, abovePretestGain pre immediate i := by
    rcases (div_pos_iff.mp havgpos) with h | h
    · exact h.1
    · exact False.elim ((not_lt_of_ge hcard.le) h.2)
  exact retainedGain_inUnitInterval hdenom

/-! ## Feedback trajectories -/

def transitionDiff (errors : ℕ → ℝ) (k : ℕ) : ℝ :=
  errors (k + 1) - errors k

def cumulativeErrorDecrease (errors : ℕ → ℝ) (steps : ℕ) : ℝ :=
  ∑ k ∈ Finset.range steps, positivePart (-transitionDiff errors k)

def cumulativeErrorIncrease (errors : ℕ → ℝ) (steps : ℕ) : ℝ :=
  ∑ k ∈ Finset.range steps, positivePart (transitionDiff errors k)

def endpointGain (errors : ℕ → ℝ) (steps : ℕ) : ℝ :=
  errors 0 - errors steps

def totalVariation (errors : ℕ → ℝ) (steps : ℕ) : ℝ :=
  ∑ k ∈ Finset.range steps, |transitionDiff errors k|

theorem cumulativeErrorDecrease_nonneg (errors : ℕ → ℝ) (steps : ℕ) :
    0 ≤ cumulativeErrorDecrease errors steps := by
  exact Finset.sum_nonneg fun k _ => positivePart_nonneg _

theorem cumulativeErrorIncrease_nonneg (errors : ℕ → ℝ) (steps : ℕ) :
    0 ≤ cumulativeErrorIncrease errors steps := by
  exact Finset.sum_nonneg fun k _ => positivePart_nonneg _

theorem sum_transitionDiff (errors : ℕ → ℝ) (steps : ℕ) :
    (∑ k ∈ Finset.range steps, transitionDiff errors k) =
      errors steps - errors 0 := by
  simpa [transitionDiff] using Finset.sum_range_sub errors steps

theorem cumulativeErrorDecrease_sub_increase
    (errors : ℕ → ℝ) (steps : ℕ) :
    cumulativeErrorDecrease errors steps -
      cumulativeErrorIncrease errors steps = endpointGain errors steps := by
  calc
    cumulativeErrorDecrease errors steps - cumulativeErrorIncrease errors steps =
        ∑ k ∈ Finset.range steps,
          (positivePart (-transitionDiff errors k) -
            positivePart (transitionDiff errors k)) := by
          simp [cumulativeErrorDecrease, cumulativeErrorIncrease,
            Finset.sum_sub_distrib]
    _ = ∑ k ∈ Finset.range steps, -transitionDiff errors k := by
      apply Finset.sum_congr rfl
      intro k _
      simpa using positivePart_sub_positivePart_neg (-transitionDiff errors k)
    _ = -(∑ k ∈ Finset.range steps, transitionDiff errors k) := by
      rw [Finset.sum_neg_distrib]
    _ = -(errors steps - errors 0) := by rw [sum_transitionDiff]
    _ = endpointGain errors steps := by simp [endpointGain]

theorem totalVariation_eq_decrease_add_increase
    (errors : ℕ → ℝ) (steps : ℕ) :
    totalVariation errors steps = cumulativeErrorDecrease errors steps +
      cumulativeErrorIncrease errors steps := by
  unfold totalVariation cumulativeErrorDecrease cumulativeErrorIncrease
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro k _
  simpa [add_comm] using
    (positivePart_add_positivePart_neg (transitionDiff errors k)).symm

theorem endpointGain_inSignedUnitInterval {errors : ℕ → ℝ} {steps : ℕ}
    (herrors : ∀ k, inUnitInterval (errors k)) :
    inSignedUnitInterval (endpointGain errors steps) := by
  unfold endpointGain inSignedUnitInterval inUnitInterval at *
  constructor <;> linarith [(herrors 0).1, (herrors 0).2,
    (herrors steps).1, (herrors steps).2]

theorem abs_endpointGain_le_totalVariation (errors : ℕ → ℝ) (steps : ℕ) :
    |endpointGain errors steps| ≤ totalVariation errors steps := by
  rw [← cumulativeErrorDecrease_sub_increase,
    totalVariation_eq_decrease_add_increase, abs_le]
  constructor <;>
    linarith [cumulativeErrorDecrease_nonneg errors steps,
      cumulativeErrorIncrease_nonneg errors steps]

end Formalization
