# Referee review triage, 2026-07-22
<!-- SUMMARY: Triage of a major-revision referee review; ten fixes applied, five structural items awaiting Brett's decision · status: partly actioned · updated: 2026-07-22 -->

**Verdict on the review: take it seriously.** Every one of its five external citations
was checked and every one is real, correctly identified, and accurately characterised.
That is not the norm for model-generated reviews and it materially raises the weight of
the rest. Its diagnosis of the paper's centre of gravity also converges with a problem
found independently earlier the same day from a different direction.

## Verification

| Cited | Status |
|---|---|
| arXiv:2510.18212, Hendrycks et al., *A Definition of AGI* | Real. **Already our `hendrycks2025agi`** — so the "audit this" suggestion needs no new source |
| ACL 2024.acl-long.861, Liu et al., *ECBD* | Real; applies to BoolQ, SuperGLUE, HELM as described |
| arXiv:2406.10366, Binette & Reiter, estimands framework | Real; described accurately |
| EACL 2026.eacl-long.380, Jung et al., psychometric tests on LLMs | Real; 17 models, low ecological validity, as described |
| arXiv:1503.01603, Pearl & Bareinboim, transportability | Real; described accurately |

None of the four new works is in the central bib or `references-local.bib`.

**One correction to the review.** It reports a red--green contrast in Figure 4. Figure 4
panel B is coral against deep blue. The red--green pair is in **Figure 3** panel B
(coral/blue/sage). Its figure numbering slips by one in two places, including the
"Figure 3B ... close to arithmetic" remark, which concerns Figure 4B. The underlying
points are right; the labels aren't.

## Applied

1. **"Earns no projective credit" corrected** to "earns no extrapolative credit beyond
   the declared evaluation universe," with an explicit pointer that Table 1's first row
   treats within-universe generalization as a genuine inference. This was a real tension,
   in a sentence added earlier the same day.
2. **Interval-crossing passage rewritten.** The previous version objected to discreteness
   as such, which is wrong: every rule mapping continuous evidence to discrete action has
   a boundary, expected-loss minimization included. The objection is now the narrower and
   correct one, that such a rule imports an error-control convention and an implicit loss
   function instead of using the declared losses, constraints, and alternatives.
3. **"An imprecise estimate can't support a confident action" narrowed** — imprecision
   can strongly support a conservative action.
4. **Composition claim qualified.** Now states the conditions under which links may
   chain (interface population match, compatible assumptions, dependence and effect
   modification represented, no facet silently freed, uncertainty propagated) and
   identifies what actually fails as composition by accumulation.
5. **Item-bootstrap intervals declared model-based**, resting on exchangeability of items
   of the declared type, since benchmark items weren't probability-sampled.
6. **"22 of 32" given the same dependence caveat** as "31 of 32," generalised to every
   count and average over the cells.
7. **Lineage partial observability** noted: training overlap, distillation, and shared
   components are often proprietary, so assumed independence is itself an assumption.
8. **Companion URL made visible** as a printed address rather than hyperlinked text, and
   the sentence now names data-generating processes, replication counts, and estimator
   implementations as included.
9. **Figure 3 panel B de-coloured**: hatching plus direct value labels, so it survives
   greyscale and doesn't depend on the coral/sage contrast.

## Awaiting decision

**A. Centre of gravity: AGI paper or general AI-evaluation paper.** The reviewer's
preferred fix is a systematic projectibility audit of Hendrycks et al., claim by claim.
This converges with the independent finding earlier today that the running example
instantiates the AGI question only after being re-specified, and that the multidomain
apparatus has no worked instance. Two independent reads reaching the same fault is a
signal. Recommend doing it; it is the largest single item and interacts with the venue
decision record.

**B. Related-work section.** ECBD and Binette--Reiter are genuinely adjacent and their
absence is the kind of gap a referee treats as a novelty question. Roughly 600--800 words
plus four bib entries. Recommend doing.

**C. Distinguish informal *transport* from formal transportability.** One paragraph
citing Pearl & Bareinboim, saying our usage is broader and why. Cheap, and currently the
term is used unqualified throughout. Recommend doing.

**D. Jung et al. in the CHC section.** Directly supports the existing argument that
within-test reliability doesn't establish external meaning for an artificial-system
population. One or two sentences. Recommend doing.

**E. A real declared-projection study.** This is a research project, not a revision. The
reviewer's own alternative is to present §4 explicitly as an estimand tutorial rather
than as evidence for the framework, which is close to what the section already says.
Recommend the reframing, not the study.

**F. One-page declaration template**, filled twice (law firm, and the AGI framework being
audited). Depends on A.

## Noted, not yet acted on

- Page count is now 27 and items A, B, and F would push toward the mid-thirties. *Minds
  and Machines* states no article length limit in its submission guidelines, but that is
  a real cost to a reader.
- Table 1 density and possible landscape orientation.
- Sensitivity of conclusions across a small preregistered range of \(q\).
- A named procedure for the maximum-of-conditional-tails interval, rather than the
  current general warning.
- Whether the split estimate averages both split directions or repeated random splits
  should be stated compactly in the text.
- Permanent archival identifier (Zenodo or similar) rather than a mutable repository.
- AI-disclosure placement under anonymous review.
