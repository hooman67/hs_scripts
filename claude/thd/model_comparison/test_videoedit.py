#!/usr/bin/env python3
"""Test Seedance 2.5 VIDEO-EDIT (reference-to-video + video_urls) on a Seedance-GENERATED people shot.
Test A: change the CHARACTER.  Test B: change a NON-character element.
Reports whether each is blocked (content_policy_violation) or renders."""
import os, sys, time, json, urllib.request
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

MODEL=os.environ.get("VE_MODEL","sd25")   # sd25 | sd20
EP=f"bytedance/seedance-{'2.5' if MODEL=='sd25' else '2.0'}/reference-to-video"
DEF_SRC=("/home/colligo/THD_laundry_sink_storyboard/gen_compare/%s/S11_8B/S11_8B.mp4"
         % ("sd25" if MODEL=="sd25" else "sd20"))
SRC=os.environ.get("VE_SRC", DEF_SRC)
OUT="/home/colligo/THD_laundry_sink_storyboard/videoedit_test"+("" if MODEL=="sd25" else "_"+MODEL)
os.makedirs(OUT,exist_ok=True)

TESTS={
 "A_change_character":
   "Video edit. Keep the camera, framing, room, lighting and all body motion EXACTLY the same. "
   "Change ONLY the appearance of the two people: replace them with a different couple — a young woman "
   "with long wavy red hair in a mustard-yellow cardigan, and a clean-shaven man in his 30s with short "
   "dark-brown hair in a dark-green henley. Same poses, same positions, same movement. Do not change "
   "anything else in the scene.",
 "B_change_object":
   "Video edit. Keep the two people, their clothing, faces, poses and all motion EXACTLY the same, and "
   "keep the camera and room the same. Change ONLY the base cabinet under the sink: recolor it from white "
   "to a deep matte navy blue. Everything else stays identical.",
}

def submit_poll(name, prompt, url):
    payload={"prompt":prompt, "video_urls":[url], "resolution":"720p", "duration":"6", "aspect_ratio":"16:9"}
    if MODEL=="sd20": payload["generate_audio"]=False
    k=sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
    t=time.time()
    code,body=sv._req(k, sv.QUEUE+EP, payload)
    rec={"name":name,"submit_code":code}
    if code not in (200,201,202):
        rec["result"]="BLOCKED_OR_ERROR"; rec["detail"]=str(body)[:600]
        json.dump(rec,open(f"{OUT}/{name}.json","w"),indent=1); print(name,"-> submit",code, str(body)[:300]); return rec
    surl=body.get("status_url"); rurl=body.get("response_url")
    st=None
    while time.time()-t<1800:
        time.sleep(10); sc,sb=sv._req(k,surl); st=sb.get("status")
        print(f"  [{name}] {st} ({round(time.time()-t)}s)",flush=True)
        if st=="COMPLETED": break
        if st in ("FAILED","ERROR"):
            rec["result"]="FAILED"; rec["detail"]=str(sb)[:600]
            json.dump(rec,open(f"{OUT}/{name}.json","w"),indent=1); print(name,"-> FAILED",str(sb)[:300]); return rec
    k2=sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
    rc,rb=sv._req(k2,rurl)
    vid=(rb.get("video") or {}).get("url") or (rb.get("videos") or [{}])[0].get("url")
    if not vid:
        rec["result"]="NO_VIDEO"; rec["detail"]=str(rb)[:600]
        json.dump(rec,open(f"{OUT}/{name}.json","w"),indent=1); print(name,"-> no video",str(rb)[:300]); return rec
    dst=f"{OUT}/{name}.mp4"
    with urllib.request.urlopen(vid,timeout=600) as r,open(dst,"wb") as f: f.write(r.read())
    rec["result"]="OK"; rec["mp4"]=dst; rec["prompt"]=prompt
    json.dump(rec,open(f"{OUT}/{name}.json","w"),indent=1); print(name,"-> OK",os.path.getsize(dst),"bytes"); return rec

if __name__=="__main__":
    which=sys.argv[1]
    k=sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
    url=sv.upload(k, SRC)
    open(f"{OUT}/src_url.txt","w").write(url)
    print("uploaded src ->", url)
    submit_poll(which, TESTS[which], url)
