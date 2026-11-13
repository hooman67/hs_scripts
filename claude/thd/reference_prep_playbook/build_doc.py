#!/usr/bin/env python3
"""Build the Reference-Image Prep Playbook (self-contained HTML with before/after examples).
Copies+resizes example images into the media dir, renders index.html. Source lives in the repo;
images + HTML go to /home/colligo/THD_ref_prep_doc/ and get uploaded to S3."""
import os, glob, html, shutil
from PIL import Image

LAUN="/home/colligo/THD_laundry_sink_storyboard"
MAK="/home/colligo/THD_makita_storyboard"
OUT="/home/colligo/THD_ref_prep_doc"; A=os.path.join(OUT,"assets")
os.makedirs(A,exist_ok=True)

def g(pat):  # resolve a path or glob (handles the U+202F screenshot filename)
    if os.path.exists(pat): return pat
    m=glob.glob(pat); 
    return m[0] if m else None

def stage(src, name, maxw=760):
    """copy+resize an image into assets, return the asset filename"""
    p=g(src)
    if not p: return None
    im=Image.open(p).convert("RGB")
    if im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)))
    out=os.path.join(A,name+".jpg"); im.save(out,quality=85)
    return name+".jpg"

NANO="fal-ai/nano-banana-pro/edit  (resolution 2K)"

# each technique: title, when/why, before(src,label), after(src,label), model, prompt, notes[]
T=[
 dict(id="paintout", title="1a · Paint the person OUT → person-free scene plate",
   why="The base move for any beat with people. Seedance's R3 filter rejects ANY photoreal human in an image reference, so we remove the real talent and let Seedance GENERATE our invented couple from text on top of the clean plate.",
   before=(f"{LAUN}/images/image26.jpeg","Customer still (real talent at the finished sink)"),
   after=(f"{LAUN}/prep/8A_plate.png","Person-free plate (talent painted out, room kept)"),
   model=NANO,
   prompt=("Remove the people entirely (all faces, bodies, arms and hands) from this photo and fill the "
     "vacated area with the plausible continuation of the laundry room and the cabinet/sink parts behind "
     "them. Keep the room, cabinet, sink, floor and background exactly as they are. Photoreal, no people, "
     "no text, no logos."),
   notes=["Then generate the couple in ref-mode with a fixed 'couple bible' description reused verbatim.",
     "Keeps the SET consistent across shots (same room/wardrobe come from the plate + reused text)."]),
 dict(id="coverbody", title="1b · Cover the body, KEEP the hands (hands are R3-safe)",
   why="You do NOT always have to remove the whole person. Bare hands and forearms PASS the R3 filter — only the face, head and torso trip it. So for a tool/measurement shot, keep the real hands + the tool exactly, and replace ONLY the head, face and torso. This preserves the true hand pose and the tool's real look (from the door-lock 'How to Install a Door Lock' work).",
   before=("/home/colligo/THD_How_to_Install_a_Door_Lock/work/shot0003_frames/f2_t2.14.jpg","Original frame — head + torso + hands + a baked-in 'TIP' graphic"),
   after=("/home/colligo/THD_ref_prep_doc/src/wbeat1.png","Cover-body result — head/torso + graphic gone, real hands + tape kept"),
   extra_after=("/home/colligo/THD_ref_prep_doc/src/wbeat3.png","Another beat — same technique (measuring door thickness)"),
   model=NANO,
   prompt=("Edit this image. KEEP the person's forearms, hands and the tape measure EXACTLY as they are — "
     "identical pixels, same natural length and position; do NOT stretch, lengthen, move or redraw the arms "
     "or hands. Replace ONLY the head, face, hair, neck and torso/upper body with the plain background that "
     "belongs behind them. Also remove any on-screen graphics, step labels or caption text, replacing them "
     "with the plain scene behind. Keep the door, hardware, tools and the whole background scene otherwise "
     "unchanged. The result: natural forearms and hands using the tape measure, with no head, face or torso "
     "and no on-screen graphics. Photoreal. No text, no logos."),
   notes=["R3 rule of thumb: HANDS/FOREARMS pass; FACE, HEAD, TORSO (and gloves) get rejected.",
     "Also strips baked-in step/TIP caption graphics in the same edit (brand-safe, no stray text).",
     "Do NOT remove the arms too — nano then regrows long, unnatural hands. Keep the real hands verbatim.",
     "Then generate the rest of the person around the kept hands via the prompt ('full person visible…')."]),
 dict(id="flat", title="2 · Keep pieces FLAT & SEPARATE (stop nano hallucinating assembly)",
   why="When painting people out of a half-built product, nano 'helpfully' COMPLETES it (flat panels → finished box). You must forbid that explicitly.",
   before=(f"{LAUN}/images/image8.jpeg","Couple laying out FLAT panels on the floor"),
   after=(f"{LAUN}/prep/1A_plate_v2.png","Fixed plate — flat panels kept separate"),
   model=NANO,
   prompt=("Remove ONLY the two people (all faces, bodies, arms, hands) from this overhead photo. Keep "
     "EVERYTHING ELSE EXACTLY as it is — especially the FLAT, UNASSEMBLED white cabinet panels lying on the "
     "floor. Do NOT assemble, stand up, fold, or complete the cabinet — the panels MUST stay lying flat on the "
     "floor exactly as shown. Only fill the areas where the people's bodies were with the plain tile floor."),
   notes=["FAILURE MODE (first attempt): the plate came back as a fully-assembled 3D cabinet box — wrong.",
     "RULE: always eyeball the plate before generating; nano silently 'finishes' partially-built products."]),
 dict(id="raised", title="3 · Keep a RAISED / held panel (don't flatten it)",
   why="If a person is holding a panel UP, a naive paint-out lays it flat and you lose the progression.",
   before=(f"{LAUN}/images/image5.jpeg","Man holding a side panel UP"),
   after=(f"{LAUN}/prep/S2b_image5_raised.png","Panel kept standing/tilted (person removed)"),
   model=NANO,
   prompt=("Remove ONLY the two people (faces, bodies, arms, hands, and any reflections). CRITICAL: keep the "
     "white panel that is RAISED/TILTED UP off the floor exactly where it is, standing/tilted in the same spot "
     "(it is OK if it looks unsupported). Do NOT lay any panel down flat, do NOT move, rotate, assemble or "
     "connect any panel."),
   notes=["Gives a real flat→lifted→standing progression for ordered-keyframe assembly shots."]),
 dict(id="reflections", title="4 · Remove people AND their reflections (R3 edge cases)",
   why="R3 also catches partial people at frame edges and REFLECTIONS of people in glass/metal (washer doors). A plate that looks clean can still be rejected.",
   before=(f"{LAUN}/images/image7.jpeg","Overhead flat-lay (people/reflections at edges)"),
   after=(f"{LAUN}/prep/S2a_image7_plate.png","People + reflections removed → passes R3"),
   model=NANO,
   prompt=("Remove ALL people and ANY parts or traces of people from this photo — including partial bodies, "
     "legs, feet or hands at the edges, and any reflections of people in the washer/dryer glass doors or "
     "stainless surfaces. Keep every cabinet panel and the sink basin exactly where they are, flat and "
     "separate. Photoreal, absolutely no people and no person reflections, no text, no logos."),
   notes=["This exact image tripped R3 as-is (washer-drum shapes/reflections at the top edge) until cleaned."]),
 dict(id="sketchify", title="5 · Sketchify a photo / screenshot → structure keyframe",
   why="When the customer gives PHOTOS or video screenshots (with the WRONG couple + baked-in captions + browser chrome), convert them to line-art. A sketch carries the composition/pose but NO real-person likeness (R3-safe) and no text.",
   before=("/home/colligo/thd_screen/*3.32.38*PM.png","Customer screenshot (chrome + SUPER + wrong couple)"),
   after=(f"{LAUN}/prep/S6a_sk1_pushleft.png","Line-art sketch (structure only)"),
   model=NANO,
   prompt=("Convert this photo into a CLEAN, BOLD black-and-white LINE DRAWING on pure white paper of ONLY the "
     "white cabinet box being assembled and the people's hands/arms. Draw the exact composition, box shape, "
     "panel positions and hand positions. IGNORE and OMIT everything else: do NOT draw any on-screen text, "
     "captions, UI, play buttons, timestamps, black bars, floor-mat pattern or background clutter. Pure line "
     "art of the cabinet and hands only."),
   notes=["Pair the sketches (structure) with a PRIOR generated frame as the photoreal 'style' reference so the",
     "video renders photoreal with OUR couple — not the sketch look, not the screenshot's people."]),
 dict(id="cleanmarks", title="6 · Clean camera / annotation MARKS off a sketch",
   why="Hand-drawn storyboards (and customer-annotated sketches) carry red camera arrows, 'CUT'/'ZOOM IN' text, colored motion marks. If you leave them in, Seedance RENDERS them into the video.",
   before=(f"{MAK}/images/page_38_img_02.jpeg","Storyboard sketch with red 'CUT'/'ZOOM IN' arrows"),
   after=(f"{MAK}/prep/S901_sketch_clean.png","Clean line-art (marks removed)"),
   model=NANO,
   prompt=("Remove ALL the red arrows, red lines and hand-written text ('CUT','ZOOM IN') that are annotation "
     "marks overlaid on this storyboard sketch. Keep the underlying grey-and-black line drawing exactly as it "
     "is. Line art only, no red marks, no words."),
   notes=["LESSON: telling the model to 'honor but not draw' the marks does NOT work — it still draws them.",
     "Either clean the sketch (this) and describe motion in prose, OR generate then video-EDIT the marks out."]),
 dict(id="recolor", title="7 · Recolor a finish → color variant",
   why="For color-variant beauty shots, recolor ONLY the finish and keep everything else identical.",
   before=(f"{LAUN}/images/image1.jpeg","Hero still — white cabinet"),
   after=(f"{LAUN}/prep/S18_whiteoak.png","White Oak variant (only finish changed)"),
   model=NANO,
   prompt=("Change ONLY the white laundry-sink cabinet's finish to a warm WHITE OAK wood-grain laminate — light "
     "natural oak with visible straight wood grain on the doors, drawer and sides. Keep the stainless sink and "
     "faucet, the brushed-nickel knobs, the washer and dryer, the shelves, art, floor and the ENTIRE room and "
     "composition exactly the same. Photoreal, no text, no logos."),
   notes=["Then animate with the same locked-off 'camera does not move' establishing recipe."]),
 dict(id="sketch2real", title="8 · Sketch → PHOTOREAL render (ground the real product)",
   why="For hand-drawn tool storyboards there's no photo to reference. nano renders the sketch into a photoreal frame — and it knows the real product look (e.g. Makita teal/black). That photoreal frame becomes the i2v keyframe.",
   before=(f"{MAK}/prep/S901_sketch_clean.png","Clean storyboard sketch"),
   after=(f"{MAK}/prep/S901_photoreal.png","nano photoreal render (real Makita saw)"),
   model=NANO,
   prompt=("Render this storyboard line-drawing as a PHOTOREALISTIC film frame. It shows a real MAKITA 7-1/4in "
     "rear-handle circular saw — Makita's signature TEAL/turquoise and black body, silver metal blade and base "
     "plate — being pushed along a board, cutting, with a pro's two hands on the handles (hands/forearms only, "
     "NO face), fine sawdust spraying. Keep the exact composition, camera angle and framing of the sketch. "
     "Photoreal, cinematic workshop lighting, shallow depth of field."),
   notes=["Pipeline for sketch storyboards:  sketch → clean marks → nano photoreal render → i2v animate."]),
 dict(id="toolmacro", title="9 · Make a tool macro PERSON-FREE (so it passes R3)",
   why="Even a photoreal render can trip R3 if it shows a torso or gloved hands. Re-render tool CUs person-free.",
   before=(f"{MAK}/prep/S806_photoreal.png","Photoreal render WITH torso + gloves (R3 REJECTED)"),
   after=(f"{MAK}/prep/S806_photoreal_v2.png","Person-free tool macro (R3 OK)"),
   model=NANO,
   prompt=("Reframe to an EXTREME CLOSE-UP of ONLY the Makita angle grinder's cutting disc meeting the steel "
     "pipe/weld, with a bright shower of orange sparks. REMOVE the person entirely — no torso, no shoulder, no "
     "arm, no gloves, no hands anywhere; show ONLY the teal-and-black Makita grinder tool head, the metal pipe "
     "and the sparks. Fill vacated area with the dark workshop background. Photoreal, dark cinematic, glowing sparks."),
   notes=["R3 nuance: bare forearms/hands often PASS, but a visible torso or gloves REJECT. Keep macros person-free."]),
 dict(id="cautionary", title="10 · ⚠ Cautionary — do NOT feed a synthetic person as a Seedance ref",
   why="It's tempting to swap the real couple for an invented one and feed THAT. It looks perfect — but Seedance's R3 filter rejects it anyway (it can't tell it's synthetic). This route is a dead end.",
   before=(f"{LAUN}/images/image8.jpeg","Customer still (real couple)"),
   after=(f"{LAUN}/prep/1A_couple.png","Synthetic couple swap — looks right, but R3-REJECTED as a video ref"),
   model=NANO,
   prompt=("Edit this photo. Replace the two people with <invented couple description>. Keep their poses, hands "
     "and the action exactly the same, and keep the whole background identical. Natural photoreal people, plain "
     "clothing, no logos. Only change who the people are."),
   notes=["Seedance returns content_policy_violation for ANY photoreal human in image_url/image_urls — real OR synthetic.",
     "USE INSTEAD: paint the people OUT (#1) and generate the couple from a reused text 'bible'.",
     "EXCEPTION: the video-EDIT route (reference-to-video + video_urls) does NOT trip R3 — use it to clean an existing clip."]),
]

def card(t):
    b=stage(*t["before"][:1], name=t["id"]+"_before"); a=stage(*t["after"][:1], name=t["id"]+"_after")
    def img(fn,cap):
        return (f'<figure><a href="assets/{fn}" target="_blank"><img loading="lazy" src="assets/{fn}"></a>'
                f'<figcaption>{html.escape(cap)}</figcaption></figure>') if fn else '<figure class="miss">missing</figure>'
    extra=""
    if t.get("extra_after"):
        e=stage(*t["extra_after"][:1], name=t["id"]+"_after2")
        extra=f'<span class="arrow">+</span>{img(e,t["extra_after"][1])}'
    return f'''<section class="card" id="{t['id']}">
      <h2>{html.escape(t['title'])}</h2>
      <p class="why">{html.escape(t['why'])}</p>
      <div class="pair"><div class="ba">{img(b,t['before'][1])}<span class="arrow">→</span>{img(a,t['after'][1])}{extra}</div></div>
      <div class="meta"><span class="k">MODEL</span> {html.escape(t['model'])}</div>
      <details class="prompt" open><summary>nano-banana edit prompt</summary><pre>{html.escape(t['prompt'])}</pre></details>
      <ul class="notes">{''.join(f'<li>{html.escape(n)}</li>' for n in t['notes'])}</ul>
    </section>'''

CSS="""*{box-sizing:border-box}body{margin:0;background:#0b0d10;color:#e6e6e6;font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:28px}
h1{font-size:26px;margin:0 0 6px}.sub{color:#9aa4af;margin:0 0 8px}
.intro{background:#11161b;border:1px solid #232a31;border-radius:10px;padding:16px 18px;margin:18px 0}
.intro b{color:#7fb0ff}.intro code{background:#0d1216;border:1px solid #232a31;border-radius:4px;padding:1px 5px;color:#9fd0a0}
.toc{columns:2;font-size:14px;color:#b9c2cb;margin:8px 0 24px}.toc a{color:#7fb0ff;text-decoration:none}
.card{background:#11161b;border:1px solid #232a31;border-radius:12px;padding:18px 20px;margin:0 0 20px}
h2{font-size:18px;margin:0 0 8px;color:#fff}.why{color:#cdd6df;margin:0 0 14px}
.ba{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
figure{margin:0;flex:1;min-width:300px}figure img{width:100%;border-radius:8px;border:1px solid #232a31;display:block}
figcaption{font-size:12px;color:#8b95a0;margin-top:6px}.arrow{font-size:28px;color:#f96302;font-weight:700}
.miss{color:#ff8f8f;padding:20px;border:1px dashed #6b1e1e;border-radius:8px}
.meta{margin:14px 0 6px;font-size:13px;color:#b9c2cb}.k{background:#232a31;border-radius:5px;padding:2px 8px;font-size:11px;letter-spacing:.5px;color:#9fd0a0;margin-right:8px}
details.prompt{margin:8px 0;background:#0d1216;border:1px solid #232a31;border-radius:8px;padding:8px 12px}
details.prompt summary{cursor:pointer;color:#7fb0ff;font-size:13px}details.prompt pre{white-space:pre-wrap;color:#c8d1da;font-size:13px;margin:8px 0 0}
ul.notes{margin:10px 0 0;padding-left:18px;color:#cdd6df;font-size:14px}ul.notes li{margin:4px 0}
"""
INTRO=('<div class="intro"><b>What this is.</b> Customer storyboard assets (photos, hand-drawn sketches, video '
 'screenshots) can almost never be sent to the video model as-is. This is the set of image edits we run FIRST, '
 'why each is needed, and the exact prompts.<br><br>'
 '<b>The prep model:</b> <code>fal-ai/nano-banana-pro/edit</code> (image editing, 2K) for every edit below. '
 'The video model that consumes the prepared refs is <b>Seedance 2.5</b> '
 '(<code>bytedance/seedance-2.5/{image-to-video, reference-to-video}</code> on fal.ai).<br><br>'
 '<b>The constraint that drives most of this — "R3":</b> Seedance rejects (422 content_policy_violation) ANY '
 'photoreal human in an image reference — real OR synthetic, including partial bodies at edges and reflections. '
 'Bare hands/forearms usually pass; a face, torso or gloves do not. So references are prepared to be '
 'person-free (paint-out), non-photoreal (sketch), or hands-only.</div>')
toc=''.join(f'<a href="#{t["id"]}">{html.escape(t["title"])}</a><br>' for t in T)
body=(f'<div class="wrap"><h1>Reference-Image Prep Playbook</h1>'
 f'<p class="sub">How customer storyboard assets are prepared before the video model — THD storyboard→video (FFDY-7304 laundry sink, FFDY-7309 Makita)</p>'
 f'{INTRO}<div class="toc">{toc}</div>'+''.join(card(t) for t in T)+'</div>')
SCRIPTS=("<script src=\"https://auth-stg1.services.adobe.com/imslib/imslib.js\"></script>"
 "<script src=\"./imsauth.js\"></script>"
 "<script>function onAuthReady(){}"
 "document.addEventListener('DOMContentLoaded',function(){try{initializeIMS();}catch(e){}"
 "setTimeout(function(){var c=document.getElementById('content'),l=document.getElementById('loading');"
 "if(c&&c.classList.contains('hidden')){c.classList.remove('hidden');if(l)l.style.display='none';}},9000);});</script>")
DOC=(f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
 f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>Reference-Image Prep Playbook</title>'
 f'<style>{CSS}\n#loading{{padding:48px;text-align:center;color:#9aa4af}}.hidden{{display:none}}</style></head><body>'
 f'<div id="loading">Loading\u2026</div><div id="content" class="hidden">{body}</div>{SCRIPTS}</body></html>')
open(os.path.join(OUT,"index.html"),"w").write(DOC)
print("wrote", os.path.join(OUT,"index.html"), f"({len(DOC)} bytes),", len(os.listdir(A)), "asset images")
