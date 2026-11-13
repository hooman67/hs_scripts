# Peninsula Bay Area 3BR Market Research Guide
## Data Collection for 2025-2026

**Project Goal**: Find median 3-bedroom home prices for 8 Peninsula Bay Area towns to inform $2M property purchase research.

**Target Towns** (in geographic order, North to South):
- Daly City (northernmost, SF border)
- Millbrae 
- Burlingame
- San Carlos
- Foster City
- Belmont
- Pacifica (coastal)
- Half Moon Bay (coastal)

**Research Period**: 2025-2026 (prioritize 2026 Q2 data, accept 2025 Q4+)

---

## Quick Reference: Where to Find Data

### Option 1: Fast Track (15-30 min)
1. Open Zillow city pages for all 8 towns
   - URL pattern: `https://www.zillow.com/homes/for_sale/[CITY-NAME]-CA/`
   - Look for median home value in market insights section
   - Screenshot the value and date

2. Cross-check with Redfin
   - URL pattern: `https://www.redfin.com/CA/[CITY]/homes-for-sale`
   - Click "Market insights" tab
   - Note median sale price

3. Compare both sources, use most recent

### Option 2: Authoritative (1-2 hours)
1. **San Mateo County MLS** (best data, requires broker access or contacting agent)
   - Contact: Local real estate agent or MLS directly
   - Request: "3BR median sold price, 2026 YTD" for each town
   - They often have this in their monthly market reports

2. **San Mateo County Assessor**
   - Visit: https://www.smcgov.org/assessor
   - Search by city, access median valuations
   - Note: Assessor values usually lag behind market; use as confirmation, not primary

3. **Bay Area Board of Realtors**
   - Visit: https://reports.bayarearealtors.org/
   - Download monthly reports for Peninsula (San Mateo County)
   - Usually includes city-level medians

### Option 3: Comprehensive (2-4 hours)
Combine Options 1 + 2:
- Start with Zillow/Redfin for quick baseline
- Reach out to 2-3 local agents in each town for confirmation
- Request their market reports or recent comps
- Compile all sources into JSON template

---

## Data Collection Template (Per Town)

For **each of the 8 towns**, capture:

```
Town: [NAME]
Median Price: [NUMERIC]
Price Per SqFt: [NUMERIC] (if available)
Source 1: [NAME] - $[PRICE] (Date: [MM/YY])
Source 2: [NAME] - $[PRICE] (Date: [MM/YY])
Source 3: [NAME] - $[PRICE] (Date: [MM/YY])
Data Type: 3BR median OR overall median (specify)
Most Recent: [HIGHEST CONFIDENCE SOURCE]
Notes: Any conflicting data, methodology notes, etc.
```

---

## Key Metrics to Extract

### Primary (Required)
- **Median sale price** (most recent 2026 data available)
- **Data collection date** (when was this measured/published?)
- **Source name** (Zillow, Redfin, MLS, Assessor, etc.)
- **Data type** (3BR-specific? or overall median?)

### Secondary (Helpful)
- **Price per sqft** (useful for comparing value across towns)
- **Price trend** (YoY change, +/- %?)
- **Months of inventory** (how many months to sell all listed homes?)
- **Days on market** (are homes selling fast or sitting?)
- **Sales volume** (how many homes sold in period?)

### Context (For Analysis)
- **What does $2M buy here?**
  - Example: "In San Carlos, $2M buys a 4BR/2BA, 2200 sqft, 0.3-acre lot"
  - This tells you purchasing power in each market

---

## Important Notes on Data Quality

### Recency Issues
- **Zillow**: Updated often but includes estimates; some pages lag by 1-2 weeks
- **Redfin**: More current; updates frequently with actual sales
- **MLS**: Most current but broker-access only; real actual sales data
- **Assessor**: Official but lags market by 6-12 months; use as confirmation only

### 3BR vs. Overall Median
- **Preferred**: 3BR-specific median (aligns with your 3BR minimum requirement)
- **Acceptable**: Overall median (if 3BR unavailable; usually higher than overall)
- **Always note which** you're using so comparisons are consistent

### Price Ranges Across Sources
If sources differ by >10%, this usually means:
- Stale data (one source hasn't updated recently)
- Different filtering (one includes condos, one is SFH-only)
- Different time period (one is Q1, one is Q2)

**Action**: When sources diverge, use the most recent and note the discrepancy.

---

## Expected Data Pattern

Based on Bay Area real estate trends, expect roughly:

| Town | Expected Range | Rationale |
|------|---|---|
| **Daly City** | $1.1M - $1.3M | SF suburb, more affordable |
| **Millbrae** | $1.3M - $1.5M | SFO-adjacent, moderate price |
| **Burlingame** | $1.5M - $1.8M | More affluent; good schools |
| **San Carlos** | $1.6M - $1.9M | Popular with families; strong schools |
| **Foster City** | $1.7M - $2.0M | Planned community; desirable |
| **Belmont** | $1.4M - $1.7M | Less known; more value |
| **Pacifica** | $1.2M - $1.5M | Coastal but isolated; more affordable |
| **Half Moon Bay** | $1.3M - $1.6M | Coastal town; rural character |

**Note**: These are estimates. Your research will confirm or contradict.

---

## Red Flags in Data

🚩 **Stale data**: If page says "As of July 2025" in June 2026, it's outdated  
🚩 **Wide ranges**: If median shows "$1.2M - $2.4M" with no specific number, dig deeper  
🚩 **Outliers**: Single $5M mansion shouldn't skew 3BR median (request data excluding outliers)  
🚩 **Condos included**: If median includes condos, note it (usually 20-30% cheaper than SFH)  

---

## Next Steps After Data Collection

1. **Populate the JSON file** (`peninsula_market_research_2025-2026.json`)
2. **Calculate regional statistics** (min, max, average across all 8 towns)
3. **Determine your buying power**: What does your $2M budget buy in each town?
4. **Integrate into Step 2 neighborhood scoring** for Peninsula region (Region 4 in research-plan.md)
5. **Update project memory** with findings
6. **Schedule quarterly refresh** (Q3 2026) to capture seasonal changes

---

## Quick URLs for Bookmarking

**Zillow Market Insights** (by city):
- https://www.zillow.com/homes/for_sale/Daly-City-CA/
- https://www.zillow.com/homes/for_sale/Millbrae-CA/
- https://www.zillow.com/homes/for_sale/Burlingame-CA/
- https://www.zillow.com/homes/for_sale/San-Carlos-CA/
- https://www.zillow.com/homes/for_sale/Foster-City-CA/
- https://www.zillow.com/homes/for_sale/Belmont-CA/
- https://www.zillow.com/homes/for_sale/Pacifica-CA/
- https://www.zillow.com/homes/for_sale/Half-Moon-Bay-CA/

**Redfin Market Insights** (by city):
- https://www.redfin.com/CA/Daly-City/homes-for-sale
- https://www.redfin.com/CA/Millbrae/homes-for-sale
- https://www.redfin.com/CA/Burlingame/homes-for-sale
- https://www.redfin.com/CA/San-Carlos/homes-for-sale
- https://www.redfin.com/CA/Foster-City/homes-for-sale
- https://www.redfin.com/CA/Belmont/homes-for-sale
- https://www.redfin.com/CA/Pacifica/homes-for-sale
- https://www.redfin.com/CA/Half-Moon-Bay/homes-for-sale

**Official Resources**:
- San Mateo County Assessor: https://www.smcgov.org/assessor
- Bay Area Board of Realtors: https://reports.bayarearealtors.org/
- San Mateo MLS: https://www.sanmateocountymls.com/

---

## Time Estimate

- **Option 1 (Fast)**: 20-30 minutes (Zillow/Redfin only)
- **Option 2 (Authoritative)**: 1-2 hours (includes MLS/assessor outreach)
- **Option 3 (Comprehensive)**: 2-4 hours (all sources + local agent calls)

**Recommendation**: Start with Option 1 to establish baseline, then fill gaps with Option 2 sources.

---

## File Locations

- **JSON Template** (to fill in): `/home/colligo/hs_scripts/claude/prop_research/runs/peninsula_market_research_2025-2026.json`
- **Research Plan** (context): `/home/colligo/hs_scripts/claude/prop_research/research-plan.md`
- **Project Memory**: `/home/colligo/.claude/projects/-home-colligo-hs-scripts/memory/prop_research_project.md`
