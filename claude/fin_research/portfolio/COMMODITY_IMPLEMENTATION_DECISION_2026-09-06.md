# Commodity Implementation Decision — Modular Rather Than BCI

**Decision date:** 2026-09-06  
**Status:** Current portfolio structure; individual trades still require account and tax-lot review.

## Decision

Do not add BCI. It remains an effective one-fund commodity portfolio, but it is inefficient as an
incremental holding because the portfolio already owns dedicated gold, copper, natural-gas and
agriculture exposures.

Use the existing 33.5% commodity-policy allocation as follows:

| Sleeve | Target structure |
|---|---:|
| Agriculture | 2% PDBA plus up to 1% CF if the dividend-company thesis is retained |
| oil-companies | 6% selected oil and energy companies |
| ref_oil_prod | 2% DBE |
| nat_gas | 1% UNG |
| copper | 2% dedicated copper holdings |
| industrial_metals | 1% PICK if broader producer exposure is desired |
| Gold | 14% physical bullion, MNT and/or GLDM |
| Silver/platinum | 1% direct metal vehicles |
| Uranium/AI-power | 3.5% separate uranium/nuclear holdings |

## Why BCI Is Not Needed

- PDBA already covers the complete agriculture and livestock complex. Its April 30, 2026 portfolio
  included 14.4% live cattle, 10.5% lean hogs and 6.9% feeder cattle, or 31.8% livestock, alongside
  grains, soy products and soft commodities.
- Gold is intentionally much larger than its BCI weight and should remain separately controlled.
- Copper, natural gas and energy-company exposure already exist.
- BCI's genuinely missing exposures are direct crude/refined-product futures and industrial metals
  beyond copper. Those gaps are better evaluated separately than acquired with another large allocation
  to agriculture and gold.

## Refined Products

There is no attractive liquid U.S.-listed ETF holding only gasoil, ULSD/heating oil and RBOB gasoline.
ULSD is the diesel/heating-oil futures contract rather than a separate fourth category.

DBE is the nearest one-fund implementation. On June 30, 2026 it held 33.19% Brent, 28.89% WTI, 14.36%
gasoil, 10.22% ULSD, 7.26% RBOB gasoline and 6.08% natural gas. Its refined-products weight was therefore
31.84%. A 2% portfolio allocation contributes approximately 0.64% direct refined-products exposure.
DBE charges a 0.75% management fee plus operating expenses and issues a Schedule K-1. The separate
`ref_oil_prod` target is 2%; it replaces part of the former combined energy allocation rather than
increasing the portfolio's aggregate 9% energy-related target.

UGA is not preferred: it holds only gasoline, reported 1.08% total annual expenses and also issues a
Schedule K-1. CRAK is a possible 1099-reporting dividend-equity alternative at 0.61% net, but it owns
refining companies and tracks refining margins rather than refined-product prices.

## Industrial Metals

No liquid direct-futures ETF was identified that owns aluminum, nickel, zinc and lead while excluding
copper. DBB was rejected because it charges a 0.75% management fee plus expenses, issues a Schedule K-1
and was 48.35% copper on June 30, 2026.

PICK is the lower-cost liquid alternative if mining-company exposure is acceptable. It charges 0.39%,
had approximately $2.6 billion of assets and a 2.22% trailing yield on September 4, 2026, and excludes
gold and silver. It is not a direct-metals fund and includes diversified miners and steel producers.

EVMT is closer to a direct electrification-metals basket and issues no K-1. Its April 30, 2026 mix was
22.9% copper, 27.3% aluminum, 26.7% nickel, 16.7% cobalt, 3.6% lithium and 2.8% iron ore. It was rejected
as a core holding because it had only $5.7 million in assets and very thin trading volume. Its net expense
ratio is 0.59% under a waiver through August 31, 2027.

## Implementation Guardrails

- Track the former 9% combined energy target as three distinct sleeves: 6% `oil-companies`, 2%
  `ref_oil_prod`, and 1% `nat_gas`.
- Keep PDBA as the agriculture/livestock vehicle; do not use BCI to duplicate it.
- Track metals as separate 2% `copper` and 1% `industrial_metals` sleeves. PICK is optional rather than
  required because it is mining-company equity, not direct metals exposure.
- Do not use DBE or other Schedule K-1 commodity pools in an account without confirming that account's
  tax handling. Do not use them in the HSA.
- Preserve `FR_Portfolio!E1:K23` unchanged; it is Hooman's manually maintained notes area.

## Primary Sources

- PDBA/EVMT shareholder report: <https://www.sec.gov/Archives/edgar/data/1595386/000119312526295451/8ded75689975687.htm>
- PDBA prospectus: <https://www.sec.gov/Archives/edgar/data/1595386/000119312526079091/d67468d497k.htm>
- DBE filing: <https://www.sec.gov/Archives/edgar/data/1383062/000119312526338714/dbe-20260630.htm>
- DBE prospectus: <https://www.sec.gov/Archives/edgar/data/1383062/000119312526368460/d67266d424b3.htm>
- DBB filing: <https://www.sec.gov/Archives/edgar/data/1383084/000119312526338712/dbb-20260630.htm>
- DBB prospectus: <https://www.sec.gov/Archives/edgar/data/1383084/000119312526368423/d18044d424b3.htm>
- UGA prospectus: <https://www.sec.gov/Archives/edgar/data/1396878/000207187626000123/i26206_uga-424b3.htm>
- PICK fund page: <https://www.ishares.com/us/products/239655/ishares-msci-global-metals-mining-producers-etf>
- CRAK fund page: <https://www.vaneck.com/us/en/investments/oil-refiners-etf-crak/overview/>
