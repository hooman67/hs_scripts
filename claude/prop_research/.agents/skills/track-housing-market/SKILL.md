---
name: track-housing-market
description: Track verified housing-price, inventory, affordability, and listing changes for the configured principal-residence finalist markets. Use when the user asks to check, update, monitor, or compare those housing markets or look for unusually attractive listings. Do not use for selecting the initial shortlist, scraping restricted consumer portals, or executing property transactions.
---

# Track Housing Market

This is a repository-local monitoring workflow. It creates evidence-backed review alerts, never autonomous buy recommendations.

## Start

Read, in order:

1. `/home/colligo/hs_scripts/claude/prop_research/AGENTS.md`
2. `/home/colligo/hs_scripts/claude/prop_research/RESEARCH_METHODOLOGY.md`
3. `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/tracking_housing_process.md`
4. `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/config/tracker_config.json`

Run `python3 /home/colligo/hs_scripts/claude/prop_research/.agents/skills/track-housing-market/scripts/validate_config.py` before collecting data.

If configuration status is `AWAITING_AUDITED_SHORTLIST` or `PAUSED`, do not improvise markets, cohorts, data feeds, or alert thresholds. Report the missing activation prerequisites and stop the market update. You may still explain tracker status or help configure it from an audited shortlist.

`PILOT` permits bounded collection only for the single `pilot.market_id`. It does not permit cross-market alerts or claims that alert thresholds are calibrated. `ACTIVE` requires the pilot to be marked complete and reviewed, plus versioned alert rules.

## Source policy

- Use only public official downloads/APIs, explicitly authorized APIs/feeds, licensed exports, or user-supplied manual files.
- Do not scrape Redfin, Realtor.com, Zillow, MLS systems, or undocumented endpoints. Do not evade CAPTCHAs, access controls, rate limits, or terms.
- Treat consumer-portal data as secondary even when supplied manually.
- Preserve the raw artifact and retrieval metadata for every run. Never overwrite an older source snapshot with revised history.
- Open every cited source. Search snippets and prior reports are not evidence.
- Follow the evidence and confidence labels in the repository methodology.

For the evaluated source stack and limitations, read `/home/colligo/hs_scripts/claude/prop_research/tracking_housing_process/analysis/tracking_methodology_research.md` only when configuring sources, adding an adapter, or interpreting a metric.

## Modes

### Status

- Validate configuration and source freshness.
- Report configured markets, cohorts, sources, last successful run, and blockers.
- Do not fetch data unless the user requested an update.
- Treat this as a mechanical read-only status operation; no research recommendation is produced.

### Configure

- Accept markets only from the audited principal-residence shortlist.
- Define stable market boundaries and immutable cohort versions.
- Separate detached homes, townhouses, and condos.
- Record bedroom, bathroom, living-area, lot, price, age/style, condition, new-construction, distressed-sale, school-boundary, and exclusion rules as applicable.
- Pilot one representative market end to end. Incorporate its source and schema lessons before configuring the remaining markets.

### Update

1. Create a new timestamped run directory; never alter a prior run.
2. Ingest authorized automated sources and files placed in `manual_inputs`.
3. Record a run manifest and source snapshot metadata, including URL, publication/as-of/retrieval times, access mode, terms-check date, byte count, SHA-256, parser version, and status.
4. Normalize observations without discarding raw source definitions.
5. Validate geography, cohort, property type, transaction stage, period/window, units, sample size, and source vintage.
6. Compute only documented metrics from stored inputs.
7. Compare the newest vintage both with the prior vintage and with seasonal history; distinguish revisions from actual new observations.
8. Produce raw tables before signals and signals before narrative.
9. Assign only `NORMAL`, `WATCH`, `REVIEW`, `PROPERTY_DILIGENCE`, `INSUFFICIENT_DATA`, or `CONFLICTED` states. A signal is a prompt for human review, not a buy call.
10. Write a dated report containing sources, evidence labels, confidence, failures, stale inputs, changed assumptions, and reversal conditions.

## Interpretation safeguards

- Never treat a falling median as proof that comparable homes became cheaper; check property mix and matched cohorts.
- Never mix asking, pending, closed, assessed, or modeled values.
- Show sample size, window, cohort version, and quartiles where available.
- Widen a thin comparable set in this order: time, distance, then attribute bands. Record every relaxation.
- National mortgage averages are context, not the user's quote.
- A listing-level anomaly requires current matched comps plus manual checks of condition, disclosures, title, taxes, insurance, hazards, and location externalities.
- Missing or conflicted inputs cannot become favorable scores.
- Do not emit `WATCH`, `REVIEW`, or `PROPERTY_DILIGENCE` unless the configuration contains reviewed, versioned alert rules. Otherwise report raw observations and `INSUFFICIENT_DATA`.

## Parallelism

After the first-market pilot is validated, collect independent configured markets or independent source adapters in parallel. Each worker writes to its own staging path. Keep schema changes, cross-market synthesis, alerts, and final reports in the coordinating session. Pause fan-out if one source exposes a definition or licensing issue that affects the others.

## Boundaries

- Do not contact agents, purchase paid data, register accounts, send messages, or change external systems without explicit user authorization.
- Do not make offers or execute trades or transactions.
- Do not present tax, legal, insurance, immigration, or financing analysis as professional advice.
