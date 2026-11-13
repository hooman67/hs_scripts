# Household Emergency Food Plan

As of: 2026-11-07

Research status: household diagnostic, authority review, Costco and Target package screening, calorie calculation, and initial emergency-cooking/fuel decision are complete. Hooman confirmed buying the counted 14-day Costco basket with three Horizon milk cases, except that canned beans/chickpeas, mandarin cups, and orange/dark-green vegetables were unavailable. The confirmed purchase therefore carries a conservative planning count of 99,310 kcal before uncounted vegetables. Received Nutrition Facts panels have not been audited.

The original illustrated purchase sheet is `/home/colligo/hs_scripts/claude/s_research/research/food/COSTCO_14_DAY_SHOPPING_LIST_WITH_PHOTOS.docx`. The current add-on lists are `/home/colligo/hs_scripts/claude/s_research/research/food/COSTCO_41_DAY_FOOD_ADD_ON_WITH_PHOTOS.docx` and `/home/colligo/hs_scripts/claude/s_research/research/food/TARGET_41_DAY_FOOD_ADD_ON_WITH_PHOTOS.docx`.

## 2026-11-07 implementation and 41-day add-on

- `[USER-CONFIRMED]` Hooman bought all counted rows in the illustrated Costco list in their listed quantities, including three 18-carton Horizon milk cases. Costco did not have the proposed canned beans/chickpeas, mandarin cups, or orange/dark-green vegetables.
- `[USER-CONFIRMED]` Hooman bought two additional 55-gallon WaterPrepared tanks. They have not arrived or been sanitized and filled, so their water is planned rather than stored.
- `[ASSUMED]` Four bottled-water cases contain 40 bottles of 16.9 fluid ounces each. On that assumption, three full tanks plus the cases hold `3 × 55 + 4 × 40 × 16.9 ÷ 128 = 186.125 gallons`, or `186.125 ÷ 4.5 = 41.36 days` at the project's household floor.
- `[RESEARCHER DECISION]` Match the planned water horizon with at least 41.36 days of food at 6,000 kcal/day. The target is about 248,167 kcal. The confirmed basket contributes 99,310 counted kcal, leaving about 148,857 kcal.
- `[PROPOSAL]` The two illustrated add-on lists contribute 153,300 counted kcal: 91,580 from Costco and 61,720 from Target. Combined inventory would be 252,610 kcal, or 42.10 days at 6,000 kcal/day, leaving about 0.74 day beyond the assumed water duration.
- `[PROPOSAL]` Every add-on item requires no added cooking water. Some products still require or benefit from heating; the received package directions control. The add-on restores canned beans/chickpeas, fruit, and orange vegetables and adds ready brown rice, canned meals, shelf-stable protein, fat, dairy, and retort meals.
- `[LIMITATION]` Costco and Target product pages establish product identity and displayed label data, not San Jose shelf stock, current local price, received best-by date, or an audited owned calorie count. Recalculate any substitution from its package label.

## Confirmed household constraints

- `[USER-CONFIRMED]` Two adults, a 2-year-old, a breastfed 1-month-old, and a 50-pound dog live in the household.
- `[USER-CONFIRMED]` Hooman prefers red meat; his wife avoids red meat but eats chicken and fish.
- `[USER-CONFIRMED]` Normal foods include rice, beans, meat, and dairy. The household favors fresh food and ordinarily avoids canned foods.
- `[USER-CONFIRMED]` A utility gas stove, electric Ninja multicooker, outdoor charcoal Weber grill, and purchased Coleman Triton two-burner propane stove are available. A rocket stove and backpacking stove are deferred.
- `[USER-CONFIRMED]` Pantry and garage storage are available.
- `[USER-CONFIRMED]` Infant formula and a separate dog-food reserve are excluded at Hooman's direction.
- `[USER-CONFIRMED, 2026-10-28]` There are no reported food allergies, intolerances, medical diets, or toddler food restrictions. Brown rice is preferred over white rice.
- `[USER-CONFIRMED, 2026-10-28]` Usable propane is available for the Coleman stove. There is no hard budget or storage-space limit for this first 14-day food layer.
- `[VERIFIED, 2026-10-28]` The supplied Costco map link resolves to San Jose warehouse #148, 2201 Senter Road, San Jose, CA 95112.

## Immediate recommendation

Build a **14-day rotating food reserve** before buying long-life meal buckets. Divide it into:

1. **Three days requiring no cooking:** ready-to-eat foods that remain usable if gas, power, and safe outdoor cooking are unavailable.
2. **Eleven days of low-fuel foods:** rice, oats, pasta, red lentils, ready beans, shelf-stable proteins, dairy, fats, fruits, and vegetables.

The American Red Cross recommends a three-day evacuation supply and a two-week home supply of nonperishable, easy-to-prepare food. That is an authority-backed starting layer, not the project's final 90-day target.

## Calorie model

`ASSUMED`: Plan on **6,000 stored calories/day**, or **84,000 calories for 14 days**.

Basis:

- 35-year-old male, sedentary reference: 2,400 kcal/day.
- 34-year-old female, sedentary reference: 1,800 kcal/day.
- First six months of lactation: add 330 kcal/day.
- 2-year-old: 1,000 kcal/day.
- Reference sum: `2,400 + 1,800 + 330 + 1,000 = 5,530 kcal/day`.
- Rounded reserve target: 6,000 kcal/day, an approximately 8.5% margin.

These are population estimates, not personalized prescriptions. The official table states that actual calorie requirements vary with height, weight, activity, health, and other factors. This model excludes the breastfed infant's direct food and excludes the dog. If the dog is fed from this inventory, it will last less than 14 days.

## Exact proposed Costco-first shopping list

Buy these package configurations at Costco San Jose #148. Costco product IDs identify the current catalog listings; they do not prove that warehouse #148 has an item on the shelf at a particular moment. Warehouse inventory and price must be checked in the Costco app or at the shelf. The calorie figures use current listed package/label data and conservative rounding. The received labels remain controlling.

| Qty | Exact product and package | Costco product ID | Calorie calculation | Counted kcal | No-cook kcal |
|---:|---|---:|---:|---:|---:|
| 1 | Lundberg Organic Short Grain Brown Rice, 12 lb | warehouse item 219890 | 120 servings × 150 | 18,000 | 0 |
| 1 | Quaker Old Fashioned Rolled Oats, 10 lb (2 × 5 lb) | 100381521 | 113 servings × 150 | 16,950 | 0 |
| 1 | Garofalo Organic Pasta Variety Pack, 17.6 oz × 6 | 100381417 | 54 servings × 210 | 11,340 | 0 |
| 1 | Kirkland Signature Organic Peanut Butter, 28 oz × 2 | 100334334 | 50 servings × conservative 180 | 9,000 | 9,000 |
| 3 | Crunchmaster 6-Seed Multi-Grain Crackers, 28 oz | 4000332792 | 3 × 26 servings × 140 | 10,920 | 10,920 |
| 1 | Kirkland Signature Organic Extra Virgin Olive Oil, 2 L | 100334841 | about 135 Tbsp × 120 | 16,200 | 0 |
| 1 | Tasty Bite Organic Madras Lentils, 10 oz × 8 | 4000444157 | 8 pouches × 260 | 2,080 | 2,080 only if received package says ready-to-eat without heating |
| 1 | Horizon Organic Whole Shelf-Stable Milk, 8 fl oz × 18 | 100533380 | 18 cartons × 150 | 2,700 | 2,700 |
| 1 | Kirkland Signature Chicken Breast, 12.5 oz × 6 | 100334960 | 6 cans × 3.5 servings × 60 | 1,260 | 1,260 |
| 1 | Kirkland Signature Wild Alaskan Pink Salmon, 6 oz × 6 | 100334750 | conservative 150 per can × 6 | 900 | 900 |
| 1 | Kirkland Signature Premium Brisket Roast Beef, 12 oz × 4 | 100082718 | conservative 240 per can × 4 | 960 | 960 |
| 1 | Kirkland Signature Organic Applesauce, 3.17 oz × 24 | 100334203 | conservative 45 per pouch × 24 | 1,080 | 1,080 |
| 1 | Del Monte Whole-Kernel Corn, 15.25 oz × 12 | 100443694 | 12 cans × 3.5 servings × 60 | 2,520 | 2,520 |
|  | **Counted total** |  |  | **93,910** | **31,420** |

The total exceeds the 84,000-calorie target by **9,910 kcal, or 11.8%**. The no-cook subset exceeds 18,000 kcal by **13,420 kcal, or 74.6%**. This margin absorbs modest label variation, damage, or a rejected item; it does not add calories for the breastfed infant or dog.

Also buy one Del Monte Canned Cut Green Beans case, 14.5 oz × 12 (Costco product 100443940), for vegetable variety; its calories are not needed to pass the target. Obtain a sturdy manual can opener if one is not already available. Salt and familiar low-sodium seasonings may come from the normal pantry and are not duration-critical.

If any exact item is absent, substitute only by role and package-label calories: brown rice for brown rice; dry oats/pasta for cooked staples; smooth peanut butter plus crackers for no-cook calories; shelf-stable single-serving milk for milk; fully cooked shelf-stable chicken/fish/beef for protein; and single-serving unsweetened fruit for applesauce. Recalculate the two totals before checkout. Do not substitute refrigerated products into the emergency count.

The list deliberately uses cans and retort packages despite the household's ordinary preference. They remain usable when refrigeration, utility gas, and safe outdoor cooking are unavailable. A planning checkout budget is **about $200-$275 before tax**, but this is not a warehouse #148 quote; Costco's live local prices were not publicly exposed in the inspected unsigned catalog session.

## Three-day no-cook sub-cache

Set aside the peanut butter, all three cracker packages, shelf-stable milk, canned meats/fish, applesauce, and corn in one clearly marked bin. The conservatively counted total is **29,340 kcal before the Madras lentils**, so the bin still clears 18,000 kcal if those pouches require heating. Use combinations of:

- nut butter and crackers;
- ready beans;
- chicken, salmon, sardine, or beef pouches/cans;
- shelf-stable milk in packages that can be finished promptly;
- packaged fruit;
- Madras lentils only if the received label confirms they are fully cooked and safe to eat without heating.

Do not make this layer dependent on heating, refrigeration after opening, an electric can opener, or the outdoor grill.

## Nutrition and family fit

- Current 2025-2030 federal guidance emphasizes minimally processed foods, protein, vegetables, fruits, dairy/healthy fats, and whole grains. A reserve made only of rice and dry beans would be calorie-capable but nutritionally and operationally incomplete.
- CDC says well-nourished breastfeeding mothers generally need an additional 330-400 kcal/day; the first-phase calculation uses 330 because the infant is one month old.
- Use separate clearly labeled chicken/fish and beef packages so every meal does not force one adult's preference on the other.
- For the 2-year-old, stock familiar age-appropriate foods and textures. Follow current pediatric guidance on choking hazards and allergies; do not improvise new foods during an emergency.
- Give the toddler smooth peanut butter only in a thin layer on an age-appropriate food, never as a spoonful or thick glob. Break or soften hard crackers as needed, serve the child seated and supervised, and remove pouch caps immediately. The no-cook calorie count does not require whole nuts or dried fruit, avoiding two common choking hazards; it also avoids raisins, which are hazardous to the dog.
- The model contains no infant formula by user choice.
- The model contains no dog-food allocation. Ordinary family foods are not automatically safe for dogs; onions, garlic, grapes/raisins, chocolate, and xylitol are examples of hazards. Dried fruit and other unsafe foods must be kept away from the dog.

## Water and cooking dependency

The proposed rice, oats, pasta, and lentils consume safe water and fuel. Use soaking and absorption-style cooking rather than boiling in excess water and discarding it. The exact cooking-water and fuel budget will be measured in the menu-test batch before expanding to 30 or 90 days.

Do not assume the utility gas stove works during every emergency. CDC states that charcoal grills and portable camp stoves produce carbon monoxide and must never be used indoors. The Weber and any future rocket stove are outdoor-only and may be unusable during wildfire restrictions, heavy smoke, severe weather, or evacuation. That is why a no-cook food layer is mandatory.

## Confirmed emergency cooking and fuel decision

`[USER-CONFIRMED]`: The Coleman Triton two-burner propane stove is the primary outdoor emergency and vehicle-evacuation cooker. The existing Weber kettle is the secondary solid-fuel cooker. A rocket stove and backpacking stove are deferred.

The confirmed mixed 90-day fuel target is:

- three full 20-pound propane cylinders;
- four 1-pound propane cylinders for evacuation/direct-connect redundancy; and
- 80 pounds of plain charcoal briquettes.

No fuel, bulk-cylinder hose, or storage purchase is inferred complete. Implementation is staged: first obtain two 20-pound cylinders, the four 1-pound cylinders, and 40 pounds of charcoal; conduct a two- or three-day meal test; then add the third cylinder and remaining 40 pounds if the measured rate supports the model.

`[ASSUMED]`: Moderate to higher-use family cooking consumes 0.50-0.75 pound propane/day. The Triton's 22,000 BTU/hour total maximum input is approximately one pound of propane per hour with both burners at maximum, so burner intensity and time drive the range. Sixty nominal pounds models approximately 80-120 days before losses. Charcoal planning uses 2-3 pounds per consolidated Weber session, making 80 pounds approximately 27-40 sessions. These figures are not measurements of this household.

For validation, weigh a propane cylinder before and after the test. The propane remaining is the cylinder's total weight minus the stamped tare weight (`TW`). Record charcoal weight, safe water used, cooking time, wind, burner settings, cookware, meals prepared, and leftovers.

`[VERIFIED as observed 2026-10-06]`: U-Haul's ZIP 95121 results listed its Tully Road location at 2395 Senter Road at $3.85/gallon plus tax. A nominal 20-pound fill is approximately 4.7 gallons, or about $18.10 plus tax. Recheck before travel. The current purchasing baseline is refillable 20-pound cylinders, with four one-pound cylinders reserved for mobility rather than bulk economics.

Use the Coleman five-foot high-pressure propane hose and adapter, model 2000035049, unless the received Triton documentation specifies otherwise. Bulk cylinders remain upright and outdoors in a shaded, ventilated, impact-protected location; neither an attached garage nor a sealed deck box is presumed acceptable. Charcoal remains dry, separate from ignition sources, and in pest/moisture-resistant storage. Both appliances are outdoor-only, and current fire restrictions control whether charcoal use is lawful.

## Power-outage operations

CDC states that, if doors remain closed, food is generally safe for up to four hours in a refrigerator, 48 hours in a full freezer, and 24 hours in a half-full freezer. At outage onset:

1. Keep refrigerator and freezer doors closed.
2. Use a thermometer and follow current CDC/local-health instructions; never taste food to determine safety.
3. Transition to shelf-stable food before spending scarce fuel or water merely to protect convenience foods.
4. Discard food exposed to floodwater or unsafe temperatures according to current authority guidance.

## Storage and rotation

- Keep brown rice, oil, nut butter, shelf-stable milk, meat/fish, and the no-cook bin in the cooler indoor pantry when possible. Brown rice's natural oils make it less storage-stable than white rice, so rotate it actively and obey the printed best-by date.
- Use the garage primarily for dry staples inside pest-resistant, food-contact-suitable containers, away from chemicals and direct sun. Garage heat shortens quality; printed storage directions and dates still control.
- Do not put the entire reserve into one large package. Once opened, smaller packages reduce contamination, pests, moisture exposure, and leftovers without refrigeration.
- Label each item with purchase date and printed best-by/use-by date. Review the inventory every six months and consume/replace the oldest items through normal meals.
- Do not infer that a dry food is safe indefinitely. Damaged, leaking, swollen, rusted-through, pest-contaminated, wet, or suspicious packages are rejected.

## Expansion path

- **Phase 1:** 14 days / at least 84,000 audited calories.
- **Phase 2:** 30-day rotating pantry / approximately 180,000 calories at the current planning rate.
- **Phase 3:** 90-day hybrid reserve / approximately 540,000 calories, divided into three independent 30-day lots.

The 90-day number is not yet a shopping list. It requires family menu tests, actual package-label calories, current pricing, storage volume/weight, cooking-water use, fuel use, and a decision about whether feeding the dog from household food should be modeled after all.

## Next validation

At the warehouse, photograph or record each received Nutrition Facts panel and best-by date before treating the 93,910-kcal projection as an audited owned inventory. Prepare three representative meals with utility gas turned off, using the intended outdoor backup where lawful and safe. Record package calories, water used, fuel used, preparation time, leftovers, and whether both adults and the toddler will actually eat the meal. Those results control the 30- and 90-day design.

## Sources

Authority sources were retrieved 2026-10-05 through 2026-10-07 and re-inspected 2026-10-28. Costco, Costco Same-Day, manufacturer, and current retailer-index data were inspected 2026-10-28.

1. American Red Cross, "Survival Kit Supplies." Recognized emergency-response organization. Supports three-day evacuation and two-week home supplies of nonperishable, easy-to-prepare food. https://www.redcross.org/get-help/how-to-prepare-for-emergencies/survival-kit-supplies.html
2. CDC, "Maternal Diet and Breastfeeding." Primary federal public-health guidance. Supports the general 330-400 kcal/day additional requirement and notes individualized factors. https://www.cdc.gov/breastfeeding-special-circumstances/hcp/diet-micronutrients/maternal-diet.html
3. USDA/HHS, *Dietary Guidelines for Americans, 2020-2025*, archived official edition, Appendix 2 tables A2-2 and A2-3. Supports the age/sex reference calorie estimates and +330 kcal for the first six months of lactation. It is used for transparent calorie sizing because the current edition does not provide the same age/sex calorie table in the inspected public summary; individual needs vary. https://odphp.health.gov/sites/default/files/2026-02/dietary_guidelines_for_americans-2020-2025.pdf
4. USDA/HHS, *Dietary Guidelines for Americans, 2025-2030*. Current federal nutrition framework. Supports emphasis on real/minimally processed foods, protein, vegetables, fruit, dairy/healthy fats, and whole grains. https://realfood.gov/ and https://cdn.realfood.gov/DGA.pdf
5. CDC, "Keep Food Safe After a Disaster or Emergency." Primary federal food-safety guidance. Supports refrigerator/freezer time limits and emergency food handling. https://www.cdc.gov/food-safety/foods/keep-food-safe-after-emergency.html
6. CDC, "About Carbon Monoxide." Primary federal public-health guidance. Supports the prohibition on indoor charcoal burning and indoor portable camp-stove use. https://www.cdc.gov/carbon-monoxide/about/index.html
7. FoodSafety.gov, "FoodKeeper App." Official USDA/HHS/FDA food-storage reference for product-specific storage guidance. https://www.foodsafety.gov/keep-food-safe/foodkeeper-app
8. Coleman, "Triton 2-Burner Propane Camping Stove." Manufacturer source for the 22,000 BTU total rating, two-burner design, and stated runtime/specifications. Access was partially blocked during retrieval; the material specification was cross-checked against the current retailer listing. https://www.coleman.com/grills-stoves/camping-stoves/multi-burner/triton-2-burner-propane-camping-stove/SAP_2157319.html
9. Coleman, "5-Ft. High-Pressure Propane Hose and Adapter," model 2000035049. Manufacturer compatibility source; access was partially blocked during retrieval, so the received stove/hose instructions remain controlling. https://www.coleman.com/grills-stoves/grill-stove-accessories/5-ft.-high-pressure-propane-hose-and-adapter/SAP_2000035049.html
10. U-Haul, "Propane near San Jose, CA 95121." Retailer source for the observed $3.85/gallon Tully Road refill listing; price and inventory are dynamic. https://www.uhaul.com/Locations/Propane-near-San-Jose-CA-95121/Results/
11. Bureau of Land Management California, "Fire Restrictions." Primary government source for current California-area restrictions and permit requirements; the exact incident location and current restriction order must be checked before charcoal or other open-flame use. https://www.blm.gov/programs/public-safety-and-fire/fire-and-aviation/regional-info/california/fire-restrictions
12. Costco, warehouse-locator API and San Jose warehouse page. Current retailer source establishing that the supplied map location is warehouse #148 at 2201 Senter Road, San Jose, CA 95112; it does not establish grocery shelf inventory. https://www.costco.com/w/-/ca/san-jose/148 and https://ecom-api.costco.com/core/warehouse-locator/v1/salesLocations.json?latitude=37.309872&longitude=-121.8523109&limit=10
13. Costco current catalog pages for Lundberg Organic Short Grain Brown Rice, Quaker Old Fashioned Rolled Oats, Garofalo Organic Pasta, Kirkland Organic Peanut Butter, Crunchmaster 6-Seed Crackers, and Kirkland Organic Extra Virgin Olive Oil. Retailer sources for package identity, current listing, and displayed supplier-label data; local price and stock vary. https://sameday.costco.com/store/costco/products/17090653-lundberg-family-farms-og-sht-grain-brn-rice-brown-rice-12-lb ; https://www.costco.com/p/-/quaker-oats-old-fashioned-rolled-oats-10-lbs/100381521 ; https://www.costco.com/p/-/garofalo-organic-pasta-variety-pack-176-oz-6-count/100381417 ; https://www.costco.com/p/-/kirkland-signature-organic-peanut-butter-28-oz-2-count/100334334 ; https://www.costco.com/p/-/crunchmaster-6-seed-multi-grain-crackers-28-oz/4000332792 ; https://www.costco.com/p/-/kirkland-signature-organic-extra-virgin-olive-oil-2-l/100334841
14. Costco current catalog pages for Tasty Bite Madras Lentils, Horizon shelf-stable whole milk, Kirkland canned chicken, canned pink salmon, canned roast beef, organic applesauce, whole-kernel corn, and cut green beans. Retailer sources for package identity and displayed supplier-label data; the received label and storage directions control. https://www.costco.com/p/-/tasty-bite-organic-madras-lentils-10-oz-8-count/4000444157 ; https://www.costco.com/p/-/horizon-organic-whole-milk-8-oz-18-count/100533380 ; https://www.costco.com/p/-/kirkland-signature-chicken-breast-125-oz-6-count/100334960 ; https://www.costco.com/p/-/kirkland-signature-wild-alaskan-pink-salmon-6-oz-6-count/100334750 ; https://www.costcobusinessdelivery.com/p/-/kirkland-signature-premium-brisket-roast-beef-12-oz-4-ct/100082718 ; https://www.costco.com/p/-/kirkland-signature-organic-applesauce-317-oz-24-count/100334203 ; https://www.costco.com/p/-/del-monte-canned-corn-whole-kernel-1525-oz-12-count/100443694 ; https://www.costco.com/p/-/del-monte-canned-cut-green-beans-145-oz-12-count/100443940
15. Lundberg Family Farms, "Organic Short Grain Brown Rice." Current manufacturer source for product identity and 45-minute stovetop directions. https://www.lundberg.com/products/organic-short-grain-brown-rice-2lb
16. Target, "San Jose East Store #2238." Current retailer source establishing the selected Target location at 3155 Silver Creek Road, San Jose, CA 95121. Local grocery stock and price remain dynamic. Inspected 2026-11-07. https://www.target.com/sl/san-jose-east/2238
17. Target current product pages for Good & Gather low-sodium black beans, low-sodium chickpeas, sliced carrots, pure pumpkin, and organic coconut milk; Dole mandarin oranges; Del Monte no-sugar-added peaches; Hormel chili with beans; Chef Boyardee beef ravioli; Ben's Original whole-grain brown ready rice; and less-sodium SPAM. Retailer sources for current package identity, package imagery, and displayed label data; received labels control. Inspected 2026-11-07. https://www.target.com/p/organic-low-sodium-black-beans-15oz-good-38-gather-8482/-/A-78654032 ; https://www.target.com/p/organic-low-sodium-chickpeas-garbanzo-beans-15oz-good-38-gather-8482/-/A-78654074 ; https://www.target.com/p/sliced-carrots-14-5oz-good-38-gather-8482/-/A-79466796 ; https://www.target.com/p/100-pure-pumpkin-15oz-good-38-gather-8482/-/A-81647715 ; https://www.target.com/p/organic-coconut-milk-13-5oz-good-38-gather-8482/-/A-54600365 ; https://www.target.com/p/dole-canned-mandarin-oranges-15oz/-/A-94987215 ; https://www.target.com/p/del-monte-no-sugar-added-sliced-peaches-14-5oz/-/A-13429371 ; https://www.target.com/p/hormel-gluten-free-chili-with-beans/-/A-95174560 ; https://www.target.com/p/chef-boyardee-beef-ravioli-15oz/-/A-13130178 ; https://www.target.com/p/ben-39-s-original-ready-rice-whole-grain-brown-rice-microwavable-pouch-8-8oz/-/A-13393706 ; https://www.target.com/p/spam-less-sodium-lunch-meat-12oz/-/A-13217522
