# V6.2 surfaces r4 text audit

Audited 2026-11-09. Scope is the 16-bank, 160-prompt GPT-5.5 text run in `v6.2-surfaces-20261109-r4`. This was a read-only review: no model calls, prompt edits, runtime edits, or image generation.

## Outcome

- The r4 runtime returned 11 successful banks and 5 terminal-error banks. Six laptop banks passed on attempt 1, two laptop banks used repair, all eight printer banks used repair, and five printer banks remained rejected by r4 recognition.
- I independently passed the final normalized GPT response from every bank through the frozen `v6.2-surfaces-20261109-r5-recognition` validator and finalizer: **16/16 banks pass**. Finalization preserves the prompt-text multiset and sorts every bank by descending source relevance, then C-Tech score.
- No unresolved factual prompt-policy failure was found in the 160 final normalized prompts. The five r4 terminal failures were bounded recognizer or relationship false positives described below.

## Surface compliance

- Laptop aggregate: 35 round, 5 oval, 3 rectangular, and 37 unspecified primary shapes across 80 prompts. Every bank has at least four recognized round primaries. All **14/14 Café prompts** have a recognized round primary table.
- Printer aggregate: 19 table, 18 freestanding-cabinet, 20 credenza/sideboard, and 23 fitted-counter primaries. Thus 61/80 are non-table. Every printer bank independently has at least three families and at least five non-table primaries.
- Supports are ordinary and role-credible: dedicated/resource/studio worktables; wide, low storage and flat-file cabinets; low credenzas/sideboards; fitted base cabinetry; and built-in equipment counters. No customer café, gaming, fragile, narrow, floating, or tall cabinet is used as a printer primary.

## r4 false rejections resolved by frozen r5

- `magic__printer_FrontCloseUp`, row 6: `A substantial home workspace sideboard stands along a plain wall...` was misread as an implausible/background sideboard. It is the first named primary support.
- `magic__printer_FrontLeftMedium`, row 6, and `magic__printer_FrontWide`, row 7: `Open cubbies containing plain color bins...` triggered `shelf_population_missing`. This is the exact approved composite `V61-EDU-030`, whose name is `open cubbies containing plain color bins` and whose groups are `storage_cubbies` and `open_shelving`.
- `tassel__printer_FrontRightCloseUp`, row 10: `a shallow wall box containing an abstract model mounted on the adjacent wall` triggered `printer_support_personal_prop`. It is approved composite `V61-STU-045`, located on the adjacent wall rather than on the built-in equipment counter.
- `tassel__printer_FrontWide`, row 5: `Fitted office base cabinets with a continuous worktop...` was treated as extra cabinetry instead of the first primary fitted support.

Two earlier metadata misses were also recognizer issues rather than scene failures. R4 recorded `A circular living-room end table...` as shape `unspecified`; r5 records it as round. R4 also rejected `A circular bistro table in a café...`; r5 extracts `circular bistro table` as a round primary. The repaired final text is compliant in either case.

## Other validation diagnostics

The first repaired Cashmere FrontCloseUp bank had two real authoring issues: the unresolved choice `a short call or working discussion`, and undeclared `nearby seating`. Repair removed those exact phrases. Other repaired initial responses included genuine issues such as Office prose saying `home-office`, undeclared `worksheets`, and a repeated catalog group. Those issues are absent from the final normalized responses.

## Content review

- No prompt names a laptop, printer, computer, product model, brand, or generic device. The only `screen` uses are approved non-computing privacy screens.
- Prop declarations and repetition groups pass the frozen r5 checks in all 16 banks. Extra cabinets, sideboards, seating, wall treatments, and contents remain catalog-managed.
- Shelves, pegboards, cubbies, and wall boxes are populated by explicit approved props or by approved composite entries. `V61-GAM-024` is itself named `illuminated display shelving with abstract objects only`; the Cashmere FrontWide Gaming row therefore does not invent undeclared shelf contents.
- Close-up prompts use a local support arrangement plus limited wall/background context. No close-up asks for a full room, complete table perimeter, full cabinet base, or multiple competing layouts.
- Language is useful, ordinary, and physically plausible overall. No remaining prompt-level issue warrants blocking deterministic r5 publication.

## Publication implication

Use the unchanged final normalized GPT responses with the frozen r5 validator/finalizer, retaining the r4 raw attempts and rejection diagnostics as provenance. The r4 success/error status alone is not a reliable publication filter because its five terminal errors are the false rejections above.
