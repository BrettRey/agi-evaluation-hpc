# Empirical companion

This directory tests the paper's proposed reporting discipline without adding
new model generations or treating the released benchmarks as external-validity
evidence. It does four bounded things:

1. reanalyses all 32 model-by-benchmark cells released by Zhang, Koyejo, and
   Yang;
2. compares raw, null-referenced, and held-out split-tail estimators;
3. simulates cancellation, known latent effects, trial/tail sensitivity, and
   stable absolute failure; and
4. tests how Pearson profile correlation behaves with only ten domain means.

The package does **not** validate projectibility to deployment outcomes, CHC
structure for machines, target-specific weights, construct validity, or any
mechanistic interpretation.

## Provenance and source locking

[`source_manifest.json`](source_manifest.json) declares the primary sources.
[`source_manifest.lock.json`](source_manifest.lock.json) resolves them to:

- Zhang et al., arXiv:2607.12963v2;
- `SALT-NLP/illusion-of-robustness` commit
  `411ceecd714068d161ab5ff307015a7e0eba8fd6`; and
- 64 public Hugging Face dataset commits covering the 32 baseline/context
  pairs, with the LFS SHA-256 and byte count of every Parquet file.

The full locked download is about 280 MiB. Downloads are placed in
`analysis/cache/`, verified before use, and excluded from version control. At
pinning time neither the GitHub repository nor the Hugging Face dataset
metadata exposed a license. The lock establishes provenance and integrity; it
isn't a grant of redistribution rights.

`pin_sources.py` uses the Hugging Face metadata API only to *refresh* the lock.
An exact reproduction should use the committed lock and should not refresh it.
The reanalysis downloads locked data files but never calls a model, grader, or
generation API.

## Environment and checks

From the project root:

```bash
python3 -m venv .venv-analysis
.venv-analysis/bin/pip install -r analysis/requirements.txt
.venv-analysis/bin/python -m unittest discover -s analysis/tests -v
```

The tests cover metric signs and tail cardinality, exact cancellation,
untruncated negative corrections, deterministic split-tail and absolute-tail
cases, constant-profile guards, source-lock completeness, pairing, and the
known-truth scenario definitions.

## Reproduce the artifacts

A fast smoke run uses one released cell and reduced Monte Carlo counts:

```bash
.venv-analysis/bin/python -m analysis.simulate_instability --profile smoke
.venv-analysis/bin/python -m analysis.simulate_pss --profile smoke
.venv-analysis/bin/python -m analysis.reanalyse_zhang --profile smoke
```

The publication-oriented settings are:

```bash
.venv-analysis/bin/python -m analysis.simulate_instability --profile standard
.venv-analysis/bin/python -m analysis.simulate_pss --profile standard
.venv-analysis/bin/python -m analysis.reanalyse_zhang --profile standard
.venv-analysis/bin/python -m analysis.summarize_evidence
```

The equivalent shortcuts are `make -C analysis PYTHON=.venv-analysis/bin/python
smoke` and `make -C analysis PYTHON=.venv-analysis/bin/python standard`.

After one online run, add `--offline` to `reanalyse_zhang` to require that every
locked file already be present and checksum-valid. To run a single cell, add,
for example, `--cell mmlu_pro.gpt54`. `--skip-sensitivity` retains the main
32-cell analysis while omitting the more expensive trial-subsampling grid.

Refresh the source lock only as a deliberate provenance update:

```bash
.venv-analysis/bin/python -m analysis.pin_sources
```

## Estimands kept separate

For item (i), let \(\delta_i\) be perturbed minus baseline success
probability. The scripts report:

- signed change: \(N^{-1}\sum_i\delta_i\);
- INS: \(N^{-1}\sum_i|\delta_i|\);
- WTD at tail fraction \(q\): the negative mean of the smallest \(q\)-fraction
  of \(\delta_i\); and
- case-risk tail: the largest \(q\)-fraction of latent itemwise expected loss
  \(1-s_{i1}\). This is not the tail of realized binary errors.

The baseline-only pseudo-null expectation follows the authors' released procedure: two
pseudo-conditions are resampled from each item's baseline trials, and the mean
null INS/WTD is subtracted from the raw estimate. Subtraction is untruncated;
a negative null-referenced value is retained. This is a diagnostic relative to a null
centred on the baseline response distribution, not a general bias correction under
nonnull alternatives. Internal output columns retain the authors' ``adjusted`` label
for source compatibility.

The split-tail procedure selects items on one random half of both conditions
and measures them on the disjoint halves, then swaps the halves and averages.
It removes reuse of the same noise for selection and measurement. It is
unbiased for the latent effect of the *noisy-selected set*, which can differ
from the oracle tail selected using latent effects. The simulations report both
targets rather than describing split-tail WTD as a universal correction.

The case-risk tail is separate because a system can be stably poor:
condition-to-condition WTD can be zero while perturbed-condition loss remains
high. Both raw and cross-fitted versions are reported.

## Outputs

`outputs/zhang_reanalysis/` contains:

- `main_reanalysis.csv` and `.tex`: the 32 released cells, raw/pseudo-null/null-referenced
  INS and WTD, split-tail WTD, split-half reliability, and case-risk tail;
- `download_audit.csv`: the dataset commit and verified file hash used;
- `published_comparison.pdf`: recomputed values against the rounded main table;
- `wtd_estimators.pdf`: raw, null-referenced, and held-out estimates kept
  visually distinct; and
- `trial_tail_sensitivity.csv` / `.pdf` when sensitivity isn't skipped.

At the top of `outputs/`, `evidence_summary.json` collects exact values suitable
for prose claims, while `section5_evidence_table.csv` / `.tex` and
`section5_evidence.pdf` provide a compact five-row table and four-panel figure.

`outputs/instability/` contains the known-truth summaries, the explicit
cancellation construction, the stable-failure comparison, trial-count/tail-q
sensitivity, run metadata, and four vector PDF figures.

`outputs/profile_correlation/` contains replicate- and summary-level ten-domain
results, a compact LaTeX table, sensitivity results, run metadata, and three
vector PDF figures. The conventional Fisher interval is included only as a comparator.
The paired nested bootstrap resamples items within domains and trials within
items. Neither procedure turns the synthetic domains into evidence for CHC
transport or machine capability structure.

## Limits on manuscript claims

The released-output analysis can establish that the reported aggregate
cancellation and estimator differences are recoverable from the public trials.
The simulations can establish finite-sample behavior under their declared data
generating processes. They cannot establish that any metric predicts a new
deployment outcome, that the ten-domain profile is measurement-invariant, that
the affected items transfer across model families, or that behavioural
stability identifies a representation or control mechanism.
