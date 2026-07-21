# Revision plan: projectibility-first AGI evaluation

**Date:** 2026-07-17
**Working target:** *Minds and Machines*
**Scope:** Re-architect the paper around declared projection targets, then integrate Zhang, Koyejo, and Yang's item-level robustness findings. This supersedes the April plan to strengthen the HPC claim.

## Recommended direction

The paper should no longer argue that general intelligence is a homeostatic property cluster or that black-box stability scores reveal mechanisms that maintain such a cluster. Its stronger and more defensible contribution is methodological:

> An AGI evaluation earns its use only by improving specified out-of-sample predictions or decisions for a declared population, unit of analysis, and intervention range. Robustness must be reported at profile, level, item, and harmful-tail granularities because stability at one level does not entail stability at another.

Zhang et al. make the granularity point empirically decisive. Aggregate accuracy can remain nearly unchanged while large item-level improvements and degradations cancel. The current paper reproduces that vulnerability one level up: a stable domain profile and stable domain mean can conceal severe item-level churn and harmful-tail failures.

The recommended working title is **From Aggregate Scores to Projectible Profiles: Robustness in AGI Evaluation**. A plainer alternative is **What AGI Scores Should Predict**.

## What the reconnaissance found

Two live TODOs were added to `warranted-inference-in-agi-evaluation.tex` on 17 July:

1. a project-wide instruction to retire the HPC/homeostasis framing and rebuild around projectibility and predictive validation;
2. a Zhang-specific instruction to add item-transition distributions, two-sided instability, harmful-tail degradation, repeated sampling, noise correction, and split-sample tail estimation.

Other breadcrumbs left since the April manuscript session:

- **Reynolds (2026) and Weinberger (2026):** stability, network order, maintenance, and corrective control are separate achievements; only corrective control warrants strict `homeostatic` language.
- **von der Malsburg and Padó (2026) and Kuribayashi et al. (2026):** apparently coherent aggregate capability labels can hide construction- or subprocess-level divergence.
- **Yetman (forthcoming) and Arora et al. (2026):** behavioural performance underdetermines representation and mechanism; probing plus causal intervention would be needed for stronger competence claims.
- **Groeger, Wen, and Brbic (2026):** raw similarity or convergence needs a null calibrated to the statistic and selection procedure.
- **Simon et al., Nefdt and Ladyman, and the Many Minds note:** possible broader framing, but not necessary to the core revision.

The current `STATUS.md`, `DECISIONS.md`, and `CLAUDE.md` still describe the superseded HPC-strengthening strategy. The June Lean formalization also encodes the current capped level-shift and CSI formulas, so equation changes have downstream consequences.

A formula audit found two further problems worth fixing rather than carrying forward. The current eCSI prose calls (B) a fraction of transitions even though it is a share of total transition variation, and its worked example (I=0.8, B=0.6) can't arise from one trajectory: positive endpoint improvement entails more total decrease than increase, so (B<0.5). The current Lean Fisher result establishes the range of a totalized `tanh(artanh(...))` construction without validating that the inputs are admissible, non-degenerate correlations.

## Load-bearing assumptions and tests

| Assumption | What would make it false? | Revision response |
| --- | --- | --- |
| The July projectibility-first TODO supersedes the April HPC decision. | The TODO was meant as a question rather than a direction. | Brett's current instruction to update from the new findings confirms the supersession; record it explicitly in `DECISIONS.md`. |
| CHC domains remain a useful reporting vocabulary for AI systems. | They fail measurement invariance across model families or don't improve the target predictions. | Treat CHC as a defeasible battery organization, not an ontology of machine intelligence; require comparative validation against simpler and alternative decompositions. |
| Profile-level stability remains informative after Zhang. | It adds no held-out prediction once item-level and tail measures are included. | Retain it as a candidate descriptor, not a constitutive score; test incremental predictive validity. |
| Black-box behaviour can support evaluation without supporting mechanism claims. | The paper continues to infer representation, consolidation, control, or kind membership from behaviour alone. | Rename the measures behaviourally and state what mechanistic evidence would be additional rather than implied. |
| A combined score is useful. | Components lack a shared projection target, or aggregation loses predictive/calibration performance. | Default to a dashboard. Permit aggregation only when a declared decision target and held-out validation justify it. |
| Repeated per-item sampling is feasible enough to recommend. | Cost makes uniform high-repetition testing impractical. | Specify precision- or power-based allocation, report the compute budget, and allow adaptive sampling while preserving held-out estimation. |

The strongest pressure test is that the revised paper could collapse into the truism “disaggregate and validate.” To avoid that, its distinctive contribution must be the full design rule: **declare the projection first; keep granularities separate; compare against simple baselines; aggregate only when a shared target validates the aggregation; never infer a securing mechanism from behavioural stability alone.**

## Proposed architecture

### 1. What should an AGI evaluation let us infer?

Open with decisions and projection targets rather than with clusters or mechanisms. Give concrete examples: out-of-sample task success, calibration under deployment conditions, retention after clean-session delays, failure under task-irrelevant context, and graceful degradation when a declared component of the deployed system is changed.

Specify five parameters for every claim: target outcome, population/model family, unit of analysis, intervention or distribution range, and time horizon. Make clear that the field selects the question; evidence determines whether the projection succeeds.

### 2. Why aggregate scores are insufficient

Retain the best criticism of snapshot evaluation, but replace the “equal weights are intrinsically wrong” argument. Equal weighting becomes a transparent baseline. Any alternative weighting must demonstrate out-of-sample improvement for a declared target.

Use Zhang et al. as the central case: near-zero average change can coexist with large two-sided item shifts and severe worst-tail degradation. Add von der Malsburg and Padó plus Kuribayashi as convergent evidence that aggregation can hide construction- and subprocess-specific divergence.

### 3. A multi-granular robustness profile

Report, for every perturbation-by-domain cell:

1. **Profile shape similarity (PSS):** correlation or another preregistered similarity between baseline and perturbed domain profiles, with uncertainty. Report it by perturbation; don't Fisher-pool heterogeneous designed perturbations by default. Mark it undefined when either profile has zero variance, and do not treat high PSS as item-level robustness.
2. **Signed level change:** report (L_p = N^{-1}\sum_i \delta_{ip}), or the analogous mean-domain difference, on its natural ([-1,1]) scale. Positive and negative shifts remain visible; any ratio is secondary and explicitly labelled.
3. **Item-level instability:** for item (i) and perturbation (p), estimate \(\delta_{ip}=s_{ip}-s_{i0}\); report its distribution and \(\operatorname{INS}_p=N^{-1}\sum_i |\delta_{ip}|\).
4. **Harmful tail:** preregister (q) and report \(\operatorname{WTD}_{q,p}\), the negative mean of the bottom (q)-fraction of \(\delta_{ip}\), with selection and estimation performed on disjoint samples.
5. **Directional transitions:** report correct→incorrect and incorrect→correct movement, or their probabilistic analogues, so cancellation is inspectable rather than hidden.

Use repeated trials per item and condition. Estimate the positive null floor created by absolute values and tail selection through a baseline-only bootstrap; report raw estimates, the estimated floor, untruncated adjusted estimates, uncertainty, and the sampling budget. A negative adjusted estimate is diagnostic of correction noise and should not be clamped away. Split-sample WTD removes selection/measurement reuse but doesn't recover the oracle latent tail. Keep profile, signed change, instability, and tail risk separate unless held-out prediction supports an aggregation.

Predeclare when these quantities are not interpretable: non-paired item sets, perturbations that add task-relevant information, one-shot deterministic outputs, zero-variance domain profiles, severe floor/ceiling compression, too few items for the chosen tail, and pooling across heterogeneous perturbations or delays. Do not transfer a worst-tail item set from one model to another; Zhang et al. find that affected items are largely model-specific.

### 4. Retention, updating, and scaffold dependence as separate tests

Retain the durable-learning and error-update protocols, but remove `dCSI`, `eCSI`, and “stabilizing mechanism” language. At each delay, report signed change, INS, and WTD rather than averaging all delays into one score. If a one-sided retained-mass summary is useful, use

\[
\operatorname{DR}_d = \frac{\sum_t \min(s_{t0},s_{td})}{\sum_t s_{t0}},
\]

with a positive denominator, and keep gains visible in the signed statistics. Use independent screening and estimation samples to reduce regression-to-the-mean after excluding ceiling/floor items.

For feedback trials, report endpoint gain (G=e_1-e_K) and

\[
B=\frac{\sum_k(e_k-e_{k-1})_+}{\sum_k|e_k-e_{k-1}|+\varepsilon}
\]

as the share of transition variation due to error increases. Drop the unvalidated eCSI product. These are behavioural response measures, not evidence that a corrective controller exists.

Replace “contortion versus compensation” with **unit of evaluation and scaffold dependence**. A model-only score and a deployed-system score answer different questions. Test full, degraded, and minimal configurations, but do not call a scaffold fake merely because the model-only configuration performs poorly. State which composite is the bearer of the deployment prediction.

Use Yetman to mark the evidential boundary: robust behaviour does not by itself establish representation-based competence. If the paper discusses mechanism, present probing, activation intervention, or ablation as additional evidence required for that stronger claim.

### 5. Validation and weighting

Replace the fixed CHC centrality prior and its 14/13/12-percent table with a validation protocol:

- equal weights and unweighted component reports as baselines;
- candidate target-specific weights estimated or preregistered for a declared outcome;
- nested or external validation across model families, with calibration and uncertainty;
- incremental predictive performance over the equal-weight and snapshot baselines;
- explicit failure conditions and transport tests across populations and environments.

Human CHC loadings may remain as one hypothesis or shrinkage prior, but not as a defensible default for machine systems without evidence of transport.

### 6. Decision use, limitations, and conclusion

Heavily trim the governance section. Remove illustrative regulatory tiers and the capability–CSI figure. Replace them with a short account of decision-specific loss, uncertainty, tail constraints, and the need to calibrate thresholds against actual downstream outcomes.

End with the contribution the evidence supports: a projectibility-first, multi-granular evaluation design. Do not conclude that high scores show “genuine general intelligence,” cluster membership, internal consolidation, or homeostatic control.

## Metric and formalization decisions

Recommended default:

- retire the `CSI` family name and the geometric-mean combined CSI;
- remove the `min(1, x/y)` cap from general level-change reporting because it erases beneficial shifts that can cancel harmful ones;
- replace unstable per-item retention ratios with the retained-mass summary only if a one-sided retention estimand is useful, and pair it with signed change so gains are not silently discarded;
- retain backsliding (B) only as a separately reported diagnostic; remove the eCSI product and its impossible worked example;
- formalize the new bounded item-level quantities only after the estimands and terminology are settled.

The current Lean appendix should not continue to imply empirical adequacy. After the prose/equations stabilize, either:

1. update the canonical Lean file to prove range and aggregation properties for signed change, mean-absolute instability, PSS, retained mass, endpoint gain, and a fixed-cardinality selected tail, while labelling the old Aristotle-generated directories historical; or
2. remove the formalization appendix from this version and retain the code as an archived formal check of the superseded metric family.

Recommendation: choose option 1 only if it remains compact. Mathematical boundedness is useful, but it should not dominate a paper whose central problem is validity across targets and granularities.

Bootstrap confidence intervals, noise-floor subtraction, and split-sample unbiasedness should remain protocol claims unless the project undertakes a substantially larger probability formalization. Noise-adjusted metrics need signed bounds rather than false ([0,1]) guarantees.

## Literature triage

**Core citations:** Zhang et al.; Hendrycks et al.; Hernández-Orallo; Reynolds on stable clusters/homeostasis; Weinberger; von der Malsburg and Padó; Kuribayashi et al.; Yetman.

**Use if a specific sentence needs them:** Arora for causal intervention evidence; Groeger et al. for null calibration; Nefdt and Ladyman for projectible regularities.

**Probably omit:** Simon et al. and the Many Minds podcast. They are useful background but would broaden the paper without solving a live argumentative problem.

Add Zhang and any selected new sources to `references-local.bib`; do not push to the central bibliography until the revised citation set is stable.

## Execution sequence

1. Record the superseding decision and update `STATUS.md`/`CLAUDE.md` after the new architecture is accepted.
2. Rewrite title, abstract, introduction, and the current HPC section into the projection-target framework.
3. Rebuild the robustness section around the multi-granular dashboard and Zhang's estimators.
4. Recast retention, feedback, and scaffold protocols; settle the unit of analysis.
5. Replace centrality-default scoring with predictive validation; trim governance.
6. Rewrite predictions, limitations, and conclusion around incremental validity and explicit failure conditions.
7. Update bibliography, notation, figures, metric specs, and Lean appendix as warranted.
8. Build and run bibliography validation, house-style audit, proofreading, the HPC/projectibility audit, and a final source-grounding pass.

The first implementation checkpoint should come after steps 2–3. At that point, reassess whether the centrality material still earns a full section or should become a short validation subsection.

## Implementation note

The approved direction was implemented on 17 July 2026. One algebraic detail
was tightened during implementation: the backsliding diagnostic is defined as
$B=U/V$ when total variation $V>0$, and $B=0$ when $V=0$. This makes $B$ an
exact share of transition variation and removes the epsilon term in the
planning formula. The manuscript, Lean companion, project records, and
historical-specification banners now agree on that definition.
