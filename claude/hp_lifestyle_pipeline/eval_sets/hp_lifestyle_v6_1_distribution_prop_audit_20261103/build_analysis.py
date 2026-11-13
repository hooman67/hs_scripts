#!/usr/bin/env python3
"""Build the frozen V6.1 all-160 distribution and declared-prop audit."""
from __future__ import annotations

import argparse, csv, hashlib, importlib.util, json, math, re, shutil, sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline")
HERE = Path(__file__).resolve().parent
REVISION = PROJECT / "eval_sets/hp_lifestyle_phrase_diversity_v6_1_four_devices_20261103/revisions/v6.1-expanded-20261103-r6"
SOURCE = REVISION / "exports/final/prompts_all_160.json"
EXPECTED_SOURCE_SHA256 = "adcb9edb2643e45acb0cb882cdc4d65b8c256a52d58ad4a44ddd9c235287b3cd"
CATALOG = REVISION / "runtime/v6_1/approved_catalog.json"
PROPS_REVIEW = PROJECT / "research/approved_props_v6_1/PROPS_FOR_REVIEW.md"
REFERENCES = REVISION / "runtime/v6_1/reference_library.json"
TEMPLATE = HERE / "template"
DEFAULT_OUTPUT = HERE / "built"
HELPERS = PROJECT / "eval_sets/hp_lifestyle_ctech_v4_1_pilot_20261026/distribution_analysis_v1/build_analysis.py"

def load_helpers():
    spec = importlib.util.spec_from_file_location("distribution_helpers", HELPERS)
    if not spec or not spec.loader: raise RuntimeError("Cannot load distribution helpers")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
H = load_helpers()

def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def total(row, document): return sum(int(v) for v in (row.get("score_components") or {}).get(document, {}).values())
def entropy(counts):
    n=sum(counts.values()); return round(-sum((v/n)*math.log2(v/n) for v in counts.values() if v),6)
def hist(values, edges):
    return [{"label":f"{a:g}–{b:g}","count":sum(a<=v< b if i<len(edges)-2 else a<=v<=b for v in values)} for i,(a,b) in enumerate(zip(edges,edges[1:]))]
def document_metrics(values):
    return {"mean":round(float(np.mean(values)),6),"quantiles":H.quantiles(values)}

def approved_catalog_summary(catalog_doc):
    entries = sorted(catalog_doc["entries"], key=lambda x:(x["environment"],x["role"],x["name"],x["id"]))
    families = sorted({group for entry in entries for group in entry["repetition_groups"]})
    return {
        "version":catalog_doc["version"], "revision":catalog_doc["revision"], "purpose":catalog_doc["purpose"],
        "source_sha256":sha(CATALOG), "review_source_sha256":sha(PROPS_REVIEW),
        "entry_count":len(entries), "visual_family_count":len(families),
        "environment_counts":dict(sorted(Counter(e["environment"] for e in entries).items())),
        "role_counts":dict(sorted(Counter(e["role"] for e in entries).items())),
        "visual_families":families, "entries":entries,
        "review_note":"This is the complete V6.1 runtime catalogue, including approved entries that were not selected in the 160-prompt evaluation. Aliases are validator-recognized wording, not additional prop approvals."
    }

def load_validation():
    sys.path.insert(0, str(REVISION / "runtime"))
    from v6_1 import validation
    return validation

def normalize(doc):
    rows=[]
    for item in doc["prompts"]:
        if hashlib.sha256(item["text"].encode("utf-8")).hexdigest() != item["text_sha256"]:
            raise ValueError(f"Prompt text hash mismatch: {item['prompt_key']}")
        rows.append({
            "prompt_key":item["prompt_key"], "device_id":item["device_id"],
            "device_display_name":item["device_display_name"], "device_type":item["device_type"],
            "source_pair":item["source_pair"], "camera_tag":item["camera_tag"],
            "source_camera_name":item["source_camera_name"], "view_role":item["view_role"],
            "bank_rank":int(item["bank_rank"]), "environment":item["environment"], "text":item["text"],
            "source_relevance_score":int(item["source_relevance_score"]),
            "ctech_reference_score":int(item["ctech_reference_score"]), "ctech_reference_id":item["ctech_reference_id"],
            "source_relationship":item.get("relationship", ""), "source_explanation":item.get("explanation", ""),
            "ctech_explanation":item.get("ctech_explanation", ""), "camera_fit_explanation":item.get("camera_fit_explanation", ""),
            "source_evidence":item.get("evidence", []), "creative_departures":item.get("creative_departures", []),
            "score_components":item.get("score_components", {}), "smart_brief_support_total":total(item,"smart_brief"),
            "source_messaging_support_total":total(item,"source_messaging"), "prop_ids":list(item.get("prop_ids",[])),
            "prop_mentions":list(item.get("prop_mentions",[])), "prop_count":len(item.get("prop_ids",[])),
            "source_revision":item.get("source_revision", ""), "bank_debug_ref":item["bank_debug_ref"],
            "word_count":len(H.words(item["text"])), "sentence_count":len(H.sentences(item["text"])),
            "debug":doc["bank_audit"][item["bank_debug_ref"]]["debug"],
        })
    if len(rows)!=160 or len({r["prompt_key"] for r in rows})!=160: raise ValueError("V6.1 export must contain 160 unique rows")
    banks=defaultdict(list)
    for row in rows: banks[row["bank_debug_ref"]].append(row)
    if len(banks)!=16 or any(len(v)!=10 for v in banks.values()): raise ValueError("V6.1 export must contain 16 banks × 10 rows")
    if any(sorted(r["bank_rank"] for r in v)!=list(range(1,11)) for v in banks.values()): raise ValueError("Every bank must contain ranks 1 through 10")
    return rows, banks

def lexical_summary(rows):
    audit=H.lexical_audit([{**r,"candidate_key":r["prompt_key"]} for r in rows])
    return {"distinct_text_count":len({" ".join(r["text"].split()) for r in rows}),
            "exact_duplicate_groups":audit["exact_duplicate_groups"], "canonical_duplicate_groups":audit["canonical_duplicate_groups"],
            "recurring_phrases":audit["recurring_phrases"][:40], "closest_lexical_pairs":audit["closest_pairs"][:20]}

def distribution(rows):
    env=dict(sorted(Counter(r["environment"] for r in rows).items())); source=[r["source_relevance_score"] for r in rows]
    declared=[r["ctech_reference_score"] for r in rows]; measured=[r["measured_ctech_similarity"] for r in rows]
    props=[r["prop_count"] for r in rows]
    out={"count":160,"environment_counts":env,"environment_entropy_bits":entropy(env),
         "device_counts":dict(sorted(Counter(r["device_id"] for r in rows).items())),
         "view_counts":dict(sorted(Counter(r["view_role"] for r in rows).items())),
         "source_score":{**document_metrics(source),"histogram":hist(source,list(range(0,101,10)))},
         "declared_ctech_score":{**document_metrics(declared),"histogram":hist(declared,list(range(0,101,10)))},
         "measured_ctech_similarity":{**document_metrics(measured),"histogram":H.similarity_hist(np.asarray(measured))},
         "word_count":document_metrics([r["word_count"] for r in rows]), "sentence_count":document_metrics([r["sentence_count"] for r in rows]),
         "prop_count":{**document_metrics(props),"zero_prop_prompts":sum(v==0 for v in props)},
         "document_support":{"both_documents_nonzero":sum(r["smart_brief_support_total"]>0 and r["source_messaging_support_total"]>0 for r in rows),
             "smart_brief_only":sum(r["smart_brief_support_total"]>0 and r["source_messaging_support_total"]==0 for r in rows),
             "source_messaging_only":sum(r["smart_brief_support_total"]==0 and r["source_messaging_support_total"]>0 for r in rows),
             "neither_document":sum(r["smart_brief_support_total"]==0 and r["source_messaging_support_total"]==0 for r in rows)},
         "similarity_by_environment":H.grouped(rows,"environment","measured_ctech_similarity"),
         "similarity_by_view":H.grouped(rows,"view_role","measured_ctech_similarity")}
    out.update(lexical_summary(rows)); return out

def prop_audit(rows,banks,catalog_entries,V):
    catalog={e["id"]:e for e in catalog_entries}; uses=defaultdict(set); group_uses=defaultdict(set); group_ids=defaultdict(set)
    for r in rows:
        for pid in r["prop_ids"]:
            if pid not in catalog: raise ValueError(f"Unresolved approved prop ID: {pid}")
            if catalog[pid]["environment"]!=r["environment"]: raise ValueError(f"Prop environment mismatch: {r['prompt_key']} {pid}")
            uses[pid].add(r["prompt_key"])
            for g in catalog[pid]["repetition_groups"]: group_uses[g].add(r["prompt_key"]); group_ids[g].add(pid)
    approved=[{"prop_id":pid,"name":catalog[pid]["name"],"environment":catalog[pid]["environment"],"role":catalog[pid]["role"],
               "repetition_groups":catalog[pid]["repetition_groups"],"prompt_count":len(keys),"prompt_share":round(len(keys)/160,6),"prompt_keys":sorted(keys)} for pid,keys in uses.items()]
    approved.sort(key=lambda x:(-x["prompt_count"],x["prop_id"]))
    families=[{"family":g,"prompt_count":len(keys),"prompt_share":round(len(keys)/160,6),"prop_ids":sorted(group_ids[g]),"prompt_keys":sorted(keys)} for g,keys in group_uses.items()]
    families.sort(key=lambda x:(-x["prompt_count"],x["family"]))
    bank_rows=[]; semantic_rows=[]; shelf_rows=[]; printer_rows=[]
    for bank,br in sorted(banks.items()):
        family_to_keys=defaultdict(list); semantic_to_keys=defaultdict(list)
        for r in br:
            groups={g for pid in r["prop_ids"] for g in catalog[pid]["repetition_groups"]}
            for g in groups: family_to_keys[g].append(r["prompt_key"])
            for family,pattern in V._SEMANTIC_PHRASE_FAMILIES.items():
                if pattern.search(r["text"]): semantic_to_keys[family].append(r["prompt_key"])
            selected=groups.intersection(V._SHELF_GROUPS)
            if selected:
                shelf_rows.append({"prompt_key":r["prompt_key"],"shelf_families":sorted(selected),"content_families":sorted(groups-V._SHELF_GROUPS),
                    "explicitly_populated":bool(V._POPULATED_SHELF_RE.search(r["text"])),"empty_wording":bool(V._EMPTY_SHELF_RE.search(r["text"])),"text":r["text"]})
            if r["device_type"]=="printer":
                input_doc=doc_bank_source[bank]; combined=(str(input_doc.get("smart_brief",""))+" "+json.dumps(input_doc.get("source_messaging",{}),ensure_ascii=False))
                env=r["environment"]; support=V._PRINTER_SUPPORT_RE.get(env)
                printer_rows.append({"prompt_key":r["prompt_key"],"environment":env,
                    "source_environment_supported": not ((env=="Café" and not re.search(r"\b(?:caf[ée]|coffee shop)\b",combined,re.I)) or (env=="Gaming" and not re.search(r"\b(?:gaming|game room|gamer)\b",combined,re.I))),
                    "credible_support_surface":support is None or bool(support.search(r["text"])),"implausible_surface":bool(V._PRINTER_FORBIDDEN_SURFACE_RE.search(r["text"])),"text":r["text"]})
        repeated={g:k for g,k in family_to_keys.items() if len(k)>1}; semrep={g:k for g,k in semantic_to_keys.items() if len(k)>1}
        bank_rows.append({"bank":bank,"prompt_count":len(br),"unique_families":len(family_to_keys),"passed":not repeated,"reused_families":repeated})
        semantic_rows.append({"bank":bank,"matched_phrase_families":len(semantic_to_keys),"passed":not semrep,"reused_phrase_families":semrep})
    return {"scope":{"prompt_rows":160,"banks":16,"prompts_per_bank":10,"images_available":False,"downstream_text_available":False},
        "headline":{"unique_approved_prop_ids_used":len(approved),"approved_prop_assignments":sum(len(r["prop_ids"]) for r in rows),"unique_semantic_families_used":len(families)},
        "environment_counts":dict(sorted(Counter(r["environment"] for r in rows).items())),"approved_props":approved,"semantic_families":families,
        "bank_family_compliance":bank_rows,"semantic_phrase_family_compliance":semantic_rows,"populated_shelving_pegboard":shelf_rows,
        "printer_environment_support_desk":printer_rows,
        "status_note":"No downstream text transformation or image audit exists until images are generated."}

doc_bank_source={}
def build(output:Path,cache_dir:Path):
    if not SOURCE.is_file(): raise FileNotFoundError(f"Required accepted V6.1 export is absent: {SOURCE}")
    if sha(SOURCE)!=EXPECTED_SOURCE_SHA256: raise ValueError("Accepted V6.1 export hash differs from the pinned final composite")
    source_doc=json.loads(SOURCE.read_text()); catalog_doc=json.loads(CATALOG.read_text()); refs_doc=json.loads(REFERENCES.read_text())
    manifest_path=Path(source_doc["snapshot_manifest_path"])
    if not manifest_path.is_file() or sha(manifest_path)!=source_doc["snapshot_manifest_sha256"]:
        raise ValueError("Accepted export snapshot-manifest hash does not resolve")
    rows,banks=normalize(source_doc)
    global doc_bank_source
    doc_bank_source={k:v["source_input"] for k,v in source_doc["bank_audit"].items()}
    refs=[{"reference_id":r["id"],"group":r["environment"],"original_text":r["text"],"scope_adjusted_text":r["text"]} for r in refs_doc["references"]]
    embeddings,model_meta=H.embed([r["text"] for r in rows]+[r["scope_adjusted_text"] for r in refs],cache_dir)
    pe,re=embeddings[:160],embeddings[160:]; sim=pe@re.T; nearest=sim.argmax(1); pair=pe@pe.T; np.fill_diagonal(pair,-np.inf); near_prompt=pair.argmax(1)
    coords,explained=H.pca_2d(np.vstack([pe,re]))
    for i,r in enumerate(rows):
        declared=next(j for j,x in enumerate(refs) if x["reference_id"]==r["ctech_reference_id"])
        r.update(measured_ctech_similarity=round(float(sim[i,nearest[i]]),6),measured_ctech_reference_id=refs[int(nearest[i])]["reference_id"],
            declared_reference_similarity=round(float(sim[i,declared]),6),nearest_prompt_similarity=round(float(pair[i,near_prompt[i]]),6),
            nearest_prompt_key=rows[int(near_prompt[i])]["prompt_key"],map_x=round(float(coords[i,0]),6),map_y=round(float(coords[i,1]),6))
    mapped_refs=[{**r,"map_x":round(float(coords[160+i,0]),6),"map_y":round(float(coords[160+i,1]),6)} for i,r in enumerate(refs)]
    counts=Counter(r["measured_ctech_reference_id"] for r in rows); declared=Counter(r["ctech_reference_id"] for r in rows)
    coverage=[{**r,"nearest_count":counts[r["reference_id"]],"declared_count":declared[r["reference_id"]]} for r in refs]
    sources={}
    for bank,payload in doc_bank_source.items():
        pair=next(r["source_pair"] for r in rows if r["bank_debug_ref"]==bank)
        sources.setdefault(pair,{"smart_brief":payload["smart_brief"],"source_messaging":payload["source_messaging"],"banks":[]})["banks"].append(bank)
    audit=prop_audit(rows,banks,catalog_doc["entries"],load_validation())
    catalog_summary=approved_catalog_summary(catalog_doc)
    analysis={"version":"hp-lifestyle-v6.1-all160-distribution-declared-prop-audit-v2","as_of":"2026-11-05",
        "status":"accepted_text_and_declared_props_before_image_generation","scope":{"prompt_rows":160,"banks":16,"prompts_per_bank":10,"ctech_reference_count":len(refs)},
        "inputs":{"accepted_export":{"path":str(SOURCE),"sha256":sha(SOURCE)},"approved_catalog":{"path":str(CATALOG),"sha256":sha(CATALOG)},"approved_prop_review_source":{"path":str(PROPS_REVIEW),"sha256":sha(PROPS_REVIEW)},"reference_library":{"path":str(REFERENCES),"sha256":sha(REFERENCES)}},
        "methods":{"semantic_embedding":model_meta,"map":{"method":"Joint PCA over 160 accepted prompts and 18 C-Tech references","explained_variance_ratio_first_two":explained},
            "measured_ctech_similarity":"Maximum cosine similarity to the 18 normalized C-Tech text references.","selection":"All ten source-ranked rows from each of 16 device/camera banks."},
        "summary":distribution(rows),"reference_coverage":coverage,"references":mapped_refs,"source_pairs":sources,"prop_audit":audit,"approved_prop_catalog":catalog_summary,"rows":rows,
        "limitations":["Semantic text proximity is descriptive and is not an acceptance threshold or image-quality score.","Declared prop counts describe requested text, not visible pixels.","No downstream text transformation or image audit exists until images are generated."]}
    downloads=output/"downloads"; gallery=output/"gallery"; downloads.mkdir(parents=True,exist_ok=True); gallery.mkdir(parents=True,exist_ok=True)
    (downloads/"analysis.json").write_text(json.dumps(analysis,ensure_ascii=False,indent=2)+"\n")
    shutil.copy2(SOURCE,downloads/"v6_1_prompts_all_160.json")
    shutil.copy2(CATALOG,downloads/"v6_1_approved_prop_catalog.json")
    shutil.copy2(PROPS_REVIEW,downloads/"V6_1_PROPS_FOR_REVIEW.md")
    usage={"version":"hp-lifestyle-v6.1-declared-prop-usage-v1",**audit}; (downloads/"v6_1_prop_usage.json").write_text(json.dumps(usage,ensure_ascii=False,indent=2)+"\n")
    with (downloads/"candidate_metrics.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["prompt_key","device_id","camera_tag","view_role","bank_rank","environment","source_relevance_score","ctech_reference_score","measured_ctech_similarity","measured_ctech_reference_id","word_count","sentence_count","prop_count"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows({k:r[k] for k in fields} for r in rows)
    with (downloads/"v6_1_prop_usage.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["prop_id","name","environment","role","repetition_groups","prompt_count","prompt_share","prompt_keys"]; w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for x in audit["approved_props"]: w.writerow({**x,"repetition_groups":"|".join(x["repetition_groups"]),"prompt_keys":"|".join(x["prompt_keys"])})
    with (downloads/"v6_1_approved_prop_catalog.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["id","name","environment","role","repetition_groups","aliases"]; w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for x in catalog_summary["entries"]: w.writerow({**x,"repetition_groups":"|".join(x["repetition_groups"]),"aliases":"|".join(x["aliases"])})
    (gallery/"data.js").write_text("const ANALYSIS="+json.dumps(analysis,ensure_ascii=False,separators=(",",":"))+";\n")
    for name in ("index.html","report.js","style.css","imsauth.js"): shutil.copy2(TEMPLATE/name,gallery/name)
    artifacts={}
    for p in sorted(output.rglob("*")):
        if p.is_file() and p.name!="build_manifest.json": artifacts[str(p.relative_to(output))]={"bytes":p.stat().st_size,"sha256":sha(p)}
    manifest={"version":"hp-lifestyle-v6.1-report-build-manifest-v1","source_revision":"v6.1-expanded-20261103-r6","artifacts":artifacts}
    (output/"build_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n"); return analysis

def main():
    p=argparse.ArgumentParser(); p.add_argument("--output",type=Path,default=DEFAULT_OUTPUT); p.add_argument("--cache-dir",type=Path,default=Path("/mnt/localssd/hp_lifestyle_pipeline/cache/huggingface")); a=p.parse_args(); print(json.dumps(build(a.output.resolve(),a.cache_dir.resolve())["scope"],indent=2))
if __name__=="__main__": main()
