#!/usr/bin/env python3
"""Round 7 v2 — clean crop (no TIP graphic) + stronger door-closing motion."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

BASE = "/home/colligo/THD_How_to_Install_a_Door_Lock"
OUT = os.path.join(BASE, "work", "gen_round7")
KF = os.path.join(BASE, "work", "keyframes_v2")   # b=0.685 crops, TIP graphic removed
KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))

PROMPT = (
 "Use @Image1 through @Image3 as keyframes in that order.\n"
 "Use @Image1 as the first frame.\n"
 "This first frame defines the starting composition: a pair of hands holding a yellow tape measure "
 "against the lockset of a white glass-panel door, the hook end of the tape caught on the edge of the "
 "door beside the latch and the case in the hand near the stainless knob; close-up on the lockset.\n"
 "@Image2 defines the second keyframe: the hands hold the tape steady across the short distance from the "
 "door edge to the centre of the knob, measuring the backset.\n"
 "Use @Image3 as the last frame.\n"
 "This last frame defines the ending composition: the hands keep the tape held across the lockset with "
 "the short backset still shown.\n"
 "The shot passes through the states defined by @Image1, @Image2 and @Image3 in order with continuous "
 "natural hand motion. Partway through, he clearly swings the door a few inches toward the camera — the "
 "door visibly rotates toward the viewer — so the lockset turns to face the camera and the measurement is "
 "easier to see; the camera itself stays fixed. Throughout, the hook end of the tape at the door edge — "
 "the beginning of the tape — stays fully within the frame, and the tape stays a short span across the "
 "lockset, never extending across the door or onto the glass panel.\n"
 "Maintain continuity in the white door, the stainless steel deadbolt and knob, the yellow-and-black tape "
 "measure, the hands and bare forearm, and the frosted glass panel with blinds.\n"
 "Photoreal Home Depot how-to footage, bright natural 5500K daylight. No on-screen text, no captions, no "
 "watermarks, no added logos, no competitor brands.")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    name, status, secs, size = sv.generate(
        KEY, name="A2_door_motion_v2", mode="ref", prompt=PROMPT, out_dir=OUT,
        images=[os.path.join(KF, "kf1.png"), os.path.join(KF, "kf2.png"), os.path.join(KF, "kf3.png")],
        duration="8", resolution="720p", audio=False, aspect="16:9",
        on_status=lambda st, s: print(f"    {st} ({s}s)", flush=True))
    print(f"[{status}] {name} {secs}s {size//1024}KB\nDONE", flush=True)
