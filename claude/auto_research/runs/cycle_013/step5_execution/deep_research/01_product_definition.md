# Product Definition: AI-Powered Crane Load Monitoring Retrofit

## Problem Statement

**The core pain:** 150,000+ cranes in the US lack modern Load Moment Indicators (LMI) due to age (pre-2015 manufacture) or system failure. Replacing an LMI costs $15,000-$50,000 from incumbents (PAT/Hirschmann, Trimble, Rayco-Wylie), creating a perverse incentive to operate without compliant monitoring.

**Why now:**
1. OSHA 1926.1416 mandates LMI on cranes >6,000 lbs (manufactured after Nov 8, 2010). As these cranes age, OEM systems fail and replacement costs are prohibitive.
2. OSHA enforcement actions increased 23% YoY (2023-2025). Average citation for crane safety violations: $15,625 per instance (serious violation), up to $156,259 for willful violations.
3. Insurance carriers increasingly require load monitoring data for crane liability policies. No monitoring = higher premiums or denial of coverage.
4. Crane rental companies face fleet-wide compliance burden with no affordable solution.

**Who feels it most:** Regional crane rental companies (50-200 unit fleets) with mixed-age equipment. They face the choice of: (a) $20-40K per crane to retrofit with incumbent LMI, (b) remove older cranes from fleet (lost revenue), or (c) risk OSHA citations and liability exposure.

**Confidence: HIGH** - OSHA regulations are public record. Crane fleet demographics from ACT Research and industry associations confirm aging fleet.

---

## Product Scope v1 (MVP)

### Hardware Kit
| Component | Function | Target BOM |
|-----------|----------|-----------|
| Wireless load cell (tension-link or shackle type) | Measures line pull force | $500 |
| Boom angle sensor (MEMS inclinometer) | Measures boom angle for load chart lookup | $80 |
| Boom length sensor (ultrasonic or wire-draw) | Measures telescoping boom extension | $120 |
| MCU gateway (ESP32-S3 + cellular modem) | Processes sensor data, runs load chart logic, transmits to cloud | $150 |
| Ruggedized wireless display (7" IP67) | Shows operator load %, warnings, capacity | $200 |
| Wiring harness + mounting brackets | Crane-specific mounting kits (3-5 crane families initially) | $150 |
| **Total BOM** | | **~$1,200-$1,500** |

### Software/Cloud
- **On-device firmware**: Real-time load calculation against programmed load charts (ASME B30.5 capacity tables). Audio/visual alarms at 75%/90%/100% of rated capacity.
- **Cloud platform**: Cellular upload of load events, overload incidents, operating hours. Automatic generation of OSHA-compliant inspection records.
- **Fleet dashboard**: Multi-crane view for rental company owners/safety managers. Compliance status, maintenance alerts, utilization analytics.
- **AI layer (v2)**: Anomaly detection on load patterns, predictive maintenance alerts, operator behavior scoring.

### What v1 Does NOT Include
- Full anti-two-block (A2B) system (separate product, different sensors)
- Crane-to-crane collision avoidance
- Operator certification/training platform
- Integration with construction management software (Procore, etc.)

---

## User Workflow

### Installation (Target: <2 hours by crane mechanic, no factory training)
1. Mount wireless load cell on hook block or boom tip sheave (bolt-on, no welding)
2. Attach boom angle sensor to boom base section (magnetic mount + safety wire)
3. Install boom length sensor on telescoping section (wire-draw encoder)
4. Mount MCU gateway box in operator cab (DIN rail or magnetic)
5. Mount wireless display in cab (suction cup or bracket)
6. Power gateway from crane 12V/24V electrical system
7. Activate via phone app: scan QR code, select crane model, verify sensor readings
8. Run calibration lift (known weight at known radius) -- system self-calibrates

### Daily Operation
1. Operator turns on crane -- system auto-boots, runs self-check
2. Display shows: current load (lbs/tons), rated capacity at current radius, % utilization
3. Yellow warning at 75% capacity, red alarm + buzzer at 90%, lockout recommendation at 100%
4. All load events logged continuously via cellular (or buffered if no signal)
5. Overload events flagged immediately to fleet manager via SMS/email

### Compliance/Reporting
1. Fleet safety manager logs into web dashboard
2. Views compliance status: green/yellow/red for each crane
3. Downloads OSHA inspection-ready reports (daily load logs, overload events, annual inspection records)
4. Receives automated reminders for annual crane inspection deadlines
5. Shares reports with insurance carrier for premium discount

---

## Pricing Model

| Tier | One-Time Hardware | Monthly SaaS | Annual Value |
|------|------------------|--------------|--------------|
| **Standard** (single crane) | $3,500 installed | $99/mo | $4,688/yr first year |
| **Fleet** (10+ cranes) | $2,800 installed | $79/mo | $3,748/yr first year |
| **Enterprise** (50+ cranes) | $2,500 installed | $59/mo | $3,208/yr first year |

**Comparison to alternatives:**
- Incumbent LMI retrofit: $20,000-$40,000 one-time (no cloud/SaaS)
- OSHA serious violation: $15,625 per instance
- Crane accident average cost: $750,000-$2M (property + injury + downtime)
- Annual insurance premium reduction with monitoring: estimated $500-$2,000/crane

**Revenue model split (at scale):**
- 60% hardware (one-time, declining margin pressure over time)
- 40% SaaS (recurring, high-margin, grows with fleet)

**Confidence: MEDIUM** - BOM costs are estimated from component distributor pricing (Digi-Key, Mouser, Alibaba). Selling price validated against incumbent pricing. SaaS willingness-to-pay needs customer validation.

---

## Ideal First Customer Profile

### Primary: Regional Crane Rental Company

**Demographics:**
- Fleet size: 30-100 cranes (large enough to feel compliance pain, small enough to lack in-house engineering)
- Geography: Texas, Gulf Coast, Southeast US (high construction activity, aggressive OSHA regions)
- Crane types: Rough terrain, truck-mounted hydraulic (most common rental types)
- Revenue: $5M-$50M annually
- Pain: 30-50% of fleet lacks compliant LMI, facing $500K+ to retrofit all with incumbent systems

**Decision maker:** VP of Safety / Fleet Manager (not the crane operator)

**Why they buy:**
1. Avoid $15K+ per instance OSHA citations (fleet of 40 non-compliant cranes = $600K+ exposure)
2. Reduce insurance premiums (carriers increasingly mandating monitoring)
3. Competitive advantage: can rent cranes with "OSHA-compliant monitoring included" badge
4. Fleet visibility: know where cranes are, how they are being used, when maintenance is due

**Named target companies (public information):**
1. Maxim Crane Works (largest US rental, 2,500+ cranes -- enterprise deal)
2. ALL Family of Companies (largest privately held, 3,500+ units)
3. Bigge Crane (West Coast, 1,500+ units)
4. Sterling Crane (Midwest/Gulf, 300+ units)
5. TNT Crane & Rigging (Texas/Gulf, 200+ units)

**Realistic first customer:** A mid-size regional player (50-200 cranes) who has recently received an OSHA citation or insurance premium increase. They are actively looking for solutions but cannot justify $20K+ per crane for incumbent LMI systems.

### Secondary: Steel Erection Contractors

- Own 5-20 cranes for structural steel work
- OSHA Subpart R (Steel Erection) has specific crane requirements
- Smaller buying centers, faster decision cycles
- Good for early pilots and testimonials

**Confidence: MEDIUM-HIGH** - Fleet demographics from Crane & Rigging Hot Line magazine, ACT Research. OSHA citation data is public record. Specific company willingness-to-pay needs validation.
