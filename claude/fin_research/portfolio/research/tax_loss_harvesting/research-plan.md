# 2026 U.S./California Tax-Loss Harvesting Research Plan

**Opened:** 2026-10-23
**Status:** October 26 main harvest executed; November 16 VXUS review remains pending
**Canonical answer:** `SUMMARY.md`

## Decision question

Which current loss positions in Hooman's individual Schwab taxable account should be sold in 2026,
which should be replaced temporarily to preserve portfolio exposure, and what controls are required to
avoid wash sales?

## Known facts

- Hooman is a U.S. and California tax resident filing married filing jointly.
- The Schwab account is an individual taxable brokerage account; Hooman's wife is an authorized user.
- Hooman reports no capital-loss carryforward.
- Schwab's export through 2026-10-23 contains current tax lots, 2026 realized activity and transactions.
- Hooman reports approximately $40,000 of Adobe RSU sale proceeds, but the Adobe adjusted basis and
  actual capital gain or loss have not yet been supplied.
- Automatic dividend reinvestment is enabled where available.

## Evidence hierarchy

1. Schwab lot-level and realized-gain exports for account facts.
2. IRS Publication 550, IRS Topic 409 and Revenue Ruling 2008-5 for federal tax mechanics.
3. California FTB guidance for state capital-gain treatment.
4. Fund-sponsor pages for proposed replacement funds and benchmark differences.
5. Existing accepted portfolio decisions for whether to exit, hold or preserve an exposure.

## Work products

- `SUMMARY.md`: conclusions, exact schedule, wash-sale controls, arithmetic and limitations.
- `recommended_orders_2026.csv`: proposed sells and approximate same-day replacement buys.
- `current_positions_2026-10-23.csv`: normalized position-level reconciliation without account identifiers.
- `executed_orders_2026-10-26.csv`: user-confirmed sale and replacement fills, gross notionals and
  provisional realized results calculated from the October 23 Schwab basis export.

## Completion gate

Hooman accepted the plan on 2026-10-23 and executed its October 26 batch. AA, RBLX, CAG and BAC are
permanent exits; CCJ may be reconsidered after its wash-sale window. The next scheduled decision is
whether VXUS still has a meaningful loss on November 16; if so, swap it to IXUS as recorded in the
canonical answer.
The household-wide tax estimate remains provisional until the Adobe stock-plan gain/loss report and any
other household capital transactions are added.
