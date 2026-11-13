# Stage 4 Deep Dive — Arch Capital Group (ACGL)

**Company:** Arch Capital Group Ltd. — Bermuda-domiciled specialty insurance + reinsurance +
**mortgage insurance** holding company. NASDAQ: **ACGL**, USD. S&P 500. SEC CIK 0000947484.
**Analyst:** Claude (Opus 4.8) for Hooman Shariati. **Not financial advice.**
**Written:** 2026-08-26. Surfaced in the cheap-quality screen refresh (2026-08-26) as a
newly-cheap specialty insurer.

> **ANTI-HALLUCINATION.** Every figure carries a source + as-of date. yfinance figures are a
> **VERIFIED** real fetch (2026-08-26, `/opt/venv/bin/python3`). Company financials cross-checked
> against Arch's SEC filings (10-K filed 2026-02-26; Q2 2026 8-K/press release filed 2026-08-04;
> supplements) surfaced by a research subagent with UA `Hooman Shariati hshariati@adobe.com`.
> Reinsurance-cycle and analyst data from artemis.bm / Guy Carpenter / MarketBeat / TipRanks.
> Confidence marked VERIFIED / ASSUMED / UNVERIFIED throughout.
>
> **⚠️ TWO PREMISE CORRECTIONS (both VERIFIED vs SEC filings):**
> 1. **Marc Grandisson is no longer CEO** — he *retired* as CEO and from the board effective
>    **2024-10-15**. **Nicolas Papadopoulo is CEO** (effective 2024-10-13). The brief listed
>    Grandisson as CEO; that is now stale. See §3/§5.
> 2. **ACGL pays NO regular common dividend** (the brief's assumption is correct) — but note the
>    **one-time $5.00/sh (~$1.9bn) special dividend paid in 2024**. Capital return is buyback-led.

---

## 0. Screen snapshot — VERIFIED

yfinance `.info` pull, **as-of 2026-08-26** (`ACGL`):

| Metric | Value | Note |
|---|--:|---|
| Price | **$100.72** | 52-wk range $82.45 – $107.09 |
| Market cap | **~$34.3bn** | |
| P/E (trailing) | **7.88** | trailing EPS $12.78 (flattered by 2024–25 peak + buyback) |
| P/E (forward) | **10.31** | forward EPS $9.77 — **note: forward P/E > trailing** (earnings expected DOWN) |
| P/B | **1.47** | book value/sh **$68.32** (yfinance); co-reported BVPS $68.04 at 6/30/26 |
| ROE (TTM) | **19.9%** | |
| ROA | 4.12% | |
| Dividend yield | **None (0%)** | no regular common dividend; payout 0 |
| Beta | **0.29** | low-beta (insurance) |
| Net income (TTM) | **$4.65bn** | |
| earningsGrowth (YoY) | **−7.1%** | earnings already rolling over |
| revenueGrowth (YoY) | **−10.5%** | premium volume shrinking (discipline in soft market) |
| Analyst reco | "buy" (19 analysts) | mean target **$111.87** (~+11%) |

**The single most important tell in this table:** forward P/E (10.3×) is **higher** than trailing
(7.9×), and both earningsGrowth (−7.1%) and revenueGrowth (−10.5%) are **negative**. The market is
explicitly pricing **declining earnings** — the trailing 7.9× is 7.9× a **peak** number. This is
the crux of the whole thesis (§2). **VERIFIED.**

---

## 1. Business & Thesis

**What it is.** Arch writes three things, and the mix is the whole story:

| Segment | FY2025 GPW | FY2025 NPW | U/W income | Combined ratio | ~% of U/W income |
|---|--:|--:|--:|--:|--:|
| **Insurance** (specialty primary/E&S) | $10.4bn | $7.8bn | $375m | **95.2%** | ~13% |
| **Reinsurance** (property-cat, casualty, specialty) | $11.1bn | $7.6bn | $1,558m | **80.8%** | ~53% |
| **Mortgage** ("Arch MI") | $1.3bn | $1.1bn | $1,000m | **14.6%** | **~34%** |
| **Total** | ~$22.9bn | $16.5bn | ~$2,933m | **82.8%** | 100% |

Source: Arch FY2025 financial supplement (8-K filed 2026-02-09) + 10-K (2026-02-26). **VERIFIED.**

**Why the mortgage arm makes Arch different from a pure P&C insurer (the key structural point).**
Mortgage insurance produces **~34% of group underwriting income off only ~6% of premiums** —
because MI runs a ~14.6% combined ratio vs 80–98% for P&C. Five reasons it matters:
1. **Different risk driver — credit, not catastrophe.** MI losses come from unemployment,
   home-price declines and the credit cycle, NOT hurricanes/wildfires/quakes. It diversifies away
   from the nat-cat correlation that dominates the two P&C segments.
2. **Counter-cyclical to P&C.** MI is most profitable when housing/economy is healthy — exactly
   when P&C pricing softens. MI stress (recessions) rarely coincides with big cat years. Smooths
   group earnings.
3. **Annuity-like recurring premium** earned over the life of multi-year mortgages (sticky
   persistency) vs one-year P&C churn.
4. **Extraordinary structural margin** — ~$1.0bn of U/W income on ~$1.3bn premiums in FY2025.
5. **Separate capital regime (PMIERs)** — US MIs must meet the GSEs' Private Mortgage Insurer
   Eligibility Requirements, distinct from Bermuda/P&C group capital.
Arch became a top-6 US MI via the **2016 acquisition of United Guaranty from AIG for ~$3.4bn**
(announced 2016-08-15, closed Dec 2016; $2.2bn cash + $975m Arch shares + up to $250m pre-close
dividend), which it billed as creating "the largest private mortgage insurer in the world" by
insurance-in-force. **VERIFIED.**

**The value thesis (why it surfaced).** A best-in-class, fortress-rated (AM Best A+ / S&P AA−)
specialty compounder trading at **1.47× book on ~20% ROE and ~7.9× trailing earnings**, cheaper on
P/B than Chubb (1.76×) and far below its own quality — *if* that ~20% ROE is durable. The bull case
is book-value compounding (its real claim to fame, §3) + a diversifying mortgage arm + aggressive
buybacks below/near recent prices. **The bear case is that the 20% ROE is a cyclical peak** and the
1.47× is cheap precisely because the market expects returns to fade (§2, §4).

**Where are we in the cycle?** The reinsurance/specialty hard market **peaked at Jan-2023 renewals
and is now in an accelerating soft market** — property-cat rate-on-line +29% (2023) → +2.3% (2024)
→ −6.6% (2025) → −12% (Jan 2026) → ~−16% YTD mid-2026 (Guy Carpenter via artemis.bm). This is the
**same cycle-turn that made Swiss Re a WATCH** in prior research. Arch's own numbers confirm the
underlying margin has rolled over (§2b). **VERIFIED (cycle direction).**

---

## 2. Valuation

### 2a. Multiples vs peers (yfinance `.info`, all **2026-08-26** — VERIFIED real fetch)

| Company | P/E (ttm) | Fwd P/E | P/B | ROE | Div yld | Beta | Note |
|---|--:|--:|--:|--:|--:|--:|---|
| **Arch (ACGL)** | **7.9** | **10.3** | **1.47** | **19.9%** | **0%** | 0.29 | fwd P/E > ttm → earnings ↓ |
| Chubb (CB) | 12.2 | 11.8 | 1.76 | 14.8% | 1.19% | 0.39 | premier global P&C |
| Travelers (TRV) | 10.0 | 12.3 | 2.34 | 26.5% | 1.35% | 0.46 | US P&C; highest P/B |
| Hartford (HIG) | 9.7 | 10.2 | 1.97 | 22.1% | 1.74% | 0.46 | *(parallel deep dive)* |
| RenaissanceRe (RNR) | 5.7 | 8.1 | 1.25 | 21.5% | 0.50% | 0.17 | pure-play reinsurer |
| Everest (EG) | 8.0 | 6.4 | **0.95** | 12.6% | 2.13% | 0.28 | cheapest — reserve scars |

**Read (ASSUMED interpretation of VERIFIED multiples).** Arch sits **mid-pack on P/B (1.47×)** —
below Chubb/TRV/HIG, above the pure reinsurers RNR (1.25×) and Everest (0.95×). Because Arch earns
~20% ROE, **1.47× book is genuinely cheap *relative to returns*** — Travelers earns a similar/higher
ROE (26.5%) at 2.34× book, and Hartford earns 22% at 1.97×. On a P/B-vs-ROE line, Arch is the
**outlier that trades cheap for its return profile**. The market's answer to "why?" is: (a) that ROE
is judged unsustainable (peak cycle), and (b) the earnings mix now leans on the two P&C segments
whose pricing is softening. RNR and Everest are cheaper on P/B but are *pure* reinsurers with no
mortgage diversifier and (Everest) a $1.7bn+ 2024 casualty reserve scar. **The P/B≈P/E×ROE sanity
check** (7.9 × 0.199 = 1.57 ≈ 1.47) is internally consistent. **VERIFIED multiples; ASSUMED read.**

### 2b. vs own history — is ~20% ROE / the low P/B a peak-cycle artifact? (THE key call)

**P/B history** (year-end price ÷ split-adjusted co-reported BVPS; prices VERIFIED yfinance, BVPS
VERIFIED FY2024/25/26 from Arch, FY2021/23 from stockanalysis.com = ASSUMED):

| Year-end | Price | BVPS | P/B |
|---|--:|--:|--:|
| 2021 | $42.27 | $33.74 | **1.25×** |
| 2023 | $70.62 | $47.12 | **1.50×** |
| 2024 | $92.35 | $53.11 | **1.74×** |
| 2025 | $95.92 | $65.11 | **1.47×** |
| now (2026-08-26) | $100.72 | $68.04 | **1.48×** |

So today's **1.47–1.48× is mid-range for Arch's own recent history** (1.25×–1.74×) — it de-rated
from the 1.74× 2024 peak even as book value kept compounding (+22.6% in FY2025). It is **cheaper
than 2024 but not distressed** — the multiple compression is the market pre-empting the cycle turn.

**Underlying-margin evidence the peak has rolled over (VERIFIED, Arch releases):**
- Consolidated **combined ratio ex-cat & ex-PYD** (the cleanest margin gauge) bottomed **~78.6%
  (FY2024)** → drifted UP: 80.9% (Q2'25) → 82.5% (Q2'26, +160bps YoY).
- **Reinsurance ex-cat AY combined** rose from ~74.9% (Q4'25) to **79.9% (Q2'26)**.
- Q2'26 headline combined ratio **83.5%**, up **~2.3 pts YoY**; reinsurance NPW **−10% YoY**;
  operating ROE **15.3%** annualized (vs 18.9% in Q4'25). Earnings already falling.
- FY2026 consensus operating EPS ~$9.3 vs FY2025 GAAP EPS $11.60 — a **plateau-to-decline**.

**Verdict on the peak question (ASSUMED, argued honestly both ways):**
- **YES — this is largely peak earnings.** The clean ~78–80% combined ratios of 2024–25 coincide
  with the *top of the pricing cycle* (rates peaked Jan-2023, still elevated in absolute terms) AND
  a benign 2025 cat year (no US hurricane landfall — first since 2015). Rates are now falling
  10–20%; the underlying loss ratio is visibly widening; management itself says margins are "under
  pressure" and the market is "entering the early stages of a softening cycle." A normalized ROE is
  more like **mid-teens** (matching the 14.3% *forward* implied ROE from yfinance's forward EPS
  ÷ BVPS) than 20%. **The 7.9× trailing P/E is 7.9× a peak number; the honest multiple is the
  ~10.3× forward.**
- **NO / partly — more durable than a pure reinsurer.** Three real cushions: (1) the **mortgage
  segment (~34% of U/W income)** is *counter*-cyclical and not rate-sensitive — it doesn't soften
  with reinsurance; (2) Arch is **rotating capital toward the still-firm casualty/specialty lines
  and shrinking property-cat**, defending margin rather than chasing volume (the textbook
  late-cycle Arch playbook — and why premiums are *shrinking*, a *quality* signal); (3) higher
  investment income ($417m pre-tax in Q2'26) is a structural tailwind vs the ZIRP years. So a
  **soft landing to mid-teens ROE, not a collapse**, is the base case.
- **Bottom line:** Arch is **cheap on peak-ish earnings but only fairly-valued on normalized
  earnings** — 1.47× book on a ~14–16% normalized ROE is *reasonable, not a screaming bargain*.
  The mortgage diversifier makes it a **better-protected way to own the specialty cycle than a pure
  reinsurer** (RNR/EG/Swiss Re), but it does NOT escape the cycle. Confidence: cycle direction
  **VERIFIED**; degree of ROE mean-reversion **ASSUMED**.

---

## 3. Quality (the real story: book-value compounding)

- **Book-value-per-share compounding — its claim to fame.** BVPS roughly **doubled from ~$33.74
  (12/31/21) to $68.04 (6/30/26)** — ~16–17% CAGR over 4.5 years (my arithmetic on VERIFIED
  endpoints); FY2025 alone **+22.6%** ($53.11 → $65.11). Arch's headline 10-K lifetime metric is
  "growth in BVPS + accumulated dividends" annualized since 12/31/2001; the widely-cited long-run
  figure is **~mid-teens % over ~two decades** — **UNVERIFIED** (couldn't pin the exact 10-K p.1
  number to a primary quote), but the recent VERIFIED trajectory corroborates a low-double-digit-plus
  compounder. This is the single best reason to own Arch: a disciplined underwriter that **grows
  intrinsic value per share through the cycle**, amplified by buybacks shrinking the share count
  ~8.6% in the last year.
- **Underwriting record.** Consolidated combined ratio **82.8% (FY2025)**, **83.5% (Q2'26)** —
  consistently sub-90, best-in-class for a diversified specialty writer. Reinsurance 80.8% FY2025;
  Insurance 95.2%; Mortgage 14.6%. **VERIFIED.**
- **Reserve conservatism (a genuine quality marker).** Group reserve development has been **net
  FAVORABLE every quarter** through 2024–26: FY2024 **$507m favorable**, FY2025 **$600m favorable**
  (Reinsurance $322m, Mortgage $235m, Insurance $43m). Arch *did* strengthen casualty modestly
  inside otherwise-favorable segments ($64m adverse reinsurance casualty in FY2025) — a prudent tick
  vs peers who took big charges (**Everest ~$1.7bn casualty action for FY2024**; CNA $77m Q2'26).
  Management: "we just don't see [social-inflation relief] in the numbers yet" — cautious, no
  discrete charge. **This is the opposite of Swiss Re's $3.1bn 2024 forced reserve build.** VERIFIED.
- **Balance sheet / ratings.** Total capital ~$28.3bn (Q2'26). Operating subs **AM Best A+
  (Superior), S&P AA−, Moody's A1, Fitch AA−** (Arch IR; standing VERIFIED, dated actions mostly
  not). Fortress. Beta 0.29.
- **Leadership.** CEO **Nicolas Papadopoulo** (since 2024-10-13; at Arch since 2001, ex-President &
  CUO, actuary). CFO François Morin. Maamoun Rajeh President (Mortgage+Reinsurance). Grandisson
  retired 2024-10-15 — a **clean, planned succession** of a long-tenured insider, not a rupture.
  VERIFIED.

---

## 4. Bear Case / Risks

1. **Softening reinsurance/specialty pricing cycle (THE #1 risk — same as made Swiss Re a WATCH).**
   Property-cat RoL −12% (Jan 2026), ~−16% YTD mid-2026 — steepest softening since the late 1990s;
   AM Best cut the sector to Stable, **Fitch calls it "Deteriorating" into 2027**, record $785bn
   reinsurer capital = buyers' market. Arch's own ex-cat combined has widened +160bps YoY and
   reinsurance NPW is −10%. A prolonged soft market pushes ROE toward the low-teens, from which
   1.47× book is only *fair*. **Core bear thesis.** VERIFIED direction.
2. **Cheap on peak earnings.** Forward P/E (10.3×) > trailing (7.9×); management guides to
   softening. The headline "7.9× P/E" bargain is an artifact of peak margins + a benign 2025 cat
   year + buyback-shrunk share count. VERIFIED.
3. **Catastrophe volatility.** Q1'25 **LA wildfires cost Arch $547m** (combined ratio spiked to
   90.1% that quarter); FY2024 cats ~$1.1bn (Helene/Milton). A heavy hurricane year arriving *as
   rates soften* is the classic double-hit. 2025 was benign — do not extrapolate.
4. **Mortgage-insurance / housing-downturn exposure.** IIF $478.9bn; US primary delinquency 2.07%
   (6/30/26, low and improving QoQ but up YoY from 1.93%). PMIERs sufficiency **165%** (down from
   179% on the GSEs' Aug-2024 update; pro-forma ~162% fully phased). The segment's fat margins rest
   on an embedded home-equity cushion from 2020–24 HPA — a genuine home-price *decline* (not just
   affordability stall) would raise claims and compress the ~34%-of-profit engine. Currently
   healthy; a real tail risk in a housing/credit recession. VERIFIED (data); ASSUMED (severity).
5. **No dividend.** Zero regular common dividend — pure total-return/compounding vehicle. Fine for
   Hooman's total-return tilt, but no income cushion, and capital return is discretionary buybacks
   (which Arch rightly throttles in hard markets). VERIFIED.
6. **Bermuda tax / corporate minimum tax** — the 15% global minimum tax erodes the historical
   Bermuda tax advantage somewhat (industry-wide, not Arch-specific). ASSUMED-relevant.

**Bull rebuttal (both sides).** The mortgage arm is counter-cyclical and rate-insensitive; Arch is
*shrinking* into the soft market (discipline, not desperation); reserves are net-favorable and
conservatively set (unlike peers); investment income is a structural tailwind; buybacks below/near
book compound BVPS; ratings are fortress. If ROE soft-lands to mid-teens rather than collapsing,
1.47× book is a reasonable entry into a serial compounder — *better protected than any pure
reinsurer.*

---

## 5. Catalysts & Timing

- (+) **Aggressive buybacks** — ~$1.9bn (2025), ~$1.17bn in Q2'26 alone (12.4m shs @ $94.38, i.e.
  *below* current price), ~$2.16bn authorization remaining (+$3.0bn added Apr 2026). Directly
  compounds BVPS while the multiple is depressed. VERIFIED.
- (+) **Casualty/specialty stays firm** while property-cat softens — Arch's rotation could defend
  group margin better than peers expect. Q2'26 already beat (op EPS $2.56 vs ~$2.47 consensus).
- (+/−) **Cat-season outcome** — a benign 2026 extends the record; a heavy year exposes the cycle
  turn. Neutral-to-negative skew.
- (−) **Each renewal season (Jan/Jun 2026, Jan 2027)** is now a "how bad is the softening" event —
  the dominant swing factor, trending against the P&C segments.
- **Analyst view:** consensus ~Hold/Moderate-Buy, mean target ~$111 (~+11%); post-Q2'26 mostly
  target *raises* (BofA $134 Street-high, RBC $120, UBS $120), **Goldman lone Sell $93** on peak
  earnings, KBW trimmed to $99. Sentiment constructive but not euphoric. VERIFIED (aggregators).
- **Timing read (ASSUMED):** no urgent catalyst *up*; the risk is a soft-market/big-cat de-rating
  *down* toward ~1.2–1.3× book — which would be the higher-margin-of-safety entry.

---

## 6. Fit for Hooman

Hooman runs a **small, underweight Financials sleeve = CI (Canadian financials/CI Financial) +
BRK-B**, total-return / quality-at-a-price tilt, Canadian investor (no US-person constraints — no
issue here; ACGL is Bermuda/US-listed, ordinary for a Canadian).

- **Quality fit: strong.** ACGL is a genuine best-in-class compounder (net-favorable reserves,
  fortress ratings, ~20% ROE, disciplined shrink-in-soft-markets) — exactly the "high-quality
  company that's cheap" profile the project hunts. Beta 0.29, low equity correlation = a defensive
  diversifier.
- **Does it duplicate BRK-B?** *Partially, and this is the main caution.* Berkshire is, at its core,
  a giant insurance/reinsurance float machine (GEICO, Gen Re, BHRG, plus Alleghany specialty). Adding
  ACGL **doubles down on insurance-underwriting-cycle risk** already inside BRK-B. It is not a clean
  diversifier away from what Hooman owns via Berkshire — it's a *concentrated, purer* bet on the
  specialty/reinsurance + mortgage cycle. The mortgage arm is the one piece Berkshire doesn't
  meaningfully replicate.
- **Does it carry SREN-style reinsurance-cycle risk?** *Yes — same cycle, better-cushioned.* Both
  Arch and Swiss Re are exposed to the softening property-cat market that made SREN a WATCH. Arch is
  **better protected** (mortgage counter-cyclicality, casualty rotation, cleaner reserves, US-listed
  no-FX) but it does NOT escape the peak-earnings problem — you'd be buying near the cycle top, same
  as SREN.
- **HIG vs ACGL (parallel agent doing HIG):** On the live numbers, **HIG earns a higher ROE (22.1%
  vs 19.9%), pays a dividend (1.74% vs 0%), and is a US primary P&C/group-benefits writer with much
  LESS property-cat/reinsurance-cycle exposure** — i.e. HIG is the *more defensive, less
  cycle-peaked* insurer add, but at a higher P/B (1.97× vs 1.47×). **ACGL is the higher-quality
  compounder and cheaper on P/B-for-ROE, but more cycle-exposed and duplicative of BRK-B's insurance
  float.** If the goal is *diversify the Financials sleeve away from insurance-cycle risk*, HIG's
  primary-P&C/benefits mix is the cleaner complement to BRK-B; if the goal is *own the single best
  specialty compounder cheaply and you're willing to underwrite the cycle*, ACGL wins on quality.
  (Cross-check the HIG agent's numbers before finalizing.)
- **Net fit:** a legitimate quality-at-a-price candidate, but it **stacks insurance risk on top of
  BRK-B** and is bought near a pricing peak — argues for **WATCH / small starter at best**, not a
  core add, unless it de-rates.

---

## 7. Scorecard & Verdict

Weights per CLAUDE.md §3 (Cheapness 30 / Quality 30 / Trap-risk 20 / Moat 15 / Catalyst 5).

| Factor | Weight | Score /10 | Weighted | Rationale |
|---|--:|--:|--:|---|
| **Cheapness** | 30% | **6** | 1.80 | 1.47× book / 7.9× *trailing* / 10.3× *forward*, ~20% ROE — cheap-for-its-ROE vs peers (CB/TRV/HIG all richer P/B), and mid-range vs its own 1.25–1.74× history. Docked because the low trailing multiple is on **peak earnings** (fwd P/E > ttm); on normalized mid-teens ROE it's only *fair*. |
| **Quality** | 30% | **9** | 2.70 | Best-in-class: ~16%+ BVPS compounding, sub-83% combined ratio, **net-favorable reserves every quarter** (vs peers' big charges), AM Best A+, counter-cyclical mortgage arm, clean insider CEO succession. Top-tier. |
| **Trap risk (inverse)** | 20% | **6** | 1.20 | Not a value trap in the balance-sheet sense (fortress, growing book). But real "cheap on peak earnings" risk — earnings already −7% YoY, revenue −10%, ex-cat margin widening, soft market accelerating. The trailing multiple flatters. |
| **Moat & leadership** | 15% | **8** | 1.20 | Genuine underwriting skill + scale + data (esp. mortgage, a top-6 US MI oligopoly); disciplined capital allocation (shrinks in soft markets, buys back below book). Specialty insurance is competitive but Arch has proven through-cycle edge. |
| **Catalyst** | 5% | **5** | 0.25 | Aggressive sub-price buybacks (+); Q2'26 beat; but dominant swing (renewals) skews negative and no near-term re-rating catalyst. |
| **TOTAL** | 100% | | **7.15 / 10** | |

### VERDICT: **WATCH** (leaning higher-quality than SREN, but same cycle-timing problem)

Arch is a **higher-quality name than Swiss Re** — a serial book-value compounder with net-favorable
reserves, fortress ratings, and a counter-cyclical mortgage arm that no pure reinsurer has — and it
is **cheaper on P/B-for-ROE than Chubb, Travelers or Hartford**. But the headline cheapness (7.9×
trailing) is **7.9× peak-cycle earnings**: the softening property-cat market that made SREN a WATCH
is the *same* market Arch's reinsurance segment sits in, its underlying margin has already rolled
over, and the market is pricing declining earnings (fwd P/E > ttm). Bought at 1.47× book on ~20%
ROE, you're paying a fair-to-slightly-cheap price on **normalized** earnings and a cheap price on
**peak** earnings — decent, not a screaming bargain, and it **duplicates BRK-B's insurance exposure**.

- **Flip-to-BUY trigger:** a de-rate toward **~1.2–1.3× book** (a soft-market or big-cat drawdown)
  with reserves/ratings intact — buy the best specialty compounder *after* the cycle scares the
  multiple, not near the peak. A small starter here is defensible for the quality; a full add is not.
- **vs HIG (for the sleeve):** ACGL = higher-quality compounder, more cycle- and BRK-B-duplicative;
  HIG = more defensive, dividend-paying, cleaner complement. Confirm against the parallel HIG dive.

### Rough fair-value range (ASSUMED — not a price target)
- **Bear (normalized mid-teens ROE, soft market bites):** ~1.15–1.25× book → **~$78–$85**.
- **Base (soft landing, mortgage cushions, mid-teens–17% ROE):** ~1.35–1.55× book on a growing
  ~$70 book → **~$95–$110** (i.e. ~current; consensus mean $111.87).
- **Bull (casualty stays firm, benign cats, ~18%+ ROE holds, buybacks compound):** ~1.6–1.7× book →
  **~$115–$125**.
Skew is roughly symmetric-to-slightly-negative near-term given the cycle; the long-run compounding
is the real prize *if bought cheaper*. **ASSUMED — my judgment, not verified.**

---

## 8. Sources & Confidence

- **yfinance** `.info` for ACGL + CB/TRV/HIG/RNR/EG/BRK-B, **2026-08-26** (real fetch via
  `/opt/venv/bin/python3`) — all live multiples, ROE, EPS, targets, NI, growth. **VERIFIED.**
  Historical equity (2022–2025) and shares also from yfinance. **VERIFIED.**
- **Arch SEC filings** (research subagent, EDGAR UA `Hooman Shariati hshariati@adobe.com`):
  Q2 2026 press release / supplement (8-K filed 2026-08-04); FY2025 10-K (filed 2026-02-26);
  Q4/FY2025 release (8-K 2026-02-09); United Guaranty 8-K (2016-08-16). Segment data, combined
  ratios, BVPS, reserve development, cat losses, buybacks, PMIERs, delinquency, CEO succession —
  **VERIFIED** from primary filings.
- **Guy Carpenter / artemis.bm / Howden / Gallagher Re** — property-cat rate-on-line index and
  renewal commentary Jan 2023→mid-2026; AM Best (Stable) / Fitch (Deteriorating) sector outlooks.
  **VERIFIED direction** (some via reader-proxy of 403-blocked canonical URLs).
- **MarketBeat / TipRanks** — analyst consensus, targets, rating changes (BofA/RBC/UBS/JPM/GS/KBW),
  **2026-08-26**. **UNVERIFIED** vs a 2nd source per action.
- **stockanalysis.com** — FY2021/FY2023 BVPS for the P/B-history table; peer P/B cross-checks.
  **ASSUMED** (aggregator).
- **Could NOT verify:** exact 10-K p.1 lifetime BVPS CAGR (the "~15% since 2001" is UNVERIFIED);
  dated S&P/Moody's/Fitch rating actions 2024–26; Arch MI exact market-share rank; PMIERs dollar
  amounts (only ratios); FY cat totals are derived sums; David Gansberg's current status (co-Pres
  Nov-2024, absent from current leadership page). Earnings-call quotes are transcript mirrors —
  substance VERIFIED, exact wording ASSUMED.
- **Interpretation confidence:** cycle direction & underlying-margin-rollover **VERIFIED**;
  peak-vs-normalized-ROE degree, fair-value range, scorecard, and verdict are my **ASSUMED** judgment.
