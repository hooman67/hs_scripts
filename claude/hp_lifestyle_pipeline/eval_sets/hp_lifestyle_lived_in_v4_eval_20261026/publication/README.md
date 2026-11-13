# V4 progressive gallery publisher

`supervise_publication.py` rebuilds the progressive gallery when validated local inputs change and
uploads only changed, hash-verified objects. It performs no model or image-generation calls.

The publisher remains gated until the manifest authorizes image generation, all 18 banks contain
540 validated candidates, the selection artifact has status `approved_for_image_generation`, and
all 108 selection rows have semantic status `accepted`.

Destination:

`s3://foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generated_v4/`

Gallery URL after publication:

https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/generated_v4/gallery/index.html

No publisher process is started by this scaffold.

The post-export gallery validator builds the local gallery, enforces the 540/108 counts, checks the
seven generated-view headers and actual-image code path, verifies the native six-environment
taxonomy, and checks that source, explanation, usedPrompt, and generation debug remain collapsed:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/validate_gallery.py
```

It uses a local headless Chromium render when a supported browser is installed. Otherwise its
report explicitly records that the browser check was skipped after static HTML, JavaScript syntax,
and serialized gallery-data validation. The durable report is written to
`/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/publication/ui_validation.json`.

After all 108 records are done, require actual generated-image assets for every row with:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_lived_in_v4_eval_20261026/validate_gallery.py --final
```
