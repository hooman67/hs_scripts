# 01 - Product Definition: Precision Pollination Monitoring Radar

## Problem Statement

**Who:** California almond growers (7,600 operations covering 1.3M acres) and specialty berry growers who rent honeybee hives for pollination at $200-400/acre annually.

**How painful:** Growers spend $260M-$520M/year on pollination services in California almonds alone, yet have ZERO objective way to verify that rented hives are actively pollinating their fields. They rely on visual spot-checks (walking rows during bloom) or trust the beekeeper's word. Under-performing hives (weak colonies, diseased, poorly placed) can reduce yield by 20-40%, costing a 640-acre almond operation $128K-$256K in lost revenue per bloom season.

**What they do today:**
1. Walk rows during bloom and visually estimate bee activity (subjective, time-consuming, covers <5% of acreage)
2. Accept beekeeper's colony strength reports on faith
3. Notice only at harvest if pollination was poor (too late to remediate)
4. Some use fruit-set sampling 2-3 weeks post-bloom as a lagging indicator

## Product Scope v1

**Three features only:**

1. **Real-time pollinator flight density map** -- Radar units on poles detect and count flying insects in-field, classifying honeybees vs. other insects via micro-Doppler wingbeat signatures. Dashboard shows heat map overlaid on field map.

2. **Hive placement optimization alerts** -- Based on spatial density patterns, recommends where hives should be moved to improve coverage of under-pollinated zones.

3. **Service verification report** -- Automated daily/weekly PDF report showing pollinator activity levels per zone, timestamped, suitable for sharing with beekeepers as objective evidence of service delivery (or failure).

**What it does NOT do:**
- Does not monitor hive health (that is BeeHero's territory)
- Does not replace beekeepers or perform mechanical pollination
- Does not identify individual bees or track specific insects
- Does not provide pest detection or spray timing (v1)
- Does not integrate with farm management software (v1)

## User Workflow (Day 1)

1. **Install** -- Mount radar unit on existing irrigation pole or T-post at 3m height. Solar panel faces south. Unit auto-powers on. (15 min/unit, no wiring needed)
2. **Connect** -- Unit registers on cellular network automatically. Grower receives SMS with activation link.
3. **Configure** -- Log into web dashboard, confirm field boundaries on satellite map, mark radar unit locations. System calculates coverage zones.
4. **Monitor** -- During bloom, check dashboard 1-2x daily. View real-time insect flight density by zone. Color-coded: green (>8 bees/m^2/min), yellow (4-8), red (<4).
5. **Act** -- Receive alert if any zone drops below threshold for >2 hours during daylight. Contact beekeeper with data to request hive repositioning.
6. **Report** -- At end of bloom, download service verification report showing daily activity curves, zone coverage %, and comparison to optimal benchmarks.

## Pricing Model

| Component | Price | Justification |
|-----------|-------|---------------|
| Hardware unit | $3,995 one-time | 7.8x markup on $510 BOM. Premium for novel, zero-competition product. Comparable to weather stations ($3K-8K) that growers already buy. |
| Annual data subscription | $1,200/unit/year | Covers cellular, cloud compute, ML model updates, support. Grower pays ~$100/month during active season + maintenance. |
| Installation service (optional) | $500/unit | For growers who want professional setup. Most will self-install. |

**Unit economics per customer:** A 640-acre almond operation needs ~8-12 units for coverage (each covers ~50-80 acres at assumed 50m effective range). Total Year 1 cost: $32K-48K hardware + $9.6K-14.4K subscription = $42K-62K.

**ROI justification:** If radar-guided hive placement improves yield by even 5% on a 640-acre operation ($4,800/acre average revenue), that is $153,600 incremental revenue vs. $42K-62K investment. 2.5-3.6x Year 1 ROI.

**Problem with this model:** At 50m effective range, coverage per unit drops dramatically. If real-world range is 20-30m (more likely for bee-sized targets), a 640-acre operation would need 40+ units ($160K+), destroying the ROI argument.

## Ideal First Customer Profile

- **Operation size:** 200-800 acres of almonds in California's Central Valley (Kern, Fresno, or Stanislaus County)
- **Tech adoption:** Already uses precision ag tools (variable rate irrigation, satellite NDVI, soil sensors)
- **Pain indicator:** Has complained about pollination service quality in past 2 years OR has switched beekeepers
- **Budget:** Spends $40K-$200K annually on pollination rental
- **Decision maker:** Owner-operator or farm manager with authority to trial new technology
- **Personality:** Data-driven, willing to be an early adopter, has a relationship with their county ag extension office
