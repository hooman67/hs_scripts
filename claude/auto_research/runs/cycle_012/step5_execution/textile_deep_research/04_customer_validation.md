# Customer Validation Plan: AI Textile Defect Detection for Small Mills

## First 5 Target Customers

### Customer 1: Woven Grey Fabric Mill, Surat (India)

**Profile:**
- 80-150 power looms (rapier or air-jet)
- Produces grey cotton/polyester fabric for garment exporters
- 150-300 employees; $3M-$8M annual revenue
- Currently: 2-3 human inspectors checking 30-50 rolls/day
- Pain: 3-5% defect pass-through rate; buyers deducting 5-10% from invoice for quality claims

**Why them first:**
- Surat has 600,000+ power looms in a concentrated cluster [VERIFIED - India's largest weaving hub]
- Progressive mill owners invest in automation (many have computerized Jacquard looms)
- Direct export pressure from European buyers demanding inspection certificates
- Relatively simple fabric (plain weave grey goods) -- easier for AI model v1
- High volume: 50-100 rolls/day per mill = clear ROI demonstration

**Expected objections:**
- "Will it work on my specific fabric?" -- need live demo on their fabric
- "I cannot stop my inspection table for installation" -- install during planned shutdown
- "What if it breaks? Who will service it?" -- need local support commitment
- "My inspectors will feel threatened" -- position as tool that helps inspectors, not replaces

**Decision-maker:** Mill owner (typically sole proprietor or family-owned)
**Budget authority:** Can approve $8K without external approval
**Sales cycle:** 2-4 weeks (decision-makers are accessible, not corporate bureaucracy)

---

### Customer 2: Knit Fabric Manufacturer, Tiruppur (India)

**Profile:**
- 20-50 circular knitting machines
- Produces single jersey, interlock, rib fabrics for t-shirt/activewear
- 100-250 employees; $2M-$5M annual revenue
- Currently: Visual inspection on open-width frame after dyeing
- Pain: Knitting defects (needle lines, holes, drop stitches) often found only after dyeing -- expensive rework

**Why them:**
- Tiruppur is India's knitwear capital: $6B+ in exports annually [VERIFIED]
- Knit defects are well-defined and repetitive (good for AI)
- Multiple export brands (H&M, Decathlon, Walmart) pushing quality requirements
- Mill owners are organized (TIRUPPUR EXPORTERS ASSOCIATION -- 3,000+ members)
- Higher margin products = more willingness to invest in quality

**Expected objections:**
- "Smartex already does this for knitting" -- Smartex is not present in India; also $3-5x our price
- "Defects are visible to the eye, why do I need a machine?" -- show data on miss rate of human inspectors
- "My dye house is humid and hot" -- need IP54 rated enclosure

**Decision-maker:** Owner or quality head
**Budget authority:** $8K-$15K within owner authority
**Sales cycle:** 3-6 weeks

---

### Customer 3: Denim Mill, Sanliurfa or Denizli (Turkey)

**Profile:**
- Mid-size denim weaver (50-100 shuttle-less looms)
- Produces denim fabric for European fast-fashion brands
- 200-400 employees; $5M-$15M annual revenue
- Currently: Manual inspection + periodic third-party audits
- Pain: Denim defects (broken selvedge, missing picks, oil stains) cause rejected shipments to EU buyers

**Why them:**
- Turkey is world's 5th largest textile exporter [VERIFIED]
- Turkish mills are more tech-forward than Indian/Bangladeshi counterparts
- Higher willingness-to-pay (can afford $8K-$12K)
- Proximity to European buyers who demand quality certificates
- Denim is a high-value fabric (more defect cost per meter)
- English proficiency is higher among Turkish mill managers

**Expected objections:**
- "We already comply with buyer audits" -- show that automated inspection BETWEEN audits prevents surprises
- "What about indigo color variation?" -- this is color, not defect; clarify scope
- "We need integration with our existing MES" -- plan for API integration in v2

**Decision-maker:** Quality director or plant manager
**Budget authority:** May need owner approval for $10K+; quality director can champion
**Sales cycle:** 4-8 weeks

---

### Customer 4: Export-Oriented Woven Fabric Processor, Dhaka (Bangladesh)

**Profile:**
- Fabric inspection + packing house (receives fabric from multiple weaving units)
- Inspects 200-500 rolls/day for export buyers
- 50-150 employees; $1M-$3M revenue (service business)
- Currently: 10-20 human inspectors working in shifts; high turnover
- Pain: Labor cost rising 15-20%/year in Bangladesh; inspector fatigue causes afternoon quality drops

**Why them:**
- Bangladesh is world's 2nd largest garment exporter [VERIFIED]
- Inspection houses are a distinct business segment -- they BUY inspection as their core service
- Clear ROI: reduce inspector count from 20 to 10 with same throughput
- High volume = fast payback
- One installation proves value across dozens of fabric suppliers

**Expected objections:**
- "We inspect many different fabrics" -- this IS the hardest test case; if it works here, it works everywhere
- "Power supply is unreliable" -- need UPS integration
- "My inspectors are already cheap ($100/month)" -- but rising, and quality is inconsistent

**Decision-maker:** Business owner
**Budget authority:** $8K is significant but justified by labor savings
**Sales cycle:** 2-4 weeks (service businesses are ROI-driven)

---

### Customer 5: Technical Textile Manufacturer, Bursa (Turkey) or Ahmedabad (India)

**Profile:**
- Produces technical fabrics (filter cloth, geotextile, medical textile)
- 30-80 specialized looms
- 100-200 employees; $5M-$15M revenue
- Currently: 100% manual inspection with ZERO tolerance for defects in finished goods
- Pain: Technical textiles have very tight specifications; one defect can cause product failure in the field

**Why them:**
- Higher willingness to pay ($10K-$15K) because defect cost is extreme
- Smaller variety of fabric types (easier to train AI)
- Often ISO 9001 / ISO 13485 certified -- need documented quality records
- Smaller volume but higher value per meter
- Less price-sensitive than commodity fabric producers

**Expected objections:**
- "Our specs are too tight for generic AI" -- offer custom model training for their specific defect types
- "We need full traceability" -- offer roll-level serial tracking with timestamp
- "This needs to integrate with our quality management system" -- API-first design

**Decision-maker:** Quality manager + plant director
**Budget authority:** $15K within quality department budget
**Sales cycle:** 6-10 weeks (more bureaucratic)

---

## Discovery Questions (for initial conversations)

### Understanding Current Pain (ask before pitching)

1. "How many rolls per day does your inspection team check? How many inspectors per shift?"
2. "What percentage of fabric gets rejected by your buyers after shipment? What does that cost you annually?"
3. "What are your top 3 most common defect types? Which ones do your inspectors miss most often?"
4. "How do you currently train new inspectors? How long before they are effective?"
5. "Have you ever lost an order or a buyer relationship due to quality issues?"
6. "What does your buyer require in terms of inspection documentation?"

### Understanding Budget & Decision Process

7. "If a system could catch 90%+ of defects automatically, what would that be worth to your business per year?"
8. "Have you ever looked at automated inspection systems? What stopped you from purchasing?"
9. "What is your typical equipment purchase process? Who approves purchases of $5K-$10K?"
10. "Would you prefer to pay once for hardware + monthly for software, or a single monthly fee covering everything?"

### Understanding Technical Environment

11. "What types of fabric do you inspect? How many different styles per month?"
12. "What speed does your fabric move during inspection? (meters per minute)"
13. "What width range do your fabrics cover?"
14. "How is your inspection area lit? Natural light, fluorescent, or other?"
15. "Do you have reliable internet connection in the factory? WiFi?"
16. "What power supply do you have? Any issues with outages or voltage fluctuation?"

### Qualifying Interest

17. "If we could install a trial unit for 2 weeks at no cost, would you be interested?"
18. "Would you be willing to share examples of defective fabric for us to train our AI on?"
19. "Who else in your cluster/association might benefit from this?"
20. "If this worked as described, would you buy it today at $6,000-$8,000?"

---

## Demand Signals (evidence the market wants this)

### Strong Signals (observed or verifiable)

| Signal | Source | Confidence |
|--------|--------|------------|
| "fabric inspection machine" search volume growing 30%+ YoY in India | Google Trends | ASSUMED (needs verification) |
| IndiaMart has 50+ listings for manual inspection machines ($2K-$10K) | IndiaMart search | HIGH |
| ITMA 2023 (Barcelona) had 5+ new vision inspection exhibitors | Trade show reports | ASSUMED |
| EU REACH/OEKO-TEX compliance driving documentation requirements | Regulatory trend | HIGH |
| Bangladesh minimum wage rose 56% in 2023 (from $95 to $113/month) | News reports | VERIFIED |
| India PLI scheme for textiles (2021) incentivizing tech adoption | Government policy | VERIFIED |
| H&M, Zara, Walmart pushing supplier quality compliance programs | Buyer requirements | HIGH |

### Weak/Ambiguous Signals

| Signal | Source | Confidence |
|--------|--------|------------|
| Smartex raised $24.7M (validates market) | Crunchbase | VERIFIED |
| Chinese low-cost systems appearing on Alibaba | Alibaba listings | VERIFIED |
| Multiple textile engineering colleges adding AI/ML courses | Academic trend | ASSUMED |
| Textile industry publications increasing AI coverage | Trade press | ASSUMED |

### Counter-Signals (reasons to be cautious)

| Signal | Implication | Confidence |
|--------|-------------|------------|
| Small mills historically resist technology investment | May prefer $0 (human inspectors) over $8K system | HIGH |
| Payment collection in India/Bangladesh is notoriously difficult | May need upfront payment or hardware lease model | HIGH |
| COVID depressed textile investment 2020-2022; recovery uneven | Capital budgets may still be tight | MEDIUM |
| Fabric inspection is seen as "cost center" not "profit center" | Hard to get owner attention unless buyer demands it | HIGH |

---

## Outreach Plan (First 90 Days)

### Week 1-2: Research & Warm Introductions

**Actions:**
- Join LinkedIn groups: "Indian Textile Industry," "Bangladesh Garment Manufacturers," "Turkish Textile Forum"
- Post 3-5 educational content pieces: "How AI is changing fabric inspection" (build awareness)
- Reach out to 10 textile engineering professors (IIT Delhi, BTRA Mumbai, NIFT) for mill introductions
- Contact Textile Association of India (TAI), SIMA, PDEXCIL for member directories
- Identify 50 target mills from IndiaMart/TradeIndia/LinkedIn (those listing "export" + "quality")

**Target**: 10 warm introductions to mill owners/quality managers

### Week 3-4: Discovery Calls

**Actions:**
- Conduct 15-20 discovery calls/video calls using question framework above
- Record and analyze responses: pain level, budget, decision process, technical environment
- Identify top 5 "most ready" prospects (clear pain + budget + willingness to pilot)
- Send follow-up with simple ROI calculator customized to their numbers

**Target**: 5 mills expressing strong interest in pilot; 2-3 offering factory access

### Week 5-6: In-Person Visits (India)

**Actions:**
- Travel to Surat + Tiruppur (or Erode) for 7-10 days
- Visit 8-10 mills in person (observe inspection process, photograph setup)
- Conduct live demos with laptop + webcam showing basic defect detection concept
- Sign 2-3 LOIs (Letter of Intent) for pilot installation
- Collect fabric samples (5-10 meters of various types with known defects)

**Target**: 2 signed LOIs; fabric samples for model training; deep domain understanding

### Week 7-8: Prototype Build

**Actions:**
- Build first working prototype using components ordered in parallel
- Train initial model on collected fabric samples + public datasets
- Create 2-minute demo video showing system detecting defects in real-time
- Share video with all 20+ discovery contacts for feedback

**Target**: Working prototype; demo video generating additional inbound interest

### Week 9-12: Pilot Installation

**Actions:**
- Install at first partner mill (Surat or Tiruppur)
- Run side-by-side with human inspector for 2 weeks
- Measure and document: detection rate, false positive rate, speed, uptime
- Collect testimonial and case study data
- Use data to refine pitch for next 10 prospects

**Target**: One mill running system in production; quantified performance data; referenceable customer

---

## Validation Gates (Go / No-Go Checkpoints)

### Gate 1: After Discovery Calls (Week 4)
**GO if**: 5+ mills say "I would pay $5K-$8K for this" AND can articulate specific annual cost of defects
**NO-GO if**: Fewer than 3 mills express willingness to pay; or max WTP is below $3K

### Gate 2: After In-Person Visits (Week 6)
**GO if**: 2+ mills sign LOI for free pilot; provide factory access and fabric samples
**NO-GO if**: No mill willing to install even a free pilot (indicates deep technology resistance)

### Gate 3: After Pilot (Week 12)
**GO if**: System detects >85% of defects with <10% false positives; mill owner says "I would buy this"
**NO-GO if**: Detection rate below 75%; or mill owner says system is "not practical" for daily use

### Gate 4: After First Paid Sales (Month 6)
**GO if**: 3+ mills pay full price ($6K-$8K) after seeing pilot results; <30 day sales cycle
**NO-GO if**: Cannot close a single paid sale despite successful pilot; or payment collection fails

---

## Customer Acquisition Cost (CAC) Estimate

| Channel | Cost per Lead | Conversion Rate | CAC |
|---------|--------------|-----------------|-----|
| Textile trade shows (ITMA, India ITME) | $200-$500 | 5-10% | $2,000-$10,000 |
| LinkedIn + content marketing | $50-$100 | 2-5% | $1,000-$5,000 |
| Textile association referrals | $0-$50 | 10-20% | $250-$500 |
| Word of mouth (after first installs) | $0 | 20-40% | $0 |
| Channel partners (loom dealers) | 15-20% commission | 10-15% | $900-$1,600 |
| IndiaMart/TradeIndia listings | $100/month | 3-5% | $2,000-$3,300 |

**Target blended CAC**: <$2,000 (on $8K hardware + $4,800/year SaaS = $12,800 first-year revenue)
**Target LTV:CAC ratio**: >6:1 (if customer stays 3+ years)
