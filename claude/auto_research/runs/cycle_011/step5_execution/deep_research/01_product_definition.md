# Product Definition: AI Pallet Damage Detection Station

## Problem Statement

**Who:** Warehouse operations managers and dock supervisors at 3PLs, grocery distribution centers, and food/pharma warehouses. Secondary buyer: VP of Safety/Risk.

**How painful:** Damaged pallets cause two categories of loss:
1. **Product damage**: A broken pallet board fails during racking or transport, dropping $5K-$50K worth of product. Industry estimates suggest 2-5% of pallets in circulation have structural defects. For a facility receiving 500 pallets/day, that is 10-25 damaged pallets daily.
2. **Worker injuries**: Protruding nails and splintered wood cause puncture wounds, lacerations, and foot injuries. OSHA reports approximately 30,000 pallet-related injuries annually in the US. A single recordable injury costs $40K-$80K (direct + indirect).

**What they do today:** Manual visual inspection by forklift operators or dock workers -- typically a 2-3 second glance as the pallet passes. Detection rate is estimated at 30-50% for non-obvious defects (hairline cracks, rear-side damage, internal board weakness). Many facilities have NO formal inspection process. Some use "kick test" -- literally kicking the pallet to see if it holds.

**Quantified cost of inaction:** A mid-size DC (1,000 pallets/day) likely experiences:
- 2-4 product damage incidents/month: $10K-$200K/month
- 1-2 pallet-related injuries/quarter: $40K-$160K/quarter
- Cumulative: $200K-$800K/year in preventable losses

## Product Scope v1

### Three Core Features (and nothing else)

1. **Automated Pass-Through Inspection**: Pallets are scanned as they pass through the dock door on a forklift. No workflow change required. System captures multi-angle images and renders a pass/fail verdict in <2 seconds.

2. **Defect Classification & Evidence Capture**: Detects broken boards, protruding nails, cracks/splits, missing blocks, excessive wear, and structural warping. Captures timestamped images with defect annotations for audit trail.

3. **Alert & Routing**: Failed pallets trigger a red light + audio alert at the dock door. Dashboard shows defect type, severity, and recommended action (reject, repair, reroute to lighter loads).

### What v1 Does NOT Do

- Does NOT inspect products ON the pallet (no case/box damage detection)
- Does NOT integrate with WMS/ERP systems (v2 feature)
- Does NOT track pallets across supply chain (no RFID/barcode scanning)
- Does NOT predict remaining pallet life or recommend repair actions
- Does NOT handle load stability or overhang analysis
- Does NOT provide supplier chargeback automation

## User Workflow (Day 1)

1. **Installation (4 hours)**: Technician mounts frame over dock door opening. Attaches 3 cameras (top, left, right angles) and LED light bars. Connects to edge PC mounted on adjacent wall. Powers on.

2. **Calibration (30 minutes)**: Technician runs calibration procedure -- passes 5 known-good pallets and 5 known-damaged pallets through. System confirms detection baseline. Sets sensitivity threshold (low/medium/high).

3. **Normal operation**: Forklift operator drives pallet through dock door as usual. Zero workflow change.

4. **Detection event**: System detects damage. Red LED bar illuminates above door. Optional buzzer sounds. Forklift operator sees signal, sets pallet aside in designated reject area.

5. **Review (end of shift)**: Dock supervisor opens web dashboard on any device. Reviews flagged pallets with annotated images. Approves rejections or overrides false positives. Views daily/weekly stats.

6. **Ongoing**: System improves with feedback loop. Overridden false positives retrain the model. Sensitivity auto-adjusts to facility's tolerance level.

## Pricing Model

| Component | Price | Justification |
|-----------|-------|---------------|
| Hardware station (one-time) | $7,000 | 2x BOM ($3,500). Industry-standard 2x markup for industrial vision hardware. Comparable to IVISYS pricing tier. |
| Monthly SaaS subscription | $300/month | Covers cloud dashboard, model updates, support. Low enough to avoid procurement scrutiny (<$5K annual). |
| Installation & calibration | $1,500 | One-time. Covers technician half-day on-site. |
| Annual maintenance contract (optional) | $1,200/year | Camera cleaning, hardware replacement warranty, on-site visit. |

**Total Year 1 cost per station**: $7,000 + $3,600 + $1,500 = $12,100

**ROI justification**: If station prevents just 2 product damage incidents ($10K-$100K) or 1 injury ($40K-$80K) per year, payback period is 2-6 months. This is an easy ROI conversation.

**Alternative pricing considered but rejected:**
- Pure SaaS (camera-as-a-service): $800/month all-in. Rejected because hardware margins fund early growth and customers prefer to own physical assets.
- Per-pallet pricing ($0.02/pallet): Rejected because metering creates trust issues and revenue is unpredictable.

## Ideal First Customer Profile

**Company type**: Regional 3PL or grocery distribution center
**Size**: 10-50 dock doors, 500-2,000 pallets/day
**Geography**: Within 3-hour drive of founder's location (for on-site support during pilot)
**Key characteristics**:
- Uses whitewood (non-pooled) pallets (CHEP/PECO customers already have inspected pallets)
- Has had at least 1 recordable pallet-related injury in past 12 months
- Has a safety committee or VP of Safety role (signals they invest in safety)
- Runs refrigerated or high-value goods (higher cost of product damage)
- Does NOT have an internal ML/engineering team (eliminates DIY risk)
- Annual revenue $50M-$500M (big enough to afford it, small enough to not build internally)

**Decision maker**: VP of Operations or VP of Safety/Risk
**Champion**: Dock supervisor who is tired of dealing with broken pallet incidents
**Budget holder**: Operations or Facilities budget (not IT)
