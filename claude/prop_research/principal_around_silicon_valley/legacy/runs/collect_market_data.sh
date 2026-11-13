#!/bin/bash
# Peninsula Bay Area 3BR Market Research Data Collection Helper
# Usage: bash collect_market_data.sh

set -e

TOWNS=("Daly-City" "Millbrae" "Burlingame" "San-Carlos" "Foster-City" "Belmont" "Pacifica" "Half-Moon-Bay")
OUTPUT_DIR="/home/colligo/hs_scripts/claude/prop_research/runs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=========================================="
echo "Peninsula Bay Area Market Research Helper"
echo "=========================================="
echo ""
echo "This script will generate URLs for market research across 8 towns."
echo "Run Time: $(date)"
echo ""

# Create directory if needed
mkdir -p "$OUTPUT_DIR/market_urls"

# Generate URL lists
echo "[INFO] Generating market research URLs..."

cat > "$OUTPUT_DIR/market_urls/zillow_urls_$TIMESTAMP.txt" << 'EOF'
# Zillow Market Insights URLs - Open in browser
# Copy each URL into your browser and capture median price + date

Daly City:
https://www.zillow.com/homes/for_sale/Daly-City-CA/

Millbrae:
https://www.zillow.com/homes/for_sale/Millbrae-CA/

Burlingame:
https://www.zillow.com/homes/for_sale/Burlingame-CA/

San Carlos:
https://www.zillow.com/homes/for_sale/San-Carlos-CA/

Foster City:
https://www.zillow.com/homes/for_sale/Foster-City-CA/

Belmont:
https://www.zillow.com/homes/for_sale/Belmont-CA/

Pacifica:
https://www.zillow.com/homes/for_sale/Pacifica-CA/

Half Moon Bay:
https://www.zillow.com/homes/for_sale/Half-Moon-Bay-CA/
EOF

cat > "$OUTPUT_DIR/market_urls/redfin_urls_$TIMESTAMP.txt" << 'EOF'
# Redfin Market Insights URLs - Open in browser
# Click "Market Insights" tab and capture median price + date

Daly City:
https://www.redfin.com/CA/Daly-City/homes-for-sale

Millbrae:
https://www.redfin.com/CA/Millbrae/homes-for-sale

Burlingame:
https://www.redfin.com/CA/Burlingame/homes-for-sale

San Carlos:
https://www.redfin.com/CA/San-Carlos/homes-for-sale

Foster City:
https://www.redfin.com/CA/Foster-City/homes-for-sale

Belmont:
https://www.redfin.com/CA/Belmont/homes-for-sale

Pacifica:
https://www.redfin.com/CA/Pacifica/homes-for-sale

Half Moon Bay:
https://www.redfin.com/CA/Half-Moon-Bay/homes-for-sale
EOF

cat > "$OUTPUT_DIR/market_urls/mls_contacts_$TIMESTAMP.txt" << 'EOF'
# San Mateo County MLS - Request Data From Local Agents

Sample email template:

---
Subject: Market Data Request - Peninsula Bay Area 3BR Medians (Q2 2026)

Hello [Agent Name],

I'm researching the Peninsula Bay Area real estate market. Could you provide the following for [TOWN NAME]:

1. Median home sale price for 3BR+, 1700+ sqft homes, YTD 2026 (or most recent 30-60 days available)
2. Overall median sale price (all homes sold)
3. Price per sqft trend
4. Days on market (average)
5. Any recent market reports for [TOWN]?

Town(s) of interest:
- San Carlos
- Belmont
- Foster City
- Burlingame
- Millbrae
- Pacifica
- Half Moon Bay
- Daly City

Thank you for your time!

---

Suggested Local Agents to Contact (for each town):
- Search: "[TOWN NAME] + real estate agent" + "market analysis"
- Or contact: San Mateo County MLS directly
- Or visit: Zillow/Redfin for agent recommendations in the area
EOF

echo "[OK] URL files generated:"
echo "    - $OUTPUT_DIR/market_urls/zillow_urls_$TIMESTAMP.txt"
echo "    - $OUTPUT_DIR/market_urls/redfin_urls_$TIMESTAMP.txt"
echo "    - $OUTPUT_DIR/market_urls/mls_contacts_$TIMESTAMP.txt"
echo ""

# Create data entry CSV template
cat > "$OUTPUT_DIR/market_data_collection_$TIMESTAMP.csv" << 'EOF'
town,zillow_median,zillow_date,zillow_url,redfin_median,redfin_date,redfin_url,mls_median,mls_date,mls_source,final_median,confidence,notes
Daly City,,,,,,,,,,,
Millbrae,,,,,,,,,,,
Burlingame,,,,,,,,,,,
San Carlos,,,,,,,,,,,
Foster City,,,,,,,,,,,
Belmont,,,,,,,,,,,
Pacifica,,,,,,,,,,,
Half Moon Bay,,,,,,,,,,,
EOF

echo "[OK] CSV data collection template created:"
echo "    - $OUTPUT_DIR/market_data_collection_$TIMESTAMP.csv"
echo ""

# Create checklist
cat > "$OUTPUT_DIR/COLLECTION_CHECKLIST_$TIMESTAMP.txt" << 'EOF'
PENINSULA BAY AREA 3BR MARKET RESEARCH CHECKLIST
================================================

Phase 1: Quick Zillow/Redfin Scan (20 min)
[ ] Open all Zillow town pages (use zillow_urls_*.txt)
[ ] Screenshot/note median price and date for each town
[ ] Open all Redfin town pages (use redfin_urls_*.txt)
[ ] Screenshot/note median price and date for each town
[ ] Fill in zillow_median, zillow_date, redfin_median, redfin_date columns in CSV

Phase 2: MLS Validation (30 min - 2 hours)
[ ] Identify 1-2 local real estate agents for each town
[ ] Send data request email (template in mls_contacts_*.txt)
[ ] Receive responses with current market data
[ ] Fill in mls_median, mls_date, mls_source columns in CSV

Phase 3: Compilation (15 min)
[ ] For each town, compare the 2-3 data points (Zillow, Redfin, MLS)
[ ] Identify "final_median" (average or most recent/authoritative)
[ ] Assign confidence level: HIGH (3 sources, recent), MEDIUM (2 sources or slightly stale), LOW (1 source or >6 months old)
[ ] Add notes for any conflicts or methodology differences
[ ] Fill in final_median and confidence columns

Phase 4: Integration (30 min)
[ ] Open peninsula_market_research_2025-2026.json
[ ] Populate median_price_data array with results
[ ] Update summary_statistics with min/max/average across all towns
[ ] Commit to git: git add . && git commit -m "prop_research: Peninsula market data Q2 2026"

Quality Checks:
[ ] All 8 towns have at least 1 data source (prefer 2+)
[ ] Data dates are within last 6 months (prioritize Q2 2026)
[ ] Confidence levels are justified
[ ] Any conflicts (>10% difference) are documented in notes
[ ] Price ranges make sense (no town is dramatically cheaper/more expensive than neighbors)

Estimated Time: 1-2 hours (Option 1+2 combined)
EOF

echo "[OK] Checklist created:"
echo "    - $OUTPUT_DIR/COLLECTION_CHECKLIST_$TIMESTAMP.txt"
echo ""

echo "=========================================="
echo "NEXT STEPS"
echo "=========================================="
echo ""
echo "1. Review the market research guide:"
echo "   cat $OUTPUT_DIR/MARKET_RESEARCH_GUIDE.md"
echo ""
echo "2. Open the URL files in your browser:"
echo "   cat $OUTPUT_DIR/market_urls/zillow_urls_$TIMESTAMP.txt"
echo "   cat $OUTPUT_DIR/market_urls/redfin_urls_$TIMESTAMP.txt"
echo ""
echo "3. Fill in the CSV as you collect data:"
echo "   $OUTPUT_DIR/market_data_collection_$TIMESTAMP.csv"
echo ""
echo "4. Populate the JSON template when complete:"
echo "   $OUTPUT_DIR/peninsula_market_research_2025-2026.json"
echo ""
echo "5. Review example completed research:"
echo "   cat $OUTPUT_DIR/EXAMPLE_COMPLETED_RESEARCH.md"
echo ""
echo "=========================================="
echo "Files created:"
ls -lh "$OUTPUT_DIR"/market_urls/* "$OUTPUT_DIR"/market_data_collection_$TIMESTAMP.csv "$OUTPUT_DIR"/COLLECTION_CHECKLIST_$TIMESTAMP.txt 2>/dev/null | tail -20
echo "=========================================="
echo ""
