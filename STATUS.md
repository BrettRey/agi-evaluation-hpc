# STATUS.md -- AGI Evaluation

## Current State

**Phase:** Framework revision complete and shipped; venue preparation pending

**Last updated:** 2026-07-23

**Working title:** *From Aggregate Scores to Warranted Inference in AGI Evaluation*

The October 2025 preprint, arXiv:2510.15236, was **withdrawn on 2026-07-23** (`submit/7861781`; arXiv confirmed the withdrawal public 2026-07-23; its homeostatic-cluster thesis retracted) and is the historical starting point only. The live paper is a target-indexed measurement framework, not an HPC-kind argument or a proposal for a universal robustness score, and will be posted as a new arXiv submission rather than as a replacement of the withdrawn v1.

### 2026-07-23 Session Notes

- **Running example reshaped from noun-labels to observables** across §1--§3 and §5 (shipped, commit `31d72ca`). Brett judged an earlier "weave the firm through" grounding pass a cosmetic failure ("All you've done is throw 'the firm' in at various places"). Redone with observables, contrasts, procedures, and failure conditions: the §1 anchor now specifies a 94% legal-reasoning-section score vs. finding controlling authority for residential-tenancy matters at Ontario's Landlord and Tenant Board, the two named non-transfers (self-contained questions vs. retrieval; scored answers vs. the invented citation, Magesh 17--33%), the bridging tests, the supported/unsupported contrast, and the stop rule.
- **§2 definition now states the substantive point:** projectibility is assessed by describing two settings and investigating the sources of non-transfer between them, not "for a link" in the abstract.
- **§3 declared claim** states its estimand observably (worst tenth of matters at ≤ .20 expected loss under off-point padding, on a rubric turning on controlling authority and invented citations); §3's estimand math left technical; §5.1 predictive increment and §5.2 commensurability/compensability rewritten to observables.
- **Frame kept** (legal research, not clause extraction) to preserve the multidomain/aggregate framing and the Magesh hook; Brett confirmed.
- **Paper now 29 pp**, build clean, style at baseline. Two new memories written: `concreteness-is-observables-not-nouns`, `take-initiative-on-systemic-issues`.
- **Earlier in the session:** §2 machinery + §5 grounding pass (commit `4293778`, superseded in substance by the reshape); this is where the `/ship` skill fork made its own §2 facets edits and self-reverted a §5.3 overreach.

### 2026-07-23 Session Notes (evening -- concreteness redo)

- **The morning observable pass (commit `31d72ca`) was judged a total failure and replaced.** Diagnosis: it added *decoration* (a 94% score, "Ontario's Landlord and Tenant Board", "residential tenancy", a .20 threshold) that looks concrete but doesn't constrain the argument -- swap any of those specifics and the paragraph reads identically. That is the exact failure `concreteness-is-observables-not-nouns` warns against, committed by the fix that memory motivated.
- **Adopted a genuinely concretized rewrite as the new base** (from `Downloads/...-concretized.tex`), which replaces decoration with an operational study design: an eligible-request inclusion rule (Ontario wrongful-dismissal; termination-clause / reasonable-notice), a two-lawyer blind reference standard, client-file-clustered dev/confirmation splits, a three-type defect taxonomy (citation doesn't resolve / passage doesn't support / controlling authority omitted), registered answer-preserving alterations, a developer-vs-firm evidence division, and a firm-supplied tolerance τ. Running example moved from residential tenancy to employment law.
- **Terminology synced (paper wins):** "source--target link" → **projection**; "evidential standing" → **degree of warrant**. Paper is internally consistent; Current Thesis above updated to match. NOT propagated to the global `check-projectibility` skill or sibling projectibility papers, which use "link / edge-level" program-wide -- flag for a program-level decision if the rename should spread.
- **τ kept** (firm-supplied tolerance the paper deliberately doesn't fix) rather than the retired numeric .20.
- **One calibration trim pass** on the densest example paragraphs (§3 study protocol, §5.4 decision-use cluster): cut ~9 sentences of restated protocol and repeated policy/records enumerations, no abstraction reintroduced. 13751 → 13656 words.
- **`coady1992testimony` dropped by the concretized §1** (added this morning in `d0d35d6`); likely collateral, no build impact. Flagged, not restored (an add, outside the trim scope).
- **Paper now 30 pp, build clean**, no undefined refs/citations. Project file overwritten; not yet committed.

## Current Thesis

A finite evaluation first declares its projection target and scope, then preserves distinctions that aggregation compresses, and finally tests the intended inference against evidence matched to that scope. The projection declaration names the interpretation, system population, task and item population, bearer, intervention range, horizon, evidential test, and failure conditions. Decision use additionally declares loss, utility, alternatives, constraints, authority, and an action rule.

Projectibility is the degree of warrant for each specified projection within a broader Messickian and Kanean validity argument. Such a projection may extend a score interpretation, prediction, or explanation beyond observed responses. A decision is not itself an epistemic projection; it depends on projectible factual premises plus a defensible decision structure.

An aggregate can describe its construction sample without supporting a broader inference. Generalization from those observations to a declared evaluation universe and extrapolation from that universe to other tasks, contexts, systems, or times are distinct steps. The declared target identifies distinctions that may need preservation; matched evidence determines which support a target-specific report.

## Current Architecture

1. Introduce validity as warrant for a proposed interpretation and use, then use Goodman's grue case to explain the source--target problem for readers outside psychometrics.
2. Make the law-firm deployment a running example and distinguish construction sample, standardized evaluation universe, and broader target.
3. Separate item, task-domain, context, system, operator/site, temporal, causal, consequence, and decision relations rather than treating all as generic generalization.
4. Record crossed or nested sampling facets and distinguish fixed-set description, stochastic-response estimation, and population inference.
5. Preserve profile correlation, signed level, item instability, directional components, worst-tail degradation, case-risk tails, and realized-loss tails as non-substitutable outputs.
6. Demonstrate those distinctions through a locked reanalysis of all 32 released Zhang comparisons and known-truth simulations while explicitly withholding any external-projection claim.
7. Match the statistical row and outer holdout to the intended projection; distinguish descriptive aggregates, measurement interpretations, predictive models, value models, and decisions.
8. Treat CHC as an organizing content taxonomy unless factor structure, cross-system comparability, and AGI interpretation receive their own evidence.
9. Divide responsibility between developers' bounded source evidence and deployers' local completion and monitoring of warrants.
10. Close with an operational workflow, limits, and the rule that successful bounded links don't automatically compose into unrestricted AGI.

## Measurement Decisions

- Report Pearson \(r\) directly; the former unit-interval PSS transform is retired.
- WTD is signed worst-tail degradation, an expected-shortfall-like change statistic. It is not an absolute harm measure.
- WTL is a separate absolute, target-specific worst-tail loss. Report baseline and perturbed levels.
- If item inclusion probabilities differ, use design weights and define tail mass over the target population.
- Show raw, pseudo-null expectations, and untruncated adjusted estimates. Pseudo-null correction is not an unbiased-recovery guarantee.
- Cross-fit noisy tail selection and estimation, while naming the noisy-selected-set estimand separately from the oracle latent tail.
- Keep response-noise correction separate from projection across tasks, contexts, systems, lineages, operators, and time.
- Match uncertainty, resampling, and holdout units to the facet over which the claim is intended to generalize.

## Completed for the Current Revision

- Reframed projectibility within validity; added task/item populations, decision structure, facet-specific holdouts, generalizability theory, causal transport, measurement invariance, and expected-shortfall context.
- Added absolute WTL, renamed WTD, retired PSS and the backsliding share, and made descriptive-score, measurement, predictive-model, value-model, and decision distinctions explicit.
- Added a reproducible empirical package under `analysis/`: arXiv v2, the source commit, and 64 Parquet revisions/hashes are pinned; cached source data are excluded from version control.
- Reproduced all 32 released comparisons within rounding-level discrepancies and added null, sparse-collapse, stable-poor, and ten-domain profile-correlation simulations.
- Passed 14/14 empirical tests and verified 64/64 locked file hashes (294,033,162 bytes).
- Retained the Lean companion in the repository as an implementation check, but removed it from the paper's main intellectual case.
- Updated recent references and validated all cited keys. Biber datamodel validation passes.
- Acquired and audited the relevant primary literature locally, including Goodman, Messick, Kane, Brennan, Embretson, CHC sources, transportability, benchmark-validity work, expected shortfall, Zhang et al., and related current AI-evaluation papers. A library scan of *Validity* has been requested separately.
- Rebuilt the opening for a cross-field philosophy reader: validity theory receives an entry point, grue is explained before projectibility is borrowed, and the law-firm case arrives before the abstract declaration machinery.
- Reordered the paper so descriptions and their empirical checks precede target-matched validation. The demonstration is expressly descriptive and estimator-focused; it doesn't validate an external deployment target.
- Completed repeated rhetoric, structure, cohesion, editorial-scar-tissue, metaphor, projectibility, house-style, bibliography, and visual passes. The abstract, introduction, Section 2, and conclusion now use one link-level definition and discharge the same Goodman, CHC, empirical-scope, and developer--deployer promises.
- Renamed the canonical artifacts from `main.*` to `warranted-inference-in-agi-evaluation.*` and updated the build and companion references.
- Built and visually verified the final 21-page PDF. It has no undefined citations, undefined references, Biber warnings, or overfull boxes. The source and PDF were shipped to `master` at commit `fb90e72`.

## Next Steps

- Choose the submission venue. *Minds and Machines* remains a strong conceptual fit; a technical ML venue would likely require validation against an external projection target.
- Apply the selected venue's formatting and disclosure requirements, then run the submission gate.
- Review the requested library scan of *Validity* when it arrives and incorporate it only if it changes the argument or source support.
- Decide whether to rename the GitHub repository, whose URL still contains the historical agi-evaluation-hpc slug.
- Update the arXiv version and public status surfaces when the revision is ready to post.
