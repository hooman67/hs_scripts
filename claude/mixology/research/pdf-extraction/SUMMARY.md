# Customer PDF image extraction

As of 2026-10-19.

## Outcome

VERIFIED: `/mnt/localssd/mixology/260605_Mixology_AI_Art_Direction_Process.pdf` is a 12-page PDF 1.7 document containing 39 raster-image placements backed by 34 distinct embedded image objects. Four objects are reused: xref 1842 appears three times; xrefs 1594, 1596, and 1242 appear twice each.

All 34 source images use JPEG/DCT compression and have a linked PDF soft mask. The extraction preserves two useful forms:

- `/mnt/localssd/mixology/extracted_from_pdf/native_original_streams/`: the 34 original JPEG streams with no image transcoding.
- `/mnt/localssd/mixology/extracted_from_pdf/png_with_transparency/`: the 34 full-resolution images with their soft masks restored as RGBA PNGs.
- `/mnt/localssd/mixology/extracted_from_pdf/all_page_placements/`: all 39 page placements in page order. Reused objects are hard-linked when supported, preserving placement identity without duplicating bytes.

Native dimensions range from 736–3272 pixels wide and 732–2464 pixels high. The output occupies approximately 119 MiB on disk.

## Validation

All 34 native JPEGs and 34 restored PNGs decoded successfully at the dimensions declared by the PDF. All 39 placement files decoded successfully. Every file's SHA-256 and byte size were reconciled with `/mnt/localssd/mixology/extracted_from_pdf/manifest.json`. All restored files have alpha channels; observed alpha ranges were 0–255, 96–255, or 255–255 depending on the source mask.

The 34-image contact sheet was visually inspected. It shows the drink/product imagery and one embedded process-board screenshot; no extracted object is blank or corrupt. The contact sheet is a derived review aid at `/mnt/localssd/mixology/extracted_from_pdf/_review/contact_sheet_unique_images.jpg`, not a customer source image.

## Method and reproducibility

The extractor enumerates page image XObjects, extracts native bytes with PyMuPDF, applies each linked soft mask to a full-resolution pixmap, and records source/page/xref provenance. It refuses to overwrite an existing extraction.

Reproducible script: `/home/colligo/hs_scripts/claude/mixology/research/pdf-extraction/scripts/extract_pdf_images.py`.

Environment: `/mnt/localssd/mixology_venv/bin/python`, Python 3.12, PyMuPDF 2.0, Pillow 13.0.0.

## Limits

This batch extracts every raster image object exposed by the PDF page resources. Vector shapes, live text, and entire slide compositions are not separate embedded images and therefore are not emitted as source images. The isolated output is the full embedded source object; PDF placement transforms or visual cropping are recorded by page identity rather than baked into the extracted pixels. The process does not infer which images are approved edit targets versus style references.

## Artifacts

- `/mnt/localssd/mixology/extracted_from_pdf/README.md`: folder guide.
- `/mnt/localssd/mixology/extracted_from_pdf/manifest.json`: complete machine-readable provenance and hashes.
- `/mnt/localssd/mixology/extracted_from_pdf/unique_images.csv`: compact inventory of the 34 distinct objects.
- `/mnt/localssd/mixology/extracted_from_pdf/placements.csv`: inventory of all 39 page placements.
- `/mnt/localssd/mixology/extracted_from_pdf/_review/contact_sheet_unique_images.jpg`: derived visual review sheet.
