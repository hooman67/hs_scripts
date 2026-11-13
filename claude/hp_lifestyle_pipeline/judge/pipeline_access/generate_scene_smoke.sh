#!/usr/bin/env bash
set -euo pipefail

BASE="${HP_PIPELINE_BASE:-https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8016.or2.colligo.dev}"
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
RUN_ROOT="${1:-$SCRIPT_DIR/../local_runs}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
RUN_DIR="$RUN_ROOT/$STAMP"
mkdir -p "$RUN_DIR"

COOKIE=$(mktemp)
trap 'rm -f "$COOKIE"' EXIT

cat > "$RUN_DIR/request.json" <<'JSON'
{
  "digitalTwinId": "cashmere_x",
  "cameraId": "Front_CloseUp",
  "prompt": "A laptop on a warm wooden cafe table near a window, soft daylight."
}
JSON

CSRF=$(curl -fsS -c "$COOKIE" "$BASE/api/credentials" | jq -er '.csrfToken')

curl -fsS -b "$COOKIE" \
  -H "Origin: $BASE" \
  -H "x-hp12-csrf: $CSRF" \
  -H "Content-Type: application/json" \
  --data-binary @"$RUN_DIR/request.json" \
  "$BASE/api/generate" > "$RUN_DIR/submit_response.json"

STATUS_URL=$(jq -er '.statusUrl' "$RUN_DIR/submit_response.json")
IMAGE_URL=$(jq -er '.imageUrl' "$RUN_DIR/submit_response.json")
printf '%s\n' "$BASE$STATUS_URL" > "$RUN_DIR/status_url.txt"
printf '%s\n' "$BASE$IMAGE_URL" > "$RUN_DIR/image_url.txt"

for ((i=1; i<=360; i++)); do
  curl -fsS "$BASE$STATUS_URL" > "$RUN_DIR/status_latest.json"
  jq -c --argjson poll "$i" '{poll:$poll,done,stages}' "$RUN_DIR/status_latest.json" >> "$RUN_DIR/status_history.ndjson"
  if jq -e '.done' "$RUN_DIR/status_latest.json" >/dev/null; then
    jq -e '
      .stages.hero.status == "done" and
      .stages.scene.status == "done" and
      .stages.scene.has_image and
      .stages.ibl.status == "skipped" and
      .stages.backplate.status == "skipped" and
      .stages.recomposite.status == "skipped" and
      .stages.relight.status == "skipped"
    ' "$RUN_DIR/status_latest.json" >/dev/null || {
      jq '.stages' "$RUN_DIR/status_latest.json" >&2
      exit 1
    }
    cp "$RUN_DIR/status_latest.json" "$RUN_DIR/final_status.json"
    curl -fsS "$BASE$IMAGE_URL" -o "$RUN_DIR/generated.png"
    sha256sum "$RUN_DIR/generated.png" > "$RUN_DIR/generated.png.sha256"
    file "$RUN_DIR/generated.png"
    printf 'Job: %s\nStatus: %s%s\nImage: %s%s\n' \
      "$(jq -r '.jobId' "$RUN_DIR/final_status.json")" "$BASE" "$STATUS_URL" "$BASE" "$IMAGE_URL"
    exit 0
  fi
  sleep 5
done

printf 'Polling timed out. Resume at %s%s; do not resubmit blindly.\n' "$BASE" "$STATUS_URL" >&2
exit 1
