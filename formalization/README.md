# Lean companion: v3 algebraic estimands

This package formalizes the elementary definitions and raw-estimand results
retained in `metrics_spec_v3.md`:

- signed level change $L$ and mean absolute paired change (INS);
- positive- and negative-change component decompositions;
- signed worst-tail degradation (WTD) on an externally supplied lower tail;
- target-specific worst-tail loss (WTL) on an externally supplied high-loss
  tail;
- retained above-pretest gain with a positive denominator or positive
  preregistered average-gain threshold; and
- cumulative error decrease $D$, cumulative error increase $U$, endpoint gain
  $G$, and total variation $V$ for feedback trajectories.

The central checked results include:

$$
|L|\le \mathrm{INS},\qquad
L=F^+-F^-,\qquad
\mathrm{INS}=F^++F^-,
$$

and

$$
G=D-U,\qquad V=D+U,\qquad |G|\le V.
$$

PSS and the discontinuous backsliding ratio $B$ are no longer defined.

Run the checks from this directory with:

```sh
lake build
```

## Deliberate boundary

Tail membership is an external selector. The Lean module proves WTD and WTL
bounds for the selected finite set, but does not formalize sorting, quantiles,
noisy tail recovery, pseudo-null correction, split-sample selection, or
cross-fitting. In particular, it does not prove the sorted-tail inequalities
from the empirical specification. Those require assumptions about the selector
that are clearer and more useful in the statistical implementation than in
this compact algebraic companion.

The proofs establish no claim about sampling adequacy, estimator reliability,
holdout validity, transport, calibration, construct validity, causal
attribution, decision value, or mechanism. Pseudo-null-adjusted estimates are
deliberately allowed to fall outside the raw-estimand ranges.
