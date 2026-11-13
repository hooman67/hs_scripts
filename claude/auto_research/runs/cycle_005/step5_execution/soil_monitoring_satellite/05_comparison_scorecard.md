# Comparison Scorecard: Remote Dryland Farm Soil Monitoring (Satellite)

## Scoring Criteria (1-10 scale, 10 = best)

| Criterion | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Capital Required | 15% | 7 | 1.05 | $300K is achievable for angel/pre-seed. Hardware adds cost vs. pure SaaS but BOM is low ($25/unit). Shared architecture with livestock tags reduces if built second. Deducted because hardware always has unexpected costs. |
| Time to Revenue | 15% | 5 | 0.75 | ~10 months to first revenue. Hardware prototype + field pilot + manufacturing = slower than SaaS (3-4 months). Hubble Network dependency could add delays beyond our control. |
| Moat Strength | 15% | 4 | 0.60 | Connectivity moat is REAL but TEMPORARY (2-4 years). Once Lacuna/Myriota/Starlink IoT commoditize satellite-IoT, the moat is gone. Sensor tech is commodity. Long-term moat requires data/agronomic intelligence layer that does not exist yet. Hubble relationship is not exclusive. |
| Technical Risk | 10% | 6 | 0.60 | Moderate. Sensor tech is proven. BLE is proven. Satellite connectivity via Hubble is the SINGLE unproven element. If Hubble works, technical risk is low. If Hubble fails, product cannot exist. Binary risk profile. |
| Market Size | 10% | 8 | 0.80 | Dryland farms = 80% of global agriculture. Even 1% penetration in Australia alone = 10,000+ farms. Addressable market estimated at $500M+ globally for soil monitoring in connectivity-dark regions. Massive unserved demand. |
| Founder-Market Fit | 15% | 5 | 0.75 | Cloud/ML skills match software layer (40% of work). Hardware design and agricultural domain are significant gaps requiring co-founder or senior contractor. Not a natural fit but not impossible. Rises to 7/10 if livestock tags are built first (shared platform). |
| Customer Accessibility | 10% | 6 | 0.60 | Australian farmers are reachable through GRDC, field days, agronomists. Not as accessible as software developers or IT teams. Requires physical presence, trust-building, agricultural credibility. Carbon credit companies are more accessible (B2B, fewer decision makers). |
| Scalability | 10% | 7 | 0.70 | Once hardware is designed and manufacturing is set up, scaling to 10K-100K units is straightforward (contract manufacturing). Software/cloud scales naturally. Geographic expansion requires only Hubble coverage (no local infrastructure). Limitation: physical product = inventory/logistics complexity vs. pure SaaS. |

---

## Weighted Total: 5.85 / 10

---

## Score Context

| Rating | Interpretation |
|--------|---------------|
| 8-10 | Exceptional opportunity, strong alignment |
| 6-8 | Good opportunity, manageable gaps |
| 4-6 | Conditional opportunity, significant gaps or dependencies |
| 2-4 | Weak opportunity, major structural issues |
| 0-2 | Non-viable |

**This idea scores in the "conditional opportunity" range**, primarily dragged down by:
- Weak long-term moat (4/10)
- Moderate founder-market fit (5/10)
- Slower time to revenue vs. software plays (5/10)

---

## Key Strengths

1. **Massive underserved market**: The gap between "farms that need monitoring" and "farms that can get monitoring" is enormous. Every competitor confirmed cellular-only. This is not a theoretical gap — it is a verified, quantifiable one.

2. **Shared platform economics**: If livestock tags are built first, 70% of the engineering (firmware, Hubble integration, cloud backend, app) is reusable. The incremental cost to add soil probes drops from $300K to ~$80-100K.

3. **Low BOM, high margin**: $25 BOM selling at $99 + $5/month recurring is healthy unit economics. Hardware is simple (no GPS, no accelerometer, no complex enclosure) compared to livestock tags.

4. **Multiple value propositions**: Soil moisture for planting decisions + carbon credit documentation + insurance verification. If one angle fails, others may succeed.

5. **Geographic land-grab**: First mover in connectivity-dark regions (Australian outback, African dryland, Central Asia) builds distribution and brand before satellites become commodity.

---

## Key Weaknesses

1. **Single dependency on Hubble Network**: If Hubble fails, pivots, or does not cover target geographies, there is no product. No cheap mitigation exists — switching to Myriota/Kineis means adding a $30-50 proprietary module, destroying the cost advantage.

2. **Temporary moat**: The connectivity differentiation has a 2-4 year shelf life. After that, any sensor maker can add satellite via Lacuna/Myriota/commodity modules. Must build durable advantages (data, brand, distribution) in that window.

3. **Dryland demand uncertainty**: The #1 proven value of soil moisture data is irrigation scheduling. Dryland farms DO NOT IRRIGATE. Alternative value props (planting timing, grazing rotation, carbon credits) are logical but UNVALIDATED. This is the biggest unknown.

4. **Hardware + agriculture = slow + unfamiliar**: For a software-background founder, this requires learning two new domains simultaneously (hardware engineering + agricultural sales). Each alone is hard; both together multiply the challenge.

5. **Myriota already exists**: A well-funded ($50M+) Australian company already offers satellite-IoT for agriculture. They have a 3-5 year head start in satellite operations and agricultural partnerships. They are the obvious acquirer — or killer.

---

## Comparison to Other Ideas in Portfolio

| Criterion | Soil Monitoring (Satellite) | Livestock Tags (Satellite) | Laser Cutting Optimization (SaaS) |
|-----------|---------------------------|---------------------------|-----------------------------------|
| Capital Required | $300K | $345K | $200K |
| Time to Revenue | 10 months | 9 months | 4 months |
| Moat Strength | 4/10 (temporary) | 4/10 (temporary) | 7/10 (network effects) |
| Technical Risk | 6/10 | 5/10 (more complex HW) | 8/10 (low) |
| Founder Fit | 5/10 | 5/10 | 9/10 |
| Weighted Score | 5.85/10 | 5.7/10 | 7.8/10 |

**Verdict**: Soil monitoring is a viable product EXTENSION of the livestock tags platform (shared architecture, shared Hubble relationship, shared manufacturing). As a STANDALONE first product for this founder, it scores below pure-software alternatives. Best deployed as Product #2 after tags validate the Hubble connectivity layer.

---

## Go / No-Go Recommendation

**CONDITIONAL-GO as Product #2 on a shared platform.**

**GO conditions**:
1. Livestock tags validate Hubble connectivity first (de-risks the fatal dependency)
2. Customer validation yields 3+ signed pilot LOIs within 8 weeks of outreach
3. Hubble confirms coverage over Western Australia by deployment date

**If building standalone (without livestock tags first)**: Scored at 5.85/10, this is below the 6.5 threshold for a confident GO. The Hubble dependency risk + demand uncertainty + founder-fit gaps create too many simultaneous unknowns for a solo venture. Would need to see very strong demand signals (>5 LOIs) to override.
