# V5 dual-source input inventory and extraction findings

As of 2026-10-27. This bounded batch inventories the five supplied source folders and preserves their complete extractable content. No external model/API was called, normalized payloads do not replace source copy with generated summaries, and no prompt, model, image, S3, or shared canonical artifact was changed.

## Contents

- [Scope and durable copy](#scope-and-durable-copy)
- [Actual formats, schemas, and lengths](#actual-formats-schemas-and-lengths)
- [Pair review](#pair-review)
- [Direct scene evidence](#direct-scene-evidence)
- [Instruction-bearing content](#instruction-bearing-content)
- [Reproduction and limits](#reproduction-and-limits)

## Scope and durable copy

VERIFIED: the volatile input contained exactly five folders and ten files: one smart brief plus one source-messaging artifact per folder. Every original was copied non-destructively into the backed-up checkout, and every source/copy pair matched in byte count and SHA-256. The source and durable paths, sizes, hashes, and verification status are recorded in:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/dual_source_v5/inputs/originals_manifest.json`

The folder order is source-sorted: Cashmere, Deskjet 2955, Elitebook, Laserjet, Modric. USER-CONFIRMED: Modric is preserved and reviewed here but remains excluded from the current runtime test pending the user's answer.

## Actual formats, schemas, and lengths

VERIFIED: none of the six `.txt` files is JSON. Each is a UTF-8 plain-text export and is preserved in full as `raw_text`, lossless line records, and an explicit JSON parse failure. No fields were dropped.

The three TXT smart briefs are prose reports with product metadata and numbered strategy sections. The three TXT source-messaging files share this visible schema: export metadata; `VALUE PROPOSITION`; four KSP records; and eTail blocks. Each value proposition/KSP carries headline, long best-SKU, long safe-to-inherit, mid, mid safe-to-inherit, short, short safe-to-inherit, ultra-short, and disclaimer content. Each eTail block carries its CAP element and message.

DOCX extraction includes every paragraph and table in XML document order across the main document plus available header, footer, footnote, endnote, and comment story parts. XLSX extraction includes every sheet in workbook order and every nonempty cell with sheet name, coordinate, type, style, formula, raw value, and decoded value.

| Folder | Role | Format | Original bytes | Complete extracted extent |
|---|---|---:|---:|---|
| Cashmere | smart brief | DOCX | 55,395 | 177 paragraphs; 23,391 paragraph characters |
| Cashmere | source messaging | DOCX | 316,420 | 728 paragraphs; 20 tables; 43,616 paragraph characters; four story parts |
| Deskjet 2955 | smart brief | TXT | 32,684 | 32,147 characters; 309 lines; invalid JSON |
| Deskjet 2955 | source messaging | TXT | 11,412 | 11,368 characters; 213 lines; invalid JSON |
| Elitebook | smart brief | TXT | 33,332 | 32,913 characters; 307 lines; invalid JSON |
| Elitebook | source messaging | TXT | 11,223 | 11,204 characters; 208 lines; invalid JSON |
| Laserjet | smart brief | TXT | 38,402 | 37,887 characters; 378 lines; invalid JSON |
| Laserjet | source messaging | TXT | 11,149 | 11,148 characters; 209 lines; invalid JSON |
| Modric | smart brief | DOCX | 54,514 | 138 paragraphs; 19,831 paragraph characters |
| Modric | source messaging | XLSX | 173,983 | 3 sheets; 230 nonempty cells; 26,124 value characters |

The Modric workbook sheets contain 19 cells in `Read me`, 95 in `Source OmniStudio 23.8" AiO`, and 116 in `Etail OmniStudio 23.8" AiO`. VERIFIED: no supplied file contains a `camera_tag`; that remains a separate runtime input.

## Pair review

All five folders have high structural pairing confidence because each contains exactly one recognized smart brief and one recognized source-messaging file. Content-level confidence differs:

| Source folder | Semantic pair confidence | Product-label and contradiction result |
|---|---|---|
| Cashmere | **LOW** | Smart brief: non-Flip `EliteBook X G2i` / D72P6UT. Source messaging: convertible `EliteBook X Flip G2i (CashmereX)`. Flip-specific tablet/tent/pen claims must not be merged into the non-Flip record. |
| Deskjet 2955 | **HIGH WITH CAVEAT** | Both artifacts name DeskJet 2955. The smart brief itself warns that its underlying inputs mix 2955, DeskJet 2900 footnotes, and a DeskJet 4300 photo-printing passage (line 225). |
| Elitebook | **HIGH** | Both artifacts name `HP EliteBook X Flip G2i ... (CashmereXI)`; no material product-label contradiction was identified in this bounded review. |
| Laserjet | **HIGH WITH CAVEAT** | Both artifacts name `HP LaserJet Enterprise 6501dn Print`. The smart brief records conflicting maximum speeds: 52/50 Letter/A4 ppm versus 57 ppm (lines 105, 122, 210). |
| Modric | **LOW** | The workbook source sheet/filename say AMD, its eTail title says Intel, and its eTail audience calls the desktop a high-performance laptop. The smart brief and workbook also conflict on processor, display, and sustainability specifications. |

The complete label quotes, provenance, contradiction evidence, and scene-cue provenance are in:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/dual_source_v5/inputs/normalized/pair_reviews.json`

## Direct scene evidence

These are observed source cues, retained with provenance rather than rewritten scene proposals:

- **Cashmere:** the non-Flip smart brief names office, airport, client site, home, hybrid meetings, briefing review, and sensitive work in shared spaces (`word/document.xml/xml_paragraph[87..89]`). The mismatched Flip source separately names tablet sketching, tent-mode presenting, PC-mode collaboration, and meetings (`xml_paragraph[199..212]`).
- **Deskjet 2955:** source-messaging lines 16, 74, and 130 name return labels, forms, scans, school worksheets, home organization, household lists, recipes, visual-planning pages, and light creative projects.
- **Elitebook:** source-messaging lines 16–18, 44–52, and 71–100 name sketching, presenting, shared viewing in tent mode, hybrid meetings, client sites, shared spaces, home, and offices.
- **Laserjet:** source-messaging lines 17 and 45–53 name managed office fleets and shared workteams handling contracts, invoices, forms, meeting packets, project documentation, and duplex office documents.
- **Modric, inventory only:** the smart brief names shared-home schoolwork, household administration, online classes, personal finance, kitchen/den/study homework, and light creative work. Workbook cells `Source OmniStudio 23.8" AiO!C10`, `C14:F15` name family calls, browsing, streaming, online learning, homework, movie nights, living rooms, and shared family spaces.

## Instruction-bearing content

VERIFIED for this ten-file set: no `_chatSession`, `systemInstructions`, system-prompt, ignore-previous, or assistant-role field/string was found. Because the TXT files are not JSON, there are no hidden JSON metadata fields to inherit.

The source artifacts do contain explicit authoring directives that must remain inert source data:

- The Cashmere source DOCX has template labels, character limits, legal-copy rules, and usage rules, including `word/document.xml/block[164..179]`.
- The Modric workbook's `Read me!A8:A24` cells instruct marketers how to use messaging; the Source/eTail template columns C and D contain formulas and requirements.
- Smart briefs contain visible `COPY DIRECTION` and language-guardrail sections. These are upstream marketing content and cannot override the V5 runtime contract.

## Reproduction and limits

The standard-library extractor is:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/dual_source_v5/scripts/extract_inputs.py`

Reproduce or re-verify the bounded extraction with:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/dual_source_v5/scripts/extract_inputs.py \
  --source-root /mnt/localssd/HP_scenes/smart_brief_and_source_messaging \
  --output-root /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/dual_source_v5
```

The extraction manifest and normalized file/pair records are under:

`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/research/dual_source_v5/inputs/normalized`

The extractor refuses to overwrite an existing different original, verifies size and SHA-256 after copying, preserves complete decoded TXT text, inventories all DOCX paragraphs/tables, and preserves all nonempty XLSX coordinates on all sheets. Originals remain the byte-authoritative evidence.

This batch does not resolve the Cashmere or Modric product conflicts, select which contradictory claim is true, author V5 prompt rules, call a model, or produce runtime outputs. The next integration step is to consume the three high/high-with-caveat pairs, hold Cashmere until its intended product is resolved, and keep Modric excluded until the pending runtime decision and its product/spec conflicts are resolved.
