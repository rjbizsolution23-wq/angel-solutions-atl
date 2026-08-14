#!/usr/bin/env zsh
# ============================================================
# Angel Solutions ATL — Set Cloudflare Secrets + Deploy
# Run this from your terminal:  zsh deploy-secrets.sh
# ============================================================
set -euo pipefail

WORKER_DIR="$(dirname "$0")/cloudflare-worker"
cd "$WORKER_DIR"

echo "🔐 Setting Cloudflare Worker secrets..."

# --- Real secrets (ready to go) ---
echo '8291323937b56cec3edab60fc9f72a9a' | npx wrangler secret put META_APP_SECRET
echo 'ANGEL_SOLUTIONS_VERIFY_TOKEN_2026' | npx wrangler secret put META_VERIFY_TOKEN
echo '4762116:ebcba757acecde41bbacaae8a41a2387' | npx wrangler secret put MANYCHAT_API_KEY
echo 'pit-c612b415-89da-40c4-85ee-60247ef49777' | npx wrangler secret put GHL_API_KEY

# --- ⚠️ PAGE TOKEN (CRITICAL — expires if user token) ---
# Correct Page: Angel Solutions ATL (107318795356062)
# Instagram: @jordynnpatrice (17841417063408906)
# Prefer Business System User token (never expires).
#
# Fast path:
#   zsh cloudflare-worker/fix-meta-token.sh 'EAA...'
#
# Or uncomment and paste page token:
# echo 'PASTE_YOUR_PAGE_ACCESS_TOKEN_HERE' | npx wrangler secret put META_PAGE_ACCESS_TOKEN

# Get OPENROUTER_API_KEY from: openrouter.ai/keys
# Uncomment and paste your real key below:
# echo 'PASTE_YOUR_OPENROUTER_KEY_HERE' | npx wrangler secret put OPENROUTER_API_KEY

echo ""
echo "⚠️  If META_PAGE_ACCESS_TOKEN is expired, bot drafts replies but cannot SEND."
echo "    Check: curl -s 'https://angel-solutions-webhook.rickjefferson.workers.dev/api/meta-status?secret=ANGEL_SOLUTIONS_SECURE_DEBUG_2026'"
echo "    Fix:   zsh cloudflare-worker/fix-meta-token.sh 'EAA...'"
echo ""
echo "🚀 Deploying worker..."
npx wrangler deploy

echo ""
echo "✅ Done! Worker deployed to:"
echo "   https://angel-solutions-webhook.rickjefferson.workers.dev"
echo ""
echo "📋 Meta webhook config"
echo "   Callback URL: https://angel-solutions-webhook.rickjefferson.workers.dev/webhook"
echo "   Verify token: ANGEL_SOLUTIONS_VERIFY_TOKEN_2026"
echo "   Page ID:      107318795356062 (Angel Solutions ATL)"
echo "   Objects:      page (messages, feed) + instagram (messages)"
