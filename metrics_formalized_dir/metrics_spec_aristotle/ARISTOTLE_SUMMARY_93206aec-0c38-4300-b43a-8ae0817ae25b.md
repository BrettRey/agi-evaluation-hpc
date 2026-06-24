# Summary of changes
Successfully formalized all definitions and proved all lemmas from `metrics_spec.md` in `RequestProject/Metrics.lean`. The file builds cleanly with no sorries, no warnings, and only standard axioms (`propext`, `Classical.choice`, `Quot.sound`).

**Definitions formalized:**
1. `inUnitInterval` — unit interval predicate `0 ≤ x ∧ x ≤ 1`
2. `priorWeight` — convex combination `λ·g + (1−λ)·s`
3. `priorWeights` — finite-family version indexed by `ι`
4. `pcsi` — profile stability map `(1 + r̄) / 2`
5. `cappedRatio` — generic capped ratio `min(1, x/y)`
6. `ecsi` — error-decay index `I · (1 − min(1, B))`
7. `csiCore` — combined stability core `max(ε,p) · max(ε,d) · max(ε,e)`
8. `csi` — combined stability index `csiCore^(1/3)`

**Theorems proved:**
1. `priorWeight_inUnitInterval` — priorWeight maps [0,1]³ → [0,1]
2. `priorWeights_sum` — family weights sum to 1 when components do
3. `pcsi_inUnitInterval` — pcsi maps [−1,1] → [0,1]
4. `cappedRatio_inUnitInterval` — cappedRatio ∈ [0,1] for x ≥ 0, y > 0
5. `ecsi_inUnitInterval` — ecsi maps [0,1] × [0,∞) → [0,1]
6. `csiCore_inUnitInterval` — csiCore maps [0,1]⁴ → [0,1]
7. `csi_inUnitInterval` — csi maps [0,1]⁴ → [0,1]