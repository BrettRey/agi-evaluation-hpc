# Rhetoric and structure reading pass

**Manuscript:** *From Aggregate Scores to Projectible Profiles: Robustness in AGI Evaluation*
**Date:** 2026-07-17
**Scope:** Read-only first-reader audit of the current `main.tex`. No manuscript edits were made.

## Verdict

The difficulty is in the manuscript, not in the reading. There is a strong paper here, but its argumentative identity becomes fully legible only in Section 5. Before then, it successively presents itself as:

1. a reply to Hendrycks et al.;
2. a conceptual paper about validity and projectibility;
3. a Zhang-inspired robustness paper;
4. a technical dashboard proposal; and
5. a general handbook for AGI evaluation.

The manuscript says that projectibility organizes all this material, but it does not state early enough how the conceptual and technical halves fit together. Its clearest controlling claim is currently implicit across Sections 3 and 5 and explicit only in the conclusion.

The paper's strongest version is a two-stage evidential argument:

> AGI evaluation should first describe performance change without allowing aggregation to conceal its granularity, then establish on held-out evidence which of those descriptions supports a predeclared inference or decision.

That is more precise than “use projectible profiles” and more informative than “disaggregate and validate.” It explains why Zhang and Messick belong in the same paper.

## What a first-time reader thinks the paper is about

| Reading point | Apparent paper | Source of uncertainty |
|---|---|---|
| Title and abstract | A comprehensive replacement methodology for AGI evaluation | “Projectible profiles” sounds like a new kind of intrinsically valid score, although the paper later denies that projectibility is intrinsic. The abstract gives many coequal reforms without a dominant problem. |
| Opening page | A repair of Hendrycks et al.'s CHC evaluation using measurement theory | Hendrycks is the grammatical subject of the paper's first paragraph but is not the sustained interlocutor. The title promised robustness; the opening foregrounds CHC and validity. |
| End of Section 1 | A general projectibility-first framework | Five declaration parameters and four rules are clear, but the reader does not yet know why they require the particular dashboard that follows. |
| End of Section 2 | A Zhang-inspired critique of aggregate robustness | This is the first vivid empirical problem and feels like the real beginning. Equal weighting then changes the subject from cancellation to score construction. |
| End of Section 3 | A technical multi-granular dashboard proposal | The section is coherent internally. Only its final subsection reconnects the metrics to target-specific inference. |
| End of Section 4 | A broader handbook covering retention, feedback, composite agents, and mechanisms | No principle explains why these three protocols are privileged. The mechanism discussion makes an otherwise peripheral opponent look central. |
| End of Section 5 | An integrated paper about candidate evidence that must earn support for an external target | This is where projectibility, disaggregation, validation, aggregation, and weighting finally click together. It arrives too late. |
| Sections 6–9 | An implementation manual, research programme, governance note, and limitations inventory | Useful pieces accumulate rather than tightening one argument. |
| Conclusion | A coherent projectibility-first argument against premature aggregation | The conclusion is the first passage from which the whole manuscript can be summarized easily. |

## The missing bridge

The paper has two central claims:

- **Validity claim:** an inference or use must be indexed to a declared target and supported over the range across which it is meant to travel.
- **Information-preservation claim:** aggregate means and profiles can destroy distinctions that may matter for that target, so profile, level, item, and tail information should initially remain separate.

Both claims are persuasive. Their relationship is not stated near the start. The missing bridge is:

> Disaggregation can reveal what an aggregate conceals, but it does not itself make a score projectible. The proposed outputs are candidate evidence; their interpretation is warranted only when they support a declared target on observations not used to construct them.

This sentence would tell the reader what the paper is about, how Zhang and Messick fit together, and why the dashboard precedes validation.

The argument should visibly progress as follows:

```text
finite observations
      ↓
candidate descriptions at several granularities
      ↓
declared extrapolative target and range
      ↓
held-out validation and calibration
      ↓
warranted interpretation or decision use
```

The current order instead gives the declaration framework, then the motivating evidence, then several pages of metrics and auxiliary protocols, and only later supplies the validation step that connects them.

## Major structural findings

### 1. Motivation arrives after the framework

The abstract and Section 1 tell the reader what to declare and report before making the failure vivid. The first concrete surprise is the Zhang case in Section 2: nearly unchanged aggregate accuracy coexists with substantial opposed item changes and severe harmful-tail degradation.

That case should lead the argument. It gives the reader something to explain before introducing projectibility. Hendrycks et al. can then appear as an important multidomain setting in which this problem matters, without making the paper look like a reply it does not sustain.

The introduction also needs one sentence explaining why the problem is specifically acute for AGI evaluation. AGI batteries sample finite tasks but invite unusually broad inferences about competence across tasks, contexts, systems, and time. Without that point, the framework can look like generic measurement advice wearing an AGI label.

### 2. The paper has unresolved genre ambiguity

The title promises a robustness paper. Section 1 offers a validity framework. Section 3 is a methods paper. Section 4 is a protocol catalogue. Section 8 is a governance application. The appendix adds a formal-methods signal.

The manuscript has roughly 4,100 words of body text, nine numbered main sections, 29 headings, 20 displayed equations, and two tables. That density of sectional and mathematical apparatus makes it feel like a compact technical specification rather than a cumulative argument.

The recommended governing genre is **a conceptual measurement argument with a concrete methods proposal**. Projectibility states the evidential problem; the dashboard preserves candidate information; external validation supplies the warrant. Everything else should be subordinated as an application, implication, or limitation.

### 3. “Target” currently covers more than the validation protocol can handle

Section 1 permits a target to be an outcome, inference, explanation, or decision. These are not one evidential kind. Section 5 operationalizes projectibility mainly as prediction of an external outcome (Y). Decision use receives a loss-based treatment later. Explanatory claims about representation or mechanism require different evidence.

This makes the framework sound broader than its operational core. The paper should distinguish three lanes:

- **Extrapolative prediction:** supported by held-out prediction, calibration, and transport tests.
- **Decision use:** additionally depends on losses, thresholds, and the decision environment.
- **Construct or mechanistic explanation:** requires evidence that discriminates rival interpretations or causal routes.

Messick supplies the broader validity frame. Projectibility should remain the narrower extrapolative question rather than becoming a new name for everything an evaluation might warrant.

### 4. The target declaration and the dashboard are not mapped to each other

The paper supplies five projection-card parameters and four robustness granularities, but it never gives the decision rule connecting them. The reader needs to see how a declared target determines:

1. the relevant unit of analysis;
2. the perturbation or transport range;
3. the failure unit and loss;
4. the needed granularity;
5. the held-out criterion; and
6. the condition that would falsify the interpretation.

Table 1 names targets, and Table 2 names measures, but no table or running example joins the two. This missing mapping is the conceptual centre of the paper.

### 5. Section 4 looks inherited rather than derived

Retention, response to feedback, and scaffold dependence are individually sensible, but the reader is not told why these three receive full protocols rather than distribution shift, adversarial testing, long-context interaction, human-agent coordination, or another candidate.

Their structural rationale is available:

- retention varies the **time horizon**;
- feedback varies the **intervention range**;
- scaffolding changes the **unit of analysis**.

They should be introduced explicitly as worked applications of the projection card, not as privileged constituents of AGI. If that is not their role, the section should be reduced. The feedback equations are the least integrated and still read like residue from the retired CSI programme.

### 6. Validation is the payoff but arrives too late

Section 5 finally supplies the full sequence: declare (Y), treat the dashboard outputs as candidate predictors, compare them with a simple baseline, prevent target leakage, validate externally, and permit weights only when they transport.

This section should follow the core dashboard directly. Messick should recur at its opening because this is where a proposed interpretation and use earns support. “Incremental Predictive Evidence” or “External Validation Against Declared Targets” would fit better than “Incremental Predictive Validity.”

The schematic richer model also needs to be labelled clearly as target-specific. Written as a regression containing every metric, it momentarily looks like the generic composite the paper has warned against.

### 7. Several sections are in the wrong argumentative neighbourhood

| Material | Current location | Better role |
|---|---|---|
| Equal weighting | Section 2, under aggregate stability | Consolidate with target-specific validation and weighting in Section 5. |
| “Why No General Robustness Scalar” | End of the dashboard section | Use it to frame the dashboard before presenting formulas. The actual claim is “no purpose-free scalar.” |
| Construct-validity boundary | Inside scaffold dependence | Establish near the projectibility definition and return at validation. |
| Behaviour/mechanism boundary | Full subsection plus P4, limitations, and appendix | Reduce to one scope boundary unless explanatory targets remain a genuine branch. |
| Workflow and governance | Separate late sections | Combine around a concrete decision example. |
| Lean limitation | Main limitations section | Keep with the appendix unless formalization becomes part of the central contribution. |

### 8. The technical core needs a running example

The 70%/70% example is the clearest piece of exposition and then disappears. Carry two toy systems with the same aggregate change but different signed level, INS, and WTD through the dashboard and validation sections. That would let the reader understand why each quantity exists before encountering several pages of notation and estimation cautions.

A running deployment or release target would also make the later governance material feel earned rather than appended.

### 9. The final third repeats rather than escalates

Workflow, predictions, governance, limitations, and conclusion form five short consecutive sections. Each contains useful material, but the accumulation produces a handbook ending. Target specificity, tail constraints, mechanism limits, and validation recur without forming a visibly staged close.

The paper should end by showing what would make the proposal fail, what remains outside scope, and what the resulting discipline changes for one concrete decision—not by offering four more inventories.

## Recommended rhetorical spine

### 1. The inferential overreach of AGI scores

Open with Zhang's cancellation anomaly. Explain why broad AGI claims make the anomaly consequential. Introduce multidomain batteries, including Hendrycks et al., as the setting rather than the addressee.

### 2. From observations to declared projections

Introduce Messick, define projectibility as the narrower extrapolative issue, give the projection card, and state the two-stage thesis. Distinguish predictive, decision, and explanatory targets.

### 3. What aggregate robustness conceals

Generalize the granularity problem and present profile shape, level, item instability, and harmful tails as a minimal starting set of candidate descriptions. Use the 70% example throughout. Explain before the formulas why there is no purpose-free scalar.

### 4. From descriptive profiles to projectible inferences

Move current Section 5 here. Reintroduce Messick. Validate against held-out targets, compare simple baselines, prevent leakage, and handle aggregation, weighting, and CHC in one place.

### 5. Applying the projection card

Use retention, feedback, and scaffolds only as worked examples of changing time horizon, intervention range, and unit of analysis. State that they are illustrative, not exhaustive or constitutive.

### 6. Implementation and decision use

Merge the workflow and governance material around one running example, ending with an auditable report and explicit loss or tail constraint.

### 7. Empirical tests and limitations

Sharpen P1–P3 and pair each with its failure condition. Remove P4 unless explanatory targets remain central. Consolidate construct and mechanism limits here.

### 8. Conclusion

Return to the opening anomaly and state what the framework now permits the evaluator to claim—and what it still does not.

## Highest-leverage revision sequence

1. Rewrite the title, abstract, and first two pages around the concrete inferential failure and the two-stage thesis.
2. Move validation immediately after the core dashboard.
3. Add the explicit target-to-granularity mapping and one running example.
4. Recast Section 4 as applications or cut the parts that cannot be derived from the projection card.
5. Consolidate weighting, mechanism caveats, workflow, governance, and the ending.
6. Only then polish prose and equations.

This is a structural revision, not a matter of adding more signposts to the existing order.

## Secondary rhetoric and style observations

- The abstract is one dense inventory. It needs a problem–claim–method–payoff arc.
- “Projectible profiles” in the title suggests an intrinsic property, conflicting with the claim that projectibility is always target-indexed.
- “Why Aggregate Stability Isn't Reliability” risks invoking psychometric reliability more broadly than the section establishes. The demonstrated claim is that aggregate stability is insufficient evidence of robustness at another granularity.
- “Evaluation becomes decision-relevant only when the score travels” is too strong. A descriptive evaluation can be useful; an interpretation extending beyond the observations requires validation.
- Table 2 calls retention and feedback measures “robustness outputs,” while Section 4 says retention is not part of generic robustness.
- The paper should call the four core outputs a minimal starting set unless it intends to prove they are exhaustive.
- Mechanism caveats currently recur in Section 4, P4, limitations, and the appendix. This makes a retired debate look like a hidden central concern.
- The house-style checker found no rhetoric-changing mechanical defect. Its meaningful local flags were the long abstract, repeated argumentative-object paragraph openings, and an unglossed residual use of *homeostatic*. The underscore warnings are false positives inside mathematics.

## Recommended editorial decision

Retain the broad projectibility-first ambition, but make the paper narrower in execution. Its distinctive contribution is not a universal AGI handbook and not a reply to Hendrycks. It is the claim that **disaggregation preserves candidate evidence, while only target-indexed external validation turns any of that evidence into a warranted extrapolation or decision aid**.

Everything that does not advance, instantiate, test, or delimit that claim should move, shrink, or leave.

---
comments:
  c1:
    body: this all seems right. Hold out for a review from gpt-pro (imminent)
    by: user
    at: 2026-07-17T23:38:42.696Z
  c2:
    body: Understood. I will keep the manuscript unchanged and wait for the GPT-Pro
      review before recommending or applying the rearchitecture.
    by: Codex
    at: 2026-07-17T23:44:24.000Z
    re: c1
  c3:
    body: >-
      # Overall verdict


      **Major revision, with a strong publishable core.**


      The paper has a clear and consequential central claim: an evaluation score
      is useful only insofar as it supports a declared inference beyond the
      observations from which it was constructed, and the evidential basis for
      that inference must be stated in terms of a target, population, unit,
      intervention range, and time horizon. The four associated rules—declare
      the projection first, distinguish granularities, compare richer models
      with simple baselines, and aggregate only against a shared validated
      target—give the paper a coherent argumentative spine.


      The paper is strongest as a framework for disciplining interpretation
      rather than as a proposal for a novel family of metrics. The individual
      quantities are mostly familiar operations: correlation, signed
      differences, mean absolute differences, lower-tail averages, and retention
      ratios. The original contribution lies in assembling them into a
      target-indexed architecture and explaining why they should not ordinarily
      be collapsed. That is a worthwhile contribution, but the novelty claim
      should be framed explicitly in those terms.


      My overall assessment is:


      | Dimension                  | Assessment                              |

      | -------------------------- | --------------------------------------- |

      | Importance                 | High                                    |

      | Conceptual coherence       | High                                    |

      | Expository quality         | Very high                               |

      | Methodological originality | Moderate to high at the framework level |

      | Statistical specification  | Promising but incomplete                |

      | Empirical support          | Currently insufficient                  |

      | Recommendation             | Major revision                          |


      For a conceptual or measurement-theoretic venue, I would recommend revise
      and resubmit. For a technical machine-learning venue, the absence of a
      worked empirical demonstration would probably be decisive against
      acceptance in the present form.


      ## What already works well


      The distinction among profile-shape similarity, signed level change, item
      instability, and worst-tail degradation is analytically clean. In
      particular, the paper correctly insists that a high profile correlation
      establishes only relative profile preservation, while a near-zero signed
      change may conceal substantial two-sided churn.


      The refusal to propose a general robustness scalar is one of the paper’s
      best decisions. The examples—stable shape with falling level, cancellation
      with high item instability, and moderate overall instability with a
      concentrated bad tail—show that these are not merely alternative noisy
      indicators of one latent construct.


      The distinction between a base model, a stateful agent, and a deployed
      model–tool–retrieval composite is similarly strong. So is the boundary
      between behavioural evidence and mechanistic conclusions: the manuscript
      does not treat retention as proof of consolidation, falling error rates as
      proof of corrective control, or stable profiles as proof of an internal
      homeostatic organization.


      Finally, the operational workflow and explicit failure conditions prevent
      the paper from becoming a merely cautionary essay. The requirements
      concerning paired conditions, repeated sampling, external validation,
      auditability, and preregistered failure conditions make the proposal
      actionable.


      # Major revisions


      ## 1. Make *projectibility* more discriminating than a broad synonym for
      validity


      The definition currently ranges over an “outcome, inference, explanation,
      or decision”. Those targets require different warrants. Section 5
      primarily explains how to validate prediction of an external outcome,
      whereas Section 4.4 correctly observes that behavioural prediction does
      not by itself establish a representational or causal explanation.


      I would distinguish at least the following forms of projection:


      | Projection
    by: user
    at: 2026-07-17T23:57:21.683Z
