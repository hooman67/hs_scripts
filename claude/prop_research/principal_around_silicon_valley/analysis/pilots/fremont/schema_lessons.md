# Fremont pilot methodology and schema lessons

**Date:** 2026-09-12  
**Status:** proposed changes for coordinator review; this file does not alter shared methodology or criteria.

## Lessons that should change the next run

### 1. Candidate names need immutable geometry identity

City/submarket names are not sufficient. Store:

```text
candidate_id
boundary_publisher
boundary_service_url
boundary_layer_id
boundary_object_id
boundary_name_field
boundary_name_value
boundary_update_field
retrieved_at
geometry_snapshot_path
geometry_hash
```

Why: official Fremont neighborhood polygons are reproducible, but several feature-level update fields are old and informal names can refer to different geographies. A snapshot/hash makes later changes detectable. `[INFERRED | HIGH | FRE-BND-001 through FRE-BND-008]`

### 2. Market evidence needs a property-observation table, not a city metric

Required columns:

```text
property_id, address, apn, latitude, longitude, candidate_id,
boundary_match_method, close_date, close_price, source_record_id,
sale_verification, arms_length_status, property_type, bedrooms,
bathrooms, finished_sqft, lot_sqft, yard_evidence, hoa_monthly,
condition_evidence, source_retrieved_at, exclusion_reason
```

The county transfer feed should be a join/corroboration source, not the sole comp source. It lacks required dwelling attributes and is stale for the present run. `[PRIMARY | HIGH | FRE-MKT-001; FRE-MKT-002]`

Proposed sampling rule: begin with a common 12-month close window and require at least 10 fully qualifying verified sales per submarket for a stable distribution summary; if fewer exist, report the exact count and extend to 24 months as a separate cohort rather than merging silently. This threshold is a methodological `ESTIMATE | MEDIUM`, to be approved after the first licensed MLS export shows actual density.

### 3. Commute evidence needs one row per observation

Required columns:

```text
candidate_id, origin_id, origin_selection_method, destination_address,
direction, mode, target_arrival_or_departure, weekday, observed_at,
typical_low_min, typical_high_min, live_eta_min, incident_state,
parking_min, walk_min, transfers, source_url_or_query_id, notes
```

Do not store a single “commute time.” Report the observation distribution, median, upper tail, sample count, and worst observed result separately. The destination is fixed at 345 Park Ave, San Jose; use consistent flexible-arrival scenarios and at least two origins per polygon because a centroid is not a neighborhood. `[UNKNOWN | UNKNOWN | FRE-COM-001; ESTIMATE | MEDIUM | FRE-LES-003]`

### 4. School outcomes and school assignment are separate entities

Store:

```text
property_id, assignment_level, assigned_school_cds,
assignment_source, assignment_checked_at, assignment_status,
school_metric_name, school_metric_year, subgroup_id, grade,
denominator, value, suppression_status, metric_source
```

A CDE directory row validates school identity. A CAASPP row validates one outcome. Neither validates address assignment. FUSD assignment needs an address-level locator result or written district confirmation, captured at finalist refresh. `[PRIMARY | HIGH | FRE-SCH-001 through FRE-SCH-005; UNKNOWN | UNKNOWN | FRE-SCH-006]`

### 5. Hazard schemas must record map legal/version context

Required columns:

```text
property_id, hazard_type, source_agency, layer_url, layer_name,
map_status, effective_or_adoption_date, retrieved_at, query_geometry,
classification, source_record_id, distance_if_applicable,
overlay_result, limitations, professional_verification
```

Add `map_status` values such as `effective`, `preliminary`, `recommended`, `adopted-local`, `superseded`, and `unknown`. A layer title alone is insufficient: the Fremont fire layer's row/source dates show why version context is decision-critical. `[PRIMARY | HIGH | FRE-HAZ-002]`

### 6. Taxes require component and parcel separation

Store the parcel's TRA separately from each tax-rate component and fixed/special assessment. Calculate:

```text
ad_valorem_rate = sum(applicable TRA rate components)
modeled_ad_valorem_tax = modeled_assessed_value * ad_valorem_rate
total_modeled_tax = modeled_ad_valorem_tax + fixed/special assessments
```

The 1.1741% TRA 12-1 calculation demonstrates the join, but it must not become a citywide constant. `[INFERRED | HIGH | FRE-TAX-001]`

### 7. Unknowns need reason codes

Add `unknown_reason` with controlled values:

```text
INPUT_MISSING
SOURCE_BLOCKED
SOURCE_STALE
SOURCE_GEOGRAPHY_MISMATCH
SOURCE_FIELDS_INCOMPLETE
NO_AUTHORIZED_ACCESS
NOT_COLLECTED
CONFLICT_UNRESOLVED
```

This pilot uses multiple distinct kinds of `UNKNOWN`. Encoding the cause tells the coordinator whether to ask the user, obtain credentials/data, select a better source, or defer to property-level diligence.

## Gate-B rerun checklist

The Fremont pilot should be rerun—and audited—before fan-out. A passing rerun needs:

1. An authorized current comp export joined to official polygons and filtered at property level.
2. Repeated drive/transit observations to 345 Park Ave across the defined flexible-arrival and return windows.
3. Representative-address school assignments and corresponding multi-level school evidence.
4. A current adopted wildfire source, FEMA flood query, geologic overlays, and explicit property-level insurance deferral.
5. At least one complete traceable claim in every source-plan category, or a coordinator-approved narrowing of what Gate B means.
6. A validation run with zero claim-ledger schema errors and a second-person evidence audit.

Parallel research should begin only after these shared protocol defects are resolved, because each would otherwise reproduce the same ambiguity across every city.
