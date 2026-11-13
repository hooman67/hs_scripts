# V6.1 props and scene details for review

Status: **V6.1 execution catalogue authorized by Hooman on 2026-11-03; review remains open for later refinement.** V6 remains frozen.

This proposal expands V6 with more visually distinct props, furnishings, and wall details. It also adds a stricter visual-family layer: semantically or visually similar objects count as one family across all ten prompts produced from one input.

## Global rules

- A visual family may appear in only one of the ten prompts, including foreground props, background furnishings, shelf contents, and wall details.
- Moving an object to the background does not make it a different family.
- Composite objects reserve every visible family they contain. A pen cup reserves both `tool_cup` and `writing_tools`; shelving with plants reserves both `open_shelving` and `plant`.
- Paper notebooks, sketchbooks, binders, folders, loose papers, worksheets, books, and similar flat paper objects all belong to `paper_materials`.
- Pens, pencils, markers, crayons, charcoal, and similar slim drawing or writing tools all belong to `writing_tools`.
- Cups, mugs, glasses, and bottles all belong to `drinkware`. Teapots, carafes, and serving jugs belong to the separate `serving_vessels` family.
- Human faces, portraits, figurative photographs, branded objects, recognizable characters, and additional digital devices are unavailable.
- Avoid objects likely to produce readable text. When a setting-defining object such as a café menu or whiteboard is necessary, it must remain a distant background detail with explicitly non-legible markings.
- Fixed architecture and the primary support surface are exempt from prop-family repetition, but their descriptive language must still vary across the ten prompts.
- Shelving, display ledges, and pegboards must be visibly populated. Their contents must use additional approved and declared prop families; never describe shelves or pegboards as empty or blank.
- Close-up prompts use a compact local arrangement and a restrained background cue. Medium prompts can establish one coherent background zone. Wide prompts may use layered local, mid-ground, wall, and architectural details without creating several competing focal areas.

## Cross-environment visual families

These families are global. Variants listed under different environments still collide with one another.

| Visual family | Included examples |
| --- | --- |
| `paper_materials` | Notebook, sketchbook, binder, document folder, loose papers, worksheets, textbook, art book |
| `writing_tools` | Pen, pencil, marker, crayon, charcoal, pastel, drawing pen |
| `tool_cup` | Pen cup, pencil cup, brush jar, brush holder |
| `paper_fasteners` | Stapler, paper clips, binder clips |
| `measurement_tools` | Ruler, set square, protractor, compass, measuring tape |
| `drinkware` | Mug, coffee cup, water glass, reusable bottle |
| `serving_vessels` | Teapot, carafe, milk jug, pressed-glass bottle |
| `food_bowl` | Fruit bowl, snack bowl, sugar bowl |
| `food_plate` | Pastry plate, snack plate, serving plate |
| `tray_catchall` | Serving tray, key tray, ceramic catchall |
| `eyewear` | Reading glasses, glasses case |
| `plant` | Houseplant, desk plant, hanging plant, herb pot |
| `open_shelving` | Bookshelf, bookcase, display shelving, open studio shelf |
| `closed_storage` | Low cabinet, side cabinet, storage cabinet, flat-file cabinet |
| `task_seating` | Office chair, classroom chair, drafting chair |
| `lounge_seating` | Accent chair, reading chair, lounge chair |
| `sofa` | Sofa, settee |
| `bench_seating` | Banquette, bench |
| `stool` | Café stool, studio stool |
| `floor_textile` | Area rug, woven rug, reading rug |
| `window_textile` | Curtains, sheers, café curtains |
| `soft_textile` | Throw blanket, cushion, floor cushion |
| `framed_wall_art` | Framed abstract print, framed student artwork, framed geometric composition |
| `wall_texture` | Limewash, textured plaster, exposed brick, concrete finish |
| `wall_slats` | Wood-slat wall, ribbed wood panel |
| `acoustic_wall` | Felt acoustic panels, geometric sound-diffusion blocks |
| `wall_relief` | Ceramic relief, carved panel, geometric relief panel |
| `wall_display_board` | Corkboard, pinboard, abstract material board |
| `wall_writing_board` | Whiteboard or chalkboard with non-legible background markings |
| `wall_shelving` | Floating shelf, picture ledge, wall-mounted display ledge |
| `floor_lighting` | Floor lamp |
| `task_lighting` | Desk lamp, task lamp |
| `pendant_lighting` | Pendant lamp, ceiling pendant cluster |
| `wall_lighting` | Wall sconce, geometric wall light |

# Home

## Smaller props

- `paper_materials`: clothbound notebook, blank household folder, closed paperback with an unmarked cover.
- `eyewear`: folded reading glasses or a plain glasses case.
- `drinkware`: ceramic mug, clear water glass, or matte reusable bottle.
- `serving_vessels`: ceramic teapot or clear water carafe.
- `food_bowl`: fruit bowl or small snack bowl.
- `tray_catchall`: wooden serving tray, small ceramic key dish, or woven valet tray.
- `fiber_craft`: ball of yarn with knitting needles.
- `sewing_kit`: closed sewing box with a loose measuring ribbon.
- `jigsaw_puzzle`: partially assembled abstract-color puzzle with no text or faces.
- `strategy_game`: wooden chess set or abstract peg game.
- `woven_storage`: small woven storage basket.
- `decorative_candle`: plain pillar candle or low ceramic candleholder.
- `reed_diffuser`: unlabelled glass diffuser with natural reeds. **New.**
- `stone_object`: small arrangement of smooth river stones. **New.**
- `wood_sculpture`: original abstract wooden tabletop sculpture. **New.**
- `ceramic_object`: matte ceramic ornament with a simple geometric form.
- `hourglass`: clear sand timer with no markings. **New for Home.**
- `coaster`: woven or cork coaster.

## Background furnishings and décor

- `sofa`: comfortable sofa.
- `lounge_seating`: upholstered accent chair or reading chair.
- `closed_storage`: low sideboard or tall residential storage cabinet. **Expanded.**
- `open_shelving`: bookshelf with unmarked spines kept softly out of focus.
- `floor_lighting`: simple floor lamp.
- `window_textile`: relaxed curtains or translucent sheers.
- `floor_textile`: woven rug.
- `soft_textile`: casually draped throw or textured cushion.
- `plant`: houseplant or trailing plant.
- `blanket_ladder`: simple wooden ladder with one plain textile. **New.**

## Wall and architectural details

- `framed_wall_art`: abstract art without text, faces, or recognizable characters.
- `woven_wall_hanging`: simple woven fiber wall piece. **New.**
- `wall_slats`: narrow natural-wood slats. **New.**
- `wall_texture`: warm limewash or lightly textured plaster. **New.**
- `acoustic_wall`: muted felt panels in a home workspace. **New.**
- `wall_relief`: small ceramic or carved-wood relief. **New.**
- `wall_shelving`: shallow picture ledge with one abstract ceramic form. **New.**
- `wall_lighting`: compact wall sconce. **New.**
- `geometric_wallpaper`: restrained nonfigurative pattern. **New.**
- `peg_rail`: wooden peg rail holding one plain woven basket or textile. **New.**

# Office

## Smaller props

- `paper_materials`: notebook, binder, folder, clipboard, or stack of plain papers; choose only one form for the entire ten-prompt bank.
- `writing_tools`: single pen or pencil; unavailable if another prompt already uses a writing or drawing tool.
- `tool_cup`: pen cup holding a few plain pens or pencils. **New and intentionally grouped with studio brush holders.**
- `paper_fasteners`: stapler, paper clips, or binder clips.
- `measurement_tools`: metal ruler or compact set square.
- `letter_tray`: empty architectural letter tray, or one holding only the already-declared `paper_materials` family.
- `document_box`: plain unlabelled document storage box.
- `eyewear`: folded reading glasses or plain glasses case.
- `drinkware`: water glass, matte bottle, or ceramic mug.
- `serving_vessels`: meeting-room water carafe. **New for Office.**
- `food_bowl`: fruit bowl or small snack bowl.
- `lunch_container`: plain closed lunch container.
- `tray_catchall`: low ceramic or felt desk tray. **New.**
- `paperweight`: clear glass or stone paperweight. **New.**
- `desk_sculpture`: small abstract metal or wood sculpture. **New.**
- `ceramic_object`: small unlabelled abstract ceramic form. **New for Office.**
- `kinetic_object`: unbranded metal balance toy with no text. **New.**
- `hourglass`: compact clear sand timer. **New for Office.**
- `material_samples`: two or three unlabelled architectural finish samples. **New.**
- `plant`: compact potted plant.
- `coaster`: cork, felt, or stone coaster.

## Background furnishings and décor

- `task_seating`: ordinary upholstered office chair.
- `open_shelving`: clean bookcase or open shelving with unmarked objects.
- `closed_storage`: low storage cabinet or tall filing cabinet with no labels. **Expanded.**
- `coat_stand`: simple coat stand with no visible garments.
- `floor_lighting`: floor lamp.
- `floor_textile`: area rug.
- `window_textile`: plain curtains or solar sheers.
- `plant`: potted floor plant.
- `room_divider`: translucent ribbed-glass divider. **New.**
- `meeting_screen`: freestanding felt privacy screen. **New; not a digital display.**

## Wall and architectural details

- `framed_wall_art`: abstract framed artwork.
- `acoustic_wall`: felt acoustic panels or geometric sound-diffusion blocks. **New.**
- `wall_slats`: vertical wood-slat feature. **New.**
- `wall_texture`: soft plaster, pale brick, or board-formed concrete finish. **New.**
- `wall_display_board`: blank corkboard or pinboard with unlabeled color blocks.
- `wall_writing_board`: whiteboard with distant, non-legible marks only when useful to the scene.
- `wall_planter`: shallow wall-mounted planter. **New.**
- `wall_shelving`: floating ledge with one abstract ceramic object. **New.**
- `wall_relief`: geometric relief panel. **New.**
- `wall_lighting`: slim architectural wall sconce. **New.**
- `glass_partition`: clear or frosted architectural partition.
- `perforated_panel`: powder-coated perforated metal panel. **New.**

# Education

## Smaller props

- `paper_materials`: textbook, exercise notebook, worksheet, folder, or binder; choose only one paper form for the entire bank.
- `writing_tools`: pencil, crayon, marker, or colored pencil.
- `stationery_utility`: eraser with a manual pencil sharpener.
- `measurement_tools`: ruler, protractor, or drawing compass.
- `tool_cup`: cup holding plain pencils; collides with office pen cups and studio brush jars. **New.**
- `counting_blocks`: loose group of solid-color counting blocks.
- `abacus`: wooden abacus with colored beads.
- `hourglass`: clear sand timer.
- `geometric_solids`: small set of wooden geometric solids. **New.**
- `balance_scale`: simple tabletop balance with no numbers. **New.**
- `magnifier`: handheld magnifying glass. **New.**
- `mineral_samples`: small set of unlabelled mineral specimens. **New.**
- `relief_globe`: unlabelled globe with raised land shapes and no rendered place names. **New.**
- `molecule_model`: original ball-and-stick molecular form with no label. **New.**
- `gear_model`: interlocking wooden gear demonstration. **New.**
- `color_sorting`: shallow cups with solid-color counters. **New.**
- `clay_model`: simple abstract student clay form.
- `origami_model`: plain geometric paper fold with no printed pattern.
- `watercolor_set`: unlabelled watercolor pans.
- `shape_puzzle`: wooden geometric inset puzzle. **New.**
- `prism`: clear optical prism casting a small spectrum. **New.**
- `magnetic_tiles`: small abstract construction made from translucent geometric tiles. **New.**
- `fossil_replica`: unlabelled shell or leaf fossil replica. **New.**
- `bridge_model`: small generic wooden truss model. **New.**
- `drinkware`: unlabelled reusable water bottle.

## Background furnishings and décor

- `task_seating`: classroom or library chair.
- `open_shelving`: low bookshelf with unmarked spines.
- `book_cart`: rolling library cart with books softly out of focus.
- `closed_storage`: storage cabinet or closed supply cupboard. **Expanded.**
- `storage_cubbies`: open cubbies containing plain color bins.
- `materials_cart`: rolling classroom materials cart. **New.**
- `floor_textile`: reading-area rug.
- `soft_textile`: floor cushion.
- `plant`: potted plant.
- `stool`: simple lab or art-room stool. **New for Education.**

## Wall and architectural details

- `wall_writing_board`: empty whiteboard or board with distant non-legible geometric marks.
- `wall_display_board`: corkboard with solid-color paper shapes and no text.
- `framed_wall_art`: abstract student artwork without faces, characters, or words.
- `geometric_mural`: simple color-block mural. **New.**
- `acoustic_wall`: soft geometric acoustic tiles. **New.**
- `relief_map`: unlabeled raised geographic wall panel. **New.**
- `shape_display`: wall-mounted arrangement of geometric solids. **New.**
- `colored_glass`: translucent colored wall inserts. **New.**
- `peg_rail`: wall rail holding plain aprons with no logos. **New.**
- `wall_slats`: pale wood slats. **New.**
- `wall_relief`: carved geometric learning panel with no symbols or text. **New.**

# Gaming

Gaming objects remain décor and hobby alternatives. They must not introduce controllers, consoles, headsets, monitors, recognizable characters, licensed imagery, or additional digital devices.

## Smaller props

- `strategy_game`: wooden chess set or abstract peg strategy game.
- `dice_game`: small group of plain dice with no branding.
- `puzzle_cube`: solid-color geometric puzzle cube.
- `mechanical_puzzle`: interlocking wooden or metal puzzle. **New.**
- `block_sculpture`: original building-block sculpture with no recognizable character.
- `abstract_model`: original geometric vehicle or spacecraft-like model with no franchise cues. **New.**
- `trophy`: small unbranded trophy with no inscription.
- `collector_coin`: decorative coin with abstract relief and no writing.
- `kinetic_object`: metal balance toy or kinetic desk sculpture. **New.**
- `geode`: crystal or mineral specimen. **New.**
- `lava_lamp`: compact lava lamp. **New.**
- `plasma_globe`: small plasma globe. **New.**
- `hourglass`: clear sand timer.
- `metal_sculpture`: small abstract metal desk object.
- `display_plinth`: low empty plinth or one holding the declared abstract model. **New.**
- `keepsake_box`: plain keepsake box.
- `drinkware`: matte bottle, drinking glass, or ceramic mug.
- `food_bowl`: snack bowl or fruit bowl.
- `popcorn_container`: plain unbranded popcorn tub with no writing.
- `food_plate`: small snack plate.
- `serving_vessels`: clear drink carafe.
- `coaster`: stone or felt coaster.
- `marble_track`: compact sculptural marble track. **New.**

## Background furnishings and décor

- `open_shelving`: illuminated display shelving with abstract objects only.
- `closed_storage`: white storage cabinetry.
- `backlit_niche`: recessed backlit display niche. **New.**
- `lounge_seating`: simple lounge chair.
- `ottoman`: upholstered ottoman.
- `floor_lighting`: floor lamp.
- `floor_textile`: area rug.
- `soft_textile`: throw blanket or lounge cushion.
- `acoustic_wall`: geometric acoustic treatment.
- `indirect_rgb`: concealed RGB light strip.

## Wall and architectural details

- `framed_wall_art`: original abstract geometric wall art.
- `wall_texture`: dark plaster, brick, or concrete texture. **Expanded.**
- `wall_slats`: dark wood slats. **New.**
- `acoustic_wall`: wedge, felt, or block-style acoustic panels. **Expanded.**
- `neon_shape`: non-text neon line or geometric symbol. **New.**
- `wall_light_panels`: abstract decorative light panels.
- `perforated_panel`: dark perforated metal wall panel. **New.**
- `gradient_light`: colored light wash across a plain wall. **New.**
- `shadow_box`: framed shadow box holding a single abstract object. **New.**
- `wall_shelving`: narrow floating ledge with geometric objects. **New.**
- `sound_diffuser`: dimensional wood sound-diffusion blocks. **New.**

# Café

Laptop scenes may use Café normally. Printer scenes use Café only when the Smart Brief or source messaging explicitly supports that setting.

## Smaller props

- `drinkware`: ceramic coffee cup, water glass, or reusable bottle.
- `serving_vessels`: ceramic teapot, small milk jug, or pressed-glass water bottle.
- `food_bowl`: sugar bowl or fruit bowl.
- `cutlery`: teaspoon or small dessert fork.
- `food_plate`: small pastry plate.
- `baked_food`: croissant, muffin, cookie, or cake slice; all collide as one family.
- `savory_food`: small sandwich with no branded wrapping.
- `bread_basket`: woven basket with plain bread.
- `napkin`: folded cloth napkin or plain napkin holder.
- `coaster`: cork or ceramic coaster.
- `flower_vessel`: bud vase with a single simple flower.
- `decorative_candle`: small plain candleholder. **New for Café.**
- `serving_tray`: wood or metal café tray.
- `condiment_set`: small unlabelled ceramic condiment pair. **New.**
- `cake_stand`: low pastry stand or clear pastry dome. **New.**
- `plant`: small herb pot or leafy tabletop plant. **New form.**
- `decorative_tile`: one hand-glazed ceramic tile used as a tabletop accent. **New.**
- `ceramic_object`: small unlabelled ceramic form for populated shelving. **New for Café.**
- `paper_materials`: one blank notebook form when the scene specifically depicts focused table work.
- `eyewear`: folded reading glasses.

## Background furnishings and décor

- `bench_seating`: upholstered banquette.
- `cafe_chair`: bentwood chair.
- `stool`: simple counter stool. **New.**
- `service_counter`: café service counter kept secondary. **New.**
- `pastry_display`: simple glass pastry case with no labels. **New.**
- `open_shelving`: shelves holding unlabelled ceramics.
- `pendant_lighting`: pendant lamp or small pendant cluster.
- `plant`: leafy floor plant or hanging plant.
- `coat_stand`: plain coat stand.
- `window_textile`: café curtains.
- `floor_textile`: woven rug.
- `room_divider`: wood or fluted-glass divider. **New.**

## Wall and architectural details

- `wall_writing_board`: distant chalkboard menu with explicitly non-legible writing; use only when important to the café setting.
- `framed_wall_art`: abstract framed art without text or faces.
- `tile_wall`: glazed tile or handmade zellige-style wall. **New.**
- `wall_texture`: warm plaster or exposed brick. **New.**
- `wall_slats`: natural-wood slats. **New.**
- `acoustic_wall`: fabric-wrapped acoustic panels. **New.**
- `decorative_plates`: small arrangement of plain ceramic wall plates. **New.**
- `botanical_mural`: nonfigurative leaf-shape mural with no words. **New.**
- `plant_grid`: metal wall grid with sparse greenery. **New.**
- `wall_lighting`: warm wall sconce. **New.**
- `carved_panel`: carved geometric wood panel. **New.**
- `colored_glass`: small textured or stained-glass insert without imagery. **New.**

# Creative Studio

## Smaller props

- `paper_materials`: sketchbook, portfolio folder, blank drawing sheets, or rolled drawing; choose only one form for the entire bank.
- `writing_tools`: graphite pencils, charcoal, colored pencils, drawing pens, markers, or pastels.
- `paint_tools`: watercolor palette, paintbrushes, palette knife, or small mixing dish.
- `tool_cup`: brush holder or clear brush jar; collides with office and education pen cups.
- `material_swatches`: fabric, color, wood, or finish swatches; all collide as one visual family.
- `textile_notions`: ribbon, thread spool, or cord samples.
- `measurement_tools`: measuring tape, ruler, or set square.
- `cutting_tools`: scissors or craft knife placed safely on the work surface. **Expanded.**
- `work_mat`: plain craft cutting mat with no visible numbers or lettering.
- `adhesive`: masking tape or plain paper tape.
- `paper_fasteners`: binder clips.
- `ceramic_samples`: ceramic test tile or small glaze sample.
- `clay_samples`: two or three abstract clay forms. **New.**
- `prototype_model`: small wooden model, geometric origami form, or plaster prototype.
- `wire_form`: small abstract wire armature. **New.**
- `foam_forms`: geometric foam mock-up pieces. **New.**
- `glass_samples`: unlabelled translucent glass or acrylic sample tiles. **New.**
- `pigment_jars`: small unlabelled pigment jars with closed lids. **New.**
- `stencil_shapes`: plain geometric stencils with no letters or numbers. **New.**
- `loom_sample`: compact woven test panel. **New.**
- `hand_roller`: small unbranded brayer or printmaking roller. **New.**
- `dowel_set`: short group of natural-wood dowels. **New.**

## Background furnishings and décor

- `stool`: studio stool.
- `easel`: wooden easel with an abstract, unfinished canvas.
- `materials_cart`: rolling cart with unlabelled materials.
- `closed_storage`: side cabinet, drawer unit, or flat-file cabinet.
- `open_shelving`: shelves with unlabelled jars or material samples.
- `dress_form`: headless plain dress form with no facial features. **New.**
- `drying_rack`: simple drying rack with blank material sheets. **New.**
- `material_roll_rack`: rack holding plain fabric or paper rolls. **New.**
- `task_lighting`: studio task lamp.
- `window_textile`: linen curtains.
- `plant`: potted plant.
- `display_pedestal`: low studio pedestal with one abstract prototype. **New.**

## Wall and architectural details

- `tool_pegboard`: pegboard holding a restrained set of declared, non-digital tools.
- `wall_display_board`: material board using only unlabeled color and texture samples.
- `large_canvas`: large abstract canvas without text, faces, or recognizable characters. **New.**
- `acoustic_wall`: neutral studio acoustic panels. **New.**
- `wall_slats`: pale or dark wood slats. **New.**
- `wall_texture`: plaster test wall with subtle finish variation. **New.**
- `wire_display_grid`: wall grid holding geometric samples only. **New.**
- `hanging_textiles`: narrow hanging fabric strips with no printed imagery. **New.**
- `ceramic_tile_grid`: small grid of handmade ceramic test tiles. **New.**
- `wall_shelving`: floating shelf with unlabelled jars or one prototype.
- `shadow_box`: shallow wall box containing an abstract model. **New.**
- `track_lighting`: ceiling-mounted studio track lights. **New.**

# Device placement rules

## Laptop

Laptops may naturally appear in Home, Office, Education, Gaming, Café, and Creative Studio scenes. Plausible support surfaces include a dedicated desk, meeting table, study table, café table, gaming desk, drafting table, or studio worktable.

## Printer

Printers normally appear only in Office, Home workspace, Education, and Creative Studio scenes. Café or Gaming is allowed only when the Smart Brief or source messaging explicitly supports it. Their primary support must read as a dedicated table or worktable, never an occupied desk or personal workstation. Keep personal work arrangements off that main table and establish lived-in character around it.

| Environment | Plausible printer support surfaces | Unavailable placements |
| --- | --- | --- |
| Office | Dedicated output table, sturdy office worktable, utility table, or substantial side table | Occupied desk, personal workstation, lounge table, reception coffee table, bar-height social counter |
| Home workspace | Dedicated home-workspace table, sturdy utility table, or wide worktable reserved for equipment | Occupied desk, coffee table, end table, dining table, kitchen island, sofa-side surface |
| Education | Classroom resource table, library worktable, sturdy supply table, or shared project table | Student desk, reading-nook side table, café-style table |
| Creative Studio | Sturdy studio worktable, production table, utility table, or wide project table | Occupied drafting desk, small display plinth, narrow drafting ledge, fragile side table |
| Café | Source-required only, on a credible back-office worktable or service table | Customer café table, bar counter, pastry table |
| Gaming | Source-required only, on a dedicated utility table separate from the gaming focal area | Gaming desk, lounge table, display shelf |

# Scene-language repetition rules

The application should treat each row below as one semantic family and allow it in only one of the ten prompts. This table is a minimum registry, not an exhaustive permission to repeat other descriptive concepts. The writer must plan all ten prompts together and avoid repeating any distinctive room, lighting, atmosphere, composition, or activity concept through synonyms. Common grammar and the canonical environment label are exempt.

| Semantic family | Phrases that collide |
| --- | --- |
| `modern_office` | Modern office, modern corporate office, contemporary corporate office, polished modern workplace |
| `bright_modern` | Bright modern, light-filled modern, bright contemporary |
| `warm_natural_light` | Warm natural light, warm daylight, warm window light, soft warm daylight |
| `soft_daylight` | Soft daylight, gentle daylight, diffused daylight, soft natural light |
| `window_proximity` | Near a window, beside a window, window-side, positioned by a window |
| `paper_has_no_text` | Blank pages, unmarked pages, blank unmarked pages, plain blank paper |
| `markings_are_indistinct` | Indistinct markings, non-readable markings, illegible writing, non-legible details |
| `lived_in` | Lived-in, authentic everyday use, casually used, everyday working feel |
| `clean_professional` | Clean professional feel, polished workplace, refined professional atmosphere |
| `layered_depth` | Layered depth, natural depth, furnishings extend into the background |
| `casual_arrangement` | Casually arranged, set slightly askew, loosely grouped, naturally scattered |
| `simple_uncluttered` | Simple and uncluttered, restrained workspace, tidy minimal setting |

When an environment repeats within a bank, it should use a genuinely different subsetting, activity, light source, wall treatment, support surface, and prop-family allocation rather than paraphrasing the same room.

# Unavailable unless separately approved

- Keyboards, mice, webcams, docks, external drives, speakers, headphones, microphones, controllers, consoles, VR equipment, monitors, phones, tablets, and other digital devices.
- Chargers, power banks, cables, mouse mats, laptop bags, printer consumables, or branded packaging.
- Human portraits, family photographs, figurative reference photography, recognizable characters, or licensed artwork.
- Magazines, newspapers, business cards, nameplates, receipts, posters, signs, calendars, forms, or other objects likely to generate prominent readable text.
- Clocks, number charts, alphabet tiles, labeled maps, and text-forward educational displays.
- Specialized gaming chairs until explicitly approved.

