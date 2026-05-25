#!/bin/bash
# One-shot IndexNow ping for all 10 new URLs across Phase 27/28/29
# Run this AFTER deploying the updated robots.txt + verifying key file is reachable
#
# Expected response: HTTP 200 or HTTP 202 = success
# If you get HTTP 403: key file isn't reachable — re-check deployment
# If you get HTTP 422: URL/key host mismatch — re-check the URL list

KEY="cebd0f739339490594ae3738f31b5ed0"
HOST="www.re9guide.it.com"
KEY_LOCATION="https://${HOST}/${KEY}.txt"
ENDPOINT="https://api.indexnow.org/indexnow"

URLS=(
  # Phase 27 — 4 articles × 2 lang
  "https://www.re9guide.it.com/puzzle-box-solutions.html"
  "https://www.re9guide.it.com/ko/puzzle-box-solutions.html"
  "https://www.re9guide.it.com/organless-corpse-puzzle.html"
  "https://www.re9guide.it.com/ko/organless-corpse-puzzle.html"
  "https://www.re9guide.it.com/blood-specimen-analyzer.html"
  "https://www.re9guide.it.com/ko/blood-specimen-analyzer.html"
  "https://www.re9guide.it.com/re9-eye-spy-charm-explained.html"
  "https://www.re9guide.it.com/ko/re9-eye-spy-charm-explained.html"
  # Phase 28 — flagship endings
  "https://www.re9guide.it.com/re9-all-endings-explained.html"
  "https://www.re9guide.it.com/ko/re9-all-endings-explained.html"
  # Phase 29 — vs RE8 comparison
  "https://www.re9guide.it.com/re9-vs-re8-village-which-to-play.html"
  "https://www.re9guide.it.com/ko/re9-vs-re8-village-which-to-play.html"
  # Updated index + sitemap (signal to Bing these changed)
  "https://www.re9guide.it.com/index.html"
  "https://www.re9guide.it.com/ko/index.html"
  "https://www.re9guide.it.com/sitemap.xml"
)

echo "→ Submitting ${#URLS[@]} URLs to IndexNow API..."

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

RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
  -X POST "${ENDPOINT}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "${PAYLOAD}")

BODY=$(echo "$RESPONSE" | sed '$d')
STATUS=$(echo "$RESPONSE" | tail -n 1 | sed 's/HTTP_STATUS://')

case "$STATUS" in
  200) echo "✓ HTTP 200 — Accepted. Bing will start crawling within 24h." ;;
  202) echo "✓ HTTP 202 — Accepted (processing). Same effect as 200." ;;
  400) echo "✗ HTTP 400 — Bad request. Check JSON syntax." ;;
  403) echo "✗ HTTP 403 — Key file not found at ${KEY_LOCATION}. Verify deployment." ;;
  422) echo "✗ HTTP 422 — URL/key host mismatch. All URLs must be on ${HOST}." ;;
  429) echo "✗ HTTP 429 — Rate limited. Wait 1 hour, try again." ;;
  *)   echo "? HTTP ${STATUS} — Unexpected response: ${BODY}" ;;
esac

echo ""
echo "After successful submission:"
echo "  1. Wait 24-48 hours"
echo "  2. Check BWT 'Suggestions' page — IndexNow High warning should disappear"
echo "  3. Check BWT 'URL Submission' page — quota should appear"
echo "  4. Check BWT 'Search Performance' — impressions should start rising in 3-7 days"
