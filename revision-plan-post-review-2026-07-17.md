# Major-revision plan after the rhetoric and GPT-Pro reviews

**Date:** 2026-07-17
**Status:** Proposed for Brett's review; no manuscript changes have been made from this plan
**Working venue:** *Minds and Machines*
**Relation to the earlier plan:** This plan preserves the projectibility-first turn but supersedes `revision-plan-projectibility-zhang.md` on estimands, empirical support, statistical design, and paper structure once approved.

## Bottom line

The two reviews converge on the paper's publishable core:

> A multidomain evaluation should preserve potentially relevant differences across granularities, but none of those descriptions warrants an inference beyond the observations used to construct it until the inference, target population, sampling range, and evidential test are declared.

The current manuscript already contains that argument, but it becomes fully legible only in the validation section. It also overstates several descriptive quantities: the current tail statistic measures change rather than absolute harmful failure; the feedback ratio is algebraically redundant and discontinuous at a flat trajectory; and the retention ratio does not isolate newly learned performance. These are not copyediting issues. The revision should repair the estimands, make the data-generating hierarchy explicit, add a bounded empirical demonstration, and then rebuild the rhetoric around the repaired framework.

The novelty claim should be modest and precise. The paper does not introduce fundamentally new mathematical operations. Its contribution is a **target-indexed measurement architecture** that:

1. separates descriptive granularity from inferential warrant;
2. matches every extrapolation to an appropriate sampling or holdout design;
3. prevents aggregation from erasing distinctions before their relevance to a target has been tested; and
4. distinguishes descriptive, predictive, decision, and explanatory claims rather than treating them as if they shared one validation procedure.

## Recommended decisions

These are the decisions I recommend approving before prose is rewritten.

### 1. Retain AGI as the motivating limiting case, not as the scope of the mathematics

Keep AGI in the framing because the intended inference range is exceptionally broad relative to any finite battery. Say explicitly that the framework applies to multidomain AI evaluation generally and that AGI claims make the projectibility problem unusually severe. Hendrycks et al. remain a motivating case, not the paper's addressee.

A title such as **From Aggregate Scores to Warranted Inference in AGI Evaluation** would avoid suggesting that a profile is intrinsically projectible. Final title selection should follow the rewrite.

### 2. Place projectibility inside validity rather than above it

Define projectibility as a common structural feature of interpretations or uses that travel beyond the observations used to construct a score. It is target-indexed and forms one part of a Messickian validity argument; it is not a new umbrella that replaces construct validity, generalizability, predictive validity, transportability, or decision analysis.

The paper should distinguish the relations because their warrants differ:

| Proposed projection | Evidence that could warrant it |
| --- | --- |
| Tested to untested items | Declared item/task universe, sampling frame, and item-level holdout |
| One context to another | Held-out perturbation realizations or, for a stronger claim, held-out perturbation families |
| One system population to another | Validation on held-out model families, deployment configurations, or lineages |
| Present to future behaviour | Temporal holdout on later sessions, releases, or deployment periods |
| Behaviour to a causal explanation | Mechanistic interventions and controls for rival routes; black-box prediction alone is insufficient |
| Score to a decision | Calibration plus a declared loss, utility, constraint, or action threshold |

Messick should therefore return in the validation section: first to establish that validity belongs to interpretations and uses, then to show that held-out performance is one strand of a larger validity argument. Goodman supplies the historical projectibility vocabulary. Boyd and Reynolds should remain only where their more specific philosophical work is doing real work.

### 3. Expand the projection declaration and separate it from the sampling audit

The opening declaration should contain:

- the claim type and target outcome or decision;
- the target system population;
- the target task/item population and sampling frame;
- the bearer and unit of analysis;
- the perturbation or intervention families over which the claim is meant to hold;
- the time horizon;
- the decision loss, utility, or constraint when the target is an action; and
- the holdout or evidence type that would test the claim.

A companion sampling audit should record perturbation family, realization, response replicate, scorer or grader, model version, deployment time, and all crossed or nested dependencies. This keeps the conceptual declaration readable while making the data-generating hierarchy statistically usable.

### 4. Repair the core dashboard

Use the following minimal descriptive set:

1. **Profile correlation, $r$:** report the correlation directly. Retire the affine PSS transform, which adds no information and invites the false reading that 0.5 means “half preserved.”
2. **Signed level change, $L$:** retain on its natural signed scale.
3. **Item instability, INS:** retain mean absolute paired change, together with directional changes.
4. **Worst-tail degradation, WTD:** retain the lower-tail change statistic as an empirical expected-shortfall analogue, but describe it as a signed change statistic rather than an absolute harm measure.
5. **Worst-tail loss, WTL:** add an absolute perturbed-condition tail measure defined over a declared target-specific loss. Report it for baseline and perturbed conditions so stable severe failures remain visible. If item consequences differ, the loss must encode severity rather than treating every incorrect response as equally harmful.

The paper should no longer use “harmful tail” for a correctness-change statistic. WTD answers *where did performance deteriorate most?* WTL answers *where is absolute loss worst?* Neither substitutes for the other.

The metric section should also distinguish three estimands:

- **fixed-set description:** exact values for a declared deterministic item set;
- **conditional response behaviour:** probabilities under a declared stochastic generation and scoring protocol; and
- **item- or context-population inference:** claims over a wider universe supported by a sampling or holdout design.

Repeated responses are needed for the second estimand, not for the first. Item resampling supports the third only when an admissible item universe and exchangeability or sampling assumption has been stated.

### 5. Replace the feedback ratio and refine retention

For feedback trajectories, define cumulative error decreases $D$, cumulative error increases $U$, endpoint gain $G=D-U$, and total variation $V=D+U$. Since

\[
B=\frac{U}{V}=\frac{V-G}{2V}\qquad(V>0),
\]

the current backsliding share adds no independent information and has no continuous extension at $V=0$. Retire $B$ as a primary output. Report $G$ and $U$, with $U/(K-1)$ available when trajectories have different numbers of attempts; $V$ may remain a secondary path-length diagnostic. Add a matched no-feedback condition with attempt count, token budget, tools, and sampling held constant.

For retention, measure pre-instruction, immediate post-instruction, and delayed performance. Keep the current ratio only if it is explicitly labelled retention of immediately demonstrated performance. If the claim concerns learning, use attributable immediate and delayed gains above the pre-instruction baseline, report the denominator, and impose a preregistered minimum immediate-gain mass before interpreting the ratio.

### 6. Make validation target-specific and statistically concrete

Replace the schematic flat regression with worked validation designs. For each target, specify:

- what one observational row represents;
- which units are independent and which share items, baselines, perturbations, or model lineage;
- how dashboard cells become predictors;
- what regularization, partial pooling, or dimension reduction is used;
- how uncertainty in estimated predictors is propagated; and
- which unit is held out.

The holdout must match the projection: held-out items test item generalization, held-out perturbation families test intervention transport, held-out model families test system-population transport, and later releases test temporal transport. A hierarchical or repeated-measures model is a natural default when the data actually support it; the manuscript should not prescribe one universal model.

Separate two products:

- an **interpretable score**, which may use a nonnegative convex weighting so component direction remains transparent; and
- a **predictive or decision model**, which may require negative coefficients, interactions, nonlinearities, or constraints derived from the declared loss.

Equal weighting remains a useful baseline but is not measurement-neutral merely because domains have been mapped to $[0,1]$.

### 7. Add a bounded empirical package using released Zhang artifacts

This is feasible without new model calls. The [official Zhang repository](https://github.com/SALT-NLP/illusion-of-robustness) contains implementations and tests for INS, WTD, noise correction, split-tail estimation, and bootstrap procedures. The [released dataset collection](https://huggingface.co/collections/SALT-NLP/context-induced-instability) retains item identifiers and repeated baseline/context trials for the main $4\times8$ benchmark-by-model design.

The empirical package should contain:

1. a synthetic cancellation example in which equal aggregate means conceal different item structures;
2. a known-truth simulation comparing raw, pseudo-null-adjusted, and split-sample estimators under a null, diffuse instability, symmetric churn, sparse collapse, and floor/ceiling conditions;
3. sensitivity analyses over trial count and tail fraction;
4. a reanalysis of the 32 released Zhang cells with raw and adjusted INS/WTD, clustered uncertainty, reliability, and split-tail estimates;
5. an absolute-tail example showing that WTD can be near zero while a system remains stably poor; and
6. a ten-domain simulation showing the sampling instability and degeneracies of profile correlation.

Pin the repository commit and dataset revisions. Use the authors' released outputs rather than attempting to regenerate proprietary-model responses.

This empirical section may establish that the proposed distinctions matter descriptively and that some estimators behave better under specified conditions. It cannot establish external predictive validity, deployment transport, CHC measurement invariance, retention, scaffold dependence, or the consequences of observed tails. The paper must state those limits rather than present the reanalysis as validation of projectibility itself.

### 8. Keep adjacent literatures in their proper roles

- **Raji et al.** should enter the opening as the closest antecedent for broad claims outrunning finite, contextual benchmarks.
- **Messick** supplies the encompassing validity framework.
- **Generalizability theory** supplies the vocabulary of admissible universes, facets, and decision designs. It is a complement, not a substitute for signed and tail-sensitive paired estimands; a full G-study is not required here.
- **Expected shortfall** supplies established terminology and properties for tail means. It does not make a correctness tail consequential without a target-specific loss.
- **Bowman and Dahl** support item quality, statistical power, and disciplined perturbation design in the workflow.
- **Pearl and Bareinboim** should appear only to delimit causal transport: ordinary held-out prediction does not license transfer of causal effects.
- **Yetman** continues to ground the behaviour–mechanism boundary, but that boundary should be stated once rather than recurring as a hidden second thesis.

Update the MIRAGE author from Kamyar Fardi to Kamyar Rajabalifardi. The Yetman DOI, `10.3998/ergo.10324`, is valid and is preassigned to an accepted article; retain “forthcoming” rather than importing placeholder issue metadata.

## Load-bearing assumptions and tests

| Assumption | Evidence now available | Revision consequence |
| --- | --- | --- |
| The paper is aimed at a conceptual or measurement-theoretic venue. | The working target is *Minds and Machines*, and the contribution is architectural rather than a new metric family. | A bounded empirical demonstration is sufficient; a technical ML submission would require materially stronger outcome validation. |
| AGI remains useful in the title. | The framework is general, but AGI claims have an unusually large gap between finite observations and intended inference. | Retain AGI only if the introduction makes this limiting-case rationale explicit. Otherwise broaden the title to multidomain AI evaluation. |
| Zhang's public artifacts can support the empirical section. | Trial-level outputs and analysis code are public; the relevant repository tests pass, and a smoke reanalysis produced sensible INS and tail estimates. | Proceed without API spend, but pin revisions and do not claim exact regeneration of proprietary model outputs. |
| The dashboard can be validated against an external outcome in this revision. | No suitable external deployment outcome is presently in the project or Zhang release. | Present external validation as the framework's requirement and a worked design, not as an accomplished result. |
| CHC domains are comparable across AI systems. | This has not been established. | Treat CHC as a defeasible reporting vocabulary and name invariance checks as future requirements; do not undertake a full IRT/DIF study unless suitable data appear. |
| Every added methodological tradition must be implemented in full. | The cited traditions solve different problems and require different data. | Use them to locate and delimit the framework; do not expand this revision into do-calculus, a full G-study, or a general measurement-invariance program. |

## Revised paper architecture

### 1. The inferential overreach of AGI scores

Open with Zhang's cancellation anomaly, then explain why it matters for broad AGI claims. Use Raji et al. to establish that the problem predates this particular battery. Introduce Hendrycks et al. as a current multidomain case, not as the paper's sustained opponent. State the two-stage thesis and the framework-level novelty claim before listing metrics.

### 2. From observations to declared projections

Place projectibility within Messickian validity, distinguish the six inferential relations, and introduce the expanded projection declaration plus the sampling audit. Explain why AGI is the limiting case. Use one running release or deployment decision to make target, unit, item universe, intervention range, horizon, and loss concrete.

### 3. What aggregate descriptions conceal

Present profile correlation, signed level change, INS, WTD, WTL, and directional flows as a minimal descriptive set. Explain each question before its formula. Distinguish fixed-set, stochastic-response, and superpopulation estimands; then introduce the crossed data hierarchy, noise correction, tail selection, multiplicity, and failure conditions.

Rename the section **Why Aggregate Stability Does Not Establish Robustness**.

### 4. From descriptions to warranted inferences

Move the current validation material here. Map each projection to its observational unit and holdout. Reintroduce Messick, compare simple and richer models, separate interpretable scores from predictive models, and discuss calibration, lineage dependence, measurement error, CHC, weighting, and aggregation in one sequence.

### 5. Worked demonstration

Present the synthetic example, known-truth simulations, and bounded Zhang reanalysis. The section's conclusion should be exact: the granular descriptions recover distinctions that aggregate accuracy loses, while external projectibility remains a further empirical question.

### 6. Applications of the projection declaration

Recast retention, feedback, and scaffold dependence as three applications that vary the time horizon, intervention, and bearer of evaluation. Add the pretest and no-feedback controls. Allow small factorial scaffold designs when component interactions matter. Keep the behaviour–mechanism boundary short and local.

### 7. Workflow, empirical claims, and failure conditions

Merge the current workflow, predictions, governance, and limitations inventories. End with a completed report for the running decision, including cellwise versus simultaneous uncertainty, decision loss, absolute tail constraints, and auditability.

Replace universal or asymmetrical predictions with bounded claims: define the population of targets and systems, the minimum useful predictive increment or decision value, and the conditions under which a dashboard component fails to earn its cost. Recast the current mechanistic prediction as empirical proxy sufficiency within a declared population; do not suggest that predictive success removes the logical underdetermination of mechanism by behaviour.

### 8. Conclusion

Return to the opening cancellation case. State what an evaluator may claim after disaggregation and matched validation, and what remains descriptive, population-bound, or mechanistically underdetermined.

## Formal companion

Move the Lean discussion to a supplement or repository unless it grows beyond elementary range checks. If retained, update it only after the estimands settle and prove relations that clarify the paper:

- absolute signed level change is no greater than INS;
- the relation between overall signed change and a genuinely selected lower-tail mean;
- the identities among $D,U,G,V$, showing why $B$ is redundant;
- boundedness and denominator conditions for retained demonstrated mass and retained gain; and
- separate bounds for raw estimands and deliberately untruncated noise-adjusted estimates.

Do not formalize pseudo-null correction, tail-selection consistency, or projectibility merely to preserve the appearance of a formal appendix.

## Execution sequence and checkpoints

1. **Approve this plan.** Resolve the four headline choices: AGI framing, WTD plus absolute WTL, retirement of PSS and $B$, and the bounded empirical package.
2. **Freeze the estimands.** Update the metric specification first, including data hierarchy, finite-set/stochastic/population distinctions, controls, and mathematical identities. Checkpoint before prose rewrite.
3. **Build the empirical package.** Vendor or pin only the required Zhang analysis inputs, add reproducible scripts and generated artifacts, and run the simulation and 32-cell reanalysis. Use an iteration checkpoint after inspecting the outputs; revise claims to fit the results.
4. **Rebuild the paper's opening and core sequence.** Rewrite title, abstract, introduction, projection section, metric section, and validation section around the running example and two-stage thesis.
5. **Integrate the empirical section and applications.** Rework retention, feedback, and scaffolds only after the core framework is stable.
6. **Update references and formalization.** Add the selected sources, correct MIRAGE metadata, preserve Yetman's forthcoming status, and either strengthen or demote the Lean companion.
7. **Verify the complete revision.** Build and visually inspect the PDF; validate citations; run statistical tests, house style, proofreading, HPC/projectibility, and unearned-inference audits; then use a review board for a cold submission reading.

## Deliberately out of scope unless separately approved

- new paid model or API experiments;
- a claim that the Zhang reanalysis demonstrates external validity;
- a full generalizability-theory variance decomposition;
- causal transport identification with do-calculus;
- a full multi-group IRT or differential-item-functioning study;
- venue formatting or repository publication before the substantive revision is accepted.

## Approval checkpoint

The recommended package is: **retain AGI as the hardest case; place projectibility within validity; add the item population and decision loss to the declaration; report $r,L,\mathrm{INS},\mathrm{WTD},\mathrm{WTL}$; retire PSS and $B$; add pre-instruction and no-feedback controls; run the bounded Zhang reanalysis and simulations; and keep external projectibility as an explicit unfulfilled validation requirement rather than claiming the reanalysis supplies it.**
