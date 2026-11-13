# Stage 1b — Cheap × Secular-Trend Cross-Sector Matrix

Run: 2026-07-04 by Claude (Opus 4.8). Owner: Hooman Shariati (Canadian citizen, quality-first, global).
**RESEARCH, not financial advice.** Crosses the **CHEAPNESS axis** (from `screens/sector_cheapness.md`
Stage-1a — Damodaran 11-yr own-history percentiles + ROIC/ROE, as-of **2026-01-05**) against a **TREND
axis** of major durable secular tailwinds (web-cited, 2025-2026 as-of dates), and classifies every notable
sector into: **SWEET SPOT** (cheap + tailwind + decent quality) / **Expensive-but-trendy** / **Cheap-but-
declining (trap)** / **Cheap, no strong trend (ordinary value)**.

> **Anti-hallucination (CLAUDE.md §5, #1):** cheapness/quality columns are REAL Damodaran fetched values
> (`data/damodaran/history/sector_cheapness_{US,Global,Emerging}.csv`, as-of **2026-01-05**) — reused from
> Stage-1a, not recomputed. Trend claims are web-cited with 2025-2026 as-of dates and marked
> **VERIFIED / ASSUMED / UNVERIFIED**. Where a "trend" is hype with no earnings, I say so.
> `hist% =` percentile of the current multiple within that sector's own 2015-2025 history (low = cheap vs
> its own past); `xsec% =` percentile vs region peers this year (low = cheap vs peers).

---

## TL;DR — the bottom line first

The single most important finding: **almost every "exciting" AI/electrification/reshoring/defense trend
is ALREADY EXPENSIVE.** In Damodaran's own-history percentiles, Electrical Equipment, Machinery,
Semiconductors, Semi-Cap-Equipment, Aerospace/Defense, Metals & Mining and Precious Metals sit at the
**80th–95th+ percentile of their own 11-year valuation ranges** across all three regions. The market has
paid up for the good stories. **The value is in the trends nobody wants to pay for.**

**The 3–5 genuine SWEET SPOTS (cheap + durable tailwind + decent quality):**

1. **Oil & Gas — Exploration & Production / Integrated (Global + US + EM).** The cheapest thing on the
   whole board relative to *both* its own history *and* peers. US E&P **EV/EBITDA 5.1× (31st pctile own
   hist), ROIC 13.7%, xsec 0.5** (literally the cheapest cross-section slot); Global E&P **4.8× (32nd
   pctile), ROIC 14.9%**; EM Integrated **6.5×, ROIC 20.0%, xsec 1.6**. Trend = the *supply-side*
   underinvestment thesis (global upstream capex −4% in 2025 to <$570B vs the ~$738B/yr the IEA/IEF say is
   needed by 2030) + capital discipline + shale plateau + a contracted-and-durable US LNG buildout.
   VERIFIED. **This is the "uniquely investable now" answer.** Caveat: a 2026-27 supply glut (IEA sees
   ~4 mb/d surplus in 2026) can make it early/painful. → maps to our finalists **CNOOC / EOG.**

2. **EM Life Insurance (+ P&C / Reinsurance broadly).** EM Life **EV/EBITDA 7.3× (5th pctile own hist),
   ROIC 15.1%, ROE 17.6%, xsec 6** — the best-quality name in cheap EM. Global/US P&C Insurance cheap on
   EV/EBITDA with **17–19% ROIC**. Trend = rates-*normalized* (Fed 3.50-3.75%, ECB re-hiking) lifting
   investment income + **aging-demographics / Asia protection-gap** premium growth (US annuities 4th
   straight record $464B FY2025; Asia protection gap $390B; China life +5.6% real 2026). VERIFIED. Caveat:
   the P&C/reinsurance *pricing* cycle is clearly softening (Jan-2026 property-cat reinsurance −12 to
   −15%), so favor the demographics-driven **life** leg over the cyclical P&C leg. → maps to finalist
   **CPIC (China Pacific Insurance) / EM life.**

3. **Building Materials — US (aggregates/cement), and CRH/Eagle Materials as the *reasonably-priced*
   expression.** US Building Materials **EV/EBITDA 11.6× (41st pctile own hist), ROIC 20.2%, US P/E at the
   5th pctile** — a genuine cyclical-cheap, high-ROIC name. Trend = reshoring + IIJA/infrastructure floor
   (US construction ~$1.26T, IIJA $568B/47% allocated). VERIFIED. **Important nuance from the research:**
   the *premium aggregate* names (Vulcan/Martin Marietta) are NOT cheap (near decade-high multiples); the
   reasonably-valued expressions are **CRH (~12× EV/EBITDA) and Eagle Materials (~11×)**. → maps to
   finalist **Buzzi (cement / reshoring-infra building materials).**

4. **Information Services (US + Global) — the AI *sentiment* discount on moaty franchises.** US **EV/EBITDA
   11.5× (5th pctile own hist), ROIC 22.2%**; Global **10.8× (5th pctile), ROIC 22.8%.** Trend = AI is a
   *split* — a headwind for pure data/analytics vendors, but the ratings/index franchises (S&P Global,
   Moody's, MSCI) are protected and the cheapness is AI *overhang*, not realized damage. Segment-select.
   → connects to our AI-deflation theme (`theme_ai_deflation.md`): the "AI victim vs beneficiary" split.

**Honorable mention (cheap + real-but-slower trend):** **European banks** — re-rated hard (+48% trailing
52wk) but still only ~9× fwd P/E, discount justified by lower ROE not mispricing; rates-normalization leg
is durable but the easy re-rating is largely done.

**Expensive-but-trendy — do NOT overpay (watchlist only):** Aerospace/**Defense** (esp. European
pure-plays like Rheinmetall — ran +150-190% then rolled over; US primes LMT/NOC less stretched),
**Electrical Equipment** (GE Vernova ~+700%, ~40-45× fwd), **Semiconductors / Semi-Cap-Equipment**,
**Machinery** (CAT ~48× trailing), **Independent Power (Constellation/Vistra)**, **Uranium miners**
(Cameco trailing P/E ~92), **Precious Metals**, premium aggregates (Vulcan/Martin Marietta). Great trends,
no value.

**Cheap-but-the-trend-is-AGAINST-it — TRAPS:** **Cable TV** (secular cord-cut bleedout — cheapest of all,
for a reason), **Food Processing** (GLP-1 + MAHA + private-label), **IT Services / pure data vendors**
(the AI-deflation VICTIM side — cheap because the billable-hour unit is under attack → **CTSH/TCS**),
**AI-exposed Education / edtech** (Chegg-type substitution). Cheap ≠ safe.

---

## The Matrix

**Cheapness/ROIC/ROE = real Damodaran (as-of 2026-01-05).** `comp` = own-history composite percentile
(lower = cheaper); `hist%` on EV/EBITDA; `xsec%` = vs-peers. Classification is the cross of cheapness ×
trend-direction.

### AI + Electrification + Reshoring + Defense trends (the "exciting" ones — mostly EXPENSIVE)

| Sector (region) | comp (own-hist) | EV/EBITDA hist% (curr) | P/B / P/E hist% | ROIC | ROE | xsec% | Relevant trend | Tail/Head | Classification |
|---|--:|--|--|--:|--:|--:|---|---|---|
| **Aerospace/Defense** (US) | 92 | 95% (21.6×) | P/B 95% / PE 86% | 16.0% | 15.3% | 86 | Defense rearmament | **Tailwind** | **Expensive-but-trendy** |
| Aerospace/Defense (Global) | 95 | 95% (22.4×) | P/B 95% | 15.5% | 18.4% | 93 | Defense rearmament | Tailwind | **Expensive-but-trendy** |
| **Electrical Equipment** (US) | 89 | 95% (24.6×) | P/B 95% / PE 77% | 15.6% | 1.5% | 91 | Electrification/grid | Tailwind | **Expensive-but-trendy** |
| Electrical Equipment (Global) | 91 | 86% (20.9×) | P/B 95% | 11.4% | 9.6% | 90 | Electrification/grid | Tailwind | **Expensive-but-trendy** |
| **Machinery** (US) | 65 | 77% (16.2×) | P/B 77% / PE 41% | 24.4% | 16.4% | 68 | Reshoring/automation | Tailwind | **Expensive-but-trendy** (mid-range; not cheap) |
| **Semiconductor** (US) | 74 | 95% (34.8×) | P/B 95% / PE 32% | 27.2% | 31.4% | 96 | AI compute | Tailwind | **Expensive-but-trendy** |
| **Semiconductor Equip** (US) | 80 | 95% (24.7×) | P/B 86% / PE 59% | 28.4% | 35.8% | 92 | AI capex / semis-cap | Tailwind | **Expensive-but-trendy** |
| **Metals & Mining** (US) | 89 | 77% (11.4×) | P/B 95% / PE 95% | 27.0% | 17.8% | 37 | Copper/electrification | Tailwind (LT) | **Expensive-but-trendy** |
| **Precious Metals** (US) | 83 | 68% (10.7×) | P/B 95% / PE 86% | 25.5% | 23.5% | 32 | Gold/safe-haven | Tailwind | **Expensive-but-trendy** |
| **Power** (US) | 68 | 86% (12.4×) | P/B 95% / PE 23% | 6.9% | 12.4% | 46 | Datacenter power / IPPs | Tailwind | **Expensive-but-trendy** (low ROIC) |
| Power (Global) | 86 | 77% (10.1×) | P/B 95% | 7.0% | 10.3% | 25 | Datacenter power | Tailwind | **Expensive-but-trendy** |
| **Green & Renewable Energy** (US) | 50 | 50% (13.4×) | P/B 68% / PE 32% | 3.6% | -7.4% | 51 | Energy transition | Tail, but IRA-gutted | **Mid + weakened trend** (neg ROE; OBBBA repealed credits) |
| **Coal & Related Energy** (US) | 80 | 95% (10.4×) | P/B 68% / PE 77% | -4.8% | -2.5% | 29 | (mixed) | Head (LT) | Expensive + neg return |
| **Utility (General)** (US) | 44 | 68% (13.7×) | P/B 14% / PE 50% | 6.0% | 10.4% | 55 | Power-demand growth | Tailwind | **Mid-range + tailwind** (low ROIC; regulated) |
| **Engineering/Construction** (US) | 95 | 95% (17.2×) | P/B 95% / PE 95% | 25.3% | 26.1% | 75 | Reshoring/infra capex | Tailwind, but growth fading | **Expensive-but-trendy** (peaked; −30% from mfg-constr peak) |

### Energy, Financials, Materials, Staples, Comms (the CHEAP-and/or-trend-supported ones)

| Sector (region) | comp | EV/EBITDA hist% (curr) | P/B / P/E hist% | ROIC | ROE | xsec% | Relevant trend | Tail/Head | Classification |
|---|--:|--|--|--:|--:|--:|---|---|---|
| **Oil/Gas E&P** (US) | **35** | 32% (5.1×) | P/B 41% / PE 32% | **13.7%** | 12.2% | **0.5** | Upstream underinvest. + LNG | **Tailwind (supply-side)** | **★ SWEET SPOT** |
| **Oil/Gas E&P** (Global) | 36 | 32% (4.8×) | P/B 41% | **14.9%** | 11.8% | **0.5** | Underinvestment + LNG | Tailwind | **★ SWEET SPOT** |
| **Oil/Gas (Integrated)** (EM) | 50 | 50% (6.5×) | P/B 50% | **20.0%** | 15.9% | **1.6** | Underinvestment | Tailwind | **★ SWEET SPOT** (EM integrated; CNOOC) |
| Oil/Gas (Integrated) (Global) | 50 | 41% (6.2×) | P/B 59% | 13.9% | 12.2% | 1.6 | Underinvestment | Tailwind | Cheap + tailwind (majors 7-12× fwd) |
| Oilfield Svcs/Equip. (US) | 56 | 59% (8.6×) | P/B 68% | 11.9% | 8.6% | 17 | Upstream capex | Tail (if capex turns) | Cheap-ish, capex-dependent |
| Oil/Gas Distribution (US) | 44 | 32% (11.6×) | P/B 86% / PE 14% | 12.4% | 18.0% | 41 | LNG / gas infra | Tailwind | Cheap-ish + LNG midstream |
| **Insurance (Life)** (EM) | **18** | **5% (7.3×)** | P/B 32% | **15.1%** | **17.6%** | **6** | Aging / Asia protection gap + rates | **Tailwind** | **★ SWEET SPOT** |
| Insurance (Life) (Global) | 68 | 41% (7.3×) | P/B 95% | 14.5% | 14.1% | 6 | Aging + rates | Tailwind | Cheap vs peers (xsec 6), mid own-hist |
| **Insurance (Prop/Cas.)** (US) | 29 | 14% (8.4×) | P/B 68% / PE 5% | **18.5%** | **18.7%** | 12 | Rates + hard market (softening) | Tail turning to Head | Cheap + quality, but cycle softening |
| Insurance (Prop/Cas.) (Global) | 50 | 14% (7.8×) | P/B 86% | **18.1%** | 17.2% | 8 | Rates | Tail softening | Cheap + quality; watch cycle |
| Reinsurance (Global) | 55 | 14% (7.9×) | P/B 95% | **17.5%** | 15.6% | 9 | Rate cycle | **Head (−12-15% Jan-26)** | Cheap-ish but cycle turned down |
| Insurance (General) (Global) | 77 | 59% (9.0×) | P/B 95% | **25.6%** | 18.5% | 18 | Rates/underwriting | Tail softening | Higher-quality but not cheap own-hist |
| Banks (Regional) (US) | 59 | — | P/B 32% / PE 86% | — | 9.8% | — | Rates normalization | Tailwind | Mid; rates help NIM |
| Bank (Money Center) (Global) | 95 | — | P/B 95% | — | 11.5% | — | Rates normalization | Tailwind | Re-rated (Euro banks +48%); not cheap own-hist |
| **Building Materials** (US) | **23** | 41% (11.6×) | P/B 23% / **PE 5%** | **20.2%** | 16.0% | 44 | Reshoring/infra floor | **Tailwind** | **★ SWEET SPOT** |
| Building Materials (Global) | 73 | 77% (12.4×) | P/B 68% | 14.2% | 12.0% | 52 | Infra | Tailwind | Not cheap own-hist |
| Construction Supplies (US) | 74 | 95% (16.8×) | P/B 95% / PE 32% | 16.7% | 22.9% | 70 | Infra | Tailwind | Expensive-but-trendy |
| **Information Services** (US) | **14** | **5% (11.5×)** | P/B 14% / PE 23% | **22.2%** | 14.9% | 40 | AI (split: victim vs protected) | Mixed | **★ SWEET SPOT (segment-select)** |
| **Information Services** (Global) | **9** | **5% (10.8×)** | P/B 14% | **22.8%** | 14.5% | 34 | AI (split) | Mixed | **★ SWEET SPOT (segment-select)** |
| Computer Services (US) | 59 | 86% (14.1×) | P/B 77% / PE 14% | 26.3% | 18.3% | 57 | AI (victim: IT services) | **Headwind** | Not cheap own-hist; AI-victim risk |

### Cheap-but-the-trend-is-AGAINST-it (TRAPS) and Cheap-no-trend (ordinary value)

| Sector (region) | comp | EV/EBITDA hist% (curr) | ROIC | ROE | Relevant trend | Tail/Head | Classification |
|---|--:|--|--:|--:|---|---|---|
| **Cable TV** (US/Global) | 5-17 | 5% (6.2-6.6×) | 11-12% | 8-11% | Cord-cutting / streaming | **HEADWIND (secular)** | **TRAP** |
| **Food Processing** (US) | 11 | 5% (10.0×) | 15.9% | 4.6% | GLP-1 + MAHA + private label | **HEADWIND** | **TRAP** |
| **IT / Computer Services** (Global) | 68 | 68% (14.6×) | 21.0% | 17.1% | AI-deflation (billable-hour) | **HEADWIND** | **TRAP-risk → CTSH/TCS** |
| **Education / edtech** (Global/EM) | 14 | 14% | 13-14% | 10-12% | AI substitution (edtech) | **HEADWIND (edtech leg)** | Split: TRAP (edtech) / value (regulated tutoring) |
| Beverage (Alcoholic) (US/Global) | 14-17 | 5% (8.6×) | 15.7% | 0.6% | (cyclical trough) | Neutral/slow-head | **Cheap, no strong trend** (cyclical mean-reversion) |
| Real Estate (Development) (US) | 17 | 5% (10.2×) | 7.0% | 5.1% | (rates) | Neutral | Cheap, low-return (ordinary/trap-ish) |
| Utility (Water) (US/Global) | 14-18 | 22% (14.1×) | 6.5-7.3% | 9.8-10.3% | (none material) | Neutral | Cheap, low-return; **not** the power-demand play |
| EM Railroads / Trucking / Auto retail | 5-18 | 4-14% | 7-10% | 4-7% | EM logistics / low vehicle penetration | Mild tailwind | Cheap; lower quality — selective |

---

## Per SWEET-SPOT sector: why cheap · which trend · durability · caveat

### 1. Oil & Gas — E&P / Integrated (the clearest cheap × durable-tailwind × quality)
- **Why cheap:** the single cheapest cluster on the board vs *both* own history and peers. US E&P
  **EV/EBITDA 5.1× (31st pctile own 11-yr hist), P/B 41st pctile, ROIC 13.7%, xsec 0.5** (rock-bottom
  cross-section); Global E&P **4.8× (32nd pctile), ROIC 14.9%, xsec 0.5**; EM Integrated **6.5×, ROIC
  20.0%, xsec 1.6.** Majors trade **7-12× fwd P/E vs a ~32× S&P 500** and energy is only ~3% of the S&P
  (near multi-decade low weight). [Damodaran 2026-01-05; multpl.com/StockAnalysis 2026-07-02] VERIFIED.
- **The trend (durable, supply-side):** global upstream O&G investment *fell* ~4% in 2025 to <$570B
  (upstream oil −6% to ~$420B — first decline since 2020), against the **$738B/yr the IEF/S&P say is
  needed by 2030** ($4.3T cumulative). Majors now return 30-50% of cash flow to shareholders rather than
  drill; WoodMac warns of ~40% production decline 2025-40 from current projects; US shale is plateauing
  (EIA: 13.6→13.7 mb/d 2025-26). LNG adds a durable, *contracted* demand leg — US export capacity ~18.3
  Bcf/d on track to nearly double by 2031, 4 projects hit FID in 2025 (+7.2 Bcf/d). [IEA World Energy
  Investment 2025-06-05; IEF/S&P 2024-06; WoodMac 2026-02-26; EIA STEO/Today-in-Energy 2026] VERIFIED.
- **Caveat:** the thesis is *supply-side/long-term* — near-term the IEA sees a **~4 mb/d 2026 surplus**
  and Citi flags Brent to $60 on normalization, so the trade can be early/painful; and the *power-sector*
  gas leg faces renewable displacement (2025 solar met ~75% of global demand growth). Oil-demand still
  grew in 2025 (+1.2 mb/d) and peak-oil calls keep slipping (BP pushed its peak back 5 yrs to 2030), so
  the demand-destruction risk is real but not imminent. **Favor E&P/integrated with capital discipline +
  low breakevens; be patient on entry.** → **CNOOC (0883.HK) / EOG** are exactly this thesis.

### 2. EM Life Insurance (and the demographics leg of insurance generally)
- **Why cheap:** EM Life **EV/EBITDA 7.3× (5th pctile own hist), P/B 1.4×, ROIC 15.1%, ROE 17.6%, xsec 6**
  — cheap vs its own history AND vs peers AND the highest-quality name in cheap EM. [Damodaran 2026-01-05]
  VERIFIED.
- **The trend (durable):** *two* reinforcing tailwinds. (a) **Rates normalized** — Fed 3.50-3.75%, ECB
  re-hiking +25bps (Jun 2026) vs 2010s ZIRP — lifting insurer investment income (MetLife NII +6%,
  Prudential +9%). (b) **Aging demographics / Asia protection gap** — US annuity sales a 4th straight
  record ($464.1B FY2025, +7%); Asia protection gap ~$390B; China life +5.6% real (2026); global
  retirement gap ~$70T→$400T by 2050. [Fed/ECB; SEC 8-Ks; LIMRA; Swiss Re sigma/WEF, 2025-2026] VERIFIED.
- **Caveat:** distinguish the *life/demographics* leg (durable) from the *P&C/reinsurance pricing* leg,
  which is clearly **softening** (Jan-2026 property-cat reinsurance −12 to −15%, commercial pricing down
  3+ quarters — record margins but falling price = late cycle). Favor life/savings-driven names over
  cyclical P&C. → **CPIC (China Pacific Insurance)** is this thesis (EM life + aging + rates).

### 3. Building Materials — US aggregates/cement (reshoring + infra floor)
- **Why cheap:** US Building Materials **EV/EBITDA 11.6× (41st pctile own hist), P/B 3.6× (23rd pctile),
  US P/E at the 5th pctile, ROIC 20.2%, ROE 16.0%** — a genuine cyclical-cheap + high-ROIC name.
  [Damodaran 2026-01-05] VERIFIED.
- **The trend (durable floor):** reshoring + public-infra spend gives a floor under a rate/housing-driven
  cyclical trough — US total construction ~$1.26T, IIJA $568B / 47% allocated across 68k+ projects, CHIPS
  awards finalized. [Fitch 2025-10-12; US Census/IIJA trackers 2026] VERIFIED.
- **Caveat — pick the right expression:** the research shows the *premium aggregate* names (**Vulcan
  ~36× P/E / ~19× EV/EBITDA, Martin Marietta ~20× EV/EBITDA**) are NOT cheap — near decade-high multiples.
  The *reasonably-valued* expressions are **CRH (~12× EV/EBITDA, ~20× P/E) and Eagle Materials (~11×
  EV/EBITDA, ~17× P/E)**. And the manufacturing-construction *growth rate* has crested (−30% from the Sep
  2024 peak, IRA gutted by OBBBA) even though the *level* is ~2× pre-2020. Buy the laggards, not the
  darlings. → **Buzzi (cement)** is this thesis (reshoring/infra building materials, cheap cement leg).

### 4. Information Services — US + Global (AI *sentiment* discount on moaty franchises)
- **Why cheap:** US Info Services **EV/EBITDA 11.5× (5th pctile own hist), ROIC 22.2%**; Global **10.8×
  (5th pctile), ROIC 22.8%** — near the bottom of their own 11-yr ranges while earning ~22% ROIC.
  [Damodaran 2026-01-05] VERIFIED.
- **The trend (a SPLIT, not a clean tailwind):** AI is repricing *pure data/analytics* vendors (Morningstar
  cut FactSet/SS&C moats on AI-substitution fear) but the **ratings/index franchises (S&P Global, Moody's,
  MSCI)** remain moaty and still guide double-digit 2026 EPS. So the sector-level cheapness is **AI
  *overhang* on protected 22%-ROIC names** — realized damage is in *pure vendors*, not the franchises.
  [Forbes 2026-06-08; Morningstar] VERIFIED (verdict split by sub-segment). This is the *beneficiary/
  protected* side of the same AI axis whose *victim* side (IT services) we detail in `theme_ai_deflation.md`.
- **Caveat:** strictly segment-select — buy the protected ratings/index franchises; avoid the pure
  data/analytics vendors that ARE the AI-substitution target. Sector-average cheapness masks this split.

**Honorable mention — European banks (rates leg, largely re-rated):** cheap on ~9× fwd P/E, ROE-justified
discount to US, rates-normalization is durable (NII near records), but the STOXX-600-Banks +48% trailing
52wk rally means the easy re-rating is done. Cheap-ish + real trend, but not the deep-value entry it was.

---

## Expensive-but-trendy — great trend, NO value (watchlist; do not overpay)

The market has already paid up for these. Damodaran own-history percentiles in brackets; run-up/multiple
evidence web-cited (2025-2026).

- **Defense / Aerospace** [US comp 92, Global 95; 95th-pctile EV/EBITDA]. Trend VERIFIED-durable (global
  milex $2.72T +9.4% 2024; NATO Hague 5%-by-2035; Germany's *permanent* constitutional debt-brake carve-out
  — the strongest durability signal; prime backlogs at records: Rheinmetall €63.8bn, Lockheed $179bn).
  BUT **European pure-plays ran +150-190% then rolled over −30%+ in 2026** (Rheinmetall fwd P/E peaked ~39×
  ≈2× its median); European defense index ~34× P/E, above US tech. **Nuance:** US primes (LMT 17.9×, NOC
  19.4×, GD 22.2×) are *at/below* 5-yr-avg fwd P/E — the one value-lens counter-case. [SIPRI 2025/26; NATO
  Hague; SEC/IR backlogs — VERIFIED. Multiples — VERIFIED underlying, some analyst notes UNVERIFIED.]
- **Electrical Equipment / grid** [US comp 89, Global 91]. Datacenter-power demand VERIFIED-durable (IEA:
  DC electricity ~doubles to ~945 TWh by 2030; Goldman +165% power demand by 2030; US load growing after
  ~20yr flat, EIA 2025 generation record +2.8%). BUT **GE Vernova ~+700% (fwd ~40-45×), Vertiv ~+535%
  (~44-47×)**. Least-stretched = **Hubbell (~22-24× fwd, in-line w/ history)**. [IEA Energy&AI 2025-04;
  EIA STEO 2026-06 — VERIFIED. Multiples — VERIFIED data / UNVERIFIED some notes.]
- **Independent Power Producers** [US Power comp 68, but low ROIC 6.9%]. Nuclear-PPA / datacenter demand
  real (Constellation Microsoft-TMI restart + Meta-Clinton PPAs VERIFIED). BUT Constellation +90%/+46-58%
  then −22% YTD-2026; **PJM cut its demand outlook on an "overstated AI boom"** — the firmest bear datapoint.
  Cheapest of group = NRG/Vistra.
- **Semiconductors / Semi-Cap-Equip** [US comp 74/80; 95th-pctile EV/EBITDA, P/B 13.3×/9.7×]. AI-compute
  tailwind real; valuations at extremes. No value.
- **Machinery** [US comp 65, mid-range but CAT ~48× trailing]; **Engineering/Construction** [US comp 95,
  95th pctile] — reshoring growth-rate has *faded* (mfg-construction −30% from peak, IRA gutted), yet
  priced for continued boom.
- **Metals & Mining / Precious Metals / Copper** [US comp 89/83]. Copper long-term deficit VERIFIED (IEA:
  ~10% gap by 2030) BUT **near-term 2026-27 surplus** + aluminium substitution accelerating; miners rich.
- **Uranium / nuclear** — spot ~$85.70/lb (Jul 2026), renaissance real but **back-loaded** (restarts
  ~2.2GW near-term; SMRs first-power ~2030+). **Equities run far ahead of spot** (Cameco trailing P/E ~92);
  Kazatomprom the profitable exception (~12× fwd). Boom-bust base rate. Trendy, not cheap.
- **Green & Renewable Energy** [US comp 50, but ROE −7.4%] — trend materially *weakened*: OBBBA (Jul 2025)
  repealed/phased EV, residential-solar, wind/solar credits; $34.8B of 2025 clean-energy cancellations
  (~3:1 vs new). Not a clean tailwind anymore.

---

## Cheap-but-the-trend-is-AGAINST-it — TRAPS (cheap for a reason)

- **Cable TV** [US/Global comp 5-17 — the cheapest of all, EV/EBITDA 5th pctile]. **Secular decline
  confirmed** — S&P Global: linear cable "formally entered the decline stage," subs peaked 2012, "long
  slow bleedout, no comeback"; basic cable −7.1% subs in 2024. [Fortune/S&P 2025-12-29] VERIFIED. **Trap.**
- **Food Processing** [US comp 11]. **Structural headwind** — GLP-1 adoption, MAHA/FDA ultra-processed-food
  crackdown (def. due Apr 2026), sticky private label; cheap names show trap traits (falling FCF, rising
  leverage). [Circana 2026; Bloomberg/Bernstein 2026-06-05] VERIFIED. **Trap.**
- **IT / Computer Services** [Global comp 68 — not even that cheap own-hist; US 59]. **The AI-deflation
  VICTIM.** GenAI attacks the billable-hour/labor-arbitrage unit itself (MOFSL: 9-12% revenue eliminated;
  HSBC 14-16% deflation; the tell — TCS revenue −3.1% cc while headcount −20k and margin *up*). Cheap
  because the model is under structural attack. → this is precisely **CTSH / TCS** (see
  `theme_ai_deflation.md`): CTSH = deep-value margin-of-safety (P/B 1.31, net cash) on a *real* risk;
  TCS = quality but no cushion (7× book). **Bounded trap — value only where price gives a margin of
  safety.** VERIFIED.
- **AI-exposed Education / edtech** [Global/EM comp 14 — cheap]. **Split** — SECULAR trap for AI-exposed
  edtech (Chegg collapsed ~$14.7B→~0, cut 45% of staff Oct-2025); CYCLICAL survivor for regulated EM
  tutoring (New Oriental rev +13.6%). Stock-pick within; the *edtech* leg is a trap. [CNBC 2025-10-27]
  VERIFIED.
- **Low-return cheap-no-trend (ordinary/trap-ish):** RE Development, Utility (Water), R.E.I.T. — cheap
  partly because returns are structurally thin (ROIC 3-7%); NOT quality-first candidates and NOT the
  power-demand play (Utility Water ≠ the datacenter-load story). **Beverage (Alcoholic)** is cheap but a
  *cyclical trough* with no strong trend — ordinary mean-reversion value, not a secular story.

---

## How this connects to the finalists we already deep-dived

| Finalist | Sector cell on this matrix | Trend it rides / fights | This matrix's read |
|---|---|---|---|
| **CNOOC (0883.HK)** | EM Oil/Gas Integrated (**SWEET SPOT**, ROIC 20%, xsec 1.6) | Oil & gas underinvestment | Cheapest × durable supply-side tailwind × top quality. (Investability is a *separate* OFAC/Canadian-citizen question — see `deep_dives/0883_HK/`.) |
| **EOG** | US Oil/Gas E&P (**SWEET SPOT**, ROIC 13.7%, EV/EBITDA 5.1×) | Underinvestment + shale discipline | Textbook cheap-E&P-with-quality; low-breakeven operator. |
| **CPIC (China Pacific Ins.)** | EM Life Insurance (**SWEET SPOT**, ROIC 15%, ROE 17.6%, xsec 6) | Aging / Asia protection gap + rates | Best-quality cheap EM; ride the *life/demographics* leg, not P&C. |
| **Buzzi** | Building Materials (**SWEET SPOT** US comp 23, ROIC 20%) | Reshoring / infra building materials | Cement = the *reasonably-valued* infra expression (vs pricey Vulcan/Martin Marietta). |
| **CTSH** | IT/Computer Services (**TRAP-side of AI axis**) | AI-deflation VICTIM (not beneficiary) | Cheap because the billable-hour unit is under attack; value only via CTSH's balance-sheet cushion. |
| **TCS** | IT/Computer Services (**TRAP-side**, no cushion) | AI-deflation VICTIM | Quality but 7× book = no margin of safety; WATCH pending revenue re-inflection. |
| **INTU** | Software (System & App) — *expensive own-hist but a fallen angel* | AI: seat-compression vs upsell | Not a "cheap sector" per Damodaran (US comp 41); the value is *stock-specific* de-rating, per `theme_ai_deflation.md`. |

**The pattern:** every finalist that survived as a *value* case sits in a **SWEET-SPOT cheap cell**
(CNOOC/EOG = energy underinvestment; CPIC = EM life/aging; Buzzi = reshoring cement). The finalists that
are *contested* (CTSH/TCS/INTU) all sit on the **AI axis** — CTSH/TCS on the *victim/trap* side (value
only with a cushion), INTU as a stock-specific fallen angel rather than a cheap sector. **The exciting
trends (defense, electrification, semis, machinery) produced ZERO value finalists — because they are all
expensive.** That is the core message of this matrix.

---

## Method & limitations

- **Cheapness/quality axis:** reused verbatim from Stage-1a (`sector_cheapness.md`) — Damodaran 11-yr
  own-history percentiles (EV/EBITDA + P/B + US P/E) and current ROIC/ROE, as-of **2026-01-05**, from
  `data/damodaran/history/sector_cheapness_{US,Global,Emerging}.csv`. Not recomputed. These are **annual,
  simple industry averages, ~6 months stale** → good for *relative sector cheapness/quality*, not a live
  price. Percentiles are within an **11-year** window (spans COVID + the rate cycle, not 2008-09).
- **Trend axis:** web-cited 2025-2026 evidence from two research subagents (defense/electrification;
  energy/financials/reshoring). Each trend was tested for (a) durability, (b) already-priced-in/valuation,
  (c) fade risk. **Classification = the cross of the Damodaran cheapness percentile × the trend direction**
  — i.e. a sector is "SWEET SPOT" only if it is cheap own-hist AND has a durable tailwind AND respectable
  ROIC; "expensive-but-trendy" if the trend is durable but the sector is at the top of its own range.
- **Confidence marks:** all Damodaran multiples/ROIC/ROE = **VERIFIED** (real fetched values). Trend
  durability anchors (SIPRI, NATO, EIA STEO, IEA investment/Energy&AI, Fed/ECB, LIMRA, SEC 8-Ks) =
  **VERIFIED (primary or 2+ agreeing)**. Equity **run-ups/multiples** rest on stockanalysis.com/Finviz/
  Yahoo raw data — VERIFIED on the underlying data, but **specific EV/EBITDA figures, some analyst notes,
  and historical-P/E-average premiums are single-aggregator (UNVERIFIED/ASSUMED)** — reconfirm from a
  Bloomberg/Reuters terminal before acting.
- **Known data caveats carried forward:** (1) 2025-2026 oil price/demand figures are distorted by a 2026
  US-Iran / Strait-of-Hormuz episode — treat as crisis-state, not baseline. (2) US P&C industry combined
  ratio and several insurer/European-bank valuation multiples are single-aggregator (UNVERIFIED). (3)
  Reshoring job data is advocacy-sourced (directional). (4) IEA/OPEC/Reuters/FT primary portals were
  network-blocked to automated fetch this session; figures came via primary reporting / 2+ agreeing
  secondaries. (5) Healthcare is placed on the matrix at a high level only — **deep decomposition is
  deferred to the separate healthcare agent** (aging-demographics tailwind noted; US Healthcare Products
  comp 35, Hospitals comp 56, Global Pharma comp 68 — mostly mid-range, not a cheap-sector standout).
- **Not financial advice.** Research to inform Hooman's own decisions.

**Reproduce the cheapness axis:**
```
/opt/venv/bin/python3 screens/fetch_damodaran_history.py    # build 11yr history
/opt/venv/bin/python3 screens/analyze_sector_cheapness.py   # rank + per-region CSVs
```
Trend evidence: see the two 2026-07-04 research-subagent briefs (citations inline above).
