# Verified query excerpts

These compact excerpts preserve the exact fields relied upon in the claim ledger. Full datasets remain at the listed official URLs; no restricted data is copied here.

## City of Fremont neighborhood query

Source: https://services2.arcgis.com/AVso4yDITKsybTJg/arcgis/rest/services/Neighborhoods/FeatureServer/0/query?where=NAME%20IN%20(%27Ardenwood%27,%27Centerville%27,%27Irvington%27,%27Mission%20San%20Jose%27,%27Niles%27,%27Warm%20Springs%27)&outFields=OBJECTID_1,NAME,Acres,UPD_DATE&returnGeometry=true&returnCentroid=true&outSR=4326&f=json

```text
Ardenwood: OBJECTID_1=2; Acres=1188.80692258905; UPD_DATE=20240913; centroid=(-122.05378079054314,37.5654145186022)
Centerville: OBJECTID_1=10; Acres=909.738758464597; UPD_DATE=20070201; centroid=(-122.00517902850076,37.55422347213207)
Irvington: OBJECTID_1=17; Acres=627.680779781693; UPD_DATE=20040617; centroid=(-121.96048558910245,37.53109447736973)
Mission San Jose: OBJECTID_1=21; Acres=2626.24666055326; UPD_DATE=20070201; centroid=(-121.91044349598681,37.53609095058683)
Niles: OBJECTID_1=23; Acres=2662.72049702602; UPD_DATE=20070201; centroid=(-121.9818887594545,37.58552470406103)
Warm Springs: OBJECTID_1=30; Acres=1081.13518215346; UPD_DATE=20240801; centroid=(-121.91885126786202,37.47938490667434)
```

## Ownership-transfer freshness query

Source: https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Assessor_Office_Ownership_Transfer_List/FeatureServer/0/query?where=UPPER(city_name)%3D%27FREMONT%27&outStatistics=%5B%7B%22statisticType%22%3A%22max%22%2C%22onStatisticField%22%3A%22transfer_dt%22%2C%22outStatisticFieldName%22%3A%22latest_transfer%22%7D%5D&returnGeometry=false&f=pjson

```json
{"latest_transfer":1743292800000}
```

Converted in UTC: `2025-03-30`.

## Fremont TRA 12-1 property-tax components

Source: https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Property_Tax_Rates_2025/FeatureServer/0/query?where=UPPER(TRA_LONG_DESC)%20LIKE%20%27%25FREMONT%25%27&outFields=TAX_RATE_YEAR,TRA_PRIM,TRA_SEC,TAX_RATE,LEGACY_FUND_NO,LEGACY_FUND_NAME,TRA_LONG_DESC&returnGeometry=false&f=json

```text
0.010000 COUNTYWIDE TAX
0.000084 COUNTY GO BOND
0.000908 FREMONT UNIF SCH BONDS 3 UP
0.000276 OHLONE COM COLL BONDS
0.000218 WASHINGTON TWP HOSP
0.000152 BAY AREA RAPID TRANSIT
0.000011 EAST BAY REGIONAL PARK 1
0.000060 ALAMEDA CO WATER
0.000032 CITY OF FREMONT
sum = 0.011741 = 1.1741%
```

## 2024-25 CAASPP extracts

Source: https://caaspp-elpac.ets.org/caaspp/researchfiles/sb_ca2025_1_csv_v1.zip

Filter: county code `01`, district code `61176`, Student Group ID `1` (all students), grade `11`, Test ID `1` (ELA) or `2` (mathematics).

```text
American High (school 0130062): ELA tested=595, met+above=87.73; math tested=594, met+above=72.39
Irvington High (school 0134270): ELA tested=503, met+above=82.70; math tested=503, met+above=73.96
Mission San Jose High (school 0135244): ELA tested=420, met+above=93.81; math tested=420, met+above=88.81
Washington High (school 0138693): ELA tested=431, met+above=77.26; math tested=427, met+above=59.95
```

The file's research-page warning that results for groups with fewer than 11 students are suppressed remains applicable. These school rows are not address-assignment evidence.

## Stale Fremont fire layer

Source: https://services2.arcgis.com/AVso4yDITKsybTJg/arcgis/rest/services/Very_High_Fire_Hazard_Severity_Zones/FeatureServer/0

```text
editingInfo.dataLastEditDate=1607624360120 (2020-12-10 UTC)
feature 1: NAME=Hazardous Fire Area; SOURCETHM=CO 33-2007
feature 2: NAME=Hazardous Fire Area; SOURCETHM=CO 33-2007
feature 3: NAME=Hazardous Fire Area; SOURCETHM=CO 33-2007
```

## FEMA NFHL fields validated

Source: https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28

```text
name=Flood Hazard Zones
decision-relevant fields=FLD_ZONE, ZONE_SUBTY, SFHA_TF, STATIC_BFE, V_DATUM, DEPTH, LEN_UNIT, SOURCE_CIT
```
