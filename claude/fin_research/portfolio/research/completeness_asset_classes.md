# Completeness Audit — Asset Classes & Risk Factors

**Prepared 2026-07-08 (Opus 4.8). RESEARCH, NOT FINANCIAL ADVICE.** This is a *completeness* audit,
not a bet-adding exercise. Question for each item: given Hooman's **actual goals** (Canadian citizen,
quality-first, 3–5yr house down-payment needing <10% portfolio vol, 20yr wealth, poor forecasting
confidence, strong USD-debasement conviction), is this a **genuine gap** or is it already handled by
VT + cash + TIPS? All prices/returns/correlations are **live yfinance pulls dated 2026-07-06/08**;
methodology + raw numbers in the Verification Log at the bottom. Confidence marked VERIFIED / ASSUMED /
UNVERIFIED.

**Portfolio being audited (post-plan, ~$556k liquid):** ~30% cash+short-TIPS · 22% VT · 5% EM · 8% quality
compounders · ~26% commodities/real-assets (energy+gold+copper+ag) · ~2% crypto. **Plus** ~$732k Adobe RSUs
(US-tech, single-name) and a separate $250k CAD house reserve (with his father, outside this book).

---

## The one framing that drives half the answers

Two of Hooman's constraints are in **direct tension** and the whole audit hinges on which wins:

- **"USD will debase / I fear nominal bonds"** → argues for real assets, gold, TIPS, NO nominal duration.
- **"I need <10% vol and my house money must survive a stock crash in 3–5 years"** → argues for exactly
  the asset that debasement-fear rejects: **nominal government duration**, because that is the asset that
  reliably *rises* when equities crash in a **deflationary/growth shock** (the most common kind of crash).

The evidence below shows these are **two different crash regimes**, and he is currently insured against
only one of them. That is the single biggest completeness gap. Everything else is smaller.

---

## Ranked summary table

Grade = must-have (10) → safe-skip (1), **for his specific goals**, not in the abstract.

| # | Asset class / factor | Currently? | Genuine gap? | Grade | Cleanest instrument | One-line verdict |
|--:|---|---|---|:--:|---|---|
| 1 | **Intermediate nominal govt duration (flight-to-quality hedge)** | ZERO | **YES — biggest gap** | **8** | IEI / IEF (US) or **XSB.TO/VAB.TO (CAD)** | The house-goal *needs* a deflation-crash hedge; cash+TIPS don't rise in a crash. Small sleeve. |
| 2 | **Currency: CAD/USD balance vs the liability** | USD-tilted | **YES — mis-weighted** | **8** | Hold house-horizon cash in the **currency of the house** | His near-term *liability* may be CAD; a USD-tilted reserve is an un-hedged FX bet on the house. |
| 3 | **Canadian real-return / short bonds vs US TIPS** | US short-TIPS | Partial gap | **6** | Split some TIPS → **XSB.TO / XRB.TO** if house is likely CAD | Currency-match the inflation hedge to the currency of the thing you're hedging. |
| 4 | **Deliberate value / small-cap-value tilt** | VT cap-weight only | YES — and he *says* he wants it | **6** | **AVUV** (US SCV) + **AVDV** (intl SCV), small | He wants "cheap quality"; cap-weighted VT is the opposite. Modest tilt closes the say-do gap. |
| 5 | **Managed futures / trend** | none | Optional — real diversifier | **5** | **DBMF** (single, cheap-ish) | The one alt that *actually* helped in 2022 (+20%). Complexity tax; 3–5% max or skip. |
| 6 | **Cash-management optimization** | plan says SGOV | Minor tune, not a gap | **4** | SGOV/BIL is already near-optimal; add **CAD GIC/HISA** for the CAD portion | He's NOT leaving much on the table. Main fix is *currency split*, not instrument. |
| 7 | **REITs (liquid real estate)** | ~0 | **NO — correctly absent** | **3** | (REET/VNQ if anything) | REIT ≠ house hedge; it's levered equity-beta. Adds vol he doesn't need pre-purchase. |
| 8 | **International / FX bonds as USD hedge** | none | NO — worse tools exist | **2** | (BWX/BNDX — don't) | Gold + VXUS + Cdn assets already hedge USD better. FX bonds add duration+credit for little. |

---

## 1. Bonds / duration — the real gap (Grade 8)

**His position:** refuses US long bonds (USD-debt fear), holds only cash + short TIPS → **zero nominal
government or intermediate duration.**

**The claim I tested:** *"cash + short TIPS is enough; I don't need bonds because bonds fall when the
dollar debases."* **This conflates two different crash regimes,** and the data separates them cleanly.

**Evidence — how each asset behaves when stocks crash (VERIFIED, live pull):**

**(a) Deflationary / growth-shock crash (the COVID-19 crash, 2020-02-19 → 03-23, SPY −33.7%):**
| Asset | Return in the crash |
|---|--:|
| IEF (7-10yr UST) | **+6.4%** |
| IEI (3-7yr UST) | **+4.4%** |
| TIP | −0.6% |
| VTIP (short TIPS) | −2.4% |
| GLD | −3.6% |
| SGOV/cash | ~0% (flat) |
| SPY | −33.7% |

**(b) 2018 Q4 growth-scare (SPY −19.2%):** IEF **+3.4%**, IEI +2.3%, BND +1.3%, GLD +6.6%, short TIPS ~0.
→ **Intermediate Treasuries were the single best equity hedge in both deflationary crashes.** This is the
"flight-to-quality" bid: when growth fear dominates, money runs *to* government bonds, they rise, and they
offset equity losses. **Cash just sits flat; it does not rise, so it doesn't offset — it only fails to
fall.** Short TIPS behave like cash here.

**(c) Inflationary / rate-shock crash (2022, the year "bonds failed"):** SPY −18.6%, IEF −14.4%,
BND −12.5%, TIP −11.8%, **but** VTIP (short TIPS) −2.9%, SGOV +1.6%, GLD +0.8%, **DBMF +20.5%.**
→ This is the regime Hooman is (correctly) afraid of, and it's the one he's *already insured against*:
short TIPS + cash + gold all held up; long duration got destroyed.

**Also confirming the diversification math — daily correlation to SPY over ~6y (VERIFIED):**
SGOV −0.02 · IEI/IEF **+0.07** · TIP +0.19 · GLD +0.16 · LQD +0.36 · VT +0.97. Intermediate Treasuries are
about as *de-correlated* from equities as anything available, and *negatively* correlated in the left tail.

### The verdict on bonds
His "no long bonds" instinct is **right**; his "no intermediate govt at all" conclusion is **an over-correction**.
- **He is insured against the inflationary crash (2022-type) and completely uninsured against the deflationary
  crash (2020/2008-type)** — which is historically the *more common* equity-market crash and the more dangerous
  one for a 3–5yr house goal, because that's exactly when he might also face job/RSU risk (Adobe = US tech,
  correlated to the same shock).
- **Cash does NOT substitute for the flight-to-quality hedge.** Cash is a vol-reducer (great, keep it) but it
  is *not* a crash-*offsetter* — it doesn't rise. Intermediate Treasuries do. For someone who "can't forecast
  which crash regime," owning *both* insurances is the completeness move.
- **Duration to own:** *intermediate, not long.* 3–7yr (IEI) or 7–10yr (IEF) captures ~80% of the crash-hedge
  convexity with far less rate-shock downside than 20yr+ (TLT). This threads his needle: the crash protection
  without the USD-debasement/long-end exposure he fears.
- **Sizing:** small — **~5–8% of the liquid book**, funded from the fat cash sleeve (he has ~30% cash+TIPS;
  carving 5–8pts of *cash* into intermediate govt keeps vol ~flat while adding a crash-offsetter). This is a
  *reallocation within Bucket A*, not new risk.

**US vs Canadian govt bonds:** For the 3–5yr **house** money, prefer **CAD** (XSB.TO short / VAB.TO aggregate)
**if the house is likely Canadian** — it removes FX risk on the money earmarked for a CAD purchase (see §8).
Canadian bonds gave the same crash-hedge/rate-shock profile (XBB.TO −9.8% in 2022, similar to US Agg −12.5%,
VERIFIED). If the house is likely US, US intermediate Treasuries are fine and simpler.

> **Bottom line #1 gap: add ~5–8% intermediate government bonds (currency-matched to the house), funded from
> cash — NOT long bonds. This is the missing crash-regime insurance, and it's the highest-value change in this
> audit.**

---

## 2. International / foreign-currency bonds as a USD hedge (Grade 2 — skip)

**Tempting because** USD-debasement is his #1 conviction, and unhedged foreign bonds (BWX, IGOV) rise when
USD falls.

**But the data says these are a poor tool (VERIFIED):**
- BWX (intl govt unhedged) correlation to SPY **+0.26**, vol **9.7%**, and it **fell −18.7% in 2022** — worse
  than SPY. It stacks *foreign duration + foreign credit + FX* into one instrument and got hit on all three.
- In the COVID crash BWX was −0.23%/day in the worst-5% days — it did **not** provide flight-to-quality.
- BNDX (hedged) removes the FX — which defeats the entire purpose of holding it as a USD hedge.

**He already hedges USD four better ways:** gold (the true monetary hedge), VXUS/VT's ~40% ex-US earnings,
Canadian energy/gold assets, and CAD cash. Foreign-currency *bonds* add duration and credit risk to chase a
currency move he can express more cleanly. **Skip.**

---

## 3. REITs / liquid real estate (Grade 3 — correctly absent, do NOT add for the house)

**The intuition to test:** *"I want to buy a house; should I own REITs now as liquid real-estate exposure
while I wait 3–5 years?"*

**Answer: No — REITs are not a proxy for a house, and adding them now works against the house goal.**
- **REITs are levered equity, not a real-estate-price hedge.** VNQ correlation to SPY is high and its
  **vol is 18.9%** — *higher* than VT (16.2%) and SPY (17.2%) (VERIFIED). REET (global) 17.0% vol, Cdn XRE.TO
  16.2%. These trade like small-cap financials, not like house prices.
- **They fall *with* stocks in a crash**, i.e., exactly when he'd want stability before a purchase — VNQ has
  no flight-to-quality property.
- **Owning REITs to "pre-buy" real estate is a category error:** house-price risk for *his* purchase is
  local, idiosyncratic, and doesn't track a global REIT index. The clean hedge for "houses get more
  expensive" is (a) the CAD/USD cash earmarked for it and (b) broad real assets he already owns.
- **Note:** VT already contains ~2–3% REITs at market weight — he has *some* incidental exposure and needs
  no more.
- **The one nuance worth a footnote, not a buy:** data-center / cell-tower REITs (DLR, AMT) are an AI/
  infrastructure theme, but AMT is −22.6% 1yr and DLR vol is 28.8% — these are theme-equity bets, and his
  AI-power theme is already covered by CEG/BWXT. No REIT action recommended.

> He is **right** to own ~0 REITs pre-purchase. Adding them would add equity-correlated vol he explicitly
> doesn't want. **Safe to skip.**

---

## 4. TIPS: US vs Canadian Real Return Bonds (Grade 6 — currency-match some)

He's adding **US short TIPS (VTIP/TIP)** — good instrument, right idea (short TIPS held up in 2022: VTIP
−2.9% vs TIP −11.8%, because short TIPS strip out most duration risk while keeping the inflation accrual;
VERIFIED). Short is correct for a 3–5yr horizon.

**The Canadian angle:** TIPS protect **US** CPI in **USD**. If his inflation liability is a **Canadian**
house, US TIPS hedge the wrong country's inflation *and* carry FX risk. Canadian **Real Return Bonds** (XRB.TO,
ZRR.TO) hedge CAD CPI in CAD.

**Caveats (important, verified/known):**
- **Canadian RRBs are long-duration and volatile.** XRB.TO annualized vol **11.9%** and it fell **−11.8% in
  2022** (VERIFIED) — because Canada **stopped issuing new RRBs in 2022** (Federal Budget 2022), so the
  outstanding pool is old, long-dated, illiquid, and rate-sensitive. There is **no short-dated Canadian
  real-return ETF** equivalent to VTIP. This is a real structural limitation.
- So the clean "short + currency-matched real-return" instrument **does not exist in CAD.**

**Practical resolution:** keep the short-inflation hedge in **US VTIP** (best short-real-return vehicle that
exists), and if the house is likely CAD, get the *currency* match via **CAD nominal short bonds / GICs**
(§3-adjacent) rather than volatile long CAD RRBs. Don't force Canadian RRBs just for the flag — the duration
penalty isn't worth it for a 3–5yr horizon.

---

## 5. Value / small-cap-value / factor tilts (Grade 6 — closes a say-do gap)

**The say-do gap:** Hooman's stated philosophy is **"quality names that are cheap"** (value + quality). But
his equity core is going 22% into **VT, which is pure cap-weighted** — the *opposite* of a value tilt (it
overweights whatever is most expensive/largest, currently US mega-cap tech, which he *also* already owns via
$732k Adobe RSUs). **His index choice contradicts his stated factor preference and doubles his mega-cap-tech
concentration.**

**Evidence the value/SCV factor is live, not dead (VERIFIED 1yr returns to 2026-07-06):** AVUV (US small
value) **+31.5%**, IWN +35.7%, VLUE +68.9%, AVDV (intl small value) +33.3%, VTV (large value) +24.8% — all
beat or matched VT +22.6% over the trailing year. (One year isn't proof of a premium — mark the *long-run*
premium ASSUMED — but it confirms the factor isn't broken.)

**The completeness move:** tilt a **slice** of the equity core toward small-cap-value / quality-value:
- **AVUV** (US small-cap value, Avantis) — the cleanest, most-cited SCV vehicle; vol 22.6% (higher than VT,
  size it accordingly).
- **AVDV** (intl developed small-cap value) — diversifies the tilt away from the US, fits his ex-US goal.
- **QUAL** if he wants the *quality* factor explicitly (vol 17.4%, ~market).
- **Sizing:** ~3–6% of the book (e.g., carve a few points *out of VT*, not additive), so the core is
  "VT + a value/quality tilt" rather than pure cap-weight. This is the factor expression he says he wants,
  done with ETFs instead of stock-picking — which suits "poor forecaster."
- **Caveat:** SCV is *higher* vol and can underperform for years. Keep it a tilt, not the core. And note his
  8% "quality compounders" sleeve is a *concentrated stock* version of the same idea — the ETF tilt is the
  diversified, lower-regret way to get it.

---

## 6. Managed futures / trend (Grade 5 — the one alt worth considering)

**Why it's on the table:** it's the one diversifier that *provably* helped in the exact scenario he fears.
**DBMF returned +20.5% in 2022** while stocks AND bonds both fell double digits (VERIFIED). Correlation to
SPY **+0.14**, vol 12.5%. It's a genuine "third leg" — trend-following goes short in sustained selloffs.

**Evidence, honestly (VERIFIED):**
- **The good:** +20.5% in 2022 (crisis alpha in the inflationary crash), low correlation.
- **The bad:** in the *fast* COVID crash DBMF was **−6.6%** (trend can't reposition in a 4-week crash), and
  KMLM/CTA 1yr returns are mediocre (+10.7% / +0.7%). Managed futures help in *sustained* trends, not sudden
  gaps. It's also a "black box" — higher fees (~0.85%), harder to hold through flat years.

**Verdict:** a **legitimate but optional** completeness item. If he wants a diversifier that covers the
inflationary-crash regime *even better* than his gold+TIPS already do, **3–5% DBMF** is defensible and would
make the book genuinely all-weather. But it adds complexity and a behavioral hold-through-flat-years cost.
**For a "keep-it-simple, poor-forecaster" investor, this is a nice-to-have, not a must — grade 5.** If he
skips it, gold + short-TIPS + cash already cover the inflationary crash adequately.

---

## 7. Cash-management optimization (Grade 4 — minor tune, not a gap)

He'll hold ~$189k in cash/TIPS. Is plain SGOV optimal?

**Largely yes (VERIFIED yields, 2026-07-08):** SGOV yields **~3.85%**, BIL ~3.85%, both vol **0.3%** — this
is essentially the risk-free rate with near-zero volatility and daily liquidity. **He is not leaving material
yield on the table** with SGOV. Money-market funds would be within a few bps.

**The only real optimizations:**
1. **Currency split (this is the actual issue — see §8):** SGOV is USD. If part of the reserve backs a *CAD*
   house, that portion should be in **CAD instruments**: a Canadian **HISA ETF / GIC ladder / CASH.TO-type**
   fund. Canadian short paper (XSB.TO yields ~3.1%) currently yields a touch less than USD, but that gap is
   an FX bet, not free money.
2. **GIC ladder** for any CAD tranche he's *certain* he won't touch for 1–3yr can beat HISA by a bit and is
   CDIC-insured — but sacrifices liquidity; only for the "definitely not the emergency" slice.
3. **Don't over-engineer.** The yield differences here are 2nd-order. The *currency* decision dominates the
   *instrument* decision by an order of magnitude.

> **He's fine on instrument (SGOV is near-optimal). The cash question is really a currency question.**

---

## 8. Currency exposure as its own decision (Grade 8 — genuinely mis-weighted)

**This is the second-biggest gap, and it's subtle because the plan made it deliberately.** The execution plan
**tilts cash to USD** on the logic "the $250k house reserve is already CAD, so this book leans USD." That
reasoning has a hole:

- **His largest single risk asset — ~$732k Adobe RSUs — is already USD** (US tech, paid in USD). His book is
  therefore **already massively USD-exposed** before any cash tilt. Adding a USD cash tilt *compounds* an
  existing USD concentration; it doesn't balance a CAD reserve.
- **His near-term liability (the house) may be CAD.** If he buys in Canada, a USD-tilted reserve means his
  down-payment's purchasing power swings with CAD/USD — an **un-hedged FX bet on his most important 3–5yr
  goal.** In 2022 CAD fell −6.6% vs USD (VERIFIED) — that cuts both ways, i.e., it's uncompensated volatility
  on the house money, which directly conflicts with the <10%-vol / capital-certainty mandate.
- **FXC (CAD ETF) correlation to SPY is +0.45** (VERIFIED) — CAD is itself a risk-on/commodity currency, so a
  Canadian holding USD cash is *also* getting some diversification. The point isn't "all CAD" — it's "match
  the currency to the *liability*, not tilt on a macro hunch."

**The completeness fix — currency-match to the liability, resolve the house-location fork:**
- **If house is likely Canadian:** the money earmarked for it (a big chunk of the $189k Bucket A) should be
  **CAD**, not USD. That neutralizes FX risk on the purchase. Keep only the *emergency/optionality* slice USD.
- **If house is likely US:** the USD tilt is correct and consistent (this is the case the plan assumed, tied
  to a possible green card).
- **If genuinely 50/50 / undecided:** hold the house-horizon reserve **split ~50/50 CAD/USD** — that's the
  minimum-regret hedge when the liability currency is unknown. A one-sided USD tilt is only right if he's
  fairly sure the house is US.

> **This is a real decision he owns, and the current plan quietly pre-decided it toward USD. Given his total
> book is already ~$1.4M USD-heavy (RSUs + tilt), and the house may be CAD, the currency of the reserve is
> arguably his most under-examined risk. Flag it explicitly, don't let it ride by default.**

---

## Cross-cutting observation: he's already more complete than he feels

Most of his instincts are **correct**, and completeness here means *reallocating within* what he has plus two
targeted additions — **not a pile of new bets.** He's right to skip REITs, right to skip foreign-currency
bonds, right to fear long bonds, right on short-TIPS, and near-optimal on cash instrument. The gaps are
narrow and specific.

---

## TOP GAPS TO FIX (in priority order)

1. **Add ~5–8% intermediate government bonds (IEI/IEF or CAD XSB/VAB), funded from the cash sleeve — NOT long
   bonds.** This is the missing deflationary-crash insurance: intermediate Treasuries *rose* +4–6% in the
   COVID crash and +2–3% in 2018 while stocks fell 20–34%, whereas his cash+short-TIPS only stayed flat. For a
   3–5yr house goal held by someone who can't forecast the crash regime, owning *both* crash-insurances
   (inflation: TIPS/gold ✅ already; deflation: intermediate govt ❌ missing) is the completeness move. Keeps
   vol ~flat because it's funded from cash. **(Grade 8)**

2. **Explicitly decide the currency of the house-reserve, and stop the default USD tilt.** His book is already
   ~$732k USD (Adobe RSUs) + a USD cash tilt = deeply USD-concentrated, while his near-term liability may be
   CAD. Match the reserve's currency to the *likely house location*; if undecided, split ~50/50 CAD/USD.
   A one-sided USD tilt is an un-hedged FX bet on his most important 3–5yr goal. **(Grade 8)**

3. **Tilt a slice (~3–6%) of the VT core toward small-cap/quality-value (AVUV + AVDV/QUAL), carved out of VT.**
   Closes the say-do gap: he wants "cheap quality" but VT is pure cap-weight (overweighting the mega-cap tech
   he already owns via RSUs). Do it with ETFs, not stock-picking — fits "poor forecaster." **(Grade 6)**

4. **Currency-match the inflation hedge where feasible:** keep the *short* real hedge in US VTIP (no good short
   CAD RRB exists — Canada stopped issuing RRBs in 2022, and XRB.TO is long/volatile: −11.8% in 2022), but get
   the CAD match via CAD short nominal bonds/GICs if the house is Canadian. **(Grade 6)**

## THINGS YOU CAN SAFELY SKIP

- **REITs (Grade 3).** Not a house-price hedge; they're high-vol (VNQ 18.9% vol) equity-beta that falls *with*
  stocks. VT already holds ~2–3% incidentally. Adding them works against the <10%-vol goal. **Skip.**
- **International / foreign-currency bonds as a USD hedge (Grade 2).** BWX fell −18.7% in 2022 and gave no
  flight-to-quality; it stacks foreign duration+credit+FX. Gold + VXUS + CAD assets hedge USD far more
  cleanly. **Skip.**
- **Cash instrument tinkering (Grade 4).** SGOV at ~3.85% / 0.3% vol is already near-optimal; GIC/MMF gains are
  bps. Don't over-engineer — the cash *currency* decision (gap #2) is the only thing that matters here.
- **Managed futures (Grade 5) — optional, not required.** DBMF is a *legit* diversifier (+20.5% in 2022), and
  3–5% would make the book genuinely all-weather. But it adds complexity/fees and lagged in the fast COVID
  crash (−6.6%); gold+TIPS+cash already cover the inflationary regime. **Take it only if he wants max
  robustness and will hold through flat years; otherwise a clean skip.**
- **Long-duration bonds (TLT/EDV) — skip, his instinct is right.** −14%+ in 2022; the long end carries exactly
  the rate/debasement risk he fears. Intermediate (gap #1) captures the crash-hedge without the long-end tail.

---

## VERIFICATION LOG

**Data source:** yfinance 1.5.1, live pulls 2026-07-06 → 2026-07-08 (auto-adjusted total-return prices).
Scripts: `/tmp/pull_ac.py`, `/tmp/corr.py`, `/tmp/crash.py`, `/tmp/yld.py`, `/tmp/xbb22.py` (ephemeral; logic
reproduced below).

| Claim | Value | Source / method | Confidence |
|---|---|---|:--:|
| IEF +6.4%, IEI +4.4% in COVID crash (SPY −33.7%) | 2020-02-19→03-23 window | yfinance total return | **VERIFIED** |
| Short TIPS (VTIP) −2.4%, GLD −3.6%, cash flat in COVID crash | same window | yfinance | **VERIFIED** |
| IEF +3.4%, GLD +6.6% in 2018 Q4 (SPY −19.2%) | 2018-10-01→12-24 | yfinance | **VERIFIED** |
| 2022: SPY −18.6%, IEF −14.4%, BND −12.5%, TIP −11.8%, VTIP −2.9%, GLD +0.8%, SGOV +1.6%, DBMF +20.5% | calendar 2022 | yfinance | **VERIFIED** |
| XBB.TO (Cdn Agg) −9.8%, XRB.TO (Cdn RRB) −11.8% in 2022 | 2022 full year (.history) | yfinance | **VERIFIED** |
| Daily corr to SPY (~6y): SGOV −0.02, IEI/IEF +0.07, TIP +0.19, GLD +0.16, LQD +0.36, BWX +0.26, FXC +0.45, VT +0.97 | 6y daily returns | yfinance corr matrix | **VERIFIED** |
| Vol (annualized, 5y): VNQ 18.9%, REET 17.0%, XRE.TO 16.2%, VT 16.2%, SPY 17.2%, AVUV 22.6%, VTIP 2.8%, DBMF 12.5%, SGOV 0.3% | daily std ×√252 | yfinance | **VERIFIED** |
| 1yr returns to 2026-07-06: AVUV +31.5%, IWN +35.7%, VLUE +68.9%, AVDV +33.3%, VTV +24.8%, VT +22.6%, GLD +22.9%, DBMF +25.8% | trailing 252d | yfinance | **VERIFIED** |
| BWX −18.7% in 2022; −0.23%/day avg in SPY worst-5% days | 2022 + stress quantile | yfinance | **VERIFIED** |
| Yields (2026-07-08): SGOV ~3.85%, BIL ~3.85%, VTIP ~3.6%, TIP ~3.77%, XSB.TO ~3.11%, XRB.TO ~2.4%, FXC ~0.28% | .info yield field | yfinance | **VERIFIED** (Yahoo yield fields can lag; treat as approximate) |
| CAD −6.6% vs USD in 2022 | CADUSD=X 2022 | yfinance | **VERIFIED** |
| Long-run value/SCV premium exists | — | financial theory (Fama-French); not tested here | **ASSUMED** |
| Canada stopped issuing Real Return Bonds in 2022 (Budget 2022) | — | Dept of Finance Canada announcement; widely reported | **ASSUMED** (from knowledge, not re-pulled — explains XRB.TO illiquidity/vol) |
| Deflationary crashes are the "more common" equity crash type | — | historical pattern (2000, 2008, 2020 vs 1970s/2022) | **ASSUMED** |
| VT contains ~2–3% REITs at market weight | — | index composition | **ASSUMED** |
| Adobe RSUs ~$732k are USD/US-tech | — | from project context | **VERIFIED (context)** |

**Reproduction notes:** Total-return figures use `auto_adjust=True`. Correlations/vol on daily `pct_change`.
Crash windows are peak-to-trough calendar dates. XBB.TO/XRB.TO 2022 required `.history()` (bulk `download`
returned NaN for the multi-year TO-listed series — a yfinance quirk, resolved by single-ticker history). One
year of factor outperformance is **not** proof of a premium — it only confirms the factor is functioning;
the long-run premium is marked ASSUMED.

**NOT financial advice.** Confirm all figures and account-tax treatment at execution; re-verify ASSUMED items.
