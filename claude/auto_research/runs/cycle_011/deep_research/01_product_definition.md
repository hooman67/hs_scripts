# Product Definition: IoT Bolt Tension Monitor for Wind Turbines

## Problem Statement

Wind turbines have 100-300+ critical bolted connections (tower flange, blade root, yaw bearing, main bearing housing). These bolts experience continuous cyclic loading from wind, thermal expansion, and vibration. When bolts loosen and fail, consequences range from:

- **Minor**: Unplanned maintenance visit ($5K-$50K per climb, $200K+ offshore)
- **Major**: Tower section separation, blade throw, nacelle collapse ($3-10M per event)
- **Catastrophic**: Adjacent turbine damage, grid instability, potential fatalities

**Current practice** is periodic manual inspection: technicians climb the tower (or rappel) every 6-12 months, use ultrasonic handheld devices or torque wrenches to spot-check a subset of bolts. This means:
- 80%+ of bolts are never checked between inspections
- Failures between inspection intervals are undetectable
- Offshore turbines cost $50K-$200K per inspection visit (vessel + crew)
- Manual measurements are operator-dependent (10-20% variance)

**The gap**: No commercially available system provides continuous, automated, per-bolt tension monitoring for wind turbines at an economically viable price point.

**Confidence: HIGH** -- bolt failures in wind turbines are well-documented in industry literature (NREL, DNV standards), and the inspection cost/limitation problem is universally acknowledged by O&M providers.

---

## Product Scope: Version 1.0

### Hardware Layer
| Component | Function | Target Cost |
|-----------|----------|-------------|
| Strain gauge washer | Measures bolt clamping force via deformation | $20/unit |
| Wireless sensor node | A/D conversion, local processing, LoRa radio | $30/unit |
| Tower-level gateway | Aggregates data from ~150 nodes, cellular uplink | $500/unit |
| Installation kit | Calibration tool, adhesive, weatherproofing | $10/bolt |

**Per-turbine hardware cost**: ~$8,000-$15,000 (80-150 monitored bolts depending on tier)

### Software Layer
- Cloud ingestion (time-series database)
- Real-time alerting (tension drop below threshold)
- Dashboard (fleet view, turbine view, bolt-level view)
- Trend analysis (seasonal patterns, degradation curves)
- API for integration with existing SCADA/CMMS systems

### V1 Exclusions (future roadmap)
- Predictive ML models (requires 12+ months of failure data)
- Automated work order generation
- Digital twin integration
- Offshore-specific hardware variant (IP68, marine-grade)
- Blade root monitoring (higher vibration environment)

---

## User Workflow

### Installation (One-time, ~4 hours per turbine)
1. During scheduled maintenance window, technician removes existing bolt
2. Places strain gauge washer under bolt head (or nut)
3. Re-torques bolt to specification
4. Snaps wireless node onto washer (magnetic/clip mount)
5. Calibrates node against known torque value
6. Gateway installed in tower base (power from existing 24V rail)
7. Gateway auto-discovers nodes, confirms connectivity

### Operations (Continuous)
1. Each node samples bolt tension every 15 minutes (configurable)
2. Data transmitted to gateway via LoRa (sub-GHz, penetrates steel tower)
3. Gateway batches and uploads to cloud every hour
4. Alerts triggered if: bolt tension drops >15% from baseline, rate-of-change exceeds threshold, or communication lost >24h
5. O&M team receives alert via email/SMS/SCADA integration
6. Dashboard shows which specific bolts need attention, with priority ranking

### Reporting (Monthly)
- Fleet health summary
- Bolts approaching intervention threshold
- Maintenance planning recommendations
- Compliance documentation for insurers/regulators

---

## Pricing Model

### Tier 1: Essential (target independent operators)
- **$150/turbine/month** (annual contract)
- Monitoring up to 80 critical bolts per turbine
- Real-time alerts
- Basic dashboard
- Monthly reports

### Tier 2: Professional (target large fleet operators)
- **$200/turbine/month** (annual contract)
- Monitoring up to 150 bolts per turbine
- SCADA/CMMS integration
- Custom alert thresholds
- Quarterly on-site review
- Insurance documentation package

### Tier 3: Enterprise (target offshore/premium)
- **$350/turbine/month** (annual contract)
- Full bolt coverage (200+ points)
- Predictive analytics (when available)
- Dedicated support engineer
- SLA: <1h alert latency

### Hardware
- Sold at cost or slight margin ($80-$120/bolt installed)
- OR leased as part of monthly fee (higher monthly, lower upfront)
- Gateway included in service fee

### Unit Economics (at scale)
- Hardware COGS: ~$50/bolt (including washer, node, share of gateway)
- Cloud/software cost: ~$5/turbine/month
- Support cost: ~$15/turbine/month
- **Gross margin at $200/mo: ~75-80%** (after hardware payback in month 8-12)

---

## Ideal First Customer Profile

### Primary Target: Mid-size Independent Wind Farm Operator

**Characteristics:**
- Owns/operates 50-200 turbines (onshore)
- Turbines aged 8-15 years (past warranty, bolt fatigue risk increasing)
- No existing OEM service contract (or expensive one they want to replace)
- Has experienced at least one bolt-related incident or near-miss
- Located in US (Texas, Iowa, Oklahoma, California) for logistics
- EBITDA-positive, spending $50K-$100K/turbine/year on O&M

**Why they buy:**
- Direct ROI argument: $200/mo/turbine vs. $3-10M potential collapse
- Reducing unplanned maintenance visits (each costs $5K-$20K onshore)
- Insurance premium reduction potential (5-15% with continuous monitoring data)
- Extending turbine lifespan from 20 to 25-30 years (bolt integrity is key constraint)
- Regulatory compliance (growing requirements for structural monitoring)

**Named targets (US):**
1. **Invenergy** -- largest independent wind operator in US, 12,000+ MW, no OEM affiliation
2. **NextEra Energy Resources** -- massive fleet, data-driven culture
3. **Avangrid Renewables** -- 8,000+ MW, aging Gamesa fleet
4. **EDP Renewables** -- growing US presence, receptive to innovation
5. **Pattern Energy** -- mid-size, technology-forward reputation

**Why NOT start with OEMs:**
- OEMs (Siemens Gamesa, GE, Vestas) have long procurement cycles (18-36 months)
- They may view bolt monitoring as something they should build internally
- They control the customer relationship and could squeeze margins
- Better to build installed base with independents, then negotiate OEM partnerships from strength

---

## Key Assumptions & Risks (Product Definition)

| Assumption | Confidence | Mitigation |
|------------|-----------|------------|
| Strain gauge washer survives 20-year turbine life | MEDIUM | Accelerated life testing in first 6 months |
| LoRa signal penetrates tower steel reliably | MEDIUM | May need repeater nodes or slot antenna design |
| 15-min sampling interval sufficient for safety | HIGH | Failure modes develop over hours/days, not seconds |
| Operators will allow hardware installation on bolts | MEDIUM | Pilot agreement + insurance backing |
| $200/mo price point acceptable | HIGH | Well below insurance deductible for one incident |
| 80 bolts per turbine is minimum viable coverage | MEDIUM | Need DNV/turbine OEM input on critical bolt map |

---

## Success Metrics (First 12 Months)

1. **Pilot deployed**: 5 turbines, 400+ bolts monitored continuously for 3+ months
2. **Zero false-positive tower evacuations** (alert precision >95%)
3. **At least 1 genuine bolt degradation detected** (proving value)
4. **3 paying customers** signed (not just pilot partners)
5. **Insurance partner** engaged (LOI from insurer for premium reduction program)
6. **Hardware MTBF** demonstrated: >50,000 hours (no node failures in pilot)
