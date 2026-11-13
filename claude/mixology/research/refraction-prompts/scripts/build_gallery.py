"""Build the complete, append-only-in-content Foundry research gallery from run records."""
from __future__ import annotations
import html
import json
import shutil
import sys
from pathlib import Path
from composition_gallery import render as render_composition, TAB_CSS, TAB_JS
from combined_gallery import render as render_combined
from corrected_composition_gallery import render as render_corrected_composition

PROJECT=Path('/home/colligo/hs_scripts/claude/mixology/research/refraction-prompts')
RUN=Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
TEMPLATE=Path('/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/gallery')
BUCKET='foundry-tccc-enterprise-adobe-assets'
PREFIX='mixology/refraction_research_2026-10-19'
sys.path.insert(0,str(PROJECT.parent/'recipe-to-image/scripts'))
from recipe_gallery import render as render_recipe
sys.path.insert(0,str(PROJECT.parent/'multi-cup-refractions/scripts'))
from multi_cup_gallery import render as render_multi_cup


def esc(x):return html.escape(str(x))
def rel(path):return '../'+str(Path(path).resolve().relative_to(RUN.resolve()))
def details(title,text,opened=False):
    return f'<details{" open" if opened else ""}><summary>{esc(title)}</summary><pre>{esc(text)}</pre></details>'
def figure(path,title,note='',css='input'):
    uri=rel(path)
    return f'<figure class="{css}"><a href="{esc(uri)}" class="zoom" data-caption="{esc(title)}"><img loading="lazy" src="{esc(uri)}" alt="{esc(title)}"></a><figcaption><b>{esc(title)}</b><span>{esc(note)}</span><a class="file-link" href="{esc(uri)}" target="_blank">Open original</a></figcaption></figure>'


def main():
    notes=json.loads((PROJECT/'review_notes.json').read_text())
    records=[json.loads(p.read_text()) for p in sorted((RUN/'runs').glob('*/record.json'))]
    order=list(notes['versions'])
    records.sort(key=lambda r:(order.index(r['version']) if r['version'] in order else 99,r['case_id']))
    gallery=RUN/'gallery';gallery.mkdir(exist_ok=True)
    package=RUN/'prompt_package';package.mkdir(exist_ok=True)
    for name in ['USAGE.md','SUMMARY.md','preset.json','cases.json','review_notes.json']:
        shutil.copy2(PROJECT/name,package/name)
    shutil.copytree(PROJECT/'prompts',package/'prompts',dirs_exist_ok=True)
    shutil.copytree(PROJECT/'scripts',package/'scripts',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
    for name in ['run_fal_experiments.py','fal_transport.py']:
        source=PROJECT.parent/'model-access/scripts'/name
        if source.exists():shutil.copy2(source,package/'scripts'/name)
    # Exact known-working IMS implementation required by the skill.
    shutil.copy2(TEMPLATE/'imsauth.js',gallery/'imsauth.js')
    base_css=(TEMPLATE/'style.css').read_text()
    extra_css='''
    .controls{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0;align-items:center}.controls select,.controls button{background:#1b202a;color:#f1f4f8;border:1px solid #596478;padding:9px 12px;border-radius:7px}.run{scroll-margin-top:100px}.run h2{font-size:25px}.run .grid{margin-top:15px}.run .grid img{height:410px}.file-link{display:inline!important;background:transparent!important;color:#9dceff;font-size:12px}.user-prompt{font-size:19px;background:#102a23;border:1px solid #387764;padding:13px 17px;border-radius:8px}.review{border-left:3px solid #ffcb70;padding-left:14px;color:#d8dde5}.tag{display:inline-block;border:1px solid #576279;border-radius:6px;padding:3px 8px;margin:4px;font-size:12px}.reference-library .grid img{height:240px}.recommended{border-color:#54d88a}.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.95);z-index:200;display:flex;align-items:center;justify-content:center}.lightbox[hidden]{display:none}.lightbox img{max-width:96vw;max-height:91vh;object-fit:contain}.lightbox button{position:absolute;right:20px;top:16px;background:#222;color:white;border:1px solid #888;font-size:25px;padding:5px 15px}.lightbox p{position:absolute;bottom:0;background:#111;padding:6px 15px}.run[hidden]{display:none}table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid #303846;text-align:left;padding:9px}a{color:#9dceff}.small{font-size:13px;color:#a9b3c1}.grid.four{grid-template-columns:repeat(4,minmax(0,1fr))}@media(max-width:1100px){.grid.four{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:720px){.grid.four{grid-template-columns:1fr}}
    .controls label{display:grid;gap:4px;max-width:100%;min-width:0}.controls select{max-width:100%;min-width:0}#ims{flex-wrap:wrap}@media(max-width:720px){.controls{align-items:stretch}.controls label{width:100%}.jump{position:static}.run .grid img{height:auto;max-height:500px}.sku,.notice,.method{padding:16px}pre{word-break:break-word}}
    '''
    recipe_css='\n#recipe-to-image summary,.recipe-run .eyebrow{overflow-wrap:anywhere}\n.mcr-run summary,.mcr-run .eyebrow{overflow-wrap:anywhere}\n'
    (gallery/'style.css').write_text(base_css+extra_css+TAB_CSS+recipe_css)
    variants=''.join(f'<option value="{esc(k)}">{esc(v)}</option>' for k,v in notes['versions'].items())
    cases={r['case_id']:r['case']['label'] for r in records}
    case_options=''.join(f'<option value="{esc(k)}">{esc(v)}</option>' for k,v in cases.items())
    body=[f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mixology — Refraction Prompt Lab</title><link rel="stylesheet" href="./style.css"></head><body>
    <div id="ims"></div><div id="loading" class="loading-screen">Signing in to view the Mixology research gallery…</div><main id="content" class="hidden">
    <header><p class="eyebrow">MIXOLOGY · REFERENCE → LIGHTING EDIT · 19 OCTOBER 2026</p><h1>Refraction Prompt Lab</h1><p class="sub">A minimal user request, a reusable system prompt, and every experiment kept for review.</p>
    <div class="stats"><span>{sum(r['status']=='complete' for r in records)} refraction outputs</span><span>{len(cases)} input cases</span><span>GPT-6 Astra → GPT Image 2.5 Sunburst</span><span>High quality · full prompts and inputs</span></div></header>
    <div class="research-tabs" role="tablist" aria-label="Research topic"><button id="refractions-tab" role="tab" aria-selected="true" aria-controls="refractions">Refractions</button><button id="composition-tab" role="tab" aria-selected="false" aria-controls="composition" tabindex="-1">Group composition</button><button id="composition-corrected-inputs-tab" role="tab" aria-selected="false" aria-controls="composition-corrected-inputs" tabindex="-1">Group composition corrected inputs</button><button id="combined-tab" role="tab" aria-selected="false" aria-controls="combined" tabindex="-1">Composition + refractions</button><button id="recipe-to-image-tab" role="tab" aria-selected="false" aria-controls="recipe-to-image" tabindex="-1">Recipe → image</button><button id="multi-cup-refractions-tab" role="tab" aria-selected="false" aria-controls="multi-cup-refractions" tabindex="-1">multi-cup-refractions</button></div><section id="refractions" role="tabpanel" aria-labelledby="refractions-tab">
    <section class="notice"><h2>V3 · new drinks and corrected-input review</h2><p>{esc(notes['summary'])}</p><p>Automatic critiques and agent assessments are shown separately. Customer examples are references, not newly generated outputs.</p><p>Earlier corrected-input results: <a href="#v3corrected_overhead_clean">Corrected overhead</a> · <a href="#v3corrected_group_clean">Corrected group</a>. Previous results remain below for comparison: <a href="#v3_overhead">old V3 overhead</a> · <a href="#v3_group">old V3 group</a>.</p><p>Reusable files: <a href="../prompt_package/prompts/system_v3.md">System prompt V3</a> · <a href="../prompt_package/preset.json">Preset configuration</a> · <a href="../prompt_package/USAGE.md">How to use</a> · <a href="../prompt_package/SUMMARY.md">Research findings</a></p></section>
    <nav class="jump"><a href="#experiments">Experiments</a><a href="#inputs">Corrected inputs</a><a href="#reference-library">Customer examples</a><a href="#source-doc">PDF context</a><a href="#method">Method & limits</a></nav>
    <section id="experiments"><h3>Refraction experiments · exact input shown per run</h3><div class="controls"><label>Iteration <select id="versionFilter"><option value="all">All iterations</option>{variants}</select></label><label>Case <select id="caseFilter"><option value="all">All cases</option>{case_options}</select></label><button id="expandPrompts">Expand all prompts</button><span id="visibleCount"></span></div>''']
    catalog={}
    for r in records:
        rid=r['id'];folder=RUN/'runs'/rid
        judge=json.loads((folder/'judge.json').read_text()) if (folder/'judge.json').exists() else None
        recommended=rid==notes.get('recommended_run')
        body.append(f'<article class="sku run{" recommended" if recommended else ""}" id="{esc(rid)}" data-version="{esc(r["version"])}" data-case="{esc(r["case_id"])}"><div class="sku-head"><div><p class="eyebrow">{esc(notes["versions"].get(r["version"],r["version"]))}</p><h2>{esc(r["case"]["label"])}</h2><p class="small">Run {esc(rid)} · {esc(r["status"])}</p></div><span class="badge">{"Recommended for review" if recommended else "Research sample"}</span></div>')
        body.append(f'<p class="user-prompt">User prompt: {esc(r["user_prompt"])}</p>')
        if r.get('provider')=='fal.ai':
            body.append(f'<p class="small provider-note">Provider: fal.ai · {esc(r["fal_endpoint"])}. Astra via OpenRouter; reasoning enabled, effort not exposed. Requested models are unchanged; backend snapshot identity is not returned. Separate provider batch, not a controlled prompt-only comparison.</p>')
        if r['case_id'] in ['overhead','group']:
            old_number='012' if r['case_id']=='overhead' else '023'
            body.append(f'<p class="review"><b>Historical input warning:</b> Hooman rejected image {old_number} as too cropped. This result is retained pending review; see the <a href="#v3corrected_{r["case_id"]}_clean">corrected-input V3 rerun</a>.</p>')
        body.append('<div class="grid three">')
        target=r['input_images'][0]
        body.append(figure(target['path'],'Input 1 · edit target','Sent to Astra and Sunburst' if r['rewriter_model'] else 'Sent directly to Sunburst'))
        if r['status']=='complete':
            body.append(figure(r['output'],'Generated output',f'{r["output_dimensions"][0]} × {r["output_dimensions"][1]} · {r["image_seconds"]} s','generated'))
        else: body.append(f'<figure><figcaption><b>Generation {esc(r["status"])}</b><p>{esc(r.get("error_type","In progress"))}</p></figcaption></figure>')
        body.append(figure(RUN/'assets'/r['case']['positive'],'Customer lighting comparison',r['case']['pair_status'],'real'))
        body.append('</div>')
        if len(r['input_images'])>1:
            body.append('<h3>Additional model inputs · preset lighting style</h3><div class="grid two">')
            for n,im in enumerate(r['input_images'][1:],start=2):
                body.append(figure(im['path'],f'Input {n} · {im["role"]}','Sent to BOTH Astra and Sunburst. Target identity remains Image 1.','inspired'))
            body.append('</div>')
        else:body.append('<p class="small">No lighting-style image was sent to the generator in this run. The customer comparison above was used for evaluation only.</p>')
        body.append(f'<p class="review"><b>Agent visual review:</b> {esc(r.get("visual_review") or notes["runs"].get(rid,"Visual review pending."))}</p>')
        if judge:
            body.append('<p>Automatic critic: '+''.join(f'<span class="tag">{esc(label)} {esc(judge.get(key,"?"))}/5</span>' for key,label in [('refraction_score','Refraction'),('identity_score','Identity'),('composition_score','Composition'),('coherent_light_score','Light coherence')])+'</p>')
            body.append(details('Automatic critique · advisory',json.dumps({k:v for k,v in judge.items() if k!='_meta'},indent=2)))
            critic_meta=dict(judge.get('_meta',{}))
            critic_paths=[Path(r['input_images'][0]['path']),folder/'output.png',RUN/'assets'/r['case']['positive'],RUN/'assets'/'image_015_p06_xref590.jpg']
            if r['case_id']=='single':critic_paths.append(RUN/'assets'/'image_027_p10_xref1385.jpg')
            critic_meta['ordered_image_paths_reconstructed_from_harness']=[str(p) for p in critic_paths]
            body.append(details('Critic inputs and instructions',json.dumps(critic_meta,indent=2)))
        body.append(details('GPT system prompt · exact',r.get('system_prompt','Pending')))
        body.append(details('GPT-generated image-edit prompt · exact' if r['rewriter_model'] else 'Customer baseline image prompt · exact',r.get('image_prompt','Pending')))
        body.append(details('Generation settings and provenance',json.dumps({k:v for k,v in r.items() if k not in ['system_prompt','image_prompt']},indent=2)))
        if r.get('provider')=='fal.ai':
            for p in sorted(folder.glob('*_request.json')):
                body.append(details('Exact provider request · '+p.stem,p.read_text()))
            body.append('<p class="small">Provider queue/result records: '+ ' · '.join(f'<a href="{esc(rel(p))}">{esc(p.name)}</a>' for p in sorted(folder.glob('*.json')) if p.name!='record.json')+'</p>')
        body.append('</article>')
        catalog[rid]=[{'n':Path(im['path']).name,'s':Path(im['path']).stat().st_size,'p':rel(im['path'])[3:]} for im in r['input_images']]
        if r['status']=='complete':catalog[rid].append({'n':rid+' output','s':Path(r['output']).stat().st_size,'p':rel(r['output'])[3:]})
    new_cases={key:value for key,value in json.loads((PROJECT/'cases.json').read_text()).items() if key.startswith('new_')}
    if new_cases:
        new_done=sum(r['case_id'] in new_cases and r['status']=='complete' for r in records)
        body.append(f'</section><section class="sku" id="new-reference-inputs"><h2>New finished-drink inputs · frozen V3</h2><p>Five inputs selected; empty cup and white cap excluded. {new_done} completed new-drink results are shown in the experiments above. The fal batch retains V3; the original Foundry route awaits cluster allowlisting.</p><div class="grid five">')
        for key,case in new_cases.items():body.append(figure(RUN/'assets'/case['input'],case['label'],'Prepared for Add refractions. · unchanged system V3'))
        body.append('</div>')
    body.append('</section><section id="inputs" class="sku"><h2>Corrected inputs</h2><div class="grid two">')
    catalog['corrected_inputs']=[]
    for name,label,source_id in [('overhead_013_clean.png','Overhead input','013'),('group_027_clean.png','Group input','027')]:
        path=RUN/'assets'/name
        if path.exists():
            body.append(figure(path,label,f'Corrected reference derived from customer {source_id}; used in the new V3 run.'))
            catalog['corrected_inputs'].append({'n':name,'s':path.stat().st_size,'p':'assets/'+name})
    body.append('</div></section><section id="reference-library" class="sku reference-library"><h2>Customer example library</h2><p class="section-note">All 13 curated images. User-provided preferences take precedence over automatic critique. An unpaired image is style evidence; its unknown source is not fabricated.</p><div class="grid four">')
    labels={2:'Approved cola output · exact input uncertain',3:'Approved berry output · originates from right drink in 018',12:'Overhead input → 013',13:'Approved overhead output from 012',14:'Single dragonfruit input → rejected 015',15:'Rejected output · vein-like light',18:'Two-drink parent image',23:'Strongest group input → 027',24:'Additional curated style example · no explicit rating',25:'Additional curated style example · no explicit rating',26:'Additional curated style example · no explicit rating',27:'Strongest approved group output',29:'Approved separated group output · input unknown'}
    labels[12]='Historical input · rejected for its crop';labels[23]='Historical group input · rejected for its crop'
    for path in sorted((RUN/'assets').glob('image_*.jpg')):
        number=int(path.name.split('_')[1]);body.append(figure(path,f'Image {number:03d}',labels.get(number,'Additional reference'),'real'))
    body.append('</div></section><section class="sku" id="source-doc"><h2>Source PDF context</h2><p class="section-note">Page 4 describes base drinks and camera variations. Page 5 describes refraction. Page 6 includes later restrained-light instructions; the user’s explicit preference for branching light overrides contradictory constraints there.</p><div class="grid two">')
    for n in [4,5,6,10]:body.append(figure(RUN/'pdf_context'/f'page_{n:02d}.png',f'Customer PDF · page {n}','Rendered page for context','real'))
    body.append('</div>'+details('Exact extracted page-5 image prompt',(RUN/'pdf_context'/'customer_page5_prompt.txt').read_text())+'</section>')
    body.append('<section class="method" id="method"><h2>Method & limits</h2><ul>'+''.join('<li>'+esc(s)+'</li>' for s in notes['limitations'])+'</ul><p>Every refraction run starts from its displayed input. Corrected-input V3 runs use the new clean reference assets; historical runs keep their original inputs. All style references and exact prompts are shown.</p></section></section>')
    composition_html,composition_catalog=render_composition(RUN,PROJECT,esc,rel,figure,details)
    body.append(composition_html);catalog.update(composition_catalog)
    corrected_html,corrected_catalog=render_corrected_composition(RUN,PROJECT,esc,rel,figure,details)
    body.append(corrected_html);catalog.update(corrected_catalog)
    combined_html,combined_catalog=render_combined(RUN,PROJECT,esc,rel,figure,details)
    body.append(combined_html);catalog.update(combined_catalog)
    recipe_html,recipe_catalog=render_recipe(RUN,PROJECT,esc,rel,figure,details)
    body.append(recipe_html);catalog.update(recipe_catalog)
    multi_cup_html,multi_cup_catalog=render_multi_cup(RUN,PROJECT,esc,rel,figure,details)
    body.append(multi_cup_html+'</main>');catalog.update(multi_cup_catalog)
    body.append('''<div class="lightbox" id="lightbox" hidden><button id="closeLightbox" aria-label="Close">×</button><img id="largeImage" alt=""><p id="largeCaption"></p></div><script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script><script src="./imsauth.js"></script><script src="./data.js"></script><script src="./main.js"></script><script>document.addEventListener("DOMContentLoaded",()=>initializeIMS());</script></body></html>''')
    (gallery/'index.html').write_text('\n'.join(body))
    (gallery/'data.js').write_text('const GALLERY_DATA = '+json.dumps(catalog,ensure_ascii=False)+';\n')
    (gallery/'main.js').write_text('''function onAuthReady(){filterRuns();followResearchHash();}
function filterRuns(){const v=document.getElementById('versionFilter').value,c=document.getElementById('caseFilter').value;let n=0;document.querySelectorAll('.run').forEach(r=>{r.hidden=!((v==='all'||r.dataset.version===v)&&(c==='all'||r.dataset.case===c));if(!r.hidden)n++;});document.getElementById('visibleCount').textContent=n+' runs shown';}
document.getElementById('versionFilter').addEventListener('change',filterRuns);document.getElementById('caseFilter').addEventListener('change',filterRuns);
document.getElementById('expandPrompts').addEventListener('click',e=>{const open=e.target.textContent.startsWith('Expand');document.querySelectorAll('.run:not([hidden]) details').forEach(d=>{if(d.querySelector('summary').textContent.includes('prompt'))d.open=open;});e.target.textContent=open?'Collapse all prompts':'Expand all prompts';});
const box=document.getElementById('lightbox');function closeBox(){box.hidden=true;document.body.style.overflow='';}
document.querySelectorAll('a.zoom').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();document.getElementById('largeImage').src=a.href;document.getElementById('largeCaption').textContent=a.dataset.caption;box.hidden=false;document.body.style.overflow='hidden';}));document.getElementById('closeLightbox').addEventListener('click',closeBox);box.addEventListener('click',e=>{if(e.target===box)closeBox();});document.addEventListener('keydown',e=>{if(e.key==='Escape')closeBox();});
'''+TAB_JS)
    print(json.dumps({'runs':len(records),'complete':sum(r['status']=='complete' for r in records),'html':str(gallery/'index.html'),'url':f'https://foundry-aws-corp.adobe.io/asset/{BUCKET}/{PREFIX}/gallery/index.html'}))


if __name__=='__main__':main()
