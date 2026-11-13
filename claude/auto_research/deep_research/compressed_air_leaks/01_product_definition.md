# Product Definition: Continuous Compressed Air Leak Detection System

## Problem Statement

**Who has this problem**: Every manufacturing facility with a compressed air system (automotive, food & beverage, plastics, metals, textiles, packaging — essentially all discrete and process manufacturing).

**How painful**: Compressed air is the most expensive utility in a typical plant — 10x the cost of electricity per unit of work delivered. Industry data consistently shows 20-30% of compressed air is lost to leaks in a typical facility. For a mid-size plant running 3 compressors, that's $20,000-$50,000/year in wasted electricity.

**What they do today**: 
1. **Nothing** (most common) — leaks accumulate until compressors can't keep up, then maintenance gets involved
2. **Annual/quarterly surveys** using handheld ultrasonic guns ($5K-$30K devices like Fluke ii905, UE Ultraprobe, FLIR Si124) — a technician walks the plant for 1-2 days, tags leaks, generates a report. Leaks return within months.
3. **Third-party leak survey services** ($3,000-$10,000 per visit) — same as above but outsourced
4. **Energy monitoring only** — track total compressor energy but can't localize individual leaks

**Why current solutions fail**: Surveys are point-in-time snapshots. A plant fixed on Monday develops new leaks by Friday. The survey model is fundamentally reactive — it catches leaks after they've been wasting money for months.

---

## Product Scope: v1 (MVP)

### What it does (3 features max):
1. **Continuous ultrasonic leak detection** — always-on MEMS sensor nodes mounted near common leak points (fittings, valves, connections) that detect the 20-40kHz ultrasonic signature of escaping air
2. **Leak severity estimation** — ML model estimates CFM lost and translates to $/month per leak based on local energy costs
3. **Prioritized repair dashboard** — web UI showing all active leaks ranked by cost, with location mapping and repair status tracking

### What it does NOT do:
- Does NOT pinpoint leaks to centimeter accuracy (that still requires a handheld for final localization)
- Does NOT replace compressor monitoring/control systems (separate market)
- Does NOT detect gas leaks other than compressed air (no safety-rated gas detection claims)
- Does NOT require plant shutdown to install (wireless, battery-powered nodes)

---

## User Workflow (Day 1)

1. Maintenance manager orders starter kit (1 gateway + 30 sensor nodes)
2. Technician clips sensor nodes onto pipe fittings, valves, and manifolds in 2-4 hours (no wiring, no shutdown)
3. Gateway auto-discovers nodes, begins collecting ultrasonic data
4. Within 24-48 hours, dashboard shows first leak detections with estimated severity
5. Maintenance team uses prioritized list to schedule repairs during next planned downtime
6. Dashboard tracks leak-fix-verify cycle and shows cumulative savings

---

## Pricing Model

| Component | Price | Justification |
|-----------|-------|---------------|
| Sensor node (hardware) | $150 each | BOM ~$25; 6x markup covers support + margin |
| Gateway (covers 50 nodes) | $500 | LoRa concentrator + cellular backhaul |
| Starter kit (gateway + 30 nodes) | $5,000 | Discounted bundle; gets foot in door |
| SaaS subscription | $200/month per plant | Monitoring, ML updates, dashboard, alerting |

**Customer's alternative cost**: Annual leak survey = $5,000-$10,000/visit. Our system costs ~$7,400 in year 1 (hardware + 12 months SaaS) but provides CONTINUOUS monitoring vs. annual snapshot. ROI is typically 3-6 months from energy savings alone.

---

## Ideal First Customer Profile

| Attribute | Value |
|-----------|-------|
| Company size | 50-500 employees (mid-market manufacturing) |
| Industry | Automotive parts, plastics injection molding, food packaging |
| Compressed air spend | $50K-$500K/year |
| Current approach | Periodic surveys OR no leak management at all |
| Decision maker | Maintenance Manager or Plant Engineer |
| Budget authority | Can approve $5-10K without executive sign-off |
| Pain signal | "Our compressors are running at capacity but we haven't added equipment" |
| Geography | US/Canada initially (English-speaking, strong energy costs) |
