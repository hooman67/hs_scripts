# Peninsula Bay Area 3BR Median Home Price Research - 2025-2026

## Research Status
**Date Created:** June 22, 2026
**Purpose:** Collect 3BR median home prices for 8 Peninsula towns to support $2M property purchase analysis
**Target Towns:** San Carlos, Belmont, Foster City, Burlingame, Millbrae, Pacifica, Half Moon Bay, Daly City

---

## Recommended Data Sources (Ranked by Accessibility & Reliability)

### PRIMARY SOURCES (Direct Price Data)

#### 1. **Zillow Market Overview Pages**
- **Access:** Desktop browser (web scraping blocked, manual viewing required)
- **URL Pattern:** `https://www.zillow.com/homes/for_sale/[CITY]-CA/`
- **Data Available:**
  - Median listing price
  - Median sold price (if available)
  - Price trends
  - Days on market
- **2025-2026 Status:** Current real-time data
- **Confidence:** HIGH for current market
- **Instructions:**
  1. Visit URL for each town
  2. Look for "Median home price" or "Price estimates" section
  3. Note the "Sold" tab for actual transaction prices
  4. Record date shown on page

**Town URLs:**
- San Carlos: https://www.zillow.com/homes/for_sale/San-Carlos-CA/
- Belmont: https://www.zillow.com/homes/for_sale/Belmont-CA/
- Foster City: https://www.zillow.com/homes/for_sale/Foster-City-CA/
- Burlingame: https://www.zillow.com/homes/for_sale/Burlingame-CA/
- Millbrae: https://www.zillow.com/homes/for_sale/Millbrae-CA/
- Pacifica: https://www.zillow.com/homes/for_sale/Pacifica-CA/
- Half Moon Bay: https://www.zillow.com/homes/for_sale/Half-Moon-Bay-CA/
- Daly City: https://www.zillow.com/homes/for_sale/Daly-City-CA/

---

#### 2. **Redfin Market Reports**
- **Access:** Desktop browser
- **URL Pattern:** `https://www.redfin.com/CA/[CITY]/`
- **Data Available:**
  - Median list price
  - Median sale price
  - Average sale price
  - 3-bed specific filters available
  - Year-over-year trends
- **2025-2026 Status:** Current real-time data with historical comparison
- **Confidence:** HIGH
- **Instructions:**
  1. Visit Redfin page for each town
  2. Use left sidebar filters: "Beds" = 3 for 3BR-specific data
  3. Record "Median home price" and "Average sale price"
  4. Check "Market Trends" section for historical context

**Town URLs:**
- San Carlos: https://www.redfin.com/CA/San-Carlos/
- Belmont: https://www.redfin.com/CA/Belmont/
- Foster City: https://www.redfin.com/CA/Foster-City/
- Burlingame: https://www.redfin.com/CA/Burlingame/
- Millbrae: https://www.redfin.com/CA/Millbrae/
- Pacifica: https://www.redfin.com/CA/Pacifica/
- Half Moon Bay: https://www.redfin.com/CA/Half-Moon-Bay/
- Daly City: https://www.redfin.com/CA/Daly-City/

---

#### 3. **County Assessor & MLS Data**
- **San Mateo County Assessor:** https://www.smc-ca.gov/assessor
  - Property search tool with sales data
  - Most authoritative source for transaction history
  - Can search by zip code for each town
  
- **MLS Direct (SFRMLS):** https://www.sfrmls.com/
  - Bay Area's official MLS
  - Requires agent login, but public limited data available
  - Contact local real estate agent for detailed MLS reports

- **Local Real Estate Agents:**
  - Each town's top agents maintain current market data
  - Many publish monthly market reports
  - Email template provided in "MLS Contact Template" section below

---

### SECONDARY SOURCES (Market Analysis & Reports)

#### 4. **Real Estate News & Market Reports**
- **San Francisco Chronicle Real Estate:** https://www.sfchronicle.com/real-estate/
  - Look for "Bay Area Market Report" articles
  - Search: "[Town name] median home price 2025" or "2026"
  
- **Silicon Valley Business Journal:** https://www.bizjournals.com/sanjose/real-estate
  - Quarterly market reports
  - Peninsula market analysis
  
- **Bay Area Real Estate News:** https://www.realtor.com/real-estate-news
  - National Realtor Association data for Bay Area

---

#### 5. **Government & Census Data**
- **U.S. Census Bureau:** https://www.census.gov/
  - Median home values by area (slower to update)
  - Demographic context
  
- **California Department of Housing:** https://www.hcd.ca.gov/
  - State-level market data
  - Regional housing reports

---

## Data Collection Template

```json
[
  {
    "town": "San Carlos",
    "medianPrice": null,
    "pricePerSqFt": null,
    "bedrooms": "3BR",
    "sources": [
      {
        "source": "Zillow",
        "url": "https://www.zillow.com/homes/for_sale/San-Carlos-CA/",
        "medianPrice": null,
        "date": "2026-06-22",
        "confidence": "high",
        "notes": ""
      },
      {
        "source": "Redfin",
        "url": "https://www.redfin.com/CA/San-Carlos/",
        "medianPrice": null,
        "date": "2026-06-22",
        "confidence": "high",
        "notes": ""
      }
    ]
  },
  {
    "town": "Belmont",
    "medianPrice": null,
    "sources": []
  },
  {
    "town": "Foster City",
    "medianPrice": null,
    "sources": []
  },
  {
    "town": "Burlingame",
    "medianPrice": null,
    "sources": []
  },
  {
    "town": "Millbrae",
    "medianPrice": null,
    "sources": []
  },
  {
    "town": "Pacifica",
    "medianPrice": null,
    "sources": []
  },
  {
    "town": "Half Moon Bay",
    "medianPrice": null,
    "sources": []
  },
  {
    "town": "Daly City",
    "medianPrice": null,
    "sources": []
  }
]
```

---

## MLS Contact Template

Use this to reach out to local real estate agents for detailed MLS market reports:

```
Subject: Market Data Request - Peninsula Towns 3BR Median Prices (2025-2026)

Hi [Agent Name],

I'm researching the current real estate market in the Peninsula Bay Area and would appreciate your professional perspective on current 3-bedroom median home prices for the following towns:

- San Carlos
- Belmont
- Foster City
- Burlingame
- Millbrae
- Pacifica
- Half Moon Bay
- Daly City

Could you provide:
1. Current median list price for 3BR homes
2. Current median sale price for 3BR homes
3. Average days on market
4. Year-over-year price change
5. Current market conditions (buyer's/seller's market)

This information will help me understand the local market better. Thank you!

Best regards,
[Your Name]
```

---

## Data Quality Checklist

For each data point collected:

- [ ] **Source Identified:** Name, URL, and date accessed
- [ ] **Data Type Confirmed:** Median vs. average, listing vs. sold price
- [ ] **Time Period:** Confirmed data is for 2025-2026 (not older)
- [ ] **Confidence Level:** HIGH (recent, primary source) / MEDIUM (recent, secondary) / LOW (older than 3 months)
- [ ] **3BR Specific:** If yes, note it; if overall median, note that
- [ ] **Conflicting Data:** If two sources differ >10%, flag for verification

---

## Collection Workflow

### Option A: Quick (20-30 minutes) - MEDIUM Confidence
1. Visit Zillow for each town (8 pages, ~2 min each)
2. Visit Redfin for each town (8 pages, ~2 min each)
3. Cross-reference and average prices
4. Use highest confidence sources as primary data

### Option B: Thorough (1-2 hours) - HIGH Confidence  
1. Complete Option A
2. Email 2-3 local real estate agents per town for MLS data
3. Check county assessor for recent transaction data
4. Cross-validate with news reports
5. Document any discrepancies

### Option C: Comprehensive (2-4 hours) - VERY HIGH Confidence
1. Complete Option B
2. Call local real estate offices for market expertise
3. Request formal market analysis documents
4. Check historical trends (2024, 2023) to validate patterns
5. Create confidence matrix for final report

---

## Expected 2025-2026 Price Ranges (Estimated Based on Historical Trends)

| Town | Estimated 3BR Median | Confidence |
|------|----------------------|------------|
| San Carlos | $2.0M - $2.4M | Medium |
| Belmont | $1.8M - $2.2M | Medium |
| Foster City | $2.1M - $2.5M | Medium |
| Burlingame | $1.9M - $2.3M | Medium |
| Millbrae | $1.7M - $2.1M | Medium |
| Pacifica | $1.3M - $1.7M | Medium |
| Half Moon Bay | $1.2M - $1.6M | Medium |
| Daly City | $1.1M - $1.5M | Medium |

*Note: These are estimates based on 2024 data. Actual 2025-2026 prices should be verified through current sources above.*

---

## Next Steps After Data Collection

1. **Format Results:** Fill in final JSON with all collected data
2. **Calculate Averages:** If multiple sources, average or use median value
3. **Assess Confidence:** Rate each town's data based on source recency and agreement
4. **Document Outliers:** Note any prices that differ significantly from estimates
5. **Integration:** Use results for property research Step 2 (Neighborhood Identification & Scoring)

---

## Contact Information for Direct Research

**San Mateo County Real Estate:**
- County Assessor: (650) 364-4320
- San Mateo Board of Realtors: (650) 345-1000
- Common MLS contacts will respond to market data requests

**Alternative Digital Tools:**
- Zillow API (requires registration): https://www.zillow.com/howto/api/
- Redfin Trends: https://www.redfin.com/research
- Trulia Market Research: https://www.trulia.com/research/

---

## Notes on Data Interpretation

- **Median Price:** The middle price point (50% above, 50% below)
- **Average Price:** The mean (can be skewed by luxury properties)
- **Listing Price vs. Sold Price:** Sold price is more accurate (actual transactions)
- **Price Per Sqft:** Useful for comparing value across towns
- **Market Trend:** Check if prices are trending up/down month-over-month

---

**Document Created:** June 22, 2026
**Last Updated:** June 22, 2026
**Research Coordinator:** Claude Code Research Assistant
