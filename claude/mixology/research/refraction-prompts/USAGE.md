# Minimal refraction prompt — V3 working checkpoint

Hooman selected system V3 to keep for now on 2026-10-19. The user supplies one drink image and types **Add refractions.** The application supplies the reusable system prompt and a fixed lighting-style preset. This is a tested configuration, not a deployed application or blanket approval of its outputs.

Review gallery: https://foundry-aws-corp.adobe.io/asset/foundry-tccc-enterprise-adobe-assets/mixology/refraction_research_2026-10-19/gallery/index.html .

After the restart, durable artifacts live at `/home/colligo/mixology_data/refraction_research_2026-10-19`; the historical SSD run path is a compatibility symlink. Use the rebuilt `/home/colligo/.venvs/mixology/bin/python`, not the deleted SSD virtualenv. The five new-drink refraction edits and four separate composition tests completed through the user-authorized fal fallback. They are generated research samples, not user-accepted results. The direct Foundry route still awaits new-cluster allowlisting.

Fal batch: `/home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/run_fal_experiments.py` uses `openrouter/router/vision` with requested `openai/gpt-6-astra` and mandatory `reasoning=true`, then `openai/gpt-image-2.5/sunburst/edit`. System/user prompts and ordered references are unchanged. Fal does not expose the same reasoning-effort setting or returned backend snapshot, so the provider batch is labeled separately (`v3fal`). All actual image prompts, sanitized requests, queue IDs and outputs are preserved. The gallery includes all five new results and all 14 earlier refraction outputs.

Preferred overhead input: `/mnt/localssd/mixology/refraction_research_2026-10-19/assets/overhead_013_clean.png`, derived by removing external shadows/refractions from customer image 013 and restoring its original cup interiors; Hooman approved this clean input. Preferred group input: `/mnt/localssd/mixology/refraction_research_2026-10-19/assets/group_027_clean.png`, derived from customer image 027. Old inputs 012/023 are rejected for their crop and retained only for historical provenance. System V3 itself is unchanged.

Corrected-input runs are named `v3corrected_overhead_clean` and `v3corrected_group_clean`. One-off input preparation is intentionally excluded from the review HTML; the resulting clean inputs remain visible next to the refraction generations. Prior refraction outputs must stay until Hooman reviews the replacements.

## Request contract

1. Load `/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/prompts/system_v3.md` as Astra's `instructions`.
2. Send the short user text, then Image 1 labeled `edit target, authoritative for drink identity and composition`, then the fixed preset Image 2 labeled `lighting style reference ONLY, not a replacement for Image 1`.
3. Pass Astra's returned text as the Sunburst image-edit prompt. Attach the same two images in the same order. Use `gpt-image-2.5-sunburst`, high quality, auto size, PNG. Do not pass the rewriter system instructions directly to the image endpoint.
4. Keep the source crop by default. The separately tested modifier `Add refractions and show the full cups.` authorizes a pullback; it is not the default.

Presets are under `/mnt/localssd/mixology/refraction_research_2026-10-19/assets`: overhead uses `image_013_p05_xref1594.jpg`, upright group uses `image_027_p10_xref1385.jpg`, and upright single uses `image_003_p03_xref116.jpg`. The source drink controls ingredient and straw colors; the preset controls only the light. The single-cup preset is a different drink, deliberately testing separation of these roles.

The experiment used manual case-to-preset selection. Automatic view classification, arbitrary uploaded targets, a UI, and a production service are outside this batch. New targets and repeated samples need evaluation before treating the preset as generally reliable.

## Reproduce

Environment: `/home/colligo/.venvs/mixology/bin/python`; credentials retrieved in process through `foundry_aws_gateway.llm.get_openai()` using authorized machine access. The unchanged bundled imagegen CLI executes every image edit. Never put credentials into prompt files, the gallery, or tracked source.

The existing IDs are immutable: complete runs are skipped. For a new overhead sample, choose a fresh version ID:

```bash
/home/colligo/.venvs/mixology/bin/python /home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/scripts/run_experiments.py generate --version v3repeat01 --system-version v3 --cases overhead_clean --style image_013_p05_xref1594.jpg
/home/colligo/.venvs/mixology/bin/python /home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/scripts/run_experiments.py judge v3repeat01_overhead_clean
```

This incurs new model usage. Do not execute as part of merely viewing this documentation. To rebuild the gallery without inference:

```bash
/home/colligo/.venvs/mixology/bin/python /home/colligo/hs_scripts/claude/mixology/research/refraction-prompts/scripts/build_gallery.py
```

## Known limits

Text-only examples tended toward coarse webs or glitter. Reference-conditioned examples are more promising, but still show some regular mesh and starburst-like cores. V3 is recommended for its concise, explicit role contract and comparable observed quality, not a proven win over V2. Hooman approved the clean overhead input; the two corrected-input refraction outputs await review. See the full experiment history and advisory critiques in the gallery.
