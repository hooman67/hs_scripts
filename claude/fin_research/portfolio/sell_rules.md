# Sell Rules & Position Thesis Ledger

**Prepared 2026-07-07 (Opus 4.8).** RESEARCH, NOT FINANCIAL ADVICE. This is the file you asked for:
**why we own each thing, when to buy more, when to sell.** Pre-committing exits is the antidote to "I
could've sold XOM higher but didn't." Update as theses evolve.

## Quality and silver policy override — updated for November 5 executions

- Direct GOOGL was sold in full on October 30: 16 shares at $280.9362. Ameritrade bought 71 JQUA at
  $76.46. The live Sheet records both fills. Do not re-enter GOOGL merely because it rebounds, and
  avoid a household repurchase before November 30; confirm tax lots before any later purchase.
- The unchanged 5.5% Quality sleeve now contains existing AMZN plus 211 JQUA, 20 LRCX and 17 ANET
  shares. Direct positions replace JQUA dollar-for-dollar. LRCX remains capped at 1%; ANET has no
  adopted target and is no-add pending review. Do not add KLAC without reallocating within the sleeve.
- Do not add direct silver while 154 WPM shares remain. Future long-term brokerage implementation,
  if room is created, defaults to SIVR; SLV is tactical and OneGold is for minority custody.

---

## Sell when profitable — confirmed by Hooman, 2026-10-15

All currently held **Speculation** positions are in a conditional full-exit queue:
**LULU.TO, SHOP.TO and UBER**. `ASTS` was sold in full on 2026-10-19 at $43.19, `NKE` was sold in
full on 2026-10-20 at $37.9926, `FIS` was sold in full on 2026-10-29 at $37.493, `TTD` was sold in
full on 2026-11-10 at $15.401, and `CLX` was sold in full on 2026-11-12 at $108.785. These positions
are closed and removed from the queue. Include any additional holding currently classified
Speculation on each `/fin_check`; retain queued names until sold or explicitly removed from this
instruction, even if reclassified.

Flag for sale as soon as the current quoted price is **strictly above the recorded average purchase
cost in the same currency**. At/below cost: wait under this rule. Confirm actual broker lots, selling
fees and executable bid; the monitoring flag is nominal price profit before unrecorded taxes/fees,
not guaranteed net profit or historical-FX tax P/L. Missing/stale quotes or missing/ambiguous cost
must show a verification warning, never a profitable-sale trigger.

Keep holdings in Speculation for exposure/cap tracking until execution. Do not recommend averaging
down or adding to names in this queue. This user condition takes precedence over conflicting generic
add/trim advice for these names; surface thesis-break or cap concerns separately. Existing legacy
exit rules, portfolio targets and protected Google Sheet notes are unchanged. Hooman executes trades;
fin-check checks the queue on every invocation and records no fills.

## Universal sell triggers (apply to EVERY position)

Sell (or trim) when ANY of these fires — decided in advance, executed without re-litigating:
1. **Thesis break:** the specific reason you bought is no longer true (see per-position thesis below).
2. **Concentration:** any single stock exceeds **5% of total** portfolio → trim back to ≤5%.
3. **Factor cap:** any macro-factor exceeds **~18-20% of total** → trim the richest/highest-beta name in it.
4. **Valuation blow-off:** a position runs to an extreme multiple vs its own history with no fundamental
   change (e.g. GEV at ~89× EV/EBITDA) → trim into strength.
5. **Better use of capital:** a clearly higher-conviction, cheaper opportunity needs funding.
6. **Tax-loss harvest:** a taxable-account loser with a broken/weak thesis → harvest (mind superficial-loss).
7. **You can't restate the thesis in one sentence** → you don't understand it well enough to hold it.

**NOT a sell trigger:** price falling while the thesis is intact (that's an add signal if quality holds);
short-term volatility; a pundit's opinion; boredom.

---

## Per-position thesis + buy/sell levels (living)

Legend: **T** = thesis (why own). **ADD** = when to buy more. **SELL/TRIM** = exit trigger. Grade from
Phase-1 research.

### Dividend selection rule — accepted 2026-09-07

Dividends are a tie-breaker after growth, quality, valuation and sleeve fit—not a reason to create a
position or retain an overweight. Track dividend growth, mid-cycle FCF payout, leverage, net share count,
ROIC and total return versus the relevant ETF. Do not substitute producer equities for DBE, PDBA or PICK.

### CORE — keep, add on weakness
| Pos | Thesis (why own) | ADD when | SELL/TRIM when |
|---|---|---|---|
| **VT/VTI/VXUS** (to build) | Own the world's productive companies; my "no edge" baseline | every DCA tranche; any −10%+ market dip | ~never (this is the core); only to rebalance band |
| **AMZN** 7.5 | Best-conviction AI winner; AWS + retail, 50% GM, fair ~25× | dips below ~$220 | thesis break: AWS growth stalls / margin collapse; or >5% cap |
| **JQUA** | Diversified Quality-factor residual core; reduces single-company and employer/AI-cycle concentration | no automatic add until the November 5 positions and manual Ameritrade cash are reconciled | rebalance outside the 5.5% sleeve; direct positions count dollar-for-dollar |
| **ANET** | High-quality Ethernet networking leader with direct AI-cluster exposure, exceptional margins and a strong balance sheet | no automatic add; review around $150-$155 with fresh results | AI-network growth/customer concentration thesis break; rebalance above the 2% hard cap |
| **LRCX** | Leading wafer-fabrication equipment supplier with strong margins, net cash and AI-memory exposure | no automatic add; fund any later increase from JQUA and remain within the 1% cap | WFE/China/service thesis break; rebalance above 1% |
| **CNQ** | Highest-quality Cdn oil sands, long-life low-decline, Cdn tailwind | only after it is at/below its 2% name target and oil <$60 | oil demand peak evident; balance-sheet deterioration; trim above 2% target |
| **XOM** | Defensive integrated, refining cushions crude swings | deep energy selloff | dividend risk; integrated model breaks; >5% |
| **EOG** (via OXY swap) | Best-quality US shale, fortress balance sheet, sub-$50 breakeven | oil pullback | quality erosion; leverage rises |
| **AEM** 7 | Best-in-class gold miner, fwd P/E 11.2, gold hedge proxy | gold $3,400-4,000 zone | gold thesis break (real rates spike + CB buying stops) |
| **Physical gold + MNT** | THE monetary USD-debasement hedge; sovereign bid | gold $3,400-4,000; USD-crisis signals | only to rebalance (this is the hedge, not a trade) |
| **VPU** | Broad regulated-heavy utilities diversification; defensive equity, not a bond or house-cash substitute | stage toward the 2.5% sleeve target | rebalance outside 2.0%-3.0%; thesis break in rate-base recovery, balance sheets, or regulation |
| **SHLD** | Global defense primes plus AI/software, drones, autonomy and space | stage toward 1.5% under the accepted three-tranche plan | trim above 2%; sell if real defense procurement reverses or backlog broadly fails to convert into profit |
| **CEG** ~21× | Cleanest AI-power/nuclear value, contracted PPAs | pullbacks | PPA/regulatory break; >4% uranium-power cap |
| **BWXT** | Naval/defense nuclear quality, durable govt demand | pullbacks | defense-budget break; valuation blow-off |
| **CF** 7.0 | Best commodity-quality: low-cost nitrogen, 33% margin, 27% ROE | ~10× or below | nat-gas cost spike destroys margin; >3% ag cap |
| **LLY** 6.5 | Elite pharma, GLP-1 franchise, growth-justified premium | **only <$1,080** | GLP-1 share loss to Novo/orals; valuation de-rate on a miss |
| **CI** (to buy) | Cheapest quality healthcare, fwd 8.4×, ROE 16%, no patent cliff | now / weakness | PBM-reform hit; managed-care thesis break |
| **BABA** | Highest-quality China, net cash, buying back stock | broad China selloff | VIE/delisting escalation; Taiwan tail; >China 5% cap |
| **KWEB / VWO** | EM/China diversification, cheap part of EM | build to 5% target | Taiwan escalation; China 5% hard cap |
| **BTC** | Small asymmetric non-sovereign hedge | only to rebalance to 2% | >3% (trim); thesis = it's just risk-asset in a real crash |

### RIGHT-SIZE / TRIM (holding too much or too rich)
| Pos | Issue | Action |
|---|---|---|
| **WPM** | 4.49% of portfolio; Q2 mix 52% silver / 46% gold; no meaningful platinum | trim from 192 to approximately 82 shares as the current ceiling; trim further if adding platinum |
| **CCJ** | fwd P/E ~78×, equity froth | trim ~half; keep uranium exposure via CEG |
| **PFE** | 3.17% of portfolio; high yield but patent/pipeline and concentration risk | trim toward the accepted 1% name target; dividend is not a reason to remain overweight |
| **GEV** | +87%, ~89× EV/EBITDA | trim ⅓, bank win |
| **XLU** | Legacy broad-utilities holding after VPU was selected as the sole core | sell/swap to VPU; do not own both |
| **Adobe RSUs** | ~$732k = largest asset, US-tech/salary same risk | **trim on vest** (highest-value move) |

### SELL / EXIT (thesis weak or broken)
| Pos | Why exit |
|---|---|
| BAC | confirmed permanent exit; no accepted portfolio role (2026-10-23 tax-harvest plan) |
| BIDU | broken (ROE 0.3%, shrinking) |
| CRCL | unprofitable, −74%, held twice (via ARKK) |
| CAG | confirmed permanent exit; value-trap; keep KHC only |
| SBSW | platinum falling-knife, broken SA miner |
| XME | not a steel ETF (½ gold/coal) — redundant |
| AA | confirmed permanent exit; redundant w/ XME |
| RBLX | confirmed permanent exit; off-thesis / bubble-beta |
| ARKK, SBUX | off-thesis / bubble-beta |
| MARA | crypto-miner (own BTC directly instead) |
| 10 micros (AEVA/AUR/CHPT/NIO/F/LCID/RIVN/JMIA/GLBS/CSGP) | negligible, contradict ETF-philosophy |
| **ARX** | Shell takeover — decide hold-to-close vs sell-and-redeploy (recommend redeploy) |

### NEVER BUY (from research)
Nickel (falling knife, no clean vehicle), steel, rare earths (momentum not value), more uranium equity at
these multiples, more oil into the 2026-27 glut, 60-190× AI names (Tesla/AMD/Palantir), OpenAI-bailout
speculation, long-duration US Treasuries, high-yield covered-call ETFs (QQQI/SPYI/TLTW — bad for long-term
total return, you already concluded this).

---

## Rebalancing cadence (enforces discipline)
- **Quarterly review** (not continuous). Only trade a sleeve when it drifts **>5 percentage points** off
  its `ideal_allocation.md` target — a band rule that cuts taxes and over-trading.
- **Annual deep review** — re-grade the macro theses (this whole Phase-1 exercise, repeated).
- **Event-driven** — only for a genuine thesis break or a corporate action (like ARX/Shell), not for
  headlines.

---

## How to use this file
1. Before ANY buy: write the one-sentence thesis + the ADD and SELL levels here first.
2. Before ANY sell: check it against the universal triggers — is this a trigger, or an emotion?
3. Quarterly: read the SELL/TRIM column top to bottom; act on what fired.
4. Keep it live — when a thesis changes, edit the row and date it.

**NOT financial advice.**
