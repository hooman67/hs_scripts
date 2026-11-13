# Sector Deep-Dive — HEALTHCARE (is it cheap, and is the AI/aging thesis real?)

Run: 2026-07-04/05 by Claude (Opus 4.8). Owner: Hooman Shariati (Canadian citizen; quality-first, global, value).
Builds on Stage-1a (`sector_cheapness.md`), where broad "healthcare" did **not** appear among the cheapest
US/Global/EM sectors. This decomposes healthcare into its Damodaran sub-industries and tests the two-part
narrative Hooman heard: "healthcare is very cheap right now and will benefit a lot from AI."

> **Anti-hallucination.** Every multiple is a real fetched value from (a) Aswath Damodaran's NYU industry
> datasets (as-of **2026-01-05**, 11-yr history to 2016-01-05) or (b) a **live yfinance pull on 2026-07-05**
> (prices move; treat as of that timestamp). Every trend/policy claim is web-cited with an as-of date and marked
> VERIFIED / UNVERIFIED. No multiple, price, date, or statistic is invented. This is RESEARCH, not advice.

---

## TL;DR (bottom line first)

1. **Broad healthcare is NOT cheap. One corner is: managed care / health-insurers.** Damodaran's healthcare
   sub-industries mostly sit in the *middle-to-expensive* part of their own 11-year ranges (US biotech EV/EBITDA
   & P/B at the **95th** percentile; pharma P/E at the **95th**). Med-devices and life-science tools are
   *expensive* on live multiples (fwd P/E 19-36). **The "healthcare is cheap" narrative is almost entirely the
   managed-care (HMO) group** — UnitedHealth, Elevance, Cigna, CVS, Humana — which repriced hard in 2024-2025.
   Live fwd P/E (2026-07-05): **CI 8.6, CVS 12.5, ELV 14.3, UNH 20.3, HUM 25.2** vs an S&P that is not cheap.
   In Damodaran, "Healthcare Support Services" (the bucket that contains HMOs) shows **P/B at the 5th percentile
   with 31% ROIC** — the single cheapest-on-book, high-return signal in all of healthcare.
2. **The managed-care cheapness is cyclical + company-specific + policy-overhang — not (yet) proven structural.**
   It is driven by a 2024-25 Medicare Advantage cost shock (UNH medical-cost ratio jumped to **89.4%** in Q2 2025,
   +430bps YoY), a UNH DOJ Medicare-billing probe (criminal + civil, 2025), a CEO change, and a guidance reset
   from ~$29.75 to "≥$16.00" adjusted EPS. That is a classic cyclical-cheap setup **if** MA pricing catches up to
   cost trend — but the DOJ probe and AI-denial litigation are real tail risks.
3. **The AI thesis is real where it cuts admin cost, mostly narrative where it discovers drugs.** Strongest,
   best-documented AI payoff is in **managed-care/health-IT admin** (UNH/Optum: ~$1.5B/yr AI spend, ~$1B cost-cut
   targets, 95% auto-adjudicated claims, prior-auth from days → seconds) and **ambient clinical documentation**
   (peer-reviewed burnout/time gains; 81% of physicians now use AI). AI in **med-device/diagnostics** accrues to
   incumbents (GE HealthCare, Siemens Healthineers, Philips lead FDA AI-clearance counts; ~1,524 AI devices
   cleared, 76% radiology). AI in **drug discovery is capital-rich but clinically unproven — zero AI-originated
   drugs are FDA-approved or generating product revenue as of mid-2026.** AI is also a *liability* for payers
   (three algorithm-denial class actions survived motions-to-dismiss in 2025).
4. **The aging tailwind is real and multi-decade** (US 65+ 17%→23% by 2050; US health spend 18%→~20% of GDP by
   2032, growing 5.6%/yr vs 4.3% GDP; Medicare fastest at 7.4%/yr). **The headwind is policy/pricing:** IRA drug
   negotiation (10 drugs priced for 2026, 15 more for 2027 incl. Ozempic at −71%, 15 more for 2028), a 100%
   Section-232 pharma tariff proclaimed (effective mid/late-2026, not yet in force), and MA rate/utilization
   pressure. Pharma faces the sharpest pricing headwind; managed care faces the utilization/regulatory one;
   **devices, tools, and health-IT are the cleanest AI+aging beneficiaries but are not cheap.**
5. **Single most attractive sub-sector for a quality-first value investor: managed care (health insurers)** —
   it is the only genuinely cheap, high-ROIC healthcare corner, and it is *also* the best-documented near-term AI
   cost beneficiary. **Lead candidate: UnitedHealth (UNH)** — most quantified AI story, dominant scale — but it
   carries the DOJ probe; **Elevance (ELV)** and **Cigna (CI)** are the cleaner-risk value alternatives. **Key
   headwind to watch: Medicare Advantage medical-cost trend + the UNH DOJ investigation.**

---

## 1. Damodaran sub-industry map & cheapness vs OWN 11-year history

Damodaran's taxonomy splits healthcare into **5** industries (no separate "Healthcare Information & Technology"
or "Life Sciences Tools" line — those fold into *Healthcare Products* / *Healthcare Support Services* /
*Diagnostics*; **managed care / HMOs fold into "Healthcare Support Services"**). All figures below are VERIFIED
fetched values from `data/damodaran/history/sector_cheapness_{US,Global,Emerging}.csv` (current as-of
**2026-01-05**; history 2016-01-05→2026-01-05). `hist%` = percentile of the *current* multiple within that
industry's own 11-year range (**low = cheap vs its own past**). ROIC/ROE as-of 2026-01-05.

### US (source: Damodaran pedata/vebitda/pbvdata, 2026-01-05)

| US sub-industry | EV/EBITDA (hist%) | P/B (hist%) | Curr P/E | Fwd P/E | ROIC | ROE | Own-hist composite (low=cheap) | Read |
|---|--|--|--:|--:|--:|--:|--:|---|
| Drugs (Biotechnology), n=496 | 15.8 (**95%**) | 8.22 (**95%**) | 109.3 | 63.8 | 3.5% | −5.7% | **83** (dear) | Expensive vs own history; avg dragged by ~500 loss-makers (net margin −5%) |
| Drugs (Pharmaceutical), n=228 | 15.2 (77%) | 6.64 (**95%**) | 335.3* | 24.2 | 16.9% | 24.0% | **89** (dear) | *Curr P/E distorted by loss-makers; **fwd 24×** is the real read. Not cheap on avg |
| Healthcare Products (devices), n=204 | 19.8 (50%) | 4.44 (41%) | 55.9 | 42.3 | 17.0% | 11.3% | **35** (mid) | Mid-range vs history; live leaders confirm *not* cheap |
| **Healthcare Support Services** (incl. HMOs), n=104 | 11.2 (50%) | **2.80 (5%)** | 94.4 | 55.3 | **31.2%** | 9.9% | **35** (mid) | **P/B at 5th pctile + 31% ROIC = the cheap-on-book, high-return signal** |
| Hospitals/Healthcare Facilities, n=31 | 8.9 (68%) | 5.62 (59%) | 24.4 | 15.7 | 22.2% | 50.8% | **56** (mid) | Lowest EV/EBITDA in HC but mid vs its own history; high ROE |

### Global & Emerging (source: Damodaran vebitda/pbv Global & emerg, 2026-01-05; no Global/EM P/E table)

| Sub-industry | Region | EV/EBITDA (hist%) | P/B (hist%) | ROIC | ROE | Composite | Read |
|---|---|--|--|--:|--:|--:|---|
| Drugs (Biotechnology) | Global | 16.7 (86%) | 6.17 (68%) | 3.0% | −3.2% | 77 (dear) | Dear |
| Drugs (Pharmaceutical) | Global | 13.8 (41%) | 4.17 (**95%**) | 14.7% | 16.8% | 68 (dear-ish) | P/B dear |
| Healthcare Products | Global | 18.5 (50%) | 3.53 (23%) | 13.7% | 9.1% | 36 (mid) | Mid |
| Healthcare Support Services | Global | 11.3 (68%) | **2.31 (5%)** | 20.7% | 8.5% | 36 (mid) | Same P/B-5th-pctile pattern as US |
| Hospitals/Healthcare Fac. | Global | 11.9 (32%) | 3.55 (59%) | 13.2% | 17.6% | 45 (mid) | Mid |
| Healthcare Support Services | Emerging | 11.1 (32%) | **1.13 (5%)** | 6.6% | 4.2% | **18 (cheapest HC in EM)** | Cheap but low-return (6.6% ROIC) |
| Healthcare Products | Emerging | 21.1 (41%) | 2.53 (14%) | 5.0% | 5.9% | 27 | Cheap-ish, low-return |

**Interpretation.** Across all three regions the *only* consistently cheap-vs-own-history healthcare line is
**Healthcare Support Services** on **price-to-book (5th percentile everywhere)** — the Damodaran bucket that
contains managed-care/HMOs. In the US it pairs that cheap book value with a **31% ROIC**, which is the
quality-first sweet spot. Everything else (biotech, pharma, devices) is mid-range to expensive vs its own past.

> **Method caveat (important, VERIFIED from the data itself):** Damodaran ratios are **simple industry
> averages**, not cap-weighted, and the biotech/pharma P/E averages are wrecked by hundreds of tiny loss-making
> firms (496 biotech names, industry net margin −5%; pharma "current P/E" 335× is meaningless — its *forward*
> P/E is 24×). So the Damodaran healthcare averages *understate* the quality and *distort* the valuation of the
> large-cap leaders. The live company pulls in §4 are the reliable read on the actual investable leaders.

---

## 2. Is healthcare cheap — and WHICH part? (ranked)

Ranking by cheapness-vs-own-history, cross-checked with live large-cap multiples (§4):

1. **Managed care / health insurers (Damodaran "Healthcare Support Services")** — **the cheap part.**
   P/B at the 5th percentile of its 11-yr range in all regions; US ROIC 31%. Live large-caps trade at fwd P/E
   **8.6-14.3** (CI, CVS, ELV) — genuinely cheap in an expensive market. **Cheap-cyclical + company-specific +
   policy-overhang**, not proven structural (see §3, §5). *This is the source of the "healthcare is cheap"
   narrative.*
2. **Big pharma** — **moderately cheap on live forward multiples, dear on Damodaran averages.** Live fwd P/E:
   **PFE 8.6, MRK 13.5, GILD 13.6, AMGN 15.9, NVS 16.2, NVO 15.6** — below-market, reflecting **patent-cliff +
   IRA + tariff** overhangs (cheap-for-a-reason risk). LLY (fwd 27.3) is a GLP-1 growth premium, not value.
3. **Hospitals/facilities** — lowest absolute EV/EBITDA (8.9× US) but only mid-range vs own history; HCA live
   fwd P/E 12.4. Cyclical (labor costs, payer mix), not a screaming vs-history discount.
4. **Med-devices & life-science tools — NOT cheap.** Live fwd P/E: ISRG 36, DHR 21.5, SYK 19.5, TMO 19.2, ABT
   15.7, MDT 13.0. Quality-compounder valuations, not value.
5. **Biotech (broad) — expensive** vs own history (95th pctile) and structurally loss-making on average.

**Verdict:** "Healthcare is cheap" is **true for managed care, partly true for big pharma, false for devices/
tools/biotech.** And the managed-care cheapness is **cyclical/sentiment/policy**, not confirmed structural decline.

---

## 3. Sub-sector scorecard — valuation, cyclical-vs-structural, AI impact

| Sub-sector | Cheap vs own hist? | Live valuation read (2026-07-05) | Cyclical vs structural | AI impact | Aging tailwind |
|---|---|---|---|---|---|
| **Managed care / HMOs** | **Yes** (P/B 5th pctile, ROIC 31%) | Cheap: fwd P/E 8.6-14 (CI/CVS/ELV), UNH 20 | **Cyclical + policy** (MA cost shock, DOJ probe) — not proven structural | **Beneficiary (admin) + Liability (denial litigation)** | Positive (MA enrollment) but rate-pressured |
| **Big pharma** | No (dear on avg); moderate on fwd | Moderately cheap: fwd P/E 9-16 (ex-LLY) | **Structural headwind** (patent cliffs, IRA, tariffs) + selective growth | **Beneficiary long-term (discovery) — narrative near-term** | Positive |
| **Biotech (broad)** | No (95th pctile) | Expensive; avg loss-making | Mixed / binary | Beneficiary long-term, unproven | Positive |
| **Med-devices** | No (mid) | Expensive (fwd 13-36) | Structural growth | **Beneficiary** (FDA AI clearances accrue to incumbents) | Strong positive |
| **Life-science tools/diagnostics** | No (mid) | Expensive (fwd 19-21) | Structural growth (post-COVID destock cyclical dip) | Beneficiary (AI-enabled R&D demand) | Positive |
| **Hospitals/facilities** | No (mid) | Cheap-ish (HCA fwd 12) | Cyclical (labor, payer mix) | Neutral/modest (documentation) | Strong positive (volumes) |

---

## 4. Candidate quality leaders per attractive sub-sector — LIVE valuations

All figures = **live yfinance pull, as-of 2026-07-05** (`data/cache/healthcare_leaders_summary.csv`). Prices move;
these are candidate names for a *later* deep-dive, not recommendations. "fwd P/E" = forwardPE; "EV/EBITDA" =
enterpriseToEbitda; ROE = returnOnEquity. Cross-check vs EDGAR before any thesis (EDGAR revenue shown where fresh).

### Managed care (the cheap, high-ROIC sub-sector — primary focus)
| Ticker | Name | Price | Mkt cap | Trail P/E | **Fwd P/E** | P/B | EV/EBITDA | ROE | Op margin | FCF yield |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **UNH** | UnitedHealth Group | $425.36 | $386B | 32.1 | **20.3** | 3.95 | 20.5 | 12.2% | 8.0% | 4.6% |
| **ELV** | Elevance Health | $417.89 | $91B | 17.7 | **14.3** | 2.07 | 10.0 | 12.1% | 5.3% | 4.7% |
| **CI** | The Cigna Group | $287.77 | $76B | 12.2 | **8.6** | 1.80 | 7.4 | 16.3% | 5.5% | 9.1% |
| **CVS** | CVS Health | $104.72 | $134B | 45.9 | **12.5** | 1.72 | 13.0 | 3.8% | 4.1% | 3.9% |
| **HUM** | Humana | $396.75 | $48B | 42.4 | **25.2** | 2.56 | 11.9 | 6.3% | 4.7% | 3.0% |

Read: CI (fwd 8.6, ROE 16.3%, FCF yield 9.1%) and ELV (fwd 14.3) are the cleanest cheap-and-profitable payers;
UNH is the scale leader and best AI story but carries the DOJ probe and depressed trailing earnings; HUM is a
pure-MA name with the highest medical-cost sensitivity (lowest margin 4.7%).

### Big pharma (moderately cheap, but pricing/patent-cliff overhang)
| Ticker | Name | Price | Mkt cap | Fwd P/E | P/B | EV/EBITDA | ROE | Op margin |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| **PFE** | Pfizer | $24.32 | $139B | **8.6** | 1.54 | 7.5 | 8.3% | 31.6% |
| **MRK** | Merck | $129.56 | $320B | 13.5 | 6.97 | 12.3 | 18.9% | 38.6% |
| **NVS** | Novartis | $159.90 | $305B | 16.2 | 7.92 | 15.1 | 34.9% | 30.5% |
| **AZN** | AstraZeneca | $195.15 | $303B | 22.4 | 6.39 | 16.4 | 23.5% | 27.9% |
| **ABBV** | AbbVie | $261.07 | $461B | 16.1 | neg (buybacks) | 17.5 | — | 32.2% |
| **LLY** | Eli Lilly | $1,213.91 | $1.08T | 27.3 | 34.8 | 30.9 | 107% | 35.0% | (GLP-1 premium, not value) |
| **NVO** | Novo Nordisk | $50.43 | $223B | 15.6 | 7.22 | 2.0* | 71.4% | 37.2% | (*EV/EBITDA screen looks anomalous; verify) |

### Med-device / diagnostics / tools leaders (quality, NOT cheap — for a growth-at-a-price watchlist)
| Ticker | Name | Fwd P/E | EV/EBITDA | ROE | Op margin | Note |
|---|---|--:|--:|--:|--:|---|
| **ISRG** | Intuitive Surgical | 36.1 | 37.7 | 17.2% | 30.9% | Robotic surgery; premium |
| **SYK** | Stryker | 19.5 | 19.9 | 15.2% | 17.8% | Ortho/med-surg |
| **BSX** | Boston Scientific | 12.1 | 14.0 | 14.7% | 20.6% | Cardio; relatively cheaper |
| **MDT** | Medtronic | 13.0 | 12.6 | 9.8% | 22.0% | Diversified devices; cheapest large device |
| **GEHC** | GE HealthCare | 12.2 | 10.9 | 19.5% | 11.1% | #1 in FDA AI-device clearances (130) |
| **SHL.DE** | Siemens Healthineers | 13.9 | 13.5 | 11.5% | 12.7% | #2 AI clearances (95); imaging |
| **DHR** | Danaher | 21.5 | 19.4 | 7.1% | 22.9% | Life-science tools; post-COVID reset |
| **TMO** | Thermo Fisher | 19.2 | 20.8 | 13.5% | 17.9% | Tools leader; premium |

### Hospitals
| Ticker | Name | Fwd P/E | EV/EBITDA | ROA | Op margin |
|---|---|--:|--:|--:|--:|
| **HCA** | HCA Healthcare | 12.4 | 9.2 | 12.3% | 15.0% | (P/B negative — heavy buybacks/leverage; verify balance sheet) |

---

## 5. The tailwind (AI + demographics) vs the headwind (pricing/policy) — evidence

### AI benefit — where it's REAL vs NARRATIVE (all VERIFIED unless noted)

**Managed care / health-IT admin = REAL and near-term (strongest evidence).**
- UNH/Optum: **~$1.5B/yr AI spend in 2026** (Optum Insight CEO, Q4 2025 call 2026-01-27); **"1,000+ active AI use
  cases"** (UNH IR); **95% of claims auto-adjudicated** (Q3 2025); pharmacy prior-auth cut **7.5 days → 29
  seconds**, medical prior-auth target **−30% by end-2026**; auto-coding **+73% productivity** (ambulatory).
  ~150bps operating-cost-ratio improvement in 2024, half AI-driven (CFO, 2025-01-16). Source:
  stockanalysis.com/stocks/unh/transcripts + unitedhealthgroup.com AI page.
- Humana: Google Cloud "Agent Assist" for ~80M calls/yr, **">$100M savings"** (Healthcare Dive 2026-02-03).
- Ambient clinical documentation: **81% of physicians use AI professionally in 2026** (AMA survey, 2026, n=1,692,
  ama-assn.org). Peer-reviewed ROI: Sutter/Abridge JAMA Network Open 2025-05-01 (time-in-notes 6.2→5.3 min,
  burnout 42%→35%); Providence/DAX (burnout −30%, doc-time −52%, 2025-07-24). *Caution:* one head-to-head RCT
  (medRxiv 2025-07-11) found DAX's raw time-savings **not statistically significant**. Abridge ~$100M ARR (2025),
  $5.3B valuation (Series E, via Sacra).
- Revenue-cycle AI: RadNet claim-error 8.3%→1.5%; OhioHealth denials −42%; Notable/CommonSpirit 74,878 staff-hrs
  saved 2024 (all vendor case studies — attribute as vendor-sourced). 80% of health systems piloting/using GenAI
  for docs & RCM (HFMA/AKASA 2025-12-17). But **only 45% of gen-AI adopters have quantified any ROI** (McKinsey
  2026-06-15) — proof lags deployment.

**Med-device / diagnostics = REAL beneficiary, accrues to incumbents.**
- **~1,524 FDA-authorized AI/ML medical devices cumulatively (Q1 2026); 76% are radiology** (The Imaging Wire,
  2026-06-18). Top vendors by AI clearances: **GE HealthCare 130, Siemens Healthineers 95, Philips 58** — the big
  imaging OEMs, not startups. Pure-play Aidoc: ~2,000 hospitals, 60M+ cases/yr, $150M raise 2026 (MedTech Dive
  2026-05-01). Reimbursement pathway (Health Tech Investment Act, H.R.6197/S.1399) still pending = the swing
  factor for revenue.

**Drug discovery (pharma/biotech) = mostly NARRATIVE near-term.**
- **Zero AI-originated drugs are FDA-approved or generating product revenue as of mid-2026** (VERIFIED headline,
  Tech Times 2026-06-30). Best human-efficacy signal is a *single Phase 2a* — Insilico's rentosertib (IPF), Nature
  Medicine 2025-06 (+98mL FVC vs −20mL placebo, n=71). Furthest-advanced AI-designed program: Generate
  Biomedicines GB-0895, just *entering* Phase 3 (2025-26). Capital is real and accelerating: Isomorphic Labs
  (Alphabet) **$2.1B Series B, 2026-05-12**, ~$3B Lilly+Novartis milestone deals but **no clinical trials started
  yet**; Nvidia–Lilly BioNeMo up to $1B (2026-01-12); Recursion FY2025 revenue $74.7M (all collaboration, no
  product) with a $645M net loss. **Verdict: long-dated option, not a near-term earnings driver.** Historical
  base rate is poor (Exscientia DSP-1181 killed in Ph1; BenevolentAI Ph2 failure/delisting).

**AI as a payer LIABILITY (the other side).**
- Three algorithm-denial class actions **survived motions-to-dismiss (in part) during 2025** and are in discovery,
  none dismissed/settled as of mid-2026: **UnitedHealth/naviHealth (nH Predict), Lokken** (D.Minn. 0:23-cv-03514,
  MTD granted-in-part 2025-02-13); **Humana/Barrows** (W.D.Ky. 3:23-cv-00654); **Cigna/PxDx, Kisting-Leung**
  (E.D.Cal. 2:23-cv-01477, MTD partial 2025-03-31). Source: Georgetown Law Health Care Litigation Tracker (updated
  2026-06-05). Regulatory tightening is concrete: **CMS-4201-F** (CY2024 rule) bars algorithm-only MA denials;
  **California SB 1120** (effective 2025-01-01) legally requires a licensed physician — not AI — to make
  medical-necessity calls.

### Aging demographics = REAL, multi-decade tailwind (all VERIFIED)
- US 65+: **58M / 17% (2022) → 82M / 23% (2050)**, +42% (PRB citing Census, 2024-01-09). Global 60+: **1.0B (2019)
  → 2.1B (2050)**; 80+ triples to 426M by 2050 (WHO fact sheet, 2025-10-01).
- US health spending: **$5.3T / 18.0% of GDP in 2024** (Peterson-KFF 2026-01-22), projected to grow **5.6%/yr
  2023-2032, outpacing GDP's 4.3%**, reaching **19.7% of GDP by 2032** (CMS NHE projections, 2024-06-12). **Medicare
  grows fastest at 7.4%/yr** — the most demographically direct beneficiary. This is share-of-wallet expansion, not
  just nominal growth. Most-exposed beneficiaries: hospitals, med-devices, managed care (MA enrollment).

### Pricing / policy HEADWIND (the reason big pharma & payers are cheap)
- **IRA Medicare drug-price negotiation** (VERIFIED, CMS fact sheets):
  - *Round 1 — 10 drugs, prices effective **Jan 1, 2026*** (announced 2024-08-15): Eliquis −56%, Jardiance −66%,
    Januvia −79%, Enbrel −67%, Stelara −66%, Farxiga −68%, Entresto −53%, Xarelto −62%, Imbruvica −38%, insulin
    aspart −76%. ~8.8M enrollees, ~$6B est. savings.
  - *Round 2 — 15 drugs, prices effective **Jan 1, 2027*** (list 2025-01-17, prices Nov 2025): **Ozempic/Wegovy
    (semaglutide) −71%** (Novo Nordisk), Trelegy −73%, Xtandi −48%, Ibrance −50%, Otezla −65%, etc. ~$12B est.
    savings (~44%). Directly hits Novo, Pfizer, AstraZeneca, AbbVie, Amgen, Merck, BMS, GSK.
  - *Round 3 — 15 drugs (incl. first Part B drugs), effective **Jan 1, 2028*** (list 2026-01-27; all 15 makers
    agreed 2026-03-13): Trulicity, Biktarvy, Cosentyx, Entyvio, Verzenio, Botox, Xolair, etc.
- **Section-232 pharma tariff — proclaimed but NOT yet in force** (VERIFIED, Federal Register 91 FR 18183,
  Proclamation 11020, signed 2026-04-02): **100% base ad valorem on patented drugs/APIs**; 20% for firms with
  approved onshoring plans; 15% for Japan/EU/Korea/Switzerland, 10% UK, **0% for firms under MFN pricing
  agreements**. Exempts generics/biosimilars/orphan/cell-gene/US-origin. Effective **Jul 31 / Sep 29, 2026**.
  (Trump's floated 25%/200% figures NOT FOUND in primary sources — only 100% is documented.)
- **Most-Favored-Nation drug pricing** (EO 14297, signed 2025-05-12, Fed. Reg. 2025-08876): benchmarks US prices to
  the lowest among developed nations; pursued mainly via *voluntary* "TrumpRx" company deals (Pfizer 50-85%
  discounts announced 2025-09-30). Binding rulemaking status UNVERIFIED.
- **Managed care specific:** UNH Q2 2025 medical-cost ratio **89.4% (+430bps YoY)** on Medicare Advantage cost
  acceleration (SEC 8-K 2025-07-29); FY2025 guidance cut from ~$29.75 → suspended (May 2025) → reset to "≥$16.00"
  adjusted EPS (Jul 2025); **DOJ criminal + civil Medicare-billing probe** disclosed (SEC 8-K 2025-07-24); CEO
  Witty out, Hemsley returned (2025-05-13). Peers' Q2 2025 loss ratios also jumped (Centene 93.0%, Elevance 88.9%).

---

## 6. Method & limitations

- **Cheapness (vs own history):** reused Stage-1a's 11-yr Damodaran percentile method
  (`sector_cheapness_{US,Global,Emerging}.csv`, as-of 2026-01-05). Damodaran ratios are **simple industry
  averages, not cap-weighted, ~6 months stale**, and the biotech/pharma P/E averages are badly distorted by
  hundreds of small loss-makers — so they read the *breadth* of a sub-sector, not the investable large-caps. That
  is exactly why the live yfinance pull (§4) is the load-bearing valuation for the leaders.
- **Live multiples:** yfinance pull on **2026-07-05** (`data/cache/healthcare_leaders_summary.csv`), cross-checked
  vs EDGAR where available. Prices move; treat as of that timestamp. A few screen fields look anomalous and are
  flagged (NVO EV/EBITDA 2.0, ABBV/HCA negative P/B from buybacks) — verify before any thesis.
- **No separate Damodaran "managed care" line** — HMOs sit inside "Healthcare Support Services," so the sub-sector
  read leans on the live payer group (UNH/ELV/CI/CVS/HUM), which is the correct proxy.
- **Web/policy claims:** researched via a fan-out web-research subagent (2026-07-04). Many news outlets (Reuters,
  STAT, Fierce, CNBC) were network-blocked, so load-bearing facts lean on **primary sources** (CMS.gov, Federal
  Register, SEC EDGAR 8-Ks, peer-reviewed journals, Georgetown litigation tracker) — stronger for citation. Items
  that rest on aggregators/single sources are marked UNVERIFIED inline.
- **Not done here:** company-level deep dives (thesis/valuation/catalysts) — this identifies candidates for that
  later stage. No cap-weighted live sector multiple was built.

**Reproduce:**
```
/opt/venv/bin/python3 screens/analyze_sector_cheapness.py                       # 11-yr percentiles (Stage-1a)
grep -iE "^US,\"?(Drugs|Healthcare|Hospitals)" data/damodaran/damodaran_combined.csv   # current sub-industry multiples
/opt/venv/bin/python3 data/fetch_fundamentals.py LLY NVO JNJ PFE MRK ABBV AZN NVS VRTX REGN GILD AMGN \
  ISRG MDT SYK BSX GEHC PHG SHL.DE ABT DHR TMO A UNH ELV CI HUM CVS HCA \
  --out data/cache/healthcare_leaders_summary.csv                              # live leader valuations
```
Data: `data/damodaran/history/sector_cheapness_*.csv`, `data/damodaran/damodaran_combined.csv`,
`data/cache/healthcare_leaders_summary.csv` + per-ticker `data/cache/yf_*.json`.
