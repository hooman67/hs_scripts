# RESEARCH PLAN — Finding Cheap, Quality Stocks

Last updated: 2026-07-01 by Claude (Opus 4.8). Status: **CHOSEN — Hybrid A+B, quality-first,
global. Ready for Stage 0.**

**Locked scope (see `DECISIONS.md` for rationale):**
- Methodology: **Hybrid A+B**, cross-validated, deep-dive the overlap.
- Framing: **quality-first** — high-quality companies that are cheap; quality dominates.
- Universe: **global** (US mid/large + developed + emerging; wants ex-US diversification).
  **Small caps as exceptions** — exceptional quality overrides the market-cap floor.
- Data: **free now** (Damodaran + yfinance + EDGAR), paid API only if EM coverage too thin.
- Output: **one-shot report + deep dives now**, recurring monitor later. Total-return tilt.

This document proposes the methodologies (below, for the record). The chosen funnel is the
Hybrid; the finalized stage-by-stage spec is mirrored in `CLAUDE.md §3`.

---

## 0. Background — what "value" methods actually work (so we don't reinvent)

Four well-established, evidence-backed families of value investing. We'll borrow from all:

1. **Top-down sector rotation into cheap sectors.** Rank sectors by valuation vs their *own*
   history (not just vs market — a sector can be "always cheap"). Buy the cheap, sell the
   dear. Signal: sector forward P/E, EV/EBITDA, P/B percentile vs 10–20yr history.
2. **Classic quantitative value screens.** Low P/E, P/B, EV/EBITDA, high FCF yield, high
   shareholder yield. Academic backing: value factor (Fama-French HML), though it needs a
   quality overlay to avoid traps.
3. **Quality-at-a-reasonable-price (QARP) / "Magic Formula" style.** Joel Greenblatt: rank on
   *cheapness* (earnings yield = EBIT/EV) **and** *quality* (ROIC) together; buy names strong
   on both. This is the cleanest formalization of "cheap AND high-quality."
4. **Contrarian / special situations.** Deeply out-of-favor sectors, spin-offs, net-nets,
   sum-of-the-parts. Higher effort, higher variance — treat as an optional lane.

**The value-trap problem** (the #1 risk): cheap ≠ good. A stock is cheap for a reason. Every
proposal below includes a **quality / trap filter** (Piotroski F-score, ROIC, debt, FCF,
margin trend) so we don't buy melting ice cubes.

---

## The three proposals

Each is a funnel. They differ in **where they start** (sector vs company) and **how much
machinery** they use. All share Stage 0 (data setup) and a final deep-dive stage.

### Proposal A — "Top-Down Cheap-Sector → Leaders" (matches Hooman's primary framing)

The most direct read of the ask. Start at the sector, drill to the quality leaders.

- **A1. Rank sectors by cheapness.** Using NYU Damodaran + Yardeni + multpl: for each of ~11
  GICS sectors (and finer sub-industries), compute current forward P/E, EV/EBITDA, P/B and
  the **percentile vs their own 10–20yr history**. Flag sectors in the cheap tail (e.g.
  bottom quartile vs own history) — this is *relative-to-self* cheap, which beats
  relative-to-market.
- **A2. Sanity-gate the cheap sectors.** Is it cheap for a *temporary/cyclical* reason
  (opportunity) or a *structural/secular-decline* reason (trap)? Brief qualitative check +
  earnings-revision trend.
- **A3. Find leaders in each surviving cheap sector.** Rank constituents by quality (ROIC,
  ROE, margins, balance sheet) and moat/market-share. The "leader that is cheap because its
  whole sector is out of favor" is the sweet spot.
- **A4. Quality/trap filter** on the leader shortlist (Piotroski, FCF, debt, margin trend).
- **A5. Deep dive** on finalists.
- **Pros:** directly answers the primary ask; sector data (Damodaran) is free and high
  quality; naturally surfaces "good company dragged down by bad sector sentiment."
- **Cons:** misses cheap quality names in *expensive* sectors (Hooman's bottom-up case);
  sector cheapness data updates only ~yearly from Damodaran (mitigate with live prices).

### Proposal B — "Bottom-Up Quality-at-a-Price Screen" (Magic-Formula-style)

Start at the company. Screen the whole universe for cheap **and** high-quality simultaneously.

- **B1. Universe.** e.g. US-listed, market cap > $X, exclude financials/REITs initially
  (different accounting) or handle separately.
- **B2. Dual rank.** Rank every name on **cheapness** (earnings yield EBIT/EV, FCF yield) and
  **quality** (ROIC, ROE, gross-margin stability) — Greenblatt combined rank. Top combined
  scores = "cheap and good."
- **B3. Trap filter.** Piotroski F-score ≥ 6–7, positive FCF, manageable debt, no
  deteriorating margins/accruals red flags.
- **B4. Tag by sector** to see clustering (often the survivors *cluster* in a few cheap
  sectors — which cross-validates Proposal A).
- **B5. Deep dive** on finalists.
- **Pros:** catches Hooman's "great company that happens to be cheap even if its sector
  isn't"; fully data-driven, reproducible, and rankable; least hand-waving.
- **Cons:** needs per-company fundamentals for a big universe (data plumbing); pure screens
  can surface accounting-distorted or one-off-cheap names → trap filter must be strict.

### Proposal C — "Contrarian / Special-Situations Deep Dive" (highest effort, highest variance)

Go where others won't. Focus on maximum-pessimism sectors and structural mispricings.

- **C1. Find maximum-pessimism zones.** Sectors/industries at multi-year-low valuations,
  heavy negative sentiment, forced selling (e.g. index deletions, tax-loss season, sector
  ETFs at outflow extremes).
- **C2. Within them, hunt specific setups.** Net-nets (price < net current asset value),
  sum-of-the-parts discounts, recent spin-offs, hated-but-deleveraging balance sheets.
- **C3. Rigorous per-name work** (this lane is deep-dive-heavy from the start).
- **Pros:** where the biggest mispricings live; differentiated.
- **Cons:** labor-intensive, higher risk, harder to systematize/automate, more judgment →
  more room for error. Best as a *satellite* lane, not the core.

---

## RECOMMENDED: Hybrid (A + B run in parallel, C optional later)

**Run A and B in parallel and use them to cross-validate each other, then deep-dive the
intersection and the best of each.** This is the strongest plan and maps exactly onto
Hooman's two paths:

- **A gives the top-down view** (which sectors are cheap → their quality leaders) = Hooman's
  path 1.
- **B gives the bottom-up view** (cheap quality companies anywhere) = Hooman's path 2.
- **Where A and B agree** (a cheap-sector leader that *also* tops the quality-at-a-price
  screen) = highest-conviction candidates.
- **Where they disagree** is informative too: B-only names = cheap quality in an expensive
  sector; A-only names = a cheap sector whose leaders aren't screening cheap yet (watchlist).
- **C** stays a labeled optional satellite lane for later, on 1–2 max-pessimism sectors.

### Concrete funnel (the hybrid), with parallelism

```
Stage 0  Data setup (serial, once)
         └─ NYU Damodaran datasets + yfinance + EDGAR company-facts. Verify reproducible pulls.

Stage 1  Screen  (A and B run as PARALLEL subagents)
         ├─ A1–A2: sector cheapness vs own history → cheap-sector list      → screens/sector_cheapness.md
         └─ B1–B3: universe-wide cheap+quality dual rank + trap filter      → screens/quant_screen.md

Stage 2  Merge & quality/trap filter (serial — depends on both screens)
         └─ combine, tag sector clustering, apply Piotroski/FCF/debt gate   → screens/candidates.md

Stage 3  Leaders in cheap sectors (parallel — one subagent per surviving sector)
         └─ rank constituents by ROIC/moat/share; find the cheap leaders

Stage 4  Deep dives on finalists (parallel — one subagent per finalist, but only ~top 6–10)
         └─ thesis, valuation (DCF or multiple-based), risks, catalysts,
            confidence-marked claims                                        → deep_dives/{ticker}/

Stage 5  Ranked comparison table + write-up for Hooman                      → screens/ranked_output.md
```

### Scoring (draft — tune with Hooman after first run)

A weighted scorecard per finalist (0–10 each, weights sum to 100%):
- **Cheapness (30%)** — valuation percentile vs own history + vs peers (EV/EBITDA, P/E,
  FCF yield).
- **Quality (30%)** — ROIC/ROE, margin stability, balance-sheet strength.
- **Trap-risk (inverse, 20%)** — Piotroski, FCF trend, debt maturity, earnings-revision trend.
- **Moat / leadership (15%)** — market share, durable advantage, pricing power.
- **Catalyst / timing (5%)** — is there a reason it re-rates in a reasonable horizon?

### Anti-hallucination discipline (applies to every stage)

- Every multiple, price, margin, and ratio is **pulled from a cited source** with an as-of
  date — never recalled from memory.
- Prefer **code that fetches data** (yfinance/EDGAR/Damodaran CSV) so runs are reproducible
  and auditable.
- Cross-check any figure that drives a ranking against a second source.
- Mark every feasibility/quality claim VERIFIED / ASSUMED / UNVERIFIED.

---

## Scoping questions for Hooman (needed before Stage 0)

1. **Universe & geography** — US-only, US + developed markets, or global?
2. **Market-cap floor** — include small/micro-caps (more mispricing, more risk) or large/
   mid-cap only (safer, cleaner data)?
3. **Data budget** — free sources only (Damodaran + yfinance + EDGAR — slower, some plumbing)
   or OK to use a paid fundamentals API (FMP/Alpha Vantage paid tier) for cleaner bulk data?
4. **Style tilt** — deep-value / total-return, or a dividend-income tilt?
5. **Automation** — one-shot report now, or stand up a recurring monitor from the start?
6. **Anything off-limits** — sectors/companies to exclude (e.g. tobacco, no financials, ESG
   constraints)?

(These are captured as pending items in `DECISIONS.md` and `PROJECT_STATE.md`.)
