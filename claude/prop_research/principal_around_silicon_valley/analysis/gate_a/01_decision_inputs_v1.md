# Gate A Decision Inputs v2

**Status:** Active specification for the Gate B rerun

**Recorded:** 2026-09-11; revised 2026-09-12

**Source:** User answers in the active Codex thread on 2026-09-11 and 2026-09-12

**Scope:** Principal residence only

This file records the user-supplied decision inputs separately from external facts and analytical recommendations. Direct user statements are `PRIMARY` evidence for the user's preferences and circumstances; interpretations and proposed policies are labeled separately.

## Confirmed user inputs

| Topic | Active input | Evidence status | Confidence |
|---|---|---|---|
| Available assets | Approximately USD 600,000 in savings: about USD 300,000 in cash and the remainder invested | `PRIMARY` | `HIGH` |
| Monthly ceiling | User does not want to spend more than USD 5,000–7,000 per month on housing | `PRIMARY` | `HIGH` |
| Office attendance | Adobe office Tuesday, Wednesday, and Thursday | `PRIMARY` | `HIGH` |
| Commute tolerance | One hour maximum; worst case up to 90 minutes | `PRIMARY` | `MEDIUM` because “maximum” and “worst case” require an operational interpretation |
| Property type | Detached house | `PRIMARY` | `HIGH` |
| Bedrooms | At least three | `PRIMARY` | `HIGH` |
| Outdoor space | Backyard is required | `PRIMARY` | `HIGH`; minimum usable dimensions remain `UNKNOWN` |
| Condition | Flexible if renovation/condition is financially sensible | `PRIMARY` | `HIGH` for flexibility; the acceptable project size remains `UNKNOWN` |
| Schools | Better districts are strongly preferred because the family has two young children; Montessori and homeschooling are also acceptable possibilities | `PRIMARY` | `HIGH` |
| Health-policy screen | Remove the former health-policy constraint from principal-residence research | `PRIMARY` | `HIGH` |
| Timing | Buy within roughly three years, with no urgency; buy sooner if an unusually good deal appears | `PRIMARY` | `HIGH` |
| Holding period | User requested a recommendation | `PRIMARY` | `HIGH` |
| Hazard/insurance tolerance | User requested help defining it | `PRIMARY` | `HIGH` |
| Primary office destination | 345 Park Ave, San Jose, CA 95110 | `PRIMARY` | `HIGH` |
| Other Adobe offices | The user can also work from Adobe offices in San Francisco and Seattle | `PRIMARY` | `HIGH`; frequency and whether relocation is in scope remain `UNKNOWN` |
| Work hours | Arrival time is flexible | `PRIMARY` | `HIGH`; actual recurring arrival/departure pattern remains `UNKNOWN` |
| Budget contents | The USD 5,000–7,000 ceiling includes maintenance and utilities; tuition is outside it | `PRIMARY` | `HIGH` |
| Invested savings | The invested USD 300,000 is freely deployable | `PRIMARY` | `HIGH`; liquidation tax cost remains `UNKNOWN` |
| Yard function | Yard should be large enough for two young children and a dog to play | `PRIMARY` | `HIGH`; dimensions remain intentionally functional rather than fixed |
| HOA/renovation limits | User requested recommended limits | `PRIMARY` | `HIGH` |
| School threshold | School quality must be balanced against other factors; user requested a recommended threshold | `PRIMARY` | `HIGH` |
| Geographic expansion | Seattle-area homes may enter the research in a later phase | `PRIMARY` | `HIGH` |
| Office priority | San Francisco is a real work possibility, but San Jose is preferred because it is Adobe headquarters | `PRIMARY` | `HIGH` |
| MLS data | User likely can obtain an agent export but needs to investigate | `PRIMARY` | `MEDIUM` until an export is received |
| Commute collection | Manual Google Maps observations are acceptable | `PRIMARY` | `HIGH` |
| Local data retention | Exact candidate addresses and map screenshots may be stored in this private repository | `PRIMARY` | `HIGH` |

## Operational interpretations for the pilot

| Item | Pilot rule | Evidence status | Confidence | Revisit trigger |
|---|---|---|---|---|
| Commute | Score travel to 345 Park Ave. Sample flexible arrival scenarios rather than assuming one peak time: 8:00, 9:30, and 11:00 a.m., with paired return windows. Target no more than 60 minutes one way for the selected recurring schedule; treat 90 minutes as a hard bad-day boundary | `INFERRED` from the user's wording | `MEDIUM` | Actual preferred schedule or measured route distribution |
| Office optionality | Keep San Jose as the primary commute gate. Score San Francisco access as a meaningful secondary factor. Evaluate Seattle as a separate later-phase relocation scenario rather than mixing it into Bay Area commute rankings | `INFERRED` | `HIGH` for scope control |
| Monthly cost | Use USD 5,000 as comfortable, USD 6,000 as target ceiling, and USD 7,000 as hard ceiling. Include P&I, property tax, required insurance, HOA, maintenance reserve, and utilities; keep each component visible | `INFERRED` | `HIGH` as a conservative implementation of the stated range |
| Price | Do not impose the legacy USD 2,000,000 cap. Derive a live price ceiling from rate, down payment, taxes, insurance, HOA, and maintenance assumptions | `INFERRED` | `HIGH` |
| Size | Three bedrooms is hard. The legacy 1,700-square-foot figure is not hard because the user did not reaffirm it; retain interior area as a preference and report it explicitly | `INFERRED` | `MEDIUM` |
| Yard | Require a private, directly accessible, reasonably level play area. Use 800 usable square feet as a review trigger—not an automatic rejection—and prefer roughly 1,200+ usable square feet. Lot size is only a discovery proxy | `ESTIMATE` | `MEDIUM` |
| HOA | Prefer no HOA. Treat USD 0–200/month as acceptable if documents are sound, USD 201–350 as a review item, and more than USD 350 as presumptively unsuitable unless it replaces costs the household would otherwise pay and total carry still passes | `INFERRED` | `MEDIUM` |
| Renovation | Require the home to be habitable, financeable, and insurable at closing. Permit cosmetic work up to USD 50,000; review USD 50,001–75,000 only with a 20% contingency and preserved reserves; exclude larger, structural, foundation, retaining-wall, or full-gut projects from the standard search | `INFERRED` | `MEDIUM` |
| Schooling | Do not impose a single rating cutoff. Require a verified assigned public-school path and multi-year evidence across academic outcomes, growth where available, chronic absenteeism, suspension/climate, and practical fit. Treat persistent serious weakness across several measures as a hard review, not an automatic city rejection; record Montessori/private/home-school alternatives separately | `INFERRED` | `MEDIUM` |

## Assumptions that are not yet facts

1. San Jose remains the primary office anchor; San Francisco is meaningful optionality and Seattle is a later relocation scenario rather than a Bay Area commute destination. `PRIMARY` for the user's preference; phase separation is `INFERRED`.
2. A USD 500/month utility allowance is used until property-specific history exists. `ESTIMATE`.
3. “Freely deployable” means the invested USD 300,000 is not legally/account restricted; liquidation taxes and market risk remain `UNKNOWN`.
4. The provisional yard dimensions are functional screening aids, not evidence that every family or dog needs that area. `ESTIMATE`.
5. Employment, income, credit, immigration, lender eligibility, other debts, and tax filing status remain `UNKNOWN` and must not be guessed.

## Remaining decision-critical unknowns

These do not block market/source research, but they block a lender-grade affordability conclusion or final property decision:

1. Gross and after-tax household income, other monthly debts, and credit/loan assumptions.
2. Tax basis and liquidation tax cost for the invested funds.
3. The exact Adobe San Francisco and Seattle office destinations and how often each would realistically be used.
4. Whether the proposed yard, HOA, and renovation bands match the family's experience after viewing real example properties.
5. School-program fit and tuition budget for Montessori/private alternatives; tuition is confirmed outside the housing ceiling.
