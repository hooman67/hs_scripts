# Stage 1a — Top-Down Sector Cheapness Screen

Run: 2026-07-01 by Claude (Opus 4.8). Owner: Hooman Shariati.
Scope: which SECTORS/INDUSTRIES are currently CHEAP across **US / Global / Emerging Markets**,
judged **primarily vs each sector's OWN 11-year history**, with a cross-section (vs-peers) and
a quality (ROIC/ROE) read layered on. Quality-first framing → each top cheap sector is tagged
**cyclical-cheap (opportunity)** vs **structurally-declining (trap)**.

> **Anti-hallucination:** every multiple, ROIC and ROE below is a real fetched value from
> Aswath Damodaran's NYU industry datasets (current + archived yearly files). Sources + as-of
> dates are given. No multiple or historical value is invented. Sector-outlook judgments cite
> live 2025-2026 web sources and are marked VERIFIED / ASSUMED / UNVERIFIED.

---

## TL;DR

- **I DID get real history.** Built an **11-year** per-industry series (data years 2015→2025,
  i.e. as-of **2016-01-05 → 2026-01-05**) for **EV/EBITDA and P/B across all three regions**,
  plus US P/E — from Damodaran's live + archived `.xls` files (72→77/77 files parsed).
- **Primary cheapness measure = percentile of the current multiple within the sector's own
  11-year history** (low percentile = cheap vs its own past). Composite = mean of available
  hist percentiles (EV/EBITDA, P/B, and US P/E). Secondary = cross-section percentile (vs the
  region's other industries) + a **cheap-vs-quality** read (low multiple paired with high ROIC).
- **Cheapest per region (own-history composite, lower = cheaper):**
  - **US:** Food Processing, Utility (Water), Information Services, Cable TV, Real Estate (Dev),
    Beverage (Alcoholic).
  - **Global:** Cable TV, Information Services, Food Processing, Education, Household Products,
    Beverage (Alcoholic).
  - **Emerging:** Transportation (Railroads), Shoe, Retail (Building Supply), Education,
    Insurance (Life), Retail (Automotive), Trucking.
- **Shortlist worth drilling into for quality leaders (cheap AND not structurally dying AND
  decent ROIC):** **Information Services, Beverage (Soft), Beverage (Alcoholic), Building
  Materials, Household Products** (developed); **EM Life Insurance, EM Railroads, EM Trucking/
  Auto retail** (emerging). **Avoid as traps: Cable TV, Food Processing, AI-exposed Education/
  pure data vendors.**

---

## Method (exactly what I did, and its limits)

**Data built (reproducible):**
- `screens/fetch_damodaran_history.py` → downloads Damodaran's **archived yearly** industry
  files from `https://pages.stern.nyu.edu/~adamodar/pc/archives/<stem><YY>.xls` (YY = 15..24)
  plus the current live file, for `vebitda*` (EV/EBITDA), `pbv*` (P/B, ROIC, ROE) in **US /
  Global / Emerging**, and `pedata` (US P/E). Output:
  `data/damodaran/history/damodaran_history_long.csv` (**15,685 rows**, 11 data years) +
  `damodaran_history_manifest.csv` (per-file fetch/parse audit log) + the raw `.xls` files.
- `screens/analyze_sector_cheapness.py` → computes the percentiles below. Output:
  `data/damodaran/history/sector_cheapness_{US,Global,Emerging}.csv` (full ranked tables).

**Archive naming gotcha (VERIFIED):** file `<stem><YY>` is stamped "Date updated:
20(YY+1)-01-05" — so `vebitda24` = as-of **2025-01-05**, and the live `vebitda.xls` = as-of
**2026-01-05** (the current snapshot). Every row is labelled by its true as-of date.

**Cheapness measures (per industry, "current" = as-of 2026-01-05):**
1. **`histpct_<metric>`** — percentile of the current multiple within that industry's own
   11-year history of positive values (0 = cheapest it's been, 100 = dearest). Requires ≥6
   positive-value years; negative multiples (loss-makers) excluded. **This is the primary,
   vs-own-history signal the brief asked for.**
2. **`hist_cheap_composite`** — mean of available hist percentiles (EV/EBITDA + P/B + US P/E).
   Lower = cheaper vs its own past.
3. **`xsecpct_EV/EBITDA`** — percentile of the current EV/EBITDA within the region's
   cross-section of industries this year (low = cheap vs peers). Relative-not-historical.
4. **Quality:** current **ROIC** and **ROE** (Damodaran `pbv*` files, as-of 2026-01-05) — used
   to separate *cheap-and-profitable* (interesting) from *cheap-and-low-return* (trap risk).

**Honest limits:**
- Damodaran ratios are **annual, simple industry averages** (not cap-weighted), a snapshot ~6
  months stale (as-of 2026-01-05) → good for **relative sector cheapness/quality**, NOT for a
  live price. Pair with live company multiples in Stage 3.
- History is **11 years** (2015→2025). Covers the 2020 COVID shock and 2021-22 rate cycle but
  not e.g. 2008-09 — so a "cheapest in 11 years" is not "cheapest ever."
- A handful of industries have <11 years due to Damodaran renames (e.g. Retail (Online) 8 yrs)
  or typos in his own header cells ("Induistry Name", handled). Percentiles shown only where
  ≥6 years exist; `n_hist_signals` in the CSVs flags how many metrics backed each composite.
- **P/E is US-only** on Damodaran (no Global/EM PE file). For Global/EM, cheapness rests on
  **EV/EBITDA + P/B** (paired with ROIC/ROE), per the brief.

---

## US — cheapest industries vs own 11-year history

Source for all numbers: Damodaran `pedata.xls`, `pbvdata.xls`, `vebitda.xls` (current, as-of
**2026-01-05**) + archived `...15..24.xls` for history. `hist %` = percentile within the
industry's own 2015-2025 history (low = cheap). Full table: `sector_cheapness_US.csv`.

| Industry | comp. (own-hist, low=cheap) | EV/EBITDA (hist%, 11yr median) | P/B (hist%) | Curr P/E (hist%) | ROIC | ROE | vs-peers (xsec EV/EBITDA %) |
|---|--:|--|--:|--|--:|--:|--:|
| **Food Processing** | 11 | 10.0 (5%, med 12.9) | 1.8 (5%) | 31.0 (23%) | 15.9% | 4.6% | 25 |
| **Utility (Water)** | 14 | 14.1 (23%, med 15.8) | 2.0 (5%) | 22.0 (14%) | 7.3% | 10.3% | 58 |
| **Information Services** | 14 | 11.5 (5%, med 18.4) | 3.8 (14%) | 29.3 (23%) | **22.2%** | 14.9% | 40 |
| **Cable TV** | 17 | 6.2 (5%, med 9.3) | 1.3 (5%) | 13.7 (41%) | 12.1% | 11.1% | **2** |
| **Real Estate (Development)** | 17 | 10.2 (5%, med 26.1) | 1.0 (14%) | 29.4 (32%) | 7.0% | 5.1% | 26 |
| **Beverage (Alcoholic)** | 17 | 8.6 (5%, med 16.3) | 1.9 (5%) | 35.0 (41%) | 15.7% | 0.6% | 16 |
| **Beverage (Soft)** | 23 | 16.9 (32%, med 18.1) | 6.9 (5%) | 37.1 (32%) | **29.0%** | **30.9%** | 73 |
| **Building Materials** | 23 | 11.6 (41%, med 12.0) | 3.6 (23%) | 21.1 (5%) | **20.2%** | 16.0% | 44 |
| Telecom. Services | 26 | 6.5 (23%, med 6.8) | 1.6 (41%) | 26.5 (14%) | 12.0% | 15.4% | **4** |
| Insurance (Prop/Cas.) | 29 | 8.4 (14%, med 10.2) | 2.0 (68%) | — (5%) | — | — | 12 |

Read: **Food Processing, Information Services, Beverage (Alcoholic), Cable TV, RE-Development**
are near the bottom of their own 11-year multiple ranges. **Cable TV & Telecom** are also cheap
vs *peers* (xsec 2-4). **Information Services (22% ROIC), Beverage Soft (29%), Building
Materials (20%)** are the *cheap-yet-high-return* names — the quality-first sweet spot. Beverage
Soft is dear vs peers (xsec 73) but at the *low end of its own rich history* — a "great business
on sale," not an absolute-cheap.

---

## Global — cheapest industries vs own 11-year history

Source: Damodaran `vebitdaGlobal.xls`, `pbvGlobal.xls` (current 2026-01-05) + archives. No
Global P/E table exists (US-only) → composite uses EV/EBITDA + P/B only (`n_hist_signals`=2).
Full table: `sector_cheapness_Global.csv`.

| Industry | comp. (own-hist) | EV/EBITDA (hist%, median) | P/B (hist%) | ROIC | ROE | vs-peers (xsec %) |
|---|--:|--|--:|--:|--:|--:|
| **Cable TV** | 5 | 6.6 (5%, med 9.7) | 1.4 (5%) | 11.1% | 8.1% | **3** |
| **Information Services** | 9 | 10.8 (5%, med 18.2) | 3.3 (14%) | **22.8%** | 14.5% | 34 |
| **Food Processing** | 14 | 11.1 (14%, med 13.0) | 2.2 (14%) | 12.0% | 10.5% | 38 |
| **Education** | 14 | 9.0 (14%, med 11.2) | 1.9 (14%) | 14.4% | 12.3% | 16 |
| **Household Products** | 14 | 14.6 (23%, med 16.1) | 4.6 (5%) | **23.1%** | 18.0% | 68 |
| **Beverage (Alcoholic)** | 14 | 12.2 (14%, med 14.4) | 2.8 (14%) | 15.4% | 13.7% | 49 |
| Utility (Water) | 18 | 11.9 (23%, med 12.7) | 1.5 (14%) | 6.5% | 9.8% | 47 |
| R.E.I.T. | 18 | 19.7 (5%, med 21.0) | 1.5 (32%) | 3.7% | 5.3% | 88 |
| Beverage (Soft) | 23 | 16.0 (23%, med 16.1) | 5.8 (5%) | **29.6%** | 30.9% | 75 |
| Transportation (Railroads) | 27 | 10.9 (50%, med 10.9) | 1.9 (5%) | 13.2% | 11.0% | 36 |

Read: the developed-world picture rhymes with the US — **Cable TV cheapest** (and cheap vs
peers), **Information Services** cheap-with-22.8%-ROIC, staples (**Food Processing, Household
Products, Beverages**) at the low end of their own ranges. **Household Products (23% ROIC) &
Beverage Soft (29.6%)** are the high-quality-on-sale names globally.

---

## Emerging Markets — cheapest industries vs own 11-year history

Source: Damodaran `vebitdaemerg.xls`, `pbvemerg.xls` (current 2026-01-05) + archives. No EM
P/E table → composite = EV/EBITDA + P/B. Full table: `sector_cheapness_Emerging.csv`.

| Industry | comp. (own-hist) | EV/EBITDA (hist%, median) | P/B (hist%) | ROIC | ROE | vs-peers (xsec %) |
|---|--:|--|--:|--:|--:|--:|
| **Transportation (Railroads)** | 5 | 8.2 (5%, med 12.1) | 0.9 (5%) | 6.8% | 6.9% | 11 |
| **Shoe** | 9 | 9.0 (14%, med 11.7) | 1.4 (5%) | 9.6% | 10.8% | 15 |
| **Retail (Building Supply)** | 9 | 9.6 (14%, med 14.2) | 2.2 (5%) | 13.9% | 4.5% | 21 |
| **Education** | 14 | 8.4 (14%, med 12.6) | 1.5 (14%) | 13.0% | 10.4% | 13 |
| Office Equipment & Services | 14 | 16.6 (23%, med 19.1) | 2.2 (5%) | 7.4% | 6.6% | 74 |
| **Retail (Automotive)** | 18 | 9.0 (23%, med 10.4) | 1.4 (14%) | 9.6% | 3.7% | 16 |
| **Trucking** | 18 | 7.3 (14%, med 9.5) | 1.6 (23%) | 8.9% | 3.6% | **7** |
| **Insurance (Life)** | 18 | 7.3 (5%, med 10.5) | 1.4 (32%) | **15.1%** | **17.6%** | **6** |
| Food Wholesalers | 18 | 9.7 (5%, med 12.6) | 1.4 (32%) | 10.4% | 10.2% | 22 |
| Food Processing | 18 | 11.1 (14%, med 12.5) | 2.1 (23%) | 10.9% | 10.8% | 35 |

Read: EM's cheapest cluster is **transport & logistics (Railroads, Trucking) + consumer retail
(Auto, Building Supply, Shoe) + Life Insurance**. **Insurance (Life)** stands out — cheap vs
own history AND vs peers (xsec 6) AND the highest-quality of the cheap EM group (ROIC 15%, ROE
17.6%). EM Railroads is the single cheapest EM industry but low-return (ROIC 6.8%).

---

## Cyclical-cheap (opportunity) vs structurally-declining (trap) — per top cheap sector

Verdicts from live 2025-2026 web sources (subagent research, citations below). Confidence marks
apply to the *outlook judgment*; the multiples above are all VERIFIED Damodaran pulls.

| Sector (regions) | Verdict | Why (cited) | Conf. |
|---|---|---|---|
| **Cable TV** (US, Global) | **SECULAR — trap** | S&P Global: linear cable "formally entered the decline stage of its life cycle," subs peaked 2012, "long slow bleedout, no comeback"; basic cable -7.1% subs in 2024. Cord-cutting is permanent. [Fortune/S&P 2025-12-29] | VERIFIED |
| **Food Processing** (US, Global) | **SECULAR-lean — mostly trap** | Volumes still pressured after pricing normalized; structural drivers: GLP-1 adoption, MAHA/FDA ultra-processed-food crackdown (def. due Apr 2026), sticky private label. Cheap names (e.g. Conagra) show trap traits (falling FCF, rising leverage). [Circana 2026; Bloomberg/Bernstein 2026-06-05] | VERIFIED |
| **Information Services** (US, Global) | **MIXED — mostly cyclical/sentiment** | AI-substitution fear is repricing pure data/analytics (Morningstar cut FactSet/SS&C moats), but ratings franchises (S&P Global, Moody's) still guide double-digit 2026 EPS. Cheapness = AI overhang on protected 22%-ROIC names. Segment-select. [Forbes 2026-06-08; Morningstar] | VERIFIED (verdict split by sub-segment) |
| **Beverage (Alcoholic)** (US, Global) | **CYCLICAL trough — not a trap** (wine = structural exception) | IWSR: 2025 volumes -2% driven by *reversible* factors (destocking, weak on-trade, China luxury clampdown, cognac, tariffs cut to 15% Jul-2025); IWSR/Diageo call it "more cyclical than structural." Slow secular undertow (US drinking rate at record-low 54%). US ROE at 0.6% = trough earnings, not dead demand. [IWSR 2025-10-02; Gallup 2025-08-13] | VERIFIED |
| **Beverage (Soft)** (US, Global) | **Mostly CYCLICAL — not a trap** | Coca-Cola +5% organic rev / +4% price-mix FY2025, guides 4-5% 2026 → intact pricing power + EM growth. Real but managed secular headwinds (GLP-1 ~7% soft-drink drop, MAHA dye removal). 29% ROIC, on sale vs own history. [Nasdaq KO 2026-02-10; AlixPartners 2025-02-05] | VERIFIED |
| **Building Materials** (US) | **CYCLICAL — opportunity** | Rate/housing-driven softness with a public-infra floor; Vulcan guides +1-3% aggregates volume 2026, total US construction +~4% to $1.26T (IIJA/CHIPS). 20% ROIC. [Vulcan Q4 FY2025 2026-02-17; Fitch 2025-10-12] | VERIFIED |
| **Household Products** (Global) | **CYCLICAL — not a trap** | Weak-consumer + tariff/input cost squeeze, but brands keep pricing power (P&G FY25 +2% organic, +4% core EPS, ~23% ROIC). Fidelity calls headwind duration "overstated." Modest structural private-label drag (21.3% share) caps upside. [eMarketer 2026-01-21; Fidelity 2026-01-07] | VERIFIED |
| **Telecom Services** (US) | **SECULAR-lean — not "dying"** | Fitch 2026 US telecom outlook "neutral": low-single-digit growth, saturation, price war; but AT&T fiber (+11.5% connections) / FWA (+51.6% rev) momentum offsets. Structurally slow, cheap vs peers (xsec 4). [Fitch 2025-09-12; Morningstar 2025-06-25] | VERIFIED (neutral read); ASSUMED (price-war detail) |
| **EM Transportation/Railroads** | **CYCLICAL — opportunity** | Cheapness tracks broad-EM trade/tariff discount; rail volumes + infra spend growing (China rail freight +~3% H1-2025; India rail capex +10.5% to ₹2.93tn FY26-27). Low 6.8% ROIC = watch quality. [China gov 2025-07-20; India budget ~2026-02-01] | VERIFIED (volumes); ASSUMED (EM-rail equity valuation inferred from broad-EM discount) |
| **EM Trucking + Retail (Auto)** | **CYCLICAL — opportunity** | Normalizing freight/dealer-margin down-cycle + EM FX/rate pressure; EM vehicle penetration structurally low (India 44 cars/1,000). Structural risk = Chinese-automaker export share-shift. [Moody's 2025-05-27; ACT 2026-06-29] | VERIFIED |
| **EM Insurance (Life)** | **CYCLICAL — opportunity** | Temporary low-rate/spread squeeze on a strong secular growth runway (Swiss Re: global life premiums +~3%/yr 2025-26, 2x last decade; APAC life to $1.6T by 2029, 7.3% CAGR). Moody's sees China premium growth rebounding to 15-20% in 2026. Best quality of cheap EM (15% ROIC, 17.6% ROE). [Swiss Re sigma; GlobalData 2025; Moody's 2025-06] | VERIFIED (via trade press; primaries paywalled) |
| **Education** (Global, EM) | **MIXED — split** | CYCLICAL for regulated EM tutoring survivors (New Oriental FY25 rev +13.6% to $4.9B post China "double-reduction" shock); SECULAR trap for AI-exposed edtech (Chegg collapsed ~$14.7B→~0, cut 45% of staff Oct-2025). Stock-pick within. [New Oriental 2025-07; CNBC 2025-10-27] | VERIFIED (TAL specifics = ASSUMED) |

---

## Shortlist — cheap sectors worth drilling into for quality leaders (feeds Stage 3)

Ranked by **(cheap vs own history) AND (not structurally dying) AND (respectable ROIC)**:

**Developed (US / Global):**
1. **Information Services** — cheap vs own history (US EV/EBITDA 5th pctile), **ROIC ~22%**;
   cyclicality is AI *sentiment*, and the ratings/index franchises (S&P Global, Moody's, MSCI)
   are moaty. Pick the protected sub-segment, avoid pure AI-exposed data vendors.
2. **Beverage (Alcoholic)** — 5th-pctile EV/EBITDA vs own 11yr, ROE at a 0.6% *trough*
   (destocking/tariff cycle, called cyclical by IWSR/Diageo) → mean-reversion candidate. Hunt
   for balance-sheet-strong spirits/beer leaders; avoid wine-heavy names (structural).
3. **Beverage (Soft)** — **29% ROIC**, P/B at the bottom of its own range; a quality compounder
   on relative sale. Dear vs peers, so it's a "great business at a fair-ish price," not deep value.
4. **Building Materials** — **20% ROIC**, cyclical housing trough with an infrastructure floor
   and 2026 volume growth guided. Classic cyclical-cheap opportunity.
5. **Household Products (Global)** — **23% ROIC**, staples on a cyclical cost/consumer squeeze
   with intact pricing power. Watch private-label drag; buy the pricing-power leaders.

**Emerging:**
6. **Insurance (Life, EM)** — best risk/reward in cheap EM: cheap vs own history AND vs peers,
   **ROIC 15% / ROE 17.6%**, strong secular premium-growth runway, cyclical rate headwind
   reversing.
7. **EM Railroads / Trucking / Retail (Automotive)** — cheapest EM cluster, cyclical (trade,
   freight, dealer-margin normalization) with structurally-low vehicle penetration tailwind.
   Lower ROIC (7-10%) → be selective on quality; screen hard for the leaders.

**Explicitly do NOT drill (value traps / secular decline):**
- **Cable TV** (US + Global) — cheapest of all but a confirmed secular bleedout.
- **Food Processing** — GLP-1 + MAHA + private-label structural pressure; cheap for a reason.
- **AI-exposed Education (Chegg-type) & pure data vendors** — secular substitution risk.
- Low-return cheap-but-mediocre: **RE Development, Utility (Water), R.E.I.T.** (ROIC 3-7%,
  cheap partly because returns are structurally thin) — not quality-first candidates.

---

## Method & limitations (summary)

- **Cheapness measure used:** primary = **percentile of current multiple within the sector's own
  11-year (2015-2025) history** (EV/EBITDA + P/B, + US P/E); composite averages the available
  ones. Secondary = **cross-section percentile** (vs region peers) and **cheap-vs-quality**
  (multiple paired with ROIC/ROE). I *did* obtain real history (Damodaran archives, 11 years,
  all 3 regions) — this is a genuine vs-own-history read, not a relative-only fallback.
- **Why 11 years / why these metrics:** archives verified reachable back to file `15` (as-of
  2016-01-05); older files exist but change layout — 11 years already spans COVID + the rate
  cycle. EV/EBITDA & P/B chosen because they have full US/Global/EM coverage; P/E is US-only.
- **Could NOT obtain:** pre-2015 Damodaran industry archives at the same URL pattern (would
  need a different probe); a live/cap-weighted sector multiple (Damodaran is annual, simple-avg,
  as-of 2026-01-05 — ~6 months stale). Mitigation: Stage 3 pairs these with live company
  multiples via `fetch_fundamentals.py`.
- **Confidence:** all multiples/ROIC/ROE = VERIFIED (real fetched Damodaran values, cited).
  Cyclical-vs-secular verdicts = VERIFIED/ASSUMED as marked, from cited 2025-2026 web sources.

**Reproduce:**
```
/opt/venv/bin/python3 screens/fetch_damodaran_history.py            # build 11yr history
/opt/venv/bin/python3 screens/analyze_sector_cheapness.py           # rank + write per-region CSVs
```
Data: `data/damodaran/history/{damodaran_history_long.csv, sector_cheapness_{US,Global,Emerging}.csv, damodaran_history_manifest.csv}` + raw `.xls` archives.
