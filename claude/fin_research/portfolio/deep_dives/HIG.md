# The Hartford (HIG) — Deep Dive

**Ticker:** HIG (NYSE) · **Sector:** Financials — Property & Casualty Insurance (multiline) · **Country:** US
**Legal name:** Hartford Insurance Group, Inc. (renamed from "The Hartford Financial Services Group, Inc." eff. 2026-02-06; brand still "The Hartford"). **[V]** — SEC
**Deep-dive date:** 2026-08-26 · **Analyst:** Claude (Opus 4.8) for Hooman Shariati (Canadian; quality-first, total-return value)
**Why it's here:** surfaced in the cheap-quality screen refresh (2026-08-26) as a "newly-cheap US insurer" — a candidate DEFENSIVE non-bank addition to the small Financials sleeve (CI managed-care + BRK-B, ~2.5% target, underweight).

Confidence tags: **[V]** verified from primary filing / ≥2 agreeing sources · **[A]** assumed / my derivation · **[U]** unverified single-source. Prices move — all multiples as-of 2026-08-26. **Research, not advice.**

---

> ⚠️ **HEADLINE FINDING — this is NOT a "newly-cheap" fallen angel. It is a HIGH-QUALITY insurer trading at a FAIR price near a CYCLICAL EARNINGS PEAK.** HIG is ~$139.85, **near its 52-week high** ($120.33–$146.07) and up from ~$44 in 2020 — no drawdown, no de-rating. The ~9.7× trailing P/E that tripped the screen is **structural, not a discount**: HIG has traded at ~10× for its entire modern history (2021: 10.0× · 2023: 9.7× · 2024: 10.3× · 2025: 10.1× · now: 9.5×). What HAS changed is that it now trades at a **record ~2.0× book on record ~19–22% ROE and combined ratios near cycle lows** — i.e. the low P/E sits on top of **peak-cycle earnings**. The single most important tell: **forward EPS ($13.69) is BELOW trailing EPS ($14.49)** — the market is pricing an earnings *decline*. That is the signature of a cyclical-peak insurer, not a bargain. The honest question is not "why is this quality name so cheap" but **"am I paying a full price for peak underwriting margins right as the P&C cycle softens?"**

---

## 0. Verified snapshot (as-of 2026-08-26)

| Metric | Value | Source / confidence |
|---|---|---|
| Price | **$139.85** | yfinance live pull 2026-08-26T20:14Z — **[V]** |
| Shares outstanding | **~270.9M** | yfinance — **[V]** |
| Market cap | **~$37.9B** | **[V]** |
| 52-week range | **$120.33 – $146.07** (near high) | yfinance — **[V]** |
| Trailing P/E | **~9.65** (net-income basis) | yfinance; TTM EPS $14.49 — **[V]** |
| Forward P/E | **~10.2** | yfinance; fwd EPS **$13.69 < trailing $14.49** — **[V]** ⚠️ |
| P/B | **~1.97** (reported book, incl. AOCI) | yfinance; BVPS $71.05 — **[V]** |
| P/B (ex-AOCI) | **~1.77** | on Q2'26 BVPS-ex-AOCI $78.91 — **[V, A calc]** |
| EV/EBITDA | **~6.8** | yfinance — **[V]** |
| ROE (TTM, net income) | **~22.1% / 23.8%** | yfinance / Q2'26 release — **[V]** (inflated; see §3) |
| **Core ROE (TTM)** | **18.7%** | Q2'26 8-K release — **[V]** (the honest number) |
| Dividend yield | **~1.7%** ($2.40/yr; payout ~16% of net income) | yfinance / releases — **[V]** |
| Buyback | **new $4.2B authorization** (+27%), thru end-2028 | Q2'26 release — **[V]** |
| Total capital-return yield | **~6–6.5%** (div + buyback) | **[A]** on $37.9B cap |
| Beta | **~0.46** | yfinance — **[V]** (low — genuinely defensive) |
| AM Best rating | **A+ (Superior)**, affirmed 2026-07-22 | via research pass — **[V]** |
| Analyst consensus | **Buy / Moderate Buy**, avg PT **~$149.85** (~7% upside) | yfinance; 20–23 analysts — **[V]** |

**Reproduce:** `/opt/venv/bin/python3 data/fetch_fundamentals.py HIG TRV CB ACGL CINF ALL --refresh --out data/cache/hig_peers_summary.csv` → `data/cache/yf_HIG.json`, `edgar_HIG.json` (CIK 0000874766).

---

## 1. Business & Quality Overview

The Hartford is a **~200-year-old multiline US insurer** — a commercial-P&C-led writer with a personal-lines book, a group-benefits arm, and (soon-departing) an asset manager. Four segments **[V, Q2'26 8-K]**:

- **Business Insurance (BI) — the profit engine.** Commercial P&C: small-commercial (a genuine franchise — Hartford is a scale leader in small-business package/BOP), middle-market, and **workers' compensation** (Hartford is one of the largest US WC writers). Q2'26 core earnings **$695M of ~$962M** total segment core earnings — ~70%+ of profit. Written premiums +5%.
- **Personal Insurance (PI).** Auto + home, largely through the **AARP affinity relationship** (a direct-to-member exclusive — a real, sticky distribution moat). **The AARP book is STILL ACTIVE** (79 mentions in the Q2'26 10-Q) — the 2023-24 "Hartford exits personal lines" reports were WRONG. Q2'26 core earnings $128M; PI written premiums **−7%** (deliberate shrink/re-underwriting of auto+home for profitability). Renewal pricing: auto +5.5%, home +10.4%.
- **Employee Benefits (EB).** Group life & disability — a top-tier US group-benefits carrier. Q2'26 core earnings $139M; margin 7.4% (down from 9.2% — softening). **Expanding: agreed to buy Equitable's employee-benefits business (announced 2026-08-04, ~$500M premium), close ~Q4 2026.** [V]
- **Hartford Funds — BEING SOLD to Wellington Management** (announced 2026-06-03; now **discontinued operations**, close ~Q1 2027). $300M cash + contingent payments (filing shows an NPV collar of **$1.5B floor / $2.1B ceiling**; the press "~$1.9B" is not in the filing — **[A]**); ~$150M after-tax realized loss at close. This **simplifies HIG into a pure insurer** and hands back capital. [V]

**Revenue mix (FY2025, TTM revenue ~$29B):** overwhelmingly P&C-premium-driven, with EB premium and net investment income the other two legs. Net income FY25 **$3.84B** on equity **$18.98B** (EDGAR CIK 0000874766 — **[V]**).

**Quality read — genuinely high:**
- **Core ROE 18.7% TTM / 19.4% FY25** [V] — top-quartile for a multiline insurer, and *sustained* (not a one-year spike).
- **Book value compounding ~10–12%/yr:** BVPS-ex-AOCI $73.62 (12/31/25) → **$78.91 (6/30/26)** [V]; reported BVPS $41.69 (2022) → ~$66.57 (2025) [A calc] — a ~17%/yr book-value CAGR through the hard market.
- **Underwriting discipline:** BI **underlying** combined ratio has held **~88–89 for five straight years** (§3) — steady, profitable underwriting, not a lucky year.
- **A+ (Superior) AM Best**, low financial leverage (~$4.4B debt vs $19B equity), clean investment book (§3).
- **Aggressive, disciplined capital return** (§4).

This is a well-run, high-return, defensively-postured insurer. **Quality is not the question. Price-vs-cycle is.**

---

## 2. Valuation — cheap, or optically cheap? (The crux)

### 2a. Vs. its OWN history — NOT de-rated; near the RICH end on book

| FY | P/E | P/B (reported) | Div yld | ROE |
|---|--:|--:|--:|--:|
| 2021 | 10.0 | 1.32 | 2.28% | 13.0% |
| 2022 | 13.4 | 1.76 | 2.23% | 11.5% |
| 2023 | 9.7 | 1.58 | 2.27% | 17.3% |
| 2024 | 10.3 | 1.93 | 1.81% | 19.6% |
| 2025 | 10.1 | 2.02 | 1.58% | 21.7% |
| **Now** | **9.5** | **1.95** | **1.71%** | **22.1%** |

*(stockanalysis.com/stocks/HIG/financials/ratios, 2026-08-26 — **[V]**; ROE cross-checks yfinance/Q2'26 release.)*

**This table is the whole story.** HIG's P/E has been a flat ~10× the entire time — the multiple is *structurally* low for insurers (thin GAAP "earnings yield" optics on a leveraged balance sheet). So "9.7× P/E" is **not a discount** — it's HIG's normal. What actually moved is **P/B: 1.32 → ~2.0, a record**, and **ROE: 13% → 22%, a record**. The stock is priced at the *top* of its own valuation-on-book range, precisely because underwriting margins and investment returns are at cycle highs. There is **no de-rating to buy**.

### 2b. The cyclical-peak tell — forward EPS < trailing EPS

- yfinance **forward EPS $13.69 vs trailing $14.49** → the Street models EPS *down* ~5% [V]. Same pattern across the peer set (TRV, ACGL, CINF, ALL all show fwd EPS < trailing) — **the whole P&C group is at/near an earnings peak.**
- TTM **net-income** ROE (23.8%) is *further* inflated by items that don't repeat at that level: **LP/alternative-investment yield 7.6%** in Q2'26 (vs 1.0% a year earlier), strong **favorable prior-year reserve development (+$111M)**, and discontinued-ops gains. **Core ROE 18.7%** strips some of that out and is the honest figure — still excellent, but itself elevated vs HIG's own 13–17% run in 2021-23.
- Translation: the "cheap" 9.5× trailing P/E is **9.5× peak earnings**. Normalize ROE toward a mid-cycle 14–15% and the multiple on *normalized* earnings is meaningfully higher.

### 2c. Vs. P&C peers — mid-pack on the metric that matters (P/B-per-unit-ROE)

For insurers the clean frame is **P/B relative to ROE** (a higher-ROE book deserves a higher P/B). Live 2026-08-26 [V]:

| | Price | Mkt cap | Trail P/E | Fwd P/E | P/B | ROE | **P/B ÷ ROE** | Div yld |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| **HIG** | $139.85 | $37.9B | 9.7 | 10.2 | **1.97** | 22.1% | **8.9** | 1.7% |
| TRV | $371.03 | $77.4B | 10.0 | 12.3 | 2.34 | 26.5% | 8.8 | 1.4% |
| CB (Chubb) | $343.79 | $132.6B | 12.2 | 11.8 | 1.76 | 14.8% | 11.9 | 1.2% |
| ACGL (Arch) | $100.72 | $34.3B | 7.9 | 10.3 | **1.47** | 19.9% | **7.4** | — |
| CINF | $172.38 | $26.5B | 8.1 | 19.1* | 1.59 | 21.5% | **7.4** | 2.2% |
| ALL (Allstate) | $261.95 | $66.2B | 5.2 | 9.5 | 2.10 | 46.1%* | 4.5 | 1.7% |

*(CINF fwd P/E 19.1 and ALL ROE 46% are distorted by mark-to-market equity-portfolio gains / one-off items — treat as noisy. **[A]**)*

**Read:** On P/B-per-unit-ROE, **HIG (8.9) sits mid-pack — essentially tied with TRV (8.8), cheaper than Chubb (11.9), but MORE expensive than Arch (7.4) and Cincinnati (7.4).** It is **not** the cheapest quality insurer in its own peer group. Arch (higher-quality specialty/reinsurance mix, 1.47× book) and Cincinnati (1.59× book, 2.2% yield) screen cheaper on this frame. HIG is a fairly-priced quality insurer, not a standout bargain.

### 2d. Rough fair value **[A — illustrative, not precise]**

Two anchors:
1. **P/B-on-normalized-ROE (Gordon justified-P/B).** Justified P/B = (ROE − g)/(r − g). On book-ex-AOCI **$78.91**, cost of equity ~9%, growth ~4%:
   - Sustained ROE 18% → justified P/B ~2.8 → too high to be credible through a soft cycle.
   - **Mid-cycle ROE 15% → justified P/B ~2.2 → ~$174** (bull).
   - **Normalizing ROE 13% → justified P/B ~1.8 → ~$142** (base).
   - **Soft-market ROE 11% → justified P/B ~1.4 → ~$110** (bear).
2. **Multiple-on-normalized-EPS.** Normalized core EPS ~$13–14; HIG's own historical ~10× → **~$130–145**.

**Fair-value range ≈ $115–165, midpoint ~$140 [A].** The current $139.85 is **right in the middle** — i.e. roughly **fairly valued**, with the outcome hinging entirely on where P&C underwriting margins and ROE settle as the cycle softens. Analyst mean PT $149.85 (~7% upside) sits just above the midpoint. There is no large margin of safety here.

**Verdict on cheapness:** **Optically cheap, genuinely fair.** The low trailing P/E is a structural feature of insurers, not a discount; HIG trades at a *record* P/B on *peak* ROE with the Street modeling EPS *down*, and it is only mid-pack vs peers on the P/B-vs-ROE frame. This is quality-at-a-fair-price, **not** a value dislocation.

---

## 3. Quality — underwriting, reserves, balance sheet, capital return

### Combined-ratio trend (lower = better; <100 = underwriting profit) **[V]**

| FY | Consolidated P&C CR | BI **underlying** CR |
|---|--:|--:|
| 2021 | 95.8 | 89.1 |
| 2022 | 90.2 | 88.3 |
| 2023 | 89.6 | 87.8 |
| 2024 | 89.9 | 87.9 |
| 2025 | **88.3** | 88.5 |
| Q1'26 | ~ | 89.2 |
| Q2'26 | 91.4 (cat-elevated) | 89.3 |

**Read:** BI *underlying* combined ratio (ex-cat, ex-prior-year-development — the truest measure of current underwriting) has held **~88–89 for five years** — remarkably stable, profitable underwriting. It is **not deteriorating, but also NOT expanding** — margins are flat at a good level, which means the earnings upside from here is not underwriting-margin expansion but volume + investment income + buyback. Q2'26's headline 91.4 was **catastrophe-elevated** ($222M cats: tornado/wind/hail), not a margin break. **[V]**

### Reserves — the watch item **[V]**
- **Net favorable prior-year development** continues (+$111M in Q2'26; BI +$52M, PI +$59M) — a *tailwind*, driven mainly by **workers'-comp releases** (WC has developed favorably for years).
- **BUT the buffer is thinning:** HIG is **strengthening reserves for social inflation in general liability and commercial auto** (litigation financing, rising attorney-representation and bodily-injury severity — the industry-wide 2023-25 problem). Discrete charges: **Q1'26 $70M** legacy 1970s-80s sexual-abuse GL reserve increase; **FY25 $165M** asbestos/environmental increase; FY24 explicit social-inflation language. The favorable-WC vs adverse-GL/casualty dynamic nets to *modestly favorable today* — but WC is itself softening (below), so this offset shrinks over time. **This is the reserve risk to monitor.**

### Investment book — clean, a rate beneficiary **[V, 10-Q 6/30/26]**
- Total invested assets **~$64.0B**; **~95% investment-grade** fixed maturities (BB-and-below only ~4.9%).
- **Commercial mortgage loans $7.31B** (amortized cost), ACL just $49M (0.67%), no past-due/watchlist, 84% at <65% LTV, new originations industrial-weighted at 58% LTV — **CRE is NOT a red flag.**
- **NII $800M in Q2'26 (+22% YoY)**; new-money reinvestment yield ~5.4% vs ~4.8% maturing → **higher-for-longer rates are a tailwind** to the float (the "insurers benefit from higher rates on float" thesis is real and *currently active* here). The flip side: a sharp *rate-cut* cycle slowly compresses NII (a multi-year, not cliff, risk).

### Balance sheet & capital return **[V]**
- Low leverage: ~$4.4B debt vs ~$19B equity. Beta ~0.46.
- **Q2'26 returned $615M** ($450M buybacks + $165M dividends); **new $4.2B buyback authorization (+27%)** running through end-2028. Dividend $0.60/qtr ($2.40/yr), hiked from $0.52 in late 2025.
- Total capital-return yield **~6–6.5%** — with a ~16% net-income payout ratio, the buyback (not the 1.7% dividend) is the per-share engine. Shares out have fallen steadily (~330M issued → ~271M) — **the buyback is the main way this stock compounds per-share at a flat multiple.**

**Quality verdict:** genuinely high-quality — disciplined, stable underwriting; strong sustained ROE; clean balance sheet & investment book; excellent capital allocation. The only quality caveats are the *thinning* reserve cushion (social inflation) and that margins are flat-at-peak rather than improving.

---

## 4. Bear Case / Risks

1. **CYCLICAL-PEAK EARNINGS + SOFTENING P&C MARKET (HIGH — the core risk).** The commercial P&C hard market is **rolling over**. HIG's BI premium growth decelerated from ~10% (2024) → +6% (Q1'26) → +5% (Q2'26). Hartford quotes pricing **"ex-workers-comp"** — the standard industry tell that **WC pricing is flat-to-negative** (and WC is a huge, high-margin book for HIG). Personal-lines renewal pricing is also decelerating (auto +6.8%→+5.5%, home +11.8%→+10.4% Q1→Q2'26). As pricing softens toward loss-cost trend, the ~88-89 underlying combined ratio and ~19% ROE **mean-revert down** — which is exactly what the forward-EPS-below-trailing (§2b) is pricing. **Buying at a full price into a softening cycle is the central bear case.**

2. **RESERVE / SOCIAL-INFLATION RISK (MEDIUM).** Adverse development in general liability & commercial auto from litigation financing / social inflation is an active, industry-wide problem; HIG is already strengthening. The favorable-WC offset that keeps net development positive is itself eroding as WC softens. A larger casualty reserve charge would hit both earnings and the "disciplined reserving" quality premium. Legacy A&E and abuse charges recur in small doses.

3. **CATASTROPHE / CLIMATE EXPOSURE (MEDIUM).** As a commercial-heavy CA writer, HIG took **$325M net from the 2025 California wildfires** (BI $207M / PI $118M). 2026 cats have normalized (~$220–230M/qtr, no CA wildfire), but climate-driven cat volatility is a structural, lumpy tail risk that can turn any quarter's combined ratio (as Q2'26's 91.4 showed).

4. **RATE SENSITIVITY OF THE FLOAT (LOW-MEDIUM, two-sided).** NII is currently a *tailwind* (higher reinvestment yields). A sustained rate-cut cycle would slowly compress the ~$64B portfolio's yield and the LP/alternatives income that boosted recent ROE. This is a slow bleed, not a cliff — and it partly *hedges* Hooman's book (see §6).

5. **VALUATION HAS NO MARGIN OF SAFETY (MEDIUM).** At the midpoint of a $115–165 fair-value band, near a 52-week high, at record P/B on peak ROE, there is little cushion if either underwriting or investment returns disappoint. Downside to a soft-market re-rate (~$110–120) is comparable to the ~7% analyst upside.

6. **Minor:** EB margin softening (7.4% vs 9.2%); Equitable-EB integration risk; Hartford Funds sale books a ~$150M after-tax loss. None thesis-breaking.

**No red flags on management** (CEO/Chairman Christopher Swift and President Mo Tooker both in place; CFO Beth Costello; A+ AM Best affirmed 2026-07-22).

---

## 5. Catalyst / Timing — why it re-rates (or why the cheapness is *earned*)

**The honest answer: there is no obvious near-term re-rating catalyst, because there is nothing to re-rate FROM — it's already near highs at a normal multiple.** The bull path is *compounding*, not *re-rating*:
- **Per-share compounding via buyback** ($4.2B authorization at ~2× book) + ~10% book-value growth + 1.7% dividend → a plausible **~high-single-digit to low-double-digit total return** IF underwriting margins hold and the cycle stays benign.
- **NII tailwind** persists while rates stay high.
- **Simplification** (Hartford Funds sale) + EB scale (Equitable deal) modestly improve the mix and free capital.

**The bear/"cheapness-is-earned" path** is the more likely explanation for *why it's not more expensive*: the market correctly senses this is **peak-cycle earnings**, prices EPS to decline, and holds the multiple flat — so the stock drifts with book value while margins slowly compress. **The re-rate that actually matters is a DE-rate**: a genuine soft-market air-pocket (a couple of quarters of rising combined ratios + adverse casualty development) could take HIG to ~$110–120 (P/B-ex-AOCI ~1.4–1.5) — **which is the price at which it becomes a genuine quality-at-a-discount buy.** Timing favors patience.

---

## 6. Fit for Hooman

**Context:** small Financials sleeve — CI (managed-care, cheap-quality) + BRK-B (~2.5% target, underweight). Stagflation-defensive tilt; wants defensive, rate-benefiting, uncorrelated diversifiers.

- **Defensive quality? YES.** Beta ~0.46, A+ balance sheet, ~6% capital-return yield, low correlation to his commodity/AI book. This is genuinely the *kind* of thing his completeness work flagged (insurance/reinsurance gap, grade 6/10) — a cheap-ish, uncorrelated, rate-on-float beneficiary.
- **Stagflation / higher-rates fit? PARTIAL-YES.** Rising float yields are a live tailwind (NII +22%), so HIG *does* express "insurers benefit from higher rates." **BUT** the stagflation *shock* also brings the two things that hurt P&C insurers most: **social-inflation casualty-reserve pressure** and **cat-cost inflation** (rebuild costs). So it's a rate-on-float beneficiary but a claims-inflation *victim* — a wash more than a clean stagflation hedge.
- **⚠️ DOES IT DUPLICATE BRK-B? PARTIALLY, YES.** BRK-B is, at its core, a **P&C insurance-float compounder** (GEICO + Berkshire Hathaway Reinsurance / Primary). Adding HIG **stacks a second P&C-insurance-cycle bet** on the sleeve — same cat exposure, same soft-market risk, same casualty-reserve risk, correlated underwriting cycle. It is *not* orthogonal to BRK-B the way CI (health) is. For a 2.5%-target, deliberately-underweight sleeve, doubling the P&C exposure is questionable diversification.
- **Vs. the incumbent plan:** his own research already picked **BRK-B as the "elegant single-name" insurance compounder** (cash-rich, un-levered, self-hedging) and CI as the cheap-quality health name. HIG is a *good* insurer but adds P&C-cycle/cat risk that BRK-B already carries more conservatively, at a fuller point in the cycle, with less margin of safety. If he wants *more* insurance beta, Arch (ACGL) or Cincinnati (CINF) screen cheaper on P/B-vs-ROE; if he wants *diversified* financials, a bank or exchange (not a third insurer) fills a real hole.

**Sleeve verdict:** a fine defensive name in isolation, but **redundant with BRK-B** and bought at the wrong point in the cycle for a value investor. Not a priority add.

---

## 7. Scorecard & Verdict

**Weights (CLAUDE.md §3):** Cheapness 30 / Quality 30 / Trap-risk-inverse 20 / Moat 15 / Catalyst 5. Scores 0–10.

| Factor | Wt | Score | Wtd | Rationale |
|---|--:|--:|--:|---|
| **Cheapness** | 30% | **4** | 1.20 | Optically cheap (9.7× P/E) but that's *structural* for insurers; near 52-wk high, **record ~2.0× book on peak ~19-22% ROE**, forward EPS *below* trailing, only mid-pack vs peers on P/B-per-ROE (Arch/CINF cheaper). Fair, not cheap. No margin of safety. [V] |
| **Quality** | 30% | **8** | 2.40 | Genuinely high: 18.7% sustained core ROE, ~88-89 underlying CR stable 5 yrs, ~10-12% book-value compounding, A+ AM Best, clean 95%-IG investment book, ~6% capital-return yield, low leverage. Docked only for thinning casualty-reserve cushion + flat-at-peak (not expanding) margins. [V] |
| **Trap-risk (inverse)** | 20% | **5** | 1.00 | Real cyclical-peak trap: softening P&C market (esp. WC), forward EPS modeled down, social-inflation GL/auto reserve pressure, cat/CA-wildfire tail. Not a *broken* business — just the wrong cycle point. [V] |
| **Moat & leadership** | 15% | **6** | 0.90 | Moderate/durable: small-commercial scale, WC leadership, sticky **AARP personal-lines affinity**, top-tier group benefits; strong disciplined management. Not a wide moat — P&C is competitive/commoditizing in a soft market. [V] |
| **Catalyst** | 5% | **4** | 0.20 | No re-rating catalyst (already near highs at a normal multiple); return = buyback + book growth. The catalyst that *matters* is a de-rate that creates a better entry. [A] |
| **TOTAL** | 100% | | **5.70 / 10** | |

### VERDICT: **WATCH** (high-quality insurer, fair price, wrong cycle point — and redundant with BRK-B)

HIG scores **5.7/10**. It is a **genuinely high-quality, well-run, defensively-postured insurer** — but the screen's "newly cheap" flag is **misleading**: the low P/E is structural, the stock sits near its 52-week high at a *record* P/B on *peak* ROE with the Street pricing an earnings decline, and it's only mid-pack cheap versus its own peer group. This is **quality-at-a-fair-price at a cyclical earnings peak**, not a value dislocation — the opposite of the INTU-style "crashed compounder" setup. For Hooman specifically it **duplicates BRK-B's P&C-insurance-float bet** (correlated cat/soft-market/reserve risk), so it's weak diversification for a 2.5%-target, underweight sleeve.

**Recommendation:** **WATCH, do not buy at ~$140.** Revisit as a genuine quality-at-a-discount buy only if a soft-market air-pocket (rising combined ratios + adverse casualty development over 1-2 quarters) takes it toward **~$110–120 (P/B-ex-AOCI ~1.4–1.5)**. If he wants to *add* insurance beta before then, **Arch (ACGL) or Cincinnati (CINF) screen cheaper on P/B-vs-ROE**; if he wants to fill the Financials hole with something *non-redundant*, a bank/exchange/asset-manager diversifies better than a third insurer stacked on BRK-B.

**Rough fair value: $115–165, midpoint ~$140 [A]** — i.e. roughly where it trades. Buy zone: **≤$120.**

---

## Appendix — Verification Log & Sources

**Live data pulls (2026-08-26):**
- yfinance pull 2026-08-26T20:14Z — `data/cache/yf_HIG.json`, `yf_{TRV,CB,ACGL,CINF,ALL}.json`, summary `data/cache/hig_peers_summary.csv`. HIG: price $139.85, mkt cap $37.9B, trail P/E 9.65, fwd P/E 10.2 (fwd EPS $13.69 < trail $14.49), P/B 1.97, EV/EBITDA 6.83, ROE 22.1%, beta 0.46, div yld 1.7%, shares 270.9M, 52-wk $120.33–$146.07, analyst mean PT $149.85. **[V]**
- EDGAR company-facts (CIK 0000874766), UA "Hooman Shariati hshariati@adobe.com" — `data/cache/edgar_HIG.json`: FY25 net income $3.836B, equity $18.979B, assets $85.997B, LT debt $4.371B. yfinance financials: FY25 total revenue $28.07B, diluted EPS $13.32, BVPS trend. **[V]**

**Primary SEC filings (EDGAR, CIK 0000874766):**
- **Q2 2026 earnings** 8-K EX-99.1, filed 2026-07-23: https://www.sec.gov/Archives/edgar/data/874766/000087476626000059/ex991earningsnewsrelease63.htm — net income to common $1.293B/$4.68 dil; **core earnings $945M/$3.42 dil**; **core ROE 18.7%** (net-income ROE 23.8%); **BVPS $70.28, ex-AOCI $78.91**; **P&C combined 91.4**, BI 91.4 / underlying 89.3, PI 90.1 / underlying 86.3; EB margin 7.4%; **NII $800M (+22%)**; cats $222M; **net favorable PYD +$111M**; P&C written premium +3%, BI +5%, PI −7%; renewal pricing auto +5.5%, home +10.4%. **[V]**
- July-15 8-K (filed 2026-07-15): board appointment (Randy Larsen), **NOT** a Hartford Funds / buyback release — confirms Swift remains Chairman & CEO. **[V]**
- Recent filings list: 10-Q 6/30/26 (2026-07-23, acc 0000874766-26-000060); 10-K FY25 (2026-02-20); 8-Ks 2026-06-03 (Hartford Funds sale), 2026-08-11. **[V]**

**Historical ratios:** stockanalysis.com/stocks/HIG/financials/ratios (2026-08-26) — P/E & P/B & ROE 2021-25 table in §2a. **[V]**

**Research pass (background agent, 2026-08-26)** — cross-verified against primary filings above:
- Combined-ratio trend 2021-25 (consolidated + BI underlying); FY25 core ROE 19.4%, CR 88.3; Q1'26 core EPS $3.09, BI CR 94.8/underlying 89.2. **[V]**
- **Hartford Funds → Wellington Management** sale announced 2026-06-03, now discontinued ops, close ~Q1'27, ~$150M after-tax loss; NPV collar $1.5B–$2.1B (press "$1.9B" = **[A]**, not in filing). **[V for the sale; A for the $ figure]**
- **Equitable employee-benefits acquisition** announced 2026-08-04 (~$500M premium), close ~Q4'26. **[V]** — purchase multiple not disclosed **[U]**.
- **AARP personal-lines book STILL ACTIVE** (not exited) — corrects the 2023-24 "exit" reports. **[V]**
- Social-inflation reserve strengthening in GL/commercial auto; Q1'26 $70M legacy-abuse GL charge; FY25 $165M A&E. WC still releasing favorably. **[V]**
- New $4.2B buyback (+27%) eff. 2026-08-01 thru end-2028; $2.40/yr dividend. **[V]**
- Investment book: ~$64B invested assets, ~95% IG, CML $7.31B (ACL 0.67%, no watchlist) — CRE not a red flag. **[V]**
- 2025 CA wildfire net cat loss $325M (BI $207M / PI $118M). **[V]**
- AM Best A+ affirmed 2026-07-22; CEO Swift & President Tooker in place. **[V]**

**Explicit gaps / [U] items:** consolidated portfolio *duration* (not in 10-Q; would need 10-K); exact per-line renewal-pricing incl. the WC figure (only in call transcripts); Equitable-EB purchase multiple; Hartford Funds precise NPV; exact 1-yr total return. None affect the verdict.

**Confidence key:** [V] = primary filing (EDGAR) or ≥2 agreeing feeds · [A] = my derivation/single-source · [U] = flagged, not relied upon. Prices as-of 2026-08-26 and will move. **Research, not financial advice.**
