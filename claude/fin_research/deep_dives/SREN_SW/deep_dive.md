# Stage 4 Deep Dive — Swiss Re (SREN.SW)

**Company:** Swiss Re AG — global reinsurance leader, HQ Zürich, Switzerland. Listed SIX (SREN.SW),
trades CHF; **reports financials in USD**. ADR: SSREY.
**Analyst:** Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.**
**Written:** 2026-07-02. **Screen snapshot verified** below.

> **ANTI-HALLUCINATION.** Every figure carries a source + as-of date. yfinance figures are a
> **VERIFIED** real fetch (2026-07-02) but cross-checked vs company-reported results relayed by
> specialist reinsurance media (artemis.bm, reinsurancene.ws) — Swiss Re is **not a US filer, no
> EDGAR**; swissre.com and reuters.com blocked to fetching, so company results are cited via those
> two independent specialist outlets (most figures corroborated across both). Confidence marked
> VERIFIED / ASSUMED / UNVERIFIED throughout. **Accounting-basis break:** Swiss Re reported **US
> GAAP through FY2023, IFRS from FY2024** — do NOT compare a pre-2024 combined ratio or ROE to a
> post-2024 one without noting the restatement.

---

## 0. Screen snapshot — VERIFIED

yfinance `.info` pull, **as-of 2026-07-02** (`SREN.SW`), matches the brief's snapshot exactly:

| Metric | Value | Note |
|---|--:|---|
| Price currency | CHF | financialCurrency = **USD** (Swiss Re reports USD) |
| Market cap | ~CHF 38.3bn | native CHF |
| P/E (trailing) | **10.31** | EPS 12.59 |
| P/E (forward) | 9.92 | |
| P/B | **1.82** | book value/sh 71.53 |
| ROE | **19.5%** | |
| ROA | 3.20% | |
| Dividend yield | **4.84%** | payout ratio 47.3% |
| Beta | 0.35 | low-beta (insurance) |
| Net income (TTM) | **USD 4.855bn** | matches co-reported FY2025 record |
| earningsGrowth | +18.6% | |

Screen (financials_screen_ranked.csv) had P/B 1.81, P/E 10.3, ROE 19.5%, DY 4.84%, trap-PASS,
score 69 within DEV_EXUS reinsurers — **all reproduced**. The TTM net income ($4.855bn) lines up
with the company-reported **FY2025 record $4.8bn** (§3), so the trailing multiples reflect
peak-cycle earnings, not a stale snapshot. **VERIFIED.**

---

## 1. Business & Thesis

**What it is.** One of the world's two largest reinsurers (with Munich Re). Founded 1863 (Glarus
fire). ~14,000 staff, ~80 offices, 29 countries (Wikipedia, 2026-07-02). Three divisions:
- **P&C Re** — property & casualty reinsurance. The cyclical engine; nat-cat + casualty. FY2025
  net income **USD 2.8bn** (reinsurancene.ws, 2026-02-27).
- **L&H Re** — life & health reinsurance. Steadier, longer-tail. FY2025 net income **USD 1.3bn**.
- **Corporate Solutions** — commercial primary/large-corporate insurance. FY2025 net income
  **$988m**, CR 86.5%.

FY2024 it became **#1 global reinsurer by revenue among IFRS-17 reporters ($36.2bn)**, ahead of
Munich Re ($32.6bn), Hannover Re ($27.5bn), SCOR ($16.8bn) (artemis.bm AM Best ranking,
2025-08-18). VERIFIED.

**The value thesis (why it's on the finalist list).** Best developed-ex-US insurer in the
financials screen: a fortress-balance-sheet global #1 at **1.8× book / ~10× earnings / ~4.8%
yield**, delivering **~20% ROE**, with a **never-cut, explicitly progressive dividend (7%+/yr
target 2025–27)** plus buybacks — quality-at-a-price, diversifying Hooman's book into
developed-ex-US financials and a low-beta (0.35), low-correlation-to-equities insurance cash
machine. The bull case is capital return + underwriting discipline through the cycle.

**Where are we in the reinsurance pricing cycle? (the central question — answered in §2/§5.)**
Short version: the **hard market has clearly peaked and is now softening**. Rates hardened
violently at Jan-2023 renewals (Guy Carpenter global property-cat rate-on-line **+27.2%**), then
decelerated in 2024, turned **negative for the first time since 2017 at Jan 2025 (−6.6% global)**,
and are in **accelerated softening into 2026 (Jan-2026 −12% global, −15% Europe)** (artemis.bm,
2024-01-09 / 2025-01-06 / 2025-12-31). So current profitability is being earned **at/near a
cyclical peak** on pricing — the crux of the valuation debate.

---

## 2. Valuation

### 2a. Multiples vs peers (all stockanalysis.com, **2026-07-02**; UNVERIFIED vs a 2nd source per name)

| Reinsurer | P/E | P/B | Div yield | ROE |
|---|--:|--:|--:|--:|
| **Swiss Re (SREN.SW)** | **10.3** | **1.82** | **4.84%** | **19.5%** (yfinance, co-reported FY25 19.6%) |
| Munich Re (MUV2.DE) | 9.4 | 1.80 | 4.91% | 19.9% |
| Hannover Re (HNR1.DE) | 10.2 | 1.97 | 5.14% | 21.7% |
| SCOR (SCR.PA) | 6.6 | 0.86 | 6.0% | 13.2% |
| Everest Group (EG) | 7.3 | 0.94 | 2.2% | 13.8% |

**Read (ASSUMED interpretation of VERIFIED multiples):** Swiss Re sits **mid-pack among the big-3
European reinsurers** — essentially in line with Munich Re on P/B (1.80–1.82) and a touch below
Hannover Re (1.97, highest-quality premium, highest ROE 21.7%). The **cheaper names (SCOR 0.86×,
Everest 0.94×) are cheap for a reason** — lower ROE (13%) and, for SCOR, a history of reserve/L&H
volatility. So Swiss Re is **NOT the cheapest reinsurer on P/B**; it is the *quality #1 at a fair,
not screaming, multiple*. The ~1.8× book is a **premium to book that only makes sense if ~19–20%
ROE is durable** — and that is precisely what the pricing cycle threatens (see below).
P/B ≈ P/E × ROE sanity check: 10.3 × 0.195 ≈ 2.0, roughly consistent with 1.8× (VERIFIED-consistent).

### 2b. vs own history — is ~20% ROE a cyclical peak? (the key call)

Swiss Re group ROE & P&C Re combined ratio, FY2019–FY2025 (**US GAAP through 2023, IFRS from
2024** — break noted; sources artemis.bm + reinsurancene.ws FY-results articles per year):

| FY | Group ROE | P&C Re combined ratio | Note |
|---|--:|--:|---|
| 2019 | n/a (NI $727m) | **107.8%** | pre-hard-market, weak underwriting |
| 2020 | **negative** (net LOSS $878m) | **109%** (96.9% ex-COVID) | COVID + nat-cat trough |
| 2021 | **5.7%** | 97.1% | recovery |
| 2022 | **2.6%** | 102.4% (96.9% norm.) | nat-cat + inflation hit |
| 2023 | 22.3% USGAAP / **16.2% IFRS** | 94.8% USGAAP / **85% IFRS** | hard market earning through |
| 2024 | **15% (IFRS)** | **89.9% (IFRS)** | *missed target — $3.1bn reserve build (§3)* |
| 2025 | **19.6% (IFRS)** | **79.5% (IFRS)** | *record; net income $4.8bn* |

**Cyclical-peak assessment (ASSUMED, argued both sides):**
- **Yes, this is a cyclical peak.** The clean **79.5% P&C Re combined ratio and 19.6% ROE in FY2025
  are the best in the series and coincide with the top of the pricing cycle** (rates peaked Jan
  2023, still elevated in absolute terms through 2025). The average through-cycle ROE is far lower:
  2019–2022 was two loss/near-loss years and two single-digit ROEs. A 79.5% CR is **not a
  mid-cycle number** for a reinsurer — mid-80s to high-80s is more normal. As rates soften (−6.6%
  in 2025, −12% in 2026), and assuming a normal-to-heavy nat-cat year eventually lands, the
  combined ratio should drift back toward the mid-80s and ROE toward the mid-teens.
- **No / partly, it's more durable than it looks.** (1) Reinsurers reset **terms & conditions**
  (attachment points, exclusions) in 2023 that persist even as rate softens — Swiss Re's Jan-2026
  book was +0.3% headline / −4.3% net-of-loss-model but **still consistent with a sub-85% CR
  target** (artemis.bm, 2026-02-27), i.e. discipline held. (2) Higher interest rates lift
  **investment/recurring income** structurally vs the 2019–21 ZIRP years — a tailwind that persists
  even if underwriting softens. (3) The 2024 reserve rebuild (§3) means FY2025 earnings are
  arguably *cleaner/under-reserved-risk-lower* than headline. So a soft landing to mid-teens ROE
  (not a collapse) is plausible.
- **Verdict:** current ROE is **near a cyclical peak — treat ~19–20% as unsustainable and underwrite
  to a normalized ~13–16% ROE.** At 1.8× book, the stock is priced closer to the peak than to that
  normalized level, which is why the multiple isn't cheap and sell-side is cautious (§5).

### 2c. Currency note
Swiss Re **reports in USD** but the SREN.SW share trades in **CHF**; the dividend was historically
declared in CHF and **switched to USD declaration from FY2024** (dividendmax, 2026-07-02). A
CHF-based investor bears USD/CHF translation on both earnings and (now) the dividend. yfinance
ROE/P/B/P/E are currency-neutral ratios (safe); market cap is native CHF (do not cross-compare).

---

## 3. Quality

- **ROE trend:** see §2b table. FY2025 **19.6%** (co-reported); interim ran even hotter — Q1 2025
  22.4%, H1 2025 23%, 9M 2025 22.5% (reinsurancene.ws/artemis.bm, 2025-05-16 / 08-14 / 11-14).
  High-quality *at the cycle top*. VERIFIED.
- **P&C Re combined ratio (the key metric):** FY2025 **79.5%** (co-reported), well inside the
  <85% target; FY2026 target **<85%** (reinsurancene.ws, 2026-02-27). This is the number to watch
  as rates soften — VERIFIED as of FY2025, but structurally cyclical.
- **The 2024 reserve strengthening (brief flagged this — CONFIRMED, and larger than a single item).**
  Two actions under new CEO **Andreas Berger** (started 2024-07-01):
  - H1/Q2 2024: ~**$1.15bn** (nat-cat/man-made $500m + **$650m casualty IBNR**) (artemis.bm,
    2024-08-22).
  - **Q3 2024: USD 2.4bn strengthening of US liability (casualty) reserves** after a comprehensive
    review for legal/social-inflation trends (reinsurancene.ws, 2024-11-07).
  - **9M 2024 total P&C Re reserve additions: $3.1bn**, adding **+13.3 pts** to the combined ratio
    (→ 92.8% at 9M) (reinsurancene.ws/artemis.bm, 2024-11-14). This is **why FY2024 ROE was only 15%
    and the CR (89.9%) missed target.**
  - **Berger's stated goal:** "positioning overall P&C reserves at the **higher end of our
    best-estimate range**" (reinsurancene.ws, 2024-11-14; reaffirmed 2025-02-27). VERIFIED.
  - **Read:** a big negative in 2024 but a **quality-positive going forward** — a new-CEO "clean the
    decks" reserve reset to conservative confidence, which de-risks the reserve tail and is *part
    of why* FY2025 could print a clean 79.5% CR. It also flags a genuine US-casualty
    social-inflation risk that hit the whole industry (see §4).
- **Capital / SST solvency:** **257%** year-end 2024, **264%** at 1-Jul-2025, **250%** at 1-Jan-2026
  — at/above the top of the **200–250% target range** (reinsurancene.ws 2025-03-13; artemis.bm
  2025-08-14, 2026-02-27). Fortress capital; supports buybacks. VERIFIED.
- **Dividend track record + special returns:** **never cut in a decade.** Regular DPS (native):
  CHF 4.60 (FY15) → 6.80 (FY23) → **USD 7.35 (FY24, +8%)** (dividendmax, 2026-07-02). During 2020
  COVID it **raised** the dividend (to CHF 5.90) while **cancelling the buyback** — a
  dividend-priority signal. Special dividends 2013–15 (CHF 7.50 / 8.00 / 7.25). Buybacks: CHF 1.0bn
  (2017, 2019), cancelled 2020, and **USD 1.5bn approved with FY2025 results** ($500m recurring +
  $1bn extraordinary) plus ~9% dividend hike at the 2026 AGM. Explicit policy: **DPS growth 7%+/yr,
  2025–27** (reinsurancene.ws, 2025-03-13). Payout ratio ~47% (yfinance) — well covered. VERIFIED.
- **L&H Re earnings:** FY2025 net income **$1.3bn** but *below* the ~$1.6–1.7bn target and the 9M
  run-rate was flagged as likely to miss (reinsurancene.ws, 2025-11-14 / 2026-02-27). FY2026 L&H
  target **$1.7bn**. L&H is the steady leg but has under-delivered vs plan — a minor quality watch.
  VERIFIED.

---

## 4. Bear Case / Risks

1. **Pricing-cycle turn (the #1 risk — see §2b/§5).** Rates negative since Jan 2025 and softening
   at double digits into 2026; JPMorgan noted mid-2025 pricing "almost on par with 2023"
   (artemis.bm, 2025-05-08). A prolonged soft market compresses the combined ratio back toward
   mid-80s+ and ROE toward the low-teens — from which 1.8× book looks full. Peel Hunt modeled ~35%
   cumulative rate declines over five years (artemis.bm, 2025-01-06). **Core bear thesis.**
2. **Major-catastrophe year / nat-cat volatility.** A reinsurer's earnings are inherently lumpy;
   FY2025's clean CR partly reflects a *benign* large-loss year. The 2025 LA wildfires cost Swiss
   Re ~$570m (artemis.bm, 2025-05-16) and it still printed records — but a single $1bn+ event or a
   heavy hurricane season, arriving *as rates soften*, is the classic double-hit. 2024 global
   insured cat losses were >$140bn (artemis.bm, 2025-08-18) — the backdrop is not benign.
3. **Reserve-deficiency history / US casualty social inflation.** The **$3.1bn 2024 reserve build**
   proves the tail risk is real; US liability social/legal inflation is an industry-wide,
   hard-to-model creep. Berger's "higher-end best-estimate" reset *reduces* but does not eliminate
   the risk of further additions if court-award inflation keeps running.
4. **Investment-portfolio / rate risk.** Higher rates *help* recurring income but a sharp
   rate move hits bond marks and, for L&H, discounting; a rate *cut* cycle would trim the
   investment-income tailwind that currently props ROE.
5. **Big-loss tail / model risk.** Pandemic (COVID cost Swiss Re ~$3.9bn cumulatively — artemis.bm
   FY2020), a mega-cat, or a casualty "black swin" can produce a loss year (as 2020 did: net loss
   $878m). Low beta ≠ low tail risk.
6. **Valuation/sentiment.** Sell-side is **distinctly bearish**: European consensus 0 Strong-Buy /
   1 Buy / 8 Hold / 4 Sell / 3 Strong-Sell → "Sell"; average CHF price target ~129 ≈ current price
   (stockanalysis.com, 2026-07-02). A 2026 downgrade cluster (Goldman→Sell, UBS→Sell, Morgan
   Stanley UW, RBC, Barclays) explicitly cites **soft-cycle pressure + full valuation**. The market
   already sees the peak.

**Bull rebuttal (both sides):** T&Cs stayed disciplined into 2026 (Swiss Re still guides sub-85% CR
on a −4.3% net-price book), higher-for-longer rates support investment income, the reserve reset
de-risks the tail, SST 250% funds buybacks, and the dividend is progressive and never-cut. If ROE
soft-lands to mid-teens rather than collapsing, 1.8× book with a 4.8% yield is *reasonable*, not
expensive.

---

## 5. Catalysts, Reinsurance-Cycle Call & Verdict

**Catalysts (mostly modest / slightly negative-skewed):**
- (+) Continued capital return: $1.5bn buyback + 7%+ progressive dividend; possible further
  extraordinary returns given SST 250%.
- (+) FY2026 targets ($4.5bn net income, P&C Re CR <85%, L&H $1.7bn) — if hit despite softening
  rates, validates T&C discipline and durability.
- (−) **Softening renewals (Jan/Apr/Jun 2026)** are the dominant swing factor and are trending
  *against* the stock; each renewal season is now a "how bad is the softening" event.
- (−/neutral) Nat-cat season outcome (a benign year extends the record; a heavy year exposes the
  cycle turn).

**Reinsurance pricing-cycle-peak call (explicit, per brief):** **The hard market has peaked. We are
past the top and into a softening phase.** Evidence is unambiguous — Guy Carpenter global
property-cat rate-on-line: **+27.2% (Jan 2023 peak) → +5.4% (Jan 2024) → −6.6% (Jan 2025, first
decline since 2017) → −12% (Jan 2026, accelerating; −15% Europe)** (artemis.bm, 2024-01-09 /
2025-01-06 / 2025-12-31). Therefore **Swiss Re's FY2025 ~79.5% combined ratio and ~19.6% ROE should
be read as at/near a cyclical peak** and normalized to the mid-teens ROE / mid-80s CR for
valuation. This is the single most important framing for the name. (Confidence: cycle direction
**VERIFIED**; degree of ROE mean-reversion **ASSUMED**.)

### Scorecard (CLAUDE.md §3 weights)

| Factor | Weight | Score /10 | Weighted | Rationale |
|---|--:|--:|--:|---|
| **Cheapness** | 30% | **5** | 1.50 | 1.8× book / 10× earnings / 4.8% yield is *fair, not cheap* — mid-pack vs peers, and the earnings/ROE that justify 1.8× are **at a cyclical peak**. Not the cheapest reinsurer (SCOR/Everest sub-book). |
| **Quality** | 30% | **8** | 2.40 | Global #1, fortress SST 250%, 79.5% CR, never-cut progressive dividend, disciplined T&Cs. Docked for L&H target miss and the cyclicality of the "quality." |
| **Trap risk (inverse)** | 20% | **7** | 1.40 | Trap-gate PASS; earnings *rising* not collapsing; but the 2024 $3.1bn reserve build + peak-cycle earnings mean the trailing multiple flatters — real risk the "cheap on 10× P/E" is 10× *peak* earnings. |
| **Moat & leadership** | 15% | **8** | 1.20 | Scale, data/pricing sophistication, capital, diversification (P&C+L&H+CorpSol), #1 global. Reinsurance is genuinely oligopolistic (Swiss/Munich/Hannover). New CEO reset reserves credibly. |
| **Catalyst** | 5% | **4** | 0.20 | Capital return is a plus but the dominant catalyst (renewals) skews negative; sell-side bearish, target ~flat. |
| **TOTAL** | 100% | | **6.70 / 10** | |

### VERDICT: **WATCH** (lean-positive quality name, but bought at the wrong point in the cycle)

Swiss Re is a genuinely high-quality, fortress-capitalized global #1 reinsurer returning cash
generously — but at **1.8× book on peak-cycle ~20% ROE**, with reinsurance rates now **softening at
double digits** and sell-side broadly at Sell, the risk/reward is **fair, not compelling**. It is a
**WATCH**, not a BUY-worth-more-work: the thing that would flip it to BUY is a **de-rating toward
~1.3–1.4× book (a soft-market or big-cat drawdown) while the balance sheet and dividend stay
intact** — i.e., buy the quality #1 *after* the cycle scares the multiple down, not at the peak. Of
the finalist insurers, the cheap-EM-life cohort (China Taiping at 0.71× book / 25% ROE) offers more
absolute cheapness; Swiss Re offers more safety and a cleaner balance sheet but less margin of
safety on valuation.

---

## 6. Sources & Confidence

- **yfinance** SREN.SW `.info`, 2026-07-02 — screen multiples (P/E, P/B, ROE, yield, EPS, NI).
  **VERIFIED** real fetch; matches screen + co-reported FY2025 NI.
- **reinsurancene.ws** & **artemis.bm** — company-reported FY2024 (2025-02-27), FY2025 (2026-02-27),
  interim 2024/2025 results; the $3.1bn / $2.4bn reserve actions; SST ratios; dividends/buybacks;
  Guy Carpenter rate-on-line index (Jan 2023/24/25/26); AM Best reinsurer ranking (2025-08-18).
  Specialist reinsurance media relaying Swiss Re's own releases — **VERIFIED** (most figures
  corroborated across both outlets); primary swissre.com blocked (no EDGAR — not a US filer).
- **stockanalysis.com / marketbeat.com** — peer multiples (MUV2.DE, HNR1.DE, SCR.PA, EG) and
  analyst consensus/targets, 2026-07-02. **UNVERIFIED** vs a 2nd source per name; ADR-EPS artifacts
  possible on Swiss Re's own P/E there (co-reported ROE used as the anchor instead).
- **dividendmax.com** — dividend history, 2026-07-02. **VERIFIED** (native-currency series).
- **Wikipedia** — business overview / segment structure / history, 2026-07-02.
- **Could NOT verify:** exact USD size of the *FY2024*-results buyback (Feb 2025); exact FY2025 DPS
  amount (only the ~9% hike is confirmed); peer multiples at a mid-2025 date (only current live);
  FY2019/2020 ROE as a % (only net income/loss stated). Flagged inline.
- **Interpretation confidence:** cycle-direction **VERIFIED**; cyclical-peak ROE mean-reversion,
  scorecard, and verdict are my **ASSUMED** judgment.
