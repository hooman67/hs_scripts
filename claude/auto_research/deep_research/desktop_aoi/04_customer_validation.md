# 04 Customer Validation: Desktop AI-Powered AOI

## First 5 Customers to Approach

### 1. Small Contract Manufacturer -- Bay Area

- **Profile:** 10-20 person shop, does prototype and low-volume assembly (100-2,000 boards/run) for hardware startups
- **Example companies to research:** Tempo Automation (now larger, but their early customers are our target), A2 Global Electronics (Fremont, CA), Sierra Circuits (Sunnyvale, CA -- does assembly), Bittele Electronics (if they have US operations)
- **Why first:** Bay Area shops serve hardware startups that demand quality but the shops can't afford $50K AOI. They're tech-forward (likely use modern EDA tools, comfortable with software).
- **How to find:** Google "PCB assembly" + city name for SF/Oakland/San Jose/Fremont. Check IPC member directory. LinkedIn search "PCB assembly" + "production manager" in Bay Area.

### 2. Makerspace / Hackerspace with PCB Capability

- **Profile:** Community workshop that offers PCB assembly services or classes, 2-5 staff, high technical sophistication but limited budget
- **Example:** Noisebridge (SF), Pumping Station One (Chicago), NYC Resistor, HeatSync Labs (Phoenix)
- **Why:** Extremely accessible (community-oriented, open to new tools), willing to beta test, great word-of-mouth to hardware startup ecosystem. Less price-sensitive on "cool tools" even if volume is low.
- **How to find:** Hackerspace.org directory. Local meetup groups. Direct visit.

### 3. University Electronics Lab / Research Group

- **Profile:** EE department or research lab that assembles custom PCBs for research projects, needs quality verification but has zero budget for industrial AOI
- **Example:** Stanford EE prototyping lab, MIT Media Lab hardware shop, any university with active hardware research
- **Why:** Lower price sensitivity (grant budgets flex), generates academic credibility, grad students provide detailed feedback, potential for research collaboration (published papers = free marketing)
- **How to find:** Department websites listing lab facilities. Email lab managers directly.

### 4. Growing Startup with In-House Assembly

- **Profile:** Hardware startup (Series A/B, 20-50 people) that brought PCB assembly in-house to control quality and iteration speed. Producing 500-5,000 boards/month.
- **Example companies:** Any hardware startup in consumer electronics, IoT, or robotics that has graduated from outsourced to in-house assembly
- **Why:** They have budget ($5K is trivial in a $5M fundraise), they care intensely about quality (their brand depends on it), and they're tech-forward.
- **How to find:** AngelList/Crunchbase search for hardware startups. LinkedIn "manufacturing engineer" at companies with 20-50 employees in hardware.

### 5. Military/Aerospace Small Subcontractor

- **Profile:** 5-15 person shop building specialty boards for defense/aerospace primes. IPC Class 3 requirements. Currently does 100% manual inspection because they can't afford AOI but MUST have zero defect escapes.
- **Why:** Extreme pain point (regulatory requirements mandate inspection, failure costs are catastrophic), willing to pay premium ($5K is nothing vs. cost of a field failure in a satellite), and they're underserved (too small for Koh Young, too quality-critical for no AOI).
- **How to find:** SAM.gov contractor search. IPC member directory filtered by small business. SMTA chapter meetings in defense corridors (San Diego, Huntsville, Colorado Springs).

## Discovery Questions

### Pain Qualification
1. "Walk me through what happens after a board comes off your reflow oven. What's your current inspection process?"
2. "How many boards per week do you inspect? How long does each one take?"
3. "In the last 6 months, how many defects escaped to a customer? What did that cost you (in dollars, time, or relationship damage)?"
4. "Have you ever lost a contract or bid because of quality concerns?"
5. "What's the most frustrating part of your current quality process?"

### Solution Validation
6. "If a tool could automatically flag solder defects in 10 seconds per board, what would that be worth to you per month?"
7. "At what price point would this be an obvious yes? At what price would you say no?"
8. "Would you prefer to buy hardware outright or pay a monthly subscription?"
9. "What would prevent you from using a tool like this?" (Looking for: trust in AI, workflow disruption, training time)
10. "If I showed you a working demo in 30 days, would you be willing to trial it on your line for 2 weeks?"

### Workflow & Integration
11. "What EDA tool do you use? (KiCad, Altium, Eagle, OrCAD)"
12. "How many unique board designs do you run per month?"
13. "Who would operate this tool -- a technician, engineer, or the owner?"
14. "Where on your bench would this sit? What's your space constraint?"
15. "Do you already have any vision/magnification equipment (microscopes, cameras)?"

## Demand Signals (What Confirms Interest)

**Strong positive signals (proceed with confidence):**
- Customer says "How soon can I buy this?" or "Can I be a beta tester?"
- Customer quantifies their defect escape cost at >$10K/year
- Customer has ALREADY tried to solve this (looked at Chinese AOI on Alibaba, built a DIY jig, hired a dedicated inspector)
- Customer offers to pay a deposit for early access
- Customer refers you to other shops with the same problem

**Moderate positive signals (promising but need more validation):**
- Customer agrees the problem exists but hasn't quantified the cost
- Customer says "If it works reliably, I'd consider it"
- Customer asks detailed technical questions (resolution, defect types, speed)
- Customer invites you to see their production floor

**Negative signals (reconsider the approach):**
- Customer says "We don't have a quality problem" (denial or genuinely not painful)
- Customer says "$5K is too much" (price sensitivity suggests low-value application)
- Customer says "I don't trust AI for quality decisions" (adoption barrier)
- Customer says "Our volumes are too low to justify any automation" (<50 boards/month)
- Multiple customers say "We'd need 3D inspection / X-ray" (scope creep beyond v1)

**Kill criteria:** If 8+ out of 10 shops visited show negative signals, the market is not ready. Pivot to software-only (sell to shops that already have cameras) or pivot to a different vertical (e.g., medical device assembly where regulatory pressure forces inspection).

## Cold Outreach Plan

### Where Buyers Hang Out

| Channel | Specifics | Reach | Quality |
|---------|-----------|-------|---------|
| Reddit | r/PrintedCircuitBoard (28K), r/electronics (2.2M), r/AskElectronics (580K) | High | Medium (mix of hobbyists and pros) |
| Forums | EEVBlog forum, SMTnet.com forum | Medium | High (industry professionals) |
| LinkedIn | "PCB assembly" + "production manager" OR "quality" | High | High |
| Trade shows | IPC APEX EXPO (Jan, San Diego), SMTA International (Sep), Productronica | Low (annual) | Very High |
| Trade associations | IPC chapters (local meetings monthly), SMTA chapters | Medium | Very High |
| YouTube | EEVBlog, Phil's Lab, Robert Feranec -- viewers are target customers | High | Medium |
| Alibaba/forums | People searching for "desktop AOI" on Alibaba are literally our buyers | Medium | Very High (active shoppers) |

### Outreach Sequence

**Phase 1: Local (Weeks 1-3)**
1. Google Maps search for "PCB assembly" within 50 miles
2. Visit 3-5 shops in person (call ahead, offer to buy lunch)
3. Ask discovery questions, observe their workflow
4. Do NOT pitch the product yet -- just learn

**Phase 2: Digital (Weeks 2-4)**
1. Post on r/PrintedCircuitBoard: "I'm building a low-cost AI inspection tool for small PCB shops. What would you need it to do?" (genuine question, not sales pitch)
2. Join SMTnet forum, contribute knowledge for 2 weeks before mentioning product
3. LinkedIn outreach to 50 production managers at small CMs (personalized messages referencing their company)

**Phase 3: Demo (Weeks 5-8)**
1. Build minimal demo (even if it's just a camera + laptop showing detection on pre-captured images)
2. Offer free on-site demos to interested contacts
3. Post demo video on YouTube (target PCB assembly community channels)
4. Submit talk proposal to local IPC/SMTA chapter meeting

**Phase 4: Beta Program (Weeks 9-12)**
1. Select 3-5 beta customers from Phase 2-3 interest
2. Offer: "Free hardware + 3 months free software in exchange for weekly feedback and permission to use anonymized inspection data"
3. Install, support intensively, iterate rapidly
4. Collect testimonials and case studies for sales material

### Cold Email Template

Subject: Quick question about your inspection process

Hi [Name],

I noticed [Company] does [low-volume / prototype / specialty] PCB assembly. I'm researching how small shops handle solder inspection -- most I've talked to rely on manual visual checks under magnification.

I'm building a desktop AI inspection tool (think: automated AOI for $5K instead of $50K) and would love 15 minutes to understand your workflow. Not selling anything -- just trying to understand if this problem is painful enough to solve.

Would you be open to a quick call or coffee? I'm local to [area].

Best,
Hooman
