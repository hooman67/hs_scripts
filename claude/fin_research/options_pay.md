# Options Pay — Cash-Secured Puts and Covered Calls

**Prepared:** 2026-09-06  
**Purpose:** Evaluate whether selling puts instead of placing limit buys, and selling covered calls instead of selling shares outright, can improve execution without violating the portfolio's growth-first allocation and risk rules.  
**Status:** Research and decision framework, not individualized tax or investment advice. Option quotes are snapshots, not standing recommendations.

## Executive conclusion

The idea is **conditionally sound as an execution tool, but unsound as an income strategy applied mechanically**.

- A cash-secured put can improve a patient entry **only when the strike is already a price at which you would unconditionally buy 100 shares**, the assignment fits the target sleeve, and the premium adequately compensates for tying up cash and accepting downside.
- A covered call can improve a planned trim **only when you are genuinely indifferent between keeping the shares and selling them at the strike**. It is not a substitute for selling a broken thesis: if the stock falls, the call expires and you still own the loser.
- The premium is **not a commission** and is not free income. It is compensation for accepting an asymmetric obligation: limited upside/premium, with most of the underlying's downside.
- Systematic option overwriting conflicts with a 35-year-old investor's growth objective. From 2007-01-03 through 2026-09-04, the Cboe PUT and BXM benchmark indexes had lower volatility and drawdowns than the S&P 500 Total Return Index, but materially lower annualized returns in my calculation: approximately **7.2% PUT, 6.1% BXM, and 11.1% S&P 500 TR**. This is the central trade-off: smoother income in exchange for surrendered upside, not extra return from nowhere.
- For the current portfolio, **do not sell puts on KWEB, UNG, or BOIL now**. KWEB is already above its 2% name target, UNG is almost three times its 1% sleeve target, and BOIL is an exit holding with daily 2x path dependence.
- The best current uses are narrowly targeted covered calls on shares already designated for a non-urgent trim: **PFE first**, then possibly **CCJ** or **WPM**. The current exit sleeve should generally be sold outright.
- Use a **U.S. taxable account** for the initial pilot. Covered calls may be reasonable in an RRSP, but written puts in an RRSP carry a specific CRA business-income warning even though Questrade currently permits cash-secured puts operationally. Do not write RRSP puts without written cross-border tax advice.
- Make the portfolio's speculation target **1% of total portfolio**, currently about **$6,620**. With approximately **$3,174 of LULU.TO already in it**, only about **$3,446** remains. Strategic-entry options should be tracked as an execution overlay, but their full assignment notional must fit the underlying sleeve; genuinely speculative short options must count their full maximum loss against the remaining 1% cap.

## Current portfolio facts used

Live `FR_Portfolio` values read on 2026-09-06; the sheet was not edited.

| Item | Current | Policy implication |
|---|---:|---|
| Total portfolio | $662,048 | 1% = about $6,620 |
| Cash | $324,051 / 48.9% | Ample collateral, but cash is also house reserve and planned deployment capital |
| Speculation | $3,174 / 0.5% | LULU.TO already consumes about 48% of a proposed 1% cap |
| KWEB | 609 shares / $15,864 / 2.4% | Above its current 2.0% name target; about 101 shares excess |
| UNG | 1,834 shares / $19,367 / 2.9% | Far above the 1.0% `nat_gas` target; about $12,747 must be trimmed |
| BOIL | 100 shares / $2,039 | In `(exit)`; leveraged daily-reset product |
| PFE | 738 shares / $20,996 / 3.2% | Healthcare implementation calls for about 1%; roughly 500 shares are excess |
| CCJ | 150 shares / $15,111 / 2.3% | Uranium sleeve is overweight; one 100-share lot is a plausible trim |
| WPM | 192 shares / $29,756 / 4.5% | Silver/platinum sleeve target is 1%; materially oversized |
| Exit sleeve | $27,470 / 4.1% | Broken/off-thesis positions should not be retained merely to sell calls |

Current whole-lot exit candidates that are mechanically coverable are AUR (100 shares), CHPT (100), NIO (120), CAG (292), BOIL (100), and SBSW (200). Their availability for covered calls does **not** make covered calls the right exit.

## What the trades really are

### Cash-secured put versus a limit buy

For one short put with strike `K`, premium `P`, and 100-share multiplier:

- Cash committed: normally `K × 100` under the conservative rule used here.
- Maximum profit: `P × 100`.
- Effective purchase price if assigned: `K − P` per share.
- Maximum loss: `(K − P) × 100` if the underlying goes to zero.
- Expiration result: above `K`, keep the premium and receive no shares; below `K`, buy 100 shares at `K` even if market value is far lower.

A put is not simply a paid limit order:

1. A limit order may fill whenever the market touches the limit; a put is normally assigned based on exercise, often near expiry, and may never acquire shares even if the price briefly dips.
2. The put seller gives up participation if the asset rises before purchase.
3. The obligation remains through a gap down. The premium is usually small relative to the loss from buying above the new market price.
4. Cash is encumbered and may earn less than it otherwise could, depending on the broker's collateral treatment.
5. U.S. equity and ETF options are generally American-style and can be assigned before expiration.

**Use a put only if this sentence is true:** “I would submit an irrevocable order today to buy exactly 100 shares at this strike, and I would still be comfortable after a sudden 30% decline.”

### Covered call versus an outright sale

For 100 owned shares and one short call:

- Maximum option profit is the premium.
- If the stock finishes above the strike and assignment occurs, the effective sale price is `strike + premium`.
- If the stock falls, the premium only offsets a small portion of the stock loss and the shares remain owned.
- Upside above the strike is surrendered.

A covered call is therefore appropriate for **“I am happy to hold, but equally happy to sell at this higher price.”** It is inappropriate for **“I have decided this position should be gone.”** A limit sell is cancellable and sells when reached; a covered call can cap upside after the price crosses the strike yet still leave the shares unsold if the price later falls before expiration.

Cash-secured puts and covered calls with the same strike and expiry are closely related economically through put-call parity. Calling one “income” does not change its equity/short-volatility exposure.

## Why the strategy sometimes appears profitable

Option buyers pay for convexity, leverage, and insurance. Sellers frequently receive an implied-volatility premium, time decay works in their favor, and many options expire without exercise. But the seller's distribution is negatively skewed: many small gains can be offset by occasional large losses or large forgone rallies.

My reproducible index check used the official Cboe daily histories for the cash-secured S&P 500 PutWrite Index (`PUT`) and covered-call BuyWrite Index (`BXM`), and the S&P 500 Total Return series, from 2007-01-03 through 2026-09-04:

| Strategy index | CAGR | Annualized daily volatility | Maximum drawdown |
|---|---:|---:|---:|
| Cboe PUT | 7.2% | 13.8% | -37.1% |
| Cboe BXM | 6.1% | 14.3% | -40.1% |
| S&P 500 Total Return | 11.1% | 19.7% | -55.3% |

This period is not a forecast and theoretical indexes omit an investor's taxes, implementation mistakes, and some real-world frictions. It nevertheless shows why a growth investor should not overwrite the whole portfolio: lower volatility came with a large return sacrifice during a strong equity era.

## Mandatory execution rules

### 1. Strategy eligibility

Open a short option only if all are true:

- The underlying already has a written BUY or TRIM decision independent of option premium.
- Assignment at the strike leaves the resulting sleeve at or below its target plus the normal rebalance tolerance.
- The trade is cash-secured or share-covered in the **same account**; no cross-account “coverage.”
- There is no need to sell or buy by a deadline.
- The underlying is liquid, unleveraged, and understood well enough to own through a 30% drawdown.
- No earnings, FDA ruling, merger vote, court ruling, major investor day, or other binary event falls inside the holding period unless the event risk is the explicit, separately approved thesis.

### 2. Initial sizing

- Pilot with **one contract at a time** for the first three completed cycles.
- Total open cash-secured-put assignment notional: no more than **1% of portfolio (~$6,620)** during the pilot, and never more than the remaining dollar gap in the destination sleeve.
- Covered calls: no more than one contract per name initially and no more than **25% of a strategic core holding**. Calls may cover a larger percentage only when the covered shares are explicitly excess and already designated for sale.
- Never use margin, portfolio margin, naked calls, uncovered puts, or borrowed cash.
- Do not count premium as reducing portfolio exposure. A $2,400 put assignment is $2,400 of pro-forma equity exposure, not a $21 trade.

### 3. Expiry and strike

- Default expiry: **30–45 days to expiration (DTE)**.
- Avoid opening below 21 DTE; close or make an assignment decision by 7–10 DTE because gamma and operational risk rise near expiry.
- Entry puts: use the pre-set valuation price first, then prefer roughly **0.20–0.30 absolute delta**. Use 0.30–0.35 only when assignment is positively desired.
- Covered calls on long-term holdings: approximately **0.15–0.25 delta**. Covered calls on pre-approved trim lots: approximately **0.25–0.40 delta**.
- Delta is not a literal or stable probability. Strike suitability overrides delta.

### 4. Liquidity

- Use limit orders only; start near midpoint and do not chase.
- Prefer at least **500 contracts of open interest** at the exact strike and at least **100 contracts of same-day volume**.
- Prefer bid/ask width no more than **$0.05 for sub-$1 options**, and no more than roughly **10% of midpoint** for larger premiums. If neither condition is met, skip rather than pay the spread.
- A high-volume underlying does not guarantee a liquid option strike. VWO, VXUS, GEHC, DBE, PICK, and VPU all showed unattractive or stale spreads in the reviewed 2026-10-16 chains.

### 5. Volatility and return hurdle

- Do not sell merely because absolute IV is high; high IV usually signals real event or gap risk.
- Prefer 30-day implied volatility above comparable trailing 20–30 day realized volatility and an IV percentile/rank above roughly 40–50, **after excluding event-driven spikes**.
- For a put, calculate gross annualized cash yield as:

  `net premium ÷ (strike × 100 − net premium) × 365 ÷ DTE`

- Require both: (a) an effective entry price that passes the underlying valuation rule, and (b) a net option yield meaningfully above the actual yield earned on collateral. A practical screen is at least **0.75%–1.0% net premium per 30–45 day cycle**; this is a filter, not a return promise.
- Never compare annualized option yield with a stock's expected return as if they are equivalent. Annualizing assumes repeatable premiums and omits tail losses and missed rallies.

### 6. Management and exits

- Enter a good-till-cancelled limit only for the trading day; reassess price and thesis each day.
- Buy to close at **50–75% of maximum profit** if reached with more than 14 DTE remaining.
- Do not “roll forever.” Roll only when the thesis and target price are unchanged, the roll produces a net credit, total assignment exposure does not increase, and the new expiry remains within 60 DTE.
- If a put is assigned, stop the wheel and re-underwrite the now-owned security. Do not automatically sell a call merely to recover a loss.
- If a covered stock's thesis breaks, buy back the call and sell the shares as one order. Do not wait for premium decay.
- Record gross premium, commissions/fees, cash collateral, assignment notional, effective basis/proceeds, realized option P/L, and foregone upside.

## Current-candidate screen

Quotes below are delayed Cboe snapshots for 2026-10-16 expiration, observed after the 2026-09-04 close. Bid-side economics are shown because a seller cannot assume midpoint execution. Refresh all quotes and event dates before any trade.

| Candidate | Snapshot | Portfolio fit | Verdict |
|---|---|---|---|
| **KWEB $24 put** | Spot $26.05; bid/ask $0.21/$0.26; delta -0.17; OI 2,506; volume 1,501. Bid gives $21 premium, $23.79 effective entry, 8.7% discount, and 0.88% gross 40-day collateral yield. | Mechanically attractive and well sized at $2,400 notional, but KWEB is already $15,864/2.4% versus a 2.0% name target. Assignment would worsen concentration and crowd out VWO. | **Do not sell now.** Reconsider only after KWEB falls below target or the target is explicitly raised. |
| **KWEB $28 call** | Bid/ask $0.29/$0.39; delta 0.26; OI 16,817; volume 900. Bid implies $29 premium and $28.29 effective sale. | Current holding exceeds its 2% name target by about 101 shares, almost exactly one contract. | **Best small covered-call test**, but only if $28.29 is a genuinely acceptable sale price and tax lots are favorable. Spread is still wide relative to premium; use a midpoint limit or skip. |
| **UNG $10 put** | Spot $10.56; bid/ask $0.28/$0.39; delta -0.31; OI 11,805; volume 457. | The portfolio already holds 1,834 shares/$19,367 against a 1%/$6,620 target. | **Reject.** No additional assignment is permissible. |
| **UNG $11 call** | Bid/ask $0.42/$0.44; delta 0.42; OI 16,146; volume 1,106. Twelve calls on 1,200 excess shares would collect about $504 at bid and create an $11.42 effective sale if assigned. | Liquidity is good, but the allocation requires an immediate ~$12,747 trim. If UNG falls, the calls expire and the oversized exposure remains. | **Sell excess shares outright.** Premium is not worth preserving an unintended, roll-sensitive overexposure. |
| **BOIL options** | BOIL spot about $20.58; 30-day IV about 66.9%. Oct. $21 call was roughly $1.68/$1.96 with only 230 OI and 78 volume. | BOIL targets 2x the **daily** natural-gas index result; ProShares warns returns over longer periods can deviate significantly, especially with volatility. It also generates a K-1. | **Reject all puts and calls; sell the 100 shares outright.** Options on a daily leveraged commodity pool layer short-volatility and path dependence on top of leverage and futures roll. |
| **PFE $30 call** | Spot $28.44; bid/ask $0.33/$0.36; delta 0.28; OI 13,002; volume 936. Five contracts generate roughly $165–$180 and, if assigned, sell 500 shares at an effective $30.33–$30.36. | 738 shares are about 3.2% of portfolio; the implementation target is about 1%, leaving roughly 500 excess shares. Thesis is weakened/overweight rather than an immediate zero-weight exit. | **Best practical candidate.** Pilot one contract, then scale only if willing to hold through expiry. Check earnings and ex-dividend dates; early assignment can occur around dividends. |
| **CCJ $110 call** | Spot $100.65; bid/ask $2.63/$3.25; delta 0.33; OI 5,589; reported volume 15,324. Bid implies $263 premium and $112.63 effective sale. | One contract would reduce 150 shares to 50 if assigned, materially repairing the overweight uranium sleeve. | **Conditionally suitable**, but only with a patient limit near midpoint. Spread is wide and the call gives up a potentially sharp uranium rally. Outright sale is better if the trim is urgent. |
| **WPM $170 call** | Spot $155.01; bid/ask $5.00/$5.60; delta 0.33; OI 179; volume 9. | Position is 4.5% versus a 1% silver/platinum sleeve. One assignment still leaves 92 shares, more than the full target at today's price. | **Second-tier only.** Sell about 50 shares outright first; one call could then cover 100 of the remaining 142 and leave about 42 shares if assigned. Low volume and large upside surrender argue for an outright trim instead. |
| **CAG $16 call** | Spot $15.48; bid/ask $0.40/$0.60; delta 0.43; OI 214; volume 48. | CAG is in the exit sleeve because the thesis was judged broken/value-trap. Calls cover only 200 of 292 shares. | **Reject; sell outright.** A 40-cent bid is poor compensation for retaining downside and failing to complete the exit. |
| **AUR, CHPT, NIO, SBSW calls** | Whole lots exist and premiums can look large because implied volatility is high. | Each is already an exit/cleanup position. CHPT and similar high-IV names can lose far more than one option premium before expiry. | **Reject; sell outright.** High premium is evidence of risk, not a gift. |
| **VWO / VXUS / GEHC puts** | Their reviewed 2026-10-16 strikes had wide or stale markets: VWO $58 put $0.00/$0.75; VXUS $85 put $0.20/$0.85; GEHC $62.50 put $0.45/$0.70 with zero reported same-day volume. | These are more logical acquisition targets than KWEB because their sleeves are underweight. | **Correct thesis, wrong current contracts.** Use limit buys or wait for a liquid expiry; never force an option trade. |
| **VTI put** | One contract near current price commits roughly $36,000–$38,000; reviewed strikes had modest OI and wider spreads than ideal. | It fits the large global-core gap but one contract is 5%–6% of the total portfolio. | **Too large for the pilot.** Buy VTI shares in tranches instead. |
| **DBE / COPX / PICK / VPU puts** | DBE and PICK/VPU chains were extremely sparse; COPX was more active but one contract near $90 commits about $9,000. | DBE/refined-products has a $13,241 gap, but assignment creates K-1 commodity-pool exposure; COPX would overshoot the current copper gap of only about $1,779. | **Use direct share purchases, not puts.** |

### Ranked implementation

1. **PFE covered call pilot:** one 30–45 DTE call on 100 of the approximately 500 shares already designated for a trim. Pick the strike from the acceptable sale price, not from premium size. Scale later only after one full lifecycle.
2. **KWEB covered call on one excess lot:** optional only if a roughly $28 effective exit is acceptable. This is a sizing cleanup, not an income program.
3. **CCJ covered call on one 100-share trim lot:** optional if the uranium trim is non-urgent and the bid/ask tightens.
4. **No cash-secured put today:** the logical underweight targets currently have unattractive chains, while the liquid KWEB/UNG contracts would worsen allocation errors.
5. **Outright sells:** BOIL and all broken-thesis exit names. Do not let option premium veto the existing decision.

## The 1% speculation sleeve

The portfolio should formalize **Speculation at 1%**, not “0% with a $10k note.” At the current total, the cap is approximately $6,620. LULU.TO already occupies $3,174, leaving about $3,446.

Options require two ledgers because notional and premium are different:

1. **Allocation ledger:** A put's full assignment notional is pro-forma exposure in the destination sleeve. A covered call's shares remain in their existing sleeve. Reserved put cash is marked `committed`, not available dry powder.
2. **Speculation-risk ledger:** Track realized and mark-to-market option P/L, fees, and any trade not backed by a pre-approved allocation. A truly speculative short put counts its full maximum loss—not the premium—against the 1% cap.

This means:

- A strategic PFE covered call does not move PFE into the speculation sleeve; it is an execution overlay on a planned trim.
- A VWO put could be an execution overlay if assignment fits the EM sleeve, even though the cash notional is near 1%.
- A KWEB or UNG put sold merely because premium looks attractive is speculative. It must pass both the remaining $3,446 risk cap and the destination-sleeve cap. KWEB fails the latter; UNG fails it badly.
- No combination of open option obligations plus LULU may create more than $6,620 of plausible incremental loss outside strategic sleeve exposures.

Do not run a continuous “wheel” program. The wheel systematically converts puts into unwanted holdings and then caps the rebounds needed to recover. That is especially harmful for high-volatility China, biotech, uranium, and commodity ETPs.

## Account and tax structure for a U.S. tax resident

### U.S. taxable brokerage — recommended pilot account

Advantages:

- Cleanest access to U.S. option chains and generally lower contract costs.
- Cash-secured puts and covered calls are ordinarily available with approval.
- Tax lots and assignment are easier to monitor in the same reporting system as the U.S. return.

U.S. federal treatment under IRS Publication 550:

- Premium on a written put or call is not recognized when received.
- If it expires, premium is generally short-term capital gain.
- If bought back, premium minus close cost is short-term gain or loss.
- Put assignment reduces the acquired stock's tax basis by premium; the stock holding period starts on assignment.
- Call assignment increases sale proceeds by premium; gain character then depends on the stock holding period.
- Covered calls can affect stock holding periods, qualified-dividend holding periods, straddle loss deferral, and wash-sale analysis. Deep-in-the-money/non-qualified calls are especially undesirable for tax-sensitive long-term lots.

Operational tax rules:

- Select the intended tax lot before likely assignment; do not assume the broker's default lot is optimal.
- Do not write calls against shares held fewer than 61 days around a dividend without checking qualified-dividend holding-period consequences.
- Do not sell a loss position by assignment and replace it with substantially identical shares/options within 30 days without wash-sale review.
- ETF options such as KWEB, UNG, and BOIL are generally equity/ETF options, not broad-based Section 1256 index options. Do not assume 60/40 treatment.
- If a UNG or BOIL put is assigned, the resulting fund units introduce partnership/K-1 reporting. USCF identifies UNG as a K-1/K-3-issuing commodity partnership; ProShares states BOIL generates a K-1.

### RRSP — covered calls only unless a cross-border specialist approves puts

- IRS Revenue Procedure 2014-55 generally permits eligible U.S. residents to defer U.S. tax on undistributed RRSP income until distribution and removes Form 8891/3520/3520-A reporting, but it does not remove possible Form 8938 or FBAR duties.
- CRA Folio S3-F10-C1 ¶1.40–1.44 says option writing itself is not a qualified-investment acquisition, but speculative option writing can constitute a business. CRA specifically says a covered call by itself does not cause that result, while writing a put—alone or in combination—**may** cause the plan to be considered to carry on a business. Registered plans also generally cannot borrow.
- Questrade's 2026 options-level page says registered accounts may receive Level 2 approval and currently permits cash-secured puts except on indices. Broker permission is not tax clearance; it does not override CRA's stated business-income risk.
- Therefore: infrequent, fully covered calls on already-owned qualified shares may be reasonable. Avoid RRSP put writing until a Canadian/U.S. cross-border CPA confirms the intended frequency and facts in writing.

### Canadian non-registered brokerage — not preferred

- U.S. tax residency generally means worldwide income remains reportable to the United States.
- The foreign account may require FBAR and/or Form 8938 disclosure, and every CAD premium, close, assignment, basis, and proceeds figure must be translated into USD under U.S. rules.
- Canadian withholding, nonresident-account restrictions, and Canadian-source tax treatment can add reconciliation without improving option economics.
- Use only if the covered shares already sit there and moving them would itself create material tax/currency costs. Otherwise the U.S. taxable account is simpler.

## Practical checklist before each order

Record all fields before clicking sell:

| Field | Required entry |
|---|---|
| Strategy | Cash-secured put or covered call |
| Independent reason | Existing BUY target or TRIM target |
| Account | Exact account holding cash/shares |
| Underlying sleeve | Current $, target $, and pro-forma $ after assignment |
| Contract | Ticker, expiry, strike, put/call, quantity |
| DTE / delta | 30–45 DTE target and observed delta |
| Market quality | Bid, ask, spread %, volume, OI, timestamp |
| Gross and net premium | Premium less all per-contract/exercise/FX charges |
| Assignment notional | `strike × 100 × contracts` |
| Effective entry/exit | Strike minus put premium / strike plus call premium |
| Max loss | Put: effective entry × shares; call: underlying can approach zero, less premium |
| Event check | Earnings, dividend/ex-date, FDA, merger, macro release |
| Exit rule | 50–75% profit, 7–10 DTE decision, thesis-break action |
| Tax rule | Lot selected, holding period, wash-sale/straddle checked |

## Final decision

Adopt the concept, but narrowly:

- **Yes:** one-contract pilots on pre-existing buy/trim decisions, starting with a PFE covered call if the shares are in an eligible account and $30-plus is an acceptable exit.
- **Maybe:** one KWEB covered call on the approximately 100-share excess; one CCJ call on the planned 100-share trim.
- **No:** puts on KWEB or UNG at current weights; any BOIL option; calls used to postpone broken-thesis exits; market orders; margin; naked options; automatic wheel strategies.
- **Portfolio accounting:** formalize the 1% speculation cap, but treat legitimate execution overlays in their underlying sleeves and track their option risk separately. A short option is never a premium-sized exposure.
- **First action:** sell the exit names and correct UNG/BOIL sizing directly. Options should optimize a sound allocation decision, never replace one.

## Assumptions to validate

1. U.S. tax residency continues for 2026 and Hooman is not also filing as a Canadian tax resident.
2. The Canadian registered account is an RRSP—not a TFSA—and its U.S. treaty deferral has been handled consistently under Revenue Procedure 2014-55.
3. The shares proposed for covered calls are held in whole 100-share lots within a single option-approved account.
4. No covered shares are restricted, pledged, or required for a near-term house purchase.
5. The current 2% KWEB name target, 1% UNG sleeve, 1% healthcare PFE implementation, 3.5% uranium sleeve, and 1% silver/platinum sleeve are still authoritative.
6. The current PFE/CCJ/WPM decisions are trims, not immediate thesis-break exits.
7. Option collateral in the selected broker can remain in an interest-bearing sweep or Treasury vehicle; this must be checked rather than assumed.
8. Hooman accepts assignment and missed upside without overriding the rules emotionally or rolling indefinitely.
9. A cross-border tax professional will review any RRSP option writing and any Canadian-account implementation.
10. Quotes will be refreshed during market hours; all quoted chains in this memo are delayed snapshots and may be stale by the next session.

## Sources

Accessed 2026-09-06 unless otherwise stated.

- Options Industry Council, “Cash-Secured Put”: https://www.optionseducation.org/strategies/all-strategies/cash-secured-put
- Options Industry Council, “Covered Call (Buy/Write)”: https://www.optionseducation.org/strategies/all-strategies/covered-call-buy-write
- IRS Publication 550, written puts/calls, qualified dividends, wash sales, and straddles: https://www.irs.gov/publications/p550
- IRS Revenue Procedure 2014-55, Canadian retirement-plan treaty deferral/reporting: https://www.irs.gov/pub/irs-drop/rp-14-55.pdf
- IRS, comparison of Form 8938 and FBAR requirements: https://www.irs.gov/businesses/comparison-of-form-8938-and-fbar-requirements
- CRA Income Tax Folio S3-F10-C1, especially ¶1.40–1.44 on option writing in registered plans: https://www.canada.ca/en/revenue-agency/services/tax/technical-information/income-tax/income-tax-folios-index/series-3-property-investments-savings-plans/series-3-property-investments-savings-plan-folio-10-registered-plans-individuals/income-tax-folio-s3-f10-c1-qualified-investments-rrsps-resps-rrifs-rdsps-tfsas.html
- Questrade, “Options levels,” current page reviewed 2026-09-06: https://www.questrade.com/learning/using-questrade/options-levels
- Questrade, “Options Strategies in Registered Accounts,” updated 2026-03-27: https://www.questrade.com/learning/options-active-trading/option-strategies-reg-accounts-overview
- Schwab pricing, including $0.65 per online options contract and $0 online exercise/assignment at access date: https://www.schwab.com/pricing
- USCF, UNG mandate and near-month futures design: https://www.uscfinvestments.com/ung
- USCF partnership tax information identifying UNG as a K-1/K-3 fund: https://www.uscfinvestments.com/tax-information
- ProShares, BOIL daily 2x objective, multi-day deviation warning, and K-1 disclosure: https://www.proshares.com/our-etfs/leveraged-and-inverse/boil
- FINRA, leveraged/inverse ETP compounding and holding-period risks, 2022-07-28: https://www.finra.org/investors/insights/lowdown-leveraged-and-inverse-exchange-traded-products
- Cboe delayed KWEB chain snapshot: https://cdn.cboe.com/api/global/delayed_quotes/options/KWEB.json
- Cboe delayed UNG chain snapshot: https://cdn.cboe.com/api/global/delayed_quotes/options/UNG.json
- Cboe delayed BOIL chain snapshot: https://cdn.cboe.com/api/global/delayed_quotes/options/BOIL.json
- Cboe delayed PFE chain snapshot: https://cdn.cboe.com/api/global/delayed_quotes/options/PFE.json
- Cboe delayed CCJ chain snapshot: https://cdn.cboe.com/api/global/delayed_quotes/options/CCJ.json
- Cboe delayed WPM chain snapshot: https://cdn.cboe.com/api/global/delayed_quotes/options/WPM.json
- Cboe delayed CAG chain snapshot: https://cdn.cboe.com/api/global/delayed_quotes/options/CAG.json
- Cboe PUT daily history: https://cdn.cboe.com/api/global/us_indices/daily_prices/PUT_History.csv
- Cboe BXM daily history: https://cdn.cboe.com/api/global/us_indices/daily_prices/BXM_History.csv
- S&P 500 Total Return series (`^SP500TR`) used for the same-date comparison: https://finance.yahoo.com/quote/%5ESP500TR/
- Cboe PUT index overview: https://www.cboe.com/us/indices/dashboard/put/
- Cboe BXM index overview: https://www.cboe.com/us/indices/dashboard/bxm/
