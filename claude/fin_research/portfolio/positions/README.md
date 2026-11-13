# Positions Ledger — Your Live Operating Dashboard

This folder is the **living record of what you own, why, and your buy/sell triggers** — the thing you
asked for. It's how we track the portfolio going forward and how a future session (or you) resumes with
full context.

## Files
- **`ledger.csv`** — one row per position (current + to-acquire). Columns:
  - `ticker, name, theme, mkt_val_usd, gl_pct` — what & how much (live-priced 2026-07-07)
  - `ACTION` — KEEP / TRIM / SELL / SWAP / BUY(new) / REVIEW
  - `grade` — Phase-1 quality-at-price score (0-10) where we scored it
  - `THESIS` — one sentence: WHY we own it
  - `ADD_when` — the pre-committed buy-more trigger
  - `SELL_when` — the pre-committed exit trigger
  - `status` — OPEN / TO-ACQUIRE / CLOSED (update as you trade)
  - `last_review` — date of last thesis check

## How to use it (the discipline loop)
1. **Before any trade:** find the row. Is this action already the plan? Is a SELL trigger actually firing,
   or is it emotion? If buying something new, ADD A ROW FIRST with its thesis + triggers.
2. **After a trade:** update `status`, `mkt_val_usd`, and note the date. Move closed positions' status to
   CLOSED (keep the row for history).
3. **Quarterly:** re-price (run `../data/holdings.py`), read every `SELL_when` column, act on what fired,
   update `last_review`.
4. **When a thesis changes:** edit the `THESIS` / triggers and date it. A thesis you can't state in one
   sentence = you don't understand the holding well enough to own it.

## Refresh the live prices
```bash
cd /home/colligo/hs_scripts/claude/fin_research
/opt/venv/bin/python3 portfolio/data/holdings.py        # re-prices all holdings
/opt/venv/bin/python3 portfolio/data/analyze_structure.py   # factor weights + vol + stress test
```

## Current state (2026-07-07)
- 53 held positions priced; ~21 flagged SELL/cleanup, ~18 KEEP, ~6 TRIM, 7 new to acquire.
- Full plan: `../execution_plan.md`. Rules: `../sell_rules.md`. Targets: `../ideal_allocation.md`.
- As you execute the Month-0→6 tickets, update this ledger so it always reflects reality.

**NOT financial advice.**
