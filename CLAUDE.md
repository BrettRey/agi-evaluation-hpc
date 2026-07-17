# CLAUDE.md -- AGI Evaluation

## Role: Editor/Researcher

Deep editorial and research work welcome here. This is not a PM session.

## Project Overview

Paper arguing for projectibility-first AGI evaluation. Every score must be tied to a declared out-of-sample prediction or decision, population or model family, unit of analysis, intervention or distribution range, and time horizon. Aggregate stability is insufficient: Zhang, Koyejo, and Yang show that nearly unchanged accuracy can conceal large, two-sided item-level prediction flips and harmful-tail degradation. The paper therefore proposes a multi-granular robustness dashboard and a held-out validation protocol for any weighting or aggregation.

**Title:** From Aggregate Scores to Projectible Profiles: Robustness in AGI Evaluation
**Preprint:** [arXiv:2510.15236](https://doi.org/10.48550/arXiv.2510.15236) (October 2025)
**Target:** Minds and Machines

### Core Argument

1. **Declare the projection first:** An evaluation is useful only relative to a specified outcome, population, unit, intervention range, and horizon. Field interests select the target; held-out evidence determines whether the projection succeeds.

2. **Aggregates underdetermine robustness:** Stable domain means or profile shapes can hide offsetting item-level gains and losses. Zhang et al. provide the central demonstration; construction- and subprocess-level findings from von der Malsburg and Padó and Kuribayashi et al. reinforce it.

3. **Keep granularities separate:** Report profile-shape similarity, signed level change, mean absolute item instability, harmful-tail degradation, and directional transitions. Use repeated trials, estimate the positive noise floor, and separate tail selection from tail estimation.

4. **Behaviour is not mechanism:** Retention, updating, and scaffold-dependence tests characterize behaviour. They don't by themselves establish representation, consolidation, corrective control, homeostasis, or kind membership; Yetman identifies the additional mechanistic evidence needed for stronger claims.

5. **Validate weights and aggregation:** Equal weights and disaggregated reports are baselines. CHC structure is at most a defeasible organizational hypothesis or shrinkage prior for machines. Target-specific weights or a combined score must improve held-out prediction or calibration over simple baselines.

6. **Name the bearer of the inference:** Model-only and deployed-system evaluations answer different questions. Test full, degraded, and minimal configurations, but specify which composite system is supposed to support the deployment prediction.

### Key Sources

| Source | Role |
|--------|------|
| Hendrycks et al. (2025) "A Definition of AGI" | Primary interlocutor |
| Zhang, Koyejo, and Yang (2026) | Aggregate accuracy masks item flips and tail risk |
| Hernández-Orallo (2017) | Evaluation and fair characterization |
| Reynolds (2026); Weinberger (2026) | Stability, maintenance, and strict homeostasis distinguished |
| von der Malsburg & Padó (2026) | Construction-level divergence hidden by broad labels |
| Kuribayashi et al. (2026) | Layer/subprocess divergence in sentence processing |
| Yetman (2026) | Behaviour–representation evidential boundary |
| Carroll (1993); McGrew (2009); Schneider & McGrew (2018) | CHC as defeasible reporting vocabulary |

### Connections to Brett's Research Programme

- **Projectibility profiles:** Categories and metrics are assessed by the inferences they license for declared fields and populations.
- **Kinds and measurement:** Stable behaviour can be evidence for a projection without establishing a natural kind or its securing mechanism.
- **Boundary phenomena:** AGI labels remain purpose-sensitive, but successful prediction isn't merely conventional.
- **LLM competence:** The paper separates behavioural evaluation from representation- and mechanism-based explanations developed in companion work.

## Build

```bash
make              # Full build (xelatex + biber + 2x xelatex)
make quick        # Single xelatex pass
make clean        # Remove artifacts, keep PDF
```

Requires XeLaTeX (not pdfLaTeX or LuaLaTeX).

## Formalization

The canonical Lean companion is formalization/Formalization/Metrics.lean.
Run lake build from formalization/. Root metrics_spec files and the
metrics_formalized outputs document the retired CSI family and are marked as
historical artifacts.

## House Style

See `.house-style/style-rules.yaml`. Key rules:
- `\term{}` for concepts, `\mention{}` for forms, `\enquote{}` for quotes
- En-dash with spaces (`~-- `), never em-dashes
- Contractions preferred, ~60 word paragraphs
- `\textcite{}` narrative, `\citep{}` parenthetical
