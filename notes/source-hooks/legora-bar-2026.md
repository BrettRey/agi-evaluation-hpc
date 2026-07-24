# Source hook: Legora Research 2026 — the Legora BAR (Benchmark for Agentic Reasoning)

**Source:** Legora Research, "Introducing the Legora BAR," reads as July 2026. Vendor-published legal-AI benchmark for "complex legal work in the agentic era." Central note: `literature/legora-bar-2026.notes.md`. **Primary post not yet retrieved** (not on legora.com/blog; /research 404s; unindexed) — what's on disk is a Figma social-media asset pack, not the study.

**Why this project cares:** it is a dated, real-world, *vendor-published* instance of the paper's central thesis, and the vendor published the evidence against its own headline number. Their "Cited answers" vs "Grounding" chart shows the sub-score rankings inverting: GPT-5.6 Sol leads on cited answers (~1.04×) but drops below average on grounding (~0.96×), while Fable 5 and Opus 4.8 lead grounding (~1.10×+) and sit barely above average on citations. One "overall quality relative to the seven-model average" figure sits on top of that. A second chart shows rank order changing across a difficulty facet (Short/Medium/Long): a narrow spread on Short, and on Long, Fable 5 and Grok 4.5 near 1.10× while GPT-5.6 Terra and Luna fall to roughly 0.80×.

**Where it could attach:**
- §1 / §3, as a current illustration that aggregation hides offsetting sub-dimension movement — with the point that this is a *vendor's own* chart, not a critic's reanalysis.
- The developer–deployer division: the BAR is the developer/vendor-side reference evaluation, exactly the artifact a firm would be handed and exactly what §6 says can't complete the local warrant. Legora sells the product class the running example describes (a legal-research assistant), so the transport gap is concrete rather than hypothetical.
- The Magesh contrast in §1: vendor assurance vs. independent audit (17–33% fabricated authority). The BAR is a live specimen of the vendor-assurance side.
- Table 1's present-to-future row: their "5% improvement on the Legora harness between June and July" is precisely a temporal projection.
- §5.4 decision use: they publish quality-vs-cost and quality-vs-median-minutes-per-case frontiers, i.e. procurement tradeoffs, without a loss scale or affected-party analysis.

**Caveat before citing:** do not put any chart value in the manuscript as a finding. It is vendor self-published with no independent replication; all values are normalized to a seven-model average (relative, not absolute); and the pack contains no task set, N, rubric, difficulty definition, scorer/judge description, or uncertainty. Byline illegible, URL unretrieved. Capture the primary post and its methodology first. Safe use now is as an *example of current vendor benchmarking practice*, not as evidence about any model.
