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
- On-device firmware: Real-time load calculation against ASME B30.5 capacity tables
- Cloud platform: Cellular upload of load events, overload incidents, operating hours
- Fleet dashboard: Multi-crane compliance status, maintenance alerts, utilization analytics
- AI layer (v2): Anomaly detection on load patterns, predictive maintenance alerts

## User Workflow
- Installation: <2 hours by crane mechanic (bolt-on, no welding, QR-code activation)
- Daily Operation: Auto-boot, load display, yellow/red/lockout alarms, continuous logging
- Compliance: Web dashboard with OSHA inspection-ready PDF reports, automated reminders

## Pricing Model
| Tier | Hardware | Monthly SaaS | Year 1 Value |
|------|----------|--------------|--------------|
| Standard | $3,500 | $99/mo | $4,688 |
| Fleet (10+) | $2,800 | $79/mo | $3,748 |
| Enterprise (50+) | $2,500 | $59/mo | $3,208 |

## Ideal First Customer
Regional crane rental company, 30-100 cranes, Gulf Coast/Texas, 30-50% of fleet lacking compliant LMI, recently received OSHA citation or insurance premium increase.

---DOCUMENT BREAK---

/home/colligo/hs_scripts/claude/auto_research/runs/cycle_013/step5_execution/deep_research/02_competitive_analysis.md
