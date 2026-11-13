# Region 1: Sacramento & Central Valley — Data Collection Guide
**Target Neighborhoods**: Folsom, Roseville, El Dorado Hills  
**Property Criteria**: 3 BR, 1700+ sqft, single-family homes  
**Data Period**: March–May 2026 (recent sales)

---

## Data Collection Approach

Since automated web scraping is blocked, use these direct-access methods:

### 1. Zillow — Sold Homes Filter
**URL**: https://www.zillow.com/homes/for_sale/  
**Steps**:
1. Search "Folsom, CA" (or Roseville, El Dorado Hills)
2. Click **"Sold"** filter (left sidebar)
3. Set date range: **Last 90 days** (covers March–May 2026)
4. Filter: **Beds: 3+**, **Min Sq Ft: 1700**
5. Sort by price
6. Record: min price, max price, median, count visible
7. Take screenshot of listing page with URL/date stamp

### 2. Redfin — Sold Homes with Date Filter
**URL**: https://www.redfin.com/CA/  
**Steps**:
1. Search area
2. Click **"Sold"** (top tabs)
3. Adjust date range to March 1 - May 31, 2026
4. Add filters: **3+ bedrooms**, **Min sqft 1700**
5. Download CSV if available (right sidebar "Downloads")
6. Or manually record: count, price range, median

### 3. County Assessor Records
**Sacramento County Assessor**: https://assessor.saccounty.net/  
**El Dorado County Assessor**: https://assessor.edcgov.us/  
**Steps**:
1. Use property search tool (usually free, no auth required)
2. Search by address or owner name
3. Filter for sales in March–May 2026 if possible
4. Record: sale price, sales date, property size, lot size
5. These sites often have less restrictive access than market sites

### 4. Local MLS / Real Estate Agent Sites
- **Folsom**: Local real estate agents often publish market reports
- **Roseville**: Placer County MLS data
- **El Dorado Hills**: El Dorado County MLS data

---

## Data Template — Fill In From Direct Source Access

### Folsom, CA — 3BR 1700+ sqft Single-Family Homes (March–May 2026)

**Source 1: Zillow**  
- URL: [paste Zillow link with filters applied]  
- Access date: [YYYY-MM-DD]
- Screenshot: [filename in /runs/step2_neighborhood_scoring/folsom/]
- Min price: $[amount]
- Max price: $[amount]
- Median price: $[amount]
- Count of sales visible: [N]
- Notes: [any filters not applied, data quality notes]

**Source 2: Redfin**  
- URL: [paste Redfin link]  
- Access date: [YYYY-MM-DD]
- Min price: $[amount]
- Max price: $[amount]
- Median price: $[amount]
- Count: [N]
- CSV downloaded: Yes/No

**Source 3: Sacramento County Assessor**  
- URL: [assessor link with search performed]
- Access date: [YYYY-MM-DD]
- Comps found: [list 3–5 specific properties with sale price/date]
- Notes: [any limitations on date range]

**Consolidated Folsom Finding**:
- **Median price (3BR 1700+ sqft)**: $[amount] (based on N sales)
- **Price range**: $[min] – $[max]
- **Average price/sqft**: $[X]
- **Data confidence**: HIGH / MEDIUM / LOW
- **Sources merged**: Zillow (N) + Redfin (N) + Assessor (N) = [total verified]

---

### Roseville, CA — 3BR 1700+ sqft Single-Family Homes (March–May 2026)

**Source 1: Zillow**  
- URL: 
- Access date: 
- Min price: $
- Max price: $
- Median price: $
- Count: 
- Screenshot: 

**Source 2: Redfin**  
- URL: 
- Min price: $
- Max price: $
- Median price: $
- Count: 

**Source 3: Placer County Assessor** (https://www.placer.ca.gov/department/assessor)
- URL: 
- Comps: [list specific sales]

**Consolidated Roseville Finding**:
- **Median price**: $[amount] (based on N sales)
- **Price range**: $[min] – $[max]
- **Data confidence**: HIGH / MEDIUM / LOW

---

### El Dorado Hills, CA — 3BR 1700+ sqft Single-Family Homes (March–May 2026)

**Source 1: Zillow**  
- URL: 
- Access date: 
- Min price: $
- Max price: $
- Median price: $
- Count: 
- Screenshot: 

**Source 2: Redfin**  
- URL: 
- Min price: $
- Max price: $
- Median price: $
- Count: 

**Source 3: El Dorado County Assessor** (https://assessor.edcgov.us/)
- URL: 
- Comps: [list specific sales]

**Consolidated El Dorado Hills Finding**:
- **Median price**: $[amount] (based on N sales)
- **Price range**: $[min] – $[max]
- **Data confidence**: HIGH / MEDIUM / LOW

---

## Specific Properties to Capture

For each area, once you've found the price range, identify and record 5–10 specific comparable sales:

**Template per property**:
- Address: [full address]
- Sale price: $[amount]
- Sale date: [MM/DD/YYYY]
- Bedrooms: [N]
- Bathrooms: [N]
- Sq ft: [N]
- Lot size: [N sqft or acres]
- Year built: [YYYY]
- Type: Single-family / Townhome / [other]
- URL/MLS #: [link or MLS number]
- Source: Zillow / Redfin / County Assessor / [other]

---

## File Organization

```
prop_research/runs/step2_neighborhood_scoring/
├── REGION1_Sacramento_data_collection.md       # This file
├── folsom/
│   ├── zillow_search_[date].png                # Screenshots of Zillow/Redfin
│   ├── redfin_search_[date].png
│   ├── folsom_comps.csv                        # 5–10 specific properties
│   └── folsom_summary.md                       # Consolidated findings
├── roseville/
│   ├── roseville_comps.csv
│   └── roseville_summary.md
└── el_dorado_hills/
    ├── el_dorado_hills_comps.csv
    └── el_dorado_hills_summary.md
```

---

## Data Quality Checklist

Before finalizing each neighborhood's data:

- [ ] Confirmed date range is March–May 2026 (or as close as possible)
- [ ] Confirmed bedrooms ≥ 3
- [ ] Confirmed sq ft ≥ 1700
- [ ] Confirmed single-family home only (no townhomes/condos)
- [ ] Verified sales (not just listed) — look for "sold" status, not "active"
- [ ] At least 3 data sources consulted (Zillow, Redfin, Assessor)
- [ ] Minimum 5–10 specific comparable properties identified
- [ ] URLs and access dates recorded for reproducibility
- [ ] Outliers identified and noted (unusually high/low sales)
- [ ] Sample size is sufficient (N ≥ 5 for confidence; N < 3 = LOW confidence)

---

## Expected Timeline

- [ ] Folsom: March–May 2026 sales data compiled
- [ ] Roseville: March–May 2026 sales data compiled
- [ ] El Dorado Hills: March–May 2026 sales data compiled
- [ ] All three consolidated into summary table (below)

---

## Final Summary Table

| Area | Median Price | Price Range | # Sales | Avg $/sqft | Data Confidence | Sources | Last Updated |
|------|--------------|-------------|---------|------------|-----------------|---------|--------------|
| Folsom | $[X] | $[min]–$[max] | [N] | $[X] | HIGH/MED/LOW | [source list] | [YYYY-MM-DD] |
| Roseville | $[X] | $[min]–$[max] | [N] | $[X] | HIGH/MED/LOW | [source list] | [YYYY-MM-DD] |
| El Dorado Hills | $[X] | $[min]–$[max] | [N] | $[X] | HIGH/MED/LOW | [source list] | [YYYY-MM-DD] |

---

## Notes for Your Personal Reference

**Why these three areas?**
- Region 1 (Sacramento & Central Valley) is your baseline comparison for affordability
- Folsom, Roseville, El Dorado Hills are the suburban "growth" towns in Placer/El Dorado/Sacramento counties
- Long commute to DTSJ (~1.5–2 hrs) BUT significantly lower prices than Peninsula (expected ~$200K–$400K less)
- Will help establish: "What does $2M buy here vs. Peninsula?"

**Commute reality check** (from research-plan):
- These are likely to score 2–4 on job proximity (45–90 min to DTSJ)
- Route: I-80 East or Hwy 50 East (generally reliable, some closure history in winter)
- This is a TRADE: cheaper housing + worse commute + less urban amenities

**Next step after data collection**:
- Input this data into `neighborhood_scorecard.csv` (Step 2)
- Will then score each area on all 11 criteria (jobs, schools, growth, safety, diversity, price, community, property, survivability, beach, climate)
- Expect these to score HIGH on price (criterion 6) and MEDIUM on growth (developers active in Folsom/Roseville)
- Expect LOW on diversity and beach proximity
