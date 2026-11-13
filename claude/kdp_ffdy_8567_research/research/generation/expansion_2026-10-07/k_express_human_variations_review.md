# K-Express Black human-interaction variations — 2026-10-07

## Scope and method

This bounded batch generated four human-interaction variations for K-Express Black SKU `5000358267`.
All calls used the OpenAI image-edit endpoint through the Foundry gateway, model
`gpt-image-2.5-sunburst`, `quality="high"`, 1536×1024 PNG output, and the bundled CLI at
`/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py`.

Only these two clean exact-SKU product references were passed as image inputs:

- `/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/references/K-Express-Single-Serve-Coffee-Maker/Black/K-Express-Single-Serve-Coffee-Maker_5000358267.jpg`
- `/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/dataset/data/references/K-Express-Single-Serve-Coffee-Maker/Black/K-Express-Single-Serve-Coffee-Maker_en_general.jpg`

No scraped or generated lifestyle image was used as an input. The Black `K-Express_Alt_4.jpg` file was
excluded because it contains promotional text and accessory callouts.

## Run results

| Scenario | Prompt | Output | Runtime |
|---|---|---|---:|
| Precise index-finger button press | `k_express_precise_press.txt` | `k_express_precise_press_sunburst_high_v4.png` | 27.775s |
| Older hand placing a mug | `k_express_place_mug.txt` | `k_express_place_mug_sunburst_high_v5.png` | 34.215s |
| Hand closing brewer handle/lid | `k_express_close_handle.txt` | `k_express_close_handle_sunburst_high_v6.png` | 30.261s |
| Wider candid upper-body interaction | `k_express_wide_candid.txt` | `k_express_wide_candid_sunburst_high_v7.png` | 31.102s |

## Direct visual inspection

Inspection was performed at the original 1536×1024 resolution on 2026-10-07.

- **`VERIFIED` — precise press:** one continuous, plausible wrist/hand and five-finger structure; the index
  fingertip meets the `10` control without hiding the panel. This is visibly more relaxed and less elongated than
  the prior smoke-test press. The Black product silhouette, reservoir, front control strip, tray, and wordmark are
  coherent. Minor limitation: the pose remains deliberately staged because it is a close product-interaction shot.
- **`VERIFIED` — mug placement:** natural older-hand skin texture, plausible mug-handle grip, mug-to-tray contact,
  and unobstructed controls. This is the strongest anatomy/contact result in the batch. The environment is
  visually distinct through terrazzo, wood, plants, and hard late-afternoon light.
- **`VERIFIED WITH LIMITATION` — handle/lid closing:** the hand anatomy, top contact, lid alignment, product body,
  controls, logo, and reservoir are coherent. However, the generated hand presses across the top/front lip instead
  of clearly wrapping around and lifting the handle as requested. Treat this as a plausible end-of-close gesture,
  not proof that the model reproduced the full handle-opening mechanism.
- **`VERIFIED` — wide candid:** one plausible hand grasps the mug while the cropped upper body remains secondary;
  the mug rests on the tray and the brewer stays in focus and fully readable. The stainless counter, wider framing,
  cool daylight, and warm practical lamp expand scene diversity. Minor limitation: the head/hair is outside the
  crop, so the requested hair detail cannot be evaluated.
- **`UNVERIFIED` — exact SKU correctness:** all four are visually coherent against the two references, but a KDP
  product expert still needs to validate fine control labeling, lid/handle mechanics, reservoir seams, scale, and
  manufacturing details.

## File checks

All four outputs are unique 1536×1024 RGB PNG files. SHA-256 values:

```text
49740151bb137be89f3d5367d8d56f5eba4e84ed6efc4d02d861ed3e12078576  k_express_precise_press_sunburst_high_v4.png
55c11f43115847bac72a08a511256baa925709087877fd7c405606089ed06d0e  k_express_place_mug_sunburst_high_v5.png
43b875ff24691e44912005e41b24d8363211e1f8aae8d99d3e9476690f94af54  k_express_close_handle_sunburst_high_v6.png
58b551333a230d5760432f9252c2f487d2066e3b047c1cf0b075dbe767970bcc  k_express_wide_candid_sunburst_high_v7.png
```
