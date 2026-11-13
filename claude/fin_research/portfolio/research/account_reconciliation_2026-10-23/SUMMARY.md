# Portfolio Account Reconciliation

**Original comparison:** 2026-10-23

**Live reconciliation updated:** 2026-11-11

**Status:** Holdings reconciled; account cash awaits the user's manual update

## Current verdict

All 29 security discrepancies identified in the October 23 broker comparison are resolved in the live
`FR_Portfolio` Sheet. Hooman confirmed that AEVA was sold in full and that the existing physical-gold
and three Bitcoin entries are correct. Separate November 10 Questrade Cash and RRSP exports reconcile
every Questrade quantity and account assignment.

After that reconciliation, Hooman sold the complete **101-share Questrade Cash `CNQ.TO` lot** on
November 11. The current live Canadian-listed CNQ record is therefore **122 shares at C$45.0404** in
Questrade RRSP. The November 10 evidence file remains an immutable pre-sale broker snapshot.

The holdings reconciliation is complete. Cash remains provisional until Hooman manually replaces the
account balances. AEVA's sale date, execution price, fees, and account were not supplied, so its
realized result and proceeds are not recorded.

## Post-reconciliation execution on November 11

- Sold 101 `CNQ.TO` from Questrade Cash at C$69.61 for **C$7,030.61 gross proceeds**.
- Provisional gain versus the exported C$46.6706 average is **C$2,316.8794** before fees or broker
  basis adjustment.
- Removed `QT Cash` from the live holding's account field and retained the Questrade RRSP lot of 122
  shares at C$45.0404.
- Did not change account cash; Hooman will enter current balances manually.
- Ameritrade subsequently bought 48 `GLDM`, 57 `PDBA`, 87 `VGIT`, and 6 `VHT`. The resulting live
  quantities/bases are GLDM 48 / $3,783.36; PDBA 267 / $9,505.7669; VGIT 263 / $15,007.8962; and
  VHT 24 / $7,862.3818.
- Hooman clarified that Ameritrade's cash cell always represents the current market value of its SGOV
  reserve; Ameritrade holds no separate idle cash. The separate SGOV holding row was deleted, and an
  explicit instruction was added to `FR_Portfolio!E11` so the reserve is counted exactly once.

## Corrections completed on November 10

- Set AEVA from 70 shares to zero and marked the position closed. No cash adjustment or realized
  gain/loss was inferred.
- Reconciled 48 Questrade position lines: 14 in Questrade Cash and 34 in Questrade RRSP. All aggregate
  share quantities match the live Sheet, including 36 NVDA, 1,314 UNG, 55 CCO.TO, 95 NLR, 223 CNQ.TO,
  and the mixed Questrade/Ameritrade/Dads positions.
- Refined broker bases from the current account averages: UNG $13,957.0048; CCO.TO C$7,281.70 before
  USD translation; NLR $9,064.924; CRCL $3,075.552; and SLB $5,427.389. The exact fill-derived NVDA
  basis of $6,168.858 was retained because it is more precise than the rounded account averages.
- Preserved the confirmed physical-gold and Bitcoin entries without modification.

Normalized Questrade evidence:

`/home/colligo/hs_scripts/claude/fin_research/portfolio/research/account_reconciliation_2026-10-23/questrade_account_positions_2026-11-10.csv`

## Corrections completed on November 9

| Holding | Prior live record | Corrected live record | Evidence |
|---|---:|---:|---|
| GEV | 8 shares; $4,913.52 basis | 8.013 shares; $4,951.04 basis | October 23 Ameritrade export |
| XOM | 58 shares; $6,913.02 basis; two accounts | 59.1665 shares; $7,072.53 basis; Ameritrade | October 23 Ameritrade export |
| VXUS | 138 shares; $11,734.8172 basis | 138.0697 shares; $11,740.92 basis | October 23 Ameritrade export |
| WPM | $148.11 average | $149.4437 average; $23,014.3298 basis | October 23 Questrade Dads record |
| TRMLF | $43.926 average | $44.241818 average; $973.32 basis | October 23 Ameritrade export |

The Bitcoin CAD-cost lot's book-value formula was also repaired. Its market price is a USD BTC quote,
while the recorded C$112,000 average cost must be translated to USD. At the live CAD/USD rate, the
Sheet now reports the USD book cost instead of treating C$7,000 as US$7,000. The BTC quantity and
source basis were subsequently confirmed by Hooman. The dashboard formula generator was corrected as
well so a future rebuild does not recreate this error.

## Earlier discrepancies now resolved

- AEM.TO, NCX.V, and UROY use the correct listings and currencies.
- AMZN, CEG, CHPT, IHI, LCID, SBSW, and the other broker-confirmed quantities and bases were corrected
  on November 5.
- CNQ is split into 314 U.S.-listed Ameritrade shares and, after the November 11 Questrade Cash sale,
  122 Canadian-listed Questrade RRSP shares.
- SGOV is explicit at 2,266.1215 shares and Ameritrade cash is zero, so it is no longer hidden in or
  double-counted with synthetic cash.
- BAC, BWXT, CAG, CCJ, and VWO were resolved by the October 26 tax-loss-harvest executions.
- KWEB reflects the 197-share October 26 sale and the retained 413-share Questrade position.
- MNT.TO, PDBA, and VGIT incorporate both the corrected broker starting balances and their subsequent
  user-confirmed purchases.

The row-by-row resolution ledger is:

`/home/colligo/hs_scripts/claude/fin_research/portfolio/research/account_reconciliation_2026-10-23/resolution_status_2026-11-10.csv`

The immutable October 23 comparison remains:

`/home/colligo/hs_scripts/claude/fin_research/portfolio/research/account_reconciliation_2026-10-23/reconciled_positions.csv`

## Confirmed external assets

- **AEVA:** no position remains. The zero-share row is retained as a closed-position record.
- **Physical gold:** Hooman confirms the existing **5 + 10.86 = 15.86 ounces** and recorded basis are
  correct.
- **Bitcoin:** Hooman confirms the existing 0.07730247 BTC, 0.0625 BTC CAD-cost lot, and 0.0374162 BTC
  records are correct.

### Cash

Questrade Cash and RRSP cash cells remain stale. Hooman will replace all current account cash balances
manually. Until then, cash totals and portfolio percentages remain provisional. No cash was inferred
from the AEVA sale or from transaction arithmetic.

### Questrade account splits

The November 10 separate exports confirm every current Questrade Cash and RRSP position, quantity,
average price, and account assignment. The dashboard continues to show combined rows for securities
held in more than one account; the normalized evidence file preserves the exact split.

## Assumptions used

- Every execution reported by the user through November 11 has been recorded.
- No unreported sale, transfer, split, or journal affected the reconciled holdings other than AEVA's
  confirmed full sale.
- `Cash - 40053747` means Questrade Cash and `RSP - 52345815` means Questrade RRSP.
- The October 23 broker export remains authoritative for holdings untouched by later trades.
- Hooman's November 10 confirmation is authoritative for physical gold and Bitcoin.

## Controls

- The target grid was not changed.
- Post-write `fin_check.py --json` loaded 70 positive holdings, read $35,947.02 of provisional account cash,
  and confirmed that targets sum to 100.00000000000004% within floating-point precision. Its
  price-dependent portfolio total was approximately $676,113.47.
- The protected `FR_Portfolio!E1:K23` block was not edited. Its verified formula/value hash is
  `7b7380985eac02c3bc7bea1fb430b9bc1c892387c6fbbbc82bba008d36a8b471`.
- The legacy dashboard builder now refuses by default to overwrite the live tab from its stale
  October 13 holdings snapshot.
- No unconfirmed cash balance was deleted or invented.
- Reconciliation is based on broker quantities and bases; market quotes are irrelevant to the tie-out.
