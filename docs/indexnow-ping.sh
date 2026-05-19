#!/bin/bash
# IndexNow ping script for re9guide.it.com
# Usage:
#   ./indexnow-ping.sh                          # ping all sitemap URLs
#   ./indexnow-ping.sh <url1> <url2> ...        # ping specific URLs
#
# Reference: https://www.bing.com/indexnow/getstarted
# Key file:   https://www.re9guide.it.com/cebd0f739339490594ae3738f31b5ed0.txt
#             (file content = key itself, hosted at site root)

KEY="cebd0f739339490594ae3738f31b5ed0"
HOST="www.re9guide.it.com"
KEY_LOCATION="https://${HOST}/${KEY}.txt"
ENDPOINT="https://api.indexnow.org/indexnow"

# Collect URLs to submit
if [ $# -gt 0 ]; then
  # Use args
  URLS=("$@")
else
  # Auto-extract from sitemap.xml (must be in same dir as this script)
  SITEMAP="$(dirname "$0")/../sitemap.xml"
  if [ ! -f "$SITEMAP" ]; then
    echo "✗ sitemap.xml not found at $SITEMAP"
    exit 1
  fi
  mapfile -t URLS < <(grep -oE '<loc>https://[^<]+</loc>' "$SITEMAP" | sed -E 's|</?loc>||g')
fi

if [ ${#URLS[@]} -eq 0 ]; then
  echo "✗ No URLs to submit"
  exit 1
fi

echo "→ Submitting ${#URLS[@]} URL(s) to IndexNow..."

# Build JSON payload
JSON_LIST=$(printf '"%s",' "${URLS[@]}" | sed 's/,$//')
PAYLOAD=$(cat <<EOF
{
  "host": "${HOST}",
  "key": "${KEY}",
  "keyLocation": "${KEY_LOCATION}",
  "urlList": [${JSON_LIST}]
}
EOF
)

# Submit
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
  -X POST "${ENDPOINT}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "${PAYLOAD}")

BODY=$(echo "$RESPONSE" | sed '$d')
STATUS=$(echo "$RESPONSE" | tail -n 1 | sed 's/HTTP_STATUS://')

case "$STATUS" in
  200) echo "✓ Accepted (HTTP 200) — Bing will crawl the URLs soon." ;;
  202) echo "✓ Accepted (HTTP 202) — submitted, waiting for processing." ;;
  400) echo "✗ HTTP 400 — bad request. Check JSON / key format." ;;
  403) echo "✗ HTTP 403 — key file not found or doesn't match. Verify ${KEY_LOCATION}" ;;
  422) echo "✗ HTTP 422 — URL/key mismatch. Are all URLs on host ${HOST}?" ;;
  429) echo "✗ HTTP 429 — rate limited. Try again later." ;;
  *)   echo "? HTTP $STATUS — response: $BODY" ;;
esac
