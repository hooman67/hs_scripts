---
type: concept
title: Eval result HTML reports (plain + fe_html)
tags: [foundry, eval, html, fe-html, ims, thd, reporting]
created: 2026-09-14
updated: 2026-09-14
sources: ["[[raw/thd-seedance-video-pipeline-learnings-2026-09]]"]
---

# Eval result HTML reports (plain + fe_html)

How [[wiki/concepts/foundry-eval-workflow|eval runs]] are published as browsable pages backed by
IMS-authed S3 assets. Two views per set, uploaded beside the set in S3 and indexed in the app's
`eval_htmls.md`.

## Two required views
- **Plain report** — a single self-contained HTML (one row per shot).
- **`_fe` report — always the two-file `/fe_html` form:** a vendored same-origin `viewer.html`
  (`<stem>_fe.html`) **plus** a separate `<stem>_fe.json` data file, opened as
  `…<stem>_fe.html?src=<stem>_fe.json`. **Never** ship a self-contained single-file "card view" as the
  `_fe` version — that's been flagged as wrong.

## The two fixed gotchas (both required or assets 404 / page is blank)
1. **IMS scaffold** (so IMS-authed `/asset/` URLs load): staging imslib
   `https://auth-stg1.services.adobe.com/imslib/imslib.js` + `./imsauth.js` + an inline
   `onAuthReady()`/`initializeIMS()` wired on `DOMContentLoaded`; body has `<div id="ims">` and
   `<div id="loading">` **before** `<div id="content" style="display:none">`.
2. **Absolute asset URLs** with the **full** `seedance_video_eval_sets/<set>/` prefix — form
   `https://foundry-aws-corp.adobe.io/asset/<bucket>/<key>` (the [[wiki/entities/foundry-gateway|Foundry
   gateway]] asset path). Relative URLs break.

## Columns (video eval)
input prompt (stripped) · input images (each with a **reference/storyboard asset-type badge**) ·
processed/anonymized inputs + motion-bank panel (grid as `<img>`, clip inline `<video>`) · rewritten
prompt · output video.

## Related
- [[wiki/concepts/foundry-eval-workflow]] · [[wiki/entities/thd-video]]
- [[wiki/entities/foundry-gateway]] — the `/asset/<bucket>/<key>` path + IMS auth
