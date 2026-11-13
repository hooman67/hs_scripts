# Tracking Housing Prices and Market Conditions

## Goal

Design a repeatable process—and then a repository-local Codex skill—to monitor property prices and market conditions in the principal-residence finalists. The shortlist will be populated only after the principal-residence re-research is audited.

## Research questions

1. Which sources provide reproducible sold prices, asking prices, inventory, days on market, price reductions, sale-to-list ratios, rents, mortgage rates, taxes, and insurance signals at city and neighborhood level?
2. Which sources are primary, licensed, public, scrape-restricted, paid, or manually collected?
3. How can the tracker avoid survivorship bias, listing-mix shifts, stale medians, duplicated listings, and asking-versus-closing-price confusion?
4. What cadence is appropriate for volatile versus slow-moving metrics?
5. What output best reveals an exceptional buying opportunity instead of merely reporting that prices fell?
6. Which steps can be automated legally and reliably, and which require browser review or a real-estate professional?

## Proposed tracking layers

This is a hypothesis to test, not a settled design.

- Weekly: active inventory fitting the family's actual property constraints, new listings, delistings, price cuts, relists, and time on market.
- Monthly: closed sales and comparable-property cohorts, median and distribution changes, months of supply, sale-to-list ratio, and mortgage-payment affordability.
- Quarterly: taxes, insurance availability, school boundaries, major development, commute policy, hazards, and employment-market context.
- Event-driven: mortgage-rate shocks, employer policy changes, immigration changes, insurance withdrawals, zoning changes, or material family-constraint changes.

## Deliverables

- A source matrix with access method, provenance level, geographic resolution, freshness, cost, and failure modes.
- A canonical observation schema and append-only history.
- A buy-opportunity signal with disclosed formula and backtesting limitations.
- A repository skill at `/home/colligo/hs_scripts/claude/prop_research/.agents/skills/track-housing-market/`.
- Human-readable periodic reports with per-claim evidence labels and confidence.

## Status

Methodology research is complete. No monitoring cities or alert thresholds are final.

The supported design is a hybrid, vintage-preserving tracker:

- authorized MLS/API data or agent exports for listing-level history and comparable sales;
- official government data for slower independent context;
- permitted manual downloads for secondary cross-checks;
- manual property diligence for taxes, insurance, condition, disclosures, and legal restrictions.

Automated scraping of Redfin or Realtor.com is excluded by the inspected terms. The tracker will preserve each source vintage because publishers can revise historical values.

## Current files

- Methodology research: `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/analysis/tracking_methodology_research.md`
- Evidence ledger: `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/evidence/source_claims_2026-09-10.csv`
- Tracker configuration: `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/config/tracker_config.json`
- Repository skill: `/home/colligo/hs_scripts/claude/prop_research/.agents/skills/track-housing-market/SKILL.md`

## Activation dependency

The skill is installed and can report setup status, but collection remains disabled until the principal-residence re-research yields an audited shortlist and the first finalist passes a source-qualification pilot.
