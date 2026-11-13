#!/usr/bin/env python3
"""Multi-model video gen driver for the model comparison (Seedance 2.5 / Seedance 2.0 / MiniMax H3).
Reuses the fal client (upload/_req/poll) from seedance_video.py. Config-per-shot-per-model.

Config JSON: { id, model:"sd25|sd20|h3", mode:"i2v|ref", images:[...], prompt, duration, resolution,
               end_image?  }  (end_image used for i2v first->last on sd20/h3)
Endpoints:
  sd25: bytedance/seedance-2.5/{image-to-video(image_url), reference-to-video(image_urls)}
  sd20: bytedance/seedance-2.0/{image-to-video(image_url,end_image_url), reference-to-video(image_urls)}
  h3  : minimax/h3/image-to-video (image_url, end_image_url)   [no multi-ref on this endpoint]
"""
import os, sys, time, json, urllib.request
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

EP = {
 ("sd25","i2v"):"bytedance/seedance-2.5/image-to-video",
 ("sd25","ref"):"bytedance/seedance-2.5/reference-to-video",
 ("sd20","i2v"):"bytedance/seedance-2.0/image-to-video",
 ("sd20","ref"):"bytedance/seedance-2.0/reference-to-video",
 ("h3","i2v"):"minimax/h3/image-to-video",
 ("h3","ref"):"minimax/h3/image-to-video",   # h3 has no multi-ref here -> use first(+last) frame
}

def key():
    return sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))

def run(cfg):
    k=key(); model=cfg["model"]; mode=cfg["mode"]
    imgs=cfg["images"]; out=os.path.join(cfg["work_dir"],cfg["id"]); os.makedirs(out,exist_ok=True)
    open(os.path.join(out,"prompt.txt"),"w").write(cfg["prompt"])
    urls=[sv.upload(k,p) for p in imgs]
    ep=EP[(model,mode)]
    payload={"prompt":cfg["prompt"]}
    res=cfg.get("resolution"); dur=cfg.get("duration")
    if model in ("sd25","sd20"):
        payload["resolution"]=res; payload["duration"]=str(dur)
        if mode=="i2v":
            payload["image_url"]=urls[0]
            if cfg.get("end_image"): payload["end_image_url"]=sv.upload(k,cfg["end_image"])
            if model=="sd20": payload["generate_audio"]=False
        else:
            payload["image_urls"]=urls
            payload["aspect_ratio"]="16:9"; 
            if model=="sd20": payload["generate_audio"]=False
    elif model=="h3":
        payload["resolution"]=res              # 480P/768P/2K/4K
        payload["duration"]=max(5,int(round(float(dur))))
        payload["image_url"]=urls[0]
        # multi-keyframe on h3 -> use last image as the end frame
        if len(urls)>1: payload["end_image_url"]=urls[-1]
        elif cfg.get("end_image"): payload["end_image_url"]=sv.upload(k,cfg["end_image"])
        payload["enable_safety_checker"]=True; payload["prompt_expansion_mode"]="balanced"
    t=time.time()
    code,body=sv._req(k, sv.QUEUE+ep, payload)
    if code not in (200,201,202): return cfg["id"],f"submit {code}: {str(body.get('_error'))[:300]}",0,0
    surl,rurl=body.get("status_url"),body.get("response_url")
    dbg={"submit":body,"status":[]}
    while time.time()-t<1800:
        time.sleep(10); sc,sb=sv._req(k,surl); st=sb.get("status"); dbg["status"].append(st)
        print(f"  [{model}] {st} ({round(time.time()-t)}s)",flush=True)
        if st=="COMPLETED": break
        if st in ("FAILED","ERROR"):
            json.dump(dbg,open(os.path.join(out,"debug.json"),"w")); return cfg["id"],f"FAILED {str(sb)[:200]}",round(time.time()-t),0
    else: return cfg["id"],"timeout",round(time.time()-t),0
    rc,rb=sv._req(k,rurl)
    vid=(rb.get("video") or {}).get("url") or (rb.get("videos") or [{}])[0].get("url")
    if not vid: json.dump(rb,open(os.path.join(out,"debug.json"),"w")); return cfg["id"],f"no video url: {str(rb)[:250]}",round(time.time()-t),0
    dst=os.path.join(out,cfg["id"]+".mp4")
    with urllib.request.urlopen(vid,timeout=600) as r,open(dst,"wb") as f: f.write(r.read())
    json.dump({**cfg,"response":rb},open(os.path.join(out,cfg["id"]+".json"),"w"),indent=1,default=str)
    return cfg["id"],"ok",round(time.time()-t),os.path.getsize(dst)

if __name__=="__main__":
    cfg=json.load(open(sys.argv[1])); print("RESULT:",run(cfg))
