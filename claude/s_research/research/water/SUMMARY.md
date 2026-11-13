# Ninety-Day Household Water Plan

As of: 2026-11-07

Research status: initial evidence, quantity modeling, architecture comparison, and starter-container screening complete. Hooman confirmed the first WaterPrepared 55-gallon tank filled with potable municipal water and labeled for replacement by 2027-04-28. He later confirmed four bottled-water cases and purchased two more 55-gallon WaterPrepared tanks. The two new tanks have not arrived and have not been sanitized or filled; they remain planned capacity.

`[USER-CONFIRMED, 2026-11-07]`: The intended final stored-water system is three 55-gallon tanks plus four bottled-water cases. `[ASSUMED]`: if each case is the common Costco 40 × 16.9-fluid-ounce configuration, planned volume is `3 × 55 + 4 × 40 × 16.9 ÷ 128 = 186.125 gallons`, equal to 41.36 days at the 4.5-gallon/day household floor. Only the first tank is confirmed filled. Actual bottle count and size should be checked on the cases before treating 186.125 gallons as audited capacity.

## Table of contents

- [Scope and decision](#scope-and-decision)
- [Confidence legend](#confidence-legend)
- [Executive synthesis](#executive-synthesis)
- [Household demand model](#household-demand-model)
- [Immediate starter purchase](#immediate-starter-purchase)
- [Proposed 90-day expansion system](#proposed-90-day-expansion-system)
- [Storage alternatives and budgets](#storage-alternatives-and-budgets)
- [Safety, filling, and maintenance](#safety-filling-and-maintenance)
- [Placement and seismic constraints](#placement-and-seismic-constraints)
- [Hazard-specific operations](#hazard-specific-operations)
- [Contradictions and rejected shortcuts](#contradictions-and-rejected-shortcuts)
- [Open decisions and next validation](#open-decisions-and-next-validation)
- [Sources](#sources)

## Scope and decision

Determine a safe, low-maintenance, cost-conscious water system for two adults, a 2-year-old, a breastfed 1-month-old, and a 50-pound dog for 90 days in a detached home in San Jose, California. Compare survival-minimum, moderate-conservation, and higher-comfort service levels across earthquake, contamination, outage, wildfire, supply disruption, and complete utility-loss scenarios.

## Confidence legend

- `VERIFIED`: directly supported by an inspected primary source or independently corroborated reliable sources.
- `ASSUMED`: transparent planning assumption or extrapolation awaiting validation.
- `UNVERIFIED`: plausible but not sufficiently supported for decision-making.
- `VENDOR-CLAIM`: product information reported by a manufacturer or seller but not independently certified in this research.
- `USER-CONFIRMED`: household fact, preference, constraint, or decision provided directly by Hooman.

## Executive synthesis

The realistic first target is the survival tier, not 90 days of ordinary household water use.

- `VERIFIED`: CDC and Ready.gov both use **at least 1 gallon per person per day** for emergency drinking and sanitation. CDC says to store more for children, nursing mothers, pets, sickness, and hot climates; Ready.gov says needs can double in very hot temperatures.
- `ASSUMED`: A 50-pound dog is budgeted at **0.5 gallon/day**. Current AKC guidance gives a general adult-dog rule of about 1 fluid ounce per pound per day, or 0.39 gallon/day for this dog; the planning value adds heat and spillage margin.
- `ASSUMED`: For this household, the authority floor is **405 gallons** for 90 days. A prudent baseline design target is **500 gallons**, which adds 20% and rounds to deployable container sizes.
- `ASSUMED`: A sustained extreme-heat case can approach **900 gallons** for 90 days if human and dog demand doubles and 10% is added for losses. This is a sensitivity bound, not a prediction that all 90 days will be extremely hot.
- `VERIFIED` plus modeled assumptions: WHO's emergency framework supports a moderate essential-health-and-hygiene target near **20 liters/person/day**. Applied here with dog water and 10% losses, this is about **2,200 gallons**.
- `ASSUMED`: A higher-comfort but still conserving system with short showers, conventional toilet use, efficient laundry, and one dishwasher cycle/day is about **7,500 gallons**. EPA's national benchmark implies roughly **18,900 gallons** of indoor water for an average American family over 90 days, so 7,500 gallons is not normal unrestricted comfort.

Hooman has purchased **three new 55-gallon WaterPrepared emergency-water tanks** and has four cases of factory-sealed bottled water. The first tank is confirmed filled. The two additional tanks are purchased but have not arrived or been sanitized and filled. Assuming each case contains 40 × 16.9-fluid-ounce bottles, the completed system will hold about 186.1 gallons, or 41.4 days at the modeled 4.5-gallon/day household floor.

Why this starter leads:

- It provides a meaningful outage reserve immediately for roughly $186 plus bottled water, before tax and subject to checkout.
- Its integrated gravity spigot avoids choosing an unverified food-contact pump for a conventional drum.
- At about 22 × 28 × 30 inches and approximately 459 pounds of water when full, it is more manageable as a first module than a 2,424-pound filled IBC.
- It remains useful as a redundant module if the household later expands to the proposed 625-630 gallon system.

The cheapest screened 275-gallon candidate is the new NTO T275 at $350 **before freight**. It is still a sensible later bulk option, but its delivered San Jose price, roughly 2,424-pound filled mass, translucent tank, valve protection, cover, and seismic restraint make it a larger commitment than the user requested for the first step.

The main compromise is maintenance: **CDC says self-filled water should be replaced every six months**. No independent authority inspected in this batch supports extending self-filled household water to five years merely by adding a proprietary preservative. Commercially packaged water reduces filling risk, but must still be stored correctly, inspected, and used by its labeled expiration.

## Household demand model

### Quantity summary

| Level | Daily model | 90-day modeled total | Rounded design target | Water weight at target | What it supports |
|---|---:|---:|---:|---:|---|
| Authority floor | 4 humans × 1 gal + dog 0.5 gal | 405 gal | 405 gal | 3,378 lb | Drinking, cooking, brushing teeth, and only minimal sanitation |
| Survival baseline | Authority floor + 20% | 486 gal | **500 gal** | 4,170 lb | Same uses, with modest nursing/child/pet/spillage margin |
| Sustained extreme heat | Human and dog demand doubled + 10% | 891 gal | **900 gal** | 7,506 lb | Conservative sensitivity if extreme heat persists |
| Moderate conservation | 4 humans × 20 L + dog 0.5 gal + 10% | 2,142 gal | **2,200 gal** | 18,348 lb | Drinking/cooking plus basic personal and domestic hygiene |
| Higher comfort/conservation | Component model below + 10% | 7,444 gal | **7,500 gal** | 62,550 lb | Short showers, efficient toilet/laundry/dishwasher use; still conserved |
| National normal-use benchmark | 300 gal/household/day × 70% indoors | 18,900 gal | Not a storage target | 157,626 lb | Context only; approximately normal indoor household use |

Unit conversions use 1 US gallon = 3.785411784 liters and 8.34 pounds of water per gallon for planning.

### Survival math

- Humans: `4 × 1 gal/day × 90 = 360 gal` (`VERIFIED` minimum rate; household arithmetic).
- Dog: `0.5 gal/day × 90 = 45 gal` (`ASSUMED`, rounded above the 0.39-gallon general rule).
- Absolute floor: `360 + 45 = 405 gal`.
- Baseline margin: `405 × 1.20 = 486 gal`, rounded to **500 gallons**.
- Very-hot sensitivity: `(4 × 2 + 1) gal/day × 90 × 1.10 = 891 gal`, rounded to **900 gallons**. Doubling the dog's allocation as well as human allocation is conservative.

The one-gallon human minimum must not be treated as comfortable use. Ready.gov explicitly says not to ration drinking water unless authorities direct it; reduce activity and stay cool instead.

### Moderate-conservation math

WHO says 7.5-15 liters/person/day is a simplified survival requirement and separately reports research indicating **20 liters/person/day** as the minimum safe quantity for minimum essential health and hygiene. This humanitarian-emergency figure is a useful planning anchor, but it is not a San Jose residential standard.

`[(20 L ÷ 3.7854) × 4 humans + 0.5 gal dog] × 1.10 loss factor × 90 = 2,142 gal`, rounded to **2,200 gallons**.

At least 500 gallons must remain the protected potable floor. The additional safe-water allocation depends on the intended uses: dishes, food preparation, brushing teeth, handwashing, and personal hygiene still require safe water when authorities declare tap water unsafe, while appropriately separated lower-quality water may serve toilet or some laundry/cleaning uses. The 2,200-gallon tier therefore cannot be divided into potable and non-potable storage until its exact sanitation practices are defined.

### Higher-comfort component model

This model assumes all relevant appliances, the sewer, and a water-heating/cooking energy source remain usable. Stored water alone cannot provide this service during a power failure or damaged sewer. It intentionally retains the full 20 L/person essential allowance and then adds the comfort services rather than subtracting overlapping basic washing; the result is conservative by design.

| Component | Assumption | Gallons/day |
|---|---|---:|
| Essential household base | 20 L/person/day × 4 | 21.13 |
| Dog | Planning allowance | 0.50 |
| Adult showers | 2 adults × 5 min × 2.0 gpm daily | 20.00 |
| Child bathing | 10 gallons total every other day | 5.00 |
| Toilet | 3 users × 4 flushes × 1.28 gal/flush | 15.36 |
| Laundry | 5 loads/week × 14 gal/load | 10.00 |
| Dishwasher | 1 efficient cycle/day | 3.20 |
| Subtotal | | 75.19 |
| With 10% loss/operating margin | | 82.71 |

`82.71 gal/day × 90 = 7,444 gal`, rounded to **7,500 gallons**.

Sensitivity:

- A 1.6-gallon toilet adds about 346 gallons over 90 days compared with the 1.28-gallon assumption.
- A 2.5-gpm rather than 2.0-gpm adult shower adds about 900 gallons over 90 days.
- More frequent child bathing, leaks, hand dishwashing, or more laundry increases the total.

## Immediate starter purchase

Status: `[PARTIALLY IMPLEMENTED — 55-GALLON MODULE FILLED 2026-10-28; BOTTLED RESERVE PENDING]`

### Recommended first order

1. **One new WaterPrepared 55-gallon tank — PURCHASED:** the Amazon listing displayed **$185.99** before tax, with an opaque blue tank, integrated gravity spigot, and approximate dimensions of 22 × 28 × 30 inches. The manufacturer describes the material as BPA-free and FDA food-grade. Confirm the received item is new and undamaged and inspect its markings before filling.
2. **Approximately 16 gallons of factory-sealed bottled water:** for example, three 40-packs of 16.9-fluid-ounce bottles total about 15.8 gallons. Buy this locally using the printed expiration date rather than paying parcel freight.

Combined nominal storage is about **71 gallons**, which provides:

- `71 ÷ 4.5 = 15.8 days` at the modeled household authority floor;
- `55 ÷ 4.5 = 12.2 days` from the tank alone;
- a separate portable reserve if the tank or garage outlet becomes inaccessible.

The full tank contains approximately **459 pounds of water**, plus the container. Put it directly on a sound, level garage slab in the coolest shaded interior location Hooman selects; keep it away from gasoline, pesticides, solvents, vehicle impact, and direct sun. Do not plan to move or stack it after filling. Protect the spigot from impact and child operation.

The direct WaterPrepared storefront displayed a $269 price, making the Amazon listing the cheaper current purchase path. The manufacturer's FDA/NSF statements are vendor claims; no independent NSF certification record was established in this batch. CDC's applicable requirement is a food-grade water-storage container, and the received label/documentation should be inspected before filling.

### Why not the cheaper conventional 55-gallon drum?

An Augason Farms 55-gallon food-grade drum was listed at approximately **$139.99**, but it needs a bung wrench and separately verified drinking-water-contact pump or siphon. A marketplace bundle with an unverified pump was about $171, only around $15 below the WaterPrepared tank. The integrated-spigot tank is the simpler first purchase.

### If 275 gallons is preferred now

The strongest current bulk candidate is the **new NTO T275** at **$350 before freight**. The listing states 275 gallons, new HDPE, FDA-approved food-grade/potable resin, 48 × 40 × 46 inches, 130 pounds empty, a six-inch lid, and a two-inch camlock outlet. Filled gross weight is approximately **2,424 pounds**, and the volume lasts `275 ÷ 4.5 = 61.1 days` at the household floor.

Before ordering, obtain the final delivered quote to ZIP 95121. Add NTO's two-inch female-camlock-to-3/4-inch-garden-hose adapter (currently $20), an opaque fitted cover, and a verified drinking-water/RV hose. Gravity dispensing works if the receiving container is below the tote outlet; an electric pump is not required. Reject used, rebottled, or reconditioned totes even if their previous contents are described as food.

Uline and Global Industrial have new 275-gallon alternatives, but their displayed tank prices were higher—approximately $595 and $485.95 before freight—and the inspected pages did not provide a better potable-water case than NTO's explicit food-grade/potable designation. Uline also explicitly says its candidate does not meet NSF 61.

## Proposed 90-day expansion system

Status: `[PROPOSAL — NOT YET CONFIRMED]`

### Later phase: 625-630 gallon baseline

1. **Bulk reserve:** two separate, brand-new 275-gallon IBCs whose exact tank, lid, gasket, valve, and outlet are documented by the manufacturer for potable-water contact. Never use a tote that previously contained any substance.
2. **Rapid-access reserve:** 75-80 gallons of unopened commercial bottled water in smaller original containers. This covers roughly 14 days at the 4.5-gallon/day household floor plus 20%.
3. **Placement:** side-by-side, not stacked, on a verified level garage slab. Separate and guard the outlet valves, use opaque fitted covers, and restrain each tote for earthquake movement using a design appropriate to the exact tote and slab.
4. **Access:** potable-water-safe hose and gravity nozzle for each tote, plus an independent manual transfer pump. Do not depend on electricity or connect the tanks inline with house plumbing.
5. **Maintenance:** replace all self-filled bulk water every six months; rotate commercially bottled stock before its printed expiration; conduct a brief monthly leak, pest, cap, valve, and restraint check.

A current candidate listing illustrates the form factor: the NTO T275 is listed at 275 gallons, 48 × 40 × 46 inches, 130 pounds empty, $350 before freight, new HDPE in a galvanized cage/pallet, and made with FDA-approved resin described by the retailer as food-grade/potable. The listing says it is translucent and has UV inhibitors. The received components and delivered price must still be verified before a later bulk purchase.

Approximate installed characteristics for two such totes plus 80 gallons modular:

- nominal volume: **630 gallons**;
- water alone: **5,254 pounds**;
- containers plus water: approximately **5,500 pounds** before anchoring/accessories;
- two-tote footprint: **26.7 square feet** before access/clearance, arranged approximately 8 feet long by 40 inches deep;
- tank-only example price: **$700 before freight**;
- planning budget: **$1,500-$3,000 installed**, including a modular commercial reserve, potable hose/fittings, opaque covers, valve protection, restraints, and freight. This range is `ASSUMED` until San Jose delivery and restraint quotes are obtained.

### Phase 2: high-heat expansion option

If the garage passes the site checks and Hooman wants 90 days even under the conservative sustained-heat calculation, add one further independent 275-gallon bulk module. Three 275-gallon totes plus 75-80 gallons modular provide about **900-905 gallons**. This adds approximately 2,424 pounds filled and 13.3 square feet before clearance.

## Storage alternatives and budgets

| Architecture | 500-gallon-scale example | Current indicative container cost | Maintenance | Main advantage | Main limitation |
|---|---:|---:|---|---|---|
| New potable-rated IBCs | 2 × 275 gal = 550 gal | $700 before freight for current candidate | Six-month replacement under CDC self-filled guidance | Lowest screened container cost; gravity outlet | Translucent; bulky; vulnerable valve; difficult seismic mass; exact potable documentation required |
| Purpose-built 160-gal stackable tanks | 3 × 160 + 20 gal modular = 500 gal | $2,097 for three tanks before freight and modular supply | Six-month authority guidance still controls | Compact, dark plastic, integrated valves | About 1,335 lb water/tank; stacking is undesirable without seismic design; expensive |
| WaterBricks | 15 ten-packs = 525 gal | $3,435 before freight | Six-month replacement | Highly modular; about 30 lb filled per 3.5-gal unit | 150 separate containers; high cost and inspection burden |
| Five-year emergency pouches | 158 DATREX cases ≈ 501 gal | About $9,679 before freight | Five-year manufacturer shelf life | Factory sealed and individually portioned | Prohibitively expensive and wasteful for bulk household sanitation |
| Commercial grocery bottled water | Labeled cases totaling 500 gal | Not yet locally priced | Observe printed expiration | CDC calls unopened commercially bottled water safest and most reliable | Large package count, leakage/waste risk, repeated purchase/rotation |
| One large 500-gal tank | 1 × 500 gal | Not yet normalized | Six-month replacement if self-filled | Efficient footprint and plumbing | Single-point failure; 4,170 lb water in one unit; access and seismic consequences |

Product costs are snapshots retrieved 2026-10-01 through 2026-10-05, not quotes. Purpose-built tank and WaterBrick claims are manufacturer claims, not independent proof of extended water shelf life. The DATREX five-year claim is a manufacturer specification tied to its sealed product.

## Safety, filling, and maintenance

### Non-negotiable authority guidance

- `VERIFIED`: Use commercially bottled water or food-grade water-storage containers. Do not reuse containers that held bleach, pesticides, or other toxic chemicals.
- `VERIFIED`: Self-filled water should be replaced every six months. Label each container "drinking water" and record the fill date.
- `VERIFIED`: Store water at 50-70°F, away from direct sunlight, gasoline, pesticides, and other toxic substances.
- `VERIFIED`: When tap water is known or suspected unsafe, do not use it for drinking, dishes, teeth, food, handwashing, ice, formula, or personal hygiene unless authorities say it is safe or it is appropriately treated.
- `VERIFIED`: Boiling or disinfecting does **not** make fuel-, chemical-, heavy-metal-, salt-, or radioactive-contaminated water safe.
- `VERIFIED`: Portable filters do not necessarily remove viruses, bacteria, chemicals, or all parasites. A filter is not a universal substitute for protected stored water.
- `VERIFIED`: CDC says people who are pregnant or have thyroid problems should avoid iodine-disinfected water; no one should use iodine-treated water for more than a few weeks. Given the reported thyroid medication and the unresolved clinical indication, iodine is not the proposed household treatment method unless her clinician or pharmacist confirms it is appropriate.

### Fill procedure for a self-filled potable tank

1. Confirm the exact container and every wetted component are documented for potable-water contact. Reject used, rebottled, or reconditioned IBCs for this plan.
2. Prepare the final level location, restraints, valve guard, drain path, and clearances before filling. A filled tote cannot be safely repositioned by hand.
3. Follow the container instructions. CDC's container sanitation method is: wash with soap and rinse completely; contact all interior surfaces with a solution of **1 teaspoon unscented 5-9% sodium-hypochlorite bleach per 1 quart of water**; wait at least 30 seconds; drain; and air-dry. A large tank needs enough solution and an appropriate circulation/contact method to reach every interior surface.
4. Fill with currently safe municipal water through a drinking-water-safe hose. Do not add a proprietary preservative merely to extend rotation unless its exact use is independently validated for this application.
5. Close tightly. Label as drinking water with fill and mandatory replacement dates. Record the tank, valve, and batch in the inventory.
6. Leak-check at partial fill and again when full. Keep the outlet physically protected and child-resistant.
7. Dispense through a clean outlet/hose into a clean container. Do not insert hands or an unclean scoop.
8. At six months, drain into landscaping, cleaning, or toilet use where appropriate; inspect and sanitize; then refill. Do not let conservation concerns delay safe replacement.

Implementation note, 2026-10-28: this tank's molded ridges retain less than one cup even after repeated inversion. CDC says to pour out the sanitizer and air-dry but does not specify how to handle a large container that cannot drain fully. Because this tank remained open outdoors under cheesecloth for two days, the practical project decision is to repeat sanitation in a clean protected area, drain as fully as practical, slosh-rinse once with two gallons of currently potable municipal water, drain again, and fill immediately. Do not insert towels, sponges, or a non-food-safe vacuum. This adaptation remains a researcher decision rather than a CDC-specific instruction.

Keep fresh unscented household bleach in the emergency kit for authority-directed disinfection; EPA says liquid bleach used for that purpose should be stored at room temperature for less than one year. Bleach concentration varies, so treatment dosing must follow the current EPA/CDC table and product label at the time of use, not a memorized generic number.

## Placement and seismic constraints

### Garage

The garage is the leading location. Hooman has chosen to handle exact placement details rather than make photos, measurements, or a temperature logger prerequisites to the starter purchase. The applicable safety constraints remain:

- The tanks are on a level, sound slab with their concentrated load and restraint design reviewed for the actual slab. Do not place filled bulk tanks on ordinary household shelving.
- They are away from gasoline, paint, pesticides, solvents, batteries, exhaust, ignition/heat sources, and vehicle impact.
- They do not block vehicle or pedestrian egress, utilities, electrical panels, or emergency access.
- Each container has an opaque cover, independent restraint, protected valve, and enough clearance for inspection and complete draining.
- At least one modular reserve remains reachable if the garage door or one storage zone is damaged.

The official NOAA 1991-2020 normal daily maximum for San Jose reaches 81.4°F in August. This is outdoor airport data, not a measurement or reliable estimate of this garage's interior temperature. It supports treating a typical unconditioned garage as warmer than CDC's preferred 50-70°F range during some summer periods, not inventing an exact garage average. Use the coolest interior location available, keep the tank opaque and out of sunlight, and retain the six-month replacement schedule.

The proposed two-tote expansion system places roughly 2,424 pounds gross on each 48 × 40-inch pallet footprint. Tank temperature rating is not the same as a safe long-term water-storage temperature; the current candidate's 120°F tank rating does not override CDC's 50-70°F water-storage guidance.

### Backyard

The current unroofed backyard is **not acceptable for the potable reserve as-is** because CDC says to keep stored water away from direct sunlight and at 50-70°F. Outdoor use would require, at minimum, a secure opaque weather enclosure, stable engineered pad, verified temperature control, protected valves, seismic/wind restraint, pest control, drainage, access, and local code/HOA review. Wildfire radiant heat and evacuation access also remain unresolved. An opaque tank or UV inhibitor alone does not establish that its water stays within CDC's temperature guidance.

## Hazard-specific operations

- **Earthquake:** modular redundancy matters because tanks, valves, garage doors, and plumbing can fail independently. Do not flush toilets or use house plumbing until local authorities confirm water and sewer status. Keep a small reserve reachable without entering a visibly damaged structure.
- **Water contamination:** isolate stored tanks from house plumbing. Follow the exact public-health advisory; boiling and chlorine only address certain biological hazards, not fuels or toxic chemicals.
- **Power outage:** use gravity outlets and a manual pump. Electric washers, dishwashers, well pumps, and water heating may be unavailable even when stored volume exists.
- **Wildfire:** a 90-day stationary reserve does not replace evacuation water. Keep a separate grab-and-go cache; do not remain to protect bulk water when ordered to evacuate.
- **Supply disruption:** use the oldest commercial stock first and preserve the protected potable floor. Shift early to low-water sanitation rather than spend drinking water on routine flushing.
- **Complete utility loss:** the survival tier is operable; the 7,500-gallon comfort model is not unless power, wastewater disposal, heating, and appliance functions are separately solved.

## Contradictions and rejected shortcuts

- **Five-year self-filled storage additives:** some manufacturers claim proprietary copper/silver or other products keep tank water usable for up to five years. The inspected federal guidance still says replace self-filled water every six months. Manufacturer claims do not yet clear the evidence gate, so the plan does not use them to extend rotation.
- **Used food-grade totes:** a tote advertised as "food grade" after prior use is not equivalent to a new container with a verified history. Unknown residues, valves, gaskets, cleaning chemicals, and permeation create avoidable uncertainty.
- **One giant tank:** cheaper plumbing and footprint do not compensate for losing the entire reserve to one crack, valve failure, contamination event, or inaccessible location.
- **Backyard without an enclosure:** UV-resistant plastic does not solve direct sun, heat, wildfire exposure, tampering, valve damage, or CDC's cool-storage guidance.
- **A filter as the whole plan:** consumer filters have organism and chemical limits and need a source, power or labor, consumables, and validated throughput.
- **Storing comfort-tier volume first:** 7,500 gallons weighs over 31 tons and still depends on power and sewer service. It is more rational to secure the potable floor and develop low-water sanitation plus redundant replenishment before building comfort-scale storage.

## Open decisions and next validation

Immediate next decision: buy the recommended 55-gallon starter plus approximately 16 gallons of bottled water, or proceed directly to a delivered quote for the 275-gallon NTO tote.

After a starter tank arrives:

1. Inspect the item for damage, confirm it is new, and verify its food-grade/potable labeling and all supplied wetted parts before filling.
2. Set it on the level garage-slab location Hooman selects, away from sunlight, heat, toxic chemicals, vehicles, and child access.
3. Sanitize according to CDC/container instructions, fill from a safe municipal supply through a drinking-water-safe hose, leak-check, and label the fill and six-month replacement dates.
4. Store the bottled reserve separately and observe its printed expiration.

For later 275- to 630-gallon expansion, obtain a delivered San Jose quote, verify exact potable-contact documentation, and design appropriate valve protection and seismic restraint. Actual toilet, showerhead, washer, and dishwasher specifications remain necessary only before treating the comfort-tier model as household-specific.

## Sources

Sources 1-15 were retrieved 2026-10-01; sources 16-23 were retrieved 2026-10-05. CDC source 1 and WaterPrepared sources 14 and 16 were re-inspected 2026-10-14 and again 2026-10-28 for the tank-cleaning and filling procedure. EPA source 4 was re-inspected 2026-10-28 for current emergency chlorination guidance. Marketplace prices and availability can change.

1. CDC, "How to Create an Emergency Water Supply," updated and reviewed 2025-06-27. Primary federal public-health guidance. Supports minimum quantity, special populations, food-grade containers, six-month self-filled rotation, 50-70°F/dark/toxin-free storage, and sanitation procedure. https://www.cdc.gov/water-emergency/about/how-to-create-and-store-an-emergency-water-supply.html
2. CDC, "How to Make Water Safe in an Emergency," updated 2024-09-19. Primary federal public-health guidance. Supports unsafe-water use restrictions, treatment limits, filter limits, and iodine contraindications. https://www.cdc.gov/water-emergency/about/index.html
3. Ready.gov, "Water." Primary federal preparedness guidance. Supports one gallon/person/day for drinking and sanitation, increased nursing/child/hot-weather needs, commercial storage, and six-month replacement of noncommercial water. https://www.ready.gov/water
4. US EPA, "Emergency Disinfection of Drinking Water," modified 2026-02-24. Primary federal drinking-water guidance. Supports biological versus chemical-contamination limits, boiling, current bleach selection/dosing framework, and using properly disinfected water for food-contact/personal uses. https://www.epa.gov/ground-water-and-drinking-water/emergency-disinfection-drinking-water
5. WHO/WEDC, "How much water is needed in emergencies," Technical Note 9, updated July 2013. Primary international emergency WASH guidance. Supports 7.5-15 L/person/day simplified survival requirements, 20 L/person/day essential-health target, staged provision, 10% wastage example, and conventional versus pour-flush water ranges. Limitation: humanitarian/displaced-population context rather than a San Jose household. https://cdn.who.int/media/docs/default-source/wash-documents/who-tn-09-how-much-water-is-needed.pdf
6. US EPA WaterSense, "Residential Toilets." Primary federal product-efficiency guidance. Supports 1.28 gal/flush for WaterSense toilets. https://www.epa.gov/watersense/residential-toilets
7. US EPA WaterSense, "Showerheads." Primary federal product-efficiency guidance. Supports 2.0 gpm WaterSense and 2.5 gpm standard showerhead modeling. https://www.epa.gov/watersense/showerheads
8. US EPA WaterSense, "How We Use Water." Primary federal benchmark. Supports more than 300 gallons/day for the average American family and roughly 70% indoor use. Limitation: national average, not this household. https://www.epa.gov/watersense/how-we-use-water
9. ENERGY STAR, "Clothes Washers." Primary federal efficiency-program guidance. Supports 14 gal/load for full-size ENERGY STAR versus 20 for standard models. https://www.energystar.gov/products/clothes_washers
10. ENERGY STAR, "Dishwashers Key Product Criteria." Primary federal efficiency-program specification. Supports no more than 3.2 gal/cycle for standard-capacity models under the specification effective 2023-07-19. https://www.energystar.gov/products/appliances/dishwashers/key_product_criteria
11. American Kennel Club, "Is Your Puppy Drinking Enough Water?", updated 2026-03-27. Strong secondary veterinary guidance. Supports the general adult-dog estimate of 1 fluid ounce/pound/day and higher heat/activity needs. Limitation: not a disaster-water standard or peer-reviewed intake study. https://www.akc.org/expert-advice/health/puppy-drinking-enough-water/
12. Valley Water, "How we clean your water." Local primary utility context. Supports regional treatment infrastructure and the separation between wholesale treatment and local retailers. https://www.valleywater.org/your-water/water-quality/how-we-clean-your-water
13. National Tank Outlet, "275 Gallon New IBC Tote Tank," current product listing. Retail/manufacturer specification used only for candidate dimensions, price, materials, outlet, weight, and temperature rating. Product claims require documentation before purchase. https://www.ntotank.com/275gallon-nto-white-ibc-new-tote-tank-x2008473
14. WaterPrepared, product data and FAQ, current manufacturer material. Used for alternative 160-gallon and WaterBrick capacity, price, dimensions, and manufacturer claims. Does not independently verify extended water shelf life. https://waterprepared.com/collections/all and https://waterprepared.com/pages/faq
15. DATREX, "Emergency Overwrap Water," current manufacturer listing. Supports case content, $61.26 snapshot price, five-year manufacturer shelf-life claim, and cited USCG/ISO compliance. https://www.datrex.com/product/datrex-emergency-water-ration/
16. WaterPrepared, "55 Gallon Water Tank." Manufacturer source for the $269 direct price, dimensions, materials, integrated spigot, free-shipping statement, and FDA/NSF claims. https://waterprepared.com/products/blue-55-gallon-water-storage-tank
17. Amazon, WaterPrepared 55-gallon listing. Current marketplace purchase path; displayed $185.99 new before tax. Seller, price, stock, and ZIP-specific delivery require checkout verification. https://www.amazon.com/dp/B0785BHYFG
18. Amazon, Augason Farms 55-gallon water-storage drum. Marketplace source for the approximately $139.99 price, dimensions, food-grade-polyethylene claim, and lack of an integrated dispenser. https://www.amazon.com/dp/B06Y2H5GVX
19. National Tank Outlet, "275 Gallon New IBC Tote Tank." Updated candidate listing supporting the $350-before-freight snapshot, dimensions, empty weight, outlet, new-HDPE construction, and retailer's FDA-approved food-grade/potable designation. https://www.ntotank.com/275gallon-nto-white-ibc-new-tote-tank-x2008473
20. National Tank Outlet, two-inch female camlock to 3/4-inch garden-hose adapter. Current $20 accessory snapshot; polypropylene material. https://www.ntotank.com/2-pp-female-camlock-coupler-3-4-pp-garden-hose-thread-x6547824
21. Uline, 275-gallon IBC tank H-3886. Retailer source for $595 snapshot, dimensions, weight, BPA/FDA statements, and explicit statement that the item does not meet NSF 61. https://www.uline.com/Product/Detail/H-3886/IBC-Tanks/IBC-Tank-275-Gallon
22. Global Industrial, 275-gallon IBC WB493531. Retailer source for $485.95 snapshot, dimensions, weight, and FDA/UN-compliance claims. https://www.globalindustrial.com/p/ibc-container-275-gallon-un-fda-approved-with-steel-pallet-base
23. NOAA National Centers for Environmental Information, 1991-2020 Monthly Normals for San Jose station USW00023293. Primary federal climate data supporting the outdoor monthly normal daily maxima; it does not measure a residential garage. https://www.ncei.noaa.gov/access/services/data/v1?dataset=normals-monthly-1991-2020&stations=USW00023293&format=json&units=standard
