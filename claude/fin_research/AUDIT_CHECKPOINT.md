# Independent Research Audit — Durable Checkpoint

Purpose: preserve the exact stopping point for the user's request to read the full project,
independently verify its research, and re-check its reasoning and decisions. Update this file
after every completed batch because the Codex session has repeatedly disconnected during
large tool calls.

Last updated: 2026-09-07 (America/Los_Angeles), Codex.

## User request

Read all project files, understand the complete context, independently verify the research,
and audit whether the reasoning and decisions were correct. Existing research files should
remain unchanged unless the user later asks for corrections.

## Disconnect diagnosis and mitigation

- Repeated disconnects occurred during unusually large or long-running tool calls.
- The first repository inventory returned a truncated listing (~1,700 files); a later read
  requested up to 40,000 output tokens; another interruption reproduced during a web search
  that ran beyond 30 seconds.
- Local diagnosis on 2026-08-25: the saved thread transcript is intact (~6.7 MB), the thread
  remains active, and the retained structured log window contains no WARN/ERROR records or
  network/API failure. The session lifecycle does show automatic context compactions at
  10:10 and 10:23 America/Los_Angeles during the long audit turn. The evidence therefore
  points to an oversized long-running context and automatic compaction causing apparent
  resets/disconnects; an underlying UI transport failure cannot be ruled out without app
  logs, which are not present at the documented macOS log location in this environment.
- Local Codex CLI is 0.149.0. The thread's memory mode is enabled, but the global config has
  no `[features] memories = true` flag, no generated `~/.codex/memories/` directory exists,
  and memory generation is asynchronous in any case. Built-in memory is not a dependable
  recovery mechanism for this active task.
- Mitigation: cap command output aggressively, use small file batches, avoid long combined
  calls, write findings here after each completed batch, and make each batch independently
  resumable. Root `AGENTS.md` now requires every future session to read this checkpoint first
  and update it after each substantive batch.

## Completed reading

- Full repository inventory was initiated. Repository is ~18 MB and has about 1,700 files.
  Most are cached yfinance/EDGAR JSON and Damodaran XLS evidence files.
- Read `CLAUDE.md` completely.
- Read `portfolio/CLAUDE.md` completely.
- Read `DECISIONS.md` completely.
- Read `LONG_TERM_PLANS.md` completely.
- Read `RESUME_README.md` completely.
- Read `research-plan.md` completely.
- Read `sources.md` completely.
- Read `PROJECT_STATE.md` completely.
- Read root `LEARNINGS.md` completely (three bounded batches).
- Read `portfolio/DECISIONS.md` completely.
- Read `portfolio/PROJECT_STATE.md` completely (two bounded batches).
- Read `portfolio/LEARNINGS.md` completely (two bounded batches).
- Read `portfolio/PHASE1_AUDIT.md` completely.
- Read `portfolio/ideal_allocation.md` completely.
- Read `portfolio/buy_list.md` completely.
- Read `portfolio/execution_plan.md` completely.
- Read `portfolio/sell_rules.md` completely.
- Read `portfolio/structural_audit.md` completely.
- Read `portfolio/COMPLETENESS_AUDIT.md` completely.
- Read `portfolio/holdings_snapshot.md`, `portfolio/data/holdings.py`, and
  `portfolio/data/analyze_structure.py` completely.
- Read `portfolio/dashboard/build_dashboard.py` completely, including its latest July 28 target model,
  source-of-truth handling, cash preservation, risk formulas and Google-Sheets write behavior.
- Read `portfolio/research/macro_usd_decay.md` completely.
- Read `portfolio/research/macro_energy.md` completely (three bounded batches).
- Read `portfolio/research/macro_china.md` completely (three bounded batches).
- Read `portfolio/research/macro_ai_thesis.md` completely (two bounded batches).
- Read `portfolio/research/macro_metals_uranium.md` completely (three bounded batches).
- Read `portfolio/research/macro_supercycle_metals.md` completely (two bounded batches).
- Read all three `portfolio/research/name_targets_*.md` files completely.
- Read `portfolio/research/completeness_asset_classes.md` completely (three batches).
- Read `portfolio/research/completeness_geography_blindspots.md` completely (two batches).
- Read `portfolio/research/completeness_sectors.md` completely.
- Read `portfolio/research/healthcare_thesis.md` completely, including the targeted section
  that was previously truncated.
- Read `portfolio/deep_dives/healthcare_PFE_LLY.md` completely (two bounded batches).
- Read `portfolio/deep_dives/healthcare_vehicles.md` completely.
- Read `portfolio/deep_dives/scorecard_misc_holdings.md` completely.
- Read `portfolio/dashboard/DASHBOARD_SPEC.md`, `SETUP.md`, `sheets_client.py`,
  `sheet_config.json`, and all 607 lines of `build_dashboard.py` completely.
- Read `data/README.md`, `data/fetch_damodaran.py`, `data/fetch_fundamentals.py`,
  `portfolio/positions/README.md`, and `RESTORE_SESSION.sh` completely.
- Read `screens/sector_cheapness.md` and `screens/sector_trends.md` completely (the latter
  in two bounded batches).
- Read `screens/sector_healthcare.md` and `screens/theme_ai_deflation.md` completely.
- Read `screens/candidates.md` completely.
- Read `screens/quant_screen.md` and `screens/run_quant_screen.py` completely.
- Read `screens/quant_screen_exus.md`, `screens/run_quant_screen_exus.py`, and
  `screens/universe_exus.py` completely.
- Read `screens/financials_screen.md` and `screens/run_financials_screen.py` completely
  (the memo in two bounded batches).
- Read `screens/ranked_output.md` completely (two bounded batches).
- Read `screens/fetch_damodaran_history.py`, `screens/analyze_sector_cheapness.py`,
  `screens/consolidate_candidates.py`, `screens/merge_candidates.py`,
  `screens/em_stress_test.py`, `screens/financials_universe.py`, and
  `screens/universe.py` completely.
- Read all three CNOOC files completely: `deep_dives/0883_HK/canadian_investability.md`,
  `deep_dive.md`, and `profile_and_diligence.md` (the latter in two bounded batches).
- Read `deep_dives/0966_HK/deep_dive.md` completely.
- Read all three CPIC files completely: `deep_dives/2601_HK/deep_dive.md`,
  `investability_and_alternatives.md`, and `profile_and_diligence.md` (the latter in
  two bounded batches).
- Parsed all 18 Python files with Python's AST parser: zero syntax errors. Validated
  `RESTORE_SESSION.sh` shell syntax: no syntax error.

## Preliminary internal-consistency issues found (not yet externally verified)

- `ideal_allocation.md` calls itself final but was superseded by a 2026-07-26 decision to drop
  VTIP and raise gold; the living target documents were not reconciled afterward.
- `execution_plan.md` states deploy sources of about $168k but revised uses of about $203k;
  the explanation says the gap comes from more trims without specifying/reconciling those
  additional sources.
- `execution_plan.md` says VTI+VXUS replaced VT, but its monthly tickets still instruct VT
  purchases; its closing USD-tilt note also conflicts with the amended 50/50 USD/CAD decision.
- Portfolio-volatility and crash-safety conclusions use a two-year normal-regime sample and
  a simple non-cash shock; they do not establish safety under joint equity/commodity/FX,
  liquidity, tax, or house-price shocks.
- Multiple decision-driving documents contain claims that require primary-source verification,
  including the alleged Shell–ARC acquisition, July 2026 Iran/US escalation, and live prices/
  multiples.
- The original 2026-07-07 holdings JSON omitted physical gold from market value because that
  row had no price source. Therefore the stated $275,426 non-cash total and $555,832 total
  excluded roughly $10k of physical gold even while the narrative said physical gold was
  included. Allocation percentages, volatility scaling, and crash arithmetic used an
  understated denominator.
- The current `portfolio/data/holdings_live.json` has seven material share/value mismatches.
  Examples: XOM 58 shares but value for 168; VTI 14 but value for 7; VXUS 39 but value for 19;
  XLU 58 but value for 23; GOOGL 18 but value for 3; WPM 192 but value for 227; ROOF.V value
  zero despite positive shares/price. Git history shows trades updated share counts without
  updating stored market values. The Google Sheet formulas may recalculate correctly, but
  the JSON and any analyses consuming `mkt_val_usd` are not trustworthy.
- `portfolio/data/holdings.py` still contains the original 53-position ledger and writes to
  obsolete absolute `/home/colligo/...` paths. The live JSON now has 63 rows, so rerunning
  this claimed source-of-truth generator would either fail here or overwrite later trades.
- `analyze_structure.py` also hard-codes the obsolete `/home/colligo/...` base path and consumes
  stale stored market values; it is not reproducible on this machine as documented.
- The Shell–ARC transaction itself is CONFIRMED from current primary sources: Shell announced
  the definitive agreement on 2026-04-27 for C$8.20 cash plus 0.40247 Shell shares per ARC
  share; ARC shareholders approved it on 2026-07-14, and ARC's current site says closing is
  anticipated in Q3 2026 subject to remaining conditions. This confirms the corporate-action
  premise, but not yet whether selling on 2026-07-10 was the economically optimal choice.
- The macro memos use labels such as `VERIFIED-as-cited` even when the author explicitly did
  not open the primary source. For this audit those claims are treated as secondary/unverified,
  regardless of the memo's label.
- The China memo mixes incompatible allocation denominators: it proposes 3% direct China and
  discusses filling a 25% EM target, while the finalized allocation has only 5% total in an
  `EM incl. China` sleeve. Broad-EM embedded China plus KWEB/BABA can also exceed the stated
  direct-China cap unless look-through exposure is measured.
- The industrial-metals memo reports BHP EBITDA shares of 55.4% iron ore plus 47.4% copper,
  which sum to 102.8%; those cannot both be shares of the same total without an explained
  adjustment. The proxy conclusion may be reasonable, but the presented arithmetic is not.
- The research repeatedly collapses gold, energy, agriculture, and industrial metals into one
  supposedly correlated factor. That is too coarse for portfolio-risk conclusions: gold's
  monetary/real-rate behavior can differ materially from growth-sensitive oil, copper, and ag.
  A factor model or stress matrix is needed before treating the full 37% as one exposure.
- The 2026-07-26 decision to raise gold to 14% conflicts with the metals memo's own suggested
  6-8% monetary-gold core and 12-14% combined precious-metals-plus-uranium range; no updated
  risk or funding reconciliation accompanies the change.
- The per-name real-assets targets still allocate only 9% to gold and therefore do not
  implement the later 14% gold decision. Several files independently call themselves final
  while encoding different target portfolios.
- `name_targets_energy_uranium.md` says ETN and SMR were not current holdings on 2026-07-26,
  but git history shows both were added to the holdings JSON earlier in July. Its starting
  inventory was stale.
- The bond-completeness work uses only a few hand-picked crash windows, labels IEF inconsistently
  as long/intermediate, and suggests XSB/VAB as government-duration hedges even though those
  funds are not pure government-duration exposures. A 5-8% bond sleeve also offsets only a
  small part of a major equity/commodity drawdown; the memo overstates the hedge's practical
  portfolio impact.
- Replacing that proposed bond hedge with XLU is not equivalent. Utilities remain equities and
  can fall sharply in equity crashes; a low beta does not make XLU a reliable principal or
  deflation hedge. This decision needs a fresh scenario test.
- The Foundayo/orforglipron FDA approval claim is CONFIRMED from FDA and Lilly primary sources:
  approval occurred 2026-04-01 for chronic weight management. The healthcare memo's key new
  product fact is sound.
- The PFE/LLY deep dive's qualitative conclusion is directionally coherent: PFE was the lower-
  quality, patent-cliff/coverage-risk value holding, while LLY was the high-quality but valuation-
  sensitive growth holding; the portfolio's larger PFE position was inconsistent with its stated
  quality-first philosophy. However, the document's exact prices, multiples, analyst targets,
  and proposed entry/trim levels were one-day snapshots and must not be treated as durable rules.
- The PFE/LLY deep dive repeatedly marks claims `VERIFIED` merely because another project memo
  cited them. Those inherited labels are not independent verification. Its AI-drug, AI-device,
  tariff, IRA-pricing, and competitor claims remain pending primary-source review in this audit.
- The PFE/LLY memo was already stale on a decision-driving fact: it listed orforglipron approval
  as unverified even though FDA approval had occurred on 2026-04-01. This illustrates why the
  project's point-in-time `live` labels cannot substitute for an as-of-date evidence ledger.
- The healthcare-vehicles memo's proposed dollar trades use the same ~$555,832 total that omitted
  physical gold, so its exact percentage and dollar targets inherit the denominator error.
- It treats GEHC's count of FDA AI-device clearances as proof of `real AI revenue`, but no disclosed
  AI-attributable revenue, margin, or valuation contribution is shown. Clearance count establishes
  product/regulatory presence, not that the proposed AI thesis is financially material.
- It calls PFE `income/ballast` largely from a low historical beta and dividend yield. A single pharma
  issuer facing patent, policy, and payout risk is not reliable portfolio ballast in the same sense as
  cash or high-quality sovereign bonds; this label is inconsistent with the memo's own risk analysis.
- The reported BSX decline from a $109 high to a $45 price is suspicious for a corporate-action or
  adjusted/unadjusted yfinance-series mismatch. That apparent drawdown must be reconstructed from an
  adjusted total-return series before being used as evidence of cheapness. The same check applies to
  every 52-week drawdown used in the memo.
- The memo's statement that holding CI in a `financials sleeve` means the healthcare exposure should
  not be counted twice is only an implementation observation. Sector labels do not alter the economic
  exposure: CI still contributes to total healthcare/payer concentration and must be included in the
  portfolio look-through risk calculation.
- ETF basket P/E, AUM, holdings, and fees labeled live/verified from yfinance or general knowledge still
  require issuer-factsheet verification. Exact entry/trim prices and the proposed XLV/PFE/GEHC reshuffle
  are stale tactical recommendations, not validated strategic rules.
- The miscellaneous-holdings scorecard contains basic balance-sheet/accounting overreads. CF's stated
  $3.6B debt versus $2.0B cash is net debt, not `net-cash-ish`; Ford's consolidated debt must be separated
  between automotive and Ford Credit before drawing leverage conclusions; and unusually high/negative
  ROE or book-value ratios often reflect capital structure, impairments, buybacks, or reverse splits rather
  than standalone evidence of quality or distress.
- Several dramatic 52-week price declines in the scorecard (including reverse-split-prone small caps and
  possible corporate-action cases) are not trustworthy until adjusted-price histories and split histories
  are reconciled. Raw yfinance `.info` current/high fields may compare incompatible share bases.
- PDBA is called `low-cost` without presenting its expense ratio and `low-beta ballast` from a tight single
  52-week range. A collateralized agriculture-futures fund still has roll-yield, curve, collateral, swap,
  tax, and commodity-shock risks; a quiet year does not make it capital-preserving ballast.
- The recommendation to sell small `orphan` positions may be sensible simplification, but the memo did not
  establish account type, tax residency, unrealized gains/losses, spreads, commissions, or whether the 3-5
  year house horizon applies to those assets. Exact sell/tax-loss actions are therefore conditional, not
  validated. Canadian citizenship alone does not determine Canadian tax or superficial-loss treatment.
- The scorecard infers durable value from point-in-time forward P/E and yfinance analyst fields without
  normalizing cyclical earnings (notably CF/AA/metals) or independently underwriting catalysts and cash
  flows (KHC breakup, CRCL economics, GEV backlog/margins). The consolidation logic is stronger than most
  individual buy/hold/trim price calls.
- `build_dashboard.py` contradicts its `NON-DESTRUCTIVE: only touches the FR_ tab` header: every rebuild
  deletes `FR_Dashboard`, `FR_Holdings`, `FR_Targets`, `FR_Rebalance`, `FR_TradeLog`, and `FR_perm_test` if
  present. That can destroy the very trade log the dashboard spec says should be retained.
- `_read_existing_nametgt()` misparses percentage-formatted values at or below 1%. For example, a sheet
  value displayed as `0.5%` is stripped to `0.5` and, because the code divides only when `v > 1`, becomes
  `0.5` (50%) rather than `0.005`. `1%` similarly becomes 100%. Rebuilding can therefore corrupt user-
  edited per-name targets by 100x.
- Dashboard holdings are filtered to tickers present in the hard-coded `HOLD_MAP`. Any new or unrecognized
  position is silently omitted from the holdings table, non-cash total, allocation, risk, and house-cushion
  calculations. A source-of-truth dashboard must instead surface unmapped positions as errors or include
  them in an `unclassified` sleeve.
- The dashboard claims volatility updates on rebuild, but hard-codes `VOL_TOTAL = 0.065` and
  `VOL_NONCASH = 0.132`. It also hard-codes a physical-gold fallback price of $4,132 and relies on stale JSON
  fallbacks for throttled/missing quotes. Dates update with `TODAY()` even when underlying inputs do not,
  creating a misleading impression of freshness.
- The dashboard's bucket targets are arithmetically inconsistent with its sleeve model: sleeve mapping puts
  Gold 14% + Ag 3% + XLU 4% = 21% in bucket B and only 20.5% cash in bucket A, while the displayed targets
  remain A=25.5% and B=16%, apparently retaining the dropped 5% TIPS allocation in the wrong bucket.
- Geography tags are crude domicile/theme rules, not look-through exposure. A US-domiciled international
  ETF can be tagged USA; global commodity companies are tagged GLB; and broad ETF country weights are not
  decomposed. The resulting geography chart cannot support diversification decisions.
- Book value for CAD positions is converted at current CADUSD rather than transaction-date FX, so the USD
  P/L calculation mixes security return with an inaccurate cost basis. Static BTC/gold values and a single
  average cost across accounts add further tax-lot limitations.
- The `house cushion after -30% crash` formula reports cash plus 70% of all non-cash assets as `still
  available`; it ignores taxes, liquidity, settlement, earmarking, joint shocks, and the possibility that a
  house purchase must occur during stress. It is remaining marked value, not a validated house reserve.
- `sheets_client.py --test` says a write/read round-trip is being tested but explicitly skips the write.
  `sheet_config.json` also commits the personal sheet ID even though the docstring says it is not committed;
  the ID is not a credential, but the documentation/privacy claim is inaccurate.
- The data pipeline equates field completeness with reliability. Its own TSM sample (about $2.3T market
  cap, 99.8x book, and 5.67x EV/EBITDA simultaneously) is an obvious unit/ADR/field-quality warning, yet is
  described as full successful coverage. Rankings need plausibility bounds and cross-field reconciliation,
  not merely a count of non-null fields.
- yfinance records `as_of` as the pull timestamp, not the reporting-period or provider timestamp of each
  fundamental. Calling these fundamentals `live` or timestamp-verified does not establish that earnings,
  book value, analyst estimates, or ratios were current on that date.
- The EDGAR extractor filters by filing form and end date but does not require fiscal-period `FY`, inspect
  `start`/duration, choose the latest filed/recast fact explicitly, or align concepts to a common fiscal
  period. A 10-K/20-F can contain comparative and duration facts; deduplicating solely by `end` can select
  a wrong-duration or superseded value. EDGAR is primary evidence, but this extraction is not yet a reliable
  ratio-validation layer.
- EDGAR values are fetched and printed but are not used to recompute or reject yfinance rankings. Thus the
  stated primary-source `ground truth` did not actually protect most decision-driving valuation/quality
  fields. Non-US names remain especially exposed to currency, ADR, and provider mapping errors.
- Damodaran `Global` includes US companies; it is not developed ex-US. Comparing US to Global as though they
  were disjoint regions mechanically dilutes regional differences. Annual aggregate industry averages are
  useful priors, but cannot by themselves identify current investable sector cheapness.
- `RESTORE_SESSION.sh` is unsafe as a memory mechanism: when a real Claude project directory exists, it
  ignores copy errors (`cp ... || true`) and then recursively deletes that directory before linking the
  durable store. It can therefore destroy sessions that failed to merge. It also calls `.session_history`
  both git-backed and gitignored. The new audit checkpoint is intentionally plain text in this repository
  and avoids that destructive restore path.
- The sector-history method compares changing industry aggregates over 11 annual observations. Industry
  membership, loss-maker inclusion, accounting, leverage, and rates change over time; an equal-weight mean
  of EV/EBITDA, P/B, and sometimes P/E percentiles has no demonstrated predictive validity or backtest.
  It is a hypothesis generator, not evidence that low-percentile sectors will outperform.
- Damodaran Global is repeatedly described as `developed`, even though it includes the US and emerging
  markets. This makes US/Global/EM tables overlapping rather than mutually exclusive and undermines some
  geographic conclusions.
- Life insurance is ranked with EV/EBITDA and industrial-style ROIC even though debt, investment income,
  statutory capital, reserves, embedded value, and asset-liability duration make those metrics poorly
  suited to insurers. The project itself later created a separate financials screen for this reason, so
  the EM-life `sweet spot` is methodologically inconsistent and must be re-underwritten with insurer metrics.
- The trend matrix has no explicit, reproducible trend-scoring rule; qualitative tailwind labels are crossed
  with noisy sector percentiles and presented as a ranked matrix. Many `VERIFIED` trend labels were inherited
  from subagent/secondary reports rather than independently opened primary sources.
- The oil underinvestment thesis relies partly on an interested-industry estimate of `required` investment,
  which depends on demand/scenario assumptions, while the same memo cites a possible 4 mb/d 2026 surplus.
  This can support a long-run scenario, not the claim that energy was `uniquely investable now`.
- The US Building Materials aggregate is used to validate Italy-listed Buzzi without demonstrating Buzzi's
  revenue/geographic mix, segment economics, or comparable valuation basis. A sector tailwind in one market
  does not automatically transfer to a global issuer.
- Information Services is heterogeneous; sector-level cheapness cannot establish that ratings/index firms
  are the discounted constituents rather than lower-quality data vendors. Constituent-level attribution is
  required before the 11.5x aggregate can support SPGI/MCO/MSCI selection.
- The sector memos overgeneralize entire industries as traps (food processing, cable, education) from selected
  examples. Secular headwinds are valid risk flags, but company-specific pricing power, balance sheets, capital
  allocation, and valuation still determine whether an investment is a trap.
- The healthcare thesis assumes without constituent evidence that Damodaran `Healthcare Support Services`
  is a valid HMO/managed-care proxy. That broad bucket may mix distributors, services, IT, and other business
  models; its 31% aggregate ROIC and 5th-percentile P/B cannot be attributed to UNH/CI/ELV without a membership
  bridge. This is the load-bearing premise behind `managed care is the only cheap corner` and is unproven.
- It again uses EV/EBITDA/ROIC to compare insurers/payers, where medical reserves, regulated capital, debt,
  PBM economics, risk adjustment, and investment assets require payer-specific measures. CI's low forward P/E
  alone does not establish cleaner risk; PBM reform/Evernorth concentration and forecast quality need analysis.
- Aging populations and rising healthcare spending are real demand facts, but they do not guarantee shareholder
  returns: government/payer bargaining, utilization, labor, reimbursement, and capital intensity determine who
  captures the spending. The memo often moves directly from demographic growth to beneficiary labels.
- FDA AI-device authorization counts establish regulatory/product activity but not company-specific AI revenue,
  incremental margins, adoption, reimbursement, or valuation. UNH/Optum productivity claims are largely company-
  reported and must be reconciled against implementation cost, pass-through to customers, denial litigation,
  medical-cost trends, and any current investigation outcome.
- The AI-deflation memo's software-versus-services mechanism split is a useful framework, but `services has no
  pricing power` is too categorical: contract mix includes fixed-price, managed service, subscription, and
  outcome-based work, and providers may retain some productivity gains or expand scope. The net outcome remains
  empirical, as the memo ultimately acknowledges.
- CTSH at 1.31x book is not demonstrated downside protection. For an acquisitive asset-light services company,
  goodwill/intangibles and working capital make book value a poor liquidation floor. Conversely, TCS at 7x book
  is not by itself evidence of no margin of safety for a high-ROE asset-light franchise. Both need normalized
  owner-earnings/FCF scenarios, balance-sheet composition, and currency-consistent valuation.
- The claim that Intuit's low-end TurboTax unit decline is `AI-adjacent` is causal inference, not established
  fact; price, product mix, IRS policy, competition, and macro factors must be separated. Two or three quarters
  of bookings/revenue can update near-term probability but cannot validate or refute terminal AI disruption.
- Point-in-time forward P/E, PEG, yfinance FCF yield, and sell-side price targets are treated as proof that severe
  outcomes are priced in. No audited DCF/reverse-DCF or normalized cash-flow bridge is shown in this synthesis;
  therefore the INTU/CTSH buy asymmetry remains a hypothesis pending the individual deep-dive audit.
- The candidate join misclassifies CTSH, TCS, and ACN (IT outsourcing/consulting) as Damodaran `Information
  Services`, the cheap/moaty ratings-data bucket, even though the project's own trend memo places IT/Computer
  Services on the AI-deflation risk side. This mapping error is load-bearing: it promotes flagship `BOTH`
  candidates using the wrong sector cheapness and quality statistics.
- TCS is allowed to use US/Global Information Services cheapness despite the stated region gate that an EM name
  needs an Emerging-sector verdict. The dagger note explicitly overrides rather than follows the method.
- Italy-listed/global Buzzi is promoted from cheap US Building Materials even though the memo reports Global
  Building Materials at a 73rd-percentile composite (not cheap). Without geographic segment attribution, this
  is another wrong region/sector transfer.
- The finalist list enforces arbitrary equal region counts and maximum two names per sector without an objective
  optimization, covariance, valuation-confidence, or portfolio-need basis. It still concentrates common factors
  (two gold miners, two China life insurers, multiple China names) while claiming sector diversification.
- `K.TO diversifies miner exposure into Canada` confuses listing/domicile with economic diversification; Kinross
  and Newmont remain highly exposed to the same gold-price factor and global mine jurisdictions.
- Non-comparable financial and non-financial percentile scores are combined through judgment into one locked list.
  Known corrupted inputs (TSM 99.8x book, PDD/TME FCF yields, miner proxy issues) remained in high-ranked outputs,
  showing that warnings did not reliably gate bad data before selection.
- The candidate memo labels each raw yfinance field `VERIFIED` because it was fetched, while acknowledging it was
  not checked against filings. In this audit, fetched-but-unreconciled fields remain unverified evidence.
- The quant score averages all available metrics with `skipna=True` but imposes no minimum metric count or
  missingness penalty. A company ranked on one or two favorable fields can compete with a fully observed company;
  missing D/E explicitly passes the trap gate. Cross-name scores therefore have uneven evidence bases.
- Extreme FCF yields (PDD 61%, PBR 80.5%, NTES 41%, ABEV 37.7%) are flagged in prose but neither winsorized nor
  removed from scoring, so known suspected artifacts materially boost cheapness ranks. The data guard only blanks
  EV/EBITDA below 2 and ROIC above 100%.
- The ranking applies a flat 21% tax rate to every jurisdiction and compares gross margin, operating margin,
  current ratio, D/E, P/E, P/B, and FCF yield across banks, REITs, miners, software, ADRs, and cyclicals. These
  metrics are not uniformly comparable, and no industry-neutral or cycle-normalized ranking is used.
- The `Piotroski-lite` score is not Piotroski: it uses a single snapshot, substitutes OCF>0 for accrual quality,
  rewards current ratio and positive revenue growth rather than changes, and divides by the number of available
  signals. A name with few observed signals can pass on a small denominator. Calling repeated 7/7 results a trap
  safeguard materially overstates what the gate establishes.
- VICI's displayed 99% gross margin and 107.5% operating margin, TSM/MU currency/share-class artifacts, and
  financial companies in the non-financial screen demonstrate that plausibility and business-model gates failed.
  Known bad fields remained visible in top-40 selection and subsequent finalist logic.
- A one-day cross-sectional percentile gives no absolute valuation margin, cycle normalization, or expected-
  return estimate. The 60/40 quality/cheapness weights are arbitrary and have not been sensitivity-tested or
  validated out of sample.
- The ex-US/global merge deduplicates tickers, not issuers or share classes. ADRs, local listings, CDIs, and
  dual classes remain multiple observations (e.g. Newmont US/Australia and ResMed US/Australia), distorting
  percentile distributions, region counts, and the claim that ex-US dominates the global top tier.
- Region is inferred mainly from exchange suffix/list membership, not issuer domicile, revenue, assets, or risk.
  This is especially misleading for global miners/ADRs and for a Canadian investor, for whom Canada is domestic
  rather than a generic developed-ex-US diversification bucket.
- The hard-coded universe is brittle and contains classification mistakes: `CFR.SW` (Richemont, luxury goods)
  is excluded as an obvious financial. Wikipedia table indexes and hand-curated lists can silently drift; issuer-
  level identifiers and logged constituent snapshots are needed.
- The global top ranks are dominated by miners on trailing boom-period margins/earnings. No commodity-price or
  mid-cycle normalization is performed, so the screen can systematically label peak earnings as cheap. Listing
  duplicates amplify the same commodity factor rather than add independent evidence.
- The financial screen's `capital strength` proxy ROA/ROE only approximates equity/assets if ROA and ROE use
  aligned numerators, periods, and average balance sheets; yfinance does not establish that. It is not regulatory
  capital, and ranking higher equity/assets as universally better ignores business-model and risk-weight differences.
- Financial quality inputs ROE, ROA, and ROA/ROE are algebraically dependent; value inputs P/B, P/E, and dividend
  yield are also linked through ROE/payout. Averaging percentile ranks double-counts related signals rather than
  providing three independent confirmations.
- The financial score again averages missing metrics with `skipna=True`; peer-cell sizes vary, and no minimum
  observations or stability test is required. `trap_status` does not gate ranking, allowing flagged names such as
  BMPS to appear first. Snapshot thresholds (-40% earnings growth, 0.6x book/8% ROE, payout 100%) are arbitrary.
- The memo says EM life is `confirmed at the company level` while acknowledging it lacks embedded value, VNB,
  solvency capital, asset duration/quality, reserve assumptions, and normalized earnings. Those omissions are
  exactly what determine whether China life P/E/ROE/P/B figures reflect durable value or market/accounting gains.
- Dividend yield can include specials or stale distributions (not a sustainable forward yield), and REITs remain
  ranked on GAAP P/E/ROE despite the memo acknowledging FFO/AFFO is required. PGR/VICI and other income-heavy
  results must be rebuilt from issuer distributions and sector-specific cash-flow measures.
- The master ranking's CNOOC correction is legally unsafe. Canadian citizenship does not resolve whether the
  owner is a `US person` or is transacting from within the United States; other project context indicates TN/US
  residence or green-card-pending possibilities. Broker domicile alone may not cure a transaction initiated by
  a person/location within scope. CNOOC must remain blocked pending current OFAC text, exact immigration/tax/
  physical-location facts, broker compliance, and qualified legal advice.
- CNOOC's ranking is left internally contradictory: banner and candidate portfolio call it investable/#1, while
  later tier/theme sections still call it blocked/uninvestable. This is a dangerous state for an operating memo.
- Applying the same nominal scorecard weights does not make 16 separately judged deep-dive scores comparable.
  Anchor definitions, normalization, evidence quality, and scoring calibration differ by issuer and analyst run;
  no inter-rater or sensitivity analysis supports fine distinctions such as 7.75 versus 7.65.
- The master list inherits the candidate sector-mapping errors (CTSH/TCS Information Services, Buzzi US sector
  transfer), yfinance/ADR artifacts, and arbitrary finalist composition. Later qualitative work can improve an
  issuer thesis but does not retroactively validate the screening funnel.
- Pairing CNOOC and EOG diversifies jurisdiction/listing but doubles the main oil-price and energy-cycle factor,
  which the memo acknowledges. Likewise three China names share policy, capital-control, geopolitical, currency,
  and market-access risks even when their company-specific risks differ.
- Claims such as `EDGAR-tied-out` do not establish that valuation multiples, forward estimates, FCF definitions,
  prices, or normalized earnings were reconciled. INTU/CTSH exact valuation asymmetry and all tactical entry
  decisions remain pending primary-filings reconstruction and reverse-DCF sensitivity.
- The sector-analysis code will publish/rank a composite supported by only one historical signal
  (`n_hist_signals >= 1`) even though the methodology emphasizes a multi-metric composite. No same-industry
  continuity check handles taxonomy/member changes across 11 years, and exact-name matching silently drops
  renamed industries.
- The candidate code makes the known bad mappings explicit: `Information Technology Services -> Information
  Services`, and `DEV_EXUS` is allowed to use either Global or US cheapness. These are code-level causes of the
  CTSH/TCS/ACN and Buzzi promotion errors, not merely wording problems.
- `FINALISTS` is a manually hard-coded list with narrative theses; the script only looks up metrics afterward.
  Thus `reproduce` regenerates a preselected judgment list, not an algorithmically derived finalist portfolio.
- Region assignments change across universe files and often reflect exchange/list provenance rather than economic
  exposure: Tencent/China Mobile/HK banks/AIA, Korea, Singapore banks, Barrick/GOLD, and dual ADR/native lines are
  classified inconsistently. Region-relative percentiles and the claimed US/dev/EM balance are therefore unstable.
- `financials_universe.py` places developed Singapore banks and some HK/global financials into EM peers, while the
  generic universe can place China-exposed HK firms into developed ex-US. This directly distorts peer scoring.
- Universe selection is hand-curated and index-heavy, with duplicated issuers and no permanent issuer identifier;
  it cannot support claims about the global opportunity set or small-cap absence. `None qualified` only means no
  small caps were included.
- CNOOC documents contain conflicting sanctions/divestment dates (2021-11-11 versus 2022-06-03) and opposite
  practical verdicts based on unconfirmed personal facts. Current primary law/list status must be reconstructed;
  no trade should rely on these files as written.
- CNOOC's company-defined `main/all-in cost per boe` includes DD&A but is not an economic breakeven or a cash
  production cost. Subtracting it from realized crude price and calling the difference a `$40/boe cash margin`
  ignores gas mix, royalties/taxes, exploration, sustaining/development capital, and differing volume bases.
- The stated 45% payout `floor` is a management policy/commitment, not shown to be a legally enforceable contract.
  Dividend capacity remains cyclical and subject to board/state action, law, capital needs, FX, and minority-
  shareholder governance. Calling it contractual overstates downside protection.
- CNOOC cash-flow figures need reconciliation: FY2025 operating cash flow RMB209.0B less stated capex RMB120.5B
  equals RMB88.5B, not the reported RMB97.4B FCF. Capex definition, acquisitions, accruals, and company non-GAAP
  adjustments must be bridged before testing dividend coverage.
- Dividend history is internally inconsistent across CNOOC files: FY2021/FY2022 special-dividend timing and whether
  HK$1.45 includes or excludes HK$1.18 are described differently. Per-share distributions and withholding must be
  rebuilt from HKEX declarations.
- `Net cash ~$25B` is still taken from yfinance and marked approximate; low gearing is not the same as net cash.
  Cash restrictions, lease liabilities, decommissioning obligations, parent balances, and currency must be tied to
  the annual report before calling it the only net-cash peer.
- Related-party sales/purchases and state control are correctly surfaced, but their actual transfer-pricing terms,
  receivable risk, caps, and minority approvals need filings analysis. Parent dividend alignment does not eliminate
  directed capex, acquisition, national-security, or expropriation/subordination risk.
- China-life EV and VNB are management models, not hard asset values or contracted cash that can be accepted at
  face value. Investment return, risk discount, lapse, mortality, expense, option/guarantee, tax, and capital
  assumptions require a common-basis sensitivity. EV/VNB growth under changed/restated assumptions does not by
  itself prove a franchise is unbroken.
- Taiping's P/EV must use embedded value attributable to the listed company's owners; dividing its market cap by
  total group EV including minority interests is invalid. The memo notes a higher owners'-EV ratio but headlines
  the lower ~0.29x figure. Peer EV bases may also differ, weakening the comparison.
- Comparing a 4.5% long-run portfolio-return assumption directly with the current 10-year government yield is an
  incomplete stress test: existing asset duration, credit/equity/property mix, new-money yields, liability cash
  flows, guarantees, participating features, and discount rate all matter. The negative-spread risk is real, but
  its magnitude was not modeled.
- Regulatory solvency of 2-4x a minimum is repeatedly called `fortress`; regulatory ratios are not linear multiples
  of economic loss capacity, and domestic ratings/concentrations may not map to global credit quality. State
  recapitalization can be support, evidence of need, or dilution/subordination—not automatically a catalyst.
- CPIC's `normalized` 16-18% ROE is based on a short, market-sensitive period rather than a through-cycle bridge.
  VNB acceleration partly reflects repricing/assumption changes and can coexist with weak volumes. The `BUY 7.2`
  conclusion therefore remains conditional on an independent ALM/EV sensitivity and filings tie-out.
- Claims that CPIC/Taiping are `freely` or `cleanly` US-investable are point-in-time legal conclusions and should be
  limited to `not found on checked lists`; broker, physical-location, sanctions changes, market access, and legal
  advice still apply. The project explicitly notes a TN visa and expected green card, which makes personal-status
  assumptions especially important for any sanctioned name.
- Broker-access research is perishable and must be rechecked. Choosing PUK/MFC/SLF for access does not validate
  valuation; PUK still has material China/HK operational risk despite UK domicile. A TSX CAD listing removes a
  currency-conversion step, not underlying business FX exposure.
- China/HK dividends, ADR/GDR fees, withholding, registered-account qualification, and Canadian/US tax residence
  were not integrated. Those can materially alter comparisons for this investor.
- All three INTU files are now fully read. The later `buy_diligence.md` correctly retracts the original
  `$560-800` DCF framing and recognizes SBC as a real owner cost, but its replacement BUY case remains
  too confident for the evidence:
  - The documents mix GAAP trailing P/E, non-GAAP forward EPS/multiples, gross FCF, and SBC-adjusted
    `owner FCF` as though they converge. Non-GAAP EPS excludes large SBC and acquisition amortization;
    it is not an independent confirmation of a DCF that subtracts SBC.
  - The stated TTM FCF anchor (~$6.8B) is not transparently bridged from the seasonal quarterly cash-flow
    statements. Intuit's nine-month period contains the tax-season cash peak; the files warn not to
    annualize a quarter but then lean on nine-month OCF to support the TTM narrative.
    Primary-source reconstruction gives TTM OCF of about $7.888B (`FY25 $6.207B + 9m FY26 $7.507B -
    9m FY25 $5.826B`). After filed property/equipment and internal-software capex classifications, gross
    TTM FCF is roughly $7.7B, not $6.8B. TTM SBC is about $2.039B (`FY25 $1.968B + $1.549B - $1.478B`).
    This raises the raw anchor but does not validate it: 9m FY26 OCF includes a $1.150B deferred-tax addback
    versus a $278M subtraction in 9m FY25, so normalized cash taxes and working capital need a bridge.
  - The DCF has a method mismatch: `OCF - capex` is levered cash flow after interest (FCFE-like), but the
    model discounts it at WACC and then subtracts net debt, an enterprise-value/FCFF procedure. It must
    either build unlevered FCFF and use WACC/subtract debt, or use normalized FCFE and cost of equity
    without subtracting debt.
  - The DCF `bear` assumes positive 2% five-year growth and a 3.5% perpetual growth rate with a 9% WACC.
    That is not a genuine structural-AI bear case. A higher discount rate, negative transition growth,
    lower terminal growth/margin, continuing dilution, or impaired QuickBooks economics can produce
    materially more downside than the claimed `-10% to flat`. Reperforming the memo's simplified DCF on
    its own $5B owner-FCF anchor gives about $317/share for its `bear` assumptions, but ~$205 at 0% five-
    year growth / 2.5% terminal growth / 10.5% discount rate and ~$148 at -5% / 2% / 11%. The memo's base
    case derives about 78% of enterprise value from the terminal value, so its apparent downside floor is
    mostly an assumption, not observed protection.
  - The claimed DCF/multiple `convergence` is partly circular: both capitalize management-adjusted
    earnings/FCF under optimistic durability assumptions. Historical 57-70x bubble-era P/E is not a
    sensible valuation anchor or evidence that a 20x re-rating is conservative.
  - `Trap tail confined to ~25% (TurboTax)` contradicts the thesis itself: the AI risk explicitly applies
    to QuickBooks/bookkeeping as well, while the new Consumer reporting segment also includes Credit Karma
    and ProTax. Segment revenue share does not cap enterprise-value downside when a common platform multiple,
    pricing power, retention, and cross-sell are at issue.
  - The claimed ~7.7% `shareholder yield` uses gross repurchases, not net buybacks. With about $2B/year of
    SBC, much of the buyback offsets employee issuance; share-count change and actual net repurchases are
    the relevant owner return. Buybacks are not evidence of intrinsic value or management credibility by
    themselves and can add leverage. The filed nine-month equity roll-forward shows 6.559M shares retired
    but 1.698M issued under employee plans, for a net 4.861M reduction from 279.129M (~1.74% over nine months),
    far below the memo's 5.9% gross `buyback yield`; $3.6B of unrecognized equity compensation also remained.
  - Plaintiff-law-firm investigation solicitations are not filed securities cases or medium-severity
    fundamental evidence. They should be monitored separately from operating diligence.
  - Subsequent primary filings add a material normalization issue: on 2026-05-20 Intuit announced a roughly
    **17% full-time workforce reduction** and estimated $300-$340M of restructuring charges, largely in fiscal Q4.
    It then issued $750M of 4.95% notes due 2031 and $1.0B of 5.50% notes due 2036 in June. FY2026 actuals must
    separate the temporary restructuring charge from recurring savings, reconcile cash use/net debt, and show
    whether repurchases after employee issuance still represent meaningful net owner yield.
  - Broker availability, treaty withholding, RRSP/TFSA treatment, and the user's tax residency/status are
    current personal facts, not established by the listing or Canadian citizenship. The practical account
    advice needs broker/tax confirmation before use.
  - Preliminary verdict: INTU may still be a valid watchlist/starter-position candidate, but the files do
    not establish the asymmetric `bear roughly flat / base +45% / bull +90%` payoff. The correct verdict is
    `conditionally attractive; revise valuation and wait for/verify FY2026 results`, not high-conviction BUY.
    Intuit's official calendar schedules FY2026 results for 2026-08-25 at 4:30 p.m. EDT; as of this audit
    batch the IR results page still stopped at Q3, so the decision is immediately event-stale and should not
    be acted on before the release is incorporated.
- `deep_dives/managed_care/comparison.md` is fully read. Its high-level preference for CI over ELV/UNH may
  be directionally reasonable, but the analysis does not support a 7.3/10 BUY decision:
  - The scorecard arithmetic is deliberately overridden: CI calculates to 7.40 then is called 7.3; ELV
    calculates to 6.15 then is `rounded up` to 6.6; UNH calculates to 5.95 then is raised to 6.2. These are
    not rounding differences and make the nominal framework non-reproducible.
  - Forward P/E is sourced from yfinance/analyst estimates and compared with GAAP trailing results without
    an adjusted-to-GAAP bridge. For payers, reserve development, divestitures, acquisition/cyber/restructuring
    charges, risk-corridor items, and claims timing can materially change normalized EPS. No reverse DCF,
    normalized EPS bridge, or downside valuation is provided for CI.
  - The file acknowledges that payer FCF is distorted by float/claims timing, then uses CI's ~9% screen FCF
    yield as a primary cheapness/quality proof. Revenue and margins are also not economically comparable
    across insurance and PBM pass-through businesses without gross-to-net and segment-capital analysis.
  - CI's Medicare divestiture and services-heavy mix reduce direct medical-cost exposure but do not make it
    low risk. Express Scripts/PBM regulation, rebate/spread-pricing reform, litigation, customer concentration/
    retention, specialty-drug economics, debt and sale-proceeds-funded buybacks require equal billing. The
    monitoring list is misaligned: it leads with UNH's DOJ probe even though CI is the recommended purchase;
    CI-specific PBM economics/regulatory milestones should be first.
  - UNH's raw GAAP net-income decline is treated as an operating/MA-cost collapse without a bridge for major
    one-offs and discontinued operations; its dividend payout and historical multiple comparisons inherit
    that distortion. Cross-company MLRs are mix- and definition-dependent and Q1 is seasonal, so the table
    cannot establish relative quality on its own.
  - `Cheapest`, `least exposed`, and `clean way to own the sector` do not establish margin of safety. CI's
    transition to a new CEO, regulatory regime, PBM contract economics, and a severe policy/rebate scenario
    must be modeled before BUY. Preliminary verdict: `CI preferred watchlist candidate; decision incomplete`,
    ELV `watch/recovery speculation`, UNH `avoid/watch pending legal and normalized-earnings work`.
- All CTSH authored files and its stored SEC JSON evidence are fully read/validated (both JSON files parse).
  The later profile corrects several errors in the earlier deep dive, but the WATCH→BUY tilt remains premature:
  - The deep dive says FY2025 capital return was ~10% of current market cap and implies buybacks cap downside;
    the profile admits actual float shrink averaged only ~2.5%/year since 2018 and the earlier ~10%/year claim
    was wrong. Yet the profile/table then reports a 2.4% `buyback yield` while $1.378B of gross FY2025 repurchases
    divided by the stated $19.7B current cap is ~7.0%. Gross historic dollars/current depressed cap, net share
    retirement, and forward yield are being conflated.
  - FY2025 FCF of $2.595B is real, and stored SEC facts show SBC was a relatively modest $181M, but the memo
    selects the strongest FCF year since 2020 without normalizing. Six-year average FCF is about $2.30B, and
    acquisitions are excluded despite $1.615B spent in 2024 (including Belcan/Thirdera effects on subsequent
    growth). A durable growth/maintenance-acquisition allowance and working-capital bridge are needed.
  - Q1 FY2026 reported revenue +5.8% is emphasized as proof fundamentals contradict the AI bear, while the
    profile shows organic constant-currency growth was only +3.9%, down from +8.2% a year earlier; largest
    segment Health Sciences fell 0.9%. TTM bookings +11% / quarterly bookings +21% are TCV, not guaranteed
    revenue or margin, and do not resolve pricing/productivity deflation.
  - The bear valuation is not modeled. If EBITDA/FCF shrinks, holding the multiple at 5x lowers equity value;
    a ~$0.98B net-cash position (~5% of stated market cap) and buybacks do not cap downside to dead money.
    No downside DCF, contract repricing/runoff, margin sensitivity, or client-concentration analysis exists.
  - P/B is not a meaningful cross-peer quality measure for an acquisitive services firm: stored SEC facts show
    $7.106B goodwill (~47% of Q1 equity), and buybacks alter book equity. ROIC methodology is point-in-time and
    should be reconciled to acquisition capital and average operating assets.
  - The profile itself says the recommendation needs another print, client concentration, and current H-1B
    legal status. Because Q2 FY2026 should now be available, the July thesis is event-stale. Preliminary verdict:
    `genuinely cheap but unresolved structural risk; WATCH pending current results and normalized downside model`,
    not BUY-worth-more-work based on a claimed protected downside.
  - Current primary-source check materially weakens the thesis: Cognizant's 2026-07-29 Q2 release reported
    quarterly bookings **down 6%**, TTM bookings growth slowing from Q1's 11% to **5%**, and narrowed FY2026
    constant-currency revenue guidance from 4.0-6.5% to **4.0-5.5%**. Adjusted margin guidance was unchanged;
    the EPS range rose, so EPS does not substitute for the weakening demand indicator.
  - Q2 reported revenue grew 4.5% / 4.1% constant currency, but Cognizant says recent acquisitions contributed
    ~100 bps and third-party product resale ~170 bps to total growth. An inference excluding both leaves only
    roughly 1.4 percentage points of constant-currency growth from the remaining mix; resale may be strategically
    valid but has different margin/quality from labor services. This no longer supports the memo's `fundamentals
    contradict the AI bear` wording.
  - H1 FCF fell to $657M from $724M. Cognizant spent $1.6B on repurchases and $1.3B on acquisitions in H1,
    acquired Astreya for $634M in Q2, and borrowed $1.0B on its revolver. The Q1 net-cash snapshot and buyback
    `cushion` are therefore obsolete; capital returns exceeded internally generated cash and added financial
    risk. Updated verdict: **do not promote to BUY**. Retain only as a cheap WATCH pending a Q2 balance-sheet/
    acquisition bridge, normalized FCF, and evidence bookings/core organic growth stabilize.
- `deep_dives/TCS_NS/deep_dive.md` is fully read. Its WATCH conclusion is directionally more disciplined
  than the CTSH recommendation, but several decision claims need revision:
  - TCS is `cheap versus its own history`, not demonstrably cheap in absolute terms or versus peers. A prior
    27-30x median from the zero-rate/premium-growth era is not an intrinsic-value anchor after constant-currency
    revenue contraction. No DCF/reverse DCF or normalized owner-earnings downside is provided.
  - P/B is economically weak for human-capital services businesses and cannot establish `balance-sheet margin
    of safety`; conversely, TCS at ~7x book does not by itself mean zero downside cushion. CTSH's ~1.3x book is
    also distorted by goodwill/buybacks. Net cash at TCS is only a small share of market value.
  - The advertised ~5.3% yield includes a ₹46 special dividend; ordinary FY2026 dividends of ₹64 imply ~3.1%
    at the memo price. A 99% payout is not automatically quality: it limits reinvestment and needs analysis of
    sustainable FCF, withholding/tax, Tata Sons' cash needs, and minority-holder capital allocation.
  - Tata Sons controls ~72%, but parent/related-party governance, minority rights, dividends, succession,
    group transactions and any pledges/regulatory issues are barely analyzed. These matter alongside the Tata
    brand benefit.
  - There is no sponsored ADR. Direct NSE/BSE access, foreign-investor/account rules, broker availability,
    INR conversion, Indian withholding/capital-gains/treaty treatment and custody are not resolved, so the name
    is not yet an actionable candidate for this Canadian/US-connected investor.
  - The US `reciprocal tariff` is not shown to tax exported IT services directly; it is at most a macro/client-
    demand risk absent a legal mechanism. The $100k H-1B fee and current court status remain explicitly unverified.
  - Preliminary verdict: WATCH is reasonable, but `quality at fair price` and CTSH>TCS cannot be finalized until
    current TCS results, access/tax, normalized FCF, controlling-shareholder risk, and the same structural downside
    scenario are evaluated.
  - Current official Q1 FY2027 (2026-07-09) only partially confirms an inflection: total revenue grew 3.2%
    YoY constant currency and 0.4% QoQ, with $9.5B TCV and AI revenue annualizing at $2.6B. That is positive
    versus FY2026 contraction but still below the memo's mid-single-digit upgrade trigger; operating margin
    fell to 24.0% (excluding an exceptional item) and consumer/UK/major non-India markets were mixed. WATCH
    remains appropriate, not BUY.
  - The memo's `first-ever full-year reported revenue decline` needs currency qualification. TCS's annual
    report says FY2026 revenue grew 4.6% in reported INR; the decline is in USD (-~0.5%) and constant currency
    (-2.4%). For an INR-listed investor both operating currency mix and INR translation matter.
- `deep_dives/info_services/comparison.md` is fully read. It correctly admits the sector screen's cheap
  `Information Services` average does not apply to SPGI/MCO/MSCI, reinforcing the earlier finding that the
  screen fatally mapped two different industries (CTSH/TCS labor services versus ratings/index/data). But its
  #1 SPGI recommendation is not yet supported:
  - SPGI at ~28x trailing earnings / 18.3x EV-EBITDA / 4.2% FCF yield is `less expensive than a very expensive
    history`, not a demonstrated margin-of-safety purchase. No DCF/reverse DCF, required growth, recessionary
    issuance case, or MI retention/pricing downside is modeled. A prior ~40x five-year P/E is not fair value.
  - The memo repeatedly says `two-thirds` of SPGI is ratings/index protected, but its own segment table lists
    Ratings at 30% and Indices at 12%—only ~42%. Market Intelligence (32%), Commodity Insights, Mobility and
    other data products have differing AI, cyclicality and competition risks; the protected-share claim is
    arithmetically unsupported.
  - Goodwill is not merely an accounting distortion to remove from ROIC. SPGI's ~$45B IHS Markit goodwill
    represents real acquisition consideration paid; economic returns must test the combined purchase price,
    synergies and impairment risk. `Ex-goodwill high returns` can overstate acquisition economics.
  - MCO/MSCI high or meaningless ROE/ROIC after aggressive buybacks/negative equity requires leverage, interest,
    debt-maturity and net-buyback analysis. Gross FCF conversion and gross capital-return/current-cap ratios do
    not by themselves establish quality or shareholder yield.
  - Ratings have a powerful regulatory/reputation moat, but issuer-pays conflicts, enforcement/litigation,
    model error, cyclic issuance and regulatory reform are underdeveloped. MSCI also carries index-client/
    BlackRock concentration and equity-market/AUM beta; a long license term does not eliminate renegotiation or
    concentration economics.
  - Scores 7.30/7.20/7.15 imply precision far beyond the subjective inputs and valuation uncertainty; the rank
  is not robust. Preliminary verdict: SPGI/MCO/MSCI are quality watchlist names, with SPGI the relatively
  cheapest, but none is a verified value BUY on this work. Current Q2 FY2026 results must replace Q1 inputs.
- The SPGI/MCO/MSCI comparison has now been updated through official Q2/H1 FY2026 releases and SEC filings. The
  franchises all performed strongly, but the corrected verdict remains **WATCH for all three; SPGI is the least
  demanding on current forward earnings, not a demonstrated bargain**:
  - SPGI completed the 1-for-1 Mobility Global spin on 2026-07-01. Q2 continuing-business pro-forma revenue rose
    11% to $3.678B, adjusted operating margin rose 200bp to 54.3%, and adjusted EPS rose 23% to $4.83. FY2026
    post-spin guidance is 5.9-7.9% revenue growth, 6-8% organic constant-currency growth and **$17.50-$17.75
    adjusted EPS**. At the roughly $434.46 2026-08-24 close, that is about **24.6x** guidance, a ~4.1% adjusted
    earnings yield before leverage, stock compensation and conversion differences. This is more reasonable than
    the old snapshot but not an independently established margin of safety.
  - The old SPGI history/segment mix is no longer directly usable. Holders on the record date received one MBGL
    share per SPGI share, while a new buyer gets only the four continuing segments; beginning Q3, Mobility history
    will be discontinued operations and product/cost allocations also changed. Any claim that price fell or the
    multiple compressed must add the distributed MBGL value for legacy-holder return and use the recast SPGI
    statements for a new investment. The memo's old `two-thirds protected` claim is still invalid.
  - SPGI's continuing segment mix did improve in the desired direction—Ratings and Indices posted record results—
    but Market Intelligence adjusted/recast revenue was only +6% and the company is reorganizing MI/Energy. More
    than $7B of planned 2026 buybacks can increase per-share value if executed below intrinsic value, but it is not
    organic growth; post-spin cash, the approximately $13.1B fair value of debt remaining after Mobility's $2B
    notes transfer, acquisition/divestiture cash and repurchase prices must be reconciled first.
  - Moody's Q2 revenue rose 15% to $2.185B, adjusted margin expanded 440bp to 55.3%, and adjusted EPS rose 31% to
    $4.68. The split shows cyclicality rather than uniformly recurring growth: MIS revenue rose 25%, transaction
    revenue 34% and MIS margin reached 68.3%, while MA reported revenue rose only 4% (8% organic constant currency),
    albeit with 99% recurring revenue and ARR +9%. This is an issuance-boom quarter layered on a sound subscription
    franchise, not a new normalized base.
  - Moody's retained only high-single-digit FY revenue guidance and narrowed adjusted EPS to **$16.50-$17.00**;
    it actually reduced FCF guidance to $2.7-$2.9B while raising buybacks to up to $3B. At roughly $511.35 on
    2026-08-24, the stock trades around **30.5x** midpoint adjusted EPS and the $88.6B market value implies only
    about a 3.0-3.3% guided FCF yield before net debt. The strongest reported growth therefore has the richest
    earnings valuation and meaningful capital-market normalization risk.
  - MSCI Q2 revenue rose 12.2% organically, adjusted EPS rose 18.5% to $4.94, and retention was 95.3%. Index revenue
    rose 17.5%, with asset-based fees +26.6% and Index run rate +17.4%, directly demonstrating equity-market/AUM
    beta alongside the moat. Analytics revenue rose only 6.6% while adjusted EBITDA fell 5% and margin contracted
    from 52.1% to 46.5%; Sustainability and Climate revenue rose 3.4% and its run rate only 1.9%. Growth quality is
    mixed below the core Index engine.
  - MSCI guides FY2026 FCF to $1.485-$1.545B. Against an approximately $43.7B market value near $566-571/share,
    that is only ~3.4-3.5% before debt; principal debt was $6.4B and total debt/adjusted EBITDA 3.1x, within the
    company's 3.0-3.5x target but not conservative. H1 adjusted EPS was $9.49, so a simple ~$19 annualization also
    puts the stock near 30x. The 5.9% YoY diluted-share reduction amplifies EPS but is financed alongside leverage,
    dividends and acquisitions; it is not free growth.
  - Corrected comparative decision: **SPGI WATCH, currently the relative valuation leader; MCO WATCH; MSCI WATCH.**
    SPGI's ~24.6x guided adjusted earnings is less demanding than MCO/MSCI near 30x, and its Q2 execution is strong,
    but the spin/recast, debt, buyback funding and cyclic Ratings contribution require a fresh continuing-business
    DCF/reverse DCF. MCO needs an issuance-normalized case; MSCI needs an equity-market drawdown, leverage and weak-
    segment case. None is protected 3-5 year house capital, and the prior 7.30/7.20/7.15 ranking remains spurious.
- The CTSH-vs-TCS choice has now been reconciled against current official results and balance-sheet data.
  The project's **CTSH > TCS deep-value BUY tilt is invalid**, although this does not automatically make TCS
  a buy:
  - At 2026-06-30 CTSH had $1.051B cash plus short-term investments against $1.560B short- and long-term debt,
    or about **$509M net debt**. This directly overturns the memo's net-cash/downside-cushion premise. Cash fell
    $863M from year-end while debt rose $984M; H1 repurchases ($1.607B) plus acquisitions ($1.334B) greatly
    exceeded H1 FCF ($657M). The cheap multiple now comes with acquisition integration, goodwill and leverage
    risk rather than excess-cash optionality.
  - The supposedly protected bear case was not a downside model. Using the memo's $41.66 price/~$19.7B market
    cap and a deliberately simple normalized-FCF sensitivity, a 20% decline from a $2.3B normalized FCF base
    valued at 8x implies about $14.7B equity value (~25% downside); at 6x it implies ~$11.0B (~44% downside).
    A 40% decline at 6x implies ~$8.3B (~58% downside). These are sensitivities, not price targets, but disprove
    the claim that a 5x headline EBITDA multiple limits the outcome to `dead money + yield`.
  - TCS's official Q1 FY2027 table confirms +3.2% YoY / +0.4% QoQ constant-currency growth, $9.5B TCV,
    24.0% adjusted operating margin and $1.31B operating cash flow. A contradictory -2.4% figure currently
    shown on the investor-relations landing-page summary appears to describe FY2026 rather than Q1 FY2027;
    the dated quarter release and its segment/geography table are the decision source.
  - TCS entered FY2027 without conventional borrowings in the FY2026 audited balance sheet and with substantial
    cash/current investments, so it currently has the stronger financial-risk profile and operating margin.
    It still has valuation, controlling-shareholder, investability/tax and AI/labor-deflation risks, and +3.2%
    CC growth is below the memo's own mid-single-digit upgrade trigger.
  - **Corrected decision:** neither name is a verified BUY. TCS is the higher-quality WATCH; CTSH is a leveraged,
    acquisition-dependent cheap WATCH that requires bookings/core organic stabilization and an FCF-funded capital-
    allocation reset. The evidence no longer supports ranking CTSH ahead of TCS on risk-adjusted downside.
- `deep_dives/NEM/deep_dive.md` is fully read. Its final WATCH decision is **sound**, but important supporting
  reasoning and numerical claims must be revised:
  - The memo correctly identifies the low-multiple-on-peak-commodity-earnings trap, the balance-sheet repair,
    2024 execution scar, by-product/co-product cost distinction, dividend cut and jurisdiction risks. This is
    materially better calibrated than the screen's #2 rank and supports WATCH rather than BUY.
  - The stated `normalized $3,000-$3,500 gold` earnings of roughly FY2025's $7B are not modeled and are almost
    certainly far too high. FY2025 itself realized $3,498/oz and adjusted earnings were $7.634B; Newmont's current
    sensitivity says each $100/oz move changes revenue/cost by about $505M pretax, before an additional ~$6/oz
    royalty/tax/worker-participation effect. Relative to the company's $4,500 guidance assumption, $3,500 implies
    roughly a **$4.75B pretax** reduction after the stated royalty effect and $3,000 roughly **$7.13B**. A proper
    mine-by-mine tax/cost/volume model is still required, but the memo's normalization cannot be used.
  - The $2,000 reserve price is an economic-assumption/cutoff input, not a floor under the share price, margin or
    reserve quantity. Lower prices, higher costs or project changes can remove ounces from reserves and create
    impairments; reserve life is not a contractual 20-year cash stream.
  - Realized price minus by-product AISC is not `cash margin`: AISC is non-GAAP, includes/excludes specified
    sustaining items, and by-product accounting credits volatile copper/silver/zinc revenue. Development capital,
    taxes, working capital, reclamation and acquisitions also matter. Cross-peer comparisons must use consistent
    by-product/co-product bases.
  - P/NAV figures dated 2025 and aggregated analyst price targets do not verify July 2026 value. The subjective
    `60% cyclical / 40% real value` split and 5.78 score have no reproducible basis and should be removed from
    decision weight.
  - Current official Q2 2026 supports operational execution but also shows the commodity sensitivity in real time:
    realized gold fell from $4,900 to $4,414, adjusted net income from $3.156B to $2.2B, and FCF from $3.144B to
    $2.2B. Production stayed near 1.3Moz, Q2 by-product AISC rose to $1,621, full-year 5.26Moz/$1,680 guidance was
    maintained, and quarter-end net cash was $3.4B. H1 repurchases were $3.462B, creating material timing risk
    if executed near cycle/stock highs.
  - Corrected framing: **WATCH / tactically attractive only as explicit high-volatility gold equity exposure**,
    not safe capital or a substitute for bullion. Given this portfolio already has physical gold/miner exposure
    and a 3-5 year house objective, any NEM position must be small, funded from the risk bucket, and assessed for
    total gold-factor concentration. Do not count net cash or reserves as house-fund downside protection.
- `deep_dives/TROW/deep_dive.md` is fully read. The WATCH conclusion is **conditionally sound**, but the thesis
  overstates retirement stickiness and omits the most important product-quality evidence:
  - About two-thirds of AUM is **retirement-related** per the company; only ~$622-623B, roughly one-third of
    $1.89T, is specifically target-date. `Retirement-related`, `target-date`, and `sticky` are not synonyms:
    participants can roll assets out, plan sponsors can replace managers, and retirement portfolios overlap the
    asset-class totals. The memo's repeated `2/3 sticky retirement/target-date` shorthand is misleading.
  - Equity/fixed-income/multi-asset are asset classes, while mutual fund/ETF/CIT/SMA/subadvisory are wrappers or
    channels. Calling all $919B equity AUM the active-equity-mutual-fund problem is not supported by that table.
    Flow analysis must be by both strategy and vehicle/channel, net of mandate wins and manager distributions.
  - The memo scarcely tests investment performance, the causal bridge to future flows. At 2026-06-30 only 47%,
    44%, 40% and 48% of US funds beat passive-peer medians over 1/3/5/10 years; only 43%, 43%, 35% and 53% of
    composites beat benchmarks. Equity composite results were weaker (31/29/24/43%). Stronger fixed income is
    a real offset, but the broad performance record does not establish a moat.
  - Current Q2 shows improvement but not an inflection: firmwide net outflows narrowed to $6.5B from $13.7B in
    Q1, with May and June positive, yet H1 outflows were $20.2B. Q2 equity outflows were $13.5B, offset by fixed-
    income +$4.6B, multi-asset +$0.4B and alternatives +$2.0B. Market appreciation of $190.2B—not organic growth—
    drove the quarter-end AUM record.
  - Fee compression continued: Q2 average AUM rose 15.7% YoY and advisory fees 11.3%, while the effective rate
    fell from 39.6 to 38.1 bps. Adjusted EPS rose to $2.57 from $2.24 and adjusted expense growth was held to
    4.9%; this confirms resilient current economics, not terminal organic stability. GAAP EPS $2.88 included
    market-sensitive investment gains, so use adjusted/core results for valuation.
  - Analyst ratings/targets, high short interest, Dividend-Aristocrat status and an old Morningstar fair value are
    sentiment/context, not independent valuation evidence. The suggested `$85-95 buy zone` has no DCF, earnings-
    sensitivity or required-return derivation. Peer P/E/PB tables are also not comparable without adjusting for
    BLK/BEN/IVZ business mix, acquisitions, leverage and investment gains.
  - On 2026-08-20 TROW agreed to buy $19B-AUM fixed-income ETF/SMA manager F/m Investments, more than doubling
    fixed-income ETF AUM, but price/financial terms were undisclosed. It fits the strategic response yet cannot be
    scored as value-creating until purchase price, retention, fee rate, organic flows and integration economics
    are disclosed.
  - Corrected decision: **WATCH**, not buy-on-yield. Upgrade only after sustained firmwide organic neutrality,
    better equity relative performance, stabilization of effective fees and a valuation that survives a market-
    drawdown/AUM sensitivity. It is an equity/market-beta asset and unsuitable for protected 3-5 year house funds.
- Both `deep_dives/NTES/deep_dive.md` and `deep_dives/NTES/profile_and_diligence.md` are fully read. The currency-
  artifact diagnosis is valuable and correct, but the `WATCH leaning BUY-worth-more-work` decision must be
  **revised to WATCH only** until cash accessibility, owner earnings and governance are normalized:
  - Correct: yfinance mixed USD market value with RMB statement fields, corrupting the raw 6.4x EV/EBITDA,
    17x P/B and ~41% FCF-yield. Rebuilding in one currency is mandatory. The filed 45.5% Ding ownership, 85.2%
    VIE revenue share, one-ADS-to-five-shares ratio and core FY2025 segment numbers tie to primary filings.
  - The revised `ex-net-cash P/E` is still internally inconsistent. It subtracts essentially all consolidated cash,
    time deposits, restricted cash and short-term investments from value while leaving interest/investment income
    earned by those assets in net income. A valid operating multiple must subtract only genuinely excess,
    attributable/distributable cash and also remove its after-tax earnings from the denominator.
  - Consolidated net cash is not equivalent to cash immediately available to Cayman/ADS holders. The 20-F says
    NetEase does not have direct access to subsidiary/VIE cash or future earnings; subsidiaries/VIEs held RMB142.6B
    of cash/time deposits at FY2025. Transfers face retained-earnings, reserve, tax, foreign-exchange and approval
    limits. RMB13.3B of net assets was explicitly restricted, and the filing's illustration shows a standard maximum-
    tax path may deliver only 67.5% of pre-tax PRC earnings to the parent/shareholders (or worse if service-fee tax
    treatment fails). This does not make all cash stranded, but it invalidates a 100-cent subtraction.
  - Net cash also includes restricted cash and assets in majority-owned separately listed subsidiaries, while the
    group has noncontrolling interests. A sum-of-parts/attributable-cash bridge is required. Likewise, financing cash
    flow combines repurchases of NetEase ADSs with purchases of subsidiaries' shares; not every reported purchase
    reduces NTES's own share count. `Through-cycle shareholder yield` must use actual NTES ADS shrink plus dividends.
  - Founder ownership is dual-edged, not unqualified alignment. Ding has 45.5% voting/economic control and is also
    a registered owner/counterparty in material VIE agreements. One-share-one-vote avoids dual-class leverage but
    does not remove entrenchment, related-party, succession or minority-rights risk. The board/conflict controls and
    historical related-party transactions need an explicit review before scoring governance as a positive.
  - The `2/3 China discount / 1/3 genuine value`, 6.9 score and claim that a US-equivalent would plausibly trade at
    twice the multiple are unsupported judgments. Western peer P/E/margin comparisons ignore different development-
    cost accounting, platform mix, game lifecycle, taxes, growth and control structures. Tencent at a similar forward
    P/E and faster growth is an especially important counterexample to the claim of unique NTES cheapness.
  - CSRC filing rules acknowledge/regularize overseas listings but do not `bless` VIE enforceability or guarantee no
    future restriction. Normal license issuance and the withdrawn 2023 draft reduce current regulatory pressure but
    do not turn policy risk into a catalyst. Holding 9999.HK mitigates ADR/depositary/delisting mechanics only; it
    does not mitigate the Cayman/VIE, PRC regulation, capital-control or underlying China equity risk.
  - Current official Q2 2026 confirms excellent core operations: revenue +7.9% YoY, games +9.7%, gross profit +17.5%,
    ~70.5% consolidated gross margin and ~40.2% operating margin. But headline economics are more volatile than the
    memo presents: Q2 shareholder net income fell to RMB7.0B from RMB8.6B YoY and RMB10.7B QoQ because of a RMB2.95B
    investment loss/impairments and a 25.5% effective tax rate; H1 net income fell to RMB17.7B from RMB18.9B despite
    revenue growth. Q2 operating cash fell to RMB10.0B from RMB13.7B QoQ and RMB10.9B YoY. Net cash stayed RMB167.5B,
    but loans doubled from RMB6.4B at year-end to RMB12.6B while short-term investments rose sharply.
  - Corrected decision: **quality China-games WATCH**, not yet a BUY. Rebuild value with attributable/distributable
    cash, cash-earnings removal, normalized tax/investment results, actual share-count change and a game-by-game
    concentration/pipeline scenario. Any eventual position belongs in a small speculative/geopolitical-risk bucket,
    aggregated with all other China exposure, never in protected 3-5 year house capital.
- All three Buzzi files—`deep_dives/BZU_MI/deep_dive.md`, `profile_and_diligence.md`, and
  `buy_diligence.md`—are fully read. Buzzi remains genuinely inexpensive and financially resilient, but the specific
  `BUY at ~€46` conclusion is **not adequately modeled and should be revised to conditional WATCH/starter-only**:
  - The country recurring-EBITDA table is arithmetically unreconciled: listed regions total roughly €1.335B versus
    €1.234B group recurring EBITDA, so the stated shares total ~108%, not 100%. Mexico is equity-method while other
    regions are consolidated, and central/elimination costs appear omitted. `US = 47% of profit` may be directionally
    useful but is not a clean geographic profit allocation until the bridge is shown.
  - The normalized-margin model is not decision-grade. It applies a constant FY2025 net-income/EBITDA ratio to every
    margin scenario even though D&A, tax, equity-method Mexico earnings, FX and nonrecurring items do not scale with
    EBITDA. It also compares 1H margin with full-year margin and calls the difference normalization without controlling
    for construction seasonality. The conclusion that `two-thirds of the windfall was unwound` is unsupported.
  - Current official H1 2026 confirms that weakening continued: sales were flat (+0.1%, -1.1% like-for-like), recurring
    EBITDA fell 9.7% to €475M, recurring margin fell from ~24.1% to ~21.7%, and net profit fell 16.8% to €324M. Net cash
    remained strong at €896M but fell €214M from year-end. Full-year recurring-EBITDA guidance of €1.1-1.2B is below
    FY2025's €1.234B. Italy improved, but Russia EBITDA fell 56.5% and Russia net assets rose to €543M; the claim that
    the US/overall trough is already safely behind the company is not proven by the release.
  - The share price has also fallen from ~€46 in the memo to roughly €40 on 2026-08-25, partially offsetting the lower
    earnings. With ~€7.0B current market value, €896M net cash and €1.1-1.2B guidance, the headline EV/EBITDA remains
    low, but exact value still requires an audited segment/associate bridge, maintenance/decarbonization capex, pension/
    provisions, normalized tax and a volume-price-cost scenario—not a linear P/E shortcut.
  - The Mexico JV's market value above carrying value is not automatically `hidden value`; the listed stake's value is
    visible to the market and needs tax, liquidity/control-discount and already-recognized equity-income treatment in a
    sum-of-parts. Adding the gross difference to book or using it as independent upside double counts without a bridge.
  - The EU-ETS section applies spot carbon price times gross cement/clinker emissions as if it were an incremental cash
    cost. It omits Buzzi-specific verified emissions/free-allocation baseline, clinker substitution, carbon capture,
    pass-through, hedging, CBAM, production mix and decarbonization capex. The phase-out is a real risk; the €48-64/t
    `potentially comparable to product value` number is not a company earnings forecast.
  - The new €200M authorization is only ~2.5-3% of market value; it is conflated with cancellation of accumulated
    treasury shares (~7%). A cancellation is economically useful but does not prove the entire 7% was newly bought at
    the current price. Similarly, failure to uncover abuse in a limited filing review is not proof of an `exemplary`
    minority-holder record, especially with 69.2% voting control, 53.0% economics and 9/10 directors from the controller.
  - Buyability/tax analysis incorrectly treats citizenship as the deciding fact. Broker access, Italian transaction tax,
    withholding/treaty relief and account treatment depend on residence, tax domicile, account type and broker—not
    merely Canadian citizenship. IBKR Canada permission and the quoted tax rates were explicitly unverified, so the
    recommendation is not yet operationally actionable.
  - Corrected decision: **conditional WATCH / possible small starter from long-horizon risk capital**, not a house-fund
    holding and not an unconditional BUY. It can be upgraded if the segment math is reconciled, a seasonal multi-year
    owner-earnings/downside model remains attractive at the execution price, and residence-specific access/tax is
  confirmed. Net cash is real protection against insolvency, not against cyclical share-price drawdowns.
- All five EOG files—`deep_dives/EOG/deep_dive.md`, `profile_and_diligence.md`, `portfolio_fit.md`,
  `sleeve_analysis.md`, and `hooman_oil_gas_holdings.md`—are fully read. The high-level finding that EOG is a
  strong E&P and that adding it would increase an already-large energy factor is sound, but the `6.9/10`,
  `WATCH -> lean BUY` and preferred `OXY -> EOG` swap are **not validated as written**:
  - The central forward-P/E interpretation is mathematically backwards. At a fixed share price, a forward P/E
    below trailing P/E implies a **higher**, not lower, forward EPS denominator. The memo twice says 8.7x below
    12.8x means analysts expect earnings to fall; that is false and invalidates part of the peak-cycle narrative.
    Aggregator forward P/E also needs the exact estimate period/consensus EPS before it can carry decision weight.
  - The `$68 WTI / mid-cycle 6.5% FCF yield` framing is a dated point estimate, not a normalized valuation. EIA
    confirms WTI near $69-72 around 2026-07-02, but EOG's just-reported Q2 benchmark averaged **$92.85**, and EIA
    then shows roughly $80-93 through much of July and ~$84-86 in mid-August. The same quarter's windfall earnings
    therefore cannot be extrapolated as mid-cycle owner earnings. Conversely, one `$68` strip snapshot cannot
    establish a durable forward FCF denominator.
  - Official Q2 2026 confirms excellent execution and financial resilience: 1,410.4 MBoed total production,
    $2.724B GAAP/$2.683B adjusted net income, $4.386B adjusted CFO, $1.587B capex, $2.799B company-defined FCF,
    $3.019B net debt and $10.57/Boe cash operating cost. Full-year guidance remains ~$6.3-6.7B capex, 548.7 MBod
    oil/condensate and 1,400.7 MBoed total at midpoint. These data support quality, but the Q2 jump from Q1's
    $1.493B FCF was mainly the commodity-price change; EOG's own bridge attributes about $1.062B of revenue change
    to realizations. This is price leverage, not proof of a through-cycle moat or valuation floor.
  - H1 company-defined FCF was about **$4.292B**. Repurchases were roughly $1.714B and regular dividends roughly
    $1.08B, so the recurring claim that current FCF is `fully returned` is not established for H1 2026; `100%`
    describes FY2025, not a verified perpetual policy. The specific 70% framework floor and sub-$50 corporate
    breakeven remain unverified in the materials cited by the project and cannot support the score until sourced
    and defined consistently.
  - The Encino acquisition figures are reconcilable, not contradictory: approximately $4.47-4.48B was equity/cash
    consideration, while roughly $5.6-5.7B was total value inclusive of assumed/repaid Encino debt. The deep dive
    wrongly calls `$4.484B all-cash` the whole deal and later says net debt rose only modestly; in reality, EOG issued
    $3.5B of new notes and assumed/redeemed ~$1.2B of Encino notes. The balance sheet remains conservative, but the
    acquisition cost and post-deal returns need to be judged on total enterprise consideration.
  - Reserve replacement of 254% and 5.5 Bboe proved reserves do not by themselves prove `deepest inventory` or a
    moat. Acquisition additions, price revisions, drilling economics, decline rates and future capital required to
    convert undeveloped reserves must be separated. The peer table omits precisely the like-for-like inventory,
    cost, reserve-life and normalized-return evidence needed to call EOG unambiguously best-in-class.
  - Valuation comparisons use mixed, stale yfinance fields (trailing/forward periods, GAAP impairments, equity-
    method businesses and different commodity mixes) and analyst targets as a catalyst. EOG moved from $129.70 in
    the memo to about **$147.87 on 2026-08-25**, reducing the original entry margin materially. A fresh normalized
    price-deck model at `$50/$65/$80` oil plus gas/NGL cases is required; neither the old 5.8x EV/EBITDA nor a Q2
    run-rate answers today's value question.
  - The sleeve work is right that ~13.79% in oil/gas-related positions is already a major, correlated factor bet and
    that an ADD is not genuine diversification. However, three-year weekly correlations/betas are sample-dependent,
    mix equity beta, CAD/USD, leverage and market factors, and do not prove a stable hedge relationship. The memo
    also shifts between `~12%` and the complete 13.79% book; use the complete book and current weights.
  - The case for `OXY -> EOG` over-relies on a weighted-average ROE calculation. Portfolio-weighting company ROEs
    (which have different accounting bases and cycle points) does not measure portfolio quality or expected return,
    and leverage normally magnifies ROE rather than mechanically causing a low ROE. The claimed +1.1-point sleeve-
    quality improvement is arithmetic, not economic proof.
  - OXY facts are stale/inaccurate. As of Q2 2026, preferred stock carrying value was **$8.287B**, not $10B;
    OxyChem closed to Berkshire on 2026-01-02 for about $9.4B after adjustments, not merely `agreed`; and OXY had
    reduced principal debt to $11.8B. Its balance sheet still has materially more leverage than EOG (quarter-end
    debt less cash on the release tables is roughly $9.6B versus EOG's $3.0B net debt), plus ~$170M quarterly
    preferred dividends, but Q2 also delivered $3.021B FCF before working capital and $2.40 adjusted EPS at the
    same commodity spike. A swap requires normalized per-share FCF/asset-value scenarios for both names, not old
    ROE and aggregator P/E.
  - `UNG has no leverage decay` is misleading. It avoids BOIL's 2x daily-reset compounding, but both futures funds
    can suffer roll yield/contango, collateral and tracking drag; neither is equivalent to long-term spot-gas
    ownership. BOIL can be a short tactical instrument, but `structurally unsuitable beyond days-to-weeks` should
    be framed as path-dependent high risk rather than an absolute law.
  - Corrected decision: **EOG remains WATCH / highest-quality-candidate within this particular US-E&P comparison,
    but no ADD and no automatic OXY sale.** If the strategic goal is to cap energy exposure and favor lower leverage,
    a weight-neutral OXY-to-EOG swap may be sensible, but only after current normalized valuation, cost basis,
    account tax treatment, currency exposure and the desired OXY high-torque/preferred-deleveraging optionality are
    evaluated. Neither volatile E&P belongs in protected 3-5 year house capital.
- `deep_dives/DGE_L/deep_dive.md` is fully read. Its final **WATCH** is sound and now reinforced by FY2026
  results, but valuation/yield claims and the score need correction:
  - The claimed `~9% FCF yield` is a currency-denominator error: it divides roughly **$3B USD** FCF by a
    roughly **£34B GBP** market value. At the memo date the comparable market value was around $44-45B, implying
    only ~6.7%; at the recent roughly $52B ADR-implied market value, FY2026's $3.211B FCF is ~6.2%. Management's
    FY2027 FCF guide is only ~$2B after restructuring cash costs, roughly 3.8% on that recent value. All valuation
    ratios need a single currency and current share count/ADR conversion.
  - The old ~4.2% dividend yield was explicitly pre-cut and is no longer a decision metric. FY2026's recommended
    full-year dividend is 50 cents per ordinary share (about $2 per four-share ADR), roughly 2.1% at a ~$96 ADR,
    not 4.2%. The 50-cent policy floor is management policy, not contractual downside protection.
  - The scorecard arithmetic is **6.55**, yet the document labels it 6.0 and then `rounds` it to 6.0-6.6. That is
    not reproducible scoring. More fundamentally, qualitative 0-10 labels and analyst multiples do not replace a
    cash-flow downside/required-return model.
  - Official FY2026 results show partial stabilization, not a sales inflection: reported net sales fell 3.0% to
    $19.643B and organic sales fell 2.0% (volume -0.4%, price/mix -1.6%). Pre-exceptional operating profit was
    $5.683B and organic operating profit rose 2.0%, with margin +116bp, mainly because of savings. Reported profit
    fell 27.2% after restructuring/impairments; $1.5B of impairments included Türkiye and Don Papa, evidence that
    brand/M&A capital allocation is not uniformly `best in class`.
  - Cash and leverage improved: FCF rose to $3.211B, net debt fell to $20.5B and adjusted net debt/EBITDA to 3.1x.
    This supports solvency and the turnaround, but the EABL sale was still pending and leverage remained above the
    2.5-3.0x target. FY2027 guidance calls for broadly flat organic sales, North America down mid-single digits,
    low-to-mid-single-digit organic operating-profit growth and about $2B FCF after ~$850M exceptional programme
    cash costs. Management targets ~$1B savings over three years and ~$8B cumulative FY2027-29 FCF, but those are
    forward commitments to be monitored, not earned value today.
  - The claim that GLP-1/health moderation is only a `2-3% cumulative decade headwind` is too precise. The memo
    mixes individual drug studies, third-party industry forecasts, total-alcohol volumes and Diageo-specific
    spirits/brand demand. It fairly presents evidence on both sides, but it cannot resolve structural versus cyclical
    demand quantitatively. Diageo's own negative volume/price-mix and lost North American competitiveness carry more
    direct decision weight.
  - The stock/ADR has risen materially since the memo (DEO roughly $81 to ~$96 by 2026-08-24; DGE roughly 1,525p
    to around 1,700p+), reducing the original de-rating margin even as FY2027 FCF is guided lower. Historical peak
    price and unverified old multiple bands are not intrinsic-value evidence.
  - Corrected decision: **WATCH / turnaround candidate**, with improvement conditional on North American share and
    organic-sales stabilization, realised—not just announced—cost savings, EABL/RCB proceeds, leverage below 3x and
    FCF recovery after restructuring. It remains equity/FX/turnaround risk, not protected 3-5 year house capital.
- `deep_dives/ISP_MI/deep_dive.md` is fully read. The standalone-bank quality/yield case is directionally strong,
  and H1 2026 execution improved, but the document omits a **transformational MPS acquisition announced 2026-06-08,
  before the memo's 2026-07-02 run date**. That omission invalidates `leaning BUY-worth-more-work`; corrected status
  is WATCH pending full pro-forma deal analysis:
  - Intesa offered 1.6 newly issued ISP shares plus €1 cash per MPS share, implying €10.091/MPS and **€30.6B** total
    consideration. With about 3.037B MPS shares subject to the offer, this implies roughly **4.86B new ISP shares**
    plus ~€3.0B cash, versus an existing ISP share count around 17-18B: material ~27-28% gross share issuance. The
    offer requires at least 66.67% acceptance unless waived and still needs shareholder/regulatory/antitrust/FDI/
    foreign-subsidy approvals. Completion was targeted by December 2026.
  - Intesa has agreed to sell an MPS-branded bank perimeter with about 635 branches to Unipol for an estimated
    €3.0-3.5B and retain Mediobanca, ~625 MPS branches and assets said to represent ~80% of MPS+Mediobanca 2025 net
    income. Management forecasts €2.9B pretax run-rate synergies by 2029 against €2.1B integration charges and >€16B
    combined 2029 net income. Those are management projections with material execution, revenue-synergy, customer/
    employee retention, regulatory-remedy, accounting, credit-book and price-paid risk—not `no integration risk`.
  - The acquisition changes capital returns and valuation per share. Management now projects €61B 2025-29 total
    distribution and ~8% 2029 EPS/DPS/distribution-per-share accretion versus the standalone plan, but those outputs
    depend on the offer perimeter, share issuance, asset sale, synergies, integration costs and future approvals.
    The memo's standalone €50B plan and 95% payout cannot simply be carried forward.
  - Current H1 results are excellent: net income €5.554B (+6.5%), NII +0.6%, fees +4.9%, insurance +5.5%, costs
    -0.7%, cost/income 35.9%, gross/net NPL 1.8%/0.9%, annualised cost of risk 20bp and 2026 net-income guidance
    upgraded above €10B. However, fair-value profits rose €353M to €905M, roughly the same pretax magnitude as the
    €338M net-income increase, so fee/NII/cost lines—not the headline record alone—should drive normalization.
  - CET1 was about 13.1% after deducting €5.3B accrued H1 distribution and the €2.3B buyback, or 13.8% including
    expected DTA absorption. This is solid and above plan floors, but `fortress` is too promotional for a bank
    undertaking a large share-and-cash acquisition. Compare pro-forma CET1, MREL/TLAC, risk-weighted assets,
    deposit mix, duration and regulatory buffers against peers and requirements.
  - The ECB-rate correction is valid: the ECB did raise the deposit rate from 2.00% to 2.25% effective 2026-06-17.
    Still, a single 25bp move does not make rates a durable tailwind; Intesa's asset/liability repricing, deposit
    beta and hedge runoff need scenario analysis across the full curve.
  - `€50B returned, roughly half the market cap over four years` is misleading. 2025-29 is five inclusive fiscal
    years; dividends and buybacks are contingent gross distributions, not the same thing as a cash yield received
    by today's holder; buybacks' benefit depends on execution price, dilution and subsequent earnings. Taxes and
    withholding affect the holder's dividend return.
  - Rough P/TBV derived as market cap divided by `net income / ROTE` mixes current market value with an implied
    average tangible-equity denominator and company-adjusted ROTE. Use reported period-end tangible book per share,
    exclude AT1/minorities/goodwill consistently, and incorporate the MPS purchase-price allocation.
  - ISP has also risen from €6.14 to roughly €6.8-6.9 by 2026-08-25, while most historical Italian-bank re-rating
    has already occurred. Current price, new shares/cash, retained MPS/Mediobanca earnings and normalized credit/
    rate scenarios are required before calling the yield cheap.
  - Corrected decision: **WATCH only**. Upgrade only if the pro-forma MPS model shows attractive per-share value
    under conservative cost/revenue synergies and credit losses, regulatory approvals/remedies are acceptable,
    CET1/distributions remain robust and the current price offers an adequate downside return. A concentrated,
    leveraged Italian bank/sovereign/merger exposure is unsuitable for protected 3-5 year house capital.
- `deep_dives/ITC_NS/deep_dive.md` is fully read. The tobacco cash engine, high returns, large liquid investment
  balance and explicit ESG gate are real, but `WATCH -> BUY-worth-more-work` is **premature and should be revised
  to WATCH** after the tax shock and because the core SOTP was knowingly built without primary segment data:
  - ITC's official FY2026 standalone segment filing now supplies the missing bridge. Cigarettes generated
    ₹37,099.65cr of ₹90,713.20cr pre-elimination segment revenue (~40.9%) but ₹21,051.12cr of ₹25,138.86cr total
    segment results (~83.7%). FMCG-Others generated ₹24,209.75cr revenue and only ₹1,802.63cr segment result,
    roughly a **7.4% PBIT margin**, versus cigarettes around 56.7%. Tobacco dependence is therefore even higher
    than the memo's unverified 75-80% profit range; FMCG growth cannot offset a large cigarette profit shock soon.
  - Q1 FY2027 is the first substantive post-tax evidence and does not validate `volume resilience`. ITC says it
    used staggered pricing and more than 30 portfolio interventions, but consolidated EBITDA fell about **24% YoY**
    and PAT before exceptional items about **23%**; standalone EBITDA/PAT fell about 28%/27%. Gross revenue rose
    28% while net revenue fell 14% because excise accounting changed, so old revenue growth, margins, EV/EBITDA
    and price/mix comparisons are not comparable without restatement. FMCG-Others was strong (+12% revenue,
    +21% PBIT) and paper recovered, but their absolute profits are far too small to neutralize cigarettes.
  - The SOTP is not a valuation. It assigns HUL/Nestle-like multiples to ITC FMCG without modeling its much lower
    margin, category mix, brand investment, growth, working capital or separation tax/control costs. Saying the
    consolidated 12.6x multiple proves a discount double counts the very cigarette regulatory/terminal risk that
    drives most EBITDA. A segment DCF/multiple bridge with net cash, corporate costs, associates and taxes is needed.
  - FY2026 continuing EPS was about ₹16.20 and dividend ₹14.50, a roughly **89.5% payout**. This confirms the memo's
    adjusted 85-90% estimate and disproves reliance on the aggregator's 52% payout. The dividend is meaningful
    carry but not a floor: a high payout leaves limited protection if post-tax cigarette profit stays lower.
  - The hotel treatment is misstated. ITC's retained ~40% interest does not mean it `still consolidates some hotel
    exposure`; absent control, ITC Hotels is an associate/equity-method exposure, with the share of profit and stake
    value requiring separate treatment. Adding 40% of ITC Hotels market cap to an ITC value that already includes
    the investment, without removing associated earnings/assets, would double count.
  - `Net cash` from yfinance needs reconstruction. ITC's filing separates cash, bank balances and large current/
    non-current investments, some of which are strategic/associate holdings rather than equivalent excess cash.
    Subtract only liquid, attributable excess investments after tax and remove their income from operating value.
  - Near-zero/negative yfinance beta is not evidence that the stock is defensive, especially across NSE trading,
    INR/USD moves, a short lookback and the hotel demerger. A Canadian investor faces INR, custody/access, dividend-
    withholding and account-treatment issues that are not resolved by the business analysis.
  - The current price has fallen further from ₹289.90 to roughly **₹271 on 2026-08-25**, raising the prospective
    yield to ~5.35% on the ₹14.50 dividend but coinciding with the first post-tax earnings collapse. Lower price alone
    does not show the permanent excise burden is over-discounted.
  - Corrected decision: **WATCH, conditional first on willingness to own tobacco**. If tobacco is acceptable, require
    at least several comparable post-tax quarters of cigarette volumes/net revenue/PBIT, a primary-source segment
    SOTP/DCF, treatment of liquid investments and associates, and verified Canadian access/tax mechanics before a
  buy. It is regulated tobacco/INR equity, not protected 3-5 year house capital.
- `deep_dives/K_TO/deep_dive.md` is fully read and checked against Kinross's official FY2025 and Q2/H1 2026
  disclosures, SEC-filed MD&A, and the Great Bear PEA. The memo's final **WATCH** is directionally sound, but its
  relative-value claim that Newmont is clearly safer/better is not demonstrated and its normalization is not an
  investable valuation model:
  - Current execution and liquidity are genuinely strong. Q2 attributable production was 492,326 Au-eq oz,
    operating cash flow $1.146B and attributable FCF $726.8M; H1 attributable FCF was $1.564B. Quarter-end cash was
    $2.7B and company-defined net cash $1.9B. Kinross kept 2026 guidance at 2.0Moz (+/-5%), $1,730/oz AISC (+/-5%)
    and $1.5B attributable capex (+/-5%). These facts support resilience and capacity to self-fund projects.
  - The same results prove that current earnings are highly gold-price sensitive, though not literally `100%
    price-driven`. Q2 attributable production fell 4% and ounces sold fell, while realised gold rose 37% to
    $4,487/oz; revenue rose 29% and adjusted earnings reached $847.8M. H1 production was 984,889 oz versus
    1,024,662 oz, while realised gold was $4,679 versus $3,071. Volume, grade, cost, royalties, fuel, labour, FX,
    tax, by-products and capex all matter; price was simply the dominant favorable variable.
  - Costs are not fixed and `realised price minus AISC` is not distributable FCF. Q2 attributable AISC rose 22% to
    $1,821/oz and H1 AISC rose 25% to $1,777/oz. Q2 all-in cost was $2,404/oz, materially above AISC. Management
    explicitly attributes cost increases to fuel, labour/reagents and gold-linked royalties; its FY2026 sensitivity
    says each $100/oz gold change moves production cost about $5/oz from royalties. Taxes, working capital, growth
    capex, interest and corporate costs remain outside a simple AISC margin.
  - The memo's `$2,200-$2,600 normalized gold` is an unsupported scenario range, not intrinsic value. It applies
    today's/2026 cost base to an arbitrary metal price, then invokes Kinross's 2022 net loss without adjusting for
    the Russia/Ghana portfolio changes, impairments, production, inflation, taxes or capex. A proper mine-level or
    at least consolidated DCF needs reserve lives, grades, sustaining/growth capex, royalties/tax and correlated
    cost/FX cases at several gold decks. The memo correctly recognizes peak-cycle risk but does not quantify value.
  - The FY2025 FCF figures mix definitions. Official attributable FCF was **$2.4735B**, while reported operating
    cash flow less consolidated capex is about $2.566B. The table's `$2.57B` is therefore a rough consolidated
    subtraction, not the attributable non-GAAP figure described in the prose. Valuation must use one reconciled
    definition and distinguish sustaining from project capital.
  - Capital return is meaningful but not a valuation floor. Kinross returned about $615M through 2026-07-29,
    including $480M H1 repurchases and another $40M in July, and targets 40% of annual FCF in 2026. Since April 2025
    repurchases represented about 4% of shares. The residual 60%, dividend policy and future project spend still
    depend on gold prices and board/management decisions.
  - Great Bear's `$1.4B` is broadly correct only when properly labeled: the 2024 preliminary economic assessment
    showed $1.181B initial construction plus $248M capitalized mine development = **$1.429B total initial project
    capital**, plus $1.034B life-of-mine sustaining capital. Its $1.9B NPV/24.3% IRR used $1,900 gold, a 5% discount
    rate and partly inferred resources; the PEA itself says there is no certainty the economics will be realized.
    By Q2 2026 AEX surface construction was ~93%, the first decline blast occurred July 27, detailed engineering was
    ~50%, and federal permitting was in the information-request phase. This is valuable optionality, not a proved
    reserve-like value; first production targeted for late 2029 remains permitting/execution dependent.
  - The development pipeline is larger than the memo's Great Bear framing. On 2026-07-29 Kinross refreshed
    Lobo-Marte at ~$1.8B initial capex, ~350koz steady-state annual output and ~$1,000 AISC, with first gold in the
    early 2030s. Its headline $4.3B NPV/26% IRR uses **$4,100 gold** and a 5% discount rate; even the presented
    $3,500 case gives $3.2B NPV. These are management study economics before full detailed-engineering capex and
    permitting, so they cannot be added at face value to equity value or treated as a free catalyst.
  - The `NEM is safer/better` conclusion is unsupported by stale P/E and P/B. Book values for miners depend on
    acquisition accounting and impairments; trailing P/E at unusually high gold is pro-cyclical. Newmont has more
    asset/commodity/geographic diversification but also its own portfolio, execution and cost risks. The completed
    Newmont audit also concluded WATCH because its normalization was flawed. Compare both with consistent mine NAV,
    net cash/debt, reserve life, jurisdiction, project capital and downside gold decks—not analyst targets or P/B.
  - Kinross's recent NYSE quote remained in roughly the mid-$20s versus the memo's $24.56, so the entry has not
    changed enough to cure the missing valuation work. An analyst price target is neither a catalyst nor evidence
    of value. Total gold-factor exposure across physical bullion, ETFs and miners must be measured before adding
    another leveraged gold-equity position.
  - Corrected decision: **WATCH / cyclically strong, not BUY**. The memo is right not to chase record spot-driven
    earnings, but should not automatically prefer NEM. Upgrade only after a consistent mine/project NAV and
    per-share FCF sensitivity show an adequate return at conservative gold and inflated capex/cost assumptions,
    and only if the total portfolio's gold exposure is intentional. Kinross is volatile commodity equity and is
    unsuitable for protected 3-5 year house capital.
- `deep_dives/SREN_SW/deep_dive.md` is fully read and checked against Swiss Re's official FY2025 annual report,
  dividend history, strategy targets and H1 2026 release. The final **WATCH** remains sound and is now somewhat
  more cautious on valuation, but several supporting claims and the proposed buy level need correction:
  - H1 2026 execution was excellent on the face of it: group net income rose 9% to $2.833B, annualised ROE was
    22.7%, P&C Re net income rose 18% to $1.446B with a 76.7% combined ratio, Corporate Solutions earned $490M at
    86.1%, and L&H Re earned $1.045B. Recurring investment yield was 4.2% and estimated SST was 264% at 2026-07-01,
    above the 200-250% target range. This supports quality/capital strength and progress toward the $4.5B FY target.
  - Those results do **not** refute the cycle concern. P&C Re insurance revenue fell 8%, group insurance revenue
    fell 3%, P&C new-business CSM fell from $2.2B to $1.6B, and group new-business CSM fell from $3.1B to $2.1B.
    Year-to-date treaty renewal nominal price was -0.2%, or **-4.6% after Swiss Re's higher loss assumptions**;
    June/July was -1.2% nominal and -5.3% net of loss assumptions. Terms were said to be stable and volume +0.5%,
    but official data clearly show challenged economics and selective/non-renewed volume—not an uncomplicated
    `structural growth` story.
  - H1's underwriting result was unusually benign, not a normalized loss year. P&C Re large natural-cat claims
    were only **$169M versus an $836M H1 budget**; Corporate Solutions added $31M. Swiss Re itself attributes the
    strong P&C result partly to low large-cat experience and warned that hurricane-season risk remained. The 76.7%
    ratio therefore cannot be annualized as durable earning power.
  - The memo recognizes the 2024 US-GAAP/2024 IFRS break but still builds an invalid long-run combined-ratio series
    and labels `mid-80s` normal. Swiss Re's IFRS combined ratio includes discounting; management says its 2026 P&C
    target below 85% assumes roughly a **9-point discounting benefit**. Pre-2024 US-GAAP ratios, current IFRS ratios,
    and peers using different definitions are not economically interchangeable. FY2025's 79.4% and H1 2026's 76.7%
    are clearly strong relative to Swiss Re's same-basis target/comparatives, but a normalized ratio must be built
    on an undiscounted/restated same-basis loss and expense bridge.
  - The conclusion that `$3.1B reserve strengthening was a quality-positive clean-the-decks reset` is too generous.
    Management's move to the high end of its best-estimate range may reduce risk, but the charge first demonstrates
    prior casualty under-reserving and model/governance error. Social inflation and long-tail emergence can still
    require additions. Treat future favorable/adverse development and reserve triangles as evidence; do not award
    a quality point merely because a new CEO recognized the deficiency.
  - Capital return is accurately identified but now has primary-source numbers. The AGM-approved FY2025 dividend
    paid in 2026 was **$8.00/share**, converted to CHF6.3008, and the 2026 buyback authorization is up to $1.5B:
    $500M sustainable plus $1B extraordinary. The policy is to grow dividends with long-term earnings and at least
    maintain them, while the buyback is conditional on annual target achievement. These are board/AGM policies,
    not contractual downside protection.
  - `Never cut in a decade` is true only in the company's declaration-currency framing. The ordinary dividend was
    held at CHF5.90 in 2020-22, then declared in USD from the 2023 payment year. Because of FX, the CHF cash paid
    actually fell from CHF6.21554 in 2024 to CHF6.00752 in 2025 even though declared USD DPS rose. A Canadian owner
    also faces CHF share-price exposure, USD-declared/CHF-paid dividend conversion, Canadian-dollar translation,
    Swiss 35% statutory withholding and treaty/refund/account mechanics. The gross yield is not the net spendable
    yield without this work.
  - The current price was about **CHF140.15 on 2026-08-25**, versus roughly CHF130 implied by the memo's CHF38.3B
    market cap, and market value was about CHF41B. The paid CHF6.3008 dividend is therefore about a 4.5% trailing
    gross yield. With H1 book value $83.89/share and currency/basis differences across quote services, current P/B
    is roughly 2.0-2.1x, not the memo's 1.82x. The modest further re-rating makes the margin of safety thinner.
  - `P/B ~= P/E x ROE` is only a rough identity when price, trailing earnings and average versus ending equity are
    aligned; here they are not. More importantly, a 1.8-2.1x book multiple can be reasonable if sustainable ROE is
    14-16%, growth and capital returns persist, and the cost of equity is around 9-10%; or expensive if reserve/cat
    losses pull ROE lower. The memo's desired **1.3-1.4x book** is not derived from a residual-income/required-return
    model and may demand a very large drawdown without explaining why that is fair value.
  - Being the largest IFRS-reporting reinsurer by one revenue ranking is scale evidence, not proof of a moat or
    shareholder returns. Likewise a yfinance beta of 0.35 does not establish low correlation or safety: reinsurers
    warehouse catastrophe, casualty, mortality, credit, duration and model tail risks that ordinary beta misses.
    Peer quality must use same-basis reserves, loss ratios, CSM, capital, book growth and total shareholder return,
    not current P/B/ROE alone; the claim that cheaper SCOR/Everest are `cheap for a reason` is plausible but unproved.
  - Corrected decision: **WATCH / high-quality cyclical insurer, not BUY**. The original softening-cycle caution is
    validated, while current benign losses and stronger headline ROE have lifted the price. Upgrade only after a
    same-basis residual-income/normalized-ROE model, reserve-development review, renewal/loss-cost monitoring and
    Canadian tax/access analysis show an adequate after-tax return. Swiss Re can diversify long-horizon equity,
    but catastrophe and mark-to-market risk make it unsuitable for protected 3-5 year house capital.
- `deep_dives/etf_routes.md` is fully read and checked against current issuer holdings/product pages, Schwab's
  official international-trading terms, Questrade's published product pages, and treaty/withholding sources. Its
  broad lesson that an ETF dilutes a single-name valuation thesis is sound, but the memo's central CPIC-holdings,
  broker-access, PRIIPs and tax claims are materially wrong. **The routing recommendation must be revised.**
  - `CPIC specifically via an ETF: essentially NO` is false. iShares' official FXI schedule as of 2026-01-31
    included China Pacific Insurance H shares worth about $70.3M, roughly **1.06%** of fund net assets. Current
    third-party mirrors of iShares' full MCHI holdings show CPIC H shares at about **0.37-0.40%**, with a smaller
    CPIC A-share position as well. Thus both accessible US-listed funds provide direct CPIC exposure; it is small
    and cannot reproduce a concentrated CPIC thesis, but `no`, `skip`, and `unverified tail` are factually wrong.
  - FXI's current official page still has only 50 names and about 34% financials, so an approximately 1% CPIC weight
    is economically plausible and meaningfully larger than MCHI's tail weight. The right statement is: **FXI gives
    a small but identifiable CPIC slice; MCHI gives a still smaller diversified slice.** Neither is a substitute
    if the desired exposure is mostly CPIC, and both introduce dominant China bank/tech/policy factors.
  - Buzzi via EWI is correctly characterized as immaterial, but weights are dynamic. EWI's current official page
    shows only 25 holdings, 54.47% financials and 0.88% materials as of 2026-08-11; Buzzi is effectively the tiny
    materials sleeve, down from the memo's ~1.01%. This remains an Italy/banks allocation, not a Buzzi route.
    The MXI/VGK tail questions should be answered from full issuer files before claiming absence, but any Buzzi
    weight would remain too small to express the single-name thesis.
  - `CPIC/Buzzi need IBKR` is not generally true. Schwab's current official Global Account supports online local-
    currency equity trading in **Hong Kong and Italy** (HK$250 and €19 listed online commissions), and ordinary
    Schwab brokerage accounts can place foreign-market trades through its Global Investing desk. A separate
    Global Account application and account eligibility are required; Schwab describes it as designed for and,
    in one eligibility disclosure, limited to U.S. residents. Therefore the decisive facts are the user's current
    tax residence, Schwab account domicile/type and security eligibility—not Canadian citizenship or IBKR alone.
    CPIC/BZU.MI must be checked by ISIN with Schwab before accepting an ETF substitute.
  - Questrade's `global markets` page describes leveraged derivatives/CFDs, not ownership of cash equities on the
    Hong Kong or Milan exchanges. It cannot be used as evidence that Questrade offers the local ordinary shares.
    Conversely, absence from the normal order ticket should be confirmed with the broker rather than inferred from
    PRIIPs. Broker capability, account rules, local lots, commissions, FX and custody are separate questions.
  - The UCITS/PRIIPs explanation is backwards. PRIIPs requires a KID when products are marketed to EU/EEA retail
    investors; it does not itself prohibit a Canadian resident from buying a London-listed UCITS ETF. A Canadian or
    U.S. broker may not offer that exchange/fund, and Schwab's Global Account eligibility may exclude non-U.S.
    residents, but that is broker/product/residency access—not an `inverse PRIIPs block`. AGES needs an actual
    broker-symbol test; it should not be ruled out on the stated legal theory.
  - The tax discussion wrongly treats **citizenship as residence** and oversimplifies fund-level withholding. The
    Canada-US treaty benefits generally depend on tax residence and recognized pension ownership, not merely a
    Canadian passport. If the user is also a US citizen/resident, TFSA/RRSP reporting and Canadian/non-US fund
    treatment can change materially. The memo must first establish residence, citizenships, account domicile and
    whether the holdings are in RRSP/RRIF, TFSA/FHSA, taxable Canadian, or US accounts.
  - `A China or Europe ETF pays little US-source dividend` is misleading for a **US-domiciled ETF**. Its distribution
    to a Canadian holder is generally a US-source fund distribution even when portfolio companies are foreign.
    Foreign tax can be withheld inside the fund first; then US nonresident withholding can apply to the fund's
    distribution. A directly held US-listed ETF in an eligible RRSP/RRIF can generally avoid the second US layer,
    while TFSA does not get that treaty pension exemption; the internal foreign layer remains. Character, return of
    capital and reclaimability vary, so compare after-tax fund structure rather than underlying-company geography.
  - Current ETF facts also show why `best proxy` is a portfolio decision, not a static label. EWI is now >54%
    financials. IFRA is about 41% utilities/37% industrials/13% materials and trades around 25.6x forward/issuer P/E
    methodology; XLB is ~49% chemicals and only ~13% construction materials; MXI is a global materials basket with
    a recent issuer P/E near 24.7x. PAVE remains a purposeful US infrastructure-development basket at 0.47%, but
    current holdings, valuation, overlap with existing energy/materials exposure, and intended factor bet must be
    checked before calling it superior.
  - The direct-alternative conclusion is too categorical. PUK was separately audited as WATCH, not an automatic
    `direct stock wins`; CPIC insurer comparisons used flawed scorecards; and Buzzi was only a conditional WATCH
    pending governance, source-tax, segment and price work. CRH/Eagle/PAVE likewise require current valuation and
    portfolio-fit analysis. Ease of purchase is not evidence of expected return.
  - Corrected decision: **revise the routing memo**. First verify user residence/account type and test the exact
    local lines with Schwab Global/desk and Questrade. If concentration is intended, a direct line may be available
    without IBKR; if diversification is intended, choose the broad fund on its complete current holdings, cost,
    tax layers and portfolio overlap. FXI/MCHI do own CPIC but only at small weights; EWI owns only a tiny Buzzi
    slice. None of these equity routes belongs to protected 3-5 year house capital merely because it is an ETF.
- Repository-wide raw-data validation is complete for all **1,501 JSON** and **93 legacy XLS** files. Every file
  was opened and its contents traversed, not merely inventoried. This confirms that the corpus is mechanically
  readable, but it also exposes important provenance, missingness, reproducibility and source-quality limits.
  - All 1,501 JSON files parse successfully; none is empty and all have a top-level object. The corpus comprises
    1,463 standard yfinance cache records, 32 EDGAR cache objects and six special/project objects. No exact-file
    duplicate groups or non-finite JSON numbers were found.
  - The yfinance cache is a **July 2/5, 2026 pull snapshot**, not point-in-time financial history. Although none of
    the 1,463 records contains an explicit fetch `error`, **643** records have one or more fields in `_missing`.
    Leading gaps include earnings growth (239), free cash flow (233), debt/equity (219), EV/EBITDA (203), quick
    ratio (190), current ratio (188), dividend yield (184), PEG (155), trailing P/E (133), operating cash flow
    (115) and ROE (95). Mechanical fetch success therefore does not equal usable comparability.
  - `earnings_yield_ebit_ev` is null in all 1,463 yfinance records, indicating a derived-field/pipeline defect or
    absent EBIT dependency rather than a cross-sectional signal. Fifty-seven records have negative enterprise
    value, heavily concentrated in banks/insurers/other financials, reinforcing that EV-based ranks are not valid
    for those business models. Together with the already-proven foreign-currency mixing, this invalidates any
  claim that the raw universal score is uniformly comparable across sectors, regions and ADR/local listings.
  - All 93 XLS workbooks open successfully: 151 non-empty sheets, 65,551 numeric cells, 14,176 text cells and 93
    date cells were traversed. The current margin, P/B, ROE and EV/EBITDA US/Global/Emerging triplets have the
    same 96-industry sets, row order and column schemas. The EVA triplet has the same industries/order and only
    harmless unit-label wording differences in the US headers.
- **Prudential plc (PUK) standalone audit:** the accessible Asia/Africa insurer thesis is real, but the project
  overstates both cheapness and certainty. FY2025 official results show new-business profit of $2.782bn (+12% at
  constant exchange rates), operating free-surplus generation of $3.059bn (+15%), adjusted operating after-tax
  profit of $2.772bn, 15% operating return on tangible embedded value (TEV), 14% operating return on IFRS equity,
  a 221% free-surplus ratio and 262% shareholder GWS cover. Q1 2026 new-business profit rose another 10% CER and
  APE sales 6%, with broad segment growth. This supports business momentum and balance-sheet resilience.
  - The cached/yfinance 20.6% ROE is not the company's normalized operating measure; the comparable official
    operating IFRS-equity return is 14%. FY2025 IFRS profit/EPS were boosted by market and investment effects, so
    the lower headline IFRS P/E is not a clean recurring-earnings multiple.
  - Citi's official ADR record confirms one NYSE ADR represents two ordinary shares. At an ADR around $28.05,
    FY2025 TEV of $14.83 per ordinary implies about **0.95x TEV**, and adjusted operating EPS of $1.014 per ordinary
    implies about **13.8x** adjusted earnings. That is reasonable, not deep distress pricing. The $1.2bn 2026
    buyback is roughly 3.4% of the approximate market capitalization, but some capital return is supported by
    ICICI Prudential AMC IPO proceeds and should not all be treated as recurring free cash yield.
  - Material risks remain: embedded-value assumption sensitivity, market/FX effects, lapses and mortality,
    joint-venture/minority economics, Hong Kong and mainland-China exposure, distribution concentration and the
    ability to remit subsidiary surplus. Prudential itself cautions that TEV is assumption-based and neither a
    substitute nor a superior measure to IFRS.
  - The H1 2026 release is scheduled for 2026-08-26 18:00 EDT / **15:00 PDT** (2026-08-27 06:00 HKT), so it is not
    yet evidence. Corrected
    decision: **WATCH pending H1**, not `clear pragmatic winner` or immediate buy. Reassess price/TEV, normalized
    operating profit, new-business margin, free-surplus remittance and FY2026 capital returns after the release.
  - Nineteen cached Excel formula-error cells exist. Ten are in current `EVA.xls`: EVA for money-center banks,
    regional banks, brokerage/investment banking and building materials; ROC-WACC and EVA for non-bank financial
    services; and ROE-COE/equity EVA for retail building supply and tobacco. Nine are in historical `pedata23.xls`
    (as of 2024-01-05): expected growth/PEG for coal and two real-estate industries, plus trailing P/E-related and
    PEG fields for rubber/tires. The parser coerces these to null, so they should never be treated as zero or as
    evidence of low valuation/returns. The historical sector composite consumes Current PE, not the affected
    expected-growth/PEG columns; only the rubber/tires trailing-PE history is directly incomplete. The current
    broad sector calls therefore are not reversed by these formula cells, but EVA-based claims for the affected
    industries are unsupported and should use the cleaner P/B/ROIC table or primary-company accounts.
  - `EVAGlobal.xls` is dated **2025-01-05**, one year behind every other current regional source except its own
    metadata; this lag was noticed in `LEARNINGS.md` and the P/B Global ROIC fallback was the right mitigation.
    `history/vebitda17.xls` is anomalously stamped **2017-01-05**, the same date-year as the preceding archive
    vintage rather than the expected 2018-01-05. Its file and all 92 overlapping EV/EBITDA observations differ
    from `vebitda16.xls`, so this is an ambiguous source-metadata/date-label defect, **not proof that the values are
    duplicated**. The pipeline nevertheless assigns the year from the filename and claims that every row uses its
    real as-of date. A sensitivity run dropping that ambiguous vintage changes the documented headline sectors'
    EV/EBITDA percentiles by only about 0.5-4.1 points and leaves the broad cheap/expensive classifications intact;
    it can cause larger ordinal moves among tightly clustered middle-ranked industries. Fix or annotate the source
    date before representing the series as an exact 11-year chronology.
  - The repository currently contains **no CSV outputs at all**, despite reports citing
    `damodaran_history_long.csv`, regional `sector_cheapness_*.csv`, quant rankings and candidate CSVs as the exact
    runtime sources from which their prose tables were copied. Raw XLS and JSON caches exist, and scripts describe
    how to regenerate some outputs, but the delivered research is not fully reproducible as-is. Treat every copied
    ranking/table in Markdown as a historical result until regenerated from pinned inputs with a manifest/hash,
    validation report and stored outputs. This does not by itself falsify each number, but it materially lowers
    audit confidence in exact score/rank precision and prevents an end-to-end provenance check.
- Final portfolio/strategy reconciliation adds several decision-critical corrections beyond the earlier code
  defects. The latest operative allocation is the July 28 dashboard code, not any Markdown file labelled `FINAL`;
  even that code is internally inconsistent and cannot safely generate trade dollars without a new ground truth.
  - The JSON says `as_of: 2026-07-10` but git history changed positions through at least July 28. Later commits
    changed share counts without values, added zero-share placeholders, and did not update the as-of marker. Its
    root cash field is $296,929, while the live Google Sheet preserves a separate cash-account table that is not
    locally available. The local ledger is therefore neither a dated historical snapshot nor current ground truth.
  - Recalculating all 63 rows as shares times each stored price (with the stored CADUSD and a $4,132/oz physical-
    gold fallback matching the dashboard) gives about **$269,972 non-cash and $566,901 including the JSON cash**.
    This is only a consistency reconstruction, not current value. Twenty-two positions mapped to the `(exit)`
    sleeve total about **$26,964** at those stored prices; zero-share placeholders are not holdings.
  - On that reconstructed base, the latest 20.5% cash target is about **$116,215**, yet the plan simultaneously
    promises a $100,000 permanent floor plus a $45,000 crash tranche—$145,000 or about 25.6%. The shortfall is
    roughly **$28,785**. Dropping 5% VTIP and moving it to gold necessarily reduced safety from 25.5% to 20.5%; the
    code's old A=25.5% label and new 20.5% cash sleeve cannot both be honored. The target must choose either the
    $145k safety promise or 14% gold/other risk allocations and explicitly fund the difference.
  - The latest stored-price sleeve reconstruction shows the intended orders are still enormous relative to the
    unverified ledger: roughly +$105k global core, +$40k gold, +$24k EM, +$20k utilities and +$11k defense, offset
    mainly by -$181k cash, -$16k uranium/power, -$16k WPM and the $27k exit sleeve. This directly contradicts the
    July 26 instruction to hold cash and stop broad-equity deployment during the forecast stagflation phase. A
    long-run target and a temporary timing overlay must be separate, dated policies with falsifiable triggers.
  - The broad-index-core decision remains the strongest strategic decision **for long-horizon risk capital**; the
    fixed six-month DCA was behaviorally coherent. Replacing it with discretionary oil-phase market timing is not
    supported by a demonstrated forecasting edge and recreates the emotional timing problem DCA was meant to
    solve. Protected house capital should never be forced into the DCA schedule, so first separate the liability-
    matched pool; then use either a rules-based schedule or documented valuation/rebalancing bands for risk capital.
  - Cleanup is directionally sound, especially removing daily-reset leveraged BOIL/SQQQ from any long-term book,
    consolidating redundant micro positions and trimming WPM/uranium concentration. It remains conditional on live
    holdings, spreads, account type, residence and tax lots. Adding ETN, SMR, BRK-B, GEHC, XLV and a defense ETF
    while 22 exits remained contradicted simplification and the admitted lack of stock-picking edge. Tiny thematic
    `confetti` should be consolidated rather than given false precision through 0.05%-0.4% targets.
  - The July CI purchase was not supported by the managed-care diligence: that comparison was already audited as
    score-overridden and decision-incomplete. CI remains a preferred payer **WATCH**, not a validated financials-
    sleeve buy, until normalized earnings/PBM/regulatory downside is modeled. Likewise the completed OXY sale does
    not create a requirement to buy EOG; EOG remains WATCH and the old automatic-swap thesis is invalid.
  - The project calls $732k of Adobe RSUs `57% of net worth`, but the source description says they vest over four
    years. IRS guidance confirms an unvested RSU is an unsecured/unfunded promise and no stock/property transfers
    until vesting. Unless the $732k is already vested and saleable, it is future compensation exposure—not a
    current owned asset to place in the portfolio denominator. It should be modeled as an after-tax, vesting-
    probability/human-capital scenario. The salary/employer/technology correlation is still material, so selling
    vested shares promptly remains a sound diversification policy. The `57%` current-net-worth statistic and all
    VTI/geography weights derived from it must be rebuilt from vested shares only; even if fully vested, the stated
    ratio excluded the separate house reserve and thus was not whole-net-worth arithmetic.
  - Tax logic must start with current tax residence, not Canadian citizenship. CRA explicitly says Canadian income-
    tax obligations depend on residence, determined case by case from facts/ties. The user's US residence/green-card
    context can change TFSA/RRSP, fund, reporting and withholding treatment. No account-placement ticket should be
    executed from the memo alone; obtain a cross-border tax review using actual residence, citizenships, account
    registrations and broker domicile.
  - Splitting VTI and VXUS can be useful for rebalancing and locating US equity in an eligible RRSP while putting
    ex-US exposure in taxable. But `VXUS separate lets a Canadian claim the international foreign-tax credit` is
    incomplete: Vanguard's official Canadian withholding guide shows a directly held US-listed international ETF
    still loses first-level source-country withholding in RRSP, TFSA and taxable; only the second US layer can be
    treaty-exempt in RRSP or potentially creditable in taxable. Separation does not recover VXUS's internal first
    layer and does not by itself prove lower total tax than VT for this user.
  - The protected house pool needs its own dollar target derived from purchase currency, expected down payment,
    closing costs, timing and emergency reserve. `$250k with father` is user context, not independently evidenced
    ownership/liquidity, and the reports never establish the prospective house price. A 50/50 USD/CAD split is a
    reasonable temporary hedge only if the two purchase outcomes are genuinely comparable and the total reserve is
    sufficient in both; gold, XLU, equities, energy, copper, uranium and crypto are risk capital, not house reserve.
  - Corrected action hierarchy: **(1)** pause allocation-driven trades until broker statements/cash/tax lots and
    vested RSUs reconcile; **(2)** ring-fence a currency-matched house/emergency reserve in cash, insured deposits,
    GICs or short high-quality government instruments; **(3)** remove uncompensated leveraged/micro complexity
    subject to tax review; **(4)** build the broad low-cost global core only with verified long-horizon capital;
    **(5)** cap all macro/thematic satellites in aggregate and do not add any audit-WATCH single name without a
    current downside model. This supersedes the dashboard's exact action-dollar column.
- The decisions log's already-executed 2026-07-10 trades require process verdicts distinct from hindsight returns:
  - **ARX sale: conditionally sound.** The official transaction pays C$8.20 plus 0.40247 Shell ordinary shares per
    ARC share and remained subject to shareholder/court/regulatory closing conditions. Selling at C$30.89-30.90
    accepted the remaining spread in exchange for immediate liquidity, no deal risk and no unwanted Shell equity;
    it also reduced an acknowledged Canadian-energy concentration. That is coherent if those were the objectives,
    but it was not proven value-maximizing because the project did not quantify the then-current implied Shell-linked
    consideration, expected dividends, closing probability/timing, tax, or annualized merger spread.
  - **OXY exit and WPM trim: conditionally sound deconcentration, not security-level alpha proof.** OXY was the
    selected lower-quality energy position and WPM exceeded the intended precious-metals sub-sleeve. The trades can
    reduce common-factor risk, but current tax lots/account type and whole-portfolio look-through were not verified.
    The subsequent decision to raise total gold to 14% also means a WPM trim cannot be justified merely by calling
    it a 1% `silver/platinum` sleeve; its gold/silver economics belong in the consolidated precious-metals exposure.
  - **VTI/VXUS buys: strategically sound only for long-horizon capital.** A broad global core directly addresses
    the fragmented portfolio and weak single-name selection evidence. The taxable/RRSP withholding rationale was
    incomplete as described above, and no evidence proves the dollars were surplus to the house liability.
  - **XLU and GOOGL buys: conditional risk-capital choices, not safety assets.** Utilities can diversify equity
    factors but can fall with stocks and rates; XLU is not a principal-stable replacement for government duration
    or cash. GOOGL is a high-quality AI/platform exposure, but it adds US mega-cap/technology and employer-human-
    capital correlation and lacked a current normalized valuation in the allocation memo. Neither belongs in the
    protected house pool. The small initial tranche reduced implementation risk, but does not cure the missing
    source-of-funds, tax and aggregate-exposure reconciliation.
  - **Skipping a separate Japan/DXJ tilt: sound simplification, weak stated rationale.** Existing global funds
    already supply Japan exposure and the user lacked conviction, so avoiding another tactical sleeve is coherent.
    Japan's government-debt/GDP ratio alone is not an equity expected-return analysis and should not be presented
    as the investment proof.
  - **`Trim what is up / buy what is down` and the two-phase oil playbook: revise.** Rebalancing toward lagging
    target sleeves can be disciplined, but one-week relative performance is not valuation and can add to a broken
    thesis or sell a strengthening one. The project supplied no tested forecasting edge for geopolitical/oil-phase
    timing. Use pre-set allocation bands plus security-level thesis/valuation triggers, with tax and liquidity
    constraints, instead of short-window price direction.
- Current-primary-source macro verification supports the project's cautious strategic direction but not the
  confident timing/weight decisions:
  - **USD/debasement:** IMF COFER shows the US-dollar reserve share rose to 57.13% in 2026Q1 from 56.42% and describes
    it as broadly stable; the reported gold-over-Treasuries crossover was largely a gold-price valuation effect.
    Gradual diversification/fiscal concern is real, but a rapid dollar-collapse premise is not confirmed. Moderate
    foreign assets and liability-currency matching are sound; a concentrated anti-USD portfolio is not.
  - **Energy:** the original February EIA glut forecast was overtaken by Middle East/Hormuz disruption. The August
    2026 STEO forecasts Q3 Brent around $85 because of shut-ins/transit constraints, but still expects recovery and
    average Brent near **$69 in 2027**. This supports trimming excessive energy into conflict-driven strength and
    not adding on a structural-shortage story. It does not validate the two-phase timing system or prove exact sell
    dates; energy remains volatile risk capital and current conflict assumptions can change.
  - **China:** official NBS data show H1 2026 GDP +4.7% but Q2 slowed to +4.3%; January-July real-estate investment
    fell 19.2%, new starts 24.0%, sales area 11.8% and sales value 13.1%. China is neither collapsing nor cleanly
    healed. A small, capped long-horizon satellite can be reasonable for valuation/diversification, but `must own`
    is unsupported and VWO+KWEB+BABA must be measured look-through against one China cap.
  - **AI:** updated primary releases strongly confirm real monetization alongside extraordinary reinvestment.
    Alphabet Q2 revenue rose 24%, Cloud 82% and operating income 30% (while a $98B unrealized equity gain distorted
    net income); Amazon Q2 revenue rose 20%, AWS 37% and operating income 43%, but H1 cash capex reached $96.3B;
    Meta Q2 revenue rose 28% while capex was $31.1B and its 2026 range is $130-$145B; Microsoft continues to report
    capacity constraints and massive AI capex. `AI is real, winners exist, capex/valuation risk is high` is sound.
    Broad indexing plus very limited quality exposure is more defensible than many thematic names; exact GOOGL/
    AMZN buy levels still require current normalized valuation, and unvested Adobe RSUs must not set asset weights.
  - **Copper/critical minerals:** IEA's 2026 outlook confirms strong long-run demand and a projected 2035 copper
    supply gap, but that gap narrowed from about 30% to **25%** as projects advanced; copper had also reached record
    highs. A small patient long-run sleeve is conditionally reasonable, not an imminent-shortage trade. Nickel and
    other early-stage bets remain supply/project/policy forecasts rather than clear value.
  - **Uranium:** IEA confirms tighter markets, nuclear-growth needs and concentrated conversion/enrichment capacity;
    NEA/IAEA also says resources are sufficient if timely investment occurs. Thus the fuel-cycle theme is real but
    not a literal resource-exhaustion thesis. Trimming richly valued CCJ/GEV/URC and avoiding pre-revenue SMR as a
    core holding are sound; equity price/valuation, not uranium scarcity alone, determines return.
  - **Gold:** World Gold Council Q2 data confirm 289t central-bank buying and a durable diversification bid, but H1
    central-bank demand was the lowest since 2022, Q2 ETFs lost 45t and average gold was about $4,506/oz, 37% above
    Q2 2025. This supports a strategic gold sleeve, not a valuation-based jump from 9% to 14% or replacement of a
    liability-matched safety asset. The 14% weight is a user macro preference and concentration bet, not a result
    compelled by the evidence.
- **2026-08-25 instrument review for the user's newly supplied 100% sleeve table:** retain the requested top-level
  weights for purposes of product selection, but do not treat product selection as authorization to execute the
  dashboard's action dollars. The table still says both `trim cash by $187,833` and `do NOT deploy to equities yet`;
  timing policy and strategic targets must remain separate. The implied current portfolio base is about $618.6k.
  Current issuer/product materials support the following cleaner implementation:
  - Cash 20.5%: USD direct T-bills or SGOV (0-3 month Treasuries, 0.09%); CAD direct Government of Canada T-bills or
    a maturity-matched, CDIC-eligible GIC ladder. CBIL is a liquid Canadian 0-3 month T-bill ETF (0.11% 2025 MER)
    but is not deposit insured, and a Canadian pooled vehicle needs PFIC review if the user is a US tax person.
  - Global core 20%: VTI/VXUS remain excellent, currently 0.03%/0.05%. A coherent carve-up is 10.5% VTI, 7% VXUS
    and 2.5% AVUV; AVUV is an intentional small-value/profitability factor bet (0.25%), not an additional neutral
    core. VXUS was 26.36% emerging markets at 2026-06-30, so its 7% allocation already adds about 1.85 percentage
    points of EM before the dedicated sleeve.
  - EM/China 5%: retain 2.5% VWO (broad all-cap FTSE EM, 0.06%) and replace KWEB+BABA with 2.5% broad China through
    FLCH (current reported net cost 0.19%) if the intent is a country tilt. KWEB is a 0.69% China-internet sector
    fund that already held Alibaba 9.25% and Baidu 3.23% on 2026-08-21; therefore separate BABA is redundant and
    `cut BIDU` does not remove BIDU exposure while KWEB remains. IEMG (0.09%) is a valid alternative to VWO if the
    MSCI classification including South Korea is deliberately preferred.
  - Quality 5.5%: QUAL (0.15%, sector-neutral US quality screen) is the cleaner sleeve vehicle. If concentrated
    GOOGL/AMZN conviction is retained, cap each and use QUAL for the balance; both stocks are already embedded in
    VTI, so a 3%/2.5% pair is an active mega-cap bet rather than diversified `quality` exposure.
  - Energy 9%: IXC is the best one-fund match for the stated global XOM/CNQ/oil-and-gas intent: 50 global energy
    stocks, 0.37%, with XOM about 18%, CNQ about 2.7% and Canada about 13.5% in current official data. It is not a
    direct natural-gas-price vehicle; avoid daily-reset or futures gas products as long-term core instruments.
  - Gold 14%: use allocated physical bullion and/or GLDM (physically backed, 0.10%) for gold-price exposure. AEM is
    a mining equity and must be reclassified as such; MNT may trade at a premium/discount and its cross-border tax
    classification must be verified. Keeping AEM inside `gold core` understates equity/operating leverage.
  - Utilities 4%: VPU is preferred to XLU for a long-term holding because it gives broader multi-cap exposure (68
    stocks) at 0.09%; XLU remains acceptable when maximum trading/options liquidity is important. Neither is a
    principal-stable recession hedge.
  - The current `Financials` 2.5% is mislabeled. For actual broad financial-sector exposure use VFH (0.09%). If the
    stated intent is defensive insurance without a bank overweight, rename it `insurance/defensive compounders`
    and use roughly 1.5% KIE (53-name modified-equal-weight insurance ETF, 0.35%) plus 1% BRK.B. CI is health-services/
    managed-care exposure and belongs in healthcare; it remains WATCH from the security audit, not an automatic buy.
  - Uranium/AI-power 3.5%: NLR is the clean one-fund implementation of the current mixed ecosystem. It explicitly
    owns uranium miners, nuclear-power producers and equipment/services companies; current top positions included
    CCJ, CEG and BWXT and its current expense ratio was 0.52%. URNM (0.75%) is the higher-beta alternative for a
    fuel/miner thesis (about 81% uranium equities/19% physical at 2026-07-31), not a substitute for power exposure.
  - Copper 3%: COPX remains fit if the intended exposure is global copper-miner equities (40 holdings, 0.65%); it is
    not spot copper and has material operating, jurisdiction and equity beta. No instrument change is required,
    only correct labeling.
  - Agriculture 3%: PDBA alone is the cleaner commodity-price/inflation implementation. It is an actively managed,
    no-K-1 US ETF using agriculture futures and collateral, with a current 0.59% management/net fee under waiver
    versus roughly 0.74-0.75% gross. CF is a single fertilizer-company equity; use it only as a separately capped
    stock thesis, not as interchangeable agriculture-commodity exposure.
  - Healthcare 5%: for the stated `defensive + demographics + device tilt` intent, use 4% XLV (60 S&P 500 health
    names, 0.08%) plus at most 1% IHI. VHT (0.09%, more than 400 names) is the cleaner alternative if maximum sector
    breadth matters more than the large-cap/defensive emphasis. IHI holds GEHC but is itself concentrated (46 names;
    top three about 43% in recent official holdings) and cost 0.37%. Standalone GEHC/PFE are not required for sector
    exposure, and XLV already held PFE at 2.54% and LLY at 15.83% on 2026-08-18.
  - Defense 2%: XAR is preferred to ITA/PPA for diversified pure aerospace/defense exposure because its modified
    equal-weight design reduces mega-cap concentration; current gross expense ratio is 0.35%.
  - Crypto 2%: direct BTC remains lowest ongoing-cost only if self-custody, succession and security are genuinely
    solved. IBIT is the clean brokerage implementation (spot bitcoin trust, 0.25%, no distributions) but lacks the
    1940 Act protections of an ordinary ETF. Do not use Canadian-listed bitcoin funds for a US tax person without
    PFIC review.
  - Silver/platinum 1%: WPM is a royalty/streaming company and does not implement direct metal exposure. A clean
    split is 0.75% SIVR (allocated physical silver, current waived sponsor fee 0.30%) and 0.25% PPLT (physical
    platinum, 0.60%). US taxable holders also need the precious-metals/collectibles tax treatment reviewed.
  - Account domicile is decision-critical. IRS guidance says US tax residence can arise from the green-card or
    substantial-presence tests and Form 8621 generally applies to a US person's direct or indirect PFIC holdings.
    This supports using US-domiciled ETFs as the provisional default for a US tax resident, while Canadian-listed
    pooled vehicles require cross-border tax confirmation. Tax residence/account registration must be confirmed
    before execution.
- **2026-08-26 HIG/ACGL insurer-thesis audit:** the other agent's `newly cheap, buyable, defensive, fits
  stagflation` conclusion is directionally interesting but too confident. Full work is preserved in
  `portfolio/HIG_ACGL_REVIEW_2026-08-26.md`; the earlier sleeve-instrument review is preserved in
  `portfolio/INSTRUMENT_REVIEW_2026-08-25.md`.
  - At approximately 12:59 PDT, HIG was $139.86 and ACGL $100.72. HIG was only 4.3% below its $146.07 52-week
    high; ACGL was only 5.9% below its $107.09 high. Neither is newly beaten down. The screen is detecting low
    insurer earnings multiples, not a recent price dislocation.
  - HIG's 9.1x headline GAAP P/E is not the clean comparable valuation because Q2 GAAP EPS included $1.15/share
    of discontinued-operations income associated with Hartford Funds, including a $251m tax benefit. Its cleaner
    continuing/core multiple is roughly 10x. HIG produced an excellent 18.7% trailing core ROE, but core earnings
    grew only 1% while EPS grew 6%; repurchases supplied much of the per-share gain. At 1.99x reported book and
    1.77x ex-AOCI book versus KIE's 1.62x aggregate book multiple, HIG is reasonable value rather than clearly
    cheap. Business Insurance's underlying ratio worsened, Middle & Large reached 101.9 reported/95.3 underlying,
    favorable reserve development remained material, Personal premiums fell 7% amid competition and Employee
    Benefits weakened. Verdict: **WATCH / fair value**, not a priority buy.
  - ACGL is the stronger security-level candidate. Current price is 1.48x reported book and about 1.56x estimated
    tangible book. Its last four operating EPS observations total $10.81, or about 9.3x current price; book value
    grew 15% year over year and Q2 operating ROE remained 15.3%. But operating EPS was almost flat year over year,
    operating ROE fell from 18.2%, net written premium fell 6.9%, underwriting income fell 20%, and the ex-cat/
    ex-prior-development combined ratio worsened 1.6 points. Q2 also contained $165m of favorable reserve
    development; mortgage's exceptional result relies partly on reserve releases/cure rates. Catastrophe, long-tail
    reserve, reinsurance-cycle and mortgage-downturn risks make this **cyclical quality, not defense**. Verdict:
    **WATCH / best of the two**, suitable only as risk capital.
  - The stagflation fit is two-sided. Annual repricing and reinvestment at higher yields can help, but both companies'
    filings say claim-cost inflation can impair reserve adequacy; higher rates can lower bond values and weaken the
    economy. HIG currently has adverse general-liability/commercial-auto reserve signals and major long-tail workers'
    compensation exposure. ACGL models catastrophe and severe-mortgage-downturn losses explicitly. Neither is a
    principal-stable recession hedge.
  - KIE currently holds 53 modified-equal-weight insurance names, including both HIG and ACGL, at 0.35%; official
    characteristics were 11.20x FY1 earnings and 1.62x book. The single-name earnings discount is modest compensation
    for reserve/catastrophe risk. Corrected portfolio decision: retain **1.5% KIE + 1% BRK.B** as the default
    `insurance/defensive compounders` implementation. If deliberate active risk is accepted, a limited ACGL carveout
    (for example 0.75% ACGL + 0.75% KIE + 1% BRK.B) is more defensible than buying both names merely because the
    sleeve is underweight. Do not deploy protected/dry-powder cash or trade from the stale holdings table.
- **2026-08-26 stagflation/KIE regime audit:** full analysis is preserved in
  `portfolio/STAGFLATION_THESIS_AND_KIE_2026-08-26.md`. Current evidence supports above-target near-term inflation
  and some slowing risk, but not a confirmed stagflation regime or a high-confidence multi-year 4%-plus inflation
  forecast.
  - July CPI was 3.4% year over year but core CPI 2.5%; energy was up 14.7% and explains much of the headline
    elevation. Q2 PCE prices rose 5.3% annualized and core 3.6%, so the current shock is real, but July monthly CPI
    slowed to 0.1% headline/0.2% core. July payrolls fell 23k, an early slowdown warning, while unemployment remained
    4.1%.
  - The 2026-08-26 Q2 GDP second estimate retained 1.5% real growth, but private domestic final sales grew 4.2%,
    real GDI 2.2% and corporate profits rose sharply. The economy is slowing on headline GDP but is not presently
    stagnant. The Fed's June median projected 2026 GDP/PCE at 2.2%/3.6% and 2027 at 2.3%/2.3%; 10-year and 5y5y
    market inflation expectations were about 2.32%-2.33% on August 25. These forecasts can be wrong, but neither
    official nor market baselines embed persistent stagflation.
  - Inflation's source determines insurer outcomes. Demand-led inflation with healthy nominal growth can be good
    for premium volumes, exposure growth and float reinvestment. Energy/supply shocks, medical/wage/legal inflation
    and aggressive monetary tightening can instead raise claim severity, expose stale reserves, lower bond values
    and weaken credit/mortgage conditions. KIE is probably better positioned for **inflation plus real growth** than
    for true stagflation.
  - Corrected KIE thesis: own **1.5% KIE + 1% BRK.B** only as a modest long-horizon `insurance/defensive compounders`
    equity tilt. KIE remains reasonable if stagflation does not occur because recurring insurance demand, premium
    repricing, float income, capital returns, modified-equal-weight diversification and low valuation are structural
    arguments. It is unnecessary if the only thesis is macro: VTI already owns the sector, and KIE is neither a new
    asset class, an inflation hedge nor safe house capital. Do not add merely on higher CPI or sell merely because
    growth remains positive.
  - The broader portfolio already has 33.5% in energy/gold/uranium/copper/agriculture/silver-platinum. Current
    inflation data do not compel that weight; the resource block remains a user macro concentration that can fail
    differently under supply normalization, demand destruction, disinflation or recession. Strategic construction
  should remain multi-regime rather than depend on the stagflation timing thesis.
- **2026-08-27 Iran/Hormuz fertilizer-shortage audit:** full analysis is preserved in
  `portfolio/FERTILIZER_SHORTAGE_THESIS_2026-08-27.md`. The user's thesis is validated for
  severe physical disruption in nitrogen (urea/ammonia) and sulfur, partly validated for
  phosphate through input scarcity, and rejected as a broad potash/all-fertilizer shortage.
  IFA estimates the exposed region/route normally represents about 34% of global urea trade,
  23% of ammonia, 49% of sulfur and 18% of MAP/DAP. FAO warns missed application windows can
  lower H2 2026/2027 yields, while World Bank and company evidence shows prices remain volatile
  rather than one-way: the fertilizer index fell 4.3% in July after the spring spike, CF said
  nitrogen prices returned to pre-conflict levels at Q2 end, and Nutrien reported Q3 firming.
  - CF is the cleanest listed expression but was already up about 27.5% from 2026-02-27 and near
    $125 on 2026-08-27. Verdict: HOLD / conditional staged ADD only inside a 1% total-portfolio
    cap, preferably on a pullback toward roughly $110-$115; this is a risk-control zone, not an
    intrinsic-value estimate. NTR is the more diversified but less pure alternative.
  - MOS is the wrong simple expression because sulfur scarcity damaged phosphate margins: Q2
    net loss was $273M, adjusted EBITDA fell and company-defined FCF was negative. UAN is too
    concentrated, leveraged, tax-complex and already up about 38.7% since the conflict began.
    PDBA remains a broad agriculture-futures holding, not direct fertilizer exposure, and was
    at a one-year adjusted high.
  - Current portfolio action: HOLD/no urgent buy. The user-supplied 2.5% agriculture weight is
    inside a reasonable 2.25%-3.75% rebalance band around the 3% target. If exact-target
    implementation is explicitly desired after live broker/tax verification, use at most the
    $2,896 shortfall for CF in stages, provided CF remains <=1% of total portfolio, and fund it
    only from long-horizon risk capital—not protected house/recession cash. Preferred strategic
    sleeve remains approximately 2% PDBA + 1% CF.
- **2026-09-06 broad-commodity follow-up and recovered context:** recovered the compacted
  2026-09-02 exchange from the local Codex transcript. The prior broad-fund shortlist was PDBC,
  BCI and COM in USD, with ZCOM as the CAD-listed alternative; the user had already confirmed a
  preference for pure commodity exposure, CAD denomination when practical, and no general K-1
  restriction outside the small HSA.
  - Current issuer facts favor BCI/ZCOM for the stated goal of owning the whole commodity complex.
    Both follow Bloomberg Commodity Index Total Return, covering 25 futures contracts representing
    23 commodities. BCI was $2.28B with a 0.26% expense ratio as of 2026-06-30. ZCOM was C$616M,
    0.30% estimated MER, RRSP-eligible, and traded in CAD as of 2026-07-31. PDBC uses a 14-commodity
    benchmark but is an active fund: its 2026-04-30 SEC portfolio showed broader economic exposure
    through direct futures and multiple 28-contract swap baskets, including livestock, softs and
    platinum. It costs 0.59% net. COM is a 12-contract long/flat trend
    strategy at 0.72% and can move individual commodities to cash, so it does not cleanly implement
    a persistent whole-sector thesis.
  - The user subsequently confirmed current U.S. tax residency, access to U.S. taxable and Canadian
    RRSP/taxable accounts, a tactical supercycle objective of uncertain duration, and flexibility on
    CAD versus USD. This supersedes the provisional wrapper decision: **BCI is the preferred single
    core vehicle**. ZCOM is a Canadian-domiciled alternative mutual fund and is likely a PFIC for a
    U.S. tax resident if held in taxable accounts; CAD trading denomination does not itself create a
    CAD currency hedge. A treaty-covered RRSP can receive U.S. tax deferral and has a Form 8621 annual-
    reporting exception for PFICs held through the plan, but BCI remains cleaner and more established.
    Hold BCI in an already-funded RRSP if the user's cross-border filings are in order, otherwise in a
    U.S. taxable brokerage; do not contribute or transfer solely for this trade without tax review.
  - PDBC remains the high-beta/active-roll alternative rather than a narrower-coverage fund. Its
    representative 2026-04-30 swap basket was about 50% energy (including roughly 15.3% gasoil,
    heating oil and RBOB), versus ZCOM/BCOM's 36.6% energy and 12.2% refined products on 2026-07-31.
    That active energy tilt overlaps heavily with the user's XOM/CNQ/UNG exposure. COM remains a
    drawdown-control alternative, not a whole-sector core, because individual components can be flat.
  - The latest ZCOM/BCOM look-through was 36.63% energy, 28.71% agriculture, 15.42% precious metals,
    14.54% industrial metals and 4.69% livestock. Direct refined-products contracts were 5.01% low-
    sulphur gasoil, 3.82% ULSD and 3.36% RBOB gasoline, or 12.19% combined; there is no direct jet-
    fuel contract.
  - Live `fin-check` pricing on 2026-09-06 estimated the portfolio at $640,553 including
    $296,929 cash. Existing policy commodity sleeves totaled about $217,077 (33.9%), already near the
    33.5% strategic target, so a broad fund should replace concentrated/exit positions rather than
    be added on top. A stricter commodity/producer classification covering 22 held positions totaled
    about $203,732 (31.8%).
  - Current direct refined-products futures exposure is zero. Gross integrated-company linkage is
    XOM plus CNQ, about $38,902 or 6.1% of the portfolio, but only a fraction is refining. Applying
    latest reported segment earnings gives an approximate $2,300/0.36% portfolio look-through on a
    2026 YTD basis and about $3,400/0.54% using Q2's unusually strong refining-margin quarter. Treat
    this as a 0.35%-0.55% estimate, not a precise security decomposition. XOM's Energy Products
    segment is nearly all of it; CNQ's Midstream and Refining segment earned only C$85M versus
    C$5.851B consolidated net earnings in H1 2026.
  - Of the 22 current direct-commodity/resource-equity positions, 14 paid a dividend or fund
    distribution during the trailing year. Estimated trailing cash was about $2,224 USD (roughly
    1.09% of those holdings); a latest-rate annualized estimate is about $2,296. This definition
    excludes food manufacturers KHC/CAG and power/industrial names CEG/BWXT/SMR/GEV.
    Under the dashboard's broader six-sleeve definition, including commodity-linked power/industrial
    holdings and still-held commodity exit positions, 19 of 28 positions paid about $2,655 USD over
    the trailing year.
  - The live Google Sheet was re-read after the user added `FR_Portfolio!E1:K23`, headed `TODO Notes
    (by HS only)`. This range is permanently user-owned. The sheet then showed $662,002 total,
    $324,046 cash and $337,956 non-cash. `portfolio/dashboard/build_dashboard.py` previously cleared
    the whole tab and rewrote a full A1 matrix, which would have erased the notes. It now clears,
    writes and formats only around E1:K23. A mock build inspected every clear, value update and cell-
    formatting request and found zero intersections with the protected range. The live sheet itself
    was not rebuilt or modified during this verification.
  - BCI cannot reproduce every existing commodity target with one allocation. Individually, the
    current policy targets imply 24.57% BCI for 9% energy, 111.20% for 14% gold, 48.94% for 3% copper,
    10.45% for 3% crops/softs, or 35.34% for 1% silver; BCI contains no platinum or uranium. The clean
    provisional core-satellite implementation is about **9% BCI** if `Ag` is broadened to include
    livestock and `Copper` is broadened to industrial/electrification metals. At 9%, BCI supplies
    approximately 3.30% energy, 3.01% agriculture/livestock, 1.31% industrial metals (0.55% copper),
    1.13% gold and 0.25% silver. The residual policy sleeves would be about 5.70% direct energy,
    12.87% direct gold, 1.69% industrial metals, 0.75% silver/platinum and 3.5% uranium, preserving the
    33.5% aggregate commodity-policy target. Treat 9% as a proposal until the user confirms the revised
    sleeve definitions and tax-lot/account implementation.
  - Subsequent constituent-level review materially weakens BCI as an *incremental* purchase, even
    though it remains the best single broad-fund implementation. PDBA's 2026-04-30 SEC shareholder
    report shows it already held the full crop/softs complex plus 14.4% live cattle, 10.5% lean hogs
    and 6.9% feeder cattle: 31.8% livestock. PDBA therefore covers BCI's agriculture and livestock
    role, and actually supplies more livestock breadth than BCI.
  - Relative to the existing portfolio, BCI's genuinely missing exposures are primarily direct crude
    oil/refined-product futures and industrial metals beyond copper (aluminum, nickel, zinc and lead).
    Gold, copper, natural gas, agriculture/softs and livestock already have direct or proxy holdings;
    uranium and platinum are not in BCI at all. BCI's remaining advantage is operational simplicity
    and automatic rebalancing, not unique exposure.
  - A modular alternative is provisionally superior if Schedule K-1 administration is acceptable:
    retain/build PDBA for agriculture/livestock, use DBE inside the 9% energy sleeve and DBB inside a
    redefined 3% industrial/electrification-metals sleeve. DBE's 2026-06-30 weights were 33.19% Brent,
    28.89% WTI, 14.36% gasoil, 10.22% ULSD, 7.26% gasoline and 6.08% natural gas, so 31.84% was refined
    products. DBB's weights were 27.98% aluminum, 48.35% two copper contracts, 11.10% nickel, 8.62%
    zinc and 3.95% lead. Both charge a 0.75% management fee plus operating expenses and issue Schedule
    K-1s. A clean target illustration is 3% PDBA + 3% DBE + 3% DBB, with the remaining 6% energy in
    selected producers, gold/uranium/precious metals held separately. This is not yet a locked decision.
  - More granular review shows PDBA itself already fully covers agriculture and livestock. Its official
    2026-04-30 risk allocation was 14.4% live cattle, 10.5% lean hogs and 6.9% feeder cattle (31.8%
    livestock), plus corn, soybeans, two wheat contracts, soybean oil/meal, sugar, cotton, coffee and
    cocoa. Therefore BCI adds no material agriculture/livestock category missing from PDBA.
  - No clean, liquid U.S.-listed ETF was identified that bundles only gasoil, ULSD/heating oil and RBOB
    gasoline. ULSD is the diesel/heating-oil contract, so `diesel` is not a fourth separate exposure.
    UGA tracks only RBOB gasoline and reported 1.08% total annual expenses; the former UHN heating-oil
    vehicle is no longer an active practical option. DBE remains the nearest one-fund direct-futures
    implementation, but its 2026-06-30 portfolio was 62.08% Brent/WTI, 31.84% refined products and 6.08%
    natural gas. A 3% DBE sleeve therefore supplies about 0.96% refined products and costs roughly the
    same portfolio-level dollars as 9% BCI despite DBE's higher percentage fee. It should replace, not
    supplement, part of UNG and the energy-equity sleeve.
  - No liquid direct-futures ETF cleanly owns aluminum/nickel/zinc/lead while excluding copper. DBB was
    48.35% copper on 2026-06-30. EVMT is the closest no-K-1 electrification-metals basket (22.9% copper;
    27.3% aluminum, 26.7% nickel, 16.7% cobalt, 3.6% lithium and 2.8% iron ore; 0.59% net), but official
    2026-04-30 assets were only $5.7M and recent trading volume was very thin, creating closure/spread
    risk. PICK is a liquid 0.39% global mining-equity alternative with a 2.22% trailing yield, but it is
    producer equity rather than direct metals and includes substantial diversified mining and steel.
    Final allocation structure approved by the user: skip BCI; agriculture remains 3% as 2% PDBA plus
    up to 1% CF; energy remains 9% as 6% selected companies plus 2% DBE plus 1% UNG; the former 3%
    copper sleeve becomes industrial metals, structured as 2% copper plus up to 1% PICK. Gold remains
    14%, silver/platinum 1%, and uranium/AI-power 3.5%. The live `FR_Portfolio` allocation labels and
    corresponding holding sleeve tags were updated surgically in columns A and C only. A before/after
    hash confirmed `FR_Portfolio!E1:K23` remained unchanged. No trades were recorded or implied.
  - Hooman subsequently rejected the combined allocation labels and required each distinct thesis to
    have its own sleeve. The live `FR_Portfolio` allocation now tracks `oil-companies` at 6%,
    `ref_oil_prod` at 2%, `nat_gas` at 1%, `copper` at 2%, and `industrial_metals` at 1%. Three rows
    were inserted below the protected notes block, relevant holdings were retagged, and the target total
    remains 100%. At the live sheet value of $662,002.29, the respective current balances were
    $47,942.72, $0, $19,367.04, $11,461.14, and $0. The `E1:K23` formula/value hash remained exactly
    `936ed6537c49fbf6b14fbc1846df12571914e893a803387803d0530ceb9bcb1f` before and after the migration.
    `portfolio/dashboard/build_dashboard.py`, `portfolio/ideal_allocation.md`, `portfolio/DECISIONS.md`,
    and `portfolio/COMMODITY_IMPLEMENTATION_DECISION_2026-09-06.md` now use the same split taxonomy.
    No trades or user-note edits were made.
  - The live agriculture sleeve and dashboard model were subsequently simplified from
    `Agriculture (2% PDBA + ≤1% CF)` to `Agriculture`; the underlying 3% target and holdings were unchanged.
  - The allocation `Status` formula previously treated any drift below two percentage points as `OK`.
    That deadband was inappropriate for the new 1% and 2% sleeves because even a completely empty sleeve
    could show `OK`. Status now follows the sign of `ACTION $` (with a sub-$1 rounding tolerance), while
    the exit sleeve remains forced to `SELL`.
  - The 2026-09-06 dividend review is recorded in `divident_play.md`. On current-share-equivalent trailing
    cash, 32 of 59 positions paid about $6,004, but retained positions excluding exit names and KWEB's
    unusually large variable distribution produced a more representative $4,199. Fourteen of 22 strict
    resource holdings paid about $2,225. Jeff Currie's exact Munificent 7 were verified from his own post
    as XOM, CVX, COP, SHEL, TTE, BP and EQNR; his approximately 15% claim was FCF yield, not dividend yield.
    The conclusion is to use dividends only as a tie-breaker and not add the other six or replace DBE/PDBA.
    WPM's latest Q2 2026 revenue mix was 52% silver and 46% gold. Its live $29,756 position therefore
    represented approximately 2.34% of the portfolio in silver look-through—234% of the entire 1%
    `Silver/Plat` target—but essentially no platinum exposure; it overfills the sleeve quantitatively
    while failing to provide the intended metal diversification.
  - The 2026-09-06 options review is recorded in `options_pay.md`. Short options are conditionally useful
    only as an execution overlay on a pre-existing buy/trim decision. The preferred pilot is one PFE
    covered call; KWEB and UNG puts are rejected at current overweight sizes, all BOIL options are rejected,
    and broken-thesis exits should be sold outright. Strategic options remain in the underlying sleeve;
    speculative options count full maximum loss rather than premium against the speculation cap.
  - `Speculation (cap $10k)` is now an official 1% allocation, funded by lowering cash from 20.5% to 19.5%.
    At the live $662,048.23 portfolio value, its target was $6,620.48 versus $3,173.62 in LULU.TO. The live
    `FR_Portfolio` targets and `portfolio/dashboard/build_dashboard.py` were updated; the target total
    remained 100%, no trades were recorded, and `FR_Portfolio!E1:K23` remained unchanged.
  - On 2026-09-07 Hooman accepted the dividend research, recommendations and stated assumptions. The
    accepted plan is now recorded in `divident_play.md`, `portfolio/ideal_allocation.md`,
    `portfolio/buy_list.md`, `portfolio/sell_rules.md` and `portfolio/DECISIONS.md`. Dividends remain a
    tie-breaker rather than a sleeve; no additional Munificent-7 names are planned; PFE targets 1%, CI
    1.5%, CF 1%, PDBA 2%, DBE 2%, PICK 1%, and the oil-company names retain their 2%/2%/1%/1% targets.
    WPM's accepted current ceiling is approximately 82 shares: at the Q2 52% silver / 46% gold mix this
    represents about 1% portfolio silver look-through plus 0.88% gold look-through. Platinum remains
    unfilled and any future platinum purchase must replace part of WPM rather than expand the 1% satellite.
    The corresponding live holding-level target cells were corrected without changing allocation notes,
    the protected `E1:K23` block, or recording any trade.
  - On 2026-09-07 Hooman rejected IBM and chose not to buy it. NKE remains watch-only: a conditional
    0.25% starter at $36–$39 (about $1,655 / 43 shares at the $38.40 research price), with at most another
    0.25% after operational confirmation or below roughly $34 while the thesis remains intact. NKE is
    capped at 0.5% while LULU remains and both must fit inside the existing 1% speculation sleeve. No
    holding or trade was added; a standard 100-share NKE put is disallowed because assignment exceeds the cap.
  - A dedicated options-strategy review was completed in `options_pay.md` using the live 2026-09-06
    portfolio and delayed Cboe chains through 2026-09-04. The central conclusion is to use cash-secured
    puts and covered calls only as narrow execution overlays, not as a systematic income allocation.
    No KWEB or UNG puts are currently justified because both positions are already at/above their intended
    weights, and all BOIL options should be avoided because the underlying is a daily 2x commodity pool.
    PFE is the cleanest covered-call pilot; one excess KWEB lot and one planned CCJ trim lot are conditional
    alternatives. The proposed 1% speculation cap is about $6,620 at the current $662,048 portfolio value,
    of which LULU.TO already consumes about $3,174. U.S. taxable is the preferred pilot account. CRA Folio
    S3-F10-C1 expressly warns that put writing in an RRSP may constitute business activity even though
    Questrade currently permits cash-secured puts operationally, so RRSP put writing requires specific
    cross-border tax advice. The live Google Sheet was read but not modified.
  - A fresh healthcare/AI sleeve review was completed on 2026-09-07 and recorded in
    `portfolio/research/healthcare_ai_sleeve_2026-09-07.md`. The live sheet showed a 5% Healthcare target,
    funded only by PFE at $20,996 / 3.17%; CI added $4,520 / 0.68% of economic healthcare exposure from
    the Financials sleeve, while LLY, XLV and GEHC were unfunded. The old arithmetic is 2.5% XLV + 1.5%
    GEHC + 1% PFE = 5%; selling PFE while buying only XLV and GEHC would leave 1% unassigned. Primary
    SEC and fund-source review supports revising the implementation to 3% VHT, 1% IHI and up to 1% LLY
    bought only at valuation gates, with direct PFE and GEHC at zero by default. XLV remains an acceptable
    liquidity-first substitute for VHT; GEHC is an acceptable concentrated substitute for IHI, not an
    addition. At $1,149.36 LLY was only 7% below Hooman's $1,235.56 RRSP sale and about 31.9x the midpoint
    of company 2026 adjusted-EPS guidance, so the first direct re-entry gate is $1,050 or about 22x current
    next-year consensus, subject to estimate and thesis verification. PFE's Q2 operating evidence improved,
    but its direct holding remains inconsistent with the growth/AI objective; current aggregate taxable gain
    is about $2,339 before lot-level adjustments. The live sheet and portfolio plan were read but not edited.
  - A dedicated Nike review was completed on 2026-09-07 and recorded in
    `portfolio/research/nke_buy_review_2026-09-07.md`. At the 2026-09-04 close of $38.40, NKE was about
    78% below its 2021-11-05 peak and traded near 1.23x fiscal-2026 sales. The low multiple reflects real
    impairment: fiscal-2026 currency-neutral revenue fell 2%; Nike Direct fell 6%, Digital fell 12%,
    Greater China fell 11% reported/13% currency-neutral, and Converse fell 31%. Reported EPS of $2.10
    included a $0.52 tariff-recovery benefit; the company stated underlying EPS was $1.58, making the
    shares about 24x trough underlying earnings rather than a simple deep-value stock. Fiscal-2026 simple
    FCF was $2.18B versus $2.41B of dividends, although $9.03B cash plus short-term investments exceeded
    $7.94B funded debt. The turnaround has early proof in five quarters of double-digit Running growth,
    improved North American wholesale and full-price realization, but Sportswear/Jordan (about half of
    revenue), China and Digital remain unproven while On, HOKA and adidas are growing faster. Verdict:
    good but damaged franchise; staged speculation rather than core. If desired, use a 0.25% starter near
    $36-$39 and add at most another 0.25% after operating confirmation or below about $34 with the thesis
    intact. Keep NKE plus LULU within the existing 1% speculation cap and fund no NKE from strategic-core
    or house-reserve capital. The live sheet and portfolio plan were not modified.
  - A dedicated IBM review was completed on 2026-09-07 and recorded in
    `portfolio/research/ibm_buy_review_2026-09-07.md`. At the 2026-09-04 close of $234.89, IBM was about
    29% below its speculative June peak but still about 7% above its 2024 year-end close. The July 14
    collapse followed a genuine Q2 execution shortfall: reported Software grew 5% but was approximately
    flat organically, Transaction Processing fell 9% at constant currency, IBM Z fell 42%, and management
    reduced full-year constant-currency revenue guidance to 4%-5%. Red Hat, Software ARR, Distributed
    Infrastructure and Consulting AI signings remained healthy, so the weakness is primarily execution and
    product-cycle related, but the claim that delayed deals are merely deferred still needs confirmation.
    At the current price IBM trades near 14.1x management's approximately $15.7B 2026 FCF guidance, 16.1x
    after annualized SBC, and 19.1x current-year consensus operating EPS: fair, not distressed. The
    short-term chart is an unconfirmed post-crash base and the longer-term bear-flag interpretation remains
    plausible below the 50/100/200-day moving averages. Verdict: WATCHLIST/no purchase now; consider at most
    0.5% from the existing speculation capacity, staged below $220 and preferably $190-$200, only if delayed
    deals, organic Software and FCF validate. IBM and NKE must compete for the same cap. The live sheet and
    portfolio plan were not modified.
  - A fresh uranium/nuclear review was completed on 2026-09-07 and recorded in
    `portfolio/research/uranium_sleeve_review_2026-09-07.md`. The final policy supersedes an
    intermediate implementation: the former combined 3.5% `Uranium/AI-power` budget is split into
    **2.5% uranium/nuclear + 1.0% grid/electrification**, with GEV/ETN excluded from uranium and no
    reduction to cash. The live sheet still shows the stale intermediate 3.5% uranium, 1% grid and
    18.5% cash targets; this background agent did not edit it. The uranium-only holdings were
    $24,826 / 3.75% as displayed, or about $25,422 / 3.84% after correcting the stale `TSE:URC`
    corporate-action quote. VanEck's 2026-09-03 NLR holdings were reconstructed as approximately
    54.27% uranium/fuel, 25.34% operating nuclear utilities and 20.42% equipment/reactor developers.
    NLR directly overlapped CCJ 8.09%, CEG 8.99%, BWXT 5.44% and SMR 4.51%, but held no GEV, ETN or
    UROY. The research-only proposed uranium end state is **1.0% NLR + 0.75% CCJ + 0.40% CEG +
    0.35% BWXT**; reconcile and sell old URC/UROY, sell direct SMR, trim CCJ toward 49 shares and
    BWXT toward 15, add CEG toward 9 only at its valuation/confirmation gate, and buy about 55 NLR.
    This releases about $8.8K from the uranium sleeve. No trade was recorded.
  - A first-principles utilities review was completed on 2026-09-07 and recorded in
    `portfolio/research/utilities_sleeve_review_2026-09-07.md`. The live sheet held 58 XLU worth
    $2,499 / 0.38% against a 4% target. The report rejects the claim that utilities are a true
    recession or house-capital hedge: VPU and XLU fell roughly 36% in the 2020 crash, although their
    five-year beta to VTI was about 0.44 and they diversified the 2022 inflation/rate shock. It
    recommends retaining a smaller **2.5% utilities sleeve**, using **VPU** as the broad, low-cost
    core; VPU had 68 stocks, a 0.09% fee and 86.4% combined electric/multi-utility exposure in its
    2026-06-30 factsheet. FUTY is an economically interchangeable 0.084%-fee alternative; XLU is
    best only for maximum liquidity/options, RSPU is too expensive at 0.40%, and concentrated active
    UTES overlaps the separate merchant/nuclear thesis. Proposed implementation is to sell/swap the
    58 XLU shares and stage 89 VPU shares 45/22/22, while redirecting the freed 1.5 percentage points
    to the global equity core. At corrected targets, utilities + uranium/nuclear + grid total 6%,
    versus 7.5% under the stale live targets. No live sheet or plan was edited.
  - A fresh financials/insurance sleeve review was completed on 2026-09-07 and recorded in
    `portfolio/research/financials_sleeve_review_2026-09-07.md`. The live dashboard's 1.67%
    `Financials` balance incorrectly included $4,520 / 0.68% of Cigna, which is economically
    healthcare. Correct direct financial exposure was only the four Fairfax shares, approximately
    $6,568 / 0.99%; current broad-fund financial look-through added roughly 0.23%. At the target
    VTI/VXUS/VWO/KWEB weights, broad funds should supply about 3.84% financial look-through, so a
    dedicated sleeve is an optional modest tilt rather than a missing asset class. The research-only
    recommendation is to retain a capped 2.5% `financials/insurance allocators` sleeve as 1.5% BRK.B
    plus the existing 1.0% FFH, reclassify CI to Healthcare, and avoid adding a third financial ETF.
    BRK.B is staged as roughly ten shares now plus ten at $490 or after confirming results; FFH is a
    hold/no-add at four shares. CI is a hold and conditional add only to a 1.0% Healthcare target that
    replaces 1% of VHT rather than expanding total healthcare exposure. VFH is the 0.09%-fee fallback
    if ETF diversification is preferred, replacing BRK.B rather than supplementing it. Broad financial
    ETFs and bank funds were near highs while credit spreads and delinquency rates were benign, so
    KBE/KBWB were rejected as tactical pro-cyclical additions. No live-sheet or plan change was made.
  - Hooman subsequently accepted a revised implementation: reduce `financials/insurance allocators` to
    2.0% as 1.0% BRK.B + the existing approximately 1.0% FFH, with no financial ETF; increase Healthcare
    to 5.5% as 2.5% VHT + 1.0% IHI + 1.0% CI + up to 1.0% LLY only at an acceptable valuation. BRK.B is
    staged as roughly 6–7 shares initially and the remainder near $490 or after confirming results; FFH
    is hold/no-add. CI moves exclusively to Healthcare, PFE is slated for sale subject to tax-lot review,
    and unfilled LLY capacity remains cash. Hooman will update the live portfolio himself; no sheet edit
    or trade was made in recording this decision.
  - A fresh defense-sleeve review was completed on 2026-09-07 and recorded in
    `portfolio/research/defense_sleeve_review_2026-09-07.md`. NATO's 2025 estimates and Hague
    commitment plus 2026 Q2 prime-contractor filings validate a durable multi-year spending/backlog
    thesis, but the reviewed funds still traded near 28-34x earnings and remain volatile equity rather
    than a house-reserve hedge. Current VTI/VXUS holdings contain only about $150 of defense/aerospace
    look-through; at the fully funded 20% global-core target, strict defense look-through would be about
    0.22%, while the accepted BWXT plus NLR implementation contributes about 0.58% more. The research-only
    recommendation is therefore a 1.5% dedicated sleeve rather than 2%, implemented with staged SHLD:
    0.5% near current levels, 0.5% near $56-$58 or after a confirmed 200-day-average recovery with
    improving estimates, and 0.5% after two reporting cycles confirm backlog/margin conversion. SHLD is
    preferred for global primes plus AI/software, drones, autonomy and space; XAR is the lower-cost
    equal-weight U.S. substitute. ITA is rejected for extreme GE/RTX/Boeing concentration and PPA for
    its 0.58% fee without a decisive exposure advantage. No live-sheet or portfolio-plan change was made.
  - A standalone PetroVietnam Ca Mau Fertilizer review was completed on 2026-09-07 and recorded in
    `portfolio/research/dcm_pvcfc_buy_review_2026-09-07.md`. The issuer is PVCFC, HOSE ticker DCM,
    not PVChem. DCM has a strong net-cash balance sheet, scaled urea/NPK assets and exceptional H1 2026
    earnings, but 2025 operating cash flow was negative, the trailing 6.3% dividend yield overstates the
    board's 3.1% planned 2026 yield, and earnings remain exposed to urea normalization, related-party gas,
    state control and a large 2027-2028 capex/debt ramp. DCM has no foreign-traded security or identified
    ADR; ordinary U.S./Canadian brokers generally lack HOSE access, while direct ownership requires
    Vietnam trading-code, custody, VND-account and tax/reporting administration. The recommendation is
    WATCH / do not open Vietnam custody solely for DCM. If compliant direct access already exists, cap it
    at 0.25%, stage entries near VND 28,000-31,000 and below VND 26,000 or after cash-flow confirmation,
    and fund it by reducing CF rather than expanding Agriculture. No live-sheet or plan change was made.
  - A dedicated The Trade Desk review was completed on 2026-09-07 and recorded in
    `portfolio/research/ttd_buy_review_2026-09-07.md`. TTD closed at $14.43 on 2026-09-04, about 90%
    below its December 2024 peak, and now trades near 2.3x TTM sales, 16.7x TTM GAAP earnings and
    17.1x TTM free cash flow after treating stock compensation as an economic cost. The low valuation
    reflects a genuine operating break: revenue growth slowed from 26% in 2024 to 18% in 2025, 12% in
    Q1 2026 and 3% in Q2; Q3 guidance implies about 12% contraction and a roughly 50% adjusted-EBITDA
    decline, while Q2 existing-client gross spend fell despite greater-than-95% logo retention. On
    2026-09-03 the company approved a 15% workforce reduction. The balance sheet remains strong with
    approximately $1.49B of cash/investments, no conventional funded debt and $434M lease liabilities;
    independent buy-side positioning, CTV/retail-media integrations, Kokai, OpenPath and UID2 remain
    valuable, but Google/Amazon/Meta data advantages and platform control are structural risks. Verdict:
    WATCH/no purchase before Q3 results. An optional 0.25% contrarian starter is limited to $12.50-$13.25
    absent new bad news, or 0.25% up to $18 after existing-client spend and forward growth stabilize;
    hard maximum 0.5% after a second confirming quarter. TTD must be funded only from the existing 1%
    Speculation cap and compete with LULU/NKE; it is not diversification from Hooman's Adobe/GOOGL/AMZN
    exposure. No live-sheet or portfolio-plan change was made.
- Identified an unrelated modified file outside this project:
  `../prop_research/runs/step1_region_screening/STEP1_REPORT.md`. Do not touch it.
- On 2026-09-07 Hooman accepted the corrected utilities reallocation and updated the portfolio
  himself. Local records now set Utilities to 2.5% via VPU, Gold to 15%, and grid/electrification
  to 1.5%, while preserving uranium/nuclear at 3.5%, energy at 9%, global equity core at 20%, and
  cash at 18.5%. The direct power-complex target is 7.5%. The staged planning record remains 45/22/22
  VPU shares and a sell/swap of the legacy 58 XLU shares, but no broker fills, prices or tax lots are
  asserted. Updated files: `portfolio/dashboard/build_dashboard.py`, `portfolio/ideal_allocation.md`,
  `portfolio/DECISIONS.md`, `portfolio/buy_list.md`, `portfolio/sell_rules.md`, and
  `portfolio/research/utilities_sleeve_review_2026-09-07.md`. The live Google Sheet was not modified.
- On 2026-09-08 Hooman accepted the defense review's 1.5% SHLD recommendation and directed the 0.5%
  removed from the former 2% Defense target to `Speculation (cap $10k)` rather than cash. The resulting
  targets are Defense 1.5%, Speculation 1.5% subject to the unchanged $10,000 cap, and Cash 18.5%.
  The live sheet already reflected the two 1.5% target cells when verified, so only its stale Defense
  and Speculation system notes required synchronization. No SHLD holding or trade fill was recorded,
  and `FR_Portfolio!E1:K23` remained user-owned and untouched.
- On 2026-09-08 Hooman accepted the quality-factor decision framework: use JQUA when the sleeve's
  purpose is diversified profitable-company exposure and portfolio balance; use QUAL only for an
  intentional concentrated mega-cap/AI tilt; use neither if a substantially larger VTI/VXUS core
  makes the tilt unnecessary. The clarified research recommendation remains JQUA because it is a
  Russell 1000 large/mid-cap fund—not a small-cap bet—and retains substantial AI participation while
  reducing top-ten concentration and reported valuation. Excluding technology plus communications,
  QUAL was approximately 52.5% non-tech and JQUA approximately 57.5%; QUAL's 3.64% LLY position would
  contribute about 0.20% of the total portfolio at a 5.5% sleeve weight. Hooman had already updated
  the portfolio; no live sheet, target, holding or trade record was changed.
- Hooman subsequently finalized the allocation at **3.5% JQUA plus 1.5% direct AMZN**. AMZN remains
  a bounded AWS/AI/commerce conviction because it was absent from JQUA's reviewed holdings; GOOGL can
  be converted to JQUA because Alphabet is represented in the fund. Hooman updated the portfolio and
  will maintain his notes; this record update changed neither one.
- A OneGold/gold-vehicle review was completed on 2026-09-08 and recorded in
  `portfolio/research/onegold_gold_vehicle_review_2026-09-08.md`. OneGold Switzerland Gold is a
  credible allocated, pooled physical-gold account stored with MKS PAMP, insured for physical loss
  and independently verified, but physical redemption is economically a sale of the vaulted position
  followed by purchase of an APMEX retail product—not withdrawal of the Swiss bar. The public quote
  showed a $73.59/oz, 1.66% buy/sell spread and 0.12% annual storage; on $43,000, three-year spread plus
  storage is approximately $871 before retail-product premium/international costs. Whether the stated
  bid-minus-0.30% is already embedded in the displayed sell quote should be confirmed in the order
  preview rather than double-counted. Canadian-resident account continuity and Canadian delivery are
  not guaranteed clearly enough in the public terms and require written confirmation. Swiss custody
  diversifies location but is not seizure-proof because the account and redemption channel remain
  subject to U.S. platform, legal and KYC/AML controls. Research-only recommendation: keep the existing
  approximately five ounces, but use GLDM for the remaining approximately $43,000; IAUM is a near-tie.
  This complements the existing MNT position, lowers friction and preserves brokerage liquidity for an
  uncertain U.S./Canada house horizon. No live sheet, allocation target or trade record was changed.
- Hooman accepted that gold-vehicle conclusion on 2026-09-08 and updated his notes manually. The
  accepted decision is now recorded in `portfolio/DECISIONS.md`; no Google Sheet, allocation target,
  holding quantity, execution price or trade record was changed.
- A research-only quality-compounders sleeve review was completed on 2026-09-08 and recorded in
  `portfolio/research/quality_compounders_sleeve_review_2026-09-08.md`. The live sheet showed a 5.5%
  / $36,413 target, with 51 AMZN shares worth $13,184 and 18 GOOGL shares worth $6,092, for a $17,136
  gap. The review concluded that the sleeve is defensible as a modest U.S. quality-factor tilt that
  balances the portfolio's resource and thematic concentration, but is not house-purchase protection
  and is almost entirely security-level overlap with VTI. QUAL is a strong, liquid 0.15% vehicle but
  currently has 118 holdings, 44.24% in its top ten, 47.46% in technology plus communication services,
  and a reported 30.08x P/E. Its strict AI platform/infrastructure exposure was calculated at 32.64%
  of the fund (1.80% of the total portfolio at a 5.5% QUAL allocation), rising to 43.46% / 2.39% under
  an expanded AI-beneficiary definition; Amazon was not a holding. JQUA is the research recommendation
  for the full 5.5% sleeve because its 0.12% fee, 309 holdings, sector matching, diversified quality
  definitions, 18.5% top-ten concentration, 19% turnover and $8.22B scale better fit Hooman's existing
  Adobe and mega-cap exposure. QUAL remains the alternative if a deliberate quality-plus-AI tilt is
  preferred. The clean end state is one fund, not JQUA plus QUAL; current AMZN/GOOGL can be migrated
  tax-aware. No Google Sheet, allocation, planning, or trade record was changed, and
  `FR_Portfolio!E1:K23` was untouched.
- On 2026-09-08 Hooman supplied 15 executed trades and the live `FR_Portfolio` holdings were
  reconciled to them without changing his already-updated cash balances or the protected
  `FR_Portfolio!E1:K23` notes block. Full exits recorded: 30 F, 185 SMR, 25 XME, 58 XLU and
  18 GOOGL. Partial exits recorded: 38 WPM.TO, leaving 154 aggregate WPM shares, and 271 PFE,
  leaving 467 shares in Ameritrade. Purchases recorded: 220 TTD, 80 NKE, 50 SHLD, 45 VPU,
  8 CI (24 total), 7 BRK.B, 100 VWO and 90 JQUA. The holdings aggregation formulas were extended
  from row 133 through row 138, and `portfolio/positions/ledger.csv` now records the fills. Stale
  per-name targets were also cleared for exited PFE, GOOGL and SMR; CI and BRK.B were corrected to
  1.0% targets, VWO was corrected to Emerging geography, and BRK.B's quote fallback was refreshed.
- On 2026-09-10 the global `fin-check` script was corrected after its daily report exposed that
  it still sized the portfolio from July's generated `holdings_live.json`. It now reads holdings,
  zero-share exits, cash, sleeves and target percentages from the live `FR_Portfolio` sheet first,
  falling back to JSON only if the sheet is unavailable. The stale watchlist and fallback targets were
  refreshed, Canadian ticker mappings were fixed, and the exit queue now sizes correctly. The verified
  live run showed an approximately $694,047 portfolio, $305,607 cash, and a $24,276 remaining exit queue.
- On 2026-09-10 Hooman bought 34 COPX at $88.86 in Ameritrade. The live `FR_Portfolio` row now shows
  49 shares, a $85.3909 weighted average cost and `Ameritrade` as the account. Ameritrade cash was
  reduced by the exact $3,021.24 fill notional, from $265,076.00 to $262,054.76. The protected
  `FR_Portfolio!E1:K23` notes block was verified unchanged, and the fill was recorded in the local ledger.
- On 2026-09-10 Hooman bought 47 PICK at $63.31 in Ameritrade. A new `industrial_metals` holding row
  was added to live `FR_Portfolio`, all holdings aggregation formulas were extended through row 139,
  and Ameritrade cash was reduced by the exact $2,975.57 notional from $262,054.76 to $259,079.19.
  The protected `FR_Portfolio!E1:K23` notes block remained unchanged and the local ledger records the fill.
- On 2026-09-10 the verified U.S.-to-Canada rules for personally carrying investment-grade physical
  gold were recorded in `moving_physical_bars_from_us_to_cad.md`. The record distinguishes temporary
  visits from permanent moves, explains why bullion is declarable property but ordinarily not a
  CAD$10,000/FinCEN currency-reporting instrument, documents the Canadian precious-metal tax and tariff
  treatment, and includes practical E29B, BSF186, CBP Form 4457 and travel-security checklists.
- On 2026-09-10 Hooman bought 15 NLR at $118.8408 in the Questrade cash account. A new
  `uranium/nuclear` holding row was added to live `FR_Portfolio`, and all holdings aggregation formulas
  were extended through row 140. The sheet's QT Cash USD balance was already only $285, so cash was
  intentionally left unchanged rather than deducting the $1,782.61 fill twice. The protected
  `FR_Portfolio!E1:K23` notes block remained unchanged and the local ledger records the fill.
- On 2026-09-18 Hooman sold his full actual Ameritrade KHC position of 212.2349 shares at
  $24.6127 and bought 58 IHI at $51.885 in Ameritrade. The live `FR_Portfolio` KHC row was closed
  at zero despite its stale 208.7079-share count, and the sale note records the 3.527-share / about
  $86.81 fill-notional discrepancy. IHI was appended as a Healthcare holding with a 1% name target;
  all 28 holdings-dependent summary, sleeve, bucket and geography formulas were extended from row 144
  through row 145. Per instruction, sheet cash was not changed. The `fin-check` live-source run
  recognized IHI and included it in Healthcare. The protected `FR_Portfolio!E1:K23` formula/value block
  remained unchanged, with formula hash `8f93483a8aaa273be4ba46849e03e6c9f49c549d10e3a4c10ce3810304e5952a`,
  and `portfolio/positions/ledger.csv` records both fills.

## Current reconstructed context (historical project framing; audit conclusions above supersede it)

- Original stock-screening project used a global, quality-first Hybrid A+B method:
  sector cheapness plus bottom-up quality/value screens.
- It expanded ex-US/EM coverage after recognizing US-universe bias and added a separate
  financials screen because standard EV/EBITDA/ROIC metrics mishandle banks/insurers.
- The project ultimately favored INTU, CI, SPGI, PUK, Buzzi, and an OXY-to-EOG swap; CNOOC
  was reopened after correcting an unsupported assumption that the Canadian owner was a
  U.S. person.
- A separate portfolio project targets wealth preservation/growth, a USD hedge, and a house
  purchase in 3–5 years, with macro theses around USD decay, commodities, energy, uranium,
  gold, AI, and China.
- The audit has reached corrected conclusions for the stock, macro, data and portfolio decisions documented
  above. Only the scheduled Intuit FY2026 release recheck and final synthesis remain.

## Next exact batch

Main audit handoff issued with a live-data cutoff of **2026-08-25 12:05 PDT**. All currently available local and
external evidence is incorporated. The following are deliberately time-gated follow-ups, not missing local review:

1. Recheck Intuit's official IR/SEC pages after the expected 2026-08-25 13:00 PDT release / 13:30 PDT call and
   incorporate FY2026 actuals, FY2027 guidance, restructuring savings/costs, cash flow, SBC, net share reduction
   and post-release price into the INTU verdict. Until then the operative verdict is WATCH / no action.
2. Recheck Prudential plc's official H1 release after 2026-08-26 15:00 PDT and update price/TEV, normalized
   operating profit, new-business margin, free-surplus remittance and capital returns. Until then: WATCH.
3. If the user wants an executable portfolio, obtain current broker statements, cash by account, tax lots,
   vested-versus-unvested Adobe RSUs, residency/citizenships/account registrations and the house budget/currency;
   rebuild the allocation only from that ground truth.

## Final deliverable requirements

- Separate confirmed facts from stale data, unsupported claims, calculation errors, and
  judgment calls.
- For each major decision: verdict (sound / conditionally sound / revise / invalid), evidence,
  sensitivity to assumptions, and recommended correction.
- Explicitly address portfolio suitability for the 3–5 year house horizon and avoid treating
  volatile assets as safe capital.

## Full allocation validation resumed — 2026-10-14

This is a distinct user-requested full allocation/macro audit. The historical stock-screen audit and its time-gated Intuit/Prudential follow-ups above are preserved, not restarted.

- Read this entire checkpoint through its former line 2010; read the complete October 1 macro report, PHASE1_AUDIT.md and ideal_allocation.md. Prior findings are leads, not fresh verification.
- User answered the five diagnostic questions: inflation/currency protection first, recession second, house/job security third; conditional house in 2–3 years, probably not 2027; would use portfolio minus emergency reserve; CAD250k with father still available; California/U.S. MFJ, one income, Canada fallback but no planned move.
- Adobe extract: 59 sellable shares USD13,940.52; 1,506 unvested RSUs USD355,837.68; cumulative vested count is not current holdings. Exclude unvested compensation from liquid resources. Risk tolerance remains to be derived with user; monthly spending/reserve access question is pending.
- Main-model provider rate errors repeated in two delegated workers. Local /home/colligo/.codex/config.toml already has request_max_retries=100 and stream_max_retries=100 for foundry_azure. Official config reference confirms keys; no retry config change needed. Workers will be retried with bounded batches; no model switch.
- New working report: portfolio/research/macro_monitoring/reports/2026-10-14_macro_check.md. It is not yet complete. No new allocation or thesis accepted, and no live-sheet edits/trades.

### Next exact batch — new full allocation audit

1. Improve authoritative fin_chk_macro.md for natural-language full audit, data reconciliation, personal liabilities and scenario comparison; validate generated adapter.
2. Refresh live holdings/sheet and dated quotes with explicit freshness; include full 100% target grid, correct CAD Bitcoin, preserve static physical-gold/URC limitations.
3. Fresh primary-source macro and instrument/tax verification; reconstruct available transaction history with missing ledger explicitly marked.
4. Write reproducible current/target/alternative stresses, reserve and house-capacity sensitivities; complete dated report and pending-review proposals. Do not update canonical investment records.

### Full audit progress — fresh evidence and scenarios completed, 2026-10-14

- Authoritative fin_chk_macro.md now supports natural-language full allocation review, verified data reconciliation, liability/risk scenarios and report-only alternatives without redundant full-review approval. Generated adapter description synchronized; quick_validate passes.
- Live sheet now 71 holding rows including user-recorded ASTS70; quote snapshot retrieved 2026-10-14T20:33:16Z: totalUSD678,040.70, cash262,215.40, speculation22,570.98 versus$10kcap. Full target grid100%; fin_check hardcoded parser still95% because omitted VGIT. Snapshot applies quote currency including BTC and COP-U.TO rather than blindly using recordcurrency. Physicalgold$65,534 and URC$932 retain stored marks.
- Current quotes/account inputs and reproducible scenario code saved under portfolio/research/macro_monitoring/data/2026-10-14/. No live portfolio write.
- Primary evidence report complete: September CPI3.74%YoY/0.65%MoM, core2.56%/0.33%; payroll+29k, unemployment4.2%; Q2GDP+2.2% and AugrealPCE+0.6% counter generalizedstagnation. EIAOct6 forecasts2027Brent$84 notold$74; gasstorage2%aboveaverage. September goldETFinflows replaceoldQ2outflows. IMF/IEAdirect403gapsremainvisible.
- Primary Treasury/IRS/CaliforniaFTB sources opened. FTB2025Pub1001 explicitly says California taxes annual RRSPearnings; at least$76,314 assets in exclusivelyidentifiedRRSPpositions/cash, additionalmixedaccounts unresolved. Allportfolio wealth is not automatically tax-free spendable house cash.
- Scenario calculations verified sums100%; current demand-recession shock−21.50%/$145,757; live-target approximation−24%/$162,730. These are assumed shocks, not forecasts/maxloss. Historical proxy retrieval verified VPU2020drawdown−36.4%,VGIT2022totalreturn−10.53%,VTIP2022−2.94%; rates/FX/inflation roles distinct.
- Transaction worker recovered and is normalizing60records withfieldprovenance; currentledger absent. No final report conclusion issued yet.

Next exact work: finish instrument/exposure spot-checks and transaction artifact; integrate complete thesisdashboard, reserve/housecapacity, target alternatives, tax limits, source log and explicit old→proposed changes into existing 2026-10-14_macro_check.md; check all arithmetic and report final findings to user. Do not restart historicalrepositoryaudit or updatecanonicalinvestmentrecords.

### Full allocation audit completed — 2026-10-14

Completed report: portfolio/research/macro_monitoring/reports/2026-10-14_macro_check.md (PENDING USER REVIEW OF PROPOSALS). Primary evidence and transaction companion reports complete. No live-sheet edits, trades or canonical investment-policy changes made by this audit.

- Refreshed WPMQ2 filing:52%silver46%gold;H149/49;useonlyillustrativerevenuelookthrough. CamecoQ2reportedprofitsofterYoYwithWestinghousebaseeffect. NLRofficialOct13holdingsCCJ8.43%,CEG9.89%,BWXT6.53%.
- Reconstructed59identifiabletrades+1nontradePDBAadjustment;8Octobertrades locallycorroborated.31of51oldertradeshavesomeoutsidepriorreportcorroboration,20remainprioronly/inferred. VTI/VXUS/PFE/gold/accountgapsretained;tradeclusteringandcashpauseare notautomaticallybadprocess.
- Main arithmetic checks passed:71holdings,cash/totalreconciliation,live100%targets,all5modelsand20scenarioresults,60eventCSVrecords;newPythonscriptscompile;skilladaptervalidationpasses.
- Independent review found no arithmetic mismatch. Correctedthreephrases:152kpayrollgaincoversJuly–SeptemberincludingSeptember;EIArevisionestablisheshigherpricelevelnotnecessarilylaternormalization;noncashscenariosareassumedUSDvaluemoveswithFXembedded,notindependentFXmodel.
- Review-only alternatives:55%nominalshortcash/5%VGIT/15%bullion/20%global/5%commodities, or35%nominalshortcash+20%shortTIPSwithotherssame. TIPSrevisitexplicitlyrequiresuserpreferencechange;notadopted. Provisional10–15%lossbudgetand12–18monthsexpenses+bufferforuserdecision.

**Next exact step:** Present completed findings to Hooman. Await optional spending/reserve-access details and decisions on risk budget, house delay and proposedpolicychanges; these are implementationchoices, not unfinishedauditreading. Do not restart the prior repository review or request the fiveanswereddiagnosticquestions. If useracceptschanges, mergeonlyacceptedchangesontolatestcanonicalrecords/livepolicyunderexistingauthorization. Continueholdingstaxlot/restrictedaccountreconciliationbeforeanyspecificorders.

### Allocation proposal follow-up — 2026-10-14

User asked for concrete proposed allocation changes. Re-read latest live target grid (unchanged,100%) and current decisions. Saved separate report-only proposal at portfolio/research/macro_monitoring/reports/2026-10-14_allocation_proposal.md:35%cash/shortTreasuries,20%shortTIPS,15%bullion,5%VGIT,11%VTI,9%VXUS,5%commodity-riskbudget. Explicitly conditional on provisional10–15%loss-budgetdiscussion and reconsideringpriorTIPSpreference; no preferences or livepolicychanged. Optionalretainedconvictionsmustreplacepartof20%equitybudgetandrequirefreshstresscalculation. Cashfloor depends on unansweredmonthlyspending/access; implementationdependstaxlots/RRSP. Next: presentproposal; incorporateuserfeedbackratherthanrepeatcompletedresearch.

### Trade-record update — 2026-10-19

- User supplied five completed Ameritrade fills: bought VHT8@$326.86 and VXUS29@$83.375 and sold
  SGOV50@$100.5808 on October16; sold ASTS70@$43.19 and MCD12@$242.715 on October19.
- Live `FR_Portfolio` now records Ameritrade cash $236,577.0136, VHT18 with $5,771.98 basis,
  VXUS138 with $11,734.8172 basis, and ASTS0. Net cash change across the fills is +$5,932.165 before
  unreported fees. MCD and SGOV had no active holding rows; proceeds were recorded without inventing
  missing cost bases. ASTS's nominal comparison with its recorded basis is +$58.45 / +1.97%.
- Protected `FR_Portfolio!E1:K23` values and formulas were unchanged; combined SHA-256 is
  `5d3473fdd0a3689148c7dd80a04d785443902f95462965da6a57bc104ed8ad1b`. Allocation targets were not
  changed. `DECISIONS.md`, `PROJECT_STATE.md` and `sell_rules.md` contain the durable local update.
- Next exact operational step: use these revised balances on the next requested portfolio review and
  record additional broker fills only when Hooman supplies them. The completed allocation audit and
  pending proposal decisions remain at their prior stopping point.

### Trade-record update — 2026-10-20

- User supplied a completed QT RRSP fill: sold all 80 NKE at $37.9926 at 2:57:49 p.m. ET with a
  $37.99 Day limit. Gross proceeds were $3,039.408.
- Live `FR_Portfolio` now records NKE0 and QT RRSP USD cash $3,898.408. Against the recorded $38.23
  average cost and $3,058.40 basis, the nominal realized result is -$18.992 / -0.62% before fees or
  broker-lot differences. NKE is closed and removed from the standing Speculation exit queue.
- Protected `FR_Portfolio!E1:K23` values and formulas were unchanged; combined SHA-256 remains
  `5d3473fdd0a3689148c7dd80a04d785443902f95462965da6a57bc104ed8ad1b`. Allocation targets were not
  changed. `DECISIONS.md`, `PROJECT_STATE.md` and `sell_rules.md` contain the durable local update.
- Next exact operational step: use these revised balances on the next requested portfolio review and
  record additional broker fills only when Hooman supplies them. The completed allocation audit and
  pending proposal decisions remain at their prior stopping point.

### Build Canada research started — 2026-10-20

User requested eight-name comparative research and Andrey Omelchak/LionGuard interview and past-pick review; explicitly authorized GPT-5.6-sol high-effort delegation. Canonical topic: portfolio/research/build_canada/SUMMARY.md. Prior allocation audit stays complete and proposal unaccepted. No trades or policy changes. Storage: checkout resolves under /home/colligo; /mnt/localssd volatile; container overlay means off-host durability not independently established. Next exact batch: parallel issuer evidence for VNP/ELVA, FTG/CGY/MAL, EFX/BDGI/CF; main agent interview, reputation, live portfolio and source verification.

Build Canada batch1: live sheet and official interview metadata read; no caption access, public mirror recovery delegated. Opened Walter2019 partnership, LionGuard bio and BNN June26 full picks/past-picks table. VNP/ELVA evidence received; quote-feed CAD/USD EV contamination identified and workers correcting. EFX Oct1/13 data-center awards require root verification. Next exact batch: source/arithmetic integration, nine-event historic pick comparison, Canadian policy evidence and report.

### Build Canada synthesis and arithmetic — 2026-10-20 Pacific / October 21 UTC

- Completed all eight issuer streams with user-requested GPT-5.6-sol/high workers. Root independently verified decisive orders, warrant mechanics, Calian cash/backlog scope, FTG temporary premiums, manager/past-pick evidence and policy stages. Recovered relevant sections of public publisher audio; partial ASR, not an official full transcript.
- Canonical synthesis written: `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/SUMMARY.md`. EFX/CGY lead; BDGI next watch; others ranked with valuation/cash/governance caveats. These are proposals, not accepted allocation changes. Live sheet and current policy untouched.
- Normalized all seven industrial EV comparisons in one currency; separate leases; CF evaluated with adjusted versus IFRS/mid-cycle earnings. Offline script recomputes 12 recommendation-event returns, CAD conversion and XIC benchmarks; all checks pass. Four complete three-name sets, not a manager track record.
- Storage preflight reconfirmed real checkout `/home/colligo/hs_scripts` under Hooman's backed-up home location. Needed sources/scripts remain under home, not volatile localssd. Source manifest and final review are the next bounded batch.
- Next exact step: integrate final worker review, generate/verify source manifest, check project-only changes and preserve Git checkpoint; present completed findings. Do not reopen the old allocation/repository audit or infer approval of positions/weights.

### Build Canada research completed — 2026-10-20 Pacific / October 21 UTC

- All three requested workers reviewed the integrated synthesis. Incorporated precise FCF adjustment directions, Calian customer period, Magellan adjusted-EBITDA/source provenance, FTG forecast versus observed growth, and VNP interview currency uncertainty. No material ranking/arithmetic disagreement remains.
- Verified common-currency valuations/lease sensitivities, all 12 public-pick/benchmark calculations, JSON parsing, indexed path existence and source manifest hashes. Needed evidence remains in backed-up home. Original bulky PDF/audio/HTML/XML are retained there; Git keeps text, provenance, calculations and checksums.
- Canonical report, project state, researcher-only decisions/learnings and charter index complete. No live sheet, trade, target or accepted investment-policy change. Unrelated project edits untouched.
- Next exact step: deliver the completed comparison. There is no unfinished generic collection. Reopen only at report-specific primary disclosure/valuation gates or Hooman's request; obtain actual risk budget/tax/account choices before execution advice. Prior allocation proposal remains unaccepted.

### Trade-record update — 2026-10-21

- User supplied an executed buy: 400 UNG at $9.9787, $9.98 GTEM limit, 5:23:01 p.m. ET; gross
  notional $3,991.48 before any unreported fees. Existing live account of record and order convention
  identify QT Cash; no separate account was invented.
- Live `FR_Portfolio` now records UNG 2,234 shares, $23,711.937302 basis and $10.614116966 weighted
  average. At the $9.97 sheet mark it is about $22,273 / 3.3%, versus the unchanged 1% nat-gas target.
- QT Cash USD was reduced from $198 to -$3,793.48, preserving the resulting debit/margin balance;
  total sheet cash recalculated to about $267,279 and total portfolio value to $683,535.
- `FR_Portfolio!E1:K23` values/formulas passed an exact before/after equality check; current hash using
  the newly recorded canonical serialization is `da054ceac0661403f983193437cc4c82eb9c34cd192870a54626ebc89a05818a`.
  Targets, notes and trade rules were not changed. The legacy `portfolio/positions/ledger.csv` is absent
  (only historical backups remain), so the fill is preserved in the live sheet plus `DECISIONS.md`,
  `PROJECT_STATE.md` and this checkpoint rather than fabricating a stale position ledger.
- Next exact operational step: include 2,234 UNG and the QT Cash USD debit in the next requested
  portfolio review; record any fee, FX conversion or broker cash correction only when supplied or
  visible in the live account. Do not infer a changed 1% natural-gas target from this execution.

### Build Canada trade and research-record update — 2026-10-22

- Hooman supplied six executed Canadian-dollar fills: CGY 5@C$84.88 in QT Cash and 6@C$84.93 in
  QT RRSP; EFX 60@C$32.64, BDGI 25@C$83.84, VNP 80@C$26.56 and FTG 60@C$34.47 in QT RRSP.
  Gross notional was C$9,181.38 before unreported fees. CGY is aggregated as 11 shares with
  C$933.98 basis and C$84.907273 weighted average while retaining both accounts.
- Live `FR_Portfolio` rows 153-157 now contain the five holdings. All holdings-dependent summary,
  allocation, bucket and geography formulas were extended through row 157. QT RRSP CAD cash changed
  from C$8,764.00 to C$7.02; QT Cash CAD changed from C$16.54 to -C$407.86. No unstated FX,
  funding or fee transaction was invented. The sheet target grid remains 100%.
- Provisional economic-role mappings: CGY/FTG `Defense`, EFX `oil-companies`, BDGI
  `grid/electrification`, VNP `industrial_metals`. No `Build Canada` sleeve or allocation target was
  created. Canada is recorded as a cross-cutting theme pending Hooman's taxonomy decision.
- `portfolio/research/build_canada/SUMMARY.md` now records all eight businesses in plain English,
  physical-business strength, AI/data-center dependence, assumed AI-spending-collapse drawdowns,
  historical maximum drawdowns, October 22 valuation refresh, exact fills and mapping limitations.
  `PROJECT_STATE.md`, `DECISIONS.md` and `LEARNINGS.md` contain the durable operational and research
  update. The absent legacy `portfolio/positions/ledger.csv` was not recreated.
- Protected `FR_Portfolio!E1:K23` values and formulas were exactly equal before and after. Current
  canonical-serialization SHA-256 is
  `7cfc422cf053559796e8c2c28357292571795242c9f45e2256954c1a0210c649`.
- The first monitor verification exposed missing Yahoo mappings for the five new Google Finance
  symbols. `/home/colligo/.claude/scripts/fin_check.py` now maps them to CGY.TO, EFX.TO, BDGI.TO,
  VNP.TO and FTG.TO. Syntax check and rerun passed: all five received October 22 quotes, the five
  positions and provisional sleeves were recognized, and targets summed to 100%. The pre-existing
  URC quote failure remains unrelated.
- Next exact operational step: use these revised holdings/cash balances on the next requested review.
  Discuss whether Canada should be a secondary tag or formal sleeve before changing any target; do not
  infer allocation approval from the executed fills. Record fees, FX or broker cash corrections only
  when Hooman supplies them or they are visible in the source account.

### Schwab tax-loss-harvest execution — 2026-10-26

- Hooman supplied ten completed full-position sales in Schwab: AA 50, RBLX 50, CAG 303.5594,
  BAC 51, CCJ 45, KWEB 197, COPX 78, VWO 150, PICK 80 and BWXT 29.1288. Gross proceeds were
  $42,159.751875 before unreported fees. Applying the October 23 broker-export bases gives a
  provisional $10,840.538125 loss: $8,576.978125 short term and $2,263.56 long term.
- The accepted bridges were also filled: MCHI 92@$49.1499, ICOP 119@$48.35, IEMG 112@$75.48,
  MXI 41@$106.525 and NLR 80@$91.0289. Gross purchase cost was $30,379.0378; net Schwab cash
  increased $11,780.714075 before fees.
- Live `FR_Portfolio` now records KWEB 413 (Questrade only), NLR 95 at a $95.420221 aggregate
  average, and the four other replacements at exact quantities/bases. Closed rows were reused or
  cleared, so formula coverage remains through row 157. Ameritrade synthetic cash increased from
  $228,197.99 to $239,978.704075; the pre-existing SGOV-as-cash convention and other October 23
  reconciliation issues were not silently changed.
- `FR_Portfolio!E1:K23` values and formulas were exactly equal before and after; canonical hash was
  `94319a36d329447401a6f5e447791635e31c3ffb22afdeb198fac0f1f2dab3bb`. Targets still sum to 100%.
  A private pre-write sheet backup was saved outside version control.
- Exact execution CSV and revised plan are under
  `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/tax_loss_harvesting/`.
  Next exact tax step: keep original securities blocked through November 25, review VXUS→IXUS on
  November 16 only if the loss remains material, and obtain a refreshed Schwab realized-gain report.

### Trade-record update — 2026-10-27

- Hooman supplied an executed Ameritrade buy: 70 PDBA at $36.6422 with a $36.66 Day limit at
  12:36 p.m. ET; gross notional was $2,564.954 before unreported fees.
- The October 23 broker export superseded the stale Sheet quantity and basis: 140 pre-trade shares at
  $35.25, not the Sheet's 155 at $38.77. Live `FR_Portfolio` now records 210 shares, $7,499.954 basis
  and a $35.714066667 weighted average. Ameritrade synthetic cash decreased from $239,978.704075 to
  $237,413.750075. A private pre-write Sheet backup was saved outside version control.
- At the post-write $36.65 Sheet mark, PDBA is $7,696.50 and Agriculture is $14,427.14 / 2.15% versus
  its unchanged 3% target. The full target grid still sums to 100%.
- Protected `FR_Portfolio!E1:K23` values and formulas were exactly equal before and after; canonical
  hash remains `94319a36d329447401a6f5e447791635e31c3ffb22afdeb198fac0f1f2dab3bb`.
- Next exact operational step: use 210 PDBA at the corrected basis on the next portfolio review. Record
  a commission, SGOV sale or cash correction only if Hooman supplies it or it appears in broker data.

### Trade-record and fin-check workflow update — 2026-10-28

- Hooman supplied an executed Ameritrade buy: 88 VGIT at $57.2899 with a $57.30 Day limit at
  12:56 p.m. ET; gross notional was $5,041.5112 before unreported fees.
- The October 23 broker export superseded the stale Sheet row for the pre-trade balance: 88 shares at
  a $56.65 average, not 53 shares. Live `FR_Portfolio` now records 176 shares, $10,026.7112 basis and
  a $56.96995 weighted average. Ameritrade synthetic cash decreased from $237,413.750075 to
  $232,372.238875.
- At the $57.29 Sheet mark, VGIT is $10,083.04 / 1.491% versus the unchanged 5% target; the remaining
  gap is about $23,729.87. Targets still sum to 100%. `FR_Portfolio!E1:K23` values and formulas were
  exactly equal before and after the three-cell update.
- Hooman changed the daily-review output preference. The authoritative `fin_check.md` now requires
  inspecting all raw quote rows internally but omitting the repeated per-stock return tables from the
  response. A required special-watch section covers every live underweight sleeve, emphasizing
  healthcare, Build Canada, China/broad EM and uranium/nuclear names, their entry gates and constraints.
- Next exact operational step: use 176 VGIT and the revised Ameritrade cash on future reviews. Do not
  infer another Treasury purchase or any special-watch purchase without a separate user execution.

### AI quality-sleeve and silver-vehicle research completed — 2026-11-01

- Completed primary-source comparison of LITE, MRVL, LRCX, ANET, ARM, COHR and KLAC against the
  existing 5.5% JQUA Quality sleeve, with current GOOGL and MSFT results as broad-platform context.
  Canonical report and reproducible arithmetic are under
  `portfolio/research/ai_quality_silver_2026-11-01/`. Official JQUA holdings dated October 30 show
  LRCX at 0.80% and KLAC at 0.68%; the other five candidates are absent.
- Recommendation is report-only: retain 5.5% JQUA now. LRCX is the best valuation/quality watch name
  and KLAC the best-moat second choice; ANET is high quality but too expensive; ARM, MRVL, LITE and
  COHR do not clear current valuation/cash-flow/dilution/concentration requirements. An optional
  future active variant is 4.5% JQUA plus no more than 1.0% LRCX, funded from JQUA only after a fresh
  re-underwrite near the recorded valuation gate. No target or live holding was changed.
- Verified silver structures and current costs from issuer/SEC sources. SIVR is the preferred
  long-term Ameritrade vehicle at a currently waived 0.30% sponsor fee (0.45% gross); SLV's 0.50%
  fee is justified only by tactical liquidity; OneGold charges 0.30% silver storage plus a $5
  quarterly account minimum and live spreads; PSLV is a 0.52%-MER closed-end PFIC requiring timely
  QEF/annual Form 8621 handling for a U.S. taxable investor.
- Secondary October 30 futures data show silver only 4.2% above its one-year closing low, but gold
  was also at its one-year closing low and the gold/silver ratio was about 79.4. Treat the decline as
  a better entry than the spike, not proof of fundamental cheapness or recession protection.
- At the October 30 WPM price, 154 shares are about 2.66% of the portfolio. Applying the latest WPM
  Q2 revenue mix produces an illustrative 1.38% silver and 1.22% gold look-through, so incremental
  silver would increase the existing economic overweight. This remains illustrative revenue
  attribution, not bullion equivalence or exact beta.
- Research storage preflight remains satisfied: all durable artifacts are under the real checkout in
  `/home/colligo/hs_scripts`; volatile `/mnt/localssd` was not used. No live sheet, trade record,
  accepted target, monitoring policy or pending GOOGL/JQUA fill was altered.
- Next exact step: present the completed recommendation. Reopen only after exact GOOGL/JQUA fills,
  a WPM reduction/reclassification, an explicit Silver/Platinum policy change, or an LRCX/KLAC
  valuation/earnings gate. Do not repeat the completed repository audit or answered diagnostics.

### AI quality and silver policy accepted — 2026-11-02

- Hooman accepted the 5.5% JQUA default, no immediate direct AI-infrastructure purchase, LRCX as the
  first valuation watch near $205, KLAC as the second near $140, and dollar-for-dollar funding from
  JQUA for any future direct position. The accepted active variant caps LRCX at 1.0%; combined LRCX
  plus KLAC stays at or below 1.5%; the user-level single-company ceiling remains 2%.
- Hooman accepted no direct GOOGL re-entry based on a bounce and the 30-day household repurchase
  restraint pending the exact loss-sale date and tax lots. The approximately $270 GOOGL sale and
  JQUA purchase still require exact broker fills before live quantities or cash can be changed.
- Hooman accepted no incremental silver while 154 WPM shares remain. SIVR is the future long-term
  Ameritrade default after room is created; SLV remains tactical and OneGold a minority custody option.
- Durable policy files and the fin-check research watch were updated. The live Sheet and transaction
  quantities remain unchanged. Storage preflight is satisfied under `/home/colligo/hs_scripts`.
- Next exact step: run the requested live fin-check and compare LRCX with the accepted $205/earnings
  review gate. Then await exact GOOGL/JQUA executions for the transaction record.

### Fin-check and Lam review completed — 2026-11-02

- Ran the complete default fin-check against `FR_Portfolio` and inspected all holdings, watch names,
  sleeve gaps, research watches, profit exits, legacy exits and auto-flags. The live Sheet still shows
  GOOGL and lacks the exact pending JQUA fill, so its 3.6% Quality weight and $13,042 gap are stale.
- At about 1:39 p.m. ET LRCX was approximately $231.97, down about 3.1% for the day and 33.0% over 20
  sessions, but 13% above the accepted $205 review gate. SEC submissions show no new operating filing
  after the October 21 results; the November 2 Form 4 is a 491-share tax-withholding transaction.
  Primary sources: `https://www.sec.gov/Archives/edgar/data/707549/000070754926000052/lrcx_exhibitx991xq1x2027.htm`
  and `https://www.sec.gov/Archives/edgar/data/707549/000196546226000002/wk-form4_1793642873.xml`.
- Researcher decision: do not buy LRCX today. Reopen near $205 or when confirmed results support the
  approximately 22x GAAP review test. Exact pending JQUA sizing and household AI concentration are
  additional constraints.
- Reported U.S.-Iran diplomatic hopes explain the roughly 8%-12% crude-futures decline. Treat this as
  war-premium compression, not verified Phase-2 demand destruction; total energy remains overweight.
- The run identified FIS, SHOP.TO, LULU.TO and CLX as current profitable standing exits; SBUX and SQQQ
  are the legacy exits above aggregate cost. TSE:URC remains a quote error.
- Next exact step: await exact GOOGL/JQUA broker fills; repeat LRCX review only at the price/earnings gate
  or after material issuer evidence. Do not repeat the completed AI/silver research.

### Build Canada counterfactual price screen — 2026-11-02

- Hooman asked what would be bought today if existing sleeve capacity were ignored. Refreshed the five
  held names and compared them with the completed Build Canada valuation sensitivities.
- Researcher judgment, not a user decision or order: EFX.TO is the only current small-starter candidate.
  At C$31.98 / US$22.87 it is 1.8% above the prior US$22.46 upper review level. A hypothetical 0.25%
  add is approximately US$1,689 / C$2,362 / 74 shares and would bring the existing 60-share position
  to about 0.45% of the current US$675,588 portfolio.
- BDGI.TO at C$84.62 is 6.3% above its C$79.58 upper range; CGY.TO, VNP.TO and FTG.TO remain roughly
  19%, 19% and 23% above their respective upper ranges. EFX still requires contract-economics and cash-
  conversion evidence and remains exposed to AI/data-center and gas-capex cycles.
- Next exact step remains the pending GOOGL/JQUA fill reconciliation. Reopen Build Canada after a user
  trade, a company filing, or one of the recorded price/evidence gates.

### Oil-company trim selection — 2026-11-02

- Refreshed the live Sheet before answering whether XOM should fund the oil-company sleeve reduction.
  Total portfolio was approximately US$669,153; oil companies were US$55,277 / 8.26% versus the 6%
  target, an excess of about US$15,128.
- XOM was 58 shares at $180.69, US$10,480 / 1.57%, below its 2% name target. CNQ was 588 shares at
  C$74.86, US$31,460 / 4.70%, versus its 2% name target. SLB and combined Tourmaline were also below
  their accepted name targets. The aggregate Sheet contains multiple accounts and not executable lots.
- Researcher judgment, not a user decision or order: do not sell XOM to solve this excess. CNQ is the
  concentration source. Approximately 282 CNQ shares at the snapshot price would remove the full
  sleeve excess and leave about 306 shares / 2.44%; approximately 95 shares would be a one-third first
  tranche. Reaching CNQ's full 2% name target would require roughly 338 shares, subject to broker lots,
  accounts, currency and tax review.
- Today both anchors are down with the diplomacy-driven crude reversal, so a staged CNQ trim is more
  disciplined than liquidating the entire excess into the selloff. Reconsider XOM only after a thesis
  break, a deliberate Canada-only policy change, or XOM exceeding its own target.

### Exact GOOGL/JQUA and CNQ.TO executions recorded — 2026-11-02

- Hooman supplied exact Ameritrade fills from October 30: sold 16 GOOGL at $280.9362 for $4,494.9792
  and bought 71 JQUA at $76.46 for $5,428.66. The GOOGL sale provisionally realizes a $257.0208
  short-term loss against its October 28 $4,752 basis. Ameritrade synthetic cash declined by a net
  $933.6808 to $226,686.55807544.
- JQUA is now 161 aggregate shares, $12,072.46 basis and $74.984223602 weighted average across QT Cash
  and Ameritrade. GOOGL is zero. Live policy fields now encode JQUA as the 5.5% clean end state, AMZN
  as an existing no-add holding to migrate opportunistically, and no GOOGL repurchase before November 30.
- Hooman also sold all 56 CNQ.TO shares in Questrade Dads at C$74.97 on November 2, for C$4,198.32.
  Questrade Dads CAD cash increased to C$8,451.32. The October 23 broker export showed 593 pre-sale
  aggregate CNQ shares, correcting the stale 588-share Sheet row, so the current aggregate is 537.
  The Dads account was removed; U.S./Canadian listing and remaining lot-basis reconciliation stays open.
- The live Sheet target grid remains 100%. Protected `FR_Portfolio!E1:K23` values and formulas were
  exactly unchanged; before/after hash:
  `5d3473fdd0a3689148c7dd80a04d785443902f95462965da6a57bc104ed8ad1b`.
- Post-write planning snapshot: total about $672,653; cash $265,142; Quality $24,812 / 3.69% versus
  5.5% with a $12,184 gap; oil companies $52,614 / 7.82% versus 6% with a $12,255 excess.
- Next exact step: reconcile remaining CNQ listing/account lots before another CNQ sale. GOOGL/JQUA
  execution is no longer pending; retain LRCX/KLAC and silver as review-only policies.

### Exact MNT.TO purchase recorded and stale aggregate corrected — 2026-11-03

- Hooman supplied the Questrade Dads execution: bought 74 `MNT.TO` at C$59.20 on November 3 at
  3:59:34 p.m. ET, for C$4,380.80 before any unreported commission.
- The October 23 broker export, rather than the stale 588-share live-Sheet row, established the
  authoritative 373-share pre-trade position at a reported C$51.6788 average. The live aggregate is
  now **447 shares**, approximately **C$23,656.9924 basis** and **C$52.923920358 weighted average**,
  across `QT RRSP, QT Dads`. The historical component is provisional to the precision of the exported
  four-decimal broker average.
- Questrade Dads CAD cash was restored to the exact post-CNQ-sale path and reduced from C$8,451.32 to
  **C$4,070.52**; its existing US$108.95 was preserved. The stale live cash row had reverted to C$100
  before this write.
- The target grid still sums to 100%. Current `FR_Portfolio!E1:K23` values and formulas were exactly
  unchanged before and after. The hash for this run's serialized protected-block tuple is
  `c4514ad98f6ff0f216398544a807888b9d650e223f0f02d3e82eb9f72a85aecb`.
- Next exact step: use the corrected MNT and Questrade Dads balances in the next live review; continue
  the already-open remaining-CNQ listing/account reconciliation separately.

### Omitted October 29 FIS sale recovered and recorded — 2026-11-04

- Hooman supplied the missed Ameritrade execution: sold all 138 `FIS` shares on October 29 at
  $37.493, with $0.11 reported cost. Gross proceeds were $5,174.034 and broker-displayed net proceeds
  were $5,173.92.
- Against the live record's $4,476.03 basis, the provisional realized gain is $697.89 before tax and
  any broker basis adjustment. The live Sheet now has zero FIS shares and marks the position closed.
- Ameritrade synthetic cash was corrected upward by $5,173.92, from $226,686.55807544 to
  $231,860.47807544. Targets still sum to 100%; `FR_Portfolio!E1:K23` values and formulas were exactly
  unchanged with before/after hash
  `7b7380985eac02c3bc7bea1fb430b9bc1c892387c6fbbbc82bba008d36a8b471`.
- The prior November 4 fin-check recommendation to sell FIS was invalid because it was based on the
  stale 138-share row. Future checks must omit FIS unless a later user-confirmed repurchase occurs.
- Next exact step: use the corrected Ameritrade cash and zero FIS balance in future reviews; the
  remaining CNQ and IHI reconciliations remain separate open data-quality items.

### November 5 ANET/LRCX/JQUA/SHLD executions recorded — 2026-11-05

- Hooman supplied four completed Ameritrade purchases: ANET 17 at $159.4435, LRCX 20 at $190.5181,
  JQUA 50 at $73.50 and SHLD 60 at $58.86. Combined purchase notional was $13,727.5015.
- The live aggregates are ANET 17 at $159.4435; LRCX 20 at $190.5181; JQUA 211 at
  $74.632511848 with $15,747.46 basis; and SHLD 110 at $60.655454545 with $6,672.10 basis.
- Per explicit instruction, the 99-share SGOV sale was omitted and Ameritrade cash was left unchanged
  for Hooman to replace manually. Until then, live total value and allocation percentages are
  provisional. No EFX or BDGI trade was recorded because neither TSX order executed.
- The Quality target remains 5.5%. ANET, LRCX, AMZN and JQUA count inside it; LRCX retains its 1% cap
  and ANET is no-add pending review. The Defense target remains 1.5%.
- The protected Sheet block was unchanged and the target grid still totals 100%. Verification hash:
  `e1a99859e72141da2121683028c85db423d8f655e8f33aeca04ac09a057b5093`.
- Next exact step: read Hooman's manually updated Ameritrade cash before interpreting allocation gaps;
  record EFX/BDGI only after exact completed fills arrive.

### Broker-position reconciliation applied — 2026-11-05

- Hooman supplied current Ameritrade details plus Questrade Cash and RRSP position excerpts. The live
  Sheet now records Ameritrade cash at zero and 2,266.1215 SGOV shares explicitly, while retaining
  SGOV in the 18.5% cash sleeve and Bucket A.
- CNQ is split into 314 U.S.-listed Ameritrade shares and 223 CAD-listed Questrade shares. Corrected
  material rows include IHI 138, AMZN 15, SBSW 485, CHPT 5, LCID 2, CEG 7, AEM.TO, NCX.V and UROY.
  JQUA is 211 shares at a corrected $74.649232227 weighted average.
- Existing aggregate lots backed by the prior broker reconciliation were not deleted merely because
  they were absent from one pasted account excerpt. UNG 2,234, CCO.TO 55, NLR 95 and VPU 70 remain.
- Reusable fin-check logic now adds explicit cash-equivalent securities to account cash instead of
  replacing them, and maps AEM.TO/NCX.V correctly. Dashboard rebuild formulas implement the same rule.
- Validation passed: targets sum to 100%, 73 positive holdings load from the live Sheet, SGOV plus
  account cash equals the Sheet's cash-sleeve current value, and protected `FR_Portfolio!E1:K23`
  values/formulas are unchanged.
- Next exact step: if Hooman intended the Questrade excerpts as exhaustive statements, confirm whether
  older lots absent from the excerpts were sold or transferred before removing them.

### U.S. USD to Questrade Cash funding review — 2026-11-05

- Confirmed the destination is a true Questrade Cash account, the proposed amount is US$15,000–20,000,
  the source is settled U.S.-bank cash, and the linked TD Canada account currently has no CAD.
- Official Questrade terms show no reliable route to fund a Friday TSX purchase from the U.S. bank:
  USD wires take 1–2 business days and the Cash account cannot retain a temporary CAD debit.
- Next-week choices are direct wire plus 1.5% Questrade FX for speed, or direct wire plus an interlisted
  operating-company journal for lower explicit cost and greater timing/price risk. Avoid DLR/DLR.U in
  the taxable account because of potential PFIC/Form 8621 consequences for a U.S. tax resident.
- Coinbase/NDAX was rejected: Coinbase holds can block outbound crypto; the route adds trading/network
  fees, NDAX's 0.20% sale charge, CAD withdrawal and another bank-to-Questrade leg, plus a reportable
  U.S. digital-asset disposition.
- Canonical report: `portfolio/research/us_to_questrade_funding_2026-11-05/SUMMARY.md`.
- Next exact step: Hooman chooses between paying Questrade FX on an urgent tranche, waiting for the
  interlisted-stock journal, or using a live Wise quote through his same-name TD Canada account.

### Account reconciliation advanced to evidence boundary — 2026-11-09

- Re-read the complete durable checkpoint and the October 23 account-reconciliation evidence rather
  than restarting the broader audit. The original comparison contained 29 distinct security issues
  plus five external/cash/account-split gaps.
- Corrected the five broker-supported rows missed by the November 5 write: GEV 8.013 shares and
  $4,951.04 basis; XOM 59.1665 Ameritrade shares and $7,072.53 basis; VXUS 138.0697 shares and
  $11,740.92 basis; WPM $149.4437 average; TRMLF $973.32 basis.
- Repaired the CAD-cost Bitcoin lot's USD book formula from `=D109*J109` to
  `=D109*J109*$B$4`. Updated `portfolio/dashboard/build_dashboard.py` so future rebuilds preserve the
  same USD-market/CAD-basis treatment. Its balance and underlying basis remain unverified.
- Verified the live results through a bounded Sheet batch read and a fresh `fin_check.py --json` run:
  72 positive holdings, $35,962.71 account cash, targets summing to 1.0000000000000004, and an
  approximately $680,107.22 price-dependent total. Protected `FR_Portfolio!E1:K23` was unchanged;
  formula/value hash `7b7380985eac02c3bc7bea1fb430b9bc1c892387c6fbbbc82bba008d36a8b471`.
- Replaced the stale canonical summary with the current status and added
  `portfolio/research/account_reconciliation_2026-10-23/resolution_status_2026-11-10.csv`. Also
  updated `portfolio/PROJECT_STATE.md`, `portfolio/DECISIONS.md`, and the research plan.
- Five evidence gaps remain: AEVA ownership/account/basis; physical-gold ounces/custody/basis;
  Bitcoin balances/custody/bases; current cash by account/currency including Chase/BMO scope; and
  separate current Questrade Cash/RRSP exports for exact per-account position splits.
- **Next exact batch:** consume Hooman's answers and current account evidence, update only supported
  live cells, rerun the same protected-block and 100%-target validations, then mark the reconciliation
  complete. Do not restart previously completed repository batches or infer missing cash.

### November 10 NVDA purchase and TTD exit recorded — 2026-11-10

- Hooman supplied a completed Questrade RRSP purchase of 20 `NVDA` at $167.74 and a completed sale
  of all 220 `TTD` at $15.401. A replaced 20-share `NVDA` order at $167.49 had zero fill and was
  correctly ignored.
- The live Sheet now records `NVDA` at 36 shares, $6,168.858 basis and a $171.357166667 weighted
  average across Questrade Cash and RRSP. `TTD` is zero and marked closed. Gross TTD proceeds were
  $3,388.22 and the provisional realized gain against its $14.0599 broker average is $295.042 before
  any unreported fee or basis adjustment.
- The two executions imply a net +$33.42 Questrade RRSP USD cash movement. The live account-cash cell
  was not changed because the absolute Questrade balances remain unreconciled.
- Fresh `fin_check.py --json` validation loaded 71 positive holdings, $35,946.82 of account cash,
  targets totaling 1.0000000000000004, and an approximately $676,976.96 price-dependent total.
  Protected `FR_Portfolio!E1:K23` remained unchanged with formula/value hash
  `5d3473fdd0a3689148c7dd80a04d785443902f95462965da6a57bc104ed8ad1b`.
- **Next exact batch:** obtain current Questrade Cash and RRSP CAD/USD cash balances and separate
  position exports; replace only supported live cells and do not infer absolute cash from trades.

### Holdings reconciliation completed; cash remains user-pending — 2026-11-10

- Hooman confirmed AEVA was sold in full, the physical-gold line is correct, and all three Bitcoin
  rows are correct. Set AEVA to zero and marked it closed; did not infer sale proceeds, account,
  execution price, or realized result.
- Normalized the supplied separate Questrade Cash and RRSP exports into
  `portfolio/research/account_reconciliation_2026-10-23/questrade_account_positions_2026-11-10.csv`.
  All 48 lines reconcile to live aggregate quantities and account assignments, including the
  Questrade portions of mixed Ameritrade/Dads positions.
- Used the current account averages to refine UNG basis to $13,957.0048, CCO.TO native basis to
  C$7,281.70, NLR basis to $9,064.924, CRCL basis to $3,075.552, and SLB basis to $5,427.389. Kept
  NVDA at its exact $6,168.858 fill-derived basis instead of replacing it with rounded broker averages.
- Fresh `fin_check.py --json` validation loaded 70 positive holdings, $35,947.02 of provisional
  account cash, targets summing to 1.0000000000000004, and an approximately $676,113.47
  price-dependent total. Protected `FR_Portfolio!E1:K23` was exactly unchanged with hash
  `7b7380985eac02c3bc7bea1fb430b9bc1c892387c6fbbbc82bba008d36a8b471`.
- Updated the canonical summary, resolution ledger, research plan, `portfolio/PROJECT_STATE.md`, and
  `portfolio/DECISIONS.md`. Holdings are reconciled; cash remains the single open reconciliation item.
- Added a default refusal in `portfolio/dashboard/build_dashboard.py` because its October 13
  `holdings_live.json` snapshot would otherwise reintroduce AEVA and omit newer holdings such as NVDA.
  Only `FR_PORTFOLIO_ALLOW_STALE_REBUILD=1` permits that intentional historical rebuild.
- **Next exact batch:** after Hooman manually replaces the cash cells, reread the live values, verify
  the protected block and 100% target sum, update the canonical status to complete, and stop. AEVA
  execution details are needed only for a realized gain/loss record.
