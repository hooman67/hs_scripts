# EOG — Portfolio Fit: Does Adding EOG Diversify, or Just Double an O&G Bet You Already Have?

**Question (Hooman's framing):** You are **already ~12% weighted in oil & gas**. Does adding
**EOG Resources (EOG)** *add* value/diversification to that sleeve, or does it just pile more
onto exposure you already own — especially versus your two largest O&G positions, **ExxonMobil
(XOM)** and **Canadian Natural Resources (CNQ)**?

**Prepared:** 2026-07-05 by Claude (Opus 4.8). Owner: Hooman Shariati (**Canadian citizen**).
**RESEARCH, NOT FINANCIAL ADVICE — a decision framework, not a recommendation.**
**Builds on** `deep_dives/EOG/deep_dive.md` (score 6.9/10) and `deep_dives/EOG/profile_and_diligence.md`
and `screens/sector_trends.md` (O&G = the cheapest sweet-spot). It does **not** re-litigate the EOG
peak-cycle valuation test — read those files for that.

> ### ⚠️ BLOCKER / LIMITATION — READ FIRST
> **Your full O&G holdings table did NOT come through.** You intended to paste all your oil-&-gas
> tickers with their portfolio %, but the message arrived with only the **two named largest
> positions: XOM and CNQ**. So this analysis does the rigorous **EOG-vs-XOM-vs-CNQ** comparison in
> full, but:
> - It is built to have **more holdings slotted in later** — the framework generalizes; send the
>   rest of the table and I'll finalize the sleeve-level view (correlation matrix, concentration,
>   factor tilts across *all* names).
> - The **~12% total O&G weight** is treated as backdrop. **12% in one sector is already a full-to-
>   heavy allocation** in most asset-allocation frameworks (a market-cap-neutral energy weight is
>   ~3–4% of global equities), so a live question — **separate** from "is EOG a good name" — is
>   **whether the O&G sleeve should grow at all.** Both framings are laid out in §4.

> **Anti-hallucination (CLAUDE.md §5 #1).** Every number is a **live yfinance pull (as-of
> 2026-07-05)** or a filing figure carried from the two EOG files (EDGAR-verified there), or a cited
> commodity price. Confidence marks: **VERIFIED** = pulled live/primary this session; **ASSUMED** =
> my derivation/judgment; **UNVERIFIED** = single secondary source. yfinance snapshot as-of
> **2026-07-05 00:32 PT**. Commodity/FX (yfinance futures/FX, ~15-min delayed, 2026-07-05):
> WTI **$68.78**, Brent **$72.13**, Henry Hub **$3.24**, **USD/CAD 1.42**.

---

## Jargon key (read once)

| Term | Plain meaning |
|---|---|
| **Integrated / supermajor** | An oil company that does **everything**: pumps oil (upstream) *and* refines it into fuels/chemicals (downstream) *and* often ships gas (LNG). Downstream *makes more money when oil is cheap* (cheaper input), so it partly **offsets** upstream swings → lower sensitivity to the oil price. **XOM** is this. |
| **E&P (upstream pure-play)** | Only finds and pumps oil/gas, then sells the raw commodity. No refining cushion → **full exposure** to the oil price. **EOG and CNQ** are both this (different flavours). |
| **Short-cycle (shale/tight-oil)** | Wells that are fast to drill and pay back in months, but **decline fast** (~high first-year drop) → must keep re-drilling. High "torque" to price. **EOG.** |
| **Long-life low-decline (oil sands)** | Reserves that produce for **decades** at a slow, steady decline — like a utility-ish oil asset. Very long reserve life, low re-investment need, but heavy upfront capital. **CNQ.** |
| **WCS differential** | Western Canadian Select (heavy Canadian oil) trades at a **discount** to WTI (the US light benchmark) because it's heavier/sourer and land-locked. That discount ("the diff") is a Canada-specific risk **CNQ** carries and EOG/XOM largely don't. |
| **Torque / oil-price sensitivity** | How much the stock moves per unit move in oil. High torque = more upside if oil rises, more downside if it falls. Measured here as **beta-to-WTI** (§2c). |
| **Breakeven** | The oil price at which cash flow just covers capex + the base dividend. Lower = survives deeper troughs. |
| **Total shareholder yield** | Dividend yield **+** buyback yield **+** special/variable dividends — the *total* cash returned per year ÷ market cap. |

---

## TL;DR — the verdict up front

1. **EOG is NOT redundant to XOM+CNQ — it fills a genuine gap: the US light-shale, short-cycle,
   buyback-heavy, high-torque leg** that neither XOM (defensive integrated) nor CNQ (long-life
   heavy oil sands) covers. On the three *business* axes — refining cushion, reserve life/decline,
   oil-price torque — the trio are genuinely three different animals. **ASSUMED/VERIFIED (business
   descriptions from the two EOG files + web-standard; the torque/quality numbers VERIFIED below).**

2. **BUT within one sector "different flavours" is not the same as "uncorrelated."** All three still
   rise and fall with the oil price. **3-year weekly return correlations: EOG–XOM 0.79, EOG–CNQ
   0.76, XOM–CNQ 0.69 (VERIFIED, yfinance).** Adding a third O&G name gives you a *better-blended*
   sector sleeve, **not** true portfolio diversification — the dominant risk (oil price) is shared.

3. **The 12%-weight point may matter more than the name.** ~12% in energy is **already a full/heavy
   sector bet.** The first-order decision is *"should the O&G sleeve grow at all?"* — separate from
   *"is EOG the right name."* If you like EOG, the cleaner question is likely **SWAP, not ADD**
   (fund it by trimming XOM and/or CNQ), so the sleeve doesn't concentrate past 12%. Both framings
   in §4.

4. **What EOG uniquely adds if you do slot it in:** the *highest quality* balance sheet + returns of
   the three (ROE 18.2%, lowest leverage), the *most torque to oil* (tied with CNQ), the *US
   light-oil* geography (vs CNQ's Canada/heavy), and a *buyback-heavy* return style (share count
   −9% in 4 yrs) vs XOM's dividend-aristocrat style and CNQ's high-dividend style.

5. **Still needed to finalize:** the **full holdings table** (all tickers + %). With only XOM+CNQ I
   can characterize the *core* but not the whole sleeve's concentration/factor tilt.

---

## 1. Three DIFFERENT kinds of O&G exposure — do they overlap or complement?

The whole diversification question turns on this: are XOM, CNQ, and EOG **three ways to own the same
bet**, or **three genuinely different bets that happen to share a commodity**? Answer: structurally
**different businesses**, but **one shared master-risk (the oil price)**.

| | **XOM — ExxonMobil** | **CNQ — Canadian Natural Res.** | **EOG — EOG Resources** |
|---|---|---|---|
| **What it is** | **Integrated supermajor** | **Oil-sands-heavy E&P** | **US shale/tight-oil E&P** |
| **Business model** | Upstream **+ downstream refining + chemicals + LNG** | Upstream only — but **long-life, low-decline** (oil sands + conventional heavy) | Upstream only — **short-cycle premium shale** |
| **Cycle length** | Mixed (refining is counter-cyclical) | **Long** (decades of reserve life) | **Short** (fast payback, fast decline → constant re-drill) |
| **Oil type** | Diversified (light + refined products) | **Heavy oil / oil sands** (WCS-linked) | **Light oil + gas** (WTI-linked) |
| **Geography / politics** | US-HQ, **global** operations | **Canada** (oil sands), CAD reporting | **US onshore** (Permian, Eagle Ford, Utica) |
| **Key differentiator** | **Refining cushions** oil-price swings → **lower torque** | **Very long reserve life**, WCS differential exposure | **Highest returns + fortress balance sheet + high torque** |
| **Return style** | **Dividend aristocrat** (42+ yrs of raises) | **Dividend growth** (~24 yrs, high yield) | **Buybacks + growing base div + specials** |
| **Currency for you (CAD investor)** | USD | **CAD-linked** (natural home-currency match) | USD |

**Does EOG fill a gap or overlap?**
- **vs XOM:** genuine gap. XOM's **refining + chemicals + LNG** make it a *lower-torque, defensive
  integrated* — its downstream *earns more when crude is cheap*, damping the swings. EOG has **no
  such cushion** — it's pure upstream. So EOG adds **more direct oil-price upside/torque** than XOM
  gives you. **Complementary.** (VERIFIED: XOM beta-to-WTI 0.30 vs EOG 0.40, §2c.)
- **vs CNQ:** partial gap. Both are pure E&Ps, so on the "pure upstream torque" axis they *overlap*.
  But the **asset is opposite**: CNQ = **long-life heavy oil sands** (decades of low-decline WCS
  barrels, Canada, CAD); EOG = **short-cycle US light shale** (WTI, fast decline, constant re-drill).
  So EOG adds **US light-oil + short-cycle** exposure that CNQ (Canada/heavy/long-life) doesn't, and
  vice-versa. **Complementary on geography/oil-type/cycle; overlapping on "it's still an E&P price-
  taker."**

**Net:** on the *business* axes EOG is the distinct **"US light-shale, short-cycle, high-return,
buyback"** leg — a real third flavour, not a clone. The overlap lives at the *commodity* level (§2c).

---

## 2. Head-to-head comparison table (live yfinance, as-of 2026-07-05)

### 2a. Valuation

| Metric | **EOG** | **XOM** | **CNQ** | Read |
|---|--:|--:|--:|---|
| Price | $130.78 | $137.09 | $39.64 | (CNQ = NYSE line, quoted USD) |
| Market cap | $69.7B | **$568B** | $82.7B | XOM ~7× the others |
| Enterprise value | $74.1B | $614B | $102B | |
| **EV/EBITDA** | **5.9×** | 11.0× | 6.9× | **EOG cheapest**; XOM's 11× reflects lower-margin downstream in the mix |
| Trailing P/E | 12.9× | 23.1× | 11.8× | **CNQ + EOG cheap; XOM optically dear** (earnings down −43% YoY) |
| Forward P/E | 8.8× | 12.7× | 10.9× | EOG cheapest fwd too |
| **FCF yield (TTM)** | 4.1% | 2.0% | **6.5%** | **CNQ highest** (yfinance TTM FCF); see note ‡ |
| Price/Book | 2.26× | 2.21× | 2.63× | All similar; CNQ slight premium (high ROE) |

‡ **FCF-yield note (VERIFIED live + carried filing):** yfinance TTM FCF gives EOG **4.1%**, but EOG's
own guided 2026 FCF (~$4.5B at strip) is a **~6.5% yield** on the same cap (see `deep_dive.md` §2c) —
the gap is because yfinance's TTM FCF ($2.9B) is depressed by 2025's soft quarters and Utica-deal
capex. Use ~6% as EOG's mid-cycle FCF yield. XOM's low 2.0% is TTM FCF ÷ its huge cap after heavy
capex + the Pioneer deal. **Directionally: all three throw off mid-single-digit-plus FCF yields — the
cheap-energy sweet-spot from `sector_trends.md` shows up in all three.**

### 2b. Quality & balance sheet

| Metric | **EOG** | **XOM** | **CNQ** | Read |
|---|--:|--:|--:|---|
| **ROE** | 18.2% | 9.9% | **22.8%** | **CNQ highest**, EOG close 2nd, XOM lowest (downstream dilutes returns) |
| ROA | 9.0% | 4.2% | 5.0% | **EOG far highest** — capital-efficient |
| Debt/Equity | **26.9%** | 18.3% | 44.9% | XOM lowest ratio (huge equity base); **CNQ most levered** |
| Total debt | $8.3B | $47.7B | $20.0B | |
| Cash | $3.8B | $8.4B | $0.8B | **CNQ runs almost no cash** (returns it all) |
| **Net debt** | **~$4.5B** | ~$39B | ~$19.2B | EOG **lowest net debt** of the three |
| Net-debt/EBITDA | **~0.36×** | ~0.70× | ~1.3× | **EOG cleanest; CNQ most levered** to EBITDA |
| Op. margin | 37.9% | 6.4% | 21.8% | XOM's low margin = big low-margin refining revenue |
| **Breakeven oil (WTI)** | **~sub-$50** | ~$35 corporate (integrated) | **~$40–45** | All low-breakeven survivors; see note § |

§ **Breakeven marks — mixed confidence.** EOG **~sub-$50 WTI** (UNVERIFIED, EOG investor framing, see
`deep_dive.md`). XOM ~$35 and CNQ ~$40–45 are **UNVERIFIED / secondary industry framing** — XOM's
integrated breakeven is structurally low because downstream earns in a crude trough; CNQ's oil-sands
breakeven is low on an *operating* basis (long-life assets, sunk capital) but the WCS **differential**
raises its *realized* breakeven vs WTI. **Confirm each against filings before sizing.** Directionally:
**all three survive a deep oil trough** — none is a leveraged wildcatter.

### 2c. Capital return & oil-price torque (VERIFIED live)

| Metric | **EOG** | **XOM** | **CNQ** | Read |
|---|--:|--:|--:|---|
| Dividend yield (regular) | 3.12% | 3.01% | **4.44%** | **CNQ highest raw yield** |
| Div-growth style | Base +8%/yr **+ specials** | **Aristocrat**, steady +5%/yr, 42+ yrs | **~24 yrs of raises**, high grower |
| Payout ratio | 39% | 68% | 46% | **EOG lowest payout** = most room + most protected |
| Buyback (share-count Δ, 2021→2026) | **−9.0%** (585→533M) | −2.7% (4261→4145M) | flat* | **EOG most aggressive buyback** |
| **Total shareholder yield** (div+buyback+specials) | **~6–7%** | ~5% | ~6–7% | EOG & CNQ highest; all strong |
| **Beta-to-WTI** (3y weekly) | **0.40** | **0.30** | **0.42** | **CNQ & EOG most torque; XOM least** |
| Correlation-to-WTI (3y weekly) | 0.59 | 0.51 | 0.59 | EOG/CNQ move most tightly with oil |
| Reported beta (mkt) | 0.26 | 0.16 | 0.88 | CNQ's higher mkt beta partly = FX/Canada factor |
| **Reserve life** | short-cycle, ~**deep multi-yr** premium inventory (5.5 Bboe, 254% replacement) | very long (global) | **very long** (oil sands, decades) | EOG shortest-cycle, CNQ/XOM longest-life |
| Oil-vs-gas mix | ~39% oil, rest gas/NGL | diversified + big gas/LNG | **heavy-oil weighted** | |
| Geography | **US onshore** | Global | **Canada** (+intl) | |

\* CNQ share count *rose* 2024 only because of a **2:1 stock split (June 2024)** — VERIFIED (yfinance
splits). On a split-adjusted basis CNQ **buys back** steadily; do not misread the raw count.

**The torque takeaway (VERIFIED):** rank by oil-price sensitivity is **CNQ ≈ EOG (~0.40 beta-to-WTI)
> XOM (0.30).** So **EOG adds torque relative to XOM** (more oil upside *and* downside), but adds
**little torque beyond what CNQ already gives you** — on the pure "leverage to oil" axis, **EOG and
CNQ are similar.** Where EOG differs from CNQ is *quality/geography/cycle*, not *torque*.

---

## 3. The diversification question — additive or redundant?

**Short answer: additive on business-mix and quality, only mildly additive on risk (correlations are
high).** Detail:

**(a) Correlation — the honest test (VERIFIED, yfinance 3y weekly returns):**
```
        EOG    XOM    CNQ
EOG    1.00   0.79   0.76
XOM    0.79   1.00   0.69
CNQ    0.76   0.69   1.00
```
These are **high** correlations. Adding EOG to an XOM+CNQ core is **NOT** like adding an uncorrelated
asset class — all three are driven by the same oil price, so a third name **does not meaningfully cut
the sleeve's volatility.** What it *does* do is **improve the blend** (see (b)/(c)). **Interpretation:
within-sector "diversification" here = better mix and factor balance, not lower correlation.**

**(b) Does EOG improve the sleeve's QUALITY/VALUATION blend?**
- **Quality: yes, additive.** EOG brings the **cleanest balance sheet** (net-debt/EBITDA ~0.36× vs
  CNQ ~1.3×, XOM ~0.70×) and near-top ROE (18.2%). Adding EOG **de-risks the sleeve's leverage
  profile** — it pulls the blended balance sheet toward "fortress." (VERIFIED.)
- **Valuation: modestly additive.** EOG is the **cheapest on EV/EBITDA (5.9×)** and forward P/E
  (8.8×). Adding it *lowers* the sleeve's blended EV/EBITDA vs XOM's 11.0×. (VERIFIED.)
- **So EOG improves both the quality and the cheapness of the blend** — it's the high-ROE, low-debt,
  low-multiple leg.

**(c) Does the trio over-index to any single factor?**
- **Oil price:** YES — obviously; that's the shared master-risk. Three O&G names = a **concentrated
  bet on oil/gas prices staying firm.** (This is the 12%-weight point, §4.)
- **Currency:** XOM + EOG are **USD**; CNQ is **CAD-linked** (financials in CAD; the NYSE line embeds
  USD/CAD 1.42). For **you as a Canadian**, CNQ is the **natural home-currency match** — CAD strength
  helps CNQ's USD-quoted value and matches your spending currency. Adding EOG (USD) tilts the sleeve
  *further* toward USD. Not a big issue at these weights, but note it: a two-USD-one-CAD trio is
  slightly USD-heavy for a CAD investor. (VERIFIED currencies; ASSUMED interpretation.)
- **Oil type:** EOG (light) + XOM (diversified) + CNQ (heavy) is actually **well-balanced** across the
  crude-quality spectrum — a mild *positive*. The WCS-differential risk sits only in CNQ.
- **Cycle length:** EOG (short) + XOM/CNQ (long-life) balances short- vs long-cycle. Also a positive.

**Verdict on diversification:** EOG is **additive to the *composition*** of the sleeve (adds US
light-shale, short-cycle, best-quality/lowest-debt, buyback style; balances oil-type and cycle) but is
only **weakly additive to *risk reduction*** because all three ride the same oil-price factor
(correlations 0.69–0.79). **It makes a better O&G sleeve; it does not make the sleeve safe against an
oil drawdown.**

---

## 4. The 12%-weight overlay — the decision framework (research, not advice)

**~12% in one sector is already a full-to-heavy allocation.** For reference, energy is only ~3–4% of
global equity market cap; a 12% weight is a **~3–4× overweight** — a deliberate, sizeable *sector bet*.
So there are really **two separate questions**, and it's worth not conflating them:

> **Q1 (allocation): Should the O&G sleeve grow beyond ~12% at all?**
> **Q2 (selection): If you want EOG, is it a good name / the right flavour?**

The two EOG files answer Q2: **yes, EOG is the highest-quality large US E&P, at a reasonable (not
fire-sale) price, 6.9/10, WATCH→lean-buy** — its merit as a *name* is established. This file's job is
Q1 and the **ADD-vs-SWAP** structure:

### Framing A — ADD (sleeve grows past 12%)
- **What it means:** buy EOG *on top of* XOM+CNQ → O&G rises to ~13–14%+.
- **When it makes sense:** if you are **deliberately bullish on oil/gas** (the `sector_trends.md`
  supply-underinvestment thesis) and *want* a bigger, more concentrated energy bet, and are
  comfortable that 3 correlated names (ρ≈0.7–0.8) means a bigger *single-factor* bet on oil.
- **The cost:** concentrates further into one factor. A drawdown to $50–55 WTI hits all three
  together (§3a). You'd be *increasing* a bet that's already ~3–4× market weight.

### Framing B — SWAP (sleeve stays ~12%, EOG funded by a trim)
- **What it means:** trim XOM and/or CNQ to fund EOG → O&G stays ~12%, but the *internal mix* improves.
- **When it makes sense:** if you're happy with 12% energy but want a **higher-quality, cheaper,
  better-balanced sleeve.** Two natural swaps:
  - **Trim XOM → EOG:** moves from lower-torque/lower-ROE integrated to higher-torque/higher-ROE
    pure-play. *Increases* the sleeve's oil sensitivity and quality; *reduces* the refining cushion.
    Do this if you want **more oil upside + a cleaner balance sheet** and think XOM's 23× trailing
    P/E / 11× EV/EBITDA is expensive vs EOG's 5.9×. (Cost: you give up XOM's defensive downstream
    cushion and 42-yr aristocrat dividend.)
  - **Trim CNQ → EOG:** swaps **Canada/heavy/long-life/CAD** for **US/light/short-cycle/USD**. Similar
    torque (both ~0.40 beta-to-WTI), but you trade **CNQ's higher yield (4.4%) + CAD match + long
    reserve life** for **EOG's cleaner balance sheet (0.36× vs 1.3× net-debt/EBITDA) + buybacks +
    US-shale geography.** Do this if you want to **cut leverage and WCS-differential risk** and are OK
    with more USD and shorter-cycle inventory. (Cost: less yield, less CAD hedge, more re-drill
    dependence.)

**Which framing?** That is **your call** (research, not advice). The decision rule:
- If your view is **"I want more energy"** → Framing A (ADD).
- If your view is **"12% is enough energy, but I want a better sleeve"** → Framing B (SWAP), and the
  swap target depends on what you want to trade *away* (XOM's cushion, or CNQ's yield/CAD/long-life).

---

## 5. Verdict

**EOG is ADDITIVE, not redundant, to an XOM+CNQ core — but "additive" here means it improves the
*composition and quality* of the O&G sleeve, not that it diversifies away the sleeve's dominant risk
(the oil price).**

- **Distinct role EOG plays:** the **US light-oil, short-cycle shale, best-quality (highest ROA,
  lowest net debt), buyback-heavy, high-torque** leg. XOM is the *defensive integrated* (refining
  cushion, aristocrat dividend, least oil torque); CNQ is the *long-life heavy-oil-sands* leg (highest
  ROE + yield, CAD-linked, but most levered and carries WCS-differential risk). **EOG genuinely fills
  the gap between them** — it is the *quality-pure-play* that neither the integrated nor the oil-sands
  name gives you.
- **Where it overlaps:** on **oil-price torque it duplicates CNQ** (both ~0.40 beta-to-WTI) — EOG's
  torque premium is mainly *vs XOM*, not vs CNQ. And all three share the master-risk: correlations
  0.69–0.79.
- **Add vs swap (given the 12% weight):** because 12% is **already a full/heavy sector bet**, the
  cleaner question is likely **SWAP, not ADD** — fund EOG by trimming XOM (to gain torque + quality +
  cheapness, give up the downstream cushion) or CNQ (to cut leverage + WCS risk, give up yield + CAD
  match). **ADD only if you're deliberately raising your oil-price bet.** This is your allocation call
  — research, not advice.
- **What to watch (same top risk as the deep-dive):** the **oil price** dominates all three; a move to
  $50–55 WTI draws them down together, so a third O&G name raises single-factor concentration. Watch
  also: CNQ's **WCS differential**, XOM's **refining margins**, EOG's **capital discipline / Utica
  type-curves**, and — for you — **USD/CAD** (a two-USD-one-CAD trio is mildly USD-heavy for a Canadian).

> **⚠️ To finalize, I still need your full O&G holdings table (all tickers + %).** With only XOM+CNQ
> confirmed I've characterized the *core* and built the framework, but I cannot compute the *whole
> sleeve's* concentration, correlation matrix, or factor tilt until the rest arrives. Send it and I'll
> slot every name into §2–§3 and give you the sleeve-level verdict.

---

## Verification log
- **VERIFIED live (yfinance 2026-07-05):** all prices, market caps, EV, EV/EBITDA, P/E (t/f), P/B, ROE,
  ROA, D/E, debt, cash, dividend yields, payout ratios, margins, share-count history (buyback proxy),
  dividend history, **3y weekly return correlations (EOG-XOM 0.79 / EOG-CNQ 0.76 / XOM-CNQ 0.69)**,
  **beta-to-WTI (EOG 0.40 / XOM 0.30 / CNQ 0.42)**, WTI $68.78 / Brent $72.13 / Henry Hub $3.24 /
  USD-CAD 1.42, CNQ 2:1 split June-2024.
- **Carried from EDGAR-verified EOG files:** EOG net debt ~$4.5B, ROE 18.2%, breakeven ~sub-$50,
  reserves 5.5 Bboe / 254% replacement, 100%-of-FCF return, guided ~6.5% FCF yield. (See `deep_dive.md`
  / `profile_and_diligence.md`.)
- **UNVERIFIED / to confirm before sizing:** XOM (~$35) and CNQ (~$40–45) corporate breakevens
  (secondary industry framing); XOM's dividend-aristocrat streak length (42+ yrs) and CNQ's dividend-
  raise streak (~24 yrs) — both widely reported, not primary-verified this session; per-peer reserve-
  life exact years; total-shareholder-yield figures (ASSUMED from div + observed buyback).
- **Data caveats:** yfinance CNQ is the **NYSE line** (quoted USD, financials CAD) — beta/currency
  reflect that; the TSX line (CNQ.TO, pure CAD) would differ on FX. yfinance TTM FCF understates EOG's
  mid-cycle FCF (see note ‡). Correlations are 3y weekly — a different window would shift them modestly
  but the "high, 0.7–0.8" conclusion is robust.
- **LIMITATION (repeated):** full O&G holdings list did **not** arrive — only XOM + CNQ named. Analysis
  is complete for the core three; sleeve-level finalization pending the full table.
- **NOT financial advice — research to inform Hooman's own decision.**
