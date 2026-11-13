"""Attach canonical direct reviews and validate the bounded combined batch."""
import hashlib
import json
from pathlib import Path

ROOT = Path('/home/colligo/hs_scripts/claude/mixology/research/combined-composition')
RUN = Path('/home/colligo/mixology_data/refraction_research_2026-10-19')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    notes = json.loads((ROOT/'review_notes.json').read_text())
    results = []
    paths = sorted((RUN/'combined/runs').glob('*/record.json'))
    assert len(paths) == 7
    for p in paths:
        record = json.loads(p.read_text())
        assert record['status'] == 'complete'
        assert record['id'] in notes['runs']
        assert digest(Path(record['output'])) == record['output_sha256']
        for im in record['input_images']:
            assert digest(Path(im['path'])) == im['sha256']
        payload = json.loads((p.parent/'image_request.json').read_text())['payload']
        assert payload['prompt'] == record['image_prompt']
        assert [i['sha256'] for i in payload['image_urls']] == [i['sha256'] for i in record['input_images']]
        assert record['system_prompt'] == (ROOT/'prompts'/f'system_{record["system_version"]}.md').read_text()
        critique = json.loads((p.parent/'judge.json').read_text())
        record['visual_review'] = notes['runs'][record['id']]
        p.write_text(json.dumps(record, indent=2, ensure_ascii=False)+'\n')
        results.append(dict(id=record['id'], inputs=len(record['input_images']),
            drink_count=record['drink_count'], output_sha256=record['output_sha256'],
            dimensions=record['output_dimensions'], system_sha256=hashlib.sha256(record['system_prompt'].encode()).hexdigest(),
            advisory_scores={key:value for key,value in critique.items() if key.endswith('_score')},
            visual_review=record['visual_review']))
    result = dict(status='verified', outputs=len(results), all_input_output_hashes_match=True,
                  all_provider_prompts_and_image_order_match=True, all_direct_reviews_present=True,
                  all_advisory_critiques_present=True, files=results)
    (RUN/'_review/combined_execution_validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='files'}))


if __name__ == '__main__':
    main()
