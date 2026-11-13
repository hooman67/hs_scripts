# Portfolio allocation and macro audit — October 14, 2026

**Status: COMPLETED REVIEW — PENDING USER REVIEW OF PROPOSALS.** Full allocation/assumption validation requested by Hooman, with current primary-source checks and all available recorded transaction history. No trades, live-sheet changes, or canonical investment-policy changes were made by this audit. Earlier research remains preserved.

**Verdict: retain the inflation/currency-diversification objective; revise the portfolio construction and the confidence attached to the old research.** Gold, some real-asset exposure and a distinct Treasury hedge are defensible. The exact collection of targets is not a demonstrated optimum, utilities are not safe house capital, and the current cash buffer does not make the fully invested destination safe. Several earlier recommendations assumed incorrect personal facts or overstated what their evidence proved.

This report separates evidence from judgment. **USER-CONFIRMED** means your stated circumstances; **VERIFIED** means directly checked source content or current sheet entries, not an independent audit of the source institution; **REPORTED** identifies issuer/vendor data; **DERIVED** identifies arithmetic; **ASSUMED/JUDGMENT** identifies scenarios and recommendations. Missing data remain **UNVERIFIED**. Confidence is claim-specific, not a numerical portfolio score.

## The conclusions that change the decision

1. **You have substantial protection today, principally from cash; the target would materially reduce it.** The refreshed tracked portfolio is about **$678,041**, including **$262,215 cash (38.67%)**. The destination is **18.5% cash**, approximately **$125,438**. That destination cannot be endorsed before a reserve amount and acceptable house-purchase delay are chosen. A conditional house purchase makes some risk reasonable; an expectation that prices will fall does not make the invested money safe.
2. **Inflation concern is justified, but a single deterministic stagflation path is not.** September CPI accelerated, payroll growth slowed, and energy inventories are tight. Q2 GDP and August real spending still grew, core annual CPI is 2.56%, and market inflation compensation remains far below a currency-collapse path. Build for both inflation and recession instead of assuming the portfolio can rotate perfectly between them.
3. **The main risk-control failures are measurable.** Speculation is **$22,571 versus a $10,000 hard cap**; UNG is **3.03% versus 1%**; combined Cameco listings are **2.46% versus the accepted 1% direct-issuer target**, before NLR overlap. Seventeen exit holdings remain worth **$17,993**. None requires a precise macro forecast to identify.
4. **Gold is useful but does not replace inflation-linked government bonds or emergency cash.** The old decision to replace VTIP with gold relied partly on gold being excellent in both phases of stagflation. That is too strong. WGC reports gold fell 8.5% in September even as ETF inflows were strong. Reconsider short/maturity-matched TIPS if purchasing-power protection is truly the first priority; the existing no-VTIP preference is preserved until you choose otherwise.
5. **The old Adobe and tax assumptions need correction.** Your extract shows **$13,940.52 sellable**, with **$355,837.68 unvested**. The latter is contingent compensation, not house money. California taxes annual RRSP earnings even when federal treaty deferral applies. At least **$76,314** in identified RRSP positions/cash is included in the tracked total, plus portions of mixed-account rows; the whole $678k is not automatically spendable after-tax cash.
6. **A plausible adverse scenario loses six figures.** The stated demand-recession shocks produce about **$146k loss currently** and **$163k at the live targets**. A simultaneous liquidation/rate-shock scenario produces about **$175k/$198k**. These are deliberately adverse examples, not forecasts, probabilities or maximum possible losses. They invalidate the old blanket assurance that a correction cannot compromise a purchase.

## Your circumstances and the remaining assumptions

The five diagnostic questions have already been answered; they are not being asked again. The analysis uses:

- Inflation/currency protection first; recession protection second; house/job security third. No growth-first objective is imposed.
- A conditional purchase in roughly 2–3 years, probably not 2027. You would use this portfolio except emergency funds. No assumed purchase price, mortgage approval or guaranteed fall in local house prices.
- CAD250,000 with your father is separate and available, per you. At the snapshot FX rate it is about **USD175,650**. Ownership, instrument, access time and transfer/tax treatment are unverified. It is counted separately, never twice as both house money and emergency money.
- U.S./California residence, married filing jointly, one income, dependent spouse currently unable to work. Canada is a contingency rather than a planned 3–5-year move. No assumption of Canadian salary or Canadian tax residency.
- No other major assets/debts reported. Adobe's 1,360 cumulative vested shares are not assumed still owned. The 59 sellable shares are outside the sheet; their quoted value is your supplied extract, not a fresh broker valuation. Excluding unvested RSUs, tracked assets plus sellable Adobe plus the family reserve total about **$867,631 gross**, subject to the above access/tax limits.
- Essential monthly spending, health-insurance/relocation costs, tax reserves, house funding requirement and tolerance for delaying the purchase remain unknown. A short spending/access question was asked; tables below show sensitivities rather than filling those gaps with invented facts.

**Judgment:** use 12–18 months of essential expenses plus a separately estimated relocation/insurance/legal buffer as the initial reserve discussion for this one-income household. The exact number is a choice, not a universal rule. Do not rely on severance, continued RSU vesting or instant access to family funds unless verified.

## Data quality and what the live targets actually say

Live Google Sheet `FR_Portfolio` was re-read October 14. Dated Yahoo metadata prices were retrieved through **20:33 UTC / 13:33 Pacific**; they are monitoring quotes, not execution prices. There are **71 positive holding rows**. Physical gold **15.86 oz / $65,534** and old URC **$932** retain stored marks. The other rows have October 14 metadata timestamps; a timestamp does not prove that an illiquid security traded at that instant. Cash was translated at **0.7026 USD/CAD**. Account balances/quantities remain user-maintained records, not broker reconciliation.

The raw sheet showed about $672,083 at its own marks. The corrected quote snapshot is $678,041; different quote times and currency handling explain why these should not be treated as identical valuations. Source, raw sheet, quote currency/date, calculations and limitations are retained in the data directory.

**Verified defects/conflicts:**

- The standard `fin_check.py` target parser omits the new 5% VGIT sleeve and returns only 95%. This audit read the whole grid and verified 100%; a 95% output is not a complete allocation.
- A CAD cost record for Bitcoin does not turn the USD coin quote into CAD. Likewise `COP-U.TO` quotes in USD despite the sheet's CAD label. The audit uses quotation currency, converting once.
- The dashboard still shows a **hardcoded 6.5% annual volatility** and a blanket non-cash-minus-30% illustration. Neither is a freshly estimated risk model or a loss ceiling.
- The live quality target is 5.5%, while the accepted September 8 composition is 3.5% JQUA + 1.5% AMZN = 5%. Per-name cells have further discrepancies, including a CCJ value of 0.6 in the earlier live review. Reconcile the applicable rule before sizing an order.
- A table that mixes capital weights with WPM revenue look-through can sum to 100% without describing an implementable portfolio. The $10,000 speculation cap also overrides 1.5% whenever the dollar cap is smaller; at this total the effective cap is about **1.475%**, with the difference retained in cash.
- The title and lower 'FINAL TARGET' sections in `ideal_allocation.md` contain superseded figures. Current accepted VGIT is 5%, funded by reducing the global target to 15%; it is not still merely an unapproved October 1 idea.

No protected notes (`FR_Portfolio!E1:K23`) were changed.

| Sleeve | Current USD | Current % | Live target % |
| --- | --- | --- | --- |
| Cash (50/50 USD/CAD) | $262,215 | 38.67% | 18.5% |
| (exit) | $17,993 | 2.65% | 0% |
| Silver/Plat | $19,955 | 2.94% | 1% |
| nat_gas | $20,577 | 3.03% | 1% |
| oil-companies | $51,945 | 7.66% | 6% |
| Speculation | $22,571 | 3.33% | 1.5% |
| uranium/nuclear | $25,188 | 3.71% | 3.5% |
| copper | $11,385 | 1.68% | 2% |
| grid/electrification | $11,214 | 1.65% | 1.5% |
| Crypto | $17,679 | 2.61% | 2% |
| industrial_metals | $4,678 | 0.69% | 1% |
| Gold core | $96,931 | 14.30% | 15% |
| Financials | $10,119 | 1.49% | 2% |
| Utilities | $12,624 | 1.86% | 2.5% |
| Defense | $2,984 | 0.44% | 1.5% |
| Agriculture | $12,536 | 1.85% | 3% |
| EM/China | $24,075 | 3.55% | 5% |
| ref_oil_prod | $0 | 0.00% | 2% |
| Quality compounders | $19,718 | 2.91% | 5.5% |
| Healthcare | $13,239 | 1.95% | 5.5% |
| Treasuries (VGIT) | $3,010 | 0.44% | 5% |
| Global equity core | $17,402 | 2.57% | 15% |

## Economic exposures: labels hide several different risks

- **Bullion versus companies:** physical gold plus MNT is about **13.49%**; AEM/Empress add **0.81%** gold-linked equity. WPM is another **2.94% company position**, not direct silver/platinum. Its opened Q2 filing reports revenue 52% silver/46% gold; H1 was 49%/49%. At current size those mixes imply about **1.44%–1.53% silver** and **1.35%–1.44% gold revenue exposure**. These are illustrative revenue allocations, not exact price betas or principal protection. Platinum is not supplied. Applying a 1% capital target to all WPM would overstate the required trim relative to the accepted economic target.
- **Duplicate issuers:** CCJ plus CCO.TO = **$16,703 / 2.46%**. TOU.TO plus TRMLF = **$3,726 / 0.55%**. SLB plus BKR = **$6,333 / 0.93%** services exposure. Different listings do not diversify the issuer.
- **NLR overlap:** opened VanEck holdings dated October 13 show CEG **9.89%**, CCJ **8.43%**, BWXT **6.53%** of NLR. Adding NLR diversifies the nuclear basket but also adds to those existing names. Current overlap is small because NLR itself is only about 0.21% of the portfolio; it grows when funded to target.
- **Cameco's industry thesis does not establish a cheap share:** the opened July 31 Q2 release reports lower H1 earnings/adjusted EBITDA than 2025, partly because a large prior-year Westinghouse contribution did not recur. Long-term contracting improved. Neither the old 78x forward multiple nor a current buy valuation was freshly established; the concentration finding does not require either.
- **Futures versus businesses:** UNG targets daily near-month futures changes plus collateral interest, less expenses. LNG demand growth is not a guarantee of UNG holding-period returns; supply, weather and roll structure matter. PDBA is a crop/livestock futures strategy, CF a nitrogen business. DBE's historical broad-energy mandate is not a pure diesel position; its current contract weights/roll economics were not recovered sufficiently to endorse an entry.
- **Crypto versus an operating company:** direct Bitcoin is about **2.14%**. CRCL adds **$3,182** operating/equity risk under the Crypto label. Counting it with venture/speculative exposures gives about **3.80%**, though that is an analytical view, not a retroactive change to the accepted cap classification.
- **Sector equity is still equity:** utilities, insurers, healthcare and defense can diversify business drivers but can all lose money in recession/liquidation. Broad funds already contain many of these businesses. More separate sleeves do not prove additional risk reduction.
- **FX:** actual cash is about **$255,997 USD plus CAD8,851**, not 50/50. Your separate CAD250k already supplies meaningful Canada contingency currency. A Canadian listing of a global commodity producer is not the same hedge as CAD cash.

The design contains several independent economic mechanisms; it is inaccurate to claim that all commodities always move together. It is nevertheless heavily exposed to resource prices and capital-intensive equities, which can suffer together in demand destruction. Their exact correlations vary by regime.

## Fresh macro evidence and full thesis register

The complete opened evidence, exact excerpts and access failures are in the separate primary-evidence report. Publication of a forecast is verified; its eventual outcome is not.

| Indicator | Fresh observation | Decision implication |
| --- | --- | --- |
| September CPI, released Oct 14 | Headline +0.65% monthly / +3.74% yearly; core +0.33% / +2.56% | Inflation pressure strengthened; do not annualize one month into a permanent forecast |
| September employment, released Oct 2 | +29k payrolls; July–September +152k combined; unemployment 4.2% | Slowing labor demand; not by itself proof of recession |
| Q2 GDP / August real spending | GDP +2.2% annualized; real PCE +0.6% monthly | Positive but lagging counterevidence to economy-wide stagnation |
| Fed September policy / SEP | Policy 3.75%–4%; projected 2027 GDP +2.4%, PCE +2.3% | A competing positive-growth/disinflation case, not a guarantee |
| 10-year breakeven, Oct 13 | 2.33% | Inflation compensation is far below a literal dollar-collapse path; includes risk/liquidity premia |
| EIA October STEO | 2027 Brent $84, raised from $74; Q4 2026 $105 | Higher forecast prices, including during normalization; conditional forecast with Oct 1 cutoff |
| Gas storage, Oct 2 week | 3,500 Bcf; +2% vs five-year average, -3.6% vs last year | No nationwide scarcity confirmation; regional constraints can coexist |
| Gold ETF flows, September | +$10bn / +67t; record Q3 inflows, yet gold price fell | Old Q2 outflows are stale as a current-flow argument; inflows are not a floor |
| Commodity breadth, September averages | Energy +25.7%, nonenergy +1.3%, agriculture +1.6%; precious metals down | Breadth extends beyond oil, but a month of prices does not establish a decade supercycle |
| China latest opened activity | Manufacturing PMI 50.1; Jan–Aug investment -7.2%, property -19.9% | Industrial strengths coexist with domestic weakness; cheapness needs security-level evidence |

The original factual basis and falsification tests are included in the register below. Recorded convictions come from the earlier report; **NR** means not separately recorded, not low conviction. Confidence grades apply to the specific economic claim, not its ability to predict investment returns. Every decision-driving belief was challenged in this full review; where a fresh source or security valuation could not be verified, the result is unresolved rather than silently carried forward as verified.

| Thesis | Recorded conviction | Evidence confidence | Verdict | Original basis → new evidence | Expression and falsification |
| --- | --- | --- | --- | --- | --- |
| Literal USD loses 70% in 10 years | High | Low | Unsupported magnitude / revise | Deficits, debt and reserve diversification; now breakeven 2.33%, dollar index121.60 | Gold/foreign assets; require evidence of sustained extreme inflation/FX deterioration, not a reserve-share headline |
| Purchasing-power erosion / currency diversification | High | High mechanism; medium sizing | Retain | Positive inflation compounds; liabilities and tax affect hedge choice | Gold, foreign earnings, possible TIPS; invalidate a particular hedge if it fails the relevant liability rather than a dollar slogan |
| Broad commodity supercycle | High | Low–medium | Unresolved; price breadth stronger | Underinvestment/electrification; September nonenergy also rose | Resource sleeves; need multi-year inventories/capex/curves across sectors; supply response/demand contraction weakens |
| Oil constraints | High | Medium–high tactical | Strengthened tactically | Underinvestment plus disruption; October EIA revised oil upward | Oil6% target; persistent outage/inventory decline confirms; restored flows/demand destruction weakens |
| Canadian energy relative advantage | High | Medium business; low excess-return | Conditional | Past policy/transport advantages; current relative valuation not freshly proven | CNQ/TOU; test realized differentials, capex/FCF after royalties; relative underperformance alone not falsification |
| Refined-product tightness | Medium | High inventories; medium investment | Retain conditionally | East Coast distillates32% below seasonal mean; EIA expects gradual recovery | DBE2% planned; persistent cracks support; normalized inventories/expensive roll weaken; no pure-refined assumption |
| Gas LNG/data-center growth | Medium | Medium | Long-run demand plausible; scarcity unconfirmed | EIA exports rise but production offsets; endOctober storage forecast +2% average | UNG3.03% actual vs1%; persistent storage deficits confirm; output/inventory surplus weakens |
| Copper/grid bottlenecks | High | Medium physical need; low timing/valuation | Conditional | Electricity investment and old long mine lead-time evidence; current IEA access failed | Copper/PICK/GEV/ETN; verify orders, costs, supply and substitution; do not call old2030s deficit current shortage |
| Gold monetary/fiscal hedge | High | Medium–high role; low timing | Retain, remove guarantee | Official/ETF demand supports; September -8.5% price despite inflows | Bullion target about15%; flows/real rates/FX matter; gold is not short-horizon CPI insurance |
| Uranium/nuclear/AI power | High | Medium | Conditional, issuer concentration excessive | EIA power demand/issuer contracting supports; Cameco H1 profits lower YoY | NLR/CCJ/CEG/BWXT; fuel contracts/cash flows confirm; cancellations, dilution or price-over-earnings assumptions weaken |
| AI economically real, valuations risky | High | Medium | Retain with valuation caveat | EIA commercial electricity growth includes data centers but also weather/other demand | Adobe work, broad/quality/grid; need incremental profits/FCF after capex, not revenue/capex alone |
| Oil as an AI-power proxy | Medium | Low | Reject oil-specific shortcut | Old indirect link; current EIA separates power fuels and demand | Gas equipment/power are more direct; oil holdings need an oil-business case |
| China/EM diversification/value | Medium–high | Medium diversification; low cheapness | Conditional | Valuation discount is not enough; fresh NBS property/consumption weakness | VWO/KWEB/BABA; need earnings/governance/access evidence; broad EM is not equivalent to China internet |
| China clean-energy exports | NR | Medium industrial; low investability | Watch, unresolved | High-tech manufacturing strong; security access/valuation unverified | No automatic new satellite; test margins, trade restrictions and shareholder returns |
| Two-phase stagflation base case | High | Medium risk; low precise path | Revise to risk scenario | Oil shock plus weaker jobs raises risk; GDP/real spending still positive | Cash/gold/resources; both inflation and sustained stagnation needed; do not presume timely rotation |
| Fertilizer/Hormuz shortage | Medium | Medium historical; low current blanket shortage | Nutrient-specific / conditional | World Bank fertilizer index nearly flat September; CF page currently403 | CF/PDBA; verify nitrogen realized prices/feedstock versus potash/phosphate, not all-fertilizer extrapolation |
| Agriculture diversification | Medium | Medium | Retain as risk asset | Different weather/harvest drivers; food prices firmer | PDBA/CF; crops and futures total return require inventory/roll checks; not capital protection |
| Nominal Treasury recession hedge | Medium | High mechanism; medium timing | Retain accepted5%, not principal guarantee | VGIT duration4.9 years in June factsheet; 2022 return -10.53% | Rate declines help; term-premium/inflation increases hurt; 5% sleeve cannot offset a large equity crash |
| Tactical semiconductor entry | Medium | Medium industry; low price gate | Watch | Previous SOXQ price triggers are execution rules, not intrinsic value | No new holdings; use existing equity risk budget if accepted, not emergency cash |
| Utilities/healthcare/insurance defense | NR | High classification; medium allocation | Retain optional tilts, reject safe-asset label | Old utilities-as-Treasury claim contradicted by 2020 -36.4% VPU drawdown | All equity; earnings resilience helps but does not prevent market losses |
| Defense spending/AI weapons | NR | Medium structural; low current valuation | Optional capped equity tilt | Old spending/backlog evidence not newly independently revalued this run | SHLD1.5%; require funded orders/cash conversion versus multiples; no defense label for ASTS |
| Dividend income as a separate edge | NR | High mechanism | Reject free-return inference | Cash distribution is part of total return; issuer cash-flow yield is not dividend yield | No extra oil names simply for yield; test payout coverage/taxes |
| Options income overlay | NR | High mechanics; low extra-return claim | Conditional execution only | Covered calls cap upside; cash-secured puts retain downside on assignment | No new systematic income sleeve; size full risk, not just collected premium |
| Crypto as currency protection | NR | Low reliable hedge | Small optional risk capital | BTC has no contractual inflation linkage; CRCL is an operating company | Do not count either as job/house reserve; tolerate large independent drawdown |
| Gold replacing short TIPS | High preference | Low equivalence | Reconsider prior rationale | July26 chose gold over VTIP; Treasury principal links to CPI, gold does not | No preference override; optional TIPS comparison below; maturity/purchase-price/tax caveats apply |
| Cash50/50USD/CAD | NR | Low universal target | Replace arbitrary split with liabilities | Old undecided house location; now USresident with separateCAD250k | Keep required USD liquidity; CAD fallback sized to CAD expenses rather than listing currency |
| Cash pause until recession | High recorded rule | Low timing edge; high reserve value | Separate reserve from tactical forecast | July26 explicitly paused global-equity deployment; waiting was authorized | Use a bounded reserve/risk budget; no promise of buying after a crash at lower prices with intact employment |

**USD arithmetic:** a 70% domestic purchasing-power loss in ten years requires prices to rise 3.333-fold, or about **12.79% inflation annually**. A 70% FX decline means about **11.34% annual depreciation** against the named comparator. A loss relative to gold is different again. Current data do not support using any one of those magnitudes as the base allocation input. The long-horizon claim is not logically disproven by one strong week in the dollar; it is unsupported at that magnitude. Current IMF COFER was inaccessible, so no stale reserve-share percentage is presented as fresh.

## Risk tests: actual holdings versus the destination

**Method:** apply explicit assumed immediate USD-value changes to every current holding's economic category, and repeat for the target and alternatives. Non-cash shocks are assumed total USD-value moves; foreign-price and FX components are not independently modeled. CAD cash receives a separate FX shock, and the family reserve is tested separately. This is not a full currency-factor model of company earnings or foreign-fund holdings. Interest/dividends, subsequent inflation accrual, fees, tax, trading costs and rebalancing are excluded from these acute mark-to-market tests. They are not one-year expected total returns or probabilistic estimates. The existing portfolio was not fitted to a preferred answer.

The live-target approximation treats the 18.5% cash as USD and the 15% gold target as bullion. This is favorable to liability matching and avoids pretending the inconsistent WPM/quality cells define a unique executable portfolio. If the cash label were literally implemented 50/50, a 15% CAD depreciation would subtract another **1.39 percentage points / $9,408** from that target in the adverse FX scenarios. Speculation's dollar-cap rounding and WPM's economic/capital discrepancy are left visible above.

The 'simpler same safe fractions' alternative keeps the target's cash18.5%, gold15% and nominal Treasuries5%, and uses global equity56.5% plus broad commodities5%. It isolates some complexity costs without claiming equal volatility. The two reserve-led examples reduce risky capital; their improvement is mostly due to that decision, not to fewer ticker symbols.

| Portfolio | Demand recession | Inflation + rates | Joint liquidation | Disinflation recovery |
| --- | --- | --- | --- | --- |
| Current | -21.5% ($-145.8k) | +0.1% ($+0.9k) | -25.8% ($-175.0k) | +1.4% ($+9.3k) |
| Live targets (USD cash) | -24.0% ($-162.7k) | -2.3% ($-15.6k) | -29.2% ($-198.2k) | +5.0% ($+33.9k) |
| Simpler same safe fractions | -22.5% ($-152.7k) | -4.7% ($-32.0k) | -25.8% ($-174.8k) | +8.3% ($+56.3k) |
| Reserve-led, no TIPS | -9.8% ($-66.1k) | +0.8% ($+5.1k) | -13.0% ($-88.1k) | +1.0% ($+6.8k) |
| Reserve-led, with TIPS | -9.3% ($-63.4k) | -0.2% ($-1.2k) | -14.0% ($-94.9k) | +1.2% ($+8.1k) |

**Interpretation:** the current resource tilt helps in the assumed inflation scenario. Merely replacing themes with more broad equities would weaken that result and does not solve the house-capital problem. The fully funded targets remain exposed to large losses. In a joint liquidation, bullion and Treasuries are allowed to fall too; the analysis does not assume all hedges work simultaneously. Actual losses can be worse.

**Sensitivity:** a 10-percentage-point worsening of the assumed return on each current non-cash asset would subtract about **6.13 percentage points / $41,583**. If gold rose 10% instead of falling 10% in the recession scenario, current results improve by about **2.70 points / $18,291**, still leaving a material loss. If VGIT failed to rally, a 5% target adds only 0.5 percentage points less protection than the +10% bond scenario. A small bond sleeve cannot neutralize a large risk book.

Historical cross-checks below are observed fund outcomes from adjusted Yahoo closes, not a backtest of today's portfolio. '2020 drawdown' is each fund's own peak-to-trough loss within that calendar year; those extrema need not occur on the same dates and must not be added as a portfolio return. The 2022 column includes the vendor's dividend/split adjustments. These windows test concrete hedge claims; they are not an exhaustive history or a volatility calibration.

| Proxy | 2020 maximum drawdown | 2022 calendar total return |
| --- | --- | --- |
| COPX | -53.26% | -0.76% |
| DBC | -35.15% | 19.34% |
| GLD | -14.04% | -0.77% |
| UNG | -50.23% | 12.89% |
| VGIT | -2.31% | -10.53% |
| VPU | -36.42% | 1.06% |
| VTI | -35.00% | -19.52% |
| VTIP | -6.27% | -2.94% |

## Choosing your tolerable loss and reliable reserve

A temporary loss matters because it can become permanent if you must sell after job loss or for a house. Start with three choices: essential spending coverage, minimum after-tax house funding, and whether you would delay the purchase after a market decline. A psychological percentage alone cannot answer this.

The following reserve examples include an **ASSUMED $25,000 extra buffer** for health insurance, relocation, legal costs and other transition needs. Replace it with your actual estimate; do not add it twice if included in monthly expenses. Known tax bills are additional.

| Essential spending/month | 12 months + $25k | 18 months + $25k |
| --- | --- | --- |
| $5,000 | $85,000 | $115,000 |
| $8,000 | $121,000 | $169,000 |
| $10,000 | $145,000 | $205,000 |
| $12,000 | $169,000 | $241,000 |

At $10k/month, a 12-month reserve is **$145k** and an 18-month reserve **$205k**. Current cash covers both illustrations; the **$125k destination cash target does not**. This is why the reserve must be a dollar floor before cash is called excess or tactical dry powder. Keep an immediately accessible operating amount, with the rest in instruments maturing when needed. Do not lock the entire emergency reserve into a nonredeemable GIC or depend on selling a bond fund at a favorable price.

The table below subtracts a $145k example reserve and assumes no other cash flow. It excludes Adobe and the family reserve. **These are gross balances, not spendable house proceeds:** RRSP restrictions/withdrawal taxes, taxable gains, closing costs and reserves for tax must still be deducted.

| Portfolio loss | Dollars lost | Portfolio remaining | Gross remainder after $145k reserve |
| --- | --- | --- | --- |
| 0% | $0 | $678,041 | $533,041 |
| 5% | $33,902 | $644,139 | $499,139 |
| 10% | $67,804 | $610,237 | $465,237 |
| 15% | $101,706 | $576,335 | $431,335 |
| 20% | $135,608 | $542,433 | $397,433 |
| 25% | $169,510 | $508,531 | $363,531 |

**Provisional recommendation, not an assumed preference:** use a **10%–15% loss budget ($68k–$102k)** as the initial discussion range, given one income and a potential near-term use of most assets. The current and destination adverse scenarios exceed that range. If you decide that a $150k–$200k decline is acceptable because you would comfortably postpone the house, a larger risk budget is coherent; it should be an explicit choice rather than hidden behind a 6.5% volatility cell. If even a $68k loss is unacceptable, protect more of the potential purchase amount by maturity/currency and reduce the risky allocation further.

A falling house market need not rescue the plan. A cheaper house may coincide with job loss, stricter mortgage underwriting, higher mortgage rates and falling investments. Without a specific house price and financing plan, neither an offsetting house decline nor a minimum required portfolio can be calculated.

**Canada contingency:** CAD250k remains CAD250k if held in a nominal CAD-safe instrument, but its USD value falls from $175,650 to about **$149,303** under a 15% CAD decline. Do not call it guaranteed USD house capital. Conversely, CAD spending after a move is naturally matched by that reserve. Access delay matters as much as denomination for the first months after job loss.

**House funding formula:** require `available after-tax assets − emergency/tax reserves ≥ down payment/purchase amount + closing/moving costs`. Assets that must meet this floor on a particular date should mature by that date. A market loss tolerance is permissible only for the residual or if delaying the purchase is acceptable.

## Allocation alternatives for review

There is no evidence that one exact percentage vector is optimal. These are coherent 100% illustrations to expose the trade-offs; they are not orders and do not override your existing no-VTIP or sleeve preferences.

| Economic role | Current live destination | Reserve-led, respect no-TIPS preference | Reserve-led, reconsider TIPS |
| --- | --- | --- | --- |
| USD operating cash / short Treasury ladder | 18.5% cash, currency label unresolved | 55% | 35% |
| Short / maturity-matched TIPS | 0% | 0% | 20% |
| Intermediate nominal Treasuries | 5% VGIT | 5% | 5% |
| Bullion monetary hedge | 15% gold label, implementation mixed | 15% | 15% |
| Broad global equity | 15%, plus many separate equity sleeves | 20% | 20% |
| Broad commodity-risk budget | Multiple sleeves; not directly comparable | 5% | 5% |
| Other equity/speculation themes | 46.5% residual across existing sleeves | 0% outside above budgets | 0% outside above budgets |
| Total | 100% | 100% | 100% |

**How I would use this comparison:** prefer the reserve-led structure if the 10%–15% loss-budget discussion reflects your capacity. With inflation protection first, the TIPS version is the stronger liability-matching candidate to investigate, provided you are willing to revisit the July preference. The no-TIPS version is included because that preference is real; its larger nominal balance is more exposed to persistent after-tax inflation. Neither is claimed immune to losses or U.S. policy risk.

For an uncertain 2028–2029 purchase, an individually maturity-matched Treasury/TIPS ladder is more precise than a perpetual bond ETF. New TIPS are issued at 5/10/30-year terms; shorter remaining maturities require existing issues in the secondary market. VTIP is a convenient diversified proxy but is not a bond that matures on your house date. The scenario uses a 2.3-year duration short-TIPS proxy; a specific ladder would need its own prices and cash flows.

The illustration's 5% commodity budget may be implemented broadly or with selected existing exposures; it does **not** automatically reinstate the rejected BCI decision. Likewise, if you retain nuclear, healthcare, defense, individual quality stocks or speculation, carve them out of the stated risky budget rather than adding them on top. Keep the speculation ceiling at the lower of 1.5% and $10k unless you deliberately revise it. Existing lots, tax costs and account access may justify a gradual transition or a different mix.

**Simplification alone is insufficient.** The same-safe-fractions alternative still lost about 22.5% in the recession example. The substantive decision is how much money can fluctuate, not whether it is held in 5 funds or 70 rows. Broad equities remain valuable long-horizon productive assets and diversification; their expected long-run role does not make 2–3-year house money safe.

## Tax, instruments and after-tax purchasing power

- **Treasury bills:** TreasuryDirect confirms federal income tax on interest and exemption from state/local income taxes. Matching maturities stabilizes nominal dollars due at those dates, subject to sovereign/operational risk. Selling early exposes market price; fund NAVs fluctuate.
- **TIPS:** principal tracks U.S. CPI; principal may decline with deflation. Treasury pays at least original par at maturity, not necessarily your secondary-market purchase price or accrued inflation premium. Interest and inflation accretion can create annual federal tax, including accretion not yet paid in cash. No direct hedge for CAD FX, gold prices or your exact Bay Area housing basket. They are a better contractual CPI match than a gold-price forecast, but not a perfect after-tax real guarantee.
- **Duration:** Vanguard's June 30 factsheets report VGIT duration **4.9 years** and VTIP **2.3 years**, each expense ratio **0.03%**. A +2-point relevant-yield move implies roughly -9.8% VGIT or -4.6% VTIP price impact before carry/convexity/inflation accrual. Those are dated duration approximations, not current executable yield estimates.
- **California fund exemption:** FTB Publication 1001 requires qualifying asset composition and attributes exemption to qualifying U.S./California obligation income; use the fund's annual tax statement. A fund name, distribution rate or Treasury collateral label is insufficient.
- **RRSP:** FTB explicitly states federal treaty deferral does not apply for California income-tax purposes and residents must include RRSP earnings in the year earned. Federal treaty eligibility, reporting, withholding, withdrawal basis and California tracking require account-specific reconciliation. The IRS foreign-pension/PFIC reporting exception has conditions; it does not mean every foreign fund/account is tax-free.
- **Metals and losses:** IRS Topic409 describes a maximum 28% federal rate for net collectible gains; vehicle-specific precious-metal treatment and NIIT/state tax can matter. Net capital losses can offset gains; the annual deduction against other income is generally $3,000 for MFJ, with carryforward—not a dollar-for-dollar tax refund. Do not infer a deductible U.S. taxable loss from an aggregate sheet loss in an RRSP or from today's FX-translated cost.
- **U.S. residence controls the starting framework:** Canadian citizenship and Canadian brokerage location do not negate U.S. worldwide-income or foreign-asset reporting. No current OFAC or PFIC classification is inferred solely from citizenship or a ticker. Foreign pooled vehicles and MNT/COP.U require the actual legal structure/account review; an operating Canadian company is not automatically a PFIC.

**Illustration, not your tax bracket or current yield:** a 4% Treasury yield taxed federally at24% leaves3.04% nominal; at32% it leaves2.72%. With4% inflation, those are roughly **-0.92%/-1.23% real**. Zero-yield cash loses about11.1% purchasing power over three years at4% inflation; actual interest reduces that loss. Treasury cash can therefore be the right emergency asset while still being an incomplete long-run inflation hedge. Compare actual brokerage sweep yields, after-tax bill yields and TIPS cash flows before choosing the implementation; no current yield was invented for the alternatives.

The USCIS page retrieved for job-loss options redirects to an explicitly archived page. Its historical 'up to60days' language is not relied on here as current legal advice. The reserve rationale needs no exact visa-day assertion: loss of employment can simultaneously reduce income, stop vesting and create relocation/insurance costs.

## Transaction audit: what the records do and do not prove

A separate report and normalized CSV preserve **59 identifiable buy/sell events plus one PDBA adjustment**. Eight October trades are corroborated in current accepted records; older records vary in strength. Only31 of51 earlier events have at least some corroboration outside the October1 report;20 remain prior-report-only or inferred. This is all available identifiable history, not a complete brokerage ledger.

**Supported findings:** speculation grew through documented FIS and ASTS purchases while the hard cap remained; NKE starter size exceeded accepted guidance; TTD differed from a research recommendation whose separate acceptance was not proved. Current UNG is three times its target, but the clearly documented1% target postdates the claimed September2 add—do not invent a retroactive rule breach.

**Positive habits:** executed ARX/OXY/WPM reductions, XME/XLU/SMR/GOOGL substitutions, healthcare diversification, BHP cleanup, and a staged VGIT starter. These deserve credit independently of short-term returns.

**Corrections to the earlier audit:** clustered trades can implement one planned rebalance; count alone is not evidence of harmful overtrading. The July26 rule deliberately paused broad-equity buying, so the low core is not automatically a compliance failure. Seventeen residual exits do not establish a psychological motive. Recent profits or losses do not prove decision quality.

**Unresolved reconciliation:** VTI current22 versus15 identified purchased shares; VXUS109 versus54; PFE467 recorded remaining versus later claimed501 sale; physical gold's old5oz platform note versus current15.86oz aggregate; mixed-account assignments and all historical cash flows/tax lots. A broker activity export is the cheapest way to resolve these. No total realized-return or complete5/20/60-day event study is asserted.

## Ranked recommendations and concrete proposed record changes

| Priority | Recommendation | Why / confidence | Boundary |
| --- | --- | --- | --- |
| 1 | Define reserve dollars and acceptable purchase delay before deploying cash | Very high impact; spending unknown, arithmetic clear | Use sensitivity now; final reserve depends on your spending/access answer |
| 2 | Enforce current speculation/issuer/sleeve limits before adding satellites | High confidence: live values and recorded caps | Do not raise caps merely to legitimize existing drift; no orders in this report |
| 3 | Replace guaranteed-house-safety/utility-hedge/Adobe claims | High confidence: primary mechanics and user extract | Correct records only after your review |
| 4 | Reconsider TIPS versus gold substitution; retain bullion but remove guarantees | High confidence mechanism; allocation is judgment | Existing no-VTIP choice is not silently overridden |
| 5 | Reconcile target grid and quote/account/currency defects | High confidence; prevents bad sizing | Audit calculations are separate; live sheet unchanged |
| 6 | Review California RRSP reporting and after-tax accessible house funds | Primary FTB guidance; account amounts incomplete | Account-level tax reconciliation, not assumed tax liability |
| 7 | Choose an overall risky-capital budget; simplify within it | Medium sizing confidence; stress results transparent | Avoid another theme added on top |
| 8 | Use observable economic/valuation evidence rather than automatic phase rotation | Medium regime confidence; low timing edge | Energy can remain a bounded thesis; normalization and job loss are adverse cases |

| Old state | Proposed state — not applied |
| --- | --- |
| Portfolio theory70%right / precise conviction grades determine weights | Use explicit objectives, liability floors, economic exposures and sensitivity; remove unsupported numerical certainty |
| Low6.5%volatility means a correction cannot price you out | Risk estimate is stale/hardcoded; state adverse dollar losses and after-tax house-floor conditions |
| Adobe$732k /57%networth | User extract$13,940.52sellable; $355,837.68contingent unvested compensation, separated from spendable assets |
| Current basecase necessarily transitions oil shock→recession | Inflation/slowdown risk strengthened; recession and exact rotation remain conditional |
| Gold excellent in both stages, replaces TIPS | Gold is volatile monetary diversification; TIPS separately matches CPI-linked liabilities |
| Utilities are the recession hedge | Utilities are equity; acceptedVGIT is a distinct duration hedge, neither guaranteed principal at sale |
| 2027Brent$74, gasstorage+5%, currentgoldETFoutflows | OctoberEIA$84, endOctoberstorageforecast+2%; SeptembergoldETFinflows; retain forecast cutoffs |
| Automatic50/50CAD/USDcash | Allocate by actual USD expenses/house and CAD contingency, including separateCAD250k |
| RRSP broadly tax-deferred | Federal/California treatment differs; California annualearnings and withdrawal basis must be tracked |
| All recorded trades complete / clusters prove overtrading | 59identifiabletrades+1adjustment, incomplete sourcecoverage; assess then-current rules and funded risks |

## Uncertainties and cheapest next checks

| Uncertainty | Next check | Effect on conclusion |
| --- | --- | --- |
| Essential spending and family-reserve access | Your approximate monthly essentials and transfer timing | Sets emergency floor; scenarios already show why it matters |
| Exact house amount/date/mortgage access | A price/down-payment range and willingness to delay after loss | Sets the amount that must be maturity-matched |
| After-tax spendable assets/account split | Broker balances and tax lots; RRSP earnings/basis records | May reduce house funding below gross illustrations |
| CF current fundamentals, DBE contracts/roll | Accessible latest issuer/SEC filing and holdings | No new fertilizer/refined-products purchase endorsed while unresolved |
| Current IEA minerals / IMF COFER | Official downloadable tables or browser access; preserve observation dates | Old precise scarcity/reserve-share statistics remain unverified |
| Current individual-stock valuations | Normal-cycle cash flow, financing and current price for large residual issuers | No cheapness/buy claim rests on stale forward multiples |
| Transaction gaps | Activity export with beginning holdings, transfers, fills, fees, FX and ending holdings | Needed for full performance/tax audit; current cap findings already supported |
| Physical gold/URC realizable value and access | Actual custody/platform balances, spreads and current corporate-action identifier | Small-to-moderate valuation/access uncertainty; no assumed instant liquidation |
| Hedge reliability outside selected histories | Additional long-run regime tests if choosing final strategic policy | Does not turn any shown stress into a maximum-loss guarantee |

## Sources and reproducibility

Detailed primary-source excerpts, publication dates, observation periods and retrieval failures:
`/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/reports/2026-10-14_primary_evidence.md`

Complete transaction table, evidence categories, positive/negative process findings:
`/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/reports/2026-10-14_transactions.md`

Fresh official sources driving conclusions (retrieved October14, publication dates noted above or in the companion report):

- BEA GDP: https://www.bea.gov/data/gdp/gross-domestic-product
- BEA August PCE: https://www.bea.gov/news/2026/personal-income-and-outlays-august-2026
- BLS via FRED headline/core CPI: https://fred.stlouisfed.org/series/CPIAUCSL and https://fred.stlouisfed.org/series/CPILFESL ; conventional annual rates use https://fred.stlouisfed.org/series/CPIAUCNS and https://fred.stlouisfed.org/series/CPILFENS
- Jobs/unemployment: https://fred.stlouisfed.org/series/PAYEMS and https://fred.stlouisfed.org/series/UNRATE
- Inflation compensation: https://fred.stlouisfed.org/series/T10YIE
- Broad nominal dollar: https://fred.stlouisfed.org/series/DTWEXBGS
- Federal Reserve policy/SEP: https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm and https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm
- EIA October STEO/forecasts: https://www.eia.gov/outlooks/steo/ and https://www.eia.gov/outlooks/steo/pdf/steo_full.pdf
- EIA gas detail/storage: https://www.eia.gov/outlooks/steo/report/natgas.php and https://ir.eia.gov/ngs/ngs.html
- World Gold Council September flows/commentary: https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/10 and https://www.gold.org/goldhub/research/gold-market-commentary-september-2026
- China NBS activity/PMI: https://www.stats.gov.cn/english/PressRelease/202609/t20260915_1965305.html and https://www.stats.gov.cn/english/PressRelease/202610/t20261008_1965466.html
- World Bank September prices: https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Pink-Sheet-October-2026.pdf
- Treasury TIPS/bills: https://www.treasurydirect.gov/marketable-securities/tips/ and https://www.treasurydirect.gov/marketable-securities/treasury-bills/
- Vanguard dated June30 factsheets: https://fund-docs.vanguard.com/F3143.pdf and https://fund-docs.vanguard.com/F3365.pdf
- California FTB 2025 Publication1001, including RRSP and qualifying fund interest: https://www.ftb.ca.gov/forms/2025/2025-1001-publication.pdf
- IRS gains/losses/investment income/PFIC instructions: https://www.irs.gov/taxtopics/tc409 , https://www.irs.gov/publications/p550 , https://www.irs.gov/instructions/i8621
- WPM August6 Q2 release: https://www.sec.gov/Archives/edgar/data/1323404/000119312526338641/d15525dex991.htm
- Cameco July31 Q2 release: https://www.sec.gov/Archives/edgar/data/1009001/000119312526326768/d125942dex991.htm
- VanEck October13 NLR holdings: https://www.vaneck.com/Main/FundDatasetBlock/Get/?blockId=351334&pageId=233098&ticker=NLR

Access limits: BLS direct pages failed but official FRED observations were recovered. IMF/IEA pages failed; CF issuer page returned403; DBE's retrieved page did not expose adequate current contracts. The USCIS page redirected to an explicitly archived version, which is excluded as current legal authority. No inaccessible source is labeled freshly verified.

Local inputs reviewed: root and portfolio charters/state/decisions/learnings, full `AUDIT_CHECKPOINT.md`, `PHASE1_AUDIT.md`, `ideal_allocation.md`, October1 macro report, prior relevant sleeve research, current live sheet and transaction narratives. These are historical/user records, not substitutes for primary verification.

Calculation artifacts:

- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/data/2026-10-14/snapshot.json`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/data/2026-10-14/refresh_snapshot.py`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/data/2026-10-14/analyze_allocation.py`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/data/2026-10-14/scenario_analysis.json`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/data/2026-10-14/scenario_results.csv`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/data/2026-10-14/historical_proxies.csv`
- `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/macro_monitoring/data/2026-10-14/transactions/events.csv`

## Skill, credentials, retry handling and review boundary

Updated the authoritative workflow at `/home/colligo/hs_scripts/claude/dotclaude/commands/fin_chk_macro.md`; synchronized its generated Codex adapter and passed `quick_validate.py`. Changes recognize a natural-language full-audit request, reconcile data/currencies/targets, separate personal assets and liabilities, require economic exposure/stress comparisons, preserve provenance in incomplete transaction histories, and remove redundant full-review/deletion questions. No accepted allocation was rewritten.

The verified Google Sheets key remains securely at `/home/colligo/.claude/hshariati/portfolio_sheets_sa.json`; setup locations are documented in `/home/colligo/hs_scripts/claude/dotclaude/memory/reference_fin_portfolio_machine_setup.md`. No secret value is included in research records.

For the rate-limit problem, the official Codex reference documents provider `request_max_retries` and `stream_max_retries`: https://developers.openai.com/codex/config-reference/ . `/home/colligo/.codex/config.toml` already sets both to100 for `foundry_azure`. No config change was needed. Failed research workers were retried, and a smaller-context worker completed the evidence and transaction tasks using the same model. Retry settings do not guarantee recovery from every provider/outer-client failure; an unavailable model cannot run its own in-turn recovery loop. Your answers are saved, and checkpointed work can resume without resending them.

**Pending choices:** reserve dollars/access, acceptable dollar loss and house delay, whether to reconsider TIPS, and which proposed policy corrections you want adopted. The skill requires your review before canonical investment-record changes. This audit and its proposals are complete; those choices affect implementation, not the validity of the findings already demonstrated.

## Appendix: exact scenario shocks

Non-cash figures are assumed percentage changes in total USD market value; CAD-cash figures are FX changes. Economic labels classify the model; they are not proposed new live-sheet labels. Cash carry and subsequent inflation accrual are excluded; a 'recovery' column is not an annual total-return forecast. Leveraged/inverse outcomes are separately assumed because their path dependence cannot be inferred from endpoint asset returns alone.

| Category | Demand recession | Inflation and rates | Joint liquidation | Disinflation recovery |
| --- | --- | --- | --- | --- |
| usd_cash | +0% | +0% | +0% | +0% |
| cad_cash | -15% | +10% | -15% | +5% |
| gold_bullion | -10% | +20% | -25% | -15% |
| gold_equity | -35% | +15% | -50% | -15% |
| energy_eq | -45% | +20% | -45% | -15% |
| nuclear_grid | -40% | -15% | -45% | +20% |
| industrial_eq | -45% | +10% | -45% | +10% |
| ag_eq | -35% | +20% | -40% | -10% |
| ag_futures | -20% | +20% | -25% | -15% |
| copper_physical | -35% | +20% | -40% | +10% |
| silver_streamer | -40% | +10% | -45% | -10% |
| naturalgas | -45% | +30% | -60% | -20% |
| refined_futures | -40% | +30% | -45% | -25% |
| global_eq | -35% | -15% | -35% | +20% |
| em_eq | -40% | -15% | -45% | +20% |
| quality_eq | -30% | -20% | -35% | +20% |
| defensive_eq | -30% | -15% | -35% | +15% |
| spec_eq | -60% | -35% | -65% | +25% |
| bitcoin | -65% | -40% | -70% | +30% |
| legacy_eq | -55% | -30% | -60% | +15% |
| boil | -80% | -25% | -90% | -50% |
| sqqq | +50% | +30% | -50% | -50% |
| nominal_intermediate | +10% | -10% | -10% | +5% |
| short_tips | +2% | -4.6% | -5% | +1% |
| broad_commodity | -35% | +25% | -35% | -20% |
