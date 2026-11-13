# Session Handoff — 2026-09-28

## Resume Point

This file is the durable checkpoint for the side conversation ending on 2026-09-28. Start the next session by reading this file, then read the two research files linked below. Do not infer that any research recommendation was approved unless this file explicitly says so.

No portfolio files, allocation targets, accepted decisions, or user-authored notes were changed in this side conversation.

## User Context Relevant to Current Research

- U.S. tax resident and Canadian citizen living in California.
- Married filing jointly; spouse currently does not work.
- Approximate 2026 household taxable income: $400,000.
- Income is principally Adobe W-2 compensation.
- User is in the U.S. on a visa, so an operating side business may require immigration/work-authorization review.
- Existing accounts can be U.S. or Canadian and can hold CAD or USD, subject to brokerage access and tax constraints.
- For the China clean-energy thesis, political, tariff, and sanctions volatility is acceptable, but delisting risk is a major concern.
- User does not want EVs or general battery makers counted in the China clean-energy thesis.
- Never touch or overwrite the user's spreadsheet notes area `FR_Portfolio!E1:K23`.

## Completed Work

### Agriculture Clarification

The standing target is:

- Agriculture: 3% total.
- PDBA: 2% preferred diversified direct-commodity core.
- CF: up to 1% optional nitrogen-producer/dividend-company complement.

The earlier `fin-check` sentence suggesting CF as an add candidate was directionally incomplete. CF can be added only up to its cap and only if valuation is attractive; PDBA remains the main implementation priority.

At the snapshot reviewed:

- Total portfolio: approximately $688,760.
- CF: approximately $5,153, 0.748%, 40 shares; room to its 1% cap was about $1,735.
- PDBA: approximately $5,822, 0.845%, 155 shares; room to its 2% target was about $7,953.
- The dashboard Agriculture total included KHC, producing a displayed shortfall of about $4,537.
- KHC is packaged food and does not implement direct agriculture exposure.
- The true PDBA-plus-CF implementation shortfall was approximately $9,688.

Relevant existing records:

- `/home/colligo/hs_scripts/claude/fin_research/portfolio/DECISIONS.md`
- `/home/colligo/hs_scripts/claude/fin_research/divident_play.md`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/FERTILIZER_SHORTAGE_THESIS_2026-08-27.md`

No file changes were requested or made for this clarification.

### Tax-Efficiency Research

The full research is saved at:

`/home/colligo/hs_scripts/claude/fin_research/tax_efficiency_research.md`

Core conclusion:

- Permanent 100% federal bonus depreciation under Section 168(k) is real for qualifying property acquired after 2025-01-19.
- Bitcoin-mining hardware can likely qualify if used in a bona fide business and placed in service.
- A deduction is not a reimbursement and does not make an uneconomic investment profitable.
- Hosted mining can fail the material-participation test, causing losses to be passive and unable to offset Adobe W-2 income.
- At approximately $400,000 married-filing-jointly taxable income, the user's marginal federal bracket is closer to 24% than the promoted 37% example.
- California does not conform to federal bonus depreciation.
- Promotional mining revenue figures omitted electricity, hosting, fees, downtime, difficulty increases, taxes, and depreciation recapture.
- Do not deploy $100,000 or borrow through a HELOC or Bitcoin-backed loan for this strategy.
- If still interested after CPA and immigration review, only a $5,000-$10,000 cash pilot was considered defensible.

This was research only; the user has not approved an implementation.

### China Clean-Energy Export Thesis

The full research is saved at:

`/home/colligo/hs_scripts/claude/fin_research/china_clean_energy_export_research.md`

Core conclusion:

- The thesis is credible over roughly three to five years, especially for transformers, switchgear, grid automation, inverters, and power electronics.
- Solar-module export volume is not currently an attractive equity thesis because of severe overcapacity and poor profitability.
- The portfolio already had approximately 9.8% exposure to the broader AI-power/electrification chain as of the 2026-09-23 snapshot.
- Direct China-specific clean-energy exporter exposure was effectively zero.
- Global X China Clean Energy ETF, Hong Kong tickers 2809/9809, was the best packaged thematic fit found.
- It presents brokerage-access, PFIC, cross-border tax, and liquidity complications.
- No immediate purchase was recommended.
- If access and tax treatment are resolved, a maximum 0.5% exploratory allocation could be considered, funded from existing China or electrification exposure rather than added on top.

This recommendation is pending user acceptance. Do not add it to the portfolio or accepted decision records yet.

## Exact Next Step

Ask whether the user accepts the China clean-energy conclusion or wants deeper diligence on one of these paths:

1. Brokerage and tax feasibility of buying 2809/9809.
2. Fundamental comparison of Sungrow, NARI, Deye, China XD, Goldwind, and Dongfang Electric.
3. A no-China-specific alternative using existing GEV/ETN exposure.
4. A monitored watchlist with valuation and profitability triggers rather than a current purchase.

Before proposing any trade, refresh the live portfolio and current market/fund data. The figures in the research are snapshots, not live values.

## Portfolio Source of Truth

Use the live portfolio workflow and script rather than copying the snapshot in this file:

`/home/colligo/hs_scripts/claude/dotclaude/scripts/fin_check.py`

Preserve all user edits and never overwrite `FR_Portfolio!E1:K23`.
