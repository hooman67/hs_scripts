# 2026 Schwab Tax-Loss Harvesting Plan

**As of:** 2026-10-26 after the confirmed main-batch fills
**Scope:** Hooman's individual U.S. taxable Schwab account
**Status:** October 26 main batch executed; November 16 VXUS review remains pending
**Tax posture supplied by Hooman:** California resident, married filing jointly, no capital-loss
carryforward

## Answer

The October 26 main harvest was executed. Ten full-position sales generated **$42,159.75**, five
replacement purchases used **$30,379.04**, and the permanent exits left **$11,780.71** of net Schwab
cash before any unreported fees or regulatory charges. Using the October 23 broker basis export, the
sales provisionally realized a **$10,840.54 capital loss**: approximately **$8,576.98 short term** and
**$2,263.56 long term**. Against Schwab's prior $8,104.89 short-term gain, the account is provisionally
at a **$2,735.65 net capital loss** before Adobe, other accounts, broker wash adjustments and subsequent
activity.

Delay the smaller VXUS→IXUS decision until **Monday, 2026-11-16** so the October 16 VXUS purchase is
outside the 30-day pre-sale window. Execute it only if VXUS still has a meaningful unrealized loss.

This is preferable to harvesting every available loss. It leaves CF, CLX, BKR, VTI and immaterial
fractional losses alone because their combined incremental benefit is small relative to the trading and
portfolio disruption.

### Subsequent Ameritrade activity outside the Schwab-only totals

Hooman bought 16 GOOGL at $297 on October 28 and sold all 16 at $280.9362 on October 30. The direct
arithmetic is a provisional **$257.0208 short-term loss** before fees and broker wash-sale adjustments.
This is an Ameritrade transaction and is **not included** in the Schwab-only $2,735.65 net-loss estimate
above. Combining only the currently recorded Schwab estimate and this later Ameritrade loss produces a
provisional known-account loss of **$2,992.67**, before Adobe, other accounts, later trades and final
1099-B adjustments. JQUA was purchased two minutes after the GOOGL sale, but the final broker/tax record
and any household GOOGL acquisitions remain controlling for wash-sale reporting.

### Confirmed user decisions — 2026-10-23

- Execute AA, RBLX, CAG and BAC as **permanent exits**. No replacement or later buyback is planned.
- CCJ is a tax-harvest sale rather than a permanent ban. If sold October 26, do not acquire either CCJ
  or CCO.TO through November 25. November 26 is outside the window but the U.S. market is closed;
  **Friday, November 27 is the first practical repurchase date**.
- The earliest tax-valid date does not change the separate combined Cameco sizing rule; check total
  CCJ plus CCO.TO exposure before any repurchase.

## Source-of-truth reconciliation

### VERIFIED — broker exports

The source package was exported from Schwab on October 23 and contains 29 current position files, a
detailed 2026 realized-gain report, a realized summary, a transaction report and the 2025 Form 1099.
The package was copied without altering the originals, permissions were restricted, and SHA-256 hashes
were recorded in its manifest.

Private source directory:

`/home/colligo/.claude/hshariati/portfolio_private/2026_tax_harvesting/schwab_export_2026-10-23_1939`

Manifest:

`/home/colligo/.claude/hshariati/portfolio_private/2026_tax_harvesting/schwab_export_2026-10-23_1939/manifest.json`

The broker files supersede the Google Sheet for tax lots. The Sheet aggregates accounts and average
costs, and it materially differs from the broker export for several positions, including IHI, VGIT,
BAC and SGOV. Do not use the Sheet to prepare Form 8949.

### Current broker totals

| Measure | Amount |
|---|---:|
| Current positions | 29 |
| Market value | $370,121.58 |
| Cost basis | $366,791.13 |
| Net unrealized gain | $3,330.45 |
| Sum of every currently negative short-term lot | -$9,125.82 |
| Sum of every currently negative long-term lot | -$2,260.20 |
| All negative lots | **-$11,386.02** |

The normalized full position table is in `current_positions_2026-10-23.csv`.

### 2026 realized activity through October 23

| Measure | Amount |
|---|---:|
| Proceeds | $463,191.40 |
| Adjusted basis | $455,121.22 |
| Net realized gain | **$8,104.89** |
| Short-term component | $8,104.89 |
| Long-term component | $0.00 |
| Wash-sale loss already disallowed in Schwab report | $34.71 |

The main realized gains are UNG $1,931.62, AMZN $1,737.43, OXY $1,370.83, PFE $771.00, BTC $641.04,
BOIL $495.84 and USO $405.37. The existing $34.71 wash adjustment is already included in Schwab's
adjusted figures; do not deduct it again.

## October 26 execution — completed

The exact user-confirmed fills are preserved in `executed_orders_2026-10-26.csv`. The realized figures
below apply the October 23 exported lot bases to the actual fills; Schwab's later realized-gain report
and final 1099-B remain controlling.

| Measure | Actual amount |
|---|---:|
| Gross sale proceeds | $42,159.75 |
| Gross replacement purchases | $30,379.04 |
| Net cash increase | **$11,780.71** |
| Estimated short-term loss | -$8,576.98 |
| Estimated long-term loss | -$2,263.56 |
| **Estimated harvested loss** | **-$10,840.54** |

| Sold | Actual fill | Estimated realized result | Replacement actually bought |
|---|---:|---:|---|
| AA 50 | $38.44 | -$1,653.00 ST | None |
| RBLX 50 | $53.336 | -$1,158.13 ST | None |
| CAG 303.5594 | $14.4024 | -$892.63 ST | None |
| BAC 51 | $50.7343 | -$319.55 ST | None |
| CCJ 45 | $79.12 | -$1,073.70 ST | NLR, combined with BWXT proceeds |
| KWEB 197 | $23.172 | -$233.92 ST / -$2,263.56 LT | MCHI 92 at $49.1499 |
| COPX 78 | $74.115 | -$911.54 ST | ICOP 119 at $48.35 |
| VWO 150 | $56.574 | -$641.12 ST | IEMG 112 at $75.48 |
| PICK 80 | $55.3324 | -$565.45 ST | MXI 41 at $106.525 |
| BWXT 29.1288 | $130.2001 | -$1,127.95 ST | NLR, combined with CCJ proceeds |

The combined NLR purchase was **80 shares at $91.0289**. Together with the previously reconciled
15-share Questrade position, the live aggregate is **95 NLR shares at a $95.420221 weighted average**.
The Questrade KWEB position remains **413 shares at $27.0145**; only the 197-share Schwab position was
sold.

### Original accepted order design

Use **Sell All** for every sale. All current lots in each swap position are below basis; full liquidation
also prevents a recently purchased lot from remaining behind as replacement property. Approximate buy
quantities use October 22 sponsor prices and must be recalculated from the actual sale proceeds.

### Exit without replacement

| Sell | Shares | Estimated loss | Reason |
|---|---:|---:|---|
| AA | 50 | -$1,673.58 | Confirmed permanent exit; existing review already places AA in the exit queue. |
| RBLX | 50 | -$1,186.93 | Confirmed permanent exit from the speculation position. |
| CAG | 303.5594 | -$750.68 net | Confirmed permanent exit; weaker and redundant with retained packaged-food exposure. |
| BAC | 51 | -$325.38 | Confirmed permanent exit; absent from the accepted allocation and portfolio records. |
| CCJ | 45 | -$1,096.65 | Combined CCJ/CCO.TO issuer exposure is already above the accepted Cameco target. |
| **Subtotal** |  | **-$5,033.22** |  |

Selling CAG in full realizes both positive and negative lots but remains an estimated $750.68 net loss.
Selling CCJ requires blocking purchases of both `CCJ` and `CCO.TO`, because they are two listings of the
same Cameco common equity.

### October 26 same-day tax swaps

| Sell | Est. loss | Buy after the sale fills | Approx. shares | Exposure change |
|---|---:|---|---:|---|
| KWEB 197 | -$2,491.96 | MCHI | 93 | China internet becomes broad China; appropriate as a 31-day bridge. |
| COPX 78 | -$971.94 | ICOP | 119 | Copper miners remain the core exposure, under a different index and sponsor. |
| VWO 150 | -$563.72 | IEMG | 113 | Broad emerging markets remain; benchmark and country classification differ. |
| PICK 80 | -$600.84 | MXI | 41 | Temporary bridge broadens into chemicals and forestry as well as mining. |
| BWXT 29.1288 | -$1,194.95 | NLR | 40 | Temporary bridge diversifies into uranium, generation and nuclear equipment. |
| **October 26 swap subtotal** | **-$5,823.41** |  |  |  |

Together with the five exits, the October 26 batch is approximately **-$10,856.63**. On the current
realized ledger, that batch alone would leave an estimated **-$2,751.74** net capital loss.

### November 16 same-day tax swap

| Sell | Est. loss | Buy after the sale fills | Approx. shares | Exposure change |
|---|---:|---|---:|---|
| VXUS 138.0697 | -$307.38 | IXUS | 123 | Broad developed/emerging ex-U.S. exposure remains under an MSCI index. |

VXUS includes 29 shares bought on October 16. Waiting through November 15 removes that acquisition from
the 30-day pre-sale window and avoids a partial wash-sale basis chain for a modest tax benefit. Execute
the November swap only if VXUS still has a meaningful unrealized loss.

Buy the replacement only after its paired sale fills and use the actual dollar proceeds. The share counts
above are guides, not limit prices or standing orders. Use limit orders near the live bid/ask midpoint and
avoid the opening minutes if spreads are unstable.

The replacements are **ASSUMED reasonable, not IRS-approved safe harbors**. Each uses a different index
or a materially broader basket, but the IRS has not published a mechanical rule declaring when two ETFs
cease to be “substantially identical.” A tax adviser can choose an even wider bridge if a zero-ambiguity
position is preferred.

## Arithmetic after the actual October 26 sales

| Component | Amount |
|---|---:|
| Existing Schwab short-term realized gain | +$8,104.89 |
| Actual estimated short-term losses | -$8,576.98 |
| Estimated net short-term loss | -$472.09 |
| Actual estimated KWEB long-term loss | -$2,263.56 |
| **Estimated total net capital loss after October 26** | **-$2,735.65** |

If the planned VXUS harvest still produces the previously estimated $307.38 loss on November 16, the
account would reach approximately a **$3,043.03 net capital loss**. Refresh the price and basis first;
if the loss disappears, stop after the completed October 26 batch.

Federal Schedule D first nets short-term items and long-term items, then combines the two net results.
With no other gains, the current estimated $2,735.65 net loss can reduce ordinary income. If the
provisional November VXUS transaction raises the loss to $3,043.03, $3,000 can reduce 2026 ordinary
income and approximately $43 would carry forward. Adobe or other gains will change that result.

### Estimated tax value — PROVISIONAL

“$400,000 disposable income” does not establish adjusted gross income or taxable income, so no exact tax
rate is claimed. If the relevant federal ordinary bracket is 24%–32%, California's marginal rate is 9.3%,
and the existing investment gains are subject to the 3.8% NIIT, the completed harvest plus the pending
VXUS step is roughly worth **$4,000–$4,900** for 2026 before trading slippage and any Adobe/outside
capital activity. The completed October 26 batch alone is slightly below that range because its net
loss is $264.35 below the $3,000 ordinary-income deduction ceiling.

That range assumes the current Schwab short-term gains are eliminated and the remaining loss deduction
reduces ordinary income. If Adobe generated capital gains, more of the loss will offset those gains and
the value will depend on whether they are short- or long-term.

## Exact wash-sale calendar

### Before the October 26 sale

1. Disable dividend reinvestment for AA, RBLX, CAG, BAC, CCJ/CCO.TO, KWEB, COPX, VWO, VXUS, PICK and
   BWXT in every account.
2. Cancel open buy orders, recurring investments, written puts and other contracts that can acquire any
   of those securities.
3. Confirm Hooman's wife will not purchase them in her own accounts during the window. Being only an
   authorized user on Hooman's account does not change ownership, but IRS Publication 550 separately
   applies the spouse-purchase rule.
4. Use full-position sales. The one material recent-purchase issue, VXUS, is deliberately delayed until
   November 16 rather than depending on a same-day replacement-basis chain.

### Blocked period

For an October 26 sale, do not acquire the sold security from **September 26 through November 25**, in
Hooman's taxable or retirement accounts or in his wife's accounts. Apply the block conservatively to
RRSP/TFSA accounts as well; the IRS authorities reviewed explicitly address U.S. IRAs and Roth IRAs,
not every foreign registered-account fact pattern.

The block includes options and contracts to acquire the security. For Cameco it includes both `CCJ` and
`CCO.TO`. Buying the different replacement ETFs is the intended exposure bridge.

The first calendar day outside the window is Thursday, November 26, which is Thanksgiving and a U.S.
market holiday. The first practical trading day is **Friday, November 27**; **Monday, November 30** is
the cleaner review date.

For the planned November 16 VXUS sale, block VXUS purchases from **October 17 through December 16**.
The first eligible repurchase date is **December 17**. Buying IXUS during that period is the intended
exposure bridge.

### November 30 review

- Return MXI to PICK if the accepted industrial-metals mandate still requires the narrower exposure.
- Return NLR to BWXT if the direct 0.5% BWXT role remains desired after total nuclear-sleeve sizing.
- Decide whether to retain or reverse MCHI, ICOP and IEMG based on portfolio fit and fees. Tax-loss
  harvesting does not require buying the originals back.
- Re-enable reinvestment only after the final fund choice is settled.

Review IXUS on December 17 or later. Do not rotate it back to VXUS on November 30 because that remains
inside the separate VXUS wash-sale window.

### December second pass

Run a second lot export during the week of **December 14**. Harvest only new material losses or known
exits, preferably by December 16 rather than December 31. For every additional sale, block the original
security for 30 days before and after that sale and use sale date plus 31 calendar days as the earliest
repurchase date.

## Positions deliberately left alone

| Position | Available loss | Decision |
|---|---:|---|
| CF high-basis 16-share lot | -$135.54 | Hold; CF remains an accepted quality agriculture holding and the benefit is small. |
| CLX | -$34.16 | Hold under the existing conditional profit-exit rule. |
| BKR | -$26.64 | Hold; current energy-export implementation remains active. |
| VTI | -$7.60 | Hold; trivial loss in a strategic core position. |
| Tiny GEV/BWXT/VXUS fractions | about -$8 | Captured only when the parent position is sold; otherwise ignore. |

## Adobe RSUs — remaining required reconciliation

The reported “$40,000 sold” is sale proceeds, not the capital gain. For RSUs, compensation value is
generally included in wages when the shares vest; capital gain or loss is then sale proceeds minus the
correct adjusted stock basis. A broker 1099-B may omit or understate that basis, so use the Adobe stock
plan's supplemental statement and vest records to prevent double taxation.

Before filing, add an Adobe export with acquisition/vest date, shares, vest-date fair market value,
sale date, proceeds and 1099-B reported basis. Until that is done, the household-wide $3,059 net-loss
figure and $4,000–$4,900 tax-value range remain provisional.

## Filing controls

- Preserve trade confirmations and the pre-sale and post-sale lot exports.
- Reconcile Schwab's final 1099-B wash-sale column to this schedule.
- Enter broker transactions on Form 8949/Schedule D as reported, with any documented basis correction.
- Give the tax preparer the Adobe supplemental statement and disclose Canadian registered accounts and
  cross-listed Cameco holdings.
- This plan does not determine foreign-asset reporting, RRSP/TFSA treatment or Canadian tax obligations.

## Primary sources

All links were opened on 2026-10-23.

### Tax rules

- IRS Publication 550 (2025 edition, revised in 2026), wash sales and capital-loss netting:
  https://www.irs.gov/pub/irs-pdf/p550.pdf
- IRS Topic 409, $3,000 deduction, carryforward and short-term ordinary rates:
  https://www.irs.gov/taxtopics/tc409
- IRS Revenue Ruling 2008-5, IRA purchase permanently disallowing the taxable-account loss:
  https://www.irs.gov/pub/irs-drop/rr-08-05.pdf
- IRS Publication 525, compensation and restricted-property basis principles:
  https://www.irs.gov/pub/irs-pdf/p525.pdf
- California FTB, capital gains taxed as ordinary income:
  https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html

### Replacement-fund evidence

- MCHI — MSCI China Index, 0.59% expense ratio:
  https://www.ishares.com/us/products/239619/ishares-msci-china-etf
- COPX — Solactive Global Copper Miners Total Return Index, 0.65% expense ratio:
  https://www.globalxetfs.com/funds/copx
- ICOP — STOXX Global Copper and Metals Mining Index, 0.47% expense ratio:
  https://www.ishares.com/us/products/332280/ishares-copper-and-metals-mining-etf
- VWO — Vanguard FTSE Emerging Markets ETF, 0.06% expense ratio:
  https://investor.vanguard.com/investment-products/etfs/profile/vwo
- IEMG — MSCI Emerging Markets Investable Market Index:
  https://www.ishares.com/us/products/244050/ishares-core-msci-emerging-markets-etf
- VXUS — FTSE Global All Cap ex US Index, 0.05% expense ratio:
  https://investor.vanguard.com/investment-products/etfs/profile/vxus
- IXUS — MSCI ACWI ex USA IMI Index:
  https://www.ishares.com/us/products/244048/ishares-core-msci-total-international-stock-etf
- PICK — MSCI ACWI Select Metals & Mining Producers ex Gold and Silver IMI, 0.39% expense ratio:
  https://www.ishares.com/us/products/239655/ishares-msci-global-metals-mining-producers-etf
- MXI — S&P Global 1200 Materials Sector Capped Index, 0.37% expense ratio:
  https://www.ishares.com/us/products/239748/ishares-global-materials-etf
- NLR — MVIS Global Uranium & Nuclear Energy Index, 0.52% net expense ratio:
  https://www.vaneck.com/us/en/investments/uranium-nuclear-energy-etf-nlr/

## Limitations

- Loss estimates move with market prices and must be refreshed at execution.
- The Adobe capital gain/loss is unknown.
- The income description is insufficient for an exact federal or California marginal rate.
- The Schwab export cannot show purchases or reinvestments in the wife's accounts or every Canadian
  account. The cross-account no-purchase rule is therefore an execution control, not a broker-verified fact.
- Fund-pair wash-sale treatment is a facts-and-circumstances judgment, not a published ETF safe harbor.
