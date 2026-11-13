#!/usr/bin/env python3
"""Evaluate an unedited V4 development run against only explicit published comments."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTATIONS = ROOT / "data/development_15_expectations.json"
V3_CONTEXT = ROOT / "astra/evidence/joined_feedback_context.json"
CLUSTERS = {
    "chair_calibration": {"chair_displacement"},
    "support_geometry_layout": {"misplaced_support_furniture", "furniture_layout_conflict", "missing_required_support", "malformed_support_furniture", "conflicting_perspective"},
    "device_position_orientation": {"unmotivated_device_position", "device_support_axis_conflict"},
    "prop_coherence": {"incoherent_prop_arrangement"},
    "artifact_scope": {"unrelated_rendering_artifact"},
}


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--run-name', required=True)
    ap.add_argument('--output-stem', required=True)
    args=ap.parse_args()
    run=ROOT/'runs'/args.run_name
    expectations=json.loads(EXPECTATIONS.read_text())
    v3={r['record_id']:r['current_final']['predicted_verdict'] for r in json.loads(V3_CONTEXT.read_text())['records']}
    rows=[]
    for expected in expectations['records']:
        ident=expected['record_id']; path=run/ident/'result.json'
        row={
            'record_id':ident,
            'human_comment_exact':expected['human_comment_exact'],
            'verdict_labeled':expected['verdict_labeled'],
            'expected_verdict':expected['explicit_verdict'],
            'expected_issue_any':expected['expected_issue_any'],
            'v3_predicted_verdict':v3.get(ident),
            'v3_verdict_match':None if not expected['verdict_labeled'] else v3.get(ident)==expected['explicit_verdict'],
        }
        if not path.is_file():
            row.update(status='missing',predicted_verdict=None,verdict_match=None,observed_issue_codes=[],issue_any_match=None)
        else:
            result=json.loads(path.read_text()); row['status']=result['status']
            row['result_path']=str(path.resolve())
            if result['status']!='ok':
                row.update(predicted_verdict=None,verdict_match=None,observed_issue_codes=[],issue_any_match=None,error=result['error'])
            else:
                observed=[]
                for check in result['assessment']['checks'].values(): observed.extend(check['issue_codes'])
                observed.extend(w['code'] for w in result['assessment']['general_artifact_warnings'])
                observed=sorted(set(observed)); predicted=result['derived']['verdict']
                row.update(
                    predicted_verdict=predicted,
                    score=result['derived']['score'],
                    verdict_match=None if not expected['verdict_labeled'] else predicted==expected['explicit_verdict'],
                    observed_issue_codes=observed,
                    issue_any_match=None if not expected['expected_issue_any'] else bool(set(expected['expected_issue_any']) & set(observed)),
                    model_returned=result['audit']['model_returned'],
                )
        rows.append(row)

    labeled=[r for r in rows if r['verdict_labeled'] and r['status']=='ok']
    issue_labeled=[r for r in rows if r['expected_issue_any'] and r['status']=='ok']
    clusters={}
    for name,codes in CLUSTERS.items():
        relevant=[r for r in issue_labeled if set(r['expected_issue_any']) & codes]
        clusters[name]={
            'cases':len(relevant),
            'detected_any_expected':sum(bool(set(r['expected_issue_any'])&set(r['observed_issue_codes'])) for r in relevant),
            'record_ids':[r['record_id'] for r in relevant],
        }
    summary={
        'run_name':args.run_name,
        'records_expected':len(rows),
        'records_ok':sum(r['status']=='ok' for r in rows),
        'records_missing_or_error':sum(r['status']!='ok' for r in rows),
        'explicit_verdict_cases_scored':len(labeled),
        'v4_verdict_matches':sum(r['verdict_match'] is True for r in labeled),
        'v4_verdict_accuracy':round(sum(r['verdict_match'] is True for r in labeled)/len(labeled),4) if labeled else None,
        'v3_verdict_matches_same_completed_cases':sum(r['v3_verdict_match'] is True for r in labeled),
        'v3_verdict_accuracy_same_completed_cases':round(sum(r['v3_verdict_match'] is True for r in labeled)/len(labeled),4) if labeled else None,
        'issue_cases_scored':len(issue_labeled),
        'issue_any_matches':sum(r['issue_any_match'] is True for r in issue_labeled),
        'prediction_distribution':dict(Counter(r['predicted_verdict'] for r in rows if r.get('predicted_verdict'))),
        'miss_clusters':clusters,
        'unlabeled_verdict_cases_excluded':expectations['unlabeled_verdict_record_ids'],
    }
    out={'schema_version':'placement-v4-development-evaluation-v1','summary':summary,'rows':rows}
    json_path=ROOT/'data'/f'{args.output_stem}.json'; md_path=ROOT/'data'/f'{args.output_stem}.md'
    json_path.write_text(json.dumps(out,indent=2)+'\n')
    lines=[f'# {args.run_name} development evaluation','',f'- Completed OK: {summary["records_ok"]} / {summary["records_expected"]}',f'- Verdict match: {summary["v4_verdict_matches"]} / {summary["explicit_verdict_cases_scored"]}',f'- V3 verdict match on the same completed labeled cases: {summary["v3_verdict_matches_same_completed_cases"]} / {summary["explicit_verdict_cases_scored"]}',f'- Expected-issue detection: {summary["issue_any_matches"]} / {summary["issue_cases_scored"]}','','Two comments without an explicit absolute verdict are excluded from verdict accuracy. Missing comments are never inferred as passes. Model outputs were not edited.','','| Record | Human verdict | V4 | Match | Expected issue(s) | Observed issue(s) |','|---|---:|---:|---:|---|---|']
    for r in rows:
        lines.append('| '+ ' | '.join((r['record_id'],str(r['expected_verdict'] or 'unlabeled'),str(r.get('predicted_verdict') or r['status']),str(r.get('verdict_match')),', '.join(r['expected_issue_any']) or 'none specified',', '.join(r.get('observed_issue_codes',[])) or 'none'))+' |')
    lines.extend(['','## Expected-issue detection by cluster',''])
    for name,value in clusters.items(): lines.append(f'- {name}: {value["detected_any_expected"]} / {value["cases"]}')
    md_path.write_text('\n'.join(lines)+'\n')
    print(json.dumps({'json':str(json_path),'markdown':str(md_path),'summary':summary},indent=2))

if __name__=='__main__': main()
