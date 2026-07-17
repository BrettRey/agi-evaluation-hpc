# STATUS.md -- AGI Evaluation

## Current State

**Phase:** Projectibility-first rearchitecture implemented and verified (*Minds and Machines* preparation)
**Last updated:** 2026-07-17
**Working title:** *From Aggregate Scores to Projectible Profiles: Robustness in AGI Evaluation*

The October 2025 preprint, arXiv:2510.15236, is the historical starting point. The live revision no longer argues that general intelligence is a homeostatic property cluster or that black-box stability scores reveal mechanisms that maintain one. The March–April HPC-strengthening plan is preserved in `DECISIONS.md` but superseded by the decision of 2026-07-17.

## Current Thesis

An AGI evaluation earns its use only by improving a specified out-of-sample prediction or decision for a declared target outcome, population or model family, unit of analysis, intervention or distribution range, and time horizon. Robustness must be reported at profile, level, item, and harmful-tail granularities because stability at one level doesn't entail stability at another.

Zhang, Koyejo, and Yang's arXiv:2607.12963v2 is the central empirical case: nearly unchanged aggregate accuracy can conceal substantial two-sided item-level prediction flips and severe harmful-tail degradation. Von der Malsburg and Padó, together with Kuribayashi et al., supply convergent construction- and subprocess-level cases. Yetman marks the evidential boundary between behavioural performance and representation- or mechanism-based competence claims.

## Approved Architecture

1. Open with projection targets and decision use, not clusters or securing mechanisms.
2. Diagnose why aggregate scores are insufficient, using Zhang et al. as the central case.
3. Replace combined CSI scoring with a multi-granular dashboard: profile-shape similarity, signed level change, item-level instability, harmful-tail degradation, and directional transitions.
4. Report retention, updating, and scaffold dependence as separate behavioural tests; don't infer consolidation, corrective control, representation, or homeostasis without additional mechanistic evidence.
5. Treat equal weights as a transparent baseline. Allow target-specific weights or aggregation only when held-out prediction or calibration validates them. CHC domains may organize reporting or supply a shrinkage hypothesis, but don't establish a machine ontology or default weighting.
6. Trim governance to decision-specific loss, uncertainty, and tail constraints, then conclude with the projectibility-first design rule.

## Measurement Decisions

- Use repeated trials per item and condition where feasible.
- Estimate the positive null floor induced by absolute values and tail selection with a baseline-only bootstrap; report raw, floor, untruncated adjusted estimate, uncertainty, and sampling budget.
- Select and estimate the harmful tail on disjoint samples. This avoids data reuse but doesn't identify an oracle latent tail.
- Keep profile shape, signed change, item instability, and tail harm separate unless a common projection target validates aggregation.
- Don't Fisher-pool heterogeneous designed perturbations by default; mark profile similarity undefined for zero-variance profiles.
- Don't presume that a worst-tail item set transfers across models without validation; Zhang et al. find the affected items are largely model-specific.
- Retire the CSI family name, geometric-mean CSI, fixed centrality table, and eCSI product. Keep endpoint gain and backsliding, if used, as separate behavioural diagnostics.
- Define backsliding exactly as $U/V$ for positive total variation and as $0$ for a constant trajectory; don't use an epsilon-distorted ratio.

## Completed for the July Revision

- Located and assessed the two live July TODO hooks in `main.tex`.
- Mapped later literature breadcrumbs: Reynolds and Weinberger on strict homeostasis, von der Malsburg and Padó, Kuribayashi et al., Yetman, Arora et al., Groeger et al., Simon et al., and the Many Minds note.
- Audited the inherited metrics. The eCSI worked example is trajectory-inconsistent, its backsliding description is inaccurate, and the current Lean Fisher result proves a totalized range rather than empirical admissibility.
- Drafted and approved `revision-plan-projectibility-zhang.md`.
- Updated project instructions, the decision log, and local bibliography for the new direction.
- Rewrote `main.tex` around declared projection targets, Zhang's cancellation result, and a multi-granular dashboard; recast retention, feedback, scaffold dependence, weighting, validation, governance, failure conditions, and conclusion.
- Added Zhang, Yetman, and the published ACL record for Kuribayashi et al. to `references-local.bib`; all 14 cited keys resolve and Biber datamodel validation passes.
- Replaced the canonical Lean metric module with compact definitions and range proofs for PSS, signed change, INS, WTD, retained mass, endpoint gain, and backsliding. `lake build` passes (8,028 jobs).
- Marked the superseded root and Aristotle-generated CSI specifications as historical artifacts.
- Built and visually checked the 13-page PDF. The final log has no undefined citations, undefined references, Biber warnings, or overfull boxes.
- Ran the house-style, terminology, proofreading, source-grounding, bibliography, HPC/projectibility, and unearned-inference audits. Projectibility is structural throughout; no securing-tier or mechanism overclaim remains.

## Next Steps

- Brett review of the completed rearchitecture and any desired expansion or compression before venue formatting.
- Apply *Minds and Machines* author guidelines and prepare the submission package.
- Decide whether to rename the GitHub repository, whose URL still contains the superseded `agi-evaluation-hpc` slug.
- Update the arXiv version and public status surfaces when the revision is ready to post.
