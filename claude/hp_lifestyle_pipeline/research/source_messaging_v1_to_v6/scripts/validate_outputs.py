"""Audit saved model results against the output contract and original source data.

These checks establish structure and traceability, not image quality or full prose quality.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def field(source, path):
    value = source
    for key in path.split('.'):
        if not isinstance(value, dict) or key not in value:
            raise KeyError(path)
        value = value[key]
    return value


def audit(record, schema):
    failures, observations = [], []
    output = record.get('parsed_output')
    if output is None:
        return {'failures': ['No parsed output'], 'observations': []}
    failures.extend(error.message for error in jsonschema.Draft202012Validator(schema).iter_errors(output))
    if failures:
        return {'failures': failures, 'observations': []}
    source = json.loads(record['raw_input_json'])
    source = source if isinstance(source, dict) else {}
    prompts, debug = output['prompts'], output['debug']
    ids = [p['id'] for p in prompts]
    if ids != [f'p{i}' for i in range(1, len(ids) + 1)]:
        failures.append('Prompt IDs are not sequential and unique')
    ksps = [k for k in source if re.fullmatch(r'KSP\d+', k)]
    mapped = [m['ksp_id'] for m in debug['ksp_mappings']]
    if sorted(mapped) != sorted(ksps):
        failures.append('KSP mappings do not cover exactly the input KSPs')
    eligible = sum(m['eligible_for_additional_prompt'] for m in debug['ksp_mappings'])
    if not 1 <= len(prompts) <= max(1, eligible):
        failures.append('Output count exceeds the declared useful-KSP limit')
    for mapping in debug['ksp_mappings'] + [debug['value_proposition']]:
        if not set(mapping['prompt_ids']).issubset(ids):
            failures.append('Mapping cites a nonexistent prompt')
        owner = mapping.get('ksp_id', 'ValueProposition')
        for evidence in mapping['source_evidence']:
            path, quote = evidence['path'], evidence['quote']
            try:
                value = field(source, path)
            except KeyError:
                failures.append('Nonexistent evidence path: ' + path)
                continue
            if not (path == owner or path.startswith(owner + '.')):
                failures.append('Evidence belongs to a different message: ' + path)
            if not isinstance(value, str) or not quote or quote not in value:
                failures.append('Evidence is not a verbatim source substring: ' + path)
    if sorted(x['prompt_id'] for x in debug['creative_additions']) != sorted(ids):
        failures.append('Creative additions do not cover exactly the prompts')
    for ignored in debug['ignored_fields']:
        try:
            field(source, ignored)
        except KeyError:
            failures.append('Ignored-field list cites an absent field: ' + ignored)
    if '_chatSession' in source and '_chatSession' not in debug['ignored_fields']:
        failures.append('Upstream metadata is not listed as ignored')
    for p in prompts:
        text = p['text']
        forbidden = re.findall(r'\b(?:laptops?|printers?|computers?|monitors?|devices?|hardware|screens?|EliteBook|LaserJet|Intel|SKU)\b|\bHP\b|NOTEBOOK-|DESKTOP-|PRINT-', text, re.I)
        if forbidden:
            failures.append(p['id'] + ' contains device wording: ' + ', '.join(forbidden))
        if re.search(r'no (?:additional )?(?:hardware|devices)|blue carrier|\d+\s*(?:%|mm)|depth of field|photorealistic|rendering|digital twin', text, re.I):
            failures.append(p['id'] + ' contains excluded instruction/style language')
        count = len(re.findall(r"\b[\w’-]+\b", text))
        observations.append({'prompt_id': p['id'], 'words': count, 'environment': p['environment']})
    if not record['response']['model'].startswith('gpt-5.5'):
        failures.append('Unexpected response model')
    return {'failures': failures, 'observations': observations,
            'prompt_count': len(prompts), 'declared_eligible_ksps': eligible,
            'used_fallback': debug['used_fallback']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directories', nargs='+', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    schema = json.loads((ROOT / 'output.schema.json').read_text())
    results = []
    for directory in args.directories:
        for path in sorted(directory.glob('*.json')):
            if path.name.endswith('.pending.json'):
                continue
            record = json.loads(path.read_text())
            results.append({'path': str(path), **audit(record, schema)})
    report = {'cases': results, 'case_count': len(results),
              'passed': sum(not r['failures'] for r in results),
              'prompt_count': sum(r.get('prompt_count', 0) for r in results)}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return int(any(r['failures'] for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
