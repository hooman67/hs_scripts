# Modesto Market Data Collection Guide
**Quick Reference for Manual Data Gathering**  
**Created**: 2026-06-22  
**Target**: 3BR, 1700+ sqft SFH, March–May 2026 sales

---

## Quick Start

### Step 1: Zillow Search (5 min)
1. Open: https://www.zillow.com/homes/for_sale/Modesto-CA/
2. Click "Sold" (left sidebar)
3. Set date: "Last 90 days"
4. Filters:
   - Beds: 3+
   - Min Sq Ft: 1700
   - Type: Single-family home
5. **Take screenshot** (include URL in screenshot)
6. **Record**: Min price, max price, ~median, count

### Step 2: Redfin Search (5 min)
1. Open: https://www.redfin.com/city/14657/CA/Modesto/homes-for-sale
2. Click "Sold" tab
3. Date range: March 1, 2026 - May 31, 2026
4. Filters: 3+ beds, 1700+ sqft
5. **Export CSV** if available (right sidebar)
6. **Record**: Min/max/median prices, count

### Step 3: County Assessor (10 min)
1. Open: https://assessor.stanislaus-county.com/
2. Use "Property Search" tool
3. Filter: Modesto, sold March–May 2026, 3BR+
4. **Find 5–10 specific properties**:
   - Address
   - Sale price
   - Sale date
   - Sq ft
   - Lot size
5. **Save as CSV** or note in spreadsheet

### Step 4: Consolidate (5 min)
1. Average the three sources
2. Fill in MODESTO_DATA_TEMPLATE.csv (below)
3. Note data confidence: HIGH/MEDIUM/LOW
4. Save to: `/home/colligo/hs_scripts/claude/prop_research/runs/step2_neighborhood_scoring/modesto/`

**Total time**: ~25 minutes for complete data collection

---

## Data Template — CSV Format

```csv
source,min_price,max_price,median_price,count_properties,price_per_sqft,access_date,url,notes
Zillow,550000,850000,675000,47,105,2026-06-22,https://www.zillow.com/homes/for_sale/Modesto-CA/,Sold last 90 days; 3BR+ 1700sqft SFH
Redfin,560000,860000,680000,45,108,2026-06-22,https://www.redfin.com/city/14657/CA/Modesto/homes-for-sale,March-May 2026; CSV exported
Assessor,555000,840000,670000,52,104,2026-06-22,https://assessor.stanislaus-county.com/,Public records; 10 comps verified
AVERAGE,555000,843000,675000,48,105,2026-06-22,,All three sources combined
```

Save as: `/home/colligo/hs_scripts/claude/prop_research/runs/step2_neighborhood_scoring/modesto/modesto_data.csv`

---

## Comparable Properties Template

Once you've found listings, capture these 5–10 properties:

```csv
address,sale_price,sale_date,bedrooms,bathrooms,sqft,lot_size,year_built,property_type,mls_number,url,source
"123 Oak St, Modesto CA 95350",650000,2026-05-15,3,2,1750,6500,1995,Single-Family,M12345678,https://www.zillow.com/,Zillow
"456 Elm Ave, Modesto CA 95350",695000,2026-04-28,4,2.5,1850,7200,2002,Single-Family,M87654321,https://www.redfin.com/,Redfin
```

Save as: `/home/colligo/hs_scripts/claude/prop_research/runs/step2_neighborhood_scoring/modesto/modesto_comps.csv`

---

## Expected Results

Based on regional market analysis:

| Metric | Conservative | Realistic | Optimistic |
|--------|--------------|-----------|-----------|
| Median Price | $620K | $670K | $720K |
| Price Range | $450K–$850K | $500K–$900K | $550K–$950K |
| Price/sqft | $95–$100 | $100–$110 | $105–$115 |
| Typical DOM | 25–35 days | 20–30 days | 15–25 days |
| Sales/quarter | 35–50 | 45–60 | 55–75 |

---

## Interpretation Guide

### What This Data Means for Your Decision

**If median ~$650K:**
- With $2M budget: Buys 3BR well, room for upgrades
- Compared to Peninsula: 40–50% cheaper housing
- Trade-off: 2+ hour commute vs 30 min in South Bay

**If median ~$750K:**
- With $2M budget: Still 3BR comfortable, less buffer
- Market may be heating up
- May want to compare to Fresno/Stockton for even better value

**If median <$600K:**
- Market cooling or data lag
- Best affordability deal in your research
- Must weigh against job proximity/long commute concerns

### Next Step in Research Plan

1. **Update neighborhood_scorecard.csv** with Modesto row:
   - Criterion 6 (Price & Value): **Score 9–10** (very affordable)
   - Criterion 1 (Job Proximity): **Score 2–4** (long commute ~2 hrs)
   - Criterion 5 (Diversity): **Score 4–5** (mixed, less multicultural)
   - Criterion 10 (Beach Proximity): **Score 2–3** (3+ hrs to coast)
   - **Estimated weighted total**: 4.5–5.5 (Tier C or D)

2. **Regional comparison**: Place Modesto alongside Folsom/Roseville/El Dorado Hills
   - Modesto likely cheapest but worst commute
   - May serve as "affordability floor" baseline

3. **Decision**: If Tier C/D, use as comparison only — not advancing to Step 3 deep dive

---

## Troubleshooting

### "Zillow says 0 results"
- Try broadening filters: 2BR instead of 3BR, or remove sqft minimum
- May be limited inventory matching exact criteria
- Try "For Sale" instead of "Sold" to see market depth
- Record what you find even if fewer than expected

### "Redfin CSV export not available"
- Export manually by copying/pasting table to Excel
- Or take screenshot and manually transcribe key prices
- Note the limitation in your data entry

### "County assessor site not loading"
- May be maintenance or regional network issue
- Try alternate: https://gis.co.stanislaus.ca.us/
- Or call Stanislaus County Assessor: (209) 468-3300
- Record attempt and note as "DATA UNAVAILABLE"

### "Prices seem too high/low"
- Check filters: Confirm 3BR, 1700+ sqft, SOLD (not active)
- Check date range: Must be March–May 2026 (within ~6 weeks of now)
- Compare against context: Modesto should be 40–50% cheaper than Bay Area
- If data anomaly, note in "confidence" field as MEDIUM or LOW

---

## Quality Checklist

Before finalizing data:

- [ ] Confirmed date range is March–May 2026 (or within last 90 days)
- [ ] Confirmed bedrooms ≥ 3
- [ ] Confirmed sq ft ≥ 1700
- [ ] Confirmed SOLD status (not active listings)
- [ ] Confirmed single-family homes only (no townhomes/condos)
- [ ] At least 40+ properties in sample (for statistical confidence)
- [ ] At least 3 data sources consulted (Zillow + Redfin + Assessor)
- [ ] 5–10 specific comparable properties identified with full details
- [ ] URLs and screenshots saved for reproducibility
- [ ] Median calculated correctly (middle of sorted price list)
- [ ] Price/sqft calculated (total_price / total_sqft)

---

## Files to Create/Update

After data collection, you'll have:

```
prop_research/runs/step2_neighborhood_scoring/modesto/
├── modesto_zillow_screenshot_2026-06-22.png
├── modesto_redfin_screenshot_2026-06-22.png
├── modesto_data.csv                    # Summary table
├── modesto_comps.csv                   # 5-10 specific properties
└── modesto_summary.md                  # Write-up with findings
```

---

## Summary for Your Notes

**Modesto Market (Expected)**
- Very affordable: $600–$750K median for 3BR+
- Long commute: ~2 hours to Adobe DTSJ
- Agricultural base: Lower tech job density
- Trade-off: Best value, worst location for your job
- Likely tier: C or D (comparison baseline, not deep-dive candidate)
- Immigration/visa consideration: Long commute may be unsustainable if job changes required

---

## Questions?

Refer to:
- Full research guide: `MODESTO_research_summary.md`
- Attempt log: `RESEARCH_ATTEMPT_LOG.md`
- Property research plan: `/home/colligo/hs_scripts/claude/prop_research/research-plan.md`
- Step 2 scoring rubric: Same file, "Step 2: Neighborhood Identification & Scoring" section
