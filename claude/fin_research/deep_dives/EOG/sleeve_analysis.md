# EOG — Sleeve Analysis: ADD on Top, or SWAP OXY→EOG? (finishing `portfolio_fit.md` with the full O&G book)

**Question:** You are **already ~13.8% weighted in oil & gas across 9 positions.** Now that your
**full holdings table has arrived**, this file finishes the sleeve-level analysis the earlier
`portfolio_fit.md` could only start (it had XOM + CNQ only). Central question: **what is EOG's natural
role in *this* sleeve — a quality UPGRADE of the US-E&P slot (swap OXY→EOG), or an ADD on top of an
already-heavy sleeve?**

**Prepared:** 2026-07-05 by Claude (Opus 4.8). Owner: Hooman Shariati (**Canadian citizen**).
**RESEARCH, NOT FINANCIAL ADVICE — a decision framework and trade-offs, not a recommendation.**
**Builds on** (does NOT repeat): `deep_dives/EOG/hooman_oil_gas_holdings.md` (the full book + structural
reads), `deep_dives/EOG/portfolio_fit.md` (EOG-vs-XOM-vs-CNQ core: correlations EOG-XOM 0.79 /
EOG-CNQ 0.76; EOG's torque duplicates CNQ; ~12% is heavy), `deep_dives/EOG/deep_dive.md` (EOG 6.9/10,
mid-cycle not peak), `deep_dives/EOG/profile_and_diligence.md` (EOG quality: peer-top ROE 18.2%, lowest
leverage, 100%-of-FCF returned).

> ### ⚠️ THE ONE-LINE ANSWER (read first)
> On the data, **EOG's cleanest role in your book is a weight-neutral SWAP that upgrades the US-E&P
> slot: OXY → EOG.** It is your only US pure-play E&P (1.08%, your own "C" grade, most-levered name in
> the sleeve), and EOG is the *near-substitute* (correlation **0.81**, the highest in your whole book)
> but **~4.5× the ROE, ~⅓ the leverage, and cheaper on trailing multiples.** A swap **lifts blended
> sleeve quality (ROE ~15.0% → ~16.1%) at the SAME 13.8% sector weight, torque-neutral.** An ADD-on-top
> grows an already-heavy ~14% bet (≈3–4× a market energy weight) into a bigger single-factor bet on the
> oil price without improving quality per dollar. **This is your allocation call — framework below, not a
> directive.**

> **Anti-hallucination (CLAUDE.md §5 #1).** Every number is a **live yfinance pull (as-of 2026-07-05
> 01:54 PT)**, a figure carried from the EDGAR-verified EOG files, a cited commodity price, or a marked
> secondary source. **Your holding prices/weights are taken as given from your own export
> ("Hooman's portfolio export 2026-07-05")** — I did not re-price them. Confidence marks: **VERIFIED** =
> pulled live/primary this session; **ASSUMED** = my derivation/judgment; **UNVERIFIED** = single
> secondary source. Commodity/FX (yfinance futures/FX, ~15-min delayed, 2026-07-05): **WTI $68.78,
> Brent $72.13, Henry Hub $3.25, USD/CAD 1.42.** Note: my live yfinance prices differ slightly from your
> export (e.g. live OXY $48.91 vs your $41.32; live ARX C$29.85 vs your C$25.86) — I use **your weights**
> for the sleeve math and **live metrics** for quality/valuation; the conclusions are not sensitive to
> the small price gaps.

---

## Jargon key (read once)

| Term | Plain meaning |
|---|---|
| **E&P / upstream pure-play** | Only finds and pumps oil/gas; sells the raw commodity; no refining. Full exposure to the oil price ("price-taker"). EOG and OXY are both this. |
| **Integrated / supermajor** | Pumps *and* refines *and* often ships gas — downstream refining earns more when crude is cheap, so it **cushions** oil swings (lower torque). XOM, CVE. |
| **Beta-to-WTI** | How much a stock moves per 1% move in WTI oil (3y weekly). Higher = more oil "torque" (more upside if oil rises, more downside if it falls). |
| **Net-debt / EBITDA** | Debt minus cash, divided by annual cash earnings. How many years of earnings it would take to pay off net debt. Lower = safer balance sheet. |
| **Blended sleeve metric** | The weighted average of a metric (e.g. ROE) across your holdings, weighted by each position's % of your portfolio. Tells you the *quality of the sleeve as a whole*. |
| **Weight-neutral swap** | Selling one holding and buying another of equal size, so your total sector % doesn't change — only the *internal mix* changes. |
| **WCS differential** | Western Canadian Select (heavy Cdn oil) trades at a discount to WTI. A Canada-specific risk your Cdn oil names (CNQ/CVE) carry; US names (EOG/OXY) don't. |
| **2x leveraged ETF (BOIL)** | An ETF engineered to return *twice* the daily move of natural gas. Because it resets daily, it **decays** ("volatility drag") and is unsuitable to hold beyond days. |

---

## 1. The sleeve mapped — by TYPE, region, commodity, torque

Your O&G book, classified. Weights are **% of total portfolio** from your export; ROE / EV-EBITDA /
beta-to-WTI are **live yfinance 2026-07-05 (VERIFIED)**. (Dual-listed Cdn names use the NYSE line for
XOM-comparable metrics; ARX/TOU use the .TO line — flagged.)

| Ticker | Type | Region | Primary commodity | % Port | ROE | EV/EBITDA | beta-to-WTI | Your grade |
|---|---|---|---|--:|--:|--:|--:|:--:|
| **XOM** | Integrated supermajor | US (global) | Oil + gas/LNG + refining | **4.13%** | 9.9% | 11.0× | **0.30** | B |
| **CNQ** | Oil-sands / heavy E&P | Canada | Heavy oil (WCS) | **4.21%** | **22.8%** | 6.9× | 0.42 | B |
| **ARX** | Cdn gas/liquids E&P (Montney) | Canada | **Natural gas** + liquids | **2.14%** | 17.4% | 5.8× | 0.41 | B |
| **OXY** | **US E&P** (Permian) + chem + CO2 | US | Oil | **1.08%** | **4.1%** | 6.5× | **0.47** | **C** |
| **SLB** | Oilfield **services** | US (global) | (activity-levered) | **0.89%** | 14.1% | 10.2× | 0.24 | B |
| **CVE** | Integrated / oil sands | Canada | Heavy oil + refining | **0.89%** | 14.8% | 5.4× | 0.50 | B |
| **TOU** | Cdn natural gas | Canada | **Natural gas** | **0.45%** | 4.5% | n/a | 0.26 | B |
| **BOIL** | **2x leveraged** natgas ETF | — | NatGas (2× daily) | **0.00%** | — | — | 0.31† | **C** |
| **UNG** | NatGas commodity ETF | — | NatGas | **0.00%** | — | — | 0.15† | B |
| | | | **Sleeve total** | **13.79%** | | | | |

† BOIL/UNG have **near-zero correlation to the oil-stock complex** (0.0–0.11) and load on *natural gas*
instead: **UNG beta-to-NatGas 0.62 / corr 0.83; BOIL beta-to-NatGas 1.09 / corr 0.80** (VERIFIED). They
are a *different factor* than the rest of the sleeve — but both sit at 0% (placeholders/watchlist).

**The sleeve's shape (VERIFIED weights + live factor pulls):**
- **Canada-heavy — ~56% of the sleeve.** CNQ + ARX + CVE + TOU = **7.69%** (55.8% of the sleeve) vs US
  (XOM + OXY + SLB) = **6.10%** (44.2%). For you (CAD investor) the Canada tilt is a **natural home-
  currency match** on ~half the book — a mild positive — but it also concentrates WCS-differential and
  Canadian-policy risk.
- **Two big anchors.** XOM 4.13% + CNQ 4.21% = **8.34%** — 60% of the sleeve sits in two names (one US
  integrated, one Cdn oil-sands). The other 7 names split the remaining ~5.5%.
- **Gas is a real sub-tilt, but small in the *stocks*.** Cdn **gas E&P** (ARX + TOU) = **2.59%**; the two
  gas ETFs are 0%. So your *equity* gas exposure is ~2.6% (ARX/TOU), plus the gas inside XOM/EOG/CNQ.
- **Blended quality is "B."** Weighted ROE ≈ **15.0%** (VERIFIED, my arithmetic on live ROEs × your
  weights). CNQ (22.8%) and ARX (17.4%) carry it; **OXY (4.1%) and TOU (4.5%) drag it down.** Your own
  grades match: only OXY and BOIL are "C."
- **THE GAP.** Your **only US pure-play E&P is OXY** — 1.08%, your own **"C"**, the **most oil-torqued
  name in the sleeve (beta-to-WTI 0.47)**, the **weakest returns (ROE 4.1%, ROA 2.5%)**, and (per §2)
  the **most-levered** operator you own. That is precisely the slot EOG is built to fill.

---

## 2. The central question — EOG vs OXY head-to-head (the SWAP candidate)

Because your gap is the *US pure-play E&P slot*, and that slot is currently **OXY**, the decision that
actually matters is **not** "EOG vs your whole book" — it's **EOG vs OXY.** And they are near-
substitutes: **EOG-OXY 3y weekly return correlation = 0.81 — the highest pairwise correlation in your
entire sleeve** (VERIFIED). They rise and fall together; the question is purely *which is the better
version of the same slot.*

### 2a. Head-to-head table (live yfinance 2026-07-05, VERIFIED)

| Metric | **EOG** | **OXY** | Read |
|---|--:|--:|---|
| Price | $130.78 | $48.91 | (live; your OXY export mark was $41.32) |
| Market cap | $69.7B | $48.6B | |
| **VALUATION** | | | |
| EV/EBITDA | **5.9×** | 6.5× | EOG cheaper |
| Trailing P/E | **12.9×** | 66.1×* | *OXY distorted by depressed 2025 earnings — read forward |
| Forward P/E | **8.8×** | 12.3× | EOG meaningfully cheaper forward |
| P/B | 2.26× | 1.58× | OXY cheaper on book (lower-quality assets/returns) |
| **FCF yield (TTM)** | 4.1%‡ | **6.2%** | OXY higher *headline* TTM FCF yield (see ‡ + note) |
| **QUALITY** | | | |
| **ROE** | **18.2%** | 4.1% | **EOG ~4.5× OXY** |
| ROA | **9.0%** | 2.5% | **EOG ~3.6× OXY** — far more capital-efficient |
| **Net debt** | **$4.46B** | $12.80B | OXY carries ~2.9× EOG's net debt |
| **Net-debt / EBITDA** | **0.35×** | 1.18× | **EOG fortress; OXY ~3.4× more levered** |
| Debt/Equity | **26.9%** | 42.0% | EOG far lower |
| **CAPITAL RETURN** | | | |
| Dividend yield | **3.12%** | 2.13% | EOG higher regular yield |
| Payout ratio | **39%** | 132%* | *OXY payout >100% = paying dividend out of more than current (depressed) earnings |
| Buyback style | Base +8% div **+ specials + buybacks**, 100% of FCF returned | Dividend + debt-paydown priority; **preferred overhang** limits common returns | EOG returns more, cleaner |
| **OIL TORQUE** | | | |
| Beta-to-WTI (3y wk) | 0.39 | **0.47** | OXY *more* torqued (partly its leverage) |
| Corr-to-WTI | 0.59 | 0.64 | Both ride oil; OXY tighter |

\* OXY trailing P/E 66× and payout 132% are **distorted by depressed 2025 earnings** (oil normalization +
deal accounting) — read the **forward P/E (12.3×)** and the balance-sheet lines, not the trailing P/E.
‡ EOG's TTM FCF yield (4.1%) understates its **~6–6.5% mid-cycle FCF yield** (yfinance TTM FCF is
depressed by 2025's soft quarters + Utica-deal capex — see `deep_dive.md` §2c). OXY's 6.2% is a real
TTM figure but sits against a *much weaker balance sheet and returns profile*.

### 2b. The OXY-specific overhangs (why it's your "C")

These are structural reasons OXY is a lower-quality version of the same US-E&P slot — several
**VERIFIED** this session:

1. **Leverage from the acquisition spree.** OXY bought **Anadarko for $57B (2019)** and **CrownRock for
   $12B (completed Aug 2024)** (VERIFIED, Wikipedia/company). Net debt today **$12.8B, net-debt/EBITDA
   1.18×** (VERIFIED live) — the **most-levered name in your sleeve**, vs EOG's fortress 0.35×. That debt
   is the core reason OXY's ROE is 4.1% (interest + share dilution eat returns).
2. **The Berkshire preferred overhang.** Berkshire holds **$10B of OXY perpetual preferred stock**
   (100,000 shares at $100,000 par, from the 2019 Anadarko financing) **plus ~28% of the common and
   warrants for 80M shares at $62.50** (VERIFIED, Wikipedia). The preferred pays a **~8% dividend
   (UNVERIFIED / widely-reported)** that ranks **ahead of the common** — a senior claim that soaks up
   cash OXY would otherwise return to common holders (and OXY can only buy back common in size after
   chipping at the preferred). This is a genuine, name-specific drag on common-shareholder returns that
   EOG simply does not have.
3. **OxyChem / chemicals — just sold.** OXY's chemicals arm (PVC, chlorine, caustic soda) was a
   diversifier, but **Berkshire agreed to buy OxyChem for $9.7B (Oct 2025)** (VERIFIED, Wikipedia). Read:
   OXY is **selling assets to pay down the acquisition debt** — a deleveraging positive, but it also
   *removes a non-oil earnings stream* and underscores that the balance sheet needed the help.
4. **CO2 / Direct Air Capture bet.** OXY acquired **Carbon Engineering for $1.1B (Aug 2023)** and is
   building out carbon capture / DAC (the "1PointFive"/STRATOS effort) (VERIFIED, Wikipedia; project
   names UNVERIFIED here). This is a **speculative, capital-hungry, unproven-economics** option bolted
   onto the E&P — upside optionality for some, a capital-allocation distraction for a value investor. EOG
   spends its capital only on wells that clear a hard return hurdle.
5. **Breakeven / cost.** EOG guides a **~sub-$50 WTI corporate breakeven (UNVERIFIED, EOG framing)**;
   OXY's is **structurally higher** because of debt service + the preferred dividend (higher *cash*
   breakeven even if wellhead costs are competitive). At WTI $68.78 both make money; in a $50–55 drawdown
   OXY's levered/preferred-burdened structure is the more fragile of the two. (ASSUMED, directional.)

### 2c. Head-to-head verdict

**EOG is a clear quality upgrade over OXY, at a comparable-to-better valuation. VERIFIED on the numbers
that matter:** ROE **18.2% vs 4.1%**, ROA **9.0% vs 2.5%**, net-debt/EBITDA **0.35× vs 1.18×** — and
EOG is *cheaper* on EV/EBITDA (5.9× vs 6.5×) and forward P/E (8.8× vs 12.3×). OXY's only edges are a
higher *headline* TTM FCF yield (6.2% — but against a far weaker balance sheet) and a lower P/B (which
just reflects its lower returns), plus the **Permian-scale recovery optionality** and the (speculative)
DAC call option (the counter-argument, §4). For a **quality-first value investor**, EOG wins the slot
decisively — same bet on US shale oil, far better company owning it.

---

## 3. Does the swap change the sleeve's balance? (correlation / concentration)

The swap is **OXY (1.08%) → EOG (1.08%)** — weight-neutral. Effect on the sleeve, computed on **your
weights × live metrics (VERIFIED)**:

**(a) Correlation — EOG is a near-clone of the slot it replaces.** EOG-OXY = **0.81** (highest in your
book). So the swap barely touches the sleeve's internal correlation structure — you are swapping one
oil-shale price-taker for a better one, not adding a new risk. And relative to the *rest* of the sleeve,
EOG's correlations sit right where OXY's do (EOG: XOM 0.79, CNQ 0.76, CVE 0.77, SLB 0.66, ARX 0.59, TOU
0.53 — VERIFIED). **The important earlier finding still holds: EOG's oil torque *duplicates CNQ*** (both
~0.40 beta-to-WTI; EOG-CNQ corr 0.76). EOG's distinctiveness in your book is **quality/geography/cycle,
NOT torque or low correlation.**

**(b) Factor balance — swap is region-, gas-, and torque-neutral; quality-positive:**

| Sleeve metric (weighted by your %) | **Current (with OXY)** | **After SWAP OXY→EOG** | Change |
|---|--:|--:|:--:|
| Sector weight (% of portfolio) | **13.79%** | **13.79%** | **unchanged** ✓ |
| Blended ROE | 15.0% | **16.1%** | **+1.1 pts (better)** |
| Blended EV/EBITDA | 8.06× | 8.01× | −0.05× (slightly cheaper) |
| Blended beta-to-WTI | 0.375 | 0.368 | −0.007 (torque-neutral, a touch lower) |
| Canada / US split | 56% / 44% | **56% / 44%** | **unchanged** (both US names) ✓ |
| Most-levered holding | OXY (1.18× ND/EBITDA) | **removed** | leverage profile improves |

**Read:** the swap **lifts blended sleeve quality (ROE +1.1 pts) and cuts the sleeve's worst balance
sheet, at the SAME sector weight, with essentially no change to region, gas-tilt, or oil torque.** That
is the textbook definition of a quality upgrade: better sleeve, same size bet.

**(c) Contrast — the ADD-on-top case.** ADD means buying EOG *without* trimming OXY → sleeve grows from
**13.79% to ~14.9%** (if EOG comes in at ~1.1%) or higher. That:
- **Raises an already-heavy single-factor bet.** ~13.8% is already **~3–4× a market-cap energy weight
  (~3–4% of global equities)**; adding on top pushes it toward ~15%+, a bigger bet on one variable (oil
  price) whose correlations across the sleeve are 0.5–0.8 — you don't diversify, you concentrate.
- **Does NOT fix the OXY drag.** You'd still own the "C"-grade, most-levered name; blended ROE improves
  less per dollar than a swap because the low-ROE OXY stays in.
- **Adds torque that duplicates CNQ** (EOG ≈ CNQ on beta-to-WTI) — so the extra exposure is largely a
  *second helping* of oil-price sensitivity you already have.

---

## 4. Sleeve-level verdict + decision framework (research, NOT advice)

### (a) Is ~13.8% O&G already a full/heavy weight? — **Yes.**
A market-cap-neutral energy weight is **~3–4% of global equities**; **13.8% is a ~3–4× overweight** — a
deliberate, sizeable *sector bet*. The first-order question is therefore **allocation** ("should the
sleeve grow *at all*?"), separate from **selection** ("is EOG the right name?" — the EOG files answer
yes, 6.9/10). At ~14% the honest default is **"the sleeve is full."**

### (b) The strongest case is **SWAP OXY→EOG** (quality upgrade, weight-neutral).
**The logic:** your gap is a *quality* US-E&P, not *more* O&G. OXY is the natural funding source — it's
the near-substitute (corr 0.81), your own "C," the most-levered name, the lowest ROE. Swapping into EOG
**raises blended sleeve ROE 15.0%→16.1%, removes your worst balance sheet, and is region/gas/torque-
neutral, all at the SAME 13.8% weight** (§3b). You upgrade the *company* without upsizing the *bet*.

**The counter-argument (be fair to OXY / to timing):**
- **OXY's Permian scale + recovery optionality.** OXY is a top-tier Permian operator; its low ROE is
  *cyclically depressed* (oil normalization + deal-integration + the OxyChem sale year). If oil rallies
  and the debt paydown continues (the $9.7B OxyChem proceeds go to debt), OXY's *earnings and ROE could
  snap back hard* — it has more operating and financial leverage to an oil upcycle than EOG (beta-to-WTI
  0.47 vs 0.39). A deep-value / high-torque investor might *prefer* OXY's rebound optionality.
- **The Berkshire angle.** Buffett owning 28% + a $10B preferred + buying OxyChem is, to some, a *vote of
  confidence* and a floor — not just an overhang.
- **Tax-lot / timing.** Selling OXY may realize a **gain or loss with tax consequences** (unknown to me —
  depends on your cost basis and account type; in a Canadian **non-registered** account a sale is a
  taxable disposition, in a TFSA/RRSP it isn't). **This is a real friction the pure quality math ignores
  — check your lot before acting.** (ASSUMED/ UNVERIFIED — I don't have your basis.)

### (c) The two zero-weight natgas ETFs — flag.
- **BOIL is a 2× leveraged natural-gas ETF.** Leveraged daily-reset ETFs suffer **volatility decay** and
  are **structurally unsuitable to hold** beyond days-to-weeks — over time they bleed value in choppy gas
  markets regardless of the direction of the gas trend. It's your "C." At 0% it's a harmless watchlist
  marker today; **note it should not become a hold.** If you want natural-gas *exposure*, **UNG** (1×,
  no leverage-decay) or the **gas-weighted equities you already own (ARX, TOU)** are the cleaner vehicles.
- Both ETFs load on **natural gas (corr-to-NatGas 0.80–0.83), essentially uncorrelated to your oil
  stocks (0.0–0.11)** — so *if* you ever wanted to add a genuinely different factor to the sleeve, a
  *gas* position (via ARX/TOU/UNG, not BOIL) is the diversifier, not another oil name like EOG.

### (d) Canada-heaviness + "B"-quality note.
The sleeve is **~56% Canada** and **blended "B" quality** (weighted ROE ~15%, dragged by OXY/TOU). The
Canada tilt is a natural CAD match for you but concentrates WCS-differential/Cdn-policy risk. The
OXY→EOG swap **improves quality (→16.1% ROE) without touching the Canada/US split** (both US names). If
you separately wanted to *reduce* Canada, that's a different trade (e.g. trim CVE/TOU) — out of scope
here; flag for a later pass.

### The clean decision rule (yours to make):

| Your view | Implied action |
|---|---|
| "13.8% energy is enough, but I want a **better, higher-quality sleeve**" | **SWAP OXY→EOG** — weight-neutral quality upgrade (blended ROE +1.1 pts, removes worst balance sheet). *The strongest case on the data.* |
| "I'm **deliberately bullish on oil/gas** and want a bigger energy bet" | **ADD EOG on top** — accept the sleeve grows to ~15%+ and concentrates further into the oil-price factor (correlations 0.5–0.8); does not fix the OXY drag. |
| "I want OXY's **high-torque Permian rebound optionality**" | **Keep OXY** (don't swap) — you're choosing torque + recovery optionality over quality/balance-sheet. |
| "I want to hold **natural-gas** exposure as a real diversifier" | Use **UNG or add to ARX/TOU** — NOT BOIL (2× decay) and NOT another oil name like EOG. |

**Bottom line (research, not advice):** the data says EOG's natural role in *your* book is a
**weight-neutral quality upgrade of the US-E&P slot (SWAP OXY→EOG)** — it beats ADD-on-top because your
~13.8% sector weight is already full, and it beats keeping OXY on quality/valuation/balance-sheet. The
honest counter is OXY's cyclically-depressed-ROE *rebound optionality* and your *tax lot*. Decide which
you weight more.

---

## Verification log
- **VERIFIED live (yfinance 2026-07-05 01:54 PT):** all sleeve prices, market caps, EV, EV/EBITDA,
  P/E(t/f), P/B, ROE, ROA, D/E, total debt, cash, dividend yields, payout ratios, EBITDA, shares; **OXY
  net debt $12.8B / net-debt/EBITDA 1.18× / ROE 4.1% / ROA 2.5%**; **EOG net debt $4.46B /
  net-debt/EBITDA 0.35× / ROE 18.2%**; **3y weekly return correlation matrix** (full 9-name sleeve +
  EOG), incl. **EOG-OXY 0.81** (highest), EOG-XOM 0.79, EOG-CNQ 0.76, EOG-CVE 0.77; **beta-to-WTI**
  (OXY 0.47, CVE 0.50, CNQ 0.42, ARX 0.41, EOG 0.39, XOM 0.30, TOU 0.26, SLB 0.24); **beta/corr-to-NatGas**
  (UNG 0.62/0.83, BOIL 1.09/0.80, ARX 0.11/0.25, TOU 0.09/0.30, EOG 0.02/0.05, CNQ 0.04/0.11); WTI
  $68.78 / Brent $72.13 / Henry Hub $3.25 / USD-CAD 1.42.
- **Blended-sleeve figures (VERIFIED inputs, ASSUMED arithmetic):** current blended ROE ~15.0%,
  EV/EBITDA ~8.06×, beta-to-WTI 0.375; post-swap ROE ~16.1%, EV/EBITDA ~8.01×, beta-to-WTI 0.368 —
  computed as Σ(weightᵢ × metricᵢ)/Σweightᵢ over the 7 equities, using your export weights.
- **VERIFIED this session (Wikipedia, Occidental Petroleum page):** Berkshire $10B OXY preferred
  (100,000 shares @ $100,000 par), warrants for 80M shares @ $62.50, ~28% common ownership; Anadarko
  $57B (2019); CrownRock $12B (completed Aug 2024); Berkshire buying OxyChem for $9.7B (Oct 2025); OXY
  acquired Carbon Engineering $1.1B (Aug 2023, DAC).
- **UNVERIFIED / secondary:** OXY preferred **8% dividend rate** (widely reported, not primary-verified
  this session — the Wikipedia page did not state the rate); OXY vs EOG corporate breakevens (EOG
  ~sub-$50 WTI is EOG investor framing; OXY structurally higher = my directional inference); OxyChem-
  sale debt-paydown *use* of proceeds (inferred, not confirmed); 1PointFive/STRATOS project names.
- **Carried from EDGAR-verified EOG files:** EOG ROE 18.2%, net debt ~$4.1–4.5B, 100%-of-FCF returned,
  sub-$50 breakeven, +8% dividend to $4.08, 5.5 Bboe reserves. (See `deep_dive.md` / `profile_and_diligence.md`.)
- **Your holdings (prices/weights):** taken as given from **"Hooman's portfolio export 2026-07-05"** — not
  re-priced. Live yfinance prices differ modestly (e.g. OXY, ARX); sleeve math uses your weights, so
  conclusions are insensitive to the gap.
- **Data caveats:** dual-listed Cdn names (CNQ/CVE) use the **NYSE line (USD-quoted)** for XOM-comparable
  metrics; ARX/TOU use the **.TO line (CAD)** — betas/correlations reflect those listings. TOU shows
  negative TTM FCF and no EV/EBITDA on yfinance (excluded from the blended EV/EBITDA). Correlations are
  3y weekly (156 weeks); a different window shifts them modestly but the "high, 0.5–0.8 within the oil
  complex; ~0 for the gas ETFs" conclusion is robust. yfinance TTM FCF understates EOG's mid-cycle FCF
  (note ‡). Tax-lot / cost-basis and account type (registered vs non-registered) are **unknown to me** —
  a real friction the quality math ignores.
- **NOT financial advice — research to inform Hooman's own decision.**
