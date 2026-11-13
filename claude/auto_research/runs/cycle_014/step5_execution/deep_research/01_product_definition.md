# Product Definition: AI Weld Quality Monitoring from Electrical Signatures

## Problem Statement

**The core problem:** 500K+ welding stations in the US produce welds with zero real-time quality feedback. Defects (porosity, undercut, cold lap, burn-through) are discovered hours or days later via expensive destructive testing (DT) or non-destructive testing (NDT) -- often after the part has moved downstream. A single structural weld failure can cost $5K-$50K+ in rework, scrap, liability, and downtime.

**Who feels this pain most:**
- Small/medium fabrication shops (10-100 welders) doing structural steel, pressure vessels, or pipe work under AWS D1.1, ASME Section IX, or API 1104 codes
- These shops spend 15-30% of labor on inspection/rework
- They cannot afford $15K+ camera systems (Xiris) or $3K-10K OEM add-ons (Lincoln CheckPoint)
- They often have mixed-brand equipment (some Lincoln, some Miller, some older units)

**Why now:**
1. Edge ML chips (ESP32-S3, STM32H7) now run inference at pennies per FLOP
2. Hall-effect sensors are commodity ($3-10 for 50A-400A range)
3. AWS/ASME codes are tightening inspection requirements, creating compliance pressure
4. Labor shortage means fewer experienced welders who can "feel" a bad weld

## Product Scope: Version 1 (MVP)

**Product name:** ArcSense (working name)

**What it is:** A clamp-on retrofit sensor box ($500) + SaaS platform ($150/month) that:
1. Captures welding current and voltage waveforms in real-time (100kHz sampling)
2. Runs edge ML inference to classify weld quality pass/fail and identify specific defect types
3. Provides immediate audio/visual feedback to the welder (green/yellow/red LED + optional buzzer)
4. Logs all weld data with timestamps, operator ID, and quality scores to cloud dashboard
5. Generates compliance reports for code-required documentation

**What it is NOT (v1):**
- Not a robotic welding controller
- Not a camera/vision system
- Not a replacement for required NDT (it is a screening tool to reduce NDT costs)
- Not tied to any specific welder brand

**V1 Feature Set:**

| Feature | Priority | Confidence |
|---------|----------|------------|
| Current waveform capture (Hall-effect, 100kHz) | P0 | HIGH |
| Voltage waveform capture (differential probe) | P0 | HIGH |
| Edge ML defect classification (4 types) | P0 | MEDIUM - depends on model accuracy |
| Real-time LED indicator (green/yellow/red) | P0 | HIGH |
| WiFi upload to cloud dashboard | P1 | HIGH |
| Weld log with timestamp + operator ID | P1 | HIGH |
| Compliance report generation (PDF) | P2 | HIGH |
| Multi-process support (MIG, TIG, Stick) | P2 | MEDIUM - each process needs separate models |
| Alert notifications (email/SMS) | P2 | HIGH |

**V1 Constraints:**
- Supports GMAW (MIG) only in v1 (most common process, best-studied waveforms)
- Carbon steel and stainless only (aluminum has different signatures)
- 100-400A range (covers 80% of structural work)
- Requires WiFi for cloud features (edge classification works offline)

## User Workflow

**Installation (one-time, 15 minutes):**
1. Clamp Hall-effect sensor around output cable (no wire cutting)
2. Connect voltage leads to workpiece clamp and torch connector (banana plugs)
3. Mount sensor box near power source (magnetic mount or zip ties)
4. Power on, connect to WiFi via phone app (WPS-style setup)
5. Calibrate: run 3 test beads, confirm signal quality on app

**Daily use (zero-friction):**
1. Welder starts work as normal -- no change to technique or equipment
2. Sensor box automatically detects arc-on and begins recording
3. LED shows real-time quality: GREEN = good, YELLOW = marginal, RED = defect detected
4. At end of shift, supervisor checks dashboard for flagged welds
5. Only RED-flagged welds go to NDT inspection (reduces inspection volume by 60-80%)

**Supervisor workflow:**
1. Morning: check overnight shift quality scores on dashboard
2. Identify operators with high defect rates -- schedule retraining
3. Monthly: generate compliance reports for auditors
4. Quarterly: review trend data, identify equipment maintenance needs

## Pricing Model

| Component | Price | Margin | Notes |
|-----------|-------|--------|-------|
| Sensor hardware (one-time) | $500 | 84% ($80 BOM) | Includes 1-year warranty |
| SaaS subscription (monthly) | $150/station | ~90% | Cloud, dashboard, reports, updates |
| Annual contract option | $1,500/year | ~90% | 2 months free |
| Enterprise (50+ stations) | Custom | ~85% | Volume discount, on-prem option |
| Installation service (optional) | $200 | ~60% | Partner technician installs |

**Revenue math (Year 1 target):**
- Sell 300 units: 300 x $500 = $150K hardware revenue
- SaaS (avg 8 months active in Y1): 300 x $150 x 8 = $360K recurring revenue
- Total Year 1: $510K
- Year 2 (1000 units, full-year subs): $500K hardware + $1.8M SaaS = $2.3M
- Gross margin target: >75% blended

**Why $150/month is a no-brainer:**
- A single caught defect saves $5K-50K in rework/liability
- If system catches 1 defect per month, ROI is 33x-333x
- NDT inspection reduction alone saves $200-500/month per station
- Payback period: <3 months

## Ideal First Customer Profile

**Company:** Small-to-medium structural steel fabricator or pressure vessel manufacturer

**Characteristics:**
- 10-50 welding stations (big enough to feel pain, small enough to decide fast)
- Mixed equipment brands (cannot use OEM solutions easily)
- AWS D1.1 or ASME IX certified (compliance pressure = budget justification)
- Currently spending $2K-10K/month on NDT inspection
- Has experienced a costly rework event in the past year
- Located in manufacturing corridors: Texas, Ohio, Pennsylvania, Indiana, Wisconsin
- Decision maker: VP Operations or Quality Manager (not IT)

**Ideal first 3 customers (archetypes):**
1. **Regional structural steel fabricator** (bridges, buildings) -- 20-40 stations, AWS D1.1, mixed equipment, high rework costs from field rejections
2. **Pressure vessel/heat exchanger shop** -- 10-30 stations, ASME IX, every weld requires documentation, NDT costs are brutal
3. **Pipeline fabrication spool shop** -- 15-25 stations, API 1104, remote locations, hard to get NDT crews on-site quickly

**Anti-customer (avoid in v1):**
- Automotive OEMs (already have Lincoln/Miller systems, long sales cycles)
- Aerospace (too regulated, requires years of validation)
- Hobby/garage welders (no budget, no compliance need)
- Shops with only robotic welding (different value prop, different competition)

## Success Metrics for V1

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Defect detection accuracy | >85% (4 defect types) | Before launch |
| False positive rate | <15% | Before launch |
| Units deployed (pilot) | 10 stations, 3 shops | Month 4-5 |
| Pilot customer NPS | >40 | Month 6 |
| Paid conversions from pilot | >60% | Month 7 |
| Monthly hardware sales | 30+ units | Month 8+ |
| Logo customers | 10+ | Month 10 |
| MRR | $20K+ | Month 12 |

## Open Questions (Confidence: LOW)

1. **Can we achieve >85% accuracy with limited training data?** Need labeled weld-defect pairs. Transfer learning from published datasets may bootstrap, but real-world validation is critical.
2. **Will welders accept the device?** Shop culture is resistant to "monitoring." Must frame as "tool that helps YOU" not "system that watches YOU."
3. **Regulatory path:** Is this a "quality aid" or does it need certification as an inspection device? If the latter, timeline extends significantly.
4. **Multi-process generalization:** MIG waveforms are well-studied. TIG and Stick may require significantly different models. V1 scope should be MIG-only.
5. **Liability:** If system says "pass" and weld fails, what is our exposure? Need strong disclaimers + insurance.
