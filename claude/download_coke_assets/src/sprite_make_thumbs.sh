#!/bin/bash
# Convert all Sprite images to JPEG thumbnails (max 1200px) for the HTML gallery.
# Streams: S3 orig_assets/ → ImageMagick → S3 html_gallery/
#
# Idempotent: skips files that already exist in html_gallery/.
#
# Usage:
#   ./src/sprite_make_thumbs.sh           # convert all
#   CONCURRENCY=8 ./src/sprite_make_thumbs.sh

set -uo pipefail
cd "$(dirname "$0")/.."
source aws_creds.env

BUCKET="${S3_BUCKET:-foundry-tccc-enterprise-adobe-assets}"
SRC_PREFIX="${SRC_PREFIX:-dam_assets_downloaded_by_hs_sprite/orig_assets}"
DST_PREFIX="${DST_PREFIX:-dam_assets_downloaded_by_hs_sprite/html_gallery}"
REGION="${AWS_REGION:-us-west-2}"
CONCURRENCY="${CONCURRENCY:-8}"
MAX_DIM="${MAX_DIM:-1200}"
QUALITY="${QUALITY:-82}"

# Read existing thumbnails so we can skip
EXISTING_LIST=/tmp/sprite_thumbs_existing.txt
echo "→ Listing existing thumbnails..."
aws s3 ls "s3://${BUCKET}/${DST_PREFIX}/" --recursive --region "$REGION" 2>/dev/null \
  | awk '{print $4}' > "$EXISTING_LIST" || true
echo "  ${EXISTING_LIST}: $(wc -l < "$EXISTING_LIST") entries"

# Build list of (dam_path, dest_key) pairs
python3 - <<PYEOF > /tmp/sprite_convert_jobs.txt
import json, os
existing = set(open("$EXISTING_LIST").read().splitlines())
manifest = json.load(open("sprite_image_manifest.json"))
for a in manifest:
    rel = a["damPath"].replace("/content/dam/", "")
    src_key = "${SRC_PREFIX}/" + rel
    # Always output .jpg; preserve folder structure under html_gallery/
    base, _ = os.path.splitext(rel)
    dst_key = "${DST_PREFIX}/" + base + ".jpg"
    if dst_key in existing:
        continue
    print(f"{src_key}\\t{dst_key}")
PYEOF

TOTAL=$(wc -l < /tmp/sprite_convert_jobs.txt | tr -d ' ')
echo "→ Jobs to convert: $TOTAL"
[ "$TOTAL" = "0" ] && { echo "Nothing to do."; exit 0; }

START=$(date +%s)
DONE_FILE=/tmp/sprite_convert_done.count
FAIL_FILE=/tmp/sprite_convert_fail.count
echo 0 > "$DONE_FILE"
echo 0 > "$FAIL_FILE"

convert_one() {
  local src_key="$1"
  local dst_key="$2"
  local tmp="/tmp/sprite_thumb_$$_${RANDOM}"
  if aws s3 cp "s3://${BUCKET}/${src_key}" - --region "$REGION" --quiet 2>/dev/null \
     | magick - -auto-orient -resize "${MAX_DIM}x${MAX_DIM}>" -quality "$QUALITY" "jpg:${tmp}.jpg" 2>/dev/null \
     && [ -s "${tmp}.jpg" ]; then
    aws s3 cp "${tmp}.jpg" "s3://${BUCKET}/${dst_key}" --content-type "image/jpeg" --region "$REGION" --quiet
    rm -f "${tmp}.jpg"
    flock /tmp/sprite_convert.lock -c "echo $(($(cat "$DONE_FILE") + 1)) > $DONE_FILE"
  else
    rm -f "${tmp}.jpg"
    flock /tmp/sprite_convert.lock -c "echo $(($(cat "$FAIL_FILE") + 1)) > $FAIL_FILE"
    echo "FAIL: $src_key" >&2
  fi
}

export -f convert_one
export BUCKET REGION MAX_DIM QUALITY DONE_FILE FAIL_FILE

# Periodic progress ticker
(
  while true; do
    sleep 30
    D=$(cat "$DONE_FILE" 2>/dev/null || echo 0)
    F=$(cat "$FAIL_FILE" 2>/dev/null || echo 0)
    PCT=$(awk "BEGIN{printf \"%.1f\", ($D/$TOTAL)*100}")
    ELAPSED=$(( $(date +%s) - START ))
    echo "── ${ELAPSED}s | ${D}/${TOTAL} (${PCT}%) | fail=${F} ──"
  done
) &
TICKER=$!

cat /tmp/sprite_convert_jobs.txt \
  | xargs -P "$CONCURRENCY" -I{} bash -c '
      pair="$1"
      src=$(echo "$pair" | cut -f1)
      dst=$(echo "$pair" | cut -f2)
      convert_one "$src" "$dst"
    ' _ {}

kill "$TICKER" 2>/dev/null

D=$(cat "$DONE_FILE")
F=$(cat "$FAIL_FILE")
ELAPSED=$(( $(date +%s) - START ))
echo ""
echo "✅ Done in ${ELAPSED}s. Converted: ${D}, Failed: ${F}, Total: ${TOTAL}"
