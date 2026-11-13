# FFDY-7304 — Glacier Bay laundry-sink storyboard → video (broad understanding)

## What this deck is
`Storyboard ClickReady 10_1_25 v2a-FINALBOARDS CLEAN.pptx` — 8 slides, **one continuous promotional /
how-to spot (~:60)** for the **Glacier Bay Drop-In Laundry Sink + RTA Cabinet with CLICKREADY Technology**
(Home Depot exclusive). Frames are **real shoot photos** (2048×1152 stills of a couple assembling the
product in a styled laundry room) plus a few hi-res hero/product shots. Machine index: `storyboard.json`.

## The product (what the video sells)
- RTA cabinet, **tool-free CLICKREADY** assembly — no tools/glue/screws, "push, click, connect", ~3× faster;
  orange click connectors on the panel edges.
- **9-inch deep, 9-gallon stainless steel** drop-in sink + grid basket strainer.
- **Pull-down faucet**, drain kit + water lines included.
- **Brushed nickel** hardware, **soft-close** doors/hinges.
- **5 finishes:** Alpine White, White Oak, Ink Blue, Fern Green, Raven Black.
- On-screen SUPERs: "Tool-Free Cabinet Construction", "Complete with Drain Kit and Water Lines",
  "5 Color Finishes".

## The spot, beat by beat (12 shot series, 1A–8B)
| Series | Slides | Beat | VO segment |
|---|---|---|---|
| 1A | 2–3 | Couple assembles the cabinet on the floor (WS→MCU→CU) | "Upgrade your laundry room…where style meets simplicity." |
| 2A | 4 | Clicking sideboards onto the base (MS/CU) — *Tool-Free* | "…assembly is 3X faster…no tools, glue, or screws. Just push, click, connect." |
| 3A | 4 | Click connectors engaging (ECU macro) | (same beat) |
| 4A | 5 | Couple stands the cabinet up (MS) | "The 9-inch deep, 9 gallon stainless steel sink includes a grid basket strainer…" |
| 4B | 5 | Placing the sink basin (MS) | (same) |
| 5A | 5 | Faucet attaches + pulls down (CU) — *Drain Kit + Water Lines* | "…the pull-down faucet makes cleanups simple." |
| 1B | 6 | B-roll of the 5 color finishes — *5 Color Finishes* | "Choose from five durable, chip-resistant finishes…" |
| 6A | 7 | Brushed nickel hardware (ECU/CU/MS) | "…each with brushed nickel hardware…" |
| 7A | 7 | Cabinet doors closing (talent → isolate) | "…and soft-close doors…" |
| 7B | 7 | Soft-close hinge (ECU macro) | (same) |
| 8A | 8 | Turning on the faucet (female / couple alt) | "Transform your laundry room into something you'll love." |
| 8B | 8 | Hero / walk-away | "…fast, easy and available only at the Home Depot." |

Full VO read (one continuous voiceover) is in `storyboard.json → vo_script`.

## What "full long-form video" means here
Unlike the earlier deck, this is **one spot**, not a bundle — so the goal is unambiguous: **generate the
whole ~:60 spot** by producing each shot series and assembling them in order against the VO. A good proof
path: nail the **hero assembly beats first** (1A → 2A → 3A → 4A/4B → 5A), since ClickReady assembly is the
selling point, then add the product/feature b-roll (1B, 6A, 7A/7B) and the outro (8A/8B).

## Where our method fits, and the new challenges
- **These are photos, not sketches** — so unlike shot 0003 we can't hand the model a sketch as the
  keyframe. Two paths: (a) **sketchify** the shoot photos into line keyframes (our proven person-free
  route → dodges R3), or (b) **cover_body / paint-out** for the person-present beats. The macro product
  beats (3A click, 5A faucet, 6A hardware, 7B hinge) have **no faces** → easiest wins, do them first.
- **Real recurring couple** across most human beats → the identity / R3 problem again (real likeness in a
  ref → 422). Need per-person appearance handling + continuity lock; this is the known ceiling.
- **Brand text on wardrobe** (a "Lucky Brand" tee is visible) → keep the "plain shirt, no logo" negative.
- **On-product branding is the point** (Glacier Bay, CLICKREADY) — tension with the no-logo default; the
  orange connectors and stainless basin must read correctly. Use real product plates, not prompted logos.
- **No source video** → beats come from the shot series + VO; duration is budgeted per beat to the ~:60,
  not probed from a source clip.

## Assets on disk
- **Code + text (git):** `extract_pptx.py`, `build_index.py`, `storyboard_text.md`, `text/slide_NN.txt`,
  `storyboard.json`, `extract_index.json`, this file, `README.md`.
- **Images (not git):** `/home/colligo/THD_laundry_sink_storyboard/images/` — 26 shoot/product photos
  (`imageN.jpeg`; the two 147×147 / 387×199 files are UI icons, ignorable).

## Open questions for you
1. Confirm scope = the single ~:60 spot (I'm assuming yes).
2. Talent: invent a consistent couple, or do you have real talent stills to lock identity (R3 caveat)?
3. Start with the **face-free product/assembly macros** (3A/5A/6A/7B) as the cheapest end-to-end proof — OK?
4. Do you have the raw shoot **video** (not just stills), or is the storyboard the only source?
