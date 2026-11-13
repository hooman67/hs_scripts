#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
paths=['PROVENANCE.md','system_prompt.md','build_schema.py','assessment_schema.json','build_wire_schema.py','wire_schema.json','result_schema.json','scoring.py','crop.py','anchor_selection.py','anchors/anchor_catalog.json','run_judge.py','preflight_gate.py','data/gate_6_preflight.json','data/canary_input.json','data/canary_manifest.json','test_v4_3.py','run_canary_tmux.sh']
doc={'schema_version':'hp-placement-v4.3-canary-freeze-v1','created_at':datetime.now(timezone.utc).isoformat(),'status':'frozen_before_canary','purpose':'one-case GPT-5.5 transport and valid-structured-output canary; not a quality estimate','model':{'requested':'gpt-5.5','route':'foundry_direct_openai','reasoning_effort':'high','max_completion_tokens':24000,'sdk_retries':0,'application_total_attempts_max':2,'timeout_seconds':600,'concurrency':1},'runtime':{'python':'3.12','foundry_aws_gateway':'>=2.0.0','jsonschema':'4.25.1','pillow':'12.0.0','opencv':'4.10.0.84'},'files':{p:sha(ROOT/p) for p in paths},'anchor_assets':{str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'anchors/assets').glob('*'))}}
out=ROOT/'data/protocol_freeze_canary_v1.json'; out.write_text(json.dumps(doc,indent=2)+'\n'); print(out,sha(out))
