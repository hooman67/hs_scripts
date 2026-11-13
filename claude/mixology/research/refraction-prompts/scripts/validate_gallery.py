"""Local browser validation; IMS is mocked ONLY in the test browser route."""
from __future__ import annotations
import functools
import hashlib
import json
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

RUN=Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
TEMPLATE=Path('/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/gallery')
SOURCE_NAMES = ['315fb11e7cc94ecf8103ee2cf98227ae.png', '6b61ea2d3b3f46959c6a0403879f8299.png',
                'b82dd27cd8c4471ea84aa21f9878e980.png', 'edbf33f823b842df9cd34393caea6cca.png',
                'TCCC–Crafted-Sept-2026.png']

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def main():
    assert (RUN/'gallery/imsauth.js').read_bytes()==(TEMPLATE/'imsauth.js').read_bytes()
    records=[json.loads(p.read_text()) for p in (RUN/'runs').glob('*/record.json')]
    html=(RUN/'gallery/index.html').read_text()
    data=(RUN/'gallery/data.js').read_text()
    for forbidden in ['id="input-cleanup"','href="#input-cleanup"','input_cleanup/','raw_sunburst','source_preservation_mask']:
        assert forbidden not in html+data,forbidden
    old=json.loads((RUN/'_review/before_new_inputs_manifest.json').read_text())
    old_outputs=[f for f in old['files'] if f['path'].startswith('runs/') and f['path'].endswith('/output.png')]
    assert len(old_outputs)==14
    for f in old_outputs:assert hashlib.sha256((RUN/f['path']).read_bytes()).hexdigest()==f['sha256']
    baseline_path = RUN/'_review/combined_prepublication_2026-10-20/manifest.json'
    preexisting = [item for item in json.loads(baseline_path.read_text()) if item['path'].endswith('/output.png')]
    replacements = json.loads((RUN/'_review/composition_orange_source_replacement_2026-10-20.json').read_text())
    archived = replacements['archive']['mapping']
    assert replacements['archive']['verified']
    assert len(archived) == 8
    for item in preexisting:
        old_path = RUN/item['path']
        rid = old_path.parent.name
        preserved_path = Path(archived[rid]['archive_path'])/'output.png' if rid in archived else old_path
        assert hashlib.sha256(preserved_path.read_bytes()).hexdigest() == item['sha256'], item['path']
        if rid in archived:
            assert hashlib.sha256(old_path.read_bytes()).hexdigest() != item['sha256']
    for rid in ['v3corrected_overhead_clean','v3corrected_group_clean']:
        assert any(r['id']==rid for r in records)
        r=next(r for r in records if r['id']==rid)
        assert hashlib.sha256(r['system_prompt'].encode()).hexdigest()=='652fd8895c132e7cf6d311052f55a823dbe7ea09b749077a32d82faa6948eb9e'
        assert r['user_prompt']=='Add refractions.'
    for r in records:
        assert r['status']=='complete', r['id']
        for im in r['input_images']:
            assert hashlib.sha256(Path(im['path']).read_bytes()).hexdigest()==im['sha256']
        assert hashlib.sha256(Path(r['output']).read_bytes()).hexdigest()==r['output_sha256']
        assert (Path(r['output']).parent/'judge.json').exists()
    composition=[json.loads(p.read_text()) for p in (RUN/'composition/runs').glob('*/record.json')]
    composition=[r for r in composition if r['id'] not in ['v1_side_by_side','v1_staggered']]
    assert len(composition)>=2
    for r in composition:
        source_indices = r['case'].get('input_indices', [1, 2, 3, 4, 5])
        assert len(source_indices) == len(set(source_indices))
        assert all(type(index) is int and 1 <= index <= 5 for index in source_indices)
        assert len(r['input_images']) == len(source_indices)
        for index, (im, source_index) in enumerate(zip(r['input_images'], source_indices), 1):
            assert hashlib.sha256(Path(im['path']).read_bytes()).hexdigest()==im['sha256']
            assert Path(im['path']).name not in ['white_cap.png','empty_cup.png']
            assert im['image_index'] == index
            assert Path(im['path']).name == SOURCE_NAMES[source_index - 1]
        if r['case'].get('comparison_example'):
            example = RUN/r['case']['comparison_example']
            original = Path('/home/colligo/mixology_data/source_restored_2026-10-19/multi_cup_examples/generated_examples')/example.name
            assert example.read_bytes() == original.read_bytes()
            assert str(example) not in [im['path'] for im in r['input_images']]
        if r['status']=='prepared':
            assert not Path(r['output']).exists()
            assert r['image_prompt'] is None and r['output_sha256'] is None
        elif r['status']=='complete':
            assert hashlib.sha256(Path(r['output']).read_bytes()).hexdigest()==r['output_sha256']
            assert r['visual_review']
            assert (Path(r['output']).parent/'judge.json').exists()
        if r['version'] == 'v1small':
            assert r['status'] == 'complete' and len(r['input_images']) in (2, 3)
            assert hashlib.sha256(r['system_prompt'].encode()).hexdigest() == '5dc097c24838b83cdd8bb6de26f6ab73a76c3a1c0a5b1f17a614a8ffd303d68a'
    combined=[json.loads(p.read_text()) for p in (RUN/'combined/runs').glob('*/record.json')]
    assert len(combined)==7
    for r in combined:
        assert r['status']=='complete'
        assert len(r['input_images'])==r['drink_count']+1
        assert 'STYLE ONLY' in r['input_images'][-1]['role']
        assert Path(r['input_images'][-1]['path']).name=='image_027_p10_xref1385.jpg'
        folder=Path(r['output']).parent
        assert (folder/'judge.json').exists()
        for im in r['input_images']:
            assert hashlib.sha256(Path(im['path']).read_bytes()).hexdigest()==im['sha256']
        assert hashlib.sha256(Path(r['output']).read_bytes()).hexdigest()==r['output_sha256']
        payload=json.loads((folder/'image_request.json').read_text())['payload']
        assert payload['prompt']==r['image_prompt']
        assert [im['sha256'] for im in payload['image_urls']]==[im['sha256'] for im in r['input_images']]
    for r in records+composition+combined:
        assert all(im['sha256']!=replacements['old_source']['sha256'] for im in r['input_images'])
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(RUN)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    result={'completed_runs':len(records),'input_output_hashes':'all match','ims_template':'byte-identical',
            'authentication_test':'IMS mocked in local browser only; live signed-in gateway not exercised'}
    with sync_playwright() as p:
        browser=p.chromium.launch(args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1600,'height':1100},device_scale_factor=1)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.route('https://auth-stg1.services.adobe.com/imslib/imslib.js',lambda route:route.fulfill(
            content_type='application/javascript',body='''window.adobeImsFactory={createIMSLib:(c,k)=>{
            window[k]={initialize(){c.onReady({});},isSignedInUser(){return false;},signIn(){},signOut(){}};}};'''))
        url=f'http://127.0.0.1:{server.server_port}/gallery/index.html'
        page.goto(url,wait_until='networkidle')
        page.wait_for_selector('#content:not(.hidden)')
        page.locator('img[loading]').evaluate_all("es=>es.forEach(e=>e.loading='eager')")
        page.wait_for_function("Array.from(document.querySelectorAll('img[src]')).every(i=>i.complete && i.naturalWidth>0)")
        assert page.locator('.run:not([hidden])').count()==len(records)
        assert page.locator('.run').first.get_attribute('data-version')==('v3fal' if any(r['version']=='v3fal' for r in records) else 'v3corrected')
        assert page.locator('#inputs img').count()==2
        result['loaded_images']=page.locator('img[src]').count()
        # Check every relative link, including downloadable prompt-package files.
        links=page.locator('[href],[src]').evaluate_all("es=>es.flatMap(e=>[e.getAttribute('href'),e.getAttribute('src')]).filter(x=>x&&x.startsWith('.'))")
        for link in links: assert (RUN/'gallery'/link).resolve().is_file(),link
        result['relative_links_checked']=len(links)
        assert page.locator('#new-reference-inputs img').count()==5
        page.click('#composition-tab')
        assert page.locator('#composition').is_visible()
        assert page.locator('#refractions').is_hidden()
        assert page.locator('.composition-run').count()==len(composition)
        assert page.locator('#composition img').count()==sum(len(r['input_images'])+(r['status']=='complete')*(1+bool(r['case'].get('comparison_example'))) for r in composition)
        small = [r for r in composition if r['version'] == 'v1small']
        if small:
            assert len(small) == 5
            assert page.locator('.composition-run').first.get_attribute('id') == 'composition-v1small_pair_lineup'
            for r in small:
                section = page.locator('#composition-' + r['id'])
                assert section.locator('.composition-inputs img').count() == len(r['input_images'])
                assert section.locator('.composition-comparison img').count() == 2
                assert 'NOT a model input' in section.locator('.composition-comparison').inner_text()
                page.evaluate('(id)=>location.hash=id', 'composition-' + r['id'])
                page.wait_for_selector('#composition:not([hidden])')
            section = page.locator('#composition-v1small_pair_lineup')
            section.locator('details').first.locator('summary').click()
            assert section.locator('details').first.get_attribute('open') is not None
            section.locator('.composition-comparison a.zoom').last.click()
            assert page.locator('#lightbox').is_visible()
            page.keyboard.press('Escape')
            assert page.locator('#lightbox').is_hidden()
            result['small_group_inputs_comparisons_prompts_lightbox'] = 'pass'
        page.locator('#composition-tab').focus()
        page.keyboard.press('ArrowLeft')
        assert page.locator('#refractions').is_visible()
        assert page.locator('#refractions-tab').get_attribute('aria-selected')=='true'
        page.evaluate("location.hash='composition-v1fal_staggered'")
        page.wait_for_selector('#composition:not([hidden])')
        page.click('#combined-tab')
        assert page.locator('#combined').is_visible()
        assert page.locator('#composition').is_hidden()
        assert page.locator('.combined-run').count()==7
        for r in combined:
            section=page.locator('#combined-'+r['id'])
            assert section.locator('.composition-inputs img').count()==len(r['input_images'])
            assert r['user_prompt'] in section.inner_text()
        page.evaluate("location.hash='combined-v1_trio_lineup_right'")
        page.wait_for_selector('#combined:not([hidden])')
        section=page.locator('#combined-v1_trio_lineup_right')
        section.locator('details').first.locator('summary').click()
        section.locator('.generated a.zoom').click()
        assert page.locator('#lightbox').is_visible()
        page.keyboard.press('Escape')
        page.locator('#combined-tab').focus()
        ordered_tabs=page.locator('[role="tab"]').evaluate_all("es=>es.map(e=>e.getAttribute('aria-controls'))")
        page.keyboard.press('ArrowLeft')
        assert page.locator('#'+ordered_tabs[ordered_tabs.index('combined')-1]).is_visible()
        result['combined_inputs_prompts_lightbox_tabs']='pass'
        page.evaluate("location.hash='v3corrected_group_clean'")
        page.wait_for_selector('#refractions:not([hidden])')
        result['tabs_and_deep_links']='pass'
        result['composition_prepared_cases']=sum(r['status']=='prepared' for r in composition)
        page.select_option('#versionFilter','v3corrected')
        assert page.locator('.run:not([hidden])').count()==2
        page.select_option('#caseFilter','group_clean')
        assert page.locator('.run:not([hidden])').count()==1
        page.select_option('#caseFilter','overhead_clean')
        assert page.locator('.run:not([hidden])').count()==1
        page.select_option('#caseFilter','all')
        page.select_option('#versionFilter','v3')
        assert page.locator('.run:not([hidden])').count()==3
        page.select_option('#caseFilter','overhead')
        assert page.locator('.run:not([hidden])').count()==1
        page.click('#expandPrompts')
        assert page.locator('#v3_overhead details[open]').count()==2
        page.locator('#v3_overhead a.zoom').first.click()
        assert page.locator('#lightbox').is_visible()
        page.keyboard.press('Escape')
        assert page.locator('#lightbox').is_hidden()
        review=RUN/'_review';review.mkdir(exist_ok=True)
        page.select_option('#versionFilter','v3corrected')
        page.select_option('#caseFilter','all')
        page.locator('#v3corrected_group_clean').scroll_into_view_if_needed()
        page.screenshot(path=str(review/'gallery_desktop.png'))
        page.click('#composition-tab')
        page.locator('#composition-v1fal_side_by_side' if any(r['id']=='v1fal_side_by_side' for r in composition) else '#composition-v1_side_by_side').scroll_into_view_if_needed()
        page.screenshot(path=str(review/'gallery_composition_desktop.png'))
        if small:
            page.locator('#composition-v1small_trio_orange_front .composition-comparison').screenshot(path=str(review/'gallery_small_groups_comparison.png'))
        page.set_viewport_size({'width':390,'height':844})
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(review/'gallery_mobile.png'))
        overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1')
        assert not overflow,'Horizontal mobile overflow'
        if small:
            for r in small:
                section = page.locator('#composition-' + r['id'])
                section.scroll_into_view_if_needed()
                assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1'),r['id']
                assert section.locator('.composition-inputs').evaluate("e=>getComputedStyle(e).gridTemplateColumns.split(' ').length") == 1
            page.locator('#composition-v1small_pair_lineup .composition-comparison .generated').screenshot(path=str(review/'gallery_small_groups_mobile.png'))
        page.click('#refractions-tab')
        assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1'),'Refraction mobile overflow'
        page.click('#combined-tab')
        assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1'),'Combined mobile overflow'
        page.locator('#combined-v1_trio_lineup_right .generated').screenshot(path=str(review/'gallery_combined_mobile.png'))
        page.set_viewport_size({'width':1600,'height':1100})
        page.locator('#combined-v1_trio_lineup_right .generated').screenshot(path=str(review/'gallery_combined_direction.png'))
        assert not errors,errors
        result.update(filters='pass',prompt_expansion='pass',lightbox='pass',mobile_overflow=False,javascript_errors=errors,old_outputs_preserved=14,cleanup_narrative_removed=True,system_v3_unchanged=True)
        result.update(preexisting_outputs_unchanged=len(preexisting)-len(archived),archived_original_outputs_verified=len(archived),replacement_outputs=len(archived),combined_completed=len(combined), composition_completed=sum(r['status']=='complete' for r in composition),small_group_runs=len(small))
        browser.close()
    server.shutdown()
    (RUN/'_review/gallery_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
