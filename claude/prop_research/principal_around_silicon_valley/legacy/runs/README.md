# Peninsula Bay Area 3BR Market Research — June 2026

**Status**: Research infrastructure set up; ready for data collection

## Overview

This directory contains tools and templates for systematically collecting 2025-2026 3-bedroom home price data for 8 Peninsula Bay Area towns to support your $2M property purchase research.

**Target Towns**:
- Daly City, Millbrae, Burlingame, San Carlos, Foster City, Belmont, Pacifica, Half Moon Bay

**Goal**: Find median home prices and assess what your $2M budget can purchase in each market.

---

## Files in This Directory

### Core Research Files
- **`peninsula_market_research_2025-2026.json`** — Main template for populated results
  - Contains: Town list, data sources, expected output schema, quality criteria
  - Fill this in as you collect data from authoritative sources
  - Use as master record for all 8 towns' data

### Guides & Instructions
- **`MARKET_RESEARCH_GUIDE.md`** — Complete how-to guide for data collection
  - Quick reference for where to find data (Zillow, Redfin, MLS, Assessor)
  - Time estimates (20 min - 4 hours depending on depth)
  - Expected data ranges for each town
  - Quality criteria and red flags to watch for

- **`EXAMPLE_COMPLETED_RESEARCH.md`** — San Carlos case study
  - Shows what completed research looks like for ONE town
  - Demonstrates how to compile multiple sources
  - Template you can copy/adapt for other 7 towns

### Data Collection Tools
- **`COLLECTION_CHECKLIST_*.txt`** — Step-by-step checklist
  - Phase 1: Quick Zillow/Redfin scan (20 min)
  - Phase 2: MLS validation (30 min - 2 hrs)
  - Phase 3: Compilation (15 min)
  - Phase 4: Integration (30 min)
  - Quality checks

- **`market_urls/`** — Pre-formatted URL lists
  - `zillow_urls_*.txt` — All 8 Zillow market pages
  - `redfin_urls_*.txt` — All 8 Redfin market insight pages
  - `mls_contacts_*.txt` — Email template for requesting MLS data from agents

- **`market_data_collection_*.csv`** — Data entry spreadsheet
  - Pre-populated with 8 towns (rows)
  - Columns for Zillow, Redfin, MLS, and final median
  - Easy to fill in as you collect data

- **`collect_market_data.sh`** — Bash helper script
  - Generates all URL lists and templates with timestamps
  - Run again any time you need fresh templates

---

## How to Use This

### Option A: Fast Track (20-30 minutes)
Best for: Quick baseline data, validating if this region is in your budget

1. **Open all Zillow pages** (use `market_urls/zillow_urls_*.txt`)
2. **Screenshot median prices** for each town
3. **Note the dates** stamped on each page
4. **Cross-check with Redfin** (use `market_urls/redfin_urls_*.txt`)
5. **Fill in CSV** with both sources
6. **Populate JSON** with best data (most recent)

**Result**: 8 towns with 2 data points each (Zillow + Redfin), HIGH confidence if recent

---

### Option B: Authoritative (1-2 hours)
Best for: Serious research; most accurate data for decision-making

1. **Run Fast Track** (Option A above)
2. **Reach out to local agents** (use `market_urls/mls_contacts_*.txt`)
3. **Request MLS market reports** for each town
4. **Collect recent sales comparables** (comps)
5. **Fill in MLS column** in CSV
6. **Reconcile all sources** and populate JSON

**Result**: 8 towns with 3+ data points each (Zillow + Redfin + MLS), VERY HIGH confidence

---

### Option C: Comprehensive (2-4 hours)
Best for: Deep analysis; understanding market dynamics

1. **Run Option B** (Fast Track + MLS)
2. **Research supplementary metrics**:
   - Price per sqft trends
   - Days on market
   - Months of inventory
   - YoY appreciation rates
3. **Compile summary statistics** (min, max, average across region)
4. **Assess what $2M buys** in each town
5. **Create town comparison table**
6. **Integrate findings into Step 2** neighborhood scoring

**Result**: Rich dataset ready for neighborhood-level analysis

---

## Expected Outputs

### Primary Output: JSON Template
**File**: `peninsula_market_research_2025-2026.json`

**Example populated entry**:
```json
{
  "town": "San Carlos",
  "medianPrice": 1750000,
  "source": "Redfin Q2 2026 + San Mateo MLS May 2026",
  "url": "https://www.redfin.com/CA/San-Carlos/homes-for-sale",
  "date": "2026-06-22",
  "confidence": "high",
  "notes": "3BR median: $1.68M (Zillow), $1.75M (Redfin), $1.74M (MLS). Using Redfin as primary (most recent, actual sales). What $2M buys: 4BR/2.5BA, 2300 sqft, 0.5-acre lot in good schools."
}
```

### Secondary Output: Summary Table
**Example**:
```
Town          | Median Price | Price/SqFt | Confidence | What $2M Buys
--------------|--------------|------------|------------|----------------------------
San Carlos    | $1,750,000   | $900       | HIGH       | 4BR/2.5BA, 0.5-acre, schools
Belmont       | $1,400,000   | $820       | HIGH       | 4BR/2BA, 0.6-acre, quiet
Foster City   | $1,900,000   | $950       | MEDIUM     | 4BR/2BA, 0.4-acre, planned community
[... etc]
```

---

## Integration with Property Research Plan

This market data directly supports:

**Research Plan Step 2: Neighborhood Identification & Scoring**
- **Criterion 6: Price & Value** — These medians tell you what your budget affords
- **Data source**: "Median price (3BR+, 1700+ sqft, SFH)" per scoring rubric

**Research Plan Step 3: Deep Neighborhood Analysis**
- **Section 3a: Market Deep Dive** — Use this as foundation
- **"What $2M Buys"** — Populates the description field

**Research Plan Step 4: Financial Analysis**
- Feeds into purchase scenarios (Conservative $1.5M, Mid $1.75M, Stretch $2M)
- Supports appreciation modeling and ROI projections

---

## Data Quality Standards

### Recency
- **Prioritize**: Q2 2026 data (April-June 2026) — most current
- **Accept**: Q1 2026 (January-March 2026) — still recent enough
- **Mark as "Prior Year"**: Anything before Q4 2025

### Confidence Levels
| Level | Criteria | Examples |
|-------|----------|----------|
| HIGH | Multiple sources (3+), Q2 2026 data, MLS/actual sales origin | Redfin + Zillow + MLS all within 3-5% |
| MEDIUM | 2 sources, Q1-Q2 2026, mix of estimates and actual sales | Redfin + Zillow differ by 8-10% |
| LOW | 1 source, older than 3 months, estimates only | Only Zillow estimate available, dated Q1 2026 |

### Data Type Consistency
- **Preferred**: 3BR-specific median (aligns with your 3BR minimum)
- **Acceptable**: Overall median (use if 3BR unavailable, note which)
- **Always specify**: Which type you're using so comparisons are valid

---

## Key Decisions Made

1. **Format: JSON** — Structured, machine-readable, easy to integrate into Step 2 scoring
2. **8 target towns** — Represents full Peninsula region from SF border (Daly City) to Half Moon Bay
3. **Multiple sources per town** — Cross-validation catches stale/erroneous data
4. **Confidence tracking** — Makes clear what's "known" vs. "estimated"
5. **"What $2M buys" section** — Directly answers: Is this town a viable option for your budget?

---

## Timeline

**Recommended completion**: June-July 2026 (ASAP to inform neighborhood scoring)

- **Phase 1 (Quick scan)**: Today or tomorrow (20-30 min)
- **Phase 2 (MLS outreach)**: This week (allow 2-3 days for agent responses)
- **Phase 3 (Compilation)**: When Phase 2 responses arrive (15 min)
- **Phase 4 (Integration)**: Immediately after compilation (30 min)

**Then**: Proceed to Step 2 Neighborhood Scoring with solid market foundation

---

## Troubleshooting

**Q: Zillow/Redfin pages are slow or not loading market data**
- A: Try incognito mode or clear browser cache
- A: Mobile Zillow/Redfin sites sometimes load faster
- A: If pages are "403 Forbidden", use MLS/agent data instead

**Q: Real estate agents not responding to data requests**
- A: Call instead of email (faster)
- A: Try 2-3 agents per town; at least one will respond
- A: Look for agents with "market analysis" in their listings

**Q: Data sources show very different numbers (>10% apart)**
- A: Check dates — one may be stale
- A: Check filters — one may include condos, one SFH-only
- A: Note the discrepancy in JSON and use most recent source

**Q: Can't find 3BR-specific data**
- A: Use overall median; note that you did this
- A: 3BR medians are typically 5-15% higher than overall
- A: Ask agents directly for 3BR comps

---

## Related Files

- **Main research plan**: `/home/colligo/hs_scripts/claude/prop_research/research-plan.md`
  - Full Step 1-6 detailed procedures; this market research is Step 2 foundation

- **Project memory**: `/home/colligo/.claude/projects/-home-colligo-hs-scripts/memory/prop_research_project.md`
  - Background on your property purchase criteria and timeline

- **Git repo**: `/home/colligo/hs_scripts/claude/prop_research/`
  - Version control; commit findings: `git add . && git commit -m "prop_research: Peninsula Q2 2026 market data"`

---

## Contact & Questions

If you hit blockers or need to adapt this process:

1. Check the **MARKET_RESEARCH_GUIDE.md** for common issues
2. Review **EXAMPLE_COMPLETED_RESEARCH.md** for format questions
3. Look at the actual research-plan.md for context on how this fits into larger property evaluation

---

**Last Updated**: 2026-06-22  
**Created By**: Claude Code Agent  
**Status**: READY FOR DATA COLLECTION  
