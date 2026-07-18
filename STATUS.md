# STATUS.md -- AGI Evaluation

## Current State

**Phase:** Post-review major revision implemented and verified (*Minds and Machines* preparation)

**Last updated:** 2026-07-17

**Working title:** *From Aggregate Scores to Warranted Inference in AGI Evaluation*

The October 2025 preprint, arXiv:2510.15236, is the historical starting point. The live revision is a target-indexed measurement framework, not an HPC-kind argument or a proposal for a universal robustness score.

## Current Thesis

A finite evaluation first declares its projection target and scope, then preserves distinctions that aggregation compresses, and finally tests the intended inference against evidence matched to that scope. The projection declaration names the interpretation, system population, task and item population, bearer, intervention range, horizon, and matching evidential test. Decision use additionally declares loss, utility, or constraints.

Projectibility is one epistemic question within a broader Messickian validity argument: whether evidence supports a specified inference beyond the observations used to construct the score. A decision is not itself an epistemic projection; it depends on projectible estimates plus a declared decision criterion.

## Current Architecture

1. Motivate the problem with Zhang, Koyejo, and Yang's item-level cancellation result and state the three-move thesis on page 1: declare, preserve resolution, and test.
2. Separate item, context, system, temporal, causal, and decision relations rather than treating all of them as generic generalization.
3. Record the crossed or nested data facets and distinguish fixed-set description, stochastic-response estimation, and population inference.
4. Preserve Pearson profile correlation, signed level, item instability, directional components, worst-tail degradation, and absolute target loss as separate outputs.
5. Demonstrate those distinctions through a locked reanalysis of all 32 released Zhang cells and known-truth simulations.
6. Match the validation row and outer holdout to the intended projection; distinguish interpretable scores from predictive or decision models.
7. Treat retention, feedback response, and component dependence as separate applications with pretests and matched controls.
8. Close with an operational workflow and explicit limits rather than generic capability tiers.

## Measurement Decisions

- Report Pearson \(r\) directly; the former unit-interval PSS transform is retired.
- WTD is signed worst-tail degradation, an expected-shortfall-like change statistic. It is not an absolute harm measure.
- WTL is a separate absolute, target-specific worst-tail loss. Report baseline and perturbed levels.
- If item inclusion probabilities differ, use design weights and define tail mass over the target population.
- Show raw, pseudo-null expectations, and untruncated adjusted estimates. Pseudo-null correction is not an unbiased-recovery guarantee.
- Cross-fit noisy tail selection and estimation, while naming the noisy-selected-set estimand separately from the oracle latent tail.
- Use a pre-instruction assessment and a visible minimum immediate-gain denominator for retention.
- Report feedback endpoint gain and cumulative increases/decreases. The backsliding share \(B\) is algebraically redundant and retired.
- Require a matched no-feedback control before attributing improvement to feedback.

## Completed for the Post-Review Revision

- Wrote and approved revision-plan-post-review-2026-07-17.md and the canonical metrics_spec_v3.md.
- Reframed projectibility within validity; added task/item population, decision loss, facet-specific holdouts, generalizability theory, causal transport, measurement invariance, and expected-shortfall context.
- Added absolute WTL, renamed WTD, retired PSS and \(B\), repaired retention and feedback protocols, and made score-versus-model constraints explicit.
- Added a reproducible empirical package under analysis/: arXiv v2, the source commit, and 64 Parquet revisions/hashes are pinned; cached source data are excluded from version control.
- Reproduced all 32 released cells within rounding-level discrepancies and added null, sparse-collapse, stable-poor, and ten-domain profile-correlation simulations.
- Passed 14/14 empirical tests and verified 64/64 locked file hashes (294,033,162 bytes).
- Updated the Lean companion with raw bounds, \(|L|\leq\mathrm{INS}\), directional-component identities, feedback identities, WTL, and retained above-pretest gain. lake build passes (8,028 jobs).
- Updated recent references and validated all cited keys. Biber datamodel validation passes.
- Reordered the paper so descriptions and their worked demonstration precede the validation stage. The final 16-page PDF has no undefined citations, undefined references, Biber warnings, or overfull boxes.
- Completed cold rhetoric, measurement, projectibility/HPC, proofread, house-style, bibliography, and visual audits. Remaining linter flags are verified math-subscript or spelling false positives; the terminology gloss is explicit in the abstract and Section 2.
- Completed a Lakoffian metaphor pass. The paper now consistently treats aggregation as compression, granular description as preserved resolution, inference as projection to a declared target and scope, evidence as warrant, and decisions as uses under declared loss. Misleading floor, scaffold, flow, and gain-mass language has been replaced.

## Next Steps

- Brett review of the completed revision and any desired compression before venue formatting.
- Apply *Minds and Machines* author guidelines and prepare the submission package.
- Decide whether to rename the GitHub repository, whose URL still contains the historical agi-evaluation-hpc slug.
- Update the arXiv version and public status surfaces when the revision is ready to post.
