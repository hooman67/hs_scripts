# Stage 2.5b — Financials-Specific Value + Quality Screen (Global)

**A sector-appropriate value+quality screen for banks, insurers, diversified financials
(and REITs as a separate sub-group)** — the businesses the generic Stage 1b screen
structurally *cannot* rank. Emphasis on **EM + developed-ex-US**, since Stage 1a flagged
**EM Life Insurance** as one of the cheapest AND highest-quality EM sectors (ROIC ~15%,
ROE ~17.6%) and cheap financials matter to Hooman's ex-US diversification goal.

- **Run date / as-of:** yfinance `.info` snapshot pulled **2026-07-02** (timestamp on every
  cached row, e.g. `2026-07-02T01:15:33+00:00`). Prices/multiples move daily — treat every
  number as as-of that pull.
- **Source:** **yfinance** (Yahoo Finance) for all fundamentals; US Financials/Real-Estate
  membership from the **Wikipedia S&P 500 GICS list** (cached from Stage 1b, cited). No EDGAR
  cross-check in this breadth-first stage (that is a Stage-3/4 job on survivors).
- **Owner:** Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.**
- **Code:** `screens/financials_universe.py` (universe), `screens/run_financials_screen.py`
  (fetch + derive + score). Data cached under `data/cache/yf_*.json`.
- **Outputs:** `screens/financials_screen_raw.csv` (304 rows, all pulled fields),
  `screens/financials_screen_all.csv` (304 rows incl. `live`/`rankable`/`trap_status`/flags),
  `screens/financials_screen_ranked.csv` (272 rankable, scored).

> ⚠️ **ANTI-HALLUCINATION:** every ratio below is a real yfinance pull on 2026-07-02.
> Missing fields are left blank, never guessed. Tickers that returned no data were **dropped
> and logged** — no fabricated tickers survive (0 dead in the final run). NIM / CET1 /
> combined ratio / P-tangible-book / price-to-embedded-value are **not on yfinance** and are
> reported as unavailable, never invented (see §5). yfinance is a *secondary* source — any
> name advancing to a deep dive must be cross-checked vs filings. Confidence on individual
> pulled fields: **VERIFIED** (real fetch) but **UNVERIFIED** vs a second source; confidence on
> the ranking: **ASSUMED** (single-source, snapshot, proxy capital metric).

---

## 1. Methodology — why financials need different metrics

The generic Stage 1b screen ranks on **gross margin, EV/EBITDA, EBIT/EV earnings yield** and a
ROIC proxy built from EV. **None of these apply to a balance-sheet business:** a bank's
"revenue" and margins aren't comparable to an industrial's; EV is meaningless when deposits/
policy reserves *are* the business; EBITDA is not a concept for a bank or insurer. That is why
Stage 1b dropped **85 names, mostly financials/REITs**, and why EM Life Insurance — a cheap,
high-quality EM sector per Stage 1a — never got scored. This screen fixes that with the
metrics practitioners actually use for financials.

### Value metrics (financials)
| Metric | yfinance field | Why |
|---|---|---|
| **P/B** | `priceToBook` | **THE** primary valuation gauge for banks/insurers — price vs the equity capital that generates earnings. |
| **P/E** | `trailingPE` | Earnings multiple; pairs with P/B via ROE (P/B ≈ P/E × ROE). |
| Fwd P/E | `forwardPE` | Context only (analyst-estimate based). |
| **Dividend yield** | `dividendYield` (a %) | Financials are income-heavy; a high, *covered* yield is part of the return. |
| Payout ratio | `payoutRatio` | Dividend **sustainability** (trap input). |

### Quality metrics (financials)
| Metric | yfinance field | Why |
|---|---|---|
| **ROE** | `returnOnEquity` | **THE** key quality metric for financials. High ROE + low P/B = cheap quality. |
| **ROA** | `returnOnAssets` | Capital efficiency. For banks a low ROA (~1%) is normal (levered balance sheet); for insurers it's higher. |
| **Capital-strength proxy** = ROA/ROE | derived | = equity/assets = 1/(equity multiplier). **Higher = less levered = stronger capital.** A *crude* yfinance stand-in because CET1 (banks) and combined ratio (insurers) are **not available** (§5). |
| Earnings stability | `earningsGrowth` | A large negative reading flags earnings collapse (trap signal). |

### Trap filter (financials)
A cheap bank/insurer is only a bargain if quality is intact. A name is **flagged** (not silently
dropped) when any of:
- **ROE ≤ 0** or **ROE < 5%** (de-minimis return on capital);
- **earnings collapsing** (`earningsGrowth < −40%`);
- **payout > 100%** (dividend not covered by earnings — sustainability risk);
- **classic value trap:** P/B < 0.6 **with** ROE < 8% (cheap *because* returns are weak, e.g. a
  bank at 0.4x book with collapsing ROE is a trap, not a bargain).

`trap_status = PASS` means none tripped. Flags are shown in the tables, not hidden.

### Scoring — quality-first, ranked WITHIN region × sub-group
Per the project's quality-first mandate, and so a cheap EM bank is judged against **EM banks**
(not against US asset managers), every rankable name is **percentile-ranked within its
peer group** = `region × sub-group` (banks vs banks; EM life insurers vs EM life insurers):
- **Quality composite** = mean of pctl(ROE), pctl(ROA), pctl(capital proxy).
- **Cheapness composite** = mean of pctl(low P/B), pctl(low P/E), pctl(high div yield).
- **Combined = 0.60·Quality + 0.40·Cheapness.**

Results are reported **per region** (EM / DEV_EXUS / US) so EM names get a fair shot and are
not crowded out by the larger US count.

### Data-quality guards (so artifacts don't drive the rank)
- **ADR duplicates removed:** when a company appears as both a US ADR and its native listing
  (e.g. `HSBC`+`HSBA.L`, `BBVA`+`BBVA.MC`, `ITUB`+`ITUB4.SA`, `MFC`+`MFC.TO`, `MUFG`+`8306.T`),
  the ADR is dropped from ranking and the **native** listing kept (13 ADR dupes removed).
- **P/B glitch guard:** P/B < 0.05 for a going concern is a Yahoo share-class/currency artifact
  (e.g. **BRK-B** returned P/B ≈ 0.001 — B-share price vs A-share-scaled book) → flagged and
  excluded from ranking. Genuinely-cheap distressed names (China Cinda P/B 0.17) survive.

### Universe (304 names, `screens/financials_universe.py`)
| Region | n | How built |
|---|--:|---|
| **US** | 107 | S&P 500 **Financials** (76) + **Real Estate/REIT** (28+) GICS members (Wikipedia list, cited). |
| **DEV_EXUS** | 118 | Curated large developed-ex-US: UK (FTSE financials), Switzerland, Germany, France, Benelux, Spain, Italy, Nordics, **Japan** megabanks+insurers, **Canada** Big-Six+lifecos, **Australia** Big-Four+insurers+Macquarie, + developed-market ADRs. |
| **EM** | 79 | Curated large EM: **China/HK** (life insurers **priority** + big-4 banks + CMB), **India** (banks + NBFCs + the listed life insurers incl. **LIC**), **Brazil, Mexico, South Africa, SE Asia** (Indonesia/Singapore/Malaysia/Thailand), **Taiwan/Korea**. |

Sub-groups (from yfinance `industry`): **BANK, INSURER_LIFE / _PC / _REINS / _DIV, DIVFIN**
(asset mgmt / exchange / broker / consumer finance), **REIT** (separate sub-group).

---

## 2. Coverage report (informs the paid-API question)

**Overall: 304 fetched, 0 dead, 272 rankable.** yfinance covers financials **very well** — the
core fields (P/B, ROE) that were "missing by nature" in the generic screen are present at
94–98%.

| Field | Present | Field | Present |
|---|--:|---|--:|
| priceToBook | **98%** (299/304) | returnOnEquity (ROE) | **96%** (291/304) |
| trailingPE | 97% | returnOnAssets (ROA) | 96% |
| forwardPE | 100% | payoutRatio | 98% |
| dividendYield | 96% | bookValue | 98% |
| cap proxy (ROA/ROE) | 94% | earningsGrowth | 90% |

| Region | n | **P/B + ROE both present** |
|---|--:|--:|
| US | 107 | **95%** (102/107) |
| DEV_EXUS | 118 | **97%** (115/118) |
| **EM** | 79 | **87%** (69/79) |
| **All** | 304 | **94%** (286/304) |

**Read:** the two load-bearing financial metrics (P/B + ROE) are present for **94% of the whole
universe and 87% of EM** — a dramatic improvement over the generic screen, which had *0%*
usable coverage on these names because it asked for the wrong metrics. **yfinance is sufficient
for a large-cap global financials screen.** The EM 87% (vs 95–97% developed) is the only soft
spot, concentrated in a few local-only lines that returned a partial `.info`.

**Fields yfinance LACKS for financials** (the concrete case for a paid API — §5): NIM, CET1 /
regulatory capital, loan-loss/NPL ratios (banks); combined ratio, embedded value / value of
new business (insurers); tangible book / P-tangible-book; FFO/AFFO (REITs).

---

## 3. Per-region ranked tables

Columns: **P/B**, **P/E** (trailing), **DY%** (dividend yield), **ROE%**, **ROA%**,
**Cap%** = ROA/ROE capital-strength proxy (higher = less levered), **Score** = combined
(quality-first, ranked within region×sub-group), **Trap** = trap-filter status. MktCap in the
company's **native currency** (do NOT compare across currencies without FX). All numbers
yfinance, **as-of 2026-07-02**. Blank = field not returned.

### 3A. EMERGING MARKETS

**EM — Insurers (life-heavy; the Stage 1a priority sector)**
| Ticker | Name | Country | Sub | MktCap | P/B | P/E | DY% | ROE% | ROA% | Cap% | Score | Trap |
|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|---|
| BBSE3.SA | BB Seguridade | Brazil | INS_DIV | 74B BRL | 5.86 | 8.0 | 13.7 | 75.6 | 32.81 | 43.4 | 81 | PASS |
| SLM.JO | Sanlam | South Africa | INS_LIFE | 186B ZAc | 1.83 | 11.8 | 5.6 | 16.9 | 6.61 | 39.1 | 69 | earnings_collapsing |
| PSSA3.SA | Porto Seguro | Brazil | INS_DIV | 34B BRL | 2.18 | 9.3 | 3.9 | 25.2 | 6.09 | 24.2 | 68 | PASS |
| **2328.HK** | **PICC P&C** | China | INS_PC | 313B HKD | **0.95** | 6.7 | 5.4 | **14.7** | 3.87 | 26.3 | 67 | PASS |
| **0966.HK** | **China Taiping** | Hong Kong | INS_LIFE | 68B HKD | **0.71** | 2.6 | 6.8 | **25.5** | 1.23 | 4.8 | 65 | PASS |
| 6060.HK | ZhongAn Online | China | INS_PC | 16B HKD | 0.54 | 11.5 | — | 4.8 | 3.46 | 72.8 | 64 | ROE<5%;cheap_low_ROE_trap |
| **1336.HK** | **New China Life (NCI)** | China | INS_LIFE | 148B HKD | 1.04 | 3.5 | 6.7 | **36.3** | 1.44 | 4.0 | 62 | PASS |
| **1339.HK** | **PICC Group** | China | INS_PC | 211B HKD | **0.57** | 4.1 | 5.3 | 14.0 | 2.30 | 16.5 | 62 | PASS |
| Q.MX | Qualitas | Mexico | INS_PC | 71B MXN | 2.64 | 15.8 | 7.8 | 16.8 | 3.54 | 21.1 | 62 | PASS |
| **2601.HK** | **CPIC (China Pacific)** | China | INS_LIFE | 265B HKD | **0.72** | 4.4 | 4.9 | 17.4 | 1.41 | 8.1 | 58 | PASS |
| **2628.HK** | **China Life** | China | INS_LIFE | 794B HKD | 1.15 | 4.8 | 3.6 | **25.5** | 1.50 | 5.9 | 56 | PASS |
| 2881.TW | Fubon Financial | Taiwan | INS_LIFE | 1.6T TWD | 1.67 | 14.3 | 3.5 | 18.7 | 2.01 | 10.7 | 52 | PASS |
| 2318.HK | Ping An | China | INS_LIFE | — HKD | 0.79 | 6.1 | 6.0 | 11.3 | 0.98 | 8.7 | 46 | PASS |
| 1299.HK | AIA | Hong Kong | INS_LIFE | — HKD | 1.96 | 13.8 | 2.7 | 14.8 | 1.87 | 12.6 | 45 | PASS |
| LICI.NS | Life Insurance Corp of India | India | INS_LIFE | — INR | 3.46 | 9.5 | 2.3 | 42.4 | 0.58 | 1.4 | 37 | PASS |
| HDFCLIFE.NS | HDFC Life | India | INS_LIFE | — INR | 6.95 | 64.7 | 0.4 | 11.3 | 0.39 | 3.4 | 13 | PASS |
| SBILIFE.NS | SBI Life | India | INS_LIFE | — INR | 9.38 | 72.7 | 0.2 | 13.7 | 0.35 | 2.6 | 9 | PASS |

*(Indian listed life insurers screen expensive on P/B/P/E — a real market feature: India prices
life insurers on embedded-value growth, not book. LIC itself is cheaper on P/E but its P/B is
high vs the China cohort. The **cheap-quality EM life cluster is Chinese/HK**, not Indian.)*

**EM — Banks**
| Ticker | Name | Country | MktCap | P/B | P/E | DY% | ROE% | ROA% | Cap% | Score | Trap |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|---|
| BBRI.JK | Bank Rakyat Indonesia | Indonesia | 402T IDR | 1.19 | 6.9 | 15.7 | 18.1 | 2.71 | 15.0 | 82 | PASS |
| BMRI.JK | Bank Mandiri | Indonesia | 364T IDR | 1.19 | 6.2 | 12.5 | 21.0 | 2.57 | 12.2 | 79 | PASS |
| BBAJIOO.MX | Banco del Bajío | Mexico | 67B MXN | 1.35 | 7.4 | 12.8 | 17.6 | 2.21 | 12.5 | 76 | PASS |
| BBNI.JK | Bank Negara Indonesia | Indonesia | 118T IDR | 0.73 | 5.8 | 11.3 | 12.0 | 1.58 | 13.2 | 74 | payout>100% |
| BBCA.JK | Bank Central Asia | Indonesia | 688T IDR | 2.66 | 11.9 | 6.4 | 23.0 | 3.66 | 15.9 | 72 | PASS |
| GFINBURO.MX | GF Inbursa | Mexico | 254B MXN | 1.07 | 8.2 | 2.6 | 11.1 | 3.64 | 32.9 | 70 | PASS |
| GFNORTEO.MX | GF Banorte | Mexico | 527B MXN | 2.25 | 8.8 | 9.4 | 23.5 | 2.40 | 10.2 | 69 | PASS |
| 3968.HK | China Merchants Bank | China | 1.1T HKD | 0.85 | 6.7 | 9.9 | 11.9 | 1.17 | 9.8 | 61 | PASS |
| ABG.JO | Absa Group | South Africa | 185B ZAc | 1.07 | 8.4 | 7.8 | 13.7 | 1.19 | 8.7 | 56 | PASS |
| SBK.JO | Standard Bank | South Africa | 524B ZAc | 1.83 | 10.8 | 5.6 | 18.7 | 1.64 | 8.8 | 56 | PASS |
| SCB.BK | SCB X | Thailand | 517B THB | 1.03 | 11.4 | 7.7 | 9.1 | 1.27 | 14.1 | 56 | PASS |

*(Also in-universe: ICBC/CCB/BoC/AgBank HK lines, HDFC/ICICI/SBI India, Itaú/Bradesco/BB Brazil,
KB/Shinhan Korea, Singapore DBS/OCBC/UOB — see full CSV. Big Chinese banks screen at ~0.4–0.6x
P/B with ~9–10% ROE — cheap, but the low ROE + state-policy overhang keeps them mid-pack, not
top; the P/B-0.6/ROE-8% trap rule catches the weakest.)*

**EM — Diversified financials / exchanges**
| Ticker | Name | Country | MktCap | P/B | P/E | DY% | ROE% | ROA% | Score | Trap |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|---|
| B3SA3.SA | B3 (Brazil exchange) | Brazil | 72B BRL | 3.95 | 15.7 | 6.1 | 26.7 | 9.24 | 86 | PASS |
| BAJAJFINSV.NS | Bajaj Finserv | India | 3.0T INR | 3.80 | 30.5 | 0.1 | 14.6 | 4.92 | 53 | PASS |
| 0388.HK | HKEX (exchange) | Hong Kong | 465B HKD | 8.43 | 24.7 | 3.6 | 35.0 | 2.99 | 51 | PASS |
| BAJFINANCE.NS | Bajaj Finance | India | 6.3T INR | 5.53 | 33.2 | 0.5 | 17.9 | 3.77 | 46 | PASS |
| 1359.HK | China Cinda (asset mgmt) | China | 37B HKD | 0.17 | 16.2 | 3.5 | 0.1 | 0.01 | 46 | ROE<5%;cheap_low_ROE_trap |

### 3B. DEVELOPED EX-US

**DEV_EXUS — Banks**
| Ticker | Name | Country | MktCap | P/B | P/E | DY% | ROE% | ROA% | Cap% | Score | Trap |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|---|
| BMPS.MI | Banca Monte dei Paschi | Italy | 33B EUR | 1.18 | 8.0 | 7.9 | 13.3 | 1.56 | 11.7 | 88 | earnings_collapsing |
| DNB.OL | DNB Bank | Norway | 422B NOK | 1.55 | 10.6 | 6.1 | 14.3 | 1.08 | 7.5 | 84 | PASS |
| ISP.MI | Intesa Sanpaolo | Italy | 105B EUR | 1.52 | 11.1 | 6.3 | 14.0 | 1.00 | 7.1 | 82 | PASS |
| UCG.MI | UniCredit | Italy | 122B EUR | 1.79 | 11.2 | 4.0 | 17.0 | 1.34 | 7.9 | 80 | PASS |
| BBVA.MC | BBVA | Spain | 125B EUR | 2.34 | 12.4 | 4.2 | 19.0 | 1.37 | 7.2 | 77 | PASS |
| NWG.L | NatWest Group | UK | 54B GBp | 1.38 | 9.7 | 4.8 | 14.1 | 0.82 | 5.8 | 76 | PASS |
| SWED-A.ST | Swedbank | Sweden | 408B SEK | 1.81 | 12.9 | 5.7 | 16.0 | 1.01 | 6.4 | 75 | PASS |
| BGN.MI | Banca Generali | Italy | 8B EUR | 4.76 | 16.3 | 4.4 | 28.2 | 2.57 | 9.1 | 72 | PASS |
| KBC.BR | KBC Group | Belgium | 48B EUR | 1.88 | 13.9 | 4.3 | 13.4 | 0.92 | 6.9 | 65 | PASS |
| INGA.AS | ING Group | Netherlands | 80B EUR | 1.59 | 12.8 | 3.9 | 16.6 | 0.78 | 4.7 | 60 | PASS |

*(Also in-universe: HSBA.L, BARC.L, LLOY.L, STAN.L (UK); UBSG.SW, BAER.SW (CH); DBK/CBK (DE);
BNP/GLE/ACA (FR); SAN/CABK/SAB/BKT (ES); Nordics SEB/SHB/DANSKE; Japan 8306/8316/8411/8309/8308.T
megabanks; Canada RY/TD/BNS/BMO/CM/NA.TO; Australia CBA/NAB/WBC/ANZ.AX — full CSV.)*

**DEV_EXUS — Insurers**
| Ticker | Name | Country | Sub | MktCap | P/B | P/E | DY% | ROE% | ROA% | Cap% | Score | Trap |
|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|---|
| HNR1.DE | Hannover Re | Germany | REINS | 29B EUR | 2.13 | 10.3 | 5.1 | 21.7 | 4.14 | 19.1 | 74 | PASS |
| BEZ.L | Beazley | UK | DIV | 8B GBp | 2.06 | 11.7 | 1.9 | 19.3 | 6.04 | 31.3 | 71 | PASS |
| SREN.SW | Swiss Re | Switzerland | REINS | 38B CHF | 1.81 | 10.3 | 4.8 | 19.5 | 3.20 | 16.4 | 69 | PASS |
| QBE.AX | QBE Insurance | Australia | PC | 37B AUD | 2.23 | 12.2 | 4.3 | 19.3 | 4.20 | 21.7 | 68 | PASS |
| MAP.MC | Mapfre | Spain | DIV | 13B EUR | 1.51 | 11.9 | 4.2 | 18.3 | — | — | 68 | PASS |
| SCR.PA | SCOR | France | REINS | 6B EUR | 1.23 | 6.7 | 6.0 | 13.2 | 2.28 | 17.3 | 67 | PASS |
| SAMPO.HE | Sampo | Finland | DIV | 24B EUR | 3.00 | 15.2 | 3.9 | 21.3 | 5.18 | 24.4 | 66 | PASS |
| MUV2.DE | Munich Re | Germany | REINS | 63B EUR | 1.81 | 9.4 | 4.9 | 19.8 | 2.27 | 11.4 | 66 | PASS |
| 8725.T | MS&AD Insurance | Japan | PC | 6.4T JPY | 1.34 | 8.1 | 3.3 | 17.8 | 2.59 | 14.5 | 63 | PASS |
| ALV.DE | Allianz | Germany | DIV | — EUR | 2.40 | 13.5 | 4.1 | 18.7 | 1.15 | 6.1 | ~60 | PASS |

*(DEV_EXUS life insurers screen at higher P/B than EM: Aviva/Legal&General/Prudential (UK),
Manulife/Sun Life/Great-West (Canada), Dai-ichi/T&D (Japan), Zurich/Swiss Life (CH) — none are
"cheap on P/B" the way the China cohort is; they're fair-value quality. Reinsurers
(Hannover/Swiss/Munich Re, SCOR) are the developed-ex-US value-with-quality standouts.)*

**DEV_EXUS — Diversified financials / REITs**
| Ticker | Name | Country | Sub | MktCap | P/B | P/E | DY% | ROE% | Score | Trap |
|---|---|---|---|--:|--:|--:|--:|--:|--:|---|
| PGHN.SW | Partners Group | Switzerland | DIVFIN | 18B CHF | 8.02 | 14.0 | 6.8 | 54.8 | 83 | PASS |
| BAM.TO | Brookfield Asset Mgmt | Canada | DIVFIN | 102B CAD | 9.44 | 28.8 | 4.3 | 22.4 | 69 | payout>100% |
| SDR.L | Schroders | UK | DIVFIN | 9B GBp | 2.09 | 17.3 | 3.7 | 12.3 | 65 | PASS |
| ABDN.L | Aberdeen Group | UK | DIVFIN | 4B GBp | 0.91 | 11.9 | 5.9 | 7.8 | 65 | PASS |
| IX / 8591.T | ORIX | Japan | DIVFIN | 42B USD | 1.52 | 15.5 | 2.6 | 10.4 | 64 | PASS |
| BLND.L | British Land | UK | REIT | 4B GBp | 0.70 | 9.2 | 5.6 | 7.8 | 63 | PASS |

### 3C. UNITED STATES

**US — Banks**
| Ticker | Name | MktCap | P/B | P/E | DY% | ROE% | ROA% | Cap% | Score | Trap |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|---|
| RF | Regions Financial | 26B USD | 1.51 | 12.8 | 3.5 | 11.9 | 1.39 | 11.7 | 80 | PASS |
| TFC | Truist Financial | 63B USD | 1.07 | 12.6 | 4.1 | 8.6 | 1.02 | 11.9 | 72 | PASS |
| MTB | M&T Bank | 35B USD | 1.39 | 13.6 | 2.5 | 10.3 | 1.38 | 13.4 | 71 | PASS |
| USB | U.S. Bancorp | 97B USD | 1.65 | 13.0 | 3.4 | 12.4 | 1.14 | 9.2 | 61 | PASS |
| PNC | PNC Financial | 101B USD | 1.75 | 14.6 | 2.8 | 12.1 | 1.26 | 10.4 | 57 | PASS |
| WFC | Wells Fargo | 263B USD | 1.62 | 13.3 | 2.2 | 12.0 | 1.05 | 8.7 | 50 | PASS |
| JPM | JPMorgan Chase | 895B USD | 2.60 | 16.0 | 1.8 | 16.5 | 1.27 | 7.7 | 45 | PASS |
| BAC | Bank of America | 414B USD | 1.51 | 14.5 | 1.9 | 10.6 | 0.93 | 8.7 | 38 | PASS |

**US — Insurers**
| Ticker | Name | Sub | MktCap | P/B | P/E | DY% | ROE% | ROA% | Cap% | Score | Trap |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|---|
| PGR | Progressive | PC | 131B USD | 4.11 | 11.5 | 6.4 | 37.9 | 7.94 | 20.9 | 72 | PASS |
| ACGL | Arch Capital | DIV | 34B USD | 1.48 | 7.6 | — | 21.3 | 4.57 | 21.4 | 70 | PASS |
| CINF | Cincinnati Financial | PC | 29B USD | 1.84 | 10.7 | 2.0 | 18.7 | 5.55 | 29.6 | 69 | PASS |
| ERIE | Erie Indemnity | DIV | 13B USD | 5.54 | 22.8 | 2.4 | 25.9 | 14.84 | 57.4 | 69 | PASS |
| ALL | Allstate | PC | 63B USD | 2.12 | 5.4 | 1.8 | 45.2 | 7.52 | 16.6 | 68 | PASS |
| MRSH | Marsh McLennan | DIV | 83B USD | 5.70 | 21.5 | 2.2 | 27.6 | 7.27 | 26.4 | 62 | PASS |
| HIG | Hartford | DIV | 37B USD | 1.98 | 9.4 | 1.8 | 22.7 | 3.88 | 17.1 | 58 | PASS |
| EG | Everest Group | REINS | 14B USD | 0.94 | 7.3 | 2.2 | 13.8 | 2.66 | 19.2 | 57 | PASS |
| TRV | Travelers | PC | 71B USD | 2.22 | 10.0 | 1.5 | 25.3 | 4.44 | 17.6 | 56 | PASS |
| MET | MetLife | LIFE | — USD | 2.06 | 16.9 | 2.8 | 13.0 | 0.45 | 3.5 | 30 | PASS |

**US — Diversified financials / REITs**
| Ticker | Name | Sub | MktCap | P/B | P/E | DY% | ROE% | Score | Trap |
|---|---|---|--:|--:|--:|--:|--:|--:|---|
| VICI | VICI Properties | REIT | 28B USD | 1.00 | 9.0 | 6.8 | 11.3 | 88 | PASS |
| TROW | T. Rowe Price | DIVFIN | 25B USD | 2.31 | 12.5 | 4.6 | 18.7 | 82 | PASS |
| FDS | FactSet | DIVFIN | 9B USD | 4.23 | 15.8 | 2.0 | 28.1 | 74 | PASS |
| FIS | Fidelity National Info Svc | DIVFIN | 21B USD | 1.32 | 7.9 | 4.3 | 17.2 | 73 | PASS |
| JKHY | Jack Henry | DIVFIN | 10B USD | 4.75 | 19.9 | 1.7 | 24.9 | 70 | PASS |
| BX | Blackstone | DIVFIN | 146B USD | 11.22 | 30.7 | 4.2 | 29.5 | 68 | payout>100% |

*(VICI & TROW independently re-surface at the top here — they were the two Financials/REIT names
that also cleared the generic Stage 1b top-40, a nice cross-validation.)*

---

## 4. Shortlist — best cheap-quality financials (feeds Stage 3/4)

Selection = **low P/B (or P/E) paired with high, stable ROE and a PASS trap status**, ranked
within region. Confidence on the shortlist judgment: **ASSUMED** (single-source snapshot);
underlying fields **VERIFIED** (real 2026-07-02 pull).

### ⭐ EM LIFE INSURANCE LEADERS (the Stage 1a priority — thesis CONFIRMED at the company level)
Stage 1a said the EM Life Insurance *sector* was cheap (P/B ~1.4) and high-quality (ROIC 15% /
ROE 17.6%). The company data bears this out — and the **Chinese/HK life cohort** is where the
cheap-quality is (Indian life insurers screen expensive):

| Ticker | Name | P/B | P/E | ROE% | DY% | Why it's a cheap-quality leader |
|---|---|--:|--:|--:|--:|---|
| **0966.HK** | **China Taiping** | **0.71** | 2.6 | **25.5** | 6.8 | Below book with 25% ROE — the standout cheap+quality pairing; trap-PASS. |
| **1336.HK** | **New China Life (NCI)** | 1.04 | 3.5 | **36.3** | 6.7 | Highest ROE of the cohort, ~1x book, P/E 3.5, 6.7% yield; PASS. |
| **2601.HK** | **CPIC (China Pacific)** | **0.72** | 4.4 | 17.4 | 4.9 | 0.7x book, solid ROE; sector's Stage-1a profile almost exactly. |
| **2628.HK** | **China Life** | 1.15 | 4.8 | **25.5** | 3.6 | Largest, ~1.1x book, 25% ROE; PASS. |
| **2328.HK** | **PICC P&C** | **0.95** | 6.7 | 14.7 | 5.4 | (P&C, not life, but cheap-quality EM insurer) below book, 14.7% ROE. |
| **1339.HK** | **PICC Group** | **0.57** | 4.1 | 14.0 | 5.3 | Cheapest large EM insurer on P/B with double-digit ROE; PASS. |

> **Caveat (VERIFIED from the data, judgment ASSUMED):** several China lifecos show **negative
> `earningsGrowth`** (China Life −32%, Ping An too), consistent with the Stage-1a "cyclical
> low-rate/spread squeeze" verdict — cheap on a *trough*, not broken. The screen's trap gate
> passes them because ROE is still 17–36% and payout is covered, but the negative earnings
> momentum is the key thing to verify at deep-dive (embedded-value trend, new-business value,
> rate sensitivity — none of which yfinance provides).

### Cheap-quality EM banks
- **BBRI.JK / BMRI.JK (Bank Rakyat / Mandiri, Indonesia)** — ~1.2x book, ROE 18–21%, 12–16%
  dividend yield, PASS. Top-scored EM banks; Indonesia's high-ROE state banks.
- **BBAJIOO.MX / GFNORTEO.MX (Banco del Bajío / Banorte, Mexico)** — 1.3–2.2x book, ROE 18–24%,
  attractive yields; Mexican banking quality at a fair price.
- **3968.HK (China Merchants Bank)** — 0.85x book, ROE 11.9%, 9.9% yield; best-quality large
  Chinese bank (the big-4 SOE banks are cheaper at ~0.5x book but lower-ROE/policy-driven).

### Cheap developed-ex-US banks/insurers
- **ISP.MI / UCG.MI (Intesa Sanpaolo / UniCredit, Italy)** — 1.5–1.8x book, ROE 14–17%, P/E ~11,
  6.3% / 4% yield; the re-rated but still reasonably-priced Italian bank recovery, PASS. (BMPS
  scores highest but is flagged `earnings_collapsing` — verify before trusting.)
- **DNB.OL (DNB, Norway)** — 1.55x book, ROE 14.3%, 6.1% yield, PASS; high-quality Nordic bank.
- **NWG.L (NatWest, UK)** — 1.38x book, ROE 14%, P/E 9.7; UK big-bank value.
- **SCR.PA / SREN.SW / MUV2.DE / HNR1.DE (SCOR / Swiss Re / Munich Re / Hannover Re)** — European
  reinsurers at ~1.2–2.1x book, ROE 13–22%, 5–6% yields, all PASS; **the developed-ex-US
  value-with-quality insurers**.
- **8725.T (MS&AD, Japan)** — 1.34x book, ROE 17.8%, P/E 8.1; cheap Japanese P&C.

### US (for completeness — the generic screen already had TROW; banks/insurers were skipped)
- **VICI (REIT)** and **TROW (asset mgr)** top the US list and cross-validate Stage 1b.
- **RF / TFC / MTB (regional banks)** — ~1.1–1.5x book, ROE 9–12%; cheapest quality US banks.
- **ACGL / CINF / ALL / EG (insurers)** — 0.9–2.1x book with 14–45% ROE, all PASS.

---

## 5. Which financial fields yfinance LACKS (paid-API input)

yfinance covers the **generic** financial ratios (P/B, P/E, ROE, ROA, yield, payout, book value,
beta) at 94–98% even for EM — **sufficient for a large-cap financials screen**. But it does
**NOT** provide the *financial-specific* fields that separate a bargain from a trap at deep-dive:

| Missing field | For | Consequence |
|---|---|---|
| **Net interest margin (NIM)**, loan/deposit growth, NPL / loan-loss ratio | Banks | Can't assess earning-asset spread or credit quality. |
| **CET1 / regulatory capital ratios** | Banks | Used a crude **ROA/ROE (equity/assets)** proxy instead — *not* a Basel capital ratio. |
| **Combined ratio**, loss ratio, expense ratio | P&C insurers | Can't tell an underwriting-profitable insurer from one relying on investment income. |
| **Embedded value / value of new business (VNB)** | Life insurers | The *correct* valuation base for life insurers (price/EV). **Not available** — we used P/B + P/E as the yfinance-available proxy, per brief. This is the single biggest gap for the EM-life thesis. |
| **Tangible book / P-tangible-book** | Banks (goodwill-heavy) | P/B can flatter acquisitive banks. |
| **FFO / AFFO** | REITs | The correct REIT earnings base; P/E on GAAP net income understates REIT cash earnings. |

**Recommendation (ASSUMED, evidence-based):** for **screening** large-cap financials, **stay
free** — yfinance's 94% P/B+ROE coverage is enough to rank and shortlist. **Buy a paid API
(FMP is the price/coverage pick) specifically IF Stage 3/4 deep-dives on the EM-life shortlist
need embedded value / VNB / combined ratio / CET1** — these are exactly the trap-vs-bargain
fields for financials, and the China-life "cheap on a trough" caveat above is precisely the case
they'd resolve. This is a *narrower, more concrete* trigger than the generic Stage 1b
recommendation, and it's the highest-value place to spend money in this whole funnel.

---

## 6. Method & limitations

- **Sector-appropriate by design:** ranks on P/B + P/E + yield (value) and ROE + ROA + a capital
  proxy (quality) — the metrics that *apply* to balance-sheet businesses — instead of the
  gross-margin/EV-EBITDA metrics that structurally excluded these names from Stage 1b.
- **Peer-relative ranking:** scores are percentiles **within region × sub-group**, so a score of
  82 means "top-of-its-peers," not an absolute-cheapness reading. **Do not compare a US bank's
  score directly to an EM insurer's** — compare within the peer cell.
- **Capital-strength proxy is crude:** ROA/ROE = equity/assets ≈ 1/leverage. It is **not** CET1
  or a regulatory ratio; it only says "less levered = notionally stronger." Treat as a rough
  screen input, not a capital verdict.
- **Single-source & snapshot:** one yfinance `.info` pull (2026-07-02), **not** cross-checked vs
  filings. Multiples move daily. Every shortlisted name must be re-verified at deep-dive.
- **Currency:** market caps are native (HKD, IDR, BRL, INR, JPY, EUR, GBp…). **Do not compare
  cross-currency without FX.** yfinance ROE/ROA/P/B are currency-neutral ratios (safe to
  compare); market caps are not.
- **Known artifacts (flagged, not hidden):** ADR/native duplicates deduped (13 dropped, native
  kept); **BRK-B** P/B ≈ 0.001 (B-share price vs A-share book) excluded via the P/B-glitch guard;
  a few EM local lines returned partial `.info` (the 87% EM P/B+ROE coverage vs 95–97% developed).
- **Trap filter is snapshot-based:** it flags de-minimis/negative/collapsing ROE, uncovered
  payout, and the cheap-low-ROE combo — but cannot see multi-year earnings-stability, reserve
  adequacy, or asset-quality trends (those need filings / a paid API, §5).
- **What could NOT be obtained:** NIM, CET1, combined ratio, embedded value, tangible book, FFO
  (§5) — reported as unavailable, never fabricated.
- **Confidence:** individual pulled fields **VERIFIED** (real fetch, 2026-07-02);
  ranking/shortlist **ASSUMED** (single-source, proxy capital metric, snapshot).

**Reproduce:**
```
/opt/venv/bin/python3 screens/financials_universe.py         # build the 304-name universe
/opt/venv/bin/python3 screens/run_financials_screen.py       # fetch (cached) + score + write CSVs
```
Outputs: `screens/financials_screen_{raw,all,ranked}.csv`, `data/cache/financials_universe.csv`,
per-ticker `data/cache/yf_*.json`.
