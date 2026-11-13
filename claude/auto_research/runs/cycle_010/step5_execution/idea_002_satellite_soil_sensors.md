# Execution Plan: Remote Dryland Farm Soil Monitoring (Satellite-Connected)

## 5a. Product Definition
**Core value proposition**: Soil moisture data for every acre — even where there's no cell signal — for $5/month per probe.
**MVP features**: (1) Hourly soil moisture + temperature readings via satellite, (2) irrigation/planting decision alerts, (3) multi-probe farm dashboard with field mapping
**Success metrics**: 95%+ message delivery in remote areas; sensor accuracy within 3% of reference; 30 farmers with 200+ total probes deployed

## 5b. Architecture
- Same as Cycle 005 livestock tags: nRF52840 + Hubble BLE-to-satellite
- Sensors: capacitive soil moisture (EC-5 equivalent, $15) + DS18B20 temp ($2)
- Power: 2x AA lithium batteries (3-year life with hourly readings + daily satellite uplink)
- Enclosure: waterproof probe housing (IP68, buried)
- Cloud + app: same AWS IoT stack as livestock tags

## 5c. BOM per probe: ~$35; sell at $200-300; plus $5/month satellite connectivity

## 5d. Timeline: Same as livestock tags (Cycle 005) — 28 weeks to field validation
- Could be developed BY THE SAME COMPANY as livestock tags (shared platform)

## 5e. Cost Estimate
- If built as extension of livestock tag platform: ~$150K incremental (sensor engineering + farm partnerships)
- If standalone: ~$300K (similar to livestock tags at $345K)
- **Recommended**: Build as second product for same satellite IoT company

## Revenue: 5000 probes × $5/month = $25K MRR = $300K ARR; plus hardware sales $200 × 5000 = $1M Year 1
