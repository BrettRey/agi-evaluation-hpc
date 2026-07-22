# Pairwise section audit, 2026-07-22
<!-- SUMMARY: All 15 section-pair cross-checks of warranted-inference-in-agi-evaluation.tex; punch list of cross-section inconsistencies, gaps, and opportunities · status: actioned 2026-07-22, two items deferred · updated: 2026-07-22 -->

**Status: actioned 2026-07-22.** All Tier 1 and Tier 2 items and most of Tier 3 are in
the text; the paper builds clean at 23 pages with no undefined references. Two items were
deferred because they need new computation rather than editing:

- **§4 reports no \(F^+/F^-\) values** (Tier 1 item 4). The module is now internally
  consistent (Table 2 row, §3.8, §7 all agree), but the empirical companion would have to
  compute the directional components for at least the MMLU-Pro--gpt-5.4 case for §4 to
  exercise what §3 requires.
- **Realized-loss WTL is still never computed** (Tier 2 item 11). Handled for now by
  narrowing the conclusion to the divergences actually demonstrated. Reporting the
  realized-error decile from the stable-poor simulation alongside the .80 case-risk figure
  would close it properly, and that scenario is where the gap is widest.

Method: the paper was split into six units and every pair (15) was read by a separate
agent looking only for cross-section problems. Findings below are deduplicated,
ranked, and re-verified by grep or against source where marked. Line numbers are
against `warranted-inference-in-agi-evaluation.tex` as of commit d9eecbf.

Units: **A** abstract + §1 (L24--66) · **B** §2 (L68--139) · **C** §3 (L141--296) ·
**D** §4 (L298--330) · **E** §5 (L332--407) · **F** §6+§7 (L409--456)

---

## Tier 1: real defects, cheap fixes

**1. Two names for one term: "evaluation universe" vs "test universe".** (A--B; verified by grep)
L50 coins `\term{evaluation universe}`. L80 says "generalization within a stated test
universe"; Table 1 rows at L96--97 say "Observed responses to test universe" and "Test
universe to target task domain". L119 goes back to "the source evaluation universe", and
L446 to "a declared evaluation universe". Fix: unify on *evaluation universe* at L80,
L96, L97. While there, consider labelling table rows 1--2 "generalization" and
"extrapolation" so they close the loop with Kane at L52.

**2. "Domain" drops out of two facet lists.** (B--F and B--C, independently; verified)
- L133 (sampling audit): "model and version, item, **domain**, perturbation family and
  realization, operator role, team or site, ..."
- L425 (workflow step 2): "systems and lineages, item and template clusters, perturbation
  families and realizations, operator roles, ..." — no domain.
- L256 (the \(J\sim P_T\) draw): "system, task or episode, perturbation family and
  realization, operator, affected-population stratum, and time" — no domain.

Domain is the index the whole profile argument runs on (\(r_p\), \(L_{gp}\),
\(\ins_{gp}\), \(\wtd_{q,gp}\)). Fix: add domain to L425 and L256; add lineage and
template to L133 so the three lists agree.

**3. Declaration field 10 has no "inconclusive" outcome.** (B--F and B--E; verified by grep)
L128 asks only for "what would defeat or restrict it". But three places rely on a
three-way rule: L112 "one crossing .20 is inconclusive"; L357 "the preregistered support,
defeat, and inconclusive rules from the projection declaration"; L424 "including
prospective support, defeat, and inconclusive conditions". Fix: add "what would leave it
unresolved" to field 10.

**4. Directional components are half in the module.** (C--F and C--D; verified)
L207 defines \(F^+/F^-\); L219 gives the identities; L278 says they inherit the sampling
floor; L292 lists "directional change" among the behavioural descriptions; and
`metrics_spec_v3.md:336` lists \(F^+, F^-\) among required outputs. But Table 2
(L174--178) has no row for them, §7's list at L448 omits them, and §4 never reports one
(confirmed absent from `analysis/README.md` too). Fix: either add a Table 2 row and put
them in L448, or demote them explicitly to a decomposition of INS rather than an output.

**5. §7's compression of the declaration drops three fields and imports the audit.** (B--F; verified)
L452 lists "source, target, bearer, populations, relevant facets, horizon, tolerance,
evidential test, and failure conditions". Missing: field 6 intervention range, field 8
risk measure, field 9 decision criterion. And "relevant facets" belongs to the sampling
audit, which L133 explicitly separates from the declaration. Fix: restore the three
fields and keep the two-stage structure in the compression.

**6. "Institutional authority" is asserted twice and argued nowhere.** (E--F and A--F; verified by grep)
Only occurrences are L78 and L454. §5.4, the decision-use section, lists "objectives,
affected parties, consequences, feasible alternatives, preferences and tradeoffs, and
hard constraints" (L397) and never asks who is entitled to decide. Nearest support is
L413 in §6. Fix: give it a clause in §5.4, or drop it from L454.

**7. The component-removal claim at L429 is never argued.** (E--F; verified by grep)
Step 6 asserts "a component-removal effect establishes dependence over the tested levels,
not by itself an internal representation or corrective mechanism". §5's whole causal
treatment is L373's one sentence about process evidence and rival routes. The only other
occurrence of "component removal" is L438. Fix: add the sentence to §5.2 after L375 (it
also licenses L438), or cut the clause from step 6.

---

## Tier 2: substantive, needs a judgment call

**8. The paper's own empirical work isn't held to its own prespecification standard.** (B--D)
L116 requires a confirmatory evaluator to "register a projection declaration before
calculation"; L74 says a claim formulated after inspecting source results can't be
confirmed by that source analysis. §4's only status statement is L304: "The companion
pins the preprint version, repository commit, data hashes, seeds, and analysis settings."
That's reproducibility, not prespecification, and the reanalysis is post-inspection by
construction. Fix: one sentence at L304 saying the reanalysis is verification on already
published results and claims no confirmatory standing, plus whether the simulation
settings were fixed before the runs.

**9. Lineage is defined and then never applied to the paper's own 32 comparisons.** (B--D and D--E)
L82: "Outputs from closely related versions don't supply the same evidence as independent
lineages." L304: eight models crossed with four benchmarks. L310: "Split WTD exceeds the
null-referenced value in 31 of the 32 released comparisons, by .0331 on average." Items
are shared within benchmark, lineage across models, and the same baseline half feeds both
estimators, so 31/32 is not 31 independent confirmations and "on average" pools dependent
units. Fix: state at L310 that the count describes a fixed released set.

**10. A documented algebraic dependency is missing from both the module and the
redundancy warning.** (C--E; verified against spec)
`metrics_spec_v3.md:242` states \(\wtd_{q,gp}\ge-L_{gp}\), with equality at \(q=1\). The
paper never states it (grep confirms), and L371's redundancy list is "\(L\), INS,
\(F^+\), and \(F^-\)" without WTD. So the paper warns against separately weighting
algebraically dependent quantities while omitting one dependency it has documented
elsewhere. Fix: add the bound after eq:wtd and extend L371's list.

**11. Realized-loss WTL is argued non-substitutable and never computed.** (C--D and D--F)
L248 says the case-risk and realized-loss tails "coincide only under restrictive
conditions, such as no residual loss variation within pairings". L324 says "The tail of
realized binary errors is a different estimand" and gives no number, in exactly the case
where the gap is widest. §7 L448/L450 nonetheless claims all six quantities "can diverge".
Fix: report the realized-error decile alongside .80 in the stable-poor simulation, or
narrow L450 to the pairs actually demonstrated.

**12. §7 credits the reanalysis with a result only the simulation delivers.** (D--F and A--D)
L450: "can diverge even when an aggregate is stable". The reanalysis case shows a
2.15-percentage-point decline (L308), not stability; the zero-WTD case is the stable-poor
simulation (L324). Same issue in the abstract at L29, which attributes the coexistence
claim jointly to "A reanalysis ... and simulations". Fix: split the clause so the
reanalysis gets "moves only slightly" and the simulation gets "exactly stable".

**13. The stratum-max structure of the running example is lost in §5.** (B--E; verified by grep)
L110 "The .20 rule applies to the maximum of practice-area-conditional tails" and L112
"confidence interval for the maximum practice-area tail". "practice-area" occurs nowhere
in L332--407; L353 says only "an interval for the later release's rubric-scored case-risk
WTL" and L355's exceedance event \(\wtl^{\mathrm{case}}_{q,T}>.20\) is unindexed. L353
also drops the second holdout ("held-out local matters", L112). Fix: restore both.

**14. Two Table 1 rows get no matched design in §5.** (B--E; verified by grep)
The operator/workflow/site row (L100) has no counterpart in §5.1's unit list (L340:
template clusters, context families, lineages, chronological split). The
behaviour-to-consequence row (L103, L114) needs "exposure sampling, outcome surveillance
or impact study"; "surveillance" occurs only at L417, in §6, never in §5.4. Fix: add a
site/team holdout clause to L340 and point §5.4 at the surveillance evidence.

**15. "Target loss" names two objects; \(L\) carries three senses.** (C--E)
\(L_{gp}\) is a level change (L195); \(\ell^{(T)}_{igcR}\) is an item loss (L237);
\(\mathcal L_T\) at L342 is a prediction loss on \(Y\), not an aggregate of
\(\ell^{(T)}\). Fix: gloss \(\mathcal L_T\) at L342 as distinct from the item loss of
§3.5, and state its scale.

---

## Tier 3: opportunities

- **§4 is never cross-referenced.** No `\ref{sec:demonstration}`, `\ref{ssec:zhang_reanalysis}`,
  or `\ref{ssec:known_truth}` occurs anywhere in the paper (D--E, confirmed by grep). The
  best missed link: L355's "A model of case risk, a model of realized loss, and a model of
  a tail exceedance are distinct predictive objects" is exactly what §4's stable-poor case
  demonstrates with known truth. Also L330 should point forward to §5.
- **Zhang already supplies the model-specificity numbers.** L54's "largely model-specific"
  and L440's "an empirical hypothesis" both cite Zhang generically. Their paper reports
  mean Pearson r = 0.00 across models on MMLU-Pro and Jaccard 0.09 for the 10% most
  improved and most degraded sets (zhang2026illusionRobustness-v2.md:93--97). Citing the
  figures would make L440 concrete without new computation.
- **§1 L62's three questions are §5.2's three named terms, unnamed.** "whether its
  components share a meaningful scale, whether the tradeoffs it permits are acceptable,
  and whether the resulting score supports the declared target inference" is
  commensurability, compensability, projectibility (L361). Naming them at L62 also fixes
  the fact that none of the three contributions at L66 covers §5.2--§5.3 (A--E).
- **The law-firm example vanishes from §7.** It opens at L48 and is discharged at L417;
  L444--456 has no trace of it (A--F).
- **Kane's argument-based approach is introduced twice**, at L38 and L70, with the same
  citation pair (A--B). L38 could carry Messick alone.
- **Crossed/nested is defined at L135 and never used** where nesting is the live issue:
  L284's item bootstrap conditional on fixed domains is exactly items nested within fixed
  domains, crossed with conditions and scorers (B--C).
- **Estimand modes are never used to label §4's numbers** (C--D). L157--161 sets up three
  modes; the Zhang reanalysis is mode 2 and L326's coverage claim is mode 3, neither named.
- **Step 5 (L428) is missing several §3 requirements** (C--F): the individual-vs-simultaneous
  interval distinction (L286), the primary/secondary condition-level rule (L248), surrogate
  status of the loss (L239), publishing raw profiles and spreads (L163, L191), and
  cross-fitting, which §4 uses twice but step 5's estimator list omits (D--F).
- **§6.2 surfaces none of §3.7's estimator caveats** (C--F): pseudo-null contrasts aren't
  bias corrections, cross-fitting targets the selected set.

---

## Checked and rejected

- **The 13.6% / 53.2% figures at L54 are correctly characterized.** An agent flagged a
  mismatch against `analysis/outputs/section5_evidence_table.csv`. Verified against the
  source: Zhang's Table 1 caption reads "INS and WTD are noise-floor adjusted"; 13.6% is
  gemini-3.1-fl on GPQA and 53.2% is Mistral-Large-3 on GPQA. The paper's own
  recomputation for that Mistral cell is ins_adjusted .1130 and wtd_adjusted .5310, inside
  the .21pp tolerance claimed at L306. The agent had compared against a five-row subset of
  the table, not all 32 cells.
- **L191 does not forbid the bootstrap used at L326.** L191 says item-only resampling
  doesn't capture domain-choice uncertainty; L326's simulation resamples both, which is
  what L191 implies you'd need. `metrics_spec_v3.md:293` licenses domain resampling once a
  domain universe is declared, and a simulation declares one by construction. Worth one
  clarifying clause at L326, not a correction.
- **Arithmetic in §4 checks out.** .3680 − .1049 = .2631 (L308); .4514 − .4550 = −.0036
  (L322). WTD signs at L308, L320, L322, L324 are consistent with eq:wtd and the
  convention at L229.
