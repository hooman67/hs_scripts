#!/usr/bin/env python3
from datetime import datetime, timezone
import json
from run_verifier import FREEZE_PATH, atomic_json, current_freeze, sha256

if FREEZE_PATH.exists(): raise SystemExit("freeze.json already exists")
value={**current_freeze(),"frozen_at_utc":datetime.now(timezone.utc).isoformat()}
atomic_json(FREEZE_PATH,value)
print(json.dumps({"freeze":str(FREEZE_PATH),"sha256":sha256(FREEZE_PATH)},indent=2))
