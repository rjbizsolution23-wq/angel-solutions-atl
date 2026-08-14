/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - PUBLIC COMMENT MODERATION LAYER
 * =====================================================================
 * Auto-hides spam/competition and drafts compliant public replies
 * to comments on Facebook & Instagram before directing them to DMs.
 * =====================================================================
 */

import { normalizeText } from "./keyword-engine.js";

/**
 * Checks if a comment is spam, offensive, or contains a competitor link
 * @param {string} text 
 * @returns {{isSpam: boolean, reason: string|null}}
 */
export function analyzeCommentSafety(text) {
  const norm = normalizeText(text);

  const offensiveWords = ["scam", "fraud", "shitty", "bitch", "fucking", "scammer", "liar", "fake"];
  const competitorKeywords = ["use my guy", "whatsapp +1", "telegram", "contact me", "dm for fix", "i got mine from"];

  if (offensiveWords.some(word => norm.includes(word))) {
    return { isSpam: true, reason: "offensive_language" };
  }

  if (competitorKeywords.some(kw => norm.includes(kw))) {
    return { isSpam: true, reason: "spam_competitor_link" };
  }

  return { isSpam: false, reason: null };
}

/**
 * Executes a hide action on Meta Graph API
 * @param {string} commentId 
 * @param {string} accessToken 
 * @returns {Promise<boolean>} success
 */
export async function hideCommentOnMeta(commentId, accessToken) {
  try {
    const url = `https://graph.facebook.com/v21.0/${commentId}`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        is_hidden: true,
        access_token: accessToken
      })
    });

    const data = await response.json();
    return !!data.success;
  } catch (error) {
    console.error(`Error hiding comment ${commentId}:`, error);
    return false;
  }
}

/**
 * Sends a public reply comment to Meta Graph API
 * @param {string} commentId 
 * @param {string} messageText 
 * @param {string} accessToken 
 * @returns {Promise<boolean>} success
 */
export async function replyToCommentOnMeta(commentId, messageText, accessToken) {
  try {
    const url = `https://graph.facebook.com/v21.0/${commentId}/comments`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: messageText,
        access_token: accessToken
      })
    });

    const data = await response.json();
    return !!data.id;
  } catch (error) {
    console.error(`Error replying to comment ${commentId}:`, error);
    return false;
  }
}

/**
 * Generates a warm, professional, premium public comment reply
 * @param {string} username 
 * @param {string} intent 
 * @returns {string} public reply template
 */
export function generatePublicReply(username, intent) {
  const handles = username ? `@${username} ` : "";
  return `${handles}Thanks for reaching out! I just sent you a DM. Please check your messages so we can get started! 😊`;
}

/**
 * Sends a private DM reply to a public comment on Meta Graph API
 * @param {string} commentId 
 * @param {string} messageText 
 * @param {string} accessToken 
 * @param {string} pageId 
 * @returns {Promise<boolean>} success
 */
export async function sendPrivateReplyToCommentOnMeta(commentId, messageText, accessToken, pageId) {
  try {
    const url = `https://graph.facebook.com/v21.0/${pageId}/messages`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        recipient: { comment_id: commentId },
        message: { text: messageText },
        access_token: accessToken
      })
    });

    const data = await response.json();
    if (!data.message_id) {
      console.error(`Error sending private reply for comment ${commentId}:`, data);
    }
    return !!data.message_id;
  } catch (error) {
    console.error(`Error sending private reply for comment ${commentId}:`, error);
    return false;
  }
}
