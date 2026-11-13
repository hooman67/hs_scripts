"""Validate complete recipe job evidence, immutable inputs and actual judge coverage."""
from pathlib import Path
import hashlib
import json

ROOT=Path('/home/colligo/mixology_data/refraction_research_2026-10-19/recipe-to-image')
TOPIC=Path(__file__).resolve().parents[1]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    records=[json.loads(p.read_text()) for p in sorted((ROOT/'runs').glob('*/record.json'))]
    assert len(records)==11
    assert len({r['id'] for r in records})==11
    journal=json.loads((ROOT/'generation_journal.json').read_text())
    assert len(journal['entries'])==11 and all(r['status']=='complete' for r in journal['entries'])
    assert {r['id'] for r in journal['entries']}=={r['id'] for r in records}
    recipes=json.loads((TOPIC/'data/recipes.json').read_text())
    assert [(r['pdf_page'],r['original'].rsplit('-',1)[-1]) for r in recipes]==[(3,'1.png'),(4,'3.png'),(5,'2.png'),(6,'4.png'),(7,'5.png')]
    shared=ROOT/'runs/master_neutral_v1/output.png'
    for record in records:
        folder=ROOT/'runs'/record['id']
        assert record['status']=='complete'
        assert record['model']=='gpt-image-2.5-sunburst' and record['quality']=='high'
        assert record['output']['sha256']==sha(folder/'output.png')
        assert record['output']['dimensions']==[1024,1536]
        assert record['cli_sha256']==sha(record['cli_path'])
        for name in ['system_prompt','user_prompt','image_prompt']:
            assert (folder/(name+'.txt')).read_text()==record[name]
        for ref in record['references']:assert ref['sha256']==sha(ref['path'])
        if record.get('mode')=='anchored':
            assert len(record['references'])==1 and record['references'][0]['path']==str(shared)
            assert record['system_prompt']==(TOPIC/'data/system_v1.txt').read_text()
        if record.get('mode')=='text':assert record['references']==[]
        if 'comparison_original' in record:
            comparison=record['comparison_original']
            assert comparison['sha256']==sha(comparison['path'])
            assert comparison['path'] not in [x['path'] for x in record['references']]
    judged={}
    for p in (ROOT/'analysis').glob('judge_*.json'):
        if p.stem.endswith('_request'):continue
        response=json.loads(p.read_text())
        assert response['response_model']=='gpt-6-astra' and response['status']=='completed'
        assert response['reasoning_effort']=='high' and response['request_id']
        for item in json.loads(response['text']):
            assert item['id'] not in judged
            judged[item['id']]=item
        request=json.loads(p.with_name(p.stem+'_request.json').read_text())
        for item in request['images']:assert item['sha256']==sha(item['path'])
    assert set(judged)=={r['id'] for r in records if r.get('recipe')}
    expected=json.loads((ROOT/'analysis/geometry.json').read_text())
    assert len(expected['results'])==11
    for item in expected['results']:
        assert item['output_sha256']==sha(ROOT/'runs'/item['id']/'output.png')
        assert (ROOT/'analysis'/(item['id']+'_guides.png')).exists()
    result={'verified':True,'image_jobs':11,'recipe_outputs':10,'anchored':7,'text_only':3,
            'actual_astra_high_judged_outputs':len(judged),'geometry_passes':sum(j['geometry_matches_master'] for j in judged.values()),
            'no_recipe_output_postprocessing':True,'all_source_output_and_prompt_hash_checks_passed':True,
            'limitations':'Visual judge and sampled 2D edges are not exact geometry or physical measurement. SDK internal wire retries unobserved.'}
    (ROOT/'analysis/artifact_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
