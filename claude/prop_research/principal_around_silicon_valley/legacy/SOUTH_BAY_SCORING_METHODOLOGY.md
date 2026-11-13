# South Bay Neighborhoods: Scoring Methodology (June 22, 2026)

## 11 Weighted Criteria

| Criterion | Weight | Scoring Basis | Range |
|-----------|--------|---------------|-------|
| **1. Jobs** (16%) | 16% | Commute to DTSJ + AI/ML job density within 30 min | 1-10 |
| **2. Schools** (13%) | 13% | GreatSchools district rating + alt school availability | 1-10 |
| **3. Growth** (12%) | 12% | 5-year appreciation % (higher = better) | 1-10 |
| **4. Safety** (11%) | 11% | Violent crime + property crime combined (lower = better) | 1-10 |
| **5. Diversity** (10%) | 10% | Simpson diversity index + % non-white population | 1-10 |
| **6. Price** (10%) | 10% | Median 3BR vs. $2M budget; lot size value | 1-10 |
| **7. Community** (9%) | 9% | Owner occupancy proxy, walkability, Brazilian/Persian presence | 1-10 |
| **8. Property** (6%) | 6% | Typical lot size for gardening/well feasibility | 1-10 |
| **9. Survivability** (6%) | 6% | Water reliability + growing zone + natural disaster risk | 1-10 |
| **10. Beach** (4%) | 4% | Drive time to Santa Cruz/Half Moon Bay swimmable beach | 1-10 |
| **11. Climate** (3%) | 3% | Wildfire zone, flood zone, earthquake risk, extreme heat | 1-10 |

## Scoring Rules Applied

### Score_Jobs (16% weight)
- **9-10**: < 25 min commute + 20k+ AI jobs within 30 min (Cupertino, Mountain View, Sunnyvale)
- **8**: 23-26 min commute + 5-10k AI jobs within 30 min (Campbell)
- **7**: 26-30 min commute + 2-5k AI jobs (Milpitas, Los Gatos)
- **6**: 28-35 min commute + moderate job density (Saratoga, Morgan Hill: penalized for distance)
- **4-5**: > 35 min commute or sparse jobs

### Score_Schools (13% weight)
- **8-9**: GreatSchools 8.5+, 3+ alternative schools nearby (Cupertino, Los Gatos, Saratoga)
- **7**: GreatSchools 7.5, 4+ alternative schools (Campbell, Mountain View, Sunnyvale)
- **6**: GreatSchools 7, 3 alternative schools (Milpitas, Morgan Hill)
- **Note**: Data confidence LOW for alternative schools; estimates based on private school prevalence in affluent areas

### Score_Growth (12% weight)
- **8**: > 20% appreciation (Los Gatos 22%, Saratoga 25%, Cupertino 20%)
- **7**: 15-20% appreciation (Campbell, Mountain View)
- **6**: 14-16% appreciation (Sunnyvale)
- **5-6**: < 15% appreciation (Milpitas, Morgan Hill)

### Score_Safety (11% weight)
- **9**: Violent crime < 1/1K + property crime < 15/1K (Saratoga: 0.4+5.87)
- **8**: Violent crime < 1.5/1K + property crime < 20/1K (Cupertino, Los Gatos)
- **7**: Violent crime < 1.5/1K + property crime < 20/1K (Morgan Hill)
- **6**: Violent crime 1-2/1K + property crime 18-26/1K (Sunnyvale)
- **5**: Violent crime < 3/1K + property crime > 25/1K (Mountain View, Campbell)
- **4**: Property crime > 30/1K (Milpitas)

### Score_Diversity (10% weight)
- **8**: Simpson > 0.65 + > 60% non-white + significant immigrant presence (Mountain View, Sunnyvale)
- **7**: Simpson 0.60-0.65 + 60-65% non-white (Campbell)
- **6**: Simpson 0.55-0.60 + 40-65% non-white (Los Gatos, Saratoga, Milpitas)
- **5**: Simpson < 0.55 + Asian-dominant (Cupertino 0.42 + 81% non-white, Saratoga 0.52 + 69% non-white)
- **4**: Simpson < 0.50 + limited diversity (Morgan Hill: high diversity index 0.71 but Hispanic-skewed, scores 8)

### Score_Price (10% weight)
- **7**: < $1.8M median 3BR; $2M buys 4BR+ (Milpitas $1.6M, Morgan Hill $1.55M)
- **6**: $1.8-2.0M median (Sunnyvale $1.8M, Mountain View $1.93M, Campbell $1.94M)
- **5**: $2.0-2.2M median (Cupertino $2.15M, Los Gatos $2.2M) — at/above budget median
- **4**: > $2.2M (Saratoga $2.5M+ — limited inventory in budget)

### Score_Community (9% weight)
- **7-8**: Owner-occupancy 70%+ + estimated active FB/Nextdoor groups + school-centric community (Los Gatos, Saratoga, Morgan Hill)
- **6**: Owner-occupancy 60-70% + good community signals (Cupertino, Campbell, Mountain View)
- **5**: Owner-occupancy 45-55% + more transient (Sunnyvale: 45.8% owner-occupied, 54.2% rentals; Milpitas 58.4%)

### Score_Property (6% weight)
- **8**: > 0.5 acres typical (Saratoga 0.5-1.0 acres = 30,000 sqft)
- **6**: 0.25-0.5 acres (Los Gatos 15,000 sqft)
- **5**: 0.12-0.25 acres (Campbell, Cupertino 8,000 sqft; sufficient for backyard but limited)
- **4**: < 0.12 acres (Mountain View, Sunnyvale, Milpitas: 5,227-7,840 sqft — dense development)

### Score_Survival (6% weight)
- **7**: Medium water risk + moderate earthquake + good growing zone (Los Gatos, Saratoga, Morgan Hill)
- **6**: Medium water risk + good soil/growing (Most neighborhoods)
- **5**: Medium-high water risk + Bay proximity (Milpitas, Mountain View, Sunnyvale)
- **5**: Medium water risk + well feasibility possible (Campbell, Cupertino)

### Score_Beach (4% weight)
- **7-8**: 35-45 min to Santa Cruz (Los Gatos, Saratoga)
- **6**: 45-55 min (Campbell, Morgan Hill)
- **5**: 50-60 min (Sunnyvale, Cupertino)
- **3-4**: 60+ min (Milpitas: farthest from beach)

### Score_Climate (3% weight)
- **8**: Elevated location, low flood risk, moderate earthquake (Saratoga, Los Gatos)
- **6**: Moderate risks across all hazards (Campbell, Cupertino, Mountain View, Sunnyvale, Morgan Hill)
- **5**: Bay/delta proximity increases flood risk (Milpitas)

## Weighted Total Calculation

**Formula**: (score_jobs × 0.16) + (score_schools × 0.13) + (score_growth × 0.12) + (score_safety × 0.11) + (score_diversity × 0.10) + (score_price × 0.10) + (score_community × 0.09) + (score_property × 0.06) + (score_survival × 0.06) + (score_beach × 0.04) + (score_climate × 0.03)

## Tier Classification

| Tier | Range | Meaning |
|------|-------|---------|
| **A** | ≥ 7.5 | Deep-dive candidate — strong across all dimensions |
| **B** | 6.0-7.4 | Strong contender — good balance, some trade-offs |
| **C** | 4.5-5.9 | Acceptable but not ideal — notable gaps |
| **D** | < 4.5 | Eliminated — significant deal-breaker(s) |

## Key Findings

### Best Overall Balance (Tier B)
1. **Los Gatos** (6.7): Best schools (8.5), highest safety (7), strong growth (8), but expensive ($2.2M median, price score 5)
2. **Saratoga** (7.0): Highest safety (9), best growth (8), largest lots (8), excellent schools (8.5), but very expensive ($2.5M+, price score 4)
3. **Cupertino** (6.9): Best jobs (9), excellent schools (8.5), good growth (8), but high cost ($2.15M, Asian-dominant, low diversity score 4)

### Mid-Tier Trade-offs (Tier C)
- **Mountain View** (6.5): Best jobs (9), good growth, tech hub, but lower safety (5), smaller lots (4), high water stress
- **Sunnyvale** (6.5): Very high jobs (9), decent growth, good diversity, but lower safety (6), small lots (4), transient community (45.8% owner-occupancy)
- **Morgan Hill** (6.3): Most affordable ($1.55M, highest owner-occupancy 71.8%), highest diversity index (0.71), but longest commute (34 min), fewer jobs (4)

### Eliminated (Tier D)
- **Campbell** (5.9): Mid-tier price ($1.94M), mid-tier jobs (8), but lower schools (7), lower safety (5), small lots (5)
- **Milpitas** (5.8): Most affordable ($1.6M), longest beach drive (60-70 min), highest crime (30.68 property crime/1K), lowest safety score (4)

## $2M Budget Implications

| Neighborhood | Median 3BR | $2M Buys | Status |
|---|---|---|---|
| Morgan Hill | $1.55M | Solid 3BR+, 10k sqft lot | **Well within budget** |
| Milpitas | $1.6M | Solid 3BR+, standard lot | **Well within budget** |
| Sunnyvale | $1.8M | 3BR+, small yard | **Well within budget** |
| Mountain View | $1.93M | 3BR+, very small lot | **Tight but feasible** |
| Campbell | $1.94M | 3BR+, small lot | **Tight but feasible** |
| Cupertino | $2.15M | Tight on 3BR; limited inventory | **Above median — risky** |
| Los Gatos | $2.2M | Tight on 3BR; limited inventory | **Above median — risky** |
| Saratoga | $2.5M+ | Sparse inventory at budget | **At/above budget ceiling — challenging** |

## Critical Flags

1. **$2M Budget Gap**: Saratoga, Los Gatos, Cupertino all have medians at or above $2M. Limited inventory below $2M in these areas.
2. **Water Stress**: All neighborhoods under Santa Clara Valley Water District (SCVWD) constraints. South county (Morgan Hill, Gilroy) more vulnerable to Colorado River cuts.
3. **Commute Variation**: 23-34 min range; Morgan Hill adds significant commute cost vs. tech hubs.
4. **Diversity Trade-off**: Tech hubs (Cupertino, Milpitas) are Asian-dominant (74%, 71%). Family seeking Persian/Brazilian presence may prefer Sunnyvale (60% non-white, diverse), Mountain View (67% non-white), or Morgan Hill (65% non-white Hispanic-plurality).
5. **Property Size**: Tech hubs have smallest lots (5k-8k sqft) — limits gardening/well feasibility. Saratoga offers most space (30k sqft typical).

## Recommended Deep Dives (Next Steps)

- **Tier A candidate (if available)**: Narrow gap between A and B; none currently qualify due to price-school trade-offs
- **Tier B Deep Dive Priority**: Los Gatos (best balance), Saratoga (safety premium), Cupertino (job density)
- **Tier C Value Play**: Morgan Hill (most affordable, best community, good diversity, long commute trade-off); Sunnyvale (best job density, diversity, but transient)
- **Skip (Tier D)**: Campbell, Milpitas (safety/crime concerns despite affordability)

---

**Scoring Date**: June 22, 2026
**Data Freshness**: 2024-2026 current
**Confidence**: HIGH for crime/pricing/commute data; MEDIUM for schools/appreciation/alternative schools; LOW for community signals (Nextdoor/FB estimates)
**Next Phase**: Step 3 Deep Dive on top 3 neighborhoods (Los Gatos, Saratoga, Cupertino)
