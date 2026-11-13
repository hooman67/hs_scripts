# Customer Validation Plan: AI Weld Quality Monitoring from Electrical Signatures

## First 5 Target Customers

### Customer 1: Regional Structural Steel Fabricator

**Archetype:** Mid-size structural steel fabricator doing commercial buildings, bridges, and industrial structures.

| Attribute | Target Profile |
|-----------|---------------|
| Size | 20-50 welding stations, 30-80 employees |
| Revenue | $5M-$25M annual |
| Certifications | AWS D1.1 (Structural Welding Code - Steel), AISC certified |
| Equipment | Mixed brands (Lincoln + Miller typical), 5-15 year old fleet |
| Pain | Field rejections from inspectors, rework costs, CWI inspector scheduling |
| Budget authority | VP Operations or Quality Manager |
| Geography | Texas, Ohio, Pennsylvania, Indiana (steel country) |
| Current monitoring | None (80% likelihood) or basic Lincoln CheckPoint on newest machines only |

**Why they are ideal first:**
- High volume of code-required welds (every structural weld needs inspection documentation)
- Mixed equipment brands = cannot use OEM solutions
- Field rejection of a weld on an erected beam costs $10K-$50K+ (crane, crew, scaffolding to fix)
- Quality Manager has budget authority and compliance pressure (AISC audit)
- Moderate tech-savviness (use ERP systems, familiar with SaaS)

**Example companies (public information):**
- Nucor Building Systems fabrication facilities
- Schuff Steel (regional offices)
- Mid-size AISC-certified fabricators (search AISC certified fabricator directory)

### Customer 2: Pressure Vessel / Heat Exchanger Manufacturer

**Archetype:** ASME-certified shop building pressure vessels, boilers, heat exchangers for petrochemical/power industry.

| Attribute | Target Profile |
|-----------|---------------|
| Size | 10-30 welding stations, 25-60 employees |
| Revenue | $3M-$15M annual |
| Certifications | ASME U, U2, R stamps (pressure vessel code) |
| Equipment | Mixed, often older heavy-duty equipment (sub-arc, GMAW, GTAW) |
| Pain | Every weld requires RT/UT (X-ray or ultrasonic). NDT costs are $200-500 per weld. 100% inspection required. |
| Budget authority | QA Manager or Plant Manager |
| Geography | Gulf Coast (TX, LA), Midwest (OH, IN, IL) |
| Current monitoring | Paper-based weld logs (WPS/PQR tracking manually) |

**Why they are ideal:**
- EXTREME pain from NDT costs (100% volumetric inspection required by code)
- Even a 20% reduction in NDT re-inspection saves $50K+/year
- Compliance documentation is a nightmare (our digital logs solve this)
- Very high cost of defects (pressure vessel failure = catastrophic, regulatory shutdown)
- Willing to pay premium for quality assurance tools

**Discovery insight:** These shops currently have a QC person manually recording weld parameters on paper for each joint. Digitizing this alone is worth $50/month. The defect detection is a bonus.

### Customer 3: Pipeline Fabrication Spool Shop

**Archetype:** Fabricates pipe spools (pre-welded pipe assemblies) for refineries, power plants, petrochemical facilities.

| Attribute | Target Profile |
|-----------|---------------|
| Size | 15-40 welding stations |
| Revenue | $5M-$30M annual |
| Certifications | ASME B31.3 (Process Piping), API 1104 (Pipeline) |
| Equipment | Mixed, heavy on GTAW root + GMAW fill |
| Pain | X-ray every weld, high reject rates on root pass, tight delivery schedules |
| Budget authority | Project Manager or QC Manager |
| Geography | Gulf Coast, Alberta (Canada) |
| Current monitoring | Some use weld parameter recording for nuclear work, nothing for standard pipe |

**Why they are ideal:**
- Pipe welding has high defect rates (positional welding is hard)
- RT (X-ray) inspection is expensive ($300-800/weld) and creates scheduling bottlenecks
- Real-time feedback during root pass is extremely valuable (root pass defects cause 70%+ of rejects)
- Fast ROI calculation: if we reduce repair rate from 8% to 4%, that saves $100K+/year

### Customer 4: Heavy Equipment / Mining Equipment Fabricator

**Archetype:** Builds heavy machinery, mining equipment, construction equipment components.

| Attribute | Target Profile |
|-----------|---------------|
| Size | 30-80 welding stations |
| Revenue | $10M-$50M annual |
| Certifications | AWS D1.1, D14.3 (Earthmoving Equipment), ISO 3834 |
| Equipment | Heavy MIG/flux-core, mixed brands, high deposition |
| Pain | Warranty claims from field failures, inconsistent quality across shifts |
| Budget authority | VP Manufacturing or Quality Director |
| Geography | Midwest (Caterpillar supply chain), Pacific Northwest |
| Current monitoring | Some Lincoln data logging on automated cells, nothing on manual |

**Why they are ideal:**
- High volume + high consequence = large addressable spend per customer
- Warranty claims from weld failures in the field are extremely expensive ($50K-$500K)
- Multiple shifts with varying quality = value of consistent monitoring
- Larger shops have budget and willingness to invest in technology
- Existing familiarity with data-driven manufacturing (lean, six sigma)

### Customer 5: Welding Training School / Community College

**Archetype:** AWS SENSE-accredited welding education program.

| Attribute | Target Profile |
|-----------|---------------|
| Size | 20-40 welding booths |
| Revenue | Tuition-funded or public institution |
| Certifications | AWS SENSE accredited |
| Equipment | Mixed (donated from multiple OEMs), training-grade |
| Pain | Instructor cannot watch all students simultaneously. Quality of training varies. |
| Budget authority | Department Head / Dean of Trades |
| Geography | Nationwide (1,500+ programs in US) |
| Current monitoring | None (some schools have old Lincoln U/21 units with basic displays) |

**Why they are ideal (STRATEGIC, not revenue):**
- **TRAINING DATA GOLDMINE:** Students produce thousands of welds per semester with known defects (they are learning!). Instructor grades each weld visually. This creates labeled training data at massive scale.
- **PARTNERSHIP MODEL:** Offer free/discounted hardware in exchange for anonymized training data + feedback.
- **PRODUCT VALIDATION:** If system helps students improve faster, that is a publishable case study and powerful marketing.
- **LOW RISK DEPLOYMENT:** No liability concerns (training coupons, not production parts).
- **FUTURE PIPELINE:** Students graduate and go to fab shops -- they request ArcSense at their new employer (demand generation).

**Pricing for schools:** Free hardware, $50/month/station (discounted) in exchange for data rights agreement.

## Discovery Questions

### For Fabrication Shop Quality Managers:

**Understanding current pain:**
1. "Walk me through what happens when a weld defect is found during inspection. What does that cost you in time, materials, and labor?"
2. "What percentage of your welds go through NDT? What does that inspection cost per weld?"
3. "What is your current repair/reject rate? Has it been going up or down?"
4. "How do you currently track weld quality across operators and shifts? Paper? Software? Nothing?"

**Understanding current solutions:**
5. "Do you use any weld monitoring equipment today? (Lincoln CheckPoint, Miller Insight, anything?)"
6. "If you do have monitoring, what does it actually tell you? Is it useful?"
7. "What brands of welding equipment do you use? Is it all one brand or mixed?"

**Validating our value prop:**
8. "If a device could tell you in real-time whether a weld is likely to pass or fail inspection, what would that be worth to you per station per month?"
9. "Would your welders accept a device that gives them immediate quality feedback? Or would they see it as surveillance?"
10. "If the device reduced your NDT inspection volume by 50% (by pre-screening), what would that save you annually?"

**Pricing and purchase process:**
11. "What is your annual budget for quality assurance tools and equipment?"
12. "Who would need to approve a $500 equipment purchase + $150/month subscription? How long does that take?"
13. "Do you buy equipment directly, or through distributors (like Airgas, Praxair)?"

**Qualifying interest:**
14. "Would you be interested in piloting this on 5 stations for free in exchange for feedback and letting us record anonymized weld data?"
15. "What would you need to see (accuracy, reliability, ROI) to justify purchasing this for all your stations?"

### For Welding School Instructors:

1. "How do you currently assess student weld quality? Visual only, or do you have testing capabilities?"
2. "How many welds does an average student produce per day/week?"
3. "What are the most common defects students produce? Do they match the top 4 (porosity, undercut, cold lap, burn-through)?"
4. "Would real-time feedback accelerate student learning? Have you seen evidence of this?"
5. "Would you be willing to share anonymized weld data (signals + quality grades) in exchange for free equipment?"

## Demand Signals to Watch

### Strong positive signals (proceed aggressively):
- [ ] Quality Manager says "I would pay for that today" unprompted
- [ ] Customer asks about timeline for availability (wants it NOW)
- [ ] Customer offers to be a pilot site without being asked
- [ ] Customer shares specific dollar figures for defect costs (they have quantified the pain)
- [ ] Customer asks "does it work with [brand]?" (confirms brand-agnostic is valued)
- [ ] Multiple customers independently mention the same use case

### Moderate positive signals (continue validation):
- [ ] Customer agrees to 30-minute discovery call
- [ ] Customer introduces you to their VP/Plant Manager
- [ ] Customer asks detailed technical questions (engaged, evaluating seriously)
- [ ] Customer mentions they evaluated Lincoln/Miller solutions but did not buy (price or brand lock)

### Negative signals (pivot or reconsider):
- [ ] Customer says "we already have Lincoln CheckPoint and it is fine"
- [ ] Customer says "our welders would rip it off the machine"
- [ ] Customer says "we cannot afford $150/month per station" (price too high)
- [ ] Customer says "we do not have WiFi in the shop" (connectivity barrier)
- [ ] Customer has <2% reject rate (pain is not severe enough to justify)
- [ ] Customer says "we would need this to be certified as an inspection device" (regulatory barrier)

### Critical invalidation signals (STOP):
- [ ] 10+ conversations, zero interest in pilot
- [ ] Every customer says they need >95% accuracy before they would trust it (impossible for v1)
- [ ] Insurance/liability concerns make customers unwilling to adopt
- [ ] Welding equipment OEMs announce free cross-brand monitoring (window closing)

## Outreach Plan

### Phase 1: Warm Network (Weeks 1-4)

**Goal:** 10 discovery conversations with qualified prospects

| Channel | Action | Expected yield |
|---------|--------|---------------|
| LinkedIn | Connect with Quality Managers at AISC-certified fabricators in TX/OH/PA. Personalized messages referencing their certifications. | 3-5 conversations |
| AWS (American Welding Society) | Join local section, attend monthly meeting, introduce self | 2-3 conversations |
| Local welding supply distributors | Visit Airgas/Praxair branches, ask who their biggest fabricator customers are | 2-3 introductions |
| Welding schools | Email AWS SENSE-accredited programs within driving distance | 2-3 conversations |
| Reddit/forums | Post in r/Welding, r/WeldingPorn (disguised as research question about quality monitoring) | Gauge interest, find leads |

### Phase 2: Cold Outreach (Weeks 4-8)

**Goal:** 5 LOIs (Letters of Intent) for free pilot program

| Channel | Action | Expected yield |
|---------|--------|---------------|
| AISC certified fabricator directory | Systematic outreach to all shops in target geographies (500+ listings) | 5-10 conversations |
| LinkedIn Sales Navigator | Target: "Quality Manager" OR "QC Manager" at companies with "fabrication" + "welding" | 5-10 conversations |
| Email campaign | Short, value-focused emails to QM/VP Ops at target companies | 2-3% response rate |
| Industry events | Attend regional FABTECH (September) or AWS events | 5-10 conversations per event |

### Phase 3: Pilot Recruitment (Weeks 6-10)

**Goal:** 3 signed pilot agreements (free hardware, 6-week commitment)

**Pilot offer:**
- FREE sensor hardware (5 units installed at their facility)
- FREE SaaS access for 6 weeks
- We provide installation support (on-site visit)
- They provide: access to welders, permission to record data, post-pilot interview
- Optional: share NDT results for accuracy benchmarking (anonymous)

**Pilot agreement terms:**
- No payment required during pilot
- Data collected is jointly owned (we can use anonymized data for model improvement)
- Post-pilot option to purchase at $500/unit + $100/month (pilot discount from $150)
- No obligation to purchase

### Phase 4: Trade Show Presence (Month 4-6)

**Target events:**
- **FABTECH** (September, typically Orlando/Las Vegas/Chicago) - #1 welding/fabrication trade show in North America. 40,000+ attendees. Booth cost: $5K-15K (start with "startup alley" if available)
- **AWS Weldmex** (regional events) - Smaller, more targeted
- **Local AWS Section meetings** (monthly, free) - Direct access to welding professionals

**Trade show strategy:**
- Demo unit running on a small MIG welder in the booth
- Show real-time classification on a screen
- Collect leads (target: 50+ qualified contacts per show)
- Offer pilot program sign-up on the spot

### Outreach Messaging Framework

**Cold email template (Quality Manager):**

```
Subject: Reducing your NDT costs by 40% with real-time weld monitoring

Hi [Name],

I noticed [Company] is AISC-certified and does structural steel fabrication. 
I'm building a tool that gives welders real-time quality feedback during 
welding -- catching porosity, undercut, and cold lap before the part ever 
reaches inspection.

Unlike Lincoln/Miller monitoring, it works on any brand of welder and uses 
AI to identify specific defect types (not just "parameter out of range").

Early results show 40-60% reduction in NDT inspection volume by 
pre-screening welds.

Would you have 20 minutes this week to tell me about your current quality 
process? I'm genuinely trying to understand the problem, not sell you 
anything yet.

[Name]
```

**LinkedIn connection message:**

```
Hi [Name] -- I'm developing AI-based weld quality monitoring that works on 
any welder brand. I'd love 15 minutes to understand your current quality 
challenges. No pitch, just research. Would you be open to a quick call?
```

## Validation Timeline

| Week | Activity | Deliverable |
|------|----------|-------------|
| 1-2 | Build outreach list (50 fabricators, 10 schools) | Prospect database |
| 2-4 | Warm outreach (LinkedIn, AWS sections, suppliers) | 10 discovery calls |
| 3-5 | Discovery interviews, document patterns | Pain/value validation doc |
| 4-6 | Cold outreach campaign | 5+ additional conversations |
| 5-8 | Pilot recruitment conversations | 3 signed pilot LOIs |
| 6-10 | Prototype building (parallel with outreach) | Working demo unit |
| 10-14 | Pilot deployment at 2-3 sites | Installation + data collection |
| 14-18 | Pilot results analysis + purchase conversations | 2+ paid conversions |

## Budget for Validation Phase

| Activity | Cost | Notes |
|----------|------|-------|
| LinkedIn Sales Navigator | $100/month x 3 | Prospecting tool |
| AWS Section membership | $100/year | Industry network |
| Travel (customer visits) | $3K | 5-8 visits within driving distance |
| Trade show (FABTECH booth) | $8K | Booth + travel + demo equipment |
| Pilot hardware (15 units) | $1.5K | BOM cost for prototypes |
| Pilot installation travel | $2K | On-site at 3 pilot locations |
| Email tools (Mailchimp/Apollo) | $200/month x 3 | Outreach automation |
| **Total validation budget** | **~$16K** | |
