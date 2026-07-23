# CLAUDE.md -- AGI Evaluation

## Role: Editor/Researcher

Deep editorial, statistical, and research work is welcome here.

## Project Overview

This paper develops a target-indexed evaluation discipline for AGI and multidomain AI evaluation. Projectibility is an edge-level notation and audit discipline for empirical or explanatory source--target claims within a unified interpretation-and-use argument. It is not a new validity aspect and does not by itself warrant a decision.

The framework distinguishes the projective claim, its evidence-relative warrant, the worldly dependence that makes it reliable, and any causal explanation. A decision combines projectible factual premises with values, constraints, institutional authority, feasible alternatives, and an action rule.

**Title:** *From Aggregate Scores to Warranted Inference in AGI Evaluation*

**Preprint:** arXiv:2510.15236 (the October 2025 v1, *From Checklists to Clusters: A Homeostatic Account of AGI Evaluation*) was **withdrawn 2026-07-23** with a retraction reason; its homeostatic-cluster thesis and two proposed measures are disavowed. It is the historical starting point only. The current paper will be posted as a new arXiv submission (see `submission/arxiv-posting-plan.md`).

**Target:** *Minds and Machines*

### Core Argument

1. **Declare each source--target claim.** Name the interpretation, system and task populations, operators and affected populations, bearer, intervention range, horizon, target distribution, tolerance, failure conditions, and evidential responsibilities before choosing a score.
2. **Preserve distinct descriptions.** Report Pearson profile correlation, signed level, mean absolute item instability, directional components, and signed worst-tail degradation. Distinguish the absolute tail of conditional case risk from the tail of realized deployment loss.
3. **Keep estimand modes separate.** A deterministic fixed-set description, a stochastic-response estimand, and a superpopulation inference require different evidence.
4. **Demonstrate before extrapolating.** The Zhang reanalysis and known-truth simulations show what the quantities distinguish, but don't supply a deployment outcome.
5. **Match evidence to the inferential relation.** Content, process, structural, external-sample, predictive, causal, and decision evidence answer different premises; an item split, unseen context family, independent lineage, and later release answer different questions.
6. **Separate scores from models.** Convex weights can define an interpretable score; an optimal predictive or decision model may use negative coefficients, interactions, nonlinearities, or constraints.
7. **Changing the facet changes the warrant.** Temporal retention, response to feedback, and projection from a base model to a deployed composite require different observations and controls; no universal auxiliary metric is assumed.
8. **Don't infer mechanism from behaviour.** Stable profiles, retention, or feedback response don't establish representation, consolidation, corrective control, homeostasis, or kind membership.

### Metric Conventions

- Report \(r\), not the retired PSS transform.
- WTD is signed worst-tail degradation and can be negative.
- Case-risk WTL is the tail of conditional expected losses across cases; realized-loss WTL is the tail after response, scorer, and outcome randomness. Name the constrained estimand and report condition levels.
- Report raw values and untruncated null-referenced diagnostics; the latter are not general bias corrections.
- Cross-fitting targets the effect of a noisy-selected set, not automatically the oracle latent tail.
- The backsliding ratio \(B\) is retired because it is determined by \(G\) and \(V\).
- The canonical estimand specification is metrics_spec_v3.md.

### Key Sources

| Source | Role |
|---|---|
| Messick (1995) | Unified validity of interpretations and uses |
| Embretson (1983) | Construct representation versus nomothetic span |
| Goodman (1955); Boyd (1991) | Warranted projection vocabulary |
| Hendrycks et al. (2025) | Motivating ten-domain AGI battery |
| Zhang, Koyejo, and Yang (2026), arXiv v2 | Aggregate cancellation and released trial data |
| Raji et al. (2021); Bowman and Dahl (2021) | Broad benchmark and construct-validity problems |
| Brennan (2001) | Multi-facet generalizability design |
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
