# Peninsula Neighborhoods - Data Collection Sources Guide

## Quick Reference: URLs & Lookup Instructions

### 1. COMMUTE TIMES (Google Maps)

**Base URLs:**
- DTSJ (San Jose downtown): 95113 (city center)
- SF Downtown: 94102 (city center)

**For each neighborhood, use Google Maps:**
1. Enter neighborhood center address
2. Route to "San Jose, CA 95113" (DTSJ) - note off-peak time (11am-2pm or 10pm-5am typical)
3. Route to "San Francisco, CA 94102" - same off-peak times
4. Record driving time in minutes

**Key addresses to use as "from" points:**
- Redwood City: 100 Main St, Redwood City CA 94063 (downtown)
- San Carlos: 600 Elm St, San Carlos CA 94070 (downtown)
- Belmont: 10 Sevier Ave, Belmont CA 94002 (town center)
- San Mateo: 4016 Olympic Dr, San Mateo CA 94403 (downtown area)
- Foster City: 1000 E Hillsdale Blvd, Foster City CA 94404 (downtown)
- Burlingame: 1355 Donnelly Ave, Burlingame CA 94010 (downtown)
- Millbrae: 250 Bobcat Dr, Millbrae CA 94030 (downtown)
- Pacifica: 540 Crespi Dr, Pacifica CA 94044 (downtown)
- Half Moon Bay: 300 Main St, Half Moon Bay CA 94019 (downtown)

---

### 2. HOUSING PRICES (Zillow & Redfin)

**Zillow:**
- URL template: https://www.zillow.com/homes/for_sale/[CITY]-CA/
- Look for: "Median home price" (if available in market summary)
- Filter: 3+ bedrooms, sort by recent sales
- Data to collect: Median price, average $/sqft, price range for 3BR homes

**Redfin:**
- URL template: https://www.redfin.com/CA/[CITY]/
- Look for: Market report section with median sold prices
- Filter: 3 bedrooms
- Data to collect: Median list price, median sold price, price/sqft

**Specific URLs for neighborhoods:**
- Redwood City: https://www.zillow.com/homes/for_sale/Redwood-City-CA/ + https://www.redfin.com/CA/Redwood-City/
- San Carlos: https://www.zillow.com/homes/for_sale/San-Carlos-CA/ + https://www.redfin.com/CA/San-Carlos/
- Belmont: https://www.zillow.com/homes/for_sale/Belmont-CA/ + https://www.redfin.com/CA/Belmont/
- San Mateo: https://www.zillow.com/homes/for_sale/San-Mateo-CA/ + https://www.redfin.com/CA/San-Mateo/
- Foster City: https://www.zillow.com/homes/for_sale/Foster-City-CA/ + https://www.redfin.com/CA/Foster-City/
- Burlingame: https://www.zillow.com/homes/for_sale/Burlingame-CA/ + https://www.redfin.com/CA/Burlingame/
- Millbrae: https://www.zillow.com/homes/for_sale/Millbrae-CA/ + https://www.redfin.com/CA/Millbrae/
- Pacifica: https://www.zillow.com/homes/for_sale/Pacifica-CA/ + https://www.redfin.com/CA/Pacifica/
- Half Moon Bay: https://www.zillow.com/homes/for_sale/Half-Moon-Bay-CA/ + https://www.redfin.com/CA/Half-Moon-Bay/

---

### 3. SCHOOLS & GREATSCHOOLS RATINGS

**GreatSchools.org:**
- URL template: https://www.greatschools.org/search?q=[CITY]%2C+California
- Look for: Average rating (0-10 scale) for area schools
- Data to collect: Top elementary, middle, high school ratings; count of private/alternative schools

**School Districts by City:**
- Redwood City, San Carlos: Sequoia Union High School District, various elementary districts
- Belmont: Belmont-Ravenswood Union School District
- San Mateo: San Mateo Union High School District
- Foster City: San Mateo Union High School District
- Burlingame: Burlingame School District, San Mateo Union High
- Millbrae: Millbrae School District, San Mateo Union High
- Pacifica: Pacifica School District
- Half Moon Bay: Half Moon Bay Union High School District, Half Moon Bay Elementary

**Alternative Schools Search:**
- Google: "[City] California Montessori schools"
- Google: "[City] California private schools no vaccine requirement"
- Google: "[City] California homeschool cooperatives"
- Check local Facebook groups for homeschool community recommendations

---

### 4. CRIME RATES (FBI UCR via City-Data)

**URL Template:** https://www.city-data.com/crime/crime-[City]-California.html

**Specific URLs:**
- Redwood City: https://www.city-data.com/crime/crime-Redwood-City-California.html
- San Carlos: https://www.city-data.com/crime/crime-San-Carlos-California.html
- Belmont: https://www.city-data.com/crime/crime-Belmont-California.html
- San Mateo: https://www.city-data.com/crime/crime-San-Mateo-California.html
- Foster City: https://www.city-data.com/crime/crime-Foster-City-California.html
- Burlingame: https://www.city-data.com/crime/crime-Burlingame-California.html
- Millbrae: https://www.city-data.com/crime/crime-Millbrae-California.html
- Pacifica: https://www.city-data.com/crime/crime-Pacifica-California.html
- Half Moon Bay: https://www.city-data.com/crime/crime-Half-Moon-Bay-California.html

**Data to collect:**
- Violent crime per 1,000 residents (2024-2025 most recent)
- Property crime per 1,000 residents (2024-2025 most recent)

---

### 5. DIVERSITY METRICS & CENSUS DATA

**Census Bureau ACS:**
- URL: https://censusreporter.org/
- Search: City name + California
- Data to collect: % White, % Hispanic/Latino, % Asian, % Black, % Other
- Calculate Simpson Diversity Index: D = 1 - Σ(p²)

**City-Data Demographics:**
- URL: https://www.city-data.com/city/[City]-California.html
- Look for demographics table with racial/ethnic breakdown

---

### 6. HOUSING APPRECIATION (5-Year Trends)

**Zillow Home Values:**
- URL: https://www.zillow.com/research/home-values/
- Search city and look for historical price chart
- Data to collect: Median home value 2021 vs 2026 (calculate % change)

**Alternative: Redfin Data Center**
- URL: https://www.redfin.com/news/data-center
- Search for city market data with historical trends

---

### 7. AI JOBS (30-MIN RADIUS)

**LinkedIn Job Search:**
- URL: https://www.linkedin.com/jobs/search/?keywords=ai%20engineer
- Filter: Location by zip code radius (30 min from target neighborhood)
- Look for: Job openings in nearby tech hubs (Cupertino, Mountain View, San Jose, Palo Alto areas)
- Data: Record total count of AI/ML/ML Ops/Data Science positions

**Indeed Job Search:**
- URL: https://www.indeed.com/jobs?q=ai+engineer
- Filter: Location by nearby cities
- Count positions

**Tech Company HQ Locations (within ~30 min from Peninsula):**
- Google (Mountain View - ~20-30 min)
- Apple (Cupertino - ~30-40 min)
- Meta (Menlo Park - ~15-25 min)
- Netflix (Los Gatos - ~30-45 min)
- Adobe DTSJ (San Jose - ~30-45 min from Peninsula)
- Cisco (San Jose - ~35-50 min)
- Zoom (San Jose - ~35-50 min)

---

### 8. LOT SIZES (Typical Residential)

**Zillow/Redfin Listing Data:**
- Search active listings for each city, filter 3+ bedrooms
- Record lot sizes from 5-10 recent listings
- Calculate average/median
- Alternative: Look at sold listings for past 6 months

**Zillow URL for lot size filtering:**
- https://www.zillow.com/homes/for_sale/[CITY]-CA/
- Look for "Lot size" field in listing details

---

### 9. WILDFIRE RISK (CAL FIRE SRA Maps)

**CAL FIRE SRA (State Responsibility Areas):**
- URL: https://fire.ca.gov/what-we-do/emergency-preparedness/fire-hazard-severity-zones-maps/
- Look up: Fire Hazard Severity Zones map for each city
- Data to collect: Is neighborhood in High/Very High SRA zone? Specific zone codes.

**Alternative: Local Fire Department Data:**
- Search: "[City] California wildfire risk map"
- Google local news for recent fire history (2020-2026)

---

### 10. FLOOD RISK (FEMA Flood Zones)

**FEMA Flood Zone Database:**
- URL: https://msc.fema.gov/portal/
- Search: City name or address
- Data to collect: Flood zone code (A, AE, X, etc.)
- Zone meanings:
  - Zone A: High-risk (1% annual chance flooding)
  - Zone AE: High-risk with elevation data
  - Zone X: Moderate/low risk (0.2-1% annual chance)
  - Zone X (shaded): Areas of 1% annual chance flooding and areas with 1% annual chance of shallow flooding

**Alternative: Local Flood Control District:**
- Search: "[City] flood zone map"
- Contact local planning department for flood zone confirmation

---

### 11. PARENT NETWORK STRENGTH

**Facebook Groups Search:**
- Search: "[City] Parents" or "[City] Schools" Facebook groups
- Indicators: Group size, posting frequency, member engagement
- Qualitative assessment: Strong/Moderate/Weak based on community activity

**Community Organizations:**
- Search: "[City] PTA" or "[City] community association"
- Look for: Active local nonprofits, community centers, event calendars

**NextDoor:**
- URL: https://nextdoor.com/
- Search neighborhood
- Review recent posts: frequency, tone, community engagement level

---

### 12. SCHOOL VACCINATION POLICY & BARRIERS

**California SB 277 & Exemptions:**
- CA allows only medical and newly-added parental belief exemptions (limited)
- Most districts require vaccinations or exemption request

**Per-School Policy Research:**
- Contact specific schools: ask about exemption rates + unvaccinated student accommodations
- Check school websites for policy statements

**Alternative/Private Schools (More Flexible):**
- Search: "[City] private schools"
- Call/email: Ask specifically if they accept unvaccinated families
- Montessori schools often have more flexible policies

**Homeschool Cooperatives:**
- Search: "[City] homeschool co-op"
- Facebook groups: "[City] homeschooling" or "Peninsula homeschool"
- Typically offer structured classes + community without vaccine mandates

---

## Data Quality Notes

**High Confidence Sources:**
- FBI UCR (crime) via City-Data
- US Census Bureau ACS (demographics)
- FEMA Flood Zones (official government)
- CAL FIRE SRA Maps (official state)

**Medium Confidence:**
- Zillow/Redfin prices (real estate market data, but snapshot in time)
- GreatSchools ratings (aggregated user reviews + test scores)
- Google Maps commute times (estimates; actual times vary by traffic pattern)

**Low Confidence (Qualitative):**
- Parent network strength (subjective assessment)
- School vaccination policy (must verify directly with schools)

---

## Collection Template (Copy & Fill)

```
Neighborhood: [CITY]
Date Collected: [DATE]

1. DTSJ Commute: [MINUTES] min (Source: Google Maps, [TIME CHECKED])
2. SF Commute: [MINUTES] min (Source: Google Maps, [TIME CHECKED])
3. Median 3BR Price: $[PRICE] (Source: Zillow/Redfin, [DATE])
4. Price/Sqft: $[PRICE] (Source: Zillow/Redfin, [DATE])
5. GreatSchools Rating: [RATING]/10 (Source: GreatSchools.org, [DATE])
6. Private/Alt Schools Count: [NUMBER] (Source: School websites, [DATE])
7. Violent Crime: [RATE]/1k (Source: City-Data/FBI UCR, 2025)
8. Property Crime: [RATE]/1k (Source: City-Data/FBI UCR, 2025)
9. Diversity Index: [INDEX] (Source: Census Bureau, 2024)
10. % Non-White: [PERCENT]% (Source: Census Bureau, 2024)
11. 5-Yr Appreciation: [PERCENT]% (Source: Zillow, 2021-2026)
12. AI Jobs (30 min): [COUNT] (Source: LinkedIn/Indeed, [DATE])
13. Typical Lot Size: [SQFT] sqft (Source: Zillow/Redfin listings, [DATE])
14. Wildfire Risk: [Yes/No - Zone] (Source: CAL FIRE SRA, [DATE])
15. Flood Risk: [Zone Code] (Source: FEMA, [DATE])
16. Parent Network: [Strong/Moderate/Weak] (Source: Facebook, [DATE])
17. Vax Barriers: [Description] (Source: School websites, [DATE])
```

