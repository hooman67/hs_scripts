#!/usr/bin/env bash
set -euo pipefail

root=/home/colligo/hs_scripts/claude/3d_research/FFDY-8454
blender=/mnt/localssd/blender-poc/blender-5.2.2-linux-x64/blender
source_blend="$root/blender/laundry_sink_components_v4_image7_corrected_hooman_added_motion.blend"
renderer="$root/scripts/render_blockout_clip.py"
out="$root/renders/seedance_blockouts"

render_clip() {
  local name="$1"
  local start="$2"
  local end="$3"
  local lens="$4"
  local speed="$5"
  local frames="$out/${name}_frames"

  "$blender" --background "$source_blend" --python "$renderer" -- \
    "$start" "$end" "$frames" "$lens"

  ffmpeg -y -loglevel error -framerate 24 -start_number "$start" \
    -i "$frames/frame_%04d.png" -vf "setpts=${speed}*PTS,fps=24" -an \
    -c:v libx264 -pix_fmt yuv420p -movflags +faststart "$out/${name}.mp4"
}

render_clip shot02_1A 1 48 55 1.0
render_clip shot04 48 96 55 1.0
render_clip shot05 96 192 55 1.0
render_clip shot06 192 216 65 2.0
render_clip shot07A 216 278 55 1.0
render_clip shot07B 278 324 55 1.0
render_clip shot08 324 348 35 2.0

ffprobe -v error -show_entries format=filename,duration,size \
  -of csv=p=0 "$out"/shot*.mp4
