# STATUS.md -- AGI Evaluation (HPC)

## Current State

**Phase:** Major revision in progress (Minds & Machines prep)
**Last updated:** 2026-03-12

### Genesis

Paper drafted October 2025 on Overleaf. Posted to arXiv as 2510.15236. Imported to local workspace March 2026 for house style conversion and journal submission prep.

### What's Done

- Full paper drafted and posted to arXiv (October 2025)
- Imported from Overleaf to `papers/AGI_evaluation_HPC/`
- House style conversion (March 2026)
- Project infrastructure set up (Makefile, CLAUDE.md, symlinks)

### 2026-03-12 Session Notes (afternoon)
- Began major revision based on simulated-review plan: strengthen HPC as genuinely constraining by making projectibility the third constitutive clause
- **Completed (Steps 1-2 of 12):**
  - §2.3 rewritten: HPC defined as (1) co-occurrence, (2) mechanisms, (3) projectibility. Fuzzy boundaries now a consequence. Boyd 1991 cited for projectibility argument. Agent-level focus promoted from footnote to body; Craver contrast added.
  - §2.4 rewritten: requires three things (abilities, stability, projectibility), not two. Third implication on category value added.
  - New §2.5 "Why HPC Rather Than Alternatives?" inserted (~450 words): Craver (2009), Millikan (1999), Magnus (2014), Ereshefsky & Reydon (2015), Hernández-Orallo (2017). Rapoport's Rules followed throughout.
- Full build succeeds (27 pages). Only undefined citation: `hernandezorallo2017` (bib entry pending, Step 11).
- **Remaining (Steps 3-12):** Reframe centrality as projective (§3), raise storage weight (§3.4), reframe stability indices as projectibility tests (§4), address unit of analysis (§5), tighten predictions (§7), heavy governance trim (§8), rewrite abstract/conclusion (§9), reduce Hendrycks dependency (§1), add bib entries, add symbol table, verification pass.

### Note: Arora et al. (2026) — sparse circuits and category internals

Arora et al. (2026) "Language model circuits are sparse in the neuron basis" (arXiv:2601.22594): LM computations use sparse, neuron-aligned circuits. ~100 neurons control agreement. This complicates any "LMs don't really have categories" argument — the categories are localisable internally, though they may not map onto human taxonomies. Relevant to the cluster stability indices (§4): if internal representations are sparse and causally identifiable, the CSI family could potentially be grounded in circuit-level evidence, not just behavioural metrics.

### What's Next

- Continue revision Steps 3-12
- Verification pass (/check-style, /validate-bib, /proofread, /check-hpc)
- Journal-specific formatting if needed
- Submit

### Literature: Many Minds podcast (Frank & Lupyan, 2026-03-26)
- **Multiple realizability / Quine's topiary:** Frank introduces Quine's topiary metaphor — behavior clipped by the world, different branches inside. Cooperrider searches for the right term for "different routes to same outcome." HPC kinds are exactly this: multiply realizable clusters.
- **Convergent representations:** Platonic Representation Hypothesis = different architectures converge. Relevant to your HPC evaluation framework (what counts as "having" an ability).
- See `literature/many-minds-frank-lupyan-2026.md` for full notes + transcript.
