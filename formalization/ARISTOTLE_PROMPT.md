This Lean package accompanies a projectibility-first paper on AGI evaluation.

Work only inside this package. The target file is
`Formalization/Metrics.lean`.

The module should retain compact definitions and range proofs for:

1. mapped profile-shape similarity from an admissible correlation;
2. mean signed item change;
3. mean absolute item change (INS);
4. signed change on an externally specified tail and its negation as WTD;
5. itemwise retained mass under a positive baseline total;
6. feedback endpoint gain; and
7. the exact backsliding share `U / V`, with value zero when `V = 0`.

Do not reintroduce the retired CSI geometric mean, dCSI/eCSI composites,
Fisher pooling across heterogeneous interventions, capped level ratios, or an
HPC-derived weighting formula.

Prefer short proofs from Mathlib. State every assumption needed for a range
claim. Do not describe algebraic range proofs as establishing reliability,
projectibility, construct validity, statistical validity, or mechanistic
interpretation.
