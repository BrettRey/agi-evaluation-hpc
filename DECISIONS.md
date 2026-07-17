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
