"""Render the separate composition tab without presenting prepared cases as outputs."""
import json
import shutil


def render(run, project, esc, rel, figure, details):
    topic = project.parent / 'group-composition'
    package = run / 'composition/prompt_package'
    package.mkdir(parents=True, exist_ok=True)
    for name in ['SUMMARY.md', 'cases.json']:
        if (topic / name).exists():
            shutil.copy2(topic / name, package / name)
    for name in ['prompts', 'scripts', 'data']:
        if (topic / name).exists():
            shutil.copytree(topic / name, package / name, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__'))
    records = [json.loads(p.read_text()) for p in sorted((run / 'composition/runs').glob('*/record.json'))]
    # Old unexecuted plans reference the now-rejected orange input; retain on disk only.
    records = [r for r in records if r['id'] not in ['v1_side_by_side', 'v1_staggered']]
    small_order = ['pair_lineup', 'pair_staggered', 'trio_lineup', 'trio_orange_front', 'trio_amber_front']
    records.sort(key=lambda r: (r['status'] != 'complete', r.get('version') != 'v1small',
                               small_order.index(r['case_id']) if r.get('version') == 'v1small' else 99,
                               r['id']))
    for name in ['run_fal_experiments.py','fal_transport.py']:
        source=project.parent/'model-access/scripts'/name
        if source.exists():shutil.copy2(source,package/'scripts'/name)
    completed = sum(r['status'] == 'complete' for r in records)
    content = [f'''<section id="composition" role="tabpanel" aria-labelledby="composition-tab" hidden>
      <section class="notice"><h2>Group composition · proportions first</h2>
      <p>Combine multiple reference drinks without adding refractions. Preserve each cup’s own proportions,
      molded base, rim, contents and topping; the user chooses the arrangement.</p>
      <p>{completed} generated outputs · {len(records) - completed} prepared or incomplete cases.</p>
      <p><a href="../composition/prompt_package/prompts/system_v1.md">Composition system V1</a> ·
      <a href="../composition/prompt_package/prompts/system_v2.md">V2 targeted comparison</a> ·
      <a href="../composition/prompt_package/SUMMARY.md">Research findings and status</a> ·
      <a href="../composition/prompt_package/data/source_geometry.json">Source geometry estimates</a></p>
      <p class="small">Source cups have slightly different silhouettes. Scale is assessed from cup bodies,
      not cream height. Manual pixel-ratio estimates are not physical measurements or a fidelity guarantee.</p></section>''']
    content.append('<section class="notice"><p><b>Updated upright orange input:</b> Seven affected group outputs were replaced using the new reference. Prior versions are preserved in a recovery archive outside this gallery.</p><p>Supplied arrangement examples are internally generated, <b>NOT customer-approved output</b> and NOT model inputs. They show drink selection and spatial slots only. Their refractions and cup-shape errors are not targets.</p><p><b>Working interpretation:</b> V1 remains the simpler starting prompt. Recognizable drink identity does not establish exact cup geometry; shape differences and occlusion limits remain. Automatic scores are advisory.</p></section>')
    catalog = {}
    for record in records:
        rid = record['id']
        done = record['status'] == 'complete'
        folder = run / 'composition/runs' / rid
        content.append(f'<article class="sku composition-run" id="composition-{esc(rid)}" data-status="{esc(record["status"])}">')
        content.append(f'<p class="eyebrow">Composition {esc(record["version"].upper())} · {esc(record["status"])}</p>')
        content.append(f'<h2>{esc(record.get("case", {}).get("description", record["case_id"]))}</h2>')
        content.append(f'<p class="user-prompt">User prompt: {esc(record["user_prompt"])}</p>')
        if record.get('provider')=='fal.ai':
            content.append(f'<p class="small provider-note">Provider: fal.ai · {esc(record["fal_endpoint"])}. Exact requested Astra/Sunburst model family; backend snapshot identity is not returned. Astra reasoning is enabled; effort is not exposed.</p>')
        if not done:
            content.append('<p class="review"><b>Original Foundry-route plan — not executed.</b> Retained for provenance. Completed fal-provider experiments, if available, appear above. This plan is not a generated result.</p>')
        content.append(f'<h3>All model inputs · ordered · {len(record["input_images"])} drinks</h3><div class="grid composition-inputs" style="--input-count:{len(record["input_images"])}">')
        catalog['composition_' + rid] = []
        for index, item in enumerate(record['input_images'], 1):
            content.append(figure(item['path'], f'Input {index}', item['role']))
            path = run / rel(item['path'])[3:]
            catalog['composition_' + rid].append({'n': path.name, 's': path.stat().st_size, 'p': rel(path)[3:]})
        content.append('</div>')
        if done:
            example = record.get('case', {}).get('comparison_example')
            output_class = 'composition-comparison' if example else 'composition-output'
            content.append(f'<div class="grid {output_class}">')
            if example:
                example_path = run / example
                content.append(figure(example_path, 'Internally generated arrangement · NOT customer approved · NOT a model input',
                               json.loads((topic/'cases.json').read_text()).get(record['case_id'],{}).get('comparison_note',record['case'].get('comparison_note','Comparison only.')), 'real'))
                catalog['composition_' + rid].append({'n': example_path.name,
                    's': example_path.stat().st_size, 'p': rel(example_path)[3:]})
            content.append(figure(record['output'], 'Generated group · composition only',
                           str(record['output_dimensions']), 'generated') + '</div>')
            path = run / rel(record['output'])[3:]
            catalog['composition_' + rid].append({'n': rid + ' output', 's': path.stat().st_size, 'p': rel(path)[3:]})
        if record.get('visual_review'):
            content.append('<p class="review"><b>Visual review:</b> ' + esc(record['visual_review']) + '</p>')
        for filename in ['judge.json', 'geometry_review.json', 'review.json']:
            if (folder / filename).exists():
                content.append(details(filename, (folder / filename).read_text()))
        content.append(details('GPT system prompt · exact', record['system_prompt']))
        if record.get('replacement', {}).get('manual_prompt_correction'):
            content.append(details('Factual correction applied to Astra prompt before generation',json.dumps(record['replacement']['manual_prompt_correction'],indent=2)))
        prompt_label = ('Image-edit prompt actually sent · factual correction recorded above'
                        if record.get('replacement', {}).get('manual_prompt_correction')
                        else 'GPT-generated image-edit prompt · exact' if record.get('image_prompt') else 'Image-edit prompt · awaiting Astra')
        content.append(details(prompt_label, record.get('image_prompt') or 'Not generated: no Astra call has completed.'))
        content.append(details('Settings and provenance', json.dumps({k: v for k, v in record.items()
                        if k not in ['system_prompt', 'image_prompt']}, indent=2)))
        if record.get('provider')=='fal.ai':
            for path in sorted(folder.glob('*_request.json')):
                content.append(details('Exact provider request · '+path.stem,path.read_text()))
            content.append('<p class="small">Provider queue/result records: '+ ' · '.join(f'<a href="{esc(rel(path))}">{esc(path.name)}</a>' for path in sorted(folder.glob('*.json')) if path.name!='record.json')+'</p>')
        content.append('</article>')
    content.append('</section>')
    return '\n'.join(content), catalog


TAB_CSS = '''
.research-tabs{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}
.research-tabs button{font-size:17px;background:#171d28;color:#dce6f4;border:1px solid #586c83;border-radius:8px;padding:13px 20px;cursor:pointer}
.research-tabs button[aria-selected="true"]{background:#183a4d;border-color:#8bddff;color:#fff}
[role="tabpanel"][hidden]{display:none}
.grid.five{grid-template-columns:repeat(5,minmax(0,1fr))}
.grid.five img{height:310px;object-fit:contain}.composition-run{scroll-margin-top:70px}
.composition-output{grid-template-columns:minmax(0,1fr)}.composition-output img{height:auto;max-height:900px;object-fit:contain}
.composition-inputs{grid-template-columns:repeat(var(--input-count),minmax(0,1fr))}
.composition-inputs img{height:310px;object-fit:contain}
.composition-comparison{grid-template-columns:repeat(2,minmax(0,1fr))}
.composition-comparison img{height:520px;object-fit:contain}
@media(max-width:1100px){.grid.five{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(min-width:721px) and (max-width:1100px){.composition-inputs{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:720px){.grid.five{grid-template-columns:1fr}.grid.five img{height:370px}}
@media(max-width:720px){.composition-inputs,.composition-comparison{grid-template-columns:1fr}.composition-inputs img{height:370px}.composition-comparison img{height:auto;max-height:520px}}
'''

TAB_JS = '''
function setResearchTab(id){
 document.querySelectorAll('[role="tabpanel"]').forEach(p=>p.hidden=p.id!==id);
 document.querySelectorAll('[role="tab"]').forEach(b=>{const active=b.getAttribute('aria-controls')===id;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;});
}
function followResearchHash(){
 const raw=decodeURIComponent(location.hash.slice(1)),target=document.getElementById(raw);
 const panel=target&&target.closest('[role="tabpanel"]');
 if(panel){setResearchTab(panel.id);if(target.classList.contains('run')){document.getElementById('versionFilter').value='all';document.getElementById('caseFilter').value='all';filterRuns();}requestAnimationFrame(()=>target.scrollIntoView());}
}
document.querySelectorAll('[role="tab"]').forEach((b,index,buttons)=>{
 b.addEventListener('click',()=>{const id=b.getAttribute('aria-controls');setResearchTab(id);history.replaceState(null,'','#'+id);});
 b.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(index+1)%buttons.length;else if(e.key==='ArrowLeft')next=(index+buttons.length-1)%buttons.length;else if(e.key==='Home')next=0;else if(e.key==='End')next=buttons.length-1;else return;e.preventDefault();buttons[next].click();buttons[next].focus();});
});
window.addEventListener('hashchange',followResearchHash);followResearchHash();
'''
