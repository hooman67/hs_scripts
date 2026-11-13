# 01_product_definition.md

## AI-Powered Thermal Inspection Tool for Trades — Product Definition

### Problem Statement

Trade professionals (electricians, HVAC technicians, home inspectors) perform thousands of visual and thermal inspections daily. The current workflow has three critical pain points:

1. **Cost barrier**: Professional thermal cameras with useful resolution cost $2,000-$13,000. Budget options ($200-$500) provide raw thermal imagery with zero interpretation, requiring expertise to read.
2. **Report drudgery**: After identifying issues, professionals spend 30-60 minutes per inspection manually writing reports with annotations, code references, and recommendations. This is unbillable time.
3. **Expertise gap**: Interpreting thermal imagery correctly requires years of training. A hot spot could be an overloaded circuit, a failing connection, or normal operation. Junior techs miss faults; senior techs are bottlenecked.

**The core insight**: The value is not in the thermal sensor (commodity at $200). The value is in the AI interpretation layer that turns raw thermal data into actionable diagnoses + formatted reports.

### Product Scope — V1

**What it IS**:
- A handheld device (or smartphone-attached module) with a FLIR Lepton 3.5 thermal sensor + visible camera
- On-device AI that classifies thermal anomalies in real-time: electrical faults (hot joints, overloaded circuits, failing breakers), moisture intrusion patterns, insulation gaps/voids
- One-tap report generation: annotated images + diagnosis + severity rating + code references + recommended action
- Offline-first (works in basements, crawlspaces, attics with no cellular signal)
- Companion mobile app for report management, client sharing, historical comparison

**What it is NOT (V1)**:
- Not a replacement for professional-grade research thermography ($10K+ cameras with 640x480 resolution)
- Not an energy audit calculator or load analysis tool
- Not integrated with inspection management platforms (Spectora, HomeGauge) in V1
- Not a diagnostic tool for gas leaks or refrigerant detection (thermal only)
- Not certified as a measurement instrument (qualitative, not quantitative)

### User Workflow

```
1. ARRIVE at job site (electrical panel, HVAC unit, building envelope)
2. POWER ON device (boots in <5 seconds, ready to scan)
3. POINT at area of interest (dual thermal+visible overlay on screen)
4. AI HIGHLIGHTS anomalies in real-time (color-coded by severity: yellow=monitor, orange=concern, red=immediate)
5. TAP anomaly for diagnosis card: "Phase B connection at 47C above ambient — likely loose termination — NEC 110.14(C) — Action: tighten and re-scan"
6. CAPTURE (one tap) — stores thermal + visible + AI annotation + metadata
7. REPEAT for all areas of interest
8. GENERATE REPORT (one tap) — PDF/HTML with all findings, organized by severity, with cover page, executive summary, detailed findings, recommendations
9. SHARE report via email/text to client, cloud backup, sync to app
```

**Time savings**: Steps 5-9 currently take 30-60 minutes manually. With AI: under 2 minutes.

### Pricing Model

| Tier | Price | Includes |
|------|-------|----------|
| **Hardware** (one-time) | $399 standard / $499 pro | Device + 30-day free trial of AI features |
| **AI Pro** (monthly) | $49/month | Unlimited AI scans + reports + cloud backup + model updates |
| **AI Pro** (annual) | $449/year ($37.40/mo) | Same as monthly, 24% savings |
| **Enterprise** | Custom | Fleet management, custom report branding, API access, priority support |

**Revenue math at scale**:
- Hardware: ~$260 COGS, ~$140 gross margin (35%) — covers acquisition cost
- SaaS: $49/month × 12 = $588/year pure software margin (90%+ gross margin)
- LTV calculation: If average customer retains 24 months = $1,176 SaaS + $140 hardware = $1,316 LTV
- Target CAC: <$200 (trade shows, distributor partnerships, referral bonuses)

### Ideal First Customer Profile

**Primary**: Independent home inspectors (US: ~100K active)
- Already use thermal cameras (25%+ own one)
- Report generation is their #1 time sink (they bill per inspection, not per hour)
- Low switching cost (no enterprise procurement)
- Price-sensitive enough to want $399 vs $2,000+ FLIR, but sophisticated enough to value AI
- Concentrated at trade shows (ASHI, InterNACHI conferences)
- Online communities are tight-knit (InspectorNation, Nachi.org forums)

**Secondary**: Electricians doing insurance/warranty inspection work
- Need documentation for compliance (NEC code references in reports)
- Often subcontract to insurance companies who demand standardized reports
- Higher volume (multiple inspections/day) = higher SaaS value

**Tertiary**: HVAC technicians
- Thermal for duct leakage, compressor diagnostics
- Seasonal business (heating season = peak demand for thermal)

### Key Risks to Product-Market Fit

| Risk | Mitigation |
|------|-----------|
| AI accuracy below 90% at launch | Start with highest-confidence fault types (hot electrical connections) where thermal signature is unambiguous. Expand categories as model improves. |
| Trades workers distrust AI | Frame as "assistant" not "replacement." Show confidence scores. Allow override/correction (which feeds back into training). |
| $49/month too expensive for solo operators | Annual discount + ROI calculator (if you save 30min/inspection at $100/hr billing rate, tool pays for itself in one inspection/month). |
| FLIR adds AI to their cameras | Ship faster (18-month window). Build data moat. Focus on report generation (FLIR's weakness). |
