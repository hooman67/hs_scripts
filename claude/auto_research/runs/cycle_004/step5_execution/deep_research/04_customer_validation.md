# Customer Validation Plan: Smart Warehouse QC Module (mmWave Through-Package)

## First 5 Target Customers

### Customer #1: ShipBob
- **Type**: Tech-forward 3PL, venture-backed
- **Revenue**: ~$200M+ (estimated, private)
- **Package volume**: 100,000+ packages/day across network
- **Why them first**:
  - Innovation-driven culture (VC-backed, technology as differentiator)
  - Public statements about reducing shipping errors for DTC brands
  - Likely has innovation budget and willingness to pilot unproven tech
  - Mid-size: big enough to have the problem, small enough to make decisions fast
- **Decision maker**: VP of Fulfillment Operations or CTO
- **Entry point**: LinkedIn outreach to engineering/ops leadership; attend ShipBob partner events
- **Risk**: May be too focused on software optimization, skeptical of hardware
- **Confidence in fit**: MEDIUM

### Customer #2: Radial (bpost subsidiary)
- **Type**: Established 3PL focused on e-commerce fulfillment
- **Revenue**: ~$500M (estimated, subsidiary of bpost)
- **Package volume**: 50,000+ packages/day
- **Why them**:
  - Dedicated to e-commerce fulfillment (not general freight)
  - European parent company (bpost) may have innovation mandate
  - 20+ fulfillment centers -- scale for expansion if pilot works
  - Contractually liable to their brands for shipping accuracy
- **Decision maker**: SVP of Operations or VP of Engineering
- **Entry point**: Industry conferences (CSCMP, Home Delivery World); bpost innovation team
- **Risk**: European parent may slow US decision-making
- **Confidence in fit**: MEDIUM

### Customer #3: GXO Logistics (Innovation Lab)
- **Type**: Largest pure-play contract logistics company
- **Revenue**: $9.4B (2024), NYSE-listed
- **Package volume**: Millions of packages/day across network
- **Why them**:
  - Has dedicated innovation/technology team that actively pilots new solutions
  - Public investor communications about warehouse automation investments
  - Scale means even small accuracy improvement = massive dollar impact
  - Would be landmark reference customer
- **Decision maker**: Chief Technology Officer or VP of Innovation
- **Entry point**: GXO has public innovation partnership programs; apply through their website. Also industry events.
- **Risk**: Large enterprise = long sales cycle (12-18 months); may want exclusivity
- **Confidence in fit**: LOW-MEDIUM (great fit on paper, hard to get first meeting)

### Customer #4: Deliverr (now part of Shopify Logistics, rebranding)
- **Type**: Tech-first fulfillment network
- **Revenue**: Acquired by Shopify for $2.1B (2022)
- **Package volume**: Serves thousands of Shopify merchants
- **Why them**:
  - Shopify has massive investment in fulfillment infrastructure
  - Technology-first DNA (was a startup before acquisition)
  - Shopify merchants suffer hugely from shipping errors (small brands can't absorb return costs)
  - Innovation budget likely supported by Shopify corporate
- **Decision maker**: Head of Fulfillment Operations (Shopify Logistics)
- **Entry point**: Shopify partner ecosystem; former Deliverr leadership on LinkedIn
- **Risk**: Post-acquisition organizational chaos; Shopify may be deprioritizing logistics (mixed signals in 2025-2026)
- **Confidence in fit**: LOW (organizational uncertainty)

### Customer #5: Whiplash (Port Logistics Group)
- **Type**: Mid-market 3PL focused on DTC brands
- **Revenue**: ~$100M (estimated, private)
- **Package volume**: 20,000-50,000 packages/day
- **Why them**:
  - Sweet spot: big enough to have the problem, small enough to decide fast
  - DTC brand focus means high-value items where shipping errors are costly
  - Known for operational excellence as competitive differentiator
  - Would benefit from "guaranteed accuracy" marketing to their brand clients
- **Decision maker**: VP of Operations or CEO (small enough for top-down decision)
- **Entry point**: Direct outreach; DTC brand community events; Whiplash is active on LinkedIn
- **Risk**: May not have capital budget for hardware pilots
- **Confidence in fit**: MEDIUM-HIGH (best fit for first pilot due to size and culture)

---

## Discovery Questions

### Problem Validation Questions (ask first, before discussing solution)

1. **"Walk me through what happens when a wrong item gets shipped to a customer. What's the full cost to you?"**
   - Looking for: Specific dollar amounts, process description, emotional pain
   - Red flag: "It's not a big problem for us" or inability to quantify cost

2. **"What's your current shipping error rate, and how do you measure it?"**
   - Looking for: Data-driven answer (0.5-3% is typical). If they don't know, that's also informative.
   - Red flag: "We don't track that" (means they won't value a solution)

3. **"What systems do you currently have in place to catch errors before packages leave your facility?"**
   - Looking for: Checkweighers, barcode verification, manual spot-checks -- and their limitations
   - Red flag: "We're happy with our current QC" (no perceived gap)

4. **"Of the errors that get through, what percentage are: wrong item, damaged item, missing item?"**
   - Looking for: Distribution helps us prioritize which detection mode matters most
   - Red flag: Heavily weighted toward "missing items" (checkweighers already solve this cheaply)

5. **"If you could wave a magic wand and verify every package's contents without opening it, what would that be worth to you per package? Per month?"**
   - Looking for: Willingness to assign dollar value. Target: $0.02-0.10 per package or $2K-10K/month
   - Red flag: "We'd never pay for that" or "less than a penny per package"

### Solution Fit Questions (after discussing concept)

6. **"If this system could catch 85% of wrong-item errors at 500 packages/hour, would that be useful enough to deploy?"**
   - Looking for: "Yes, absolutely" or "We need 95%+" (helps calibrate accuracy requirements)

7. **"What's your typical conveyor speed and package spacing? How much space do you have above the conveyor?"**
   - Looking for: Technical constraints for hardware design (ceiling height, conveyor dimensions)

8. **"What WMS do you use, and how open is it to third-party integrations?"**
   - Looking for: Manhattan Associates, Blue Yonder, Deposco, custom -- and API availability

9. **"Who would need to approve a $20-30K hardware purchase plus $3-5K/month SaaS? What's that process like?"**
   - Looking for: Understanding of budget authority and procurement process
   - Red flag: "That would need board approval" or "we'd need 18 months of ROI data first"

10. **"Would you be willing to run a 90-day paid pilot ($18K hardware + 3 months SaaS) if we could demonstrate the technology working in a lab environment first?"**
    - Looking for: Explicit "yes" or "yes, if..." with conditions we can meet
    - Red flag: "We only do free pilots" or "come back when you have 5 references"

---

## Demand Signals to Watch For

### Strong positive signals (GREEN):
- Customer can immediately quantify their shipping error costs (>$1M/year)
- They've already tried other solutions (checkweighers, vision) and found them insufficient
- They ask "when can we start?" or "can we be your first pilot?"
- They offer to introduce you to their peers/contacts
- They have a named budget line for QC infrastructure
- They mention specific pain with "wrong item, right weight" errors (checkweigher blind spot)

### Moderate positive signals (YELLOW):
- They acknowledge the problem but haven't quantified costs
- They say "interesting" and ask for a follow-up meeting
- They ask about accuracy requirements (means they're evaluating)
- They mention upcoming capex budget cycle (timing issue, not interest issue)

### Negative signals (RED):
- "Our error rate is already below 0.5%" (low pain)
- "We handle this with manual QC staff" and seem satisfied
- "We'd need to see 3-5 other deployments first" (fast follower, not early adopter)
- "Our customers don't complain much about wrong items" (low perceived cost)
- "We're focused on [automation/speed/other priority] right now" (timing)
- No one in the organization owns "shipping accuracy" as a metric

---

## Outreach Plan

### Phase 1: Network Mining (Weeks 1-2)

**Actions**:
1. Search LinkedIn for connections who work in 3PL/fulfillment operations
2. Post on LinkedIn about "exploring non-destructive package QC" to attract inbound (don't reveal solution yet)
3. Join relevant communities:
   - Warehouse & Fulfillment LinkedIn groups
   - r/logistics, r/supplychain on Reddit
   - WERC (Warehousing Education and Research Council) membership
   - MHI (Material Handling Industry) membership
4. Identify 30 potential contacts across 15 companies

**Target output**: 10 warm introductions requested

### Phase 2: Cold Outreach (Weeks 2-4)

**Email template** (for cold outreach to VP Ops / Director of QC):
```
Subject: Quick question about shipping error costs at [Company]

Hi [Name],

I'm researching a new approach to package QC that can verify contents 
of sealed packages without opening them -- no radiation, no slowing 
the line.

Before building anything, I'm trying to understand: how big a problem 
are wrong-item/damaged-item shipments for your operation? Would you 
have 20 minutes for a quick call to help me understand the landscape?

Not selling anything -- genuinely in research mode and would value 
your operational perspective.

[Name]
```

**Volume**: 50 personalized emails across 25 companies
**Expected response rate**: 5-10% (3-5 conversations)

### Phase 3: Warm Outreach + Conferences (Weeks 3-8)

**Conferences to attend**:
- **Home Delivery World** (next occurrence) -- focused on e-commerce logistics
- **MODEX** (Atlanta, biennial) -- material handling and logistics tech
- **CSCMP EDGE** -- supply chain professionals

**Actions at conferences**:
- Attend sessions on warehouse automation and QC
- Network in exhibition hall (talk to 3PL ops teams visiting booths)
- Do NOT exhibit (too early, too expensive)
- Collect 20+ business cards from operations leaders

**Advisor recruitment**:
- Identify 3-5 former VP Ops from 3PLs who are between roles or consulting
- Offer: 0.5-1% advisory equity for introductions + monthly call
- Target: Someone who can make warm intros to decision makers

### Phase 4: Demo & LOI (Weeks 8-16)

**Prerequisites**: Phase 0 feasibility test passed (can show working demo on bench)

**Actions**:
1. Create 3-minute video demo showing radar scanning a sealed box and correctly identifying contents
2. Share with interested contacts from Phases 1-3
3. Schedule in-person demo at interested companies (bring portable bench setup)
4. Present ROI model customized to their error rate and volume
5. Ask for LOI or paid pilot commitment

**LOI template elements**:
- 90-day pilot period
- Hardware provided at cost ($18K) or subsidized ($10K for first 2 pilots)
- Customer provides: conveyor access, WMS API access, 3 SKU categories for training
- Success criteria: >80% detection rate of intentional test errors
- If success criteria met: commitment to purchase 3-5 additional units at full price

### Metrics & Timeline

| Week | Target | Metric |
|------|--------|--------|
| 2 | Network mining complete | 30 contacts identified |
| 4 | Cold outreach sent | 50 emails, 3-5 conversations |
| 6 | Problem validated | 5+ companies confirm pain point |
| 8 | Conference attended | 20+ new contacts |
| 10 | Advisor secured | 1 logistics advisor on board |
| 12 | Demo ready | Bench-top demo working |
| 16 | LOI secured | 2+ pilot commitments |

---

## Alternative Customer Segments (if 3PL doesn't work)

### Backup #1: High-value electronics fulfillment
- Companies: Newegg, B&H Photo, micro-fulfillment for consumer electronics
- Why: High item value ($200-2000) means shipping errors are extremely costly
- Risk: Lower volume per facility, may not justify hardware cost

### Backup #2: Pharmaceutical distribution
- Companies: McKesson, AmerisourceBergen, Cardinal Health
- Why: Regulatory requirements for accuracy, high error costs (wrong medication = liability)
- Risk: Heavy regulation, different competitive landscape (already strict QC), long sales cycles

### Backup #3: Subscription box companies
- Companies: FabFitFun, Birchbox, Dollar Shave Club, HelloFresh
- Why: Highly standardized packages, limited SKU set (easier ML problem), brand damage from errors
- Risk: Lower revenue per customer, price-sensitive, seasonal volume swings

### Backup #4: Returns processing centers
- Companies: Optoro, B-Stock, goTRG, Happy Returns
- Why: Need to verify what's actually in returned packages (fraud detection)
- Risk: Different problem (identifying unknown items vs. verifying expected contents)

---

## Customer Validation Budget

| Activity | Cost | Timeline |
|----------|------|----------|
| LinkedIn Sales Navigator (6 months) | $600 | Ongoing |
| Conference attendance (2 events) | $3,000 | Months 2-3 |
| Travel for customer visits (5 trips) | $5,000 | Months 2-4 |
| Demo hardware (portable setup) | $2,000 | Month 2 |
| Advisor equity (0.5%) | $0 cash | Month 2 |
| Marketing materials (one-pager, video) | $1,000 | Month 2 |
| **Total validation budget** | **$11,600** | |
