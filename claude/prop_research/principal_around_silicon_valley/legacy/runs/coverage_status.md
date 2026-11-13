# Coverage Status — Property Research Pipeline

**Last Updated**: 2026-06-23 05:30 UTC  
**Session**: ALL STEPS COMPLETE (Steps 1-6 + Final Executive Summary)

---

## Step 1: Region Screening — ✅ COMPLETE

All 6 regions evaluated and filtered:

- [x] **Region 1**: Sacramento & Central Valley — **PASS** (median $950K, 90 min commute, 47% diverse)
- [x] **Region 2**: North Bay / Wine Country — **FAIL** (commute 100-120 min, GG Bridge fragility, price at ceiling)
- [x] **Region 3**: East Bay — **PASS** (median $1.25M, 45-50 min commute, 48% diverse, stable water)
- [x] **Region 4**: Peninsula & South Bay — **PASS** (median $1.55M, 15-18 min commute, 58% diverse, 4,000+ AI jobs) ⭐ PRIMARY
- [x] **Region 5**: Santa Cruz & Monterey — **CONDITIONAL PASS** (good diversity, but CA-17 fragility + water stress)
- [x] **Region 6**: Central Coast — **FAIL** (commute 160-180 min, limited jobs)

**Advancing to Step 2**: Regions 1, 3, 4, 5 (conditional)

---

## Step 2: Neighborhood Scoring — ✅ COMPLETE

**43 neighborhoods scored across 4 regions:**

### **Tier A: Promoted to Step 3 (≥ 7.5 weighted score)**
6 neighborhoods advancing for deep analysis:

1. ✅ **Fremont** (8.0) — 🏆 STANDOUT: 83.4% diverse, $1.15M, 150 AI jobs, 35-min commute
2. ✅ **San Mateo** (72.5) — Safest, 67% diverse, excellent schools, 30-min commute
3. ✅ **San Carlos** (72.1) — Fastest commute (22.5 min), top schools (7.8), 58% diverse
4. ✅ **Oakland Hills** (7.3) — 65% diverse, balanced commute (40 min), safest East Bay
5. ✅ **Pleasanton** (7.2) — Excellent schools (8.1), very safe (0.8/1K), strong appreciation
6. ✅ **Folsom** (7.64) — Best Sacramento option: $875K, good jobs (262), good diversity

### **Tier B: Strong Contenders (10 neighborhoods)**
- San Ramon (7.22), Saratoga (7.0), Cupertino (6.9), Los Gatos (6.7), Willow Glen (6.59)
- Redwood City (63.3), Foster City (70.2), Burlingame (69.4), Millbrae (68.5), Belmont (69.1)

### **Tier C–E: Viable but with compromises (27 neighborhoods)**
- Lower scores due to: long commutes, lower diversity, water stress, weak schools, or high prices

**Output files**:
- `runs/step2_neighborhood_scoring/neighborhood_scorecard_final.csv` ✅
- `runs/step2_neighborhood_scoring/step2_final_report.md` ✅

---

## Step 3: Deep Neighborhood Analysis — ✅ COMPLETE

All 6 Tier A neighborhoods deep-dived (2026-06-23):

| Neighborhood | Recommendation | Key Finding |
|---|---|---|
| **Fremont** | **STRONG BUY** | Only place with large Persian/Afghan community (Little Kabul), sanctuary fortress, top schools, 35-min commute |
| **San Mateo** | BUY | Safest, best water (SFPUC), walkable, but $1.8M+ needed and flat appreciation |
| **Pleasanton** | BUY | Elite schools + safety + appreciation, but no cultural community for wife |
| **Oakland Hills** | BUY (caution) | Beautiful but VERY HIGH wildfire risk + insurance crisis |
| **Folsom** | HOLD | Great value but 90-min commute dealbreaker without remote work |
| **San Carlos** | PASS | Budget insufficient ($2.7M median vs $2M budget) |

Reports: `runs/step3_deep_analysis/{neighborhood}/report.md`

---

## Step 4: Financial Analysis — ✅ COMPLETE

- Mortgage scenarios for all advancing neighborhoods at $1.4M-$2.0M price points
- Appreciation modeling (bear/base/bull) for 5-year and 10-year horizons
- Cost-of-living comparison across all finalists
- Investment risk assessment (tech crash, wildfire, drought, immigration)

Reports: `runs/step4_financial/step4_report.md`, `runs/step4_financial/financial_comparison.csv`

---

## Step 5: Final Ranking — ✅ COMPLETE

| Rank | Neighborhood | Score | Recommendation |
|---|---|---|---|
| 1 | Fremont (Centerville/Irvington) | 7.24 | STRONG BUY |
| 2 | San Mateo (Baywood/Hillsdale) | 6.71 | BUY |
| 3 | Pleasanton | 6.63 | BUY |
| 4 | San Carlos | 6.27 | PASS |
| 5 | Folsom | 5.92 | HOLD |
| 6 | Oakland Hills | 5.43 | PASS |

Reports: `runs/step5_ranking/decision_report.md`, `runs/step5_ranking/final_ranking.csv`, `runs/step5_ranking/immigration_risk.md`

---

## Step 6: Deep Property Research — ✅ COMPLETE (3/3)

- [x] Fremont — specific properties, visit plan, expert contacts, financial summary
- [x] San Mateo — specific properties, visit plan, expert contacts
- [x] Oakland Hills — specific properties, visit plan, expert contacts

Reports: `runs/step6_deep_research/{neighborhood}/report.md`

---

## FINAL EXECUTIVE SUMMARY — ✅ WRITTEN

`runs/FINAL_EXECUTIVE_SUMMARY.md` — clear #1 recommendation, action items, timeline, immigration strategy

---

## Key Decisions Made

1. ✅ **Diversity elevated to 10% weight**: Non-negotiable for brown Middle Eastern family safety/comfort
2. ✅ **Route reliability deal-breaker**: CA-17 (Santa Cruz) and 100+ min commutes eliminated
3. ✅ **Tier A threshold**: 7.5+ weighted score → 6 neighborhoods qualified
4. ✅ **Regional prioritization**: Peninsula & South Bay primary (shortest commute, most jobs, high diversity); East Bay secondary (affordable, diverse, stable water); Sacramento tertiary (cost advantage, longer commute)
5. ✅ **School vaccination**: Critical action for Step 3 — direct calls to schools to verify exemption policies

---

## Data Quality Assurance

### **Confidence Levels**
- **HIGH**: Commutes (Google Maps), median prices (Zillow/Redfin), crime (FBI UCR), diversity (Census ACS)
- **MEDIUM**: Alternative school counts (need verification), community cohesion (proxy-based), property sizes (Redfin data varies)
- **GAPS**: Specific vaccination exemption policies (requires direct school calls), water district restrictions (need district confirmation), fire zone precision (CAL FIRE verification needed)

### **Deduplication**
- All 43 neighborhoods tracked in master scorecard
- No duplicates identified (all use Zillow/Redfin canonical boundaries)
- Coverage: 100% of identified neighborhoods in passing regions

---

## Neighborhoods Evaluated This Session

**Step 1 (6 regions)**:
- Sacramento & Central Valley, North Bay, East Bay, Peninsula & South Bay, Santa Cruz & Monterey, Central Coast

**Step 2 (43 neighborhoods)**:
- **East Bay/Alameda (8)**: Fremont, Pleasanton, Livermore, Dublin, Castro Valley, Alameda, Oakland Hills, Berkeley
- **East Bay/Contra Costa (7)**: San Ramon, Lafayette, Danville, Orinda, Pleasant Hill, Walnut Creek, Concord
- **Peninsula/San Mateo (9)**: Redwood City, San Carlos, Belmont, San Mateo, Foster City, Burlingame, Millbrae, Pacifica, Half Moon Bay
- **South Bay (8)**: Campbell, Los Gatos, Saratoga, Cupertino, Mountain View, Sunnyvale, Milpitas, Morgan Hill
- **San Jose Core (6)**: Willow Glen, Evergreen, Downtown SJ/SoFA, Rose Garden, Cambrian Park, Almaden Valley
- **Sacramento Valley (5)**: Folsom, El Dorado Hills, Roseville, Davis, Elk Grove

---

## Next Immediate Actions

1. ✅ **Commit Step 2 progress** (complete)
2. ⏳ **Launch Step 3 deep dives** (6 parallel agents for Tier A neighborhoods)
3. ⏳ **Expected completion**: 1–2 sessions for all Step 3 reports
4. ⏳ **Then**: Step 4 financial modeling, Step 5 ranking

---

## Timeline Projection

| Phase | Target | Status |
|-------|--------|--------|
| Step 1: Region Screening | 2026-06-22 | ✅ COMPLETE |
| Step 2: Neighborhood Scoring | 2026-06-22 | ✅ COMPLETE |
| Step 3: Deep Analysis | 2026-06-23 to 2026-06-24 | ⏳ PENDING |
| Step 4: Financial Modeling | 2026-06-24 to 2026-06-25 | ⏳ PENDING |
| Step 5: Final Ranking | 2026-06-25 | ⏳ PENDING |
| Step 6: Property Deep Dives | 2026-06-26 to 2026-06-27 | ⏳ PENDING |
| **Final Decision** | **2026-06-27 (target)** | ⏳ IN PROGRESS |

---

## Memory & Documentation

All findings committed to git:
- Commit: `a8ffa6e9` — Step 2 interim (32 neighborhoods)
- Commit: `a8ffa6e9` — Step 2 final (43 neighborhoods)
- Master scorecard: `runs/step2_neighborhood_scoring/neighborhood_scorecard_final.csv`
- Detailed reports: `runs/step2_neighborhood_scoring/step2_final_report.md`

