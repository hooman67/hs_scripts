# Product Definition: CNC Tool Wear Acoustic Detection

## Problem Statement

Small and mid-size CNC machine shops (1-50 machines) suffer catastrophic tool breakage events that cost $5,000-$50,000 per incident in scrapped parts, machine damage, and unplanned downtime. The average shop with 10 machines experiences 2-4 tool breakage events per month, representing $120K-$2.4M in annual losses.

**Current solutions fall into two categories:**

1. **Professional tool monitoring systems** ($30K-$50K per machine from Montronix/Marposs, Caron Engineering): Force sensors, vibration accelerometers, and proprietary software. Only accessible to large aerospace/automotive manufacturers running $500K+ machines.
2. **Operator intuition + scheduled replacement**: Operators listen for "bad sounds," replace tools on conservative time schedules (wasting 30-50% of remaining tool life), and still get surprised by breakage.

**The mid-market gap**: 300,000+ CNC machines in the US alone are monitored by nothing more than an operator's ear. These shops cannot justify $50K per machine for monitoring when the machine itself cost $80-200K.

**Specific pain points:**
- Tool breakage destroys the workpiece ($50-$5,000 in material), damages the spindle ($3K-$15K repair), and causes 4-16 hours of unplanned downtime ($200-$500/hr in lost production)
- Conservative tool replacement wastes 30-50% of remaining tool life ($5-50 per tool x 50-200 tools/month = $250-$10,000/month in premature replacement)
- No data exists for process improvement: shops cannot correlate tool wear with cutting parameters because they have no wear measurement
- Operator-dependent: experienced machinists retiring takes tribal knowledge of "what sounds right" with them

**Confidence: HIGH** -- validated through industry publications (Modern Machine Shop, CNC Cookbook), trade show reports, and confirmed by academic research on acoustic emission monitoring of cutting tools (200+ published papers since 2010).

---

## Product Scope: Version 1 (MVP)

### Core Capabilities (3 features only)

**1. Acoustic Wear State Indicator**
- MEMS microphone array (3x ICS-43434) captures airborne acoustic emission during cutting
- ML model classifies tool state into 4 zones: FRESH / NORMAL WEAR / APPROACHING END-OF-LIFE / DANGER
- Simple traffic-light display (green/yellow/orange/red) on local screen and cloud dashboard
- Updates every cutting pass (typically every 5-60 seconds depending on operation)

**2. Breakage Prediction Alert**
- Real-time classification: "Tool approaching failure within next 10-30 minutes of cutting time"
- Push notification to operator's phone, audible alarm on device, cloud dashboard alert
- Alert gives operator time to complete current part and change tool at next natural pause
- Target: detect 80%+ of impending failures with <5% false alarm rate

**3. Tool Life Tracking Dashboard**
- Cloud-based dashboard showing tool wear progression over time
- Actual vs. expected tool life per tool type and operation
- Simple analytics: average tool life by tool number, by material, by operation
- Export data for process improvement

### Explicitly Out of Scope for V1
- Automatic machine stop/feed override (we alert, operator decides)
- Vibration/force sensing (acoustic only -- keeps hardware cost to $3 in mics)
- Integration with CNC controller (no G-code parsing, no RS-232/Ethernet connection to machine)
- Multi-axis monitoring (single spindle only in V1)
- Chatter detection or surface finish prediction (future roadmap)
- Tool inventory management or ERP integration

---

## User Workflow

### Day 1: Installation (Target: <30 minutes, no electrician needed)

1. Operator mounts sensor unit on CNC machine enclosure (magnetic mount or 3M VHB tape) -- positioned near spindle area but OUTSIDE the machine enclosure (no coolant exposure)
2. Plugs in USB-C power (or optional 24V DC from machine's auxiliary power)
3. Connects to shop WiFi via phone app (WPS or QR code)
4. App prompts: "What tool is in the spindle? What material are you cutting?" (drop-down selection)
5. System records 5-10 minutes of "healthy cutting" as baseline during first normal operation
6. Traffic light goes green. Setup complete.

### Ongoing Operation

1. **Operator starts cutting**: System automatically detects cutting vs. idle via acoustic signature
2. **During cutting**: Traffic light shows current tool state. Green = good. No action needed.
3. **Yellow alert** (approaching end-of-life): "Tool #3 showing increased wear. Estimated 45 min cutting time remaining."
4. **Orange alert** (end-of-life imminent): "Tool #3 nearing end of life. Change recommended at next part completion."
5. **Red alert** (breakage imminent): "DANGER: Tool #3 anomalous acoustic signature. Stop and inspect immediately." Audible alarm.
6. **Tool change**: Operator taps "Tool Changed" on device or app. System resets to green.

### Weekly Review (Optional, Cloud Dashboard)

- View tool life trends: "Tool #7 (1/2 inch end mill) averaging 47 minutes in aluminum. Industry benchmark: 60 minutes. Consider reducing feed rate."
- Cost tracking: "This week: 0 breakage events (saved ~$8K vs. last month's average). 3 tools changed at orange alert."
- Fleet view (multi-machine shops): all machines on one screen with status indicators

---

## Pricing Model

| Tier | Price | Includes | Target |
|------|-------|----------|--------|
| Basic | $49/month per machine | Hardware unit (included, no upfront cost), wear indication, breakage alerts, mobile app | 1-5 machine shops, job shops |
| Professional | $89/month per machine | Everything in Basic + cloud dashboard, analytics, tool life tracking, multi-machine fleet view | 5-20 machine shops |
| Enterprise | $129/month per machine | Everything in Pro + API access, custom alert rules, priority support, on-prem data option | 20+ machine shops, contract manufacturers |

**Hardware model**: Hardware included with 12-month subscription commitment (hardware cost ~$43 per unit subsidized by subscription revenue). Month-to-month available at $149/month with $199 upfront hardware deposit.

**Revenue model math (realistic assessment)**:
- At blended average of $79/month per machine:
- 500 machines x $79/month x 12 = $474K ARR
- To reach original $1.2M ARR target requires ~1,265 machines
- Revised Year 2 target: $500K ARR at 500 machines is achievable
- Year 3 target: $1.2M ARR at 1,200 machines (with organic growth + referrals)

**Unit economics per machine**:
- Hardware COGS: $43 (amortized over 12-month commitment = $3.58/month)
- Cloud costs: $3-5/month
- Customer support allocation: $5-8/month
- Gross margin: ~80% at $79/month blended

**Confidence: MEDIUM** -- hardware-as-a-service model validated by similar companies (MachineMetrics, Shoplogix, Samsara). Pricing validated against competitor alternatives ($50K one-time vs. our $1K-1.5K/year). ARR growth depends on customer acquisition velocity in a niche market.

---

## Ideal First Customer Profile

### Primary Target: Small Job Shops Running Aluminum (3-15 machines)

**Why they're ideal:**
- Owner-operated: one person decides to buy. No procurement department, no IT review.
- Run high-mix/low-volume work: frequent tool changes, different operations, hard to build intuition for tool life on each job
- Aluminum is the ideal material for acoustic detection (clean, high-frequency cutting sound, distinct wear signatures well-documented in literature)
- Tool breakage in aluminum often damages expensive aerospace parts ($500-$5,000 per scrap)
- Already pay $200-500/month for CAM software -- established willingness to pay for productivity tools
- Found at local machine shop meetups, Instagram CNC community, Practical Machinist forums

**Specific customer archetype:**
- "Mike's Precision" -- 8 Haas VF-2 machines, 12 employees, $2-4M revenue
- Runs aerospace aluminum parts, medical device prototypes
- Lost $15K last month to a tool breakage that gouged a titanium part
- Has WiFi in the shop (already uses probing/tool setting systems)
- Would pay $400-700/month total to protect his 8 machines from breakage

**Confidence: HIGH** -- this shop profile represents the bulk of the 300K+ CNC machines in the US. They are reachable via online communities, trade shows (IMTS, Eastec), and local manufacturing associations.

### Secondary Target: CNC Training Facilities / Makerspaces

**Why:**
- Very high breakage rate (student operators)
- Budget for tooling is a known expense line
- Easy to reach (community colleges with CNC programs, TechShop-style spaces)
- Provide testimonials and case studies quickly

### Anti-Target (Explicitly Avoid in Year 1)
- Aerospace primes (Lockheed, Boeing) -- already have Montronix, 18-month procurement cycles
- Automotive OEMs -- same issue, plus plant-wide IT security requirements
- Swiss-type lathe shops (different acoustic profile, needs separate model)
- Shops with full enclosures and through-spindle coolant at max pressure (signal-to-noise challenge)
- Shops without WiFi (surprisingly common in older facilities)
