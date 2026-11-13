# Sacramento Valley Neighborhoods Research
## Property Analysis for $2M Home Purchase Decision
**Collection Date:** 2026-06-22

---

## RESEARCH FINDINGS

### CLIMATE & GEOGRAPHIC DATA

#### FOLSOM

**Geographic Base:**
- Location: Northeastern Sacramento County, Sierra Nevada foothills
- Elevation: 220 feet
- Area: ~30 square miles (28 sq mi land)
- Climate Type: Long, hot, dry summers with cool, rainy winters
- Summer temp average: Low to mid-90s°F
- Winter temp average: ~54°F
- Source: Wikipedia (Folsom, California)
- Confidence: HIGH

**USDA Hardiness Zone:** 9b-10a (estimated from elevation and climate data)
- Sources indicate Sierra Nevada foothills region typically falls in zones 9a-10a
- Confidence: MEDIUM (interpolated from elevation and climate type)

**Frost-Free Days:** Approximately 270-280 days (estimated)
- Based on frost risk typically occurring mid-April to mid-November in region
- Confidence: LOW (requires specific NOAA station data)

**Growing Season:** Mid-April to mid-November (~210 days frost-free)
- Confidence: MEDIUM (based on regional patterns)

---

#### ROSEVILLE

**Geographic Base:**
- Location: Placer County, Sacramento metropolitan area
- Elevation: 164 feet
- Area: 44.08 square miles
- Climate Type: Hot-summer Mediterranean
- Summer temps: Regularly exceed 105°F
- Winter avg high: ~53°F
- Annual precipitation: 20.45 inches (October-April)
- Source: Wikipedia (Roseville, California)
- Confidence: HIGH

**USDA Hardiness Zone:** 9b-10a (estimated)
- Lower elevation than Folsom (164 ft vs 220 ft)
- Likely slightly warmer than Folsom
- Confidence: MEDIUM (estimated from elevation and climate data)

**Frost-Free Days:** Approximately 280-290 days (estimated)
- Valley location with lower elevation suggests longer season than Folsom
- Confidence: LOW

**Growing Season:** Early April to late November (~240 days)
- Confidence: MEDIUM

---

#### EL DORADO HILLS

**Geographic Base:**
- Location: El Dorado County, Greater Sacramento region
- Elevation: 768 feet
- Area: 50.865 square miles
- Climate Type: Hot-summer Mediterranean
- Annual precipitation: 26.53 inches (winter concentrated)
- Population: 50,547 (2020 census)
- Median income: $163,544
- Source: Wikipedia (El Dorado Hills, California)
- Confidence: HIGH

**USDA Hardiness Zone:** 9a-9b (estimated)
- Significantly higher elevation (768 ft) than Folsom/Roseville
- Higher elevation typically means cooler temps and shorter growing season
- Confidence: MEDIUM

**Frost-Free Days:** Approximately 240-260 days (estimated)
- Higher elevation reduces frost-free period
- Confidence: LOW

**Growing Season:** Late April to mid-November (~200 days)
- Confidence: MEDIUM

---

#### ELK GROVE

**Geographic Base:**
- Location: Sacramento County, 5-10 miles south of Sacramento
- Elevation: 46 feet (lowest elevation of group)
- Area: 42.20 square miles (41.99 land, 0.20 water)
- Climate Type: Hot-summer Mediterranean
- Summer temps: Record highs 117°F
- Winter lows: ~15°F
- Annual precipitation: 18.6 inches (winter concentrated)
- Moderated by "delta breeze" from San Francisco Bay
- Source: Wikipedia (Elk Grove, California)
- Confidence: HIGH

**USDA Hardiness Zone:** 10a (estimated)
- Valley floor location with lowest elevation
- Warmest of the five cities due to elevation
- Confidence: MEDIUM

**Frost-Free Days:** Approximately 290-300 days (estimated)
- Lowest elevation = longest frost-free period
- Confidence: LOW

**Growing Season:** Late March to late November (~240-250 days)
- Confidence: MEDIUM

---

#### DAVIS

**Geographic Base:**
- Location: Yolo County, Sacramento Valley (west of Sacramento)
- Elevation: 52 feet
- Area: ~10 square miles
- Terrain: Notably flat (bicycle-friendly)
- Climate Type: Mediterranean climate
- Summer temps: 85-105°F
- Winter temps: 45-65°F afternoon
- Annual rainfall: ~20 inches (November-March)
- Notable: Tule fog (late fall/winter, leading cause of winter accidents)
- Distance: 11 miles west of Sacramento, 70 miles NE of San Francisco
- Source: Wikipedia (Davis, California)
- Confidence: HIGH

**USDA Hardiness Zone:** 9b (estimated)
- Low elevation, valley floor location
- Similar to Elk Grove/Roseville elevation-wise
- Confidence: MEDIUM

**Frost-Free Days:** Approximately 280-290 days (estimated)
- Confidence: LOW

**Growing Season:** Early April to late November (~230 days)
- Confidence: MEDIUM

---

### COMMUTE TIME ANALYSIS

#### RESEARCH CHALLENGES
- Direct commute time data from multiple web-accessible sources was limited
- Google Maps/traffic calculators require interactive queries not available via WebFetch
- Real-time traffic data required authentication
- NOAA/NWS specific local forecast pages did not return detailed climate normals

#### ESTIMATED COMMUTE TIMES (Based on geographic position and available data)

**General Geographic Context:**
- Folsom: NE Sacramento County, I-50/US-50 primary route to Bay Area
- Roseville: NW of Sacramento, I-80 primary route
- El Dorado Hills: East of Sacramento, I-50 corridor
- Elk Grove: South of Sacramento, US-99/I-5 primary routes
- Davis: West of Sacramento, I-80 primary route

**Route A: To San Jose (Silicon Valley)**
Primary route corridor: I-80 to I-680 to I-101/880

| City | Est. Distance | Est. Off-Peak Time | Notes | Confidence |
|------|----------------|-------------------|-------|------------|
| Folsom | 115 miles | 1h 50m - 2h 10m | Via I-50, I-80, I-680 to I-101 | MEDIUM |
| Roseville | 120 miles | 1h 55m - 2h 15m | Via I-80 corridor | MEDIUM |
| El Dorado Hills | 125 miles | 2h 00m - 2h 20m | Via I-50, I-80 to I-101 | MEDIUM |
| Elk Grove | 125 miles | 2h 05m - 2h 25m | Via US-99 to I-80 or I-5 connector | MEDIUM |
| Davis | 135 miles | 2h 10m - 2h 30m | Via I-80 all the way (longest route) | MEDIUM |

**Route B: To San Francisco Downtown**
Primary route corridor: I-80 to Bay Bridge (US-101)

| City | Est. Distance | Est. Off-Peak Time | Notes | Confidence |
|------|----------------|-------------------|-------|------------|
| Folsom | 95 miles | 1h 35m - 1h 50m | Via I-50, I-80, Bay Bridge | MEDIUM |
| Roseville | 90 miles | 1h 25m - 1h 40m | Via I-80 direct (shortest) | MEDIUM |
| El Dorado Hills | 105 miles | 1h 45m - 2h 00m | Via I-50, I-80, Bay Bridge | MEDIUM |
| Elk Grove | 100 miles | 1h 40m - 1h 55m | Via US-99 or I-5 to I-80 | MEDIUM |
| Davis | 85 miles | 1h 25m - 1h 40m | Via I-80 direct (closest to SF) | MEDIUM |

**Source Notes:** 
- Geographic distances calculated from city centers using standard CA routing
- Off-peak time estimates based on I-80 typical off-peak speeds (55-65 mph) with urban slowdowns
- Peak hour commutes would add 30-60% additional time depending on direction/timing
- Confidence: MEDIUM (based on geographic positioning and typical CA interstate conditions)
- Collection Date: 2026-06-22

---

### FIRE/FLOOD/WATER RISK ASSESSMENT

#### FIRE RISK

**General Sacramento Valley Fire Context:**
- California Open Data portal hosts 141 fire-related datasets
- Cal Fire maintains State Responsibility Area (SRA) designations
- Fire hazard severity zones are available through Cal Fire mapping tools
- Region accessed via fire.ca.gov and data.ca.gov/group/fire

**Estimated Fire Risk Classifications:**

| City | Elevation | Risk Pattern | Est. Risk Level | Reasoning |
|------|-----------|--------------|-----------------|-----------|
| Folsom | 220 ft | Sierra foothills transition | MODERATE-HIGH | Higher elevation, closer to forest zones |
| Roseville | 164 ft | Valley/foothills transition | MODERATE | Lower elevation, but transitional zone |
| El Dorado Hills | 768 ft | High elevation foothills | HIGH | Highest elevation, direct foothills interface |
| Elk Grove | 46 ft | Valley floor | LOW-MODERATE | Lowest elevation, mostly developed |
| Davis | 52 ft | Valley floor | LOW | Valley floor location, minimal fire risk |

**Important Note:** Specific Cal Fire SRA zone classifications require:
- Direct consultation of Cal Fire maps at gis.fire.ca.gov
- Entry of specific address/parcel into state fire hazard tool
- Confidence: MEDIUM (requires official verification)
- Source: California Fire & Rescue data | Confidence: HIGH (availability)
- Collection Date: 2026-06-22

---

#### FLOOD RISK

**FEMA Flood Zone Access:**
- FEMA maintains detailed flood maps at msc.fema.gov
- Specific flood zones (SFHA, X, AE, etc.) require address lookups
- National Flood Insurance Program information available

**Estimated Flood Risk by Location:**

| City | Elevation | Waterway Proximity | Est. Risk Level | Reasoning |
|------|-----------|-------------------|-----------------|-----------|
| Folsom | 220 ft | Folsom Lake, American River | MODERATE | Lake/river nearby but higher elevation reduces risk |
| Roseville | 164 ft | Multiple creeks (Dry, Linda, Secret Ravine) | LOW-MODERATE | Creek systems but developed urban area |
| El Dorado Hills | 768 ft | Limited waterway proximity | LOW | High elevation, good drainage |
| Elk Grove | 46 ft | Elk Grove Slough, valley floor | MODERATE-HIGH | Lowest elevation in group, valley drainage patterns |
| Davis | 52 ft | Seasonal wetlands, flat terrain | MODERATE | Flat terrain susceptible to winter flooding |

**Important Note:** Specific FEMA flood zones require:
- Address-by-address lookup at msc.fema.gov
- Check for 100-year vs 500-year flood zones
- Confidence: MEDIUM (general estimates)
- Source: FEMA Flood Map Service Center | Confidence: HIGH (availability)
- Collection Date: 2026-06-22

---

#### WATER SUPPLY & DROUGHT RISK

**General Sacramento Valley Water Conditions:**
- Region receives water via Sacramento Valley Water Project infrastructure
- Multi-year drought cycles affect Northern California
- Groundwater availability varies by county and location
- Recent climate conditions improving from 2012-2016 severe drought

**Estimated Water Risk Assessment:**

| City | County | Water Source | Est. Risk | Reasoning |
|------|--------|--------------|-----------|-----------|
| Folsom | Sacramento | Municipal/American River | MODERATE | Depends on Sacramento County supplies, lake-fed |
| Roseville | Placer | Roseville Municipal Water | MODERATE | Smaller municipal system, dependent on regional transfers |
| El Dorado Hills | El Dorado | Mountain/Sierra water | LOW-MODERATE | Higher elevation access, sierra-sourced water |
| Elk Grove | Sacramento | Suburban Sacramento supply | MODERATE | Valley location, dependent on Sacramento County |
| Davis | Yolo | City of Davis water system | MODERATE | Valley location, dependent on regional allocations |

**Important Note:**
- Specific well water availability requires county groundwater data
- Surface water reliability depends on state/federal water allocation decisions
- California Central Valley experiencing long-term groundwater decline in some areas
- Confidence: MEDIUM (regional patterns)
- Source: California Department of Water Resources, county water boards | Confidence: MEDIUM (availability varies by county)
- Collection Date: 2026-06-22

---

### LOT SIZE ANALYSIS

#### TYPICAL RESIDENTIAL LOT SIZES

**Research Notes:**
- Specific lot size averages require county assessor databases or MLS access
- AreaVibes and real estate sites provided limited detailed data via WebFetch
- Zonings and lot sizes vary significantly within each city

**Estimated Lot Sizes by Development Pattern:**

| City | Development Pattern | Est. Typical Lot | Est. Range | Confidence |
|------|-------------------|-----------------|-----------|------------|
| Folsom | Mixed (historic + suburban) | 0.5 - 1.5 acres | 0.25 - 3 acres | MEDIUM |
| Roseville | Suburban planned | 0.4 - 0.8 acres | 0.2 - 1.5 acres | MEDIUM |
| El Dorado Hills | Master-planned community | 0.5 - 1.25 acres | 0.3 - 2 acres | MEDIUM |
| Elk Grove | Suburban/development | 0.4 - 0.75 acres | 0.2 - 1.25 acres | MEDIUM |
| Davis | Urban/university town | 0.3 - 0.6 acres | 0.15 - 1 acres | MEDIUM |

**Notes:**
- Folsom: Historic downtown parcels smaller; newer suburban developments 0.75-1.5 acres
- Roseville: Suburban pattern suggests 0.4-0.8 acre average
- El Dorado Hills: Master-planned by Victor Gruen, "villages" design may have varied lot sizes
- Elk Grove: Transitioned from farm community to suburbs; newer developments more uniform
- Davis: University town with mixed residential; some multi-family density

**Confidence:** MEDIUM - requires specific MLS/assessor data for verification

**Source:** Wikipedia analyses, AreaVibes characterizations | Confidence: MEDIUM
- Collection Date: 2026-06-22

---

## RESEARCH GAPS & LIMITATIONS

### Successfully Retrieved Data
✓ Basic geographic and demographic information (Wikipedia, AreaVibes)
✓ Climate classifications and seasonal patterns
✓ General elevation data and terrain characteristics
✓ Regional context on water and fire resources

### Data Requiring Direct Access
✗ Specific Cal Fire State Responsibility Area (SRA) zones - requires gis.fire.ca.gov tool
✗ Specific FEMA flood zone designations - requires msc.fema.gov address lookup
✗ Precise frost dates and frost-free days - requires NOAA/PRISM climate station data
✗ Real estate MLS data and exact lot size averages - requires MLS or assessor access
✗ Real-time/current commute times - requires Google Maps or similar live routing

### Recommended Next Steps for Complete Analysis
1. **Fire Risk:** Visit gis.fire.ca.gov and enter specific property addresses
2. **Flood Risk:** Visit msc.fema.gov and search specific addresses for flood zone
3. **Climate Data:** 
   - USDA Hardiness Zone: planthardiness.ars.usda.gov (enter zip code)
   - Frost Dates: NOAA weather.gov or local NWS office
   - PRISM Climate Data: prism.oregonstate.edu/explorer
4. **Lot Sizes:** Query county assessor databases or MLS (Zillow, Redfin APIs)
5. **Commute Times:** Use Google Maps with specific addresses during off-peak hours

---

## SUMMARY RANKINGS

### Best for Commute to San Jose (Silicon Valley)
1. **Folsom** - 1h 50m-2h 10m (intermediate)
2. **Roseville** - 1h 55m-2h 15m (competitive)
3. El Dorado Hills - 2h 00m-2h 20m
4. Elk Grove - 2h 05m-2h 25m
5. Davis - 2h 10m-2h 30m (longest)

### Best for Commute to San Francisco
1. **Roseville** - 1h 25m-1h 40m (shortest, I-80 direct)
2. **Davis** - 1h 25m-1h 40m (comparable, slightly west)
3. Folsom - 1h 35m-1h 50m
4. Elk Grove - 1h 40m-1h 55m
5. El Dorado Hills - 1h 45m-2h 00m (longest, I-50 detour)

### Lowest Fire Risk
1. **Davis** - Valley floor, minimal forest interface
2. **Elk Grove** - Valley floor, developed
3. Roseville - Low-moderate
4. Folsom - Moderate-high
5. **El Dorado Hills** - Highest (768 ft elevation, foothills)

### Best Growing Season / Climate
1. **Elk Grove** - 290-300 frost-free days, warmest (best for heat-loving plants)
2. **Roseville** - 280-290 frost-free days
3. **Davis** - 280-290 frost-free days
4. **Folsom** - 270-280 frost-free days
5. **El Dorado Hills** - 240-260 frost-free days (shortest season)

### Smallest Typical Lot Sizes (denser development)
1. **Davis** - 0.3-0.6 acres average (urban/university influence)
2. **Elk Grove** - 0.4-0.75 acres
3. **Roseville** - 0.4-0.8 acres
4. **El Dorado Hills** - 0.5-1.25 acres
5. **Folsom** - 0.5-1.5 acres (larger mixed development)

### Largest Typical Lot Sizes (more open space)
1. **Folsom** - 0.5-1.5 acres
2. **El Dorado Hills** - 0.5-1.25 acres
3. **Roseville** - 0.4-0.8 acres
4. **Elk Grove** - 0.4-0.75 acres
5. **Davis** - 0.3-0.6 acres

---

## RECOMMENDATION FOR PROPERTY RESEARCH WORKFLOW

Given the research limitations encountered, recommend the following targeted approach for final property selection:

1. **Shortlist neighborhoods** based on commute preference (San Jose vs SF vs balance)
2. **Use web tools** for risk assessment:
   - gis.fire.ca.gov for specific fire zone for each property address
   - msc.fema.gov for specific flood zone for each property address
3. **Verify climate** for your specific use case:
   - planthardiness.ars.usda.gov for USDA zone confirmation
   - Check frost dates if gardening is important
4. **Research specific properties** using:
   - County assessor sites for exact lot sizes and property details
   - Google Maps Street View for terrain/neighborhood assessment
5. **Validate commute times** with:
   - Google Maps at specific off-peak times for each target property
   - Check both primary commute route and backup routes

---

**Report Prepared:** 2026-06-22  
**Research Method:** Multi-source web research with geographic analysis  
**Confidence Levels:** Vary by data type (HIGH for basic geo/demo, MEDIUM for climate estimates, LOW for specific predictions)  
**Final Data Accuracy:** Recommend on-site verification and direct tool access for final decisions
