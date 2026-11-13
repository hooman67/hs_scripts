# Product Definition: Food Processing Quality Prediction Platform

## Problem Statement

**Who:** Plant managers and quality directors at mid-market continuous food processors (dairy, beverage, meat). Secondary buyer: VP of Operations.

**How painful:** In continuous food processing, an off-spec batch discovered at end-of-line testing means:
1. **Product waste**: $10K-$100K per off-spec batch (depends on line volume and product value). A mid-size dairy plant running yogurt might produce 20,000 kg/hour. If pH drifts undetected for 45 minutes, that is 15,000 kg of product destined for disposal or downgrading.
2. **Line downtime**: Clearing, cleaning, and restarting a continuous line after an off-spec event takes 2-6 hours. At $5K-$20K/hour in lost production, downtime alone costs $10K-$120K per incident.
3. **Regulatory risk**: Food safety recalls (Listeria, Salmonella, chemical contamination) cost $10M+ per incident. Even near-misses trigger FDA scrutiny and audit burden.

**Frequency**: A typical mid-size dairy plant (5-10 production lines) experiences 3-8 off-spec events per line per month. [CONFIDENCE: MEDIUM - based on industry reports and ProcessMiner marketing claims. Actual frequency varies significantly by process maturity.]

**What they do today:**
- End-of-line lab testing (30-90 minute delay between production and results)
- Statistical Process Control (SPC) charts with manual monitoring -- operators watch temperature, pressure, pH on SCADA displays
- Fixed-threshold alarms (e.g., temperature > X triggers alert) -- binary, no prediction capability
- Periodic inline sensors (pH probes, viscometers) with no ML correlation
- Experienced operators using intuition ("that pump sounds off")

**Quantified cost of inaction:** A 5-line dairy plant with 5 off-spec events/line/month:
- Direct waste: 25 events x $20K avg = $500K/month
- Downtime: 25 events x 3 hours x $10K/hour = $750K/month
- Total: ~$15M/year in preventable losses (conservative estimate for a $200M+ revenue plant)
- Even preventing 10% of these events = $1.5M/year in savings

[CONFIDENCE: MEDIUM-HIGH on waste costs per incident; MEDIUM on frequency assumptions]

## Product Scope v1

### Three Core Capabilities (and nothing else)

1. **Universal Sensor Connector**: OPC-UA and Modbus TCP/RTU adapter that connects to existing PLCs, SCADA systems, and historians (OSIsoft PI, Wonderware). Auto-discovers available tags. Maps to unified data model. Runs on lightweight edge gateway (Raspberry Pi 4 or customer-provided industrial PC).

2. **Predictive Quality Engine**: Cloud-hosted ML models (time-series anomaly detection + multivariate regression) that learn normal process behavior per production line. Predicts probability of off-spec outcome 30 minutes before it occurs based on correlated sensor drift patterns. Retrains automatically with operator feedback.

3. **Real-Time Alert Dashboard**: Browser-based dashboard showing live process health score (0-100), predicted time-to-deviation, contributing sensor patterns, and recommended corrective actions. Push alerts via SMS, email, Slack, or SCADA integration (OPC-UA write-back for alarm panels).

### What v1 Does NOT Do

- Does NOT replace lab testing or inline quality instruments
- Does NOT provide root cause analysis or prescriptive optimization (v2)
- Does NOT integrate with ERP/MES systems (SAP, Oracle, Plex)
- Does NOT handle batch/recipe-based production (only continuous flow)
- Does NOT provide regulatory compliance documentation (FDA 21 CFR Part 11)
- Does NOT handle multi-plant aggregation or benchmarking
- Does NOT provide supply chain or incoming raw material quality prediction
- Does NOT offer offline/edge-only inference (requires cloud connectivity)

## User Workflow (Day 1 through Steady State)

### Onboarding (Week 1-3)

1. **Discovery call (Day 1-3)**: Solution engineer maps customer's production lines, identifies sensor infrastructure (PLC make/model, SCADA system, historian). Determines which lines to instrument first (highest off-spec frequency).

2. **Edge gateway deployment (Day 5-7)**: Ship pre-configured edge gateway. Customer IT or controls engineer connects to plant network. Gateway auto-discovers OPC-UA server and available sensor tags. [Requires: network access approval from customer IT -- often the longest lead time item.]

3. **Tag mapping (Day 7-10)**: Solution engineer works with customer process engineer to map sensor tags to physical meaning (T001 = pasteurizer outlet temperature, P003 = homogenizer pressure). Identify which tags correlate with quality outcomes.

4. **Baseline learning (Day 10-21)**: System ingests sensor data passively for 2 weeks. No predictions yet. ML model learns normal operating patterns, identifies correlations, establishes baseline distributions.

### Steady State Operation

5. **Prediction mode (Week 4+)**: System begins issuing predictions. Initially in "advisory mode" -- alerts go to quality manager only, not operators. Quality manager validates predictions against actual lab results. Provides feedback (correct/false alarm).

6. **Operator deployment (Week 6+)**: After validation period (target: >70% precision), alerts are exposed to line operators via dashboard + SMS/Slack. Operators receive actionable alerts: "Line 3: pH drift predicted to exceed spec in 28 minutes. Likely cause: culture feed rate variation."

7. **Continuous improvement**: Model retrains weekly with feedback. False positive rate decreases over time. System learns seasonal patterns, raw material variation, equipment degradation signatures.

## Pricing Model

| Component | Price | Justification |
|-----------|-------|---------------|
| Monthly SaaS per production line | $5,000/month | Primary revenue. Based on value delivered ($10-100K saved per prevented off-spec batch). Even 1 prevented event/month = 2-20x ROI. Comparable to InfinityQS/Sight Machine per-line pricing tiers. |
| Integration & onboarding (one-time) | $30,000 | Covers solution engineer time for discovery, tag mapping, model tuning. 2-3 weeks of effort. |
| Edge gateway hardware (one-time) | $500-$1,500 | BOM cost, near-zero margin. Raspberry Pi 4 + industrial enclosure OR customer provides own IPC. Not a profit center. |
| Annual support & maintenance | Included in SaaS | Ongoing model monitoring, retraining, connector updates. |

**Revenue per customer (Year 1 estimate)**:
- Average customer: 2 production lines
- Revenue: 2 x $5K x 12 months + $30K onboarding = $150K/year per customer
- Target: 10 lines across ~5 customers in Year 1

**Pricing positioning**: Significantly below Augury/Sight Machine ($200K-$500K+/year) but above commodity monitoring tools ($500-$2K/month). Targets mid-market processors where $60K/line/year is clearly justified by waste reduction.

**Alternative pricing considered:**
- Per-prevented-event pricing ($5K per true positive): Rejected -- hard to attribute, creates perverse incentives, unpredictable revenue
- Per-sensor-tag pricing ($100/tag/month): Rejected -- penalizes data-rich environments, misaligned with value
- Freemium monitoring with premium prediction: Rejected -- gives away too much, hard to convert

## Ideal First Customer Profile

**Company type**: Regional dairy processor or mid-size beverage bottler
**Revenue range**: $50M-$500M annual revenue (big enough to afford $150K/year, small enough to lack internal ML team)
**Production**: 2-10 continuous processing lines
**Geography**: US or Western Europe (strong food safety regulations create urgency)

**Key characteristics**:
- Runs continuous (not batch) production -- fluid processing, not discrete/portioned
- Uses modern PLCs with OPC-UA capability (Rockwell ControlLogix, Siemens S7-1500, Schneider M340+)
- Has a historian (OSIsoft PI, Wonderware, Ignition) -- proves data maturity
- Experiences 3+ off-spec events per month per line (high enough pain to justify investment)
- Has a quality manager or process engineer on staff (someone to champion the tool)
- Does NOT have an internal data science team (eliminates DIY risk)
- Is NOT owned by a top-10 food conglomerate (Nestle, Danone, etc. -- they build internally)
- Has at least one recent quality incident that cost >$100K (creates budget urgency)

**Decision maker**: VP of Operations or VP of Quality
**Champion**: Quality Manager or Senior Process Engineer
**Budget**: Operations or quality budget (NOT IT -- avoid IT procurement gatekeeping)
**Sales cycle**: 3-6 months (shorter than enterprise: $150K/year is within VP-level authority at most mid-market food companies)

**Dream first customer**: A 4-line dairy yogurt plant doing $150M in revenue, experiencing 20+ off-spec events/month, using Rockwell PLCs with an OSIsoft PI historian, with a quality director who has been asking for "predictive analytics" but has no ML team. Located within driving distance for on-site support during pilot.
