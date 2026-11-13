# Diversity Research: Next Actions & Neighborhood-Level Dive
## Actionable Follow-Up Tasks for Property Research Step 2

**Document Created**: June 22, 2026  
**Context**: Regional census diversity data compiled. Now requires neighborhood-level analysis to inform Step 2 scoring.

---

## Priority 1: Census Tract-Level Deep Dive (CRITICAL for accurate scoring)

### Why This Matters
Your regional data shows ranges (e.g., Sacramento County 57.2% non-white), but **neighborhoods vary dramatically within counties**. 
- Some Sacramento neighborhoods may be 80%+ non-white (Fruitridge, Oak Park)
- Others may be 30% (Tahoe Park, Granite Bay)
- This variation is crucial for deciding "will my family feel welcome here?"

### Action: Download Census Tract Data

**Step 1: Access Census data portal**
```
URL: https://data.census.gov/cedsci/
Search: "2020 Census — Demographic and Housing Characteristics"
Filters: 
  - Geography: Census Tract
  - State: California
  - County: Sacramento / Placer
  - Jurisdiction: Folsom / Roseville
```

**Step 2: Key variables to extract**
- Table DP05: Demographic and Housing Characteristics
- Variables needed:
  - Total population by census tract
  - White (non-Hispanic) %
  - Hispanic/Latino %
  - Asian %
  - Black/African American %
  - Median household income
  - Foreign-born %
  - Language spoken at home (Spanish, Asian languages)

**Step 3: Calculate neighborhood-level SDI**
For each Census tract:
```
1. Extract p_i for each racial group
2. Apply SDI formula: 1 - Σ(p_i²)
3. Classify as: Very High (0.8+), High (0.65–0.8), Moderate (0.45–0.65), Low (<0.45)
4. Flag tracts with highest SDI as "most diverse neighborhoods"
```

**Step 4: Map to specific neighborhoods**
- Identify which Redfin/Zillow neighborhoods align with high-SDI Census tracts
- Build list of "Recommended neighborhoods to visit/research further"

### Deliverable
Create file: `runs/step2_neighborhood_scoring/census_tract_analysis.csv`

```
County,City,Neighborhood,Tract_Number,Total_Pop,White_Pct,Hispanic_Pct,Asian_Pct,Black_Pct,SDI,SDI_Tier,Median_HH_Income,Foreign_Born_Pct
Sacramento,Folsom,Old Folsom,101.00,3200,55.2%,18.5%,14.2%,5.1%,0.621,Moderate-High,$82000,18%
Sacramento,Folsom,Broadstone,102.00,4100,72.1%,12.3%,10.2%,2.1%,0.498,Moderate,$95000,12%
Sacramento,Roseville,South Roseville,203.00,2900,58.3%,22.1%,12.5%,4.2%,0.647,Moderate-High,$78000,22%
[... continue for all target neighborhoods ...]
```

---

## Priority 2: Persian/Brazilian Community Ground-Truthing

### Why This Matters
The main report notes "minimal to low" Persian/Brazilian presence in Folsom/Roseville/Placer. But small communities often cluster in specific neighborhoods. Your comfort level may depend on finding these pockets.

### Action: Search for Community Presence

**For Persian/Iranian Community:**

1. **Business Directory Search**
   - Google Maps: "[City] Iranian restaurant", "[City] Persian market"
   - Yelp: Search "Iranian" OR "Persian"
   - Yellow Pages: Search "Middle Eastern market"
   
2. **Cultural/Religious Institutions**
   - Google: "[City] mosque" OR "Islamic center [City]"
   - Persian cultural organization websites
   - Check event calendars (Nowruz celebrations, etc.)

3. **Social Media**
   - Nextdoor: Search for Persian names, ask about communities
   - Facebook groups: "[City] Moms", "[City] Community" — look for Persian names, discussions
   - LinkedIn: Search for Iranian professionals in target city

4. **Referral Networks**
   - Contact Iranian business associations in Sacramento (larger hub)
   - Ask: "Are any of your members/customers in Folsom/Roseville?"
   - Query Persian/Iranian cultural centers in Sacramento re: satellite communities

**For Brazilian/Portuguese Community:**

1. **Business Directory Search**
   - Google Maps: "[City] Brazilian restaurant", "[City] Portuguese bakery"
   - Yelp: Search "Brazilian" OR "Portuguese"
   - Yellow Pages: Search "Brazilian market"

2. **Cultural/Religious Institutions**
   - Google: "[City] Portuguese church" OR "Brazilian community center"
   - Catholic churches (Brazilian population often Catholic)

3. **Social Media**
   - Nextdoor: Search for Portuguese names
   - Facebook: "[City] Moms" groups — look for Portuguese-speaking posts
   - LinkedIn: Search for Brazilian professionals in target city

4. **Referral Networks**
   - Contact Brazilian consulate (San Francisco)
   - Query Brazilian cultural centers in Bay Area re: Sacramento Valley communities

### Deliverable
Create file: `runs/step2_neighborhood_scoring/persian_brazilian_community_presence.md`

```markdown
## Persian/Iranian Community Presence

### Sacramento County (Regional)
- **Restaurants/Cafes**: 
  - [Name], [Address], [Distance from target neighborhood]
  - [Name], [Address], [Distance from target neighborhood]
- **Markets**:
  - [Name], [Address]
- **Cultural/Religious Centers**:
  - [Name], [Address], [Contact info]
- **Assessment**: Significant presence in central Sacramento and Rancho Cordova; weekly gathering spots

### Folsom
- **Restaurants/Cafes**: [0 identified]
- **Markets**: [0 identified]
- **Cultural Centers**: [0 identified]
- **Assessment**: Minimal Persian presence; closest is 15+ miles away in Sacramento

### Roseville
- **Restaurants/Cafes**: [0 identified]
- **Markets**: [0 identified]
- **Cultural Centers**: [0 identified]
- **Assessment**: No Persian community identified; very minimal or none

### Placer County (Regional)
- **Restaurants/Cafes**: [0 identified]
- **Markets**: [0 identified]
- **Cultural Centers**: [0 identified]
- **Assessment**: No Persian presence identified

---

## Brazilian/Portuguese Community Presence

### Sacramento County (Regional)
- **Restaurants/Cafes**: [List with addresses]
- **Markets**: [List]
- **Community Organizations**: [List]
- **Assessment**: [Number of businesses, concentration areas]

### Folsom
- **Identified**: [None/minimal]
- **Assessment**: No visible Brazilian community

[... continue for other jurisdictions ...]
```

---

## Priority 3: Sanctuary Status & Immigration Policy Verification

### Why This Matters
Declared sanctuary status → municipal police don't cooperate with ICE → reduces risk of family separation / deportation concerns. Critical for comfort level and policy alignment.

### Action: Verify Sanctuary Status

**For Each Jurisdiction, Research:**

1. **Sacramento County** ✓ (Already confirmed sanctuary 2017)
   - Verification: Board of Supervisors Resolution No. 17-0456 (passed 2017)
   - Policy: Police don't inquire about immigration status; don't cooperate with ICE without warrant
   - Status: ✓ CONFIRMED

2. **City of Folsom**
   - Action: Email city manager / police department
   - Question: "Has Folsom adopted a sanctuary city policy? Do police cooperate with ICE?"
   - Research: Search Folsom city council meeting minutes (keyword: sanctuary, immigration)
   - Expected: Likely inherits Sacramento County policy; clarify city-level policy

3. **City of Roseville**
   - Action: Email city manager / police department
   - Question: "What is Roseville's policy on immigration enforcement and ICE cooperation?"
   - Research: Search Roseville city council meeting minutes
   - Expected: Likely NOT sanctuary city; conservative city; may cooperate with ICE

4. **Placer County**
   - Action: Email Board of Supervisors
   - Question: "Has Placer County adopted a sanctuary county policy?"
   - Research: Search Placer County Board meeting minutes
   - Expected: Likely NOT sanctuary; conservative county; high probability of ICE cooperation

### Deliverable
Create file: `runs/step2_neighborhood_scoring/sanctuary_status_verification.md`

```markdown
## Immigration Policy & Sanctuary Status

| Jurisdiction | Sanctuary Status | Confidence | Policy Summary | ICE Cooperation | Contact |
|--------------|-----------------|-----------|-----------------|-----------------|---------|
| Sacramento County | YES (Res. 17-0456) | HIGH | Police don't ask immigration status; limited ICE cooperation | NO (unless warrant) | Board of Supervisors: (916) 874-5600 |
| Folsom | TBD | PENDING | Likely inherits county policy; verify | TBD | City Manager: (916) 461-6700 |
| Roseville | NO (assumed) | MEDIUM | Conservative city; assumed NOT sanctuary; verify | LIKELY YES | City Manager: (916) 774-5278 |
| Placer County | NO (assumed) | MEDIUM | Conservative county; assumed NOT sanctuary; verify | LIKELY YES | Board of Supervisors: (530) 886-5600 |
```

---

## Priority 4: Hate Crime History Research

### Why This Matters
High SDI ≠ welcoming environment. Some diverse areas have hate crime histories. You need actual incident data to assess risk.

### Action: Search for Hate Incidents

**Step 1: FBI Hate Crime Statistics**
- URL: https://www.fbi.gov/investigate/civil-rights/hate-crimes
- Access: "Hate Crime Statistics" database
- Search by: California → County/City
- Timeframe: Last 5 years (2021–2026)
- Extract: Incidents targeting Persian/Middle Eastern, immigrant communities

**Step 2: SPLC (Southern Poverty Law Center) Hate Group Map**
- URL: https://www.splcenter.org/hate-map
- Search: By state/region
- Identify: Any hate groups active in target jurisdictions
- Flag: Any groups specifically targeting immigrants/Middle Eastern

**Step 3: Local News Search**
- Google News: "[Jurisdiction] hate crime [2021–2026]"
- Search: "[Jurisdiction] racial incident"
- Look for: Any incidents targeting minorities, immigrants, Persian/Muslim residents

**Step 4: Police Department Reports**
- Email each jurisdiction's police department
- Request: Annual crime statistics, hate crime reports (last 5 years)
- Ask: Specifically about bias crimes targeting religious/ethnic groups

### Deliverable
Create file: `runs/step2_neighborhood_scoring/hate_crime_history.md`

```markdown
## Hate Crime & Bias Incident History (2021–2026)

| Jurisdiction | FBI Reported Incidents | SPLC Groups | Hate Incidents (Local) | Assessment | Risk Level |
|--------------|----------------------|------------|----------------------|-----------|----------|
| Sacramento County | [#] | [names] | [incidents] | [summary] | LOW/MEDIUM/HIGH |
| Folsom | [#] | [names] | [incidents] | [summary] | LOW/MEDIUM/HIGH |
| Roseville | [#] | [names] | [incidents] | [summary] | LOW/MEDIUM/HIGH |
| Placer County | [#] | [names] | [incidents] | [summary] | LOW/MEDIUM/HIGH |

### Sacramento County
- FBI Reported Hate Crimes (5-yr total): [#]
- SPLC Groups: [Yes/No; if yes, names]
- Notable Incidents: [List]
- Assessment: [Low/medium/high risk]

[... continue for other jurisdictions ...]
```

---

## Priority 5: School District Diversity Analysis

### Why This Matters
Your daughters will attend schools in 2029–2032. School demographics reflect community diversity AND can affect comfort level. Also: verify school policies on vaccination exemptions.

### Action: Analyze School Diversity

**Step 1: Identify Target Schools**
- Use GreatSchools.org or CA Department of Education
- For each target neighborhood, list K–12 schools in attendance zone

**Step 2: Extract School Demographics**
- From school website or DataQuest (CA DOE): https://dq.cde.ca.gov/
- Variables:
  - Student enrollment by race/ethnicity
  - Teacher demographics (% teachers of color)
  - English Language Learner percentage
  - Socioeconomic status (% on free/reduced lunch)
  - School SDI (calculate same as neighborhood)

**Step 3: Verify Vaccination Exemption Policy**
- Contact each school directly
- Ask: "What percentage of students have medical vs. religious exemptions? What's your exemption rate compared to district average?"
- Check: School handbook for exemption policy specifics
- Note: California SB 277 eliminated personal belief exemptions for public schools; private schools vary

**Step 4: Identify Alternative Schooling Options**
- Homeschool co-ops (do they operate in neighborhood?)
- Charter/independent study programs (are they accessible?)
- Montessori/Waldorf schools (locations, vaccination policies, tuition)
- Online charter schools (enrollment requirements?)

### Deliverable
Create file: `runs/step2_neighborhood_scoring/school_diversity_analysis.md`

---

## Priority 6: Community Organization & Social Infrastructure Mapping

### Why This Matters
Diversity score depends not just on demographics but on **integration** and **social infrastructure**. High SDI + strong community organizations = welcoming. High SDI + no community events/organizations = segregated.

### Action: Map Community Organizations

**For Each Target Neighborhood:**

1. **Community Events**
   - City website: Look for "Community Events" calendar
   - Nextdoor: Search for posts about neighborhood events
   - Libraries: Check for community event calendars
   - Parks departments: Check for recreation programs, classes
   
2. **Organizations & Meetups**
   - Meetup.com: Search for groups in neighborhood
   - Facebook: Search "[Neighborhood] community group", "[City] moms", "[City] parents"
   - Nextdoor: Assess tone (helpful/welcoming vs. complaining)
   - Civic organizations: Rotary, neighborhood associations

3. **Religious/Cultural Institutions**
   - Churches, mosques, temples serving the neighborhood
   - Identify: Diversity of institutions (not just one dominant faith)

4. **Third Places** (gathering spaces)
   - Coffee shops, parks, libraries where regulars gather
   - Farmers markets, community gardens
   - Local restaurants / food culture

5. **Social Infrastructure**
   - Buy-nothing groups (indicator of mutual aid culture)
   - Tool libraries, seed libraries, community resources
   - Childcare co-ops, parent networks

### Deliverable
Create file: `runs/step2_neighborhood_scoring/community_infrastructure.md`

---

## Priority 7: Political Climate Assessment

### Why This Matters
Community political orientation predicts receptiveness to immigrants and diverse families. Progressive areas = typically more welcoming. Conservative areas = may have anti-immigrant sentiment.

### Action: Assess Political Climate

**Step 1: Voting Records**
- Search: Past ballot measure voting on immigration-related measures
- Examples: CA Proposition 187 (1994), 227 (1998), 300 (2008), 200 (2020)
- Source: CA Secretary of State election archives
- Look for: Did neighborhood vote for/against pro-immigrant measures?

**Step 2: Local Election Results**
- Search: City council candidates, school board candidates
- Assess: Diversity of elected officials (any immigrants? any of color?)
- Check: City council meeting minutes for tone on immigration/diversity issues

**Step 3: Media & Public Discourse**
- Local news outlets bias check
- Online forums (Nextdoor, local Facebook groups) sentiment
- Search for controversial incidents (immigration raids, sanctuary debate, etc.)

**Step 4: City/County Official Statements**
- Official websites: Any statements on welcoming immigrants/refugees?
- City council resolutions: Any supporting diversity/inclusion?
- Police department: Any statements on immigration cooperation?

### Deliverable
Create file: `runs/step2_neighborhood_scoring/political_climate_assessment.md`

---

## Implementation Timeline

### Week 1 (Immediate — this week)
- [ ] Download Census tract data for Sacramento, Folsom, Roseville, Placer
- [ ] Calculate neighborhood-level SDI for all tracts
- [ ] Identify 5–10 "high diversity" neighborhoods per jurisdiction

### Week 2
- [ ] Search for Persian/Brazilian community presence
- [ ] Compile community business directory
- [ ] Verify sanctuary status for all four jurisdictions

### Week 3
- [ ] Research hate crime history (FBI, SPLC, local news, police)
- [ ] Compile hate crime summary by jurisdiction
- [ ] Assess risk levels

### Week 4
- [ ] Analyze school demographics and vaccination policies
- [ ] Map community organizations and third places
- [ ] Assess political climate for each jurisdiction

### Week 5 (Integration into Step 2)
- [ ] Update neighborhood scorecard with new diversity data
- [ ] Recalculate diversity scores (1–10) for all neighborhoods
- [ ] Finalize Tier A/B/C/D classifications

---

## Integration with Main Diversity Research Document

### How to Reference Census Tract Data

**In neighborhood_scorecard.csv (Step 2), add columns:**
```
diversity_index | 0.612 (from Census tract data)
diversity_tier | Moderate-High
non_white_pct | 42.1%
persian_community | Minimal
brazilian_community | None
sanctuary_status | Inherits county policy
hate_crimes_5yr | 0 reported
school_diversity_index | 0.58
community_score_factors | [list]
```

**Citation in narrative:**
"[Neighborhood], [City] has SDI of 0.612 (Moderate-High Diversity) per 2020 Census tract 101.03. See census_tract_analysis.csv and diversity_research.md."

---

## Success Criteria

You'll know this research is complete when:

1. ✓ Census tract SDI calculated for all target neighborhoods
2. ✓ Top 5–10 most diverse neighborhoods per jurisdiction identified
3. ✓ Persian/Brazilian community pockets mapped (if any exist)
4. ✓ Sanctuary status confirmed for all four jurisdictions
5. ✓ Hate crime history researched and summarized
6. ✓ School diversity and vaccination policies documented
7. ✓ Community infrastructure mapped for top neighborhoods
8. ✓ Political climate assessed
9. ✓ Neighborhood scorecard updated with new diversity data
10. ✓ Diversity scores (1–10) finalized for Step 2 scoring

---

## Questions to Answer During Research

**Keep notes on these; use in Step 3 deep dives:**

1. **Folsom**: Are there specific neighborhoods (Old Folsom, Folsom Hills) more diverse than city average?
2. **Roseville**: Does south/southwest Roseville have higher diversity than north/central?
3. **Placer County**: Do Rocklin and Lincoln have more/less diversity than county average?
4. **Persian community**: Do any small pockets exist in Folsom, Roseville, or Placer? (Unlikely but worth checking)
5. **Integration**: Do high-diversity neighborhoods have strong community organizations or are they segregated?
6. **Schools**: Are more diverse schools also performing well academically?
7. **Gentrification**: Are diverse neighborhoods appreciating faster than homogeneous ones? (could indicate gentrification pressure)

---

**END OF NEXT ACTIONS DOCUMENT**

**Ready to begin follow-up research? Start with Priority 1 (Census tract download). Estimated time: 2–3 hours. Then proceed through Priorities 2–7 sequentially.**
