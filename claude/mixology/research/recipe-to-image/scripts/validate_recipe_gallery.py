"""Browser checks for recipe tab plus preservation/navigation of all live topics."""
import functools
import hashlib
import json
from pathlib import Path
import threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

RUN=Path('/home/colligo/mixology_data/refraction_research_2026-10-19')
REVIEW=RUN/'_review/recipe_publication_2026-10-20'
TEMPLATE=Path('/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/gallery')


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass


def main():
    assert (RUN/'gallery/imsauth.js').read_bytes()==(TEMPLATE/'imsauth.js').read_bytes()
    baseline=json.loads((REVIEW/'before_manifest.json').read_text())
    old_outputs=[r for r in baseline if r['path'].endswith('/output.png')]
    for row in old_outputs:assert hashlib.sha256((RUN/row['path']).read_bytes()).hexdigest()==row['sha256']
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(RUN)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1600,'height':1100})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.route('https://auth-stg1.services.adobe.com/imslib/imslib.js',lambda route:route.fulfill(
            content_type='application/javascript',body='''window.adobeImsFactory={createIMSLib:(c,k)=>{
            window[k]={initialize(){c.onReady({});},isSignedInUser(){return false;},signIn(){},signOut(){}};}};'''))
        page.goto(f'http://127.0.0.1:{server.server_port}/gallery/index.html#recipe-to-image',wait_until='networkidle')
        page.wait_for_selector('#content:not(.hidden)')
        page.wait_for_selector('#recipe-to-image:not([hidden])')
        page.locator('img[loading]').evaluate_all("es=>es.forEach(e=>e.loading='eager')")
        page.wait_for_function("Array.from(document.querySelectorAll('img[src]')).every(i=>i.complete&&i.naturalWidth>0)")
        links=page.locator('[href],[src]').evaluate_all("es=>es.flatMap(e=>[e.getAttribute('href'),e.getAttribute('src')]).filter(x=>x&&x.startsWith('.'))")
        for link in links:assert (RUN/'gallery'/link).resolve().is_file(),link
        assert page.locator('.recipe-run').count()==11
        panels=page.locator('[role=tabpanel]').evaluate_all('es=>es.map(e=>e.id)')
        assert {'refractions','composition','combined','composition-corrected-inputs','recipe-to-image'}<=set(panels)
        tabs=page.locator('[role=tab]').evaluate_all("es=>es.map(e=>e.getAttribute('aria-controls'))")
        assert len(set(tabs))==len(tabs) and set(tabs)==set(panels)
        for i,tab in enumerate(tabs):
            page.locator('#'+tab+'-tab').click()
            assert page.locator('#'+tab).is_visible()
            assert page.locator('[role=tabpanel]:not([hidden])').count()==1
            page.locator('#'+tab+'-tab').focus();page.keyboard.press('ArrowRight')
            assert page.locator('#'+tabs[(i+1)%len(tabs)]).is_visible()
        for record_path in sorted((RUN/'recipe-to-image/runs').glob('*/record.json')):
            record=json.loads(record_path.read_text());rid='recipe-'+record['id']
            page.evaluate('(id)=>location.hash=id',rid)
            page.wait_for_selector('#recipe-to-image:not([hidden])')
            article=page.locator('#'+rid)
            assert record['user_prompt'] in article.inner_text()
            system=article.locator('details').filter(has=page.locator('summary',has_text='System prompt · exact'))
            system.locator('summary').click()
            assert system.locator('pre').inner_text()==record['system_prompt']
            assert article.locator('.generated img').count()==1
        first=page.locator('#recipe-v1_anchored_fresh_breeze_1')
        first.locator('.generated .zoom').click();assert page.locator('#lightbox').is_visible()
        page.keyboard.press('Escape');assert page.locator('#lightbox').is_hidden()
        page.evaluate("location.hash='recipe-to-image'")
        page.wait_for_timeout(100)
        page.screenshot(path=str(REVIEW/'desktop.png'))
        page.set_viewport_size({'width':390,'height':844})
        for tab in tabs:
            page.locator('#'+tab+'-tab').click()
            assert not page.evaluate('document.documentElement.scrollWidth>window.innerWidth+1'),tab
        page.locator('#recipe-to-image-tab').click()
        first.scroll_into_view_if_needed();page.screenshot(path=str(REVIEW/'mobile.png'))
        assert not errors,errors
        result={'verified':True,'recipe_run_articles':11,'tabs':tabs,'prior_outputs_hash_preserved':len(old_outputs),
                'images_loaded':page.locator('img[src]').count(),'relative_links_checked':len(links),
                'keyboard_tabs_deep_links_prompts_lightbox_mobile':'pass','javascript_errors':errors,
                'IMS':'byte-identical; mocked only inside local browser test','live_gateway_browser':'not verified'}
        browser.close()
    server.shutdown()
    (REVIEW/'browser_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
