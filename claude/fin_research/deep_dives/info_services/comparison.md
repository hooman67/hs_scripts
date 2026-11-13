# Information Services Head-to-Head: S&P Global vs Moody's vs MSCI

**Stage-4 new-finalist deep dive.** Prepared 2026-07-05 by Claude (Opus 4.8) for Hooman Shariati (Canadian citizen, quality-first, total-return tilt). **RESEARCH, not financial advice.**

**Price basis (yfinance live pull, as-of 2026-07-05 00:32 ET):** SPGI **$439.89** · MCO **$490.51** · MSCI **$603.11**. Financials cross-checked to SEC EDGAR XBRL FY2025 10-Ks (all filed Feb-2026) + Q1-FY2026 10-Q (period ended 2026-03-31): SPGI CIK 0000064040, MCO CIK 0001059556, MSCI CIK 0001408198. Raw pull in `live_data.json`; fetch code in `fetch_infosvc.py`.

Confidence tags: **[V]** verified from primary filing / 2+ agreeing sources · **[A]** assumed/derived by me from verified inputs · **[U]** unverified / single-source.

---

## ⚠️ Framing correction vs. the screen (read this first)

The sector screen (`sector_cheapness.md`) tagged US/Global "Information Services" at **EV/EBITDA ~11.5×, 5th percentile of its own 11-year history, ROIC ~22%** and called it a SWEET SPOT. **That is a Damodaran *sector-average* (as-of 2026-01-05, annual simple-average of ALL info-services names)** — and it does NOT describe these three franchises at the company level. Live company EV/EBITDA is **SPGI 18.3× · MCO 24.1× · MSCI 26.3×** [A, computed from V inputs] — 1.6–2.3× the sector average. The 11.5× average is dragged down by the cheaper *pure data vendors* in the bucket (FactSet 10.9×, Morningstar 12.0× [V, yfinance]) — precisely the names the screen said to AVOID.

**So the screen's own thesis holds but its number does not transfer:** the *franchises* are premium and remain premium. The real question here is **relative cheapness vs their OWN recent history** (they de-rated on AI sentiment), not absolute 5th-percentile deep value. I flag this honestly throughout — these are **"great businesses at a fair-to-full price,"** not deep-value bargains. The 22% sector ROIC read IS confirmed at the company level (and then some — see §3).

---

## 1. What each business is, and why the moat is wide

All three sell **information that other people's money decisions depend on** — and the moat is that once a rating, an index, or a data feed is embedded in contracts, regulations, and workflows, customers can't cheaply switch away. Plain-language jargon guide:

- **Ratings duopoly** — a credit rating is a letter grade (AAA…D) on how likely a borrower is to repay. Bond investors' mandates and bank capital rules are written *in terms of* these grades, and issuers pay to be rated. S&P and Moody's together rate ~**80%** of the market; with Fitch it's the "Big Three" at **93.4% of all outstanding ratings (YE2024)** [V, SEC OCR 2025 Staff Report]. **NRSRO** = "Nationally Recognized Statistical Rating Organization," an SEC designation. There are only **10 registered NRSROs (as-of 2025-12-31)** [V, SEC]; the SEC's own three-year-track-record rule for new entrants is a chicken-and-egg barrier, and investor mandates/index rules name the Big Three specifically. That's a *regulatory* moat — the government's own rules entrench the incumbents.
- **Index licensing + asset-linked (asset-based) fees** — an index is a rulebook for what a fund holds (e.g. "the S&P 500," "MSCI Emerging Markets"). ETF sponsors pay the index owner a fee that scales with **assets under management (AUM)** in the tracking fund — so revenue grows automatically as passive investing grows, with near-zero incremental cost. Network effect: everyone benchmarks to the same index, so it's costly for any one fund to defect.
- **Recurring subscription** — data/analytics sold on multi-year subscriptions with 90%+ annual retention; sticky because it's wired into customer workflows.

| | **S&P Global (SPGI)** | **Moody's (MCO)** | **MSCI** |
|---|---|---|---|
| Revenue FY2025 [V] | $15.3B | $7.7B | $3.13B |
| The moaty core | **Ratings** ($4.7B, 30%) + **Indices** ($1.85B, 12%) | **Ratings / MIS** ($4.3B gross, ~54%) | **Index** ($1.79B, 57%) |
| The "data-vendor" leg (AI-exposed) | **Market Intelligence / Capital IQ** ($4.9B, 32%) + Commodity Insights/Platts ($2.3B) + Mobility ($1.7B) | **Moody's Analytics** ($3.6B gross, ~46%) | **Analytics** ($714M, 23%) + **ESG/Climate** ($354M, 11%) |
| Recurring/relationship rev [V] | Subscription $7.9B of $15.3B (~51%) + non-transaction ratings $2.1B + asset-linked $1.2B → ~70% non-transaction | **63% recurring** (MIS 33% recurring/67% transaction; **MA ~96% recurring**) | **72.7% recurring subscription** + 24.6% asset-based (ETF) fees; only 2.7% non-recurring |
| Moat width [A] | **Wide** (ratings + indices are network/regulatory moats; MI is narrower) | **Wide** (MIS is the single most-protected asset in the group) | **Wide** (index network effect + contractual lock-in; analytics/ESG narrower) |

Segment figures [V, FY2025 10-Ks; SPGI/MCO shown gross of intersegment eliminations].

**Why wide-moat, in one line each:** SPGI and MCO own halves of a *government-entrenched ratings duopoly* that issuers are effectively required to pay; MSCI owns *the benchmarks the passive-investing world is contractually built on* (it just extended its BlackRock ETF index-licensing deal **through 2035** [V, Feb-2026]). These are among the highest-return, most-defensible business models that exist — the debate is price and AI, not moat.

---

## 2. Valuation — premium names, modestly off their own peaks

All multiples below are **live** (yfinance 2026-07-05) unless dated otherwise; FCF/EV/ROIC derived from EDGAR FY2025 [A from V inputs].

| Metric | **SPGI** | **MCO** | **MSCI** |
|---|--:|--:|--:|
| Price (2026-07-05) [V] | $439.89 | $490.51 | $603.11 |
| Market cap [V] | $130.2B | $85.7B | $43.9B |
| Trailing P/E [V] | **27.9** | **35.2** | **34.5** |
| Forward P/E [V] | **21.5** | **26.4** | **26.7** |
| EV/EBITDA [A] | **18.3** | **24.1** | **26.3** |
| P/S [V] | 8.3 | 10.9 | 13.5 |
| P/B [V] | 4.2 | 28.6 | **negative** (equity −$2.8B) |
| FCF yield (on mkt cap) [A] | **4.2%** | **3.0%** | **3.5%** |
| Dividend yield [V] | 0.88% | 0.84% | 1.36% |
| Payout ratio [V] | 24% | 28% | 43% |
| Rev growth (TTM) [V] | +10.4% | +8.1% | +14.1% |
| 12-mo price change [A/V] | **~−17.5%** (hardest hit) | ~−2.9% | ~+2.7% |
| Off 10-yr high [A] | −14.9% | −4.4% | −4.5% |

**Vs. their own history — the "less expensive than usual," not "cheap," picture** [A, from the AI-research agent, cross-checked to live P/E]:
- **SPGI:** trailing P/E ~27.9 vs a **~40× five-year average** — the only one that materially de-rated (~30% below its typical multiple). Down ~17.5% over 12 months while the S&P rose; explicitly attributed in the press to AI-disruption fear in info services [V price; A attribution]. This is the closest thing to a "sale" among the three.
- **MCO:** P/E ~35 vs a **~39× five-year average** — barely cheaper than usual (~10% below). Least de-rated.
- **MSCI:** P/E ~34.5 vs a **~46× five-year average** (off a 70×+ 2021 peak) — the multiple has compressed a lot over multiple years, but the stock is roughly flat over the last 12 months. A −5.94% single-day drop on 2026-06-25 has **no sourced cause** [U] — do not attribute it to AI/ESG without confirmation.

**FCF yield reality check:** 3–4% FCF yields are the tell that **these are not cheap in absolute terms.** For comparison, the CTSH deep-dive value case sat on a ~13% FCF yield. You are paying a full price for quality and durability here — the margin of safety comes from the *durability of the cash flow*, not from a low entry multiple.

**Note on P/B and negative equity [V]:** MCO (P/B 28.6) and especially **MSCI (negative book equity, −$2.8B at Q1'26)** have shrunk their own equity to near-zero/negative through years of buybacks (MSCI bought back $2.5B in FY2025 alone [V]). This is a *feature* of an ultra-asset-light model returning nearly all capital, **not distress** — but it makes P/B and ROE meaningless for MCO/MSCI (use ROIC and FCF instead, §3).

**Verdict on cheapness:** **All three are "great business at a fair-to-full price," NOT deep value.** SPGI is the only one meaningfully below its own recent trading range (P/E ~28 vs ~40). MCO and MSCI are only slightly off peak multiples. The screen's 5th-percentile call was a sector-average artifact; at the company level the margin of safety is thin.

---

## 3. Quality — among the best business models anywhere

These are the numbers that make premium multiples defensible. [V from EDGAR FY2025 unless noted]

| Quality metric | **SPGI** | **MCO** | **MSCI** |
|---|--:|--:|--:|
| Operating margin FY2025 [V] | 42% | 43% | **55%** |
| EBITDA margin [V] | 50% | 48% | **59%** |
| Net margin [V] | 30% | 32% | **41%** |
| FCF conversion (FCF/NI) [A] | **122%** | 105% | **129%** |
| Recurring revenue [V] | ~70% non-transaction | 63% (MA ~96%) | **72.7%** |
| ROIC (NOPAT@~20% ÷ debt+equity−cash) [A] | ~11% | **~30%** | ~40%* |
| Capital returned FY2025 (buyback+div) [V] | **$6.2B** | $2.3B | $3.0B |
| — as % of market cap [A] | ~4.7% | ~2.7% | ~6.9% |
| Share count trend [V] | shrinking | shrinking | shrinking |

*MSCI ROIC is distorted upward because equity is negative; on any tangible basis it earns extremely high returns — best framed as "generates $1.7B operating income on a capital base almost entirely returned to shareholders" [A].

**Reading it:**
- **MSCI is the highest-quality on the raw metrics** — 55% operating margin, 59% EBITDA margin, 41% net margin, 129% FCF conversion, highest recurring %. Almost no capex ($39M on $3.1B revenue). This is about as good as business models get.
- **MCO** — ~30% ROIC, asset-light, 43% margins. The MIS ratings segment alone runs at **~60% operating margin** [V], vs ~40% blended.
- **SPGI's headline ROIC (~11%) looks low but is misleading** [A]: it carries ~$45B of goodwill from the 2022 **IHS Markit** merger, which inflates the invested-capital denominator. On tangible/pre-goodwill capital its returns are far higher; the *ratings segment operates at ~64% margin* [V]. SPGI is a high-quality business whose reported ROIC is depressed by acquisition accounting, not by weak economics.
- The screen's **~22% sector ROIC is confirmed and exceeded** at the franchise level (MCO ~30%, MSCI far higher, SPGI ex-goodwill high) [A/V].

**Bottom line on quality:** genuinely elite — asset-light, 40–60% margins, 100%+ FCF conversion, 60–73% recurring revenue, aggressive buybacks. MSCI edges the quality crown on margins; MCO on clean reported ROIC; SPGI is diversified and scaled but its reported returns are goodwill-diluted.

---

## 4. The AI question — the crux, and it cuts both ways

The de-rating (especially SPGI's) is an **AI-*sentiment* overhang**. The evidence says it is currently a **multiple story, not a fundamentals story** — but the risk is real and unresolved on the data-vendor legs. Both sides, per name.

### BEAR — does GenAI disintermediate the data/analytics businesses?
- **Most-exposed lines:** SPGI **Market Intelligence / Capital IQ** (its slowest large segment, ~+6% organic; "pure data terminal" = the most LLM-substitutable) [A]; MSCI **Analytics + ESG/Climate** (softest retention, weakest AI monetization) [A]; Moody's **Analytics** (commoditizable research/data) [A].
- **Analyst warning shot:** Morningstar published *"Reviewing Our Moats for the Rise of AI"* (2026-03-06) and **downgraded FactSet's moat to "None" (2026-03-04)** [V] — the clearest AI-era moat cut in the peer group and the read-across risk. **No confirmed moat downgrade of SPGI/MCO/MSCI themselves** [A]. Dedicated bear pieces exist (Seeking Alpha "S&P Global: Do You Appreciate The AI Threat?" 2026-06-09; Forbes "AI Splits How Investors Value The Credit-Ratings Giants" 2026-06-08) [A].
- **The de-rating happened:** SPGI ~−17.5% TTM, P/E ~40→~28, press ties it to AI fear [V price; A attribution].

### BULL — the offsetting forces (mostly data-backed)
- **Retention is NOT deteriorating — the key rebuttal.** MSCI firm-wide retention **rose to 94.4% FY2025 → 95.4% Q1 2026**; even the "at-risk" lines held (Analytics 95.3%, ESG/Climate 93.0%, Index 96.9%) [V, MSCI releases]. Gross churn is rising modestly but net new sales still grew. **No hard evidence of price cuts or ARR-retention declines at any of the three** [U, absence-of-evidence] — the churn thesis is narrative, not a realized metric.
- **Ratings tailwind (issuance) is intact.** Ratings revenue tracks **debt-issuance volume.** US corporate bond issuance 2026 YTD (thru May) **$1,226.8B, +21.1% YoY** [A, SIFMA]; UBS forecasts **record IG issuance in 2026** [A]. New driver: Morgan Stanley projects **>$500B of AI-related (hyperscaler) debt issuance in 2026** [A] — AI capex literally *creates* ratings volume. Issuer confirmation: S&P raised FY earnings on "strong bond issuance" (Reuters 2025-10-30); Moody's guided high-single-digit 2026 revenue "as debt issuance returns" [V]. *Nuance:* the *rate-cut refi wave* leg is weaker than hoped — the Fed cut to **3.50–3.75%** in late 2025 then **held at all four 2026 meetings through June** [V], so it's high *volume*, not falling rates, driving it.
- **Index / ETF-AUM tailwind is strong.** Global ETF AUM hit a record **~$23.08T** end-May 2026 (record ~$1.07T YTD inflows) [V, ETFGI]; **MSCI asset-based-fee run-rate ~$872M, +25% YoY** — growing faster than total revenue, a direct passive-flows signal [A]. BlackRock deal locked to 2035 [V].
- **They SELL AI — offense, not just defense.** **Moody's has the strongest monetization evidence:** ~**40% of Moody's Analytics ARR is now GenAI-enabled**, GenAI-buyer cohort ARR "approaching $200M" with **97% retention** [A, transcripts]. **SPGI:** Kensho, ChatIQ, Spark Assist (rolled to ~40k employees); it *licenses its data INTO* Anthropic Claude, Google Gemini, Cohere (2025) [A/V] — i.e., LLM providers pay S&P for its proprietary data, which raises demand rather than displacing it. **MSCI:** AI Portfolio Insights (2024), but only ~$15–20M AI-specific new-product sales (Q3'25) — **weakest AI-offense proof points** [A].
- **Regulatory moat unbroken:** large-NRSRO share barely moved (94.15% 2023 → 93.38% 2024) [A]; ratings segment margins ~60–64% [V]. LLMs cannot issue a regulatorily-recognized rating.

### AI-threat ranking (most → least threatened)
1. **SPGI — MOST AI-threatened by business mix** (and the market agrees; it de-rated hardest). Uniquely carries **Market Intelligence/Capital IQ**, the most LLM-substitutable, slowest-growing large segment. *But* ~two-thirds of the mix (ratings + indices) is regulatorily/network-protected → **the de-rating likely overshoots the fundamentals.**
2. **MCO — moderate, best risk/reward.** Moody's Analytics carries real data-vendor risk, but it's paired with the **most-protected asset in the group (MIS ratings duopoly)** and is **furthest along on AI monetization** (40% of MA ARR GenAI-enabled, 97% GenAI-buyer retention). Protected core + working AI offense.
3. **MSCI — LEAST AI-threatened structurally.** Anchored by index licensing + asset-based ETF fees (network/contractual moat LLMs cannot touch; BlackRock to 2035). Residual risk in Analytics + ESG/Climate (softest retention, weakest AI offense at ~$15–20M). Most-protected core, thinnest AI-offense evidence.

**AI verdict:** The bear case is a *live risk on the data-vendor legs* (SPGI Market Intelligence most of all) but is **not yet visible in retention, pricing, or revenue** at any of the three. So far the panic priced value into SPGI without damaging it — the classic "fear ahead of the P&L" setup.

---

## 5. Catalysts, scorecards & verdict

### Catalysts / what re-rates them
- **SPGI:** ratings volume converting the issuance boom to transaction revenue; Market Intelligence stabilizing/growth reaccelerating; proof AI is upsell not churn; continued heavy buyback ($6.2B/yr, ~5% of cap). The de-rating (P/E 28 vs 40) is itself the opportunity if AI fear fades.
- **MCO:** debt-issuance strength (2026 guide); MA GenAI ARR cohort scaling toward/past $200M; rate cuts resuming would add a refi leg.
- **MSCI:** ETF-AUM/asset-based-fee growth (+25% YoY); ESG/Climate retention holding; any credible AI-analytics monetization. Watch the unexplained 2026-06-25 drop for a cause.

### Scorecard (0–10; CLAUDE.md §3 weights — Cheapness 30 / Quality 30 / Trap-risk-inverse 20 / Moat 15 / Catalyst 5)

**SPGI — S&P Global**
| Dimension | Wt | Score | Wtd | Rationale |
|---|--:|--:|--:|---|
| Cheapness | 30% | **6** | 1.80 | Only one materially off its own history (P/E 28 vs 40, −17.5% TTM); but EV/EBITDA 18.3 / 4.2% FCF yield = fair, not cheap. [V/A] |
| Quality | 30% | **8** | 2.40 | 42% op margin, 122% FCF conv, ~70% non-transaction; reported ROIC ~11% goodwill-diluted (ex-IHS far higher). Most diversified. [V/A] |
| Trap-risk (inverse) | 20% | **7** | 1.40 | Fundamentals growing (+10% rev); AI risk concentrated in MI (~32%) but two-thirds protected. [A] |
| Moat & leadership | 15% | **9** | 1.35 | Ratings duopoly + S&P DJI indices — two wide moats. [V] |
| Catalyst | 5% | **7** | 0.35 | Issuance wave + self-help buyback + de-rating reversal if AI fear fades. [A] |
| **TOTAL** | | | **7.30** | |

**MCO — Moody's**
| Dimension | Wt | Score | Wtd | Rationale |
|---|--:|--:|--:|---|
| Cheapness | 30% | **4** | 1.20 | Barely off its own history (P/E 35 vs 39); EV/EBITDA 24 / 3.0% FCF yield = full price. [V/A] |
| Quality | 30% | **9** | 2.70 | ~30% clean ROIC, 43% op margin, MIS ~60% margin, 96% MA recurring. Highest clean-reported quality. [V/A] |
| Trap-risk (inverse) | 20% | **8** | 1.60 | Most-protected core (ratings duopoly) + best AI monetization → lowest disruption risk. [A] |
| Moat & leadership | 15% | **9** | 1.35 | Half the ratings duopoly; MIS the single most-entrenched asset in the group. [V] |
| Catalyst | 5% | **7** | 0.35 | Issuance + MA GenAI cohort scaling. [A] |
| **TOTAL** | | | **7.20** | |

**MSCI**
| Dimension | Wt | Score | Wtd | Rationale |
|---|--:|--:|--:|---|
| Cheapness | 30% | **3** | 0.90 | Most expensive (EV/EBITDA 26.3, P/S 13.5, 3.5% FCF yield); flat TTM, only off a very high peak. [V/A] |
| Quality | 30% | **10** | 3.00 | Best raw quality: 55% op / 59% EBITDA / 41% net margin, 129% FCF conv, 73% recurring, minimal capex. [V] |
| Trap-risk (inverse) | 20% | **8** | 1.60 | Index/ETF core least AI-disruptable; residual ESG/Analytics risk. Negative book = buybacks not distress. [A] |
| Moat & leadership | 15% | **9** | 1.35 | Index network effect + BlackRock-to-2035 lock-in. [V] |
| Catalyst | 5% | **6** | 0.30 | ETF-AUM/ABF growth strong; weakest AI-offense proof + unexplained recent drop. [A/U] |
| **TOTAL** | | | **7.15** | |

### Ranked recommendation

**#1 — SPGI (S&P Global) — 7.30/10 — best quality-AT-A-PRICE.** It wins not on being the best *business* (that's MSCI/MCO) but on being the only one where **AI sentiment actually gave you a discount**: P/E ~28 vs its own ~40 five-year norm, −17.5% over 12 months, while its fundamentals kept growing (+10% revenue). You get a wide-moat ratings duopoly *plus* the S&P DJI index franchise, riding a +21% issuance tailwind, at the best relative entry of the three. The AI-most-exposed leg (Market Intelligence, ~32%) is real but two-thirds of the mix is regulatorily/network-protected, so the market's fear looks overshot. **Best margin of safety of a thin-margin-of-safety group.**

**#2 — MCO (Moody's) — 7.20/10 — highest-quality-lowest-risk, but no discount.** Cleanest reported returns (~30% ROIC), most-protected core (MIS ratings duopoly), and the *best* AI-offense story (40% of MA ARR GenAI-enabled). The only knock is price: it barely de-rated, so you pay ~full freight (P/E 35, EV/EBITDA 24). A great business you're buying at a fair price with essentially no cushion. **Buy on any weakness; it's the one to own if AI fear ever hits it the way it hit SPGI.**

**#3 — MSCI — 7.15/10 — best business, worst price.** Elite margins (55% operating!) and the least AI-disruptable core (index/ETF network effect), but the most expensive (EV/EBITDA 26.3, 3.5% FCF yield), essentially no de-rating to exploit, and the weakest AI-monetization evidence. A superb compounder — but you'd be paying up with the smallest margin of safety. **Watchlist; buy on a real drawdown.**

### Are these genuinely cheap, or just "less expensive than usual"?
**Just less expensive than usual — and only SPGI meaningfully so.** These are premium franchises trading at 18–26× EV/EBITDA and 3–4% FCF yields. The screen's "5th-percentile / deep value" read was a sector-average diluted by cheaper data vendors and does not describe the franchises. **Honest framing: quality-at-a-price, not deep value.** SPGI is a fair-price entry into a wide-moat compounder with a real (if overshot) AI overhang; MCO and MSCI are close to full price. Margin of safety is *the durability of the cash flow*, not a low multiple — size accordingly.

### The top 2 things to watch
1. **Retention / pricing on the data-vendor legs** (SPGI Market Intelligence organic growth; MSCI Analytics + ESG/Climate retention; Moody's Analytics ARR) — this is where AI disruption would show up *first*. Today retention is stable-to-rising [V]; a decisive break would validate the bear case and is the single most important signal. A confirmed Morningstar moat downgrade of any of the three (they cut FactSet to "None") would be the analyst tell.
2. **Debt-issuance volume + the rate path** — ratings transaction revenue rides issuance (+21% YoY now). The Fed *paused* in 2026 (3.50–3.75%), so the tailwind is volume-driven; watch whether issuance holds and whether cuts resume to add a refi-wave leg. A sharp issuance slowdown (recession/spread widening) is the main *cyclical* risk to SPGI and MCO ratings revenue.

---

## Appendix — sources
- **yfinance live pull** (prices/multiples/margins, as-of 2026-07-05 00:32 ET): `live_data.json`, code `fetch_infosvc.py` [V].
- **SEC EDGAR XBRL companyfacts + FY2025 10-Ks + Q1-FY2026 10-Qs** — SPGI CIK 0000064040, MCO CIK 0001059556, MSCI CIK 0001408198 (segment revenue, recurring %, cash flow, balance sheet, capital return) [V primary].
- **SEC OCR 2025 Staff Report on NRSROs** (10 NRSROs; Big Three 93.38% share YE2024; QIB track-record barrier) [V].
- **SIFMA** — US corporate bond issuance 2026 YTD +21.1% [A secondary]; **ETFGI** — global ETF AUM ~$23.08T end-May-2026 [V secondary].
- **Federal Reserve** — funds rate 3.50–3.75%, held through all four 2026 meetings to June 17 [V].
- **Morningstar** — "Reviewing Our Moats for the Rise of AI" (2026-03-06); FactSet moat cut to None (2026-03-04) [V metadata; A body].
- MSCI–BlackRock ETF index-licensing extension to 2035 (Feb 2026) [V]. Moody's Research Assistant / MA GenAI ARR metrics (earnings transcripts) [A]. Forbes 2026-06-08, Seeking Alpha 2026-06-09 AI-bear pieces [A].
- **Verification caveats:** analyst-narrative and AI-uplift metrics are largely single-source/secondary [A/U]; SPGI's Q1'26 AI-renewal-uplift figures rest on one secondary source [A/U]; MSCI's 2026-06-25 −5.94% drop has no sourced cause [U]; exact NRSRO 80% duopoly split leans on a dated figure [A]. All core financials (revenue, segments, income, cash flow, balance sheet, share count, capital return) are [V] from SEC XBRL/10-Ks.
