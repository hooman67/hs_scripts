# DECISIONS — What We Decided & Why

Last updated: 2026-11-12

Format: **Date — Decision — Rationale — Who decided**

## 2026-11-12 — CLX profitable-exit rule executed

- **[EXECUTED BY USER]** Ameritrade sold all **23 `CLX` shares at $108.785** on November 12 at
  1:31 p.m. ET. Gross proceeds were **$2,502.055** before any unreported fee.
- Against the recorded **$87.985 average / $2,023.655 basis**, the provisional realized gain is
  **$478.40** before fees and tax-lot adjustments. The position is closed and removed from the
  sell-when-profitable queue.
- Ameritrade's manually maintained SGOV/cash proxy was not changed. The live holding row is zero and
  retains the execution price as its fallback close mark. Protected `FR_Portfolio!E1:K23` remained
  unchanged with before/after hash
  `6b3002a8a76be0b44d4a443c37c382ed218365f8a96a0c90e6fe624873b50588`. — Hooman + Codex.

## 2026-11-12 — NVDA new-lot exit rule and event-risk blockers confirmed

- **[CONFIRMED BY USER]** If a new `NVDA` lot is purchased, treat that lot as a one-month
  turnaround position and take profits around **$190–$200** within that month.
- Do not add if the investigation establishes **compromised secrets, export-control evasion, or a
  leadership vacuum**. These are hard no-add conditions, not temporary price concerns.
- This decision records a conditional rule only. No additional purchase is recorded, and the
  existing 36-share position remains in the Quality sleeve under the 2% company cap. The one-month
  clock begins only if a new lot is filled. — Hooman.

## 2026-11-11 — GLDM, PDBA, VGIT and VHT purchases recorded; SGOV sales omitted by instruction

- **[EXECUTED BY USER]** Ameritrade bought **48 `GLDM` at $78.82** for **$3,783.36**. This is a
  new Gold-core position.
- **[EXECUTED BY USER]** Ameritrade bought **57 `PDBA` at $35.1897** for **$2,005.8129**. The live
  aggregate is now **267 shares**, **$9,505.7669 basis**, and **$35.602123221 average cost**.
- **[EXECUTED BY USER]** Ameritrade bought **87 `VGIT` at $57.255** for **$4,981.185**. The live
  aggregate is now **263 shares**, **$15,007.8962 basis**, and **$57.064244106 average cost**.
- **[EXECUTED BY USER]** Ameritrade bought **6 `VHT` at $348.4003** for **$2,090.4018**. The live
  aggregate is now **24 shares**, **$7,862.3818 basis**, and **$327.599241667 average cost**.
- The four purchases total **$12,860.7597** before any unreported fees. They fill the existing Gold,
  Agriculture, Treasury, and Healthcare sleeves without changing any target.
- **[USER ACCOUNTING CONVENTION]** Ameritrade never holds idle cash: the Ameritrade cash cell reports
  the current market value of the SGOV reserve. The same-day 20-share and 100-share SGOV sales are
  therefore reflected only through Hooman's manually maintained cash value, not as security trades.
- The separate SGOV holding row was deleted to prevent double counting. An explicit note was added to
  `FR_Portfolio!E11`: “Ameritrade cash is held in SGOV. C11 records its current market value; do not
  add a separate SGOV holding row.” This is the standing representation for future updates.
- Post-write validation found all four quantities and weighted bases exactly, targets still totaling
  100% and holding formulas through row 146. The user-authorized E11 accounting note changed the
  protected-block hash from `c4514ad98f6ff0f216398544a807888b9d650e223f0f02d3e82eb9f72a85aecb`
  to `b08843b0e9927f7378569761622b0950aab05f0218185f176c79a340dfbb121c`; no other protected cell
  changed. — Hooman + Codex.

## 2026-11-11 — Questrade Cash CNQ.TO lot sold

- **[EXECUTED BY USER]** Questrade Cash sold all **101 `CNQ.TO` shares** at **C$69.61** on
  November 11 at 10:10 a.m. ET. Gross proceeds were **C$7,030.61** before any unreported commission.
- Against the broker-reported Questrade Cash average of **C$46.6706**, the provisional realized gain
  is **C$2,316.8794** before fees and any broker basis adjustment.
- The independently reconciled Questrade RRSP lot remains open at **122 shares**, **C$45.0404
  average cost**, and **C$5,494.9288 basis**. The live Sheet now assigns `CNQ.TO` only to `QT RRSP`;
  the separate 314-share U.S.-listed Ameritrade `CNQ` position is unchanged.
- Questrade Cash was not arithmetically changed because Hooman is maintaining account cash manually.
  The execution establishes **C$7,030.61 gross CAD proceeds** as available before any unreported
  fee. The oil-company target remains 6%.
- Post-write validation loaded the remaining 122-share lot exactly, preserved its formulas, and left
  `FR_Portfolio!E1:K23` unchanged with before/after hash
  `c4514ad98f6ff0f216398544a807888b9d650e223f0f02d3e82eb9f72a85aecb`. — Hooman + Codex.

## 2026-11-10 — Holdings reconciliation confirmations recorded

- **[CONFIRMED BY USER]** AEVA was sold in full and no position remains. Record zero shares without
  inventing proceeds or a realized result; execution details were not supplied.
- **[CONFIRMED BY USER]** The existing physical-gold line and all three Bitcoin entries are correct.
  Preserve their quantities and bases.
- **[BROKER DATA SUPPLIED BY USER]** Separate Questrade Cash and RRSP exports reconcile all 48
  position lines. Preserve the exact fill-derived NVDA basis and use the current account averages to
  refine UNG, CCO.TO, NLR, CRCL and SLB bases.
- Hooman will update account cash manually. Do not infer cash from the AEVA sale or transaction
  arithmetic. Protected `FR_Portfolio!E1:K23` remained unchanged with hash
  `7b7380985eac02c3bc7bea1fb430b9bc1c892387c6fbbbc82bba008d36a8b471`. — Hooman + Codex.

## 2026-11-10 — NVDA purchase and TTD exit recorded

- **[EXECUTED BY USER]** Questrade RRSP bought 20 `NVDA` at **$167.74** for **$3,354.80**. The
  combined Questrade position is now **36 shares**, **$6,168.858 basis** and a
  **$171.357166667 weighted average** across `QT Cash, QT RRSP`.
- The replaced 20-share `NVDA` order at $167.49 had no fill and does not affect the records.
- **[EXECUTED BY USER]** Questrade RRSP sold all 220 `TTD` at **$15.401**, for **$3,388.22** gross
  proceeds. Against the broker-reported $14.0599 average, the provisional realized gain is
  **$295.042** before any unreported commission or broker basis adjustment. The position is closed.
- `NVDA` remains inside the existing 5.5% Quality sleeve, counts dollar-for-dollar against `JQUA`,
  and remains subject to the 2% hard company cap. No target changed.
- The fills imply a net **+$33.42** Questrade RRSP USD cash movement before fees. The live cash cell
  remains unchanged because its starting balance is unreconciled. Protected `FR_Portfolio!E1:K23`
  was unchanged with before/after hash
  `5d3473fdd0a3689148c7dd80a04d785443902f95462965da6a57bc104ed8ad1b`. — Hooman + Codex.

## 2026-11-09 — Complete broker-backed reconciliation before deleting external assets

- **[BROKER RECONCILIATION]** Apply the October 23 export's exact fractional quantities and bases to
  `GEV`, `XOM`, and `VXUS`; apply the broker bases to `WPM` and `TRMLF`; and identify `XOM` only with
  Ameritrade. These five rows were missed in the November 5 reconciliation.
- Correct the CAD-cost Bitcoin lot's USD book-value formula, while leaving its quantity and source
  basis unconfirmed. Do not delete AEVA, physical gold, or Bitcoin without current ownership evidence.
- Treat Questrade Cash and RRSP cash as unreconciled until fresh broker balances are supplied. Exact
  account-level position splits also require separate current exports from those accounts.
- The protected `FR_Portfolio!E1:K23` block remained unchanged with hash
  `7b7380985eac02c3bc7bea1fb430b9bc1c892387c6fbbbc82bba008d36a8b471`. — Hooman + Codex.

## 2026-11-09 — NVDA purchases and SBUX/BOIL exits recorded

- **[EXECUTED BY USER]** Questrade RRSP bought 6 `NVDA` at **$177.168** and Questrade Cash bought
  10 `NVDA` at **$175.105**. The new aggregate is **16 shares**, **$2,814.058 basis** and a
  **$175.878625 weighted average**, across `QT Cash, QT RRSP`.
- **[EXECUTED BY USER]** Questrade Cash bought 5 `UNG` at **$9.9681**. The aggregate position is
  now **1,314 shares**, **$13,956.9183 basis** and a **$10.621703425 weighted average** across
  `QT Cash, QT RRSP`.
- **[EXECUTED BY USER]** Questrade RRSP sold all 10 `SBUX` at **$109.9572**, for **$1,099.572**
  gross proceeds. Against the broker-reported $99.459 average, the provisional realized gain is
  **$104.982** before any unreported commission or broker basis adjustment. The position is closed.
- **[EXECUTED BY USER]** Questrade Cash sold all 100 `BOIL` at **$17.91**, for **$1,791.00** gross
  proceeds. Against the recorded $2,860 basis, the provisional realized loss is **$1,069.00** before
  any unreported commission or broker basis adjustment. The leveraged natural-gas position is closed.
- `NVDA` is recorded inside the existing 5.5% Quality sleeve and counts dollar-for-dollar against
  `JQUA`, subject to the existing 2% hard company cap. No sleeve target changed.
- The fills imply a net **+$36.564** RRSP USD cash movement and **-$9.8905** Questrade Cash USD
  movement before fees. The live cash cells were left unchanged because their starting balances
  remain unreconciled; a broker cash snapshot should replace them directly. The protected
  `FR_Portfolio!E1:K23` block was unchanged, with before/after hash
  `c4514ad98f6ff0f216398544a807888b9d650e223f0f02d3e82eb9f72a85aecb`. — Hooman + Codex.

## 2026-11-06 — Build Canada additions and complete Questrade reconciliation

- **[EXECUTED BY USER]** Questrade Cash bought 60 `EFX.TO` at **C$27.28**, 40 `FTG.TO` at
  **C$32.40**, 25 `CGY.TO` at **C$84.99** and 40 `BDGI.TO` at **C$74.97** on November 6.
  Combined gross notional was **C$8,056.35** before any unreported commissions.
- The user's complete post-trade Questrade Cash/RRSP snapshot establishes the combined positions as
  **EFX 120 at C$29.9599**, **FTG 100 at C$33.6419**, **CGY 36 at C$84.9647** and
  **BDGI 65 at C$78.3815**. All four now span Questrade Cash and RRSP.
- The same complete snapshot corrects `UNG` from a stale 2,234 shares to **1,309 shares at
  US$10.6242**. This is a broker-position correction, not an inferred sale. Holdings independently
  documented in Ameritrade or Questrade Dads were preserved rather than removed because those
  accounts were outside the supplied snapshot.
- **[CONFIRMED BY USER]** Keep the existing 80 `VNP.TO` shares; no November 6 add was made because
  the price had risen too far. The four purchases and the VNP no-add decision do not create a new
  standalone Build Canada target: each name remains mapped to its existing economic sleeve.
- Questrade Cash was not inferred from the prior recorded balance because the account was recently
  funded and no post-trade CAD/USD cash balances were supplied. The live write preserved every row
  formula and the protected `FR_Portfolio!E1:K23` block; its before/after hash was
  `a338c6303b8317ef955f5d3bd1b5e272ba1ceba3a87d59b0eab438040e93a7dd`. — Hooman + Codex.

## 2026-11-05 — Broker-position reconciliation applied

- **[BROKER DATA SUPPLIED BY USER]** Ameritrade now records zero cash, 2,266.1215 `SGOV` at
  $100.550376491 average cost, 138 `IHI` with $7,080.13 basis, and 314 U.S.-listed `CNQ` with
  $11,489.82 USD basis. `SGOV` is an explicit cash-equivalent holding and is no longer hidden inside
  the Ameritrade cash row.
- The Canadian CNQ position is now separate: 223 `CNQ.TO` shares across Questrade Cash and RRSP,
  with C$10,208.6594 aggregate basis and C$45.778741704 weighted average. The live Sheet no longer
  mixes USD-listed and CAD-listed CNQ shares or currencies.
- Corrected material stale records include `IHI` 138, `AMZN` 15, `SBSW` 485, `CHPT` 5, `LCID` 2
  and `CEG` 7. `CHPT` and `LCID` now use the broker's post-corporate-action quantities and bases.
  AEM, NorthIsle and Uranium Royalty now use the correct CAD/USD listings; the supplied COP.UN,
  SQQQ, MARA, CSGP and other broker bases were also recorded.
- The corrected `JQUA` aggregate remains 211 shares but is now **$15,750.988 basis** and
  **$74.649232227 weighted average**, using the newly supplied 90-share Questrade Cash basis plus
  the two exact Ameritrade fills.
- Existing aggregate lots supported by prior broker records were preserved where the new account
  excerpt did not report a sale. In particular, the live Sheet retains 2,234 `UNG`, 55 `CCO.TO`,
  95 `NLR` and 70 `VPU`, while adding the account split established by the new snapshots. — Hooman
  + Codex.

## 2026-11-05 — ANET, LRCX, JQUA and SHLD purchases recorded

- **[EXECUTED BY USER]** Ameritrade bought 17 `ANET` at **$159.4435** on November 5 at
  5:11 p.m. ET, for **$2,710.5395** before any unreported fee. This is a new position.
- **[EXECUTED BY USER]** Ameritrade bought 20 `LRCX` at **$190.5181** at 4:55 p.m. ET, for
  **$3,810.362**. This is a new position and activates part of the previously reviewed direct
  AI-equipment variant.
- **[EXECUTED BY USER]** Ameritrade bought 50 `JQUA` at **$73.50** at 5:00 p.m. ET, for
  **$3,675.00**. The subsequent broker reconciliation above establishes **211 shares**,
  **$15,750.988 basis** and **$74.649232227 weighted average** across Questrade Cash and Ameritrade.
- **[EXECUTED BY USER]** Ameritrade bought 60 `SHLD` at **$58.86** at 5:08 p.m. ET, for
  **$3,531.60**. The aggregate is now **110 shares**, **$6,672.10 basis** and
  **$60.655454545 weighted average** across Questrade RRSP and Ameritrade.
- Gross purchase notional was **$13,727.5015**. Per Hooman's instruction, the 99-share `SGOV` sale
  was not recorded and Ameritrade cash was not changed; Hooman will enter the resulting broker cash
  balance manually. No `EFX.TO` or `BDGI.TO` trade is recorded because their TSX orders were not
  executed.
- The Quality sleeve target remains 5.5%. ANET, LRCX, AMZN and JQUA all count inside it, so there is
  no automatic additional Quality purchase until the post-trade composition is reviewed using the
  manually corrected cash balance. LRCX retains its accepted 1% cap. ANET has no adopted target and
  is a no-add holding pending review. The protected `FR_Portfolio!E1:K23` values and formulas were
  exactly unchanged. — Hooman + Codex.

## 2026-11-04 — October 29 FIS sale recovered and recorded

- **[EXECUTED BY USER]** Ameritrade sold all 138 `FIS` shares on October 29 at **$37.493**. Gross
  proceeds were **$5,174.034**; after the reported **$0.11** charge, the broker-reported net proceeds
  were **$5,173.92** after rounding.
- Against the recorded **$4,476.03** basis (138 shares at $32.435), the provisional realized gain is
  **$697.89** before tax and any broker basis adjustment. `FIS` is closed and removed from the live
  sell-on-profit queue.
- This execution had previously been omitted from the live Sheet. The correction sets the FIS holding
  to zero and increases Ameritrade synthetic cash from $226,686.55807544 to
  **$231,860.47807544**. It does not change any allocation target. The protected
  `FR_Portfolio!E1:K23` block remained exactly unchanged. — Hooman + Codex.

## 2026-11-03 — MNT.TO purchase in Questrade Dads recorded

- **[EXECUTED BY USER]** Questrade Dads bought 74 `MNT.TO` at **C$59.20** on November 3 at
  3:59:34 p.m. ET, for **C$4,380.80** before any unreported commission.
- The October 23 broker export is the authoritative pre-trade position: 373 shares at a reported
  C$51.6788 average, rather than the stale live-Sheet row of 588 shares at C$57.88. The corrected
  post-trade aggregate is therefore **447 shares**, with an approximate **C$23,656.9924 basis** and
  **C$52.923920358 weighted average**. The historical basis uses the broker export's rounded average;
  a later exact broker book value supersedes it if materially different.
- The purchase was funded from the exact Questrade Dads CAD cash path established by the November 2
  CNQ sale: C$8,451.32 less C$4,380.80 leaves **C$4,070.52**. The existing US$108.95 balance was
  preserved. The MNT account list is now `QT RRSP, QT Dads`.
- This fill adds to the existing Gold core implementation without changing its 15% sleeve target or
  MNT's 4% name target. The current live `FR_Portfolio!E1:K23` values and formulas were exactly equal
  before and after the write. — Hooman + Codex.

## 2026-11-02 — Exact quality rotation and CNQ.TO Dads sale recorded

- **[EXECUTED BY USER]** Ameritrade sold all 16 `GOOGL` at **$280.9362** on October 30 at
  4:31 p.m. ET, for **$4,494.9792** gross proceeds. Against the October 28 $4,752 basis, the
  provisional short-term result is a **$257.0208 loss** before unreported fees and broker wash-sale
  adjustments. The position is closed; the first date after the adopted 30-day no-repurchase period
  is November 30.
- **[EXECUTED BY USER]** Ameritrade bought 71 `JQUA` at **$76.46** on October 30 at 4:33 p.m. ET,
  for **$5,428.66**. Together with the existing 90 Questrade shares, the aggregate is **161 shares**,
  **$12,072.46 basis** and a **$74.984223602 weighted average**. The two October 30 fills reduced
  Ameritrade synthetic cash by **$933.6808**, from $227,620.23887544 to **$226,686.55807544**.
- **[EXECUTED BY USER]** Questrade Dads sold all 56 `CNQ.TO` at **C$74.97** on November 2 at
  2:54:44 p.m. ET, for **C$4,198.32** gross proceeds. Questrade Dads CAD cash increased from
  C$4,253 to **C$8,451.32**, and the account was removed from the CNQ holding.
- The October 23 broker export, rather than the stale 588-share Sheet row, established 593 pre-sale
  CNQ shares: 314 U.S.-listed Ameritrade shares plus 279 Canadian-listed Questrade shares, including
  the 56-share Dads lot. The correct post-sale aggregate is therefore **537 shares**. The live Sheet
  preserves the blended C$49.03 planning basis; the U.S./Canadian listing and executable tax-lot split
  remains an identified reconciliation item.
- The protected `FR_Portfolio!E1:K23` values and formulas were exactly unchanged, with before/after
  hash `5d3473fdd0a3689148c7dd80a04d785443902f95462965da6a57bc104ed8ad1b`.

## 2026-11-02 — JQUA quality default, AI-equipment watches and silver restraint accepted

- **[EXECUTED; EXACT FILLS RECORDED ABOVE]** The October 30 GOOGL sale and JQUA purchase supersede
  the October 29 direct-GOOGL hold rule. The live Sheet now reflects both fills and their cash effect.
- **[CONFIRMED BY USER]** Keep the full 5.5% Quality sleeve in JQUA for now.
  Do not buy LITE, MRVL, LRCX, ANET, ARM, COHR, KLAC or additional MSFT merely because of the latest
  decline. LRCX and KLAC are valuation-watch candidates; any future direct position must replace
  JQUA dollar-for-dollar and remain within the user's 2% single-company cap.
- **[CONFIRMED BY USER]** The default remains 5.5% JQUA. The only accepted active variant for future
  review is 4.5% JQUA plus up to 1.0% LRCX. Re-underwrite LRCX near $205 or about 22x forward GAAP
  earnings; re-underwrite KLAC near $140 or about 25x comparable GAAP earnings. These are review
  gates, not limit orders. If both are ever used, keep their combined allocation at 1.5% or less.
- **[CONFIRMED BY USER]** Do not re-enter direct GOOGL merely because it rebounds. Avoid a household
  repurchase before November 30 and confirm household tax lots before any later direct purchase. The
  lesson is to use the diversified quality policy rather than trade around break-even.
- **[CONFIRMED BY USER]** Do not add a direct silver vehicle while 154 WPM
  shares remain. If clean long-term silver exposure is later needed in Ameritrade, prefer SIVR;
  reserve SLV for tactical trading and OneGold for a minority custody allocation. Full evidence:
  `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/ai_quality_silver_2026-11-01/SUMMARY.md`.

## 2026-10-29 — GOOGL purchase recorded; bounded quality-sleeve position accepted

**Superseded by the complete October 30 GOOGL sale recorded above.**

- **[EXECUTED BY USER]** Ameritrade bought 16 `GOOGL` at $297.00 with a $297.00 Day + extended-hours
  limit at 4:57 p.m. ET on October 28, for **$4,752.00** before any unreported fees.
- The live Sheet's zero-share Alphabet row was reactivated with 16 shares, $4,752 basis and a $297
  average. Ameritrade synthetic cash decreased from $232,372.238875 to **$227,620.238875**. The
  account assignment is inferred from the same broker interface and account flow as the immediately
  preceding Ameritrade fills; correct it if the order was placed in another account.
- **[ACCEPTED BY USER]** Hold the 16 shares as a bounded direct Alphabet position inside the 5.5%
  quality sleeve. Do not add. Treat approximately 1% of the portfolio as a cap rather than a buy
  target, and reduce future JQUA deployment dollar-for-dollar because JQUA already owns Alphabet.
- The $297 cost basis is not an exit rule. Review after earnings and sell if Search monetization
  structurally deteriorates, Cloud economics fail to support the investment, or capex plus continued
  dilution/debt fails to produce per-share free cash flow. Rebalance if direct GOOGL grows materially
  above approximately 1% of the portfolio.
- Alphabet's October 28 primary release reported 25% revenue growth, 12% Search growth, 103% Cloud
  growth and 30% operating-income growth. It also reported $51.355B quarterly capex versus $42.290B
  operating cash flow, common-stock issuance and additional debt. The operating thesis is intact,
  while capital intensity, dilution and valuation remain the decisive risks. The live Sheet's quality
  instructions and GOOGL thesis/add/sell fields now encode the accepted policy; the sleeve target
  remains unchanged and no GOOGL buy target was created. — Hooman + Codex.

## 2026-10-28 — VGIT purchase executed; fin-check changed to prose and underweight watch

- **[EXECUTED BY USER]** Ameritrade bought 88 `VGIT` at $57.2899 with a $57.30 Day limit at
  12:56 p.m. ET for **$5,041.5112** before unreported fees.
- The authoritative pre-trade position was the October 23 broker-export balance of 88 shares at
  $56.65, not the stale 53-share Sheet row. The corrected aggregate is 176 shares, $10,026.7112
  basis and a $56.96995 average. Ameritrade synthetic cash is $232,372.238875 after the fill.
- The VGIT sleeve target remains 5%; recording the trade does not adopt any further Treasury order.
- **[USER OUTPUT PREFERENCE]** Future `fin-check` runs inspect every holding and watchlist name but do
  not print the repeated per-stock return tables. They provide a prose decision brief and a special
  watch for every underweight sleeve, emphasizing healthcare, Build Canada, China/broad EM and
  uranium/nuclear entry opportunities and gates. — Hooman + Codex.

## 2026-10-27 — PDBA purchase executed

- **[EXECUTED BY USER]** Ameritrade bought 70 `PDBA` at $36.6422 with a $36.66 Day limit at
  12:36 p.m. ET for **$2,564.954** before unreported fees.
- The authoritative October 23 broker export showed 140 pre-trade shares at $35.25, while the live
  Sheet was stale at 155 shares and $38.77. The corrected aggregate is 210 shares, $7,499.954 basis
  and a $35.714066667 weighted average. Ameritrade synthetic cash is $237,413.750075 after the fill.
- PDBA remains the broad agriculture-commodity implementation. The Agriculture sleeve and PDBA name
  targets remain 3% and 2%; recording this fill does not change either target. The protected
  `FR_Portfolio!E1:K23` notes/formulas were unchanged. — Hooman + Codex.

## 2026-10-26 — Schwab tax-loss harvest main batch executed

- **[EXECUTED BY USER]** Sold AA 50, RBLX 50, CAG 303.5594, BAC 51, CCJ 45, KWEB 197, COPX 78,
  VWO 150, PICK 80 and BWXT 29.1288 for combined gross proceeds of **$42,159.75**.
- Bought the accepted exposure bridges: MCHI 92, ICOP 119, IEMG 112, MXI 41 and NLR 80 for
  **$30,379.04**. AA, RBLX, CAG and BAC remain permanent exits. The replacement funds are exposure
  bridges and do not by themselves change sleeve targets.
- The October 23 exported bases imply a provisional realized loss of **$10,840.54**, comprising
  $8,576.98 short term and $2,263.56 long term. Schwab's refreshed realized report and final 1099-B
  control the tax filing.
- Block purchases of every sold original through November 25, including both CCJ and CCO.TO. Review
  direct repurchases no earlier than November 27; review the replacement funds on November 30.
- The live sheet and durable tax-harvesting record were updated. The scheduled VXUS→IXUS review
  remains November 16. — Hooman + Codex.

## 2026-10-23 — Schwab tax-loss harvest accepted (executed October 26)

- **[CONFIRMED BY USER — AWAITING EXECUTION]** Harvest approximately $11,164.01 of current losses
  by exiting AA, RBLX, CAG, BAC and the Schwab CCJ lot, and by swapping retained exposures into
  different-index funds. Execute the main batch October 26; delay VXUS until November 16 because of
  its October 16 purchase.
- AA, RBLX, CAG and BAC are permanent exits with no planned repurchase. CCJ may be reconsidered after
  the wash-sale window. For an October 26 CCJ sale, block both CCJ and CCO.TO through November 25;
  November 27 is the first practical U.S. trading date outside the window.
- This set is deliberately smaller than every negative lot. It brings Schwab's estimated 2026 result
  from a $8,104.89 short-term gain to a roughly $3,059.12 net capital loss without disrupting CF,
  CLX, BKR, VTI or immaterial fractional lots.
- No holding, live Sheet value or broker order changed. Execution requires a fresh loss
  check, disabled reinvestment and a household-wide no-purchase window through November 25.
- Exact orders, replacements, arithmetic and primary tax sources:
  `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/tax_loss_harvesting/SUMMARY.md`.

## 2026-10-22 — Build Canada purchases executed; existing sleeves retained provisionally

- **[EXECUTED BY USER]** Bought `CGY.TO` 5 at C$84.88 in QT Cash and 6 at C$84.93 in QT RRSP;
  bought in QT RRSP `EFX.TO` 60 at C$32.64, `BDGI.TO` 25 at C$83.84, `VNP.TO` 80 at
  C$26.56 and `FTG.TO` 60 at C$34.47. Total gross CAD notional was C$9,181.38 before
  unreported fees.
- The live sheet aggregates Calian as 11 shares at C$84.907273 weighted average and preserves
  both accounts. QT RRSP CAD cash is C$7.02 and QT Cash CAD is −C$407.86 after the fills; no
  unstated funding or FX conversion was assumed.
- **[RESEARCHER CLASSIFICATION — PROVISIONAL]** Map `CGY` and `FTG` to `Defense`, `EFX` to
  `oil-companies`, `BDGI` to `grid/electrification`, and `VNP` to `industrial_metals`. These are
  the closest existing economic roles and contain acknowledged imperfections.
- **No new sleeve or target was adopted.** `Build Canada` spans several different risk factors and is
  better treated as a geography/policy theme unless Hooman later chooses a separate sleeve. The live
  100% target grid and user-owned `FR_Portfolio!E1:K23` notes remain unchanged. — Hooman + Codex.
- Full research and execution record:
  `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/SUMMARY.md`.

## 2026-10-21 — UNG purchase executed

- **[EXECUTED BY USER]** Bought 400 `UNG` at $9.9787 with a $9.98 GTEM limit at 5:23:01 p.m. ET,
  for $3,991.48 before unreported fees. The fill was assigned to the existing QT Cash position based
  on the live account of record and order convention.
- The aggregate position is now 2,234 shares with $23,711.937302 basis and a $10.614116966 weighted
  average. The live-sheet quote of $9.97 values it near $22,273 / 3.3% of the portfolio.
- QT Cash USD is now -$3,793.48 after deducting the fill, recording a debit/margin balance. The 1%
  natural-gas target and all allocation/thesis rules remain unchanged; this execution does not imply
  acceptance of a larger natural-gas target. Protected `FR_Portfolio!E1:K23` content was unchanged.

## 2026-10-20 — Build Canada comparison and research shortlist

- **[RESEARCHER DECISION / PROPOSAL — NOT YET CONFIRMED]** Prioritize Enerflex and Calian for possible substitution within existing energy/defence budgets; Badger next watch. FTG/5N Plus have attractive businesses at demanding valuations; Magellan has weaker cash/governance; Canaccord is a special situation; Electrovaya is speculation and the weakest current fit. No positions, weights, orders or policy changes adopted.
- Rationale: primary financials, normalized same-currency valuations, actual Canadian-demand/AI exposure and current portfolio overlap. Existing broad funds and no new position remain alternatives. Main uncertainties: contract economics, cash conversion, future earnings, user loss budget and account/tax implementation.
- Reversible research ranking. Reconsider with new primary results, material prices or user allocation decisions. Canonical evidence and exact gates: `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/SUMMARY.md`.
- Manager review found credible institutional-business evidence but no independently verified audited fund outperformance. Twelve public recommendation events were evaluated as complete three-name sets; they are not a fund track record. Requested GPT-5.6-sol/high delegation used, with centralized synthesis.

## 2026-10-20 — NKE sale executed

- **[EXECUTED BY USER]** Sold all 80 `NKE` in QT RRSP with a $37.99 Day limit; filled at $37.9926
  at 2:57:49 p.m. ET for gross proceeds of $3,039.408. Against the sheet's $38.23 average cost,
  this is a nominal $18.992 / 0.62% loss before any fees or broker-lot differences.
- The live holding is now zero and QT RRSP USD cash increased from $859 to $3,898.408. The position
  is removed from the standing Speculation exit queue. Allocation targets and the protected
  `FR_Portfolio!E1:K23` notes block were unchanged.

## 2026-10-19 — ASTS and MCD sales executed

- **[EXECUTED BY USER]** Sold all 70 `ASTS` in Ameritrade with a $43.19 Day limit; filled at $43.19
  at 12:50 p.m. ET for gross proceeds of $3,023.30. Against the sheet's $42.355 average cost, this is
  a nominal $58.45 / 1.97% gain before fees, taxes and any broker-lot differences. The sale satisfies
  the 2026-10-15 conditional sell-when-profitable instruction; the live holding is now zero.
- **[EXECUTED BY USER]** Sold 12 `MCD` with a $242.68 Day limit; filled at $242.715 at 12:50 p.m. ET
  for gross proceeds of $2,912.58. `MCD` was not in the live holdings table, and no acquisition price
  or tax lot was supplied, so the records include the proceeds but make no realized-gain or loss claim.

## 2026-10-16 — VHT and VXUS buys funded with SGOV

- **[EXECUTED BY USER]** In Ameritrade, bought 8 `VHT` with a $326.86 Day + extended-hours limit,
  filled at $326.86 at 3:32 p.m. ET ($2,614.88); bought 29 `VXUS` with an $83.39 Day + extended-hours
  limit, filled at $83.375 at 3:32 p.m. ET ($2,417.875); and sold 50 `SGOV` with a $100.58 Day +
  extended-hours limit, filled at $100.5808 at 3:31 p.m. ET ($5,029.04 gross proceeds).
- `VHT` is now 18 shares with $5,771.98 book cost and a $320.665556 weighted average. `VXUS` is now
  138 shares with $11,734.8172 book cost and an $85.034907 weighted average.
- The October 16 fills reduced broker cash by $3.715. Together with the October 19 sales, the five
  fills increased Ameritrade cash by $5,932.165 to $236,577.0136, before any unreported fees.
- `SGOV` and `MCD` had no active holding rows, so their sale details are preserved here rather than
  inventing historical cost bases. Allocation targets were not changed. The protected
  `FR_Portfolio!E1:K23` notes block remained unchanged.

## 2026-10-15 — Speculation positions added to conditional profit exits

- **[CONFIRMED BY USER]** Add all held Speculation positions to the sell queue and flag full exits
  as soon as they become profitable: LULU.TO, TTD, NKE, CLX, SHOP.TO, UBER, ASTS and FIS, verified
  against the live sheet. Include future holdings classified Speculation in the monitoring rule.
- Profit monitoring compares current quote with recorded average purchase cost in the same currency;
  taxes, unrecorded fees, dividend history and historical-FX tax gains require broker-level checks.
- Keep the sleeve classification and allocation targets while awaiting sale. Existing legacy exits
  retain their rules. This is a conditional exit instruction, not a trade or approval of the macro
  audit's proposed allocation. No live sheet edits or brokerage orders.
- Durable instructions: `sell_rules.md`; automated display and stale/missing-data checks:
  `/home/colligo/hs_scripts/claude/dotclaude/scripts/fin_check.py`.

## 2026-07-07

- **Launch independent portfolio audit.** Hooman's prior research is AI-generated; we verify everything from scratch. Parallel agents run 7 research streams (macro, AI, China, gold/uranium, holdings, portfolio structure, rebalancing). — Claude (Hooman approved).

---

- **Redone on Opus 4.8 (2026-07-07).** Chunks 0-A had been done on a weak model (Haiku). Reloaded full
  context + all prompts, verified live-data access (yfinance installed, Yahoo+Damodaran reachable), and
  re-ran with a live-data-grounded 5-chunk plan. — Claude.
- **Verified live-data backbone before any fan-out.** Installed yfinance (curl_cffi backend; bare urllib
  gets 429 from Yahoo). All numbers live-pulled or web-cited, per anti-hallucination rule. — Claude.

## 2026-07-07 (LOCKED — Hooman answered all 5 open questions)

1. **Cash tilts USD** — the $250k house reserve with his dad is already CAD, so this book leans USD.
   Keep permanent $100k + $45k crash tranche in USD (SGOV/T-bills). — Hooman.
2. **$100k permanent safety; the rest is dry powder.** → Bucket A = $100k perm + $44k TIPS + $45k crash
   = $189k (34%), declining to ~26% as the crash tranche deploys. ~$91k excess cash is deploy fuel. — Hooman.
3. **ARX: sell-and-redeploy** (accepted recommendation) — already ~56% Cdn energy; holding to close would
   hand him unwanted Shell stock. Check account type + gain before executing. — Hooman + Claude.
4. **YES to the ~22% global-index core** — "I don't care about my feelings if it's the right approach."
   The single highest-value change. — Hooman.
5. **6-month DCA + ~$45k crash tranche** held for a real −20%+ dip. — Hooman.

→ Finalized in `execution_plan.md` (supersedes buy_list.md draft). Sources ~$168k ≈ uses ~$170k.
Account placement: RRSP=US-div payers (no withholding), TFSA=growth/AMZN, taxable=loss-harvest+gold+VXUS.

## 2026-07-08 (completeness-audit follow-ups — Hooman decided)

- **Recession/deflation hedge = UTILITIES (XLU ~4%), NOT IEF.** Hooman distrusts US-govt duration; XLU
  rallies when rates fall in a recession, is NOT a govt IOU, and doubles as his AI-power/electricity
  thesis. Discussed IEF vs SGOV: SGOV principal effectively guaranteed (ultrashort T-bills, ~0% price
  move); IEF = SAME credit (US Treasury) but −13.3% in 2022 / +6% in 2020 COVID — the price MOVEMENT is
  the hedge (rises in deflationary crash) but loses in the inflation scenario he expects → chose the
  non-duration hedge (XLU) instead. — Hooman + Claude.
- **House location = genuinely 50/50 US-vs-Canada → cash reserve split ~50/50 USD/CAD.** Corrects the
  2026-07-07 "USD tilt" default. He lives in US now / green card pending / might buy Bay Area (Dublin/
  Berkeley/Pleasanton), but might buy Canada → hedge both. ($250k dad-reserve already CAD helps the CAD side.)
  — Hooman.
- **Japan (DXJ): SKIP.** Not convicted (Japan debt ~250% GDP), already owns Japan ~5-6% via VT, and it was
  only a "tilt" not a gap. Rule reinforced: don't hold low-conviction tilts he'll abandon at the worst
  moment. — Hooman + Claude.
- **Adobe: already diversifying correctly** — sells each quarter's RSU vest as it vests (textbook). OPEN:
  confirm (a) selling 100% on vest vs a portion, (b) proceeds flow into the diversified plan (VT/uncorr),
  NOT back into US tech. — Hooman.

## 2026-07-09 (Day-1 timing)

- **Global-equity core = VTI (~60%) + VXUS (~40%), NOT VT.** As a Canadian in a taxable account, holding
  VXUS separately makes the international dividends' foreign-tax-credit claimable (buried/unclaimable
  inside VT); also cheaper + independent US/intl rebalancing. — Claude (Hooman confirmed intent).
- **Timing over mechanical execution (Hooman's ask).** VERIFIED live 2026-07-09: Iran/US escalation real
  (07-08 US strikes) → oil +6-8%/5d to WTI ~$73 (NOT the hyped $120). **DO NOW: sell energy trims (OXY
  +9.2%, ARX) into the war pop; buy VTI+VXUS + XLU + COPX (copper −3.6% = buy weakness).** WAIT: don't
  trim CCJ/WPM/AEM (fell 3-8% this week — would lock in weakness); don't chase CI/GOOGL/IAK (popped 2-4%).
  Rule reinforced: trim what's UP, buy what's DOWN/flat. — Hooman + Claude.

## 2026-07-10 (Day-1 EXECUTED — sells)

- **SOLD ARX.TO: 340 @ C$30.90 + 232 @ C$30.89 = 572 sh, C$17,672 ≈ $12,463 USD.** Full exit of the
  Shell-merger position (Questrade/CAD). Redeploying.
- **SOLD OXY: 123 @ $52.46 = $6,453 USD.** Full exit of worst energy name (Ameritrade/USD).
- **Total freed ≈ $18,915 USD.** Energy sleeve drops ~15%→~11.5%. Both were gains (cap-gains if taxable).
- Reeval that morning: oil gave back part of the war pop (WTI −2.6%), so OXY not sold at the exact top,
  but sold anyway (thesis = overweight + worst name, not war-dependent). ARX oil-insensitive → clean.

## 2026-07-10 (Day-1 EXECUTED — buys + WPM trim)

- **SOLD WPM.TO: 35 @ C$156.70 = C$5,484 ≈ $3,868 USD.** Trim into strength (WPM +3% that day); 227→192
  sh. Silver/Plat sleeve 4.9%→3.9% (target 1%; more trimming to come). Was −25% P/L (loss if taxable).
- **BOUGHT (~$6,321 USD):** VTI 7@$371.49 ($2,600) + VXUS 19@$84.97 ($1,614) + XLU 23@$45.11 ($1,038)
  + GOOGL 3@$356.32 ($1,069). Started global-equity core ($0→$4.2k), utilities sleeve, GOOGL in quality.
- **Net cash freed to date ≈ $22,783** (ARX $12,463 + OXY $6,453 + WPM $3,868); spent $6,321 → ~$16.5k
  dry powder for next DCA tranches. Disciplined pace (didn't slam it all in).
- Timing: bought on GOOGL's −1.4% dip, XLU soft (−0.5%); skipped COPX (bounced +3.5% two days). Verified.
- Dashboard + positions/ledger updated. **All buys from Questrade CASH (CAD, taxable)** — had no USD in
  RRSP. Cash table set: QT Cash C$40,025 (was 25,833 +ARX+WPM −buys), Ameritrade $267,791 (+OXY).
- ⚠️ **TAX NOTE for future core buys:** buying US-listed ETFs in a Cdn TAXABLE account loses the RRSP
  dividend-withholding shelter — VTI/XLU/GOOGL US dividends now face 15% withholding that RRSP would
  avoid; also paid CAD→USD FX. Fine for a first tranche, but **fund the RRSP with USD and buy the US-div
  core (VTI/XLU/GOOGL) THERE going forward.** VXUS-in-taxable is still correct (FTC claimable). — Claude.

## 2026-07-26 — Stagflation game-plan + drop VTIP → Gold

- **DROPPED the 5% Short-TIPS (VTIP) sleeve; moved it to GOLD (9%→14%).** Hooman doesn't want VTIP.
  Rationale after deep VTIP/IEF/stagflation discussion: gold is grade-A in BOTH phases of an oil-shock
  stagflation (his base case) and is his USD-debasement hedge; VTIP was A− but he prefers gold; IEF
  rejected (C, coin-flip, hurt by inflation/rate-spikes — the scenario he fears). — Hooman.
- **STAGFLATION PLAYBOOK adopted (baked into `/fin_check`):** two-phase oil-shock stagflation.
  Rules: (1) SELL energy into Phase-1 strength AND sell HARD when Phase-2 demand-destruction starts —
  energy is front-loaded, don't ride it into the recession; (2) HOLD CASH as DRY POWDER — do NOT deploy
  into broad equities now (equities = worst stagflation asset, grade D); wait for the recession to buy
  the crash; (3) Gold is the anchor (14%), add on weakness; (4) each daily read notes which phase we're
  in (oil spiking=P1; oil rolling over + weak demand=P2 turning). Table in `fin_check.md`. — Hooman.
- **Consequence:** cash is no longer "excess to deploy ASAP" — it's strategic dry powder. The daily
  buy-tranche pressure is REMOVED for equities; gold-on-weakness + trims are the active moves.
  New sleeve set = 15 sleeves (no Short-TIPS), sums to 100%.

## 2026-09-06 — Broad commodity core = BCI

- **Selected BCI as the single broad-commodity ETF.** BCI tracks the Bloomberg Commodity Index Total
  Return across 25 futures contracts representing 23 commodities, charges 0.26%, and uses a transparent
  scheduled rolling methodology. It offers the best combination of breadth, low cost and predictable
  implementation for the portfolio's tactical commodity-supercycle allocation. — Hooman + Codex.
- **Rejected ZCOM as the default implementation despite identical BCOM exposure.** Its estimated 0.30%
  MER is slightly higher, CAD trading does not create meaningful CAD economic diversification, and as a
  Canadian-domiciled fund it is likely a PFIC for Hooman while he is a U.S. tax resident. Avoid it in a
  taxable account absent specific cross-border tax advice. A treaty-covered RRSP may mitigate the annual
  PFIC reporting issue, but BCI remains the cleaner and more established implementation. — Codex.
- **PDBC and COM remain alternatives, not the core.** PDBC costs 0.59% net (0.74% gross), makes active
  contract/roll decisions, and recently had about 50% energy exposure, increasing overlap with existing
  energy holdings. COM costs 0.72% and can move individual commodities to cash using trend signals, so it
  does not maintain the desired whole-complex exposure. — Codex.
- **Implementation rule:** use BCI in an already-funded, treaty-eligible RRSP when its cross-border tax
  treatment and filings are confirmed; otherwise use a U.S. taxable brokerage. Fund it by consolidating
  existing commodity exposure rather than layering it on top. Detailed rationale and sources:
  `BROAD_COMMODITY_ETF_DECISION_2026-09-06.md`.

## 2026-09-06 — BCI superseded by modular commodity sleeves

- **Do not add BCI.** Constituent-level review showed that PDBA already supplies agriculture, softs
  and livestock, while dedicated holdings already supply gold, copper and natural gas. BCI would
  duplicate those exposures without meeting the portfolio's deliberately high gold target. — Hooman + Codex.
- **Track energy-related exposure as three sleeves, not one:** `oil-companies` is 6% selected companies,
  `ref_oil_prod` is 2% DBE, and `nat_gas` is 1% UNG. The aggregate remains 9%, but each thesis now has
  its own target and drift signal. DBE's 2026-06-30 portfolio was 31.84% refined products, so a 2%
  allocation adds about 0.64% direct refined-products exposure. — Hooman + Codex.
- **Agriculture target remains 3%:** use 2% PDBA plus up to 1% CF if the separate dividend-company
  thesis is retained. PDBA already held 31.8% livestock on 2026-04-30. — Hooman + Codex.
- **Track metals as two sleeves:** `copper` is 2% dedicated copper exposure and `industrial_metals` is
  up to 1% PICK if broader mining-company exposure is desired. Reject DBB because of its cost, K-1 and
  48.35% copper concentration; reject EVMT as a core because of its very small asset base and liquidity.
  — Hooman + Codex.
- Gold remains 14%, silver/platinum 1%, and uranium/AI-power 3.5%, implemented separately. Full record:
  `COMMODITY_IMPLEMENTATION_DECISION_2026-09-06.md`.

## 2026-09-06 — Dividend discipline and the Munificent 7

**Status:** Accepted by Hooman on 2026-09-07; research assumptions confirmed.

- **Dividends are a tie-breaker, not a sleeve or primary selection rule.** Buy a company only when its
  total-return quality, valuation and portfolio role independently pass; then treat a durable dividend
  as a bonus. Do not replace diversified/direct-exposure ETFs merely to maximize current yield. — Hooman + Codex.
- **Jeff Currie's exact Munificent 7 are XOM, CVX, COP, SHEL, TTE, BP and EQNR.** His approximately 15%
  figure is free-cash-flow yield, not dividend yield; actual cash yields were roughly 3%–4%. XOM plus
  CNQ already provides sufficient producer exposure, so do not add the other six solely for income. — Codex.
- **The commodity implementation is unchanged.** Stage DBE and PDBA rather than chase recent strength;
  producers do not replace refined-product or grain futures exposure. Full analysis: `../divident_play.md`.
- **WPM look-through rule:** its Q2 2026 revenue was 52% silver and 46% gold. At the live snapshot,
  approximately 82 shares supply about 1% portfolio silver look-through and about 0.88% gold look-through.
  Treat 82 shares as a ceiling; platinum remains unfilled, and any future platinum purchase must replace
  part of WPM rather than increase the 1% satellite. — Hooman + Codex.

## 2026-09-06 — Options as an execution overlay; speculation target 1%

- **Formalize `Speculation (cap $10k)` at 1% and reduce cash from 20.5% to 19.5%.** At the live portfolio
  value this is about $6,620, of which LULU.TO currently uses about $3,174. No other investment sleeve
  was reduced. — Hooman + Codex.
- **Use short options only to execute pre-existing buy/trim decisions.** Cash-secured puts must fit the
  destination sleeve after assignment; covered calls are only for shares already acceptable to sell at
  the strike. Track genuinely speculative short options by full maximum loss, not premium received. — Codex.
- **Current implementation:** a one-contract PFE covered-call pilot is the best candidate if the account,
  tax lot, earnings date and strike pass review. Do not sell KWEB or UNG puts at current overweight sizes;
  do not use BOIL options; sell broken-thesis exit names outright. Full analysis: `../options_pay.md`.

## 2026-09-07 — Accepted uranium/nuclear and grid/electrification structure

- **Keep `uranium/nuclear` at 3.5%.** Hooman accepted the uranium review and its implementation:
  1.5% NLR + 1% CCJ + 0.5% CEG + 0.5% BWXT. The review assumptions are confirmed. — Hooman + Codex.
- **Create `grid/electrification` at 1% and classify GEV and ETN there.** Fund the entire new sleeve
  by reducing cash from 19.5% to 18.5%; do not reduce uranium. — Hooman.
- **No trades are recorded by this decision update.** Hooman has separately noted the CCJ trim and
  CEG/NLR additions. Full analysis: `research/uranium_sleeve_review_2026-09-07.md`.

## 2026-09-07 — IBM rejected; NKE remains a conditional speculation watch

- **IBM: no buy.** Hooman rejected the position after review; it has no target or active entry level in
  the portfolio plan. The research remains at `research/ibm_buy_review_2026-09-07.md`. — Hooman.
- **NKE: watch for now.** A 0.25% starter is authorized only near $36–$39, approximately $1,655 or 43
  shares at the $38.40 research price. Add no more than another 0.25% after operational confirmation or
  below roughly $34 with the thesis intact. — Hooman.
- **Risk cap:** NKE is capped at 0.5% while LULU remains; together they must remain within the existing
  1% speculation sleeve. Do not sell a standard 100-share put because assignment would exceed the NKE cap.

## 2026-09-07 — Financials reduced to 2%; Healthcare increased to 5.5%

- **Financials / insurance allocators: 2.0%.** Use 1.0% BRK.B plus the existing approximately 1.0% FFH;
  do not add a financial ETF. BRK.B is the downside-resilience complement, while FFH offers greater
  growth potential and Canadian optionality. FFH alone is rejected because its catastrophe, reserve,
  succession and investment-concentration risks are higher. — Hooman + Codex.
- **BRK.B implementation:** target approximately $6,620 / 13 B shares at the research snapshot. Buy
  roughly 6–7 shares initially and complete the position near $490 or after results confirm operating-
  earnings and book-value growth. Hold FFH; do not add. — Hooman + Codex.
- **Healthcare: 5.5%.** Use 2.5% VHT + 1.0% IHI + 1.0% CI + up to 1.0% LLY only at an acceptable
  valuation. CI moves from Financials to Healthcare; PFE is slated for sale subject to tax-lot review.
  Leave the prospective LLY allocation in cash until its entry criteria are met. — Hooman + Codex.
- **No live portfolio update was requested.** Hooman will implement the allocation changes manually.

## 2026-09-07 — Utilities 2.5% via VPU; Gold 15%; Grid 1.5%

- **Reduce Utilities from 4% to 2.5% and use VPU as the sole broad-utilities core.** Sell/swap the
  legacy 58 XLU shares rather than owning both funds. The staged planning quantity is 45 VPU, then
  22, then 22, subject to account, tax-lot, price and thesis verification. — Hooman + Codex.
- **Reallocate the freed 1.5 percentage points to high-conviction themes:** add 1.0% to Gold, taking
  it to 15%, and 0.5% to `grid/electrification`, taking it to 1.5%. Keep uranium/nuclear at 3.5%,
  energy at 9%, global equity core at 20%, and cash at 18.5%. — Hooman.
- **The direct power complex is capped at a 7.5% strategic target:** 2.5% Utilities + 3.5%
  uranium/nuclear + 1.5% grid/electrification. The grid increase formalizes the existing GEV/ETN
  thesis and does not automatically authorize additional purchases. — Hooman + Codex.
- **Recordkeeping only:** Hooman made the portfolio changes himself. These files record the accepted
  policy and planned orders but do not assert broker fills, execution prices or tax-lot results.

## 2026-09-08 — Defense 1.5% via SHLD; Speculation increased to 1.5%

- **Reduce Defense from 2.0% to 1.5% and use SHLD as the sole vehicle.** Stage the position as three
  0.5% tranches under the entry and confirmation gates in the defense review. Do not buy ITA or PPA;
  XAR remains only the lower-cost substitute. — Hooman + Codex.
- **Redirect the freed 0.5% to `Speculation (cap $10k)`.** Its percentage target becomes 1.5%, but the
  hard $10,000 dollar cap remains. Cash stays at 18.5%. — Hooman.
- **No SHLD trade is recorded.** This decision updates targets and planning records only; shares,
  account, execution price and tax lots remain unconfirmed.

## 2026-09-08 — Keep existing OneGold; use GLDM for remaining gold purchases

- **Keep the existing approximately five ounces of OneGold Switzerland Gold, but do not add the
  entire remaining approximately $43,000 gold target there.** OneGold is a credible allocated,
  pooled Swiss-vault position, but its materially wider exit spread, private-platform concentration
  and sale-plus-APMEX-repurchase redemption process make it unsuitable as the sole gold vehicle.
- **Use GLDM for the remaining approximately $43,000 of the 15% gold allocation.** GLDM is a
  physically backed, allocated U.S.-listed gold trust with a 0.10% sponsor fee and substantially
  lower trading friction. IAUM remains an acceptable near-tie if its live execution is better.
- **Preserve custody diversification.** The completed sleeve will span the existing OneGold Swiss
  position, the existing Royal Canadian Mint MNT position, GLDM and the existing small mining-equity
  holdings. Swiss vaulting is diversification, not protection from lawful seizure or account freezes.
- **Canadian portability remains unconfirmed.** Before relying on future Canadian delivery, obtain
  written confirmation that the U.S.-registered OneGold account can remain open after a Canadian
  move and that redemption can ship to the new verified address. Redemption does not deliver the
  same Swiss bar; it sells the vaulted interest and purchases an APMEX product.
- **Recordkeeping only:** Hooman accepted the conclusion and updated his notes manually. No live
  portfolio, target, holding or trade record was changed. Full review:
  `research/onegold_gold_vehicle_review_2026-09-08.md`.

## 2026-09-08 — Quality-factor vehicle and final allocation

- **Final allocation: 3.5% JQUA plus 1.5% direct AMZN**, totaling 5.0% of the portfolio. AMZN is
  retained as a deliberately sized AWS/AI/commerce compounder because it was absent from JQUA's
  reviewed holdings; GOOGL can be converted to JQUA because Alphabet is represented in the fund.
  Hooman updated the portfolio directly. — Hooman + Codex.
- **The allocation's purpose is diversified U.S. quality-factor exposure plus a bounded AMZN
  conviction**, offsetting some of the
  portfolio's cyclical/resource and concentrated thematic risk. It is an equity tilt, not a separate
  asset class, an AI mandate or protected house capital. — Hooman + Codex.
- **Choose JQUA when portfolio balance is the objective; choose QUAL only for an intentional
  concentrated mega-cap/AI quality tilt; choose neither if the broad VTI/VXUS core later becomes
  substantially larger.** Hooman accepted these decision rules. — Hooman + Codex.
- **Final ETF selection: JQUA.** It is not a small-cap fund: it selects from the Russell 1000 and
  had an approximately $586B weighted-average market capitalization. It retains substantial AI
  exposure but reduces top-ten concentration from QUAL's 44.24% to 18.5% and had a lower reported
  portfolio P/E. QUAL remains the alternative if the sleeve is deliberately redefined as AI/mega-cap
  quality rather than portfolio balance.
- **Non-tech comparison:** excluding both technology and communication/telecommunications, the
  current funds were approximately 52.5% non-tech for QUAL and 57.5% for JQUA. QUAL held LLY at
  3.64%, equivalent to about 0.20% of the total portfolio at a 5.5% QUAL allocation; JQUA spread its
  roughly 9% healthcare weight more broadly.
- **Recordkeeping only:** Hooman already updated the portfolio and will maintain his notes. No live
  sheet, target, holding, notes or trade
  record was changed here. Full review: `research/quality_compounders_sleeve_review_2026-09-08.md`.

## 2026-09-14 — Healthcare growth-name follow-up accepted

- **Keep the accepted 5.5% Healthcare structure unchanged:** 2.5% VHT + 1.0% IHI + 1.0% CI + up to
  1.0% LLY at an acceptable valuation. At the reviewed $1,138 price, LLY had not run away from the
  prior decision; it remained below both the original review price and Hooman's sale price. Retain the
  first LLY entry gate near $1,050, subject to updated earnings estimates and the thesis remaining intact.
- **TWST, GH and NTRA are watchlist names, not current buys.** Twist Bioscience is an AI-drug-discovery
  picks-and-shovels supplier but remains loss-making at approximately 20 times sales. Guardant Health is
  the most direct AI/cancer-data exposure but remains deeply loss-making and cash-burning at approximately
  16 times guided revenue. Natera has the strongest operating quality and ranks first of the three, but
  remains unprofitable and similarly trades near 16 times guided revenue and a 52-week high.
- **Reassessment zones:** approximately $70-$85 for TWST, $105-$125 for GH and $220-$260 for NTRA,
  always subject to updated fundamentals rather than price alone. If NTRA eventually qualifies, cap an
  exploratory position at 0.25%-0.50% and fund it from VHT rather than enlarging Healthcare beyond 5.5%.
- **PFE:** the remaining Ameritrade position is accurate and has a GTC sell order at $28. The approved
  direct-PFE exit remains unchanged.
- **Recordkeeping only:** no allocation, live holding, trade or user-maintained portfolio notes were
  changed. Full review: `research/healthcare_ai_sleeve_2026-09-07.md`. — Hooman + Codex.

## 2026-09-22 — Semiconductor exposure remains indirect; SOXQ added to research watch

- **Do not create a permanent semiconductor sleeve or change current allocation targets.** Semiconductors
  are a strong structural industry, but fully funding VTI, VXUS, JQUA and an approximately 2% VWO position
  should already produce roughly 3.3%–3.8% look-through semiconductor exposure. A dedicated ETF would be
  an intentional tactical overweight, not gap-filling. — Hooman + Codex.
- **SOXQ is the preferred dedicated vehicle if a better entry develops.** It tracks the 30-company PHLX
  Semiconductor Sector Index, includes both AMD and Intel, costs 0.19%, and is less Nvidia-concentrated
  than SMH while avoiding XSD's small-company/speculative tilt.
- **Do not chase the current sector cycle.** SOXQ was approximately 40 times trailing earnings, up about
  100% over one year and 23% above its 200-day average when reviewed. AMD, Intel and Micron were rejected
  as direct purchases at current prices.
- **Accepted watch rules:** reassess near $85 for an up-to-0.5% starter and near $79–$80 for a second
  tranche, with a 1.0% tactical cap. Any purchase would substitute for VTI/JQUA rather than enlarge total
  equity risk, and every price trigger requires updated fundamental confirmation.
- **Monitoring only:** SOXQ was added to the read-only `$fin-check` watchlist and dedicated research
  watch block. No holding, target, trade or user-maintained portfolio notes were changed. Full review:
  `research/semiconductor_sleeve_review_2026-09-21.md`.

## 2026-10-02 — BHP exit, COPX staging plan, and FIS purchase

- **Sold BHP:** full 50-share Ameritrade position at $85.625. The realized gain versus the recorded
  $82.78 average cost was approximately $142.25 before tax and fees. The sale completes the prior
  direct-BHP cleanup and preserves the ETF-first metals structure.
- **COPX plan:** keep the existing 78 shares. Wait for a meaningful copper/COPX down day, then add
  only enough to restore the 2% copper sleeve—approximately $1,700 or 20 shares at the October 2
  reference price. Do not reinvest all BHP proceeds into COPX; retain the remainder as cash unless
  it is separately allocated.
- **Bought FIS:** 138 shares in Ameritrade at $32.435, classified as `Speculation`. This is an executed
  user-directed trade, not a researched recommendation. No additional FIS purchase is approved before
  completing fundamental research and reconciling the speculation sleeve with its 1.5% target.

## 2026-10-04 — North American energy-export names selected

- **Selected implementation:** Hooman chose `TOU.TO`/`TRMLF`, `LNG` and `BKR` rather than `MLPX` as
  the primary implementation. This is the higher-upside, less-diversified company basket from the
  North American energy-export review.
- **Roles:** `LNG` is the direct U.S. liquefaction/export franchise; `TOU.TO` is the low-cost Canadian
  gas producer with growing JKM/TTF-linked marketing; `BKR` is the LNG equipment and compression
  picks-and-shovels position.
- **Portfolio constraints:** `TOU.TO` should remain within its existing company target unless the
  allocation is separately changed. `BKR` overlaps the existing `SLB` oil-services exposure, so the
  combined services weight must be reviewed before sizing. Do not treat these selections as permission
  to add unlimited energy exposure on top of the portfolio's current approximate 10.2%.
- **Execution update — 2026-10-06:** Ameritrade bought 22 `TRMLF` at $43.926, 4 `LNG` at $275.7359 and
  18 `BKR` at $57.23. `TRMLF` and `TOU.TO` are the same issuer exposure and must be aggregated. Hooman
  maintains the live-sheet notes. Full research: `research/north_american_energy_export_thesis_2026-10-04.md`.
  — Hooman + Codex.

## 2026-10-06 — VGIT target accepted and funded from Global Equity Core

- **[CONFIRMED BY USER] Add a 5% tactical Treasury allocation using VGIT.** Its purpose is recession and
  disinflation protection plus capital-gain potential if intermediate yields fall; it is not the
  portfolio's inflation hedge.
- **Fund the target from broad equities, not Cash.** Global Equity Core falls from 20% to 15%; VTI falls
  from 11% to 8.25% and VXUS from 9% to 6.75%, preserving their proportional split. The Cash target and
  current cash balances remain unchanged.
- **Execution update — 2026-10-06:** Ameritrade bought the first 53 `VGIT` shares at $56.6181
  ($3,000.76). The remaining target should still be staged because the October 2 composite inflation
  signal was YELLOW. The purchase was partly funded by selling 30 `SGOV` shares at $100.455.
- **Research follow-up:** compare corporate bonds and other income strategies, including the tax claims
  around QQQI, GPIQ and JEPQ, before adding any further income allocation.

## 2026-10-08 — Reconfirmed 5% VGIT; rejected municipal substitution and 10% sizing

- **[CONFIRMED BY USER] Keep the full 5% tactical fixed-income target in `VGIT`.** The sleeve's primary
  purpose remains recession/disinflation protection and capital-gain potential when intermediate
  Treasury yields fall.
- **Do not substitute `VTEC`, `CMF`, `VTEB`, Texas bonds or other municipal debt for VGIT.** Municipal
  bonds can offer higher after-tax income, but credit/liquidity-spread widening, call risk and longer
  duration make them less reliable in the stressed recession regime this sleeve is meant to hedge.
- **Do not increase VGIT to 10% under the current portfolio construction.** Moving from 5% to 10% would
  reduce the Global Equity Core from 15% to 10%, create a larger tactical inflation/rate bet and add
  only modest incremental portfolio protection. Revisit 7.5%-10% only if recession evidence strengthens,
  inflation indicators turn clearly favorable or fixed income becomes a strategic allocation.
- **No allocation or implementation change is required.** Continue staging the existing 5% target under
  the accepted inflation/yield gates. The protected `FR_Portfolio!E1:K23` TODO Notes block remains untouched.
- Full municipal reviews: `research/california_municipal_bond_review_2026-10-08.md` and
  `research/other_state_municipal_bond_review_2026-10-08.md`. — Hooman + Codex.

## 2026-10-14 — ASTS speculation purchase recorded

- **Executed:** Ameritrade bought 70 `ASTS` at $42.355 at 2:52 p.m. ET, for a total basis of $2,964.85.
- **Classification:** `Speculation`; portfolio targets are unchanged. `ASTS` does not count as Defense
  or Quality Compounders.
- **Constraint:** the speculation sleeve already exceeds its 1.5% / $10,000 cap. Recording this fill
  does not approve another purchase. Any further add requires an explicit cap decision plus evidence
  on commercial service, launches, financing and unit economics. — Hooman.

## Proposed (in ideal_allocation.md / buy_list.md / sell_rules.md — awaiting Hooman sign-off)

- Ideal allocation: cash 30 / global-equity 22 / EM 5 / quality compounders 8 / energy 10 / gold 9 /
  copper 3 / uranium-power 4 / healthcare 3 / ag 3 / crypto 2 / silver-plat 1.
- China: 3-5% via KWEB/BABA/VWO in RRSP; cut BIDU.
- AI: indirect (Adobe already covers app-layer; add GOOGL/AMZN quality; breadth via index; avoid froth).
- Sell rules + quarterly band-rebalance (>5pt drift) cadence — see sell_rules.md.
