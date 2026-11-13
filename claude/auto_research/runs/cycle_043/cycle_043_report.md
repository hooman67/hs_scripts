# Cycle 043 Report — ROUND 3 (Wider Net)

**Date:** 2026-07-01
**Domain assigned:** Digital health software that is NOT FDA-gated — clinical documentation,
prior authorization, medical billing/RCM, scheduling, care coordination, patient intake.
Workflow SaaS, not devices.
**Founder:** Hooman (AI/ML + software + cloud infra; EE bachelor's; mech-eng friends; wants a
secondary income-stream SaaS he can largely build solo; already building CutLog).
**Outcome:** **ZERO graduates.** Every viable idea in this domain fails the mandatory
Incumbent/OEM Check and Moat Gate. This is an honest, quantified NO-GO for the whole domain
for a solo software founder.

---

## Method note

WebSearch is unavailable in this environment and Google/DuckDuckGo/Bing HTML endpoints return
CAPTCHA or error pages to WebFetch. Research was therefore done by fetching **primary sources
directly**: company sites (Abridge, Commure, Tebra, Adonis, PointClickCare, Counterforce),
CMS.gov (the CMS-0057-F final rule), and Wikipedia for market/regulatory framing. Funding
figures are as stated on company sites / their own marketing, marked confidence inline.
This is a limitation but the incumbent signal was so strong and consistent that the verdict is
robust: the companies' *own marketing copy is the pitch* for every candidate idea.

---

## Step 1 — Ten technologies / ideas scanned

The "enabling breakthrough" for essentially all of these is the same: LLMs good enough to do
medical-language extraction, coding, and letter-drafting at production accuracy (TRL 8-9,
shipping now). That itself is a warning — the breakthrough is horizontal and commoditized, so
everyone has it at once.

| # | Idea | Sub-vertical | TRL | Time-to-product | Step-1 decision |
|---|------|--------------|-----|-----------------|-----------------|
| 1 | Ambient AI clinical scribe (specialty-tuned) | Clinical documentation | 9 | shipping | REJECT (see Step 2) |
| 2 | AI prior-authorization submission/lookup for practices | Prior auth | 8 | <12mo | REJECT |
| 3 | Payer-side / provider-side FHIR prior-auth API tooling (CMS-0057-F) | Prior auth infra | 6-7 | 12-18mo | REJECT |
| 4 | AI denials-prediction & auto-appeal (provider RCM) | RCM/billing | 8 | shipping | REJECT |
| 5 | Consumer/patient AI insurance-appeal advocate | Patient appeals | 8 | shipping | REJECT |
| 6 | All-in-one billing/scheduling/intake for independent practices | RCM + scheduling + intake | 9 | shipping | REJECT |
| 7 | AI front-desk / scheduling voice agent for clinics | Scheduling | 8 | shipping | REJECT |
| 8 | SNF / long-term-care MDS documentation + PDPM optimizer | Documentation (post-acute) | 8 | shipping | REJECT |
| 9 | Dental practice RCM / claims automation | RCM (dental) | 8 | shipping | REJECT (adjacent-mover risk) |
| 10 | Care-coordination / referral-management workflow AI | Care coordination | 8 | shipping | REJECT |

No idea was PROMOTED past Step 2. Detail below.

---

## Step 2 — Competitive density + MANDATORY Incumbent/OEM Check + Moat Gate

### The domain-level finding (applies to all 10)

Digital-health workflow SaaS is the **opposite** of the "invisible European niche" pattern that
rounds 1-2 hunted. It is one of the most heavily VC-funded software categories in the world, and
the buyer (health system, practice) is already consolidated onto an **EHR/platform** (Epic,
Oracle Health, athenahealth, PointClickCare, Tebra) that treats each of these workflows as a
native feature or an acquired module. Two structural killers:

1. **Funded horizontal platforms already do ALL six sub-verticals as one product.**
   - **Commure** — AI-native ops platform spanning ambient documentation, end-to-end RCM/billing,
     prior auth, scheduling voice agents, and care coordination; integrates 60+ EHRs; **130+
     health systems, 2,000 sites, $25B+ claims/yr, ~$70M raised at a ~$7B valuation** (Commure
     site, marketing copy — ASSUMED accurate). This single company is the pitch for ideas
     #1, #2, #4, #7, #10 simultaneously.
   - **Abridge** — ambient documentation + revenue-cycle automation + nursing docs; **300+ health
     systems** incl. Kaiser, Mayo, Johns Hopkins, Duke; "Best in KLAS 2025 & 2026" market leader;
     100M+ conversations/yr (Abridge site). Owns idea #1.
   - **Tebra** — EHR + billing + scheduling + digital intake + AI Note Assist, **built for
     independent practices, 150,000 providers** (Tebra site). Owns idea #6 (and #7 intake/
     scheduling) for the exact small-practice buyer a solo founder could reach.

2. **The EHR/platform is the OEM, and it ships the AI itself.**
   - **PointClickCare** (SNF/senior-care EHR) ships **PDPM Coach + AI "Chart Advisor, Billing
     Advisor, Referral Advisor"** natively (PointClickCare site). Owns idea #8 and #10 for post-acute.
   - Epic/athenahealth ship ambient documentation and prior-auth/eligibility natively or via
     first-party partnerships. Any point-solution races the system-of-record that owns the data.

### Per-idea incumbent hits (all boxes checked → density 4-5)

- **#1 Ambient scribe:** Abridge (300+ systems, Best-in-KLAS), plus Nuance/Microsoft DAX Copilot,
  Nabla, Suki, Ambience, Commure. Density **5**.
- **#2 Prior-auth for practices / #3 FHIR PA tooling:** CMS-0057-F mandates the FHIR PA APIs on
  **PAYERS** (deadlines Jan 2026 provisions, Jan 2027 APIs — CMS.gov). The provider-side "PA
  requirements lookup" is a native EHR feature; Commure and Availity/Epic already do it. The
  mandate creates a payer buildout, not a solo-SaaS opening. Density **4-5**.
- **#4 Denials/appeals RCM:** Adonis (**$40M Series C**, 67% denial reduction claims), Thoughtful AI,
  Waystar, R1 RCM, Commure. Density **5**.
- **#5 Consumer appeals:** Counterforce Health (**free to individuals, NIH/UPenn grant-funded,
  10,000+ appeals, "will never accept money from insurers"**), Fight Health Insurance, Claimable.
  A grant-funded free incumbent structurally caps monetization. Density **4**, monetization dead.
- **#6 Independent-practice all-in-one:** Tebra (150K providers), athenahealth, Kareo/legacy,
  DrChrono. Density **5**.
- **#7 Scheduling voice agent:** Commure Orchestrator, plus a crowded AI-voice-agent field.
  Density **4-5**.
- **#8 SNF MDS/PDPM:** PointClickCare (OEM EHR ships PDPM Coach + AI advisors), MatrixCare. Density **5**.
- **#9 Dental RCM:** Dental-specific PMS incumbents (Dentrix/Henry Schein One, Open Dental) plus
  RCM automation vendors expanding down-market. Density **4**.
- **#10 Care coordination/referrals:** Commure, PointClickCare Referral Advisor, plus Epic Care
  Everywhere. Density **4-5**.

### Moat Gate — the decisive failure

For every idea, the honest answer to *"if this works, what stops the OEM / a funded competitor /
a weekend cloner in 6 months?"* is **nothing**:

- The enabling tech is a horizontal LLM everyone has (no technical moat for a software founder).
- The proprietary data that would create a flywheel (the clinical note, the claim, the payer
  response) lives inside the **EHR/payer**, not inside a third-party app — the exact inverse of
  CutLog, where the community-contributed cut parameters accrue to the app. Here the data moat
  accrues to the incumbent.
- No network effect: one practice's denials data doesn't make another practice's product better
  in a way the EHR can't replicate with more data.
- Regulatory lock-in (CMS-0057-F, HIPAA) accrues to whoever holds the payer/EHR integration —
  again the incumbent, and it *raises* the barrier for a new solo entrant (BAAs, HITRUST, SOC 2,
  payer contracts, EHR app-store gatekeeping).

This is precisely the round-2 kill pattern (Big-Picture Learning §2): **"the incumbent's own
marketing copy IS the idea's pitch,"** and **"cheap + trivial + no flywheel = absorbable
feature, not a company."** Commure/Abridge/Tebra advertise verbatim the value props any Step-1
idea here would claim.

---

## Step 3 — Market sizing (not reached; noted for completeness)

The domain passes size/growth easily — that is *not* the problem. US healthcare RCM was ~$344B
in 2024 (Wikipedia/industry), the software segment grows well above 15% CAGR, prior-auth alone
costs the system **$23-31B/yr** and ~13 hrs/wk of nursing-staff time (Wikipedia, AMA-cited).
**Per Learning #5, market size is the least-discriminating dimension** — a huge growing market is
exactly what attracts the wall of funded incumbents that kills founder-fit here. No idea reached
Step 3 promotion because none survived Step 2.

---

## Step 4 — Feasibility (not reached)

Not evaluated; nothing passed Step 2. Note that even feasibility would carry heavy
domain-specific execution risk for a solo founder: HIPAA + BAAs, SOC 2 / HITRUST, EHR app-store
gatekeeping, payer/clearinghouse integrations, and 6-18 month enterprise sales cycles — the
opposite of CutLog's reachable Facebook-group owner-operator buyer.

---

## Graduates

**None.** Zero ideas pass all gates. This is a valid and (per round-3 directive) preferred
outcome versus promoting an undefensible idea.

---

## Domain verdict

**NOT a promising vein for a solo AI/software founder.** Digital-health workflow SaaS is the
inverse of CutLog's winning setup: the buyer is consolidated onto an EHR/payer that owns the
data and the distribution, the enabling AI is a commodity horizontal model, and the space is
saturated with deeply funded platforms (Commure ~$7B, Abridge 300+ systems, Tebra 150K providers,
Adonis $40M) that each already ship the entire funnel of candidate ideas. The one genuinely
"different" angle — consumer insurance-appeal advocacy — is occupied by a grant-funded free
incumbent (Counterforce) that structurally forecloses for-profit monetization. Recommend
deprioritizing this domain entirely for future cycles.

---

## Citations

- Abridge — company site (abridge.com): 300+ health systems, Best-in-KLAS 2025/26, RCM + nursing docs.
- Commure — company site (commure.com): 130+ systems, 2,000 sites, $25B+ claims, ~$70M @ ~$7B val, 60+ EHRs, Orchestrator scheduling/PA.
- Tebra — company site (tebra.com): 150,000 providers, EHR + billing + scheduling + intake + AI Note Assist, independent-practice focus.
- Adonis — company site (adonis.io): $40M Series C, AI RCM agents, denials, named provider customers.
- Counterforce Health — company site (counterforcehealth.org): free to individuals, NIH/UPenn grant-funded, 10,000+ appeals, ~70-75% success.
- PointClickCare — company site (pointclickcare.com): SNF/senior-care EHR + RCM + PDPM Coach + AI Chart/Billing/Referral Advisor, 400+ integrations.
- CMS-0057-F — cms.gov: Interoperability & Prior Authorization Final Rule; FHIR Provider Access & Payer-to-Payer APIs; Jan 2026 provisions / Jan 2027 API deadlines; applies to payers.
- Prior authorization burden — Wikipedia: $23-31B/yr system cost; ~13.1 hrs/wk nursing staff.
- RCM market — Wikipedia: ~$344B (2024).
