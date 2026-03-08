# CLAUDE.md -- AGI Evaluation (HPC)

## Role: Editor/Researcher

Deep editorial and research work welcome here. This is not a PM session.

## Project Overview

Paper arguing that AGI evaluation should move from flat, equally-weighted capability checklists to homeostatic property cluster (HPC) analysis. Two battery-compatible extensions proposed: (1) centrality-prior scoring that imports CHC-derived weights with sensitivity analysis, and (2) a Cluster Stability Index family (pCSI, dCSI, eCSI) that measures profile persistence, durable learning, and error correction.

**Title:** From Checklists to Clusters: A Homeostatic Account of AGI Evaluation
**Preprint:** [arXiv:2510.15236](https://doi.org/10.48550/arXiv.2510.15236) (October 2025)
**Target:** Minds and Machines (tentative)

### Core Argument

1. **Equal-weighting problem:** CHC-style AGI evaluations (Hendrycks et al. 2025) give 10% to each domain, ignoring that some abilities (reasoning, storage) are causally upstream of others (speed).

2. **Snapshot problem:** Testing at a single time point can't distinguish robust capabilities from brittle, scaffold-dependent performance.

3. **HPC reframing:** Intelligence is a homeostatic property cluster: abilities plus mechanisms that keep them co-present under perturbation. Evaluation should test both.

4. **Centrality-prior scoring:** Weight domains by CHC g-loadings and structural priors, with sensitivity analysis across lambda values.

5. **Cluster Stability Index family:** Three complementary indices measuring profile shape persistence (pCSI), durable learning (dCSI), and error decay (eCSI), combined via geometric mean.

6. **Contortion vs. compensation:** Scaffolds that inflate snapshot scores (contortion) vs. scaffolds that genuinely extend capabilities (compensation), with operational test protocol.

### Key Sources

| Source | Role |
|--------|------|
| Hendrycks et al. (2025) "A Definition of AGI" | Primary interlocutor |
| Carroll (1993) | CHC factor-analytic foundation |
| McGrew (2009); Schneider & McGrew (2018) | CHC theory development |
| Boyd (1999) | HPC theory |
| Khalidi (2013) | Natural kinds and classification |
| Keeney & Raiffa (1993) | Multi-attribute utility (geometric mean justification) |

### Connections to Brett's Research Programme

- **HPC theory in linguistics:** This extends HPC to philosophy of AI and evaluation methodology
- **Boundary phenomena:** AGI evaluation as boundary-drawing problem (graded membership)
- **Projection purposes:** Centrality weights as projection-indexed (what inferences matter depends on purpose)
- **LLMs as boundary phenomena:** Companion paper applies HPC to LLM categorization

## Build

```bash
make              # Full build (xelatex + biber + 2x xelatex)
make quick        # Single xelatex pass
make clean        # Remove artifacts, keep PDF
```

Requires XeLaTeX (not pdfLaTeX or LuaLaTeX).

## House Style

See `.house-style/style-rules.yaml`. Key rules:
- `\term{}` for concepts, `\mention{}` for forms, `\enquote{}` for quotes
- En-dash with spaces (`~-- `), never em-dashes
- Contractions preferred, ~60 word paragraphs
- `\textcite{}` narrative, `\citep{}` parenthetical
