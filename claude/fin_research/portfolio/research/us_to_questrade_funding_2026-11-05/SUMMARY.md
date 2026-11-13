# U.S. USD to Questrade Cash Funding Review — 2026-11-05

## User facts

- California/U.S. tax resident filing jointly; Canadian citizen and not currently filing in Canada.
- Destination is a true non-registered Questrade Cash account that can hold USD and CAD but cannot borrow.
- Candidate transfer is US$15,000–20,000 of settled cash in a U.S. bank.
- A same-name TD Canada account is linked to Questrade, but currently has no CAD and the user's normal
  TD-to-Questrade transfer takes about two days.
- Objective: determine what can fund a Canadian-stock purchase tomorrow and the lowest-cost route over
  approximately the next week.

## Decision

No cross-border path is reliable for a purchase before the next TSX close. Questrade's official USD-wire
processing time is 1–2 business days after receipt, and it is already after U.S. bank cutoffs on Thursday.
Coinbase/NDAX adds holds and more settlement legs and does not solve this timing problem.

For an issuer with a liquid U.S. exchange listing, buy that listing in the U.S. brokerage if the investment
case and portfolio sizing independently support it. Enerflex is available as NYSE `EFXT`; illiquid OTC
substitutes for TSX-only names should not be used merely to meet a one-day deadline.

For the next week, use one of these two routes:

1. **Simplest and fastest after funding:** wire USD directly to Questrade, convert only the amount required
   for an approved purchase at Questrade's disclosed 1.5% currency-conversion charge, and buy in CAD.
   The FX cost is about US$225–300 on US$15,000–20,000, plus the sender's wire charge and a possible
   US$20 intermediary deduction.
2. **Lower explicit cost, slower and exposed to market movement:** wire USD to Questrade, buy a liquid
   interlisted operating company not already held (Questrade uses `TD`/`TD.TO` as its example), request
   the journal online, and sell the CAD listing with a limit order. The journal costs C$9.95 unless the
   account has Questrade Plus. A recent purchase adds one settlement day; the journal commonly needs
   another 1–2 business days and may take up to five. The position must not be traded while processing.

Obtain a live Wise USD-to-CAD quote as a third comparison. Wise must deliver to the user's same-name TD
Canada account, not directly to Questrade. Once CAD reaches TD, Questrade Instant Deposit can be immediate
and is CAD-only, up to C$10,000 per transaction or the bank's lower limit. Wise may provide a more
predictable total cost than assuming several days of single-stock price risk.

## Account-type constraint

A Questrade Cash account cannot keep a negative CAD balance. When a purchase creates a negative currency
balance, Questrade automatically converts the other currency around 4 p.m. A temporary CAD-debit bridge
is available only in a Margin account. Therefore buying TSX stocks first and completing Norbert's Gambit
later does not work in the user's current Cash account; it would trigger the 1.5% conversion.

## Why not crypto

- Coinbase says ACH-funded cash may be held and crypto bought with held funds cannot be sent off-platform.
- Coinbase charges transaction/spread and network fees; USDT withdrawals add a 0.01% processing fee up to
  20 USDT plus network cost.
- NDAX charges 0.20% to sell crypto into CAD plus the order-book spread, then C$4.99 for an EFT withdrawal
  taking 0–1 business day (or C$1.50 Interac, limited to C$10,000).
- CAD still has to move through the user's Canadian bank and into Questrade.
- The IRS treats crypto as property, making the conversion into CAD a reportable disposition.

This route has more failure points and cannot reliably beat the USD wire for speed.

## U.S. tax/reporting guardrails

Avoid `DLR.U`/`DLR` in the taxable Questrade account unless a cross-border tax adviser explicitly accepts
it. Global X says its Canadian ETFs are generally PFICs for U.S. tax filers, and IRS Form 8621 instructions
list recognized gain on a PFIC disposition as a filing trigger. A liquid interlisted operating company
avoids the Canadian-ETF PFIC issue, although its sale still creates an ordinary reportable short-term gain
or loss and carries several days of equity-price risk.

The cash transfer itself is not a sale. Questrade is a foreign financial account: FBAR applies when aggregate
foreign financial accounts exceed US$10,000 at any time. For married filing jointly while living in the
United States, Form 8938 thresholds are more than US$100,000 at year-end or US$150,000 at any point. The
additional funding increases the account's maximum balance for reporting.

## Practical sequence

- **Friday:** do not use Coinbase/NDAX. If a desired issuer has a liquid U.S. listing, use that listing only
  if its price and sleeve sizing independently pass the portfolio rules. Otherwise keep the limit order
  unplaced rather than manufacture urgency.
- **Friday morning:** initiate the same-name USD wire using Questrade's current “USD funds from outside
  Canada” instructions; retain the receipt.
- **When the wire posts:** choose either the 1.5% conversion for the urgent approved tranche or the
  interlisted-stock journal for funds that can wait several more business days.
- **In parallel:** obtain a live Wise quote and promised delivery date to the same-name TD Canada account.
  Use TD-to-Questrade Instant Deposit if available after the CAD arrives.
