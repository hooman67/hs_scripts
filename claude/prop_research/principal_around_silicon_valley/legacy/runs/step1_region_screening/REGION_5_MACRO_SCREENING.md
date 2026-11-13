# Region 5 (Santa Cruz & Monterey Counties) — Macro Screening Assessment

**Screening Date**: June 22, 2026  
**Assessor**: Claude Code  
**Step**: 1 (Macro Screening for Deal-Breaker Criteria)

---

## DEAL-BREAKER CRITERIA ASSESSMENT

### Filter 1: Commute to DTSJ > 2.5 hours one-way (non-rush)

**Threshold**: > 150 minutes = FAIL  
**Data**:
- Santa Cruz (off-peak): ~45 minutes ✓ PASS
- Monterey (off-peak): ~75 minutes ✓ PASS

**Result**: PASS — Both locations comfortably below 2.5-hour threshold.

---

### Filter 2: Route Reliability = Fragile AND No Alternatives → FAIL

**Criterion**: Single fragile route with history of multi-day closures as ONLY option = automatic FAIL

**Analysis**:

#### Santa Cruz County
- **Primary route**: CA-17 (Highway 17)
- **Reliability**: FRAGILE
  - Single freeway crossing San Andreas Fault
  - Loma Prieta earthquake (1989): 50+ day closure
  - Frequent rockslides, landslides, fog-related accidents
  - No parallel freeway alternative
- **Alternative routes**: 2 available
  - CA-1 via Big Sur: 2+ hours longer, single-lane stretches, landslide-prone, not practical for daily commute
  - CA-152 to US-101: Mountain pass, adds 45+ minutes, historically reliable but not equivalent to freeway
- **Assessment**: FRAGILE + limited alternatives = SIGNIFICANT CONCERN
  - Technically has 2 alternatives (not zero)
  - But alternatives are impractical for daily 45-min commute pattern
  - Single-point-of-failure on CA-17 is real vulnerability
  - **Borderline on deal-breaker**: Technically PASS (has alternatives), but represents structural risk

#### Monterey County
- **Primary route**: US-101 (northbound)
- **Reliability**: MODERATE
  - Multiple merges, chronic congestion ("Joe Colla" area)
  - Pajaro River flooding risk (rare, 1-2 day closures historically)
  - CA-1 coastal section (landslide risk) provides secondary option
  - No single-point-of-failure like CA-17
- **Alternative routes**: 3 available
  - CA-152 Hecker Pass: Single-lane mountain pass, Pacheco Pass section unpredictable
  - CA-1 via Big Sur: Scenic, unreliable in winter/spring, landslide-prone
  - Local Salinas Valley arterials: Lower capacity but functional
- **Assessment**: MODERATE reliability + multiple alternatives = PASS
  - No single-point-of-failure
  - Reasonable redundancy

**Result**: 
- **Santa Cruz**: MARGINAL FAIL (Fragile + limited practical alternatives)
- **Monterey**: PASS (Moderate + multiple alternatives)

---

### Filter 3: Median Home Price > $2.5M → PASS

**Threshold**: Median > $2.5M = FAIL region (nothing in budget)  
**Data**:
- Santa Cruz County: $1,254,500 median ✓ PASS
- Monterey County: $968,000 median ✓ PASS

**Result**: PASS — Both counties well below $2.5M threshold.

---

### Filter 4: AI/ML Job Density < 50 Positions Within 60 Min → FAIL

**Threshold**: < 50 open positions = FAIL region  
**Data**:
- Santa Cruz (60-min radius): 12,000–15,000 positions ✓ PASS
- Monterey (60-min radius): 4,000–4,200 positions ✓ PASS

**Result**: PASS — Both counties massively above minimum threshold.

---

### Filter 5: Violent Crime Rate > 8 Per 1,000 → PASS

**Threshold**: > 8 per 1K = FAIL region  
**Data**:
- Santa Cruz County (2022): 4.10 per 1K ✓ PASS
- Monterey County (2022): 4.21 per 1K ✓ PASS

**Result**: PASS — Both counties well below crime threshold.

---

### Filter 6: Diversity (Index < 0.2 AND Non-white < 5%) → PASS

**Criterion**: Region-wide diversity index < 0.2 AND < 5% non-white = FAIL region  
**Data**:
- **Santa Cruz**:
  - Diversity Index: 0.7131 (71%) >> 0.2 ✓
  - % Non-white: 57.5% >> 5% ✓
- **Monterey**:
  - Diversity Index: 0.6822 (68%) >> 0.2 ✓
  - % Non-white: 61.8% >> 5% ✓

**Result**: PASS — Both counties highly diverse and inclusive.

---

### Filter 7: Water Supply Status = Critical → PASS

**Criterion**: Critical shortage or mandatory rationing likely = FAIL region  
**Data**:
- **Santa Cruz**: Stressed (seasonal) — 10–20% summer rationing typical
- **Monterey**: Chronic stress — 25–40% year-round rationing structural

**Threshold question**: What counts as "Critical"?
- CA DWR has formal drought levels: Moderate → Severe → Critical
- Neither county is currently in "Critical" official status (though Monterey approaches it functionally)
- Santa Cruz is in seasonal stress cycle
- Monterey has chronic structural deficit but not emergency-level rationing (yet)

**Interpretation**: Strictly speaking, neither triggers "Critical → automatic PASS" filter, because "Critical" in DWR terminology implies emergency-level shortage declarations.

**However**: Monterey's chronic stress is functionally concerning — it's a persistent condition, not a temporary drought phenomenon.

**Result**: TECHNICAL PASS (not "Critical" in DWR terminology), but **QUALITATIVE CONCERN** (especially Monterey).

---

## OVERALL MACRO SCREENING VERDICT

### Santa Cruz County

| Filter | Status | Reason |
|--------|--------|--------|
| Commute > 2.5 hrs | ✓ PASS | 45 min off-peak |
| Route reliability (Fragile + no alternatives) | ⚠ MARGINAL | CA-17 is fragile; only 2 impractical alternatives |
| Price > $2.5M | ✓ PASS | $1.25M median |
| Jobs < 50 within 60 min | ✓ PASS | 12K–15K positions |
| Crime > 8 per 1K | ✓ PASS | 4.10 per 1K |
| Diversity (low index + low minority %) | ✓ PASS | DI 0.71, 57% non-white |
| Water status = Critical | ✓ PASS | Stressed but not Critical |

**Summary**: Passes 6/7 filters cleanly; **MARGINAL on route reliability**.

**Recommendation**: CONDITIONAL PASS — Include Santa Cruz in Step 2 (neighborhood-level scoring), but **flag CA-17 vulnerability** as a key risk factor to weight in scoring rubric. Some specific neighborhoods (e.g., Aptos, Capitola) may have slightly better redundancy than Santa Cruz city proper.

---

### Monterey County

| Filter | Status | Reason |
|--------|--------|--------|
| Commute > 2.5 hrs | ✓ PASS | 75 min off-peak |
| Route reliability (Fragile + no alternatives) | ✓ PASS | US-101 is Moderate; 3 alternatives available |
| Price > $2.5M | ✓ PASS | $968K median |
| Jobs < 50 within 60 min | ✓ PASS | 4K–4.2K positions |
| Crime > 8 per 1K | ✓ PASS | 4.21 per 1K |
| Diversity (low index + low minority %) | ✓ PASS | DI 0.68, 62% non-white |
| Water status = Critical | ✓ PASS | Chronic stress but not formally Critical |

**Summary**: Passes all 7 filters cleanly.

**Recommendation**: PASS — Include Monterey in Step 2 (neighborhood-level scoring). **Note water stress as a qualitative factor** but not a disqualifying deal-breaker.

---

## FINAL MACRO SCREENING RESULT

| Region | Overall Result | Recommendation | Key Caveats |
|--------|----------------|----------------|-------------|
| Region 5: Santa Cruz | CONDITIONAL PASS | Proceed to Step 2 | CA-17 route fragility is significant risk; flag in scoring |
| Region 5: Monterey | PASS | Proceed to Step 2 | Chronic water stress; qualitative concern but not deal-breaker |

**Conclusion**: Region 5 advances to Step 2 neighborhood-level scoring with two separate county-level assessments.

- **Santa Cruz**: Higher route risk, higher prices, more AI jobs
- **Monterey**: Better route reliability, lower prices, lower jobs, worse water outlook

Both are viable for detailed analysis.

---

## NEXT STEPS

### Step 2: Neighborhood Identification & Scoring

**Santa Cruz County neighborhoods to evaluate:**
1. Santa Cruz (city, north/south)
2. Capitola
3. Scotts Valley
4. Aptos
5. Watsonville

**Monterey County neighborhoods to evaluate:**
1. Monterey (city)
2. Pacific Grove
3. Seaside
4. Marina
5. Salinas (main city; higher crime but urban center)
6. Carmel Valley

**Scoring rubric**: Apply all 11 weighted criteria to each neighborhood, taking into account:
- CA-17 fragility (penalty to Santa Cruz neighborhoods on Route Reliability criterion)
- Water stress (penalty to Monterey neighborhoods on Survivability criterion)
- AI job proximity (advantage to Santa Cruz, advantage to northern Monterey)
- Commute time variance (Aptos/Capitola may have longer commutes than Santa Cruz city)
- Specific school options, diversity, walkability by city

**Expected output**: Neighborhood scorecard with all 11 weighted scores per neighborhood; tier into A/B/C/D.

---

**End of Macro Screening Assessment**
