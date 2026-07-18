# Metrics specification v3: target-indexed multidomain evaluation

**Status:** Canonical for the next manuscript revision and empirical implementation
**Frozen:** 2026-07-17
**Scope:** Descriptive estimands, protocol controls, sampling, uncertainty, and validation design

This specification supersedes the earlier metric specifications for forward work. The older files remain historical records. The core rule is that disaggregation preserves potentially relevant information; it does not by itself warrant inference beyond the observations used to construct the report. Every implementation must therefore declare both an estimand and the evidence design meant to support its intended projection.

## 1. Required declaration

Before calculation, register:

1. the claim type and target outcome, explanation, decision, or constraint;
2. the target system population, including model families, versions, configurations, and users;
3. the target task or item population and its sampling frame;
4. the bearer and unit of analysis: base model, stateful agent, or deployed composite;
5. the perturbation or intervention families and realizations over which the claim is meant to hold;
6. the time horizon;
7. the target-specific loss, utility, or constraint when the claim supports a decision; and
8. the holdout unit or other evidence that would test the claim.

No metric below is intrinsically projectible. No universal scalar is part of this specification.

## 2. Data model and estimand mode

### 2.1 Sampling facets

The sampling audit must identify every facet present in the design:

| Facet | Index | Typical relation |
| --- | --- | --- |
| System or model | $m$ | Crossed with items; versions may be nested in lineage and time |
| Domain | $g$ | Item $i$ is normally nested in domain $g$ |
| Item or task | $i$ | Paired across baseline and perturbation when change is estimated |
| Perturbation family | $f$ | A declared family such as irrelevant-context type |
| Perturbation realization | $p$ | Usually nested in $f$ and crossed with items |
| Condition | $c$ | Baseline $0$ or a declared perturbed condition $p$ |
| Response replicate | $h$ | Nested in system-by-item-by-condition-by-realization cells |
| Scorer or grader | $j$ | Crossed with outputs when scorer variation is in scope |
| Version or time | $\tau$ | Ordered; often nested in lineage or deployment period |

An implementation must state which facets are fixed, sampled, crossed, nested, or reused. The number of output rows is not the number of independent units.

### 2.2 Three estimand modes

Every reported cell must name one of these modes.

1. **Fixed-set description.** For deterministic scores $x_{igc}\in[0,1]$ on a declared finite set, metrics are exact descriptions of that set. They do not by themselves generalize to new responses, items, contexts, or systems.
2. **Conditional response behaviour.** For a declared stochastic generation and scoring protocol,
   $$
   s_{igc}=\operatorname{E}[X_{igchj}\mid m,i,g,c]
   $$
   is the conditional expected score. Repeated responses and, when relevant, repeated or crossed scorers estimate $s_{igc}$.
3. **Superpopulation inference.** Items, contexts, systems, or times are sampled from a declared admissible universe. Generalization requires a probability sample, defensible exchangeability assumption, or holdout at the corresponding facet. Repeated responses alone do not support this mode.

The definitions below use $s_{igc}$; in fixed-set mode, set $s_{igc}=x_{igc}$.

## 3. Core paired estimands

Suppress the system index and consider a domain $g$ with $N_g$ items observed under baseline $0$ and perturbation $p$. Define

$$
\delta_{igp}=s_{igp}-s_{ig0}\in[-1,1],
\qquad
a_{gc}=\frac{1}{N_g}\sum_{i=1}^{N_g}s_{igc}.
$$

Items must be paired. If baseline and perturbed item sets differ, these change estimands are undefined unless an explicit linking model replaces pairing.

### 3.1 Profile correlation

For $G\ge 2$ nonconstant domain profiles, report Pearson correlation directly:

$$
r_p=\operatorname{corr}_g(\mathbf a_0,\mathbf a_p)\in[-1,1].
$$

Do not transform $r_p$ to PSS. Correlation describes standardized linear association between profiles only; it is invariant to positive affine transformation and says nothing by itself about level, item stability, or loss. It is undefined if either profile has zero variance and degenerate at $G=2$, where any two nonconstant profiles have $r_p\in\{-1,1\}$. Any alternative such as Spearman correlation or cosine similarity must be preregistered and interpreted separately.

### 3.2 Signed level change

Report domain-level signed change

$$
L_{gp}=a_{gp}-a_{g0}
=\frac{1}{N_g}\sum_i\delta_{igp}\in[-1,1].
$$

If an overall level is useful, the default transparent summary is the equal-domain mean

$$
L_p=\frac{1}{G}\sum_g L_{gp}.
$$

An item-pooled mean, unequal domain weighting, or deployment-mixture weighting must be labelled and justified by the declared target. Positive and negative changes remain visible; no capped ratio is permitted.

### 3.3 Item instability and directional components

Define mean absolute paired change

$$
\operatorname{INS}_{gp}=\frac{1}{N_g}\sum_i|\delta_{igp}|\in[0,1].
$$

Report its two directional components:

$$
F^+_{gp}=\frac{1}{N_g}\sum_i(\delta_{igp})_+,
\qquad
F^-_{gp}=\frac{1}{N_g}\sum_i(-\delta_{igp})_+.
$$

$F^+$ is mean positive change and $F^-$ is mean negative change. For binary deterministic scores, they are respectively the incorrect-to-correct and correct-to-incorrect transition proportions.

### 3.4 Signed worst-tail degradation

Choose $q\in(0,1]$ and a minimum acceptable tail count before inspecting results. Let $m_g=\lceil qN_g\rceil$ and order paired changes as

$$
\delta_{(1)gp}\le\cdots\le\delta_{(N_g)gp}.
$$

Define

$$
\operatorname{WTD}_{q,gp}
=-\frac{1}{m_g}\sum_{\ell=1}^{m_g}\delta_{(\ell)gp}
\in[-1,1].
$$

WTD is a finite-sample expected-shortfall analogue for the loss $-\delta$. It is a **signed change statistic**, not an absolute harm measure. Positive values indicate mean deterioration in the selected lower tail; negative values mean that even the selected lower tail improved on average. Report $q$, $m_g$, and the full change distribution. Do not clamp negative raw or adjusted values.

### 3.5 Target-specific worst-tail loss

WTD cannot reveal a severe failure that is equally bad at baseline and under perturbation. Declare a target-specific item loss $\ell_T\in[0,1]$ whose inputs include the response, reference outcome, and any consequence severity relevant to target $T$. Define item expected loss under each condition:

$$
\lambda^{(T)}_{igc}
=\operatorname{E}[\ell_T(O_{igc},Y_i)\mid m,i,g,c].
$$

In fixed-set mode, use the observed loss. Order condition-specific item losses from largest to smallest,

$$
\lambda^{(T)}_{[1]gc}\ge\cdots\ge\lambda^{(T)}_{[N_g]gc},
$$

and define

$$
\operatorname{WTL}^{(T)}_{q,gc}
=\frac{1}{m_g}\sum_{\ell=1}^{m_g}\lambda^{(T)}_{[\ell]gc}
\in[0,1].
$$

Report $\operatorname{WTL}^{(T)}_{q,g0}$ and $\operatorname{WTL}^{(T)}_{q,gp}$ separately. Their difference may be secondary, but must not replace their absolute condition-specific levels. Here *absolute* means level of target-specific loss, not absolute value of score change. If the loss is not normalized, report it in its natural units and do not claim the unit-interval bound. Unequal inclusion probabilities require a declared design-weighted tail estimator.

## 4. Protocol-specific estimands and controls

### 4.1 Retention of above-pretest gain

For taught items $t=1,\ldots,N$, estimate performance before instruction $b_t$, immediately after instruction $u_t$, and at each clean-session delay $d$, $v_{td}$. Use independent response samples for screening and final estimation. Define above-pretest gains

$$
g_{t0}=(u_t-b_t)_+,
\qquad
g_{td}=(v_{td}-b_t)_+,
$$

and total immediate above-pretest gain

$$
M_0=\sum_t g_{t0},
\qquad
\bar g_0=M_0/N.
$$

Preregister a minimum $\gamma_{\min}>0$. Interpret the retained-gain ratio only when $\bar g_0\ge\gamma_{\min}$:

$$
R^{\mathrm{gain}}_d
=\frac{\sum_t\min(g_{t0},g_{td})}{M_0}
=1-\frac{\sum_t(g_{t0}-g_{td})_+}{M_0}
\in[0,1].
$$

Always report $N$, $b_t$, $u_t$, $v_{td}$ summaries, $M_0$, $\bar g_0$, the threshold, and signed item-level delayed changes. Do not average delays by default. Above-pretest change is attributable to instruction only when the design excludes rival causes; a causal attribution requires an appropriate no-instruction control or equivalent identification strategy. If the intended estimand is merely retention of immediately demonstrated performance, label and report that different estimand explicitly.

### 4.2 Response to feedback

For error rates $e_k\in[0,1]$ at attempts $k=1,\ldots,K$, $K\ge2$, define

$$
D=\sum_{k=2}^{K}(e_{k-1}-e_k)_+,
\qquad
U=\sum_{k=2}^{K}(e_k-e_{k-1})_+,
$$

$$
G=e_1-e_K=D-U,
\qquad
V=\sum_{k=2}^{K}|e_k-e_{k-1}|=D+U.
$$

$D$ is cumulative error decrease, $U$ cumulative error increase, $G$ endpoint gain, and $V$ total path length. Report $G$ and $U$ as primary outputs. Report $V$ only as a secondary trajectory diagnostic. When $K$ differs, report $U/(K-1)$ and $D/(K-1)$. The retired ratio $B=U/V$ is not an output.

Every feedback condition requires a matched no-feedback control with attempt count, task exposure, token budget, tools, timing, generation settings, and scoring held constant. Report at least

$$
\Delta G=G_{\mathrm{feedback}}-G_{\mathrm{control}},
\qquad
\Delta U=U_{\mathrm{feedback}}-U_{\mathrm{control}},
$$

with paired or hierarchical uncertainty at the randomization unit. Counterbalance or separate task sets when exposure to one condition can contaminate the other. Feedback type is part of the intervention and must be named.

## 5. Algebraic checks

Every implementation must test the following identities and raw-estimand bounds within numerical tolerance.

### Paired change

$$
L_{gp}=F^+_{gp}-F^-_{gp},
\qquad
\operatorname{INS}_{gp}=F^+_{gp}+F^-_{gp},
$$

$$
F^+_{gp}=\frac{\operatorname{INS}_{gp}+L_{gp}}{2},
\qquad
F^-_{gp}=\frac{\operatorname{INS}_{gp}-L_{gp}}{2},
$$

$$
|L_{gp}|\le\operatorname{INS}_{gp}\le1.
$$

Because the selected lower-tail mean cannot exceed the full mean,

$$
\operatorname{WTD}_{q,gp}\ge-L_{gp},
$$

with equality when $q=1$. For target-specific loss,

$$
\frac{1}{N_g}\sum_i\lambda^{(T)}_{igc}
\le\operatorname{WTL}^{(T)}_{q,gc}\le1,
$$

again with equality on the left when $q=1$.

### Feedback

$$
D,U\ge0,
\qquad
G=D-U,
\qquad
V=D+U,
$$

$$
D=\frac{V+G}{2},
\qquad
U=\frac{V-G}{2},
\qquad
|G|\le V\le K-1.
$$

### Retention

When $\bar g_0\ge\gamma_{\min}>0$,

$$
0\le R^{\mathrm{gain}}_d\le1.
$$

Pseudo-null-adjusted nonlinear estimates are deliberately untruncated and need not satisfy the raw-estimand bounds. Test raw and adjusted outputs separately.

## 6. Estimation and uncertainty

1. **Balance paired cells.** Use the same items and balanced response counts under baseline and perturbation. Randomize condition order where feasible.
2. **Estimate response noise only when present.** Repeated responses estimate conditional response behaviour. They are unnecessary for exact deterministic fixed-set descriptions, although item- or context-population inference still requires a sampling design.
3. **Estimate and subtract nonlinear pseudo-null contributions.** For stochastic INS and WTD, construct baseline-only pseudo-null contrasts with the same response counts as the real contrast. Report the raw estimate, mean pseudo-null expectation, untruncated difference, and uncertainty. Pseudo-null subtraction is not an unbiased recovery guarantee.
4. **Separate tail selection from estimation.** When item changes or losses are estimated noisily, select the WTD or WTL tail on one response split and estimate it on another; reverse roles and cross-fit. This addresses selection on response noise, not mismatch between the sample tail and an unobserved population tail.
5. **Match resampling to dependence.** Cluster, bootstrap, randomize, or model at the facets actually sampled. Preserve shared baselines, paired items, perturbation realizations, scorers, and model lineage. Use multiway or hierarchical methods for genuinely crossed facets; do not treat response replicates as independent items.
6. **Propagate predictor uncertainty.** Any validation model using estimated metric cells must carry their uncertainty through repeated fitting, measurement-error modelling, or a joint hierarchical model.
7. **Distinguish cellwise and simultaneous uncertainty.** Preregister the family of reported cells and tails. Provide simultaneous intervals or multiplicity control when the claim selects among many domains, perturbations, delays, or tail fractions.
8. **Keep heterogeneous interventions separate.** Pool perturbation families, realizations, or delays only under a declared target mixture and a model that represents their dependence.

For $r_p$, item and response resampling within domains propagates uncertainty in estimated domain means. Domains remain fixed unless a domain universe and sampling design have been declared.

## 7. Holdout must match the projection

| Intended projection | Minimum matching test |
| --- | --- |
| Tested to untested items | Hold out items at the item or task-template cluster; declare the item universe |
| One realization to another | Hold out perturbation realizations |
| One perturbation family to another | Hold out entire perturbation families |
| One system population to another | Hold out model families, lineages, or deployment configurations rather than randomly splitting near-identical versions |
| Present to future behaviour | Use chronological holdout on later sessions, releases, or deployment periods |
| Score to a decision | Validate calibration and decision value on independent outcomes under the declared loss, utility, or constraint |
| Behaviour to mechanism | Add mechanistic interventions and controls for rival routes; prediction from reported metric cells is insufficient |

Training, tuning, weight selection, tail-fraction selection, and threshold choice must occur inside the development partition. The outer holdout must remain untouched until final assessment. Shared items, baselines, perturbations, or model lineage across folds must be represented in the split or dependence model.

## 8. Failure conditions

Do not make the corresponding claim when any of the following holds:

- baseline and perturbed items are unpaired and no defensible linking model is supplied;
- the perturbation changes task-relevant information while the claim assumes invariance;
- profile variance is zero, or the number of domains makes correlation uninformative;
- $q$ produces too few tail items for the declared precision target;
- WTL lacks a declared target-specific loss or treats unequal consequences as interchangeable without justification;
- response stochasticity, scorer variation, or shared sampling facets are ignored;
- a deterministic fixed-set description is presented as response- or superpopulation inference;
- pseudo-null groups do not reproduce the real response-sampling design;
- a tail is selected and estimated on the same noisy responses without quantifying selection bias;
- floor or ceiling effects prevent the intended change from being observed;
- $\bar g_0<\gamma_{\min}$ for retained-gain interpretation;
- feedback lacks a matched no-feedback control when improvement is attributed to feedback;
- a holdout occurs at a narrower facet than the intended projection;
- heterogeneous cells are pooled without a declared target mixture; or
- predictive success is treated as construct, causal, decision, or mechanistic validity without the additional evidence that claim requires.

## 9. Minimum machine-readable report

An implementation should emit, at minimum:

- the registered declaration and estimand mode;
- the full facet and dependence audit;
- item identifiers and condition pairings;
- raw cell scores, $r$, $L$, INS, $F^+$, $F^-$, WTD, and baseline/perturbed WTL;
- $q$, tail count, target-loss definition, and all selection rules;
- raw, pseudo-null, adjusted, cellwise, and simultaneous uncertainty fields where applicable;
- retention pretest, immediate, delayed, $M_0$, $\bar g_0$, threshold, and retained-gain outputs;
- feedback and matched-control $D$, $U$, $G$, $V$, $\Delta G$, and $\Delta U$;
- split assignments, holdout facet, leakage checks, exclusions, missingness, and preregistered deviations; and
- software version, seeds, compute budget, model version, scorer version, and data provenance.

Any composite or target-specific weighting belongs in the validation model, not in this descriptive metric layer.
