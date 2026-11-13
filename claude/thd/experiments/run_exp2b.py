#!/usr/bin/env python3
"""Exp 2b — 3 wide beat keyframes (v2: body covered, real hands kept) as ordered keyframes."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv
BASE = "/home/colligo/THD_How_to_Install_a_Door_Lock"
OUT = os.path.join(BASE, "work", "gen_round12b")
PL = os.path.join(BASE, "work", "plates")
KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))

PROMPT = (
 "Use @Image1, @Image2 and @Image3 as keyframes in that order.\n"
 "Use @Image1 as the first frame. This first frame defines the wide medium composition, camera position "
 "and scene, and the first beat of a door-lock measurement.\n"
 "@Image2 defines the second keyframe: the second beat of the measurement.\n"
 "Use @Image3 as the last frame: the third beat of the measurement.\n"
 "The shot passes through the states defined by @Image1, @Image2 and @Image3 in order with continuous "
 "natural hand and arm motion, keeping the SAME fixed wide camera framing throughout; do not zoom or "
 "pan.\n"
 "A man in a plain denim shirt with a red carpenter's pencil over his ear performs the measurement with "
 "a yellow tape measure at the lockset; his hands and the tape follow the positions shown in the "
 "keyframes, and the tape stays a short span across the lockset without extending across the door onto "
 "the glass.\n"
 "Maintain continuity in the white door, the stainless steel deadbolt and knob, the yellow-and-black "
 "tape measure, the man's denim shirt, the plant, and the frosted glass panel. Photoreal Home Depot "
 "how-to footage, bright natural 5500K daylight. Plain denim, no text or logo. No on-screen text, no "
 "captions, no watermarks, no added logos, no competitor brands.")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    name, status, secs, size = sv.generate(
        KEY, name="exp2b_wide_beatframes", mode="ref", prompt=PROMPT, out_dir=OUT,
        images=[os.path.join(PL, "wbeat1_v2.png"), os.path.join(PL, "wbeat2_v2.png"),
                os.path.join(PL, "wbeat3_v2.png")],
        duration="8", resolution="720p", audio=False, aspect="16:9",
        on_status=lambda st, s: print(f"    {st} ({s}s)", flush=True))
    print(f"[{status}] {name} {secs}s {size//1024}KB\nDONE", flush=True)
