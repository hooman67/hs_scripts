# KDP FFDY-8567 lifestyle-image POC

Last updated: 2026-10-07

Canonical comprehensive notes:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/PROJECT_NOTES.md`

Current published generation gallery:

https://foundry-aws-corp.adobe.io/asset/foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_poc/gpt_image_2_5_smoke/gallery/index.html

Published candidate/reference review:

https://foundry-aws-corp.adobe.io/asset/foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_candidate_review/gallery/index.html

Current displayed set: 22 GPT Image 2.5 Sunburst/high 1536×1024 lifestyle generations across K-Express Black,
Mini Mate Plus Warm Stone, Mini Mate Plus Matte Black, and K-Supreme Gen 2 Black. Every displayed output was made
from clean product references only. Scraped lifestyle pixels were not inputs to displayed generations.

Generation uses:

`/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py`

with `gpt-image-2.5-sunburst`, `quality=high`, PNG, and no `input_fidelity`. Foundry OpenAI access works through
`foundry-aws-gateway==2.0.0` in:

`/mnt/localssd/kdp_imagegen_venv/bin/python`

The earlier Mini Mate synthetic-black-reference premise was invalidated after finding a genuine clean Matte Black
reference for SKU `5000390176`. Hooman asked that experiment be removed from the HTML. It is archived but not part
of the active gallery or planned evaluation.

Evaluation caveat: K-Supreme red/pink and Mini Mate Matte Black lavender/yellow real lifestyles informed textual
scene prompts, so they are not pristine holdouts for matching generated scenes. A blind test must hide provenance,
normalize file/crop characteristics, randomize one-image-at-a-time presentation, balance real/generated within SKU
and scene type, collect real/generated/unsure plus confidence/usability, and follow with product-defect review.

Verified `fe-html` fit: it supports one-image rows, custom `Real / Generated / Unsure` questions,
reviewer-attributed publish, CSV export, and aggregate Summary. It is not blind by default because the wrapper
exposes path-derived IDs/labels and preserves sorted order. Use opaque staged filenames/URLs, neutral labels,
pre-shuffled rows, normalized assets, and a private truth map. A custom viewer is only needed to lock the protocol
or randomize independently per reviewer. Full assessment:

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/FE_HTML_BLIND_EVAL_ASSESSMENT.md`

Published one-reviewer blind pilot (14 opaque candidates, balanced 7 real / 7 generated, references shown beside
each candidate, preconfigured Real/Generated question, one row per page):

https://foundry-aws-corp.adobe.io/asset/foundry-kdp-enterprise-adobe-assets/scraped_from_kdp_website/kdp_poc/blind_real_vs_generated_pilot_2026-10-07/report/viewer.html?q=W3sidGV4dCI6IklzIHRoZSBjYW5kaWRhdGUgaW1hZ2UgcmVhbCBvciBBSS1nZW5lcmF0ZWQ%2FIiwiaGFyZF9jaGVjayI6ZmFsc2UsInJ1YnJpYyI6eyJrZXkiOiJjdXN0b20iLCJuYW1lIjoiUmVhbCB2cyBHZW5lcmF0ZWQiLCJvcHRpb25zIjpbeyJ2YWx1ZSI6InJlYWwiLCJsYWJlbCI6IlJlYWwiLCJ0b25lIjoibmV1dHJhbCJ9LHsidmFsdWUiOiJnZW5lcmF0ZWQiLCJsYWJlbCI6IkdlbmVyYXRlZCIsInRvbmUiOiJhbHQifV19fV0%3D&hide=item_id&per=1

Private truth map (never upload/share with reviewer):

`/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/evaluation/blind_pilot_2026-10-07/private/truth_map.csv`

User preference: local paths must always be shown as full absolute paths in plain text/code blocks. HTML artifacts
must be uploaded to Foundry S3 and returned as full clickable `foundry-aws-corp.adobe.io` URLs.
