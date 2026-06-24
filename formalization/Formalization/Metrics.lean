import Mathlib

noncomputable section

open Finset BigOperators

set_option autoImplicit false

namespace Formalization

def inUnitInterval (x : ℝ) : Prop := 0 ≤ x ∧ x ≤ 1

def avg {ι : Type*} [Fintype ι] [Nonempty ι] (f : ι → ℝ) : ℝ :=
  (∑ i, f i) / Fintype.card ι

theorem avg_inUnitInterval {ι : Type*} [Fintype ι] [Nonempty ι] {f : ι → ℝ}
    (hf : ∀ i, inUnitInterval (f i)) : inUnitInterval (avg f) := by
  exact ⟨div_nonneg
      (Finset.sum_nonneg fun i _ => (hf i).1)
      (Nat.cast_nonneg _),
    div_le_one_of_le₀
      (le_trans (Finset.sum_le_sum fun i _ => (hf i).2) (by simp))
      (Nat.cast_nonneg _)⟩

def priorWeight (lam g s : ℝ) : ℝ := lam * g + (1 - lam) * s

theorem priorWeight_inUnitInterval {lam g s : ℝ}
    (hlam : inUnitInterval lam) (hg : inUnitInterval g) (hs : inUnitInterval s) :
    inUnitInterval (priorWeight lam g s) := by
  exact ⟨by
      unfold priorWeight
      nlinarith [hlam.1, hlam.2, hg.1, hg.2, hs.1, hs.2], by
      unfold priorWeight
      nlinarith [hlam.1, hlam.2, hg.1, hg.2, hs.1, hs.2]⟩

def priorWeights {ι : Type*} [Fintype ι] (lam : ℝ) (g s : ι → ℝ) : ι → ℝ :=
  fun i => priorWeight lam (g i) (s i)

theorem sum_priorWeights_eq_one {ι : Type*} [Fintype ι]
    (lam : ℝ) (g s : ι → ℝ)
    (hg : (∑ i, g i) = 1) (hs : (∑ i, s i) = 1) :
    (∑ i, priorWeights lam g s i) = 1 := by
  unfold priorWeights priorWeight
  simp +decide [*, mul_comm, Finset.sum_add_distrib]
  rw [← Finset.mul_sum _ _ _, ← Finset.sum_mul, hg, hs]
  ring

def pcsi (rbar : ℝ) : ℝ := (1 + rbar) / 2

theorem pcsi_inUnitInterval {rbar : ℝ} (hrbar : -1 ≤ rbar ∧ rbar ≤ 1) :
    inUnitInterval (pcsi rbar) := by
  exact ⟨by
      unfold pcsi
      linarith, by
      unfold pcsi
      linarith⟩

def fisherZBar {ι : Type*} [Fintype ι] [Nonempty ι] (r : ι → ℝ) : ℝ :=
  avg (fun i => Real.artanh (r i))

def fisherRBar {ι : Type*} [Fintype ι] [Nonempty ι] (r : ι → ℝ) : ℝ :=
  Real.tanh (fisherZBar r)

def pcsiFisher {ι : Type*} [Fintype ι] [Nonempty ι] (r : ι → ℝ) : ℝ :=
  pcsi (fisherRBar r)

theorem fisherRBar_mem_Ioo {ι : Type*} [Fintype ι] [Nonempty ι] {r : ι → ℝ}
    (_hr : ∀ i, r i ∈ Set.Ioo (-1 : ℝ) 1) :
    fisherRBar r ∈ Set.Ioo (-1 : ℝ) 1 := by
  exact ⟨Real.neg_one_lt_tanh _, Real.tanh_lt_one _⟩

theorem pcsiFisher_inUnitInterval {ι : Type*} [Fintype ι] [Nonempty ι] {r : ι → ℝ}
    (hr : ∀ i, r i ∈ Set.Ioo (-1 : ℝ) 1) :
    inUnitInterval (pcsiFisher r) := by
  apply pcsi_inUnitInterval
  have h := fisherRBar_mem_Ioo hr
  exact ⟨le_of_lt h.1, le_of_lt h.2⟩

def cappedRatio (x y : ℝ) : ℝ := min 1 (x / y)

theorem cappedRatio_inUnitInterval {x y : ℝ}
    (hx : 0 ≤ x) (hy : 0 < y) :
    inUnitInterval (cappedRatio x y) := by
  exact ⟨by
      exact le_min zero_le_one (div_nonneg hx hy.le), by
      exact min_le_left _ _⟩

def weightedScore {ι : Type*} [Fintype ι] (w a : ι → ℝ) : ℝ :=
  ∑ i, w i * a i

def meanScore {ι : Type*} [Fintype ι] [Nonempty ι] (a : ι → ℝ) : ℝ :=
  avg a

def levelShift {ι P : Type*} [Fintype ι] [Nonempty ι] [Fintype P] [Nonempty P]
    (a0 : ι → ℝ) (ap : P → ι → ℝ) : ℝ :=
  avg (fun j => cappedRatio (meanScore (ap j)) (meanScore a0))

def weightedLevelShift {ι P : Type*} [Fintype ι] [Fintype P] [Nonempty P]
    (w : ι → ℝ) (a0 : ι → ℝ) (ap : P → ι → ℝ) : ℝ :=
  avg (fun j => cappedRatio (weightedScore w (ap j)) (weightedScore w a0))

theorem weightedScore_inUnitInterval {ι : Type*} [Fintype ι] {w a : ι → ℝ}
    (hw_nn : ∀ i, 0 ≤ w i) (hw_sum : ∑ i, w i = 1)
    (ha : ∀ i, inUnitInterval (a i)) : inUnitInterval (weightedScore w a) := by
  exact ⟨Finset.sum_nonneg fun i _ => mul_nonneg (hw_nn i) ((ha i).1),
    hw_sum ▸ Finset.sum_le_sum fun i _ => mul_le_of_le_one_right (hw_nn i) ((ha i).2)⟩

theorem levelShift_inUnitInterval {ι P : Type*} [Fintype ι] [Nonempty ι]
    [Fintype P] [Nonempty P]
    {a0 : ι → ℝ} {ap : P → ι → ℝ}
    (hap : ∀ j i, 0 ≤ ap j i)
    (h0 : 0 < meanScore a0) :
    inUnitInterval (levelShift a0 ap) := by
  refine avg_inUnitInterval ?_
  exact fun j => cappedRatio_inUnitInterval
    (by
      exact div_nonneg (Finset.sum_nonneg fun _ _ => hap _ _) (Nat.cast_nonneg _))
    h0

theorem weightedLevelShift_inUnitInterval {ι P : Type*} [Fintype ι]
    [Fintype P] [Nonempty P]
    {w : ι → ℝ} {a0 : ι → ℝ} {ap : P → ι → ℝ}
    (hw_nn : ∀ i, 0 ≤ w i) (_hw_sum : ∑ i, w i = 1)
    (ha : ∀ j i, inUnitInterval (ap j i))
    (h0 : 0 < weightedScore w a0) :
    inUnitInterval (weightedLevelShift w a0 ap) := by
  apply_rules [avg_inUnitInterval]
  exact fun i => by
    rw [inUnitInterval]
    exact ⟨by
        exact le_min zero_le_one
          (div_nonneg
            (by
              exact Finset.sum_nonneg fun _ _ => mul_nonneg (hw_nn _) ((ha i _).1))
            h0.le), by
        exact min_le_left _ _⟩

def dcsi {T D : Type*} [Fintype T] [Nonempty T] [Fintype D] [Nonempty D]
    (score0 : T → ℝ) (scoreDelay : T → D → ℝ) : ℝ :=
  avg (fun t => avg (fun d => cappedRatio (scoreDelay t d) (score0 t)))

theorem dcsi_inUnitInterval {T D : Type*} [Fintype T] [Nonempty T]
    [Fintype D] [Nonempty D]
    {score0 : T → ℝ} {scoreDelay : T → D → ℝ}
    (hd : ∀ t d, 0 ≤ scoreDelay t d)
    (h0 : ∀ t, 0 < score0 t) :
    inUnitInterval (dcsi score0 scoreDelay) := by
  exact avg_inUnitInterval fun t =>
    avg_inUnitInterval fun d => cappedRatio_inUnitInterval (hd t d) (h0 t)

def ecsi (improvement backsliding : ℝ) : ℝ :=
  improvement * (1 - min 1 backsliding)

theorem ecsi_inUnitInterval {improvement backsliding : ℝ}
    (hI : inUnitInterval improvement) (hB : 0 ≤ backsliding) :
    inUnitInterval (ecsi improvement backsliding) := by
  unfold inUnitInterval at *
  constructor <;> unfold ecsi <;> cases min_cases 1 backsliding <;> nlinarith

def csiCore (eps p d e : ℝ) : ℝ := max eps p * max eps d * max eps e

theorem csiCore_inUnitInterval {eps p d e : ℝ}
    (heps : inUnitInterval eps) (hp : inUnitInterval p)
    (hd : inUnitInterval d) (he : inUnitInterval e) :
    inUnitInterval (csiCore eps p d e) := by
  unfold inUnitInterval at *
  exact ⟨mul_nonneg
      (mul_nonneg (by cases max_cases eps p <;> linarith)
        (by cases max_cases eps d <;> linarith))
      (by cases max_cases eps e <;> linarith),
    mul_le_one₀
      (mul_le_one₀ (by cases max_cases eps p <;> linarith)
        (by cases max_cases eps d <;> linarith)
        (by cases max_cases eps d <;> linarith))
      (by cases max_cases eps e <;> linarith)
      (by cases max_cases eps e <;> linarith)⟩

def csi (eps p d e : ℝ) : ℝ := Real.rpow (csiCore eps p d e) ((1 : ℝ) / 3)

theorem csi_inUnitInterval {eps p d e : ℝ}
    (heps : inUnitInterval eps) (hp : inUnitInterval p)
    (hd : inUnitInterval d) (he : inUnitInterval e) :
    inUnitInterval (csi eps p d e) := by
  have h_csiCore : 0 ≤ csiCore eps p d e ∧ csiCore eps p d e ≤ 1 := by
    exact csiCore_inUnitInterval heps hp hd he
  exact ⟨Real.rpow_nonneg h_csiCore.1 _,
    Real.rpow_le_one h_csiCore.1 h_csiCore.2 (by norm_num)⟩

def positivePart (x : ℝ) : ℝ := max 0 x

def transitionDiff {n : ℕ} (e : Fin (n + 2) → ℝ) (k : Fin (n + 1)) : ℝ :=
  e k.succ - e k.castSucc

def totalVariation {n : ℕ} (e : Fin (n + 2) → ℝ) : ℝ :=
  ∑ k, |transitionDiff e k|

def backslidingNumerator {n : ℕ} (e : Fin (n + 2) → ℝ) : ℝ :=
  ∑ k, positivePart (transitionDiff e k)

def backslidingRatio {n : ℕ} (eps : ℝ) (e : Fin (n + 2) → ℝ) : ℝ :=
  backslidingNumerator e / (totalVariation e + eps)

def improvement {n : ℕ} (eps : ℝ) (e : Fin (n + 2) → ℝ) : ℝ :=
  max 0 ((e 0 - e (Fin.last (n + 1))) / max (e 0) eps)

def ecsiFromErrors {n : ℕ} (eps : ℝ) (e : Fin (n + 2) → ℝ) : ℝ :=
  improvement eps e * (1 - min 1 (backslidingRatio eps e))

theorem backslidingRatio_inUnitInterval {n : ℕ} {eps : ℝ} {e : Fin (n + 2) → ℝ}
    (heps : 0 < eps) :
    inUnitInterval (backslidingRatio eps e) := by
  constructor
  · exact div_nonneg
      (Finset.sum_nonneg fun _ _ => le_max_left _ _)
      (add_nonneg (Finset.sum_nonneg fun _ _ => abs_nonneg _) heps.le)
  · exact div_le_one_of_le₀
      (le_add_of_le_of_nonneg
        (Finset.sum_le_sum fun _ _ => by
          cases max_cases 0 (e (Fin.succ ‹_›) - e (Fin.castSucc ‹_›)) <;>
          cases abs_cases (e (Fin.succ ‹_›) - e (Fin.castSucc ‹_›)) <;>
          linarith!)
        heps.le)
      (add_nonneg (Finset.sum_nonneg fun _ _ => abs_nonneg _) heps.le)

theorem improvement_inUnitInterval {n : ℕ} {eps : ℝ} {e : Fin (n + 2) → ℝ}
    (he : ∀ i, inUnitInterval (e i)) (heps : 0 < eps) :
    inUnitInterval (improvement eps e) := by
  refine ⟨le_max_left _ _, ?_⟩
  refine max_le_iff.mpr ⟨by norm_num, ?_⟩
  rw [div_le_iff₀]
  · cases max_cases (e 0) eps <;>
      linarith [(he 0).1, (he 0).2, (he (Fin.last (n + 1))).1, (he (Fin.last (n + 1))).2]
  · cases max_cases (e 0) eps <;> linarith [(he 0).1, heps]

theorem ecsiFromErrors_inUnitInterval {n : ℕ} {eps : ℝ} {e : Fin (n + 2) → ℝ}
    (he : ∀ i, inUnitInterval (e i)) (heps : 0 < eps) :
    inUnitInterval (ecsiFromErrors eps e) := by
  constructor
  · exact mul_nonneg
      (improvement_inUnitInterval he heps).1
      (sub_nonneg.2 (min_le_left _ _))
  · exact mul_le_one₀
      (improvement_inUnitInterval he heps).2
      (sub_nonneg.2 (min_le_left _ _))
      (sub_le_self _ (le_min zero_le_one (backslidingRatio_inUnitInterval heps).1))

end Formalization
