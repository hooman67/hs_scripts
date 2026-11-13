#!/usr/bin/env python3
"""Round 1 — reproduce shot 0003 (measure the door-lock backset). Three references, one prompt."""
import os, sys, concurrent.futures as cf
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

BASE = "/home/colligo/THD_How_to_Install_a_Door_Lock"
OUT = os.path.join(BASE, "work", "gen_round1")
REFS = os.path.join(BASE, "work", "refs")
KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))

# 5-line prompt, client register: subject -> beats -> camera -> talent -> look+negatives
L1 = ("A man in a light blue denim work shirt, a red carpenter's pencil tucked over one ear, "
      "crouches at the inside of a white exterior door and measures the backset of the lock with "
      "a yellow-and-black tape measure, holding the tape from the edge of the door across to the "
      "centre of the door knob.")
L2 = ("In order: he pulls the tape measure blade across the face of the door toward the knob; then "
      "he leans in and reads the measurement at the edge of the door.")
L3 = ("Medium shot from his left side, showing his profile, his hands and the two stainless locks. "
      "Static shot; the camera does not pan, tilt or zoom.")
L4 = "The man is visible from the chest up, working steadily with both hands."
L5 = ("Photoreal Home Depot how-to footage. Bright natural 5500K daylight through the door's glass "
      "pane and a nearby window, a green fiddle-leaf fig plant and a bright, clean room behind him. "
      "The door carries a stainless steel deadbolt above a stainless steel knob, with a tall frosted "
      "glass panel and white blinds to the right. No on-screen text, no captions, no watermarks, no "
      "added logos, no competitor brands.")
KEEP = (" Keep the door, the stainless deadbolt and knob, the man's clothing and the yellow tape "
        "measure looking exactly like the reference image.")

PROMPT_T2V = "\n".join([L1, L2, L3, L4, L5])
PROMPT_REF = "\n".join([L1, L2, L3, L4, L5 + KEEP])

JOBS = [
    ("A_article_ref",   "ref", PROMPT_REF, [os.path.join(REFS, "article_step1.jpg")]),
    ("B_facehidden_ref","ref", PROMPT_REF, [os.path.join(REFS, "shot_frame_facehidden.jpg")]),
    ("C_t2v",           "t2v", PROMPT_T2V, []),
]

def run(job):
    name, mode, prompt, images = job
    return sv.generate(KEY, name=name, mode=mode, prompt=prompt, out_dir=OUT,
                       images=images, duration="8", resolution="720p", audio=False,
                       aspect="16:9",
                       on_status=lambda st, s: print(f"    [{name}] {st} ({s}s)", flush=True))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"key ...{KEY[-4:]}  ->  {OUT}", flush=True)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for name, status, secs, size in ex.map(run, JOBS):
            print(f"==> [{status[:44]:<44}] {name:<20} {secs:>4}s {size//1024:>7} KB", flush=True)
