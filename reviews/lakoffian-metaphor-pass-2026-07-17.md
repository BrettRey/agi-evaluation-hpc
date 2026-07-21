# Lakoffian Metaphor Pass

## Verdict

The manuscript's governing metaphor is coherent and worth keeping:

> **INFERENCE IS MOTION FROM A BOUNDED OBSERVATIONAL SOURCE TOWARD A DECLARED TARGET.**

The score is constructed from finite observations; an interpretation projects beyond them; the projection has a target and scope; and matched evidence warrants that movement. *Projectibility*, *range*, *holdout*, *transport*, and the title's “From … to …” all belong to this frame.

The pass should therefore be a controlled consolidation, not a metaphor purge. The paper becomes clearer if each major metaphor has one job:

| Concept | Preferred framing |
| --- | --- |
| Aggregation | **compresses** observations and collapses distinctions |
| Granular description | **preserves resolution** needed for later inference |
| Inference | **projects** to a declared target within a stated scope |
| Evidence | **warrants** or defeats that projection |
| Decision | **uses** the warranted estimate under a declared loss or constraint |

Four secondary metaphors currently import entailments that conflict with the formal claims: *noise floor*, *scaffold*, *directional flow*, and *gain mass*. A fifth, *profile shape*, says more than Pearson correlation establishes. These should change. The manuscript should also stop making targets, dashboards, curves, and frameworks act as evidential agents.

## The structural repair: three moves, not two

The paper already has three moves, but the introduction and conclusion call it a two-stage argument:

1. **Declare** the projection target and scope.
2. **Preserve resolution** in the construction observations.
3. **Test** the projection with evidence matched to that scope.

That sequence should become the repeated rhetorical spine. It also gives the source–path–goal metaphor clear checkpoints instead of letting “the dashboard” become the accidental protagonist.

### Proposed abstract

> Finite multidomain batteries are used to support claims about untested tasks, contexts, systems, and future behaviour. Yet aggregate stability can conceal offsetting item-level changes, while a change-based tail statistic can miss failures that are severe in both tested conditions. I use *projectibility* for target-indexed support for a specified inference beyond the observations used to construct a score. Projectibility belongs within, rather than in place of, a broader validity argument.
>
> I develop an evaluation discipline with three moves. First, declare the projection target, system and task populations, bearer, intervention range, time horizon, decision loss, and evidential test. Second, preserve five distinct descriptions: domain-profile correlation, signed level change, item instability, worst-tail degradation, and absolute worst-tail loss. Third, test the projection using holdouts at the relevant facet; causal and decision claims require interventions or loss-sensitive evidence.
>
> Interpretable aggregates are separated from predictive or decision models, while retention, feedback, and component dependence are treated as applications with their own controls. A reanalysis of 32 released model–benchmark cells and known-truth simulations shows what the granular descriptions distinguish and why pseudo-null-adjusted and split-tail estimates are not interchangeable. The result is a target-indexed evaluation framework, not a new general-purpose score.

### Proposed opening statement of the argument

> The argument has three moves. First, declare the inference or decision and the scope over which it is meant to hold. Second, preserve distinctions that aggregation compresses: domain-profile association, signed level, two-sided item change, change in the worst tail, and absolute tail loss. Third, test the proposed inference with evidence not used to construct the score and matched to the declared scope. Granular description preserves candidate evidence; it does not, by itself, warrant a broader claim.

The later contribution paragraph should mirror this:

> The contribution is a target-indexed evaluation discipline rather than a novel family of mathematical operations. Its three moves are to declare the projection before choosing the score, preserve the relevant levels of description, and test the projection against a simple baseline on matching evidence. Aggregation is warranted only when held-out evidence for a shared projection target supports it.

### Proposed conclusion

> The same aggregate accuracy can describe an unchanged item pattern, balanced improvements and degradations, or stable severe failures. A broader domain profile repeats that compression at a coarser level; it does not resolve the underdetermination.
>
> The remedy has three moves. Declare the projection target and the scope over which the inference is meant to hold. Preserve the relevant distinctions in the construction observations: domain-profile correlation, signed level, item instability, directional components, worst-tail degradation, and absolute worst-tail loss. Then test the projection with a holdout defined on the corresponding facet. Held-out items, perturbation families, system-dependency groups, and later releases answer different questions.
>
> The worked demonstration warrants claims about the released cells and conditional claims under its simulation designs; it does not validate transport to deployment. Projectibility names the additional, target-indexed support needed for inference beyond the observations used to construct a score. It is one part of a validity argument, not a property of a descriptive report. AGI evaluation is a demanding case because its intended range is unusually broad, but the discipline is general: declare where the inference is meant to go, retain the distinctions present in the construction observations, and test that inference using evidence drawn from the corresponding scope. Only then is aggregation warranted for that target.

## High-value lexical changes

| Current frame | Unwanted entailment | Recommended replacement |
| --- | --- | --- |
| **noise floor** | A floor is a hard lower bound, but the paper correctly allows negative adjusted estimates. | **pseudo-null expectation**, **pseudo-null contribution**, **pseudo-null-adjusted** |
| **scaffold dependence** | A scaffold is temporary support around the “real” structure; this prejudges tools and retrieval as external to the genuine bearer. | **component dependence** or **configuration dependence**; heading: **Bearer and Component Dependence** |
| **directional flow** | Flow suggests movement of a conserved substance. That interpretation is exact only for deterministic binary transitions, not general score changes. | **directional components**, **mean positive change**, **mean negative change** |
| **immediate gain mass** | Mass suggests an acquired and conserved substance, encouraging the consolidation inference the section rejects. | **total immediate above-pretest gain** or **immediate-gain denominator** |
| **profile shape** | Pearson (r) is unchanged by positive affine transformation, even when spread and geometric shape change. | **domain-profile association**, **standardized linear association**, or simply **profile correlation** |
| **dashboard** as the main product | A control panel suggests several gauges of one underlying system health and can sound decision-authorizing. | **multilevel descriptive report** or **descriptive set**; retain *dashboard* only as an informal display label |
| **architecture** as the contribution | Invokes a novel engineered instrument and overstates the originality of the individual statistics. | **evaluation discipline**, **target-indexed framework**, or **protocol** |
| aggregation **erases**, analysis **recovers** | Suggests evidence is destroyed and that disaggregation reveals a hidden truth. The formal operation is many-to-one compression. | aggregation **compresses/collapses distinctions**; analysis **distinguishes/estimates** |

## Local repairs

These changes remove mixed metaphors, reified agents, or ambiguity without flattening the prose.

| Location | Current | Proposed |
| --- | --- | --- |
| Introduction | “breadth within a battery doesn't establish what the profile predicts beyond it” | “breadth within a battery doesn't establish which inferences the profile supports beyond it” |
| Contribution | “a shared target validates the aggregation” | “held-out evidence for a shared projection target supports the aggregation” |
| Projection card | “Claim and target” includes both inference and decision | **Claim and projection target** for the inferred outcome, interpretation, or explanation; leave action and loss under **Decision criterion** |
| Sampling audit | “models, lineages, or configurations” | Define dependency groups by training, distillation, shared components, data, or provenance; do not rely on biological family labels alone. |
| Profile table | “retain a similar linear shape?” | “remain strongly linearly associated after centring and scaling?” |
| Profile subsection | “A high (r_p) establishes only similar relative shape.” | “A high (r_p) establishes only strong linear association between the centred, scaled profiles.” |
| Uncertainty | “absolute values create a positive response-noise floor” | “absolute values give the statistic a positive expectation under the response pseudo-null” |
| Benchmark quality | “remains upstream … doesn't repair them” | “These estimands presuppose a sound benchmark. Disaggregation cannot resolve ambiguous items or an ill-designed perturbation.” |
| Scalar section | “a named target validates a function” | “held-out performance for a named target supports a function” |
| Figure caption | “baseline-floor-adjusted”; estimators “target different quantities” | “pseudo-null-adjusted”; estimators “estimate different estimands” |
| Demonstration | “what the aggregate omits” | “what the aggregate cannot distinguish” |
| Validation | “distinctions that a target may need” | “distinctions that may be needed for inference or decision about a target” |
| Validity | “one strand … additional strands” | “one source of validity evidence … additional, interacting considerations” |
| Release example | “clears a preregistered improvement”; “license the release projection” | “exceeds a preregistered minimum improvement”; “support the claimed next-cycle prediction” |
| Predictions | descriptions “earn their cost”; architecture “earns its role” | descriptions “add enough held-out value to justify their measurement cost”; granularity “improves enough to justify inclusion” |
| Component test | “A graceful curve … a sharp drop” | “A gradual change across tested degradation levels supports inference about those levels; a large discontinuous decrease indicates dependence on the altered component.” |
| Mechanism | “by exploiting language cues” | “because responses can depend on language cues even without image input” |
| Workflow | “directional flows” | “directional components” |
| Limits | “scaffold removal” | “component removal” or the named configuration change |
| Conclusion | “moves the aggregation boundary” | “repeats the compression at a coarser level” |
| Conclusion | extrapolation “travels” over a facet | test the projection “with a holdout defined on the corresponding facet” |
| Conclusion | evidence shows what can “safely” be combined | evidence shows what can **justifiably** be combined |

## Terms to keep

- **Projectibility / projection**: the master philosophical term, explicitly defined.
- **Transport / transportability**: established technical vocabulary for cross-population or cross-setting inference.
- **Tail**: mathematically disciplined through ordered fractions and expected shortfall. The text already prevents *worst degradation* from silently becoming *harm*.
- **Bearer**: precisely identifies the entity to which the score claim is attributed.
- **Profile** as a noun: useful for the vector of domain scores; only *shape* overstates what correlation preserves.
- **Holdout, facet, cell, crossed, nested, data leakage**: settled statistical or machine-learning terms here.
- **Conceal** in the opening sentence: rhetorically strong. Use *compression* and *resolution* in the technical exposition that follows.
- **Warrant**: the legal–epistemic frame is appropriate, provided administrative release authorization remains a separate decision.

## Scope of the edit

If accepted, I will apply the terminology consistently to `warranted-inference-in-agi-evaluation.tex`, reader-facing empirical labels and captions, `analysis/README.md`, `metrics_spec_v3.md`, and the public-facing Lean companion prose. Internal variable names can remain where renaming would add risk without changing what a reader sees. I will regenerate the empirical figure, run the analysis tests and Lean build, rebuild the paper, run the style and bibliography checks, and inspect the rendered pages.
