# Inflation Measurement Framework for Treasury Decisions — 2026-10-02

## Conclusion

There is no single objectively “true” inflation rate for Hooman. Three different questions require
three different measurements:

1. **Treasury-relevant inflation:** persistent national inflation and the inflation expectations
   embedded in bond prices. This determines whether nominal VGIT duration is attractive.
2. **Personal Bay Area inflation:** the change in Hooman's actual rent, food, energy, transportation,
   healthcare and other household costs. This determines whether his purchasing power is improving.
3. **House and asset affordability:** Bay Area home prices, mortgage rates and the prices of assets
   Hooman may need to buy. This is an important liability and opportunity-cost measure, but it is not
   consumer inflation and should not be averaged into CPI.

The concern that CPI understates Hooman's experience is **credible**, but the evidence does not show
that CPI is fabricated. It shows that CPI answers a different question using national-average weights,
slow-moving shelter measures and no home-purchase or financial-asset prices.

The original VGIT gate based only on the 10-year real yield and breakeven inflation is therefore too
narrow. Under the conservative multi-source framework below, the current inflation signal is
**YELLOW, not GREEN**. A 1% VGIT starter is economically defensible, but the conservative decision is
to wait for the next official release and a verifiable current Truflation reading before converting
the Treasury proposal into a confirmed allocation decision.

No portfolio target or trade is changed by this review.

**Status update — 2026-10-06:** Hooman subsequently accepted a 5% VGIT target funded from Global Equity
Core and bought an initial 53 shares at $56.6181. This does not retroactively turn the October 2
inflation signal GREEN; refresh the gate before adding further tranches.

## What the Current Data Actually Say

### Latest annual inflation readings

| Measure | Latest reading | As of | Interpretation |
|---|---:|---|---|
| U.S. CPI, all items | 3.40% YoY | Aug. 2026 | Headline remains above target, largely energy-sensitive |
| U.S. CPI excluding food and energy | 2.45% YoY | Aug. 2026 | Underlying CPI is materially cooler than headline |
| Core PCE | 3.01% YoY; 2.05% 3-month annualized | Aug. 2026 | Borderline YoY, but recent momentum is cooler |
| Cleveland Fed median CPI | 2.44% 3-month annualized | Aug. 2026 | Broad underlying inflation is near the desired zone |
| Cleveland Fed trimmed-mean CPI | 1.83% 3-month annualized | Aug. 2026 | Recent breadth is not signaling runaway inflation |
| Dallas Fed trimmed-mean PCE | 2.19% YoY | Aug. 2026 | Persistent inflation measure is close to target |
| San Francisco-area CPI | 3.39% YoY | Aug. 2026 | Similar headline rate to national CPI |
| San Francisco-area core CPI | 2.99% YoY | Aug. 2026 | Local underlying inflation is higher than national core CPI |
| San Francisco-area food | 3.09% YoY | Aug. 2026 | Moderate current inflation after a large cumulative rise |
| San Francisco-area shelter | 2.64% YoY | Aug. 2026 | Measures the broad occupied housing stock, not current asking rents |
| San Francisco-area energy | **12.27% YoY** | Aug. 2026 | Directly validates Hooman's high-energy-cost experience |
| Zillow San Francisco asking-rent index | **10.85% YoY** | Aug. 2026 | New-market rents are rising much faster than CPI shelter |
| Zillow San Francisco home-value index | 2.27% YoY | Aug. 2026 | Home prices rose moderately |
| Estimated mortgage-payment cost for the same priced home | **12.6% YoY** | Oct. 2026 | 7.28% mortgage rate versus 6.34% one year earlier plus higher home price |

The current divergence is not subtle: BLS local shelter inflation is 2.64%, while Zillow's market-rent
index is up 10.85%. Both can be statistically correct. BLS measures rent changes across the occupied
housing stock, including tenants whose rent did not reset; Zillow measures the rent available to a
person entering or changing leases. Hooman's actual lease renewal—not either aggregate—is the right
personal number.

### Why prices still feel much worse even when annual inflation slows

Inflation is the rate of change, not the price level. Slower inflation means prices rise more slowly;
it does not undo prior increases.

From August 2020 through August 2026:

| Bay Area measure | Cumulative increase |
|---|---:|
| CPI, all items | 23.3% |
| Food | 30.4% |
| Shelter | 14.5% |
| Energy | **66.2%** |
| Zillow asking rent | 27.6% |
| Zillow home value | 20.4% |

Hooman's statement that food, housing and energy feel dramatically more expensive is therefore
consistent with the data even if the current annual inflation rate is around 3%.

## Why CPI Can Understate Hooman's Experience

### CPI's legitimate purpose

CPI measures the average price change for a broad urban-consumer basket. It is designed for a
population, not for a specific high-income Bay Area renter preparing to buy a home. The most important
differences are:

- **Different weights:** Hooman reports that necessities collectively represent roughly 80% of
  spending. National weights cannot reproduce that exposure.
- **Shelter lag:** rent observations cover the occupied housing stock and reset gradually. New leases
  and mortgage-financed home purchases can move much faster.
- **Owner housing treatment:** CPI uses owners' equivalent rent as the consumption value of housing.
  It deliberately excludes home prices and mortgage principal because a home is treated as an asset.
- **Geography:** national CPI blends very different local economies. Even the San Francisco index is
  an area average, not Hooman's neighborhood, lease or utility plan.
- **Quality and substitution adjustments:** CPI attempts to separate a product's quality improvement
  from pure inflation and allows limited substitution among similar items. Those are defensible for an
  economic index but may not match the sticker-price experience of buying the preferred item.
- **Taxes and asset purchases:** income taxes, stock prices, gold and the purchase price of a house are
  outside consumer inflation even though they affect personal purchasing power.

These are measurement-design differences, not evidence that the published figures are knowingly
false. CPI remains necessary because TIPS principal, contracts and many market expectations reference
official inflation. It is insufficient as Hooman's only measure.

## Truflation: Useful but Not the Truth Oracle

Truflation's March 2026 methodology states that it uses more than 30 providers and over 15 million
price points across 12 consumption categories. Its strengths include:

- daily publication rather than a monthly lag;
- transaction, listing and market-price sources;
- housing inputs from sources including Zillow, Redfin, Apartment List, Numbeo and rental indexes;
- explicit inclusion of both new and existing rents; and
- broader owned-housing costs, including mortgages, taxes, maintenance and insurance.

Its limitations are material:

- the methodology and validation claims are published by Truflation itself;
- many underlying commercial datasets cannot be independently reproduced;
- the provider set, weights and calculation model can change;
- monthly and weekly inputs are carried forward between updates, even though the headline is daily;
- its published history is short compared with CPI/PCE;
- no meaningful independent peer-reviewed validation was found in OpenAlex or Crossref; and
- the public dashboard/API failed to return a current unauthenticated value during this review.

**Verdict:** use Truflation as a high-frequency confirmation and turning-point indicator, with about
the same decision weight as one good regional/private dataset. Never let it override CPI, PCE,
trimmed-mean measures and market expectations by itself. A current reading that cannot be retrieved
and archived is `UNVERIFIED` and cannot satisfy a VGIT entry gate.

## The Exact Measurement System

### Panel 1 — Treasury inflation regime: the trade gate

This panel determines whether nominal VGIT is attractive. It must use independent kinds of evidence:

| Block | Measures | GREEN condition |
|---|---|---|
| Real compensation | 5- and 10-year TIPS real yields | 10-year real yield at least 2.75% |
| Market inflation | 5-year, 10-year and 5y5y breakevens | 10-year at most 2.50%; 5y5y at most 2.60% |
| Model expectations | Cleveland Fed 5- and 10-year expected inflation | Both at most 2.75% |
| Persistent official inflation | Core PCE YoY and 3-month annualized; Dallas trimmed PCE; Cleveland median and trimmed CPI | At least three of four at or below 3.0%, with no broad three-month acceleration above 3.5% |
| High-frequency confirmation | Truflation 30-/90-day trend plus independent rent/energy/online-price data | Truflation at most 3.25% and not up over 0.50 points in 90 days; at least one independent source agrees |

Breakevens are not perfect forecasts: they include inflation-risk and liquidity premia. That is why
they are used alongside survey/model expectations and realized inflation rather than alone.

### Panel 2 — Hooman Personal Cost Index

This measures the annual change in the cost of the same standard of living:

`Personal inflation = sum(category spending weight × category price change)`

Use actual trailing-12-month after-tax household outflows, excluding savings, investments, debt
principal and transfers between accounts. The categories should be:

- current rent and renter costs;
- utilities by unit price where available;
- food at home and restaurants;
- gasoline, insurance, maintenance and transportation;
- healthcare premiums and out-of-pocket costs; and
- all remaining recurring consumption.

The answer “80%” is interpreted as housing, food, energy/transportation and healthcare collectively
representing approximately 80% of spending. It does not provide the category split, so an exact
personal rate cannot yet be claimed. Until actual weights are available:

- use Hooman's actual rent change for housing, not CPI shelter or Zillow;
- use San Francisco CPI category changes for the other necessities;
- use Zillow rent as the stress case faced when moving or renewing at market; and
- report a range rather than false precision.

Using CPI shelter can produce a roughly 3%-4% personal-rate estimate today; using current asking rent
for a renter facing a market reset can push the estimate toward roughly 7%-9%, depending on housing's
true weight. The wide range is why actual spending and lease data matter more than choosing a favorite
headline index.

Personal inflation is a **position-size modifier**, not the sole Treasury timing signal:

- below 4% and stable: no restriction;
- 4%-6% or concentrated in one volatile category: cap the first nominal-duration purchase at 1%;
- above 6% across several categories: delay further VGIT additions and retain the real-asset hedge;
- above 6% only because market rent or mortgage rates jumped: distinguish current cash-flow exposure
  from future house affordability before rejecting VGIT.

### Panel 3 — House and asset affordability

Track these separately rather than corrupting the consumer index:

- **House-purchase liability:** Bay Area home-price index multiplied by the 30-year mortgage payment
  factor, plus property tax and insurance when data are available.
- **Financial assets:** VTI/S&P 500, gold and other assets Hooman expects to buy or already owns.
- **Income denominator:** after-tax income and liquid investable assets.

The current signals are mixed: Bay Area home values rose approximately 2.3% YoY, estimated mortgage
payments for the same home rose approximately 12.6%, the S&P 500 rose approximately 16%, gold rose
approximately 8%, and bitcoin fell approximately 30%. Averaging these into one “inflation” number
would be arbitrary and misleading.

For Hooman, house-payment inflation is the important asset-liability measure. It does not automatically
argue against VGIT: if recession lowers Treasury and mortgage yields, VGIT should appreciate while the
future mortgage becomes cheaper. Intermediate Treasuries can therefore partially hedge house-financing
rate risk, although they do not hedge a Bay Area home-price surge.

## Conservative VGIT Decision Rule

### Entry

1. **Starter up to 1%:** all market and real-yield conditions in Panel 1 must be green, at least three
   persistent-inflation measures must be green, and the high-frequency block must be verified rather
   than missing.
2. **Second 1% near a 5.5% nominal ten-year:** the above conditions must still hold; do not add if
   personal broad-based inflation exceeds 6%.
3. **Final 1%-3% near 5.75%-6.0%:** real yield must remain at least 3%, 10-year breakeven must remain
   below 2.75%, and neither Truflation nor persistent official measures may show broad acceleration.
4. **Hard inflation stop:** no nominal-duration additions if the 10-year breakeven exceeds 3%, the
   5y5y forward exceeds 2.75% persistently, or at least two persistent measures exceed 3.5% and rise.

### Current status: YELLOW

| Block | Current evidence | Status |
|---|---|---|
| Real yield | 10-year real yield 2.93% | GREEN |
| Market breakevens | 5-year, 10-year and 5y5y all approximately 2.36% | GREEN |
| Model expectations | Cleveland 5-year 2.58%; 10-year 2.57% | GREEN |
| Persistent official inflation | Core PCE 3.01% YoY; trimmed PCE 2.19%; median CPI 2.44% 3m; trimmed CPI 1.83% 3m | GREEN/YELLOW |
| Bay Area personal proxies | CPI 3.39%, energy 12.27%, Zillow asking rent 10.85% | RED/MIXED |
| Truflation | Methodology reviewed; live current value not independently retrieved | UNVERIFIED |

The bond-market case is attractive, but the required independent high-frequency confirmation is
missing and local cost pressure is elevated. Under Hooman's conservative preference, **do not yet
promote the VGIT plan to a confirmed portfolio decision**. Recheck after the next CPI/PCE release and
after capturing a current Truflation observation. If those confirm disinflation, the 1% starter gate
will be satisfied without waiting for a 6% nominal ten-year yield.

## Sources

### Official inflation and methodology

- BLS public data API:
  https://www.bls.gov/developers/api_signature_v2.htm
- BLS CPI questions and answers:
  https://www.bls.gov/cpi/questions-and-answers.htm
- BLS owners' equivalent rent and rent methodology:
  https://www.bls.gov/cpi/factsheets/owners-equivalent-rent-and-rent.htm
- BEA PCE price index:
  https://www.bea.gov/data/personal-consumption-expenditures-price-index
- Cleveland Fed median and trimmed-mean CPI:
  https://www.clevelandfed.org/indicators-and-data/median-cpi
- Dallas Fed trimmed-mean PCE:
  https://www.dallasfed.org/research/pce

### Market expectations

- 10-year real Treasury yield:
  https://fred.stlouisfed.org/series/DFII10
- 5-year breakeven inflation:
  https://fred.stlouisfed.org/series/T5YIE
- 10-year breakeven inflation:
  https://fred.stlouisfed.org/series/T10YIE
- 5-year, 5-year forward inflation expectation:
  https://fred.stlouisfed.org/series/T5YIFR
- Cleveland Fed expected inflation:
  https://www.clevelandfed.org/indicators-and-data/inflation-expectations

### Independent and local sources

- Zillow research data, ZORI and ZHVI:
  https://www.zillow.com/research/data/
- Freddie Mac 30-year mortgage rate:
  https://fred.stlouisfed.org/series/MORTGAGE30US
- Truflation U.S. index page:
  https://truflation.com/marketplace/truflation-us
- Truflation methodology v1.4, retrieved 2026-10-02:
  https://ddsvqvocwuhvopwpzmgo.supabase.co/storage/v1/object/public/site-files/indexes/1774868904122-TruCPI-US%20Index%20-%202026%20-%20Methodology%20v1.4%20(2026-03-26).pdf

## Confidence

- Official CPI/PCE, FRED market series, Zillow data and mortgage-rate calculations: **VERIFIED**.
- Truflation methodology description: **VERIFIED as Truflation's own published methodology**; its
  claims of superiority are not independently verified.
- Current Truflation level: **UNVERIFIED** because the public data endpoint required authentication or
  failed during retrieval.
- Hooman's 80% necessities share: **USER-CONFIRMED**, but the internal category weights remain unknown.
- Personal inflation range: **ASSUMED sensitivity range**, not an observed personal rate.
