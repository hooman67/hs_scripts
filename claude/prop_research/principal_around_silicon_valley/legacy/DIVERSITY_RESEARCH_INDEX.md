# Sacramento Valley Census Diversity Metrics — Research Index
## Complete Research Package (June 22, 2026)

**Research Period**: 2020–2023 Census Data  
**Jurisdictions**: Sacramento County, Folsom CA, Roseville CA, Placer County  
**Research Objective**: Gather comprehensive diversity metrics for property research Step 2 (Neighborhood Scoring)  
**Research Status**: COMPLETE (Regional analysis); PENDING (Neighborhood-level follow-up)

---

## Documents in This Research Package

### 1. **census_diversity_research.md** — MAIN REPORT
**Purpose**: Complete demographic breakdown and Simpson Diversity Index calculations  
**Contents**:
- Executive summary
- Methodology (SDI formula, interpretation guide)
- 2020 Census data for all four jurisdictions
- 2023 ACS estimates (partial, provisional)
- Demographic trends (2020–2023)
- Comparative analysis and rankings
- Data quality assessment
- Community presence assessments (Persian/Brazilian)
- Citations and sources
- Full demographic tables in appendix

**Length**: ~1,500 lines  
**Use For**: Understanding regional diversity context; Step 1 region filtering; Step 2 regional comparison  
**Key Finding**: Sacramento County (SDI 0.711) significantly more diverse than Folsom (0.582), Roseville (0.553), Placer (0.456)

**Format**: Markdown (detailed)  
**Read Time**: 30–45 minutes (full); 5 minutes (summary sections)

---

### 2. **diversity_metrics_summary.csv** — QUICK REFERENCE TABLE
**Purpose**: One-row-per-jurisdiction summary for quick lookups and spreadsheet inclusion  
**Contents**:
- SDI 2020 and 2023 estimates
- Non-white percentages
- Racial/ethnic breakdown (all categories)
- Diversity tier classification
- Data confidence ratings
- Community presence assessments

**Columns**: Jurisdiction, SDI_2020, SDI_2023_Est, Non_White_Pct_2020, ... [17 columns total]  
**Format**: CSV (can import to Excel, Google Sheets, or neighborhood_scorecard.csv)  
**Use For**: Comparative tables, spreadsheet inclusion, quick data lookups

**Integration**: Copy-paste into `neighborhood_scorecard.csv` (Step 2) as reference columns

---

### 3. **diversity_data_crosscheck.md** — VERIFICATION & QUALITY ASSURANCE
**Purpose**: Data validation, cross-checks, confidence assessment, limitations documentation  
**Contents**:
- Census totals verification (all four jurisdictions)
- SDI calculations cross-checked (all four)
- Alternative diversity measures (HHI) validation
- Trend analysis validation
- Data quality assessment by jurisdiction
- Methodological considerations
- Sources requiring verification (checklist)
- Interpretation guide for property scoring
- How to use documents in research pipeline

**Length**: ~800 lines  
**Use For**: Understanding data quality and confidence levels; troubleshooting data discrepancies; documenting limitations  
**Key Message**: 2020 Census data HIGH confidence; 2023 ACS MEDIUM confidence; Persian/Brazilian assessments REQUIRE VERIFICATION

**Format**: Markdown (technical, but accessible)  
**Read Time**: 15–20 minutes

---

### 4. **diversity_research_nextactions.md** — ACTION ITEMS & FOLLOW-UP TASKS
**Purpose**: Detailed roadmap for neighborhood-level research (Priorities 1–7)  
**Contents**:
- Priority 1: Census tract-level deep dive (CRITICAL)
- Priority 2: Persian/Brazilian community ground-truthing
- Priority 3: Sanctuary status verification
- Priority 4: Hate crime history research
- Priority 5: School district diversity analysis
- Priority 6: Community organization mapping
- Priority 7: Political climate assessment
- Implementation timeline (5-week execution plan)
- Integration with main research document
- Success criteria and follow-up questions

**Length**: ~1,000 lines  
**Estimated Effort**: 14–20 hours total follow-up research  
**Use For**: Next phase of property research (immediately after this research package); detailed task checklists  
**Key Message**: Census tract analysis is CRITICAL — don't skip; estimated 2–3 hours per priority

**Format**: Markdown (action-oriented)  
**Read Time**: 10–15 minutes (skimming); 30 minutes (detailed planning)

---

### 5. **diversity_quick_reference.txt** — ONE-PAGE SUMMARY
**Purpose**: Single-page visual summary for quick scanning and briefings  
**Contents**:
- Key finding (one sentence)
- SDI summary table (highest to lowest diversity)
- Demographic breakdown tables (all four jurisdictions)
- Comparative rankings
- Data quality assessment
- Property research implications (diversity scoring 1–10)
- Next actions (priority order)
- Research documents summary
- Notes for property research

**Length**: ~300 lines (single page when printed)  
**Use For**: Quick reference during meetings, briefings, decision-making  
**Key Message**: "Sacramento County is significantly more diverse; Placer County least diverse"

**Format**: Plain text (ASCII formatting for readability)  
**Read Time**: 3–5 minutes

---

### 6. **diversity_research_methodology.md** — TECHNICAL DOCUMENTATION
**Purpose**: Complete research methodology, data sources, confidence frameworks, limitations  
**Contents**:
- Research objective and overview
- Five-phase methodology (identification, compilation, processing, supplementary, QA)
- Data sources hierarchy and citations
- Simpson Diversity Index technical documentation (formula, advantages, limitations)
- Step-by-step data processing example (Sacramento County)
- Confidence level assignment framework (methodology and application)
- Known limitations and caveats (6 major categories)
- Recommendations for appropriate/inappropriate uses
- Recommendations for next research phases
- References and further reading
- Document revision protocol

**Length**: ~900 lines  
**Use For**: Transparency about research methodology; peer review; reproduction of analysis; understanding confidence levels  
**Key Message**: "High confidence in 2020 Census; medium confidence in 2023 ACS; Persian/Brazilian assessments require field verification"

**Format**: Markdown (technical)  
**Read Time**: 20–30 minutes

---

### 7. **DIVERSITY_RESEARCH_INDEX.md** — THIS FILE
**Purpose**: Navigation guide for the entire research package  
**Contents**: Document descriptions, use cases, integration points, reading guide

**Use For**: Understanding what's in the package and which document to read for your needs

---

## How to Use This Research Package

### For Different Audiences:

**If you're Hooman (property research project lead):**
1. Start: Read `diversity_quick_reference.txt` (3 min) — get the headline numbers
2. Understand: Read executive summary of `census_diversity_research.md` (10 min)
3. Act: Review `diversity_research_nextactions.md` and start Priority 1 (Census tracts)
4. Reference: Use `diversity_metrics_summary.csv` in your neighborhood_scorecard.csv

**If you're someone new to the project:**
1. Start: Read `DIVERSITY_RESEARCH_INDEX.md` (this file) (3 min)
2. Overview: Read `diversity_quick_reference.txt` (5 min)
3. Deep dive: Read `census_diversity_research.md` main sections (30 min)
4. Questions: Reference `diversity_data_crosscheck.md` for methodology (10 min)

**If you're peer-reviewing this research:**
1. Methodology: Read `diversity_research_methodology.md` (30 min)
2. Data: Verify calculations in `census_diversity_research.md` (30 min)
3. Quality: Review `diversity_data_crosscheck.md` (20 min)
4. Assess: Check confidence levels and limitations (10 min)

**If you're updating this research in 2027:**
1. Template: Use `diversity_research_methodology.md` section "Document Revision Protocol"
2. Data: Re-run collections per Priority 1–7 in `diversity_research_nextactions.md`
3. Comparison: Use 2020 baseline from `census_diversity_research.md` tables
4. Update: Create new dated file (`census_diversity_research_2027-XX-XX.md`) and archive old

---

## Integration with Property Research Pipeline

### Step 1: Region Screening (Already Passed)
**Use**: `diversity_metrics_summary.csv` — compare SDI to other regions  
**Data Point**: Sacramento County SDI 0.711 rates HIGH on diversity criterion

### Step 2: Neighborhood Scoring (CURRENT STEP)
**Use**: 
- `census_diversity_research.md` — regional baseline
- `diversity_metrics_summary.csv` — copy diversity scores to neighborhood_scorecard.csv
- `diversity_research_nextactions.md` Priority 1 — download Census tract data for neighborhoods

**Implementation**:
1. Complete Priority 1 (Census tract analysis) — 2–3 hours
2. Identify top 5–10 most diverse neighborhoods in each jurisdiction
3. Score each neighborhood 1–10 on diversity criterion
4. Incorporate tract-level SDI and community assessment into scoring

### Step 3: Deep Neighborhood Analysis (Future)
**Use**: 
- Complete Priorities 2–7 from `diversity_research_nextactions.md`
- Verify Persian/Brazilian community presence (Priority 2)
- Confirm sanctuary status (Priority 3)
- Research hate crime history (Priority 4)
- Analyze school diversity (Priority 5)
- Map community organizations (Priority 6)
- Assess political climate (Priority 7)

**Deliverable**: Community cultural fit report per neighborhood (Tier A only)

### Step 4–6: Financial & Final Analysis
**Use**: Diversity scores from Step 2 in weighted scoring algorithm  
**Weighting**: Diversity = 10% of total neighborhood score

---

## Data Quality Summary

| Aspect | Status | Confidence | Notes |
|--------|--------|-----------|-------|
| 2020 Census counts | Complete | HIGH | Official decennial census; 6 years old |
| 2023 ACS estimates | Partial | MEDIUM | Rolling estimates; final data Q1 2025 |
| SDI calculations | Verified | HIGH | All four recalculated and cross-checked |
| Regional comparison | Verified | HIGH | Sacramento vs. Folsom/Roseville/Placer valid |
| Trend analysis | Verified | HIGH | Hispanic growth consistent across all four |
| Persian community | Qualitative | LOW | Requires ground-truthing (Priority 2) |
| Brazilian community | Qualitative | LOW | Requires ground-truthing (Priority 2) |
| Sanctuary status | Partial | MEDIUM | Sacramento County confirmed; others pending |
| Hate crime data | Not researched | N/A | Priority 4 follow-up needed |

---

## Key Findings (Summary)

1. **Regional Diversity Gradient**: Sacramento County (0.711) >> Roseville (0.553) > Folsom (0.582) > Placer (0.456)
   - *Implication*: Sacramento County most welcoming for diverse family; Placer least

2. **Non-White Populations**: Sacramento 58.5% > Folsom 39.2% > Roseville 35.8% >> Placer 28.8%
   - *Implication*: Only Sacramento County majority-minority; others predominantly white

3. **Growth Trends**: Hispanic and Asian growth consistent across all four (2020–2023)
   - *Implication*: All communities experiencing increasing diversity

4. **Persian/Brazilian Presence**: Only significant in Sacramento County (regional); minimal/absent in suburbs
   - *Implication*: Suburbs may require active search to find cultural community

5. **Sanctuary Status**: Only Sacramento County confirmed sanctuary (2017); others unconfirmed
   - *Implication*: Critical factor for immigration comfort; requires verification for others

---

## Files Checklist

Use this to verify you have all documents:

```
✓ census_diversity_research.md (1,500 lines; main report)
✓ diversity_metrics_summary.csv (4 data rows; quick reference)
✓ diversity_data_crosscheck.md (800 lines; verification)
✓ diversity_research_nextactions.md (1,000 lines; follow-up tasks)
✓ diversity_quick_reference.txt (300 lines; one-page summary)
✓ diversity_research_methodology.md (900 lines; technical docs)
✓ DIVERSITY_RESEARCH_INDEX.md (this file; navigation guide)
```

**Total Package Size**: ~5,500 lines of documentation + 4 data rows  
**Total Content**: 6–8 hours of reading (if comprehensive); 30 min if skimming key sections

---

## Next Steps Checklist

**Immediate (This Week):**
- [ ] Read `diversity_quick_reference.txt` (get headlines)
- [ ] Read executive summary of `census_diversity_research.md`
- [ ] Share findings with family / co-decision-makers
- [ ] Confirm these are the four target jurisdictions (or modify scope)

**Short Term (Next 2 Weeks):**
- [ ] Complete Priority 1: Census tract deep dive (start `diversity_research_nextactions.md`)
- [ ] Download Census tract data for each jurisdiction
- [ ] Calculate tract-level SDI for neighborhoods
- [ ] Identify top 5–10 most diverse neighborhoods per city

**Medium Term (Weeks 3–4):**
- [ ] Complete Priorities 2–4 (Community presence, sanctuary status, hate crime)
- [ ] Verify Persian/Brazilian community presence
- [ ] Confirm sanctuary city/county status
- [ ] Research hate crime history

**Integration (End of Month):**
- [ ] Update `neighborhood_scorecard.csv` (Step 2) with diversity data
- [ ] Incorporate tract-level SDI into scoring algorithm
- [ ] Assign diversity scores (1–10) to neighborhoods
- [ ] Identify Tier A candidates based on diversity + other criteria

---

## Contact & Questions

**Research Conducted By**: Claude Research Agent  
**Research Date**: June 22, 2026  
**Questions About Data**: See `diversity_research_methodology.md` and `diversity_data_crosscheck.md`  
**Questions About Next Steps**: See `diversity_research_nextactions.md` (Priorities 1–7)

---

## Document Version History

| File | Version | Date | Status |
|------|---------|------|--------|
| census_diversity_research.md | 1.0 | 2026-06-22 | COMPLETE |
| diversity_metrics_summary.csv | 1.0 | 2026-06-22 | COMPLETE |
| diversity_data_crosscheck.md | 1.0 | 2026-06-22 | COMPLETE |
| diversity_research_nextactions.md | 1.0 | 2026-06-22 | COMPLETE |
| diversity_quick_reference.txt | 1.0 | 2026-06-22 | COMPLETE |
| diversity_research_methodology.md | 1.0 | 2026-06-22 | COMPLETE |
| DIVERSITY_RESEARCH_INDEX.md | 1.0 | 2026-06-22 | COMPLETE |

---

## Archive & Maintenance

**How to Archive Old Research** (when updating in future):
1. Rename: `census_diversity_research.md` → `census_diversity_research_archived_2026-06-22.md`
2. Create: New `census_diversity_research.md` with fresh 2027+ data
3. Update: This index file with version history
4. Keep: Archived files in same directory for historical reference

**Retention Policy**: Keep all versions indefinitely for audit trail and re-trending

---

**END OF RESEARCH INDEX**

---

For questions or issues with this research package, refer to the specific methodology document or contact the research team.

Last Updated: June 22, 2026  
Research Status: COMPLETE (Regional Analysis) | PENDING (Neighborhood Follow-up)  
Next Milestone: Complete Priority 1 census tract analysis by end of week
