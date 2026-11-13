---
name: feedback_include_all_inputs_in_artifacts
description: "In any results artifact/gallery, always show the full prompt and every input next to each output"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 988e6174-d494-4ea5-a025-8678b58141b2
  modified: 2026-08-23T00:35:28.457Z
---

In any results artifact (gallery, report, comparison), **always include the full prompt and every
input — reference images/plates, mode, params — alongside each output**, not just the output.

**Why:** Hooman reviews by comparing inputs→outputs; he caught round 3 of the THD video rewriter
([[project_thd_video_rewriter]]) shipping outputs without their prompts. He needs to see exactly what
produced each result to critique it.

**How to apply:** `gallery/build_gallery.py` now prints a WARNING for any rendered experiment lacking a
prompt (section-level or its own) — keep that fail-loud check, and store each generation's prompt in
the manifest (or pull it from the `<name>.json` sidecar that `seedance_video.generate` writes).
