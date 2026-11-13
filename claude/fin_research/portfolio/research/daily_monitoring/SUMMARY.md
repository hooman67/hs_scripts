# Daily portfolio review — October 13, 2026

## Contents

- [Scope and evidence](#scope-and-evidence)
- [Full price tables](#full-price-tables)
- [Sizing](#sizing)
- [Exit cost check](#exit-cost-check)
- [Interpretation and news](#interpretation-and-news)
- [Data issues and next step](#data-issues-and-next-step)

## Scope and evidence

USER-CONFIRMED scope: run fin-check, show all current holdings and watchlist names, preserve the accepted portfolio framework, and take no trading action. The explicit skill specification supplies the research scope; no new strategic allocation decision is inferred.
ASSUMED: the current live sheet is the authoritative holdings/cash/target record. It is not an independent broker or tax-lot audit. Historical research is context, not current verification.
VERIFIED observations: read FR_Portfolio and Yahoo daily history/current quote metadata on October 13 Pacific time (October 14 UTC). Calculations reconcile 70 holding rows plus cash. Quote coverage is 71 symbols dated October 13, three OTC symbols dated October 12, BTC dated October 14 UTC, and one missing URC symbol. Bitcoin lots share one price row; physical bullion is displayed separately.
Percentages use the last quote versus 1, 3, 5 and 20 prior observations. For listed securities these are trading sessions; for Bitcoin these are calendar days. Current Yahoo quote metadata fills October 13 daily bars that Yahoo returned as NaN. Prices remain vendor observations, not independently verified trade executions.
Live portfolio: https://docs.google.com/spreadsheets/d/1diOiW7fk9Q5fyyCoriON-IYN8Yc-PnrixKh2PtFwQkU
Evidence: `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/daily_monitoring/data/2026-10-13.json`
Corrected approximate total: **$683,605**; cash **$265,188 (38.8%)**. Gold and URC retain stored prices, so the denominator is approximate.

## Full price tables

Prices USD except .TO/.V tickers in CAD. Futures are per standard contract unit. An asterisk marks October 12 OTC observations.

### MACRO / COMMODITIES

| Symbol | Price | 1d | 3d | 5d | 20d |
|---|---:|---:|---:|---:|---:|
| CL=F | 94.79 | +1.1% | +3.6% | +6.0% | -10.4% |
| BZ=F | 106.35 | -0.3% | +2.0% | +5.7% | -2.2% |
| NG=F | 3.32 | +4.8% | +4.8% | +6.6% | +13.7% |
| GC=F | 4,179.90 | -0.3% | +0.6% | -0.2% | -3.5% |
| HG=F | 6.72 | +0.4% | +3.1% | +1.9% | +5.6% |

### HELD — core/sleeves (trim strength / hold)

| Symbol | Price | 1d | 3d | 5d | 20d |
|---|---:|---:|---:|---:|---:|
| KWEB | 24.72 | -0.1% | +2.9% | +0.7% | +1.0% |
| BABA | 110.85 | +0.1% | +4.9% | +1.5% | +1.4% |
| NTCPF* | 2.51 | -0.4% | +0.0% | -2.3% | -20.6% |
| COP-U.TO | 12.03 | +0.8% | +0.5% | +3.2% | +2.9% |
| GEV | 1,004.04 | +0.7% | +0.5% | -2.4% | +13.7% |
| PDBA | 37.92 | -0.2% | +0.3% | -1.5% | -1.8% |
| CF | 117.25 | +2.3% | +3.2% | +1.1% | -13.5% |
| MNT.TO | 63.37 | -0.5% | +4.0% | +2.5% | -6.1% |
| AEM | 185.61 | -1.4% | +0.9% | -0.2% | -5.7% |
| EMPYF* | 0.69 | +1.0% | -0.7% | +0.2% | +5.5% |
| XOM | 174.08 | +1.1% | +3.3% | +5.8% | +2.8% |
| CNQ.TO | 74.19 | +4.8% | +9.4% | +7.6% | +6.1% |
| SLB | 48.77 | -0.0% | -0.4% | -2.5% | -10.0% |
| TOU.TO | 65.19 | +2.0% | +4.2% | +3.5% | +5.4% |
| UNG | 11.41 | +4.5% | +5.6% | +6.2% | +8.3% |
| WPM | 136.03 | -1.5% | +0.8% | -1.2% | -9.3% |
| CRCL | 84.27 | +0.5% | +4.2% | +0.2% | -2.4% |
| AMZN | 258.58 | -0.4% | +1.8% | +0.9% | +4.1% |
| CCJ | 86.15 | +0.0% | -1.1% | -7.4% | -5.5% |
| BWXT | 138.86 | -0.8% | -2.4% | -4.7% | -5.3% |
| CEG | 295.79 | +0.6% | +3.8% | -1.5% | +13.8% |
| TSE:URC | unavailable | — | — | — | — |
| BTC-USD | 83,334.23 | +1.9% | +0.5% | +2.0% | -1.2% |
| VTI | 381.32 | -0.1% | +0.5% | -0.3% | +2.5% |
| VXUS | 84.54 | +0.1% | +0.5% | -1.5% | -1.2% |
| ETN | 428.31 | +0.4% | +0.9% | -3.8% | +9.2% |
| CCO.TO | 122.57 | -2.4% | -3.5% | -1.8% | -5.5% |
| COPX | 84.40 | -1.1% | +2.7% | -2.2% | -0.2% |
| CI | 282.53 | -0.3% | +0.5% | +3.0% | -2.2% |
| VWO | 59.68 | -0.1% | +1.0% | -1.6% | +1.0% |
| BRK-B | 520.59 | +0.6% | +1.9% | +3.0% | +0.7% |
| FFH.TO | 2,287.96 | +1.6% | +4.0% | +3.5% | +0.9% |
| LULU.TO | 4.07 | -0.4% | +2.8% | +1.2% | -6.0% |
| TTD | 12.17 | +1.9% | -1.4% | +2.1% | -18.9% |
| NKE | 35.33 | -0.1% | +1.7% | +2.1% | -2.5% |
| SHLD | 59.34 | -0.8% | +0.3% | -1.2% | -5.2% |
| VPU | 181.05 | +0.5% | +1.9% | +1.6% | +2.0% |
| JQUA | 75.71 | -0.0% | +0.5% | +0.3% | +3.1% |
| PICK | 59.91 | -0.8% | +1.1% | -2.0% | -2.5% |
| NLR | 99.38 | -0.8% | -2.9% | -9.2% | -8.3% |
| VHT | 316.37 | -1.3% | +0.8% | +1.1% | +0.9% |
| CLX | 84.45 | +0.1% | +1.2% | +1.1% | -3.1% |
| SHOP.TO | 251.04 | +3.0% | +6.1% | +10.0% | +34.8% |
| UBER | 71.32 | -0.3% | +1.5% | +3.2% | -0.2% |
| IHI | 52.69 | -0.2% | +3.1% | +3.5% | +1.8% |
| VGIT | 56.74 | +0.1% | -0.0% | +0.2% | -0.5% |
| BKR | 56.45 | +0.5% | +0.3% | -1.2% | -0.5% |
| LNG | 286.92 | +1.6% | +3.3% | +4.2% | +5.9% |
| TRMLF* | 45.18 | +0.8% | +3.2% | +2.3% | +1.6% |
| FIS | 35.20 | +2.7% | +2.5% | +5.3% | -5.7% |

### HELD — (exit) queue (sell into any bounce)

| Symbol | Price | 1d | 3d | 5d | 20d |
|---|---:|---:|---:|---:|---:|
| AA | 41.49 | -0.4% | -3.1% | -3.9% | -10.8% |
| AEVA | 12.17 | -0.3% | -11.1% | -16.5% | -14.2% |
| BIDU | 83.74 | -0.7% | -0.2% | -3.8% | -7.4% |
| MARA | 9.11 | -3.5% | -8.1% | -17.0% | -19.0% |
| CHPT | 7.22 | +0.0% | -11.2% | -16.7% | -18.1% |
| NIO | 3.56 | +2.6% | +4.4% | +2.3% | -1.1% |
| LCID | 3.35 | -2.3% | -12.2% | -19.4% | -18.6% |
| RIVN | 13.37 | -1.3% | -6.7% | -7.9% | -14.0% |
| CAG | 13.70 | +0.1% | +1.0% | +1.9% | -8.8% |
| BOIL | 22.99 | +5.2% | +7.4% | +9.9% | +12.6% |
| SBSW | 9.91 | +0.2% | +0.0% | -1.0% | -12.7% |
| CSGP | 30.00 | +2.7% | +0.6% | +8.6% | -4.9% |
| SBUX | 92.00 | -0.3% | -1.3% | -4.3% | -4.7% |
| RBLX | 49.51 | -0.1% | +8.8% | +8.7% | -1.5% |
| ARKK | 87.17 | -1.0% | -0.5% | -3.7% | +4.4% |
| ROOF.V | 0.15 | -6.2% | -9.1% | -9.1% | -3.2% |
| SQQQ | 33.98 | +1.1% | +1.8% | +6.8% | -15.1% |

### BUY WATCHLIST (underweight sleeves)

| Symbol | Price | 1d | 3d | 5d | 20d |
|---|---:|---:|---:|---:|---:|
| VTI | 381.32 | -0.1% | +0.5% | -0.3% | +2.5% |
| VXUS | 84.54 | +0.1% | +0.5% | -1.5% | -1.2% |
| VWO | 59.68 | -0.1% | +1.0% | -1.6% | +1.0% |
| JQUA | 75.71 | -0.0% | +0.5% | +0.3% | +3.1% |
| DBE | 39.04 | +1.4% | +2.7% | +5.8% | +0.1% |
| NLR | 99.38 | -0.8% | -2.9% | -9.2% | -8.3% |
| COPX | 84.40 | -1.1% | +2.7% | -2.2% | -0.2% |
| PICK | 59.91 | -0.8% | +1.1% | -2.0% | -2.5% |
| VHT | 316.37 | -1.3% | +0.8% | +1.1% | +0.9% |
| IHI | 52.69 | -0.2% | +3.1% | +3.5% | +1.8% |
| LLY | 1,166.51 | -1.4% | -0.3% | +0.8% | +2.7% |
| GLDM | 82.36 | -0.1% | +0.8% | -0.1% | -3.1% |
| SHLD | 59.34 | -0.8% | +0.3% | -1.2% | -5.2% |
| VPU | 181.05 | +0.5% | +1.9% | +1.6% | +2.0% |
| SOXQ | 96.03 | -0.3% | -3.4% | -7.7% | +9.2% |

Physical Gold: 15.86 oz at stored $4,132/oz = $65,533.52. No independently refreshed bullion quote or return series. URC: 350 shares at stored C$3.79; no verified current quote.

## Sizing

Capital-based sleeve accounting; positive gap means below target, negative means above target. These are reference gaps, not orders. WPM economic gold/silver look-through differs from this capital allocation.

| Sleeve | Current USD | Current % | Target % | Gap USD |
|---|---:|---:|---:|---:|
| Cash (50/50 USD/CAD) | 265,188 | 38.79% | 18.5% | -138,721 |
| (exit) | 18,470 | 2.70% | 0.0% | -18,470 |
| Silver/Plat | 20,949 | 3.06% | 1.0% | -14,113 |
| nat_gas | 20,926 | 3.06% | 1.0% | -14,090 |
| oil-companies | 52,062 | 7.62% | 6.0% | -11,046 |
| Speculation | 19,698 | 2.88% | 1.5% | -9,444 |
| Crypto | 18,139 | 2.65% | 2.0% | -4,467 |
| uranium/nuclear | 26,483 | 3.87% | 3.5% | -2,556 |
| grid/electrification | 11,887 | 1.74% | 1.5% | -1,633 |
| industrial_metals | 4,793 | 0.70% | 1.0% | +2,043 |
| copper | 11,370 | 1.66% | 2.0% | +2,302 |
| Financials | 10,083 | 1.47% | 2.0% | +3,589 |
| Utilities | 12,674 | 1.85% | 2.5% | +4,417 |
| Gold core | 97,546 | 14.27% | 15.0% | +4,995 |
| Defense | 2,967 | 0.43% | 1.5% | +7,287 |
| Agriculture | 12,444 | 1.82% | 3.0% | +8,065 |
| EM/China | 24,314 | 3.56% | 5.0% | +9,867 |
| ref_oil_prod | 0 | 0.00% | 2.0% | +13,672 |
| Quality compounders | 20,001 | 2.93% | 5.5% | +17,597 |
| Healthcare | 13,000 | 1.90% | 5.5% | +24,598 |
| Treasuries (VGIT) | 3,007 | 0.44% | 5.0% | +31,173 |
| Global equity core | 17,604 | 2.58% | 15.0% | +84,937 |

## Exit cost check

All 17 dashboard exit-queue holdings are BELOW COST; none clears recorded aggregate basis. Values use current quotes and recorded book USD before commissions and taxes. Tax lots can differ; RRSP losses are not deductible. AEVA account is unspecified.

| Holding | Current USD | Recorded cost USD | Nominal P/L USD | Status |
|---|---:|---:|---:|---|
| CAG | 4,005 | 5,110 | -1,105 | BELOW COST |
| RBLX | 2,476 | 3,825 | -1,350 | BELOW COST |
| BOIL | 2,299 | 2,860 | -561 | BELOW COST |
| AA | 2,074 | 3,575 | -1,500 | BELOW COST |
| NYSE:SBSW | 1,982 | 3,858 | -1,876 | BELOW COST |
| ARKK | 1,395 | 1,972 | -578 | BELOW COST |
| SBUX | 920 | 995 | -75 | BELOW COST |
| AEVA | 852 | 1,303 | -451 | BELOW COST |
| CHPT | 722 | 1,896 | -1,174 | BELOW COST |
| NYSE:NIO | 427 | 4,996 | -4,568 | BELOW COST |
| BIDU | 335 | 758 | -423 | BELOW COST |
| MARA | 273 | 1,308 | -1,035 | BELOW COST |
| SQQQ | 272 | 320 | -48 | BELOW COST |
| NorthStar Clean Tech (ROOF) | 148 | 248 | -100 | BELOW COST |
| RIVN | 134 | 590 | -456 | BELOW COST |
| CSGP | 90 | 222 | -132 | BELOW COST |
| LCID | 67 | 519 | -452 | BELOW COST |
| TOTAL | 18,470 | 34,354 | -15,884 | BELOW COST |

URC also appears in the user-maintained sell notes, but remains in the uranium sleeve rather than the dashboard exit queue. Its stored valuation is about $933 versus recorded cost $748 (apparent gain about $185); this is UNVERIFIED at current prices and cannot establish that a current sale would avoid a loss.

## Interpretation and news

ASSUMED phase read, moderate confidence: renewed Phase-1-like energy strength, with no verified Phase-2 demand-destruction signal in this daily review. WTI is about $94.79 and Brent $106.35; both are up roughly 6% over five sessions. WTI remains down 10.4% over 20 sessions, so one week does not prove a lasting renewed upcycle. Broad recession/inflation indicators were not fully refreshed; keep the VGIT staging gate rather than infer an all-clear.
REPORTED news: Zacks October 13 market recap describes October 12 energy gains amid Saudi security concerns and hawkish comments from Cleveland Fed President Hammack. Its prior-day WTI $93.74/Brent $106.65 magnitudes are compatible with this run. Fortune October 13 separately reported Brent $107.29 at 7:45 a.m. Eastern; the difference reflects timing. These provide an energy/rates backdrop, not proof of a company-specific catalyst.
- https://www.zacks.com/stock/news/3006095/stock-market-news-for-oct-13-2026
- https://fortune.com/article/price-of-oil-10-13-2026/
CNQ issuer news page was inspected; no fresh October 13 corporate announcement was identified: https://www.cnrl.com/investors/news-releases/
Zacks reports SHOP U.S. listing down 1.51% October 13 but up 33.86% over the month. The Canadian listing compares against October 9 because October 12 has no TSX session in the series; do not interpret the differing daily returns as conflicting company news. Earnings November 3 is a reported expected date, not an independently verified issuer schedule: https://www.zacks.com/stock/news/3006426/shopify-shop-falls-more-steeply-than-broader-market-what-investors-need-to-know
UNVERIFIED catalysts: no adequate fresh company-specific explanation was obtained for the weekly nuclear/semiconductor decline, RBLX/CSGP bounce, FIS move, or the weak EV/speculative exit names. Yahoo news returned empty arrays; targeted DuckDuckGo searches mainly returned quote pages or commentary. The Reuters October 13 oil article returned HTTP 401; the U.S. News Reuters OPEC syndication timed out. Do not manufacture causal explanations.

Conditional portfolio context (ASSUMED interpretation of USER-CONFIRMED rules):
- CNQ +4.8% today and +7.6% over five sessions: an approximately $11,046 oil-company sleeve excess creates a trim-on-strength discussion. CNQ alone is about $30,692. Do not add LNG/BKR/TRMLF on top without resolving the same sleeve constraint; TOU and TRMLF are one issuer.
- UNG +4.5% today: about $20,926 versus $6,836 target, or $14,090 excess. BOIL +5.2% today is separately a $2,299 exit holding, still $561 below cost. These are the clearest natural-gas strength observations; natural-gas fundamentals were not independently refreshed.
- Gold/AEM/GLDM are weaker over 20 sessions. Gold capital gap is about $4,995; GLDM remains the accepted new-money vehicle. WPM is down 1.5% today and 9.3% over 20 sessions, so no automatic weakness-driven trim. WPM capital excess over the 1% silver sleeve is $14,113, but excess against its 1.92% company/look-through target is about $7,823; those are different accounting bases.
- COPX -1.1% today: copper sleeve gap about $2,302. Agriculture gap $8,065: approximately $7,794 belongs to PDBA and only $270 to CF at its 1% cap. Preserve the accepted staged entries and fundamental checks.
- NLR -9.2% over five sessions does not authorize a net sleeve add: uranium/nuclear is already about $2,556 above target. NLR is about $8,763 below its individual 1.5% target; combined CCJ/CCO direct exposure is about $17,665 versus the accepted 1% issuer cap of $6,836. Any NLR increase should be considered within the existing substitution plan and with fresh fundamentals.
- SHOP is strong over its Canadian comparison window, but Speculation is about $19,698: $9,444 above the percentage target and $9,698 above the standing $10,000 hard cap. FIS remains unresearched; a weekly gain is not an add authorization.
- Other weaker underweight sleeves remain visible: SHLD/Defense gap $7,287; VHT/IHI/CI/LLY Healthcare gap $24,598; PICK gap $2,043; VWO/EM gap $9,867. JQUA/quality capital gap is $17,597. Treat these as staged capacity, not immediate orders. LLY $1,166.51 remains above the accepted approximately $1,050 reassessment gate.
- VGIT target remains 5%; about $3,007 held leaves $31,173 unfilled. Global equity remains 15% with an $84,937 gap. Keep the inflation/yield gate and the deliberate cash decision; neither shortfall is an instruction to deploy the full cash pile.

**Melt-up / cash-drag watch: reaffirm the wait explicitly.** The fast-rally triggers do not fire: VTI is +2.5% over 20 sessions / +4.4% over 60, at 99.5% of its observed 52-week closing high, with only two of the last four completed weekly returns positive. However, the cash-heavy policy has persisted since July while equities advanced and current cash remains 38.8%. That makes the duration-of-wait counter-check relevant: consider measured core DCA or consciously reaffirm the wait. Some cash has been deployed, cash interest was not measured, and recession absence was not established; do not equate the full equity return with net cash drag.

**SOXQ research watch: WAIT at $96.03**, $11.03 above $85. Reassess fundamentals at or below $85 for up to 0.5% (about $3,418); near $79–$80 for a second tranche, capped at 1% (about $6,836). Funding substitutes for VTI/JQUA; no new permanent sleeve.

## Data issues and next step

VERIFIED calculation corrections in this report: (1) read the complete live allocation grid, including 5% VGIT, so targets sum to 100%; (2) value all BTC-USD quotes in USD regardless of original lot currency; (3) incorporate dated current quote metadata when daily history omits the current bar; (4) calculate true 20-observation returns rather than use the first row of a one-month download. The shared monitoring script was not changed.
UNRESOLVED: physical gold static valuation; unavailable URC quote; three OTC quotes dated October 12; recorded basis/account accuracy; CCJ name target erroneously reads 60%; quality target differs between accepted September decision and current sheet. Follow the live sleeve grid for this display, but do not use the invalid CCJ name target or infer approval of a changed quality strategy.
Environment setup is complete: existing Google key securely copied to the configured location; documented Python dependencies installed; read-only client test succeeded. Memory stores key paths only. No trades, live-sheet edits, or changes to existing investment decisions were made.
Next exact step for another daily run: use the configured key and current FR_Portfolio, recheck quote timestamps, include all allocation rows, and retain the valuation corrections above. Fixing the reusable monitor and reconciling inconsistent investment targets are separate follow-ups; do not silently change the sheet.

Evidence SHA-256: `1857eedeaebcc688f0fe3cc8fe7545f8611498b1c37015f5c9a92614cdf01c65`
