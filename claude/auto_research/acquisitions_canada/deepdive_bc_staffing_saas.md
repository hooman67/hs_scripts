# Deep-Dive: BC Staffing-Management Vertical SaaS (BizQuest BW2447571)

**Full acquisition deep-research — #1 pick from the Canada search.**
**Compiled:** 2026-07-04 by Claude (Opus 4.8). **Owner:** Hooman Shariati.
**Buyer profile:** Canadian citizen (BDC/bank leverage available now), US-resident on TN (green
card imminent), Adobe AI/ML + data-engineering + cloud/infra engineer, ~$500K CAD cash, willing
full-time, strong diligence. Can own+operate a Canadian company remotely from the US on TN today.

**Confidence tags:** VERIFIED = pulled from the live listing or a cited source; ASSUMED = my
inference from the listing + comps; UNVERIFIED = must be confirmed in diligence.

---

## 0. The listing — confirmed live, exact numbers

**VERIFIED — live on BizQuest at fetch time (2026-07-04).**
Source: https://www.bizquest.com/business-for-sale/highly-scalable-staffing-mgmt-saas-34k-mrr/BW2447571/
**Listing ID: 2447571.**

| Field | Value (as listed) |
|---|---|
| Asking price | **US$1,000,000** (~$1.35M CAD @ 1.35) |
| TTM gross revenue | **US$456,991** (~$620K CAD) |
| TTM cash flow (SDE) | **US$248,695** (~$338K CAD) |
| Stated net margin | **55%** |
| MRR | **US$38,000** ("$34K MRR" in the headline slug — mild inconsistency, note it) |
| Years in operation | **16** |
| Location | British Columbia, Canada — home-based, relocatable |
| Team | **3 full-time + 2 part-time contractors** (listing says contractors, not employees) |
| Customers | **100+ B2B** |
| Churn | **<2%** |
| Recurring revenue | **90%+** |
| Growth | **32% YoY (2024 vs 2023); 10% YoY (TTM vs 2024)** |
| Seller financing | **Available** |
| Seller motivation | "Pursue other interests" |
| Transition | Offered |
| Implied multiple | **~4.0x SDE / ~2.19x revenue** |

**Important correction to the search report:** the search summary said "5 contractors"; the live
listing specifies **3 FT + 2 PT** — i.e. roughly **~4 FTE-equivalent of labor already inside the
55% margin.** And the growth story has already decelerated hard: **32% → 10% YoY.** Both matter
below.

---

## 1. Product — what it actually does

**VERIFIED (listing) + ASSUMED (feature depth):** A cloud platform to "streamline the operations
of staffing and talent agencies" — managing **staff, clients, scheduling, reporting, and payroll**,
"with automation at its core." This is **not** a pure ATS/CRM (candidate-sourcing tool). It is an
**operations/back-office suite for agencies that place temp/contract workers**: shift scheduling,
timesheets, client billing, and payroll/pay-processing for placed workers.

That distinction is the whole investment thesis. The crowded, well-funded part of this market is
**front-office ATS/CRM** (find and place candidates). The **back-office** (schedule → timesheet →
bill client → pay worker → remit) is stickier, more painful to rip out, and less contested by the
AI-sourcing wave. **VERIFIED-adjacent:** competitor analysis (Section 3) shows the hot money is in
sourcing/CRM, not payroll/scheduling ops — which is where this product sits.

**UNVERIFIED and load-bearing:** whether "payroll" means it actually **runs payroll / calculates
remittances** (a heavy compliance surface, and a strong moat) or just **exports hours to a payroll
provider** (thin). Confirm exactly which. If it truly touches Canadian/US payroll remittance and
tax tables, that is both a deeper moat AND a maintenance/compliance liability Hooman inherits.

---

## 2. ICP & why they stay (the moat)

**Implied ICP (ASSUMED from price point):** MRR US$38K / 100+ customers ≈ **~US$380/customer/month
average** (~US$4.5K/yr). That's a **small-to-mid temp/staffing agency** — too small to afford or
justify Bullhorn/Avionté enterprise implementations, too operationally complex for a spreadsheet.
This is exactly the validated winning archetype in this founder's own playbook: *software for an
underserved mid-market that can't afford the enterprise incumbent.*

**Why they stay (the moat), ranked by strength:**
1. **Switching cost / operational entanglement (STRONGEST).** Scheduling + timesheets + billing +
   payroll is the operational spine of an agency. Migrating it mid-operation risks missed payroll
   and mis-billed clients — the two things an agency literally cannot get wrong. This is the real
   source of the **<2% churn**, and it is credible for a back-office ops suite (far more credible
   than <2% churn would be for a front-office CRM).
2. **16-year data + workflow lock-in.** Years of client/worker/timesheet history in-system.
3. **Vertical specialization.** Purpose-built for staffing-agency workflows vs. generic HR/payroll.
4. **Price.** At ~US$380/mo it undercuts enterprise tools by 10x on total cost.

**VERIFIED market signal supporting the moat:** the sub-2% churn and 90%+ recurring on a 16-yr base
is internally *consistent with* a back-office system-of-record, not a nice-to-have. This is the
single strongest fact in the deal — **but it is also the fact most in need of source-verification**
(Section 8), because a broker's "<2%" is worthless until you see the cohort/logo data.

---

## 3. Competitive verdict

**VERIFIED market structure (Global Info Research via search):** Top 3 players — **Zoho Recruit,
Bullhorn, Avionté — hold ~50% of the global staffing-software market.** Cloud is ~75% of the
market; North America + Europe ≈ 70% of activity.

**Segmentation (VERIFIED via comparison sources):**
- **Bullhorn** — medium-to-large agencies, comprehensive CRM, enterprise price/implementation.
- **Avionté / TempWorks** — temp/contract staffing specialists (Avionté & TempWorks are the true
  back-office/temp competitors — closest to this product's lane), mid-to-large.
- **JobDiva** — smaller firms, analytics-heavy.
- **Zoho Recruit / RecruiterFlow / Crelate** — budget / small-agency **front-office ATS/CRM**.
  RecruiterFlow is **US$75–119/user/month (VERIFIED, recruiterflow.com/pricing)** — a *per-seat
  CRM*, not a per-agency ops+payroll suite. Different product, different buyer pain.

**The verdict — does a small 16-yr vertical player defend 100 clients at <2% churn, or is it being
slowly displaced?**

- **Defends, in its lane — for now.** The direct enterprise threats (Avionté, TempWorks) are
  **moving upmarket**, not down into ~US$4.5K/yr micro-agencies; the front-office crowd
  (RecruiterFlow, Crelate, Zoho) sells a **different product** (sourcing CRM, not scheduling/
  payroll ops). The <2% churn is credible precisely because *nobody is aggressively competing for
  this exact micro-agency back-office buyer at this price.* **This is a defensible niche, not a
  contested one.**
- **But displacement risk is real on a 5–10 yr horizon (ASSUMED).** A 16-yr codebase competing
  against modern, AI-native, well-funded suites will feel dated. The moat is switching cost and
  price, **not** technology superiority. If a modern competitor (or Bullhorn's SMB tier, or an
  AI-native entrant) builds a genuinely easy migration path, the switching-cost moat erodes.
  **The moat buys time; it does not last forever without reinvestment.** This is where Hooman's
  edge (modernize the stack, add AI, keep it cheap) is the actual value-creation lever.

**Net:** No incumbent is currently eating these 100 clients. The threat is **generational/technology
decay**, not head-to-head displacement. That is a *fixable* problem for a technical owner — which is
the whole reason this is his #1 fit.

---

## 4. Market & AI-disruption outlook

**Market size / growth (VERIFIED, wide ranges):** Staffing-agency software market estimated
**$0.59B–$5B (2025)** depending on scope, growing at **~7%–18% CAGR** (a commonly cited midpoint is
~12%). Cloud is ~75% and rising. So the *software* category is growing.

**BUT — the demand base is the staffing-agency industry itself, and that's the risk.** VERIFIED
(search, incl. LA Times Feb 2026 headline + industry sources): AI is a **"double whammy"** on
staffing agencies — companies are (a) automating recruiting in-house (disintermediating agencies)
and (b) automating agencies' own back-office. **If staffing agencies consolidate/shrink, the
customer base for agency software shrinks with them.**

**Reconciling the two:** the software category grows even as the number of agencies may fall,
because surviving agencies spend more per agency on automation. For THIS business that means:
- **Tailwind:** more automation spend per surviving agency; back-office ops (this product's lane)
  is *less* AI-disruptable than front-office sourcing.
- **Headwind:** if its ICP (small agencies) is exactly the cohort most likely to be squeezed out by
  AI-enabled in-housing, the 100-customer base could attrit for **reasons unrelated to product
  quality** — churn from customers *going out of business*, which no product feature fixes.

**AI-disruption exposure verdict (ASSUMED):** **MODERATE, and asymmetric in Hooman's favor.** The
product itself (scheduling/timesheet/payroll ops) is a defensible, less-disruptable layer, and a
technical owner can bolt AI *on top* (auto-scheduling, forecasting, anomaly detection on
timesheets/billing) to move UP the value chain. The real AI risk is **macro** — the health of the
small-staffing-agency segment — not the product. Diligence must probe **customer survivorship**,
not just churn.

---

## 5. Economics — skeptical validation

### Is 55% margin + <2% churn + 32% growth internally consistent?
- **55% net margin on ~4 contractors:** **PLAUSIBLE (ASSUMED).** SDE US$249K on revenue US$457K =
  54.4% — checks arithmetically. For a mature, contractor-run SaaS with cheap infra, a 50–60% SDE
  margin is normal. **BUT "SDE" ≠ "net margin."** SDE adds back the owner's comp/benefits and
  discretionary items. The listing conflates "55% net margin" with "SDE margin." **Load-bearing
  question:** the ~4 contractors — are they inside COGS (already deducted in SDE) or is any of that
  labor added back? If the owner *also* does material work (sales, dev) that a buyer must replace
  with a hire, **true owner-independent earnings are BELOW US$249K.** Section 6 quantifies this.
- **Gross vs net:** **UNVERIFIED and important.** Cloud SaaS gross margin should be 80%+. If gross
  is much lower, there's hidden delivery/services labor (a red flag for "SaaS" purity). Get the P&L.
- **<2% churn + only 10% TTM growth:** internally consistent — <2% churn means most growth must come
  from **new logos + expansion**, and new-logo growth **decelerated from 32% to 10%.** That deceleration
  is the tell that growth is **owner-sales-driven and slowing** (Section 6), not product-led.
- **32% → 10% growth:** **This is the most important number in the deal and the search report buried
  it.** A 3x growth deceleration in one year on a low-churn base means the growth engine (owner
  outbound/conference selling) is sputtering or the owner is already pulling back ahead of a sale.

### FX exposure (VERIFIED structural)
- Priced and (almost certainly) **earning in USD**, while Hooman's cash, BDC loan, and life are
  **CAD-denominated.** He buys a USD income stream with CAD-serviced debt. **USD strength = windfall;
  USD weakness = margin compression on his CAD debt service.** ~$1.35M CAD ticket on US$1M swings
  ~±$135K CAD per 10% FX move. Manageable but must be modeled, and the debt should ideally be
  sized against a **conservative FX assumption.**

### Multiple fairness (VERIFIED comps)
- Private SaaS median ~**4.7x revenue** (Aventis); "boring" low-churn SaaS is *bid up* in 2025.
- This deal is **~2.2x revenue / ~4.0x SDE.** Against revenue comps that looks **cheap**; against
  **small/micro-SaaS SDE comps (typically 3–4.5x SDE)** it is **fair-to-slightly-full but not rich.**
- **The multiple is not the risk. The transferability of the SDE is the risk.** A 4x SDE that
  requires a $120K rainmaker to sustain is really ~6–7x on *owner-independent* earnings.

**Economics verdict:** Numbers are **internally plausible and not obviously cooked**, the price is
**fair-to-attractive on paper**, but the headline SDE is **almost certainly overstated as
owner-independent earnings**, and the **growth deceleration + owner-sales dependence** is the crack
in the thesis.

---

## 6. Owner-dependence risk — the #1 flagged risk, quantified

**The flagged risk:** growth is **owner-led outbound / conference SALES.**

**Why it's the deal's center of gravity:**
- **<2% churn means the base is safe without the owner.** Existing revenue (~US$457K) is sticky and
  contractor-supported — that part transfers. **Good.**
- **Growth is NOT safe without the owner.** If new logos come from the owner personally cold-calling
  and working conferences, then post-close a non-selling buyer (Hooman has **no sales track record**)
  sees growth collapse toward **0–2% (churn-replacement only)**, not 10–32%.
- **The 32%→10% deceleration is consistent with the owner already easing off the sales pedal** ahead
  of a sale — meaning the "10% TTM" may itself be inflated relative to a truly hands-off run-rate.

**Quantifying the dependence (framework for diligence, ASSUMED weights):**
- Ask: what % of new-logo bookings in the last 24 months came from (a) owner outbound/conferences,
  (b) inbound/referral/SEO, (c) partner channels? **If (a) > ~50%, growth is owner-equity, not
  business-equity, and you are overpaying for it.**
- **Cost to replace the seller's selling:** a B2B SaaS AE/rainmaker in this vertical ≈ **US$70–120K
  base + commission (US$120–180K OTE)**, ASSUMED. That is **~50–70% of stated SDE.** Layer that on
  and **owner-independent SDE falls from ~US$249K toward ~US$130–180K**, which re-rates the deal to
  **~5.5–7.7x true SDE** — still investable, but a very different picture than "4x."

**Mitigations Hooman can actually execute:**
1. **Longer earn-out / seller transition** tied to bookings, so the seller keeps selling through the
   handoff and part of the price is contingent on growth actually transferring. (Seller financing is
   offered — structure the note as **partly performance-contingent.**)
2. **Convert owner-outbound to product-led / inbound** — Hooman's genuine edge is engineering, not
   selling, so the smart play is to **reduce dependence on human selling** (self-serve trial, SEO,
   integrations, AI-assisted onboarding), not to become a salesperson.
3. **Hire one vertical AE** and underwrite the deal *as if* that cost is permanent (i.e., buy on
   owner-independent SDE, ~US$150K, not US$249K).

**Verdict on this risk:** **REAL and the single most likely way this deal disappoints.** It is not a
deal-killer *if* (a) the base churn is genuinely <2% and verified, and (b) the price/structure is set
against owner-independent earnings with the growth de-risked via earn-out. **Do not pay 4x on US$249K;
pay ~4x on owner-independent SDE, or push the delta into a contingent seller note.**

---

## 7. Financing math — realistic structure & post-debt take-home

**VERIFIED financing benchmarks (Canadian sources):**
- **Bank acquisition loans:** buyer equity **20–30% down**; **5–7 yr amortization**; floating
  (prime + spread). Banks lend ~**2.5–4x TTM EBITDA**. (kitswest.com)
- **BDC:** more flexible than banks on cash-flow/goodwill deals; can go higher LTV in some cases;
  pairs term loan + seller note; patient/flexible terms, interest-only ramp options. (bdc.ca,
  kitswest.com)
- **Vendor/seller notes:** **3–5 yr term, 4–8% interest**, typically a modest slice of price.
- **CSBFP:** post-2022 covers **intangibles + working capital up to $500K CAD** (max $1.15M total) —
  relevant because SaaS deals are goodwill-heavy. (ised-isde.canada.ca)

**A realistic structure for US$1M / ~$1.35M CAD** (illustrative, ASSUMED terms — confirm live):

| Component | Amount (CAD) | Terms |
|---|---|---|
| Hooman equity (down) | **~$400K** (~30%) | his cash — leaves ~$100K reserve of the $500K |
| BDC/bank term loan | **~$675K** (~50%) | 6-yr amort, ~prime+2–3% ≈ **~9–10%** all-in (2026 rates) |
| Seller note | **~$275K** (~20%) | 4-yr, ~6%, **partly performance-contingent (earn-out)** |
| **Total** | **~$1.35M** | |

**Annual debt service (ASSUMED):**
- BDC ~$675K @ ~9.5%, 6-yr amort ≈ **~$148K/yr** (P&I).
- Seller note ~$275K @ 6%, 4-yr ≈ **~$78K/yr** (P&I).
- **Total debt service ≈ ~$226K CAD/yr.**

**Post-debt take-home:**
- SDE ~$338K CAD − debt service ~$226K = **~$112K CAD/yr pre-tax free cash** *on stated SDE.*
- **On owner-independent SDE** (after a ~$180K CAD rainmaker/AE hire): $338K − $180K = ~$158K SDE −
  $226K debt service = **NEGATIVE ~$68K/yr** in the early years.

**This is the crux of the financing reality:** at 30% down + full leverage, **the deal only
comfortably services its debt if Hooman himself does the selling+ops (no rainmaker hire) and FX
holds.** If he must hire a seller AND service the debt, early-year cash flow goes underwater. So the
financeability of this deal is **inseparable from the owner-dependence question in Section 6.**

**Levers to make it work:**
- **More equity down (less leverage):** $500K down → ~$120K less debt → ~$18K/yr less service, and a
  smaller seller note. Uses his full cash but de-risks cash flow.
- **Interest-only BDC ramp (year 1–2)** to bridge the transition while he replaces the owner's sales.
- **Bigger, longer, contingent seller note** — pushes risk back onto the seller and reduces the bank
  slug.
- **Buy at a lower price** justified by owner-independent SDE — the honest number is closer to
  **~$1.0–1.1M CAD (US$0.75–0.8M)**, not US$1M, once you price out the sales dependence.

**Financing verdict:** **Financeable via BDC + seller note (this is exactly the Canadian-citizen
edge), but tightly.** The stated SDE services the debt; the *owner-independent* SDE does not without
either more equity down, a lower price, or Hooman personally running sales for 1–2 years.

---

## 8. Diligence checklist (deal-specific, prioritized)

**Tier 1 — deal-killers if they fail:**
1. **Source-verify revenue & MRR** — merchant-processor/Stripe/bank statements + accountant-prepared
   P&L for 3 yrs. Reconcile the **$38K vs "$34K" MRR discrepancy** in the listing. Confirm revenue is
   USD and the currency of costs.
2. **Source-verify churn & the <2%** — pull **logo-level cohort data**: monthly active accounts 36
   months back, logos gained/lost, MRR churn vs logo churn. **Reject the deal if <2% is a broker
   assertion without cohort export.**
3. **Customer concentration** — revenue by customer. **If top-5 or top-10 customers are >30–40% of
   revenue, the "100+ customers / diversified" story is false** and one lost logo craters SDE.
4. **Sales attribution (the owner-dependence test)** — for every new logo in 24 months, *how was it
   sourced?* Owner-outbound vs inbound/referral. This one dataset decides the valuation.
5. **SDE bridge** — reconcile SDE to net income line by line: which add-backs, is the owner's labor
   (dev? sales? support?) added back, are all 5 contractors inside COGS. Compute **owner-independent
   SDE** — the real number to value on.

**Tier 2 — pricing/structure impact:**
6. **Code / IP audit** — Hooman's core edge. Language/framework, age, test coverage, single points of
   failure, infra cost, security posture, dependency rot. Confirm **clean IP ownership** (contractors
   assigned IP? any open-source license contamination?). Quantify the modernization cost/timeline.
7. **"Payroll" scope** — does it *run* payroll/remittances (compliance liability + deeper moat) or
   *export* hours? Determines both moat depth and inherited liability.
8. **Contract terms** — are the 100 customers on month-to-month or annual? What are the actual
   contracts (auto-renew, price-lock, cancellation)? <2% churn is only bankable if contracts support
   it. Any customer able to walk on 30 days weakens the moat.
9. **Contractor dependence / key-man** — are the 3 FT contractors the only people who understand the
   16-yr codebase? Will they stay? A lost lead dev on undocumented legacy code is a hidden key-man risk
   as dangerous as the owner's sales.
10. **FX & tax** — model debt service under conservative CAD/USD; GST/HST registration; cross-border
    (US-resident operating a BC corp) tax structuring — confirm with a cross-border accountant.

**Tier 3 — market/macro:**
11. **Customer survivorship** — are ICP agencies healthy, or is churn coming from customers going *out
    of business* (the AI-disintermediation risk)? Ask for churn *reasons.*
12. **Growth pipeline** — current qualified pipeline; is the 10% run-rate real forward, or a trailing
    artifact of the owner easing off?

---

## 9. VERDICT

### **CONDITIONAL GO.**

This is correctly the #1 pick: it is the **most remote-operable, highest founder-fit, and most
financeable** durable asset in the Canadian search, and the **moat (back-office switching cost) is
real and in an uncontested niche** — not being actively displaced by the AI-sourcing wave or by
enterprise incumbents moving upmarket. Hooman's engineering edge is a genuine value-creation lever
(modernize the 16-yr stack, add AI, keep it cheap, reduce human-sales dependence). The price
(~4x SDE / ~2.2x revenue) is **fair-to-attractive on paper** and financeable via the BDC + seller-note
structure his Canadian citizenship unlocks.

**But it is CONDITIONAL, not an unqualified GO, because two facts can turn it from a good deal into a
value trap — and both are currently UNVERIFIED broker assertions:**

**Deal-killers to confirm (any one failing = PASS or major re-price):**
1. **The <2% churn must be provable from logo-level cohort data** — not a broker claim. This single
   fact is the entire moat.
2. **Growth must not be >~50% owner-personal-selling** — if it is, you are buying the seller's Rolodex,
   not a business; re-price to owner-independent SDE (~US$150K) and push growth into a contingent
   earn-out.
3. **No hidden customer concentration** (top-10 < ~35% of revenue).
4. **SDE must survive the owner-independence bridge** — the honest valuation base is
   ~US$130–180K owner-independent SDE, not US$249K. **Do not finance the full US$1M at 30% down on the
   headline SDE**; the debt service goes underwater the moment he must hire a salesperson.

**Recommended action:** Sign the NDA, get the CIM + 3-yr accountant P&L + cohort/logo export + sales
attribution. If Tier-1 diligence clears, **offer ~US$0.75–0.85M** (justified by owner-independent SDE)
structured as **~$400–500K CAD down + BDC term loan + a 20% seller note that is partly
performance-contingent**, with an **interest-only BDC ramp in year 1** and a **6–12 month seller sales
transition**. If churn or sales-attribution diligence disappoints, **PASS** — the whole thesis rests
on the base being sticky and the growth being transferable.

---

## Sources
- **Listing (VERIFIED):** BizQuest BW2447571 — https://www.bizquest.com/business-for-sale/highly-scalable-staffing-mgmt-saas-34k-mrr/BW2447571/
- **Market size/share (VERIFIED):** Global Info Research; Data Insights Market; Verified Market Reports; GII Research (via search 2026-07-04).
- **Competitor segmentation/pricing (VERIFIED):** spotsaas.com, selecthub.com, recruiterflow.com/pricing ($75–119/user/mo), crelate.com/pricing, slashdot software comparisons.
- **AI-disruption (VERIFIED):** LA Times (2026-02-18) "AI threatens staffing industry"; incruiter.com; talentmsh.com; aqore.com 2026 trends.
- **SaaS valuation comps (VERIFIED):** aventis-advisors.com (private SaaS ~4.7x rev median); feinternational.com; vestara.co.
- **Canadian financing (VERIFIED):** kitswest.com (20–30% down, 5–7yr amort, 2.5–4x EBITDA, VTB 4–8%); bdc.ca; ised-isde.canada.ca (CSBFP intangibles to $500K).
- **FX / cross-border / owner-independent-SDE math:** ASSUMED, this analysis — confirm with BDC account manager + cross-border accountant.
