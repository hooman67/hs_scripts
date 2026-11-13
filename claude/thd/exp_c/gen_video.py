#!/usr/bin/env python3
"""Exp C video gen. args: NAME MODE PLATE  (PROMPT via env)"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import seedance_video as sv

KEY = sv.resolve_key(key_file=os.path.expanduser("~/hs_scripts/claude/thd/creds.txt"))
OUTDIR = "/home/colligo/THD_How_to_Install_a_Door_Lock/work/gen_round4C"
PLATES = "/home/colligo/THD_How_to_Install_a_Door_Lock/work/plates"
os.makedirs(OUTDIR, exist_ok=True)

NAME = sys.argv[1]
MODE = sys.argv[2]
PLATE = os.path.join(PLATES, sys.argv[3])
PROMPT = os.environ["PROMPT"]

kw = dict(name=NAME, mode=MODE, prompt=PROMPT, out_dir=OUTDIR, images=[PLATE],
          duration="8", resolution="720p", audio=False,
          on_status=lambda st, s: print(NAME, st, s, flush=True))
if MODE == "ref":
    kw["aspect"] = "16:9"
r = sv.generate(KEY, **kw)
print(NAME, "RESULT", r, flush=True)
