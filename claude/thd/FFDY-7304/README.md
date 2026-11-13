# FFDY-7304 — Glacier Bay laundry-sink storyboard → long-form video

Experiment: turn a customer storyboard into a generated ~:60 video, reusing the THD article→video
rewriter techniques (`../pipeline`, sketch/cover-body keyframe method).

## Split (git rules)
- **Code + text (this dir, git-tracked):** `extract_pptx.py`, `build_index.py`, `storyboard_text.md`,
  `text/slide_NN.txt`, `storyboard.json`, `extract_index.json`, `STORYBOARD_OVERVIEW.md`.
- **Images + the PPTX (NOT git):** `/home/colligo/THD_laundry_sink_storyboard/`
  — `Storyboard ClickReady ....pptx` (source) + `images/imageN.jpeg` (26 shoot/product photos).

## Reproduce
```bash
python3 extract_pptx.py    # PPTX -> slide text (repo) + embedded photos (media dir)
python3 build_index.py     # -> storyboard.json (hand-verified shot-series index + VO + product specs)
```

## Status
- ✅ Step 1 (extract assets + text, understand broadly) — done. See `STORYBOARD_OVERVIEW.md`.
- ⏭ Next — pending scope confirmation (4 open questions at end of the overview).

## One line
A single ~:60 Home Depot spot for the Glacier Bay Drop-In Laundry Sink + ClickReady RTA cabinet: 8 slides,
12 shot series (1A–8B), a couple assembling it in a laundry room + product/feature b-roll. The frames are
real shoot photos (not sketches), so R3/identity is the main challenge; the face-free product macros
(click connectors, faucet, hardware, hinge) are the cheapest first wins.

## Note
The media folder is still named `THD_laundry_sink_storyboard` — which now correctly matches the content.
An earlier Makita PDF was placed here by mistake; its derived outputs were cleared (the stray
`Makita_..._Preread-1.pdf` may still sit in the folder — delete if unwanted).
