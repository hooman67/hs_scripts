# Macro Energy — Verifying Hooman's 3 Oil & Gas Theses (mid-2026)

**Prepared:** 2026-07-07 by Claude (Opus 4.8). Owner: Hooman Shariati (**Canadian citizen**,
quality-first value investor, 3–5yr + 20yr horizon).
**RESEARCH, NOT FINANCIAL ADVICE.** A decision framework and evidence audit — not a recommendation
to buy, sell, or hold.

**Builds on (does NOT repeat):**
- `deep_dives/EOG/sleeve_analysis.md` — the 9-name book, correlations, the OXY→EOG swap logic, "13.8%
  is already ~3–4× market weight."
- `deep_dives/EOG/hooman_oil_gas_holdings.md` — the holdings table + weights.
- `screens/sector_trends.md` — the "Oil & Gas E&P = the single cheapest sweet-spot on the board"
  finding (Damodaran as-of 2026-01-05) **plus its explicit caveats** (2026-27 glut, near-term pain).

This file answers the **macro/thesis layer** those files pointed at but didn't fully resolve: is the
*theme* real, is Canada actually favoured, is the AI-proxy logic sound, and what's a sensible weight.

---

> ## ⚠️ READ FIRST — TWO data-integrity flags that shape everything below
>
> **(1) A "2026 Iran war / Strait of Hormuz closure" narrative contaminated the search results.**
> Multiple aggregators and a Wikipedia article claim a Feb–Jul 2026 Iran war closed Hormuz and spiked
> Brent to ~$119 in March 2026, and IEA/EIA mid-2026 price *assumptions* ($95–$105 Brent) are built on
> it. **I do not trust this as fact**, because every independent live price feed this session shows oil
> trading *calmly* at **WTI ~$69 / Brent ~$72 on 2026-07-06/07** — a genuine, sustained Hormuz closure
> (≈20 mb/d of seaborne flow) is physically incompatible with $69 oil. Most likely the "war" is either
> (a) a brief, already-resolved episode whose premium has fully bled out, or (b) noise/hallucinated
> content in secondary sources. **Treatment:** I use the **~$69 WTI / ~$72 Brent spot as the real
> anchor** (it agrees with our own 2026-07-05 yfinance pull of $68.78/$72.13 in `sleeve_analysis.md`),
> and I treat any $95–$119 figure as **UNVERIFIED / distorted**. This matters: it means the forward
> P/Es below are inflated by crisis-level earnings estimates and the "cheap" read is softer than the
> screens suggested.
>
> **(2) The `sector_trends.md` cheapness data is as-of 2026-01-05 (~6 months stale) and Damodaran's
> annual averages.** The Stage-1a "E&P is the cheapest sweet-spot" finding is a *January* snapshot.
> Energy equities have since **rallied hard** (XLE peaked ~+37% intra-2026, Canadian XEG +44% trailing
> 12mo — §3), so the deep-value entry the screen flagged in January is **substantially less cheap now**.
> This directly supports Hooman's own instinct: *"I don't think oil/gas is cheap anymore."* He's right.

**Confidence marks:** VERIFIED = pulled live/primary this session or carried from an EDGAR/yfinance-
verified prior file; ASSUMED = my derivation/judgment; UNVERIFIED = single secondary source or
contaminated by flag (1). Full source log at the end.

---

## TL;DR — the three verdicts

| Hooman's sub-thesis | Conviction (1–10) | One-line verdict |
|---|:--:|---|
| **1. "Energy underinvested → structural supply deficit → oil rallies"** | **5/10** | Half-true. The *long-run* underinvestment is real (oil capex falling 2nd straight year), but it's swamped **near-term (2026-27) by an OPEC+-driven oversupply** every major forecaster sees. Right theme, wrong clock. And he already concedes it's *not cheap* — so he's paying up for a thesis whose near-term catalyst points **down**. |
| **2. "Canadian energy will outperform"** | **7/10** | **Best-supported of the three.** The pro-oil-government claim is *verified and stronger than he assumed* (Carney killed the consumer carbon tax, fast-tracked pipelines, is scrapping the emissions cap). TMX + LNG Canada are real structural tailwinds. Canadian energy **has** outperformed US (+44% vs +26% trailing 12mo). Caveats: it's realized (not forecast) outperformance, the WCS discount is re-widening as TMX fills, and he's already ~56% Canada in the sleeve. |
| **3. "Energy is an indirect bet on AI"** | **3/10** | **Weakest — a stretch.** The AI→power→**gas** link is real but *modest* (~4–6 Bcf/d of datacenter gas demand by 2030, ~4–6% of US gas use, secondary to LNG) and it lands on **natural gas / gas-fired power / turbine makers**, NOT on the **oil-weighted** names that dominate his book (CNQ, CVE, XOM, OXY). Buying oil E&P to bet on AI adds commodity-price risk without capturing the AI signal. If he wants the AI-power bet, it's a *gas* bet — and he's under-weight gas equities. |

**On sizing:** ~12–13.8% of total portfolio in O&G is **~3–4× a market energy weight (~3–4% of global
equities)** — already a large, deliberate sector bet (confirmed in `sleeve_analysis.md`). As **~30% of
*non-cash*** it is a *concentration* that only makes sense if he has high conviction — and on the
evidence, only sub-thesis #2 (Canada) clears that bar. **A sensible target is to hold, not add; trim
toward ~15–20% of non-cash (~8–10% of total) on strength; tilt the *mix* toward gas and toward
quality, rather than growing the oil bet.** Detail in §7.

---

## 1. Sub-thesis #1 — "Energy underinvested → supply deficit → oil rallies"

**His own framing (important): he does NOT think oil/gas is cheap anymore — he believes in the theme.**
So the question isn't "is it cheap" (he concedes no); it's "is the *supply-deficit* theme strong enough
to justify paying up." Verdict: **partly, on a long horizon; but the near-term evidence points the
other way.**

### 1a. The bull leg (underinvestment) — REAL but slow
- **Upstream OIL investment is falling for a 2nd straight year in 2026** (~2–3% YoY, >5% below 2024),
  driven by sub-$70 oil + capital discipline. VERIFIED-as-cited (OilPrice/S&P via search, 2026).
  Consistent with our January screen (`sector_trends.md`: global upstream −4% in 2025 to <$570B vs the
  ~$738B/yr IEF/S&P say is needed by 2030). **The long-run underinvestment thesis is intact.**
- **Producers return cash instead of drilling** — XOM/EOG/CNQ total shareholder yields ~6–7% (§4). This
  discipline is exactly what caps future supply and, over a 10–20yr horizon, supports the deficit thesis.
- **US shale is plateauing, not booming:** EIA STEO (2026-06-09) US crude 13.7 mb/d (2026) → 14.2 (2027);
  Permian described as "plateau," rig count down ~12% mid-2026. VERIFIED (EIA STEO). Shale is no longer
  the swing supply it was — a genuine structural support.

### 1b. The bear leg (near-term glut) — STRONGER right now
- **Every major forecaster sees 2026-27 oversupply.** IEA (late-2025 vintage) pegged a **~4 mb/d 2026
  surplus** ("record glut"); Goldman ~3 mb/d surplus in 2026; J.P. Morgan (pre-noise, 2026-02-27):
  **Brent ~$60 for 2026, "sizable surpluses," voluntary+involuntary cuts needed.** VERIFIED-as-cited.
- **OPEC+ is actively adding barrels** — unwinding the 2.2 mb/d of cuts through end-2026 (+188k bpd in
  July 2026), a Saudi market-share play, with ~5 mb/d spare capacity still sitting idle. VERIFIED-as-cited.
  This is the single biggest near-term headwind and it's **policy, not geology** — it can persist.
- **Bank price decks cluster at Brent $75–80 for 2027, downside $60** — i.e., **flat-to-lower** from
  today's ~$72. The forward curve does *not* pay you for the deficit thesis in 2026-27.
- Oil is **down ~24% on the month** into early July 2026 even amid the (dubious) geopolitical headlines —
  "growing supply expectations continue to weigh." VERIFIED (TradingEconomics, 2026-07-07). The glut is
  reasserting in the tape.

### 1c. Verdict on #1 — **5/10**
The theme is **directionally right on a 10–20yr view** (underinvestment + shale plateau + discipline)
but **the 2026-27 clock points down** (OPEC+ unwind + broad surplus consensus + $60–80 bank decks).
Hooman is paying a not-cheap price for a thesis whose near-term catalyst is negative. That's a **patient,
long-horizon hold — not an add-here** proposition. His own "not cheap anymore" read is the correct
instinct; the screens' "cheapest sweet-spot" was a *January* snapshot that the rally has eroded.

---

## 2. Sub-thesis #3 — "Energy is an indirect bet on AI" (taken out of order; it's the weakest)

The logic: AI/datacenters need electricity → gas is the bridge fuel → own energy to ride AI without
picking AI winners. **Verdict: mostly a stretch — and it points at the wrong part of his book.**

### 2a. What's real
- **AI/datacenter power demand is real and large:** global datacenter electricity ~415 TWh (2024, ~1.5%
  of world) → **~945 TWh by 2030** (IEA *Energy and AI*, 2025). VERIFIED. Goldman: global DC power +165%
  by 2030. VERIFIED. US electricity demand at record levels, datacenters a primary driver. VERIFIED (EIA).
- **Gas IS the near-term bridge:** SMRs/nuclear are late-decade (restarts ~2027-28, SMRs 2030+); solar+
  storage can't do 24/7 training-cluster baseload alone. GE Vernova gas-turbine backlog ~100 GW, sold
  out to 2028-29 — a hard, contracted signal. VERIFIED-ish (GE Vernova Q1-2026 earnings).

### 2b. Why it's a weak thesis *for his book*
1. **It's a GAS story, and his book is OIL-heavy.** Datacenters burn *gas* for electricity; they don't
   move *oil* demand. His two biggest positions (CNQ 4.2%, XOM 4.1%) and OXY/CVE are **oil-weighted**.
   The AI signal barely touches them. His actual gas-equity exposure (ARX + TOU) is only ~2.6% of the
   portfolio (`sleeve_analysis.md`). **He's mostly betting on the wrong molecule for this thesis.**
2. **Even the gas link is modest.** Incremental datacenter gas demand is estimated **~4–6 Bcf/d by 2030**
   (East Daley ~4.2–6.1; RBC ~6.1) — only ~4–6% of ~105-110 Bcf/d US demand, and analysts rank it
   **below LNG exports** as a Henry Hub driver. UNVERIFIED-as-cited (single-source estimates). Real
   tailwind, not a needle-mover for oil producers.
3. **Adds commodity risk without AI upside.** If AI capex booms but oil sits at $60-70 (the glut case),
   his oil names can *fall* while AI wins. He'd be short-changed on both ends: full commodity downside,
   little AI capture. The AI-power *beneficiaries* (turbines, power, grid) are — per our own
   `sector_trends.md` — **already expensive** (GE Vernova ~40-45× fwd, +700%), so there's no cheap clean
   way to express it either.
4. **Demand is partly speculative.** PJM *cut* its load forecast on "overstated AI datacenter" demand;
   ~2,600 GW of interconnection queue is heavily double-booked. The hard part (hyperscaler capex ~$700B
   2026 guidance) is real; the grid-load numbers embed speculation. VERIFIED-ish / UNVERIFIED mix.

### 2c. Verdict on #3 — **3/10**
The AI-power-demand phenomenon is real, but "own oil & gas as an AI proxy" is a **logical stretch** that
adds oil-price risk without capturing AI upside. **If** he wants this bet, the honest expression is
**natural gas** (Montney/LNG-levered producers like ARX/TOU, or Henry-Hub exposure), not oil — and he's
*under*-weight gas equities today. Even then, it's a *secondary* support under gas, behind LNG. Better to
hold gas for the **LNG + supply-discipline** reasons and treat AI as a small bonus, not the thesis.

---

## 3. Sub-thesis #2 — "Canadian energy will outperform" (the strongest)

**Verdict: best-supported of the three, and the pro-oil-government claim is verified and *stronger*
than he assumed.**

### 3a. The "pro-oil Canadian government" claim — VERIFIED (and then some)
The government is **Mark Carney's Liberals** (leadership Mar 2025; won the Apr 28, 2025 election, minority
→ working majority by 2026). VERIFIED. It is decisively more pro-oil/pipeline than Trudeau's:
- **Consumer carbon tax zeroed** effective 2025-04-01. VERIFIED. **EV mandate scrapped.** VERIFIED.
- **Bill C-5 "One Canadian Economy Act"** (royal assent 2025-06-26) — Cabinet can fast-track
  "national-interest" projects with a single authorization; **Major Projects Office** set up in Calgary.
  VERIFIED.
- **Nov 2025 Canada–Alberta MOU** for a new Alberta→BC-coast oil pipeline; the **emissions cap being
  carved out/scrapped**; climate-hawk minister Guilbeault **quit Cabinet in protest**. VERIFIED (direction).
- **Industrial carbon trajectory flattened** to $115/t by 2030 (not the old $170). VERIFIED.
- **Honest caveat:** *producers still bear an industrial carbon cost* (federal OBPS / Alberta TIER remain
  in force); the consumer-tax removal was by regulation (reversible), not full repeal. So "pro-oil" is
  real but not "zero carbon cost." VERIFIED.

### 3b. Structural tailwinds are materializing
- **TMX** (started May 2024, +590k bbl/d) **compressed the WCS-WTI differential** from ~US$18.70 (pre) to
  ~US$12 (2024-25). VERIFIED (CER). **But it's re-widening to ~US$13–16 as the line fills** (~90-95% full,
  "consistently full" by 2027 per TMX CEO). VERIFIED. So the *one-time* benefit is banked; further egress
  is the next constraint (a risk, not a tailwind, from here).
- **LNG Canada is exporting** (first cargo ~end-June 2025; Phase 1 = 14 mtpa / ~2.1 Bcf/d; 100+ cargoes in
  year one; Phase 2 FID possibly end-2026). VERIFIED. Plus Woodfibre (2027), Cedar (~2028). This is a
  **durable, contracted new demand pull for Montney/Duvernay gas** — the real structural win for Canadian
  *gas* names (ARX, TOU).

### 3c. It has actually outperformed — VERIFIED
- **Trailing 12mo to 2026-07-06: Canadian energy (XEG) +43.95% vs US (XLE) +25.90%** — ~18 pts. VERIFIED
  (stockanalysis.com). Canadian majors: Cenovus +80%, Suncor +51%, CNQ +28%; gas-weighted Tourmaline −7%
  (lagged). VERIFIED. **Note: ARC (ARX) has a pending Shell takeout at C$32.80** — a name-specific event
  in his book worth confirming (VERIFIED-as-cited; check the terms/timeline).

### 3d. Verdict on #2 — **7/10**
Supported on **policy (verified), structure (TMX/LNG, verified), and realized returns (verified)**. As a
CAD investor, the Canada tilt is also a natural home-currency match and fits his stated desire to divest
from the US. **Honest caveats that keep it off 9-10:** (a) the outperformance is *realized*, not a
guaranteed forward — some of the good news (carbon tax, TMX, LNG start) is now *in the price* after the
+44% run; (b) WCS differential is **re-widening** as TMX fills, and 2027 egress tightness is a live risk;
(c) he is already **~56% Canada within the sleeve** — the diversification-away-from-US goal is largely
*achieved*, so this argues **hold/quality-tilt within Canada, not pile in further**; (d) the win has been
**oil**-led (Cenovus/Suncor) while **gas** (Tourmaline) lagged — so if he adds, the *cheaper, more
AI/LNG-levered* leg is gas.

---

## 4. Valuation — is he right that "it's not cheap anymore"? YES

Live multiples (stockanalysis.com, 2026-07-07, VERIFIED):

| | Fwd P/E | TTM P/E | EV/EBITDA | P/B | Div yield | Total shareholder yield |
|---|--:|--:|--:|--:|--:|--:|
| XOM | 10.9× | 23.0× | 10.8× | 2.22× | 3.02% | ~5.96% |
| CVX | 10.4× | 29.2× | 9.8× | 1.81× | 4.24% | −2.6%* |
| EOG | 7.6× | 12.8× | 5.8× | 2.24× | 3.15% | ~6.94% |
| CNQ | 9.2× | 11.9× | 9.0× | 2.56× | 4.45% | ~6.01% |

\* CVX buyback yield negative = share issuance from the Hess close (data artifact); dividend (4.24%) is
the clean read.

- **Sector vs market:** XLE trailing P/E ~19-20× vs S&P 500 ~27× — the usual discount, i.e. energy is
  cheap *relative to the market* but that's structural, not a signal. VERIFIED.
- **The catch (from flag 1):** the low **forward** P/Es (majors ~10-11×, EOG 7.6×) are computed on
  **war-elevated / crisis oil estimates**. Normalize to $60-70 oil and those forward multiples rise and
  the "cheap" narrows toward **FAIR**. Meanwhile **trailing** P/Es are *high* (XOM 23×, CVX 29×) because
  2025/early-2026 realized earnings were soft. **Read: through-cycle, these are FAIR, not cheap.**
- **This confirms Hooman's instinct.** In January the Damodaran screen said E&P was the cheapest sweet-
  spot (EV/EBITDA 5.1×, 31st pctile); after a big 2026 rally, that entry is gone. **He is right: not cheap
  anymore — fair, with a ~6-7% shareholder yield paying you to wait, but no valuation margin of safety.**

---

## 5. The bear case — how strong?

| Bear pillar | Evidence | Strength |
|---|---|---|
| **Near-term oversupply** | IEA ~4 mb/d 2026 surplus (late-25 vintage); Goldman ~3 mb/d; JPM Brent ~$60/persistent surplus; OPEC+ unwinding 2.2 mb/d with ~5 mb/d spare. Oil −24% on the month. VERIFIED-as-cited. | **STRONG (near-term)** |
| **EV adoption** | Global EV >20M units 2025, 25% of car sales; China ~37% domestic share. VERIFIED. mb/d of oil displaced UNVERIFIED. | **Moderate, structural (slow-burn)** |
| **Peak demand** | Repeatedly pushed back — BP's 2020 "already peaked" call was *wrong*; OPEC sees no peak; EIA no peak before 2030. VERIFIED. | **WEAK / deferred** |
| **Recession 2026** | EIA sees 2026 demand −1.1 mb/d, but that's the (dubious) shock, not a clean recession read; rebounds +2.5 mb/d 2027. | **Unclear** |
| **Renewables displacing gas in power** | Real long-run; AI/datacenter gas demand partly offsets. Specific displacement figures UNVERIFIED. | **Moderate (for gas), LT** |

**Offsets to the bear case:** OECD inventories projected to fall to ~lowest since 2003 (thin buffer =
fragile to upside shocks); peak-demand keeps slipping; ~6-7% shareholder yields pay you to wait. VERIFIED.

**Net:** the bear case is **strong near-term (glut/OPEC+) and slow-burn structural (EV) long-term**, but
**weak on "imminent peak demand."** For a 3-5yr holder the glut is the real risk; for a 20yr holder, EV +
transition is the real risk; underinvestment is the counter to both.

---

## 6. Reconciling the weight: 13.8% of total vs "30% of non-cash"

Both are true and consistent — they describe the same dollars against different denominators:
- `sleeve_analysis.md` / `hooman_oil_gas_holdings.md`: **~13.8% of TOTAL portfolio** (his export's %
  column). The prompt says **~12% of total incl. cash** and **~30% of non-cash**. VERIFIED (his export)
  / ASSUMED (the reconciliation arithmetic).
- **Implied cash:** if O&G ≈ 12-13.8% of total *and* ≈ 30% of non-cash, then **non-cash ≈ 40-46% of the
  portfolio → cash ≈ 54-60%.** ASSUMED. **This is the buried headline: he is sitting on ~half the
  portfolio in cash, and of what he's actually invested, ~30% is a single-factor bet on the oil price.**
- **Framing correction:** the earlier "13.8% is ~3-4× market weight" understated the concentration *of
  his active book*. Against **invested capital**, O&G at ~30% is closer to **~8-10× a market energy
  weight**. That is a very large active tilt — defensible only with high conviction, and only sub-thesis
  #2 (Canada) earns that.
- **Two honest reads of the cash:** (a) if the ~50% cash is *dry powder* he intends to deploy, then O&G
  as 30% of *today's* invested book will shrink as he invests elsewhere — less alarming. (b) If the cash
  is his *permanent* allocation, then 30%-of-active in one commodity factor is genuinely concentrated.
  **→ ASK Hooman which it is; the sizing verdict hinges on it.**

---

## 7. Sizing & tilt — a sensible energy weight (framework, not advice)

**Is 30% of non-cash too much?** On the evidence, **yes, for an add — it's at/above a full weight.** The
theme that justifies concentration (Canada, #2) is 7/10; the other two legs (deficit 5, AI 3) don't earn
30%-of-active conviction. And valuation is *fair, not cheap* (§4), so there's no margin-of-safety reason
to over-size right now.

**A sensible target (ranges, his call):**
- **Of TOTAL portfolio:** holding ~12-13.8% is a large-but-defensible *thematic* sector bet; I would
  **not add on top** at fair valuation into a forecast glut. Trimming toward **~8-10% of total** on
  strength is reasonable risk management.
- **Of NON-CASH:** ~30% is heavy for one commodity factor; **~15-20% of invested capital** is a more
  proportionate "high-conviction overweight" that still expresses the (real) long-run underinvestment +
  Canada theses without betting the active book on the oil price.

**Tilt guidance (all consistent with the existing sleeve work):**
1. **Gas over oil, at the margin.** Gas has *three* supports (LNG wave — incl. LNG Canada; supply
   discipline; the AI/datacenter bridge) vs oil's *one* (underinvestment) that's currently swamped by the
   OPEC+ glut. His gas *equity* exposure is only ~2.6% (ARX/TOU) — the **under-weighted** leg. If he adds
   anywhere, gas is the better-supported add. (Use ARX/TOU/UNG — **not BOIL**, the 2× decay ETF, per
   `sleeve_analysis.md`.)
2. **Canada over US** is *already done* (~56% of the sleeve) and thesis-supported — but the goal is
   largely achieved; further Canada adds concentrate WCS-differential + 2027-egress risk. **Hold the
   tilt, don't extend it.**
3. **Producers vs the commodity:** favor **quality producers with ~6-7% shareholder yield and low
   breakevens** (they pay you to wait through the glut) over the **commodity ETFs** (UNG/BOIL carry cost +
   decay, no yield). The commodity is a *worse* vehicle for a patient value investor than the disciplined
   producers.
4. **Quality within the sleeve:** the existing `sleeve_analysis.md` case stands — the highest-leverage
   *quality* move is the **weight-neutral OXY→EOG swap** (lifts blended ROE, cuts the worst balance
   sheet, no added sector weight). That's a better use of energy dollars than growing the bet.

**Bottom line:** the *theme* is real on a 20yr view and Canada is genuinely favoured — but at *fair*
valuation, into a *2026-27 glut*, with the book already at ~30% of active capital, the evidence says
**hold and upgrade quality, tilt toward gas, don't add oil.** The AI-proxy rationale should not drive
oil buys; if anything it's a (secondary) reason to hold *gas*.

---

## Verification log (all sources, with confidence)

**Carried from prior verified files (unchanged):**
- Holdings/weights: `hooman_oil_gas_holdings.md` (his export 2026-07-05). VERIFIED (his data).
- Sleeve correlations, OXY→EOG swap math, "13.8% = ~3-4× market weight," EOG ROE 18.2% / ND-EBITDA 0.35×,
  OXY ND-EBITDA 1.18× / ROE 4.1%, BOIL decay warning, ~56% Canada: `sleeve_analysis.md` (yfinance
  2026-07-05). VERIFIED (prior live pull).
- January sector cheapness (E&P EV/EBITDA 5.1× / 31st pctile, "cheapest sweet-spot," 2026-27 glut caveat):
  `sector_trends.md` (Damodaran as-of 2026-01-05). VERIFIED (fetched values) — but **stale** (§ flag 2).

**Supply/demand (research subagent, WebFetch 2026-07-07):**
- Spot: **WTI ~$68.7, Brent ~$71.5 (2026-07-06)**; **Henry Hub ~$2.94 (May-26 avg)**. VERIFIED-as-cited
  (Forbes Advisor / AGA via search). Agrees with our 2026-07-05 yfinance ($68.78/$72.13/$3.25).
- Upstream OIL capex falling 2nd straight yr (~2-3%, >5% below 2024); gas capex ~$330B (+10%, 10yr high);
  total energy investment ~$3.4T (+5%). VERIFIED-as-cited (OilPrice/Reuters/IEA WEI 2026 via search).
- OPEC+ unwinding 2.2 mb/d by end-2026 (+188k bpd Jul-26); ~5 mb/d spare capacity. VERIFIED-as-cited.
- US crude 13.7 mb/d (2026) → 14.2 (2027); Permian "plateau," rigs −12%. VERIFIED (EIA STEO 2026-06-09).
- 2026 surplus ~4 mb/d (IEA late-25) / ~3 mb/d (Goldman); JPM Brent ~$60 2026 / persistent surplus
  (2026-02-27). Bank 2027 Brent ~$75-80, downside $60. VERIFIED-as-cited.
- Henry Hub EIA STEO $3.60 (2026)/$3.46 (2027); US LNG 17.2→18.6 Bcf/d. VERIFIED-as-cited (EIA STEO).
- **⚠️ "2026 Iran war / Hormuz closure / Brent $95-119": UNVERIFIED / likely distorted** — contradicted by
  calm ~$69-72 spot. IEA/EIA mid-2026 $95-105 price *assumptions* treated as unreliable (flag 1).

**AI/datacenter power (research subagent, WebFetch 2026-07-07):**
- Datacenter electricity ~415 TWh (2024) → ~945 TWh (2030). VERIFIED (IEA Energy and AI 2025).
- Goldman: global DC power +165% by 2030. VERIFIED. US demand at records, DC-driven. VERIFIED (EIA STEO).
- GE Vernova gas-turbine backlog ~100 GW, sold out to 2028-29. VERIFIED-ish (GE Vernova Q1-26 earnings).
- Datacenter incremental gas demand **~4-6 Bcf/d by 2030** (East Daley/RBC); ~4-6% of US gas, below LNG.
  UNVERIFIED-as-cited (single-source estimates).
- Skeptic signals: PJM cut load forecast on "overstated AI"; ~2,600 GW queue heavily double-booked.
  UNVERIFIED-as-cited. Hyperscaler capex ~$700B 2026 guidance. VERIFIED-ish (GS/Moody's via secondary).

**Canada (research subagent, WebFetch 2026-07-07):**
- PM Carney/Liberals (leadership Mar-2025, won Apr-28-2025 election). VERIFIED (Wikipedia).
- Consumer carbon tax zeroed 2025-04-01; EV mandate scrapped; Bill C-5 fast-track + Major Projects Office;
  Nov-2025 AB-Canada pipeline MOU; emissions cap being scrapped; industrial carbon flattened to $115/t
  2030. VERIFIED / VERIFIED-direction (canada.ca, alberta.ca, Wikipedia, Global News).
- Industrial carbon (OBPS / Alberta TIER) STILL in force on producers. VERIFIED.
- TMX in service May-2024 (+590k bbl/d); WCS diff ~$18.7 (pre) → ~$12 (24-25) → **re-widening ~$13-16**
  (mid-26); line ~90-95% full. VERIFIED (CER / Global News / BOE Report).
- LNG Canada first cargo ~end-Jun-2025, Phase 1 14 mtpa/~2.1 Bcf/d, 100+ cargoes; Woodfibre 2027, Cedar
  ~2028. VERIFIED (lngcanada.ca, Wikipedia).
- **Canadian energy XEG +43.95% vs US XLE +25.90% trailing 12mo to 2026-07-06.** VERIFIED (stockanalysis).
  Cenovus +80%, Suncor +51%, CNQ +28%, Tourmaline −7%; **ARC pending Shell takeout at C$32.80** (confirm
  terms). VERIFIED-as-cited.
- AECO price / AECO–HH spread, exact 2026 Alberta TIER $/t, designated-project list: UNVERIFIED (gaps).

**Valuation & bear case (research subagent, WebFetch 2026-07-07):**
- XOM/CVX/EOG/CNQ fwd P/E 10.9/10.4/7.6/9.2×, EV/EBITDA 10.8/9.8/5.8/9.0×; shareholder yields ~6/−2.6/
  ~6.9/~6.0%. VERIFIED (stockanalysis.com 2026-07-07). Agrees directionally with our 2026-07-05 pull.
- XLE P/E ~19-20× vs S&P 500 ~27×. VERIFIED (stockanalysis/worldperatio).
- EV: >20M units 2025, 25% of car sales, China ~37% domestic. VERIFIED (Wikipedia). mb/d displaced
  UNVERIFIED.
- Peak-demand repeatedly pushed back (BP-2020 wrong; OPEC no peak; EIA no peak <2030). VERIFIED.
- OECD inventories → lowest since 2003 (thin buffer). VERIFIED-as-cited (EIA STEO — but see flag 1, tied
  to the disputed shock narrative; treat the *thinness* direction as plausible, the *magnitude* as
  UNVERIFIED).
- **S&P 500 energy weight (~3%, near lows): UNVERIFIED** (sources blocked; historically fell ~11-13% (2011)
  → ~3-4% (2020s) — plausible but unconfirmed this session).

**Method caveats:** WebSearch was unavailable to the subagents; figures came via WebFetch over search-
result pages + primary sites (EIA, GE Vernova, canada.ca, stockanalysis.com), with IEA/Reuters/S&P/
Google frequently blocked → hence the many "VERIFIED-as-cited" (real source named, primary PDF not opened)
and UNVERIFIED tags. The single biggest caveat is **flag 1** (the disputed 2026 Hormuz/Iran narrative):
it distorts IEA/EIA *forward price assumptions* but NOT the *spot prices* or *company multiples*, which
are cross-confirmed. **Before acting, re-confirm from primary terminals:** IEA OMR + WEI 2026, EIA STEO
tables, the 2026-27 surplus mb/d, S&P-500 energy weight, AECO/TIER figures, and the ARC/Shell deal terms.

**NOT financial advice — research to inform Hooman's own decision.**
