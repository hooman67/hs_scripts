# 01 Product Definition: Livestock GPS+Health Tags with Satellite Backhaul

## Problem Statement

**Who:** Cattle ranchers operating on remote rangeland (primarily US West — Montana, Wyoming, Texas, New Mexico, Colorado) with herds of 200-5,000+ head spread across thousands of acres without cellular coverage.

**How painful:** 
- **Theft:** USDA estimates $1B+/year in livestock theft in the US. Ranchers have zero real-time visibility when cattle are on remote pasture. A stolen animal is typically gone 24-48 hours before anyone notices.
- **Calving losses:** 5-8% calf mortality is standard; many deaths occur because ranchers cannot locate laboring cows in time. Each lost calf = $800-1,200 in revenue.
- **Health emergencies:** Bovine Respiratory Disease (BRD) alone costs the US beef industry $900M/year. Early detection (24-48h before visible symptoms) can reduce mortality by 50%+, but requires continuous behavioral monitoring impossible with manual observation on rangeland.
- **Labor:** Ranchers spend 10-20 hours/week on horseback or ATV checking cattle across remote sections. At implicit labor cost of $25-40/hr, this is $13,000-41,600/year per ranch.

**What they do today:**
- Manual rides to check cattle (weather-permitting, 1-2x/week for remote sections)
- Passive RFID tags (ID only, no tracking, requires reader proximity)
- Nothing — accept losses as cost of doing business
- Some use cellular-based solutions that only work near ranch HQ where towers exist (covers <20% of pasture)

## Product Scope v1

**Three core features only:**

1. **Real-time GPS location** — Position report every 4 hours (configurable 1-12h), viewable on web/mobile map with geofence alerts
2. **Movement/activity monitoring** — Accelerometer-based behavioral classification (grazing, resting, walking, distressed) with anomaly alerts suggesting illness or calving
3. **Theft/boundary alerts** — Geofence violation triggers immediate satellite uplink and push notification

**What v1 does NOT do:**
- No virtual fencing (requires much higher power, different actuator hardware)
- No temperature sensing (adds cost, unreliable in ear tag form factor vs. rumen bolus)
- No integration with cattle market/auction platforms (future roadmap)
- No predictive disease AI (requires training data from v1 deployments first)
- No herd management software (partner with existing platforms like CattleMax, Ranch Manager)

## User Workflow — Day 1

1. **Purchase:** Rancher orders 200 tags online ($50/tag = $10,000 upfront) + selects $3/head/month plan ($600/month)
2. **Receive & activate:** Tags arrive pre-programmed. Rancher downloads mobile app, scans QR code on tag packaging to link to account.
3. **Apply tags:** During routine cattle working (already scheduled for vaccinations/branding), apply ear tag using standard applicator — identical motion to existing NLIS/RFID tags. Takes <30 seconds per head.
4. **Configure geofences:** On mobile app (works offline, syncs later), draw pasture boundaries on satellite imagery. Set alert preferences.
5. **Monitor:** Within 4 hours, first position reports appear on dashboard map. Activity baseline establishes over 48-72 hours. Anomaly detection activates after day 3.
6. **Respond to alerts:** Push notification: "Cow #347 — possible calving behavior detected, last position: NW corner Section 12." Rancher drives directly to location.

## Pricing Model

| Component | Price | Justification |
|-----------|-------|---------------|
| Hardware (ear tag) | $50 one-time | $26 BOM + $10 manufacturing/QC + $8 margin + $6 shipping/packaging. 48% gross margin on hardware. |
| Data subscription | $3/head/month | Hubble Network estimated at $0.50-1.00/device/month for satellite backhaul + $0.50 cloud/compute + $1.00-2.00 margin. 33-67% gross margin on subscription. |
| Replacement tags | $40 | Discounted for existing subscribers |

**Justification vs. alternatives:**
- Cellular solutions (e.g., CattleWatch): $10-15/month — we are 70% cheaper
- Ceres Tag: Estimated $30-50/tag + undisclosed monthly — we target price parity or below on hardware, competitive on monthly
- Manual labor replaced: $3/head/month vs. $5-17/head/month equivalent labor cost for manual checking (200-head herd, 15h/week at $30/hr)

**Unit economics at 10,000 heads:**
- Monthly recurring revenue: $30,000
- Estimated satellite costs: $7,500
- Cloud/infrastructure: $2,500
- Gross margin on subscription: 67% ($20,000/month)
- Hardware revenue (one-time): $500,000 at 48% margin = $240,000 contribution

## Ideal First Customer Profile

**Demographic:**
- US West cattle rancher (Montana, Wyoming, Texas Panhandle, Eastern Oregon)
- 500-2,000 head cow-calf operation
- 5,000-50,000 acres, majority without cellular coverage
- Revenue: $1-5M/year
- Tech-adopter (already uses some digital tools — weather apps, satellite imagery for grazing rotation)
- Age 35-55 (open to technology, still actively managing operations)

**Psychographic:**
- Has experienced significant loss from theft, missed calving, or disease outbreak in past 2 years
- Currently spending $15,000+/year on labor for cattle checking
- Frustrated with cellular-dependent solutions that only work near headquarters
- Participates in cattlemen's associations and ranching social media groups

**Why they buy:**
- ROI is clear: $3/head/month x 1,000 head = $36,000/year vs. $50,000+ in preventable losses + labor savings
- No infrastructure to install (key differentiator vs. LoRa/cellular base stations)
- Ear tag form factor is familiar and trusted (vs. collars which cattle fight)
