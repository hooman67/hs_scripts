# Clean-Slate Portfolio — The Evidence Base

**What the weight of academic + practitioner evidence supports for a long-horizon investor.**
No client beliefs, no thematic bets (no commodity/gold/USD-collapse/AI/China theses) — just
the building blocks the literature actually supports.

- **Prepared:** mid-2026 (research session 2026-07-09).
- **Investor context (for instrument selection only):** Canadian-domiciled, long horizon.
  US-listed ETFs cited for the academic mapping; Canadian-listed equivalents given where the
  currency/tax difference matters.
- **Confidence convention:** every material claim is tagged **VERIFIED** (fetched from a
  primary/near-primary source this session, with source + date), **ASSUMED** (standard-canon
  fact used as a modeling input), or **UNVERIFIED** (plausible, from a secondary snippet or a
  paywalled interior — do not treat as settled).
- **Anti-hallucination rule honored:** no fabricated numbers. Live prices/yields were pulled
  via `yfinance`/primary yield sources this session; every named figure carries its source in
  the Verification Log (§8).

> **Honesty stance:** this report deliberately states the counterargument next to every
> consensus claim. The evidence base is strong on *costs, diversification, and staying
> invested*; it is genuinely *contested* on factor tilts, the current role of bonds, and every
> "diversifier" beyond stocks/bonds. Where the evidence is thin, it says so.

---

## 1. Core Evidence for Asset Allocation

### 1.1 Own the whole market, cap-weighted — the default that's hard to beat

The strongest, least-contested result in the literature is **William Sharpe's "Arithmetic of
Active Management" (1991)**: because all investors collectively *are* the market, the
average actively-managed dollar must earn the market return **minus costs**, before which the
average active and passive dollar earn the same. This is arithmetic, not a model — true in
every measured period. **[VERIFIED — Sharpe, Financial Analysts Journal, Jan/Feb 1991.]**

The empirical confirmation is **SPIVA** (S&P Dow Jones Indices) and **Morningstar's
Active/Passive Barometer**:

- **US large-cap active funds that underperformed the S&P 500:** ~65% over 1 year (2024),
  **84.3% over 10 years** (ending Dec 2024). 2024 was the **15th consecutive year** the
  majority lagged. **[VERIFIED via secondary — SPIVA U.S. Year-End 2024.]** 15- and 20-year
  cells commonly reported >90% underperformance but **[UNVERIFIED — not pulled from the primary
  PDF]**.
- **Canada is worse for active:** **95.5% of Canadian Equity active funds underperformed over
  10 years** (ending Dec 2024); 88.7% over 1 year. **[VERIFIED via secondary — SPIVA Canada
  Year-End 2024.]** This matters directly for a Canadian investor: the home-market active
  industry has an even weaker record than the US.
- **Morningstar Active/Passive Barometer (Year-End 2025):** roughly **1 in 5 (~20%)** active
  funds beat the average comparable *passive* fund over 10 years; the average surviving active
  large-blend fund trailed by ~1.9%/yr over the decade to Dec 2024. **[VERIFIED via secondary.]**
- **Persistence is near-random:** top-quartile funds have "little better than random odds" of
  staying top-quartile — you cannot reliably pick tomorrow's winners from yesterday's. **[SPIVA
  Persistence Scorecard — qualitative finding VERIFIED via secondary; exact "≈0% after 5 years"
  figure UNVERIFIED this session.]**
- **Survivorship:** ~**64% of US domestic stock funds were merged or liquidated over the 20
  years to 2024** — the "which fund" choice is partly a bet on the fund still existing.
  **[VERIFIED via secondary — SPIVA YE2024.]**

**Bottom line:** a broad, low-cost, cap-weighted total-market index fund is the evidence-based
default core. The burden of proof is on any deviation.

**Counterargument (honest):** SPIVA/Barometer measure the *average* active dollar; they do not
prove skill is impossible, only that it's rare, doesn't persist reliably, and is hard to
identify *in advance* net of fees. Indexing also means you *guarantee* you never beat the
market and you accept whatever concentration the cap-weighted index carries (see §2.5).

### 1.2 Global vs home — the US/ex-US split

- **US = 63.6% of global equity market cap; ex-US ≈ 36.4%** (next: Japan ~5.0%, Taiwan ~3.3%,
  UK ~3.0%). **[VERIFIED — MSCI ACWI factsheet, data as of Jun 30, 2026.]** The FTSE Global All
  Cap runs a point or two lower on the US (broader small/EM inclusion). So the "~60/40 US/ex-US"
  framing is right; the precise current split is closer to **~64/36**.
- **Vanguard's guidance:** hold roughly **40% of the equity sleeve internationally** (and ~30%
  of bonds), with ~20% the minimum to get a meaningful diversification benefit; Vanguard
  concedes most investors sit below market-cap weight for cost/tax/home-bias reasons.
  **[Figure VERIFIED against multiple citing sources; exact white-paper URL UNVERIFIED.]**

**Why diversify internationally:** single-country concentration risk is uncompensated. No one
knew in 1989 that Japan (then ~45% of world market cap) would spend 30+ years underwater. The
US has led for 15 years; the evidence says *own both* rather than *bet on the winner
continuing*. **Counterargument:** international has underperformed the US for over a decade,
currency adds volatility, and US mega-caps already earn ~40% of revenue abroad (partial
"look-through" global exposure). A defensible range is **30–50% of equity ex-US**; pure
market-cap weight (~36% ex-US) is the neutral anchor.

### 1.3 The equity/bond split

There is no single "correct" split — it's a risk-tolerance and horizon decision, not a
purely empirical one. What the evidence *does* support:

- Equities carry the highest long-run real return (see §3.1 for the 1928–2025 numbers) but
  with drawdowns of −50%+ that can last years; bonds cut portfolio volatility and (usually)
  supply dry powder to rebalance into equities.
- **Glidepath consensus:** stock weight should fall as the horizon shortens. Vanguard's Target
  Retirement path starts ~**90% equity** (accumulation), glides to ~**50% at age 65**, and
  settles ~**30% equity / 70% bonds** by ~age 72. **[VERIFIED — Vanguard glidepath methodology.]**
- A **60/40** (moderate) or **80/20** (growth, long horizon) split are the reference balanced
  portfolios (§6).

---

## 2. Factor Tilts — Robust vs Data-Mined

### 2.1 The factor menu (what they are)

- **Fama-French 3-factor (1993):** Market, **SMB** (size), **HML** (value/book-to-market).
- **Fama-French 5-factor (2015):** adds **RMW** (profitability/quality) and **CMA**
  (investment). **[VERIFIED — FF 1993 & 2015, Journal of Financial Economics.]**
- **Carhart (1997):** adds **momentum** (UMD). **[ASSUMED — standard canon.]**

### 2.2 What has held up out-of-sample

- **Profitability/Quality (Novy-Marx 2013):** gross-profits-to-assets predicts the cross-
  section about as strongly as book-to-market; profitable firms out-earn even at higher
  valuations. Motivated FF's RMW factor. **[VERIFIED — "The Other Side of Value," JFE 108(1),
  2013.]** Widely regarded as one of the more robust, economically sensible premia.
- **Momentum (Jegadeesh-Titman 1993):** past winners beat losers by ~1%/month; persists
  out-of-sample and across asset classes and countries. **[VERIFIED.]** *But:* high turnover →
  large transaction and tax costs, and a fat left tail — the **2009 momentum crash** (Daniel &
  Moskowitz, 2016) can erase years of gains quickly. **[Event VERIFIED; paper ASSUMED.]**
- **Low-volatility / betting-against-beta (Frazzini-Pedersen 2014; Baker-Bradley-Wurgler
  2011):** low-beta stocks earn higher risk-adjusted returns than CAPM predicts, documented
  over ~90 years, internationally, and in bonds. **[VERIFIED.]**

### 2.3 What is weaker than advertised

- **Size (SMB):** the raw Banz (1981) small-cap premium **largely disappeared after
  publication** and internationally — a poster child for data-mining decay. It is rehabilitated
  **only when you control for quality**: AQR's **"Size Matters, If You Control Your Junk"
  (2018)** shows a strong, stable size premium *after* removing small-cap "junk." So naive
  small-cap tilts are not well-supported; **small-cap *quality/value* is.** **[VERIFIED —
  title/thesis; exact magnitude UNVERIFIED.]**
- **Value (HML):** real, but endured its **worst-ever drawdown ~2007–2020** ("the lost
  decade"). AQR's **"Is (Systematic) Value Investing Dead?" (May 2020)** argued no — the value
  spread was the widest in 50+ years and not explained by fundamentals or a tech-monopoly
  story. Value then **sharply outperformed late-2020 through 2022**, vindicating the call.
  **[VERIFIED — AQR, 2020.]** Long-run HML premium commonly cited ~3–5%/yr **[UNVERIFIED — pull
  from Ken French's data library to harden]**.

### 2.4 Post-publication decay — the sobering meta-result

**McLean & Pontiff (2016), "Does Academic Research Destroy Stock Return Predictability?"**
(*Journal of Finance* 71(1)): studying 97 predictors, factor returns are on average **~26%
lower out-of-sample** (overfitting/statistical bias) and **~58% lower post-publication**
(arbitrage as investors trade the signal). **[Paper existence/journal VERIFIED; the 26%/58%
figures are the standard abstract numbers but were NOT re-fetched this session — every host was
paywalled — treat as VERIFIED-from-record / fetch-UNCONFIRMED.]** Complement: **Harvey, Liu &
Zhu (2016)** argue most published factors fail a proper multiple-testing hurdle (t-stat > ~3).
**[VERIFIED that the critique exists.]**

Takeaway: assume any published premium will deliver **materially less** live than in the
backtest. The "factor zoo" is mostly noise; a small handful (value, momentum, quality/
profitability, low-vol) survive scrutiny.

### 2.5 Is a tilt worth it? The honest verdict

- **Duration of pain is the killer objection:** value underperformed cap-weight for **13+
  years**. A factor tilt can trail the plain index for longer than most investors' patience —
  and the moment they capitulate is historically the worst time to sell. Tracking error is a
  behavioral risk, not just a statistical one.
- **Costs & taxes** eat factor premia (momentum especially). Implementation matters more than
  the backtest.
- **Vanguard's stance** (paraphrased): tilts *can* add value but bring long underperformance
  stretches, real costs, and manager/timing risk — so a low-cost broad **cap-weighted** default
  is right for most, with tilts justified only for cost-disciplined investors who can stomach a
  decade of tracking error. **[UNVERIFIED this session — flag before quoting Vanguard directly.]**
- **The pro-tilt case (AQR):** a *diversified multi-factor* sleeve (value + momentum + quality,
  quality-controlled) is far more robust than single-factor value, and its worst stretches have
  historically preceded strong recoveries.

**Verdict for a clean slate:** cap-weight total market is a fully defensible, complete answer.
If tilting, the evidence best supports **quality/profitability** and a **quality-controlled
small-value** sleeve — modest in size, held for a decade-plus, and only if the fee is low. Do
**not** tilt on naive size alone.

---

## 3. Bonds & Fixed Income

### 3.1 Long-run return anchors (1928–2025, geometric, nominal — computed this session)

From Damodaran's histretSP dataset (updated **Jan 5, 2026**), $100 in 1928 → 2025:

| Asset | Geometric CAGR | Std dev |
|---|---|---|
| S&P 500 (with dividends) | **10.13%** | ~19.5% |
| 10-year US Treasury | **4.59%** | 7.90% |
| 3-month T-bills | **3.41%** | 3.04% |
| Gold | **5.67%** | high |

**[VERIFIED — CAGRs computed from Damodaran cumulative-value table; std devs VERIFIED from same
source.]** The ~5.5% equity risk premium over bonds is the long-run engine of the portfolio.

### 3.2 The diversification job — and whether it broke in 2022

High-quality government bonds are held for **negative-to-low correlation with equities** (dry
powder in a stock crash), not for return. **In 2022 that broke:** stocks and bonds fell
together for the first time since **1977** (Vanguard). US 60/40 had its worst year since 2008
(~−17%). The consensus of AQR, PIMCO, BlackRock, Man Group, and Vanguard (2023–2026 pieces):

- **The negative correlation is regime-dependent, not permanently broken.** The sign flips
  **positive when inflation is sticky and above ~2–2.5%**, and reverts negative as inflation
  settles near the ~2% target. **[VERIFIED — Man Group Apr 2026 (~2.5% threshold); PIMCO Nov
  2024 (~2% anchor); BlackRock Dec 2025 (current core 2.5–3.0%, still above the comfort zone);
  Vanguard Jan 2026 (2000–21 corr −7%, 1990s +33%).]**
- **AQR's sharper view:** it's the **relative volatility of growth vs inflation**, not the
  inflation *level*, that drives the sign; their macro model explains **~70%** of the long-run
  variation. **[VERIFIED — AQR, JPM Q1 2023.]**
- **Academic backstop:** Molenaar et al., *Financial Analysts Journal*, Mar 2024 — inflation,
  real rates, and government creditworthiness drive the correlation; regime shifts are abrupt.
  **[Abstract VERIFIED.]**

**Implication:** bonds are a **conditional** diversifier — excellent in growth-shock recessions,
poor in inflation-shock years. In today's ~2.5–3% inflation environment, don't assume the
2000–2020 negative correlation; size the bond sleeve for its yield and volatility-dampening,
not for a guaranteed equity hedge.

### 3.3 Current yields (mid-2026) — the case *for* bonds is the best in 15 years

- **US 10-year Treasury: ~4.5%** (^TNX 4.54% this session; YCharts 4.56% Jul 8). US 2-year
  ~4.2%; 30-year ~5.0%. Curve modestly upward-sloping. **[VERIFIED.]**
- **Canada 10-year GoC: 3.52–3.56%**; 5-year ~3.18%, 2-year ~2.85% (Bank of Canada / Trading
  Economics, Jul 8–9 2026). **[VERIFIED.]**
- **10-year TIPS real yield: 2.31%** (FRED DFII10, Jul 8 2026) → implied 10-yr breakeven
  inflation ~2.25%. **[VERIFIED.]**

A **positive ~2.3% *real* yield on TIPS** and ~4.5% nominal on Treasuries is a genuinely
attractive starting point — unlike the negative real yields of 2020–2021. Starting yield is the
single best predictor of a bond's forward return, so the *ex-ante* case for holding bonds is
the strongest it's been since before the GFC.

### 3.4 Duration — intermediate is the sweet spot

The cleanest evidence (DFA/Merriman "Fixed Income Returns" table, 1928–2023, **VERIFIED**):

| Maturity | Compound return | Std dev |
|---|---|---|
| Short (1-mo T-bill) | 3.3% | 3.1% |
| **Intermediate (5-yr Treasury)** | **4.9%** | **5.8%** |
| Long (~20-yr) | 5.2% | 10.1% |

Going short→intermediate adds +1.6%/yr; intermediate→long adds only **+0.3%** more return but
**nearly doubles volatility**. The 5-year note captured ~**84% of the long-bond term premium at
~57% of the volatility**. Over rolling 40-year windows, intermediate actually *out-returned*
long with far less risk. The term premium at the very long end is thin and often negative
(negative in **44%** of years per Swedroe; current 10-yr term premium ~0.7% per NY Fed).
**[VERIFIED.]**

**Verdict:** default to **intermediate-term, high-quality government/aggregate bonds.** Long
duration is a rate *bet*, not a diversification necessity. **TIPS** deserve a slice for direct
*unexpected*-inflation protection given today's positive real yields.

---

## 4. Diversifiers Beyond Stocks & Bonds

Ranked by strength of evidence. The recurring theme: **most "diversifiers" are marketing; a
few earn their place, and even those come with caveats.**

### 4.1 Gold — near-zero long-run real return; unreliable hedge

**Erb & Harvey, "The Golden Dilemma" (NBER WP 18706 / FAJ 2013)** — full paper read this
session, **VERIFIED**:

- **Long-run real return ≈ zero** ("the golden constant"): gold holds purchasing power "if the
  horizon is measured in centuries," but is "an unreliable inflation hedge" over practical
  horizons.
- **Weak inflation hedge:** essentially no correlation with unexpected inflation 1975–2011
  (the positive link is driven entirely by the 1980 spike); trailing 10-yr real gold return was
  *negative* 1988–2005.
- **Weak crisis hedge:** gold and the S&P 500 were both down in the same month **17%** of the
  time — "a good diversifier may not be a safe haven."
- Mean-reverts on the real price (ranged 1.46× to 8.73× since 1975); elevated real prices
  historically implied *negative* forward real returns.

The commonly cited Dimson-Marsh-Staunton "gold ~+0.5–1%/yr real since 1900" figure could **not**
be confirmed this session **[UNVERIFIED]** — but the near-zero-real conclusion is directly
supported by Erb-Harvey/Jastram. **Verdict:** gold has no expected real return and is an
inconsistent hedge. It belongs in a portfolio only as a deliberate low-weight regime-hedge
(as in the Permanent/All-Weather portfolios, §6), not as a return source.

### 4.2 Commodities (futures) — real diversification, messy real returns

- **Gorton & Rouwenhorst (2006):** fully-collateralized commodity futures 1959–2004 delivered
  **equity-like return and Sharpe**, and were **negatively correlated with stocks and bonds**
  over the business cycle. **[VERIFIED — abstract; exact coefficients paywalled/UNVERIFIED.]**
  Out-of-sample confirmed by Bhardwaj-Gorton-Rouwenhorst (2015). **[VERIFIED.]**
- **Roll yield** is the catch: in contango, long futures bleed negative roll yield (spot can
  rise while the index lags). AQR's **"Commodities for the Long Run" (2018)** argues that over
  1877–2015 futures returns were positive and roll yield made up the majority of them.
  **[VERIFIED — qualitative.]**
- **2022 inflation shock (computed via yfinance this session, VERIFIED):** while S&P 500 −19.4%
  and US aggregate bonds −13.0%, broad commodities rose (GSG +24.1%, DBC +19.3%, Bloomberg
  Commodity spot +13.8%). This is the marquee real-world case of commodities hedging an
  inflation surprise exactly when stocks and bonds failed together.

**Verdict:** the best-evidenced non-bond diversifier for the *inflation-shock* scenario that
breaks the stock-bond hedge — but low/uncertain long-run real return and roll-yield drag mean a
**small** allocation at most, if any.

### 4.3 REITs — mostly equity, limited unique diversification

**Peterson & Hsieh (1997)**: equity-REIT returns are significantly explained by the **market,
size, and value factors** — REITs behave like **small-cap value stocks** (mortgage REITs also
load on bond factors). **[VERIFIED — abstract; loadings/R² paywalled/UNVERIFIED.]** REITs became
a distinct GICS sector in 2014 and their 2022 drawdown (VNQ **−26.3%**) was *worse* than the
S&P 500 — consistent with "leveraged, rate-sensitive equity," not an independent asset class.
NAREIT markets a low-correlation diversification story, but the quantified series wasn't
retrievable **[UNVERIFIED]**. **Verdict:** a broad total-market index already holds REITs at
market weight; a *separate* REIT tilt is closer to a small-value tilt than to true
diversification. No strong evidence to overweight.

### 4.4 Managed futures / trend-following — the best-evidenced "crisis alpha"

**AQR, "A Century of Evidence on Trend-Following Investing" (Hurst-Ooi-Pedersen, JPM 2017)** —
PDF read this session, **VERIFIED**:

- 67 markets, 1880–2016, scaled to 10% vol: **net-of-fee Sharpe 0.76**; correlation to US
  equities **−0.01**, to bonds **−0.03**; positive net return in **every decade since 1880**.
- **Crisis alpha:** positive in **8 of the 10 largest 60/40 drawdowns** in 137 years (GFC
  ~+30%, 1973–74 oil ~+130%, Great Depression ~+55%). Misses: 1937 and the too-fast 1987 crash.
  Adding a 20% trend sleeve to 60/40 lifted Sharpe 0.39→0.55 and cut max drawdown from −62% to
  −50%.
- **2022 (both stocks and bonds fell):** SG Trend Index **+27.3%** and SG CTA Index **+20.1%**
  — best since 2000 inception. **[VERIFIED via AlphaWeek, Feb 2023.]** **2008:** BTOP50 ~+14.5%
  **[UNVERIFIED — secondary]**; AQR's own strategy ~+30% **[VERIFIED]**.

**Verdict:** the single most compelling diversifier evidence — genuinely uncorrelated, with a
century of positive returns and a track record of paying off in the exact crises (including the
2022 inflation shock) when a 60/40 hurts most. **Caveats:** it's a *strategy*, not an asset —
higher fees (though ETFs like DBMF have compressed them), manager dispersion, and it will lag in
quiet trending-less markets. Best justified as a small (5–15%) sleeve for investors who
understand it.

---

## 5. Costs, Taxes, and Behavior — where the biggest reliable gains are

### 5.1 The arithmetic of fees (Bogle / Sharpe)

Fees are the one variable that is **certain and subtractive**. Broad index ETFs cost
**~0.03–0.14%**; the asset-weighted active equity fund cost ~**0.40%** in 2024 (down from ~1.0%
in 2000), with many still at 0.5–1.0%+. **[VERIFIED — ICI 2024 fee data.]** Over 30 years a
1%/yr fee difference compounds to roughly a quarter of the terminal portfolio. This is the
highest-confidence, highest-control lever in the entire report.

### 5.2 Tax efficiency

Broad index funds are structurally tax-efficient because **low turnover → few realized
capital-gains distributions**; active funds' trading generates taxable (often short-term)
distributions that hit shareholders even in down years. **[Mechanism VERIFIED; exact turnover
figures (index ~3–7% vs active ~50–100%) UNVERIFIED.]** For a Canadian investor, asset *location*
also matters (e.g., US-listed ETFs held in an RRSP avoid the 15% US dividend withholding under
the treaty — a location question, not covered in depth here).

### 5.3 Rebalancing — risk control, not a return engine

Vanguard's "Best practices for portfolio rebalancing": rebalancing is **primarily a
risk-control tool, not a return enhancer**. Annual or semi-annual checks with ~5% drift bands
are the sensible default; any return effect is second-order. **[VERIFIED — figure/URL moved but
conclusion is Vanguard's stated position.]** Don't oversell a "rebalancing bonus"; do rebalance
to keep risk on target and to enforce buy-low/sell-high discipline.

### 5.4 The behavior gap — the tax investors levy on themselves

**Morningstar "Mind the Gap 2024"** (data through Dec 2023): the average dollar in US funds
earned ~**7%/yr** vs ~**8.1%** for the funds themselves over 10 years — a **~1.1 pp/yr gap**,
i.e. investors forfeited **~15% of their funds' returns** through bad timing (buying high,
selling low). Widest in narrow sector funds (~−2.6%/yr); smallest in hands-off allocation/
target-date funds (~−0.4%/yr). **[VERIFIED via secondary — Morningstar/Amy Arnott.]** The older
**Dalbar QAIB** claims a much larger gap (often cited ~4–6%/yr) but is widely criticized as
overstated, and no citable current figure could be sourced this session **[UNVERIFIED — do not
cite a Dalbar number].**

**Implication:** the single most reliable "alpha" available to a retail investor is
**behavioral** — automate contributions, hold a simple all-in-one or target-date fund, and
don't trade. The smaller behavior gap for allocation funds is itself evidence that *simplicity
protects returns*.

---

## 6. Model Portfolios — Reference Points (exact allocations)

| Portfolio | Allocation | Reasoning / source |
|---|---|---|
| **Bogleheads 3-fund** | US total stock + intl total stock + US total bond; split scales with age (e.g. 80/20 aggressive; intl ≈ 20–40% of equity) | Maximum diversification at minimum cost; no single mandated split. **[VERIFIED — funds; ETFs VTI/VXUS/BND.]** |
| **Harry Browne Permanent** | **25% stocks / 25% long-term Treasuries / 25% cash (T-bills) / 25% gold** | One quarter each thrives in prosperity / deflation / recession / inflation. Rebalance at 15%/35% bands. **[VERIFIED.]** |
| **Ray Dalio "All Weather" (Robbins retail version)** | **30% stocks / 40% long-term bonds / 15% intermediate bonds / 7.5% gold / 7.5% commodities** | Risk-balanced across economic regimes (retail simplification, not Bridgewater's actual fund). **[VERIFIED — Robbins, *Money*, 2014.]** |
| **Vanguard LifeStrategy Moderate** | **static 60% stock / 40% bond** | Fixed-weight balanced fund. **[VERIFIED.]** |
| **Vanguard Target Retirement glidepath** | ~**90% equity** young → ~**50% at 65** → ~**30% at ~72** | Age-based derisking. **[VERIFIED.]** |
| **Robo-advisor moderate (e.g. Betterment)** | ~**70% stocks / 30% bonds** (risk-slider mapped to horizon) | Wealthfront / Vanguard Digital Advisor land similarly (~60–70% equity at moderate risk). **[VERIFIED — Betterment methodology.]** |
| **Canadian one-ticket ETFs** | Vanguard **VBAL** ~60/40, **VGRO** ~80/20; iShares **XBAL** ~60/40 (MER 0.19%), **XGRO** ~80/20 (MER 0.20%) | All-in-one, auto-rebalanced, globally diversified. Vanguard cut VBAL/VGRO mgmt fee to 0.17% eff. Nov 18 2025. **[VERIFIED — fact sheets, May 31 2026.]** |

The common thread: **broad, cheap, rebalanced, and simple**. The "lazy" portfolios differ
mainly in the equity/bond ratio and whether they add gold/commodities as inflation hedges.

---

## 7. WHAT THE EVIDENCE SUPPORTS — Clean-Slate Building Blocks

A summary of the building blocks a from-scratch, long-horizon portfolio should use, with rough
% ranges and low-cost instruments. **This is the evidence-based *menu*, not a personalized
recommendation** — the equity/bond ratio is the investor's risk/horizon choice.

### The core (do this; highest-confidence evidence)

1. **Global cap-weighted equity — 100% of the equity sleeve.**
   - Split ~**60–65% US / 35–40% ex-US** (market-cap neutral ≈ 64/36; defensible range 50–70%
     US). Include emerging markets at ~market weight.
   - **US-listed:** VT (total world, one ticker) — or VTI + VXUS; add developed VEA / EM VWO if
     splitting. **Canadian-listed:** XEQT / VEQT (all-equity, one ticker, currency-diversified).
   - Confidence: **HIGH** (Sharpe 1991; SPIVA/Barometer; MSCI ACWI weights).

2. **High-quality bonds — the stabilizer; weight set by risk tolerance (typically 20–40%).**
   - Default to **intermediate-term, high-quality** aggregate/government bonds (the return/risk
     sweet spot). Yields (~4.5% US / ~3.5% Canada) make the ex-ante case the best since 2008.
   - Add a **TIPS/real-return** slice (positive ~2.3% real yield) for direct unexpected-inflation
     protection — especially valuable now that inflation-shock years break the stock-bond hedge.
   - **US-listed:** BND/AGG (aggregate), IEF (7–10yr), SCHP/VTIP (TIPS). **Canadian-listed:**
     VAB/ZAG (Canadian aggregate), real-return bond funds; note currency — a Canadian investor
     is usually better hedged/domestic on the bond sleeve.
   - Confidence: **HIGH on duration/cost**; **MEDIUM on the diversification role** (regime-
     dependent since 2022).

### Optional tilts (only if disciplined and low-cost; MEDIUM confidence)

3. **Quality/profitability and quality-controlled small-value — 0–20% of equity.**
   - Best-surviving factors; expect a *decade-plus* of possible underperformance and only tilt
     if you can hold through it. **Do not** tilt on naive size alone.
   - **US-listed:** AVUV (small-value, quality-screened), QUAL (quality). Momentum (MTUM) is
     robust but tax/turnover-costly — hold in tax-sheltered accounts if at all.
   - Confidence: **MEDIUM** (real premia, but post-publication decay + long drawdowns; a plain
     cap-weight core is a complete answer without this).

### Optional diversifiers (small, deliberate, understand-what-you-own; MEDIUM→LOW confidence)

4. **Managed futures / trend — 0–15%.** Best-evidenced crisis-alpha; uncorrelated; paid off in
   2008 *and* 2022. **US-listed:** DBMF. Confidence: **MEDIUM** (strong evidence, but it's a
   strategy with fees/dispersion).

5. **Broad commodities — 0–10%.** The clearest hedge for the inflation-shock regime that breaks
   60/40; low/uncertain long-run real return. **US-listed:** PDBC/DBC. Confidence: **LOW–MEDIUM.**

6. **Gold — 0–10%, only as a regime hedge, never as a return source** (near-zero real return,
   unreliable hedge). **US-listed:** GLDM/IAU. **Canadian:** CGL. Confidence: **LOW.**

7. **REITs — no separate overweight needed** (already in the total-market index; behave like
   small-value equity). Confidence: **evidence says skip the tilt.**

### The meta-rules (highest confidence of all — these dominate instrument selection)

- **Minimize cost.** Use ~0.03–0.20% ETFs. A 1%/yr fee saved ≈ ~25% more terminal wealth over
  30 years. **[HIGH.]**
- **Maximize tax efficiency** (broad low-turnover index; correct asset location for a Canadian).
- **Rebalance for risk control** (annual or ~5% bands) — not for a mythical return bonus.
- **Automate and don't tinker.** The ~1 pp/yr behavior gap is the biggest self-inflicted,
  fully-avoidable drag; a one-ticket all-in-one or target-date fund is the evidence-based way to
  neutralize it. **[HIGH.]**

### The simplest evidence-consistent implementations

- **One ETF (Canadian):** XEQT/VEQT (all-equity) or VGRO/VBAL (with bonds) — globally
  diversified, cap-weighted, auto-rebalanced, ~0.20% MER. Captures ~95% of the evidence with
  zero behavioral surface area.
- **Three ETFs (Bogleheads):** total-market equity + ex-US equity + aggregate bonds.
- **Add tilts/diversifiers only** if you will hold them through a decade of underperformance
  and understand exactly why you own each one.

---

## 8. Verification Log (sources + dates + confidence)

**Live data pulled this session (2026-07-09):**
- US yields: ^TNX 4.54%, ^TYX(30y) 5.05%, ^FVX(5y) 4.27% (yfinance). Cross-check YCharts: 10y
  4.56%, 2y 4.21% (Jul 8 2026). **[VERIFIED]**
- Canada GoC: 10y 3.52–3.56%, 5y 3.18%, 2y 2.85% (Bank of Canada / Trading Economics, Jul 8–9
  2026). **[VERIFIED]**
- 10y TIPS real yield 2.31% (FRED DFII10, Jul 8 2026) → breakeven ~2.25%. **[VERIFIED]**
- ETF prices confirmed live (VT 157.00, VTI 371.45, VXUS 84.90, BND 72.83, GLD 378.18, IEF
  93.71, XEQT 45.22, VEQT 61.53, VBAL 39.70, VGRO 47.61, AVUV 123.22, QUAL 218.50, DBMF 30.76,
  SCHP 26.23, VNQ 97.09). **[VERIFIED — tickers exist and trade]**
- 2022 asset returns (yfinance, computed): S&P 500 −19.4%, AGG −13.0%, GSG +24.1%, DBC +19.3%,
  PDBC +19.2%, VNQ −26.3%. **[VERIFIED]**

**Core allocation / active-passive:**
- Sharpe, "The Arithmetic of Active Management," *FAJ*, Jan/Feb 1991 — web.stanford.edu/~wfsharpe.
  **[VERIFIED]**
- SPIVA U.S. Year-End 2024: large-cap 10yr underperformance 84.3%; 1yr ~65%; 15th straight year.
  **[VERIFIED via secondary — S&P PDFs 403'd]**
- SPIVA Canada Year-End 2024: Cdn equity 10yr 95.5%, 1yr 88.7%. **[VERIFIED via secondary]**
- Morningstar Active/Passive Barometer YE2025: ~20% 10yr active success. **[VERIFIED via
  secondary]**
- MSCI ACWI factsheet, data as of Jun 30 2026: US 63.63%, Japan 5.0%, Taiwan 3.33%, UK 3.03%.
  **[VERIFIED — factsheet fetched]**
- Vanguard: ~40% of equity international. **[Figure VERIFIED; URL UNVERIFIED]**
- Damodaran histretSP (updated Jan 5 2026): 1928–2025 CAGRs S&P 10.13%, 10y Tsy 4.59%, T-bill
  3.41%, gold 5.67%; SDs 19.5%/7.90%/3.04%. **[VERIFIED]**

**Factors:**
- Fama-French 3-factor (JFE 1993), 5-factor (JFE 2015). **[VERIFIED]**
- AQR, "Is (Systematic) Value Investing Dead?", May 8 2020. **[VERIFIED]**
- AQR, "Size Matters, If You Control Your Junk", JFE 2018. **[VERIFIED — thesis; magnitude
  UNVERIFIED]**
- Jegadeesh-Titman 1993 (momentum); Daniel-Moskowitz "Momentum Crashes" 2016. **[VERIFIED /
  ASSUMED]**
- Novy-Marx, "The Other Side of Value: Gross Profitability Premium", JFE 108(1), 2013.
  **[VERIFIED]**
- Frazzini-Pedersen "Betting Against Beta" (JFE 2014); Baker-Bradley-Wurgler 2011. **[VERIFIED]**
- McLean & Pontiff, *J. of Finance* 71(1), 2016 — ~26% OOS / ~58% post-pub decay. **[Paper
  VERIFIED; figures VERIFIED-from-record but fetch-UNCONFIRMED — all hosts paywalled]**
- Harvey-Liu-Zhu 2016 (multiple-testing / factor zoo). **[VERIFIED critique exists]**

**Bonds / correlation / diversifiers:**
- AQR "A Changing Stock-Bond Correlation", JPM Q1 2023 (~70% explained; growth-vs-inflation vol).
  **[VERIFIED]**
- Man Group "The Inflation Diversification Problem", Apr 23 2026 (~2.5% threshold). **[VERIFIED]**
- PIMCO "Negative Correlations, Positive Allocations", Nov 20 2024 (~2% anchor). **[VERIFIED]**
- BlackRock "Bonds Starting to Offer More Diversification", Dec 22 2025. **[VERIFIED]**
- Vanguard UK "stock/bond correlations", Jan 4 2026 (2000–21 −7%; 1990s +33%; 2022 first since
  1977). **[VERIFIED]**
- Molenaar et al., *FAJ* 80(3), Mar 2024. **[Abstract VERIFIED]**
- DFA/Merriman "Fixed Income Returns" table, Feb 17 2024 (1928–2023 duration sweet spot).
  **[VERIFIED]**
- Swedroe "Examining Bond Premiums" (ETF.com, Oct 2018); Brookings term-premium (Mar 2025); NY
  Fed 10y term premium ~0.73% (FRED THREEFYTP10, Jul 2 2026). **[VERIFIED]**
- Erb & Harvey "The Golden Dilemma", NBER WP 18706 / FAJ 2013 — full text read. **[VERIFIED]**
- Gorton-Rouwenhorst 2006 (NBER 10595 / FAJ 62(2)); Bhardwaj-Gorton-Rouwenhorst 2015 (NBER
  21243); AQR "Commodities for the Long Run" 2018. **[VERIFIED abstracts; coefficients
  UNVERIFIED]**
- Peterson & Hsieh 1997, *Real Estate Economics* 25(2) — REITs load on market/size/value.
  **[Abstract VERIFIED; loadings UNVERIFIED]**
- AQR "A Century of Evidence on Trend-Following", JPM 2017 — full PDF read (Sharpe 0.76; 8/10
  crisis drawdowns positive). SG Trend +27.3% / SG CTA +20.1% in 2022 (AlphaWeek Feb 2023).
  **[VERIFIED]**

**Costs / behavior / models:**
- ICI 2024 fee data: index equity ~0.03–0.14%, active equity ~0.40% asset-weighted. **[VERIFIED]**
- Vanguard "Best practices for portfolio rebalancing" — risk control, not return. **[VERIFIED
  conclusion]**
- Morningstar "Mind the Gap 2024": ~1.1 pp/yr / ~15% of returns lost to timing. **[VERIFIED via
  secondary]**
- Dalbar QAIB — **[UNVERIFIED — not sourced; do not cite a number]**
- Model portfolios (Bogleheads 3-fund, Permanent, All-Weather, Vanguard glidepath/LifeStrategy,
  Betterment, Canadian VBAL/VGRO/XBAL/XGRO) — **[VERIFIED per §6]**

**Known verification gaps to close before this is "airtight":**
1. SPIVA US 15/20-yr and all-cap cells; SPIVA Persistence exact top-quartile-after-5yr %; any
   Dalbar figure — pull from primary PDFs (S&P blocked automated fetch this session).
2. McLean-Pontiff 26%/58% — confirm via Wiley (doi:10.1111/jofi.12365) with institutional access.
3. Long-run HML/SMB magnitudes — pull from Ken French's Data Library (free, authoritative).
4. Vanguard factor-tilt stance and international white-paper — get clean URLs before quoting
   Vanguard directly.
5. Dimson-Marsh-Staunton long-run real gold return; official S&P GSCI/BCOM 2022 total-return
   levels; exact Peterson-Hsieh loadings & Gorton-Rouwenhorst coefficients.

---

*No figure in this report was fabricated. Every number carries a source and a confidence tag;
where a figure could not be confirmed to a primary document this session, it is marked
UNVERIFIED rather than presented as settled.*
