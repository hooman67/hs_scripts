# Execution Plan: AI-Powered Thermal Inspection Tool for Trade Professionals

## 5a. Product Definition

**Core value proposition**: Point, scan, know — AI instantly identifies electrical faults, moisture intrusion, and insulation gaps that human eyes miss, at 1/5th the cost of professional thermal cameras.

**Key features for MVP (max 3)**:
1. Handheld thermal+visible camera with on-device AI that automatically identifies and labels anomalies (hot spots, cold spots, moisture patterns)
2. One-tap inspection report generation (PDF with annotated thermal images, findings, recommendations)
3. Historical comparison: scan same location over time, AI flags degradation trends

**What it does NOT do**:
- Does not replace professional judgment (AI assists, human decides)
- Does not provide electrical load analysis or energy audit calculations
- Does not integrate with home inspection management software in V1

**Success metrics**:
- AI correctly identifies 90%+ of electrical hot spots, moisture intrusion, and insulation gaps
- Report generation saves 30+ minutes per inspection vs manual documentation
- 500 units sold in first 6 months to electricians and home inspectors

---

## 5b. Technical Architecture

**Hardware**:
- FLIR Lepton 3.5 thermal module (160×120, $200 at volume)
- OV5640 visible-light camera (5MP, $3)
- Allwinner H616 or Rockchip RK3566 SoC (runs Linux + TFLite)
- 4" touchscreen LCD (800×480)
- WiFi + BLE for phone sync and cloud upload
- 3000mAh Li-Po battery (4+ hours operation)
- Ruggedized enclosure (IP54, drop-rated)

**Software stack**:
- OS: Custom Linux (Buildroot)
- ML: TensorFlow Lite model for anomaly detection + classification
- App: Companion mobile app (React Native) for report generation/sharing
- Cloud: AWS (model updates OTA, report storage, fleet management)
- Training data: Thermal images of electrical faults, moisture, insulation gaps (build proprietary dataset)

---

## 5c. Bill of Materials (Per Unit at 1K volume)

| Component | Cost |
|-----------|------|
| FLIR Lepton 3.5 module | $180 |
| Application processor (RK3566) | $12 |
| Visible camera (OV5640) | $3 |
| 4" IPS LCD touchscreen | $15 |
| WiFi/BLE module | $4 |
| Battery (3000mAh LiPo) | $6 |
| Custom PCB + assembly | $20 |
| Enclosure (injection molded, IP54) | $8 |
| Misc (buttons, connectors, packaging) | $12 |
| **Total BOM** | **~$260** |

**Target retail**: $399 (standard) / $499 (pro with higher-res thermal)
**Gross margin**: 35-45%

---

## 5d. Build Instructions

1. **Weeks 1-4**: Industrial design + HW schematic (contract EE + ID firm)
2. **Weeks 3-8**: ML model training (collect/label 10K+ thermal images of electrical faults, moisture, insulation gaps from partner inspectors)
3. **Weeks 5-10**: Firmware development (camera drivers, ML inference, UI)
4. **Weeks 8-12**: Prototype assembly (10 units), initial testing with 5 trade professionals
5. **Weeks 10-14**: Mobile app + cloud backend
6. **Weeks 12-16**: Certification (FCC, CE) + DFM with contract manufacturer
7. **Weeks 16-20**: First production run (500 units)
8. **Weeks 18-24**: Launch via electrical supply distributors + direct online

---

## 5e. Validation Plan

**Key hypotheses**: (1) AI detects 90%+ of real faults (2) saves 30min/inspection (3) worth $399 to electricians

**Go/no-go**: 8/10 beta users would recommend to colleague AND reorder rate >50%

---

## 5f. Cost Estimate

| Category | Amount |
|----------|--------|
| Hardware engineering (EE + mechanical, 6 months) | $80,000 |
| ML engineer (6 months) | $90,000 |
| Firmware + app developer (6 months) | $90,000 |
| Prototype tooling + test units | $30,000 |
| ML training data collection (partner inspectors) | $15,000 |
| Certification (FCC, CE, UL) | $25,000 |
| Injection mold tooling | $30,000 |
| First production run (500 units) | $135,000 |
| Marketing + distribution setup | $30,000 |
| **Total to first revenue** | **~$525,000** |

**Monthly burn rate**: ~$60K (3 FTE + materials)
**Funding**: Pre-seed $600K. Strong fit for hardware VCs (Lemnos, Bolt, HAX).

**Revenue (Year 1)**: 2000 units × $399 = $798K hardware + $50K SaaS subscriptions = **~$848K**
