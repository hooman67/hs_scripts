# Execution Plan: Sound-Based Tool Wear Detection for CNC Shops

## 5a. Product Definition
**Core value proposition**: Hear tool problems before they become expensive failures — $200 per machine, not $50K.
**MVP features**: (1) Real-time tool wear scoring (green/yellow/red), (2) breakage prediction alerting, (3) historical trend dashboard
**Success metrics**: Detect 90%+ of tool failures ≥30 seconds before breakage; 20 machines monitored in beta

## 5b. Architecture
- MEMS microphone array (3x ICS-43434, $1 each) + STM32 MCU + WiFi → cloud ML inference
- Cloud: AWS Lambda + SageMaker for per-machine model training
- Dashboard: React web app with real-time alerts (email/SMS/machine integration)

## 5c. BOM per unit: ~$50 (mics + MCU + enclosure + WiFi); sell at $200 + $200/month SaaS

## 5d. Timeline
- Weeks 1-6: Collect acoustic data from 5 partner CNC shops (various machines/tools/materials)
- Weeks 4-10: Train ML models for tool wear classification per machine type
- Weeks 8-14: Build hardware (simple: mic array + MCU + WiFi in IP54 box)
- Weeks 10-16: Cloud backend + dashboard + alerting
- Weeks 14-20: 20-machine beta with 5 shops
- Weeks 18-24: Commercial launch

## 5e. Cost Estimate
- ML engineer (6 months): $90K
- Embedded engineer (4 months): $50K
- Full-stack dev (4 months): $50K
- Hardware prototyping (50 units): $5K
- Shop partnerships + travel: $10K
- Cloud + misc: $10K
- **Total: ~$215K to first revenue**

## Revenue projection: 500 machines × $200/month = $100K MRR within 18 months = **$1.2M ARR**
