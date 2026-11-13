# Dashboard Spec — what Claude builds in the Google Sheet

**Design locked 2026-07-08.** Google Sheet = single source of truth. All logic lives as **sheet formulas**
so it keeps working without Claude. Claude writes to NEW tabs (prefixed `FR_`) so your existing tabs are
untouched until you're happy and choose to switch over.

> Review this BEFORE Claude writes to your Sheet. Adjust anything here first.

## Tabs Claude will create (all prefixed `FR_` = fin-research, non-destructive)

### `FR_Dashboard` (the one you look at daily)
Top summary + the action table. Columns per sleeve:
| Sleeve | Target % | Target $ | Current $ | Current % | Drift (pp) | **Action $** | Status |
|---|--|--|--|--|--|--|--|
- **Target %/$** ← pulled from `FR_Targets`.
- **Current $** ← SUMIF from `FR_Holdings` by sleeve.
- **Drift** = Current% − Target%; conditional-formatted (green |drift|<2pp, yellow 2-5, red >5).
- **Action $** = Target$ − Current$ (positive = BUY that much, negative = TRIM). This is your "what to buy."
- **Status** = formula: "BUY", "TRIM", "OK", or "WAIT (crash tranche)".
- Header block: total portfolio $, cash %, total vol (from our script), # positions, last-updated date.

### `FR_Holdings` (every position)
| Ticker | Name | Sleeve | Shares | Live Price | Ccy | FX | Mkt Val USD | Weight % | Thesis | ADD when | SELL when | Account | Status |
- **Live Price** = `=GOOGLEFINANCE(ticker)` (auto-updates, no Claude needed). CAD names use `TSE:` prefix.
- **Mkt Val USD** = Shares × Price × FX (FX cell = GOOGLEFINANCE("CURRENCY:CADUSD") for CAD rows).
- **Weight %** = Mkt Val / total.
- **Thesis / ADD / SELL** ← from our `positions/ledger.csv` (the buy/sell triggers).
- Seeded from the current live holdings; you update Shares/Account as you trade.

### `FR_Targets` (the ideal-allocation model — editable knobs)
The 16-sleeve model from `ideal_allocation.md`. You can change a target % here and the whole
`FR_Dashboard` recomputes. One row per sleeve, target % (sums to 100%, with a checksum cell).

### `FR_TradeLog` (record what you actually did)
| Date | Ticker | Buy/Sell | Shares | Price | $ Amount | Account | Note |
- You (or Claude) append a row per executed trade. Optionally a formula rolls these into `FR_Holdings`.

### `FR_Rebalance` (the disciplined action list)
Filtered view: only sleeves with |drift| > 5pp OR a fired SELL trigger → "do these trades this quarter."
Implements the band-rebalance rule from `sell_rules.md` so you don't over-trade.

## What stays formula-driven (works without Claude)
- All prices (GOOGLEFINANCE), market values, weights, drift, action-$, status flags, rebalance filter.
- You can add a holding by inserting a row in `FR_Holdings` and typing ticker+shares+sleeve — everything
  else auto-computes.

## What Claude does (when you have access)
- Refresh `FR_Holdings` from a live pull, re-seed theses when they change, adjust `FR_Targets` after a
  review, generate an optional static HTML snapshot from the Sheet.

## Migration
Claude builds the `FR_` tabs alongside your existing ones. You compare, and when happy, either delete your
old tabs or keep both. Nothing you built is overwritten.

## Optional later: HTML view
Once the Sheet works, Claude can generate a static `dashboard.html` (charts of allocation vs target, drift
bars) FROM the Sheet data, hostable on your free server. It's read-only eye-candy; the Sheet stays the
editable source of truth.
