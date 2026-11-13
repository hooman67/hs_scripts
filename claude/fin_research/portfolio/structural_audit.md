# Structural Audit — Portfolio Shape, Concentration & Volatility

**Prepared 2026-07-07 (Opus 4.8).** All figures from live-priced ground truth (`holdings_live.json`,
`analyze_structure.py`). RESEARCH, NOT FINANCIAL ADVICE. This chunk is portfolio *math & logic* on
verified data — the macro-thesis verification and per-name deep dives run separately (in `research/`
and `deep_dives/`).

---

## THE HEADLINE (read first)

Your portfolio has **two structural facts that matter more than any single holding:**

1. **You are far LESS at risk than you fear.** Total-portfolio annualized volatility is **~6.6%**
   (2y weekly, VERIFIED) — comfortably under your 10% ceiling. Your entire non-cash sleeve's worst
   drawdown over the last 2 years was only −8%. Even a **−30% crash of your whole non-cash book costs
   ~15% of total and leaves your $280k cash 100% intact.** Your fear of "a correction pricing me out
   of a house" is **not supported by your actual positioning** — you're already defensively built.
   The real cost you're paying is the *opposite*: **over-defensiveness** (50% cash + 37% commodities)
   is a drag on the 20-year wealth-building goal.

2. **Your "diversification" is mostly ONE bet wearing 15 costumes.** You have 20 theme labels, but
   collapsed to true macro factors, **~75% of your non-cash portfolio (37% of total) is a single
   correlated bet: commodities / real assets / inflation.** Energy, gold, silver, copper, uranium,
   steel, aluminum, ag — these all rise and fall together on the same drivers (inflation, global
   growth, USD, real rates). That's not 8 diversified themes; it's one giant macro position. If your
   USD-debasement/inflation thesis is *wrong* (or just early), most of the book drops together.

Everything below expands these two points and fixes the categorization.

---

## 1. True macro-factor exposure (the real picture)

Your 20 themes collapse into these actual factors (VERIFIED, live market values):

| True factor | $ (non-cash) | % non-cash | % total | What's in it |
|---|--:|--:|--:|---|
| **ENERGY/COMMODITY** | 114,499 | **41.6%** | 20.6% | oil&gas (9), uranium (4), GEV |
| **PRECIOUS METALS** | 57,898 | **21.0%** | 10.4% | gold (4), silver (WPM), plat (SBSW) |
| HEALTHCARE | 28,306 | 10.3% | 5.1% | PFE, LLY |
| US TECH/AI | 19,014 | 6.9% | 3.4% | AMZN, RBLX, ARKK, AEVA, AUR |
| AG/COMMODITY | 18,886 | 6.9% | 3.4% | CAG, KHC, PDBA, CF |
| INDUSTRIAL METALS | 14,344 | 5.2% | 2.6% | BHP, COP.U, NTCPF, XME, AA |
| CRYPTO | 14,307 | 5.2% | 2.6% | BTC (3 lots), MARA, CRCL |
| CHINA/EM | 5,021 | 1.8% | 0.9% | KWEB, BABA, BIDU, JMIA |
| EV/CLEANTECH | 1,978 | 0.7% | 0.4% | 5 tiny names |
| CONSUMER / REAL ESTATE | 1,174 | 0.4% | 0.2% | SBUX, GLBS, CSGP |

> **COMMODITY/REAL-ASSET MEGAFACTOR = ENERGY + PRECIOUS METALS + INDUSTRIAL METALS + AG =
> $205,626 = 74.7% of non-cash, 37.0% of total portfolio.**

**Why this is the #1 issue:** these factors are positively correlated (all long inflation / real
assets / global growth / short-USD). You *think* you own energy + gold + copper + uranium + ag as
separate diversifiers. In a deflationary shock, a growth scare, or simply if inflation cools and the
USD holds, **they fall together.** You have concentrated, not diversified. This is defensible *if* it's
a deliberate, high-conviction macro bet (your USD-debasement view supports a real-asset tilt) — but
37% of total in one correlated factor is a **very large** active bet for someone who (your words) has
"no special edge" and "a poor track record at predictions." The two statements are in tension.

**The missing asset classes (near-zero):** broad global equities, developed international ex-Canada,
emerging markets, quality compounders, bonds/TIPS (your Bucket A is all cash, no TIPS ladder yet
despite the plan calling for one).

---

## 2. Volatility & the house-purchase stress test (VERIFIED)

| Metric | Value | Your constraint | Verdict |
|---|--:|--:|:--:|
| Total portfolio annualized vol (2y weekly) | **6.6%** | ≤10% | ✅ well inside |
| Non-cash sleeve vol | 13.3% | — | moderate (cash halves it) |
| Non-cash worst 2y drawdown | −8.0% | — | mild |
| MV-weighted beta (non-cash names) | 0.76 | — | below-market |

**Crash scenarios (non-cash sleeve shock → total-portfolio impact):**
- non-cash −20% → total **−9.9%**, remaining $500,748
- non-cash −30% → total **−14.9%**, remaining $473,205
- non-cash −40% → total **−19.8%**, remaining $445,663

**In ALL scenarios your $280k cash is untouched** — more than a typical house down payment on its own.
Add the separate $250k house reserve and your purchasing power is essentially crash-proof already.

**Implication (important):** You are **over-insured against the house-timing risk.** The 50% cash +
$250k reserve is belt-and-suspenders. The binding risk to your *wealth* goal is not a crash before the
house — it's **10 years of 50% cash + 37% commodities badly lagging** if the world muddles along with
positive real equity returns. You have room to put meaningful cash to work without threatening the
house. (Exactly how much → the synthesis chunk, after macro verification lands.)

---

## 3. Concentration flags (single-name & single-theme)

| Flag | Detail | Why it matters |
|---|---|---|
| **WPM = 9.5% of non-cash in ONE stock** | Wheaton Precious Metals, $26.2k, −22% | Single-name silver bet larger than your entire China+EV+consumer exposure combined. Streaming model ≠ diversified silver. |
| **PFE = ~6.3% of total in one struggling pharma** | 738 shares, $17.5k | Largest single equity. Patent-cliff + IRA + tariff risk (deep dive running). Oversized for a "no-edge" investor. |
| **MNT = 9.1% of non-cash** | Canadian gold ETF, $25k | Fine as a gold vehicle, but gold overall is 21% w/ silver+plat — see megafactor. |
| **Energy 9 names, 41.6% of non-cash incl. uranium** | CNQ/XOM anchors + 7 others | Prior sleeve analysis already said 13.8% O&G was ~3–4× market weight. It's now bigger as a share of non-cash. |
| **Two anchors XOM+CNQ = ~$46k** | 16.7% of non-cash in two oil names | Both ride the same WTI factor (corr ~0.79). |

---

## 4. Contradictions between stated beliefs and holdings

| You said | You hold | Tension |
|---|---|---|
| "AI bubble will burst" | AMZN, RBLX, ARKK, AEVA, AUR, + KWEB (AI-sensitive) | You own the bubble you fear. (Some defensible — AMZN as a "winner" — but ARKK/RBLX/autonomous are pure bubble-beta.) |
| "Gold/uranium too expensive, waiting to buy" | Already 21% metals + 8.5% uranium of non-cash | You're **heavy in what you call expensive.** The honest move may be TRIM into strength, not "wait to add." (metals agent resolving.) |
| "Want EM diversification / China exposure" | EM ~1–2% vs 25% target; China $4.8k | You're barely in the thing you say you want. Intent and portfolio don't match. |
| "Minimize USD holdings" | ~43% USA equities + $261k of cash in Ameritrade (USD) | Your single biggest USD exposure is your **cash pile**, not equities. If USD-decay is your top conviction, 50% USD cash is the least-consistent position you hold. (Nuance: as a Canadian, USD cash *is* your FX risk — the macro-USD agent addresses whether to shift cash to CAD/T-bills/gold.) |
| "Avoid individual stocks, prefer ETFs, no edge" | ~45 individual names, many micro | Your behavior is the opposite of your stated philosophy. This is the single most actionable self-correction. |
| Adobe RSUs ~$732k (US tech/SaaS) | + AMZN, tech names | Your **largest single asset is US tech** already. Adding tech/AI names doubles down on your income+equity correlation (if AI hits Adobe, your job AND portfolio suffer). Argues for LESS direct tech, not more. |

---

## 5. Categorization fixes (A/B/C bucket + geography)

Your A/B/C and geography labels needed correction. Key fixes (full corrected table →
`holdings_reclassified.csv`, being finalized in synthesis):

**Geography — your labels were often wrong:**
- **WPM, AEM, MNT, CNQ, CCJ, NTCPF, EMPYF** → all **Canada (Developed)**, correct, but note this makes
  your "developed ex-US" almost entirely a **Canadian commodity** bet, not true geographic diversification.
- **BHP** → Australia (Developed), correct.
- **SBSW** → South Africa = **Emerging**, you had it right.
- **KWEB/BABA/BIDU/NIO/JMIA** → **Emerging (China/Africa)**, correct.
- **ETFs (MNT, PDBA, UNG, KWEB, XME, PALL, GLD)** → geography should be by *underlying*, not domicile.
  MNT=Canada gold, PDBA=global ag, XME=US metals&mining, KWEB=China. (yfinance shows "None" country
  for these — needs look-through, done in the reclassified table.)
- **Crypto (BTC)** → its own "global/non-sovereign" class, not a geography.

**A/B/C bucket — main corrections:**
- **Uranium (CCJ/BWXT/CEG)** you put in **C** (risky growth) — reasonable, they're volatile. But CEG is
  a regulated utility (more B-like) and BWXT is defense/naval-nuclear (quality industrial). Split them.
- **GEV** in C — correct (high-beta, +87%, richly valued after the run).
- **Food (CAG/KHC)** you put in **B** (inflation hedge) — questionable. These are *declining* packaged-
  food names (GLP-1/private-label pressure, both −21%), not clean inflation hedges. More like value-traps
  than defensive real assets. Reclassify as C-turnaround-or-exit.
- **Copper/steel/aluminum** you split across B and C inconsistently — they're all cyclical commodity
  equities; treat as one "industrial metals" C-sleeve (cyclical, not defensive).
- **Crypto** correctly in C. **Physical gold + core gold** correctly B.

The clean rule we'll apply:
- **Bucket A** = cash, T-bills, TIPS, GICs — *principal protection*. (Currently 100% cash; needs a TIPS/
  T-bill structure per your own plan.)
- **Bucket B** = *defensive* real assets that hold value in inflation AND don't crater in a growth scare:
  **physical/core gold, TIPS.** (Silver, platinum, copper, steel, oil — these are *cyclical* real assets,
  arguably C, not B. This is the key reclassification: B should be the low-vol inflation hedge, not the
  whole commodity complex.)
- **Bucket C** = *opportunistic growth / high-vol*: equities, cyclical commodities, uranium, crypto,
  China, thematic bets.

**Consequence of the honest reclassification:** a lot of what you filed under "B — inflation hedge"
(silver, copper, steel, oil ETFs) is really **C-risk**. That means your true **A/B/C is closer to
50% / ~13% / ~37%** than your reported 50/27/23 — i.e. **your genuine high-volatility bucket is ~37%,
more than double the 15% plan.** The cash hides it, but the growth-risk concentration is larger than the
bucket labels suggest. (This reconciles with the megafactor finding.)

---

## 6. Micro-position cleanup (15 names, ~$7.8k)

Legacy 2021-era speculative buys, mostly deep losses: AEVA, AUR (autonomous); CHPT, NIO, F, LCID, RIVN
(EV); MARA (crypto miner); JMIA, GLBS (misc EM); CSGP, BIDU, BABA (tiny). Plus small SBUX, ARKK, URC.

- **Diversification value: ~zero** (each <0.3% of total).
- **Cost: real** — tax-filing complexity, rebalancing friction, mental overhead, and they keep you in
  "story stocks" that contradict your ETF-first philosophy.
- **Action (pending per-name confirm from scorecard agent):** consolidate away. Harvest losses in taxable
  accounts (NIO −88%, CHPT −67%, SBSW −54% offset gains elsewhere); the winners are negligible.
- **Watch:** don't reflexively sell in a *registered* (RRSP/TFSA) account for tax-loss reasons — losses
  aren't deductible there. Sort by account type in synthesis.

---

## 7. What this audit does NOT yet answer (waiting on running agents)

- **Is each macro thesis actually RIGHT?** (USD decay, energy, metals, China, AI, supercycle — 6 agents running.)
- **Per-name hold/add/trim/sell** with valuations (healthcare + scorecard agents running).
- **The ideal allocation numbers** — the synthesis chunk builds these once the theses are graded, so we
  size by *conviction × evidence*, not just by tidying the current book.

→ Continues in `PHASE1_AUDIT.md` (synthesis) once agents land.

---

## Verification log
- **VERIFIED live (yfinance 2026-07-07):** all 53 holding prices, market values; 2y weekly returns for
  50 names → portfolio vol 6.6% total / 13.3% non-cash, worst 2y drawdown −8.0%, MV-weighted beta 0.76.
- **VERIFIED (arithmetic on live MVs):** factor aggregation, megafactor 74.7% non-cash / 37.0% total,
  bucket weights, crash scenarios. Reproducible: `data/analyze_structure.py`.
- **Data caveat:** book-value P&L uses recomputed basis (shares×avg_buy×FX 0.70347) because the export's
  book column mixed CAD/USD — see `holdings_snapshot.md`. Volatility uses 2y weekly; a longer window or a
  commodity-stress period (2008/2020/2022) would show higher tail vol for the commodity sleeve — the 6.6%
  is a *normal-regime* estimate, not a worst-case. Betas/correlations are point-in-time.
- **NOT financial advice.**
