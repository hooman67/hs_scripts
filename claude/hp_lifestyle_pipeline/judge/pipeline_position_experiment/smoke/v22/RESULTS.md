# v22 eight-fixture smoke result

The fixed protocol completed all eight rows with one live Stage-B call and one
unmasked image call per row, no retries, no best-of and no manual repair.

Feature-matched affine estimates compare product landmarks in each result to the
frozen geometry guide. They are diagnostics, not pixel-perfect masks.

| Fixture | Mode | Scale | Rotation | Translation x,y | Outcome |
|---|---|---:|---:|---:|---|
| Laptop close | original prompt | 0.8979 | +0.301° | +334, +38 px | Fail: moved and shrank about 10.2% |
| Laptop close | relocation demand | 0.8753 | +0.140° | -355, +62 px | Fail: actual move, but shrank about 12.5% |
| Laptop wide | original prompt | 0.9984 | +0.029° | +2, +1 px | Pass: retained baseline and invariants |
| Laptop wide | relocation demand | 1.0047 | +0.224° | +829, -10 px | Pass: actual move, recomposed support, scale/view preserved |
| Printer close | original prompt | 0.9755 | +0.344° | -155, +5 px | Fail exact-scale contract: shrank about 2.5% |
| Printer close | relocation demand | 0.9567 | +0.196° | +499, -1 px | Fail exact-scale contract: shrank about 4.3% |
| Printer wide | original prompt | 1.0304 | +0.059° | -25, -246 px | Fail exact-scale contract: enlarged about 3.0% |
| Printer wide | relocation demand | 1.0693 | +1.688° | +674, -256 px | Fail: enlarged about 6.9% with orientation drift |

The wide-laptop pair proves the intended experiment can work: the neutral scene
kept the baseline, while the relocation request produced a large x-y move, a new
usable table/chair composition, and no obvious guide ghost, with scale and
orientation close to exact. The high-fill close cases encouraged the model to
trade pixel size for requested movement. Printer results also need a stronger
invariant, especially the wide relocation.

The next policy therefore makes close/high-fill placement conservative: retain
the initial x-y position by default, allow movement only while exact pixel width
and height remain unchanged, and explicitly retain the initial position rather
than shrink. Medium/wide remain free to translate and recompose support, while
the same never-shrink rule applies.

