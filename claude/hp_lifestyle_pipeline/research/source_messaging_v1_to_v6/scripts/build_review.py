"""Build a text-review artifact with complete inputs, outputs, and run provenance."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fenced(value, language='json'):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    return f'\n```{language}\n{text.rstrip()}\n```\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--production', type=Path, required=True)
    parser.add_argument('--edges', type=Path, required=True)
    parser.add_argument('--validation', type=Path, required=True)
    parser.add_argument('--manual-review', type=Path, required=True)
    args = parser.parse_args()
    validation = json.loads(args.validation.read_text())
    manual = json.loads(args.manual_review.read_text())
    source_manifest = json.loads((ROOT / 'data/source_manifest.json').read_text())
    edge_manifest = json.loads((ROOT / 'data/edge_manifest.json').read_text())
    review_dir = ROOT / 'artifacts'
    review_dir.mkdir(exist_ok=True)
    records, production_rows = [], []
    for group, directory, manifest in [('Production', args.production, source_manifest), ('Synthetic', args.edges, edge_manifest)]:
        for key, source in manifest['unique_inputs'].items():
            path = directory / (key[:16] + '.json')
            record = json.loads(path.read_text())
            if not record.get('parsed_output'):
                raise RuntimeError('Incomplete case: ' + str(path))
            records.append((group, key, source, path, record))
            if group == 'Production':
                for p in record['parsed_output']['prompts']:
                    production_rows.append({'source_id': key[:16], 'source_json_path': source['input_path'], **p})
    production_count = sum(group == 'Production' for group, *_ in records)
    edge_count = len(records) - production_count
    lines = ['# GPT-5.5 environment prompt review', '',
             'As of 2026-10-14. Text review only; downstream image quality has not been evaluated.', '',
             f'{production_count} distinct production inputs produced {len(production_rows)} prompts. '
             f'{edge_count} synthetic cases are separate behavioral tests and do not add customer-SKU coverage.', '',
             f"Automated contract/traceability checks: {validation['passed']}/{validation['case_count']} cases passed. "
             'Human-readable assessments below are researcher judgments, not independent image-quality measurements.', '',
             'The prompt omits target-device references and blanket no-device clauses. Cafés and creative studios are permitted Office subsettings.', '',
             '## Contents', '', '- [Production prompts](#production-prompts)', '- [Synthetic tests](#synthetic-tests)',
             '- [Exact system prompt and schema](#exact-system-prompt-and-schema)', '', '## Production prompts', '',
             '| Source | Prompts | Environments |', '|---|---:|---|']
    for group, key, source, path, record in records:
        if group == 'Production':
            ps = record['parsed_output']['prompts']
            lines.append(f"| [{key[:16]}](#case-{key[:16]}) | {len(ps)} | {', '.join(p['environment'] for p in ps)} |")
    current_group = 'Production'
    for group, key, source, path, record in records:
        if group != current_group:
            lines.extend(['', '## Synthetic tests', '', 'These inputs were authored for testing. They are not customer source messaging.'])
            current_group = group
        label = source.get('case_name', key[:16])
        lines.extend(['', f'### Case {key[:16]}', '', f'Case label: **{label}**. Raw result: `{path}`.', '',
                      f"Requested model: `{record['settings']['model']}`; returned model: `{record['response']['model']}`; "
                      f"reasoning effort: `{record['settings']['reasoning_effort']}`; completed: `{record['completed_at']}`.", '',
                      'Source origins:'])
        for origin in source['origins']:
            suffix = f"; archive member `{origin['member']}`" if origin.get('member') else ''
            lines.append(f"- `{origin['path']}`{suffix}")
        output = record['parsed_output']
        for p in output['prompts']:
            lines.extend(['', f"**{p['id']} — {p['environment']}**", '', p['text']])
        judgment = manual['cases'].get(key[:16])
        if judgment is None:
            raise RuntimeError('Missing manual review: ' + key[:16])
        lines.extend(['', '**Text assessment:** ' + judgment['assessment'], '',
                      '**Why this count:** ' + output['debug']['count_explanation'], '',
                      '<details><summary>Complete input JSON</summary>', fenced(record['raw_input_json']), '</details>', '',
                      '<details><summary>Complete output JSON, including KSP debug mappings</summary>', fenced(output), '</details>'])
    system = (ROOT / 'system_prompt.md').read_text()
    schema = json.loads((ROOT / 'output.schema.json').read_text())
    for _, _, _, _, record in records:
        if record['system_prompt'] != system or record['schema'] != schema:
            raise RuntimeError('Run differs from canonical system prompt or schema')
    lines.extend(['', '## Exact system prompt and schema', '',
                  f'System prompt: `{ROOT / "system_prompt.md"}`. Schema: `{ROOT / "output.schema.json"}`.', '',
                  '<details><summary>Complete tested system prompt</summary>', fenced(system, 'text'), '</details>', '',
                  '<details><summary>Complete output JSON Schema</summary>', fenced(schema), '</details>', '',
                  '## Limits', '',
                  'The nine supplied inputs name four products. Synthetic Education/Gaming and robustness cases do not establish '
                  'all-nine-SKU coverage. One generation per case is a finite test, not a reliability estimate. '
                  'Hooman will evaluate downstream images before image-quality conclusions are drawn.'])
    (review_dir / 'PROMPT_REVIEW.md').write_text('\n'.join(lines) + '\n')
    (review_dir / 'generation_prompts.json').write_text(json.dumps({'prompts': production_rows}, ensure_ascii=False, indent=2) + '\n')
    (review_dir / 'production_outputs.json').write_text(json.dumps([
        {'source_id': key[:16], 'source_json_path': source['input_path'], 'output': record['parsed_output']}
        for group, key, source, path, record in records if group == 'Production'
    ], ensure_ascii=False, indent=2) + '\n')
    print('Review:', review_dir / 'PROMPT_REVIEW.md')
    print('Production prompts:', len(production_rows))


if __name__ == '__main__':
    main()
