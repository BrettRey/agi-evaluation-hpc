import Mathlib

noncomputable section

open Finset BigOperators

/-! # AGI Evaluation Metrics

Formalization of scoring definitions and boundedness/normalization lemmas
from `metrics_spec.md`.
-/

-- §1. Unit interval predicate
def inUnitInterval (x : ℝ) : Prop := 0 ≤ x ∧ x ≤ 1

-- §2. Centrality-prior weight
def priorWeight (lam g s : ℝ) : ℝ := lam * g + (1 - lam) * s

theorem priorWeight_inUnitInterval
    (hlam : inUnitInterval lam) (hg : inUnitInterval g) (hs : inUnitInterval s) :
    inUnitInterval (priorWeight lam g s) := by
  exact ⟨ by unfold priorWeight; nlinarith [ hlam.1, hlam.2, hg.1, hg.2, hs.1, hs.2 ], by unfold priorWeight; nlinarith [ hlam.1, hlam.2, hg.1, hg.2, hs.1, hs.2 ] ⟩

/-- Finite-family version of `priorWeight`. -/
def priorWeights {ι : Type*} (lam : ℝ) (g s : ι → ℝ) (i : ι) : ℝ :=
  lam * g i + (1 - lam) * s i

theorem priorWeights_sum {ι : Type*} [Fintype ι]
    (lam : ℝ) (g s : ι → ℝ)
    (hg : ∑ i, g i = 1) (hs : ∑ i, s i = 1) :
    ∑ i, priorWeights lam g s i = 1 := by
  unfold priorWeights;
  simp +decide [ *, mul_comm, Finset.sum_add_distrib ];
  rw [ ← Finset.mul_sum _ _ _, ← Finset.sum_mul, hg, hs ] ; ring

-- §3. Profile stability map
def pcsi (rbar : ℝ) : ℝ := (1 + rbar) / 2

theorem pcsi_inUnitInterval (h : -1 ≤ rbar ∧ rbar ≤ 1) :
    inUnitInterval (pcsi rbar) := by
  exact ⟨ by unfold pcsi; linarith, by unfold pcsi; linarith ⟩

-- §4. Generic capped ratio
def cappedRatio (x y : ℝ) : ℝ := min 1 (x / y)

theorem cappedRatio_inUnitInterval (hx : 0 ≤ x) (hy : 0 < y) :
    inUnitInterval (cappedRatio x y) := by
  exact ⟨ by exact le_min zero_le_one ( div_nonneg hx hy.le ), by exact min_le_left _ _ ⟩

-- §5. Error-decay index
def ecsi (I B : ℝ) : ℝ := I * (1 - min 1 B)

theorem ecsi_inUnitInterval (hI : inUnitInterval I) (hB : 0 ≤ B) :
    inUnitInterval (ecsi I B) := by
  unfold inUnitInterval at *;
  constructor <;> unfold ecsi <;> cases min_cases 1 B <;> nlinarith

-- §6. Combined stability index
def csiCore (eps p d e : ℝ) : ℝ := max eps p * max eps d * max eps e

theorem csiCore_inUnitInterval
    (heps : inUnitInterval eps) (hp : inUnitInterval p)
    (hd : inUnitInterval d) (he : inUnitInterval e) :
    inUnitInterval (csiCore eps p d e) := by
  unfold inUnitInterval at *;
  exact ⟨ mul_nonneg ( mul_nonneg ( by cases max_cases eps p <;> linarith ) ( by cases max_cases eps d <;> linarith ) ) ( by cases max_cases eps e <;> linarith ), mul_le_one₀ ( mul_le_one₀ ( by cases max_cases eps p <;> linarith ) ( by cases max_cases eps d <;> linarith ) ( by cases max_cases eps d <;> linarith ) ) ( by cases max_cases eps e <;> linarith ) ( by cases max_cases eps e <;> linarith ) ⟩

def csi (eps p d e : ℝ) : ℝ := (csiCore eps p d e) ^ ((1 : ℝ) / 3)

theorem csi_inUnitInterval
    (heps : inUnitInterval eps) (hp : inUnitInterval p)
    (hd : inUnitInterval d) (he : inUnitInterval e) :
    inUnitInterval (csi eps p d e) := by
  have h_csiCore : 0 ≤ csiCore eps p d e ∧ csiCore eps p d e ≤ 1 := by
    exact csiCore_inUnitInterval heps hp hd he;
  exact ⟨ Real.rpow_nonneg h_csiCore.1 _, Real.rpow_le_one h_csiCore.1 h_csiCore.2 ( by norm_num ) ⟩