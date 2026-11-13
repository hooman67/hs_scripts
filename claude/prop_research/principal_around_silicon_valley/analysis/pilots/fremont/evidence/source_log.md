# Fremont pilot source log

**Retrieval date:** 2026-09-12  
**Rule:** Every source below was opened directly. Search results were used only to discover sources and are not evidence for candidate facts. No restricted consumer portal was scraped.

## Opened and used

| ID | Publisher / title | Complete URL | What was inspected | Outcome |
|---|---|---|---|---|
| S01 | City of Fremont GIS Division — Neighborhoods service | https://services2.arcgis.com/AVso4yDITKsybTJg/arcgis/rest/services/Neighborhoods/FeatureServer | Service description, ownership statement, layer list | Usable primary boundary source |
| S02 | Esri item metadata for City of Fremont Neighborhoods | https://www.arcgis.com/sharing/rest/content/items/044ae5a42d924d9b94dba5c42a539c78?f=pjson | owner, title, license, modified time, service URL | Confirms official City GIS ownership and open-data license |
| S03 | City of Fremont — six-neighborhood query | https://services2.arcgis.com/AVso4yDITKsybTJg/arcgis/rest/services/Neighborhoods/FeatureServer/0/query?where=NAME%20IN%20(%27Ardenwood%27,%27Centerville%27,%27Irvington%27,%27Mission%20San%20Jose%27,%27Niles%27,%27Warm%20Springs%27)&outFields=OBJECTID_1,NAME,Acres,UPD_DATE&returnGeometry=true&returnCentroid=true&outSR=4326&f=json | Named rows, acres, update fields, full geometry, centroids | Reproducible submarket definition; exact geometry should be snapshotted before production collection |
| S04 | City of Fremont — Community Plan Areas | https://services2.arcgis.com/AVso4yDITKsybTJg/arcgis/rest/services/Community_Plan_Areas/FeatureServer | Service description and layer rows | Opened but rejected for the pilot unit: broader planning areas are not equivalent to the six selected neighborhood polygons |
| S05 | California Department of Education — Public Schools and District Data Files | https://www.cde.ca.gov/ds/si/ds/pubschls.asp | Download description, dynamic-data note, and disclaimer | Usable directory landing page; warns records are self-reported |
| S06 | California Department of Education — school directory TXT | https://www.cde.ca.gov/schooldirectory/report?rid=dl1&tp=txt | Fremont Unified district and school rows, CDS/NCES/status/grade/coordinates/update fields | Usable primary directory data; not assignment or outcome evidence |
| S07 | California Department of Education — assessment data | https://www.cde.ca.gov/ds/ad/assessmentdata.asp | Official downloadable-data landing page | Confirms availability of CAASPP downloads |
| S08 | CDE/ETS — 2024-25 Smarter Balanced research files | https://caaspp-elpac.ets.org/caaspp/ResearchFileListSB?ps=true&lstTestYear=2025&lstTestType=B&lstCounty=01&lstDistrict=61176 | Dataset scope and suppression notice | Usable primary source; definitions and suppression constraints retained |
| S09 | CDE/ETS — 2024-25 statewide Smarter Balanced file | https://caaspp-elpac.ets.org/caaspp/researchfiles/sb_ca2025_1_csv_v1.zip | Caret-delimited file; filters for county 01, district 61176, four high schools, all students, grade 11, ELA/math | Usable primary outcome data; not assignment or complete school-quality evidence |
| S10 | California Department of Education — California School Dashboard | https://www.cde.ca.gov/ta/ac/cm/ | Description of multiple state/local measures | Opened to guard against reducing school quality to test scores |
| S11 | Alameda County Open Data | https://data.acgov.org/ | Organization landing page | Confirms official county open-data context |
| S12 | Alameda County Assessor — Ownership Transfer List | https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Assessor_Office_Ownership_Transfer_List/FeatureServer | Service description, item metadata, layer fields | Usable for transfer lookup; insufficient for qualifying-home comp selection |
| S13 | Alameda County Assessor — Fremont latest-transfer query | https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Assessor_Office_Ownership_Transfer_List/FeatureServer/0/query?where=UPPER(city_name)%3D%27FREMONT%27&outStatistics=%5B%7B%22statisticType%22%3A%22max%22%2C%22onStatisticField%22%3A%22transfer_dt%22%2C%22outStatisticFieldName%22%3A%22latest_transfer%22%7D%5D&returnGeometry=false&f=pjson | `max(transfer_dt)` for Fremont | Returned 1743292800000 = 2025-03-30 UTC; stale for a 2026-09 market snapshot |
| S14 | Alameda County Assessor — Parcels | https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Parcels/FeatureServer | Service description and fields | Useful APN/address/geometry/assessed-value join; not verified sale price, bedrooms, lot size, or yard |
| S15 | Alameda County Assessor — Secured Tax Roll 2025-26 | https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Assessor_Office_Secured_Tax_Roll_2025_to_2026/FeatureServer | Service description and fields | Useful parcel/TRA/tax lookup component |
| S16 | Alameda County Tax Collector — Property Tax Rates 2025 | https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Property_Tax_Rates_2025/FeatureServer | Service description, official owner, fields, Fremont rows | Usable rate-component table; actual property requires TRA and parcel assessments |
| S17 | BART — Warm Springs / South Fremont Station | https://www.bart.gov/stations/warm | Address and lines serving station | Usable transit component evidence; not door-to-door commute evidence |
| S18 | VTA — Rapid 500 | https://www.vta.org/go/routes/rapid-500 | Route title and endpoints | Shows a Berryessa BART–San Jose Diridon connection; no complete time/reliability claim made |
| S19 | 511 SF Bay — Open Data | https://511.org/open-data | API access text | Usable source-access fact; token required and none was available in this pilot |
| S20 | FEMA — NFHL Flood Hazard Zones layer 28 | https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28 | Layer identity and fields including `FLD_ZONE`, `ZONE_SUBTY`, `SFHA_TF`, and source fields | Usable parcel-query schema; no parcel was tested |
| S21 | City of Fremont GIS — Very High Fire Hazard Severity Zones | https://services2.arcgis.com/AVso4yDITKsybTJg/arcgis/rest/services/Very_High_Fire_Hazard_Severity_Zones/FeatureServer/0 | Editing timestamps, fields, all three feature records | Rejected for current-policy use: rows cite `CO 33-2007`; data last edited 2020-12-10 |
| S22 | City of Fremont GIS — Police Zones | https://services2.arcgis.com/AVso4yDITKsybTJg/arcgis/rest/services/Police_Zones/FeatureServer | Service presence/schema | Boundary data only; not an offense dataset |

## Opened but blocked or inadequate

| ID | Source | URL | Result and lawful next step |
|---|---|---|---|
| F01 | Fremont Unified — School Locator | https://fremontunified.org/schools/school-locator/ | Cloudflare response: “Enable JavaScript and cookies to continue.” Use an authorized interactive browser and confirm each address with the district; do not infer from school names. |
| F02 | Fremont Unified legacy host | https://www.fremont.k12.ca.us/ | TLS/SSL handshake failed in this environment. Do not weaken transport security; use the current district site or direct district confirmation. |
| F03 | City of Fremont main website | https://www.fremont.gov/ | Akamai denied the command-line request. The official ArcGIS service remained available and was used for GIS facts. |
| F04 | CAL FIRE / Office of the State Fire Marshal — Fire Hazard Severity Zones | https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones | Access denied by edge service in this environment. The current adopted LRA map was not independently verified; use an authorized browser/download or official current service before parcel screening. |
| F05 | Licensed MLS-derived qualifying comps | No source credential or export available | Required fields are property type, beds, closed price/date, lot, finished area, and enough address/APN information to join the official polygons. Obtain an authorized agent/MLS export; do not scrape consumer portals. |
| F06 | Repeated commute observations | No route collection attempted | Exact Adobe address and work arrival/departure windows are still unknown; obtain those first, then use a common route protocol and 511 token or authorized route tool. |
| F07 | Neighborhood crime incidents | No official incident dataset found in the City GIS catalog search | OpenJustice can provide agency-level context, but it cannot be silently treated as six-neighborhood evidence. Seek a city incident export or record the mismatch. |

## Not collected in this bounded pilot

The following completeness-plan categories were not researched end to end: career optionality, demographics, community fit, private/Montessori/home-school availability, earthquake/geologic overlays, insurance, water resilience, air/heat/climate, transport noise, broadband, healthcare, nature/parks, and resale history. They remain `UNKNOWN`, not neutral or implicitly favorable.

