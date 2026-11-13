# Product Definition: Smart Warehouse QC Module (mmWave Through-Package)

## Problem Statement

E-commerce shipping errors cost the industry $200B+/year globally. When a customer receives the wrong item, a damaged product, or a missing component inside a sealed package, the downstream costs are severe:

- **Return shipping**: $10-30 per incident
- **Re-pick and re-ship**: $15-50 per incident  
- **Customer churn**: 33% of customers who receive a wrong item never order again (confidence: HIGH, based on NRF/Appriss Retail reports)
- **Labor for inspection**: Manual open-and-check QC costs $0.50-2.00 per package and slows throughput by 60%+

Current solutions are inadequate:
- **Checkweighers** catch only weight-based discrepancies (~60-70% of errors) and cannot detect damage or items of similar weight
- **Camera vision** sees only the exterior -- useless for verifying sealed contents
- **X-ray** works but requires radiation safety infrastructure, trained operators, and costs $100K-500K per unit with regulatory overhead
- **Manual QC** (open, inspect, reseal) is slow, expensive, and damages packaging

**The gap**: No commercial solution exists that can non-destructively verify the contents of a sealed package at conveyor speed without radiation or regulatory burden.

---

## Product Scope v1 (MVP)

### What it does:
1. **Through-package scanning**: mmWave radar array mounted above/around conveyor belt captures 3D radar signature of sealed packages in motion
2. **AI-powered content verification**: ML model compares captured signature against known-good reference signatures for that SKU/order
3. **Pass/reject decision**: Real-time classification (correct / wrong item / damaged / missing component) with automatic diverter activation or operator alert

### What it does NOT do (v1 boundaries):
- Does not identify unknown items (it verifies against expected contents only)
- Does not read labels, barcodes, or RFID (handled by existing systems)
- Does not inspect package exterior condition (cameras handle this)
- Does not replace WMS -- integrates with existing systems via API
- Does not work for metal-encased packages (mmWave cannot penetrate metal)
- Does not provide detailed item-level imaging (provides pass/fail classification, not medical-grade imaging)

### Key constraints:
- Package material: Cardboard, corrugated, thin plastic, paper (mmWave penetrates these well)
- Package size: 6" x 6" x 4" to 24" x 24" x 18" (typical e-commerce range)
- Conveyor speed: Must handle 500-1000 packages/hour per lane (8-17 packages/minute)
- Accuracy target: >90% detection rate for wrong items, >85% for damage, <3% false positive rate

---

## User Workflow

### Onboarding (one-time per SKU category):
1. Warehouse ops team identifies top 50-100 SKUs by volume for initial enrollment
2. Each SKU is scanned 10-20 times in "known good" configuration to build reference signature
3. System auto-generates tolerance bands for each SKU category
4. Integration engineer connects scanner to customer's WMS via REST API (order manifest feed)

### Runtime (continuous operation):
1. Package arrives at scanner zone on conveyor belt
2. Barcode scanner (existing infrastructure) identifies order/SKU
3. mmWave array captures radar signature as package passes through scanning zone (~0.5-2 seconds dwell time)
4. Edge AI compares signature to reference model for that SKU
5. Decision engine outputs: PASS (green) / REVIEW (yellow) / REJECT (red)
6. PASS: Package continues to shipping
7. REVIEW/REJECT: Diverter gate activates, package routed to QC station for manual verification
8. All results logged to dashboard with confidence scores

### Dashboard (management):
- Real-time detection rates, false positive tracking
- ROI calculator (prevented returns vs. scanner cost)
- Trend analysis (which SKUs have highest error rates, which shifts)
- Model performance degradation alerts

---

## Pricing Model

### Hardware (one-time):
| Tier | Configuration | Price |
|------|--------------|-------|
| Standard | Single-lane scanner, 2 radar modules | $18,000 |
| Pro | Single-lane scanner, 4 radar modules (multi-angle) | $28,000 |
| Enterprise | Multi-lane deployment (4+ scanners), custom integration | $100,000+ |

### Software/SaaS (monthly):
| Tier | Includes | Price |
|------|----------|-------|
| Base | AI inference, basic dashboard, 500 SKU categories | $2,500/mo |
| Growth | Advanced analytics, unlimited SKUs, priority support | $4,500/mo |
| Enterprise | Custom models, dedicated CSM, SLA guarantees, multi-site | $8,000+/mo |

### Justification (ROI for customer):
- A fulfillment center shipping 50,000 packages/day with 1% error rate = 500 errors/day
- Average cost per error (return + re-ship + customer impact): $25-50
- Annual error cost: $4.5M - $9.1M
- If scanner catches 50% of errors (conservative): $2.25M - $4.55M saved annually
- Scanner cost (hardware + 1 year SaaS): ~$58K-$82K
- **ROI: 27x - 55x in Year 1** (confidence: MEDIUM -- depends on detection rate proven in pilots)

---

## Ideal First Customer Profile

### Primary target: Mid-size 3PL (Third-Party Logistics) providers
- **Revenue**: $50M-$500M annually
- **Package volume**: 10,000-100,000 packages/day
- **Pain level**: HIGH -- they are contractually liable for shipping errors to their e-commerce clients
- **Decision maker**: VP of Operations or Chief Technology Officer
- **Budget authority**: Can approve $50-100K capital expenditure without board approval
- **Technology maturity**: Already using WMS (Manhattan Associates, Blue Yonder, or similar), barcode scanners, some automation

### Why 3PLs (not direct e-commerce):
1. **Contractual liability** creates urgent pain -- they pay penalties for errors to their clients
2. **Multi-client operations** mean higher SKU variety = more error opportunities
3. **Competitive differentiation** -- a 3PL offering "guaranteed content accuracy" wins contracts
4. **Faster sales cycle** than enterprise e-commerce (Amazon, Walmart build internally)
5. **Reference-able** -- one successful 3PL deployment validates for dozens of similar companies

### Specific target companies (in order of priority):
1. **Radial (subsidiary of bpost)** -- mid-size 3PL, 20+ fulfillment centers, known for e-commerce focus
2. **ShipBob** -- tech-forward 3PL, $200M+ revenue, venture-backed, innovation-driven
3. **Whiplash (acquired by Port Logistics)** -- mid-market 3PL focused on DTC brands
4. **Quiet Logistics (acquired by Shopify)** -- robotics-forward, might pilot novel tech
5. **GXO Logistics** -- large 3PL ($9B revenue) but has innovation team that pilots new tech

### Disqualified first customers:
- Amazon (builds internally, won't buy)
- Very small fulfillment centers (<5000 packages/day -- ROI doesn't justify)
- Food/pharma (different regulatory requirements, different competitive landscape)
- Companies without existing WMS (integration too complex for v1)

---

## Key Assumptions to Validate

| Assumption | Confidence | Validation Method |
|-----------|-----------|-------------------|
| mmWave can penetrate standard corrugated cardboard | HIGH | Physics confirmed, TI reference designs demonstrate |
| mmWave can distinguish "correct item" from "wrong item" inside a box | LOW | Requires prototype testing with controlled SKU set |
| 3PLs will pay $18-28K per scanner unit | MEDIUM | Customer discovery interviews needed |
| >90% detection rate achievable for wrong items | LOW | Depends on item size, material, similarity |
| System works at conveyor speed (500+ packages/hour) | MEDIUM | TI AWR2944 fast enough, but ML inference latency TBD |
| Integration with major WMS platforms is straightforward | HIGH | REST APIs are standard |
| 3PLs have capital budget for QC infrastructure | MEDIUM | Depends on contract structures |
