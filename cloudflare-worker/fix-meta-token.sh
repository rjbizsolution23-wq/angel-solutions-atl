#!/usr/bin/env zsh
# ============================================================
# Angel Solutions ATL — Fix META_PAGE_ACCESS_TOKEN
# Usage:
#   zsh fix-meta-token.sh 'EAA...'
# ============================================================
set -euo pipefail

cd "$(dirname "$0")"

PAGE_ID="107318795356062"
PAGE_NAME="Angel Solutions ATL"
IG_ID="17841417063408906"
IG_HANDLE="jordynnpatrice"
CALLBACK="https://angel-solutions-webhook.rickjefferson.workers.dev/webhook"
VERIFY="ANGEL_SOLUTIONS_VERIFY_TOKEN_2026"
WORKER="https://angel-solutions-webhook.rickjefferson.workers.dev"
DEBUG_SECRET="ANGEL_SOLUTIONS_SECURE_DEBUG_2026"

echo "════════════════════════════════════════════════════════"
echo " Angel Solutions ATL — Meta token repair"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Correct Page:  $PAGE_NAME ($PAGE_ID)"
echo "Instagram IG:  @$IG_HANDLE ($IG_ID)"
echo "Callback URL:  $CALLBACK"
echo "Verify token:  $VERIFY"
echo ""

if [[ "${1:-}" == "" ]]; then
  echo "USAGE:"
  echo "  zsh fix-meta-token.sh 'EAAxxxx...your_token...'"
  echo ""
  echo "Current live status:"
  curl -sS -m 20 "$WORKER/api/meta-status?secret=$DEBUG_SECRET" || true
  echo ""
  exit 1
fi

TOKEN="$1"
# strip whitespace / newlines / quotes if pasted messily
TOKEN="${TOKEN//$'\n'/}"
TOKEN="${TOKEN//$'\r'/}"
TOKEN="${TOKEN// /}"
TOKEN="${TOKEN//\'/}"
TOKEN="${TOKEN//\"/}"

if [[ ${#TOKEN} -lt 40 ]]; then
  echo "ERROR: Token looks too short (len=${#TOKEN}). Paste the full EAA... token."
  exit 1
fi

echo "Token length: ${#TOKEN}"
echo "Validating against Graph API..."

ME_JSON=$(curl -sS -m 25 -G "https://graph.facebook.com/v19.0/me" \
  --data-urlencode "fields=id,name" \
  --data-urlencode "access_token=${TOKEN}" || true)

if [[ -z "${ME_JSON// /}" ]]; then
  echo "ERROR: Empty response from Facebook. Check network / token paste."
  exit 2
fi

echo "Graph /me raw: $ME_JSON"

# Validate JSON + identity
python3 -c '
import json, sys
page_id = sys.argv[1]
raw = sys.argv[2]
try:
    d = json.loads(raw)
except Exception as e:
    print("ERROR: Facebook did not return JSON:", raw[:300])
    sys.exit(2)
if d.get("error"):
    print("TOKEN INVALID:", d["error"].get("message"))
    sys.exit(2)
print("Token identity: %s (%s)" % (d.get("name"), d.get("id")))
if str(d.get("id")) != page_id:
    print("NOTE: this is not the Page id yet (likely system/user token). Will try to extract Page token...")
' "$PAGE_ID" "$ME_JSON"

PAGE_TOKEN="$TOKEN"
USER_ID=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1]).get("id",""))' "$ME_JSON")

if [[ "$USER_ID" != "$PAGE_ID" ]]; then
  echo "Looking up Page token for $PAGE_ID ..."
  ACC=$(curl -sS -m 25 -G "https://graph.facebook.com/v19.0/me/accounts" \
    --data-urlencode "fields=id,name,access_token" \
    --data-urlencode "limit=100" \
    --data-urlencode "access_token=${TOKEN}" || true)

  EXTRACTED=$(python3 -c '
import json, sys
pid = sys.argv[1]
raw = sys.argv[2]
d = json.loads(raw)
if d.get("error"):
    print("", end="")
    sys.stderr.write("accounts error: %s\n" % d["error"].get("message"))
    sys.exit(0)
for p in d.get("data") or []:
    if str(p.get("id")) == pid and p.get("access_token"):
        print(p["access_token"])
        break
' "$PAGE_ID" "$ACC")

  if [[ -n "${EXTRACTED:-}" ]]; then
    PAGE_TOKEN="$EXTRACTED"
    echo "Extracted Page access token (len ${#PAGE_TOKEN})"
  else
    # Maybe system user can hit page access_token field directly
    PAGE_JSON=$(curl -sS -m 25 -G "https://graph.facebook.com/v19.0/${PAGE_ID}" \
      --data-urlencode "fields=id,name,access_token" \
      --data-urlencode "access_token=${TOKEN}" || true)
    EXTRACTED2=$(python3 -c '
import json,sys
d=json.loads(sys.argv[1])
print(d.get("access_token") or "")
if d.get("error"):
    sys.stderr.write("page probe: %s\n" % d["error"].get("message"))
' "$PAGE_JSON")
    if [[ -n "${EXTRACTED2:-}" ]]; then
      PAGE_TOKEN="$EXTRACTED2"
      echo "Extracted Page token from page node (len ${#PAGE_TOKEN})"
    else
      echo "Could not extract a separate Page token."
      echo "Will install the token you provided as-is (works if Graph /me is already the page or system user can call /me/messages)."
      echo "Accounts/page response summary:"
      python3 -c '
import json,sys
for label, raw in [("accounts", sys.argv[1]), ("page", sys.argv[2])]:
  try:
    d=json.loads(raw)
  except Exception:
    print(label, "non-json", raw[:200]); continue
  if d.get("error"):
    print(label, "error:", d["error"].get("message"))
  elif "data" in d:
    print(label, "pages:")
    for p in d.get("data") or []:
      print(" -", p.get("id"), p.get("name"), "token=", bool(p.get("access_token")))
  else:
    print(label, "id=", d.get("id"), "name=", d.get("name"), "token=", bool(d.get("access_token")))
' "$ACC" "$PAGE_JSON"
    fi
  fi
fi

# Final validate page token against page messaging capability
echo ""
echo "Final token check..."
FINAL_ME=$(curl -sS -m 25 -G "https://graph.facebook.com/v19.0/me" \
  --data-urlencode "fields=id,name" \
  --data-urlencode "access_token=${PAGE_TOKEN}")
echo "Final /me: $FINAL_ME"
python3 -c '
import json,sys
d=json.loads(sys.argv[1])
if d.get("error"):
    print("FINAL TOKEN INVALID:", d["error"].get("message"))
    sys.exit(2)
print("OK to install: %s (%s)" % (d.get("name"), d.get("id")))
' "$FINAL_ME"

echo ""
echo "Writing META_PAGE_ACCESS_TOKEN to Cloudflare Worker secret..."
# Write token to a temp file (more reliable than shell pipes for wrangler)
TOKEN_FILE="$(mktemp)"
printf '%s' "$PAGE_TOKEN" > "$TOKEN_FILE"
# Confirm file length matches token
FILE_LEN=$(wc -c < "$TOKEN_FILE" | tr -d ' ')
echo "Temp token file bytes: $FILE_LEN (expected ${#PAGE_TOKEN})"
if [[ "$FILE_LEN" != "${#PAGE_TOKEN}" ]]; then
  echo "ERROR: token file length mismatch"
  rm -f "$TOKEN_FILE"
  exit 4
fi

npx wrangler secret put META_PAGE_ACCESS_TOKEN < "$TOKEN_FILE"
rm -f "$TOKEN_FILE"

echo "Deploying worker..."
npx wrangler deploy

echo "Waiting 3s for secret propagation..."
sleep 3

echo "Re-subscribing page webhooks..."
curl -sS -m 45 -X POST "$WORKER/api/meta-subscribe?secret=$DEBUG_SECRET" || true
echo ""

echo "Final worker status:"
STATUS=$(curl -sS -m 45 "$WORKER/api/meta-status?secret=$DEBUG_SECRET" || true)
echo "$STATUS"
echo ""

# Hard fail if still expired/invalid
if echo "$STATUS" | python3 -c 'import sys,json
raw=sys.stdin.read()
try:
  d=json.loads(raw)
except Exception:
  print("WARN: could not parse status JSON"); sys.exit(0)
tok=(d.get("checks") or {}).get("token") or {}
if not tok.get("ok"):
  print("ERROR: Worker still reports invalid token:", tok.get("error"))
  print("Re-run this script with a fresh system-user token.")
  sys.exit(5)
print("SUCCESS: Worker token is valid for", tok.get("name"), tok.get("id"))
'; then
  :
fi

echo ""
echo "Done. Test: send FB/IG DM, then: npx wrangler tail"
