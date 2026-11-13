# Product Definition: AI Fire Sprinkler Inspection App

## Problem Statement

Fire sprinkler inspections are mandated annually for every commercial building under NFPA 25. Today, 50,000+ inspectors manually identify sprinkler head types, visually check for deficiencies (paint overspray, corrosion, obstruction, wrong temperature rating), take photos for documentation, and then spend 30-60 minutes per site writing up NFPA 25-compliant reports. This process has three failure modes:

1. **Missed deficiencies** -- Human fatigue in buildings with 500+ sprinkler heads leads to overlooked corrosion, paint contamination, and obstruction issues. A single missed deficiency can void insurance coverage and create liability.
2. **Report generation bottleneck** -- Inspectors spend 40-50% of their time on paperwork, not inspection. Report writing is the #1 complaint in industry surveys.
3. **Inconsistent quality** -- Junior inspectors lack the pattern recognition of veterans. A 2-year tech may not recognize a temperature rating mismatch in a high-heat environment. There is no scalable way to transfer expert knowledge.

**Confidence: HIGH** -- These pain points are well-documented in fire protection trade publications and confirmed by the existence of Inspect Point ($28M raised to solve the workflow/paperwork problem alone).

## Product Scope v1 (MVP)

### Core Features (Must-Have for Launch)

| Feature | Description | Technical Approach |
|---------|-------------|-------------------|
| **Sprinkler Head Identification** | Point iPad camera at sprinkler head; AI identifies type (pendent, upright, sidewall, concealed, ESFR), orientation, and manufacturer | CNN image classifier, ~50 classes |
| **Deficiency Detection** | AI flags: paint/coating on head, visible corrosion, physical obstruction within 18" clearance, leaking, missing escutcheon, wrong temperature rating for environment | Object detection + anomaly detection models |
| **Temperature Rating Verification** | Cross-reference detected head color code against room classification (kitchen, boiler room, attic, standard) | Color classification + building zone metadata |
| **NFPA 25 Report Generation** | Auto-generate inspection report with findings, photos, code references, pass/fail per device, summary for building owner | Template engine + findings → code violation mapping |
| **Offline Capability** | Full functionality without internet (model runs on-device); sync when connected | CoreML/ONNX on-device inference, background sync |

### Explicitly Out of Scope for v1

- Fire alarm system inspection
- Fire extinguisher inspection
- Scheduling/dispatch (integrate with Inspect Point or ServiceTrade instead)
- Invoicing/payments
- Customer portal
- Pipe inspection (standpipes, risers)
- Sprinkler system design/hydraulic calculations

## User Workflow

```
1. Inspector arrives at site → Opens app → Selects building from list (or creates new)
2. App loads building floor plan (if uploaded) or starts fresh inspection
3. Inspector navigates to first sprinkler zone
4. Points iPad camera at sprinkler head → AI identifies:
   - Head type & model (pendent, upright, etc.)
   - Temperature rating (via frame color)
   - Any deficiencies (paint, corrosion, obstruction, damage)
5. App shows detection overlay:
   - Green border = PASS
   - Red border + label = DEFICIENCY FOUND (e.g., "Paint contamination detected - NFPA 25 §5.2.1.1.1")
6. Inspector confirms or overrides AI finding (one tap)
7. App auto-captures photo evidence, tags with location/timestamp/GPS
8. Repeat for all heads in zone → move to next zone
9. When complete → "Generate Report" button
10. App produces NFPA 25-compliant PDF:
    - Executive summary (pass/fail count, critical findings)
    - Per-device detail with annotated photos
    - Code references for each deficiency
    - Recommended remediation timeline
11. Inspector reviews, signs digitally, sends to building owner + AHJ
```

**Key UX Principle:** The camera IS the interface. Minimize form-filling. The AI should handle identification and classification; the inspector just confirms/overrides.

## Pricing Model

| Tier | Price | Includes | Target |
|------|-------|----------|--------|
| **Solo Inspector** | $199/mo per seat | Unlimited inspections, AI detection, report generation, 5GB storage | Independent inspectors, 1-3 person shops |
| **Team** | $299/mo per seat | Everything in Solo + team management, shared building database, bulk export, API access | 5-20 inspector companies |
| **Enterprise** | $399/mo per seat | Everything in Team + SSO, custom report branding, AHJ integration, dedicated support, SLA | 20+ inspector companies, national firms |

**Revenue math at $299 avg:**
- Year 1: 500 seats = $1.79M ARR
- Year 2: 1,500 seats = $5.4M ARR (with expansion into fire alarms)
- Year 3: 4,000 seats = $14.4M ARR (multi-inspection-type platform)

**Confidence: MEDIUM** -- Pricing is benchmarked against Inspect Point (likely $200-400/user/month based on industry norms). Actual price sensitivity needs customer validation. The $299 price point assumes the AI saves inspectors 30+ minutes per site.

## Ideal First Customer Profile

### Company Profile
- **Size:** 8-25 inspectors (big enough to feel pain, small enough to adopt quickly)
- **Geography:** Single metro area in fire-prone/regulation-heavy state (California, Texas, Florida, New York)
- **Specialization:** Primarily sprinkler inspection (not alarm/extinguisher generalists)
- **Technology adoption:** Already using iPads in field (not paper-only shops)
- **Pain point:** Struggling to hire experienced inspectors; junior techs making costly mistakes
- **Revenue:** $2M-$10M annual revenue (can afford SaaS tools, motivated to optimize)

### Decision Maker
- **Title:** Operations Manager or Owner
- **Age:** 35-55
- **Motivation:** Reduce time-per-inspection to increase capacity without hiring. Reduce callbacks from missed deficiencies. Differentiate from competitors by offering AI-enhanced reports to building owners.

### Why They Buy
1. **Capacity problem:** They have more buildings to inspect than inspector-hours available. AI cuts time 30-50%, effectively adding capacity without headcount.
2. **Quality problem:** Their junior techs miss things veterans catch. AI provides a "second set of expert eyes."
3. **Differentiation:** They can show building owners annotated AI reports as proof of thoroughness vs. competitors using paper checklists.

### First 3 Target Companies (Hypothetical)
1. A mid-size fire protection company in Southern California (fire-prone, strict enforcement, tech-forward market)
2. A Texas-based inspection firm covering commercial real estate in DFW (high growth, lots of new construction requiring inspection)
3. A Florida company doing condo/HOA inspections (post-Surfside building safety regulations driving demand)

**Confidence: MEDIUM-HIGH** -- Profile is derived from industry structure. Actual company identification requires outreach and validation at NFSA events.

## Key Assumptions to Validate

| # | Assumption | Risk if Wrong | Validation Method |
|---|-----------|---------------|-------------------|
| 1 | Inspectors will trust AI findings enough to use them | Product fails completely | Ride-along with 3 inspectors, observe trust/override patterns |
| 2 | iPad camera quality is sufficient for deficiency detection | Need hardware attachment or fails | Test with iPhone 12+ and iPad Pro cameras on real sprinkler heads |
| 3 | 1,000 labeled images is enough to train accurate classifier | Need 10x more data = 6 more months | Benchmark with 500, 1000, 2000 images; measure accuracy curve |
| 4 | $299/mo price point is acceptable for 8-25 person shops | Lower price = lower margins, longer payback | Show pricing to 10 target customers, measure willingness |
| 5 | NFPA 25 report format is standardizable (not AHJ-specific) | Need per-jurisdiction templates = scope creep | Survey 5 AHJs on report acceptance criteria |
| 6 | Offline inference on iPad is fast enough (<3 sec per head) | Need cloud = connectivity dependency = deal-breaker for some buildings | Benchmark CoreML performance on iPad Air 5 / iPad Pro |
