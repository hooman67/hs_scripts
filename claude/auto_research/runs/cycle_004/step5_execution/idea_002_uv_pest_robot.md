# Execution Plan: Autonomous UV-C Pest Control Robot Fleet

## 5a. Product Definition

**Core value proposition**: Chemical-free pest control for high-value crops — autonomous robots patrol fields at night, killing insects and fungal spores with calibrated UV-C light, eliminating pesticide costs while enabling organic certification.

**Key features for MVP (max 3)**:
1. GPS-RTK guided autonomous robot that navigates between crop rows at night applying UV-C to foliage
2. Pest-specific UV dosing protocols (intensity + duration calibrated per pest species and crop type)
3. Fleet management dashboard showing coverage maps, pest pressure data, and treatment history

**What it does NOT do**:
- Not herbicide/weed control (focused on PEST insects and fungal disease)
- Not harvesting or any other farm task (single-purpose tool)
- Not indoor/greenhouse (outdoor field deployment)
- Not daytime operation (UV-C is most effective and safest at night)

**Success metrics**:
- 80%+ pest reduction in treated rows vs untreated control rows
- Cover 10+ acres per robot per night
- Zero pesticide use on treated acreage while maintaining yield
- 3+ commercial grower deployments in first season

---

## 5b. Technical Architecture

```
[GPS-RTK Base Station] → [Robot: Navigation Controller] → [Drive Motors (4WD skid-steer)]
                                                                    ↓
[Fleet Dashboard (Cloud)] ← [Cellular Modem] ← [Main Computer] → [UV-C Array Controller] → [UV-C LED Panels]
                                                                    ↓
                                                        [Safety Sensors (PIR, LiDAR)] → [Auto-shutoff if person detected]
```

**Technology stack**:
- **Navigation**: RTK-GPS (±2cm accuracy) + LiDAR for obstacle avoidance (Velodyne Puck Lite or Ouster OS0)
- **Drive platform**: 4WD skid-steer chassis with adjustable width for row spacing (custom or modified Clearpath Jackal)
- **UV-C source**: High-power UV-C LED arrays (265nm peak, ThorLabs/Nichia LEDs) with reflectors directing light onto foliage
- **Dosing control**: Adjustable intensity + speed based on pest type lookup table; camera for crop row following
- **Safety**: PIR motion sensors + perimeter detection; instant shutoff if human/animal detected; physical key lockout
- **Compute**: Raspberry Pi 5 or Jetson Nano for navigation; cellular for fleet reporting
- **Power**: 48V LiFePO4 battery pack (5-8 kWh for 8-hour operation)

**Build vs. Buy**:
| Component | Decision | Rationale |
|-----------|----------|-----------|
| UV dosing protocols | BUILD | Core IP — species-specific kill curves |
| Navigation/autonomy | BUY + INTEGRATE | ROS2 + RTK-GPS, well-solved |
| UV-C LED arrays | BUY + DESIGN | LED modules are commodity; array geometry is custom |
| Chassis/drivetrain | BUY (modify) | Clearpath or AgriBot base platform |
| Fleet management software | BUILD | Simple but differentiating |
| Safety system | BUILD | Critical for liability; must be robust |

---

## 5c. Bill of Materials / Resources

### Hardware per Robot

| Item | Cost |
|------|------|
| 4WD chassis + motors + controller | $8,000 |
| RTK-GPS module (u-blox F9P + base station amortized) | $1,500 |
| LiDAR (Ouster OS0-32 or similar) | $3,000 |
| UV-C LED arrays (custom, 500W total) | $4,000 |
| LiFePO4 battery (48V, 100Ah) | $3,000 |
| Main computer + cameras | $1,000 |
| Cellular modem + safety sensors | $500 |
| Enclosure, wiring, connectors | $2,000 |
| **Total per robot** | **~$23,000** |

### Development (12 months)

| Item | Cost |
|------|------|
| Prototype robots (3 units) | $69,000 |
| UV dosing R&D (controlled experiments) | $30,000 |
| University partnership (entomology lab) | $20,000 |
| Field trial costs (land lease, crop purchase) | $25,000 |
| Cloud infrastructure (fleet management) | $10,000 |

### Personnel

| Role | Count | Annual Cost |
|------|-------|-------------|
| Robotics engineer (navigation + autonomy) | 1 | $165,000 |
| Agricultural scientist / entomologist | 1 | $120,000 |
| Electrical engineer (UV arrays + power) | 1 | $155,000 |
| Software engineer (fleet management) | 1 | $160,000 |
| CEO / sales (farming relationships) | 1 | $130,000 |
| **Total** | 5 | **$730,000** |

---

## 5d. Build Instructions (abbreviated)

**Phase 1 (Months 1-4)**: UV dosing research
- Partner with university entomology lab
- Establish kill curves: UV-C intensity × duration for target pests (spider mites, aphids, whitefly, botrytis)
- Validate: which pests are UV-susceptible at practical dose levels?
- **Gate**: Can we kill target pests with UV-C exposure achievable in a single pass?

**Phase 2 (Months 3-7)**: Robot prototype
- Build autonomous platform (chassis + navigation + UV array)
- Achieve reliable row-following and coverage
- Integrate safety system (human detection → instant shutoff)
- **Gate**: Robot covers 10 acres overnight autonomously?

**Phase 3 (Months 6-12)**: Field trials
- Deploy 3 robots at partner farm (California strawberries or similar)
- Run controlled trial: treated rows vs untreated rows
- Measure pest counts, crop yield, quality
- **Gate**: 80%+ pest reduction with maintained yield?

---

## 5g. Cost Estimate

| Category | Cost |
|----------|------|
| Personnel (12 months) | $730,000 |
| Prototype hardware (3 robots) | $69,000 |
| UV dosing R&D | $30,000 |
| University partnership | $20,000 |
| Field trial operations | $25,000 |
| Cloud/software infrastructure | $10,000 |
| Travel, conferences | $20,000 |
| Insurance/legal | $30,000 |
| Contingency (15%) | $140,000 |
| **Total to validated field results** | **~$1.07M** |

**Revenue model**: Pest-control-as-a-service: $800-1500/acre/season
**Unit economics**: Robot covers 10 acres/night × 180-night season = 1800 acre-treatments. At $1000/acre = $1.8M revenue per robot per season. Cost per robot: $23K + $10K/year maintenance = exceptional ROI.
**Target**: 20 robots Year 2, serving 200+ acres = $200K+ revenue growing to 100 robots / $1.8M by Year 3.
