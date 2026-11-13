#!/usr/bin/env python3
"""Validate the V6.1 all-160 report before publication."""
from __future__ import annotations
import hashlib, json, re, shutil, subprocess
from collections import Counter, defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent; BUILT=HERE/"built"
FORBIDDEN_LABELS=("comparison","v5","gemini","rewrite","generated preview","generated-preview")

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    analysis=json.loads((BUILT/"downloads/analysis.json").read_text()); rows=analysis["rows"]
    assert analysis["scope"]=={"prompt_rows":160,"banks":16,"prompts_per_bank":10,"ctech_reference_count":18}
    assert len(rows)==160 and len({r["prompt_key"] for r in rows})==160
    banks=defaultdict(list)
    for r in rows: banks[(r["device_id"],r["camera_tag"])].append(r)
    assert len(banks)==16 and all(len(v)==10 for v in banks.values())
    assert all(sorted(r["bank_rank"] for r in v)==list(range(1,11)) for v in banks.values())
    assert all(0<=r["measured_ctech_similarity"]<=1 for r in rows)
    assert len(analysis["references"])==18 and all("map_x" in r and "map_y" in r for r in analysis["references"])
    audit=analysis["prop_audit"]
    assert audit["scope"]=={"prompt_rows":160,"banks":16,"prompts_per_bank":10,"images_available":False,"downstream_text_available":False}
    approved={x["prop_id"] for x in audit["approved_props"]}
    assert all(pid in approved for r in rows for pid in r["prop_ids"])
    assert audit["headline"]["approved_prop_assignments"]==sum(len(r["prop_ids"]) for r in rows)
    assert len(audit["bank_family_compliance"])==16 and all(x["passed"] for x in audit["bank_family_compliance"])
    assert len(audit["semantic_phrase_family_compliance"])==16 and all(x["passed"] for x in audit["semantic_phrase_family_compliance"])
    assert all(x["explicitly_populated"] and not x["empty_wording"] and x["content_families"] for x in audit["populated_shelving_pegboard"])
    printer=audit["printer_environment_support_desk"]
    assert len(printer)==80 and all(x["source_environment_supported"] and x["credible_support_surface"] and not x["implausible_surface"] for x in printer)
    catalog=analysis["approved_prop_catalog"]
    assert catalog["entry_count"]==len(catalog["entries"])==261
    assert catalog["visual_family_count"]==len(catalog["visual_families"])==158
    assert len({x["id"] for x in catalog["entries"]})==261
    assert sum(catalog["environment_counts"].values())==261
    assert sum(catalog["role_counts"].values())==261
    assert all(x["repetition_groups"] and x["aliases"] for x in catalog["entries"])
    raw=json.loads((BUILT/"downloads/v6_1_prompts_all_160.json").read_text())
    assert raw["prompts"] and len(raw["prompts"])==160
    forbidden_field=re.compile(r"(?:^|_)(?:image|images|rewrite|rewritten|generated_preview)(?:$|_)",re.I)
    assert not any(forbidden_field.search(k) for r in raw["prompts"] for k in r)
    data=(BUILT/"gallery/data.js").read_text(); assert data.startswith("const ANALYSIS=") and data.endswith(";\n")
    assert json.loads(data[len("const ANALYSIS="):-2])==analysis
    visible="\n".join((BUILT/"gallery"/n).read_text() for n in ("index.html","report.js"))
    low=visible.casefold()
    assert all(term not in low for term in FORBIDDEN_LABELS)
    assert "V6.1 distribution &amp; text quality" in visible and "V6.1 declared prop audit · all 160" in visible
    assert "Complete V6.1 props list · 261" in visible and "All approved entries" in visible
    assert "No downstream text transformation or image audit exists until images are generated." in visible
    for n in ("data.js","report.js","style.css","imsauth.js"):
        assert (BUILT/"gallery"/n).is_file() and n in (BUILT/"gallery/index.html").read_text()
    for n in ("analysis.json","candidate_metrics.csv","v6_1_prompts_all_160.json","v6_1_prop_usage.json","v6_1_prop_usage.csv","v6_1_approved_prop_catalog.json","v6_1_approved_prop_catalog.csv","V6_1_PROPS_FOR_REVIEW.md"):
        assert (BUILT/"downloads"/n).is_file()
    manifest=json.loads((BUILT/"build_manifest.json").read_text()); assert "build_manifest.json" not in manifest["artifacts"]
    for rel,meta in manifest["artifacts"].items():
        p=BUILT/rel; assert p.stat().st_size==meta["bytes"] and sha(p)==meta["sha256"]
    node=shutil.which("node") or "/opt/conda/bin/node"
    subprocess.run([node,"--check",str(BUILT/"gallery/report.js")],check=True)
    subprocess.run([node,"--check",str(BUILT/"gallery/data.js")],check=True)
    print("Validated 160 unique V6.1 rows, 16 complete banks, declared props, compliance audits, hashes, labels, and JavaScript syntax.")
if __name__=="__main__": main()
