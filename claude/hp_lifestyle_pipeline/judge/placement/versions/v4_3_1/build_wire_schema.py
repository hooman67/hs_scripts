#!/usr/bin/env python3
"""Build compact Direct OpenAI wire schema; local schema remains authoritative."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parent
def transform(v:Any)->Any:
    if isinstance(v,dict): return {k:transform(x) for k,x in v.items() if k not in {"$schema","$id","title","uniqueItems","minLength","pattern"}}
    if isinstance(v,list): return [transform(x) for x in v]
    return v
def enum_count(v:Any)->int:
    if isinstance(v,dict): return (len(v.get('enum',[])) if isinstance(v.get('enum'),list) else 0)+sum(enum_count(x) for x in v.values())
    if isinstance(v,list): return sum(enum_count(x) for x in v)
    return 0
def main():
    wire=transform(json.loads((ROOT/'assessment_schema.json').read_text())); count=enum_count(wire)
    if count>=1000: raise RuntimeError(count)
    (ROOT/'wire_schema.json').write_text(json.dumps(wire,indent=2)+'\n'); print('wire enums',count,'bytes',(ROOT/'wire_schema.json').stat().st_size)
if __name__=='__main__': main()
