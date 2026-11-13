# DECISIONS — What Hooman & I Decided + Rationale

Last updated: 2026-07-01 by Claude (Opus 4.8).

Format: date — decision — rationale — who decided.

## 2026-07-01

- **Project created: value-investing research to find cheap stocks.** Two paths (top-down
  cheap-sector → leaders; bottom-up cheap-quality company) plus researching other value
  methods. Backed by citable data, minimize hallucination. — Hooman.
- **Not financial advice / no trading.** Output is ranked, evidence-backed candidate lists
  for Hooman to act on himself. — Claude (stated assumption; Hooman to correct if wrong).
- **Methodology: Hybrid A+B.** Run top-down cheap-sector→leaders AND bottom-up
  cheap-quality screen in parallel, cross-validate, deep-dive the overlap. — Hooman.
- **Quality-first framing.** Hooman is primarily hunting HIGH-QUALITY companies that are
  cheap — quality is the dominant filter, cheapness the second. Tilts the hybrid toward the
  B-side (quality-at-a-price). — Hooman.
- **Universe: global, quality-gated.** US mid/large cap + developed markets + emerging
  markets. Hooman explicitly WANTS diversification away from the US. Small caps are IN only
  as exceptions — when quality is exceptional (great financials + proven high-track-record
  team); an unusually high quality score overrides the mid/large market-cap floor. — Hooman.

- **Data: free now, decide later.** Start with NYU Damodaran + yfinance + EDGAR (strong US,
  decent large developed-market names, thin emerging-market fundamentals). Add a paid global
  fundamentals API (FMP/EODHD) ONLY if emerging-market coverage proves too thin. — Hooman.
- **Output: one-shot now, monitor later.** Deliver a one-shot ranked report + deep dives
  first; stand up a recurring monitor in a later phase once Hooman likes the picks. Tilt:
  total-return / quality-at-a-price (not dividend-income). — Hooman.

- **Scorecard weights LOCKED as-is:** Cheapness 30% / Quality 30% / Trap-risk (inverse) 20%
  / Moat & leadership 15% / Catalyst 5%. Hooman declined bumping Quality above Cheapness. — Hooman.
- **Execute now.** Cleared to run the funnel starting Stage 0. — Hooman.

## 2026-07-02

- **Fix EM/ex-US coverage BEFORE deep dives.** Stage 2's high-conviction BOTH bucket came out
  100% developed-market (universe was US-heavy + bottom-up screen can't score insurers), which
  conflicts with Hooman's ex-US diversification goal. So: add a **Stage 2.5** — broaden the
  ex-US/EM equity universe AND build a **bank/insurer-specific screen** (P/B, ROE, NIM, CET1)
  so cheap EM sectors (esp. EM Life Insurance) can compete fairly. — Hooman.
- **Deep-dive ~15 finalists (broad).** Widen from the proposed 11 to ~15 to include more B-only
  and EM/ex-US names. More thorough, more tokens — Hooman accepted the cost. — Hooman.

- **Deep-dive all 16 finalists as-is** (no China trim), region mix US 5 / dev-exUS 5 / EM 6.
  Hooman accepted the China concentration (4/6 EM = CNOOC, NetEase, China Taiping, CPIC). — Hooman.

## 2026-07-03

- **CORRECTION: Hooman is a Canadian citizen, not a US person.** The whole project had assumed
  US-person status (Adobe/US-based) — an assumption Claude introduced, not Hooman. This drove the
  CNOOC "un-investable" (OFAC NS-CMIC) call. Re-verifying whether a Canadian can hold CNOOC
  (0883.HK); if yes, CNOOC (best business in the run, 7.75) is BACK IN CONTENTION and displaces the
  "redirect to EOG" advice. Verification agent running → `deep_dives/0883_HK/canadian_investability.md`. — Hooman.

## Pending (awaiting Hooman)

- Whether Hooman holds a US green card / transacts via a US broker (flips the CNOOC answer).
