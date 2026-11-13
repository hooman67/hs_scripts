# Execution Plan: Compressed Air Leak Detection System

## 5a. Product Definition
**Core value proposition**: Find $30K/year in wasted compressed air automatically — no manual surveys, no shutdowns needed.
**MVP features**: (1) Continuous ultrasonic leak detection with location mapping, (2) Estimated leak cost in $/month, (3) Prioritized repair list with ROI per fix
**Success metrics**: Detect 90%+ of leaks >0.5 CFM; accurately estimate leak cost within 20%; 10 plants deployed

## 5b. Architecture
- Ultrasonic MEMS sensor (Knowles SPU0410LR5H, 40kHz, $3) + STM32L4 MCU ($4) + LoRa radio ($5) + battery (2-year life)
- Gateway: LoRa → WiFi/cellular → cloud
- Cloud: AWS IoT Core → ML leak classification → dashboard
- Per-node BOM: ~$25; sell at $500 (gateway separate at $300, covers 50 nodes)

## 5c. Timeline
- Weeks 1-4: Ultrasonic signal processing R&D (detect leak frequencies 20-40kHz)
- Weeks 3-8: ML model for leak detection + severity estimation + background noise rejection
- Weeks 5-10: Hardware (simple: MEMS mic + MCU + LoRa in IP54 clip-on enclosure)
- Weeks 8-12: Cloud dashboard + leak cost estimation algorithm
- Weeks 10-16: 10-plant pilot (variety: automotive, food, plastics manufacturing)
- Weeks 14-20: Commercial launch

## 5d. Cost Estimate
| Category | Amount |
|----------|--------|
| Embedded/DSP engineer (5 months) | $65,000 |
| ML engineer (4 months) | $50,000 |
| Full-stack dev (3 months) | $40,000 |
| Hardware prototyping (100 nodes + gateways) | $5,000 |
| Pilot plant partnerships | $5,000 |
| Cloud + misc | $5,000 |
| Manufacturing first batch (500 nodes) | $15,000 |
| **Total to first revenue** | **~$185,000** |

## Revenue model
- Typical plant: 30 nodes × $500 = $15K + $200/month = $2.4K/year SaaS
- Revenue Year 1: 50 plants × $15K + 50 × $200/mo × 8mo = $750K + $80K = **$830K**
- Revenue Year 2: 200 plants = $3M + recurring from Y1 = **$3.5M**

## Why this is the best idea in the portfolio
1. **Lowest capital requirement**: $185K
2. **Simplest technology**: ultrasonic mic + ML (no complex hardware)
3. **Clearest ROI**: "we found $30K/year in leaks" is irrefutable
4. **Universal market**: every factory with a compressor is a customer
5. **No regulatory barriers**: no certifications needed
6. **Recurring revenue**: monitoring is ongoing, not one-time
7. **Self-selling**: the first survey DEMONSTRATES value immediately
