#!/usr/bin/env python3
import os, shutil, html
OUT="/home/colligo/THD_laundry_sink_storyboard/videoedit_report"
A=f"{OUT}/assets"; os.makedirs(A,exist_ok=True)
GC="/home/colligo/THD_laundry_sink_storyboard/gen_compare/sd25"
VE="/home/colligo/THD_laundry_sink_storyboard/videoedit_test"
T="/home/colligo/.claude/jobs/d24f6783/tmp"
# assets
shutil.copy(f"{GC}/S11_8B/S11_8B.mp4", f"{A}/people_hero.mp4")
shutil.copy(f"{GC}/S06_box/S06_box.mp4", f"{A}/people_overhead.mp4")
shutil.copy(f"{GC}/S01/S01.mp4", f"{A}/ctrl_before.mp4")
shutil.copy(f"{VE}/B_change_object.mp4", f"{A}/ctrl_after.mp4")
shutil.copy(f"{T}/ctrl_ba.png", f"{A}/ctrl_ba.png")
# Seedance 2.0 results (same tests — people clips NOT blocked)
GC20="/home/colligo/THD_laundry_sink_storyboard/gen_compare/sd20"
VE20="/home/colligo/THD_laundry_sink_storyboard/videoedit_test_sd20"
shutil.copy(f"{GC20}/S11_8B/S11_8B.mp4", f"{A}/s20_src.mp4")
shutil.copy(f"{VE20}/A_change_character.mp4", f"{A}/s20_char.mp4")
shutil.copy(f"{VE20}/B_change_object.mp4", f"{A}/s20_obj.mp4")
shutil.copy(f"{T}/s20_ba_charswap.png", f"{A}/s20_ba_charswap.png")
shutil.copy(f"{T}/s20_ba_objedit.png", f"{A}/s20_ba_objedit.png")
def e(s): return html.escape(s or "")
ERR=('{"detail":[{"loc":["body","video_urls"],"msg":"The images or videos provided may contain '
     'likenesses of real people or other private information that cannot be processed.",'
     '"type":"content_policy_violation"}]}')
PROMPT_A=("Video edit. Keep the camera, framing, room, lighting and all body motion EXACTLY the same. "
 "Change ONLY the appearance of the two people: replace them with a different couple — a young woman with "
 "long wavy red hair in a mustard-yellow cardigan, and a clean-shaven man in his 30s with short dark-brown "
 "hair in a dark-green henley. Same poses, same positions, same movement.")
PROMPT_B=("Video edit. Keep the two people, their clothing, faces, poses and all motion EXACTLY the same. "
 "Change ONLY the base cabinet under the sink: recolor it from white to a deep matte navy blue.")
PROMPT_CTRL=("Same video-edit prompt as Test B (recolor the base cabinet white → deep matte navy blue), "
 "run on the person-free establishing shot instead.")

CSS="""*{box-sizing:border-box}body{margin:0;background:#0b0d10;color:#e6e6e6;font:14px/1.6 -apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:26px}h1{font-size:25px;margin:0 0 6px}.sub{color:#9aa4af;margin:0 0 18px}
.verdict{background:#1a1113;border:1px solid #6b1e1e;border-left:4px solid #ff6b6b;border-radius:10px;padding:14px 18px;margin:18px 0}
.verdict b{color:#ff8f8f}
.ok{background:#0f1a12;border:1px solid #1e6b34;border-left:4px solid #3ddc84;border-radius:10px;padding:14px 18px;margin:18px 0}
.ok b{color:#3ddc84}
h2{font-size:17px;border-bottom:1px solid #232a31;padding-bottom:8px;margin:34px 0 12px}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13px}
th,td{border:1px solid #232a31;padding:8px 10px;text-align:left}th{background:#161c22;color:#cdd6df}
.blk{color:#ff8f8f;font-weight:700}.pass{color:#3ddc84;font-weight:700}
.card{background:#11161b;border:1px solid #232a31;border-radius:10px;padding:14px;margin:14px 0}
.card.bad{border-color:#6b1e1e}.card.good{border-color:#1e6b34}
video{width:100%;border-radius:8px;background:#000;margin:6px 0}img{width:100%;border-radius:8px;border:1px solid #232a31}
pre{white-space:pre-wrap;background:#0d1216;border:1px solid #232a31;border-radius:6px;padding:10px;color:#c8d1da;font-size:12px;overflow-x:auto}
.err{color:#ff8f8f;background:#1a1113;border:1px solid #6b1e1e;border-radius:6px;padding:8px 10px;font-size:12px;font-family:monospace}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.lbl{font-size:11px;color:#8b95a0;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
.hidden{display:none}.loading-screen{padding:48px;text-align:center;color:#9aa4af}
#ims{padding:8px 12px;background:#0d1216;border-bottom:1px solid #232a31;font-size:12px;color:#9aa4af}"""

BODY=f"""<div class="wrap">
<h1>Seedance video-edit &amp; people — 2.5 blocks, 2.0 allows</h1>
<p class="sub">Test date 2026-08-28. Route = <code>reference-to-video</code> with <code>video_urls</code>=[a
Seedance-generated clip] + an edit prompt. Inputs are clips Seedance itself produced (synthetic couple from
its own bank), not real footage.</p>

<div class="verdict"><b>Seedance 2.5 — CONFIRMED blocks its own people (TRUE, stronger than the claim).</b>
The 2.5 video-edit route <b>rejects any input video that contains a human likeness</b> with a
<code>content_policy_violation</code> on <code>video_urls</code> — <b>including characters Seedance itself
generated</b>. The block fires on the <i>input</i>, so it doesn't matter whether you change the character or
only an object: <b>4/4 people-clips blocked</b> (hero close-up AND overhead shots with small/occluded faces;
both a character-swap and an object-only edit).</div>

<div class="ok"><b>Seedance 2.0 — the same tests WORK, people and all.</b> Running the identical edits on
<code>bytedance/seedance-2.0/reference-to-video</code> was <b>not</b> blocked: it swapped the couple
(character change) AND recolored the cabinet while keeping the couple (object change), on the same kind of
people-clip that 2.5 refuses. <b>So for editing a finished shot that contains people, use the 2.0 video-edit
endpoint.</b> (2.5 still only works on person-free clips — the navy-cabinet recolor below.)</div>

<p><b>Note — this reverses our earlier finding.</b> On 2026-08-25 the video-edit route did <i>not</i> trip
the people filter (that's how we cleaned rendered annotation marks off a couple shot). As of 2026-08-28 it
does. The policy on this endpoint tightened in between. The overlay-cleanup trick on people shots no longer
works.</p>

<h2>Test matrix</h2>
<table>
<tr><th>#</th><th>Source clip</th><th>People in source?</th><th>Edit requested</th><th>Result</th></tr>
<tr><td>A</td><td>S11 hero (couple, close-up)</td><td>Yes (2, prominent faces)</td><td>Change the characters</td><td class="blk">BLOCKED</td></tr>
<tr><td>B</td><td>S11 hero (couple, close-up)</td><td>Yes (2, prominent faces)</td><td>Object only (recolor cabinet)</td><td class="blk">BLOCKED</td></tr>
<tr><td>C</td><td>S06 box (overhead assembly)</td><td>Yes (small/occluded faces)</td><td>Object only (recolor cabinet)</td><td class="blk">BLOCKED</td></tr>
<tr><td>D</td><td>S02 assemble (overhead)</td><td>Yes (partial bodies)</td><td>Change the characters</td><td class="blk">BLOCKED</td></tr>
<tr><td>E</td><td>S01 establishing</td><td class="pass">No people</td><td>Object only (recolor cabinet)</td><td class="pass">RENDERED</td></tr>
<tr><td colspan="5" style="background:#0f1a12"><b>Seedance 2.0 endpoint — same edits, people-clips</b></td></tr>
<tr><td>F</td><td>S11 hero (couple) — 2.0</td><td>Yes, prominent</td><td>Change the characters</td><td class="pass">RENDERED</td></tr>
<tr><td>G</td><td>S11 hero (couple) — 2.0</td><td>Yes, prominent</td><td>Object only (recolor cabinet)</td><td class="pass">RENDERED</td></tr>
<tr><td>H</td><td>S01 establishing — 2.0</td><td class="pass">No people</td><td>Object only</td><td class="pass">RENDERED</td></tr>
</table>

<h2>Blocked — Test A &amp; B (source contains Seedance's own generated couple)</h2>
<div class="card bad">
<div class="lbl">source clip fed to video-edit (Seedance-2.5 generated, synthetic couple)</div>
<video controls preload="metadata" src="assets/people_hero.mp4"></video>
<div class="lbl">Test A prompt — change the characters</div><pre>{e(PROMPT_A)}</pre>
<div class="lbl">Test B prompt — object only, people kept</div><pre>{e(PROMPT_B)}</pre>
<div class="lbl">identical error returned in &lt;10s for BOTH</div>
<div class="err">{e(ERR)}</div>
</div>
<div class="card bad">
<div class="lbl">overhead source (Test C/D) — small/occluded faces — ALSO blocked, same error</div>
<video controls preload="metadata" src="assets/people_overhead.mp4"></video>
</div>

<h2 style="border-color:#1e6b34">Rendered — Test E (person-free control)</h2>
<div class="card good">
<div class="lbl">prompt</div><pre>{e(PROMPT_CTRL)}</pre>
<div class="lbl">before → after (frame): white cabinet recolored to navy, everything else preserved</div>
<img src="assets/ctrl_ba.png">
<div class="two">
<div><div class="lbl">BEFORE (source)</div><video controls preload="metadata" src="assets/ctrl_before.mp4"></video></div>
<div><div class="lbl">AFTER (video-edit output)</div><video controls preload="metadata" src="assets/ctrl_after.mp4"></video></div>
</div>
</div>

<h2 style="border-color:#1e6b34">Seedance 2.0 — same edits on a people-clip, NOT blocked</h2>
<div class="card good">
<div class="lbl">source clip fed to 2.0 video-edit (Seedance-2.0 generated couple)</div>
<video controls preload="metadata" src="assets/s20_src.mp4"></video>
<div class="lbl">Test F — change the characters (frame): couple swapped to red-haired woman in mustard cardigan + dark-haired man in green henley; same poses, room, motion</div>
<img src="assets/s20_ba_charswap.png">
<video controls preload="metadata" src="assets/s20_char.mp4"></video>
<div class="lbl">Test G — object only, people kept (frame): cabinet white → navy, the ORIGINAL couple preserved</div>
<img src="assets/s20_ba_objedit.png">
<video controls preload="metadata" src="assets/s20_obj.mp4"></video>
</div>

<h2>What this means</h2>
<ul>
<li><b>Seedance 2.5 video-edit can no longer touch people shots</b> — character swap, wardrobe fix, or even
an unrelated object change — the source clip is rejected before any edit is attempted (block is on the
<i>input</i>, so no prompt wording gets around it). It stays valid only for <b>person-free</b> clips.</li>
<li><b>Seedance 2.0 video-edit DOES work on people shots</b> — both character swaps and people-preserving
object edits rendered cleanly. So the overlay-cleanup / character-change workflow on finished people clips
still exists — just move it to the <b>2.0</b> endpoint.</li>
<li>Trade-off: 2.0 is the older/slightly-lower-fidelity generation, so expect its edits to be a touch softer
than a 2.5 render. For editing finished people footage that's currently the only Seedance option; for
person-free clips either version works.</li>
</ul>
</div>"""
SCRIPTS=('<script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script><script src="./imsauth.js"></script>'
 '<script>function onAuthReady(){}document.addEventListener("DOMContentLoaded",function(){try{initializeIMS();}catch(e){}'
 'setTimeout(function(){var c=document.getElementById("content"),l=document.getElementById("loading");'
 'if(c&&c.classList.contains("hidden")){c.classList.remove("hidden");if(l)l.style.display="none";}},9000);});</script>')
DOC=(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
 f'<title>Seedance 2.5 video-edit — people block test</title><style>{CSS}</style></head><body>'
 f'<div id="ims"></div><div id="loading" class="loading-screen">Loading…</div>'
 f'<div id="content" class="hidden">{BODY}</div>{SCRIPTS}</body></html>')
open(f"{OUT}/index.html","w").write(DOC)
shutil.copy("/home/colligo/THD_laundry_sink_storyboard/gallery/imsauth.js", f"{OUT}/imsauth.js")
print("wrote", f"{OUT}/index.html", len(DOC),"bytes")
