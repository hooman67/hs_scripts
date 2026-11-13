# V6 downstream prop additions audit

This audit compares all 96 V6 input prompts with the complete downstream Gemini 3.1 Pro usedPrompt. It found **25/96 rows (26.0%)** where the rewrite explicitly requested at least one movable prop, furnishing, board, or shelf content that the V6 prompt did not request.

Fixed architecture such as windows, walls, glass partitions, and meeting rooms is excluded from that count. The primary device, its support surface, and rewritten wording for the same upstream prop are also excluded.

## Most frequent added families

| Family | Occurrences |
| --- | ---: |
| shelving | 9 |
| plant | 8 |
| chair | 3 |
| shelf_contents | 3 |
| whiteboard | 3 |
| sofa | 2 |
| book | 1 |
| brush_holder | 1 |
| curtains | 1 |
| drafting_board | 1 |
| framed_art | 1 |
| mood_board | 1 |
| saucer | 1 |

## Row-level evidence

| Prompt key | Added after V6 | Exact rewrite evidence | Generated image |
| --- | --- | --- | --- |
| cashmere__laptop_BackRightCloseUp::p2 | potted plant | In the background, a blurred modern corporate office environment recedes with glass partitions and a potted plant on the left. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/605c32d7b6837965f9ad__cashmere__laptop_BackRightCloseUp__p2.png) |
| cashmere__laptop_BackRightCloseUp::p5 | drafting board | In the background, a bright creative studio space recedes with a window on the left and a drafting board against the back wall. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/c5fa2f8c2177ff054bc9__cashmere__laptop_BackRightCloseUp__p5.png) |
| cashmere__laptop_FrontCloseUp::p2 | wooden chair, matching saucer | A wooden chair is tucked under a distant table; the coffee-cup entity is described as resting on a matching saucer. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/bbd5a6a65d0117db109b__cashmere__laptop_FrontCloseUp__p2.png) |
| cashmere__laptop_FrontCloseUp::p3 | glass paintbrush jar, wooden shelving unit, stacked paper and generic art supplies | The rewrite asks for a jar of paintbrushes and a wooden shelving unit holding stacked paper and art supplies. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/7bcb17c91025d590beab__cashmere__laptop_FrontCloseUp__p3.png) |
| cashmere__laptop_FrontCloseUp::p6 | potted plant | The rewritten background adds a blurred green potted plant on the left. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/796fe44045ec88a3d928__cashmere__laptop_FrontCloseUp__p6.png) |
| cashmere__laptop_FrontLeftMedium::p2 | framed print | The rewritten background adds a blurred wall with a framed print in the far background. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/c7f6999224ef9100d0a2__cashmere__laptop_FrontLeftMedium__p2.png) |
| elitebook__laptop_BackRightCloseUp::p2 | whiteboard | The rewritten background adds a distant white whiteboard on the wall to the left. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/2cf73e4257f74616e762__elitebook__laptop_BackRightCloseUp__p2.png) |
| elitebook__laptop_BackRightCloseUp::p4 | bookshelf, potted plant | The rewrite explicitly adds a blurred bookshelf on the right and a potted plant on the left. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/8c05ac51d1a40f60408d__elitebook__laptop_BackRightCloseUp__p4.png) |
| elitebook__laptop_BackRightCloseUp::p5 | bookshelf | The rewrite explicitly adds a softly blurred bookshelf against the wall on the left. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/7d3a704d0afcecce5a76__elitebook__laptop_BackRightCloseUp__p5.png) |
| elitebook__laptop_FrontCloseUp::p1 | bookshelf | The rewrite explicitly adds a bookshelf against the wall on the left. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/434cc73c48a5f003d4d6__elitebook__laptop_FrontCloseUp__p1.png) |
| elitebook__laptop_FrontLeftMedium::p1 | armchair | The rewrite explicitly adds a simple modern armchair farther back on the right. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/c0a0076fa425bef1744e__elitebook__laptop_FrontLeftMedium__p1.png) |
| tassel__printer_FrontCloseUp::p1 | bookshelf | The rewritten background adds a blurred bookshelf against a light wall. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/c6746e9d3f541a5b9b43__tassel__printer_FrontCloseUp__p1.png) |
| tassel__printer_FrontCloseUp::p2 | potted plant | The rewritten background adds a potted plant in the far background on the right. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/c30534aee111a33a42aa__tassel__printer_FrontCloseUp__p2.png) |
| tassel__printer_FrontCloseUp::p3 | sofa, potted plant | The rewritten background adds a neutral-toned sofa and a green potted plant. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/9e726ac4839fee00a678__tassel__printer_FrontCloseUp__p3.png) |
| tassel__printer_FrontCloseUp::p5 | potted plant | The rewritten background adds a blurred potted plant on the right. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/c66373a1ee2e06ad55e6__tassel__printer_FrontCloseUp__p5.png) |
| tassel__printer_FrontLeftMedium::p1 | potted plant | The rewrite adds a blurred potted plant against the wall on the left. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/a00867a10fc2cbfa4225__tassel__printer_FrontLeftMedium__p1.png) |
| tassel__printer_FrontLeftMedium::p2 | library bookshelves, books on shelves | The rewrite adds tall library bookshelves filled with neatly arranged books. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/8d9891caf28f18b9951f__tassel__printer_FrontLeftMedium__p2.png) |
| tassel__printer_FrontLeftMedium::p6 | sheer curtains | The rewritten background adds a window with sheer curtains. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/8d7ad735ae7b3d4fc8e8__tassel__printer_FrontLeftMedium__p6.png) |
| tassel__printer_FrontRightCloseUp::p1 | bookshelf | The rewrite adds a softly blurred wooden bookshelf against the wall on the left. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/f54c501716a279478fe9__tassel__printer_FrontRightCloseUp__p1.png) |
| tassel__printer_FrontRightCloseUp::p2 | potted plant | The rewrite adds a blurred potted plant on the right near a window. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/e1b925b44d4e5ae1fbda__tassel__printer_FrontRightCloseUp__p2.png) |
| tassel__printer_FrontRightCloseUp::p3 | studio shelving, generic craft supplies | The rewrite adds studio shelving holding unspecified craft supplies. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/ff594f0acbc29e6b51ae__tassel__printer_FrontRightCloseUp__p3.png) |
| tassel__printer_FrontRightCloseUp::p4 | low bookshelf, generic educational materials, whiteboard | The rewrite adds a low bookshelf filled with educational materials and a whiteboard. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/2e60714b40e281963c13__tassel__printer_FrontRightCloseUp__p4.png) |
| tassel__printer_FrontRightCloseUp::p5 | mood board | The rewrite adds a blurred mood board leaning against the wall. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/292840a65f2f314fe328__tassel__printer_FrontRightCloseUp__p5.png) |
| tassel__printer_FrontRightCloseUp::p6 | classroom chairs, whiteboard | The rewrite adds empty modern classroom chairs and a whiteboard. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/d6b35723ea4a0b2c4607__tassel__printer_FrontRightCloseUp__p6.png) |
| tassel__printer_FrontWide::p2 | sofa | The rewritten background adds a light-colored sofa receding behind the rug and floor cushion. | [image](https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/eval_sets/hp_lifestyle_approved_props_v6_top6_four_devices_20261029/generated_preview_v1/images/9f27807a84b46556ecad__tassel__printer_FrontWide__p2.png) |

## Interpreting the three C-Tech rows

- **Open notebook:** no rewrite-only cases. Every explicit rewritten open notebook came from a V6-declared notebook group.
- **Pencil/pen cup:** no input prompt, rewrite instruction, background, or rewrite entity requests one. If the approximate visual estimate is correct, it is an image-level addition or visual grouping, not an explicit stage-one rewrite request.
- **Stack of papers:** 13 of the 96 input prompts explicitly request a stack of papers, including wording such as “stack of plain papers” and “stack of household papers.” Fourteen rewrites request a stack. The one rewrite-only case is `cashmere__laptop_FrontCloseUp::p3`, where a shelving entity adds stacked paper and generic art supplies. The frozen `paper_documents` group contains 14 prompts because `tassel__printer_FrontWide::p3` declares worksheets rather than a stack. The former report’s zero input count came from an overly literal regular expression and has been corrected.

## Machine-readable trace

/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v5_v6_top6_distribution_20261030/downstream_prop_additions_audit.json
