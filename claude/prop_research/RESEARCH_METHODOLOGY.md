# Evidence-First Property Research Methodology

## Purpose

This methodology is the shared standard for property research in this repository. Its main goal is to prevent unsupported facts, false precision, citation laundering, and rankings built from incomparable inputs.

## 1. Separate evidence status from confidence

Every material claim gets both fields.

### Evidence status

| Label | Meaning |
|---|---|
| `PRIMARY` | The original authoritative source was opened and directly supports the claim. |
| `SECONDARY` | A reputable secondary source was opened and directly supports the claim. |
| `QUOTED` | A source repeats a claim attributed elsewhere; the original was not inspected. |
| `INFERRED` | Derived from cited inputs. The calculation or reasoning must be shown. |
| `ESTIMATE` | Based on an explicit assumption, proxy, sample, or model. |
| `SPECULATIVE` | Plausible but not adequately supported. Not usable for scoring. |
| `CONFLICTED` | Credible sources disagree or use incompatible definitions. |
| `UNKNOWN` | No adequate evidence was found. |

### Confidence

| Level | Minimum standard |
|---|---|
| `HIGH` | Current primary evidence at the correct geographic/unit level, with definitions understood; corroborated when the claim is decision-critical. |
| `MEDIUM` | One suitable primary source or multiple independent reputable secondary sources, with manageable limitations. |
| `LOW` | Stale, indirect, incomplete, weakly comparable, or single-secondary evidence. |
| `UNKNOWN` | Evidence is absent, irreconcilably conflicted, or not inspected. |

Confidence describes reliability, not desirability. An unpleasant fact can be high confidence; a favorable claim can be low confidence.

## 2. Claim ledger

Decision-relevant research must maintain a machine-readable claim ledger with these columns:

```text
claim_id,project,candidate,topic,claim,evidence_status,confidence,
source_publisher,source_title,source_url,source_date,retrieved_at,
source_location,evidence_excerpt,geography,unit,calculation,
limitations,refresh_after,reviewer
```

Rules:

- One row per atomic claim.
- `source_location` identifies a table, field, section, page, or API query.
- `evidence_excerpt` contains the exact supporting text or returned value.
- `calculation` records formulas and inputs for inferred values.
- A prior agent's report is `QUOTED`, never `PRIMARY`.
- A search snippet is discovery material only and cannot enter the ledger as evidence.

## 3. Source hierarchy

Prefer the closest authoritative producer for each fact:

1. Law, regulation, policy, permits: statute, regulator, municipality, official ordinance or licensing portal.
2. Property and transaction data: county recorder/assessor, MLS-derived licensed data, official statistics, then reputable market aggregators.
3. Short-term rental legality: municipal code and official permit portal; platform listings are evidence of activity, not legality.
4. Crime: local open-data incident records or state/FBI datasets with definitions and coverage noted.
5. Schools: state education department and district/school records; rating sites are secondary signals.
6. Hazards: FEMA, USGS, CAL FIRE, Environment Canada, provincial agencies, and insurer quotes for specific properties.
7. Demographics: US Census or Statistics Canada at the relevant geography.
8. Commute: reproducible route queries at stated dates/times plus in-person tests for finalists.
9. Community fit: multiple independent indicators and field visits; never infer belonging from race percentages alone.

## 4. Freshness

Each claim has an `as of` date and a refresh rule. Default maximum ages:

- Active listings and asking rents: 7 days.
- Sold-price snapshots, inventory, days on market: 30 days.
- Mortgage rates and financing terms: 7 days.
- Short-term-rental rules, permits, taxes, and caps: verify on every decision run.
- Insurance availability and premiums: property-specific quote before underwriting.
- Annual government datasets: latest published release, with reference year stated.
- Long-lived physical facts: refresh when a new official map, plan, or project changes them.

Never describe a future-dated, modeled, or unpublished value as observed current data.

## 5. Research workflow

### Gate A: question and constraints

- Record the decision, budget, time horizon, must-haves, disqualifiers, and unknowns.
- Distinguish preferences from hard constraints.
- Freeze a versioned criteria file before scoring.

### Gate B: pilot and source validation

- Research one representative candidate end to end.
- Confirm that sources are accessible, definitions align, and calculations are reproducible.
- Revise the schema and instructions based on the pilot before parallel collection.

### Gate C: independent collection

- Parallelize comparable candidates or source categories.
- Agents write separate evidence files and do not alter shared rankings.
- Record failed searches and inaccessible sources without manufacturing replacements.

### Gate D: evidence audit

- Check every material value against its opened source.
- Detect geography, date, unit, population, property-type, and asking-versus-sold mismatches.
- Mark contradictions and missing fields.
- Recompute derived values from stored inputs.

### Gate E: scoring

- Score only candidates meeting the declared completeness threshold.
- Keep raw facts separate from normalized scores.
- Publish formulas and weights.
- Run sensitivity analysis across reasonable weights and adverse scenarios.
- Report rank stability; do not call a narrow numerical lead decisive.

### Gate F: recommendation

- State what is known, inferred, estimated, conflicted, and unknown.
- Give confidence by conclusion, not merely one overall confidence label.
- Identify facts that would reverse the recommendation.
- Require professional or property-specific diligence where appropriate.

## 6. Calculations and reproducibility

- Store raw source snapshots or query results when legally permitted.
- Calculate metrics in scripts or notebooks from recorded inputs.
- Test units, missing values, denominator choice, and score bounds.
- Do not calculate investment return from appreciation alone. Include financing, vacancy, management, maintenance, insurance, taxes, utilities, platform fees, capital expenditures, transaction costs, and income taxes where applicable.
- Keep nominal returns, real returns, cash-on-cash return, and total return distinct.
- Model bear, base, and bull cases; assumptions are `ESTIMATE` even when reasonable.

## 7. Review standard

A deliverable is ready only when:

- Every material factual claim has a traceable citation and evidence label.
- Every recommendation identifies its confidence and reversal conditions.
- Unknowns remain visible.
- Direct evidence can be followed from the report to the ledger and source.
- Calculations can be rerun.
- A second pass has checked the strongest conclusion for disconfirming evidence.

