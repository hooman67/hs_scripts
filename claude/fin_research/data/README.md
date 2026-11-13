# data/ — Stage 0 Data Pipeline

Reproducible, cited data pulls for the value-investing funnel. Built 2026-07-01 by Claude
(Opus 4.8). Every number below comes from a **real fetched pull on 2026-07-01/02** — no
figures are invented. Prices move daily; treat quoted prices/multiples as as-of that pull.

Two scripts, two data layers:

| script | source | what it gives | geography |
|---|---|---|---|
| `fetch_damodaran.py` | NYU / Aswath Damodaran industry datasets (.xls) | **sector-level** multiples, margins, ROE, ROIC (top-down cheapness + quality) | US, Global, Emerging |
| `fetch_fundamentals.py` | yfinance + SEC EDGAR | **company-level** price, market cap, ratios, primary financials | global (yfinance); US-listed only (EDGAR) |

Run everything with the project venv: `/opt/venv/bin/python3`.

---

## 1. `fetch_damodaran.py`

Downloads Damodaran's industry-average datasets, auto-detects the header row (the files have
a variable-length metadata preamble), extracts each file's "Date updated:" as-of date, and
emits a tidy combined CSV plus per-region wide tables.

**Run:**
```bash
/opt/venv/bin/python3 data/fetch_damodaran.py            # fetch + parse (16 datasets)
/opt/venv/bin/python3 data/fetch_damodaran.py --no-download   # re-parse cached .xls only
```

**Base URL (VERIFIED reachable 2026-07-01):** `https://pages.stern.nyu.edu/~adamodar/pc/datasets/`
Requires no special headers; plain `requests.get` works.

### Datasets fetched (all returned HTTP 200; `damodaran_manifest.csv` records this)

| file (stem `.xls`) | topic | US | Global | Emerging |
|---|---|:-:|:-:|:-:|
| `pedata` | Current/Trailing/Forward **PE**, PEG, expected growth | ✅ | ❌ | ❌ |
| `vebitda` / `vebitdaGlobal` / `vebitdaemerg` | **EV/EBITDA**, EV/EBIT, EV/Sales | ✅ | ✅ | ✅ |
| `pbvdata` / `pbvGlobal` / `pbvemerg` | **P/B**, ROE, EV/Invested Capital, **ROIC** | ✅ | ✅ | ✅ |
| `margin` / `marginGlobal` / `marginemerg` | gross / operating / **net margins** | ✅ | ✅ | ✅ |
| `roe` / `roeGlobal` / `roeemerg` | **ROE** (unadjusted + R&D-adjusted) | ✅ | ✅ | ✅ |
| `EVA` / `EVAGlobal` / `EVAemerg` | ROE, **ROC (=ROIC)**, cost of equity, WACC, EVA, beta, D/E | ✅ | ✅ | ✅ |

**⚠️ Real limitation:** Damodaran publishes the **PE table for the US ONLY** (`pedata.xls`).
There is no `pedataGlobal`/`pedataemerg` (both probed → HTTP 404). For non-US sector P/E, use
the **P/B + ROE** table (`pbvGlobal`/`pbvemerg`, which have all regions) or derive an implied
P/E from EV/EBITDA. Every other metric has full US/Global/Emerging coverage.

### Outputs (in `data/damodaran/`)
- `<stem>.xls` — raw file, exactly as fetched.
- `damodaran_combined.csv` — **tidy long form**, 15,945 rows. Columns:
  `region, Industry Name, metric, value, source_file, source_url, as_of_date, dataset`.
  This is the table later stages should query.
- `damodaran_wide_US.csv` / `_Global.csv` / `_Emerging.csv` — convenience wide tables,
  indexed by `Industry Name`, columns prefixed by dataset (e.g. `pedata::Forward PE`,
  `EVA::ROC`).
- `damodaran_manifest.csv` — one row per dataset: file, url, status, as-of date, region,
  n_industries. **The audit trail** proving what was fetched and when.

Each region file covers **96 industries**.

### As-of dates (from the files themselves, `damodaran_manifest.csv`)
15 of 16 files: **2026-01-05**. One exception — **`EVAGlobal` is dated 2025-01-05**:
Damodaran had not yet refreshed the *global* EVA/ROIC file for 2026 at pull time. So global
ROIC-via-EVA lags a year; the global **P/B table's** ROIC column (`pbvGlobal`, 2026-01-05) is
the fresher fallback. This is a real snapshot-lag gotcha, surfaced not hidden.

### Real sample — US PE table (from `damodaran_wide_US.csv`, as-of 2026-01-05)

```
Industry Name        Current PE  Trailing PE  Forward PE  # firms
Advertising              132.24        44.43       52.87       52
Aerospace/Defense        118.00        92.80       45.87       79
Air Transport             15.55        18.32       11.37       23
Apparel                   82.10        37.83       24.89       35
Auto & Truck              44.59        64.32       49.04       33
```

### Real sample — cross-region EV/EBITDA (tidy CSV, as-of 2026-01-05)

```
Industry Name                       US   Global  Emerging
Software (System & Application)  24.48    24.64     40.57
Oil/Gas (Integrated)              8.16     6.18      6.47
Semiconductor                    34.75    26.98     17.00
Retail (General)                 17.38    17.10     14.86
```

### Real sample — cross-region ROC (=ROIC), % (from EVA files)

```
Industry Name                     US   Global  Emerging
Software (System & Application)  29.3    23.7      0.7
Oil/Gas (Integrated)              8.4    13.9     20.0
Semiconductor                    27.2    20.5     16.2
Retail (General)                 13.6    11.7      7.2
```

Note: Damodaran ratios are **simple industry averages** (or aggregate ratios), not
market-cap-weighted, and are annual snapshots — good for *relative* sector cheapness/quality,
not for pinning a single company's live multiple (use `fetch_fundamentals.py` for that).

---

## 2. `fetch_fundamentals.py`

Per-company fundamentals. yfinance for everything (global); EDGAR XBRL company-facts for
primary financials on US-listed filers (incl. foreign filers via IFRS/20-F).

**Run:**
```bash
/opt/venv/bin/python3 data/fetch_fundamentals.py AAPL SAP NESN.SW TSM INFY
/opt/venv/bin/python3 data/fetch_fundamentals.py --file tickers.txt --refresh
/opt/venv/bin/python3 data/fetch_fundamentals.py AAPL MSFT --no-edgar
```
**EDGAR requires the User-Agent header** `Hooman Shariati hshariati@adobe.com` (set in the
script). Ticker→CIK map from `https://www.sec.gov/files/company_tickers.json` (10,426 US
tickers), cached locally.

**Importable** by later stages:
```python
from fetch_fundamentals import get_fundamentals, get_edgar_financials, fetch_many
```

### yfinance ticker conventions (global reach)
US bare (`AAPL`); Yahoo exchange suffixes for non-US native listings — Swiss `NESN.SW`,
Xetra `SAP.DE`, London `.L`, Paris `.PA`, Tokyo `.T`, Hong Kong `0700.HK`, India NSE
`RELIANCE.NS` / BSE `.BO`. US-listed ADRs use the bare ADR ticker (`TSM`, `INFY`, `SAP`).

### Fields harvested (yfinance `.info`, schema stable in `YF_FIELDS`)
Identity (name, currency, sector, industry, country, exchange); price & size (price,
marketCap, enterpriseValue); valuation (trailingPE, forwardPE, priceToBook, P/S,
enterpriseToEbitda, PEG); quality (ROE, ROA, gross/operating/net/ebitda margins, revenue &
earnings growth); balance sheet (debtToEquity, totalDebt, cash, current/quick ratio); cash
flow (freeCashflow, operatingCashflow); per-share (EPS, bookValue); income (dividendYield,
payoutRatio, beta). Derived: `fcf_yield`.

### Outputs (in `data/cache/`)
- `yf_<TICKER>.json` — full yfinance pull incl. `_missing` (fields Yahoo didn't return) and
  `error` (null on success). **Cached 12h** (prices move intraday); `--refresh` forces fresh.
- `edgar_<TICKER>.json` — annual primary financials (last ~4 FYs) with `taxonomy`
  (us-gaap / ifrs-full), per-figure `tag`, `unit`, and fiscal-year `end` date. For non-US
  names: `{"available": false, "reason": "ticker not in SEC EDGAR (likely non-US-listed)"}`.
- `sec_ticker_cik_map.json` — cached CIK map.
- `fundamentals_summary.csv` — one row per ticker, the flattened key columns.

### Anti-hallucination behavior (tested)
- Missing yfinance fields → `None`, listed in `_missing`; **never fabricated**.
- Bogus ticker (`ZZZZNOTREAL`) → all fields None, `n_missing_fields=39`, `edgar_available=False`.
  (yfinance prints a harmless `404 ... Quote not found` line to stderr; the row is still clean.)
- EDGAR picks **USD** units when a foreign filer reports both USD and local currency, and
  records the `unit` on every figure so currency is never mislabeled.

### Real sample — fundamentals pull (2026-07-01, from `fundamentals_summary.csv`)

```
ticker  shortName             ccy   marketCap        trailingPE  P/B     EV/EBITDA  ROE    op.margin  edgar   missing
AAPL    Apple Inc.            USD   4,323,663,937,536  35.68     40.55   27.13      1.415  0.323      True    0
SAP     SAP SE                USD     187,627,077,632  22.42      3.56   15.81      0.164  0.300      True    0
NESN.SW NESTLE N              CHF     213,185,576,960  23.61      6.50   15.92      0.265  0.149      False   0
TSM     Taiwan Semiconductor  USD   2,303,987,286,016  38.60     99.80   5.67      0.362  0.581      True    0
INFY    Infosys Limited       USD      43,121,082,368  13.31      8.81   18.86      0.314  0.209      True    0
```
Coverage: **20/20 requested yfinance fields present for all five** (US, Germany-ADR,
Switzerland-native, Taiwan-ADR, India-ADR). `AAPL` is a US $ company; `NESN.SW` reports in
CHF (native Swiss listing); the three ADRs report in USD.

### Real sample — EDGAR primary financials (ground truth, from `edgar_*.json`)

```
AAPL (us-gaap):  revenue  $416,161,000,000  net income $112,010,000,000  equity $73,733,000,000   FY end 2025-09-27
TSM  (ifrs-full): revenue $88,268,000,000   net income $35,301,100,000   equity $130,505,400,000  FY end 2024-12-31 (USD unit)
```
TSM demonstrates the IFRS/20-F path: it files under `ifrs-full` (not `us-gaap`), reports
revenue in both TWD (2,894,307,700,000) and USD (88,268,000,000) — the script correctly
selects USD. `NESN.SW` is **not in EDGAR** (Swiss listing, no SEC filing) → cleanly flagged
unavailable with a reason, not faked.

---

## 3. Data coverage & limitations (HONEST — read before trusting a region)

This section directly informs whether a **paid global API** is needed later.

### By region — company-level fundamentals (yfinance)
- **US mid/large cap: STRONG.** Full field coverage, cross-checkable vs EDGAR ground truth.
- **Developed ex-US (Europe, Japan, etc.): GOOD.** Native listings (`NESN.SW`, `SAP.DE`) and
  ADRs return full fields in the tested sample. Currency varies (native = local ccy) — always
  read the `currency` field; don't compare marketCaps across currencies without converting.
- **Emerging markets: MODERATE / uneven.** Large EM names via **US ADRs** (`TSM`, `INFY`) and
  major exchange suffixes (`RELIANCE.NS`, `0700.HK`) worked with full fields in testing. But
  yfinance EM coverage is known to thin out fast below the mega/large-caps: missing fields,
  stale prices, and gaps for local-only small/mid EM tickers are common. **This is the single
  biggest coverage risk for the "diversify into EM" goal.** We haven't yet stress-tested a
  broad EM universe — do that before committing to free-only for EM breadth.

### Company-level primary financials (EDGAR)
- **US-listed filers only** (incl. foreign filers via 20-F/IFRS). Non-US-listed names
  (Nestlé, most European/Asian locals) are **not in EDGAR at all** — no ground-truth
  cross-check for them; you're relying on yfinance alone, which is a weaker anti-hallucination
  posture for ex-US names. Confirmed: `NESN.SW` absent from EDGAR.
- Foreign filers report under **IFRS** with different XBRL tags (handled), and some concepts
  won't map 1:1 to the us-gaap set.

### Sector-level (Damodaran)
- **Coverage GOOD across US / Global / Emerging** on EV/EBITDA, P/B, margins, ROE, ROIC.
- **Annual snapshot lag:** files dated 2026-01-05 (one, `EVAGlobal`, still 2025-01-05).
  Sector multiples are stale within the year — mitigate by combining with **live** company
  multiples from yfinance. Damodaran is for *relative sector cheapness/quality vs history*,
  not for a live price.
- **US-only PE table** (see §1). No per-company data — industry aggregates only.
- Damodaran's industry taxonomy (~96 industries) ≠ GICS sectors; a mapping layer will be
  needed to line his industries up with yfinance's `sector`/`industry`.

### Reliability protocol (carry into every stage)
1. yfinance is **secondary** — verify any surprising/ranking-driving figure vs EDGAR (US) or
   a second source. Cross-check EM names especially.
2. Record source + as-of on every number (both scripts do this).
3. Treat a missing field as missing — never infer/fill.

### Recommendation on paid API (for Hooman)
- **Free sources SUFFICE for: US (all caps), developed-market large/mid caps, and the
  large-cap EM names reachable via ADRs / major exchange suffixes.** That already covers a
  broad, diversified, quality-first global shortlist.
- **A paid global fundamentals API becomes worth it IF** the funnel needs (a) **broad EM
  breadth** below the mega-caps (where yfinance thins out and there's no EDGAR backstop),
  (b) **point-in-time / historical** fundamentals for backtesting, or (c) clean bulk
  screening across thousands of non-US tickers without per-ticker plumbing. Candidates:
  Financial Modeling Prep (good price/coverage ratio, global), or Refinitiv/FactSet (pricey).
- **Suggested path:** run Stage 1 on free sources first. If EM candidates come back sparse or
  field-poor, that's the concrete signal to buy an API — decide with evidence, not upfront.
  A quick EM-breadth stress test (pull 30-50 mixed EM tickers, measure field completeness) is
  the cheapest way to make that call.
