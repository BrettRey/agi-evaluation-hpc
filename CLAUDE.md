# CLAUDE.md -- AGI Evaluation

## Role: Editor/Researcher

Deep editorial, statistical, and research work is welcome here.

## Project Overview

This paper develops a target-indexed evaluation discipline for AGI and multidomain AI evaluation. A finite battery first declares the projection target and scope, then preserves distinctions that aggregation compresses, and finally tests the intended inference against evidence matched to the relevant item, context, system, or temporal facet.

Projectibility is one epistemic question within a broader Messickian validity argument. A decision isn't itself a projection; it depends on projectible estimates together with declared loss, utility, or constraints.

**Title:** *From Aggregate Scores to Warranted Inference in AGI Evaluation*

**Preprint:** [arXiv:2510.15236](https://doi.org/10.48550/arXiv.2510.15236) (historical October 2025 version)

**Target:** *Minds and Machines*

### Core Argument

1. **Declare the projection target and sampling universe.** Name the interpretation, system population, task/item population, bearer, intervention range, horizon, and matching test before choosing a score.
2. **Preserve distinct descriptions.** Report Pearson profile correlation, signed level, mean absolute item instability, directional components, signed worst-tail degradation, and absolute target-specific worst-tail loss.
3. **Keep estimand modes separate.** A deterministic fixed-set description, a stochastic-response estimand, and a superpopulation inference require different evidence.
4. **Demonstrate before extrapolating.** The Zhang reanalysis and known-truth simulations show what the quantities distinguish, but don't supply a deployment outcome.
5. **Match validation to projection.** An item split, held-out perturbation family, held-out lineage, and later release answer different questions.
6. **Separate scores from models.** Convex weights can define an interpretable score; an optimal predictive or decision model may use negative coefficients, interactions, nonlinearities, or constraints.
7. **Treat applications independently.** Retention uses above-pretest gain; feedback needs a no-feedback control; configuration-dependence claims name the model or deployed composite as bearer.
8. **Don't infer mechanism from behaviour.** Stable profiles, retention, or feedback response don't establish representation, consolidation, corrective control, homeostasis, or kind membership.

### Metric Conventions

- Report \(r\), not the retired PSS transform.
- WTD is signed worst-tail degradation and can be negative.
- WTL is an absolute, target-specific worst-tail loss; report condition levels.
- Report raw, pseudo-null expectations, and untruncated adjusted estimates.
- Cross-fitting targets the effect of a noisy-selected set, not automatically the oracle latent tail.
- The backsliding ratio \(B\) is retired because it is determined by \(G\) and \(V\).
- The canonical estimand specification is metrics_spec_v3.md.

### Key Sources

| Source | Role |
|---|---|
| Messick (1989, 1995) | Validity of interpretations and uses |
| Goodman (1955); Boyd (1991) | Warranted projection vocabulary |
| Hendrycks et al. (2025) | Motivating ten-domain AGI battery |
| Zhang, Koyejo, and Yang (2026), arXiv v2 | Aggregate cancellation and released trial data |
| Raji et al. (2021); Bowman and Dahl (2021) | Broad benchmark and construct-validity problems |
| Brennan (2001) | Multi-facet generalizability design |
| Pearl and Bareinboim (2014) | Causal transport is stronger than held-out prediction |
| Acerbi and Tasche (2002); Rockafellar and Uryasev (2002) | Expected-shortfall context for WTD |
| Meredith (1993) | Measurement invariance |
| Yetman (forthcoming) | Behaviour--representation evidential boundary |

## Build and Verification

- Full paper build: make
- Formalization: cd formalization, then lake build
- Empirical tests: python3 -m unittest discover -s analysis/tests -v

The LaTeX build requires XeLaTeX. The canonical Lean module is formalization/Formalization/Metrics.lean. The empirical package and reproduction instructions are in analysis/README.md; cached public trial files are checksum-verified and excluded from version control.

## House Style

See .house-style/style-rules.yaml. Key rules:

- Use semantic LaTeX macros for terms, mentions, and quotations.
- Use LaTeX en dashes where appropriate, never em dashes.
- Prefer contractions and paragraphs near 60 words.
- Use narrative citations for grammatical subjects and parenthetical citations otherwise.
