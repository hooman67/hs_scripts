#!/usr/bin/env python3
"""Evaluate V4.5.4.2 Gate A against labels withheld from all model requests."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'runs/dev_6_gate_a_v4_5_4_2_gpt55'
EXPECT=ROOT.parent/'v4_3_1/data/gate_6_expectations_withheld.json'
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
expect={r['record_id']:r['v4_3_1_gate_requirement'] for r in json.loads(EXPECT.read_text())['records']}
progress=json.loads((RUN/'progress.json').read_text()); rows=[]
for item in progress['records']:
    result=json.loads(Path(item['result_path']).read_text()); req=expect[item['record_id']]
    actual=set(result['derived']['owned_issue_codes']); required=set(req['issues']); forbidden=set(req['forbidden'])
    rows.append({'record_id':item['record_id'],'repeat':item['repeat'],'status':result['status'],'score_valid':result['derived']['score_valid'],'score':result['derived']['score'],'verdict':result['derived']['verdict'],'actual_issues':sorted(actual),'expected_verdict':req['verdict'],'required_issues':sorted(required),'detected_required':sorted(actual&required),'detected_forbidden':sorted(actual&forbidden),'calls':len(result['raw_calls']),'result_path':item['result_path'],'result_sha256':sha(item['result_path'])})
by=defaultdict(list)
for row in rows: by[row['record_id']].append(row)
cases=[]
for record_id,repeats in by.items():
    req=expect[record_id]; verdicts=Counter(r['verdict'] for r in repeats)
    issue_majority={issue for issue in req['issues'] if sum(issue in r['actual_issues'] for r in repeats)>=2}
    cases.append({'record_id':record_id,'repeat_verdicts':[r['verdict'] for r in repeats],'repeat_issue_sets':[r['actual_issues'] for r in repeats],'majority_verdict':verdicts.most_common(1)[0][0],'expected_verdict':req['verdict'],'required_issues':req['issues'],'majority_required_issues':sorted(issue_majority)})
required_total=sum(len(r['required_issues']) for r in rows); detected=sum(len(r['detected_required']) for r in rows)
all_scoreable=len(rows)==18 and all(r['status']=='ok' and r['score_valid'] for r in rows)
material_cases=[c for c in cases if c['expected_verdict']=='fail']
chair=next(c for c in cases if 'chair_displacement' in c['required_issues'])
clean=next(c for c in cases if c['expected_verdict']=='pass')
all_required_majority=all(set(c['required_issues'])<=set(c['majority_required_issues']) for c in cases)
criteria={
 'all_18_scoreable_or_explicit_sentinel':len(rows)==18 and all(r['status'] in {'ok','error','unassessable'} for r in rows),
 'all_18_scoreable_for_promotion':all_scoreable,
 'each_material_fail_majority_fail':all(sum(r['verdict']=='fail' for r in by[c['record_id']])>=2 for c in material_cases),
 'each_required_issue_detected_two_of_three':all_required_majority,
 'repeat_required_issue_recall_at_least_16_of_21':detected>=16 and required_total==21,
 'chair_majority_review_never_fail':sum(r['verdict']=='review' for r in by[chair['record_id']])>=2 and all(r['verdict']!='fail' for r in by[chair['record_id']]),
 'clean_pass_three_of_three_no_forbidden':all(r['verdict']=='pass' and not r['detected_forbidden'] for r in by[clean['record_id']]),
 'no_more_than_three_calls':all(r['calls']<=3 for r in rows),
}
promote=all(criteria.values())
summary={'schema_version':'hp-placement-v4.5.4.2-gate-a-diagnostic-v1','claim_boundary':'six reused labeled development cases; tuning diagnostic, not accuracy estimate','protocol_freeze_sha256':sha(ROOT/'protocol_freeze.json'),'progress_sha256':sha(RUN/'progress.json'),'criteria':criteria,'promote_to_gate_b':promote,'decision':'promote_to_frozen_gate_b' if promote else 'reject_v4_5_4_2_do_not_scale','repeat_count':len(rows),'required_issue_detected':detected,'required_issue_total':required_total,'rows':rows,'cases':cases}
(ROOT/'data/gate_a_diagnostic_v1.json').write_text(json.dumps(summary,indent=2)+'\n')
lines=['# V4.5.4.2 Gate A diagnostic','',f"**Decision: {summary['decision']}**",'',summary['claim_boundary']+'.','',f"- Required issue detections: {detected}/{required_total} repeat-level.",f"- Scoreable: {sum(r['status']=='ok' and r['score_valid'] for r in rows)}/{len(rows)}.",'','## Frozen criteria','']+[f"- {'PASS' if ok else 'FAIL'} — `{name}`" for name,ok in criteria.items()]
(ROOT/'data/gate_a_diagnostic_v1.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'decision':summary['decision'],'criteria':criteria},indent=2))
