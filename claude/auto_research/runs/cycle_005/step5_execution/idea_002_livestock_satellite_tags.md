# Execution Plan: Livestock GPS+Health Tags with Satellite Backhaul

## 5a. Product Definition

**Core value proposition**: Know where every animal is and how it's doing — even on the most remote ranch — for $3/month per head.

**Key features for MVP (max 3)**:
1. GPS location + movement tracking (hourly updates via satellite)
2. Accelerometer-based health alerts (calving detection, lameness, distress)
3. Web/mobile dashboard with geofencing, theft alerts, and herd overview

**What it does NOT do**:
- Does not measure body temperature or weight (requires more expensive sensors)
- Does not replace visual inspection or veterinary care
- Does not provide real-time continuous streaming (hourly updates, not live)

**Success metrics for prototype validation**:
- 95%+ message delivery rate via satellite in remote conditions
- Battery life ≥ 2 years (critical for rancher adoption)
- Calving detection accuracy ≥ 85% (accelerometer-based)
- 20 ranchers with 500+ total tags in field for 3 months

---

## 5b. Technical Architecture

**System components**:
1. Ear tag hardware: GPS + accelerometer + BLE SoC + satellite modem + battery + enclosure
2. Satellite backhaul: Hubble Network BLE-to-satellite OR Kinéis LoRa
3. Cloud backend: device management, geofencing engine, alert pipeline
4. Web + mobile app: herd dashboard, alerts, geofencing setup

**Technology stack**:
- Hardware: nRF52840 (BLE + application MCU) + u-blox MAX-M10S (GPS) + LIS2DH12 (accelerometer) + satellite modem (Hubble BLE chip OR Kinéis module)
- Firmware: Zephyr RTOS, ultra-low-power duty cycling
- Backend: AWS IoT Core → Lambda → DynamoDB → S3
- App: React Native (cross-platform)
- ML: Edge TinyML for activity classification (calving, grazing, resting, distress)

**Build vs buy**:
- GPS module: BUY (u-blox MAX-M10S, $10)
- BLE SoC: BUY (nRF52840, $5)
- Satellite connectivity: BUY (Hubble Network service or Kinéis module)
- Accelerometer: BUY (ST LIS2DH12, $1)
- Enclosure: BUILD (custom injection-molded, ear-tag form factor)
- Activity ML model: BUILD (trained on cattle behavioral data)
- Cloud/app: BUILD

**Key technical risks**:
- Battery life with GPS + satellite: mitigation = aggressive duty cycling (GPS fix every 4 hours, satellite uplink every 6 hours, wake-on-motion for alerts)
- Hubble Network coverage gaps: mitigation = dual-mode with terrestrial LoRa gateway as backup where available
- Ear tag durability (sun, rain, animal rubbing): mitigation = use proven cattle ear tag enclosure designs (follow Ceres Tag's form factor)
- Satellite uplink reliability with low-power BLE: mitigation = message queuing + retry logic in firmware

---

## 5c. Bill of Materials (Per Tag)

| Component | Supplier | Unit Cost (at 1K vol) | Notes |
|-----------|----------|----------------------|-------|
| nRF52840 BLE SoC | Nordic Semi | $4.50 | Application MCU + BLE radio |
| u-blox MAX-M10S GPS | u-blox / DigiKey | $9.00 | Ultra-low power GPS |
| LIS2DH12 accelerometer | ST Micro | $0.80 | 3-axis, ultra-low power |
| Satellite modem (Hubble BLE chip) | Hubble Network | $0.10-1.00 | BLE standard chip + Hubble firmware |
| Custom PCB (2-layer, compact) | JLCPCB | $1.50 | Flex-rigid for ear tag form |
| CR2477 coin cell battery (or custom Li-SOCl2) | Saft / Tadiran | $3.00 | 3.6V, 1000mAh, -40°C to +85°C |
| Antenna (GPS + BLE combo, chip) | Taoglas | $2.00 | Compact dual-band |
| Injection-molded enclosure (TPU) | Protolabs → China mold | $1.50 | IP68, UV-resistant, animal-safe |
| Assembly + test | Contract manufacturer | $3.00 | Per unit |
| **Total BOM per tag** | | **~$26-28** | |

**Target retail price**: $45-55/tag
**Gross margin**: ~45-50%

**Satellite connectivity cost**: $0.50-1.50/tag/month (Hubble Network pricing TBD; Kinéis ~€1/device/month)

---

## 5d. Build Instructions

1. **Weeks 1-3: Hardware Design** (EE, 1 person)
   - Schematic design: nRF52840 + GPS + accel + antenna matching
   - PCB layout optimized for ear-tag form factor (max 50mm × 35mm × 10mm)
   - Power budget analysis: target 2-year life on single battery
   - Order prototype PCBs and components

2. **Weeks 2-4: Firmware Foundation** (Embedded developer)
   - Zephyr RTOS setup on nRF52840
   - GPS driver with duty cycling (cold start optimization)
   - BLE advertising for satellite uplink
   - Power management state machine

3. **Weeks 4-6: First Prototype Assembly** (EE + mechanical)
   - Assemble 5 prototype boards
   - 3D print ear-tag enclosure mockups
   - Bench test: GPS accuracy, BLE range, current consumption
   - Validate satellite message delivery (Hubble Network dev kit)

4. **Weeks 5-8: Firmware + ML** (Embedded + ML engineer)
   - Implement activity classification (accelerometer → grazing/resting/walking/distress)
   - Develop geofence-crossing detection (on-device)
   - Implement satellite message protocol (compact binary format)
   - Power optimization: target <50µA average current

5. **Weeks 6-10: Cloud + App** (Full-stack developer)
   - AWS IoT Core device provisioning
   - Geofencing engine (server-side for complex polygons)
   - Alert pipeline (SMS/email/push for escape, calving, distress)
   - React Native app with map view + herd management

6. **Weeks 8-12: Enclosure + DFM** (Mechanical engineer)
   - Design injection-molded TPU enclosure (IP68)
   - Integrate with standard cattle ear-tag applicator
   - Drop test, UV exposure test, water immersion test
   - Source contract manufacturer for 500-unit pilot run

7. **Weeks 10-16: Field Trial** (1 person + rancher partners)
   - Deploy 50 tags across 3-5 ranches in different geographies
   - Monitor: message delivery rate, battery consumption, GPS accuracy
   - Collect accelerometer data for ML model refinement
   - Iterate on alert logic (reduce false positives)

---

## 5e. Validation Plan

**Target**: 5 ranches, 100 tags each (500 total), 3-month trial in remote areas (Montana, Texas, Australia)

**Key hypotheses to test**:
1. 95%+ satellite message delivery in open-sky ranch conditions
2. Battery lasts projected 2 years (validated via consumption measurement over 3 months)
3. Ranchers check dashboard ≥3x/week and find at least 1 actionable alert/month
4. Ranchers would pay $45/tag + $3/month/head (price sensitivity test)

**Go/no-go criteria**:
- GO: Message delivery ≥93% AND battery projection ≥20 months AND ≥4/5 ranchers want to continue AND would pay stated price
- NO-GO: Message delivery <85% OR battery projection <12 months OR <3/5 ranchers engaged

---

## 5f. Timeline & Milestones

| Week | Milestone | Decision Point |
|------|-----------|----------------|
| 3 | Hardware design complete | Power budget feasible? |
| 6 | First prototype working | GPS + satellite comms validated? |
| 8 | Activity classification working | Accuracy sufficient? |
| 10 | Cloud + app MVP functional | — |
| 12 | Injection mold enclosure finalized | DFM validated? |
| 14 | 50 pilot units manufactured | — |
| 16 | Field deployment begins | — |
| 28 | Field trial complete (3 months) | Go/no-go on commercial launch |
| 32 | First commercial batch (1000 units) ordered | — |
| 36 | Commercial launch | — |

---

## 5g. Cost Estimate

| Category | Amount |
|----------|--------|
| Hardware prototyping (50 pilot units) | $5,000 |
| PCB engineering + assembly | $15,000 |
| Injection mold tooling | $25,000 |
| Embedded firmware (6 months, 1 dev) | $90,000 |
| Full-stack developer (6 months) | $90,000 |
| Satellite connectivity (dev + pilot) | $5,000 |
| Ranch partner program (travel + support) | $20,000 |
| Hubble Network partnership/integration | $10,000 |
| Cloud infrastructure (AWS, 12 months) | $5,000 |
| Miscellaneous (tools, testing, legal) | $15,000 |
| **Total to field validation** | **~$280,000** |
| First commercial batch (1000 units mfg) | $35,000 |
| Marketing + sales launch | $30,000 |
| **Total to first revenue** | **~$345,000** |

**Monthly burn rate**: ~$45K (2 FTE + materials)

**Funding strategy**: Pre-seed/angel ($400-500K). Strong fit for ag-tech accelerators (Thrive, AgriNovus). Also eligible for SBIR Phase I from USDA.

**Revenue projection (Year 1 post-launch)**:
- 5,000 tags sold × $50 = $250K hardware
- 5,000 tags × $3/month × 8 months average = $120K recurring
- **Year 1 total: ~$370K**
