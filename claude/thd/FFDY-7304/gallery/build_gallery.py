#!/usr/bin/env python3
"""Render manifest.json -> index.html (self-contained dark gallery). Re-run to append rounds."""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "manifest.json")))

BADGE = {"ok": ("#1e6b34", "#3ddc84", "RENDERED"),
         "rejected": ("#6b1e1e", "#ff6b6b", "REJECTED"),
         "pending": ("#5a4a1e", "#ffd24d", "PENDING")}


def esc(s):
    return html.escape(s or "")


def imgs(paths, cls="thumb"):
    return "".join(
        f'<a href="{esc(p)}" target="_blank"><img class="{cls}" loading="lazy" src="{esc(p)}"></a>'
        for p in (paths or []))


def prompt_block(p):
    if not p:
        return ""
    return (f'<details class="prompt"><summary>prompt ({len(p)} chars)</summary>'
            f'<pre>{esc(p)}</pre></details>')


def render_target(s):
    out = [f'<section class="target"><h2>{esc(s["label"])}</h2>']
    if s.get("params"):
        out.append(f'<div class="params">{esc(s["params"])}</div>')
    if s.get("note"):
        out.append(f'<p class="note">{esc(s["note"])}</p>')
    if s.get("link"):
        out.append(f'<a class="report-link" href="{esc(s["link"])}">{esc(s.get("link_label", "Open report"))}</a>')
    if s.get("reference_video") and s.get("video"):
        out.append('<div class="video-compare">')
        out.append(f'<div><div class="video-label">{esc(s.get("reference_video_label", "Motion reference"))}</div>'
                   f'<video controls preload="metadata" src="{esc(s["reference_video"])}"></video></div>')
        out.append(f'<div><div class="video-label">{esc(s.get("video_label", "Generated result"))}</div>'
                   f'<video controls preload="metadata" src="{esc(s["video"])}"></video></div>')
        out.append('</div>')
    elif s.get("video"):
        out.append(f'<video controls preload="metadata" src="{esc(s["video"])}"></video>')
    if s.get("input_videos"):
        out.append(f'<div class="reflabel">{esc(s.get("input_videos_label", "Video inputs"))}</div>')
        out.append('<div class="input-video-grid">')
        for v in s["input_videos"]:
            out.append(f'<div><div class="video-label">{esc(v.get("label", "Video input"))}</div>'
                       f'<video controls preload="metadata" src="{esc(v["src"])}"></video></div>')
        out.append('</div>')
    if s.get("input_images"):
        out.append(f'<div class="reflabel">{esc(s.get("input_images_label", "Image inputs"))}</div>')
        out.append('<div class="input-image-grid">')
        for item in s["input_images"]:
            out.append(f'<div><div class="video-label">{esc(item.get("label", "Image input"))}</div>'
                       f'<a href="{esc(item["src"])}" target="_blank">'
                       f'<img loading="lazy" src="{esc(item["src"])}"></a></div>')
        out.append('</div>')
    if s.get("frames"):
        if s.get("frames_label"):
            out.append(f'<div class="reflabel">{esc(s["frames_label"])}</div>')
        out.append(f'<div class="frames">{imgs(s["frames"])}</div>')
    if s.get("prompt"):
        out.append(prompt_block(s["prompt"]))
    if s.get("downloads"):
        if s.get("downloads_label"):
            out.append(f'<div class="reflabel">{esc(s["downloads_label"])}</div>')
        out.append('<div class="downloads">')
        for item in s["downloads"]:
            out.append(f'<a href="{esc(item["src"])}" target="_blank">{esc(item["label"])}</a>')
        out.append('</div>')
    out.append("</section>")
    return "\n".join(out)


def render_exp(e):
    bg, fg, txt = BADGE.get(e.get("status", "pending"), BADGE["pending"])
    out = [f'<div class="card {e.get("status","")}">',
           f'<div class="chead"><span class="eid">{esc(e["id"])}</span>'
           f'<span class="approach">{esc(e["approach"])}</span>'
           f'<span class="badge" style="background:{bg};color:{fg}">{txt}</span></div>']
    if e.get("refs"):
        out.append(f'<div class="reflabel">reference input:</div><div class="frames">{imgs(e["refs"])}</div>')
    if e.get("video"):
        out.append(f'<video controls preload="metadata" src="{esc(e["video"])}"></video>')
    if e.get("frames"):
        out.append(f'<div class="frames">{imgs(e["frames"])}</div>')
    if e.get("error"):
        out.append(f'<p class="err">{esc(e["error"])}</p>')
    if e.get("note"):
        out.append(f'<p class="note">{esc(e["note"])}</p>')
    if e.get("prompt"):
        out.append(prompt_block(e["prompt"]))
    out.append("</div>")
    return "\n".join(out)


def render_divider(s):
    sub = f'<div class="dsub">{esc(s.get("note",""))}</div>' if s.get("note") else ""
    link = (f'<a class="report-link" href="{esc(s["link"])}">'
            f'{esc(s.get("link_label", "Open report"))}</a>') if s.get("link") else ""
    return f'<section class="divider"><h1>{esc(s["label"])}</h1>{sub}{link}</section>'


def render_round(s):
    out = [f'<section class="round"><h2>{esc(s["label"])}</h2>']
    if s.get("params"):
        out.append(f'<div class="params">{esc(s["params"])}</div>')
    if s.get("shared_prompt_note"):
        out.append(f'<p class="note">{esc(s["shared_prompt_note"])}</p>')
    if s.get("prompt"):
        out.append(prompt_block(s["prompt"]))
    out.append('<div class="grid">')
    for e in s.get("experiments", []):
        out.append(render_exp(e))
    out.append('</div></section>')
    return "\n".join(out)


CSS = """
*{box-sizing:border-box} body{margin:0;background:#0b0d10;color:#e6e6e6;
 font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1200px;margin:0 auto;padding:24px}
h1{font-size:24px;margin:0 0 4px} .sub{color:#9aa4af;margin:0 0 24px}
h2{font-size:16px;letter-spacing:.5px;border-bottom:1px solid #232a31;padding-bottom:8px;margin:32px 0 12px}
section.target{background:#11161b;border:1px solid #1e6b34;border-radius:10px;padding:16px;margin-bottom:16px}
.params{display:inline-block;background:#161c22;color:#9aa4af;border-radius:6px;padding:3px 10px;font-size:12px;margin-bottom:8px}
.note{color:#b9c2cb;font-size:13px;margin:6px 0}
.err{color:#ff8f8f;font-size:13px;background:#1a1113;border:1px solid #6b1e1e;border-radius:6px;padding:8px 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}
.card{background:#11161b;border:1px solid #232a31;border-radius:10px;padding:12px}
.card.ok{border-color:#1e6b34} .card.rejected{border-color:#6b1e1e}
.chead{display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap}
.eid{font-weight:700;background:#232a31;border-radius:5px;padding:2px 8px}
.approach{flex:1;color:#cdd6df;font-size:13px}
.badge{font-size:10px;font-weight:700;letter-spacing:.5px;border-radius:5px;padding:3px 7px}
.reflabel{font-size:11px;color:#8b95a0;margin-bottom:4px;text-transform:uppercase;letter-spacing:.5px}
video{width:100%;border-radius:8px;background:#000;margin:6px 0}
.frames{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}
.frames .thumb{height:88px;border-radius:6px;border:1px solid #232a31}
section.target video{max-width:720px}
section.target .frames .thumb{height:120px}
.video-compare{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;align-items:start}
.video-compare video{max-width:none}
.video-label{font-size:11px;color:#8b95a0;text-transform:uppercase;letter-spacing:.5px;margin-top:5px}
@media(max-width:760px){.video-compare{grid-template-columns:1fr}}
.input-video-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin:6px 0 12px}
.input-video-grid video{max-width:none}
.input-image-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin:6px 0 12px}
.input-image-grid img{display:block;width:100%;height:150px;object-fit:cover;border-radius:7px;border:1px solid #232a31}
.downloads{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.downloads a{color:#9fc3ff;background:#101923;border:1px solid #2b3f63;border-radius:6px;padding:5px 9px;text-decoration:none;font-size:12px}
.downloads a:hover{background:#18263a}
.report-link{display:inline-block;margin:10px 0;padding:9px 14px;border-radius:7px;background:#f96302;color:#fff;text-decoration:none;font-weight:700}
.report-link:hover{background:#ff7b29}
details.prompt{margin-top:8px;background:#0d1216;border:1px solid #232a31;border-radius:6px;padding:6px 10px}
details.prompt summary{cursor:pointer;color:#7fb0ff;font-size:12px}
details.prompt pre{white-space:pre-wrap;color:#c8d1da;font-size:12px;margin:8px 0 0}
.hidden{display:none}
.loading-screen{padding:48px;text-align:center;color:#9aa4af}
#ims{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:8px 12px;background:#0d1216;border-bottom:1px solid #232a31;font-size:12px}
.ims-span{color:#9aa4af}
.ims-button{background:#1b2a44;color:#cfe0ff;border:1px solid #2b3f63;border-radius:6px;padding:4px 10px;font-size:12px;cursor:pointer}
.ims-button:hover{background:#25406b}
section.divider{margin:56px 0 8px;padding:22px 20px;border-radius:12px;text-align:center;
 background:linear-gradient(90deg,#141a20,#1b2630);border:1px solid #2b3f63;border-top:3px solid #f96302}
section.divider h1{border:0;margin:0;font-size:26px;color:#fff;letter-spacing:.5px}
section.divider .dsub{color:#9aa4af;font-size:13px;margin-top:6px}
.tabs{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:5px;padding:10px 0;
 background:#0b0d10;border-bottom:1px solid #232a31;margin-bottom:18px}
.tab-btn{background:#161c22;color:#9aa4af;border:1px solid #232a31;border-radius:7px;padding:6px 12px;
 font-size:12px;font-weight:600;cursor:pointer}
.tab-btn:hover{background:#1e2730;color:#cdd6df}
.tab-btn.active{background:#f96302;color:#fff;border-color:#f96302}
.tabpanel{display:none} .tabpanel.active{display:block}
"""

# Group sections into TABS: everything before the first divider = the shot-0003 experiments tab;
# each divider starts a new shot tab.
groups = []                       # (label, [sections])
cur_label, cur = "Shot 0003 — experiments", []
for s in M["sections"]:
    if s.get("kind") == "divider":
        if cur:
            groups.append((cur_label, cur))
        gid = s.get("id", "")
        num = gid[4:8] if gid.startswith("shot") and gid[4:8].isdigit() else None
        cur_label, cur = (
            f"Shot {num}" if num else s.get("tab_label", s.get("label", "Shot")[:34])
        ), [s]
    else:
        cur.append(s)
if cur:
    groups.append((cur_label, cur))
# keep tabs in VIDEO order: sort by the FIRST run of digits in the label ("Shot 1 ·", "Shot 10 ·",
# and the "000/00" lead sections stay on top).
def _tabkey(lbl):
    n = ""
    for ch in lbl:
        if ch.isdigit(): n += ch
        elif n: break
    return int(n) if n else 9999
groups.sort(key=lambda g: _tabkey(g[0]))

tabbar = ['<div class="tabs">']
panels = []
for i, (lbl, secs) in enumerate(groups):
    act = " active" if i == 0 else ""
    tabbar.append(f'<button class="tab-btn{act}" data-tab="{i}">{esc(lbl)}</button>')
    inner = []
    for s in secs:
        if secs[0].get("hide_following") and s is not secs[0]:
            continue
        k = s.get("kind")
        inner.append(render_divider(s) if k == "divider" else
                     render_target(s) if k == "target" else render_round(s))
    panels.append(f'<div class="tabpanel{act}" data-tab="{i}">' + "\n".join(inner) + "</div>")
tabbar.append("</div>")

body = ([f'<div class="wrap"><h1>{esc(M["title"])}</h1><p class="sub">{esc(M.get("subtitle",""))}</p>',
         "".join(tabbar)] + panels + ["</div>"])

# IMS auth wiring for the foundry-aws-corp.adobe.io gateway. Content stays hidden until
# imsauth.js sets the user_token cookie (path=/asset) and reveals #content. A safety timeout
# reveals it anyway if auth never completes (e.g. viewed locally), so the page is never blank.
SCRIPTS = """
<script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script>
<script src="./imsauth.js"></script>
<script>
function onAuthReady(){}
document.addEventListener("DOMContentLoaded", function(){
  try { initializeIMS(); } catch(e){}
  setTimeout(function(){
    var c=document.getElementById("content"); var l=document.getElementById("loading");
    if(c && c.classList.contains("hidden")){ c.classList.remove("hidden"); if(l) l.style.display="none"; }
  }, 9000);
});
document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll(".tab-btn").forEach(function(b){
    b.addEventListener("click", function(){
      var t=b.getAttribute("data-tab");
      document.querySelectorAll(".tab-btn").forEach(function(x){x.classList.toggle("active", x.getAttribute("data-tab")===t);});
      document.querySelectorAll(".tabpanel").forEach(function(x){x.classList.toggle("active", x.getAttribute("data-tab")===t);});
      window.scrollTo(0,0);
    });
  });
});
</script>
"""

DOC = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
       f'<meta name="viewport" content="width=device-width,initial-scale=1">'
       f'<title>{esc(M["title"])}</title><style>{CSS}</style></head><body>'
       f'<div id="ims"></div><div id="loading" class="loading-screen">Loading…</div>'
       f'<div id="content" class="hidden">'
       + "\n".join(body) + "</div>" + SCRIPTS + "</body></html>")

# Fail-loud check: every RENDERED experiment must show its prompt (section-level or its own).
# Missing prompts shipped once in round 3 — never again.
missing = []
for s in M["sections"]:
    if s.get("kind") == "target":
        continue
    has_section_prompt = bool(s.get("prompt"))
    for e in s.get("experiments", []):
        if e.get("status") == "ok" and not e.get("prompt") and not has_section_prompt:
            missing.append(f'{s["id"]}/{e["id"]}')
if missing:
    print("WARNING: rendered experiments missing a prompt:", ", ".join(missing))

open(os.path.join(HERE, "index.html"), "w").write(DOC)
print("wrote", os.path.join(HERE, "index.html"), f"({len(DOC)} bytes)")
