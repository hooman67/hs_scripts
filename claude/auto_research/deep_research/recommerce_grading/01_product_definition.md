# Product Definition: AI Recommerce Grading Station

## Problem Statement

Product returns are a $800B+ annual crisis for retail. When a customer returns a pair of Nike shoes or a Lululemon jacket, that item enters a chaotic, labor-intensive triage process that determines whether it gets resold at full price, discounted, sent to outlet, donated, or landfilled. Today this grading is done by humans -- temporary workers earning $15-18/hr who visually inspect items for 8-10 hours/day, making subjective quality decisions with wildly inconsistent results.

**The pain is quantifiable:**

1. **Speed**: A human grader processes 30-50 items/hour for clothing, 20-30 for electronics. At $16/hr loaded, that's $0.35-$0.80 per item in labor alone. Returns centers process 10,000-50,000 items/day.
2. **Consistency**: Inter-rater reliability for cosmetic grading is 60-70% (academic studies on used-product assessment). Two graders looking at the same shoe will disagree on condition 30-40% of the time. This directly impacts pricing -- a "Grade A" item priced at $80 that should have been "Grade B" at $55 causes customer complaints and returns-of-returns.
3. **Throughput bottleneck**: Returns centers are space-constrained. Items piling up waiting for grading tie up capital (average item sits 7-14 days before disposition decision). At scale, a 1-day reduction in processing time = millions in freed working capital.
4. **Seasonality**: Returns spike 300-400% post-holiday (January). Hiring and training temp workers for 6-8 weeks of peak volume is expensive and produces the worst quality grading.

**Who suffers most:**
- Brand return centers (Nike, Lululemon, Patagonia) processing their own returns for resale programs
- Recommerce platforms (ThredUp, Poshmark wholesale, The RealReal) grading thousands of items daily
- 3PL returns processors (Optoro's warehouse partners, Happy Returns) handling multi-brand returns

**Confidence: HIGH** -- returns volume data is publicly reported by NRF (National Retail Federation), grading inconsistency is well-documented in recommerce industry publications, and multiple public companies (ThredUp S-1, The RealReal 10-K) disclose processing costs and throughput metrics.

---

## Product Scope: Version 1 (MVP)

### Core System: AI Grading Station

**Hardware (The "Photo Booth")**
- Enclosed light-controlled chamber (~3ft x 3ft x 4ft)
- 3x USB3 industrial cameras (top, front, 45-degree angle) -- 12MP minimum
- LED ring lights (CRI 95+) for consistent, diffused illumination
- Motorized turntable (360-degree rotation in 10 seconds)
- Barcode/RFID reader for item identification
- Physical footprint: ~4ft x 4ft x 6ft (fits on a standard workbench)

**Software (Edge + Cloud)**
- Edge inference PC running defect detection models (real-time, <3 second total grading cycle)
- Multi-angle image capture + stitching for full-surface inspection
- Defect classification: stains, tears, pilling, scuffs, missing components, odor indicators (discoloration patterns)
- Grade assignment: A/B/C/D/Reject with confidence score
- Integration with customer's WMS (warehouse management system) for automatic routing
- Cloud dashboard for grade distribution analytics, model performance monitoring, grading criteria customization

### V1 Category Support
- **Footwear** (highest value, most consistent form factor, easiest to photograph)
- **Apparel - flat items** (t-shirts, pants -- laid flat on turntable platform)
- **Small electronics** (phones, headphones, tablets -- rigid form factor)

### Explicitly Out of Scope for V1
- Apparel on hangers (requires different capture geometry)
- Large items (furniture, appliances)
- Functional testing (does the phone turn on?) -- separate system
- Authentication/counterfeit detection (different problem, different models)
- Automated repair/refurbishment recommendations

---

## User Workflow

### Setup (Day 1: ~4 hours)
1. Station delivered pre-assembled and pre-calibrated
2. Connect to power + Ethernet/WiFi
3. Install customer-specific grading rubric (brand provides their existing criteria document, we encode it into model constraints)
4. Run calibration: photograph 20 pre-graded reference items across each grade level
5. Connect to WMS via API (REST) or CSV export fallback

### Daily Operation (Operator Workflow)
1. Operator scans item barcode (identifies SKU, retrieves product reference images)
2. Places item on turntable, closes booth door (or presses "capture" button)
3. Station captures 12-18 images (3 cameras x 4-6 rotation positions) in 8-10 seconds
4. AI processes images, displays grade on screen: "Grade B - Minor scuffing on left toe, otherwise excellent. Confidence: 94%"
5. Operator confirms or overrides (overrides feed back into model)
6. Item routed to appropriate bin/conveyor based on grade
7. **Total cycle time: 15-20 seconds per item** (vs. 60-120 seconds manual)

### Throughput
- **Target: 180-240 items/hour per station** (vs. 30-50 manual)
- **5-8x throughput improvement** with 1 operator tending 2-3 stations

### Monthly Review
- Grade distribution analytics (are we seeing more damage? seasonal trends?)
- Model accuracy report (agreement rate with spot-check audits)
- Override analysis (where does the AI disagree with humans most? recalibrate)

---

## Pricing Model

| Component | Price | Notes |
|-----------|-------|-------|
| Hardware Station | $10,000 one-time | $3,500 BOM + margins. Includes installation & calibration. |
| SaaS Platform | $750/month per station | Includes: cloud analytics, model updates, 10K gradings/month included |
| Overage | $0.04/grading beyond 10K | Incentivizes high utilization |
| Professional Services | $5,000 (optional) | Custom grading rubric encoding, WMS integration, on-site training |
| Support & Maintenance | Included in SaaS | Hardware warranty 2 years, software updates continuous |

### Unit Economics for Customer
- 1 station processing 200 items/hr x 8 hrs x 22 days = **35,200 items/month**
- Replaces: 4-5 manual graders ($16/hr x 8hr x 22 days x 4.5 = **$12,672/month**)
- Cost of station: $750/month SaaS + $1,000 overage (25K extra items) + $455/month amortized hardware (24mo) = **$2,205/month**
- **Net savings: $10,467/month per station (82% cost reduction)**
- Payback period on hardware: **<2 months**

### Revenue Model Year 1 (Assumptions)
- 15 stations sold @ $10K = $150K hardware revenue
- 15 stations @ $750/month x average 7 months active = $78,750 SaaS revenue
- Professional services: 10 engagements @ $5K = $50K
- Overage charges: ~$15K
- **Conservative Year 1: ~$294K** (ramp scenario)
- **Aggressive Year 1: $875K** (faster sales cycle, 40+ stations)

---

## Ideal First Customer Profile

### The Perfect Pilot: Brand Return Center (Nike, Adidas, or Lululemon)

**Why:**
1. They process their OWN returns (controlled environment, brand standards already documented)
2. High volume: Nike processes 100K+ returned items/week across their network
3. Footwear is the ideal first category (rigid, consistent shape, high value per item)
4. They already have "recommerce" programs (Nike Refurbished, Lululemon Like New) -- this is not a new concept, just a faster execution
5. Budget exists: these programs are already investing millions in returns processing infrastructure
6. Brand reputation risk from inconsistent grading gives urgency

**Second-best options:**
- ThredUp (publicly traded, 100K+ items/day, but lower ASP per item -- economics slightly weaker)
- The RealReal (luxury focus, smaller volume but very high value per item -- Grade A vs B can be $200 difference)
- Patagonia Worn Wear (brand-owned resale, smaller scale but progressive early adopter culture)

**Disqualified for V1:**
- Small resellers (too low volume to justify station cost)
- Electronics recyclers (functional testing needed, not just cosmetic -- out of scope)
- General 3PLs (too many categories, need specialization first)
