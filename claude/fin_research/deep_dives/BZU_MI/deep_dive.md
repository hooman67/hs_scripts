# Deep Dive — Buzzi S.p.A. (BZU.MI · Borsa Italiana / Euronext Milan)

**Sector:** Building Materials (cement, ready-mix concrete, aggregates) · **Region:** dev-ex-US (Italy-domiciled, global)
**Bucket:** BOTH (1a-cheap Building-Materials sector **and** 1b cheap-quality gate PASS)
**Author:** Claude (Opus 4.8) · **Date:** 2026-07-02 · Owner: Hooman Shariati · **Not financial advice.**

> **Anti-hallucination:** every number carries a source + as-of date and a confidence mark
> (VERIFIED / ASSUMED / UNVERIFIED). Company financials are **Buzzi's own IFRS disclosures**
> (buzzi.com) — Buzzi is **not** a US filer, so no EDGAR backstop; independent wire
> cross-check (Reuters/MarketScreener) was largely blocked this session, so most fundamentals
> rest on a single source (company filings + one yfinance `.info` pull 2026-07-02). Sector /
> carbon / cycle facts are web-sourced with URLs. Two as-of dates in play: **yfinance market
> data 2026-07-02**; **Buzzi FY2025 results approved 2026-03-31**.

---

## 0. Snapshot (VERIFIED — yfinance 2026-07-02, price €45.49)

| Metric | Value | Source / note |
|---|--:|---|
| Price | €45.49 | yfinance 2026-07-02 |
| Market cap | €8.06B | yfinance 2026-07-02 |
| Enterprise value | €7.12B | yfinance (EV < mktcap → **net cash**) |
| Trailing P/E | 8.9 | yfinance |
| Forward P/E | 8.9 | yfinance |
| EV/EBITDA | 6.0 (5.8 on FY25 recurring EBITDA) | yfinance / derived |
| P/B | 1.16 | yfinance |
| ROE | 13.0–13.4% | yfinance 13.4%; FY25 NI/equity 13.0% (derived) |
| Operating margin | 22.8% | yfinance |
| Earnings yield | 11.4% (NI/mktcap) · 12.6% (EBIT/EV) · 14.5% (screen) | derived / screen 2026-07-02 |
| Dividend yield | ~1.5% (DPS €0.70) | yfinance / company; **low payout ~14%** |
| Piotroski (lite) | 7/7 | screen 2026-07-02 |
| Net cash (company NFP FY2025) | **+€1,130.9M** | Buzzi FY2025 results 2026-03-31 (VERIFIED) |
| Beta | 1.05 | yfinance |

Screen snapshot (EV/EBITDA ~6.0, EY 14.5%, ROE 13.4%, Piotroski 7/7, P/B 1.16, P/E ~8.9)
**VERIFIED** against a fresh yfinance pull. Buzzi is the **only Building-Materials name that
actually screens cheap** — vs trough-priced US aggregates (VMC/MLM at ~35× P/E, EV/EBITDA 18–19).

---

## 1. Business & Thesis

**What it is.** Italian building-materials group (Casale Monferrato HQ; formerly *Buzzi Unicem*,
renamed **Buzzi S.p.A.** in 2023). Makes **cement, ready-mix concrete, and aggregates** across
**13 countries, ~10,000 employees**; listed on the FTSE MIB. [buzzi.com/en/our-operations,
as-of 2026-07 — VERIFIED]

**Geography — the USA is ~half of profit.** FY2025 recurring EBITDA by country (Buzzi FY2025
results, approved 2026-03-31 — VERIFIED; country lines labeled "EBITDA," group recurring split):

| Region | FY2025 recurring EBITDA (€m) | Share |
|---|--:|--:|
| **USA** | **584.8** | **~47%** |
| Italy | 176.9 | 14% |
| Germany | 126.2 | 10% |
| Brazil | 103.9 | 8% |
| Mexico (equity-method JV) | 100.2 | 8% |
| Russia | 76.7 | 6% |
| Czech/Slovakia | 74.9 | 6% |
| Poland | 57.2 | 5% |
| Lux/NL, UAE, other | ~34 | 3% |
| **Group recurring EBITDA** | **1,234.1** | 100% |

- **USA** (~40% of sales, ~47% of EBITDA — a higher-margin business than the group): Buzzi
  Unicem USA, 8 cement plants, ~10.2 Mt/yr capacity + Texas ready-mix/aggregates. This is the
  single biggest earnings driver and the crux of the cyclical debate (§2).
- **Mexico JV — Corporación Moctezuma:** Buzzi 33.33% (equity method, joint control with
  Cementos Molins). FY2025 contribution €100.2M; carrying value €266M but **fair value of the
  listed stake €1,192M** — a hidden asset well above book. [FY2025 AR Notes 14/24 — VERIFIED]
- **Russia — still fully consolidated, NOT exited.** SLK Cement (100% via Dyckerhoff) remains
  line-by-line consolidated under IFRS 10 even though Buzzi "ceased all operational involvement"
  in May 2022; net assets €496.8M, FY2025 EBITDA €76.7M. **No sale announced;** high country
  risk, excluded from the decarbonization roadmap. [FY2025 AR Note 5 — VERIFIED]
- **Ukraine — exited** (sold Oct 2024, deconsolidated). **Brazil** — bought out to 100% (Oct
  2024), now fully consolidated. [FY2025 AR — VERIFIED; buyer/price UNVERIFIED]

**The thesis (value / cheap-cyclical).** Buzzi pairs a **genuinely cheap multiple** (EV/EBITDA
~6, P/E ~9, P/B 1.16, EY ~12–14%) with **high-quality attributes** rare in cement: a
**net-cash balance sheet** (+€1.13B), **27%+ EBITDA margins**, disciplined family stewardship,
and a US-heavy profit mix. It screens BOTH — cheap company *and* in the 1a-cheap Building-
Materials sector. The debate is **cheap-cyclical vs quality-value**: bulls say a net-cash,
half-US-profit cement compounder at 6× EV/EBITDA is a quality name on sale; bears say cement is
cyclical and the ~27% margin still reflects the post-2022 pricing surge, so "cheap" is really
mid-to-high on the cycle. My read (§2) is nuanced: **US is past peak / troughing, not peaking**,
which weakens the classic "earnings at a cyclical high" objection for Buzzi's biggest region.

---

## 2. Valuation & the Cyclicality Test

### 2a. Multiples vs peers (VERIFIED — yfinance 2026-07-02; currencies differ, do not net)

| Co. | Ticker | P/E (ttm) | Fwd P/E | EV/EBITDA | P/B | ROE | Op mgn | Net debt/(cash) | Div yld |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| **Buzzi** | BZU.MI | **8.9** | **8.9** | **6.0** | **1.16** | 13.4% | 22.8% | **net cash −€0.96B** | 1.5% |
| Heidelberg Mat. | HEI.DE | 15.2 | 11.5 | 8.7 | 1.65 | 11.1% | 17.6% | +€5.7B | 2.2% |
| Holcim | HOLN.SW | ~106* | 17.5 | 14.3 | 2.67 | 2.1%* | 12.1% | +€3.8B | 2.3% |
| CRH | CRH | 19.8 | 15.9 | 11.7 | 3.09 | 15.8% | ~0%† | +€17.2B | 1.5% |
| Vulcan | VMC | 35.4 | 27.6 | 18.4 | 4.58 | 13.5% | 15.6% | +$5.1B | 0.7% |
| Martin Marietta | MLM | 37.1 | 25.8 | 19.1 | 3.14 | 9.5% | 12.7% | +$5.4B | 0.6% |
| Cemex | CX | 36.5* | 13.8 | 7.7 | 1.37 | 3.8% | 10.5% | +$5.5B | 0.8% |

\*Holcim/Cemex trailing P/E and Holcim ROE distorted by one-offs (Holcim's 2025 Amrize North-
America spin-off — flagged, UNVERIFIED here). †CRH op-margin field looks like a yf artifact.

**Read:** Buzzi is **the cheapest of the cohort on every clean metric** — lowest P/E (8.9 vs
15–37), lowest EV/EBITDA (6.0 vs 8.7–19), near-lowest P/B (1.16), and the **only net-cash**
name (every peer carries $4–17B net debt). US aggregates (VMC/MLM) trade at ~3× Buzzi's
EV/EBITDA because they're priced as low-cyclicality, IIJA-fed, aggregates-led compounders;
Buzzi is priced as a Milan-listed, family-controlled, Russia-exposed cement pure-play. Some of
the gap is deserved (liquidity, governance, Russia — §4); much is not.

### 2b. Multiples vs own history — margins are elevated but off peak

Buzzi income statement (Buzzi filings — VERIFIED; recurring EBITDA where noted):

| FY | Revenue (€m) | EBITDA (€m) | EBITDA margin | Net income (€m) | Net cash (€m) |
|---|--:|--:|--:|--:|--:|
| 2022 | 3,996 | 892 | 22.3% | 459 | — |
| 2023 | 4,317 | 1,443 | 33.4% | 967 | — |
| 2024 | 4,313 | 1,271.7 (rec.) | 29.5% | 942.5 | +755.2 |
| 2025 | 4,518.8 | 1,234.1 (rec.) | 27.3% | 921.3 | **+1,130.9** |

The **2022→2023 margin jump (22%→33%)** is the post-energy-crisis pricing surge: cement prices
were pushed up hard to recover 2022 gas/petcoke costs, then energy fell while prices held — a
classic cyclical windfall. FY2025 margin (27.3%) is **down from the 2023 peak but still well
above the 2022 base** — so earnings *are* above a normalized mid-cycle level, though not at the
2023 high. **CYCLICAL TEST verdict:** margins are cyclically **elevated (not peak)**; a mean-
reversion toward mid-20s% margin is a real risk to the "8.9× P/E" (normalized P/E is higher).

### 2c. The cycle — US near trough, Europe depressed (VERIFIED, web-sourced)

- **US (Buzzi's ~47% of profit): past peak, troughing in 2026.** US cement consumption ~110 Mt
  (down from ~114 Mt in 2022); production −4% in 2024; construction spending (TTLCONS) peaked
  ~$2.26T Jan-2025, −2.9% YoY by Jan-2026. [USGS MCS 2025, pubs.usgs.gov/periodicals/mcs2025/mcs2025-cement.pdf;
  FRED TTLCONS, latest May-2026 — VERIFIED]. The American Cement Association Spring-2026 forecast
  calls 2026 the demand **trough (−2.5%)** with **growth resuming 2027** [secondary, via ainvest
  2026-05-04 citing ACA — UNVERIFIED magnitude]. **US prices near record highs and holding, not
  rolling over** (BLS PPI hydraulic cement WPU1322 ~357.8 May-2026, flat-to-up in 2025) [FRED/BLS
  — VERIFIED]. **Implication:** Buzzi's biggest region is **not at a cyclical earnings peak** —
  it is near a volume trough with prices holding, which cuts against the simple "peak earnings"
  bear case and is the strongest single support for the thesis.
- **Europe (Italy/Germany, ~24% of profit): depressed/bottoming.** German + Italian residential
  construction has been in a rate-driven downturn 2023–25; commentary points to a bottom in 2025
  and tentative 2026–27 recovery. [directional, magnitudes UNVERIFIED — CEMBUREAU/Euroconstruct
  primary not captured]. So Europe is **below** mid-cycle, not above.
- **Energy: a tailwind into 2026.** EU gas/power well below the 2022 crisis peak, easing the
  fuel component of cement cost — margin support that partly offsets carbon (§4). [directional —
  UNVERIFIED on 2026 price points].

**Net cyclical-peak call:** **Group earnings are moderately elevated on margin (the retained
2022–24 pricing), but volumes are near/below mid-cycle** (US troughing, Europe depressed). This
is **NOT a classic top-of-cycle setup** like the US aggregates. The honest framing: Buzzi is a
**cheap cyclical whose price is normal-to-low and whose margin is somewhat high** — the risk is
margin normalization, not a volume cliff from a peak.

---

## 3. Quality

- **Balance sheet — the standout. Net cash +€1,130.9M** at YE2025, up from +€755.2M a year
  earlier and vs €1.3B *net debt* back in 2022 — Buzzi deleveraged through the cycle and now runs
  a fortress balance sheet (total debt €441M vs €1.40B cash). [Buzzi FY2025 — VERIFIED]. This is
  genuinely unusual in a capital-intensive, cyclical industry and is the core of the "quality"
  case; it also means the low ~6× EV/EBITDA is on an EV *below* market cap.
- **Margins & returns:** EBITDA margin 27.3% (recurring FY25), operating margin 22.8%, ROE
  13.0–13.4%, ROA 6.3%. Returns are solid-not-spectacular; the net-cash drag actually *depresses*
  ROE (excess cash earns little) — an owner-operator running for durability over optics.
- **FCF & capital discipline:** FY2025 operating cash flow €914M, capex €425M, **FCF ~€489M**
  (FCF also €484M/2024, €515M/2023 — steady) [Buzzi filings — VERIFIED]. Capex ~9–10% of sales,
  disciplined. Capital return is **conservative**: DPS €0.70 (payout ~14%), plus a **€200M
  buyback-for-cancellation** launched Feb-2026; ~7% treasury stock being cancelled. [FY2025
  results / AGM 2026-05-13 — VERIFIED]. Buzzi hoards cash rather than over-distributing — good
  for downside, modest for near-term yield (this is a total-return/optionality name, not income).
- **Governance / family ownership:** Buzzi family controls **53.0% of capital** via Fimedi→Presa,
  and — critically — a **loyalty double-voting mechanism vested 2026-06-01 lifts the family to
  69.18% of voting rights** while still holding ~53% of economics. [FY2025 CG report / voting
  communications 2026-06 — VERIFIED]. Single share class (no separate super-voting class); CEO
  **Pietro Buzzi** also chairs both holding companies (related-party overlap). Long-term family
  stewardship has historically meant conservative leverage and through-cycle discipline (a plus),
  but the **economic/voting wedge is a minority-protection red flag** (a bear point, §4).

---

## 4. Bear Case / Risks

1. **Margin normalization (top risk).** FY25 27.3% recurring EBITDA margin still embeds the
   2022–24 pricing windfall (vs 22.3% in 2022). If cement prices soften as energy costs stay low
   and volumes stay weak, margin could mean-revert toward mid-20s%, lifting the normalized P/E
   well above the headline 8.9× — i.e. the stock is cheaper on *this year's* elevated margin than
   on a mid-cycle one. **This, not a volume peak, is the real cyclical risk.**
2. **EU carbon cost — the durable structural headwind (VERIFIED).** EU ETS carbon ≈ **€79.6/t
   CO2 (2026-07-02)** [tradingeconomics.com/commodity/carbon — VERIFIED]. Cement emits ~0.6 t
   CO2/t (blended) to ~0.8 t/t (clinker), ~50–60% of it unavoidable *process* CO2 from limestone
   calcination [IEA/GCCA — VERIFIED]. Historically cement got **free** allowances; those now
   **phase out on a fixed schedule** — 2.5% cut in 2026, accelerating to **100% (zero free) by
   2034** [EU Parliament EPRS 698889 & ICAP — VERIFIED]:

   | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 |
   |--|--|--|--|--|--|--|--|--|
   | −2.5% | −5% | −10% | −22.5% | −48.5% | −61% | −73.5% | −86% | **−100%** |

   At €80/t this is a **rising cost of ~€48/t cement (blended) to ~€64/t (clinker) by full
   phase-out** [derived] — potentially comparable to product value by the 2030s. **CBAM** (import
   carbon levy, definitive regime from 2026-01-01) [EC — VERIFIED] shields the EU *domestic*
   market but **not exports**, and its enforcement is debated. Buzzi's **US (~47%) and Mexico/
   Brazil profits are outside EU ETS**, so this bites ~24% of EBITDA (Italy+Germany) — real but
   *diluted* by the non-EU mix. Still, it's a decade-long structural margin drag on the EU legs.
3. **Construction-cycle downturn.** A sharper/longer US infrastructure pause (IIJA reauthorization
   is an open funding cliff — US makers lobbied Congress June-2026 [World Cement — VERIFIED]) or a
   failed European recovery would hit volumes and pricing power together.
4. **Russia.** €496.8M net assets still consolidated with no exit path; sanctions/impairment/
   forced-sale risk. Excluded from decarbonization plan.
5. **Governance / liquidity.** Family voting control now 69% vs 53% economics (loyalty-vote wedge)
   — minority interests can be outvoted; related-party overlap (CEO chairs the holdcos). Milan
   listing is **less liquid** than the US majors and carries a home-bias/small-cap-Europe discount
   — part of why it screens cheap and part of why it may *stay* cheap (a value-trap-lite risk).
6. **FX.** ~63% of EBITDA is non-EUR (USD, MXN, BRL, RUB); EUR strength compresses reported
   results (FY25 US sales −7% reported vs −2.9% constant-FX).

**Both sides:** the net-cash sheet, half-US-profit mix, and *below*-peak US volumes materially
soften bear points 1 and 3 vs a levered EU-only peer; carbon (2) and governance/liquidity (5)
are the durable, less-fixable negatives.

---

## 5. Catalysts & Verdict

**Catalysts:** (a) US 2027 volume recovery off the 2026 trough (ACA) re-rates the ~47% profit
engine; (b) continued buybacks/cancellation (€200M program) + rising dividend as the €1.1B net
cash gets deployed (M&A or return); (c) European construction bottoming into 2026–27; (d) any
Russia resolution removes an overhang; (e) simple multiple re-rating toward peers (6× vs 9–14×).

### Scorecard (CLAUDE.md §3 weights: Cheapness 30 / Quality 30 / Trap 20 / Moat 15 / Catalyst 5)

| Dimension | Score /10 | Weight | Contribution | Rationale |
|---|:--:|:--:|--:|---|
| **Cheapness** | 9 | 30% | 2.70 | Cheapest of the cement cohort on every clean metric (P/E 8.9, EV/EBITDA 6.0, P/B 1.16, EY ~12–14%); only net-cash name. Docked 1 for margin being cyclically elevated (normalized cheapness a notch less extreme). |
| **Quality** | 8 | 30% | 2.40 | Fortress net-cash B/S, 27% margins, steady FCF, disciplined capex, through-cycle deleveraging. Docked for mid-teens ROE (cash-drag) and not being a low-cyclicality aggregates compounder. |
| **Trap-risk (inverse)** | 6 | 20% | 1.20 | Genuinely cheap + net cash + Piotroski 7/7 argue against a trap; but Milan-listing illiquidity + family 69% voting wedge + cyclical/carbon overhang can keep it cheap. Moderate trap risk. |
| **Moat & leadership** | 6 | 15% | 0.90 | Cement is a local-monopoly/logistics-moat business (high, but regional not global); Buzzi is a disciplined #~1–3 in its markets, not the scale leader (Holcim/Heidelberg/CRH bigger). Strong family stewardship. |
| **Catalyst** | 6 | 5% | 0.30 | US 2027 recovery + buyback/cash deployment + re-rating potential; nothing imminent/hard-dated. |
| **Weighted total** | | | **7.50 / 10** | |

### VERDICT: **BUY-worth-more-work**

Buzzi is the cleanest expression of the Building-Materials value thesis in the whole run: the
**only cement name that is actually cheap** (EV/EBITDA 6.0, P/E 8.9, P/B 1.16), paired with a
**net-cash balance sheet** and half its profit in the US — where the cycle is **near a trough,
not a peak**. Weighted score **7.5/10**. The two things that keep it from a clean BUY are (1)
margins that still carry the 2022–24 pricing windfall (so it's cheaper on this year's elevated
margin than on a normalized one) and (2) the twin structural overhangs of **EU carbon-cost
phase-out** (free allowances gone by 2034; ~24% of EBITDA exposed) and **family voting control
(69% votes / 53% economics) plus Milan-listing illiquidity**. "More work" = (a) confirm FY2025
figures and the country EBITDA split against the audited annual report (single-source risk here),
(b) build a normalized-margin / mid-cycle earnings estimate to test how cheap it *really* is,
(c) size the EU-ETS cost curve on Buzzi's specific Italian+German clinker tonnage, and (d)
sanity-check the family-governance / minority-protection setup.

---

## 6. Summary (for the ranked report)

**BUY-worth-more-work — score 7.5/10.** Buzzi is the standout Building-Materials value: the only
cement name that screens genuinely cheap (EV/EBITDA 6.0, P/E 8.9, P/B 1.16, EY ~12–14%, all
VERIFIED yfinance 2026-07-02) and the only one with a **net-cash balance sheet (+€1.13B, FY2025)**,
27%+ EBITDA margins, steady FCF, and disciplined family stewardship. **Cyclical-peak call:
NOT a classic top-of-cycle** — Buzzi's biggest profit engine (US, ~47% of EBITDA) is *past peak
and troughing in 2026* with prices holding near records, and Europe (~24%) is depressed/bottoming;
the real cyclical risk is **margin normalization** off the retained 2022–24 pricing windfall
(margin down from 33% peak to 27.3% but still above the 22% 2022 base), not a volume cliff.
**Top risk: EU carbon cost** — free EU-ETS allowances (carbon ~€79.6/t, 2026-07-02) phase out on
a fixed schedule to **zero by 2034**, a decade-long structural margin drag on the ~24% EU EBITDA
(partly shielded on imports by CBAM, not on exports); secondary risks are the family voting wedge
(69% votes vs 53% economics) and Milan-listing illiquidity that could keep it cheap. All figures
rest on Buzzi's own filings + one yfinance pull (no EDGAR/second-source cross-check) — the "more
work" is a normalized-margin estimate and a filings/governance verification pass.
