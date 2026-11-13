# US Quant Screen — Refresh on Live Data (2026-08-26)

**Re-run of the Stage-1b bottom-up quality-at-a-price screen, US large/mid-cap universe (S&P 500).**
Same code, same method as the 2026-07-02 run — only the prices are new.

- **Run date / as-of:** yfinance `.info` pulled **live 2026-08-26**, timestamp
  `2026-08-26T18:02:09+00:00` on every row. 82-second full pull, **0 fetch errors**.
- **Method (unchanged, reused verbatim):** imported `derive_metrics` / `piotroski_lite` /
  `score_and_rank` from `screens/run_quant_screen.py` and `build_universe()` from
  `screens/universe.py` (filtered to `region=="US"`, `refresh=True`). Quality-first **60/40**
  combined percentile rank; value-trap gate = FCF>0 **and** Piotroski-lite ≥60% of max **and**
  D/E<300%. Data-quality guards active (EV/EBITDA<2 blanked; ROIC>100% flagged→ROE fallback).
- **Universe:** 503 S&P 500 names → **444 rankable**, **355 pass the trap gate** (the 59
  unrankable are mostly financials/REITs lacking gross-margin/EV-EBITDA by nature).
- **Owner:** Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.** Confidence:
  individual pulled fields **VERIFIED** (real live fetch today); the ranking **ASSUMED**
  (single-source yfinance snapshot, proxy metrics, no EDGAR cross-check in this breadth stage).
- **Code + outputs (this dir):** `run_refresh_us.py`, `quant_us_raw.csv` (503 rows),
  `quant_us_ranked.csv` (444 scored), `refresh_run.log` (verification log).

> ⚠️ ANTI-HALLUCINATION: every ratio is a real yfinance pull on 2026-08-26. Missing fields are
> blank, never guessed. ADR/foreign-filer names are excluded here (US-only run), so the
> currency-mix bug is not in play; the `.L` pence trap is not in play (no London names). ROIC>100%
> and negative/huge P/B artifacts are **flagged** and were swapped for ROE in the ranking input.

---

## 1. Top 25 cheap-quality US names (trap-gate PASS, ranked by combined score)

All figures yfinance, **as-of 2026-08-26**. `Q`=quality pctl, `C`=cheapness pctl. `EV/EBITDA`
blank = cleaned/negative-EV artifact. `*` = ROIC-proxy >100% (buyback-depressed book) — use ROE.
`†` = P/B artifact (negative or buyback-inflated book equity) — ignore P/B, use ROIC/FCF.

| # | Ticker | Name | Sector | Score | Q | C | P/E | Fwd P/E | EV/EBITDA | P/B | ROE | FCF yld | Piotr | Verdict |
|--:|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--:|---|
| 1 | **NEM** | Newmont | Materials | 84.6 | 89 | 78 | 16.7 | 12.5 | 8.2 | 3.98 | 25.9% | 6.3% | 7/7 | quality — cheap-on-peak-gold ⚠ |
| 2 | **TROW** | T. Rowe Price | Financials | 83.4 | 80 | 88 | 11.3 | 10.9 | 7.6 | 2.17 | 19.4% | 8.5% | 7/7 | **cheap AND quality** |
| 3 | **EOG** | EOG Resources | Energy | 83.4 | 81 | 86 | 11.3 | 10.0 | 5.5 | 2.52 | 22.5% | 5.8% | 7/7 | **cheap AND quality** |
| 4 | **APA** | APA Corp | Energy | 82.9 | 75 | 94 | 8.8 | 9.9 | 3.3 | 2.08 | 26.7% | 14.7% | 6/7 | cheap; higher-lev E&P |
| 5 | **CF** | CF Industries | Materials | 82.8 | 81 | 86 | 9.4 | 12.1 | 6.1 | 3.33 | 29.9% | 6.7% | 7/7 | cheap AND quality — cyclical N |
| 6 | **FSLR** | First Solar | Info Tech | 82.4 | 79 | 87 | 12.6 | 8.9 | 8.7 | 2.13 | 18.5% | 7.3% | 6/7 | cheap; policy-risk (OBBBA) |
| 7 | **INCY** | Incyte | Health Care | 81.8 | 88 | 73 | 16.4 | 14.4 | 11.2 | 4.09 | 30.7% | 4.5% | 7/7 | quality; ROIC 101%*→use ROE |
| 8 | **OXY** | Occidental | Energy | 81.5 | 77 | 88 | 17.3 | 15.3 | 5.7 | 1.76 | 10.6% | 6.4% | 7/7 | cheap; levered, lower ROE |
| 9 | **CINF** | Cincinnati Financial | Financials | 78.1 | 66 | 96 | 8.1 | 19.1 | 5.8 | 1.59 | 21.5% | 11.3% | 7/7 | cheap trailing; fwd P/E jumps 19 ⚠ |
| 10 | **TTD** | The Trade Desk | Comm Svcs | 77.1 | 72 | 84 | 15.6 | 13.2 | 7.4 | 2.52 | 15.4% | 9.5% | 7/7 | **NEW — de-rated adtech** |
| 11 | **INTU** | Intuit | Info Tech | 76.2 | 84 | 65 | 20.8 | 11.9 | 15.3 | 4.55 | 22.5% | 5.6% | 7/7 | quality; **re-rated up** (see §3) |
| 12 | **SNDK** | Sandisk | Info Tech | 76.1 | 94 | 50 | 20.4 | 5.7 | 16.8 | 16.1† | 91.6% | 3.5% | 7/7 | **NEW — memory upcycle** ⚠ |
| 13 | **DECK** | Deckers | Cons Disc | 75.9 | 75 | 77 | 12.7 | 10.7 | 8.3 | 5.31 | 42.6% | 7.2% | 7/7 | cheap AND quality |
| 14 | **IT** | Gartner | Info Tech | 75.4 | 67 | 88 | 17.4 | 11.8 | 10.3 | −74† | 114%† | 8.6% | 4/6 | **NEW**; P/B neg — use ROIC/FCF |
| 15 | **MAS** | Masco | Industrials | 75.0 | 69 | 84 | 16.9 | 15.7 | 11.7 | −40† | — | 6.2% | 5/6 | **NEW**; P/B neg — buyback |
| 16 | **MU** | Micron | Info Tech | 74.6 | 95 | 44 | 21.3 | 6.1 | 15.2 | 10.5 | 66.6% | 0.7% | 7/7 | quality; expensive trailing, cheap fwd ⚠ |
| 17 | **CPRT** | Copart | Industrials | 74.5 | 85 | 59 | 20.4 | 19.6 | 13.6 | 3.46 | 17.6% | 3.2% | 7/7 | quality, not cheap |
| 18 | **HIG** | Hartford | Financials | 74.5 | 62 | 93 | 9.6 | 10.2 | 6.8 | 1.97 | 22.1% | 14.5% | 7/7 | **NEW — cheap insurer** |
| 19 | **COP** | ConocoPhillips | Energy | 73.8 | 69 | 81 | 17.4 | 13.8 | 6.5 | 2.42 | 14.2% | 4.9% | 7/7 | **NEW — cheap major E&P** |
| 20 | **CTSH** | Cognizant | Info Tech | 73.1 | 62 | 89 | 13.3 | 9.8 | 7.3 | 1.93 | 14.9% | 7.6% | 7/7 | **cheap; re-rated up** (see §3) |
| 21 | **ZTS** | Zoetis | Health Care | 72.2 | 72 | 73 | 12.7 | 11.8 | 9.7 | 9.95 | 64.9% | 6.3% | 5/7 | quality; D/E 294% |
| 22 | **VICI** | VICI Properties | Real Estate | 71.8 | 75 | 68 | 10.1 | 8.7 | 12.9 | 0.98 | 9.8% | 0.9% | 7/7 | cheap REIT (P/B ~1) |
| 23 | **LULU** | Lululemon | Cons Disc | 71.7 | 62 | 86 | 9.5 | 10.4 | 5.5 | 2.77 | 32.0% | 8.5% | 7/7 | cheap; growth-stall risk |
| 24 | **EXE** | Expand Energy | Energy | 71.6 | 57 | 94 | 8.4 | 11.0 | 3.7 | 1.17 | 14.9% | 6.3% | 5/7 | very cheap gas E&P |
| 25 | **AMP** | Ameriprise | Financials | 71.4 | 76 | 64 | 13.6 | 10.9 | — | 7.80 | 63.4% | 5.9% | 7/7 | quality asset-mgr |

Full 444-row scored table: `quant_us_ranked.csv`.

### Cheap-AND-quality vs cheap-but-trap-flag
- **Genuinely cheap AND quality (best of both):** **TROW, EOG, CF, DECK, HIG, CTSH** — high on
  *both* percentiles, clean balance sheets, 7/7 Piotroski, no artifact flags. TROW & EOG are the
  standouts (top-3, both axes >80).
- **Quality-tilted (great business, only fair price):** NEM, INCY, INTU, MU, CPRT, ZTS, AMP —
  top-decile quality, cheapness only mid-pack (P/E/EV-EBITDA above the cheap names).
- **Cheap-tilted (screen-cheap, watch the trap):** APA/OXY/COP/EXE (levered E&Ps — cheap on oil
  ~mid-cycle; APA D/E 49%, OXY 35%), CINF (**trailing P/E 8.1 but fwd P/E 19 — earnings expected
  to fall, a cheapness mirage**), LULU (cheap on growth-stall fears). All still PASS the trap gate
  (positive FCF, Piotroski ≥5/7) but their cheapness is cyclical/contested, not durable.
- **Artifact-flagged (do NOT trust the multiple shown):** SNDK & IT & MAS have negative or
  buyback-inflated P/B (book equity distorted) → the ranking already fell back to ROE/ROIC; INCY &
  SNDK show ROIC-proxy >100% (buyback artifact) → use ROE. These passed on other metrics but their
  P/B is meaningless.

---

## 2. Sector clustering (top 25 gated)

| Sector | # |
|---|--:|
| Financials | 5 (TROW, CINF, HIG, AMP, +ACGL/ALL just below) |
| Information Technology | 6 (FSLR, INTU, SNDK, IT, MU, CTSH) |
| Energy | 5 (EOG, APA, OXY, COP, EXE) |
| Materials | 2 (NEM, CF) |
| Health Care | 2 (INCY, ZTS) |
| Consumer Discretionary | 2 (DECK, LULU) |
| Industrials | 2 (MAS, CPRT) |
| Comm Services | 1 (TTD) |
| Real Estate | 1 (VICI) |

**Read:** the same three-way cluster as July — **Energy E&Ps + value-Financials + de-rated value-Tech**
still anchor the cheap-quality tail. Vs the July run, **Financials and Energy got MORE crowded** at
the top (insurers HIG/CINF/ALL/ACGL now screen very cheap on FCF/P-E; a broad energy cohort EOG/APA/
OXY/COP/EXE). "Info Tech" here is mostly *not* growth-AI — it's memory (MU, SNDK), IT-services (CTSH),
research (IT/Gartner), solar (FSLR), i.e. the cheap corners of tech.

---

## 3. Focus: are last run's US winners still cheap, or re-rated away?

Comparison is combined-score + key multiples, **2026-07-02 → 2026-08-26** (both yfinance).

| Ticker | Jul-02 score / P/E / EV-EBITDA | Aug-26 score / P/E / EV-EBITDA | Verdict |
|---|---|---|---|
| **INTU** | 80.4 / 16.3 / 11.4 | **76.2 / 20.8 / 15.3** | **RE-RATED UP** — P/E 16→21, EV/EBITDA 11→15; still quality (Q 84) but cheapness percentile fell 75→65. The AI-deflation discount from July has partly closed. Now quality-at-a-price, not deep value. |
| **CTSH** | 75.2 / 8.9 / 4.9 | **73.1 / 13.3 / 7.3** | **RE-RATED UP (materially)** — P/E 8.9→13.3, EV/EBITDA 4.9→7.3, P/B 1.3→1.9. Still cheap (C 89) but the deepest-value AI-services discount has compressed ~50%. Was the run's cheapest quality name; now merely cheap. |
| **EOG** | 79.5 / 12.6 / 5.8 | **83.4 / 11.3 / 5.5** | **STILL CHEAP — slightly cheaper**, score UP. P/E 12.6→11.3. Mid-cycle-oil thesis intact; remains a top-3 cheap-AND-quality name. |
| **TROW** | 85.7 / 12.5 / 7.8 | **83.4 / 11.3 / 7.6** | **STILL CHEAP** — essentially unchanged, P/E 12.5→11.3, fortress balance sheet (D/E 3.7%), 8.5% FCF yield. #2 overall. |

**Bottom line:** the two IT/software names (INTU, CTSH) that were the July "AI-deflation panic" deep-value
plays have **partially re-rated upward** — the fear-discount is closing, so they've moved from deep-value
toward fair. The two commodity/financial names (EOG, TROW) are **still cheap and still quality**, unchanged
to slightly cheaper. NEM stays #1 but is cheap-on-peak-gold (normalize — see LEARNINGS).

---

## 4. NEW names cheap now that weren't in July's US top-40

Ranked among the current top-25 gated:

- **OXY (#8, Energy)** — Occidental now screens cheap (EV/EBITDA 5.7, FCF yld 6.4%) as the energy
  cohort broadened; lower ROE (10.6%) and levered (D/E 35%), so cheap-tilted not quality-tilted.
- **CINF (#9, Financials)** — Cincinnati Financial, trailing P/E 8.1 / EV-EBITDA 5.8. **Caveat: fwd
  P/E is 19.1** — the market expects earnings to fall sharply, so the trailing cheapness is a mirage;
  classic P&C insurer with a big prior-year catastrophe/investment-gain base. Treat as cheap-but-watch.
- **TTD (#10, Comm Svcs)** — **The Trade Desk**, previously a high-multiple growth name, has de-rated
  into value range (P/E 15.6, EV-EBITDA 7.4, 9.5% FCF yield) with quality intact (7/7, net-cash-ish).
  Genuinely new cheap-quality entrant — worth a look.
- **SNDK (#12, Info Tech)** — **Sandisk**, the flash-memory business spun out of Western Digital
  (2026); fwd P/E 5.7 on the memory up-cycle, 91.6% ROE. Highest quality-percentile in the top-25 but
  P/B (16.1) is a spin-off/buyback artifact and it's a deep cyclical — cheapness percentile only 50.
- **IT (#14, Info Tech)** — **Gartner**, de-rated research franchise (P/E 17.4, EV-EBITDA 10.3, 8.6%
  FCF yld). NEGATIVE book (buybacks) → ignore P/B, use ROIC/FCF. Quality franchise now at a fair price.
- **MAS (#15, Industrials)** — **Masco**, housing-products; cheap on FCF (6.2%) but negative book
  equity (buybacks) → P/B meaningless. Housing-cyclical.
- **HIG (#18), COP (#19), ALL/ACGL (#26-27), BRK-B (#30)** — a broader **insurer + energy-major**
  cohort now clears into the gated top-30 that wasn't in July's US top-40. Insurers (HIG, ALL, ACGL,
  CINF) are the clearest new theme: cheap on P/E and very high cheapness percentiles (90s).

**Two-line summary of the shift since July:** (1) the AI-deflation value trade (INTU/CTSH) has partly
played out — those names re-rated up. (2) The fresh cheap-quality supply is in **insurers** (HIG, CINF,
ALL, ACGL), a **broader energy cohort** (add OXY, COP), and **de-rated former-growth names** (TTD, and the
spin-off SNDK). Energy + Financials are the crowded-cheap sectors right now.

---

## 5. Verification log

```
REFRESH RUN start 2026-08-26T18:02:09+00:00
US universe: 503 names. Pulling yfinance (refresh=True)...
  [25..500]/503 fetched
Wrote raw:    quant_us_raw.csv    (503 names)
Wrote ranked: quant_us_ranked.csv (444 rankable)
yfinance errors: 0  |  rankable: 444/503
as_of sample: 2026-08-26T18:02:09+00:00
REFRESH RUN end 2026-08-26T18:03:30+00:00  (82s)
```
- 503/503 pulled, **0 fetch errors**; 444 rankable, 355 pass trap gate.
- Data-quality guards fired as designed: **INCY & SNDK** ROIC-proxy>100% flagged→ROE used in rank;
  **IT & MAS** negative P/B (buyback book) — kept for display, P/B not trusted; EV/EBITDA<2 blanking
  active (none in top-25 tripped it except AMP whose EV/EBITDA came back NaN, correctly blank).
- No ADR/`.L`/currency-mix names in this US-only run, so those known traps don't apply here.

## Code run
Runner: `screens/refresh_2026-08/run_refresh_us.py` — imports `derive_metrics`,
`piotroski_lite`, `score_and_rank` from `screens/run_quant_screen.py` and `build_universe`
from `screens/universe.py` (US filter + `refresh=True`). No methodology changed; only live
prices and the US-only scope differ from the 2026-07-02 run.
