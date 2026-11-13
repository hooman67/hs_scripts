# Peninsula/San Mateo County Neighborhoods - Comprehensive Research Template
**Research Date:** June 22, 2026  
**Research Scope:** 9 neighborhoods for CA home purchase evaluation ($2M budget)  
**Update Status:** Data collection in progress

---

## Target Neighborhoods
1. Redwood City
2. San Carlos
3. Belmont
4. San Mateo
5. Foster City
6. Burlingame
7. Millbrae
8. Pacifica
9. Half Moon Bay

---

## Data Fields (10 dimensions per neighborhood)

| Field | Description | Source | Data Type | Confidence |
|-------|-------------|--------|-----------|-----------|
| 1. Commute to DTSJ | Minutes from neighborhood center to San Jose downtown via 101-S/280 (off-peak) | Google Maps | Integer minutes | TBD |
| 2. Commute to SF | Minutes from neighborhood center to SF downtown via 280/101-N (off-peak) | Google Maps | Integer minutes | TBD |
| 3. Median 3BR Price | Median sale price for 3-bedroom homes (2025-2026) | Zillow/Redfin | USD currency | TBD |
| 4. Price per Sqft | Average $/sqft for recent sales | Zillow/Redfin | USD/sqft | TBD |
| 5. GreatSchools Rating | Composite rating for area schools (0-10 scale) | GreatSchools.org | Decimal 0-10 | TBD |
| 6. Private/Alt Schools | Count of private or alternative schools (esp. unvaccinated-accepting) | School district sites | Integer count | TBD |
| 7. Violent Crime Rate | Per 1,000 residents (2024-2025) | FBI UCR via City-Data | Rate per 1k | TBD |
| 8. Property Crime Rate | Per 1,000 residents (2024-2025) | FBI UCR via City-Data | Rate per 1k | TBD |
| 9. Diversity Index | Census Simpson Diversity Index (0-1 scale; calculated from demographics) | Census Bureau ACS | 0-1 decimal | TBD |
| 10. % Non-White | Percentage non-white population (2024 Census) | Census Bureau ACS | Percentage 0-100 | TBD |
| 11. 5-Yr Price Appreciation | Median price change 2021-2026 (%) | Zillow/Redfin historical | Percentage | TBD |
| 12. AI Jobs (30 min radius) | Rough count of AI/ML/tech job postings | LinkedIn/Indeed | Integer count | TBD |
| 13. Typical Lot Size | Residential lot sqft (median) | Zillow/Redfin listing data | Integer sqft | TBD |
| 14. Wildfire Risk (SRA) | High-risk SRA zones present? | CAL FIRE SRA maps | Yes/No + zone name | TBD |
| 15. Flood Risk (FEMA) | FEMA flood zone present? | FEMA Flood Zone Database | Zone code (A, X, etc.) | TBD |
| 16. Parent Network Strength | Community engagement (Facebook groups, school orgs) | Local community sites | Qualitative: Strong/Moderate/Weak | TBD |
| 17. School Vaccination Barriers | Districts/schools accepting unvaccinated students? | School district policies | Qualitative description | TBD |

---

## Structured Data Table (In Progress)

| Neighborhood | DTSJ Commute | SF Commute | Median 3BR Price | $/sqft | GS Rating | Alt Schools | Violent Crime | Property Crime | Diversity Index | % Non-White | 5-Yr Apprecn | AI Jobs | Lot Size | Wildfire | Flood | Parent Network | Vax Barriers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Redwood City | -- | -- | -- | -- | -- | -- | -- | -- | 0.6876 | 62.2% | -- | -- | -- | -- | -- | -- | -- |
| San Carlos | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| Belmont | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| San Mateo | -- | -- | -- | -- | -- | -- | 99.2/1k | -- | 0.7274 | 67.0% | -- | -- | -- | -- | -- | -- | -- |
| Foster City | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| Burlingame | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| Millbrae | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| Pacifica | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| Half Moon Bay | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |

---

## Data Collection Status

- [x] Crime data (violent) - Redwood City, San Mateo collected from existing research
- [x] Diversity indices - Multiple neighborhoods collected from existing research
- [ ] Commute times - In progress (Agent research)
- [ ] Housing prices - In progress (Agent research)
- [ ] Schools & GreatSchools - In progress (Agent research)
- [ ] Property crime rates - In progress (Agent research)
- [ ] 5-year price trends - In progress (Agent research)
- [ ] AI job counts - In progress (Agent research)
- [ ] Lot sizes - In progress (Agent research)
- [ ] Fire/flood risk mapping - In progress (Agent research)
- [ ] Community assessment - In progress (Agent research)
- [ ] Vaccination policy research - In progress (Agent research)

---

## Notes & Context

**Family Constraints:**
- 2 unvaccinated daughters (religious exemption) - need school options with high exemption rates or that accept homeschooled/unvaccinated children
- Wife loves beaches (Brazilian origin) - higher preference for coastal communities
- AI engineer at Adobe DTSJ - commute is important factor
- Growing family (family of 4 soon) - 3BR minimum, 1700+ sqft, backyard required
- Budget: $2M max
- No flight paths (cancer risk from jet fuel)
- Prefer larger land if possible (gardening, self-sufficiency)

**Comparative Context:**
- North Bay research completed (Sonoma, Santa Rosa, San Rafael, etc.) - now doing Peninsula comparisons
- South Bay (Cupertino, San Jose, Los Gatos, Saratoga, etc.) already researched
- Peninsula is middle ground: between SF (too urban, expensive, long commute from north) and more distant areas

---

## Next Steps

1. Collect all remaining data fields from research agent
2. Compile into final structured table (tab-separated or CSV)
3. Cross-reference multiple sources for each data point
4. Add confidence ratings and source citations
5. Synthesize with North Bay & South Bay research for regional comparison
6. Create decision matrix for family constraints (commute, schools, diversity, safety, growth potential, beach access)

