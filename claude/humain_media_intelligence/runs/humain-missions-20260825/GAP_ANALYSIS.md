# Humain baseline gap analysis

Status: framework and deterministic source evidence complete; semantic/retrieval evidence pending MI ingestion and postprocessing.

## Evidence standard

No collection gap is final until all three layers agree or discrepancies are explained:

1. source, canonical-manifest, stage, Feature Registry, Postgres, and OpenSearch completeness
2. deterministic/MI semantic coverage with asset IDs and timestamps
3. repeatable text/visual retrieval behavior with inspected evidence

Every apparent deficit will be labeled as exactly one of: source-data gap, ingestion gap, labeling gap, retrieval gap, or unresolved. An empty MI result alone is not evidence of source absence.

## Preliminary signals—not yet collection recommendations

| Signal | Deterministic evidence | Current classification | Required follow-up |
|---|---|---|---|
| Sparse audio eligibility | 1,144/9,436 videos (12.1%) have one or more audio streams | Possible source-data gap | Reconcile speech-stage eligibility/results; inspect language, dialogue, ambient sound, and silent tracks by mission/theme |
| Uneven Events mission size | One Events mission has 320 videos versus 1,870 in the other | Possible source-data gap | Compare semantic/event diversity per mission rather than aggregate Events counts |
| Sparse asset-level keywords | Present on 2,278/9,436 videos (24.1%) | Metadata gap | Compare captions/MI outputs; do not confuse missing keywords with missing visual content |
| Release flag not universal | 3,828/9,436 have `release_attached=false` | Governance signal | Confirm intended use and authoritative meaning before downstream sharing/training decisions |
| Strong short-form concentration | 7,882/9,436 videos are 5–10 seconds | Possible source-design constraint | Measure whether actions/events are truncated and whether temporal queries have sufficient evidence |
| Exact duplicate delivery | All 1,870 older `9c3e...` objects duplicate the newer delivery | Resolved redundancy | Keep one canonical copy and full provenance; do not request recollection based on raw delivery counts |
| Source dimension disagreement | 1,303 source-vs-coded mismatches; all decode | Metadata/normalization gap | Use probed dimensions for technical analysis; retain source values for provenance |

## Target-versus-observed matrix

Business weights and target minimums remain `TBD` until the who/what/where use cases and mission priorities are signed off. MI will populate observed counts/hours, diversity, redundancy, and evidence confidence for these cells:

- theme and subtheme: landmarks/places, food, lifestyle, events, clothing/fashion
- role: Saudi-positive, Arab-but-non-Saudi negative control, other negative control
- geography: region/city/place, urban/rural, landmark specificity
- setting: indoor/outdoor, public/private/commercial, modern/traditional
- activity: preparation, performance, movement, interaction, dining, shopping, worship-adjacent context where explicitly observable
- people: no people/single/group/crowd and role/action, without inferring sensitive identity
- clothing: traditional/modern, formal/casual, context, garment/accessory coverage
- food: still life/preparation/serving/dining, utensils, drinks, ingredient/dish evidence
- events: national/religious/seasonal/community/sport/entertainment only when evidence supports the label
- language/signage: spoken language, OCR/script, signs/menus/wayfinding
- production: portrait/landscape, shot scale, camera motion, lighting, time of day, weather, duration, technical quality
- redundancy: exact copies, near-duplicate visual clusters, dense semantic clusters, outliers

## Saved MI query suite

For every query, save the exact prompt, filters, top-k, returned asset IDs/timestamps, scores where available, and an evidence disposition. Repeat important agent queries to measure answer variability.

### Completeness and controls

- Return assets from each of the five declared themes, grouped by mission and delivery provenance.
- Find a known canonical asset by exact title and confirm its timestamps/stage outputs.
- Search for deliberately implausible concepts and measure false positives.
- Compare exact-title, keyword, semantic, and visual retrieval for the same sampled assets.

### Place and tourism

- Distinct identifiable landmarks, architecture types, streetscapes, interiors, markets, hospitality, transit, and wayfinding.
- Urban versus rural/desert/coastal/mountain settings, only where observable evidence supports the distinction.
- Indoor versus outdoor tourism contexts, day/night, weather, lighting, and crowd density.

### Food

- Finished dishes versus ingredient preparation, cooking, serving, dining, and cleanup.
- Utensils, table settings, drinks/non-alcoholic beverage evidence, menus, signage, and social dining.
- Visually repetitive dish/plate clusters and underrepresented preparation/action sequences.

### Clothing and lifestyle

- Traditional versus modern and formal versus casual garments in clearly evidenced contexts.
- Garments, footwear, accessories, shopping, work, leisure, family/group activity, and indoor daily life.
- False-positive checks for symbols or clothing cues that are visually similar but not Saudi-specific.

### Events

- Distinct event types, specific venues, performances, ceremonies, sports, audience/crowd behavior, preparation, and aftermath.
- Compare the 320-video and 1,870-video Events missions independently.
- National, religious, or seasonal labels only when explicit visual, OCR, speech, place, or source evidence supports them.

### Audio, language, OCR, and symbols

- Among audio-eligible assets only: speech/no speech, language evidence, dialogue versus ambient sound/music, transcription quality, and multi-speaker material.
- Arabic/English/other script OCR, signs, menus, labels, flags, emblems, and known false-positive symbol cases.
- Verify that no-audio assets are treated as ineligible rather than failed speech ingestion.

## Collection-brief gate

A next-round brief must include business use case, positive/negative-control role, geography/setting, current unique count/hours, target minimum, requested new unique count/hours, diversity constraints, exclusions, provenance requirements, anti-duplication rules, MI acceptance queries, and quantitative acceptance thresholds.

Do not infer nationality, ethnicity, religion, identity, or other sensitive attributes from appearance. Prefer `unknown` or separate groups when evidence is insufficient.
