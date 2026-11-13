# Stage 1b — Bottom-Up Quality-at-a-Price Screen (Global)

**Greenblatt "Magic Formula" style dual-rank, QUALITY-FIRST.** Screens a broad global
universe for companies that are BOTH high-quality AND cheap, ranks them by a combined score
(quality weighted heavier than cheapness), and applies a value-trap gate.

- **Run date / as-of:** data pulled **2026-07-02** (yfinance `.info` snapshot; timestamp on
  every cached row, e.g. `2026-07-02T01:16:15+00:00`). Prices/multiples move daily — treat
  every number as as-of that pull.
- **Source:** **yfinance** (Yahoo Finance) for all company fundamentals. US GICS sectors from
  the **Wikipedia S&P 500 list** (scraped 2026-07-02, cited). No EDGAR cross-check in this
  breadth-first stage (that is Stage 2's job on the survivors).
- **Owner:** Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.**
- **Code:** `screens/universe.py` (universe), `screens/run_quant_screen.py` (fetch + derive +
  score), `screens/em_stress_test.py` (EM coverage test). Data cached under `data/cache/`.
- **Outputs:** `screens/quant_screen_raw.csv` (639 rows, all derived metrics),
  `screens/quant_screen_ranked.csv` (554 rankable, scored), `screens/em_stress_test.csv`.

> ⚠️ **ANTI-HALLUCINATION:** every ratio below is derived from a real yfinance pull on
> 2026-07-02. Missing fields are left blank, never guessed. Where a derived figure is a proxy
> or looks like a data artifact, it is **flagged** (see "Known data artifacts"). yfinance is a
> *secondary* source — any name that advances to a deep dive must be cross-checked vs EDGAR
> (US) or filings (ex-US) before it drives a decision. Confidence on the ranking: **ASSUMED**
> (single-source, snapshot, proxy metrics); confidence on individual pulled fields: **VERIFIED**
> (real fetch) but **UNVERIFIED** against a second source.

---

## 1. Methodology — exact metric definitions & thresholds

### Universe (639 names, `screens/universe.py`)
| Bucket | n | How built |
|---|---|---|
| **US** | 503 | S&P 500 constituents, Wikipedia (GICS sector attached). `BRK.B`→`BRK-B` for Yahoo. |
| **DEV_EXUS** | 94 | Curated large developed ex-US: Europe (`.SW/.DE/.PA/.AS/.L/.CO/.ST/.MC/.MI/.HE`), Japan (`.T`), HK (`.HK`), Australia (`.AX`), Korea (`.KS`), Canada (`.TO`), plus developed-market US ADRs. |
| **EM_CORE** | 42 | Curated large EM via ADRs (`BABA, TSM, INFY, VALE, ITUB, MELI`…) + major suffixes (`.NS, .TW, .HK`). |

Deliberately **mid/large cap** (index + large ADRs). Small caps enter only as exceptions on
exceptional quality — none qualified (see §5). A separate **EM_STRESS** batch of 41 mixed EM
names is used *only* to measure coverage (§6), not ranked.

### Metrics derived (from real yfinance fields only)
**Quality**
- **ROIC proxy** = NOPAT / invested capital, NOPAT = EBIT·(1−0.21), invested capital =
  `totalDebt` + book equity − `totalCash`, book equity = `marketCap`/`priceToBook`. Falls back
  to **ROE** (`returnOnEquity`) when inputs are missing. *(Proxy — flagged when >100%, see below.)*
- **Gross margin** (`grossMargins`), **operating margin** (`operatingMargins`), **net margin**.
- **Balance sheet:** `debtToEquity` (%), `currentRatio`, `quickRatio`.
- FCF positive (`freeCashflow` > 0).

**Cheapness**
- **Earnings yield (EBIT/EV)** — the Greenblatt cheapness metric. EBIT proxy = implied EBITDA
  (`enterpriseValue`/`enterpriseToEbitda`) scaled by `operatingMargins`/`ebitdaMargins`.
- **FCF yield** = `freeCashflow`/`marketCap`.
- **EV/EBITDA** (`enterpriseToEbitda`), **P/E** (`trailingPE`), **P/B** (`priceToBook`).

**Trap filter — Piotroski-lite (0–7, honestly partial)**
Scored from a single `.info` snapshot: ROA>0, FCF>0, OCF>0, currentRatio≥1, D/E<100%,
operating margin>0, revenue growth>0. Called "lite" because year-over-year Piotroski signals
(ΔROA, Δmargin, Δshares, accruals) need multi-period data not in this snapshot — those are a
Stage-2 EDGAR add-on.

### Scoring — QUALITY-FIRST (60/40)
Each rankable name gets a **percentile rank** (0–100) within the rankable set on:
- **Quality composite** = mean of pctl(ROIC/ROE), pctl(gross margin), pctl(operating margin),
  pctl(low D/E), pctl(current ratio).
- **Cheapness composite** = mean of pctl(earnings yield), pctl(FCF yield), pctl(low EV/EBITDA),
  pctl(low P/E), pctl(low P/B).
- **Combined = 0.60·Quality + 0.40·Cheapness.** Quality weighted heavier per the project's
  quality-first mandate (CLAUDE.md §3).

### Gates
- **Rankable** (554/639): has a quality-return + a margin, has ≥1 cheapness metric, no yfinance
  error. The 85 dropped are mostly **financials/REITs** (no gross margin / EV/EBITDA by nature)
  and a few names missing an input — not a data failure.
- **Trap gate PASS** (434/554): FCF>0 **and** Piotroski-lite ≥ 60% of its max **and** D/E < 300%.

### Data-quality guards (so the ranking isn't driven by artifacts)
- **EV/EBITDA ≤ 0** (net-cash / loss firms — EV can be negative) → blanked from the cheapness
  multiple and from the EV-derived earnings yield.
- **EV/EBITDA < 2** for a going concern → treated as a data glitch (e.g. ADR-vs-local EV
  mismatch), blanked likewise. (Removed e.g. Ambev's spurious 70% earnings yield.)
- **ROIC proxy > 100%** → flagged `*` (buyback-depressed book equity inflates it), and swapped
  for ROE in the *ranking* input so one artifact can't dominate.

---

## 2. Top 40 "cheap-quality" names (rankable + trap-gate PASS, ranked by combined score)

All figures yfinance, **as-of 2026-07-02**. `Q`=quality pctl, `C`=cheapness pctl,
`Score`=combined. `EY`=earnings yield (EBIT/EV). `*` on ROIC = proxy >100%, low-confidence
(use ROE). Blank = field not returned / cleaned as artifact. MktCap in the company's **native
currency** (do NOT compare across currencies without FX).

| # | Ticker | Name | Region | Sector | MktCap | Q | C | Score | ROIC | ROE | GM | OM | D/E% | EY | FCFy | EV/EBITDA | PE | P/B | Piotr | Trap |
|--:|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--:|:--:|
| 1 | NEM | Newmont Corporation | US | Materials | 100B USD | 89 | 86 | 87.9 | 38.4% | 25.8% | 67.4% | 61.4% | 16 | 15.9% | 9.8% | 5.9 | 12.1 | 2.9 | 7/7 | PASS |
| 2 | TROW | T. Rowe Price Group | US | Financials | 25B USD | 86 | 85 | 85.7 | 29.1% | 18.7% | 52.0% | 37.2% | 4 | 12.1% | 7.6% | 7.8 | 12.5 | 2.3 | 7/7 | PASS |
| 3 | PDD | PDD Holdings | EM_CORE | Cons. Disc. | 117B USD | 77 | 92 | 82.8 |  | 25.4% | 56.0% | 18.4% | 1 |  | 61.0%⚠ |  | 8.7 | 1.9 | 7/7 | PASS |
| 4 | NTES | NetEase | EM_CORE | Comm. Svcs | 83B USD | 88 | 75 | 82.7 |  | 22.1% | 65.7% | 41.4% | 6 | 18.2% | 41.1% | 6.4 | 16.7 | 17.1 | 7/7 | PASS |
| 5 | INTU | Intuit | US | Technology | 73B USD | 84 | 75 | 80.4 | 37.5% | 22.5% | 80.8% | 47.0% | 33 | 13.4% | 7.2% | 11.4 | 16.3 | 3.6 | 7/7 | PASS |
| 6 | EOG | EOG Resources | US | Energy | 68B USD | 78 | 81 | 79.5 | 20.0% | 18.2% | 62.0% | 37.9% | 27 | 12.2% | 4.2% | 5.8 | 12.6 | 2.2 | 7/7 | PASS |
| 7 | VICI | VICI Properties | US | Real Estate | 28B USD | 77 | 82 | 79.2 | 7.5% | 11.3% | 99.1% | 107.5% | 62 | 9.5% | 4.5% | 11.5 | 9.0 | 1.0 | 7/7 | PASS |
| 8 | APA | APA Corporation | US | Energy | 11B USD | 68 | 94 | 78.4 | 23.8% | 26.2% | 72.3% | 38.5% | 61 | 19.6% | 15.0% | 3.2 | 7.4 | 1.7 | 5/7 | PASS |
| 9 | CF | CF Industries | US | Materials | 17B USD | 74 | 83 | 77.9 | 28.4% | 27.3% | 39.1% | 33.6% | 44 | 11.8% | 6.5% | 6.1 | 9.7 | 3.1 | 7/7 | PASS |
| 10 | CPRT | Copart | US | Industrials | 28B USD | 85 | 66 | 77.8 | 27.4% | 17.6% | 47.5% | 37.5% | 1 | 7.7% | 3.6% | 11.5 | 17.9 | 3.0 | 7/7 | PASS |
| 11 | ITC.NS | ITC Ltd | EM_CORE | Cons. Staples | 3,637B INR | 88 | 62 | 77.7 | 45.0% | 29.3% | 57.8% | 36.4% | 3 | 8.4% | 3.6% | 12.6 | 17.6 | 5.0 | 6/7 | PASS |
| 12 | EQT | EQT Corporation | US | Energy | 33B USD | 68 | 92 | 77.6 | 13.8% | 13.4% | 81.0% | 57.4% | 21 | 12.7% | 7.6% | 5.5 | 10.0 | 1.3 | 6/7 | PASS |
| 13 | TSM | Taiwan Semiconductor | EM_CORE | Technology | 2,304B USD† | 88 | 62 | 77.4 |  | 36.2% | 61.9% | 58.1% | 18 | 14.7% | 31.2% | 5.7 | 38.6 | 99.8† | 7/7 | PASS |
| 14 | PTC | PTC Inc. | US | Technology | 14B USD | 77 | 76 | 77.0 | 20.5% | 34.4% | 84.7% | 41.6% | 36 | 8.4% | 7.1% | 11.2 | 11.5 | 3.6 | 7/7 | PASS |
| 15 | EXE | Expand Energy | US | Energy | 21B USD | 65 | 95 | 76.8 | 15.6% | 17.6% | 48.0% | 34.0% | 26 | 18.2% | 7.9% | 3.3 | 6.7 | 1.1 | 7/7 | PASS |
| 16 | RMD | ResMed | US | Health Care | 29B USD | 86 | 62 | 76.3 | 27.2% | 25.2% | 62.2% | 35.3% | 13 | 6.9% | 5.0% | 13.4 | 19.4 | 4.5 | 7/7 | PASS |
| 17 | BIDU | Baidu | EM_CORE | Comm. Svcs | 40B USD | 63 | 96 | 76.1 | 60.2% | 0.3% | 42.1% | 10.0% | 32 |  | 19.8% |  |  | 1.0 | 6/7 | PASS |
| 18 | INCY | Incyte | US | Health Care | 23B USD | 86 | 61 | 75.8 | 65.9% | 30.8% | 52.8% | 25.6% | 1 | 7.3% | 2.5% | 12.1 | 16.1 | 4.0 | 7/7 | PASS |
| 19 | AMP | Ameriprise Financial | US | Financials | 43B USD | 81 | 68 | 75.6 |  | 66.9% | 56.6% | 37.2% | 56 |  | 7.8% |  | 12.0 | 7.0 | 7/7 | PASS |
| 20 | CTSH | Cognizant | US | Technology | 19B USD | 63 | 94 | 75.2 | 18.0% | 14.9% | 33.5% | 15.6% | 7 | 17.5% | 9.8% | 4.9 | 8.9 | 1.3 | 7/7 | PASS |
| 21 | FSLR | First Solar | US | Technology | 25B USD | 75 | 74 | 74.8 | 17.6% | 18.4% | 41.7% | 33.1% | 6 | 7.8% | 4.6% | 10.2 | 15.0 | 2.5 | 7/7 | PASS |
| 22 | TCS.NS | Tata Consultancy Svcs | EM_CORE | Technology | 7,173B INR | 78 | 71 | 74.7 | 68.9% | 48.4% | 40.3% | 25.3% | 10 | 9.8% | 5.2% | 9.8 | 14.6 | 6.7 | 7/7 | PASS |
| 23 | DECK | Deckers Outdoor | US | Cons. Disc. | 14B USD | 78 | 69 | 74.3 | 63.9% | 40.9% | 57.7% | 14.0% | 15 | 6.2% | 6.2% | 9.3 | 14.3 | 5.6 | 7/7 | PASS |
| 24 | 005930.KS | Samsung Electronics | DEV_EXUS | Technology | 1,917T KRW | 80 | 63 | 73.6 |  | 18.9% | 47.7% | 42.8% | 6 | 8.4% | 3.5% | 14.0 |  |  | 7/7 | PASS |
| 25 | SU.TO | Suncor Energy | DEV_EXUS | Energy | 90B CAD | 65 | 86 | 73.4 | 14.7% | 14.0% | 58.8% | 20.8% | 32 | 10.5% | 7.4% | 6.5 | 14.5 | 2.0 | 7/7 | PASS |
| 26 | BIIB | Biogen | US | Health Care | 31B USD | 72 | 75 | 73.0 | 8.6% | 7.7% | 78.7% | 22.9% | 35 | 6.8% | 6.2% | 9.4 | 22.6 | 1.7 | 7/7 | PASS |
| 27 | PBR | Petrobras | EM_CORE | Energy | 103B USD | 56 | 98 | 72.9 | 30.7% | 25.6% | 47.4% | 31.9% | 83 | 37.1% | 80.5%⚠ | 2.1 | 5.1 | 1.2 | 6/7 | PASS |
| 28 | ADBE | Adobe | US | Technology | 84B USD | 70 | 77 | 72.9 | 54.4% | 63.0% | 89.4% | 35.3% | 61 | 10.4% | 11.0% | 8.8 | 12.1 | 7.3 | 6/7 | PASS |
| 29 | HIG | Hartford Insurance | US | Financials | 37B USD | 61 | 90 | 72.6 | 18.8% | 22.7% | 38.2% | 15.3% | 23 | 11.9% | 15.3% | 6.7 | 9.4 | 2.0 | 7/7 | PASS |
| 30 | PFE | Pfizer | US | Health Care | 136B USD | 64 | 85 | 72.4 | 11.2% | 8.3% | 74.8% | 31.6% | 72 | 10.6% | 9.1% | 7.4 | 18.2 | 1.5 | 7/7 | PASS |
| 31 | MU | Micron Technology | US | Technology | 1,166B USD‡ | 95 | 38 | 72.2 | 108.3%* | 66.6% | 72.6% | 80.4% | 6 | 6.3% | 0.7% | 16.8 | 23.3 | 16.1 | 7/7 | PASS |
| 32 | LULU | Lululemon | US | Cons. Disc. | 13B USD | 63 | 85 | 71.9 | 18.3% | 32.0% | 55.7% | 11.2% | 44 | 9.1% | 8.6% | 5.4 | 9.4 | 2.8 | 7/7 | PASS |
| 33 | FOX | Fox Corp (B) | US | Comm. Svcs | 20B USD | 61 | 87 | 71.6 | 18.3% | 15.2% | 36.8% | 21.4% | 68 | 14.1% | 6.9% | 6.9 | 12.7 | 1.9 | 6/7 | PASS |
| 34 | GILD | Gilead Sciences | US | Health Care | 156B USD | 76 | 64 | 71.4 | 25.7% | 43.4% | 79.4% | 39.3% | 95 | 6.9% | 5.1% | 11.4 | 17.1 | 6.7 | 7/7 | PASS |
| 35 | ZTS | Zoetis | US | Health Care | 30B USD | 71 | 71 | 71.2 | 26.0% | 67.7% | 71.8% | 36.6% | 286 | 9.2% | 5.9% | 9.2 | 11.9 | 9.2 | 6/7 | PASS |
| 36 | ACN | Accenture | US | Technology | 80B USD | 60 | 89 | 71.1 | 32.5% | 24.4% | 32.0% | 17.0% | 25 | 15.5% | 15.1% | 6.2 | 10.5 | 2.5 | 7/7 | PASS |
| 37 | ACGL | Arch Capital Group | US | Financials | 34B USD | 56 | 94 | 70.9 | 17.7% | 21.3% | 39.4% | 25.3% | 11 | 14.6% | 15.3% | 5.8 | 7.6 | 1.5 | 5/7 | PASS |
| 38 | ABEV | Ambev | EM_CORE | Cons. Staples | 48B USD | 66 | 79 | 70.8 | 2379.7%* | 17.3% | 51.5% | 26.2% | 3 |  | 37.7%⚠ |  | 16.4 | 2.8 | 6/7 | PASS |
| 39 | FOXA | Fox Corp (A) | US | Comm. Svcs | 23B USD | 61 | 84 | 70.3 | 18.3% | 15.2% | 36.8% | 21.4% | 68 | 12.9% | 6.2% | 7.6 | 14.2 | 2.1 | 6/7 | PASS |
| 40 | BHP.AX | BHP Group | DEV_EXUS | Materials | 300B AUD | 78 | 58 | 70.1 | 19.6% | 24.7% | 83.1% | 40.7% | 53 | 6.8% | 2.7% | 12.4 | 20.2 | 4.1 | 7/7 | PASS |

**Flag legend:** `*` ROIC proxy >100%, buyback-depressed equity — unreliable, use ROE.
`⚠` FCF yield unusually high — likely a yfinance FCF-definition quirk for that ADR; verify
before trusting. `†` TSM/`005930.KS`/`MU` P/B or mktcap reflect ADR vs local share-class or a
currency label — do not compare cross-currency; verify at deep-dive. `‡` MU mktcap in a mixed
unit — treat as flag.

Full 554-row ranked table (incl. non-gated + all raw metrics) is in
`screens/quant_screen_ranked.csv`.

---

## 3. Sector clustering

**Top 40 gated names cluster in (normalized to common GICS labels):**

| Sector | # in top 40 |
|---|--:|
| Technology | 10 |
| Energy | 6 |
| Health Care | 6 |
| Financials | 4 |
| Communication Services | 4 |
| Materials | 3 |
| Consumer Discretionary | 3 |
| Consumer Staples | 2 |
| Industrials | 1 |
| Real Estate | 1 |

**Cross-validation vs Stage 1a (sector cheapness):** the heavy weightings in **Energy** (6),
**Materials** (3) and **Communication Services / value-tech** (Baidu, NetEase, Cognizant,
Accenture) are exactly the "cheap sector" tail one expects — commodity/energy trades at low
EV/EBITDA (APA 3.2, EXE 3.3, PBR 2.1) with strong FCF, and Chinese internet names screen very
cheap on FCF/P/B post-derating. **Technology topping the count is the quality-first tilt at
work:** it surfaces high-ROIC/high-margin software & semis (Intuit, PTC, Adobe, Accenture, TSM,
TCS) that clear the quality bar and are *reasonably* (not deeply) priced — the QARP sweet spot.
Health Care (Incyte, ResMed, Gilead, Pfizer, Biogen) shows the classic "de-rated pharma with
high margins" pattern. **This clustering should be compared against Stage 1a's sector-cheapness
ranking** — Energy/Materials/Comm-Svcs overlap = highest-conviction; Tech/Health-Care names in
otherwise-expensive sectors = the bottom-up "cheap quality in a dear sector" catches.

Across **all 434 gated** names the distribution is broad (Tech 78, Industrials 76, Health Care
56, Financials 45) — the *concentration into Energy/Materials/value-tech only appears at the
top of the ranking*, which is the intended signal.

---

## 4. Highlights (a handful, for the main session)

- **NEM (Newmont, Materials, US)** — #1. Gold major at EV/EBITDA 5.9, 15.9% earnings yield,
  ROIC 38%, Piotroski 7/7. Cheap cyclical with genuine quality.
- **TROW (T. Rowe Price, Financials, US)** — #2. Asset manager, ROIC 29%, D/E 4%, EV/EBITDA
  7.8, 12% EY, 7/7. Fortress balance sheet, cheap.
- **NTES (NetEase, Comm Svcs, EM/China)** — #4. 66% gross / 41% operating margin, EV/EBITDA
  6.4, FCF yield 41%. Best-quality of the cheap Chinese internet names.
- **INTU (Intuit, Tech, US)** — #5. 81% gross margin, ROIC 38%, reasonably priced software.
- **EOG / APA / EXE / EQT (Energy, US)** — cluster of high-FCF E&Ps at EV/EBITDA 3–6, EY 12–20%.
- **TSM & TCS (Tech, EM)** — elite-quality (58% / 25% op margin, high ROIC) at mid-teens P/E.

---

## 5. Small-cap exceptions

**None.** The universe is intentionally mid/large (S&P 500 + large ex-US/EM ADRs); the smallest
gated name in the top 40 is **APA at ~$11B**, and **zero** gated names fall below ~$5B market
cap. So there are no small-cap-on-exceptional-quality exceptions to report from this run. If
Hooman wants small-cap coverage, the universe must be extended (e.g. add a small-cap index or a
screened small-cap list) — flagged as an open item, not silently omitted.

---

## 6. EM-breadth stress test → paid-API recommendation

Pulled **41 mixed EM tickers** (India NSE, China/HK, Taiwan, Brazil B3, Mexico, South Africa
JSE, Indonesia, Thailand, Malaysia, Turkey, Saudi, Poland, Greece), measuring the 11 KEY
screening fields. Source: `screens/em_stress_test.csv`, as-of 2026-07-02.

| Metric | Result |
|---|---|
| **Usable (≥8/11 key fields)** | **29/41 = 71%** |
| Usable excluding 3 hard failures | 29/38 = **76%** |
| **Mean key-field completeness** | **83%** |
| yfinance hard errors | 0/41 |
| Total blackouts (0 fields) | 3: `TATAMOTORS.NS`, `MAYBANK.KL`, `OPAP.AT` |

**Reading it honestly:** the 9 names scoring exactly 7/11 are **all banks/financials**
(Axis Bank, ICBC Ag, Itaú, Bradesco, Banorte, FirstRand, BCA, BRI, PKO) — they *lack* gross
margin and EV/EBITDA **by nature**, not from a coverage gap. So the real "yfinance can't see
this EM name" failure rate is **~3/41 (7%)**, all from a slightly-wrong ticker symbol
(delisted/renamed form), not a systemic hole. Non-financial EM large caps came back with
**full 11/11 fields** almost universally (Maruti, Sun Pharma, Titan, Reliance-tier, PetroChina,
Sinopec, MediaTek, Chunghwa, Petrobras, Vale, WEG, Walmex, Naspers, Sasol, PTT, Saudi Aramco…).

**Recommendation (ASSUMED, evidence-based):** **Free sources (yfinance) SUFFICE for a
quality-first global screen at the large-cap level, including EM.** ~83% mean field
completeness and ~93% "reachable" rate on a deliberately-broad EM batch is enough to build a
diversified EM sleeve without paying. **Buy a paid global API (FMP is the price/coverage pick)
ONLY if** the funnel later needs (a) **EM breadth below the large-caps** (where Yahoo thins out
fast — untested here and the known risk), (b) **point-in-time/historical** fundamentals for
backtesting, or (c) **clean financials for banks/insurers** (the fields yfinance omits). For
Stage 1b's mandate — a first-pass global cheap-quality shortlist — **stay free.**

---

## 7. Coverage & limitations

- **Universe size:** 639 fetched (503 US / 94 dev-exUS / 42 EM), **554 rankable**, **434 pass
  the trap gate**. 0 yfinance fetch errors across the 639.
- **85 unrankable** — mostly **financials/REITs** (no gross margin or EV/EBITDA — a *metric
  applicability* issue, not missing data; 29 of 58 US drops are Financial Services) plus a few
  missing one composite input, and one bad ticker (`ROG.SW`/Roche returned nothing — needs the
  correct Yahoo symbol). **Financials are under-screened by design here** and need a
  bank-specific quality/value screen (P/B, ROE, CET1, NIM) as a follow-on.
- **Region skew:** the top 40 is **29 US / 8 EM / 3 dev-exUS**. This is partly real (US quality
  premium + deep coverage) and partly a **universe-construction artifact** (503 US vs 94+42
  ex-US). To fairly compare regions, either expand the ex-US/EM universe or rank *within* region.
  Under-represented: **developed Europe/Japan below mega-cap, and EM below the top ~40 names.**
- **Single-source & snapshot:** all fundamentals are one yfinance `.info` snapshot (2026-07-02),
  **not cross-checked vs EDGAR/filings** in this stage. Multiples move daily. Piotroski is
  "lite" (no YoY deltas). **Every name that advances must be re-verified at deep-dive.**
- **Known data artifacts (flagged, not hidden):** ROIC proxy inflates for heavy-buyback firms
  (Ambev 2380%*, Micron 108%*) → use ROE; some ADRs show quirky FCF yields (PDD 61%, PBR 80%,
  Ambev 38%) or P/B (TSM 99.8, Samsung/MU unit labels) from ADR-vs-local-share or currency
  mixing → verify before trusting. The scoring guards blank the worst EV/EBITDA glitches so they
  don't drive the rank.
- **Currency:** market caps are native currency (INR, KRW, CAD, AUD, BRL…). **Do not compare
  cross-currency without FX conversion.**
- **Confidence:** individual pulled fields **VERIFIED** (real fetch, 2026-07-02); the ranking
  and any cross-name comparison **ASSUMED** (single-source, proxy metrics, snapshot).
