#!/usr/bin/env python3
"""Exp 2d — same as exp2c (wide v2 keyframes, 16s) but with an explicit beat1 'tape ends at plate right edge' constraint."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv
BASE = "/home/colligo/THD_How_to_Install_a_Door_Lock"
OUT = os.path.join(BASE, "work", "gen_round14")
PL = os.path.join(BASE, "work", "plates")
KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))

PROMPT = (
 "Use @Image1, @Image2 and @Image3 as keyframes in that order. Keep a fixed WIDE medium camera framing "
 "for the entire shot; do not zoom or pan.\n"
 "Use @Image1 as the first frame — MEASUREMENT 1: the man holds the yellow tape horizontally across the "
 "round stainless knob plate, exactly as in @Image1. The tape ends AT the right edge of the round knob "
 "plate and stays that short — the yellow blade must NOT extend past the right edge of the plate toward "
 "the glass at any point during this beat.\n"
 "@Image2 defines the second keyframe — MEASUREMENT 2: he holds the tape from the edge of the door across "
 "to the left edge of the knob plate, measuring that distance.\n"
 "Use @Image3 as the last frame — MEASUREMENT 3: he holds the tape across the narrow EDGE of the door, "
 "from the front face to the back face of the door, measuring the door's thickness.\n"
 "The shot moves slowly and clearly through these THREE DIFFERENT measurements in order, settling briefly "
 "on each so all three read distinctly, with continuous natural hand and arm motion. A man in a plain "
 "denim shirt with a red carpenter's pencil over his ear performs them and stays visible in the wide shot; "
 "in every beat the tape stays a short span at the lockset and never sprawls across the door onto the "
 "glass panel.\n"
 "Maintain continuity in the white door, the stainless steel deadbolt and knob, the yellow-and-black tape "
 "measure, the man's denim shirt, the plant, and the frosted glass panel. Photoreal Home Depot how-to "
 "footage, bright natural 5500K daylight. Plain denim, no text or logo. No on-screen text, no captions, "
 "no watermarks, no added logos, no competitor brands.")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    name, status, secs, size = sv.generate(
        KEY, name="exp2d_wide_16s_beat1fix", mode="ref", prompt=PROMPT, out_dir=OUT,
        images=[os.path.join(PL, "wbeat1_v2.png"), os.path.join(PL, "wbeat2_v2.png"),
                os.path.join(PL, "wbeat3_v2.png")],
        duration="16", resolution="720p", audio=False, aspect="16:9",
        on_status=lambda st, s: print(f"    {st} ({s}s)", flush=True))
    print(f"[{status}] {name} {secs}s {size//1024}KB\nDONE", flush=True)
