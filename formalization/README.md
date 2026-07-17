# Lean companion: algebraic estimands

This package formalizes the elementary scoring definitions retained by the
projectibility-first revision of the paper:

- profile-shape similarity (PSS) as the affine map of an admissible
  correlation from `[-1, 1]` to `[0, 1]`;
- mean signed score change;
- mean absolute score change (INS);
- mean signed change on an externally selected tail and its negation as
  worst-tail degradation (WTD);
- itemwise retained mass at a specified delay;
- feedback endpoint gain; and
- the share of path variation due to backsliding.

Run the checks from this directory with:

```sh
lake build
```

## Scope of the proofs

The theorems establish algebraic range properties under explicit assumptions,
such as item scores lying in `[0, 1]` or a positive retained-mass denominator.
The exact backsliding share is defined to be zero when total transition
variation is zero. These results do **not** prove that:

- a correlation estimate is statistically reliable;
- an intervention, item sample, or tail-selection procedure is appropriate;
- a measurement profile projects to a new population, task, or deployment;
- weights have predictive or construct validity; or
- behavioural stability identifies a controller, representation, or other
  mechanism.

Those are empirical and design questions. The formalization deliberately does
not restore the retired CSI composite, Fisher pooling across heterogeneous
interventions, or an HPC-derived weighting formula.
