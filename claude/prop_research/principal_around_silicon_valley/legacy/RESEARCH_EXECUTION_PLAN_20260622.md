# Sacramento Valley 5-Neighborhood Research: Execution Plan (June 22, 2026)

## Research Scope
- **Neighborhoods:** Folsom, Roseville, El Dorado Hills, Elk Grove, Davis
- **Data Points:** 14 metrics per neighborhood (70 total data points)
- **Target Date:** Mid-June 2026 current data
- **Timeline:** Single-session comprehensive compilation

---

## Data Collection Phase Sequence

### PHASE 1: Housing Market Data (Zillow, Redfin, MLS)
**Data Points:** Median 3BR Price, Lot Size, 5-yr Appreciation
**Duration:** 30-40 minutes per neighborhood

#### Folsom
- [ ] Zillow: https://www.zillow.com/homes/for_sale/Folsom-CA/
  - Filter: 3BR, SFH
  - Collect: Median price, median lot size
  - Record: Listing date (should be June 2026)
  
- [ ] Redfin: https://www.redfin.com/CA/Folsom/
  - Filter: 3BR, SFH
  - Collect: Median price, average price, typical lot size
  - Cross-check vs Zillow
  
- [ ] Zillow Historical: Search "Folsom CA home prices 2021 vs 2026"
  - Calculate: 5-year appreciation percentage

#### Roseville
- [ ] Zillow: https://www.zillow.com/homes/for_sale/Roseville-CA/
- [ ] Redfin: https://www.redfin.com/CA/Roseville/
- [ ] Historical price data

#### El Dorado Hills
- [ ] Zillow: https://www.zillow.com/homes/for_sale/El-Dorado-Hills-CA/
- [ ] Redfin: https://www.redfin.com/CA/El-Dorado-Hills/
- [ ] Historical price data

#### Elk Grove
- [ ] Zillow: https://www.zillow.com/homes/for_sale/Elk-Grove-CA/
- [ ] Redfin: https://www.redfin.com/CA/Elk-Grove/
- [ ] Historical price data

#### Davis
- [ ] Zillow: https://www.zillow.com/homes/for_sale/Davis-CA/
- [ ] Redfin: https://www.redfin.com/CA/Davis/
- [ ] Historical price data

---

### PHASE 2: School Data (GreatSchools.org)
**Data Points:** Average Rating, Alternative Schools Count, Diversity Index
**Duration:** 20-30 minutes per neighborhood

#### Each Neighborhood
- [ ] GreatSchools neighborhood search: https://www.greatschools.org/
  - Navigate to: [Neighborhood], [State]
  - Record: Average school rating (K-12 aggregate)
  - Count: Alternative/private/charter/homeschool options visible
  - Record: Diversity index or metric provided

---

### PHASE 3: Crime Statistics (FBI UCR + NeighborhoodScout)
**Data Points:** Violent Crime per 1k, Property Crime per 1k
**Duration:** 25-35 minutes per neighborhood

#### FBI UCR Database
- [ ] Search: https://crime-data-explorer.fbi.gov/
  - Jurisdiction: [City], California
  - Years: 2024-2025 (most recent available)
  - Violent crimes, Property crimes
  - Population data (to calculate per-1000 rate)
  
#### NeighborhoodScout Backup
- [ ] NeighborhoodScout: https://www.neighborhoodscout.com/
  - Search: [City], California
  - Record: Crime rates per 1,000
  - Note: Use if FBI data unavailable

---

### PHASE 4: Demographics (Census Bureau ACS)
**Data Points:** % Non-white Residents, Diversity Index
**Duration:** 20-30 minutes per neighborhood

#### Census Bureau American Community Survey
- [ ] Census Reporter: https://censusreporter.org/
  - Search: [City], California
  - Data Year: 2024 (or most recent available)
  - Collect: Race/ethnicity breakdown
  - Calculate: % non-white (100% - % white alone)

#### Fallback
- [ ] Census.gov direct: https://data.census.gov/
- [ ] NeighborhoodScout demographic breakdowns

---

### PHASE 5: Environmental Risk (Cal Fire, USGS, FEMA)
**Data Points:** Fire/Flood/Water Risk
**Duration:** 20-30 minutes per neighborhood

#### Cal Fire State Responsibility Area (SRA)
- [ ] Cal Fire Map: https://www.fire.ca.gov/
  - Search: [City]
  - Note: SRA zones, recent fire activity
  - Record: Risk level (low/moderate/high)

#### USGS/Flood Risk
- [ ] USGS Hazard Viewer: https://hazards.usgs.gov/
  - Search: [City]
  - Record: Flood zones, earthquake zones
  
#### FEMA Flood Maps
- [ ] FEMA Flood Map: https://msc.fema.gov/
  - Search: [City]
  - Record: Flood zones if present

---

### PHASE 6: Climate & Growing Season (USDA, NOAA)
**Data Points:** Growing Season/Frost-free Days, Hardiness Zone
**Duration:** 15-20 minutes per neighborhood

#### USDA Plant Hardiness Zones
- [ ] USDA Zone Map: https://planthardiness.ars.usda.gov/
  - Search: [City], California
  - Record: Hardiness zone (e.g., 9a, 9b)
  - Note: Frost-free days implied by zone

#### NOAA Climate Data
- [ ] NOAA Local Climatology: https://www.ncei.noaa.gov/
  - Search: [City]
  - Record: Average frost dates, growing season length

---

### PHASE 7: Commute Times (Google Maps, Waze)
**Data Points:** San Jose Commute (off-peak), San Francisco Commute (off-peak)
**Duration:** 20-30 minutes per neighborhood

#### Google Maps
- [ ] Route 1: [Neighborhood center] → Adobe area, San Jose (via I-80/I-50/I-101/880)
  - Set time: 9:30 AM or 2:30 PM (off-peak)
  - Record: Estimated time, distance
  - Note: June 22, 2026 date

- [ ] Route 2: [Neighborhood center] → San Francisco downtown (via north route through Sierra foothills or I-80 to Bay Bridge)
  - Set time: 9:30 AM or 2:30 PM (off-peak)
  - Record: Estimated time, distance

#### For Each Neighborhood
- [ ] Folsom center: [coords]
- [ ] Roseville center: [coords]
- [ ] El Dorado Hills center: [coords]
- [ ] Elk Grove center: [coords]
- [ ] Davis center: [coords]

---

### PHASE 8: Community Vibe (Synthesis)
**Data Points:** Community Vibe Description
**Duration:** 10-15 minutes per neighborhood

#### Sources to Synthesize
- [ ] Zillow/Redfin neighborhood descriptions
- [ ] GreatSchools vibe/diversity observations
- [ ] Local city government websites
- [ ] Walking scores (https://www.walkscore.com/)
- [ ] Community Reddit/forums (light research)

---

## Data Quality Checkpoints

### For Each Neighborhood:
- [ ] At least 2 sources per data point (except synthesis)
- [ ] Data dates verified (mid-2026 focus)
- [ ] Confidence levels assigned
- [ ] URLs recorded
- [ ] Outliers flagged and cross-checked
- [ ] Missing data marked "DATA NOT FOUND" with LOW confidence

### Validation Thresholds:
- **Prices:** Flag if >10% variance between Zillow/Redfin
- **Crime:** Flag if >20% variance between UCR/NeighborhoodScout
- **Demographics:** Use most recent Census data available

---

## Consolidation & Output

### Upon Completion:
1. Fill main data matrix in SACRAMENTO_VALLEY_5NEIGHBORHOOD_DATA_20260622.md
2. Update CSV: SACRAMENTO_5NEIGHBORHOODS_DATAMATRIX_20260622.csv
3. Create summary scorecards for quick comparison
4. Document all sources with confidence tiers
5. Flag any incomplete data points

### Final Deliverable Format:
- Markdown table with columns: [Neighborhood | Data Point | Value | Confidence | Source URL(s)]
- CSV export for spreadsheet analysis
- Neighborhood profile summaries
- Source citation index
- Data quality notes & limitations

---

## Time Budget

| Phase | Per Neighborhood | 5 Neighborhoods | Total |
|-------|------------------|-----------------|-------|
| Housing | 35 min | 2h 55min | 2h 55min |
| Schools | 25 min | 2h 05min | 2h 05min |
| Crime | 30 min | 2h 30min | 2h 30min |
| Demographics | 25 min | 2h 05min | 2h 05min |
| Environment | 25 min | 2h 05min | 2h 05min |
| Climate | 18 min | 1h 30min | 1h 30min |
| Commute | 25 min | 2h 05min | 2h 05min |
| Vibe | 12 min | 1h 00min | 1h 00min |
| **Total** | **3h 35min** | **17h 45min** | **17h 45min** |
| Consolidation & QA | - | - | 1h 00min |
| **GRAND TOTAL** | - | - | **18h 45min** |

*Note: Parallel searching can reduce actual elapsed time to 3-4 hours if multiple sources researched simultaneously*

---

## Troubleshooting Guide

### If Zillow/Redfin data is unavailable:
1. Try MLS search (requires agent contact)
2. Use NeighborhoodScout price estimates (MEDIUM confidence)
3. Try individual county assessor websites

### If FBI UCR data is old/incomplete:
1. Use NeighborhoodScout as backup (MEDIUM confidence)
2. Check local police department dashboards
3. Search "crime statistics [city] 2026"

### If Census 2024 data not available:
1. Use Census 2020 with notes
2. Try Census Reporter beta (2024 rollout)
3. Use ACS 2023 if current year unavailable

### If Cal Fire SRA maps don't load:
1. Try USGS hazard viewer
2. Search "[city] fire risk zone 2026"
3. Check local county fire department

### If USDA hardiness zone not found:
1. Use NOAA climate normals
2. Search "[city] growing season frost dates"
3. Use adjacent county data with notes

---

## Research Status Log

**Started:** [TIME]
**Phase 1 (Housing):** [PENDING]
**Phase 2 (Schools):** [PENDING]
**Phase 3 (Crime):** [PENDING]
**Phase 4 (Demographics):** [PENDING]
**Phase 5 (Environment):** [PENDING]
**Phase 6 (Climate):** [PENDING]
**Phase 7 (Commute):** [PENDING]
**Phase 8 (Vibe):** [PENDING]
**Consolidation:** [PENDING]
**Completion:** [PENDING]

---

## Notes for Researcher

1. **Batch similar neighborhoods:** Research all 5 neighborhoods for housing first, then move to schools, etc. More efficient than neighborhood-by-neighborhood approach.

2. **Keep sources visible:** Pin tabs for Zillow, Redfin, Census Reporter, etc. Reduces context switching.

3. **Screenshot data:** When you find prices/rates, screenshot them with URL visible. Provides date proof.

4. **Cross-reference immediately:** When values conflict, mark for follow-up research rather than guessing.

5. **Use browser back-button:** Many data points come from same pages (e.g., GreatSchools has ratings + school count + diversity).

6. **Track source URLs carefully:** You'll need these for final output - copy/paste directly from address bar.

7. **Note update dates:** Every data source has a "last updated" field. Record it for confidence scoring.

---

**Next Step:** Begin Phase 1 (Housing) by opening Zillow.com
