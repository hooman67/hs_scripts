# Account Reconciliation Plan — 2026-10-23

**Status:** Holdings reconciliation complete through 2026-11-10; manual cash update pending

## Question

Does the live `FR_Portfolio` Google Sheet count every position supplied from Schwab, combined
Questrade Cash/RRSP, and Questrade Dads, with the correct quantity, listing, currency and basis?

## Method

1. Read the live `FR_Portfolio` tab using unformatted values.
2. Normalize the 79 supplied account-position lines into 72 distinct securities.
3. Aggregate only identical tickers across accounts; preserve cross-listed securities separately.
4. Compare quantity first, then listing/currency, then average cost.
5. Treat broker records as authoritative for account quantities and tax basis.
6. Apply broker-supported corrections without deleting sheet-only external assets or inventing cash.

## Outputs

- `SUMMARY.md`: current reconciliation status and remaining cash step.
- `reconciled_positions.csv`: all 72 supplied securities and comparison status.
- `resolution_status_2026-11-10.csv`: disposition of every original discrepancy and open item.
- `questrade_account_positions_2026-11-10.csv`: normalized separate Cash and RRSP positions.

## Remaining step

- Hooman will manually replace the account cash balances. Revalidate the live Sheet afterward.
- AEVA sale details are optional if a realized gain/loss record is desired; the position itself is
  reconciled at zero.
