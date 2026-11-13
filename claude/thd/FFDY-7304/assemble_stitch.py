#!/usr/bin/env python3
"""Review stitch: chosen clips per shot, in the requested order, to check harmony + character consistency.
Order: Shot1(first 1.8s) -> 2,3,4,5 -> [skip 6,7] -> 8,9 -> 17."""
import os, subprocess
A="/home/colligo/THD_laundry_sink_storyboard/gallery/assets"
OUT="/home/colligo/THD_laundry_sink_storyboard/gen/final_stitch.mp4"
# (file, start, dur)  dur=None -> full
SEQ=[
 ("S01.mp4",     0.0, 1.8),   # shot 1 establishing, first 1.8s
 ("1A.mp4",      0.0, None),  # shot 2 assemble (flat panels)
 ("3A_v1.mp4",   0.0, None),  # shot 3 connector macro
 ("opp.mp4",     0.0, None),  # shot 4 opposite side
 ("perp5B.mp4",  0.0, None),  # shot 5 perpendicular
 ("4A.mp4",      0.0, None),  # shot 8 stand up
 ("4B.mp4",      0.0, None),  # shot 9 place basin
 ("8B.mp4",      0.0, None),  # shot 17 hero
]
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",p],capture_output=True,text=True).stdout.strip())
cmd=["ffmpeg","-nostdin","-y","-loglevel","error"]
for f,ss,d in SEQ:
    p=os.path.join(A,f)
    cmd+=["-ss",str(ss)]+( ["-t",str(d)] if d else [])+["-i",p]
n=len(SEQ)
fc="".join(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{i}];" for i in range(n))
fc+="".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0[out]"
cmd+=["-filter_complex",fc,"-map","[out]","-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-preset","medium",OUT]
subprocess.run(cmd,check=True)
print("DONE ->",OUT,"("+subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",OUT],capture_output=True,text=True).stdout.strip()+"s)")
