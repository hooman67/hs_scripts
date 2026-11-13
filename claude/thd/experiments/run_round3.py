#!/usr/bin/env python3
"""Round 3 — get the MEASUREMENT right. ref-mode, front plate, one measurement per clip."""
import os, sys, concurrent.futures as cf
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

BASE = "/home/colligo/THD_How_to_Install_a_Door_Lock"
OUT = os.path.join(BASE, "work", "gen_round3")
PLATES = os.path.join(BASE, "work", "plates")
KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))

CAM = ("Medium close shot from the room side, framed on his hands, the tape measure and the lockset. "
       "Static shot; the camera does not pan, tilt or zoom.")
TALENT = ("The man is visible from the chest up and keeps his fingers clear of the tape's markings so "
          "the numbers stay readable.")
def look(ref_line):
    return ("Photoreal Home Depot how-to footage, bright natural 5500K daylight. " + ref_line +
            " His denim shirt is a plain solid colour with no text, no logo, no wordmark and no "
            "writing anywhere. No on-screen text, no captions, no watermarks, no added logos, no "
            "competitor brands.")

KEEP_KNOB = ("Keep the white door, the stainless steel deadbolt and door knob, the frosted glass panel "
             "with white blinds, the green fiddle-leaf fig plant, the walls and the lighting exactly as "
             "in the reference image; add the man in front of the door.")
KEEP_BORE = ("Keep the white door, the stainless steel deadbolt, the empty round bore hole in the door, "
             "the frosted glass panel with white blinds, the green fiddle-leaf fig plant, the walls and "
             "the lighting exactly as in the reference image; add the man in front of the door.")

V1 = "\n".join([
 "A man in a plain light-blue denim work shirt, a red carpenter's pencil tucked over one ear, crouches "
 "close to the white glass-panel door and measures the lock BACKSET. He hooks the metal end of a yellow "
 "tape measure on the edge of the door right beside the latch and pulls the blade only two or three "
 "inches across the face of the door to the centre of the door knob, reading about two and three-eighths "
 "inches.",
 "In order: he sets the tape's hook on the edge of the door by the latch; then he reads the short "
 "distance at the centre of the knob.",
 CAM, TALENT, look(KEEP_KNOB)])

V2 = "\n".join([
 "A man in a plain light-blue denim work shirt, a red carpenter's pencil tucked over one ear, crouches "
 "close to the white glass-panel door and measures the THICKNESS of the door slab. He holds a yellow tape "
 "measure flat against the narrow front edge of the door and reads the thickness straight across the edge, "
 "from the front face to the back face of the door, about one and three-eighths inches.",
 "In order: he sets the tape on the front edge of the door; then he reads the thickness across the edge.",
 CAM, TALENT, look(KEEP_KNOB)])

V3 = "\n".join([
 "A man in a plain light-blue denim work shirt, a red carpenter's pencil tucked over one ear, crouches "
 "close to the white glass-panel door and measures the DIAMETER of the round bore hole cut in the door. "
 "He lays a yellow tape measure straight across the open round hole in the face of the door, from one edge "
 "of the hole to the opposite edge, reading about two and one-eighth inches across.",
 "In order: he lays the tape across the round hole; then he reads the diameter from edge to edge.",
 CAM, TALENT, look(KEEP_BORE)])

JOBS = [
    ("V1_backset",   os.path.join(PLATES, "plate_paint_article.png"), V1),
    ("V2_thickness", os.path.join(PLATES, "plate_paint_article.png"), V2),
    ("V3_diameter",  os.path.join(PLATES, "plate_bore_article.png"),  V3),
]

def run(job):
    name, img, prompt = job
    return sv.generate(KEY, name=name, mode="ref", prompt=prompt, out_dir=OUT, images=[img],
                       duration="8", resolution="720p", audio=False, aspect="16:9",
                       on_status=lambda st, s: print(f"    [{name}] {st} ({s}s)", flush=True))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"key ...{KEY[-4:]} -> {OUT}", flush=True)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for name, status, secs, size in ex.map(run, JOBS):
            print(f"==> [{status[:44]:<44}] {name:<14} {secs:>4}s {size//1024:>7} KB", flush=True)
    print("DONE", flush=True)
