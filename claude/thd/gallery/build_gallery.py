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
    if s.get("note"):
        out.append(f'<p class="note">{esc(s["note"])}</p>')
    if s.get("video"):
        out.append(f'<video controls preload="metadata" src="{esc(s["video"])}"></video>')
    if s.get("frames"):
        out.append(f'<div class="frames">{imgs(s["frames"])}</div>')
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
    return f'<section class="divider"><h1>{esc(s["label"])}</h1>{sub}</section>'


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
"""

body = [f'<div class="wrap"><h1>{esc(M["title"])}</h1><p class="sub">{esc(M.get("subtitle",""))}</p>']
for s in M["sections"]:
    k = s.get("kind")
    body.append(render_divider(s) if k == "divider" else
                render_target(s) if k == "target" else render_round(s))
body.append("</div>")

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
