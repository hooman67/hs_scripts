# Product Definition: Remote Dryland Farm Soil Monitoring (Satellite)

## Problem Statement

80% of global agricultural land is dryland (rain-fed, non-irrigated). The majority of these farms lack cellular coverage, making existing precision agriculture tools — which universally require cellular connectivity — unusable. Farmers on these lands make planting, grazing rotation, and harvest timing decisions blind to actual soil moisture conditions.

**The specific pain**: A dryland wheat farmer in Western Australia, sub-Saharan Africa, or the Texas Panhandle cannot answer "how much moisture is in my soil at depth?" without physically driving out and taking manual readings. This leads to:
- Planting into soil too dry to germinate (crop failure)
- Overgrazing pastures before moisture recovery
- Missing optimal planting windows after rain events
- Inability to demonstrate soil health for carbon credit programs

**Confidence: HIGH** — FAO data confirms 80% dryland figure. Cellular coverage maps confirm large gaps in agricultural regions (Australia: 70%+ of farmland lacks reliable coverage; sub-Saharan Africa: 85%+; US Great Plains: 30-40% patchy/no coverage).

---

## Product Scope v1

**What it is**: A self-contained soil moisture probe that communicates directly to satellites via BLE (Hubble Network), requiring zero ground infrastructure (no gateway, no cellular tower, no WiFi). Farmer gets moisture readings on a phone app or web dashboard.

**MVP features (maximum 3)**:
1. Soil moisture at 2 depths (15cm and 45cm) — capacitive sensor
2. Soil temperature at probe tip
3. Daily readings delivered via satellite to cloud dashboard + mobile app with threshold alerts (SMS/email)

**What it does NOT do (v1)**:
- Does not measure soil nutrients (N/P/K) — requires expensive electrochemical sensors
- Does not provide irrigation control or automation — target market does not irrigate
- Does not do real-time continuous streaming — 1-4 readings per day
- Does not replace agronomist advice — provides data input only
- Does not include weather forecasting — can integrate third-party later

**Update frequency**: 4x daily (every 6 hours) — sufficient for dryland farming decisions where moisture changes slowly compared to irrigated systems.

---

## User Workflow

### Setup (one-time, <15 minutes)
1. Farmer purchases probes online or from ag supply store ($99/probe)
2. Opens app, scans QR code on probe → auto-registers device
3. Pushes probe into soil at desired monitoring point (hand-auger provided for hard soils)
4. Probe begins transmitting within 1 hour (next satellite pass)

### Daily use
1. Open app → see moisture levels at each probe location on a map
2. Color-coded: Green (adequate), Yellow (declining), Red (critically low)
3. Optional: receive SMS alert when moisture drops below configurable threshold

### Seasonal decisions enabled
- "Field A has enough moisture at depth — safe to plant this week"
- "Pasture B is drying out — move cattle to Pasture C which received rain"
- "Soil moisture has not recovered since harvest — delay planting by 2 weeks"

---

## Pricing

| Item | Price | Notes |
|------|-------|-------|
| Probe hardware | $99 one-time | Includes installation tool |
| Monthly data service | $5/month/probe | Includes satellite connectivity + cloud + app |
| Annual plan (paid upfront) | $50/year/probe | ~17% discount for commitment |

**Unit economics at $5/month**:
- Satellite data cost (Hubble): ~$1-2/month/device (estimated; UNVERIFIED)
- Cloud/infra cost: ~$0.20/device/month at scale
- Support allocation: ~$0.50/device/month
- **Gross margin on subscription: ~50-65%**

**Hardware margin**:
- BOM: $35 (at 1K volume)
- Landed cost with packaging/shipping: ~$45
- Retail: $99
- **Hardware gross margin: ~55%**

**Confidence on pricing**: MEDIUM — $5/month is viable IF Hubble data costs stay below $2/device/month. Comparable IoT subscription services (livestock trackers, asset trackers) charge $3-10/month.

---

## Ideal First Customer

**Profile**: Australian dryland grain farmer (wheat, barley, canola)
- Farm size: 2,000-10,000 hectares
- Located in Western Australia, South Australia, or western NSW
- Zero or unreliable cellular coverage across majority of paddocks
- Currently makes planting decisions based on "rule of thumb" + manual soil sampling (expensive, $30-50/sample, done 1-2x per year)
- Sophisticated enough to use smartphone apps (80%+ of Australian farmers have smartphones)
- Revenue: $500K-$5M/year — can afford $500-2000/year for monitoring (10-40 probes)
- Already invests in precision ag (variable rate seeding, yield mapping) but lacks real-time soil data

**Why Australia first**:
1. Largest concentration of high-value dryland farms with no cellular coverage
2. English-speaking (simpler support/marketing)
3. Farmers are tech-forward (high smartphone/precision ag adoption)
4. Hubble Network likely to have satellite coverage over Australia (sun-synchronous LEO covers all latitudes)
5. Existing proof point: Ceres Tag (livestock) and Myriota (IoT) both validated Australian ranch/farm demand
6. AUD pricing allows premium positioning vs. developing-world markets

**Ideal first deployment**: 5 farms, 20 probes each (100 total), across wheat belt of Western Australia during growing season (May-November). Revenue: $500/month from subscriptions + $10K hardware sale.

**Secondary markets (Year 2+)**:
- US Great Plains (Kansas, Nebraska, Montana, Dakotas) — winter wheat, rangeland
- Sub-Saharan Africa (Kenya, Tanzania, Ethiopia) — smallholder aggregator model
- Central Asia (Kazakhstan, Uzbekistan) — massive wheat regions, zero connectivity

---

## Key Assumptions to Validate

1. **Dryland farmers will pay $5/month for moisture data** — UNVALIDATED. Dryland farmers have lower per-hectare revenue than irrigated farms. Price sensitivity is real.
2. **4x daily readings are sufficient** — HIGH CONFIDENCE. Soil moisture changes slowly in dryland (days/weeks, not hours).
3. **Hubble Network will provide reliable coverage over target geographies** — UNVERIFIED. Critical dependency.
4. **Farmers can self-install probes** — MEDIUM CONFIDENCE. Capacitive probes need good soil contact. May need installation guide/support.
5. **Battery life of 3+ years is achievable** — MEDIUM CONFIDENCE. 4 transmissions/day on BLE is very low duty cycle. Similar to livestock tags architecture.
