# Product Definition: CNC Tool Wear Acoustic Detection

## 1. Problem Statement

**Who:** Owners and operators of small/mid-size CNC machine shops (1-20 machines). Typically owner-operated or managed by a shop foreman with 2-15 machinists. Annual revenue $500K-$10M. These shops run job-shop or low-volume production work for aerospace, automotive, medical, and general manufacturing customers.

**How painful:** Tool breakage is one of the most expensive unplanned events in a CNC shop:
- **Direct cost per incident:** $5K-$50K (scrapped workpiece + replacement tooling + spindle damage risk + machine downtime)
- **Frequency:** A typical 10-machine shop experiences 2-5 unexpected breakage events per month
- **Annual cost:** $120K-$3M per year in avoidable losses for a 10-machine shop
- **Secondary pain:** Missed delivery deadlines damage customer relationships; a single scrapped aerospace part can cost $20K+ in material alone (titanium, Inconel)
- **Operator stress:** Machinists develop "ear fatigue" from constantly listening for problems, especially during unattended or lights-out operation

**What they do today:**
1. **Listen manually** - Experienced machinists use their ears to detect chatter, squealing, or changes in cutting sound. Works only when they are physically present and attentive. Fails completely for lights-out machining.
2. **Scheduled replacement** - Replace tools at conservative fixed intervals (e.g., every 50 parts regardless of actual wear). Wastes 20-40% of tool life, costing $10K-$50K/year in premature tool replacement.
3. **Spindle load monitoring** - Some newer CNC controls show spindle load percentage. Crude, detects only catastrophic failures (too late), not gradual wear.
4. **Nothing** - Estimated 80%+ of small shops have zero tool monitoring. They react to failures rather than preventing them.
5. **Professional systems (rare)** - <5% of small shops have Montronix/Caron Engineering/equivalent. Cost ($20K-$50K per machine) is prohibitive. Requires integrator for installation.

---

## 2. Product Scope v1 (MVP)

### Three Features Only:

**Feature 1: Real-Time Tool Health Score**
- Continuous green/yellow/red indicator per spindle
- Updates every 2 seconds during cutting
- Visual display on local device (LED bar) + web dashboard
- No configuration needed after initial 30-minute "learning" period per tool/material combination

**Feature 2: Breakage Prediction Alert**
- Push notification (SMS + email + dashboard) when acoustic signature indicates imminent failure (>80% confidence)
- Target: 30-60 seconds advance warning (enough time for operator to hit feed hold or for automated stop)
- Alert includes: which machine, estimated severity, recommended action

**Feature 3: Tool Life Tracking Dashboard**
- Historical wear progression curves per tool
- Actual vs. expected tool life comparison
- Simple cloud dashboard accessible from phone/tablet/desktop
- Weekly summary email: tools replaced, alerts triggered, estimated savings

### What v1 Does NOT Do:
- Does NOT integrate with CNC control (no M-code triggers, no automatic feed override)
- Does NOT predict specific failure mode (just "tool is degrading" vs. "tool is about to break")
- Does NOT support turning/grinding/EDM (milling only in v1)
- Does NOT provide G-code optimization or speed/feed recommendations
- Does NOT require internet for basic alerting (local LED + buzzer works offline; cloud for dashboard only)
- Does NOT monitor spindle bearings, coolant, or other machine health indicators

---

## 3. User Workflow: Day 1

**Step 1: Unbox (2 minutes)**
- Open box containing: sensor unit (hockey-puck sized, ~100mm diameter x 30mm), magnetic mount base, USB-C power cable, quick-start card with QR code

**Step 2: Mount (5 minutes)**
- Attach magnetic base to CNC machine column or spindle housing (external, does not enter work envelope)
- Position sensor within 300mm of spindle (magnetic mount allows repositioning)
- Route USB-C power cable to nearest outlet or USB port on CNC control

**Step 3: Connect WiFi (3 minutes)**
- Scan QR code on quick-start card with phone
- Opens web app; sensor broadcasts WiFi AP for initial setup
- Select shop WiFi network, enter password
- Sensor connects to cloud; LED turns solid green

**Step 4: Create Account (2 minutes)**
- Enter email, shop name, machine name/number
- Select machine type from list (e.g., "Haas VF-2", "Tormach 1100M") or "Other"

**Step 5: Baseline Learning (30 minutes, unattended)**
- Dashboard prompts: "Run your normal cutting operations for 30 minutes. We are learning what good sounds like."
- Operator runs normal jobs; system records acoustic baseline for healthy cutting
- After 30 minutes: "Baseline complete. Monitoring active."
- LED bar on device now shows real-time green/yellow/red

**Step 6: Normal Operation (ongoing)**
- Operator runs jobs as normal; glances at LED bar occasionally
- Gets phone alert if tool wear exceeds threshold
- Checks weekly dashboard summary for tool life trends

**Total setup time: <15 minutes active, 30 minutes passive learning**

---

## 4. Pricing Model

### Hardware: $199 one-time per sensor unit
- **COGS:** ~$50 (mics $3, MCU $8, WiFi $3, PCB $5, enclosure $10, magnetic mount $5, power supply $5, packaging $5, misc $6)
- **Gross margin:** 75% on hardware
- **Justification:** Must be under $200 to be an impulse purchase for shop owner. At $199, payback period is <1 week (prevents one $5K+ incident). No purchase order or capital expenditure approval needed at most shops under $500.

### Software: $99/month per machine (or $79/month annual prepay)
- **Includes:** Cloud dashboard, unlimited alerts, data storage, model updates, phone support
- **Justification:** $99/month = $1,188/year. If system prevents even one $5K breakage event per year, ROI is 4x+. Comparable to other shop SaaS (ProShop ERP: $150/month, MachineMetrics: reportedly $500+/month).
- **Alternative considered:** $49/month was considered but $99 provides more credible positioning and supports customer success costs for early-stage company.

### Volume Discount:
- 5+ machines: $149/unit hardware, $79/month software
- 10+ machines: $99/unit hardware, $59/month software

### Revenue Model at Scale:
- 500 machines monitored: 500 x $99/month = $49,500/month = **$594K ARR from subscriptions**
- Plus ~$100K in hardware revenue = **$694K year 1**
- At steady state (low churn): approaches $1.2M ARR with 1000 machines
- Note: Original $1.2M ARR estimate at 500 machines assumed $200/month; revised to $99/month requires 1000 machines for same ARR. Alternatively, maintain $200/month for premium tier with integration features.

### Revised Revenue Projection (Conservative):
- Year 1: 100 machines x $99/month + hardware = ~$140K ARR
- Year 2: 500 machines x $99/month + hardware = ~$700K ARR  
- Year 3: 1500 machines x $99/month + hardware = ~$2M ARR

---

## 5. Ideal First Customer Profile

**Demographics:**
- CNC shop with 3-8 vertical milling machines (Haas VF series most common)
- Located within 2-hour drive of founder (for hands-on support during beta)
- Revenue: $1M-$5M/year
- 5-15 employees
- Owner is hands-on (still walks the shop floor)
- Running aluminum and steel (not exotic materials yet)

**Psychographics:**
- Owner is tech-forward (has shop ERP or at least uses digital quoting)
- Has experienced at least one painful breakage event in last 6 months
- Interested in lights-out or unattended machining but nervous about tool failure
- Active on Practical Machinist forums, Instagram CNC community, or YouTube CNC channels
- Not price-sensitive on $200 if it solves a real problem (these shops spend $500-$2K/month on tooling already)

**Disqualifiers (NOT ideal first customer):**
- Shops running only manual machines
- Shops running primarily turning (v1 is milling-focused)
- Shops with existing Montronix/Caron systems (already solved their problem)
- Shops running only production (same part all day) - they already know their tool life
- Shops unwilling to share data (ML training requires their acoustic data)

**Ideal First 3 Shops (archetype):**
1. 5-machine Haas shop doing aerospace job work (high part values, high breakage cost)
2. 8-machine mixed shop doing medical device components (tight tolerances, expensive materials)
3. 3-machine garage shop owner who is also a YouTube CNC creator (marketing value + tech-forward)
