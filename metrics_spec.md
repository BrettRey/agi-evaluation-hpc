# AGI Evaluation Metrics: Formalization Target

> **Historical artifact (superseded 2026-07-17).** This specification records
> the retired CSI/centrality formalization. The canonical projectibility-first
> definitions are in formalization/Formalization/Metrics.lean.

Formalize the following real-valued scoring definitions in Lean 4 and prove the stated boundedness/normalization lemmas.

## 1. Unit interval predicate

Define `inUnitInterval (x : R)` to mean `0 <= x <= 1`.

## 2. Centrality-prior weight

Define

`priorWeight(lam, g, s) = lam * g + (1 - lam) * s`

Interpretation: a convex combination of two normalized weight sources.

Prove:

- If `lam`, `g`, and `s` are each in `[0,1]`, then `priorWeight(lam, g, s)` is in `[0,1]`.

Also formalize the finite-family version:

`priorWeights_i = lam * g_i + (1 - lam) * s_i`

Prove:

- If `sum_i g_i = 1` and `sum_i s_i = 1`, then `sum_i priorWeights_i = 1`.

## 3. Profile stability map

Define

`pcsi(rbar) = (1 + rbar) / 2`

Prove:

- If `rbar` is in `[-1,1]`, then `pcsi(rbar)` is in `[0,1]`.

## 4. Generic capped ratio

Define

`cappedRatio(x, y) = min(1, x / y)`

Prove:

- If `x >= 0` and `y > 0`, then `cappedRatio(x, y)` is in `[0,1]`.

## 5. Error-decay index

Define

`ecsi(I, B) = I * (1 - min(1, B))`

Prove:

- If `I` is in `[0,1]` and `B >= 0`, then `ecsi(I, B)` is in `[0,1]`.

## 6. Combined stability index

Define

`csiCore(eps, p, d, e) = max(eps, p) * max(eps, d) * max(eps, e)`

Prove:

- If `eps`, `p`, `d`, and `e` are each in `[0,1]`, then `csiCore(eps, p, d, e)` is in `[0,1]`.

Define

`csi(eps, p, d, e) = (csiCore(eps, p, d, e))^(1/3)`

using the real cube root / real power function.

Prove:

- If `eps`, `p`, `d`, and `e` are each in `[0,1]`, then `csi(eps, p, d, e)` is in `[0,1]`.

## Constraints

- Use Lean 4 with Mathlib.
- Keep the formalization compact and close to the math.
- Prefer robust lemmas over brittle tactic scripts.
