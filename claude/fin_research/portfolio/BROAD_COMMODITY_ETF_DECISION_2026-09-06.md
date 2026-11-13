# Broad Commodity ETF Decision — BCI

**Decision date:** 2026-09-06  
**Original decision:** Use Aberdeen Standard Bloomberg All Commodity Strategy K-1 Free ETF (`BCI`) as
the portfolio's single broad-commodity core.

**Status:** Superseded after comparing BCI constituent-by-constituent with the existing portfolio. BCI
remains the preferred one-fund broad commodity ETF, but the portfolio already owns most of its major
categories. The revised modular implementation is documented in
`COMMODITY_IMPLEMENTATION_DECISION_2026-09-06.md`.

## Investor and Portfolio Context

- Hooman is currently a U.S. tax resident and a Canadian citizen.
- The holding may be placed in a U.S. or Canadian account, including taxable or RRSP, and either CAD or
  USD can be used when economically sensible.
- The commodity allocation is a tactical supercycle position of uncertain duration rather than a
  permanent strategic holding.
- The portfolio already has substantial energy and commodity-producer exposure. A broad fund should
  consolidate or replace concentrated exposure rather than simply increase the total commodity weight.

## Fund Comparison

| Fund | Economic coverage | Expense | Roll approach | Decision |
|---|---|---:|---|---|
| **BCI** | BCOMTR: 25 contracts representing 23 commodities | **0.26%** | Transparent scheduled index rolls, generally into contracts 1–3 months out | **Selected** |
| **ZCOM** | Same BCOMTR exposure as BCI | **0.30% estimated MER** | Same index methodology, implemented primarily with derivatives/swaps | Reject as default while U.S. tax resident |
| **PDBC** | Active portfolio; recent filings showed about 28 economic contracts despite a 14-commodity benchmark | **0.59% net / 0.74% gross** | Adviser actively selects contracts and later expiries to seek better roll yield | Aggressive alternative, not the core |
| **COM** | 12 eligible commodities, each either long or in cash | **0.72%** | Trend signals, volatility sizing and active contract selection | Drawdown-control alternative, not whole-complex exposure |

## Why BCI Won

1. **Breadth:** BCI persistently covers energy, agriculture and softs, precious metals, industrial metals,
   and livestock. COM omits several important markets and can move exposures to cash. PDBC's actual
   portfolio can be broad, but its adviser can deviate materially from its benchmark and recent exposure
   was much more energy-heavy.
2. **Portfolio fit:** The BCOM basket was approximately 36.6% energy, versus roughly 50% in PDBC's
   representative April 2026 basket. BCI therefore adds broader agriculture, metals and livestock exposure
   while creating less incremental overlap with the portfolio's existing XOM, CNQ and natural-gas exposure.
3. **Cost:** BCI's 0.26% expense ratio is below ZCOM's estimated 0.30% MER, PDBC's 0.59% net expense and
   COM's 0.72% expense.
4. **Transparency:** BCI follows a published, rules-based schedule. This makes the exposure and expected
   roll behavior easier to understand and monitor than PDBC's discretionary rolling or COM's long/flat
   trend system.
5. **Tax administration:** BCI is a U.S.-domiciled regulated investment company designed to issue Form
   1099 rather than a Schedule K-1. This simplifies U.S. tax reporting, although distributions can still
   contain taxable ordinary income and capital gains.

## Economic Holdings

BCI and ZCOM track the same Bloomberg Commodity Index Total Return. The July 31, 2026 ZCOM disclosure is
a useful look-through snapshot of the shared index exposure; BCI weights should be similar apart from
normal daily drift and implementation differences.

| Sector | Approximate index exposure | Weight |
|---|---|---:|
| Energy | Brent, WTI, natural gas, low-sulphur gasoil, ULSD/heating oil, RBOB gasoline | **36.63%** |
| Agriculture and softs | Soybeans, corn, soybean oil/meal, two wheat contracts, sugar, coffee, cotton, cocoa | **28.71%** |
| Precious metals | Gold and silver | **15.42%** |
| Industrial metals | Copper, aluminum, zinc, nickel and lead | **14.54%** |
| Livestock | Live cattle and lean hogs | **4.69%** |

Direct refined-product contracts represented approximately **12.19%**: low-sulphur gasoil 5.01%, ULSD
3.82% and RBOB gasoline 3.36%. There is no direct jet-fuel contract.

## Rolling Strategy

Commodity futures expire, so a fund must sell an expiring contract and buy a later one:

- In **contango**, the later contract costs more. Rolling creates a performance drag.
- In **backwardation**, the later contract costs less. Rolling contributes positively.
- **BCI/ZCOM** accept the published BCOM roll schedule. This is transparent and predictable but does not
  try to avoid an expensive scheduled roll.
- **PDBC** can choose later expiries in an attempt to improve roll yield. That flexibility may outperform,
  but the manager can also choose poorly or make the fund behave differently from the expected benchmark.
- **COM** combines active contract selection with trend signals that can move a commodity to cash. This
  may reduce drawdowns but can whipsaw or miss the beginning of a rebound.

For this portfolio, the broad core should be simple and rules-based because the existing single-name
commodity positions already introduce substantial tactical and active risk. PDBC is appropriate only if
Hooman deliberately chooses a higher-volatility, energy-heavy active bet. COM is appropriate only if
drawdown control matters more than maintaining continuous broad commodity exposure.

## Tax and Account Placement

| Account | Implementation | Rationale |
|---|---|---|
| Existing treaty-eligible RRSP | Prefer **BCI** | U.S. tax on income accruing inside an eligible RRSP is generally deferred until distribution; confirm the specific plan and reporting treatment |
| U.S. taxable brokerage | Prefer **BCI** | U.S.-domiciled, Form 1099 reporting and no PFIC issue |
| Canadian taxable account while U.S. resident | Avoid **ZCOM** | A Canadian-domiciled ETF is likely a PFIC and may require Form 8621 plus unfavorable/complex tax treatment |
| CAD-denominated account | Use BCI with an economical FX conversion when practical | ZCOM's CAD trading price does not itself provide meaningful CAD economic diversification |

The IRS instructions provide an annual Form 8621 reporting exception for PFIC stock held through certain
foreign pension arrangements covered by a U.S. income-tax treaty. Revenue Procedure 2014-55 provides U.S.
tax deferral treatment for eligible Canadian retirement plans. These rules do not eliminate all possible
RRSP reporting, including Form 8938 or FBAR where applicable. Confirm the specific account and filings with
a qualified U.S.-Canada cross-border tax adviser before execution.

Do not contribute to or transfer assets into an RRSP solely for this trade without tax review. If the RRSP
is already funded and treaty treatment is properly established, it is the preferred location; otherwise,
use a U.S. taxable brokerage.

## Implementation Guardrail

BCI is the chosen **vehicle**, not authorization to increase the portfolio's total commodity risk. At the
time of the decision, commodity-policy sleeves were already approximately 33.9% of the portfolio, near the
33.5% target. Establish BCI by reducing overlapping or exit-designated commodity positions and validating
current holdings, account cash and tax lots first.

## Primary Sources

- BCI fact sheet: <https://www.aberdeeninvestments.com/docs?editionId=e08e3839-182a-450f-b524-301a91e9177a>
- BCI SEC prospectus: <https://www.sec.gov/Archives/edgar/data/1597934/000199937126009673/bci-497k_050126.htm>
- ZCOM fact sheet: <https://df.bmogam.com/assets/static/etf-profiles-pdfs/BMO-Broad-Commodity-ETF-Factsheet-ZCOM.pdf>
- PDBC SEC summary prospectus: <https://www.sec.gov/Archives/edgar/data/1595386/000119312526079092/d67468d497k.htm>
- PDBC SEC semiannual report: <https://www.sec.gov/Archives/edgar/data/1595386/000119312526295451/8ded75689975687.htm>
- COM fact sheet: <https://www.direxion.com/uploads/COM-Fact-Sheet.pdf>
- Bloomberg 2026 target weights: <https://assets.bbhub.io/professional/sites/27/BCOM-2026-Target-Weights.pdf>
- IRS Form 8621 instructions: <https://www.irs.gov/instructions/i8621>
- IRS Revenue Procedure 2014-55: <https://www.irs.gov/pub/irs-drop/rp-14-55.pdf>
- IRS Form 8938 instructions: <https://www.irs.gov/instructions/i8938>
