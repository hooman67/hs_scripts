# Fin-Research — Value Investing Research (Project State & Operating Manual)

**This is the single source of truth for this project.** If you are a new agent picking
this up, read this file top to bottom first. It tells you the goal, what's been done, where
execution stands, and how to behave.

Last updated: 2026-07-01 by Claude (Opus 4.8). Owner: Hooman Shariati (hshariati@adobe.com).

> ⚠️ This machine can die at any time. **Persist everything to disk as you go** and update
> the four living records (below) after every working session. Minimize work lost.

---

## 1. The Goal (what Hooman actually wants)

> **⚠️ INVESTOR JURISDICTION (corrected 2026-07-03): Hooman is a CANADIAN CITIZEN.** Do NOT
> assume he is a "US person" for sanctions/OFAC purposes just because he works at Adobe (US).
> This matters: the CNOOC (0883.HK) "un-investable" call in the Stage-4/5 reports was based on
> the OFAC NS-CMIC US-person prohibition — which likely does NOT bind a Canadian citizen who is
> not a US green-card holder and does not transact from inside the US. Being re-verified; see
> `deep_dives/0883_HK/canadian_investability.md`. Open sub-questions that flip the answer: (a)
> does he hold a US green card? (b) does he transact via a US broker / while physically in the
> US? (c) does Canada's own SEMA regime restrict CNOOC? Confirm before finalizing any China-SOE call.

Find **cheap stocks worth investing in** — value investments, backed by data.

Two complementary paths (Hooman's framing):
1. **Top-down:** Find sectors of the economy that are **currently cheap** (vs their own
   history and vs the market), then find the **quality leaders** within those cheap sectors.
2. **Bottom-up:** Sometimes a sector isn't cheap but a **specific high-quality company inside
   it is cheap**. Catch those too.

Plus: **research and apply other proven methods for finding value** (quantitative screens,
quality-at-a-price, contrarian/special situations) — not just sector rotation.

**Hard requirement: minimize hallucination.** Every number and claim must trace to a real,
citable data source (see §4). Prefer reproducible data pulls (code) over recalled figures.
No made-up multiples, prices, or financials — ever. Mark confidence VERIFIED / ASSUMED /
UNVERIFIED.

**What this project is NOT:** it is research to inform Hooman's own decisions. It is **not
financial advice** and does not place trades. Output = ranked, evidence-backed candidate
lists + the reasoning, for Hooman to act on.

---

## 2. Where We Are Right Now (PROJECT STATE)

**Status: PLANNING.** Project just created (2026-07-01). No screening run yet.

- Scaffolding created (this file + the four living records + `research-plan.md`).
- `research-plan.md` holds **3 proposed methodologies** — awaiting Hooman's pick + scoping
  answers (universe/geography, market-cap range, automation level, data-source budget).

→ See `PROJECT_STATE.md` for the live action-item checklist. This CLAUDE.md holds stable
context; PROJECT_STATE.md holds moment-to-moment status.

---

## 3. The Research Methodology (how the funnel works — FINALIZED 2026-07-01)

**Chosen: Hybrid A+B, quality-first, global.** Full spec in `research-plan.md`. Scope
locked with Hooman (see `DECISIONS.md`):

- **Framing:** hunting HIGH-QUALITY companies that are cheap. **Quality is the dominant
  filter; cheapness is the second.** Tilts the hybrid toward the B-side (quality-at-a-price).
- **Universe:** global — US mid/large cap + developed markets + **emerging markets** (Hooman
  wants diversification away from the US). **Small caps only as exceptions:** an unusually
  high quality score (great financials + proven high-track-record team) overrides the
  mid/large market-cap floor.
- **Data:** free now (Damodaran + yfinance + EDGAR); add a paid global API only if EM
  coverage proves too thin.
- **Output:** one-shot ranked report + deep dives now; recurring monitor is a later phase.
  Tilt = total-return / quality-at-a-price (NOT dividend-income).

The funnel (A and B run as parallel subagents in Stage 1):
- **Stage 0 — Data setup.** Wire up Damodaran + yfinance + EDGAR; verify reproducible pulls.
- **Stage 1 — Screen (parallel).** (A) sector cheapness vs own history → cheap sectors;
  (B) universe-wide quality-first + cheap dual rank (Greenblatt-style) + trap filter.
- **Stage 2 — Merge & quality/trap filter.** Combine, tag sector clustering, gate on
  Piotroski F-score / ROIC / FCF / debt / margin trend.
- **Stage 3 — Leaders in cheap sectors** (parallel, one subagent per surviving sector).
- **Stage 4 — Deep dives on ~6–10 finalists** (parallel) → thesis, valuation, risks,
  catalysts, confidence-marked claims.
- **Stage 5 — Ranked comparison table + write-up** for Hooman.

Draft scorecard (tune after first run): Cheapness 30% / Quality 30% / Trap-risk (inverse)
20% / Moat & leadership 15% / Catalyst 5%. **Note:** given the quality-first framing,
consider bumping Quality's weight above Cheapness — confirm with Hooman after seeing round 1.

---

## 4. Data Sources (anti-hallucination backbone)

Prefer free, primary, reproducible sources. Full curated list + reliability notes in
`sources.md`.

- **NYU / Aswath Damodaran datasets** — free, updated ~yearly: sector-level multiples
  (PE, EV/EBITDA, P/B), margins, ROIC, ROE, betas, cost of capital by industry. Best single
  source for **top-down sector cheapness & quality**.
- **SEC EDGAR** — primary financial statements (10-K/10-Q), the ground truth for financials.
- **yfinance / Yahoo Finance** — prices, current multiples, market caps (free, scriptable).
- **Financial Modeling Prep (FMP), Alpha Vantage** — fundamentals APIs (free tiers).
- **Finviz** — fast screener for ratios, sector filters (web).
- **multpl.com / Yardeni** — S&P 500 aggregate & sector valuation history.
- **macrotrends** — long-horizon per-company ratio history.

Rule: when a number matters, pull it from one of these and **cite it** (source + as-of date).
Cross-check any single-source figure before it drives a ranking.

---

## 5. How To Work Here (operating rules — from Hooman)

Standing rules. Follow them.

1. **Diligent, human-readable records.** Maintain four living files:
   - **Action items** → `PROJECT_STATE.md`
   - **Learnings** → `LEARNINGS.md`
   - **Decisions** → `DECISIONS.md`
   - **Long-term plans** → `LONG_TERM_PLANS.md`
   After every session, check whether each needs updating. **If unsure whether Hooman acted
   on advice, how he did something, or whether he agreed to a plan change — ASK. Don't assume.**

2. **Organize by topic, minimize file count.** One file per topic (e.g. all sector-valuation
   work in one file, all quant-screen work in one file). Don't spawn a file per stock. Names
   must be navigable by someone with zero context. Fix legacy fragmentation when reasonable.

3. **Fan out subagents for parallel work — but keep the main session free.** Do work in the
   background so Hooman can hand the main session other tasks. Parallelize independent pieces
   (e.g. one agent per sector); **serialize** steps that depend on earlier learnings (deep
   dives depend on which names passed the screen). Don't over-parallelize. When unsure how to
   split, ASK. Background + correctness > more subagents.

4. **Cite sources, quantify, mark confidence.** Every claim links to a source. Numbers over
   adjectives. Mark claims VERIFIED / ASSUMED / UNVERIFIED. **No hallucinated numbers.**

5. **Bias toward action in the funnel** (when borderline, promote and let the next stage
   filter), but **bias toward asking** on direction/scope decisions that are Hooman's to make.

---

## 6. Hard-Won Learnings (short version — full list in LEARNINGS.md)

_(none yet — project just started)_

---

## 7. File / Folder Organization

```
fin_research/
├── CLAUDE.md              # THIS FILE — stable context + operating manual
├── PROJECT_STATE.md       # LIVE status: action items, current step, what's next
├── LEARNINGS.md           # durable learnings (consolidated)
├── DECISIONS.md           # decisions Hooman & I made + rationale
├── LONG_TERM_PLANS.md     # roadmap / where this is heading
├── research-plan.md       # methodology proposals → chosen funnel spec
├── sources.md             # curated data sources + reliability notes
├── screens/               # screen outputs (sector cheapness, quant screens) by topic
├── deep_dives/{ticker}/   # per-finalist thesis + valuation + risks
└── data/                  # raw/derived data pulls (CSVs, cached API results)
```
