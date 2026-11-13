# V4 actual-prose audit

As of 2026-10-26T19:01:16.737002+00:00. This report audits 120 candidates from 4 completed cases. It does not edit V4 outputs.

## Outcome

- Prose budget exceedances: **11** candidates.
- Host-forbidden device/camera lexemes: **3** candidates; actual hardware references: **0**.
- Specific lived-in/use-state cues: **115/120** candidates.
- Excessive or unsoftened distress flags: **0** candidates.
- Median words: **42.0** (range 31–60).

Prose counts come from physical noun phrases in each scene paragraph. Model visual signatures appear only as a cross-check and may produce review flags when the two disagree.

## Flag counts

- `host_forbidden_device_lexeme`: 3
- `implausible_material_wear_pairing`: 1
- `prose_local_prop_budget_exceeded`: 11
- `signature_vs_prose_background_count_disagreement`: 8
- `signature_vs_prose_people_disagreement`: 1
- `signature_vs_prose_prop_count_disagreement`: 24
- `wide_missing_arrangement_relation`: 5
- `wide_missing_specific_use_state`: 5

## Repeated artifact screening

- `22fdbf19f03d1a31__laptop_FrontRightWide`: categories {'writing_tool': 16, 'paper_artifact': 20}; pairs {'paper_artifact + writing_tool': 14}
- `ee810cf51bb82bb4__printer_FrontRightCloseUp`: categories {'document_compound': 20}; pairs {}
- `ee810cf51bb82bb4__printer_FrontRightWide`: categories {'paper_artifact': 22, 'writing_tool': 24, 'document_compound': 17}; pairs {'paper_artifact + writing_tool': 20, 'document_compound + paper_artifact': 12, 'document_compound + writing_tool': 15}

## Candidates requiring prose review

### `22fdbf19f03d1a31__laptop_FrontRightCloseUp::p14`

Flags: `implausible_material_wear_pairing`

A tight section of a residential kitchen counter used as a temporary work surface, pale quartz with a softly dulled area near the edge. Clean morning light reveals subtle wipe arcs and a few fine pressure marks.

Prose counts: {'local_props': 0, 'background_details': 0, 'people': 0}; signature cross-check: {'local_props': 0, 'background_details': 0, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p1`

Flags: `signature_vs_prose_prop_count_disagreement`

A shared workspace meeting table with a marked-up decision brief, a capped pen resting across one circled item, and a visitor badge lying slightly askew from a recent check-in. A pinboard of overlapping room schedules and reminders sits in the background. Soft late-morning light catches the rubbed edge of the laminate and the dog-eared paper corners.

Prose counts: {'local_props': 2, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p3`

Flags: `signature_vs_prose_prop_count_disagreement`

A customer site conference counter with a clipped project packet opened to a sign-off page, a pen laid beside a checked box, and a visitor pass with a slightly curled corner. In the background, a frosted glass partition carries a few taped wayfinding notes. Clean side light glances across the counter’s lightly polished stone composite.

Prose counts: {'local_props': 2, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p4`

Flags: `signature_vs_prose_prop_count_disagreement`

A business lounge table set up between appointments, with a folded travel itinerary, an annotated meeting agenda, and a half-used adhesive note pad pushed slightly out of line. A low upholstered banquette sits behind it with a coat seam casually slumped along the cushion. Warm indirect light picks up tiny scuffs in the dark wood finish.

Prose counts: {'local_props': 1, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p8`

Flags: `signature_vs_prose_background_count_disagreement`

A home office desk with an open planner showing meeting times, a document draft with a few margin ticks, and a pen resting diagonally between them. A bookshelf with unevenly aligned paperbacks sits softly behind the work surface. Afternoon daylight brings out the honeyed wood grain and a faint wiped ring near the planner.

Prose counts: {'local_props': 3, 'background_details': 0, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p11`

Flags: `wide_missing_arrangement_relation`

A kitchen table temporarily taken over for work, with a printed meeting agenda, a lined notebook opened to short action notes, and a mug leaving a faint damp crescent nearby. A simple dining chair with a softened seat edge sits behind it. Morning light cuts across the worn varnish and the slightly curled agenda corner.

Prose counts: {'local_props': 3, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p12`

Flags: `host_forbidden_device_lexeme`, `signature_vs_prose_background_count_disagreement`

A compact coworking phone-room shelf with a folded call checklist, a pen pressed into the page crease, and a small reservation card left from the previous user. A felt-lined wall panel sits close behind the shelf. Even overhead light picks out tiny rubs along the shelf lip and the checklist’s thumbed edge.

Prose counts: {'local_props': 3, 'background_details': 2, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p13`

Flags: `signature_vs_prose_background_count_disagreement`, `signature_vs_prose_prop_count_disagreement`

A small design review table with a printed content storyboard, a pencil laid over a changed sequence, and a clipped packet of notes shifted just off center. A wall rail holding overlapping project sheets sits in the background. Clear daylight emphasizes the table’s matte surface and the rubbed graphite smudges along the storyboard edge.

Prose counts: {'local_props': 2, 'background_details': 0, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p14`

Flags: `signature_vs_prose_prop_count_disagreement`

A customer-site waiting area ledge with a folded appointment sheet, a marked contract excerpt, and a pen clipped over a paragraph. A textured wall panel behind the ledge holds a small room-number plaque. Side light makes the stone ledge’s polished edge shine where hands and papers have passed through the day.

Prose counts: {'local_props': 2, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p16`

Flags: `signature_vs_prose_prop_count_disagreement`

An airport café counter with a folded boarding pass, a marked meeting note, and a paper cup with a creased sleeve set close to the notes. A row of blurred stool backs sits low in the background. Bright terminal light reflects softly from the speckled counter and the softened crease of the boarding pass.

Prose counts: {'local_props': 2, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p18`

Flags: `wide_missing_arrangement_relation`

A maker studio planning bench with a sketched production checklist, a metal ruler set across one revised measurement, and a pencil with a worn eraser. A pegboard with a few hanging templates sits behind the bench. Diffuse skylight catches fine sanding dust settled into the bench’s shallow scratches.

Prose counts: {'local_props': 3, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p19`

Flags: `signature_vs_prose_prop_count_disagreement`

A small café table during a pause, with a ceramic cup showing a lowered coffee line, a paperback folded open, and a pastry bag pinched shut with crumbs nearby. A worn wooden chair back sits behind the table. Mild window light skims the varnished surface and the uneven ring left by the cup.

Prose counts: {'local_props': 1, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p20`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`

A breakfast table at home with a folded newspaper section, a butter knife resting on a small plate with toast crumbs, and a linen napkin rumpled beside it. A simple chair rail lines the background. Clear morning light reveals the table’s lightly rubbed varnish and a few shallow utensil marks near the plate.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p24`

Flags: `signature_vs_prose_background_count_disagreement`, `signature_vs_prose_people_disagreement`, `signature_vs_prose_prop_count_disagreement`

A teacher preparation counter with a corrected worksheet, a roll of masking tape, and a red pencil angled over a circled note. A classroom cubby edge with uneven paper labels sits behind the counter. Soft side light reveals the laminate’s gentle rubs and a turned-up worksheet corner from repeated handling.

Prose counts: {'local_props': 2, 'background_details': 0, 'people': 1}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p26`

Flags: `signature_vs_prose_background_count_disagreement`

A home craft table with a folded fabric square, a small tin of loose buttons, and a needle card set at a slight angle. A wicker basket with soft yarn ends sits in the background. Overcast daylight shows the maple surface’s satin sheen and the tiny thread fibers caught near a shallow scratch.

Prose counts: {'local_props': 3, 'background_details': 0, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p28`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`

A student art table with a watercolor sheet drying at one edge, a rinsed brush laid on a folded paper towel, and a palette with diluted color wells. A smudged supply shelf sits behind the work area. Gentle daylight reveals faint paint ghosts and old tape marks across the sealed tabletop.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p29`

Flags: `signature_vs_prose_background_count_disagreement`, `signature_vs_prose_prop_count_disagreement`

A puzzle break table with a partly sorted cluster of pieces, a folded clue booklet, and a glass of water with a faint condensation trail. A low fabric ottoman sits just behind the table. Quiet afternoon light skims the matte surface and the tiny paper dust around the puzzle edges.

Prose counts: {'local_props': 2, 'background_details': 0, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `22fdbf19f03d1a31__laptop_FrontRightWide::p30`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`

A ceramics studio glazing bench with a small bisque test tile, a labeled glaze jar, and a brush resting across a stained rag. A simple drying rack sits behind the bench. Cool studio light picks up speckles of dried glaze and the smoothed patches where the bench has been wiped clean many times.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p3`

Flags: `wide_missing_specific_use_state`

An entryway paperwork shelf turned into a household administration spot, with a slightly bowed folder of records, a small stack of color pages and a pen cap resting beside a fresh check mark. A row of wall hooks softens the background. Late-day side light catches scuffs in the painted wood.

Prose counts: {'local_props': 3, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p5`

Flags: `signature_vs_prose_background_count_disagreement`, `signature_vs_prose_prop_count_disagreement`

A hallway household administration station on a narrow oak surface, with a folder of records opened to a clipped form and a pencil angled across a handwritten note. A shallow mail cubby sits in the background. Soft evening light brings out the surface’s polished center and gently dulled edges.

Prose counts: {'local_props': 2, 'background_details': 0, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p6`

Flags: `host_forbidden_device_lexeme`, `signature_vs_prose_background_count_disagreement`

A home records corner with a waxed pine desktop holding a labeled file packet, a short stack of everyday forms and a pen left uncapped beside a corrected date. A simple notice board sits behind it with overlapping household reminders. Cloudy daylight keeps the paper texture soft and believable.

Prose counts: {'local_props': 3, 'background_details': 0, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p7`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`

A shared family paperwork counter with a binder of records lying open, two color handouts tucked under a binder clip and a pencil set down after a quick note. A woven chair back appears softly in the background. Early light reveals small rubbed patches where papers have been slid back and forth.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p10`

Flags: `signature_vs_prose_prop_count_disagreement`, `wide_missing_specific_use_state`

A department document table with longer paperwork divided into a clipped set, a slim folder of records and a yellow sticky note marking the next section. A lightly worn task chair sits in the background. Overcast light flattens the shadows and shows shallow scuffs in the gray work surface.

Prose counts: {'local_props': 2, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p13`

Flags: `host_forbidden_device_lexeme`, `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`

A small business paperwork desk with an uneven pile of forms, a tabbed records folder and a pen balanced across a page with two circled totals. A shelf of mismatched binders sits behind it. Clear midmorning light makes the desktop’s rubbed writing area visible without turning the scene formal.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p14`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`

A shared paperwork area with a recurring document queue suggested by three bundled form sets, a manila records folder and a pencil tucked under the top sheet. A pinboard with overlapping shift notes sits beyond the work surface. Cool daylight shows the counter’s smoothed spots from daily sorting.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p16`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`, `wide_missing_specific_use_state`

A community office paperwork counter with handouts stacked beside a records packet and a pencil lying across a half-filled cover sheet. A corkboard with layered notices gives the background practical context. Soft overhead light reveals faint grooves from years of writing through paper.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p17`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`

A meeting-room document prep table with repeated document sets squared into a low stack, a folder of records and a pen left beside a ticked checklist. A whiteboard with partially erased boxes sits in the background. Side daylight reveals soft table-edge wear from regular paperwork sessions.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p18`

Flags: `wide_missing_specific_use_state`

A shared admin touchdown table with a clipped packet of forms, a color materials proof sheet and a pencil laid across a note that says to file by Friday. A low cabinet with uneven labels sits behind it. Bright diffuse light shows the tabletop’s subtle dull patch where pages are sorted daily.

Prose counts: {'local_props': 3, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p20`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`, `wide_missing_specific_use_state`

A library program materials table with handouts fanned into a short stack, a sign-in record sheet and a capped marker nudged sideways after labeling a packet. A low book cart sits in the background. Soft skylit daylight brings out the table’s lightly scratched plastic edge.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p21`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`

A design studio review table with a marked color materials sheet, a folder of client notes and a pencil sitting diagonally across a revised swatch list. A pinboard of overlapping references sits behind the surface. North-facing daylight picks out shallow cut marks in the pale plywood.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p24`

Flags: `wide_missing_arrangement_relation`

A café corner table with a compact planning sheet, a pencil and a small plate with pastry crumbs, all slightly out of line as if someone stepped away mid-break. A chalk menu sits softly in the background. Warm daylight shows faint ring marks in the dark wood.

Prose counts: {'local_props': 3, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p25`

Flags: `wide_missing_arrangement_relation`

A study table with a corrected worksheet, a soft-cover notebook opened to a worked page and a pencil left near an erased line. A low shelf of uneven books sits behind the surface. Cloudy daylight catches the worksheet’s turned corner and the table’s shallow writing impressions.

Prose counts: {'local_props': 3, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p26`

Flags: `signature_vs_prose_prop_count_disagreement`

An editorial layout table with a marked proof page, a roll of masking tape and a capped red pencil resting beside a revised headline. A pinboard of overlapping clippings sits behind it. Soft daylight reveals tiny blade marks and rubbed graphite smudges in the cutting mat.

Prose counts: {'local_props': 2, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p27`

Flags: `signature_vs_prose_prop_count_disagreement`

A quiet home side table with a paperback left open face-down, a pair of reading glasses and a coaster shifted off its usual pale circle. A fabric chair with softened arms sits in the background. Late afternoon light warms the walnut surface and its small everyday rubs.

Prose counts: {'local_props': 2, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p29`

Flags: `prose_local_prop_budget_exceeded`, `signature_vs_prose_prop_count_disagreement`

A morning café table with a ceramic espresso cup, a folded newspaper section and a teaspoon resting across a napkin with a small sugar mark. A softly worn banquette sits behind it. Cool daylight skims the marble surface and its faint wiped streaks.

Prose counts: {'local_props': 4, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

### `ee810cf51bb82bb4__printer_FrontRightWide::p30`

Flags: `wide_missing_arrangement_relation`

A ceramics studio glazing bench with a small bisque tile, a stained brush rest and a notebook page carrying glaze-ratio scribbles. A peg rail with hanging aprons sits softly behind the bench. Milky daylight shows dried slip flecks and the sealed wood’s rubbed working area.

Prose counts: {'local_props': 3, 'background_details': 1, 'people': 0}; signature cross-check: {'local_props': 3, 'background_details': 1, 'people': 0}

## Limitations

- Rule-based noun-phrase counts are intentionally conservative and surface all signature disagreements for human review.
- A lexical cue is evidence in text, not proof that the downstream rewrite or image retains it.
- Context mixing, distress, and coherence flags are screening signals rather than automatic quality verdicts.
- Probe findings do not establish behavior of all 18 banks until all 540 candidates are available.
