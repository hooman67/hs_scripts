#!/usr/bin/env python3
"""Spot index for the Makita Brand/CPT storyboard deck (39-page THD preread). One entry per SPOT."""
import json, os
REPO=os.path.dirname(os.path.abspath(__file__))
spots=[
 {"id":"brand_30_bbb","section":"BRAND","dur":30,"title":"Bigger. Better. Best.","intro_page":4,"boards":[5,6,7,8,9],"shots":"101-126",
  "trades":["Staircase (fine woodwork)","Commercial building frame (metal framing)","Park patio (concrete)"],
  "tools":["36V LXT Plunge Saw+vac+track","18V LXT Compact Router","18V LXT 2pc Combo Kit","36V LXT 9\" Power Cutter","18V LXT 7/8\" SDS Rotary Hammer","18V LXT Blower","MakTrak"],
  "pros":["CARLOS","VINCENT","ALEX"]},
 {"id":"brand_15_staysharp","section":"BRAND","dur":15,"title":"Stay Sharp","intro_page":11,"boards":[12,13],"shots":"201-212",
  "trades":["Drywall cut / remodel"],"tools":["18V Cut-Out Saw","12V max CXT Green Laser Level","36V LXT Vacuum","MakTrak"],"pros":["(unnamed remodeler)"]},
 {"id":"brand_15_doneright","section":"BRAND","dur":15,"title":"Done Right","intro_page":14,"boards":[15,16],"shots":"301-311",
  "trades":["Concrete post install"],"tools":["18V LXT 7/8\" SDS Rotary Hammer","18V LXT Impact Wrench","18V LXT Blower","MakTrak"],"pros":["CARLOS"]},
 {"id":"cpt_30_neversettle","section":"CPT","dur":30,"title":"Never Settle","intro_page":18,"boards":[19,20,21,22,23],"shots":"401-424",
  "trades":["House frame (rough woodwork)"],"tools":["36V LXT 7-1/4\" Circular Saw","18V LXT Compact One-Handed Recipro Saw","18V LXT Recipro Saw","18V 3-1/2\" Framing Nailer","18V LXT 3-1/4\" Planer","18V LXT Blower","18V LXT Radio","MakTrak"],"pros":["LAUREN","DERIK","VINCENT"]},
 {"id":"cpt_15_neversettle_cut","section":"CPT","dur":15,"title":"Never Settle (cut-down)","intro_page":25,"boards":[26,27,28],"shots":"501-518",
  "trades":["House frame"],"tools":["36V LXT 7-1/4\" Circular Saw","18V 3-1/2\" Framing Nailer","18V LXT Blower","Job Site Radio","MakTrak"],"pros":["LAUREN"]},
 {"id":"cpt_15_details","section":"CPT","dur":15,"title":"All in the Details","intro_page":29,"boards":[30,31],"shots":"601-611",
  "trades":["Shower tile (studio remodel)"],"tools":["18V LXT 2pc Combo Kit","18V LXT Angle Grinder","12V max CXT Green Laser Level","MakTrak"],"pros":["(unnamed tile pro)"]},
 {"id":"cpt_06_madeforyou","section":"CPT","dur":6,"title":"Made For You","intro_page":33,"boards":[34],"shots":"701-706",
  "trades":["Combo-kit versatility"],"tools":["18V LXT 2pc Combo Kit"],"pros":["(unnamed pro)"]},
 {"id":"cpt_06_mostdemanding","section":"CPT","dur":6,"title":"The Most Demanding","intro_page":35,"boards":[36],"shots":"801-807",
  "trades":["Angle grinder (tile/metal/weld)"],"tools":["18V LXT Angle Grinder","MakTrak"],"pros":["(unnamed pro)"]},
 {"id":"cpt_06_hitthemark","section":"CPT","dur":6,"title":"Hit The Mark","intro_page":37,"boards":[38],"shots":"901-905",
  "trades":["Concrete forms (circular saw)"],"tools":["36V LXT 7-1/4\" Rear Handle Circular Saw"],"pros":["(unnamed pro)"]},
]
deck={"deck":"Makita Brand + CPT Storyboards (THD Preread, 2024-07-24)","pages":39,"n_spots":len(spots),
 "campaign_taglines":["Makita. Built to be the best.","When it calls for the best, call on Makita.","Bigger. Better. Best."],
 "note":"Hand-drawn storyboard sketch frames (grey marker + red camera-move arrows). Makita power-tool brand/CPT commercials.",
 "spots":spots}
json.dump(deck,open(os.path.join(REPO,"spots.json"),"w"),indent=1)
print(len(spots),"spots,", sum(1 for s in spots for _ in [0]))
for s in spots: print(f"  {s['section']:5} :{s['dur']:>2}  {s['title']:26} pages {s['boards']}")
