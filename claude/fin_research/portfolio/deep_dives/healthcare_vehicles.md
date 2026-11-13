# Healthcare — Best VEHICLES to Own the Sector (ETFs vs single names) + Sleeve Weights

Run: 2026-07-27 by Claude (Opus 4.8). Owner: Hooman Shariati (Canadian citizen; quality-first, global value).
Builds on `screens/sector_healthcare.md` (2026-07-04/05), `deep_dives/healthcare_PFE_LLY.md` (2026-07-07),
`deep_dives/managed_care/comparison.md`, and `LEARNINGS.md` (healthcare section). **Does not re-derive** the
sector-cheapness / AI-narrative / IRA-tariff groundwork — it reuses those verdicts and focuses on the one new
question: *which vehicles best let Hooman own healthcare, and at what per-name weights?*

> **Anti-hallucination.** Every price/multiple/holding weight is a **live yfinance pull, timestamped
> 2026-07-27 ~22:12 UTC** (`data/cache/hc_vehicles.json`), except **expense ratios**, which yfinance does not
> serve — those are marked **ASSUMED (published, stable)** and should be confirmed on the issuer factsheet
> before buying. Policy/AI facts carried from prior primary-sourced research and re-marked. No number invented.
> This is RESEARCH, not financial advice.

---

## TL;DR (bottom line first)

1. **The broad healthcare ETFs (XLV / VHT / IYH) are ~the same fund.** All three are cap-weighted US healthcare:
   **#1 holding is LLY at 14-16.5%**, then JNJ, AbbVie, UNH, Merck, Amgen — i.e. **~45% big-pharma + UNH +
   device/tools names.** XLV (fee **0.08% ASSUMED**) and VHT (**0.09%**) are the cheap, sensible cores; **IYH is
   the same basket at ~5× the fee (0.39%) — no reason to own it.** Buying a broad ETf **re-buys LLY** (Hooman
   already holds it) — a real overlap to size around.
2. **For the "AI in healthcare" angle, the only *investable-today* capture is medical devices/imaging, not
   drug-discovery.** Prior research verdict stands: **zero AI-originated drugs are FDA-approved or generating
   revenue as of mid-2026.** Where AI is *real revenue* is FDA-cleared imaging/diagnostics AI, which accrues to
   incumbents (GE HealthCare, Siemens Healthineers). **GEHC is the single best "AI + value" name** — fwd P/E
   **11.4**, trading near its 52-wk low ($61.1 vs low $58.75), #1 in FDA AI-device clearances. **IHI** is the
   diversified device basket but still **not cheap** (trailing P/E 29.5, fee 0.40%) — though the whole device
   group has **de-rated hard** in the past year (IHI −22% off its high, ISRG −41%, GEHC −32%), making a *small*
   device kicker more interesting now than in the July-5 read.
3. **The AI-drug-discovery pure-plays are all speculative / pre-profit — do NOT put the sleeve on them.** RXRX
   ($3.01, revenue **−56%**, −$178M FCF), SDGR (op margin **−83%**), ABSI (revenue **−82%**, $1.8M total
   revenue), CRSP (gene editing, −$261M FCF). Tempus AI (TEM) is the only one with a real revenue base ($1.36B,
   +36%) but is unprofitable, **beta 3.46, P/B 18.5** — a growth speculation, not a value holding. **Skip as
   dedicated positions;** you already get diluted exposure to them inside XLV/VHT.
4. **The thematic "AI/health-tech" ETFs are mostly marketing.** HTEC (Robo Global HealthTech) has only **$60M
   AUM** (liquidation risk, fee ~0.68% ASSUMED); EDOC $34M; ARKG ($1.7B, fee 0.75%) and IDNA are **genomics**
   funds, not "AI," stuffed with the same pre-revenue names as #3. **None is a good vehicle for the AI thesis** —
   GEHC (or IHI on weakness) captures it far more honestly and cheaply.
5. **Recommended shape for a ~5%-of-total healthcare sleeve (≈ current size, just reshaped): XLV core +
   keep-LLY + right-sized-PFE + a small GEHC device/AI kicker.** Managed-care value (CI) is the other great
   quality-at-a-price healthcare corner **but Hooman already holds CI in his financials sleeve** — so it's
   captured; don't double-buy. Per-name weights in §6.

---

## 0. Sizing frame (so the % add up)

- **Total portfolio ≈ $555,832** (`holdings_snapshot.md`, 2026-07-07). A **4-5% total healthcare sleeve = ~$22-28k.**
- **Current healthcare sleeve = PFE + LLY** (live 2026-07-27): PFE 738 sh × $24.67 = **$18,206** + LLY 9 sh ×
  $1,197.53 = **$10,778** → **$28,984 = ~5.2% of total** (~10.5% of the $275k non-cash book).
- So Hooman is **already at ~5%.** The task is **not to add net healthcare** — it's to **reshape** the existing
  ~5% into a better-diversified, higher-quality, AI-capturing structure.

---

## 1-4. The vehicle comparison table (live 2026-07-27 ~22:12 UTC)

Prices/multiples VERIFIED live. Expense ratios **ASSUMED** (published, stable — confirm on factsheet). "fwd P/E"
= forwardPE; ETF "P/E" = trailingPE of the basket. AUM = totalAssets.

| Vehicle | What it is | Valuation (live 2026-07-27) | AI-capture | Role | Verdict |
|---|---|---|---|---|---|
| **XLV** | SPDR S&P Health Care (69 hldgs) | NAV $162.6; basket P/E **29.4**; yld **1.60%**; AUM **$40.6B**; fee **0.08%** (A) | Indirect — 16.5% LLY + devices/UNH; no pure AI | **Core** (default) | **BEST broad core** — cheapest fee, deep liquidity |
| **VHT** | Vanguard Health Care (~400 hldgs) | NAV $305.1; P/E **29.1**; yld **1.58%**; AUM **$20.4B**; fee **0.09%** (A) | Same as XLV, slightly more diluted (14.2% LLY) | Core (broader) | **Co-best core** — more names, dilutes LLY overlap a touch |
| **IYH** | iShares US Healthcare | NAV $68.4; P/E **29.3**; yld **1.19%**; AUM $3.2B; fee **0.39%** (A) | Same basket | — | **Skip** — identical basket at ~5× the fee |
| **IHI** | iShares US Medical Devices (ABT/ISRG/SYK/EW/BDX/GEHC…) | NAV $50.2; P/E **29.5**; yld 0.49%; AUM $3.0B; fee **0.40%** (A); **−22% off 52wk high** | **Best diversified AI-device basket** (AI = real FDA-cleared revenue) | Optional kicker | Thematically the cleanest AI-healthcare ETF, but **not cheap**; device group has de-rated — buy on weakness |
| **IBB** | iShares Biotech (VRTX/AMGN/GILD/REGN…) | NAV $188.1; P/E **23.7**; AUM $9.1B; fee **0.45%** (A) | Long-dated AI-discovery *beta*, large-cap tilt | Higher-risk kicker | Cheaper/less wild than XBI; still not value; skip for a defensive sleeve |
| **XBI** | SPDR S&P Biotech (equal-weight, small-cap) | NAV $150.6; AUM $10.7B; fee **0.35%** (A); 52wk $84-166 (**huge range**) | The AI-drug-discovery beta — highest risk | Speculative | **Skip** — equal-weight micro-cap biotech = a volatility bet, not defensive |
| **HTEC** | Robo Global HealthTech & Innovation | NAV $37.6; P/E 27.7; **AUM only $60M**; fee **~0.68%** (A) | Marketed as "health-tech/AI" — holds Tempus/Natera/Twist | — | **Skip** — tiny AUM (liquidation risk), high fee, no real AI edge vs IHI |
| **EDOC** | Global X HealthTech (telemedicine/digital) | NAV $9.2; P/E 38.5; **AUM $34M**; fee ~0.68% (A) | Digital-health theme; mostly de-rated names | — | **Skip** — micro AUM, expensive basket |
| **ARKG** | ARK Genomic Revolution | NAV $37.8; AUM $1.7B; fee **0.75%** (A); 52wk $22.7-44.5 | Genomics/pre-revenue (Twist, Tempus, ABSI, CRSP) — NOT "AI" | — | **Skip** — high fee, speculative genomics, not the AI thesis |
| **IDNA** | iShares Genomics/Immunology | NAV $32.0; P/E 20.7; AUM $194M; fee **0.47%** (A) | Genomics/immuno-oncology theme | — | **Skip** — thin, thematic, off-thesis |
| **LLY** *(held, 9 sh)* | Eli Lilly — elite GLP-1 growth | $1,197.53; fwd P/E **26.6**; P/B 34.3; EV/EBITDA 30.5; ROE **107%**; rev **+55%**, EPS **+170%**; PEG **1.67**; yld 0.58% | Internal R&D only — **not measurable AI revenue** | **Quality anchor** | **HOLD; do NOT add above ~$1,080** (52wk high $1,249; mean tgt $1,270). Quality-justified expensive |
| **PFE** *(held, 738 sh)* | Pfizer — cheap struggling pharma | $24.67; fwd P/E **8.7**; P/B 1.56; EV/EBITDA 7.6; ROE **8.3%**; yld **7.01%** (FCF-covered 1.26×); rev +5.4%, EPS −10% | None measurable | **Income/ballast** | **HOLD but RIGHT-SIZE** — cheap-for-a-reason (patent cliff + IRA + tariff); over-sized at 3.2% of total |
| **UNH** | UnitedHealth — scale payer, best AI-admin story | $417.64; fwd P/E **18.6**; P/B 3.62; ROE 14.2%; EPS +61.5% (off trough); yld 2.21% | **Best AI-admin story** (~$1.5B/yr AI spend) but | Watch | **AVOID for now** — live DOJ criminal+civil Medicare-billing probe (unique to UNH); fwd 18.6× is ~fair on trough EPS, not cheap |
| **ELV** | Elevance — cheaper payer, Medicaid-pressured | $378.36; fwd P/E **12.8**; P/B 1.83; ROE 11.1%; EPS −13% | Modest | Watch | Cyclical-recovery bet; Medicaid/ACA rate-lag is *its* headwind |
| **CI** *(held in financials sleeve)* | Cigna — cleanest managed-care VALUE | $291.02; fwd P/E **8.7**; P/B 1.82; EV/EBITDA 7.5; ROE **16.3%**; PEG 0.87; yld 2.15% | AI-admin (PBM/Evernorth) | **Already owned** | **Best quality-first payer value** — but **Hooman already holds it**; captures the "cheap healthcare + AI-admin" corner. Don't double-buy |
| **CVS** | CVS — integrated payer/pharmacy/PBM | $107.07; fwd P/E **12.7**; ROE 3.8%; yld 2.47%; EPS +63% (recovery) | Modest | — | Turnaround, not quality-first; skip |
| **GEHC** | GE HealthCare — #1 FDA AI-device clearances | $61.12; fwd P/E **11.4**; P/B 2.61; EV/EBITDA 10.3; ROE **19.5%**; near 52wk low ($58.75) | **BEST investable AI-in-healthcare capture** (real cleared-AI imaging revenue) | **AI/device kicker** | **Buy candidate** — value + real AI + quality (19.5% ROE); de-rated −32% off high |
| **ISRG** | Intuitive Surgical — robotic surgery | $356.83; fwd P/E **29.7**; P/B 6.95; EV/EBITDA 28.9; ROE 17.4%; rev +18.5%; **−41% off 52wk high** | AI-assisted surgery (real, premium) | Growth watch | Elite device compounder, still premium even after the crash; watch, don't chase |
| **SYK** | Stryker — ortho/med-surg | $336.74; fwd P/E **20.1**; P/B 5.62; ROE 15.2% | Modest device AI | — | Quality, fair price; not a sleeve priority |
| **BSX** | Boston Scientific — cardio | $45.51; fwd P/E **12.3**; ROE 14.7%; rev +11.6%; **−58% off 52wk high** ($109→$45) | Modest | Value-device watch | Cheapest quality device leader after a big drawdown — worth watching vs GEHC |
| **MDT** | Medtronic — diversified devices | $84.22; fwd P/E **13.1**; ROE 9.8%; yld 3.46% | Modest | — | Cheap + income, mediocre ROE; behind GEHC/BSX on quality |
| **SHL.DE** | Siemens Healthineers — #2 AI clearances (imaging) | €35.56; fwd P/E **14.4**; P/B 2.20; ROE 11.5%; yld 2.85% | #2 AI-device capture; EUR-denominated (diversifies USD) | Alt AI kicker | Good non-USD AI-device alternative to GEHC; lower ROE, listed in EUR |
| **TMO / DHR** | Life-science tools leaders | TMO fwd **20.4** / DHR fwd **21.2**; ROE 13.5% / 7.6% | AI-enabled R&D demand (indirect) | — | Quality compounders, not cheap; skip for this sleeve |
| **RXRX** | Recursion — AI drug discovery | $3.01; mkt cap $1.6B; rev **−56%**; FCF **−$178M**; op margin −1985% | The literal AI-drug theme | Speculative | **Skip / lottery-ticket only** — pre-product, cash-burning |
| **SDGR** | Schrödinger — computational drug platform | $15.28; mkt cap $1.1B; op margin **−83%**; FCF −$49M | AI/physics-based discovery | Speculative | **Skip** — pre-profit; software+pipeline story unproven |
| **ABSI** | Absci — generative-AI antibody design | $7.56; mkt cap $1.3B; revenue **$1.8M** (−82%); FCF −$41M | Pure generative-AI-bio | Speculative | **Skip** — essentially pre-revenue, beta 2.33 |
| **CRSP** | CRISPR Therapeutics — gene editing | $46.73; mkt cap $4.6B; FCF **−$261M**; op margin −8933% | Gene editing (not AI-discovery) | Speculative | **Skip** — clinical-stage, cash-burning; off the AI thesis anyway |
| **TEM** | Tempus AI — AI diagnostics/data | $42.91; mkt cap $7.7B; rev **$1.36B (+36%)**; profit margin −22%; P/B **18.5**; **beta 3.46** | The best-*revenue* AI-healthcare pure-play | Speculative growth | **Tiny or skip** — real AI-data business but unprofitable, extreme volatility, richly valued. Not quality-first |

(A) = ASSUMED expense ratio (published/stable; yfinance does not serve it — confirm on issuer factsheet).

---

## 5. Reading the table — what you actually get, per bucket

**Broad ETFs (XLV/VHT/IYH) — "healthcare" ≈ "big pharma + UNH + a few device/tools names."** All three top out
with **LLY (14-16.5%), JNJ, AbbVie, UNH, Merck, Amgen** — the mega-caps. They are diversified *within* healthcare
but are **~45% pharma-weighted and cap-concentrated**. XLV (0.08%) and VHT (0.09%) are the right cores; **IYH is
strictly dominated** (same basket, 0.39% fee). **Key caveat: a broad ETF re-buys LLY** — XLV at 16.5% LLY means
$7.8k of XLV adds ~$1.3k of LLY on top of the 9 shares Hooman already holds. VHT (14.2%) dilutes that slightly.

**Devices (IHI) — the honest "AI in healthcare" ETF, but not cheap.** IHI *is* where FDA-cleared diagnostic AI
shows up as revenue (ABT, ISRG, SYK, GEHC, MDT, DXCM…). Basket P/E 29.5 and 0.40% fee mean it's a
growth-at-a-price vehicle, but the device group has **de-rated materially** in the past year (IHI −22%, ISRG
−41%, GEHC −32%, BSX −58%). That makes a *small* device tilt more attractive now than it looked on 2026-07-05 —
best captured cheaply via the **single name GEHC** (fwd 11.4, near its low) rather than the pricier basket.

**Biotech (IBB/XBI) — the AI-drug-discovery *beta*, higher risk, no value.** IBB (large-cap, P/E 23.7) is the
tamer version; XBI (equal-weight micro-cap, 52wk $84→166) is a pure volatility bet. Neither fits a *defensive*
sleeve. Skip.

**Thematic "AI/health-tech" ETFs — mostly marketing.** HTEC ($60M AUM) and EDOC ($34M) are sub-scale (liquidation
risk, wide spreads, ~0.68% fees). ARKG/IDNA are **genomics** funds — not "AI" — packed with the same pre-revenue
names (Twist, Tempus, ABSI, CRSP) and charging 0.47-0.75%. **There is no good, cheap, liquid "AI-healthcare" ETF
as of mid-2026** — the theme is best owned through device incumbents (GEHC/IHI/SHL.DE), not a thematic wrapper.

**AI-drug pure-plays — all speculative/pre-profit.** RXRX, SDGR, ABSI, CRSP are cash-burning and pre-product;
prior research's headline holds — **zero AI-originated drugs are FDA-approved or generating revenue.** Tempus (TEM)
is the one with a real ($1.36B, +36%) AI-diagnostics revenue base, but it's unprofitable, P/B 18.5, beta 3.46 — a
growth speculation. **None belongs in a quality-first defensive sleeve;** if Hooman wants a lottery ticket, size
it as *play money outside* the healthcare allocation, not inside it.

**Managed care (CI/UNH/ELV) — the cheap, high-ROIC value corner — already partly owned.** Per
`deep_dives/managed_care/comparison.md`: **CI is the clean quality-first value** (fwd 8.7, ROE 16.3%, no MA/DOJ
exposure), ELV a cyclical-recovery bet, **UNH an AVOID** (live DOJ probe) despite the best AI-admin story. **CI is
already held in Hooman's financials sleeve** — so the cheapest-healthcare + AI-admin angle is *already captured*.
Don't buy it twice; just recognize it as part of total healthcare-economic exposure.

---

## 6. RECOMMENDED SLEEVE STRUCTURE + per-name weights

**Design goals (from the brief):** capture the theme *cheaply* (low-fee core), *defensively* (aging/innovation,
low beta), *quality-at-a-price*, keep LLY, right-size PFE, add a *small* real-AI kicker, and **do NOT bet the
sleeve on speculative pre-revenue AI-drug names.** Target ≈ **5.0% of total (~$27.9k)** — i.e. **keep the sleeve
roughly its current size and reshape it.**

| Name | Role | $ target | **% of total** | % of sleeve | Action |
|---|---|--:|--:|--:|---|
| **XLV** | Low-fee diversified **core** (defensive, one-ticket) | ~$7,800 | **1.40%** | ~28% | **BUY** (~48 sh) — the new core |
| **LLY** | Elite-quality **growth anchor** (held) | $10,778 | **1.94%** | ~37% | **HOLD** 9 sh; **do NOT add above ~$1,080** |
| **PFE** | Cheap **income/ballast** (held), right-sized | ~$7,900 | **1.42%** | ~27% | **TRIM** 738→~320 sh (sell ~418 sh, free ~$10.3k) |
| **GEHC** | **AI/device kicker** — the real, cheap AI capture | ~$2,400 | **0.43%** | ~8% | **BUY** (~40 sh) on current weakness (near 52wk low) |
| **Total sleeve** | | **~$28,878** | **~5.2%** | 100% | ~self-funding (PFE trim ≈ XLV+GEHC buys) |

**Mechanics:** trimming PFE by ~418 sh frees ~$10.3k; that funds the XLV core (~$7.8k) + GEHC kicker (~$2.4k)
with ~$0.1k to spare — **the reshape is essentially cash-neutral.** No net new capital into healthcare required.

**Why this shape:**
- **XLV core (28% of sleeve, 0.08% fee)** turns a two-name pharma bet into a diversified defensive sleeve (JNJ,
  AbbVie, Merck, Amgen, devices, UNH) at near-zero cost. **Prefer VHT if the LLY overlap bothers you** (14.2% vs
  16.5% LLY).
- **LLY held, not added** — quality anchor; but note it's *also* XLV's #1, so **true LLY exposure ≈ $12.1k
  (2.17% of total)**. That's the one concentration to watch; it argues *against* adding LLY and *for* VHT-over-XLV.
- **PFE right-sized to ~$7.9k (~3% of non-cash, ~1.4% of total)** — keeps the 7% FCF-covered yield and defensive
  beta (0.31) as ballast, without over-betting on a patent-cliff + IRA + tariff triple-overhang name (prior
  research: quality-at-a-price 5.5/10).
- **GEHC (8% of sleeve)** is the **honest "AI in healthcare" capture** — real FDA-cleared imaging-AI revenue, #1
  in clearance count, fwd P/E 11.4, ROE 19.5%, near a 52-wk low. Small size respects that devices are a *kicker*,
  not the sleeve's foundation. **Alternative: SHL.DE** (Siemens Healthineers, EUR-denominated — adds a small
  non-USD hedge, which fits Hooman's USD-decay thesis) or **IHI** if he prefers a diversified device basket to a
  single name.

**Explicitly NOT in the sleeve (and why):**
- **No IBB/XBI/ARKG/HTEC/EDOC/IDNA** — biotech beta / thematic marketing wrappers; high fee or sub-scale; not
  defensive, not quality-at-a-price.
- **No RXRX/SDGR/ABSI/CRSP/TEM** — speculative pre-profit AI-drug names; **the sleeve is defensive, so these are
  out** (own as tiny play-money *outside* the sleeve at most).
- **No new CI/UNH/ELV** — CI already held in financials (the cheap-payer + AI-admin angle is captured); UNH is an
  AVOID on the DOJ probe.

**Which vehicle best captures "AI in healthcare"?** **GEHC (single name) or IHI (basket)** — devices/imaging is
the only place AI is *booked revenue today*. The AI-drug-discovery theme is real capital but **pre-revenue** —
own it *only* diluted inside XLV, never as a sleeve bet.

---

## 7. Verification Log

| Fact | Value | Source | As-of | Mark |
|---|---|---|---|---|
| All ETF NAV/basket-P/E/yield/AUM (XLV,VHT,IYH,IHI,IBB,XBI,HTEC,EDOC,ARKG,IDNA) | see §1-4 | yfinance `.info` live | **2026-07-27 ~22:12 UTC** | VERIFIED |
| ETF top-10 holdings & weights (XLV/VHT/IYH/IHI/IBB/XBI/HTEC/ARKG/IDNA) | see §5 | yfinance `funds_data.top_holdings` live | 2026-07-27 | VERIFIED |
| XLV/VHT/IYH #1 = LLY 16.5%/14.2%/16.1% | — | yfinance funds_data | 2026-07-27 | VERIFIED |
| Single-name prices/multiples (LLY,PFE,UNH,ELV,CI,CVS,HUM,GEHC,ISRG,SYK,BSX,MDT,SHL.DE,TMO,DHR,ABT) | see table | yfinance `.info` live | 2026-07-27 | VERIFIED |
| AI-drug pure-plays (RXRX,SDGR,ABSI,CRSP,TEM) prices/revenue/FCF/margins | see table | yfinance `.info` live | 2026-07-27 | VERIFIED |
| GEHC near 52wk low ($61.12 vs $58.75); IHI −22%, ISRG −41%, BSX −58%, GEHC −32% off highs | computed from live hi/lo | yfinance | 2026-07-27 | VERIFIED (derived) |
| ETF **expense ratios** (XLV 0.08 / VHT 0.09 / IYH 0.39 / IHI 0.40 / IBB 0.45 / XBI 0.35 / ARKG 0.75 / IDNA 0.47 / HTEC~0.68 / EDOC~0.68) | — | published/general knowledge (yfinance returns null) | — | **ASSUMED — confirm on factsheet** |
| Hooman holdings (PFE 738 sh, LLY 9 sh) & total $555,832 | — | holdings_snapshot.md + live px | 2026-07-07 / 2026-07-27 | VERIFIED |
| CI already held in financials sleeve | — | task brief + holdings_snapshot | 2026-07-27 | VERIFIED (per brief) |
| Zero AI-originated FDA-approved drugs mid-2026; AI-device clearances accrue to GEHC/Siemens | — | sector_healthcare.md primary research | 2026-06-30 / 06-18 | VERIFIED (carried) |
| UNH DOJ criminal+civil Medicare-billing probe (unique to UNH) | — | SEC 8-K 2025-07-24 (via managed_care deep dive) | 2025-07-24 | VERIFIED (carried) |
| CI cleanest payer value (fwd 8.7, ROE 16.3%); UNH = AVOID on DOJ | — | deep_dives/managed_care/comparison.md | 2026-07-05 | VERIFIED (carried) |
| PFE dividend FCF-covered 1.26×; triple overhang (patent cliff + IRA + tariff) | — | deep_dives/healthcare_PFE_LLY.md | 2026-07-07 | VERIFIED (carried) |

**Reproduce:**
```
/opt/venv/bin/python3 /tmp/hc_vehicles.py            # single names + ETF .info  → data/cache/hc_vehicles.json
/opt/venv/bin/python3 /tmp/hc_etf_holdings.py        # ETF top_holdings + sector weights
```
Prior research: `screens/sector_healthcare.md`, `deep_dives/healthcare_PFE_LLY.md`,
`deep_dives/managed_care/comparison.md`, `LEARNINGS.md` (healthcare section), `portfolio/holdings_snapshot.md`.
