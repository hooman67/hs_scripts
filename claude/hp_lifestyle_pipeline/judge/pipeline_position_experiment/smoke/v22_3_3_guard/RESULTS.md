# V22.3.3 eight-fixture smoke

Pipeline: `unified-blue-scale-v22.3.3-clean-fixed-rewrite-affine-guard-twin-camera-guide-only-no-mask`

| fixture | status | image calls | Stage-B calls | selected | a1 tx | a1 ty | a1 singulars | a1 rot | a1 p95 | a1 failures | a2 tx | a2 ty | a2 singulars | a2 rot | a2 p95 | a2 failures |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cashmere__laptop_FrontCloseUp__p1__retained_control | ok | 1 | 1 | 1 | 1.7777 | -1.1277 | [0.9995386892000742, 0.9989835450039976] | 0.0391 | 3.1485 |  |  |  |  |  |  |  |
| cashmere__laptop_FrontCloseUp__p1__relocation_demand | ok | 1 | 1 | 1 | 2.0982 | 0.9831 | [0.9989301269879349, 0.99557042412701] | 0.0550 | 2.2192 |  |  |  |  |  |  |  |
| cashmere__laptop_FrontWide__p1__retained_control | ok | 1 | 1 | 1 | 1.0711 | -0.2339 | [0.9993980891747092, 0.996676113743601] | 0.0554 | 2.1477 |  |  |  |  |  |  |  |
| cashmere__laptop_FrontWide__p1__relocation_demand | ok | 1 | 1 | 1 | 776.4609 | -21.6234 | [0.9983840454268051, 0.9882428605781028] | 0.1180 | 2.4737 |  |  |  |  |  |  |  |
| magic__printer_FrontCloseUp__p1__retained_control | ok | 1 | 1 | 1 | 1.0972 | 0.6302 | [0.999515010414078, 0.9977933954290441] | 0.0190 | 2.0802 |  |  |  |  |  |  |  |
| magic__printer_FrontCloseUp__p1__relocation_demand | ok | 1 | 1 | 1 | 0.8998 | 1.3299 | [1.000392857373524, 0.9990170731539142] | -0.0104 | 2.1464 |  |  |  |  |  |  |  |
| magic__printer_FrontWide__p1__retained_control | ok | 2 | 2 | 2 | 30.9873 | -77.9914 | [0.9902285816725277, 0.9619110267791243] | 0.6342 | 1.6317 | singular_min,anisotropy | -1.5192 | 3.1788 | [1.0022280889454467, 0.9936896391595799] | 0.0680 | 1.9596 |  |
| magic__printer_FrontWide__p1__relocation_demand | ok | 1 | 1 | 1 | 813.6735 | -200.2991 | [1.0087776779967614, 1.0010452282741782] | 0.1876 | 2.2478 |  |  |  |  |  |  |  |

## Contract checks

- Frozen V6.1 product, reference, Stage-A geometry and guide used for every row.
- HIGH-FILL keeps its initial position policy.
- LOWER-FILL may use one initial generation plus at most one fresh fixed-position Stage-B rewrite and one fallback image.
- Every fallback executable was scanned for LOWER-FILL, x-y, translation and relocation language before the second image call.
- No best-of selection, image retry, mask, resize or post-generation alignment.
