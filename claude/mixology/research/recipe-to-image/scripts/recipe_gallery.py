"""Recipe tab renderer, called by the shared gallery builder under publication lock."""
import json
import shutil


def render(run, project, esc, rel, figure, details):
    topic=project.parent/'recipe-to-image'
    root=run/'recipe-to-image'
    package=root/'prompt_package'
    package.mkdir(exist_ok=True)
    shutil.copy2(topic/'SUMMARY.md',package/'SUMMARY.md')
    for name in ['data','scripts']:
        shutil.copytree(topic/name,package/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
    records=[json.loads(p.read_text()) for p in sorted((root/'runs').glob('*/record.json'))]
    metrics=json.loads((root/'analysis/geometry.json').read_text())
    measures={r['id']:r for r in metrics['results']}
    recipes=json.loads((topic/'data/recipes.json').read_text())
    content=['''<section id="recipe-to-image" role="tabpanel" aria-labelledby="recipe-to-image-tab" hidden>
      <section class="notice"><h2>Recipe → consistent individual drink</h2>
      <p class="user-prompt">User supplies a recipe. The system supplies one fixed cup/camera master and house appearance conventions.</p>
      <p>The shared-master samples preserve cup framing much more closely than the text-only controls in this small test.
      These are raw generated images: no shape warping, masking, compositing or resizing was applied to the recipe outputs.
      Approximate edge agreement is not a guarantee of exact 3D geometry or future repeatability.</p>
      <p><a href="../recipe-to-image/prompt_package/data/system_v1.txt">System V1</a> ·
      <a href="../recipe-to-image/prompt_package/data/recipes.json">Five recipes + appearance conventions</a> ·
      <a href="../recipe-to-image/prompt_package/SUMMARY.md">Findings and usage</a> ·
      <a href="../recipe-to-image/analysis/geometry.json">Reproducible edge measurements</a> ·
      <a href="../recipe-to-image/sources/TCCC_Crafted_Norway_Pilot_Recipe_Book_260703.pdf">Customer recipe PDF</a></p>
      <p class="small">Model: direct Foundry-vended GPT Image 2.5 Sunburst · high · 1024×1536.
      All reference-conditioned runs use the same neutral master derived once from the amber original.
      No individual target-drink photograph is sent for that recipe. The amber test is consequently not held out.
      Recipe quantities are from the PDF; color layering conventions are separately inferred from its photographs.</p></section>''']
    content.append('<section class="sku"><h2>Five recipes · one shared cup</h2><div class="grid composition-inputs" style="--input-count:5">')
    for recipe in recipes:
        path=root/'runs'/f'v1_anchored_{recipe["id"]}_1/output.png'
        if path.exists():content.append(figure(path,recipe['name'],'Raw shared-master result','generated'))
    content.append('</div></section>')
    content.append('<section class="sku"><h2>Controlled comparison · text alone versus shared master</h2><p>Same system, recipe and appearance convention. Only reference conditioning changes; generate versus edit endpoints also differ. No statistical reliability claim.</p>')
    for recipe_id in ['velvet_cherry','fresh_breeze','sunset_breeze']:
        recipe=next(r for r in recipes if r['id']==recipe_id)
        content.append('<h3>'+esc(recipe['name'])+'</h3><div class="grid three">')
        content.append(figure(run/'assets/ref_input_originals'/recipe['original'],'Supplied clean appearance comparison','NOT sent to the generator for this recipe','real'))
        for mode,label in [('text','Text-only control'),('anchored','Shared master')]:
            rid=f'v1_{mode}_{recipe_id}_1';value=measures[rid]['max_sampled_edge_displacement_px']
            content.append(figure(root/'runs'/rid/'output.png',label,f'Max sampled edge shift from master: {value} px','generated'))
        content.append('</div>')
    content.append('</section>')
    content.append('<section class="sku"><h2>Geometry check</h2><p>Six fixed-height edge samples, with no alignment or scaling. Blue guides mark the neutral master; pink points mark each output. These threshold-based samples can be affected by highlights and droplets and do not fully measure rim tilt, baseline or 3D pose.</p><div class="grid composition-output">'+figure(root/'analysis/geometry_contact.jpg','All sampled-edge overlays','Diagnostic only; full-size overlays linked per run')+'</div>'+details('Measurement method and limitations',json.dumps(metrics,indent=2))+'</section>')
    catalog={}
    # Recipe outputs precede one-time master preparation; every input remains inspectable.
    records.sort(key=lambda r:(r['id']=='master_neutral_v1',r['id']))
    for r in records:
        folder=root/'runs'/r['id'];rid=r['id']
        title=r.get('recipe',{}).get('name','One-time neutral master preparation')
        content.append(f'<article class="sku recipe-run" id="recipe-{esc(rid)}"><p class="eyebrow">{esc(rid)} · {esc(r["status"])}</p><h2>{esc(title)}</h2>')
        content.append('<p class="user-prompt">User prompt: '+esc(r.get('user_prompt') or 'Internal master preparation; no runtime recipe')+'</p>')
        content.append('<div class="grid three">')
        for i,im in enumerate(r['references'],1):content.append(figure(im['path'],f'Model input {i}',im['role']))
        if not r['references']:content.append('<figure><figcaption><b>No image inputs</b><p>Recipe, shared textual cup specification and house appearance convention only.</p></figcaption></figure>')
        if r['status']=='complete':content.append(figure(r['output']['path'],'Raw generated output',str(r['output']['dimensions']),'generated'))
        if 'comparison_original' in r:content.append(figure(r['comparison_original']['path'],'Supplied clean comparison','Evaluation only; not this run’s generation input','real'))
        content.append('</div>')
        if 'recipe' in r:
            content.append('<p><b>House appearance convention:</b> '+esc(r['recipe']['appearance_policy'])+'</p>')
            page=root/'sources'/f'page_{r["recipe"]["pdf_page"]:02d}.png'
            content.append('<details><summary>Original recipe page · quantities verified visually</summary><div class="grid composition-output">'+figure(page,'Recipe PDF page '+str(r['recipe']['pdf_page']),'Context/evaluation only; not a generation input')+'</div></details>')
        if rid in measures:
            content.append(details('Geometry measurements',json.dumps(measures[rid],indent=2)))
            content.append('<p><a href="'+esc(rel(root/'analysis'/(rid+'_guides.png')))+'">Full-size edge overlay</a></p>')
        content.append(details('System prompt · exact',r['system_prompt']))
        content.append(details('Compiled image prompt · exact',r['image_prompt']))
        content.append(details('Settings, inputs and provenance',json.dumps({k:v for k,v in r.items() if k not in ['system_prompt','image_prompt']},indent=2,ensure_ascii=False)))
        content.append('<p class="small">The Image API has one prompt field: the system contract and recipe are compiled into that prompt. No separate image-model system role or stochastic prompt rewriter is claimed.</p></article>')
        paths=[im['path'] for im in r['references']]+([r['output']['path']] if r['status']=='complete' else [])
        catalog['recipe_'+rid]=[{'n':str(p).split('/')[-1],'s':(run/rel(p)[3:]).stat().st_size,'p':rel(p)[3:]} for p in paths]
    content.append('<section class="sku"><h2>Advisory Astra-high evaluation · exact inputs retained</h2><p>Actual model and response metadata are saved. Evaluations are not blinded: run IDs contain the method. These do not replace direct inspection or geometric checks.</p>')
    for p in sorted((root/'analysis').glob('judge_*.json')):
        content.append(details(p.name,p.read_text()))
    content.append('</section></section>')
    return '\n'.join(content),catalog
