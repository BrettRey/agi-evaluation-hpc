# Figure plan
<!-- SUMMARY: Candidate figure menu for warranted-inference-in-agi-evaluation; 1 figure + 2 tables at present, conceptual diagrams entirely absent · status: awaiting trim · updated: 2026-07-22 -->

**Current state:** 1 figure (4 panels, all empirical), 2 tables, 23 pages.
**Diagnosis:** the count isn't the problem; the *kind* is. The paper's contribution is
an operational method, and there's no diagram of the method anywhere. Everything
visual is a result. Meanwhile two quantities the argument leans on are computed and
unused, and one is specified but unimplemented.

## Menu

| # | Fig | Kind | Makes clearer | Type | Source | Keep |
|---|-----|------|---------------|------|--------|------|
| 1 | Source--target projection schematic | conceptual | that construction sample, evaluation universe, and target range are three places, and each Table 1 relation crosses a different gap | layered boxes + labelled crossings | conceptual | **must** |
| 2 | Stable mean, four item-level states | conceptual | the paper's motivating claim: identical means over unchanged / cancelling / tail-concentrated / persistently-failing item distributions | 4 small histograms, shared mean line | conceptual (schematic, no numbers claimed) | **must** |
| 3 | Worst-decile absolute case risk vs change tail, 32 comparisons | data | that a change tail and an absolute tail are non-redundant *on real data*, not only in simulation | paired scatter or dumbbell | `analysis/outputs/zhang_reanalysis/main_reanalysis.csv` (`wtd_raw`, `absolute_loss_tail_raw`) — already computed | **must** |
| 4 | Directional decomposition \(F^+\) / \(F^-\), 32 comparisons | data | the cancellation the whole §1 argument rests on, and it discharges Table 2's directional row | diverging stacked bar | `DATA NEEDED` — computable from cached trials; `metrics.py` has no \(F^+\)/\(F^-\) | **must** |
| 5 | Developer--deployer handoff | conceptual | the third contribution, currently prose-only: what each party supplies and what neither supplies alone | two-column boundary diagram | conceptual | nice |
| 6 | Split Fig. 1 into reanalysis (A,B) and known-truth (C,D) | data | matches §4.1/§4.2; stops one figure carrying two arguments | restructure only | existing | nice |
| 7 | \|L\| vs INS across 32 comparisons | data | the identity \(\|L_{gp}\|\le\ins_{gp}\) made visual; how far signed change understates movement | scatter + diagonal bound | `main_reanalysis.csv` (`signed_delta`, `ins_raw`) | nice |
| 8 | Realized-loss vs case-risk tail, stable-poor | data | the one estimand pair §7 claims diverges but §4 never quantifies | paired bar | `DATA NEEDED` — computable in `simulate_instability.py` | nice |
| 9 | Three estimand modes as nested scopes | conceptual | what fixed-set, stochastic-response, and population inference each license | nested boxes | conceptual | stretch |
| 10 | Interval coverage degradation for \(r\) (.988 → .579) | data | that a stated 95% interval isn't one under low profile spread | coverage bar vs nominal line | `profile_correlation_summary.csv` | stretch |
| 11 | Goodman source/target divergence | conceptual | green and grue agreeing on observations, parting at the target | two-line divergence | conceptual | stretch |
| 12 | Decision structure: premises + values + authority → rule | conceptual | that a decision isn't an epistemic projection | flow | conceptual | stretch |

## Recommendation

Keep **1, 2, 3, 4** and consider **6**. That gives three figures plus the two tables:
one conceptual diagram of the method, one motivating schematic, and an empirical
figure carrying the real-data divergence and the directional decomposition.

Drop 11 and 12: the prose already does that work, and a grue diagram risks being twee.
9 and 10 are real but the text carries them adequately. 5 is genuinely useful but the
§6 prose is clear, and boundary diagrams read as consulting slides in a philosophy venue.

## Blocking note

Candidate 4 isn't only a figure gap. \(F^+\)/\(F^-\) are defined in the paper, listed in
Table 2, and required by `metrics_spec_v3.md` §7 outputs, but `metrics.py` implements
neither. A reviewer who opens the companion finds the reference implementation missing
a specified output. Building 4 closes paper, spec, and code together.
