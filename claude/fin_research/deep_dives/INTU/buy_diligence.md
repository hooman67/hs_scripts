# INTU — Intuit Inc. — Buy Diligence & Fair-Value Analysis

**Ticker:** INTU (Nasdaq Global Select Market, symbol INTU, $0.01 par — VERIFIED, 8-K 2026-06-11)
**Purpose:** buy-oriented due diligence for a value/quality-first investor (Hooman, Canadian citizen) who likes the name and wants to buy. Builds on `deep_dive.md` (thesis/score 7.65) and `profile_and_diligence.md` (business primer + EDGAR tie-out) — **does not repeat them**. This file delivers the one open item they deferred: **a proper, transparent fair-value analysis**, plus the buy-decision framing.
**Author:** Claude (Opus 4.8) for Hooman Shariati · **Date:** 2026-07-05
**Fiscal year ends July 31** (FY2026 ends Jul-31-2026; Q4/FY26 results land ~late-Aug-2026 — not yet reported as of this file).

> **NOT financial advice** — research to inform Hooman's own decision (CLAUDE.md §5). Every number is marked **VERIFIED** (EDGAR primary or ≥2 agreeing live feeds) / **ASSUMED** (my model/derivation — the fair-value range is a MODEL, not a fact) / **UNVERIFIED** (flagged, not relied on).

---

## 0. TL;DR — the buy-readiness view

- **Current price ~$275** (VERIFIED, yfinance 2026-07-05, $275.35; prior close $267). Market cap ~$75.3B, 273.5M shares.
- **Triangulated fair value (ASSUMED, my model): ~$290 (bear) / ~$380–420 (base) / ~$520 (bull).** Base midpoint ~$400 = **~+45% upside**; the price sits at/just above the **bear** case.
- **What the current price implies (reverse-DCF, VERIFIED inputs / ASSUMED model):** on an honest, stock-comp-adjusted owner-FCF basis, **$275 prices in roughly 0% long-term FCF growth** — i.e. the market is valuing a mid-teens grower as a **no-growth cash cow**. That is the whole opportunity *and* the whole risk: it's cheap only if FCF does not actually go to zero-growth.
- **Verdict: BUY-able now for a quality-first investor who accepts higher variance — but scale in / keep a starter size, because the AI overhang is a real (if segment-confined) tail.** This is a **fallen-angel barbell, not a sleeper.** A patient buyer can start now and add on the two data prints that resolve the debate.
- **Trap-vs-bargain hinges on ONE judgment call:** does AI gut TurboTax (and eventually QuickBooks), or is it an upsell channel Intuit controls? The theme agent's answer: **more overreaction than trap, with the trap tail confined to ~25% of the business (TurboTax).** Signals to watch (below): **TurboTax paid units in the 2027 tax season + QuickBooks Online growth each quarter.**
- **Easily buyable for a Canadian:** yes — Nasdaq-listed, trades in USD, available on **both Schwab and Questrade** with no special access. US-dividend withholding note in §5.

---

## 1. VALUATION / FAIR-VALUE ANALYSIS (the deferred open item)

### 1a. The verified anchors (what the model is built on)

| Input | Value | Confidence |
|---|---|---|
| Price (2026-07-05) | **$275.35** | VERIFIED (yfinance; prior close $267.08) |
| Shares outstanding | **273.5M** | VERIFIED (EDGAR dei, 2026-05-14) |
| Market cap | **~$75.3B** | VERIFIED (price × shares) |
| FY2026 revenue guide | **$21.341B – $21.374B** (+13–14%) | **VERIFIED** (EDGAR Q3-FY26 press-release exhibit, acc 0000896878-26-000024) — *matches the brief's $21.34–21.37B* |
| FY2026 GAAP diluted EPS guide | **$15.79 – $15.84** (+16%) | **VERIFIED** (same exhibit) |
| FY2026 **non-GAAP** diluted EPS guide | **$23.80 – $23.85** (+18%) | **VERIFIED** (same exhibit) — *matches the brief's $23.80–23.85* |
| TTM FCF (owner, gross) | **~$6.8B** (OCF $6.2B FY25; 9-mo FY26 OCF $7.51B, capex $0.15B) | VERIFIED components; TTM ~$6.8B ASSUMED |
| Net debt | **~$1.5B** (post the June-2026 note issuance — see §3) | VERIFIED components |
| WACC / terminal growth | 9% / 3.5% | ASSUMED (standard for a wide-moat, asset-light compounder) |

**Jargon, plain-English:**
- **FCF (free cash flow)** = cash the business throws off after keeping the lights on (operating cash minus capex). INTU is asset-light, so FCF ≈ operating cash flow.
- **FCF yield** = FCF ÷ market cap. INTU's is **~9%** on gross FCF — high for a compounder; a bond-like ~9% cash return says the market expects little growth (or lots of risk).
- **Reverse-DCF** = instead of guessing growth and computing a value, you take today's *price* as given and solve for the growth rate the market is implicitly paying for. It answers "what do I have to believe to justify $275?"
- **P/E** = price ÷ earnings per share. **Forward P/E** uses next-year expected earnings. "Non-GAAP" strips out stock-comp and amortization; "GAAP" is the audited bottom line.
- **Rule-of-40** = a SaaS health test: revenue-growth% + profit-margin% ≥ 40 is "healthy." INTU passes (~13–14% growth + ~30% FCF margin ≈ 43–47%).
- **SBC (stock-based compensation)** = paying employees in shares. It's a *real* cost (it dilutes you), even though it doesn't leave the bank account — so gross FCF flatters the picture; I adjust for it below.

### 1b. Reverse-DCF — what growth is baked into $275?

Two honest anchors, because the answer swings on how you treat stock comp:

| FCF anchor | Implied yr-1-to-5 FCF growth priced into $275 | Read |
|---|---|---|
| **Gross reported FCF ~$6.8B** | **~−5%/yr (declining)** | On raw FCF, the market is pricing FCF to *shrink*. Looks absurdly cheap. |
| **SBC-adjusted owner-FCF ~$5.0B** *(FCF minus ~$2B/yr stock comp)* | **~0%/yr (flat forever)** | On honest owner earnings, the market prices a **no-growth cash cow**. |

*(My reverse-DCF, WACC 9%, terminal 3.5%; inputs VERIFIED, model ASSUMED.)*

**This is the crux of the whole valuation, and it is the nuance the prior deep dive flagged but did not quantify.** Intuit's ~$2B/yr of stock-based comp is large and real (it dilutes shareholders). If you value the business on *gross* FCF, the DCF looks like a screaming buy (fair value 2–3× the price). If you subtract SBC to get true owner earnings, the picture is far more sober: **the market is paying for zero long-term growth.** The honest answer sits closer to the SBC-adjusted view. So the correct read is **not** "the DCF says $600–800, it's a 3-bagger" — it is **"the market is pricing INTU as if it will never grow again, which is a low bar for a franchise still guiding +13–14% revenue and +18% non-GAAP EPS."**

### 1c. Fair-value range — two methods, triangulated

**Method A — DCF on SBC-adjusted owner-FCF (~$5.0B), WACC 9%, terminal 3.5%** (the honest DCF):

| Scenario | 5-yr owner-FCF growth | Fair value/share | vs $275 |
|---|---|---|---|
| **Bear** (AI impairs TurboTax, QBO fades) | 2% | **~$310** | +13% |
| **Base** (growth holds mid-single→high-single) | 6–8% | **~$400–440** | +45–60% |
| **Bull** (AI upsell works, growth persists) | 12% | **~$553** | +101% |

**Method B — Multiple on FY2026 non-GAAP EPS ($23.83 mid, VERIFIED):**

| Scenario | Applied P/E | Fair value/share | vs $275 | Rationale |
|---|---|---|---|---|
| **Bear** | 12× | **~$286** | +4% | GARP/cash-cow multiple, no re-rate |
| **Base** | 15–16× | **~$357–381** | +30–38% | re-rate to a market-ish multiple for a durable grower |
| **Base-hi** | 18× | **~$429** | +56% | partial re-rate toward quality |
| **Bull** | 22× | **~$524** | +90% | quality re-rate (still *far* below its 57–70× history) |

*(EPS VERIFIED; multiples ASSUMED. Note current fwd P/E = 11.6× non-GAAP / 17.4× GAAP.)*

**Triangulated fair-value range (ASSUMED — this is a model, not a fact):**

> ### **Bear ~$290  ·  Base ~$380–420  ·  Bull ~$520**
> **Base-case midpoint ~$400 → ~+45% from $275.**

The two methods **converge**, which raises confidence: the honest-DCF base (~$400–440) and the multiple base (~$357–429) overlap around **$380–430**. The bear cases also converge (~$286–310), sitting **right at today's price** — meaning the downside from here is *modest re-rating risk*, not a cliff, **unless** the fundamentals actually deteriorate (the AI tail). The bull cases (~$520–553) require only a partial re-rate to ~20× on a franchise that historically traded 57–70×.

### 1d. Downside vs upside, framed for a buyer

- **Downside (bear realized — AI impairs TurboTax + slows QBO):** fair value ~$286–310, i.e. **roughly flat-to-slightly-up from $275**. The bear case is *"cheap gets no cheaper, but you make little."* A *deeper* bear (net FCF actually shrinks, multiple stays 12×, EPS misses) could take it to ~$230–250 — the 52-week low was $252.84. So realistic downside ≈ **−10% to flat**; the "price already reflects the bad news" is largely true.
- **Upside (bull — growth holds, AI monetizes at the top):** ~$520 (+90%), and that is *conservative* vs a franchise that spent 2021–25 at 57–70× P/E. Consensus PT is ~$487 (VERIFIED, yfinance targetMean; range $275–921).
- **Asymmetry:** ~−10%/flat downside vs ~+45% base / +90% bull. **The skew is favorable** — this is why the name screens as the most asymmetric idea in the run. The catch: the *probability* on the bear tail is genuinely uncertain (it's an AI judgment call), so size accordingly.

---

## 2. BUY-RELEVANT OPEN ITEMS — resolved & cross-checked vs EDGAR (CIK 0000896878)

### 2a. Two-segment reporting — CONFIRMED

Effective **Aug 1, 2025**, Intuit collapsed from four reportable segments to **two** (VERIFIED, 10-Q Note 12, period 2026-04-30):

| New segment (FY2026) | Contains | Q3-FY26 revenue | YoY | FY26 guided growth |
|---|---|---|---|---|
| **Global Business Solutions (GBS)** | QuickBooks + payments + payroll + capital + Mailchimp | **$3,285M** | **+15%** | **~16% (raised)** |
| **Consumer** | TurboTax **+ Credit Karma + ProTax** (merged in) | **$5,273M** | **+8%** | **~10% (raised)** |
| **Total** | | **$8,558M** | **+10%** | +13–14% |

*(Segment revenue & structure: VERIFIED, 10-Q. FY26 segment guidance: VERIFIED, press-release exhibit — Consumer ~10% includes TurboTax ~7%, Credit Karma ~19%, ProTax ~4%.)* The old 4-way (GBS/Consumer/Credit Karma/ProTax) remains the right *mental model*; Credit Karma + ProTax are now just reported inside Consumer.

### 2b. The AI-deflation signals to watch — latest quarter (Q3-FY26, reported 2026-05-20) — VERIFIED

- **TurboTax:** revenue $4.4B **+7%**, BUT **Online paying units +~2%**, **total units −~2%**, **ARPU +~11%**, **e-file share −~1pt**. → *Growth is price/mix, not volume; the price-sensitive low-end DIY filer is walking.* This is the single hard, reported instance of AI-adjacent price/volume pressure — the trigger for the crash. **The signal to watch.**
- **TurboTax Live (AI-monetization-at-the-top):** revenue **+36% to $2.8B (~53% of TurboTax revenue)**; Live customers **+38%**. → AI is *demonstrably* upselling to assisted tiers, not (yet) causing churn.
- **QuickBooks / Online Ecosystem (the crown jewel):** **Online Ecosystem $2.5B, +19%** (ex-Mailchimp +22%); mid-market "growing north of 30%." **No AI damage visible here** — this is the leg the bear case has *not* dented. **The other signal to watch.**

### 2c. Capital return — shareholder yield quantified — VERIFIED

| Item | Figure | Source |
|---|---|---|
| **New buyback authorization** | **$8.0B** (Board-approved, announced 2026-05-20) | VERIFIED (press-release exhibit) — **= ~10.6% of market cap** (multi-year) |
| Buybacks, 9-mo FY26 | **$3,341M** (annualizes to ~$4.45B) | VERIFIED (EDGAR PaymentsForRepurchase) |
| Buybacks, FY25 full year | $2,772M | VERIFIED |
| **Dividend** | **$1.20/qtr = $4.80/yr** (payable Jul-17-2026); **+15.4% raise effective Aug-2025** (from $1.04) | VERIFIED (EDGAR DividendsDeclared + press release) |
| **Dividend yield** | **~1.74%** (payout ~20% of non-GAAP EPS — very safe) | VERIFIED |
| **Buyback yield** (annualized 9-mo pace / mkt cap) | **~5.9%** | derived (VERIFIED inputs) |
| **Total shareholder yield** | **~7.7%** | derived |

*(Note on the brief's "div flat at last print": the $1.20 declared on 2026-05-20 was NOT a new raise — the +15% hike to $1.20 happened in Aug-2025. So the dividend is flat *quarter-on-quarter* but +15% *year-on-year*. VERIFIED.)*

**Shareholder yield** = dividends + net buybacks, as a % of market cap = the total cash returned to owners. At **~7.7%**, INTU is handing back a bond-like cash return *while still growing* — and management is leaning INTO the 66% drawdown with the $8B authorization. That is either a strong conviction signal or a bet that destroys value if the franchise is impaired (the bear's read). Either way, buybacks at 11–17× earnings are far more accretive than the 57–70× the company bought back at historically.

### 2d. Balance sheet / leverage — CONFIRMED, with a fresh update

- **Pre-June-2026:** cash $4.68B, debt $6.16B → **net debt ~$1.5B** (VERIFIED, 10-Q 2026-04-30). Essentially net-neutral.
- **NEW (VERIFIED, 8-K 2026-06-11):** Intuit **issued $1.75B of senior notes** — $750M at 4.950% due 2031 + $1.0B at 5.500% due 2036, net proceeds ~$1.74B — "for general corporate purposes, which may include refinancing" the $750M 5.250% notes due 2026 and $500M 1.350% notes due 2027. → **Mostly a refinancing** (~$1.25B rolled forward); net *incremental* debt only ~$0.5B, and it terms-out near-term maturities at reasonable investment-grade rates. Supports the buyback. Leverage remains very low (net debt / EBITDA well under 0.5×). **Not a concern.** The fact that BofA/JPM/Scotia underwrote it at IG rates is a mild credibility tell that lenders don't see a broken franchise.

---

## 3. THE AI QUESTION — buy-decision framed (synthesizing the theme agent, not re-deriving)

The theme agent's verdict (`screens/theme_ai_deflation.md`): **software = more overreaction than trap; Intuit can reprice AI as "work done"; the trap tail is confined to ~25% of the business (TurboTax); the crown jewel (QuickBooks/GBS) shows no damage.** I take that as given. Framed as a buy decision:

### What would have to be TRUE for INTU to be a VALUE TRAP (avoid / it gets cheaper):
1. **TurboTax unit erosion *accelerates*** past −2% AND ARPU can no longer offset → net TurboTax revenue turns **negative**, not just slow. (Confirms "AI + free-tier competitors commoditize DIY tax.")
2. **QuickBooks Online growth decelerates below ~10%.** This is the crown jewel; AI-native bookkeeping (e.g. Basis) validated on the most important asset would break the base-case FCF assumption. *No sign of this yet (+19%).*
3. A **filed securities class action** with genuinely adverse disclosures (currently only investigations — no complaint located).
> If (1)+(2) both hit, the SBC-adjusted DCF's ~0% growth becomes *negative* growth, fair value falls toward ~$230–260, and "cheap" was a trap.

### What would have to be TRUE for INTU to be a BARGAIN (buy / re-rates up):
1. **TurboTax units stabilize** (stop declining) even as ARPU/Live keep growing → the crack was a one-season price mistake, not a structural break.
2. **QuickBooks/GBS holds +15%+** and mid-market keeps compounding >30% → the moat is intact; AI is a tailwind (upsell) not a headwind.
3. **FY27 guidance (Aug-2026) holds** double-digit revenue + high-teens EPS → refutes the "franchise broken" thesis → re-rate off ~11× forward.
> If these hold, the market's implied ~0% growth is simply wrong, and fair value is $380–520 (+40% to +90%).

### Near-term data that confirms each (the "form a view before sizing" answer):
| Print | Date | What resolves the debate |
|---|---|---|
| **Q4/FY26 results + FIRST FY27 guidance** | **~late-Aug 2026** (next print) | Does GBS stay +15%+? Does the FY27 guide imply TurboTax stabilizing? First read on whether the layoff/restructuring is protecting margins. **The nearest catalyst — ~6-8 weeks out.** |
| **Q1–Q2 FY27** (QBO growth) | Nov-2026, Feb-2027 | QuickBooks Online Ecosystem YoY each quarter — the crown-jewel tell. Below ~10% = bear. |
| **2027 tax season (fiscal Q3-FY27)** | **~May-2027** | **The single most important signal.** TurboTax paid-unit trajectory: worse than −2% = bear hardening; stabilizing = bull confirmed. |

**My buy-framing read:** the bear needs BOTH flagships to break; so far only *one segment's low-end* has cracked, and the crown jewel is accelerating. The base rate (data-rich, workflow-embedded incumbents adapt to platform shifts) plus the demonstrated AI-upsell (TT Live +36%, QB Live doubling) tilts this **toward bargain, not trap — but it is genuinely contested and one AI judgment call swings it.** That justifies buying, at a size that respects the tail.

---

## 4. WHERE INTU SITS ON THE SCORECARD (unchanged from deep_dive.md — 7.65/10)

The valuation work here **confirms** the existing scorecard rather than moving it: genuinely cheap (base FV ~+45%, bear ~flat = favorable skew), elite quality, real-but-segment-confined trap risk. No re-score warranted. The one refinement: the "DCF says 2–3× the price" framing in `deep_dive.md` §2d is **too generous** — on SBC-adjusted owner earnings the honest fair value is **~$290–520**, not $560–800. The bull case is still large; it just isn't a guaranteed 3-bagger.

---

## 5. PRACTICAL BUY NOTES FOR A CANADIAN

- **Buyable? Yes, trivially.** INTU is a **Nasdaq-listed US common stock (symbol INTU, USD-denominated)** — VERIFIED from the 8-K cover page ("Common Stock, $0.01 par value, INTU, Nasdaq Global Select Market"). It is a large, liquid S&P-500 / Nasdaq-100 name.
  - **Schwab:** fully supported — standard US-listed equity, no special access, trades in USD. (Confirmed as a matter of course; Schwab is a US broker and INTU is a core US listing.)
  - **Questrade (Canadian broker):** fully supported — Questrade offers US-listed equities in USD accounts. Hold it in a **USD account** to avoid round-trip FX conversion on the trade and on dividends. (Well-established Questrade capability; confirm the specific USD-account setting at order time.)
  - *Confidence: VERIFIED that it's a plain Nasdaq USD common; ASSUMED-obvious that both brokers list it — any US-equity-capable broker does. No ADR, no foreign-listing friction.*
- **Currency:** priced and paid in **USD**. A Canadian holder carries USD/CAD FX exposure on both price and dividends — a USD account avoids repeated conversion costs.
- **US dividend withholding (general FYI only — NOT tax advice):**
  - The US generally withholds **15%** on dividends paid to a Canadian resident under the **Canada–US tax treaty**, provided you've filed a **W-8BEN** with your broker (Schwab/Questrade collect this; without it the default is 30%).
  - **In an RRSP**, the treaty exempts the withholding — US dividends in an RRSP are generally **not** subject to the 15% (a specific RRSP carve-out). In a **TFSA or non-registered/cash account**, the 15% **does** apply (and in a TFSA it is **not** recoverable via foreign-tax credit, since TFSA income isn't taxed in Canada — a small drag). In a non-registered account the 15% is generally creditable against Canadian tax via the foreign-tax credit.
  - **Bottom line for INTU specifically:** the dividend is small (**~1.7% yield, ~20% payout**) — this is a *total-return/quality* name, not an income name, so withholding mechanics are a minor consideration. If held long-term, put it in an **RRSP** to sidestep the withholding entirely, or a taxable account (creditable); a TFSA is the least tax-efficient home for a US dividend payer but the drag on a 1.7% yield is tiny (~0.26%/yr).
  - *Confirm specifics with a cross-border tax advisor — this is general information, marked UNVERIFIED as to your personal situation.*

---

## 6. BUY-DD VERDICT

**Is INTU a buy at ~$275 for a quality-first investor? YES — buyable now, as a scaled/starter position, with adds gated on the next two prints.**

- **Fair-value range (ASSUMED model):** **Bear ~$290 · Base ~$380–420 · Bull ~$520.** Base midpoint ~$400 = **~+45%**; the price is sitting at the **bear** case, so you're buying with the bad news already largely in the price.
- **What the price implies (VERIFIED inputs):** on honest, SBC-adjusted owner earnings, **~0% long-term growth** — the market prices a mid-teens grower as a no-growth cash cow. Low bar to beat.
- **Bull:** AI monetizes at the top (TT Live +36%, QB Live doubling), GBS holds +15%+, FY27 guide confirms the franchise → re-rate off 11× forward toward 16–20× = +40% to +90%.
- **Bear:** AI + free-tier competition impair TurboTax volume *and* AI-native bookkeeping dents QuickBooks → net FCF shrinks, no re-rate → ~flat to −10%, worst realistic case ~$230–250.
- **Trap-vs-bargain:** leans **bargain** (overreaction), because the bear needs *both* flagships to break and only one segment's *low end* has cracked while the crown jewel accelerates — but it's **contested**, hinging on a single AI judgment call.

### Entry / sizing considerations (it's higher-variance)
1. **Size it as a barbell, not a core anchor** — the AI overhang makes the outcome distribution wide. A **starter position now (say ~⅓–½ of a full weight)**, with adds gated on (a) the Aug-2026 FY27 guide and (b) the May-2027 tax season, lets you buy the confirmation without missing the entry. *(Sizing framing, not a recommendation.)*
2. **You are buying at the bear case** — the favorable part of the skew. Waiting for a deeper pullback risks the re-rate happening on the Aug-2026 guide; the margin of safety already exists at $275.
3. **Volatility is high** — the stock moved ~20% on one print. Expect turbulence; average in rather than chase.
4. **Hold vehicle (Canadian):** RRSP is most tax-efficient for the (small) US dividend; taxable is fine; TFSA is the least efficient but a negligible drag at 1.7% yield.

### What to watch each quarter (falsifiable)
- **QuickBooks / Online Ecosystem YoY** — must hold ≥~10% (currently +19%). *Deceleration below 10% = bear thesis on the crown jewel → reconsider.*
- **TurboTax paid units** — the 2027 season (May-2027) is the decisive tell. *Worse than −2% = trap hardening; stabilizing = bull confirmed.*
- **FY27 guidance (Aug-2026, ~6–8 weeks out)** — the nearest catalyst; must hold double-digit revenue + high-teens EPS.
- **Securities litigation** — watch for a *filed* class action (only investigations so far) and its class period.
- **Buyback execution** — does the $8B authorization keep compounding per-share value at 11–17× earnings (bull) or prove to be catching a falling knife (bear)?

### Confirmation it's easily buyable
**Yes — INTU is a plain Nasdaq (Global Select) USD common stock, available on both Schwab and Questrade with no special access.** Hold in a USD account to avoid FX round-trips; RRSP is the most tax-efficient home for the US dividend.

---

## Source ledger (this file)

- **Live price/multiples (2026-07-05):** yfinance — price $275.35, prior close $267.08, mkt cap $75.32B, shares 273.537M, trailing P/E 16.8, forward P/E 10.1, PEG 0.69, gross margin 80.8%, ROE 22.5%, div rate $4.80 / yield 1.74%, targetMean $486.6 (range $275–921), recommendationKey "buy" — **VERIFIED (live pull)**.
- **SEC EDGAR (CIK 0000896878), UA "Hooman Shariati hshariati@adobe.com":**
  - **Q3-FY26 earnings press-release exhibit** (8-K acc 0000896878-26-000024, `fy26q3earningspressrelease.htm`): FY26 guide **rev $21.341–21.374B, GAAP EPS $15.79–15.84, non-GAAP EPS $23.80–23.85**; segment guide (GBS ~16%, Consumer ~10% [TurboTax ~7%, Credit Karma ~19%, ProTax ~4%]); Q3 TurboTax $4.4B +7% (units −2%, ARPU +11%, Live +36% to $2.8B ≈ 53% of TT rev, Live customers +38%); Online Ecosystem $2.5B +19%; **$8B new buyback authorization**; **$1.20 dividend (+15% YoY), payable Jul-17-2026** — **all VERIFIED**.
  - **8-K 2026-06-11** (acc 0001193125-26-267866): **$1.75B senior notes issued** ($750M 4.950% due 2031 + $1.0B 5.500% due 2036, net ~$1.74B, refinancing $750M 2026 + $500M 2027 notes); cover page confirms **INTU, Nasdaq Global Select Market, $0.01 par** — **VERIFIED**.
  - **XBRL:** PaymentsForRepurchaseOfCommonStock (9-mo FY26 $3,341M; FY25 $2,772M); CommonStockDividendsPerShareDeclared (FY26 $1.20/qtr; FY25 $1.04/qtr) — **VERIFIED**.
  - Balance sheet / segment / FCF / historical: tied out in `profile_and_diligence.md` §B1 (10-K FY2025, 10-Q Q3-FY26) — VERIFIED there.
- **AI-deflation synthesis:** `screens/theme_ai_deflation.md` (2026-07-03) — verdict for INTU: overreaction-leaning, trap tail ~25% (TurboTax), signals = TurboTax units + QBO growth.
- **Valuation model:** my reverse-DCF + multiple triangulation (WACC 9%, terminal 3.5%, SBC-adjusted owner-FCF ~$5.0B and gross FCF ~$6.8B; multiples 12–22× on FY26 non-GAAP EPS $23.83) — **ASSUMED (a model, not a fact)**; VERIFIED inputs as flagged.
- **Canadian buyability / withholding:** Nasdaq USD listing VERIFIED (8-K); broker availability & treaty/RRSP mechanics = general knowledge, **UNVERIFIED as to Hooman's personal situation — confirm with a cross-border tax advisor.**

**Confidence key:** VERIFIED = EDGAR primary or ≥2 agreeing live feeds. ASSUMED = my model/derivation (the fair-value range is a model, NOT a fact). UNVERIFIED = flagged, not relied upon. **Research, not financial advice.**
