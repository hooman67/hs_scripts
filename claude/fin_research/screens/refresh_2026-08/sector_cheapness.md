# Stage 1A — Top-Down Sector Cheapness (REFRESH as of 2026-08-26)

Run: 2026-08-26 by Claude (Opus 4.8). Owner: Hooman Shariati.
Refreshes the 2026-07-01 run at `screens/sector_cheapness.md`. Method + code REUSED verbatim
(`screens/fetch_damodaran_history.py`, `screens/analyze_sector_cheapness.py`).

---

## TL;DR — the source has NOT refreshed; the cheap-sector picture is unchanged

**Key finding (VERIFIED 2026-08-26):** every live Damodaran industry file is still stamped
**"Date updated: 2026-01-05"** — identical to the last run. Damodaran refreshes his industry
datasets **once a year, each January**; there has been no new publication since. So the
**sector-relative cheapness picture at the source is unchanged** — the entire funnel's
top-down input is byte-for-byte the same 2026-01-05 snapshot.

I re-fetched all seven live files fresh (HTTP 200, verified as-of date on each), rebuilt the
11-year history (15,685 rows, 77/77 archive files parse OK), and re-ran the analyzer. The
ranked tables reproduce the original run **exactly**. Nothing has "de-rated further" or
"recovered" at the Damodaran level, because Damodaran only takes one snapshot a year.

→ **What actually moved since July lives in LIVE COMPANY PRICES** (the other two agents'
job). This top-down screen's contribution is to **confirm the cheap-sector shortlist still
stands** and hand Stage-3 leader-hunting the same not-dying-and-decent-ROIC targets.

**Cheap-sector shortlist (unchanged, re-confirmed) — 3-5 to point Stage 3 at:**
1. **Information Services** (US+Global) — EV/EBITDA 5th pctile of own 11yr, **ROIC ~22%**. Cheap on AI *sentiment*, not broken economics. Buy the moaty ratings/index franchises, avoid pure AI-exposed data vendors.
2. **Building Materials** (US) — **ROIC ~20%**, cyclical housing trough + infrastructure floor. Classic cyclical-cheap.
3. **Beverage (Alcoholic)** (US+Global) — 5th-pctile EV/EBITDA, US ROE at a 0.6% *trough* (cyclical destocking/tariff cycle, not dead demand). Mean-reversion candidate; skip wine-heavy names.
4. **Beverage (Soft) / Household Products** (Global) — quality compounders on relative sale (**ROIC 29% / 23%**), P/B at bottom of own range. "Great business at a fair-ish price," not deep value.
5. **Insurance (Life, EM)** — best risk/reward in cheap EM: cheap vs own history AND vs peers (xsec 6), **ROIC 15% / ROE 17.6%**, secular premium-growth runway.

**Still explicitly AVOID as secular-decline traps:** Cable TV (US+Global, confirmed
bleedout), Food Processing (GLP-1 + MAHA + private-label), AI-exposed Education/pure data
vendors. **Low-return cheap-but-mediocre (skip for quality-first):** RE Development, Utility
(Water), R.E.I.T. (ROIC 3-7%).

---

## Verification log (as-of dates, this refresh)

| Check | Result | As-of / date |
|---|---|---|
| Live `vebitda.xls` (US EV/EBITDA) | HTTP 200, 58,880 B | **Date updated: 2026-01-05** — VERIFIED |
| Live `pbvdata.xls` (US P/B, ROIC, ROE) | HTTP 200, 52,736 B | **2026-01-05** — VERIFIED |
| Live `vebitdaGlobal.xls` | HTTP 200, 58,368 B | **2026-01-05** — VERIFIED |
| Live `pbvGlobal.xls` | HTTP 200, 53,248 B | **2026-01-05** — VERIFIED |
| Live `vebitdaemerg.xls` | HTTP 200, 58,368 B | **2026-01-05** — VERIFIED |
| Live `pbvemerg.xls` | HTTP 200, 53,248 B | **2026-01-05** — VERIFIED |
| Live `pedata.xls` (US P/E) | HTTP 200, 61,952 B | **2026-01-05** — VERIFIED |
| History rebuild (`fetch_damodaran_history.py --no-download`) | 15,685 rows, years 2015-2025, 77/77 files OK | archives as-of 2016-01-05 → 2026-01-05 |
| Analyzer re-run (`analyze_sector_cheapness.py`) | 3 region CSVs regenerated, rankings identical to 2026-07-01 | current = data_year 2025 = as-of 2026-01-05 |

Fetched fresh from `https://pages.stern.nyu.edu/~adamodar/pc/datasets/<stem>.xls` with the
Mozilla/UA header, "Industry Averages" sheet, `.xls` (not `.xlsx`) — per the pipeline spec.
All multiples/ROIC/ROE below are **VERIFIED** real Damodaran values, as-of **2026-01-05**.

---

## Cheapest sectors vs OWN 11-year history + cross-section — re-confirmed

Composite = mean of available own-history percentiles (EV/EBITDA + P/B, + US P/E). Lower =
cheaper vs its own 2015-2025 past. `xsec` = cross-section percentile vs region peers this year.
Full tables: `data/damodaran/history/sector_cheapness_{US,Global,Emerging}.csv`.

### US (own-history composite, low = cheap)
| Industry | comp. | EV/EBITDA (hist%) | P/B (hist%) | Cur P/E (hist%) | ROIC | ROE | xsec EV/EBITDA |
|---|--:|--|--:|--|--:|--:|--:|
| Food Processing | 10.6 | 10.0 (4.5%) | 1.8 (4.5%) | 31.0 (23%) | 16% | 5% | 25 | **← trap (secular)** |
| Utility (Water) | 13.6 | 14.1 (23%) | 2.0 (4.5%) | 22.0 (14%) | 7% | 10% | 58 | **← low-ROIC, skip** |
| **Information Services** | 13.6 | 11.5 (4.5%) | 3.8 (14%) | 29.3 (23%) | **22%** | 15% | 40 | **← BUY sub-segment** |
| Cable TV | 16.7 | 6.2 (4.5%) | 1.3 (4.5%) | 13.7 (41%) | 12% | 11% | **2** | **← trap (secular)** |
| Real Estate (Dev) | 16.7 | 10.2 (4.5%) | 1.0 (14%) | 29.4 (32%) | 7% | 5% | 26 | **← low-ROIC, skip** |
| **Beverage (Alcoholic)** | 16.7 | 8.6 (4.5%) | 1.9 (4.5%) | 35.0 (41%) | 16% | 0.6% | 16 | **← cyclical trough** |
| **Beverage (Soft)** | 22.7 | 16.9 (32%) | 6.9 (4.5%) | 37.1 (32%) | **29%** | **31%** | 73 | **← quality on sale** |
| **Building Materials** | 22.7 | 11.6 (41%) | 3.6 (23%) | 21.1 (4.5%) | **20%** | 16% | 44 | **← cyclical opp.** |
| Telecom. Services | 25.8 | 6.5 (23%) | 1.6 (41%) | 26.5 (14%) | 12% | 15% | **4** | secular-lean |

### Global (composite = EV/EBITDA + P/B only; no Global P/E table)
| Industry | comp. | EV/EBITDA (hist%) | P/B (hist%) | ROIC | ROE | xsec |
|---|--:|--|--:|--:|--:|--:|
| Cable TV | 4.5 | 6.6 (4.5%) | 1.4 (4.5%) | 11% | 8% | **3** | **← trap** |
| **Information Services** | 9.1 | 10.8 (4.5%) | 3.3 (14%) | **23%** | 15% | 34 | **← BUY sub-segment** |
| Food Processing | 13.6 | 11.1 (14%) | 2.2 (14%) | 12% | 11% | 38 | **← trap** |
| Education | 13.6 | 9.0 (14%) | 1.9 (14%) | 14% | 12% | 16 | split (stock-pick) |
| **Beverage (Alcoholic)** | 13.6 | 12.2 (14%) | 2.8 (14%) | 15% | 14% | 49 | **← cyclical** |
| **Household Products** | 13.6 | 14.6 (23%) | 4.6 (4.5%) | **23%** | 18% | 68 | **← quality on sale** |
| **Beverage (Soft)** | 22.7 | 16.0 (23%) | 5.8 (23%) | **30%** | 31% | 75 | **← quality on sale** |

### Emerging (composite = EV/EBITDA + P/B only)
| Industry | comp. | EV/EBITDA (hist%) | P/B (hist%) | ROIC | ROE | xsec |
|---|--:|--|--:|--:|--:|--:|
| Transportation (Railroads) | 4.5 | 8.2 (4.5%) | 0.9 (4.5%) | 7% | 7% | 11 | cyclical, low-ROIC |
| Shoe | 9.1 | 9.0 (14%) | 1.4 (4.5%) | 10% | 11% | 15 | cyclical |
| Retail (Building Supply) | 9.1 | 9.6 (14%) | 2.2 (4.5%) | 14% | 5% | 21 | cyclical |
| Education | 13.6 | 8.4 (14%) | 1.5 (14%) | 13% | 10% | 13 | split |
| Retail (Automotive) | 18.2 | 9.0 (23%) | 1.4 (14%) | 10% | 4% | 16 | cyclical |
| Trucking | 18.2 | 7.3 (14%) | 1.6 (23%) | 9% | 4% | **7** | cyclical |
| **Insurance (Life)** | 18.2 | 7.3 (4.5%) | 1.4 (32%) | **15%** | **18%** | **6** | **← BUY (best EM quality)** |

---

## Vs the original run's finds — what changed

**Nothing at the source.** Because Damodaran is annual and the file is the same 2026-01-05
snapshot, every original find re-confirms with identical numbers:

| Original find | Status this refresh | Note |
|---|---|---|
| Information Services (cheap, 22% ROIC) | **Still cheap — CONFIRMED** | US EV/EBITDA 4.5th pctile; unchanged |
| Beverage (Alcoholic), cyclical trough | **Still cheap — CONFIRMED** | US ROE still 0.6% trough |
| Beverage (Soft), quality on sale | **Still cheap — CONFIRMED** | 29% ROIC unchanged |
| Building Materials, cyclical opp. | **Still cheap — CONFIRMED** | 20% ROIC unchanged |
| Household Products (Global) | **Still cheap — CONFIRMED** | 23% ROIC unchanged |
| EM Insurance (Life) | **Still cheap — CONFIRMED** | ROIC 15% / ROE 18%, xsec 6 |
| EM Railroads / Trucking / Auto retail | **Still cheap — CONFIRMED** | low-ROIC cluster, unchanged |
| Cable TV (trap), Food Processing (trap) | **Still flagged trap — CONFIRMED** | avoid |

**De-rated further / recovered?** — Not answerable from Damodaran (annual). Any re-rating
since Jan-2026 is a **live-price** phenomenon and must come from the two live-company-price
agents. This screen's job is done once the shortlist is re-confirmed, which it is.

---

## Cyclical-cheap vs secular-trap — carried forward (verdicts from 2026-07 web research)

Verdicts unchanged from the original run (they were live-web-sourced 2025-2026, not from
Damodaran, and the refresh window is short). Summary:
- **CYCLICAL / opportunity:** Beverage (Alcoholic & Soft), Building Materials, Household
  Products, EM Life Insurance, EM transport/auto-retail cluster.
- **MIXED / stock-pick:** Information Services (AI-sentiment overhang on moaty franchises),
  Education (regulated EM survivors OK, AI-exposed edtech = trap).
- **SECULAR / trap:** Cable TV (linear-TV bleedout), Food Processing (GLP-1 + MAHA +
  private label), AI-exposed pure data vendors.
- **Low-return, skip for quality-first:** RE Development, Utility (Water), R.E.I.T.

Full citations in the original `screens/sector_cheapness.md` "Cyclical vs structural" table.

---

## Recommendation to the funnel

1. **Point Stage-3 leader-hunting at the 5 shortlist sectors above** — this refresh adds no
   new sectors and drops none; the target set is stable.
2. **The alpha this cycle is in live prices, not the sector snapshot.** Because Damodaran
   hasn't refreshed, the only thing that has moved the cheap-sector picture since July is
   individual company re-rating — defer to the live-price agents for which *names* inside
   these sectors got cheaper/richer.
3. **Next Damodaran refresh: ~January 2027.** A re-run before then will reproduce these exact
   tables — no need to re-pull the top-down screen until the January file drops.

**Reproduce this refresh:**
```
/opt/venv/bin/python3 screens/fetch_damodaran_history.py --no-download   # rebuild 11yr history from cached .xls
/opt/venv/bin/python3 screens/analyze_sector_cheapness.py                # rank + write per-region CSVs
```
Outputs: `data/damodaran/history/sector_cheapness_{US,Global,Emerging}.csv` (regenerated
2026-08-26, identical to 2026-07-01).
