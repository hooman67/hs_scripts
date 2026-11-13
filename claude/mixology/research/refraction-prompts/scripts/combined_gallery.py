"""Third gallery tab: joint composition and V3-derived refraction experiments."""
import json
import shutil


def render(run, project, esc, rel, figure, details):
    topic = project.parent / 'combined-composition'
    package = run / 'combined/prompt_package'
    package.mkdir(parents=True, exist_ok=True)
    for name in ['SUMMARY.md', 'cases.json', 'review_notes.json']:
        if (topic / name).exists():
            shutil.copy2(topic / name, package / name)
    for name in ['prompts', 'scripts']:
        shutil.copytree(topic / name, package / name, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__'))
    records = [json.loads(p.read_text()) for p in sorted((run/'combined/runs').glob('*/record.json'))]
    order = ['pair_staggered_left', 'trio_lineup_left', 'trio_lineup_right', 'trio_orange_front', 'five_staggered']
    records.sort(key=lambda r: (r['version'], order.index(r['case_id'])))
    note_path = topic / 'review_notes.json'
    notes = json.loads(note_path.read_text()) if note_path.exists() else {}
    content = ['''<section id="combined" role="tabpanel" aria-labelledby="combined-tab" hidden>
      <section class="notice"><h2>Combine drinks + add refractions</h2>
      <p>A single system combines source drinks and applies the V3 branching-light treatment.
      Each drink supplies its own cup geometry and transmitted color; one shared key determines every projected field.</p>
      <p class="user-prompt">Try: “Combine these drinks side by side. Add refractions.”<br>
      Optional: “Light from above and behind on camera-right.”</p>
      <p>Default: shallow near-frontal composition, white support, key behind/above at camera-left,
      floor projections toward camera-right foreground. The distant background stays clean.</p>
      <p><a href="../combined/prompt_package/prompts/system_v1.md">Combined system V1</a> ·
      <a href="../combined/prompt_package/prompts/system_v2.md">V2 direction follow-up</a> ·
      <a href="../combined/prompt_package/SUMMARY.md">Research findings</a> ·
      <a href="../combined/prompt_package/cases.json">Exact test cases</a></p>
      <p class="small">The source refraction V3 is unchanged. Supplied arrangement examples are internally generated,
      not approved customer outputs. Only customer image 027 is supplied as lighting-style evidence;
      its colors, geometry and shadow placement are not targets.</p></section>''']
    content.append(f'<section class="notice"><p>{sum(r["status"]=="complete" for r in records)} generated samples · all source and style images shown below.</p><p>{esc(notes.get("summary", "Review in progress."))}</p></section>')
    catalog = {}
    for r in records:
        folder = run/'combined/runs'/r['id']
        content.append(f'<article class="sku combined-run" id="combined-{esc(r["id"])}"><p class="eyebrow">Combined {esc(r["version"].upper())} · {esc(r["status"])}</p><h2>{esc(r["case"]["description"])}</h2>')
        content.append(f'<p class="user-prompt">User prompt: {esc(r["user_prompt"])}</p><p>Key: {esc(r["case"]["key_direction"])} → projected light: {esc(r["case"]["projection_direction"])}</p>')
        content.append('<h3>Every model input · exact order</h3><div class="grid composition-inputs" style="--input-count:'+str(len(r['input_images']))+'">')
        catalog['combined_'+r['id']] = []
        for im in r['input_images']:
            content.append(figure(im['path'], f'Image {im["image_index"]} · '+('drink source' if im['image_index']<=r['drink_count'] else 'lighting style ONLY'), im['role']))
            p = run/rel(im['path'])[3:]
            catalog['combined_'+r['id']].append(dict(n=p.name, s=p.stat().st_size, p=rel(p)[3:]))
        content.append('</div>')
        if r['status'] == 'complete':
            content.append('<div class="grid composition-output">'+figure(r['output'],'Generated group + refractions',str(r['output_dimensions']),'generated')+'</div>')
            p = folder/'output.png'
            catalog['combined_'+r['id']].append(dict(n=r['id']+' output', s=p.stat().st_size, p=rel(p)[3:]))
        example = r['case'].get('comparison_example')
        if example:
            content.append('<details><summary>Arrangement context · lighting explicitly rejected · NOT a model input</summary><div class="grid composition-output">'+figure(run/example,'Internally generated layout example · NOT customer approved',r['case']['comparison_note'],'real')+'</div></details>')
        content.append('<p class="review"><b>Visual review:</b> '+esc(notes.get('runs',{}).get(r['id'],r.get('visual_review') or 'Pending.'))+'</p>')
        if (folder/'judge.json').exists():
            critique=json.loads((folder/'judge.json').read_text())
            content.append(details('Automatic critique · advisory', json.dumps(critique, indent=2, ensure_ascii=False)))
        content.append(details('GPT system prompt · exact',r['system_prompt']))
        content.append(details('GPT-generated image-edit prompt · exact',r.get('image_prompt','Pending')))
        content.append(details('Generation settings and provenance',json.dumps({k:v for k,v in r.items() if k not in ['system_prompt','image_prompt']},indent=2,ensure_ascii=False)))
        for p in sorted(folder.glob('*_request.json')):
            content.append(details('Exact provider request · '+p.stem,p.read_text()))
        content.append('<p class="small">Provider: fal.ai · Sunburst edit + Astra vision router. Reasoning enabled; effort/backend snapshot unexposed.<br>Run records: '+' · '.join(f'<a href="{esc(rel(p))}">{esc(p.name)}</a>' for p in sorted(folder.glob('*.json')) )+'</p></article>')
    content.append('</section>')
    return '\n'.join(content), catalog
