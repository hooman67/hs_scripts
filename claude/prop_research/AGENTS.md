# Property Research Rules

These instructions apply to all work under this directory.

## Source of truth

- Start with `/home/colligo/hs_scripts/claude/prop_research/PROJECT_STATE.md`, `/home/colligo/hs_scripts/claude/prop_research/README.md`, and the active project's summary file.
- Treat everything under a `legacy/` directory as untrusted historical input. It may suggest questions or candidates, but it is never evidence for a new claim.
- Follow `/home/colligo/hs_scripts/claude/prop_research/RESEARCH_METHODOLOGY.md` for evidence, citations, confidence, calculations, and review gates.

## Evidence labels

Every material factual claim in a research deliverable must include an evidence label:

- `PRIMARY`: the agent opened the original authoritative source and the cited material directly supports the claim.
- `SECONDARY`: the agent opened a reputable secondary source that directly supports the claim.
- `QUOTED`: another source states the claim, but the original source was not inspected.
- `INFERRED`: the claim is derived from cited facts; show the reasoning or formula.
- `ESTIMATE`: a stated assumption, proxy, or modeled value rather than an observed fact.
- `SPECULATIVE`: a plausible idea without sufficient evidence; never present it as a finding.
- `CONFLICTED`: credible sources disagree; preserve the disagreement and do not silently choose one.
- `UNKNOWN`: evidence is unavailable.

Keep confidence separate from evidence type. Use `HIGH`, `MEDIUM`, `LOW`, or `UNKNOWN` according to the methodology. A citation alone does not make a claim high confidence.

## Research conduct

- Open and inspect every cited source. Search-result snippets, generated summaries, and links copied from old reports do not count as verification.
- Cite the complete working URL, publisher, page or dataset title, relevant date, retrieval date, and table/field/page when available.
- Quote or capture the exact supporting passage or data row in the evidence ledger.
- Use the most granular relevant geography and comparable definitions. Do not mix city, ZIP, tract, county, listing, and sold-home statistics without labeling the mismatch.
- Separate observed facts, calculations, judgments, and recommendations.
- Never invent precision. Use ranges when the evidence supports only a range.
- Mark missing data `UNKNOWN`; do not fill gaps with plausible numbers.
- Preserve contradictory evidence and investigate it.
- Do not score or rank candidates until required fields pass the completeness gate. Run weight-sensitivity and downside scenarios before making a recommendation.
- Treat legal, immigration, tax, zoning, short-term-rental, insurance, school-health, and financing claims as professional-verification items unless supported by current primary authority.
- Never recommend evading vaccination, zoning, tax, lending, immigration, or short-term-rental rules.

## Parallel work

- Keep the main session focused on coordination, synthesis, and shared-file integration.
- Parallelize genuinely independent source collection or candidate research into separate agents when capacity exists.
- Do not parallelize across a learning dependency. Pilot the first representative candidate or source category, incorporate the lessons, and only then fan out the remaining equivalent work.
- Give each agent a separate output file or staging directory. Only the coordinating agent edits shared indexes, scoring models, or final reports.
- Before synthesis, audit agent output for opened sources, evidence labels, dates, geographic comparability, and unsupported conclusions.

## File organization

- Each research question belongs in its own top-level project directory.
- Each project has one clearly named summary file, plus `evidence/`, `data/`, `analysis/`, and `runs/` only when those directories have actual content.
- Store superseded or inherited work under that project's `legacy/` directory.
- Keep reusable methodology and repository-wide rules at the repository root.
- Use absolute filesystem paths when referring to files in user-facing responses.
