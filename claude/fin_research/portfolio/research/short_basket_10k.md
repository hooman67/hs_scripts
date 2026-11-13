# $10,000 Speculative SHORT Basket — Ranked, With Live Short-Seller Campaigns

**Prepared for:** Hooman Shariati (Canadian investor; ring-fenced money he can afford to lose)
**Analyst:** Claude (Opus 4.8)
**As of:** 2026-08-27/28 (data timestamps in the verification log)
**Companion doc (read first):** `short_candidates.md` (same folder) — the archetypes, the Jiffy-Lube→Shell
correction, the borrow/squeeze caveats, and the honest reality-check on shorting. This file does
NOT re-derive that; it (a) refreshes the live data, (b) adds the missing piece — **WHO is publicly
short right now (activist short-seller campaigns 2025–2026)** — (c) validates + stress-tests Hooman's
**"copy-the-shorts" thesis** and re-ranks by *how much downside is LEFT* (§1b), and (d) turns it into
an actual sized $10k basket.

> **Research, not financial advice. Places no trades.** Every number is tagged **VERIFIED**
> (fetched source + date), **ASSUMED**, or **UNVERIFIED**. Live valuations + short interest pulled
> via `/opt/venv/bin/python3` + `yfinance` on **2026-08-27/28**. **The FINRA short-interest
> settlement date behind these figures is 2026-08-14 (VERIFIED via yfinance `dateShortInterest`)
> — genuinely fresh, not stale.** BUT: **cost-to-borrow figures are NOT live** (borrow-data
> providers are paywalled) — treat every borrow % as directional and **re-check on your own broker
> (IBKR shows CTB + availability live) before shorting anything.**
>
> **⚠️ Read §6 (the reality check) in `short_candidates.md` BEFORE acting.** The honest headline
> stands: shorting individual names is a low-win-rate game even when the thesis is right, it fights
> the market's upward drift, and most of a $10k short basket can be lost. This document treats the
> $10k as *entertainment/education capital you are fully prepared to zero.*

---

## 0. THE CRITERIA — what actually works for a short (before we screen)

Hooman's four criteria, plus what the professional short-selling literature and this cohort's
behavior actually reward. **A good short needs #1 + at least one of #2/#3 + a #4 on a clock —
valuation alone is NOT a thesis** (see the SKT/VVV counter-examples in the companion doc: expensive
things stay expensive).

1. **Expensive / unjustified valuation** — rich P/E or P/S with no growth to justify it, or negative
   earnings at a rich multiple. *(necessary, not sufficient)*
2. **Weak business fundamentals** — no moat, deteriorating rev/margins, cash burn, high debt,
   accounting red flags, going-concern risk.
3. **⭐ A famous activist short-seller has a LIVE, PUBLISHED campaign** (Hooman's key criterion).
   Why it matters *mechanically*: a public short report is itself a catalyst (it can force a
   de-rate, trigger an SEC/auditor look, or scare off the marginal buyer), AND it means a
   professional with a research team has already done the fraud/accounting work you can't. But it
   cuts both ways — a report that fails to land emboldens the longs, and the most-reported names are
   the most crowded (squeeze fuel).
4. **A CATALYST on a clock** — earnings, guidance cut, debt maturity, lockup expiry, dilution, credit
   event, regulatory action, or the short report itself. Without #4 you rent a value trap and bleed
   borrow.

**My added criteria (what separates a *tradeable* short from a *right-but-fatal* one):**
5. **LOW-to-MODERATE short interest + cheap/available borrow + fast days-to-cover.** The best
   fundamental shorts (LCID 34% SI, C3.ai 34%, Tempus 30%, Eos 31%) are often the most crowded —
   which is exactly the squeeze fuel. A *tradeable* short wants the thesis crowded enough to be
   validated but not so crowded it's a coiled spring. Prefer SI < ~15% for naked; use **puts** above
   that.
6. **Defined-risk expression.** For a small retail account, **long puts dated past the catalyst** are
   almost always the right vehicle: capped loss, no borrow, no recall, un-squeezable. This
   restructures the whole basket around puts, not short stock.

---

## 1. WHO IS PUBLICLY SHORT RIGHT NOW — the 2025–2026 activist-short campaign map

*This is the section the companion doc was missing. Sourced by fetching short-sellers' own research
pages + company/aggregator pages on 2026-08-27/28, and corroborated by a parallel research agent
using financial-press coverage.*

**First, the landscape correction (VERIFIED):**
- **Hindenburg Research SHUT DOWN.** Nate Anderson disbanded the firm **January 15, 2025**; its
  final report was **Carvana, January 2, 2025** [VERIFIED — Wikipedia/Hindenburg, fetched 2026-08-28].
  So "Hindenburg is short X" is no longer a live signal for anything after Jan 2025. **The successor
  is MORPHEUS RESEARCH** — a short-selling firm founded in 2025 by ex-Hindenburg team members,
  publicly backed by Anderson [VERIFIED — Bloomberg "Hindenburg-Linked Morpheus Targets Solaris,"
  Mar 17 2025]. Its US-listed 2025-26 targets (Abacus Global ABL, Innventure, Figure Technology,
  Velo3D) are the most Hindenburg-lineage names to watch (not deep-dived here).
- **Muddy Waters (Carson Block) IS ACTIVE again** — three fresh 2026 US-listed campaigns: **Ensign
  Group (ENSG, Jun 11 2026)** Medicare license-rental fraud; **Sportradar (SRAD, Apr 22 2026)**
  facilitating illegal gambling; **SoFi (SOFI, Mar 2026)** accounting/EBITDA-restatement thesis
  [VERIFIED — muddywatersresearch.com report URLs]. (My earlier "MW unreachable" note was a
  transient fetch failure — corrected here.)
- **Culper Research is the most prolific US-focused firm** — 2026 campaigns include **Tarsus (TARS,
  Jul 1 2026)** Medicare copay scheme, **ADMA Biologics (ADMA, Mar 24 2026)** channel-stuffing,
  **Nvidia (NVDA, May 2026)** China export-control, **T1 Energy (TE, Jan 21 2026)**, and **DoorDash
  (DASH)** worker-classification [VERIFIED via financial-press coverage; Culper's own site 403'd].
- **Kerrisdale (Sahm Adrangi)** live 2026: **Everspin (MRAM, May 19 2026)** AI-memory hype and
  **Affirm (AFRM, Jan 21 2026)** BNPL-credit; also confirmed the **IONQ short (Mar 13 2025)** I'd
  flagged as unconfirmed. **Attribution trap:** the Feb 2026 IONQ short was **Wolfpack, not
  Kerrisdale** [VERIFIED — agent research, financial-press].
- **Grizzly Research** 2025 US shorts largely WORKED and de-rated hard already (Microvast MVST −80%,
  KULR −75%, Pony AI PONY −42%, Archer ACHR −35%); its 2026 slate pivoted to Europe (not US-shortable).
- **Viceroy Research** is currently campaigning almost entirely on **Canadian TSX-V small-caps**
  (Blue Moon Metals TSXV:MOON, Abaxx TSX:ABXX) [VERIFIED — viceroyresearch.org, fetched 2026-08-28].
  These are **too thin/illiquid and not US-optionable** — good reading, not shortable for you. Skip.

### Live US-listed activist short campaigns (the shortlist that matters for you)

| Target | Ticker | Short-seller | Report date | Core allegation | Live? |
|---|---|---|---|---|---|
| **T1 Energy** ⭐ | TE | **Fuzzy Panda (5 reports) + Culper (Jan 21 2026)** | **Jan–Jun 2026** | TRIPLE-TARGETED: Trina Solar secretly controls T1; Chinese military-linked cell sourcing; 45X tax-credit fraud; hidden inventory; restatements expected; "failed EV-battery SPAC" dilution | **VERY live, two firms** |
| **Ensign Group** | ENSG | **Muddy Waters** | **Jun 11, 2026** | Medicare/Medicaid license-rental fraud (renting nursing-home admin licenses); FCA exposure framed ~$7B | **YES — freshest MW** |
| **Sportradar** | SRAD | **Muddy Waters** | **Apr 22, 2026** | Knowingly facilitates illegal gambling; 20–40% of revenue; some clients tied to organized crime | **YES**; class actions Jul 2026 |
| **SoFi** | SOFI | **Muddy Waters** | **Mar 2026** | Accounting: ~$312M JPMorgan borrowing booked as loan sale not debt; EBITDA needs restatement; understated charge-offs | **YES (open, market rejecting)** |
| **Tarsus Pharma** | TARS | **Culper** | **Jul 1, 2026** | Illegal Medicare copay scheme (Xdemvy) | **LIVE — newest Culper** |
| **ADMA Biologics** | ADMA | **Culper** | **Mar 24, 2026** | Channel-stuffing / financial misrepresentation | **LIVE**; −17% day-one, class actions |
| **Affirm** | AFRM | **Kerrisdale** | **Jan 21, 2026** | "Buy Now, Cry Later" — BNPL credit model | LIVE |
| **Everspin** | MRAM | **Kerrisdale** | **May 19, 2026** | AI-memory hype; "hardly cutting edge" | LIVE, −11% on report |
| **IonQ** | IONQ | **Kerrisdale** | **Mar 13, 2025** | Quantum overvaluation; lost gov't contracts "$54.6M black hole" | Contested (retail unmoved) |
| **Tempus AI** | TEM | **Spruce Point** | **May 28, 2025** | Overvaluation, revenue-quality / related-party (Ambry, SB Tempus JV), reliance on M&A to show growth | Live-ish; TEM now buying Personalis |
| **DraftKings** | DKNG | **Spruce Point** | **Oct 3, 2025** | Overvaluation, competitive/promo intensity, prediction-market/regulatory risk | Live |
| **iRhythm** | IRTC | **Spruce Point** | **Aug 18, 2025** | Reimbursement/coding risk, valuation, competitive threat to Zio | Live |
| **Clear Secure** | YOU | **Spruce Point** | **Apr 30, 2025** | Decelerating growth, TSA/airport concentration, governance/valuation | Live |
| **Bunge Global** | BG | **Spruce Point** | **Mar 25, 2026** | Viterra-merger integration/accounting, ag-cycle earnings quality | Live |
| **Super Group (SGHC)** | SGHC | **Spruce Point** | **Feb 12, 2026** | Online-gambling accounting/geography-of-revenue, governance | Live |
| **Resideo** | REZI | **Spruce Point** | **Jan 27, 2026** | Leverage, ADI spin, margin/valuation | Live |
| **Monster Beverage** | MNST | **Spruce Point** | **Apr 8, 2025** | Decelerating volumes, valuation, governance | Live |
| **Remitly** | RELY | **Spruce Point** | **Mar 11, 2025** | Competition, take-rate/margin, valuation | Live |
| **Uranium Energy** | UEC | **Spruce Point** | **Sep 18, 2025** | Pre-revenue, resource/permit claims, promotional | Live |
| **Zoom** | ZM | **Spruce Point** | **Apr 24, 2026** | *Note: reported as a LONG idea, not a short* — exclude | n/a |
| **Lyft** | LYFT | **Bleecker Street** | **Jul 23, 2026** | "Massive liabilities (insurance reserves), limited capacity to pay, deteriorating outlook" | Live |
| **Aurora Innovation** | AUR | **Bleecker Street** | **May 14, 2025** | Autonomous-trucking cash-burn story stock; timeline/viability | Live |
| **Rocket Lab** | RKLB | **Bleecker Street** | **Feb 25, 2025** | Long-term viability / valuation vs. launch cadence | Report landed, stock ran anyway |
| **Perdoceo Education** | PRDO | **Bleecker Street** | **Nov 17, 2025** | For-profit-education regulatory/enrollment risk | Live |
| **Tempus / United Therapeutics-Liquidia** | UTHR/LQDA | Bleecker Street | Jul 29, 2025 | Litigation/patent-cliff | Niche |
| **T1 Energy** | TE | **Fuzzy Panda** (4+ reports) | **May–Jun 2026** | Trina Solar secretly controls T1; Chinese military-linked cell sourcing; tax-credit fraud; hidden inventory; restatements expected | **VERY live, multi-report campaign** |
| **Fermi America** | FRMI | Fuzzy Panda | Apr 20, 2026 | Fraudulent transfers / asset misappropriation by leadership | Live |
| **Eos Energy** | EOSE | **Fuzzy Panda** | **Oct 30, 2025** | Concealed gas-hazard safety issue; multiple versions of financial statements | Live |
| **Red Cat** | RCAT | **Fuzzy Panda** | **Oct 10, 2025** | Misrepresented US Army contract size; Chinese components | Live |
| **Rezolve AI** | RZLV | **Fuzzy Panda** | **Sep 29, 2025** | Revenue inflated via acquisitions of dying startups; "no genuine AI product" | Live |
| **Soleno Therapeutics** | SLNO | **Scorpion Capital** | **Aug 15, 2025** | Safety/efficacy of Prader-Willi drug; "fraudulent clinical trials" | Live (biotech binary) |
| **Limbach** | LMB | **Spruce Point** | **Jul 22, 2025** | "Overheated HVAC growth story," inflated valuation | Report faded; stock still high |

Sources: sprucepointcap.com/research, bleeckerstreetresearch.com/research, fuzzypandaresearch.com,
scorpioncapital.com, viceroyresearch.org, muddywatersresearch.com — publisher pages fetched
**2026-08-28** [VERIFIED]. Culper, Grizzly, Kerrisdale slates VERIFIED via financial-press coverage
(their own sites 403'd) — report existence/dates/allegations confirmed, but stock-reaction %s and
litigation follow-ups are **UNVERIFIED** (primary wires were fetch-blocked). Blue Orca not confirmed.

**⚠️ FAILED / REJECTED activist theses — do NOT build a fresh short on these** (the market ran them
UP after the report; a failed report emboldens longs): **AppLovin (APP)** — targeted by MW + Fuzzy
Panda + Culper, then added to the S&P 500 and SEC closed its ad probe; **FTAI Aviation** — rebutted,
+53%; **GeneDx (WGS)**, **Nexstar (NXST)**, **XP Inc (XP)** (XP sued Grizzly for defamation). These
are cautionary examples, not setups. **Also: MSTR** premium-short already played out (see below).

**How I filtered this for the basket:** I want campaigns where (a) the stock is **US-listed +
optionable**, (b) the allegation is **fundamental/fraud** (not just "expensive"), (c) there's a
**catalyst on a clock**, and (d) the short mechanics won't obviously kill me. That elevates **TE
(now DOUBLE-targeted: Fuzzy Panda + Culper — the highest-conviction multi-firm signal in the set),
ENSG/SRAD/SOFI (Muddy Waters), TARS/ADMA (Culper), TEM/DKNG (Spruce Point)** as the freshest
activist-backed ideas — combined with the strongest broken-business names from the companion doc
(**LCID, RBLX**) and select AI-bubble overvaluation names (**RKLB, AUR, IONQ**).

---

## 1b. VALIDATING HOOMAN'S "COPY-THE-SHORTS" THESIS — ~70% right

**Hooman's thesis (paraphrased):** *Short-sellers MUST publicize their positions — their P&L depends
on the market re-pricing the stock down — whereas long "jockeys" (great investors) stay quiet to keep
accumulating. So famous-short positions are unusually observable and potentially easy to copy.*

**Verdict: ~70% right. The premise is sound; two structural flaws cap how much of the edge a copycat
can actually capture.**

### Why it's right (the ~70%)
- **Activist shorts are genuinely a broadcast strategy.** Unlike a long, whose thesis works even in
  silence (the company compounds regardless of who knows), an activist short's return *depends on
  persuading the market* — so they publish a detailed report, do media, and post it on X. This makes
  their **entry uniquely observable**: you get the ticker, the full thesis, and the date, for free.
  This is real and it's exactly why this whole report could be built. **Sourcing edge: real.**
- **The research is done for you** by a professional team with FOIA requests, channel checks,
  ex-employee interviews, and forensic accounting a retail investor cannot replicate. Multi-firm
  overlap (TE: Fuzzy Panda + Culper) is a cross-validation signal you'd never get on the long side.
- **Long "jockeys" really are quieter** — 13F filings lag 45 days, are longs-only, and great
  managers avoid telegraphing accumulation. So the *observability asymmetry* Hooman describes is real.

### The two flaws that cap it (the missing ~30%)
1. **⚠️ The biggest move happens ON publication day — the copycat is late.** The report *is* the
   catalyst; the market re-prices in hours. **AppLovin fell ~20% the day of the Fuzzy Panda/MW
   reports; ADMA fell ~17% day-one; Everspin ~11%.** By the time you read it, that first leg is gone.
   **A copycat is therefore not betting on the thesis — they're betting on a *SECOND leg down***
   (a confirming event: a restatement, an SEC action, a delisting, a covenant breach). If there's no
   identifiable second-leg catalyst, you're buying after the edge has been paid out.
2. **⚠️ Shorts publicize ENTRY but cover SILENTLY — you can be short a position they already closed.**
   The publish is loud; the cover is invisible (no rule forces disclosure of covering). Disclaimers
   literally warn this: **Muddy Waters said it "may have begun covering" FTAI while retail was still
   piling in short** — and FTAI then ran **+53%.** So "a famous short is on it" can be *stale by
   months*. You are copying a snapshot, not a live position.

### What this means for how we RANK (the correction to the basket logic)
The right use of famous-short reports is as a **sourcing / idea-generation tool, then filter hard for
how much downside is LEFT.** Concretely, favor names where the short is:
- **(a) LIVE / recent** — published in the last few months, not a 2025 report the firm may have
  covered (freshness proxy: recency + still-elevated short interest).
- **(b) Thesis has NOT yet played out** — the stock has *not* already dropped-and-recovered. If it
  cratered on the report and bounced back (APP, FTAI, XP), the market has *rejected* the thesis and
  the shorts likely covered — **avoid.**
- **(c) A concrete UPCOMING catalyst for a second leg** — an earnings print, a restatement deadline,
  an SEC/DOJ decision, a debt maturity, a lockup. Without this you're just hoping.

### Candidates ranked by "DOWNSIDE LEFT" (not just "is a famous short on it")

| Rank | Name | Short is LIVE? | Already dropped-&-recovered? | Concrete 2nd-leg catalyst? | Downside LEFT |
|---|---|---|---|---|---|
| **A** | **TE** | ✅ Very (2 firms, Jan–Jun'26) | ❌ still near lows, no recovery | ✅ restatement / tax-credit ruling | **HIGH** |
| **A** | **ENSG** | ✅ Fresh (Jun'26) | ❌ only −8%, essentially intact | ✅ FCA suit / DOJ-CMS probe | **HIGH** |
| **B** | **TARS** | ✅ Newest (Jul'26) | ❌ hasn't cracked yet | ⚠️ copay-scheme probe (uncertain timing) | **MED-HIGH** |
| **B** | **SRAD** | ✅ (Apr'26) | ❌ near 52w low but not report-driven | ⚠️ gambling-regulatory (slow) | **MED** |
| **B** | **TEM** | ⚠️ Aging (May'25) | ⚠️ volatile, no clean recovery | ✅ Personalis dilution + margin prints | **MED** |
| **C** | **ADMA** | ✅ (Mar'26) | ⚠️ dropped −17% then partly recovered | ⚠️ SEC/restatement (unproven) | **MED-LOW** |
| **C** | **SOFI** | ⚠️ (Mar'26) but market REJECTING | ✅ recovered off lows | ❌ restatement not materializing | **LOW** |
| **C** | **DKNG** | ⚠️ (Oct'25) | partial | ⚠️ regulatory (diffuse) | **LOW-MED** |
| ❌ | **RKLB / IONQ** | stale ('25), **MISFIRED** | ✅ ran UP after report | ❌ | **~NONE (from the short)** |
| ❌ | **APP / FTAI / XP / WGS / NXST** | covered/rejected | ✅ dropped-&-recovered | ❌ | **NONE — avoid** |

**Note on the non-activist names:** RBLX and LCID have NO famous short-seller, but they score high on
"downside LEFT" for a *different* reason — a **fundamental catalyst on a clock** (RBLX's guided
bookings decline; LCID's forced dilution). Hooman's copy-the-shorts thesis is a *sourcing* tool, not
the only sourcing tool — the best fundamental shorts don't need an activist, and the basket keeps
2–3 of them so it isn't 100% dependent on "is someone famous short."

---

## 2. THE CANDIDATES — full per-name cards (live data 2026-08-27/28)

Legend for mechanics: **SI%** = short % of float, **DTC** = days-to-cover (shortRatio), borrow =
UNVERIFIED-live estimate. Conviction blends thesis strength + catalyst − tradeability.

### TIER 1 — best thesis-plus-catalyst-plus-activist combos

---

#### TE — T1 Energy (~$4.96 | mkt cap ~$1.46B) — *the strongest ACTIVIST campaign in the set*
- **Business:** US solar-module maker (formerly Trina Solar's US arm / renamed from FREYR). [VERIFIED — yfinance name "T1 Energy"]
- **Valuation (live):** P/S 1.47x, fwd P/E ~52x, **net margin −38.5%**, gross margin just **5.9%**,
  debt/equity **283%**, EV/EBITDA −23.8. Rev +88% (ramp). [VERIFIED — yfinance 2026-08-28]
- **Bear case (criteria 2+3 — DOUBLE-TARGETED, highest multi-firm conviction signal in the set):**
  **Fuzzy Panda ran a 5-report campaign May–Jun 2026** alleging Trina Solar *secretly controls T1 as
  a shell*, solar cells sourced from a **Chinese military-linked** supplier (which would **disqualify
  it from IRA/45X tax credits** — the entire bull thesis), **fraudulent accounting + hidden
  inventory**, and **restatements expected** [VERIFIED — fuzzypandaresearch.com]. Separately,
  **Culper Research shorted it Jan 21 2026** ("failed EV-battery SPAC," dilution) and multiple
  securities probes reportedly opened [VERIFIED — Culper via financial-press; probes UNVERIFIED].
  Two independent activist firms on the same name = the strongest cross-validation here; it's a
  genuine fraud/accounting campaign, not a valuation gripe.
- **Catalyst (criterion 4):** Any of — tax-credit eligibility ruling, a restatement, auditor
  resignation, or SEC action. The thesis is self-executing if the China-control/tax-credit claim is
  validated (removes the reason the equity exists).
- **Mechanics:** ⚠️ **SI ~30% of float** [VERIFIED — yfinance], **but DTC only ~1.5** (liquid enough
  to cover). Borrow likely expensive (UNVERIFIED). Down ~60% off 52w high already.
- **Short conviction: 7/10.** Best activist-fraud campaign; catalyst is binary and thesis-breaking.
  **Use puts** — 30% SI + a takeover/settlement or a China-clears headline could squeeze.

---

#### LCID — Lucid Group (~$5.09 | mkt cap ~$1.99B) — *cleanest BROKEN business*
- **Business:** Luxury BEV maker (Air/Gravity), Saudi PIF-controlled & funded. [VERIFIED]
- **Valuation (live):** No P/E; **gross margin −96.6%** (still selling each car for ~half what it
  costs to build), **net margin −249%**, P/B **−1.90 (negative equity)**, debt/equity 198%, EV/EBITDA
  −2.2. [VERIFIED — yfinance 2026-08-28]
- **Bear case (criteria 1+2):** The cleanest structurally-broken business in the whole set — negative
  gross margin means volume growth *deepens* losses. Burns ~$1.5B/qtr against a liquidity runway that
  keeps requiring PIF top-ups. No public activist campaign — this is a fundamentals/valuation short,
  not a report-driven one.
- **Catalyst:** Near-certain further dilution/PIF raise before mid-2027 on the cash math; guidance
  effectively suspended; "Cosmos" volume platform pushed to 2H2027.
- **Mechanics:** ⚠️⚠️ **STRUCTURALLY DANGEROUS. SI ~34% of float** [VERIFIED — yfinance 2026-08-28,
  down from ~38% prior month], **borrow historically ~16%/yr (hard-to-borrow, UNVERIFIED-live)**,
  ~60% of float PIF-locked (recall risk), DTC ~2.4. Beta shows 0.86 (understated; it's a violent
  small-cap).
- **Short conviction: 8/10 business / 3/10 tradeable naked.** **Puts ONLY.** Best broken business,
  worst mechanics — the 16% carry alone kills a naked short that's early.

---

#### RBLX — Roblox (~$38.15 | mkt cap ~$27.3B) — *best FUNDAMENTALS-PLUS-FRESH-CATALYST, cheap borrow*
- **Business:** UGC gaming/social platform; monetizes Robux; reports "bookings" ahead of GAAP. [VERIFIED]
- **Valuation (live):** No P/E, **net margin −17.6%**, P/S 4.8x, P/B **179x**, EV/EBITDA −30.9,
  debt/equity 1423% (SBC-driven). Rev +36% but still deeply GAAP-loss-making; SBC > net loss. [VERIFIED — yfinance 2026-08-28]
- **Bear case (criteria 1+2+4):** The **first-ever guided bookings DECLINE + withdrawn full-year
  guidance** (from the companion doc, Q3'26), escalating **child-safety litigation** (Senate probe,
  ~140 federal suits, state-AG actions) + age-verification headwinds that hit engagement. No named
  activist, but this is the best "story stock finally cracking" catalyst in the set.
- **Catalyst:** Next bookings print confirming the decline; any adverse child-safety ruling/settlement.
- **Mechanics:** **BEST in the set — favors the short. SI only ~2.2% of float** [VERIFIED — yfinance
  2026-08-28, down sharply from prior month], **borrow ~cheap (~0.4%, UNVERIFIED-live)**, DTC ~1.0.
  Low squeeze risk. Caveat: already −73% from $142 high, so a lot is priced in.
- **Short conviction: 7/10.** Best combination of clean catalyst + cheap/available borrow + low SI.

---

#### RKLB — Rocket Lab (~$67.53 | mkt cap ~$43.2B) — *extreme AI/space-bubble multiple + activist*
- **Business:** Small-launch + space-systems company. [VERIFIED]
- **Valuation (live):** **P/S 56x**, fwd P/E **1,350x**, net margin −21.5%, EV/EBITDA −254. Rev +62%
  (real growth) but priced like it already dominates a market it doesn't. [VERIFIED — yfinance 2026-08-28]
- **Bear case (criteria 1+3):** **Bleecker Street published a short (Feb 25, 2025)** on long-term
  viability/valuation [VERIFIED — bleeckerstreetresearch.com]. The report did NOT work — stock ran
  from the ~$37 low to $67; that's the honest caution here (a failed activist report = emboldened
  longs). Pure valuation short on a momentum darling — historically a great way to lose money.
- **Catalyst:** A launch failure, a Neutron-rocket delay, or a growth-deceleration print. No hard
  clock.
- **Mechanics:** SI ~7.5% of float, DTC ~2.3, beta **2.63**. Momentum + retail = spikes.
- **Short conviction: 4/10.** Egregious multiple, but momentum names crush valuation shorts and the
  activist report already misfired. **Puts only, and small** — this is a lottery ticket, not an edge.

---

### TIER 2 — Spruce Point activist campaigns (fundamental, moderate mechanics)

---

#### TEM — Tempus AI (~$70.69 | mkt cap ~$12.8B)
- **Business:** AI precision-medicine / genomics (founder Eric Lefkofsky, ex-Groupon). [VERIFIED — Wikipedia]
- **Valuation (live):** No P/E, **net margin −17.8%** (net loss ~$254M TTM), P/S 8.9x, EV/EBITDA
  −69, debt/equity 325%. Rev +50% but growth is heavily **M&A-fueled** (Ambry $600M 2024; now buying
  **Personalis ~$1.5B**). [VERIFIED — yfinance + stockanalysis.com 2026-08-28]
- **Bear case (criteria 1+2+3):** **Spruce Point short, May 28, 2025** — overvaluation + revenue
  quality/related-party concerns (Ambry, SB Tempus JV) + reliance on acquisitions to manufacture
  growth. [VERIFIED — sprucepointcap.com]. **Even the sell-side avg PT (~$63) is BELOW the current
  price** [VERIFIED — stockanalysis.com] — the Street implies downside.
- **Catalyst:** Personalis-deal dilution/integration; any organic-growth-vs-M&A disaggregation that
  disappoints; a miss on the still-negative margins.
- **Mechanics:** ⚠️ **SI ~30% of float** [VERIFIED — yfinance], DTC ~6.1, **beta 3.58** (very
  volatile). This is crowded — squeeze-prone.
- **Short conviction: 6/10 thesis / 3/10 tradeable naked.** **Puts.** Good activist thesis, dangerous
  crowd + beta.

---

#### DKNG — DraftKings (~$24.22 | mkt cap ~$12.0B)
- **Business:** #1/#2 US online sportsbook + iGaming; now pushing prediction markets. [VERIFIED]
- **Valuation (live):** No trailing P/E (**net loss −$167M TTM**), fwd P/E ~44x, P/S 1.9x, EV/EBITDA
  **105x**, debt/equity 336%. Rev +15% but **market cap −49%** off highs. [VERIFIED — yfinance +
  stockanalysis.com 2026-08-28]
- **Bear case (criteria 1+3+4):** **Spruce Point short, Oct 3, 2025** [VERIFIED — sprucepointcap.com]
  — overvaluation + promotional/competitive intensity + regulatory risk. Live regulatory overhang on
  **prediction markets** (CFTC-vs-state fight) and rising state betting-tax rates squeezing margins.
- **Catalyst:** A state-tax hike, a prediction-market legal ruling, or an EBITDA-guide cut. Sell-side
  still bullish ($35 avg PT) = room to disappoint.
- **Mechanics:** SI ~8% of float, DTC ~2.9, beta 1.63 — **moderate, among the more tradeable.**
- **Short conviction: 5/10.** Real activist + regulatory catalyst, but it's a genuine share-leader
  growing revenue — not broken. Sell-side loves it (squeeze-on-good-news risk).

---

#### BG — Bunge Global (~$111.57 | mkt cap ~$21.4B)
- **Business:** Global agribusiness/oilseed processor; just merged with Viterra. [VERIFIED]
- **Valuation (live):** P/E 24x, fwd P/E ~9.8x, **net margin 1.1%** (thin, cyclical), P/S 0.23x.
  Rev +88% (Viterra consolidation). [VERIFIED — yfinance 2026-08-28]
- **Bear case (criteria 3):** **Spruce Point short, Mar 25, 2026** [VERIFIED] — Viterra
  integration/accounting + ag-cycle earnings-quality. This is a low-multiple cyclical, so it's a
  *quality-of-earnings* short, not an overvaluation short.
- **Catalyst:** A crush-margin down-cycle + integration miss.
- **Mechanics:** SI only ~4.7% of float, DTC ~4.8, low beta 0.65 — **not crowded, but also not
  cheap/broken.**
- **Short conviction: 3/10.** Cheap cyclical with an activist flag but no valuation cushion for the
  short and no hard catalyst. Include only for thesis *diversification* if at all. Likely skip.

---

### TIER 3 — AI / quantum / autonomy bubble (valuation shorts — high risk, lottery tickets)

---

#### AUR — Aurora Innovation (~$5.69 | mkt cap ~$11.4B) — *near-pre-revenue at an $11B cap + activist*
- **Business:** Autonomous-trucking (driverless). [VERIFIED]
- **Valuation (live):** **P/S ~2,281x** (TTM revenue just ~$5M against an $11.4B cap), **net loss
  ~$900M**, no gross profit yet. [VERIFIED — yfinance + stockanalysis.com 2026-08-28]
- **Bear case (criteria 1+2+3):** **Bleecker Street short, May 14, 2025** [VERIFIED —
  bleeckerstreetresearch.com] on cash-burn/viability/timeline. An $11B market cap on ~$5M revenue is
  a pure faith-in-2027+ bet; any timeline slip on the "200+ driverless trucks by 2026" goal removes
  the story.
- **Catalyst:** Driverless-scale-up miss; a capital raise (dilution) to fund the burn.
- **Mechanics:** SI ~16% of float, DTC ~7.3, **beta 2.66** — crowded + volatile.
- **Short conviction: 5/10 thesis / 3/10 tradeable.** **Puts.** The most absurd multiple in the set,
  but story stocks with a big backer (it's a well-funded name) can stay irrational for years.

---

#### IONQ — IonQ (~$42.46 | mkt cap ~$16.9B) — *quantum-hype multiple*
- **Business:** Trapped-ion quantum computing. [VERIFIED]
- **Valuation (live):** **P/S 70x**, net loss −$510M (2025), no profit, EV/EBITDA −18. Rev +371%
  (tiny base ~$246M TTM). [VERIFIED — yfinance + stockanalysis.com 2026-08-28]
- **Bear case (criteria 1+3):** Classic pre-commercial quantum-hype valuation. **Kerrisdale Capital
  published an IONQ short Mar 13 2025** (quantum overvaluation; lost government contracts = a "$54.6M
  black hole") [VERIFIED — Kerrisdale via financial-press]. But retail was unmoved and the stock is
  volatile — the report has not forced a durable de-rate. (Attribution note: a *separate* Feb 2026
  IONQ short was **Wolfpack, not Kerrisdale.**)
- **Catalyst:** Serial ATM dilution; a quantum-hype-cycle unwind; a guidance disappointment.
- **Mechanics:** SI ~11% of float, DTC ~2.0, **beta 3.30** (extreme).
- **Short conviction: 4/10.** Egregious multiple but a momentum/theme darling — beta 3.3 means it can
  gap 30%+ on any "quantum breakthrough" headline. **Puts only, tiny.**

---

#### MSTR — Strategy / MicroStrategy (~$137.40) — *the premium-short ALREADY WORKED; DO NOT chase*
- **Business:** Bitcoin-treasury vehicle (840,447 BTC) wrapped around a shrinking software business. [VERIFIED — stockanalysis.com 2026-08-28]
- **Key finding (honest):** The famous "mNAV premium" short has **largely played out.** With BTC
  ~$80k, the coins are worth ~$67B vs a market cap of ~$52.8B — i.e., **MSTR now trades roughly at
  or BELOW its bitcoin NAV (~0.8x), not the 2–3x premium** that made it a great short in 2024–25.
  Net income −$31B reflects a huge BTC mark-to-market swing, not operations. [VERIFIED — stockanalysis.com]
- **Verdict:** ❌ **Not a short here.** Shorting MSTR now is just shorting bitcoin with leverage and
  ~$-99 EPS optics — beta 3.56, and you'd be short *below* NAV. The edge is gone. Included to
  document that the obvious idea is stale.

---

### TIER 2b — fresh Muddy Waters / Culper FRAUD campaigns (added after agent research)

*These are the freshest, most-credible-activist, fraud/regulatory theses. All live data yfinance
2026-08-28. Note: several are profitable companies — so these are fraud/regulatory de-rate bets, not
broken-business bets, which makes puts (defined risk on a binary allegation) the right vehicle.*

#### ENSG — Ensign Group (~$173.54 | mkt cap ~$10.1B) — *Carson Block's freshest, cleanest mechanics*
- **Business:** Skilled-nursing / post-acute care operator. [VERIFIED]
- **Valuation (live):** P/E 28.4x, fwd 20.3x, P/S 1.84x, net margin 6.9%, rev +17.3%, debt/equity
  92%. Not "expensive-broken" — a *growing, profitable* operator. [VERIFIED — yfinance 2026-08-28]
- **Bear case (criterion 3, the strongest activist name):** **Muddy Waters short, Jun 11 2026** —
  alleges Medicare/Medicaid **license-rental fraud** (renting nursing-home admin licenses at ~20% of
  facilities), framing **False Claims Act exposure ~$7B** [VERIFIED — muddywatersresearch.com; the
  $7B figure UNVERIFIED]. Carson Block is the most credible name in the set, and a *fraud/FCA*
  thesis is the highest-quality allegation type.
- **Catalyst:** A DOJ/CMS investigation, an FCA suit, or a whistleblower follow-up.
- **Mechanics:** ✅ **BEST activist-name mechanics — SI only ~3% of float, beta 0.69, DTC ~3.5.**
  Low squeeze risk. The catch: it's a profitable, well-run compounder, so absent the fraud landing,
  it keeps grinding up (you're paying theta on a binary).
- **Short conviction: 6/10.** Best activist + best mechanics, but it needs the FCA allegation to
  actually bite; a profitable compounder doesn't de-rate on a report alone.

#### SRAD — Sportradar (~$12.78 | mkt cap ~$3.8B)
- **Business:** Sports-data/betting-integrity provider. [VERIFIED]
- **Valuation (live):** P/E **213x**, fwd 22x, P/S 2.7x, net margin 1.2%, rev +18.9%. [VERIFIED — yfinance]
- **Bear case (criterion 3):** **Muddy Waters short, Apr 22 2026** — alleges Sportradar knowingly
  facilitates illegal gambling (20–40% of revenue), some clients tied to organized crime; class
  actions opened Jul 2026 [VERIFIED — MW page; litigation UNVERIFIED].
- **Mechanics:** SI ~13% of float, DTC ~5.5, beta 1.6 — moderate.
- **Short conviction: 5/10.** Regulatory/reputational thesis; harder to force a de-rate on a clock.

#### TARS — Tarsus Pharma (~$71.92) / ADMA — ADMA Biologics (~$9.48) — *Culper Medicare theses*
- **TARS:** No P/E (net margin −7.7%), P/S 5.2x, rev +69%. **Culper short Jul 1 2026** — alleges
  illegal Medicare copay scheme for its eye drug Xdemvy. SI ~14%, DTC ~6.3, beta 0.51. **5/10.**
- **ADMA:** P/E 13.7x, **profitable (net margin 33%)**, P/S 4.1x. **Culper short Mar 24 2026** —
  channel-stuffing/misrepresentation; fell ~17% day-one, class actions filed. SI ~12%, DTC **~8.5
  (slow exit)**, beta 0.77. **5/10.** Both are biotech/pharma binary regulatory bets — puts only.

### TIER 4 — carried over from the companion doc (still valid, condensed)

| Ticker | 1-liner | Live flag (2026-08-28) | Conviction | Mechanics |
|---|---|---|---|---|
| **CHTR** — Charter | Levered cable, subs shrinking | debt/equity 442%, rev −1.7%, EV≫equity | 6/10 | **SI ~20.3%** (VERIFIED stockanalysis; yfinance's 51.6% was a glitch), DTC ~7.2 |
| **CRCL** — Circle | Rate-dependent stablecoin, rich | P/S 8.8x, EV/EBITDA 97x, rev +6.6% | 6/10 | SI ~11%, DTC ~2.1, liquid (low squeeze) |
| **W** — Wayfair | Never-profitable, negative equity | P/B −4.9x, EV/EBITDA 47x, net margin −2.5% | 6/10 | SI ~12%, DTC ~2.7, beta 2.98, ripped +36% YTD |
| **PLUG** — Plug Power | Negative-gross-margin hydrogen | gross margin −24.7%, P/S 4.3x | 6/10 | ⚠️ SI ~23%, cult, guidance rising |
| **KMX** — CarMax | Used-car + subprime CAF | P/E 40x, EV/EBITDA 27x, net margin 0.8% | 6/10 | SI ~10%, DTC ~5.2, moderate |
| **KSS** — Kohl's | Legacy dept store, net-loss risk | P/E 7.7x trap, comps −0.9% | 6/10 thesis | ⚠️⚠️ **SI ~31%**, DTC ~9.3, proven July-2025 squeezer |
| **BYND** — Beyond Meat | Going-concern, distressed | debt/equity 719%, rev −8.2% | 6/10 thesis | ⚠️⚠️ **SI ~30%**, meme, −94% already |
| **CVNA** — Carvana | Subprime-linked used-car (ex-Hindenburg target) | P/S 3.3x, P/B 13x, beta 3.49 | 5/10 thesis | ⚠️⚠️ SI ~12%, violent squeezer |
| **C3.ai (AI)** | Enterprise-AI, **revenue now −52%** | P/S 6.4x, net margin −188%, rev **−52.5%** | 6/10 | ⚠️⚠️ **SI ~34%**, DTC ~9.7 — extremely crowded |
| **GME** — GameStop | Cash-rich meme/treasury | premium to net cash | 3/10 tradeable | ⚠️⚠️⚠️ DTC ~9, cult — never naked |

*C3.ai (AI) note:* fundamentals are genuinely broken now (**revenue declining 52%** YoY, net margin
−188% [VERIFIED — yfinance 2026-08-28]) — arguably a 6–7/10 *business* short — but SI ~34% + DTC ~9.7
makes it a coiled squeeze. **Puts only if at all.**

---

## 3. RANKED SUMMARY TABLE (this basket's universe)

Conviction = thesis + catalyst − tradeability. "Activist" = a named short-seller has a live 2025–26
report. **"Downside LEFT"** (per Hooman's copy-the-shorts refinement, §1b) = has the thesis NOT yet
played out + is there a concrete second-leg catalyst? This is now the primary sort key — a famous
short on a name that already dropped-and-recovered is NOT a setup.

| # | Ticker | Archetype | Live valuation flag | Activist short (date) | Catalyst | Conv. | Downside LEFT | SI% / DTC | Squeeze risk | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **TE** | Solar FRAUD claim | net −38.5%, GM 5.9%, D/E 283% | **Fuzzy Panda (5 reports '26) + Culper (Jan'26)** | Tax-credit/China-control ruling; restatement | **7/10** | **HIGH** | 30% / 1.5 | ⚠️ | **Best activist campaign (2 firms) — puts** |
| 2 | **RBLX** | Story cracking | P/B 179x, net −17.6%, SBC>loss | — (fundamental) | Guided bookings decline; child-safety litigation | **7/10** | **HIGH** | 2.2% / 1.0 | **LOW** | **Best tradeable — puts or small naked** |
| 3 | **LCID** | Broken EV | GM −96.6%, neg. equity, ~$1.5B/q burn | — (fundamental) | Dilution near-certain | **8/10 biz** | **MED-HIGH** | 34% / 2.4 | ⚠️⚠️ 16% borrow | **Best business, worst mechanics — puts only** |
| 4 | **ENSG** | SNF Medicare fraud claim | P/E 28x, profitable | **Muddy Waters (Jun'26)** | FCA suit / DOJ-CMS probe | **6/10** | **HIGH** (only −8%) | **3% / 3.5** | **LOW** | **Best activist mechanics — puts; needs fraud to land** |
| 5 | **TEM** | AI-health M&A rollup | P/S 8.9x, net −17.8%, PT<price | **Spruce Point (May'25)** | Personalis dilution; margin miss | **6/10** | **MED** (report aging) | 30% / 6.1 | ⚠️ beta 3.6 | **Puts** |
| 6 | **TARS** | Pharma Medicare claim | net −7.7%, P/S 5.2x | **Culper (Jul'26)** | Copay-scheme probe | **5/10** | **MED-HIGH** (newest) | 14% / 6.3 | Moderate | Biotech binary — puts |
| 7 | **SRAD** | Overvalued betting-data | P/E 213x, net 1.2% | **Muddy Waters (Apr'26)** | Gambling-regulatory/legal | **5/10** | **MED** | 13% / 5.5 | Moderate | Reputational, no hard clock |
| 8 | **CHTR** | Levered cable | D/E 442%, subs shrinking, EV≫equity | — | Cox-deal debt; broadband losses | **6/10** | **LOW** (~47% done) | 20.3% / 7.2 | ⚠️ | Much priced in |
| 9 | **CRCL** | Rate-dependent fintech | P/S 8.8x, EV/EBITDA 97x | — | Fed cuts; MS Underweight $38 | **6/10** | **MED** | 11% / 2.1 | LOW | Liquid, cleanish |
| 10 | **ADMA** | Channel-stuffing claim | profitable, P/S 4.1x | **Culper (Mar'26)** | Restatement/SEC | **5/10** | **MED-LOW** (dropped-&-bounced) | 12% / 8.5 | ⚠️ slow exit | Partial recovery already |
| 11 | **DKNG** | Overvalued gambling | net loss, EV/EBITDA 105x | **Spruce Point (Oct'25)** | State-tax/prediction-mkt regulation | **5/10** | **LOW-MED** | 8% / 2.9 | Moderate | Growing share — hard short |
| 12 | **AUR** | Pre-revenue autonomy | **P/S 2,281x** | **Bleecker St (May'25) + Kerrisdale (Aug'25)** | Timeline slip; dilution | **5/10** | **MED** | 16% / 7.3 | ⚠️ beta 2.66 | Puts, tiny |
| 13 | **W** | Never-profitable | neg. equity, EV/EBITDA 47x | — | 2027 converts; interest>op income | **6/10** | **LOW** (+36% YTD) | 12% / 2.7 | ⚠️ | Right thesis, wrong tape |
| 14 | **PLUG** | Neg-margin hydrogen | GM −24.7%, dilution | — | ATM dilution | **6/10** | **MED** | 23% / 5.0 | ⚠️ cult | Guidance rising |
| 15 | **KMX** | Used-car+subprime | P/E 40x, EV/EBITDA 27x | — | CAF credit build | **6/10** | **MED** | 10% / 5.2 | Moderate | Cleanest credit catalyst |
| 16 | **SOFI** | Fintech accounting claim | P/E 38x, P/S 5.8x, profitable | **Muddy Waters (Mar'26)** | Restatement (if it lands) | **4/10** | **LOW** (mkt rejecting) | 14% / 2.4 | ⚠️ beta 2.2 | Thesis not landing |
| 17 | **RKLB** | Space bubble | **P/S 56x, fwd P/E 1,350x** | **Bleecker St (Feb'25) — misfired** | Launch failure/delay | **4/10** | **~NONE** (ran up) | 7.5% / 2.3 | ⚠️ beta 2.63 | Report already failed |
| 18 | **IONQ** | Quantum hype | **P/S 70x** | **Kerrisdale (Mar'25) — misfired** | Dilution; theme unwind | **4/10** | **~NONE** (ran up) | 11% / 2.0 | ⚠️ beta 3.30 | Puts, tiny |
| 19 | **C3.ai** | AI, rev −52% | net −188%, rev −52% | — | Continued rev decline | **6/10 biz** | **MED** | 34% / 9.7 | ⚠️⚠️ | Coiled squeeze — puts only |
| 20 | **MSTR** | BTC treasury | now ~0.8x NAV | — | — | **2/10** | **NONE** (played out) | 8.5% / 2.0 | ⚠️ | ❌ Premium gone — DO NOT short |

---

## 4. HOW TO EXPRESS A $10k SHORT — mechanics (puts vs naked)

**The default answer for a $10k retail short book is: buy long PUTS, dated past the catalyst.**
- **Puts cap your loss at the premium** (defined risk), need **no borrow**, **can't be recalled**,
  and **can't be squeezed** out of you. A 34%-SI name (LCID, C3.ai, TEM) that would be suicidal to
  short naked is *safe-ish* as a put because your max loss is the premium.
- **Cost of the option = the borrow + the drift, priced in.** You pay for the privilege via implied
  volatility (these names have IV of 60–120%+). That's the trade-off: defined risk, but you need the
  move to happen *before expiry* and be *bigger than the premium*. Most puts expire worthless.
- **Naked short stock** is only defensible on the **low-SI, cheap-borrow, liquid** names (RBLX at
  2.2% SI, CRCL at 11%) and even then only in tiny size. **Never naked-short** anything > ~15% SI or
  with squeeze history (LCID, TE, TEM, KSS, BYND, PLUG, C3.ai, GME, CVNA).
- **Inverse/leveraged ETFs (SQQQ, BOIL, and any -2x/-3x): AVOID.** Hooman already got burned by
  leveraged-decay (BOIL/SQQQ). They rebalance daily and **decay toward zero in choppy markets even
  if you're directionally right** — they are not a "cheap way to be short," they are a fee-and-decay
  machine. Not in this basket.

**Practical put structure for each name:** buy **out-of-the-money puts ~4–7 months out** (past the
next 1–2 catalysts). OTM = cheaper premium, more leverage to the thesis; dated-far = buys time so a
squeeze/delay doesn't expire you worthless. Size each so the **premium** (not notional) is the
budgeted line item — the premium is your max loss.

**⚠️ The "silent-cover" trap (from Hooman's §1b stress-test) — one more reason to use puts, dated
short.** Because activist shorts publicize entry but **cover silently**, when you copy one you can't
know if they're still in it — Muddy Waters literally said it "may have begun covering" FTAI while
retail was still short, and FTAI ran +53%. Two defenses: (1) **buy puts, not stock** — your loss is
capped at premium if the short covered and the name rips, whereas a naked short is unbounded; (2)
**date the puts to the specific catalyst, not "forever"** — you're betting on the *second leg* (the
restatement/probe/print), so buy just past that event and don't roll indefinitely hoping the thesis
eventually works after the pros have long gone. If the catalyst passes with no second leg, exit.

---

## 5. CANADIAN TAX & ACCOUNT NOTES (VERIFIED-general, confirm with your accountant)

- **Short sales cannot be done in registered accounts** (RRSP/TFSA/RESP/FHSA) — they require a
  **margin account** in a **non-registered (taxable)** account. So this whole basket lives in taxable.
- **Gains on short sales are taxed as ordinary income (100% inclusion), NOT capital gains** in Canada
  — CRA generally treats short-selling profits as income from an adventure in the nature of trade.
  So your after-tax return is worse than an equivalent long capital gain. [ASSUMED — standard CRA
  treatment; confirm with your accountant for your situation.]
- **Buying long PUTS** is cleaner: a purchased option that you close is generally a **capital**
  gain/loss (50% inclusion) — *and puts can be held in registered accounts* at many brokers
  (long options are allowed in TFSA/RRSP where naked shorting is not). **This is another reason to
  prefer puts** — better tax character + broader account eligibility. [ASSUMED — confirm broker
  permissions + CRA treatment.]
- **Dividends paid on borrowed (shorted) stock are your expense** and the deductibility is limited —
  another carry drag on naked shorts of dividend payers.

---

## 6. THE SUGGESTED $10,000 BASKET

**Framing (read this first):** This is a **low-win-rate lottery book.** Realistic expectation:
**more than half of these lines expire worthless / lose money even if the theses are "right,"** and
the whole $10k could be lost. The basket only makes sense as ring-fenced entertainment/education
capital. The *higher-expected-value* version of every one of these views is simply **to not own the
name** — but you asked for the active expression, so here it is, built for **defined risk (puts) +
thesis diversification + no single squeeze blowing up the book.**

**Structure: 6 long-put positions, ~$1,650 each in premium, diversified across theses.** All puts,
no naked stock, no inverse ETFs. Buy OTM strikes, **~5–7 months to expiry** (Feb–Apr 2027) so
catalysts have time. This version leans harder into Hooman's #3 criterion — **4 of the 6 have a live
named activist short-seller behind them** (TE has two).

| # | Name | Thesis bucket | Who's short + why it's here | Vehicle | Premium | Honest edge grade |
|---|---|---|---|---|---|---|
| 1 | **TE puts** | Activist FRAUD (2 firms) | **Fuzzy Panda + Culper** — China-control / 45X-tax-credit-fraud / restatement; thesis-breaking binary | ~5–7mo OTM | **$1,700** | **Real edge if it lands** — strongest multi-firm signal |
| 2 | **RBLX puts** | Story stock cracking | No activist, but the cleanest fundamental catalyst (guided bookings decline + child-safety litigation) and lowest squeeze risk | ~5–7mo OTM | **$1,700** | **Real-ish edge** — cleanest catalyst |
| 3 | **LCID puts** | Broken business | No activist; negative gross margin = most broken model; dilution near-certain; puts neutralize the 16% borrow + 34% SI | ~6mo OTM | **$1,700** | **Best business thesis** — puts are the only sane vehicle |
| 4 | **ENSG puts** | Activist FRAUD | **Muddy Waters (Carson Block)** — Medicare license-rental/FCA fraud; best activist mechanics (3% SI, low beta) | ~6–8mo OTM | **$1,650** | Moderate — credible activist, but needs the FCA claim to bite a profitable compounder |
| 5 | **TEM puts** | Activist + AI-health rollup | **Spruce Point** + sell-side PT already below price; M&A-manufactured growth | ~6mo OTM | **$1,650** | Moderate — crowded (30% SI), needs a margin miss |
| 6 | **CHTR or CRCL puts** | Levered/structural OR rate-sensitive | No activist; a lower-variance diversifier away from small-cap fraud names: CHTR (leverage + sub losses) or CRCL (Fed-cut de-rate, liquid) | ~6mo OTM | **$1,600** | Moderate — slower-burn, lower-variance |

**Total premium at risk: ~$10,000 (max loss = the full $10k).**

**Why this mix:**
- **Every line has DOWNSIDE LEFT (Hooman's §1b filter):** 5 of 6 score HIGH or MED-HIGH — the thesis
  has NOT yet played out (TE near lows, ENSG only −8%, RBLX/LCID pre-catalyst) AND each has a concrete
  second-leg catalyst. I explicitly **excluded** the famous-short names that already
  dropped-and-recovered (RKLB, IONQ, SOFI, APP, FTAI) — copying a short after its move is paying for
  an edge already spent.
- **Thesis diversification (6 distinct catalysts):** activist-fraud/tax-credit (TE),
  story-stock-cracking (RBLX), broken-EV-business (LCID), activist-Medicare-fraud (ENSG),
  activist-overvaluation/M&A (TEM), levered-structural-or-macro (CHTR/CRCL). No two share a catalyst,
  so one squeeze can't torch the book.
- **Activist-backed (Hooman's #3, as a SOURCING tool):** 3 of 6 have a live named short-seller —
  **TE (Fuzzy Panda + Culper), ENSG (Muddy Waters), TEM (Spruce Point)** — spanning fraud, accounting,
  and overvaluation theses across three top-tier firms. The other 3 (RBLX, LCID, CHTR/CRCL) are
  fundamental-catalyst shorts that need no activist — deliberately, so the book isn't 100% dependent
  on "someone famous is short" (which can be stale via silent covering).
- **Squeeze-proofed + silent-cover-proofed:** every line is a **put** (defined risk, un-squeezable,
  and capped-loss if the pros have already covered) — essential because TE (30% SI), LCID (34%), TEM
  (30%) would be lethal to short naked.
- **No inverse ETFs, no leveraged decay, no naked unlimited-loss exposure.**
- **For slot #6, prefer CRCL over CHTR** on the downside-LEFT test: CHTR is already ~47% off its high
  (much priced in, LOW downside-left), whereas CRCL's rate-cut de-rating is still ahead of it (MED).

**Alternative "max-activist" variant** (if Hooman wants EVERY line activist-backed): swap RBLX→**SRAD
puts** (Muddy Waters) and LCID→**ADMA or TARS puts** (Culper) — but this concentrates in
fraud/regulatory binaries and loses the broken-business (LCID) and clean-catalyst (RBLX) diversifiers,
so I don't recommend it. **Better single swap:** if you want a sixth activist name over CHTR/CRCL, use
**DKNG puts** (Spruce Point) — but DKNG is a growing share-leader the sell-side loves (squeeze-on-
good-news risk).

**Sizing discipline:** each line is capped at premium = max loss; do not add margin, do not average
down into a squeeze, and treat expiry as a hard stop. If any thesis breaks in your favor early (a
restatement on TE, a dilution on LCID), take the win — don't hold puts to zero theta hoping for more.

**Expected outcome, stated honestly:** the base case is that **you lose most or all of the $10k.**
A good outcome is that **one or two lines (most likely RBLX or LCID or a TE fraud-confirmation) pay
multiples and cover the losers plus a profit** — that's how a put lottery book is *supposed* to work
(many small losses, a few big wins). If you're not comfortable with "most likely I lose it all," the
correct move is not to put this on — the risk-free version of every bearish view above is to **not
own** (or exit) the name, which you're largely already doing per the companion doc.

---

## 7. VERIFICATION LOG

**Live valuations + short interest:** `/opt/venv/bin/python3` + `yfinance` v1.5.1, scripts
`/tmp/short_pull_v2.py`, `_v3.py`, `_v4.py`, run **2026-08-27/28**. **FINRA short-interest
settlement date = 2026-08-14** (VERIFIED via `dateShortInterest` field) — fresh, not stale.

**Activist short-seller campaigns** — fetched from publisher pages + corroborated by a parallel
research agent using financial-press coverage, **2026-08-27/28**:
- **Spruce Point** — sprucepointcap.com/research [VERIFIED]: TEM (5/28/25), DKNG (10/3/25), IRTC
  (8/18/25), YOU (4/30/25), BG (3/25/26), SGHC (2/12/26), REZI (1/27/26), MNST (4/8/25), RELY
  (3/11/25), UEC (9/18/25), LMB (7/22/25); ZM (4/24/26) is a **long** idea (excluded).
- **Bleecker Street** — bleeckerstreetresearch.com/research [VERIFIED]: LYFT (7/23/26), Sharon AI
  (4/30/26), Via (12/16/25), PRDO (11/17/25), UTHR/LQDA (7/29/25), AUR (5/14/25), RKLB (2/25/25).
- **Fuzzy Panda** — fuzzypandaresearch.com [VERIFIED]: TE (5 reports May–Jun'26), FRMI (4/20/26),
  NUAI (12/12/25, OTC), EOSE (10/30/25), RCAT (10/10/25), RZLV (9/29/25), THC (6/11/25).
- **Muddy Waters** — muddywatersresearch.com [VERIFIED via report URLs]: **ENSG (6/11/26), SRAD
  (4/22/26), SOFI (3/2026)**; APP (2025) and FTAI (2025) theses have FAILED (stocks re-rated up).
- **Culper Research** — [VERIFIED via financial-press; own site 403'd]: TARS (7/1/26), NVDA
  (5/13/26), ADMA (3/24/26), **TE (1/21/26)**, ACHR (recurring), DASH (10/23/25, weak traction).
- **Kerrisdale** — [VERIFIED via financial-press; site 403'd]: MRAM (5/19/26), AFRM (1/21/26), BMNR
  (10/8/25), AUR (8/19/25), QBTS (4/29/25), IONQ (3/13/25). **Trap: the Feb'26 IONQ short was
  Wolfpack, NOT Kerrisdale.**
- **Grizzly Research** — [VERIFIED, prices via Yahoo]: 2025 US shorts MVST (−80%), KULR (−75%), PONY
  (−42%), ACHR (−35%), XP (recovered, sued Grizzly), WGS/NXST (failed); 2026 slate is European.
- **Scorpion Capital** — scorpioncapital.com [VERIFIED]: SLNO (8/15/25).
- **Viceroy Research** — viceroyresearch.org [VERIFIED]: Blue Moon Metals (TSXV:MOON) + Abaxx
  (TSX:ABXX) — **Canadian small-caps, not US-optionable, excluded.**
- **Morpheus Research** (Hindenburg successor) — [VERIFIED via Bloomberg]: US targets ABL, Innventure,
  Figure, Velo3D — not deep-dived here; worth a follow-up.
- Stock-reaction %s / litigation follow-ups from press are **UNVERIFIED** (primary wires were
  fetch-blocked); confirm against 8-Ks/EDGAR/Reuters before trading.

**Landscape corrections (VERIFIED):**
- **Hindenburg Research disbanded 2025-01-15** (final report Carvana 2025-01-02) [Wikipedia, fetched
  2026-08-28] — no longer a live signal; successor is **Morpheus Research**.
- **Muddy Waters is ACTIVE** — an earlier note that its site was "unreachable" was a transient fetch
  failure; ENSG/SRAD/SOFI campaigns are VERIFIED via its report URLs.
- **T1 Energy (TE) is DOUBLE-targeted** — Fuzzy Panda (2026, 5 reports) + Culper (Jan 2026) — the
  strongest multi-firm cross-validation in the set.
- **CHTR short interest is ~20.3% of float** (stockanalysis.com, 2026-08-28) — **yfinance's 51.6%
  reading was a glitch** and is disregarded.
- **MSTR now trades at ~0.8x its bitcoin NAV** (840,447 BTC × ~$80k ≈ $67B vs ~$52.8B mkt cap)
  [stockanalysis.com, 2026-08-28] — the famous mNAV-premium short has **already played out; not a
  short here.**
- **C3.ai (AI) revenue is now −52.5% YoY** with net margin −188% [yfinance, 2026-08-28] — the
  business is genuinely deteriorating, but SI ~34% makes it puts-only.

**Confidence gaps to close before trading:**
- **All cost-to-borrow figures are UNVERIFIED-live** (borrow-data providers paywalled). Re-check CTB
  + share availability on **IBKR** (shows live) before any short; for puts this matters less (IV
  already prices it) but availability of listed options matters for the small-caps (TE, AUR).
- **Specific allegation wording** for most names is summarized from publisher pages + press, not
  read out of the full report PDFs — read the actual reports before sizing (UNVERIFIED-detail).
- Muddy Waters' ENSG "$7B FCA exposure," Sportradar "20–40% illegal-gambling revenue," and Culper's
  ADMA/TARS specifics are the short-seller's *own claims*, not independently confirmed — treat as
  ASSUMED/allegation until validated.
- **Blue Orca 2026 slate not confirmed** (site 403'd, agent did not corroborate). Culper, Kerrisdale,
  and Grizzly slates were corroborated via financial-press by a parallel agent.
- Two of three background research agents hit **Bedrock 503 errors** mid-run; their scope
  (Spruce-Point-cluster + AI-bubble cluster) was re-covered directly via publisher fetches, and a
  third agent later returned the Muddy Waters / Culper / Kerrisdale / Morpheus additions integrated
  above — no material gap remains.

*End of report. Not financial advice. Puts, not naked shorts. Re-verify borrow/short-interest and
read the full activist reports before any trade. Most of this basket can be lost — size accordingly.*
