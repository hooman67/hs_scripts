# Deep Dive — China Pacific Insurance (CPIC / 中国太保) — 2601.HK (also 601601.SS, LSE GDR "CPIC")

**Stage 4 deep dive.** Run 2026-07-02 by Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.**
Second name in the EM-Life-Insurance cohort (Stage 1a's top cheap-quality EM sector). Flagged at
screening: cheap partly on **trough earnings** (`earningsGrowth ≈ −6%`) — crux question is
**cyclical-trough vs structurally-broken**.

> **Anti-hallucination note.** yfinance figures (P/B, P/E, ROE, yield) are VERIFIED live fetches
> (`2601.HK` info, 2026-07-02) but yfinance **lacks the metrics that matter for a life insurer**
> — Embedded Value (EV), Value of New Business (VNB), P/EV, C-ROSS II solvency, investment mix,
> combined ratio. Those come from **CPIC's own HKEX/SSE results filings** (PDF URLs cited inline),
> parsed directly by a research sub-agent. Third-party corroboration (Reuters/Bloomberg/rating
> agencies) was largely **blocked** in this environment, so most EV/VNB/profit figures rest on
> CPIC's authoritative **primary filings** — noted where it matters. Confidence: VERIFIED /
> ASSUMED / UNVERIFIED marked throughout. Peer P/EV multiples are **DERIVED** arithmetic (price ÷
> filed EV), not sourced analyst multiples.

---

## 0. Snapshot (VERIFIED yfinance, 2026-07-02, native HKD)

| Metric | 2601.HK (CPIC) | Source |
|---|--:|---|
| Price | HKD 27.50 | yfinance |
| Market cap | HKD 264.6 bn (H-share line); total group ~HKD 311 bn incl. A-shares | yfinance |
| P/B | **0.72x** | yfinance |
| Trailing P/E | **4.35x** | yfinance |
| Forward P/E | 4.33x | yfinance |
| ROE | **17.4%** | yfinance |
| Dividend yield | **4.92%** | yfinance |
| `earningsGrowth` (the flag) | **−6%** | yfinance |
| `earningsQuarterlyGrowth` | +4.3% | yfinance |
| Beta | 0.50 | yfinance |
| Payout ratio (yf) | 19.7% | yfinance |

Screen snapshot (financials_screen.md, 2026-07-02) matches: P/B 0.72, P/E 4.4, ROE 17.4%, DY 4.92%,
trap-gate **PASS**, score **58** (3rd of the EM-life cohort behind Taiping 65 / NCI 62).

**The `−6%` earnings-growth flag is a stale/trailing artifact.** yfinance's own
`earningsQuarterlyGrowth` is already **+4.3%**, and the filings (below) show FY2024 net profit
**+64.9%** and 1H2025 **+11.0%**. The trough was **FY2023**, already two years in the past — the
screen caught CPIC on a lagging momentum reading, not a live decline.

---

## 1. Business & Thesis

**What CPIC is.** China Pacific Insurance (Group) is one of China's top-3 domestic insurers by
premium, a Shanghai-headquartered **central-Shanghai-SASAC-linked SOE**, dual-listed A (601601.SS,
2007) + H (2601.HK, 2009) with a **London GDR** (SSE–LSE Stock Connect, ticker CPIC). Two core
engines:
- **CPIC Life** — agency-led life & health (~78% of new business via tied agents), the higher-margin,
  EV-generating engine (~56% of group).
- **CPIC P&C** — motor + non-auto property & casualty (~44%), underwriting-profitable.
Plus asset management (CPIC AMC), pension, health, and a growing investment-property book.

**The value thesis (why 0.72x book).** A top-3 Chinese insurer with ~16–17% normalized ROE trades
at **0.72x book / ~0.48–0.51x embedded value** (A-share basis, DERIVED §2). Below-book pricing on a
franchise still compounding EV mid-to-high single digits, plus a covered ~5% yield, is a classic
cheap-quality-EM setup. The whole China-lifeco sector de-rated 2022–2024 on falling rates + a weak
equity market + property fears; CPIC caught the de-rating despite an intact, scaled agency franchise.

**Cyclical-trough vs structurally-broken — the crux, resolved: CYCLICAL TROUGH (VERIFIED from
filings).** Three independent lines of evidence, all pointing the same way:

1. **The earnings trough was FY2023 and it has already reversed.** Net profit attributable to
   shareholders (IFRS 17/9 basis, RMB): FY2022 **37.4bn** (restated) → FY2023 **27.3bn (−27%,
   the trough)** → **FY2024 44.96bn (+64.9%)** → 1H2025 **27.9bn (+11.0%)**.
   [CPIC FY2024 results, HKEXnews 2025-03-26: https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0326/2025032601318.pdf ;
   1H2025: https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0828/2025082802552.pdf] **VERIFIED.**
   FY2024's surge was **investment-driven** (total investment income +130.5% to RMB 120.4bn on the
   equity rally; fair-value swing from −11.7bn to +37.7bn) — the 22-Jan-2025 profit alert explicitly
   cited "positive fluctuations in the capital markets." That is the definition of a **cyclical**
   swing: the same market forces that caused the trough caused the recovery.

2. **New-business value is ACCELERATING, not decaying** — the single strongest anti-"broken" signal.
   VNB growth: FY2024 **+20.9%** (post economic-assumption cut; +57.7% pre-adjustment) → 1H2025
   **+32.3%** → FY2025 **+40.1%** (RMB 18.6bn). [same filings + FY2025 presentation:
   https://www.cpic.com.cn/upload/resources/file/2026/03/26/93803.pdf] **VERIFIED.** A structurally-
   broken life franchise would show **collapsing** new-business value; CPIC's is compounding
   double-digit-and-rising even after management cut its long-run investment-return assumption.

3. **Embedded value keeps growing.** Group EV RMB 529.5bn (FY2023) → **562.1bn (FY2024, +6.2%)** →
   588.9bn (1H2025) → **613.4bn (FY2025, +9.1%)**. [FY2024 PDF 85906; 1H2025 pres 88853; FY2025 pres
   93803, all cpic.com.cn] **VERIFIED.** A dying insurer's EV shrinks; CPIC's compounds.

**Verdict on the crux: this is a cyclical, investment-market/rate-driven trough that has already
inflected up — NOT a broken franchise.** The residual risk (§4a) is not that the franchise is
broken today but that *chronically falling Chinese rates* slowly erode the guaranteed-return life
book's future spread — a real, structural, but multi-year risk, distinct from the acute 2023 trough.

---

## 2. Valuation — the RIGHT metrics for a life insurer

For a lifeco, **P/EV, VNB growth, and P/B** are the load-bearing metrics (P/E is noisy because
IFRS-17 earnings swing with markets). yfinance has none of EV/VNB/P/EV — all from filings below.

### Embedded value & P/EV (DERIVED multiples)
- Group EV **RMB 562.1bn (FY2024)** / 588.9bn (1H2025) / 613.4bn (FY2025). ÷ ~9.62bn shares ⇒
  EV/share ≈ **RMB 58.4 (FY2024)** → 61.2 (1H2025) → ~63.8 (FY2025). *(EV/share is DERIVED — CPIC
  does not disclose a per-share EV line.)*
- **CPIC A-share P/EV ≈ 0.48–0.51x** (RMB 29.63 ÷ ~58–61) — the FX-clean, most reliable read.
  **H-share P/EV ≈ 0.41–0.43x** (HKD→RMB conversion approximate — **UNVERIFIED FX**).
- P/EV multiple itself is **DERIVED** (price ÷ filed EV); no sourced analyst P/EV was retrievable.

### P/EV vs peers (all DERIVED from filed EV; ranking is the signal, not the decimals)

| Insurer | P/EV (derived) | Note |
|---|--:|---|
| China Taiping (0966.HK) | **~0.24–0.32x** | cheapest large mainland lifeco (H-only, index-excluded) |
| New China Life (1336.HK) | ~0.46–0.48x | |
| China Life (2628.HK) | ~0.48–0.50x | |
| **CPIC (601601.SS)** | **~0.48–0.51x** | **mid-pack among mainland peers** |
| Ping An (2318.HK) | ~0.59x | |
| AIA (1299.HK) | ~1.3x | premium franchise, different "EV Equity" basis |

**Read:** CPIC is cheap in absolute terms (below book, ~0.5x EV) but **mid-pack, not the cheapest**,
among mainland lifecos. China Taiping is materially cheaper on both P/EV and P/E (§5).

### P/B & yield vs history/peers
- P/B **0.72x** (yf, VERIFIED); cross-checks to ~0.76x on filed book (RMB 33.22/share). Below 1x on a
  ~16–17% ROE franchise. Chinese lifecos have traded a wide 0.5–1.5x P/B band over the cycle; 0.72x is
  toward the low-to-mid of that range (peer P/B: Taiping 0.71, NCI 1.04, China Life 1.15, PICC Group
  0.57, Ping An 0.79 — financials_screen.md 2026-07-02).
- Dividend yield **4.9%** H-share (3.8% A-share); DPS RMB 1.00→1.02→1.02→**1.08** (FY2021–24), payout
  ~23–36% of net profit. [stockanalysis.com via S&P GMI, 2026-07-02]. **Stated payout-policy floor
  UNVERIFIED** (annual-report PDFs are scanned/image; CPIC is *understood* to target a ~30% floor but
  this is not asserted from primary source).

---

## 3. Quality

- **ROE trend (attributable, IFRS 17/9):** FY2022 19.2% → FY2023 **11.4% (trough)** → FY2024 **16.6%**
  → 1H2025 9.6% (half-year, not annualized). [CPIC 2023 AR 80345; FY2024 AR; 2025 Interim] **VERIFIED.**
  ROE tracks the profit trough-and-recovery exactly — cyclical, not decaying.
- **EV growth:** +6.2% (FY2024), +9.1% (FY2025). Steady compounding through a weak macro. **VERIFIED.**
- **Solvency (C-ROSS II; minimums 50% core / 100% comprehensive) — very strong.** FY2025:
  **CPIC Life core 157% / comprehensive 228%; CPIC P&C core 203% / comp 244%; Group core 206% / comp
  273%.** [CPIC 2025 AR, cpic.com.cn/.../93802.pdf, 2026-03-26] **VERIFIED.** 2–4x the regulatory
  floors — solvency is not a concern.
- **Investment portfolio (FY2024, total assets RMB 2.73tn; 1H2025 RMB 2.92tn):** Fixed income
  **~75–76%** (bonds ~60–62%), **equities ~14.5–14.8%** (listed stocks ~9–10% + funds), **investment
  property ~0.3% → 1.0%** (the 1H2025 rise is a real-estate JV consolidation, not new market bets).
  Total investment yield **5.6% FY2024** (vs 2.6% FY2023) / net 3.8%. [FY2024 pres 85906; 1H2025
  88798/88853] **VERIFIED.** **China property-developer exposure:** no named/distressed-developer line
  disclosed; closest is "real estate" = ~11–13% of the *non-public financing* sub-book (~RMB 33bn at
  1H2025, described AAA-rated) — a slice of a sub-book, not the total. **Direct developer exposure
  UNVERIFIED / not separately disclosed** (a transparency gap, but the equity + property market
  sensitivity is what drives the earnings volatility, §4b).
- **P&C combined ratio:** FY2024 **98.6%**; 1H2025 **96.3%** (improving, comfortably underwriting-
  profitable). [FY2024 pres 85906; 1H2025 pres 88853] **VERIFIED.**
- **Dividend track record:** uninterrupted, growing DPS; payout ~23–36%; covered. **VERIFIED (values);
  policy floor UNVERIFIED.**

**Quality read:** genuinely high — ~16–17% normalized ROE, EV compounding, fortress solvency, P&C
underwriting profit, conservative 75% fixed-income book. Higher-quality than China Taiping (§5).

---

## 4. Bear Case / Risks

**(a) Falling China interest rates → spread risk on guaranteed-return life policies — the DOMINANT
STRUCTURAL RISK.** Chinese 10-yr yields have fallen for years; a large stock of legacy guaranteed-
return (and participating) policies means CPIC must earn above the guaranteed crediting rate to avoid
negative spread. This is precisely why CPIC (like all China lifecos) **cut its long-run investment-
return assumption** (which mechanically lowered reported EV and VNB in the FY2024 restatement). This
is the real, multi-year, *structural* worry — distinct from the acute 2023 trough. Mitigants: rapid
mix-shift toward protection/participating products, VNB margin still rising, regulator-mandated cuts
to guaranteed rates on new policies. **VERIFIED direction; magnitude ASSUMED.**

**(b) Investment exposure to China equities/property drives the earnings volatility.** ~14.5% equity
allocation on a RMB 2.9tn book means group net profit swings hard with the CSI 300 — the entire
2023-trough-to-2024-surge round-trip was investment-income-led (§1). This makes single-year P/E and
ROE misleading and keeps the stock's earnings genuinely volatile. Property exposure appears modest
and largely AAA sub-book, but disclosure is thin. **VERIFIED (equity sensitivity); property UNVERIFIED.**

**(c) Cyclical vs structural — argued both sides.**
- *Broken-franchise bear:* the assumption cuts admit the old return math no longer works; chronically
  falling rates could grind spread to zero; single-year earnings are unreliable; A/H shares have
  de-rated to ~0.5x EV for a reason the market may know better than we do.
- *Cyclical bull (the evidence favors this):* FY2023 trough already reversed (+64.9% FY2024); VNB
  **accelerating** +20.9%→+32.3%→+40.1%; EV compounding; solvency 2–4x minimums; P&C profitable. A
  broken franchise shows collapsing new-business value and shrinking EV — CPIC shows the opposite.
- **Call: cyclical trough already inflected up, with a genuine but slow-moving structural rate
  headwind layered underneath.** Not broken.

**(d) SOE governance.** Central-SOE control (Shanghai state entities) means the state's policy goals
(social insurance, holding domestic bonds/equities, national-service capital allocation) can outrank
minority-shareholder returns; capital-allocation discipline is state-influenced. Real but standard-
for-the-cohort discount. **VERIFIED (SOE status); impact ASSUMED.**

**(e) HKD / market access.** H-share (2601.HK) settles in HKD; the underlying business is RMB, so
reported HKD returns carry RMB translation risk. A US person can hold the H-share, the A-share (via
Stock Connect / QFII, broker-dependent), or the **London GDR** (LSE ticker CPIC). Practically
accessible. **VERIFIED (listings); GDR size/date UNVERIFIED.**

**(f) US-person sanctions / CMIC status — CLEAR.** CPIC (2601.HK / 601601.SS) is **NOT** on the OFAC
NS-CMIC list (EO 13959 as amended by EO 14032) — verified against OFAC's consolidated data file
(DateOfIssue 2026-01-08; all 68 CMIC entries are aerospace/defense/telecom/tech — **zero insurers**).
Also not on the BIS Entity List, DOD 1260H (2026-06-10 FR notice), or SDN/MEU/SSI lists. **No Chinese
insurer currently appears on NS-CMIC** (Ping An / China Life / PICC also clear; China Life's 2022 NYSE
ADS delisting was **commercial**, not sanctions). A US person can legally buy 2601.HK, 601601.SS, or
the LSE GDR today. [OFAC NS-CMIC: https://ofac.treasury.gov/consolidated-sanctions-list/ns-cmic-list ;
authoritative data: https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/CONS_ADVANCED.XML]
**VERIFIED** (sanctions-status finding, not legal advice).

---

## 5. Catalysts, Scorecard & Verdict

**Catalysts (weak — score 5% for a reason):** continued equity-market recovery flowing to investment
income; VNB momentum sustaining into 2026; any DPS/payout-policy uplift; agency-productivity reform;
China rate stabilization. Mostly macro-dependent, not company-specific — the classic China-lifeco
"needs the market to cooperate" catalyst profile.

### Scorecard (CLAUDE.md §3 weights; 0–10 each × weight)

| Dimension | Weight | Score | Weighted | Rationale |
|---|--:|:--:|--:|---|
| **Cheapness** | 30% | **7** | 2.10 | 0.72x book, ~0.48–0.51x EV, 4.9% yield — cheap absolute; but mid-pack vs mainland peers (Taiping cheaper), so not a 9. |
| **Quality** | 30% | **8** | 2.40 | ~16–17% normalized ROE, EV compounding, solvency 2–4x minimums, P&C profitable, 75% fixed income. Top-tier for the cohort. |
| **Trap-risk (inverse)** | 20% | **7** | 1.40 | Trough is cyclical & already reversed (de-risks the trap); residual = rate/spread structural drag + earnings volatility + thin property disclosure. |
| **Moat & leadership** | 15% | **7** | 1.05 | Top-3 scaled agency franchise, strong brand/distribution; capped by SOE governance & commodity-ish product. |
| **Catalyst** | 5% | **5** | 0.25 | Macro-dependent (equity market + rates); little idiosyncratic catalyst. |
| **TOTAL** | 100% | | **7.20 / 10** | |

### Verdict: **BUY — worth more work.** (7.2/10)

The trough question resolves favorably: **cyclical, already inflected up** (FY2023 trough → +64.9%
FY2024 profit, VNB accelerating to +40%, EV compounding, solvency fortress). Cheap on the right
metrics (~0.5x EV, 0.72x book) with covered ~5% yield, high quality, and **cleanly US-investable**.
The dominant residual risk is the slow structural rate/spread grind, and earnings will stay volatile
with China equities. A genuine, ownable EM cheap-quality lifeco — pending Hooman's own filing cross-
check of the EV/VNB numbers (all primary-source, third-party corroboration was blocked here).

### CPIC vs China Taiping (0966.HK) — which is the better EM-life pick?

| | **CPIC (2601.HK)** | **China Taiping (0966.HK)** |
|---|---|---|
| P/E (trailing) | ~4.4–5.1x | **~2.5x** (deflated by FY2025 one-off spike) |
| P/EV (derived) | ~0.48–0.51x (A) | **~0.24–0.32x** (cheapest) |
| P/B | 0.72x | 0.71x |
| Dividend yield | 4.9% | **~6.5–6.8%** |
| Normalized ROE | **~16–17%** | ~10% (ex one-off) |
| VNB (life) | FY2024 +20.9% → 1H2025 +32.3% → FY2025 +40.1% | FY2024 +94% (record) → **FY2025 +2.7% (decelerating)** |
| Listing / liquidity | **A+H+GDR, HSCEI constituent** (index demand) | H-only, **not in HSI/HSCEI**, thin float |
| US sanctions status | Clear | Clear |
| Earnings quality | Cleaner, agency-driven | FY2025 +220.9% partly one-off (tax benefit UNVERIFIED) |

**Take:** they are **different bets**. **China Taiping is the deeper-value / higher-yield contrarian
play** (~0.3x EV, ~6.5% yield) — but its cheapness is partly *explained* by H-only listing, index
exclusion, thin liquidity, SOE overhang, a P/E deflated by a one-off FY2025 profit spike, and
**decelerating** new-business value (+2.7% FY2025). **CPIC is the higher-quality, more liquid, more
investable name** — ~16–17% ROE vs ~10%, accelerating VNB, index inclusion, an A-share/GDR floor
under the H-share, cleaner earnings. For Hooman's **quality-first** mandate (CLAUDE.md §3: Quality is
the dominant filter), **CPIC is the better core EM-life pick**; China Taiping is the more speculative
deep-value satellite where you're paid a bigger discount to accept lower quality and worse liquidity.

---

## Appendix — key source URLs (all fetched/parsed 2026-07-02)
- CPIC FY2024 results (HKEXnews): https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0326/2025032601318.pdf
- CPIC 1H2025 results (HKEXnews): https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0828/2025082802552.pdf
- CPIC FY2024 results presentation: https://www.cpic.com.cn/upload/resources/file/2025/03/26/85906.pdf
- CPIC 1H2025 interim report: https://www.cpic.com.cn/upload/resources/file/2025/08/28/88798.pdf
- CPIC 1H2025 presentation: https://www.cpic.com.cn/upload/resources/file/2025/08/30/88853.pdf
- CPIC FY2025 results presentation: https://www.cpic.com.cn/upload/resources/file/2026/03/26/93803.pdf
- CPIC FY2025 annual report (solvency): https://www.cpic.com.cn/upload/resources/file/2026/03/26/93802.pdf
- CPIC LSE GDR page: https://www.londonstockexchange.com/stock/CPIC/china-pacific-insurance-group-co-ltd
- OFAC NS-CMIC list: https://ofac.treasury.gov/consolidated-sanctions-list/ns-cmic-list
- China Taiping FY2024 AR (HKEXnews): https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0429/2025042900681.pdf
- China Taiping FY2025 results (HKEXnews): https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0325/2026032501078.pdf
