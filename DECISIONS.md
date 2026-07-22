# Decisions Log

Append-only record of project decisions. Agents: add an entry whenever a non-trivial decision is made during a session (structural changes, venue choices, theoretical commitments, scope changes, reviewer feedback acted on). Keep entries short.

Format: `## YYYY-MM-DD` then bullet points with **bold topic** and brief rationale.

---

## 2026-03-12

- **Projectibility is 3rd constitutive clause of HPC (not fuzzy boundaries).** §2.3 rewritten to present HPC as profile + mechanisms + projectibility. This aligns the paper with the book's slogan.
- **Path A: strengthen HPC rather than weaken formal claims.** The revision strategy is to make the HPC framework more robust, not to soften the paper's commitments.
- **Storage weight to rise from 7% to 9%.** Pending Step 4 of the 12-step revision plan. Reflects centrality-prior reanalysis.

## 2026-04-06

- **Storage weight implemented: 7%→9%.** Auditory 8%→7%, Speed 6%→5% to rebalance. Sum = 100%.
- **"Category" is the consistent working term.** "Kind" reserved for philosophy-of-science engagements (mechanistic kinds, historical kinds, natural kinds). "Label" eliminated.
- **Magnus response: stand by metaphysical claim.** Intelligence IS an HPC kind, not "just a useful tool." Magnus's critique sharpens the point: HPC needn't be universal to be right about intelligence.
- **Millikan response: convergence argument.** Intelligence can converge from different histories; what matters is whether the cluster holds now and licenses predictions. Where training history affects robustness, HPC captures it via stability indices.
- **Projectibility is upstream of contortion/compensation problems.** Contortion breaks projectibility by shifting measurement locus from agent to agent-scaffold composite. Measurement validity and deployment risk are downstream consequences. Compensation preserves projectibility because agent remains the locus.
- **Stability indices sample projectibility, don't exhaust it.** CSI geometric mean is a general-purpose default; purpose-specific weighting is the natural extension. Acknowledged tension with equal-weighting critique of Hendrycks.
- **Three-field purpose-indexing anchored in §2.4 only.** Safety/psychometrics/cognitive science examples consolidated to one canonical location; §3.1, §4.1, §4.4 cross-reference rather than repeat.
- **MIRAGE (Asadi et al. 2026) added as contortion example.** Multimodal model tops visual QA benchmarks without images.
- **Cross-reference to Vector Grounding paper** via footnote in §5 (sycophancy as strand dissociation ≈ contortion).
- **GitHub repo created:** BrettRey/agi-evaluation-hpc, CC BY 4.0.

## 2026-04-16

- **Yetman (forthcoming, *Ergo*) ingested.** "Representation in Large Language Models" defends MI techniques (probing, causal interventions) for testing whether capabilities are representation-based vs memorised. Directly relevant to the contortion/compensation distinction: contortion = good performance without representation-based competence (Yetman's performance-competence underdetermination). MI operationalisation could underpin stability index measurement (pCSI, dCSI, eCSI): probing tests whether a capability is represented, not just performed. Cite when submitting to Minds and Machines. Notes at `literature/yetman_2026_representation_in_llms.notes.md`.


2026-04-24 — Reading note: Simon et al. (2026), "There Will Be a Scientific Theory of Deep Learning" (arXiv 2604.21691v1). AGI evaluation sits at the "psychology" level in their physics/biology/psychology taxonomy; the paper argues all three levels are necessary and inter-grounding. Supports centrality-weighted scoring because different capabilities project from different levels. When next touching, consider citing as convergent external support for HPC-style levels-of-analysis in AI evaluation.

2026-04-25 — Reading note: Kuribayashi, Warstadt, Oseki & Wilcox (2026), "Dual Alignment Between Language Model Layers and Human Sentence Processing" (arXiv 2604.18563v1). The paper's punchline for AGI evaluation: LMs apply "essentially the same computational operations" to every input, whereas humans switch between shallow and deep processing modes (the latter triggered by high surprisal or entropy). The authors empirically demonstrate this gap by showing that no single LM layer matches both naturalistic reading and ambiguity-resolution behavior. Capability evaluations that score "language understanding" with one number conflate sub-processes that humans dissociate at the architectural level. The finding supports centrality-weighted scoring: behaviors that depend on reanalysis or contextual integration project from a different part of the system than fluent generation, and bundling them into a single benchmark obscures real architectural differences. When next touching this paper, consider citing as evidence that benchmarks need to factor sub-processes rather than aggregate them.

## 2026-07-17

- **Projectibility-first revision supersedes the March–April HPC-strengthening strategy.** The paper will no longer claim that intelligence is an HPC kind or that behavioural stability reveals homeostatic mechanisms. An AGI evaluation earns its use by improving a declared out-of-sample prediction or decision for a specified outcome, population, unit of analysis, intervention range, and time horizon.
- **Zhang et al. make robustness granularity constitutive of the design.** Profile-shape similarity, signed level change, item-level instability, harmful-tail degradation, and directional transitions will be reported separately. Repeated per-item sampling, a baseline-only estimate of the noise floor, and disjoint tail-selection and estimation samples are protocol requirements where feasible.
- **Dashboard before aggregation.** Equal weights and unweighted component reports are baselines. Alternative weights or a combined score require a shared projection target and held-out evidence that aggregation improves prediction or calibration; CHC structure is a defeasible organizational hypothesis, not a transported ontology or default machine weighting.
- **Behaviour does not establish securing mechanism.** Retention, updating, and scaffold-dependence tests remain behavioural measures. Representation, consolidation, control, or kind-membership claims require additional mechanistic evidence of the sort discussed by Yetman.
- **Retire the CSI family pending empirical validation.** The geometric-mean CSI, dCSI/eCSI labels, fixed centrality prior, and generic capped level-shift score are not defaults for the revision. The Lean formalization remains historical until the new estimands stabilize, at which point it will either be updated compactly or removed from the paper.
- **Canonical Lean companion updated; older generated specifications are historical.** The compact module now proves algebraic bounds for PSS, signed change, INS, externally selected WTD, retained mass, endpoint gain, and an exact backsliding share. Backsliding is $U/V$ when $V>0$ and $0$ when $V=0$, avoiding the old epsilon-distorted “fraction.” The proofs make no statistical, projective, construct, or mechanistic validity claim.
- **Projectibility sits within validity and remains epistemic.** It names target-indexed support for an inference beyond score construction. Decisions aren't themselves projections; they require projectible estimates plus declared loss, utility, or constraints.
- **Task/item population and sampling facets are part of the declaration.** Fixed-set description, stochastic-response estimation, and superpopulation inference are distinct. Holdout and resampling units must match the claimed item, context, system, temporal, causal, or decision relation.
- **Retire PSS and report Pearson correlation directly.** The unit-interval transform adds no information and invites ratio-scale interpretation. Raw domain profiles and their spreads remain visible.
- **Separate WTD from WTL.** WTD is signed worst-tail degradation, not harm. Absolute target-specific worst-tail loss is reported separately because stable severe failure can have WTD \(=0\).
- **Retire the backsliding share.** \(B=U/V=(V-G)/(2V)\) is algebraically determined by endpoint gain and total variation. Report gain and cumulative increases/decreases; use a matched no-feedback control for causal claims.
- **Retention uses above-pretest gain.** Reports include pre-instruction, immediate, delayed performance, the immediate-gain denominator, and a minimum-gain threshold. Causal attribution requires additional controls.
- **The empirical companion is deliberately bounded.** It reanalyses all 32 released Zhang cells and uses known-truth simulations to study estimator behaviour. It does not claim deployment prediction, CHC invariance, or general projectibility.
- **Descriptions and demonstration precede validation.** The paper now enacts its two-stage thesis structurally: preserve and demonstrate the candidate evidence first, then ask what warrants inference beyond it.
- **A three-move spine supersedes the two-stage formulation.** The paper now repeats the sequence declare the projection and scope, preserve resolution in the construction observations, and test the projection with matched evidence. This makes projectibility structural rather than a late gloss.
- **The metaphor system is disciplined by inferential role.** Aggregation compresses observations, descriptions preserve resolution, inferences project to targets within scopes, evidence warrants projections, and decisions use warranted estimates under declared losses. Reader-facing *noise floor*, *scaffold dependence*, *directional flow*, *gain mass*, and *profile shape* are replaced by pseudo-null expectation, component dependence, directional components, total immediate gain, and profile correlation. Earlier dated terminology remains as provenance, but these are the current terms.

## 2026-07-22

- **Projectibility is link-level within an interpretation-and-use argument.** It is assessed for each specified source--target link that extends an interpretation, prediction, or explanation beyond observed responses. It is neither a separate aspect of validity nor the warrant of a whole decision, which also requires alternatives, values, authority, and an action rule.
- **Goodman supplies the inductive problem; validity theory supplies the operational architecture.** The grue case explains why equal fit to observed cases doesn't determine which continuation is supported. Entrenchment and causal structure remain relevant background rather than general validation rules. Messick and Kane locate warrant in arguments for proposed interpretations and uses.
- **Construction sample, evaluation universe, and external target are distinct.** An aggregate may describe its observed construction sample. Generalization to a standardized universe and extrapolation from that universe to other tasks, contexts, systems, or times are separate steps. The declared target identifies distinctions that may matter; matched evidence determines which support the target-specific report.
- **Open-ended AGI claims use divided evidential labour rather than exhaustive testing by one evaluator.** Developers characterize bounded source evaluations and expose unsupported facets. Deployers complete local warrants, test whether target conditions obtain, and monitor consequences in use. Successful bounded links don't automatically compose into unrestricted generality.
- **CHC enters first as a content taxonomy.** Claims that AI scores exhibit the human factor structure, remain comparable across systems, or provide evidence of AGI require separate support. A descriptive profile doesn't inherit those interpretations from its organizing taxonomy.
- **Descriptive aggregation remains permitted.** Commensurability, compensability, and projectibility become additional obligations when an aggregate is interpreted as a measure or used in a decision; the framework doesn't require external validation merely to report a fixed-sample arithmetic summary.
- **The paper is an operational synthesis, not a discovery that averages conceal heterogeneity.** Its contribution is the target-indexed combination of validity argument, non-substitutable behavioural and risk estimands, facet-matched validation, and a developer--deployer handoff.
- **Canonical artifacts use descriptive names.** `warranted-inference-in-agi-evaluation.tex` and `.pdf` replace generic `main.*`; the historical GitHub slug remains unchanged for link stability unless a later repository migration is chosen.

## 2026-07-22 (pairwise section audit)

- **Terminology unified on *evaluation universe*.** §1 coined the term while §2 and Table 1 said *test universe*. The Kane generalization/extrapolation labels are now attached to the first two table rows so the taxonomy visibly discharges the distinction introduced at §1.
- **Domain restored as a facet everywhere.** It had dropped out of the workflow's sampling-audit step and the joint target draw \(J\sim P_T\) while remaining in §2's audit list. Domain indexes the whole profile argument, so the three lists now agree. Lineage and template cluster were added to §2's list for the same reason.
- **The declaration carries a three-way outcome.** Field 10 asked only for support and defeat conditions while the worked example, §5, and the workflow all invoked an inconclusive verdict. Field 8 now also names tail type, tail fraction, minimum count, and whether the rule is joint, per-stratum, or max-conditional.
- **Directional components are a first-class module output.** \(F^+\) and \(F^-\) were defined, argued about, and required by the canonical spec but absent from Table 2 and the conclusion's list. A table row was added and the conclusion's enumeration corrected.
- **\(\wtd_{q,gp}\geq-L_{gp}\) is stated in the paper.** The bound was in `metrics_spec_v3.md` only, which left §5.2's redundancy warning incomplete: it named \(L\), INS, \(F^+\), \(F^-\) but not WTD, which equals \(-L\) at \(q=1\).
- **The paper's own empirics are held to its own standard.** §4 now states that the reanalysis is verification on already published results with no prospective standing, names its estimand mode, and records that the 32 comparisons share items within benchmark and lineage across models, so 31/32 is not 31 independent replications.
- **Empirical claims split between reanalysis and simulation.** The abstract and conclusion had credited the reanalysis with a stable-average result only the simulation delivers; the MMLU-Pro case shows a 2.15-point decline, not stability.
- **Institutional authority is argued where it is used.** It was asserted in §2 and the conclusion and never developed; §5.4 now identifies who may impose a rule and states that evidence doesn't confer that authority.
- **The component-removal claim moved to where it is argued.** The workflow asserted that a removal effect establishes dependence but not mechanism; that sentence now sits in §5.2 with the rest of the causal treatment and the workflow inherits it.
- **Zhang's model-specificity figures are cited directly.** Mean cross-model correlation .00 and mean Jaccard overlap .09 on MMLU-Pro replace two vague gestures at "model-specific" changes, at §1 and in the limitations.
- **Rejected: the 13.6\%/53.2\% figures at §1 were flagged as unsupported and are not.** Zhang's Table 1 caption states that INS and WTD are noise-floor adjusted; 13.6\% is gemini-3.1-fl on GPQA and 53.2\% is Mistral-Large-3 on GPQA, and the recomputation for the Mistral cell falls inside the stated .21-point tolerance.
