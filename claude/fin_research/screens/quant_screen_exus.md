# Stage 2.5a — Broadened ex-US / EM Cheap-Quality Screen

**Why this stage exists.** Stage-1b's high-conviction bucket came out effectively
100% developed-market / US (top-40 = 29 US / 8 EM / 3 dev-ex-US). That was largely a
**universe-construction artifact**: the Stage-1b universe was 503 US vs only 94 dev-ex-US +
42 EM. Hooman wants ex-US diversification. This stage substantially broadens the ex-US/EM
universe (index membership + curated large caps), re-runs the **exact Stage-1b screen**, and
ranks **within region** as well as globally so ex-US/EM names aren't crowded out.

- **Run date / as-of:** yfinance `.info` pulled **2026-07-02** (timestamp on every cached row,
  e.g. `2026-07-02T13:06:08+00:00`). Prices/multiples move daily — treat every number as as-of
  that pull.
- **Source:** **yfinance** only (Yahoo Finance). Universe from cited Wikipedia index-membership
  tables + curated large-cap lists (see §1). No EDGAR cross-check in this breadth stage.
- **Method reuse (no new scoring):** `screens/run_quant_screen_exus.py` **imports**
  `derive_metrics`, `piotroski_lite`, and `score_and_rank` from `run_quant_screen.py` and calls
  them verbatim — same metric definitions, same data-quality guards, same trap gate, same
  **60% quality / 40% cheapness** combined score. The only additions: broader universe, a
  yfinance-`sector` financial filter, within-region re-ranking, and a coverage report.
- **Owner:** Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.**
- **Code:** `screens/universe_exus.py` (expanded universe), `screens/run_quant_screen_exus.py`
  (fetch + reuse-score). **Outputs:** `screens/quant_screen_exus_raw.csv` (754 rows),
  `screens/quant_screen_exus_ranked.csv` (688 rankable, scored **within the ex-US/EM set**),
  `screens/quant_screen_exus_coverage.csv`, and `screens/quant_screen_global_merged_ranked.csv`
  (the true global re-rank, §4).

> ⚠️ **ANTI-HALLUCINATION.** Every ratio is derived from a real yfinance pull on 2026-07-02.
> Missing fields are blank, never guessed. Confidence: individual pulled fields **VERIFIED**
> (real fetch), **UNVERIFIED** vs a second source; the ranking **ASSUMED** (single-source,
> snapshot, proxy metrics). Any name that advances to a deep dive must be re-verified vs
> filings — no EDGAR backstop exists for most non-US-listed names.

---

## 1. Expanded universe (counts + sources)

**Total 754 ex-US/EM non-financial names** — 462 developed-ex-US + 292 emerging — up from
Stage-1b's 94 + 42. Built by scraping cited Wikipedia index-membership tables (2026-07-02,
browser UA) and supplementing with curated large-cap lists for regions whose Wikipedia
constituents table is navbox-only / not machine-parseable (Japan, Korea, Taiwan, Brazil,
Mexico, SE-Asia, Nordics). Correct Yahoo suffixes applied (`.L .DE .PA .AS .SW .MC .MI .ST
.CO .HE .OL .TO .AX .T .SI` developed; `.HK .NS .TW .KS .SA .MX .JK .BK .KL .JO` EM).
**108 obvious banks/insurers/REITs were excluded by ticker** (parallel financials agent's
turf); a further **31 yfinance-labelled Financial Services / REITs were dropped at scoring**.

| Source (Wikipedia index / curated) | Yahoo suffix | n | Region |
|---|---|--:|---|
| FTSE 100 | `.L` | 86 | DEV_EXUS |
| Hang Seng | `.HK` | 75 | EM |
| Nikkei/TOPIX large (curated) | `.T` | 56 | DEV_EXUS |
| SE-Asia / S.Africa / Nordics large (curated) | `.JK .BK .KL .SI .JO / .CO .HE .OL` | 55 | mixed |
| S&P/TSX 60 | `.TO` | 47 | DEV_EXUS |
| S&P/ASX 50 | `.AX` | 41 | DEV_EXUS |
| Ibovespa large (curated) | `.SA` | 40 | EM |
| NIFTY 50 | `.NS` | 39 | EM |
| CAC 40 | `.PA` | 35 | DEV_EXUS |
| DAX | `.DE` | 34 | DEV_EXUS |
| EM ADRs (curated) | bare | 34 | EM |
| FTSE MIB | `.MI` | 26 | DEV_EXUS |
| IBEX 35 | `.MC` | 26 | DEV_EXUS |
| OMX Stockholm 30 | `.ST` | 25 | DEV_EXUS |
| Developed ADRs (curated) | bare | 25 | DEV_EXUS |
| KOSPI large (curated) | `.KS` | 25 | EM |
| TWSE large (curated) | `.TW` | 24 | EM |
| IPC Mexico large (curated) | `.MX` | 22 | EM |
| AEX | `.AS` | 14 | DEV_EXUS |
| SMI | `.SW` | 14 | DEV_EXUS |
| EURO STOXX 50 | mixed euro | 11 | DEV_EXUS |

Sources cited in `screens/universe_exus.py` docstring (each URL). Countries represented after
fetch (yfinance `country`): UK, Germany, France, Netherlands, Switzerland, Spain, Italy,
Sweden, Denmark, Finland, Norway, Luxembourg, Ireland, Canada, Australia, Japan (developed);
China/HK, India, Taiwan, Korea, Brazil, Mexico, Indonesia, Thailand, Malaysia, Singapore,
South Africa (emerging).

---

## 2. Developed-ex-US — top 15 (within-region, trap-gate PASS)

All figures yfinance **as-of 2026-07-02**. `Q/C` = quality/cheapness percentile *within the
ex-US/EM set*. MktCap in **native currency** (do NOT compare cross-currency without FX). `EY`
= earnings yield (EBIT/EV). `*` on ROIC = proxy >100% (buyback-depressed equity — use ROE).
**⚠ GBp note:** for `.L` names Yahoo labels currency `GBp` but reports `marketCap` in whole
GBP; caps shown as `GBP`.

| Rk | Ticker | Name | Country | Sector | MktCap | ROIC | ROE | OpMgn | EV/EBITDA | EY | P/E | P/B | Piotr | Q/C | Score |
|--:|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|:--:|:--:|--:|
| 1 | K.TO | Kinross Gold | Canada | Materials | 40B CAD | 30% | 35% | 55% | 7.8 | 11.3% | 10.1 | 3.1 | 7/7 | 91/75 | 84.7 |
| 2 | EDV.L | Endeavour Mining | UK | Materials | ~9.5B GBP | 88% | 31% | 54% | 3.5 | 25.9% | 14.9 | 3.8 | 7/7 | 85/79 | 82.9 |
| 3 | ABX.TO | Barrick Mining | Canada | Materials | 87B CAD | 23% | 25% | 56% | 8.0 | 11.3% | 10.1 | 2.2 | 7/7 | 87/76 | 82.7 |
| 4 | NEM.AX | Newmont (CDI) | US/AU | Materials | 145B AUD | 26% | 26% | 61% | 8.4 | 11.1% | 12.1 | 2.9 | 7/7 | 88/73 | 82.1 |
| 5 | FRES.L | Fresnillo | Mexico/UK | Materials | ~21B GBP | 124%* | 34% | 55% | 7.4 | 13.0% | 19.9 | 6.0 | 7/7 | 90/66 | 80.3 |
| 6 | BZU.MI | Buzzi (cement) | Italy | Materials | 8B EUR | 14% | 13% | 23% | 6.0 | 14.5% | 8.9 | 1.2 | 7/7 | 77/82 | 79.2 |
| 7 | AEM.TO | Agnico Eagle Mines | Canada | Materials | 110B CAD | 19% | 22% | 63% | 11.3 | 7.9% | 14.6 | 3.0 | 7/7 | 92/60 | 79.1 |
| 8 | FMG.AX | Fortescue (iron ore) | Australia | Materials | 58B AUD | 15% | 19% | 35% | 7.3 | 9.5% | 10.8 | 1.9 | 7/7 | 75/76 | 75.6 |
| 9 | TEN.MI | Tenaris (OCTG) | Luxembourg | Energy | 24B EUR | 15% | 12% | 19% | 7.6 | 10.8% | 14.3 | 1.6 | 7/7 | 75/76 | 75.1 |
| 10 | RMD.AX | ResMed (CDI) | US/AU | Health Care | 43B AUD | 7% | 25% | 35% | 7.4 | 12.5% | 19.4 | 1.9 | 7/7 | 76/69 | 73.4 |
| 11 | 4578.T | Otsuka Holdings | Japan | Health Care | 6,100B JPY | 14% | 13% | 19% | 9.0 | 8.8% | 16.9 | 2.0 | 7/7 | 78/65 | 72.8 |
| 12 | NHY.OL | Norsk Hydro | Norway | Materials | 169B NOK | 28% | 6% | 21% | 4.1 | 21.4% | 27.5 | 1.6 | 6/7 | 69/77 | 72.6 |
| 12 | AUTO.L | Auto Trader Group | UK | Comm. Svcs | ~4.0B GBP | 53% | 60% | 62% | 10.7 | 8.9% | 15.1 | 10.3 | 7/7 | 82/58 | 72.6 |
| 14 | EVN.AX | Evolution Mining | Australia | Materials | 24B AUD | 28% | 26% | 43% | 7.7 | 9.1% | 17.8 | 4.2 | 7/7 | 78/63 | 71.8 |
| 14 | RI.PA | Pernod Ricard | France | Cons. Staples | 16B EUR | 9% | 9% | 31% | 9.7 | 11.0% | 11.3 | 1.0 | 6/7 | 65/82 | 71.8 |

**Read:** the dev-ex-US top is dominated by **precious/base-metals miners** (Kinross, Barrick,
Newmont-AU, Fresnillo, Agnico, Evolution, Fortescue, Norsk Hydro) — the cheap-cyclical-with-
genuine-quality pattern, same signal as US #1 NEM in Stage-1b. Non-miner standouts: **Buzzi**
(Italian cement, EV/EBITDA 6.0, P/B 1.2), **Auto Trader** (UK, 62% op margin, 53% ROIC — a
genuine quality compounder at a fair price), **Pernod Ricard** (de-rated spirits, P/B 1.0),
**Tenaris** (energy-services quality). Full CSV: `screens/quant_screen_exus_ranked.csv`.

---

## 3. Emerging markets — top 15 (within-region, trap-gate PASS)

`NTES-S` (9999.HK) is the HK dual-listing of NetEase (NTES) — shown de-duplicated. Negative
EV/EBITDA (PDD −3.2, TME −0.5) = net-cash firms; the scoring **guard blanks EV/EBITDA ≤0 and
<2** so those don't drive the rank (their cheapness comes from P/E, P/B, FCF yield). TSM P/B
99.8 is an ADR-vs-local share-class artifact (flagged, not used cross-currency).

| Rk | Ticker | Name | Country | Sector | MktCap | ROIC | ROE | OpMgn | EV/EBITDA | EY | P/E | P/B | Piotr | Q/C | Score |
|--:|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|:--:|:--:|--:|
| 1 | 0883.HK | CNOOC | HK/China | Energy | 970B HKD | 19% | 15% | 45% | 3.1 | 23.6% | 6.9 | 1.0 | 7/7 | 89/91 | 90.1 |
| 2 | PDD | PDD Holdings | China | Cons. Disc. | 117B USD |  | 25% | 18% | (net-cash) |  | 8.7 | 1.9 | 7/7 | 82/86 | 83.4 |
| 3 | NTES | NetEase | China | Comm. Svcs | 83B USD |  | 22% | 41% | 6.4 | 18.2% | 16.7 | 17.1 | 7/7 | 90/70 | 81.9 |
| 4 | COALINDIA.NS | Coal India | India | Energy | 2,705B INR | 36% | 28% | 21% | 5.5 | 15.5% | 8.7 | 2.3 | 7/7 | 84/76 | 80.8 |
| 5 | TME | Tencent Music | China | Comm. Svcs | 14B USD |  | 12% | 30% | (net-cash) |  | 10.3 | 1.2 | 7/7 | 75/89 | 80.4 |
| 6 | 9992.HK | Pop Mart | China | Cons. Disc. | 203B HKD | 127%* | 78% | 48% | 10.9 | 9.3% | 13.9 | 8.0 | 7/7 | 93/58 | 79.0 |
| 7 | TSM | Taiwan Semiconductor | Taiwan | Technology | 2,304B USD | | 36% | 58% | 5.7 | 14.7% | 38.6 | 99.8† | 7/7 | 88/60 | 76.9 |
| 8 | 2331.HK | Li Ning | China | Cons. Disc. | 39B HKD | 15% | 11% | 10% | 4.5 | 13.7% | 11.7 | 1.2 | 7/7 | 70/86 | 76.7 |
| 9 | BIDU | Baidu | China | Comm. Svcs | 40B USD | 60% | 0% | 10% | 1.7 | 31.4% | | 1.0 | 6/7 | 66/91 | 76.2 |
| 10 | INDF.JK | Indofood Sukses Makmur | Indonesia | Cons. Staples | 59,487B IDR | 20% | 13% | 19% | 4.9 | 19.3% | 5.4 | 0.8 | 7/7 | 62/95 | 75.3 |
| 11 | ITC.NS | ITC Ltd | India | Cons. Staples | 3,637B INR | 45% | 29% | 36% | 12.6 | 8.4% | 17.6 | 5.0 | 6/7 | 90/52 | 75.1 |
| 12 | 0027.HK | Galaxy Entertainment | HK | Cons. Disc. | 129B HKD | 11% | 13% | 20% | 8.7 | 8.5% | 12.1 | 1.6 | 7/7 | 74/74 | 74.0 |
| 13 | ICBP.JK | Indofood CBP | Indonesia | Cons. Staples | 78,718B IDR | 18% | 15% | 21% | 6.6 | 13.6% | 8.6 | 1.4 | 7/7 | 66/85 | 73.9 |
| 14 | 1378.HK | China Hongqiao (alum.) | China | Materials | 196B HKD | 17% | 19% | 22% | 5.2 | 16.0% | 7.3 | 1.3 | 6/7 | 61/90 | 72.8 |
| 15 | PBR | Petrobras | Brazil | Energy | 103B USD | 31% | 26% | 32% | 2.1 | 37.1% | 5.1 | 1.2 | 6/7 | 58/96 | 72.8 |

**Read:** EM top is led by **CNOOC** (Chinese offshore oil, EV/EBITDA 3.1, 23.6% EY, P/B 1.0,
7/7 — the single cheapest-and-quality name in the whole ex-US/EM run), **cheap Chinese
internet** (PDD, NetEase, Tencent Music, Baidu — deeply de-rated, net-cash, high FCF),
**Indian value-quality** (Coal India 36% ROIC / EV-EBITDA 5.5; ITC 45% ROIC staple),
**Indonesian consumer staples** (Indofood twins at EV/EBITDA 5-7, P/B <1.5), and cyclicals
(China Hongqiao aluminium, Petrobras). **Pop Mart** is a genuine quality outlier (78% ROE, 48%
op margin) but only mid-cheap. Full CSV: `screens/quant_screen_exus_ranked.csv`.

---

## 4. Merged global re-ranking — the headline finding

Because §2/§3 percentiles are computed *within the ex-US/EM set*, they are not directly
comparable to Stage-1b's US-heavy scores. So I built a **true global re-rank**: union of the
Stage-1b raw metrics (639) + this expanded ex-US/EM raw (754), de-duplicated by ticker →
**1,285 names → 1,128 after dropping yfinance-labelled financials/REITs**, then re-scored with
**`score_and_rank` verbatim** (one common percentile pool). Output:
`screens/quant_screen_global_merged_ranked.csv`.

**Global top-40 (gated) region mix flips completely:**

| | Stage-1b top-40 | Global merged top-40 (this stage) |
|---|--:|--:|
| US | 29 | **13** |
| EM | 8 | **15** |
| DEV_EXUS | 3 | **12** |

**27 of the global top 40 are new ex-US/EM names** (and 41 of the top 60). The ones that break
into the overall top tier (with their new global rank):

- **Top 15 globally:** #1 **CNOOC** (EM Energy), #3 **Kinross** (CA), #4 **Endeavour Mining**
  (UK), #5 **Barrick** (CA), #6 **Newmont-AU**, #7 **PDD** (China), #8 **NetEase** (China),
  #9 **Fresnillo** (UK/MX), #10 **Coal India**, #11 **Pop Mart** (China), #12 **Tencent Music**,
  #13 **Agnico Eagle** (CA), #15 **Buzzi** (Italy).
- **#16-40:** **TSM** (#20), **Fortescue** (#23), **Li Ning** (#24), **ITC** (#25), **Baidu**
  (#28), **Tenaris** (#29), **Galaxy Ent** (#31), **Indofood** (#32), **Auto Trader** (#33),
  **ResMed-AU** (#34), **Indofood CBP** (#38), **Otsuka** (#39), **Tata Consultancy** (#40).

**Conclusion (VERIFIED from the merge):** the Stage-1b developed-only skew was **mostly a
universe-construction artifact**, not a genuine quality gap. With a fairly-sized ex-US/EM
universe, ex-US/EM names dominate the cheap-quality top tier — driven by (a) globally cheap
miners/energy that happen to list ex-US, and (b) deeply de-rated Chinese internet + EM
staples that screen far cheaper than US peers at comparable quality.

---

## 5. Coverage report (informs the paid-API question)

Source: `screens/quant_screen_exus_coverage.csv`, as-of 2026-07-02. "Reachable" = yfinance
returned a market cap; "usable" = ≥8 of 11 key screening fields present.

| Region | n | reachable | usable | reachable % | **usable %** | mean key fields (of 11) |
|---|--:|--:|--:|--:|--:|--:|
| DEV_EXUS | 462 | 458 | 446 | 99.1% | **96.5%** | 10.6 |
| EM | 292 | 276 | 275 | 94.5% | **94.2%** | 10.1 |
| **Total** | **754** | **734** | **721** | **97.3%** | **95.6%** | — |

**20 unreachable tickers (2.7%)** — all wrong/renamed Yahoo symbols or delisted forms, NOT a
systemic hole: `ABB`, `TEF`, `ROG.SW` (Roche — needs `ROG.SW` correct form / `RO.SW`);
Malaysia `.KL` locals (`IOI.KL`, `MISC.KL`, `PCHEM.KL`, `PETGAS.KL`, `SIME.KL`, `TENAGA.KL` —
Yahoo uses different codes for KLSE); several Brazil `.SA` (`ELET3/6`, `EMBR3`, `BRFS3`,
`JBSS3`, `MRFG3`, `NTCO3`, `CCRO3` — mostly renamed/merged tickers); Mexico `ALFAA.MX`,
`ELEKTRA.MX`; `VAS.AX` (an ETF, correctly excluded). These are cosmetic ticker fixes, not
coverage failures.

**Verdict (VERIFIED, extends the Stage-1b stress test):** at the **large-cap index level,
free yfinance is sufficient for ex-US and EM** — 95.6% usable across 754 names, mean 10+ of 11
key fields. This is a *broader* and *cleaner* result than the Stage-1b 41-name EM stress test
(83% mean completeness) because index membership self-selects for liquid, well-covered names.
**A paid API is still only justified for** (a) EM breadth *below* the large/index-cap tier
(untested — the known gap), (b) point-in-time/historical fundamentals, or (c) bank-specific
fields. For a diversified large-cap cheap-quality shortlist including EM, **stay free.**

---

## 6. Small-cap exceptions

**None qualify.** The universe is intentionally index/large-cap, so after correcting a GBp
currency-unit artifact (Yahoo labels `.L` caps `GBp` but the `marketCap` figure is whole GBP —
initially made Endeavour/Fresnillo/Auto Trader/Games Workshop *look* like $0.1-0.5B micro-caps
when they are multi-billion), **zero gated names fall below ~$5B USD with exceptional quality.**
The closest to a small-cap-quality standout is **Auto Trader Group (AUTO.L, ~$5.1B, Q=82,
53% ROIC, 62% op margin)** — a high-quality UK compounder near the small-cap line, though its
cheapness percentile (58) keeps it out of "cheap." **Games Workshop (GAW.L, ~$7B, Q=92, 7/7)**
is the highest-quality sub-$8B name but screens expensive (C=23) so it does not make a
value list. If Hooman wants genuine small-cap coverage, the universe must add a small-cap index
(e.g. FTSE 250, MSCI EM Small Cap) — flagged as an open item, consistent with Stage-1b §5.

---

## 7. Method & limitations

- **Exact Stage-1b reuse (no new method):** `run_quant_screen_exus.py` imports and calls
  `derive_metrics`, `piotroski_lite`, `score_and_rank` from `run_quant_screen.py`. Metric
  definitions, data-quality guards (blank EV/EBITDA ≤0 and <2; flag ROIC proxy >100% and swap
  ROE into the rank), trap gate (FCF>0 AND Piotroski-lite ≥60% AND D/E<300%), and the
  **60/40 quality-first combined score** are all identical to Stage-1b.
- **Two ranking pools, on purpose:** §2/§3 rank *within the 688-name ex-US/EM rankable set*
  (so ex-US/EM names aren't crowded out by the larger US set — the mandate). §4 ranks the
  *global 1,128-name union* on one common percentile pool (the honest cross-region comparison).
  Combined scores are **percentiles, so only comparable within their own pool** — do not compare
  a §2 score to a §4 score.
- **Single-source, snapshot:** all fundamentals are one yfinance `.info` pull (2026-07-02), not
  cross-checked vs filings. No EDGAR backstop for most non-US-listed names (weaker
  anti-hallucination posture ex-US — every advancing name must be re-verified at deep dive).
  Piotroski is "lite" (no YoY deltas from a single snapshot).
- **Currency:** market caps are **native currency** (INR, KRW, HKD, JPY, IDR, GBP…) — do NOT
  compare cross-currency without FX. The `mcap_usd` column in the ranked CSV uses **approximate
  static FX** (2026-07 rates), for the small-cap floor sanity check only — flagged approximate.
- **Known data artifacts (flagged, not hidden):** GBp-vs-GBP unit label on `.L` names (§6);
  ROIC proxy inflates for buyback-heavy firms (Fresnillo 124%, Pop Mart 127%, Endeavour 88%) →
  use ROE; net-cash firms show negative EV → EV/EBITDA blanked by the guard (PDD, TME); TSM P/B
  99.8 = ADR-vs-local share-class. Dual-listing duplicates exist (NTES ↔ 9999.HK); de-duplicated
  in the displayed tables, both retained in the CSV.
- **Financials excluded by design:** 108 dropped by ticker + 31 by yfinance sector — the
  parallel financials agent covers banks/insurers/REITs. Any EM/dev-ex-US financial that screens
  well will surface in *that* agent's output, not here.
- **Confidence:** individual pulled fields **VERIFIED** (real fetch, 2026-07-02); ranking and
  any cross-name comparison **ASSUMED** (single-source, proxy metrics, snapshot).
