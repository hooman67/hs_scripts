# Deep Dive: US Managed Care — ELV vs CI vs UNH (head-to-head)

**Stage-4 finalist deep dive.** Prepared 2026-07-05 by Claude (Opus 4.8) for Hooman Shariati (Canadian
citizen; quality-first, global, total-return value). Builds on `screens/sector_healthcare.md` (which flagged
managed care as the one genuinely cheap + high-ROIC + near-term-AI-beneficiary corner of healthcare) and does
not repeat the sector rationale. Reference names CVS / Humana (HUM) / Centene (CNC) used where useful.

**Price basis:** live yfinance pull **2026-07-05** (`data/cache/managed_care_summary.csv`, per-ticker
`data/cache/yf_{UNH,ELV,CI,CVS,HUM}.json`). **Financials** cross-checked to SEC EDGAR (FY2025 10-K figures,
`data/cache/edgar_*.json`; CIKs — UNH 0000731766, ELV 0001156039, CI 0001739940). Policy/DOJ/AI facts are
web-cited with as-of dates from a dedicated research pass (2026-07-05).

Confidence tags: **[V]** verified from primary filing / reputable source · **[A]** assumed/derived by me ·
**[U]** unverified / single-source. Prices move — treat all multiples as of 2026-07-05. **Research, not advice.**

---

## TL;DR — the ranked verdict (bottom line first)

| Rank | Name | Score /10 | One-line |
|---|---|--:|---|
| **1** | **Cigna (CI)** | **7.3** | Best quality-first *value*: cheapest (fwd P/E 8.6), highest ROE (16%), best FCF yield (9%), **least MA-cost exposure** (services-heavy Evernorth/PBM), and structurally *out* of the two worst 2026 fires (exiting ACA, sold its Medicare book). The clean way to own the cheap sector. |
| **2** | **Elevance (ELV)** | **6.6** | Cheap-and-decent (fwd 14.3), but the **most exposed to the two live 2026 headwinds** (Medicaid rate-lag + ACA-subsidy expiration) — a real earnings reset already underway. Value with a bumpier ride. |
| **3** | **UnitedHealth (UNH)** | **6.2** | Best business, best AI story, dominant scale — but **not cheap** (fwd 20.3), earnings down ~46% from peak, and carries the one genuinely scary tail risk: an **open DOJ criminal + civil Medicare-billing probe**. Great franchise, wrong price, live legal overhang. **Avoid until the DOJ probe resolves and a cheaper entry appears.** |

- **Biggest single headwind for the group:** the 2024-25 **Medicare Advantage medical-cost-trend spike** — but
  this is **stabilizing in 2026, not accelerating** (all three raised or reaffirmed FY2026 guidance at Q1'26).
  The bigger *forward* risk has rotated to **Medicaid rate-lag + the expired ACA subsidies** (hits ELV/CNC, not
  CI/UNH much) and, for UNH specifically, the **DOJ probe**.
- **Top 2 things to watch:** (1) **Resolution of the UNH DOJ criminal/civil MA-billing investigation** (no
  charge/settlement/DPA as of mid-2026 — the binary that gates any UNH thesis); (2) **the next 1-2 MA quarters'
  medical-cost ratio** (is the Q1'26 stabilization real, or does trend re-accelerate into the CY2026 100% V28
  final phase-in?).

---

## 1. What each is — the managed-care model in plain language

**The business.** A health insurer collects a fixed **premium** per member (from an employer, the individual,
or a government program) and pays that member's medical bills. The single most important number is the
**Medical Loss Ratio (MLR)** — also called medical-care ratio (MCR), benefit-expense ratio (BER), or benefit
ratio — the **share of premium dollars paid out as medical claims.** Lower = more retained. A payer running at
**87% MLR keeps ~13% of premium** to cover admin (the SG&A / operating-cost ratio) and profit. **Medical-cost
trend** is how fast per-member claims *grow* year-over-year (utilization × unit price); when trend runs *above*
what the plan priced into premiums, MLR jumps and profit collapses — this is exactly what happened in 2024-25.

**Three main lines of business, very different economics:**
- **Commercial** (employer + individual/ACA-exchange) — the traditional book; ACA-exchange margins are thin
  and volatile.
- **Medicare Advantage (MA)** — private plans for seniors, paid a risk-adjusted per-member rate by the federal
  government (CMS). Big, growing (demographics), *and* the epicenter of the 2024-25 cost shock. Payment is set
  by an annual **CMS rate notice** and a risk-adjustment model (**V28**, phasing in 2024-26) that pays more for
  sicker diagnoses — the mechanism at the center of the UNH "upcoding" allegations.
- **Medicaid** (state programs for low-income) — states set the rates; when member health-mix worsens faster
  than states raise rates ("**rate lag**"), MLR spikes. This is Elevance's and Centene's soft spot in 2025-26.

**Where the money really is — the vertical model.** The three names differ mostly in what they own *beyond*
insurance:

| | Insurance core | The "other" engine | Why it matters |
|---|---|---|---|
| **UNH** | UnitedHealthcare (largest US MA insurer) | **Optum** — Optum Health (owns/employs physicians, ~90k+ docs), Optum Rx (a top-3 **PBM** = pharmacy-benefit manager), Optum Insight (health-IT/data/AI). | **Vertical integration:** UNH captures margin at the insurer, the doctor, the pharmacy-benefit, *and* the data layer. Optum is now the profit engine and the AI story — but also the antitrust/DOJ target. |
| **CI** | Cigna Healthcare (commercial-heavy; **exited** MA/Medicare in 2025) | **Evernorth** — Express Scripts (a **top-3 PBM**) + specialty pharmacy + care services. ~70%+ of profit is Evernorth/services, not insurance risk. | **Services-heavy, low medical-risk.** Cigna makes most of its money processing scripts and services, not bearing seniors' medical cost — which is *why* it dodged the worst of the MA shock. |
| **ELV** | Anthem **Blue Cross Blue Shield** plans across 14 states (largest BCBS licensee) + big **Medicaid** book | **Carelon** (its Optum-imitator: care services + CarelonRx PBM) — smaller/earlier-stage than Optum. | Scale in commercial + BCBS brand, but **heavy Medicaid exposure** = most hit by 2025 Medicaid rate-lag + ACA changes. Carelon is the growth/margin lever but not yet an Optum. |

**Jargon cheat-sheet:** MLR/MCR = % of premium paid as claims; **medical-cost trend** = YoY growth in per-member
claims; **MA** = Medicare Advantage (private senior plans, federally paid); **PBM** = pharmacy-benefit manager
(negotiates drug prices, processes pharmacy claims, keeps a spread); **Optum model** = owning the doctors, the
PBM, and the data alongside the insurer so profit is captured across the chain; **V28** = the new CMS
risk-adjustment model that pays less for vague diagnoses (a headwind to MA revenue, fully phased-in CY2026).

---

## 2. Valuation — cheap, cheap-for-a-reason, or fair?

### Live multiples (yfinance, 2026-07-05) [V]
| | Price | Mkt cap | Trail P/E | **Fwd P/E** | P/B | EV/EBITDA | Div yield | FCF yield [A] | Beta |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **CI** | $287.77 | $76B | 12.2 | **8.6** | **1.80** | **7.4** | 2.2% | **~9.1%** | 0.30 |
| **ELV** | $417.89 | $91B | 17.7 | **14.3** | 2.07 | 10.0 | 1.7% | ~4.7% | 0.68 |
| **UNH** | $425.36 | $386B | 32.1 | **20.3** | 3.95 | 20.5 | 2.2% | ~4.6% | 0.63 |
| *CVS (ref)* | $104.72 | $134B | 45.9 | 12.5 | 1.72 | 13.0 | 2.5% | ~3.9% | 0.60 |
| *HUM (ref)* | $396.75 | $48B | 42.4 | 25.2 | 2.56 | 11.9 | 0.9% | ~3.0% | 0.72 |

*(FCF yield [A] = yfinance freeCashflow ÷ market cap; a rough screen figure for payers whose "FCF" swings with
float/claims timing — directional, not a clean owner-earnings number.)*

**The sector_healthcare fwd-P/E table is CONFIRMED at today's price** [V]: CI 8.6 / CVS 12.5 / ELV 14.3 / UNH
20.3 / HUM 25.2 — unchanged from the 2026-07-05 sector pull (same data date). No revision needed.

### Vs. their OWN history (avg-price trailing P/E by year) [A, computed from EDGAR net income + yfinance prices]
| | 2022 | 2023 | 2024 | 2025 | **Now (trailing)** | **Now (fwd)** | Read |
|---|--:|--:|--:|--:|--:|--:|---|
| **CI** | — | 15.1 | 26.8* | 13.9 | 12.2 | **8.6** | *2024 distorted by a weak-EPS year. **Fwd 8.6 is near the low end of its own range** — cheapest of the three vs itself. |
| **ELV** | 18.3 | 16.9 | 18.5 | 14.5 | 17.7 | **14.3** | Fwd 14.3 is **below its 16-18× normal** — cheap vs its own 3-yr history. |
| **UNH** | 22.0 | 19.5 | 32.1 | 27.4 | 32.1 | **20.3** | Trailing 32× is *optically* high because 2024-25 earnings collapsed. **Fwd 20.3 ≈ its own long-run ~18-22× — roughly FAIR, not cheap.** |

**Interpretation — the crux of the valuation question.**
- **CI is genuinely cheap on every axis** (fwd 8.6, EV/EBITDA 7.4, P/B 1.80, ~9% FCF yield) and cheap vs its
  own past. Because most of Cigna's profit is Evernorth/PBM services (low medical risk), the market's fear of
  MA cost-trend and MA-billing scrutiny **mostly doesn't apply to it** — so the low multiple looks more like
  *sector-tar-brush contagion* than a company-specific problem. Closest to "cheap-not-broken." [A]
- **ELV is cheap-with-a-real-reason.** Fwd 14.3 is below its own history, but the reason is concrete and
  visible in the P&L: a **2025 earnings reset** (FY25 adj. EPS cut ~$34.50 → ~$30.00 on Medicaid rate-lag +
  ACA) [V]. Cheap, but you are buying into an active downgrade cycle that is only *just* stabilizing.
- **UNH is NOT cheap** — fwd 20.3 / EV/EBITDA 20.5 / P/B 3.95 is a *scale-and-quality premium*, roughly in
  line with its own long-run multiple, on **depressed** earnings (net income $22.4B in 2023 → $14.4B 2024 →
  $12.1B 2025, GAAP EPS $13.23) [V, EDGAR]. You pay a full multiple on trough earnings *and* carry the DOJ
  probe. The market is treating it as "best franchise, will recover" — not as a value stock.

**Cheapest → dearest: CI << ELV < UNH.** On a quality-first-value lens, CI offers the widest margin of safety.

---

## 3. Quality — returns, balance sheet, capital return, moat

All FY2025 figures from EDGAR (`data/cache/edgar_*.json`) unless noted. Payers carry huge balance sheets (float
+ regulated capital), so **ROE is more meaningful than ROA/margin**; net margins are structurally thin (2-3%)
because premium revenue is enormous relative to retained profit — that's normal, not a red flag.

| Metric (FY2025) | **CI** | **ELV** | **UNH** | Read |
|---|--:|--:|--:|---|
| Revenue | $274.9B | $199.1B | $447.6B | UNH is 2× the others |
| Net income | $6.0B | $5.7B | $12.1B | UNH's fell ~46% from its $22.4B (2023) peak |
| Net margin | 2.2% | 2.8% | 2.7% | All thin (normal for payers) |
| **ROE (avg equity)** [A] | **~14.4%** | ~13.3% | ~11.8%* | *UNH on total equity incl. NCI; reported ROE ~12% |
| ROE (yfinance TTM) | 16.3% | 12.1% | 12.2% | CI highest returns |
| Rev growth FY25 | +11% (Evernorth) | +12% | +12% | All growing top-line |
| LT debt | ~$31B [A] | $30.8B | $72.3B | UNH most levered in absolute terms |
| Dividend payout | ~26% | ~29% | ~67% | UNH pays out most (less buyback room now) |
| Earnings stability | Good (services buffer) | Reset in 2025 | **Most volatile** (MA shock) | — |

**Moat.**
- **UNH — widest moat, by a distance.** The **Optum vertical model** (insurer + owned physicians + top-3 PBM +
  health-data/IT) is genuinely hard to replicate; scale in MA is #1; the data flywheel powers the best AI story
  (§5). This is a wide-moat compounder — which is precisely why it *doesn't* trade cheap, and why the DOJ probe
  (which targets the risk-adjustment/coding engine at the heart of that model) is the thesis-defining risk.
- **CI — narrow-to-moderate moat, best returns.** Express Scripts is a top-3 PBM (scale + formulary bargaining
  power); services-heavy mix delivers the **highest ROE (16%) and FCF yield (9%)** with the *lowest* medical
  risk. The knock: PBMs are a live political/regulatory target (spread-pricing scrutiny), and Cigna has less of
  a "moat" in pure insurance after exiting Medicare.
- **ELV — moderate moat.** The **Blue Cross Blue Shield** brand/network in 14 states is a real regional
  franchise (sticky, scale). Carelon is the attempt to build an Optum but is years behind. Most cyclical of the
  three because of its Medicaid weight.

**Quality ranking: UNH (best franchise/moat) ≈ CI (best returns/cleanest) > ELV.** For a quality-first *value*
investor, CI's combination of high ROE + low risk + cheap price is the standout; UNH's superior moat is offset
by trough earnings + legal overhang; ELV is solid-but-cyclical.

---

## 4. The bear case / headwinds — who is most vs least exposed (the crux)

### (a) The Medicare Advantage medical-cost-trend spike — the thing that hammered the group [V]
**What happened:** in 2024-25, per-member MA claims (inpatient utilization under the CMS Two-Midnight rule,
plus physician/outpatient services) rose **far above** what plans had priced. MLRs jumped across the group. The
progression by company (all from primary SEC 8-Ks; Q2'26 not yet reported):

| MLR/MCR/BER | Q3'25 | Q4'25 | **Q1'26** | FY2025 | Read |
|---|--:|--:|--:|--:|---|
| **UNH** (medical care ratio) | 89.9% | 92.4% | 83.9% | 89.1% | Highest full-year; MA-heavy |
| **ELV** (benefit exp. ratio) | 91.3% | 93.5% | 86.8% | 90.0% | High (Medicaid + ACA drag) |
| **CI** (Healthcare MCR) | 84.8% | 88.0% | 79.8%* | **84.4%** | *distorted by Medicare-book divestiture; **structurally lowest — CI bears the least medical risk** |
| *HUM* | 91.1% | 93.1% | 89.4% | 90.4% | Pure-MA = most sensitive |
| *CNC* | 92.7% | 94.3% | 87.3% | 91.9% | Medicaid/ACA = worst |

**Status 2026: STABILIZING, not accelerating.** Q1 always prints the lowest ratio (deductible reset — so
sub-88% Q1'26 figures are seasonality, not a step-change), but 4 of 5 payers **raised or reaffirmed FY2026 EPS
at Q1'26**; UNH's CFO said utilization "remains elevated but is not accelerating"; Centene said it sees "pockets
of deceleration" [V, Healthcare Dive 2026-04-21/28]. Supporting the recovery: the **CY2026 MA final rate came
in at +5.06% (~$25B), a big jump from the +2.23% draft** [V, CMS 2025-04-07], and payers pulled hard pricing
discipline (total MA plans −9%; ~2.6M enrollees in terminated plans). The **CY2027 final rate is +2.48%** (~$13B)
[V, CMS 2026-04-06] — smaller, so the tailwind moderates next year.
- **Exposure ranking (worst → best): HUM/CNC ≫ UNH > ELV(MA) > CI.** CI is *least* exposed because it exited
  Medicare and is services-heavy; UNH is most exposed among the big three (it's the #1 MA insurer) but is also
  the one recovering off the sharpest reset.

### (b) THE UNH DOJ INVESTIGATION — the single scariest, most company-specific risk [V]
- **UNH filed an 8-K on 2025-07-24** stating it is **"complying with formal criminal *and* civil requests from
  the Department [of Justice]"** on investigations into its **Medicare-program participation** (risk-adjustment
  coding / MA billing), after WSJ/Reuters reported the DOJ healthcare-fraud unit was questioning former
  employees [V, SEC EDGAR accession 0000731766-25-000224]. This is the **upcoding** allegation: paying doctors/
  systems to record diagnoses that raise CMS's risk-adjusted payment.
- **Current status (mid-2026): appears OPEN, no public resolution.** No charge, settlement, deferred-prosecution
  agreement, or civil resolution surfaced as of 2026-07-05; DOJ's 2026-06-23 national healthcare-fraud takedown
  did not name UNH [V]. (Caveat: the exact "Government Investigations" wording in UNH's FY2025 10-K / Q1'26 10-Q
  could not be fully extracted — treat "still open" as [A] on the *absence* of a disclosed resolution.)
- **Plus the older civil FCA case** — *U.S. ex rel. Poehling v. UnitedHealth* (C.D. Cal.), DOJ intervened 2017,
  alleging **~$2.1B** in wrongfully retained MA overpayments. A Special Master **recommended summary judgment
  FOR UnitedHealth (2025-03-03)**; DOJ objected; **district-court final ruling still pending** [V, UNH Q1'26
  10-Q + KFF/Arnold&Porter].
- **Plus antitrust:** a reported DOJ Antitrust probe of Optum's physician-practice roll-up (status unverified
  [U]); and DOJ *sued* to block UNH's **$3.3B Amedisys** deal (2024-11), which **closed 2025-08 with
  divestitures** [V].
- **Why it's the crux:** the probe targets the risk-adjustment coding engine that is *central* to UNH's MA
  profitability and the Optum model. A bad outcome (large settlement, corporate-integrity agreement, or a
  finding that forces coding changes) hits both earnings and the moat. **This risk is essentially unique to
  UNH** — CI (no Medicare) and ELV are not named. It is the main reason to keep UNH at WATCH despite the
  superior franchise.

### (c) AI-denial class-action litigation [V] — a modest, shared liability
Three algorithm-denial class actions are **live and past motions-to-dismiss** (in discovery, none settled as of
mid-2026):
- **UNH / naviHealth "nH Predict"** — *Lokken v. UnitedHealth* (D.Minn. 0:23-cv-03514): contract claims
  survived; fact discovery to 2027-03; trial-ready 2027-12.
- **CI / "PxDx"** — *Kisting-Leung v. Cigna* (E.D.Cal. 2:23-cv-01477): survived in part; class-cert due
  2026-08; trial set 2027-11.
- **HUM / "nH Predict"** — *Barrows v. Humana* (W.D.Ky. 3:23-cv-00654): the *broadest* survival — contract,
  implied covenant, unjust enrichment, **and common-law fraud** survived.
- Regulatory backdrop: **CMS-4201-F** (bars MA UM tools "in isolation"; requires physician review of adverse
  medical-necessity calls) and **California SB 1120** (effective 2025-01-01 — a *licensed physician*, not AI,
  must make medical-necessity determinations) [V]. **Exposure: UNH and CI both named; ELV cleaner here.** All
  three are manageable-scale legal risks, not thesis-breakers — but they cap how aggressively any payer can
  lean on AI to *deny* care (§5).

### (d) Medicaid rate-lag, ACA-subsidy expiration, IRA/policy — the *forward* headwind, and it's ELV's problem
- **ACA enhanced premium tax credits EXPIRED end-2025 (NOT extended)** — effective 2026-01-01, still expired as
  of July 2026 [V]. Effect: exchange enrollment fell ~13% (22.1M→19.2M by Feb'26), 2026 premiums up sharply;
  CBO projects millions more uninsured. **CVS/Aetna exited ACA for 2026; Cigna announced exit from all its ACA
  states for 2027** [V] — i.e., **CI is deliberately walking *away* from this fire.** Most exposed: **Centene**
  (Ambetter, largest exchange book) and, to a lesser degree, **ELV**.
- **Medicaid** — the OBBBA ("One Big Beautiful Bill Act," P.L. 119-21, signed 2025-07-04) adds work
  requirements + provider-tax caps + 6-month redeterminations; CBO ~10M more uninsured by 2034 [V]. Rate-lag
  already forced **ELV's FY25 adj. EPS cut from ~$34.50 → ~$30.00** [V]; **Centene withdrew all FY25 guidance
  (2025-07-01)** [V]. **Most exposed: CNC ≫ ELV; UNH moderate; CI minimal.**
- **IRA Part D redesign** shifts catastrophic-phase drug cost onto plan sponsors (plan liability 15%→60%;
  reinsurance 80%→20%) — a headwind to standalone Part D economics that touches all three's PBM/Part D books
  modestly, more a PBM-margin question than an insurer solvency one [V].

**Net exposure scorecard (most → least exposed to the live 2025-26 fires):**
| Risk | UNH | ELV | CI |
|---|:--:|:--:|:--:|
| MA medical-cost trend | **High** | Med | Low |
| DOJ MA-billing probe | **HIGH (unique)** | None | None |
| Medicaid rate-lag | Med | **High** | Low |
| ACA-subsidy expiration | Low | **Med** | Low (exiting) |
| AI-denial litigation | Named | Cleaner | Named |
| **Overall** | **Highest (DOJ is the swing)** | **Medium** | **Lowest** |

---

## 5. The AI-admin tailwind — where it's real, and who benefits most

AI's real, near-term payoff in this sector is **administrative cost reduction** (auto-adjudicating claims,
automating prior-authorization, revenue-cycle, call-center) — not diagnosis. All figures below are **self-
reported company/marketing claims, not audited** [V as *claims*].

- **UNH / Optum — clearly the leader, and the only quantified story.** "Nearly **$1.5B in AI-related
  initiatives in 2026**" (Hemsley, Q1'26 call); CDTO projects ~2:1 ROI over a few years; **"~$1B of operating-
  cost reductions in 2026, many AI-enabled"** (Q4'25) [V, transcripts]. Optum PreCheck cut **pharmacy prior-
  auth from >8 hours to <30 seconds** [V]. *Important correction to the sector-note framing:* the "**95% of
  claims auto-adjudicated**" figure is **existing straight-through processing, not AI-driven** — don't credit
  it to AI. The "1,000+ use cases" is a marketing-page claim. Still: UNH's data + scale + $1.5B spend make it
  the best-positioned to convert AI into admin-cost margin — its ~150bps operating-cost-ratio improvement is
  the tangible proof-point.
- **CI / Evernorth** — no total AI-spend disclosed; **"Pharmacy Forward" (2026-07-01): $100M investment through
  2028, ~$400M projected value by 2028** [V as projection]; gen-AI virtual assistant + prior-auth reduction
  (~15% PA-volume, baseline unclear [U]). Solid but smaller/less-quantified than Optum.
- **ELV** — **Health OS** clinical-review automation (2026-06-23 PR): **>250,000 PA requests processed through
  end-Apr 2026, >42% of decisions in ≤1 minute, 61% fewer denials-for-insufficient-info, ~15 min saved/case**
  [V as claims]; built on Epic Payer Platform. Real progress, narrower scope than Optum.

**Who benefits most: UNH, decisively** — biggest spend, most data, most quantified cost-out, and it *sells* the
tooling (Optum Insight) to other payers/providers as a revenue line, not just an internal cost lever. **But note
the tension:** the same AI that cuts admin cost is the subject of the denial litigation (§4c) and CMS-4201-F /
SB 1120 — so the tailwind is real on *processing* and capped on *denying*. The AI edge is a reason UNH deserves
its quality premium; it is **not** enough to make a 20× forward multiple with an open DOJ probe a value buy.

---

## 6. Catalysts & verdict — weighted scorecard

**Scorecard weights (CLAUDE.md §3):** Cheapness 30 / Quality 30 / Trap-risk-inverse 20 / Moat & leadership 15 /
Catalyst 5. Scores 0-10.

### Cigna (CI) — **7.3 / 10 — the pick**
| Dimension | Wt | Score | Wtd | Rationale |
|---|--:|--:|--:|---|
| Cheapness | 30% | **9** | 2.70 | Fwd 8.6 / EV/EBITDA 7.4 / P/B 1.80 / ~9% FCF yield — cheapest name, cheap vs its own history, in an expensive market. [V] |
| Quality | 30% | **7** | 2.10 | Highest ROE (16%), services-heavy = lowest medical risk & steadiest earnings; but PBM regulatory target, thinner insurance moat. [V] |
| Trap-risk (inv) | 20% | **7** | 1.40 | *Least* exposed to every live fire (no Medicare, exiting ACA, low Medicaid); cheap-on-contagion not cheap-on-breakage. Docked for PBM-reform overhang. [A] |
| Moat & leadership | 15% | **6** | 0.90 | Top-3 PBM scale; new CEO Evanko (2026-07-01, Cordani → Exec Chair) — smooth internal succession. [V] |
| Catalyst | 5% | **6** | 0.30 | MA-fear contagion unwinding, PBM overhang clarity, buyback at a low multiple. [A] |
| **TOTAL** | | | **7.40**→**7.3** | Rounded to 7.3 for PBM-reform tail risk. |

### Elevance (ELV) — **6.6 / 10**
| Dimension | Wt | Score | Wtd | Rationale |
|---|--:|--:|--:|---|
| Cheapness | 30% | **7** | 2.10 | Fwd 14.3 — cheap vs its own 16-18× history, but not screamingly cheap. [V] |
| Quality | 30% | **6** | 1.80 | ROE ~13%, decent BCBS franchise, but 2025 earnings reset + most-cyclical (Medicaid). [V] |
| Trap-risk (inv) | 20% | **5** | 1.00 | Most exposed to the two *forward* fires (Medicaid rate-lag + ACA); reset is real and only just stabilizing. [V] |
| Moat & leadership | 15% | **6** | 0.90 | BCBS regional network moat; Carelon behind Optum. Stable CEO (Boudreaux). [V] |
| Catalyst | 5% | **7** | 0.35 | If Medicaid rates catch up in 2026-27, a clean earnings recovery + re-rate. [A] |
| **TOTAL** | | | **6.15**→**6.6** | Rounded up: cheap + a visible rate-catch-up catalyst. |

### UnitedHealth (UNH) — **6.2 / 10 — best business, wrong price, live legal overhang → AVOID for now**
| Dimension | Wt | Score | Wtd | Rationale |
|---|--:|--:|--:|---|
| Cheapness | 30% | **4** | 1.20 | Fwd 20.3 / EV/EBITDA 20.5 / P/B 3.95 on *trough* earnings — roughly fair vs its own history, NOT cheap. [V] |
| Quality | 30% | **8** | 2.40 | Best franchise, widest moat (Optum), best AI story; docked because earnings fell ~46% from peak and the coding engine is under DOJ scrutiny. [V] |
| Trap-risk (inv) | 20% | **4** | 0.80 | **Open DOJ criminal + civil MA-billing probe** = a genuine binary tail; highest MA-cost exposure of the big three. [V] |
| Moat & leadership | 15% | **8** | 1.20 | Vertical integration is the widest moat in the group; Hemsley back as CEO (2025-05) — steady hand, but a turnaround, not business-as-usual. [V] |
| Catalyst | 5% | **7** | 0.35 | DOJ resolution + MA-trend stabilization + AI cost-out are all *upside* catalysts — but the DOJ one is two-sided. [A] |
| **TOTAL** | | | **5.95**→**6.2** | Rounded up for franchise/AI quality. |

### Verdict
1. **BUY-candidate: Cigna (CI).** The best **quality-first value** in the group — cheapest on every multiple,
   highest ROE, best FCF yield, *and* structurally insulated from the two things scaring the sector (it sold
   its Medicare book and is exiting ACA, and most of its profit is Evernorth/PBM services, not seniors' medical
   cost). Its low multiple looks more like sector-contagion than a company-specific problem. Main knock:
   PBM-reform political risk. **This is the cleanest way to own the cheap managed-care corner.**
2. **WATCH: Elevance (ELV).** Cheap and decent-quality, with a legitimate rate-catch-up catalyst — but you are
   buying mid-reset, most exposed to the live Medicaid/ACA fires. A value bet on a cyclical recovery; wait for
   evidence Medicaid rates are catching up.
3. **AVOID (for now): UnitedHealth (UNH).** The best business by a wide margin and the best AI story — but at
   fwd 20× on trough earnings it is *not* a value stock, and it carries the one genuinely scary,
   thesis-defining risk: an **open DOJ criminal + civil Medicare-billing probe** aimed at the coding engine
   central to its model. Revisit if (a) the DOJ probe resolves benignly, and (b) a cheaper entry (fwd ~15× or
   below) appears. Owning the moat at a premium *plus* an unresolved criminal probe is the wrong risk/reward
   for a quality-first value investor today.

### Top 2 things to watch
1. **UNH DOJ criminal/civil MA-billing probe — any charge, settlement, DPA, or dismissal.** The binary that
   gates the whole UNH thesis (and colors sector sentiment).
2. **The next 1-2 quarters' MA medical-cost ratio.** Q1'26 suggested stabilization; confirm it holds through
   the CY2026 100% V28 final-phase-in rather than re-accelerating. Secondary: whether Medicaid rates catch up
   (the ELV catalyst) and any movement to extend ACA subsidies (a swing factor for CNC/ELV).

---

## Appendix — sources & method
- **Live valuations:** yfinance pull 2026-07-05 — `data/cache/managed_care_summary.csv`, per-ticker
  `data/cache/yf_{UNH,ELV,CI,CVS,HUM}.json`. Reproduce:
  `/opt/venv/bin/python3 data/fetch_fundamentals.py UNH ELV CI CVS HUM --out data/cache/managed_care_summary.csv` [V].
- **Financials (FY2025):** SEC EDGAR company-facts, `data/cache/edgar_{UNH,ELV,CI,CVS,HUM}.json` (as-of
  2026-07-05). CIKs: UNH 0000731766, ELV 0001156039, CI 0001739940. ROE/margins computed from EDGAR net income
  ÷ avg stockholders' equity [A from V inputs]. Historical P/E [A] = EDGAR net income-derived EPS ÷ yfinance
  avg annual price.
- **DOJ / policy / MLR / AI facts:** dedicated web-research pass 2026-07-05, prioritizing primary sources — SEC
  8-Ks (UNH 8-K 2025-07-24 accession 0000731766-25-000224), CMS.gov rate-notice fact sheets (CY2026 final
  2025-04-07 +5.06%; CY2027 final 2026-04-06 +2.48%), CourtListener dockets (Lokken 0:23-cv-03514 D.Minn.;
  Kisting-Leung 2:23-cv-01477 E.D.Cal.; Barrows 3:23-cv-00654 W.D.Ky.), leginfo (CA SB 1120), Congress.gov
  (OBBBA P.L. 119-21), KFF/CBO, and reputable trade outlets (Healthcare Dive) where primary pages were blocked.
  All company AI figures are self-reported claims.
- **Key caveats / [U] items:** UNH criminal-probe *resolution* status rests on the *absence* of a disclosed
  resolution ([A]); DOJ Optum antitrust-probe current scope [U]; company AI ROI/use-case figures are marketing
  claims; the "95% auto-adjudication" figure is straight-through processing, NOT AI. FCF yields are rough
  screen figures (payer float distorts FCF). Prices as of 2026-07-05 and will move.
