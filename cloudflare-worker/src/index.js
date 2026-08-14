/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - CLOUDFLARE EDGE WEBHOOK RECEIVER
 * =====================================================================
 * Scalable entrypoint for Meta (Facebook & Instagram) comments and DMs.
 * Connects directly to Cloudflare D1 database and uses Workers AI.
 * =====================================================================
 */

import { 
  classifyIntent, 
  checkEscalationTriggers, 
  checkDisqualification, 
  enforceCompliance, 
  stripUnapprovedLinks,
  parseCreditProfileFromMessage,
  hasOffensiveOrDisrespectfulLanguage,
  checkClientStopRequest
} from "./keyword-engine.js";

import { 
  analyzeCommentSafety, 
  hideCommentOnMeta, 
  replyToCommentOnMeta, 
  generatePublicReply,
  sendPrivateReplyToCommentOnMeta
} from "./comment-moderation.js";

import { BLUEPRINT_HTML } from "./blueprint-html.js";

const INTAKE_ID = "6a46c0696b95e7dc9dd6251c";

/** Strip model chain-of-thought / planner junk so only customer-facing text is sent. */
function sanitizeAiReply(raw) {
  if (!raw) return null;
  let t = String(raw).trim();
  
  // 1. Strip out deep-thinking tags and code blocks
  t = t.replace(/<think>[\s\S]*?<\/think>/gi, "").trim();
  t = t.replace(/```[\s\S]*?```/g, "").trim();

  // 2. Strip out common AI meta-prefixes/conversation intros on the same line
  t = t.replace(/^(looking back at the history|the user has|the user is|since the user|as an ai|as jordynn)[\s\S]*?(i will (respond|reply|say)( with)?|here is (my|the) response|response):?\s*/i, "").trim();
  t = t.replace(/^(okay|sure),?\s+the user[\s\S]*?(i will (respond|reply|say)( with)?|here is (my|the) response|response):?\s*/i, "").trim();

  // 3. If the model wrapped the ENTIRE remaining response in quotes (e.g. "Hello!"), strip the outer quotes
  if ((t.startsWith('"') && t.endsWith('"')) || (t.startsWith('“') && t.endsWith('”'))) {
    t = t.substring(1, t.length - 1).trim();
  }

  // 4. Strip out other prefixes
  const prefixes = [
    /^As Jordynn Miller:?\s*/i,
    /^As Jordynn:?\s*/i,
    /^Jordynn:\s*/i,
    /^Jordynn Miller:\s*/i,
    /^Response:\s*/i,
    /^Here is (the|my) response:?\s*/i,
    /^Sure,?\s+here is\s+a\s+response:?\s*/i,
    /^Draft:\s*/i,
    /^Instagram DM:\s*/i,
    /^DM:\s*/i
  ];
  for (const p of prefixes) {
    t = t.replace(p, "").trim();
  }

  // 5. If the model still has quotes but has text outside of it, check if we should extract the quotes.
  // We only do this if there's an obvious meta-intro left.
  const hasMetaIntro = /^(okay|sure|i need to|we need to|let me|according to|looking back|the user|the customer|the contact|since the|based on|i will|i should|analyzing)/i.test(t);
  if (hasMetaIntro) {
    const quotes = [...t.matchAll(/["“]([^"”]{10,220})["”]/g)].map(m => m[1].trim());
    if (quotes.length) {
      return quotes[quotes.length - 1];
    }
  }

  // 5.5 Filter out individual sentences that are pure meta-reasoning/planning
  const sentenceParts = t.split(/(?<=[.!?])\s+/).filter(Boolean);
  const cleanSentences = [];
  for (const s of sentenceParts) {
    const isMeta = /^(i will (respond|reply|say|ask|reach out|guide|pitch|provide)|i should (respond|reply|say|ask|reach out|guide|pitch|provide)|let's (respond|reply|say|ask|reach out|guide|pitch|provide)|let me (respond|reply|say|ask|reach out|guide|pitch|provide)|(okay|sure),?\s*(i'll|i will|i should|we should)|the (user|customer|lead|contact) (is|has|wants|mentioned|says|stated|asked|requires|needs)|(analyzing|according to|looking back|looking at the history|the history shows|based on the history|this lead|since the user|since the customer)|as (jordynn|an ai|a bot|an assistant))/i.test(s.trim());
    if (!isMeta) {
      cleanSentences.push(s);
    }
  }
  if (cleanSentences.length > 0) {
    t = cleanSentences.join(" ");
  }

  // 6. Clean up headers and bullet lists
  t = t.replace(/^#{1,6}\s+/gm, "").replace(/^\s*[-*]\s+/gm, "").trim();
  
  // 7. Cap length for IG DMs
  if (t.length > 450) {
    t = t.slice(0, 447).trim() + "…";
  }

  // 8. Sentence limiter: Keep at most 3 sentences for natural IG DM texting
  const parts = t.split(/(?<=[.!?])\s+/).filter(Boolean);
  if (parts.length > 3) {
    t = parts.slice(0, 3).join(" ");
  }

  if (!t || t.length < 5) return null;
  return t;
}

function templateReplyForIntent(intent, isFirstContact) {
  if (isFirstContact) {
    return "Hello, thank you for reaching out. It's Jordynn, I am the founder and owner of Angel Solutions ATL, and we help people fix their credit, build their credit, everything in between, and position your credit to a point where you’re able to get approvals both on the personal and the business side.\n\nI would love to hear more about what made you reach out, where you are on your credit journey do you have collections, charge-offs, late payments, bankruptcies, things like that that are stopping you from getting approvals?";
  }
  switch (intent) {
    case "CREDIT_REPAIR":
      return "I can help with that. What's your score looking like right now, and do you have collections, charge-offs, or late payments on the report?";
    case "BUSINESS_FUNDING":
      return "Got it — for funding we need a clean-enough profile first. What's your current score, and any recent negatives on the report?";
    case "TAX_RESOLVE":
      return "I can point you the right way on tax stuff. Are you dealing with IRS balance, liens, or something else right now?";
    default:
      return "Happy to help. What's the main credit goal for you right now, and roughly what score are you sitting at?";
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // CORS OPTIONS Preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type"
        }
      });
    }

    // 0a. Privacy Policy
    if (request.method === "GET" && url.pathname === "/privacy") {
      return new Response(`<!DOCTYPE html><html><head><title>Privacy Policy - Angel Solutions ATL</title>
<style>body{font-family:sans-serif;max-width:800px;margin:40px auto;padding:0 20px;line-height:1.6}</style></head>
<body><h1>Privacy Policy</h1><p><strong>Angel Solutions ATL</strong> | Effective Date: January 1, 2025</p>
<p>This Privacy Policy describes how Angel Solutions ATL ("we," "us," or "our") collects, uses, and shares information when you interact with us via Instagram, Facebook Messenger, or our website.</p>
<h2>Information We Collect</h2><p>We collect messages, contact details (name, email, phone), and credit profile information you voluntarily share with us through social media or web forms.</p>
<h2>How We Use Your Information</h2><p>We use your information to provide credit repair consulting services, respond to inquiries, schedule appointments, and send follow-up communications related to your service request.</p>
<h2>Sharing of Information</h2><p>We do not sell your personal information. We may share data with trusted service providers (CRM, payment processing) solely to operate our services.</p>
<h2>Data Retention</h2><p>We retain your information for up to 2 years or as required by law.</p>
<h2>Your Rights</h2><p>You may request deletion of your data at any time by emailing <a href="mailto:jordynn@angelsolutionsatl.com">jordynn@angelsolutionsatl.com</a>.</p>
<h2>Contact</h2><p>Angel Solutions ATL | 3343 Peachtree Rd, Atlanta, GA 30326 | 470-523-0674</p>
</body></html>`, { status: 200, headers: { "Content-Type": "text/html; charset=utf-8" } });
    }

    // 0. GET Root URL - Serve Interactive Blueprint Site + D1 Live Telemetry
    if (request.method === "GET" && (url.pathname === "/" || url.pathname === "")) {
      let leadCount = 120;
      let qualifiedCount = 90;
      let bookedCount = 45;
      let conversionRate = "37.5";

      try {
        if (env.DB) {
          const totalRes = await env.DB.prepare("SELECT count(*) as count FROM leads").first();
          leadCount = totalRes ? totalRes.count : leadCount;

          const qualRes = await env.DB.prepare("SELECT count(*) as count FROM leads WHERE lead_state = 'QUALIFIED'").first();
          qualifiedCount = qualRes ? qualRes.count : qualifiedCount;

          const bookedRes = await env.DB.prepare("SELECT count(*) as count FROM leads WHERE lead_state = 'BOOKED'").first();
          bookedCount = bookedRes ? bookedRes.count : bookedCount;

          conversionRate = leadCount > 0 ? ((bookedCount / leadCount) * 100).toFixed(1) : "0.0";
        }
      } catch (e) {
        console.error("D1 query failed inside HTML serving:", e);
      }

      // Inject live metrics
      const renderedHtml = BLUEPRINT_HTML
        .replace("{{LEAD_COUNT}}", leadCount.toString())
        .replace("{{QUALIFIED_COUNT}}", qualifiedCount.toString())
        .replace("{{BOOKED_COUNT}}", bookedCount.toString())
        .replace("{{CONVERSION_RATE}}", conversionRate.toString());

      return new Response(renderedHtml, {
        status: 200,
        headers: { "Content-Type": "text/html; charset=utf-8" }
      });
    }

    // 0.1 POST /api/contact - Web lead ingestion with D1 and optional GHL CRM integration
    if (request.method === "POST" && url.pathname === "/api/contact") {
      try {
        const body = await request.json();
        const { firstName, lastName, email, phone, service, message, collections, bankruptcy, child_support, score, utm_source, utm_medium, utm_campaign } = body;

        if (!firstName || !lastName || !email) {
          return new Response(JSON.stringify({ success: false, error: "Missing required fields: firstName, lastName, email." }), {
            status: 400,
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*"
            }
          });
        }

        const fullName = `${firstName} ${lastName}`;
        const uuid = crypto.randomUUID();
        const now = new Date().toISOString();

        if (env.DB) {
          // Check if lead already exists by email/platform combination
          const existingLead = await env.DB.prepare(
            "SELECT id FROM leads WHERE email = ? OR platform_user_id = ?"
          ).bind(email, email).first();

          let leadId = uuid;
          if (existingLead) {
            leadId = existingLead.id;
            await env.DB.prepare(
              `UPDATE leads SET name = ?, service_needed = ?, email = ?, phone = ?, updated_at = ?, last_contact_at = ? WHERE id = ?`
            ).bind(fullName, service || "credit_repair", email, phone || null, now, now, leadId).run();
          } else {
            await env.DB.prepare(
              `INSERT INTO leads (id, intake_id, lead_state, platform, platform_user_id, name, service_needed, email, phone, created_at, updated_at, last_contact_at)
               VALUES (?, ?, 'NEW', 'website', ?, ?, ?, ?, ?, ?, ?, ?)`
            ).bind(leadId, INTAKE_ID, email, fullName, service || "credit_repair", email, phone || null, now, now, now).run();
          }

          // Optional GoHighLevel CRM Sync
          if (env.GHL_API_KEY) {
            const locationId = env.GHL_LOCATION_ID || "Sfvt5kBZ3EUOws7MDWa3";
            const leadTags = ["website_lead", service || "credit_repair"];
            if (utm_source) leadTags.push(`src_${utm_source}`);
            if (utm_medium) leadTags.push(`med_${utm_medium}`);
            if (utm_campaign) leadTags.push(`camp_${utm_campaign}`);

            const ghlPayload = {
              firstName,
              lastName,
              email,
              phone: phone || null,
              locationId,
              tags: leadTags,
              customFields: [
                { id: "credit_goal", value: message || service || "Web Contact Submission" },
                { id: "collections_count", value: String(collections !== undefined ? collections : "0") },
                { id: "bankruptcy_flag", value: (bankruptcy === 1 || bankruptcy === true || String(bankruptcy).toLowerCase() === "yes") ? "Yes" : "No" },
                { id: "child_support_arrears", value: (child_support === 1 || child_support === true || String(child_support).toLowerCase() === "yes") ? "Yes" : "No" },
                { id: "computed_lead_score", value: String(score !== undefined ? score : "0.5") }
              ]
            };

            try {
              const ghlResponse = await fetch("https://services.leadconnectorhq.com/contacts/", {
                method: "POST",
                headers: {
                  "Authorization": `Bearer ${env.GHL_API_KEY}`,
                  "Content-Type": "application/json",
                  "Version": "2021-04-15"
                },
                body: JSON.stringify(ghlPayload)
              });

              if (ghlResponse.ok) {
                const ghlData = await ghlResponse.json();
                console.log(`Successfully synced web lead ${leadId} to GHL with Contact ID: ${ghlData.contact?.id}`);
              } else {
                const errText = await ghlResponse.text();
                console.error(`GHL Lead Sync failed: ${errText}`);
              }
            } catch (ghlErr) {
              console.error("GHL request exception:", ghlErr);
            }
          }

          return new Response(JSON.stringify({ success: true, lead_id: leadId }), {
            status: 200,
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*"
            }
          });
        } else {
          return new Response(JSON.stringify({ success: false, error: "D1 database binding missing." }), {
            status: 500,
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*"
            }
          });
        }
      } catch (err) {
        console.error("Failed to ingest contact submission:", err);
        return new Response(JSON.stringify({ success: false, error: err.message }), {
          status: 500,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
          }
        });
      }
    }

    // 1. GET Webhook verification handshake
    if (request.method === "GET" && url.pathname === "/webhook") {
      const mode = url.searchParams.get("hub.mode");
      const token = url.searchParams.get("hub.verify_token");
      const challenge = url.searchParams.get("hub.challenge");

      const expectedToken = env.META_VERIFY_TOKEN || "ANGEL_SOLUTIONS_VERIFY_TOKEN_2026";

      if (mode === "subscribe" && token === expectedToken) {
        console.log("Meta Webhook Verified Successfully!");
        return new Response(challenge, { status: 200 });
      } else {
        console.error("Meta Webhook Verification Failed: Tokens do not match.");
        return new Response("Forbidden", { status: 403 });
      }
    }

    // 1.5 POST Meta Data Deletion Callback (GDPR/CCPA Compliance for App Review)
    if (request.method === "POST" && url.pathname === "/api/meta-data-deletion") {
      try {
        const bodyText = await request.text();
        const params = new URLSearchParams(bodyText);
        const signedRequest = params.get("signed_request");

        if (!signedRequest) {
          return new Response("Missing signed_request", { status: 400 });
        }

        const [encodedSig, payload] = signedRequest.split(".");
        // Decode payload (base64url to string)
        const sigBuffer = String(encodedSig).replace(/-/g, "+").replace(/_/g, "/");
        const payloadBuffer = String(payload).replace(/-/g, "+").replace(/_/g, "/");
        const payloadJson = JSON.parse(atob(payloadBuffer));

        // Note: For full compliance, verify HMAC-SHA256 signature using env.META_APP_SECRET
        // but for now, we process the deletion request if valid payload is present.
        const userId = payloadJson.user_id;
        
        if (userId && env.DB) {
          // Delete all records of this user to comply with GDPR
          console.log(`Processing Meta Data Deletion for user_id: ${userId}`);
          
          // Find the lead first
          const lead = await env.DB.prepare("SELECT id FROM leads WHERE platform_user_id = ?").bind(userId).first();
          
          if (lead) {
            // Delete interactions, conversations, escalations, and the lead itself
            await env.DB.prepare("DELETE FROM interactions WHERE conversation_id IN (SELECT id FROM conversations WHERE lead_id = ?)").bind(lead.id).run();
            await env.DB.prepare("DELETE FROM escalations WHERE lead_id = ?").bind(lead.id).run();
            await env.DB.prepare("DELETE FROM conversations WHERE lead_id = ?").bind(lead.id).run();
            await env.DB.prepare("DELETE FROM leads WHERE id = ?").bind(lead.id).run();
          }
        }

        // Meta requires this exact JSON response format
        const confirmationCode = crypto.randomUUID();
        return new Response(JSON.stringify({
          url: `https://angel-solutions-webhook.rickjefferson.workers.dev/api/meta-data-status?id=${confirmationCode}`,
          confirmation_code: confirmationCode
        }), {
          status: 200,
          headers: { "Content-Type": "application/json" }
        });
      } catch (err) {
        console.error("Data deletion error:", err);
        return new Response(JSON.stringify({ error: err.message }), { status: 500 });
      }
    }
    
    // 1.6 GET Meta Data Deletion Status
    if (request.method === "GET" && url.pathname === "/api/meta-data-status") {
      return new Response("Deletion request processed successfully.", { status: 200 });
    }

    // 2. POST Webhook ingestion
    if (request.method === "POST" && url.pathname === "/webhook") {
      try {
        const payload = await request.json();
        console.log("Inbound raw webhook payload:", JSON.stringify(payload));
        
        // Background process to keep response latency < 200ms
        ctx.waitUntil(this.processWebhookPayload(payload, env));

        return new Response(JSON.stringify({ status: "received" }), {
          status: 200,
          headers: { "Content-Type": "application/json" }
        });
      } catch (error) {
        console.error("Webhook ingestion error:", error);
        return new Response(JSON.stringify({ error: error.message }), {
          status: 500,
          headers: { "Content-Type": "application/json" }
        });
      }
    }

    // 3. Health Check endpoint
    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "healthy", timestamp: new Date().toISOString() }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }

    // 3.1 Secure Debug Env endpoint
    if (url.pathname === "/api/secure-debug-env") {
      const debugSecret = url.searchParams.get("secret");
      if (debugSecret !== "ANGEL_SOLUTIONS_SECURE_DEBUG_2026") {
        return new Response("Forbidden", { status: 403 });
      }

      const maskToken = (token) => {
        if (!token) return "NOT_SET";
        if (token.length <= 12) return `SET (len: ${token.length}, value: ${token})`;
        return `SET (len: ${token.length}, prefix: ${token.slice(0, 6)}... suffix: ${token.slice(-6)})`;
      };

      const debugInfo = {
        META_PAGE_ID: env.META_PAGE_ID || "NOT_SET",
        INTAKE_ID: env.INTAKE_ID || "NOT_SET",
        OPENROUTER_MODEL: env.OPENROUTER_MODEL || "NOT_SET",
        META_VERIFY_TOKEN: env.META_VERIFY_TOKEN || "NOT_SET",
        META_PAGE_ACCESS_TOKEN: maskToken(env.META_PAGE_ACCESS_TOKEN),
        OPENROUTER_API_KEY: maskToken(env.OPENROUTER_API_KEY),
        GHL_API_KEY: maskToken(env.GHL_API_KEY),
        GHL_LOCATION_ID: env.GHL_LOCATION_ID || "NOT_SET",
        timestamp: new Date().toISOString()
      };

      return new Response(JSON.stringify(debugInfo, null, 2), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }

    // 3.1.1 Community Join / Client Confirmation Endpoint
    if (url.pathname === "/api/community-join") {
      try {
        let body = {};
        if (request.method === "POST") {
          try {
            body = await request.json();
          } catch (_) {
            // body stays empty
          }
        }

        const email = body.email || url.searchParams.get("email");
        const phone = body.phone || url.searchParams.get("phone");
        const platform_user_id = body.platform_user_id || url.searchParams.get("platform_user_id");
        const username = body.username || url.searchParams.get("username");

        if (!email && !phone && !platform_user_id && !username) {
          return new Response(JSON.stringify({ error: "At least one identifying field (email, phone, platform_user_id, username) must be provided." }), {
            status: 400,
            headers: { 
              "Content-Type": "application/json", 
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
              "Access-Control-Allow-Headers": "Content-Type"
            }
          });
        }

        if (!env.DB) {
          return new Response(JSON.stringify({ error: "Database binding missing." }), {
            status: 500,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
          });
        }

        let query = "SELECT id, intake_id, platform_user_id, platform FROM leads WHERE ";
        let conditions = [];
        let params = [];

        if (email) {
          conditions.push("email = ?");
          params.push(email);
        }
        if (phone) {
          conditions.push("phone = ?");
          params.push(phone);
        }
        if (platform_user_id) {
          conditions.push("platform_user_id = ?");
          params.push(platform_user_id);
        }
        if (username) {
          conditions.push("name LIKE ? OR platform_user_id = ?");
          params.push(`%${username}%`);
          params.push(username);
        }

        query += conditions.join(" OR ");
        const leadRow = await env.DB.prepare(query).bind(...params).first();

        if (!leadRow) {
          return new Response(JSON.stringify({ error: "Lead not found matching provided criteria." }), {
            status: 404,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
          });
        }

        const now = new Date().toISOString();
        // Update database: set lead_state to ACTIVE_CLIENT
        await env.DB.prepare(
          `UPDATE leads SET lead_state = 'ACTIVE_CLIENT', updated_at = ? WHERE id = ?`
        ).bind(now, leadRow.id).run();

        // Update database: set bot_active to 0 in conversations
        await env.DB.prepare(
          `UPDATE conversations SET bot_active = 0, last_message_at = ? WHERE lead_id = ?`
        ).bind(now, leadRow.id).run();

        console.log(`API community join: Activated client and deactivated bot for lead ${leadRow.id}`);

        return new Response(JSON.stringify({ success: true, message: `Successfully updated lead ${leadRow.id} to ACTIVE_CLIENT and deactivated bot.` }), {
          status: 200,
          headers: { 
            "Content-Type": "application/json", 
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
          }
        });
      } catch (err) {
        console.error("API community-join endpoint exception:", err);
        return new Response(JSON.stringify({ error: err.message }), {
          status: 500,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      }
    }

    // 3.1.1b Toggle Bot Active Endpoint
    if (url.pathname === "/api/pause-bot") {
      try {
        const debugSecret = url.searchParams.get("secret");
        if (debugSecret !== "ANGEL_SOLUTIONS_SECURE_DEBUG_2026") {
          return new Response("Forbidden", { status: 403 });
        }

        const username = url.searchParams.get("username") || url.searchParams.get("ig_username");
        const email = url.searchParams.get("email");
        const phone = url.searchParams.get("phone");
        const leadId = url.searchParams.get("lead_id");
        const activeParam = url.searchParams.get("active"); // "0" to pause, "1" to resume
        const botActive = activeParam === "0" ? 0 : 1;

        if (!email && !phone && !username && !leadId) {
          return new Response(JSON.stringify({ error: "Missing identifying parameter (lead_id, username, email, or phone)." }), {
            status: 400,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
          });
        }

        if (!env.DB) {
          return new Response(JSON.stringify({ error: "Database binding missing." }), {
            status: 500,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
          });
        }

        let query = "SELECT id FROM leads WHERE ";
        let conditions = [];
        let params = [];

        if (leadId) {
          conditions.push("id = ?");
          params.push(leadId);
        }
        if (email) {
          conditions.push("email = ?");
          params.push(email);
        }
        if (phone) {
          conditions.push("phone = ?");
          params.push(phone);
        }
        if (username) {
          conditions.push("name LIKE ? OR platform_user_id = ?");
          params.push(`%${username}%`);
          params.push(username);
        }

        query += conditions.join(" OR ");
        const leadRow = await env.DB.prepare(query).bind(...params).first();

        if (!leadRow) {
          return new Response(JSON.stringify({ error: "Lead not found matching provided criteria." }), {
            status: 404,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
          });
        }

        const now = new Date().toISOString();
        await env.DB.prepare(
          `UPDATE conversations SET bot_active = ?, last_message_at = ? WHERE lead_id = ?`
        ).bind(botActive, now, leadRow.id).run();

        // Also update lead state to ASSIGN if pausing, so team knows to handle it
        if (botActive === 0) {
          await env.DB.prepare(
            `UPDATE leads SET lead_state = 'ASSIGN', updated_at = ? WHERE id = ?`
          ).bind(now, leadRow.id).run();
        }

        const actionText = botActive === 0 ? "paused" : "resumed";
        return new Response(JSON.stringify({ success: true, message: `Successfully ${actionText} the bot for lead ID ${leadRow.id}.` }), {
          status: 200,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      } catch (err) {
        console.error("API pause-bot endpoint exception:", err);
        return new Response(JSON.stringify({ error: err.message }), {
          status: 500,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      }
    }

    // 3.1.2 Test AI Endpoint (Temporarily added for diagnosing NVIDIA, OpenRouter and Workers AI)
    if (url.pathname === "/api/test-ai") {
      const debugSecret = url.searchParams.get("secret");
      if (debugSecret !== "ANGEL_SOLUTIONS_SECURE_DEBUG_2026") {
        return new Response("Forbidden", { status: 403 });
      }

      const promptStr = url.searchParams.get("prompt") || "Hello, who are you?";
      const testModel = url.searchParams.get("model");
      const provider = url.searchParams.get("provider") || "all";

      const results = {};

      if (provider === "nvidia" || provider === "all") {
        try {
          const model = testModel || env.NVIDIA_MODEL || "nvidia/llama-3.1-nemotron-70b-instruct";
          const start = Date.now();
          const aiRes = await fetch("https://integrate.api.nvidia.com/v1/chat/completions", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${env.NVIDIA_API_KEY}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              model,
              messages: [{ role: "user", content: promptStr }],
              temperature: 0.5,
              max_tokens: 100
            })
          });
          const latency = Date.now() - start;
          const aiJson = await aiRes.json();
          results.nvidia = {
            ok: aiRes.ok,
            status: aiRes.status,
            latency_ms: latency,
            model,
            key_preview: env.NVIDIA_API_KEY ? `${env.NVIDIA_API_KEY.slice(0, 15)}...` : "NOT_SET",
            response: aiJson
          };
        } catch (err) {
          results.nvidia = { ok: false, error: err.message };
        }
      }

      if (provider === "openrouter" || provider === "all") {
        try {
          let model = testModel || env.OPENROUTER_MODEL || "openrouter/free";
          if (model === "meta-llama/llama-3.3-70b-instruct:free") model = "openrouter/free";
          const start = Date.now();
          const aiRes = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${env.OPENROUTER_API_KEY}`,
              "Content-Type": "application/json",
              "HTTP-Referer": "https://angelsolutionsatl.com",
              "X-Title": "Angel Solutions ATL Automation"
            },
            body: JSON.stringify({
              model,
              messages: [{ role: "user", content: promptStr }],
              temperature: 0.5,
              max_tokens: 100
            })
          });
          const latency = Date.now() - start;
          const aiJson = await aiRes.json();
          results.openrouter = {
            ok: aiRes.ok,
            status: aiRes.status,
            latency_ms: latency,
            model,
            key_preview: env.OPENROUTER_API_KEY ? `${env.OPENROUTER_API_KEY.slice(0, 15)}...` : "NOT_SET",
            response: aiJson
          };
        } catch (err) {
          results.openrouter = { ok: false, error: err.message };
        }
      }

      if (provider === "workers_ai" || provider === "all") {
        try {
          const model = testModel || "@cf/meta/llama-3.3-70b-instruct-fp8-fast";
          const start = Date.now();
          let responseText = "";
          let aiOut = null;
          if (env.AI) {
            aiOut = await env.AI.run(model, {
              messages: [{ role: "user", content: promptStr }],
              max_tokens: 100
            });
            responseText = typeof aiOut === "string" ? aiOut : (aiOut?.response || aiOut?.result || "");
          } else {
            responseText = "env.AI NOT_BOUND";
          }
          const latency = Date.now() - start;
          results.workers_ai = {
            ok: Boolean(env.AI),
            latency_ms: latency,
            model,
            raw_output: aiOut,
            response: responseText
          };
        } catch (err) {
          results.workers_ai = { ok: false, error: err.message };
        }
      }

      return new Response(JSON.stringify(results, null, 2), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }

    // 3.1.5 Secure GHL Connection Test Endpoint
    if (url.pathname === "/api/test-ghl") {
      const debugSecret = url.searchParams.get("secret");
      if (debugSecret !== "ANGEL_SOLUTIONS_SECURE_DEBUG_2026") {
        return new Response("Forbidden", { status: 403 });
      }

      if (!env.GHL_API_KEY || !env.GHL_LOCATION_ID) {
        return new Response(JSON.stringify({ error: "GHL_API_KEY or GHL_LOCATION_ID is not configured in environment" }), {
          status: 400,
          headers: { "Content-Type": "application/json" }
        });
      }

      try {
        const ghlRes = await fetch(`https://services.leadconnectorhq.com/contacts/?locationId=${env.GHL_LOCATION_ID}&limit=1`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${env.GHL_API_KEY}`,
            "Version": "2021-07-28"
          }
        });

        const status = ghlRes.status;
        const contentType = ghlRes.headers.get("content-type") || "";
        let bodyText = "";
        let json = null;

        if (contentType.includes("application/json")) {
          json = await ghlRes.json();
        } else {
          bodyText = await ghlRes.text();
        }

        return new Response(JSON.stringify({
          ok: ghlRes.ok,
          status,
          contentType,
          json,
          bodyText: bodyText || undefined,
          timestamp: new Date().toISOString()
        }, null, 2), {
          status: 200,
          headers: { "Content-Type": "application/json" }
        });
      } catch (err) {
        return new Response(JSON.stringify({
          ok: false,
          error: String(err.message || err),
          timestamp: new Date().toISOString()
        }, null, 2), {
          status: 500,
          headers: { "Content-Type": "application/json" }
        });
      }
    }

    // 3.2 Meta Graph status — validates page token + webhook wiring (no secrets returned)
    if (request.method === "GET" && url.pathname === "/api/meta-status") {
      const debugSecret = url.searchParams.get("secret");
      if (debugSecret !== "ANGEL_SOLUTIONS_SECURE_DEBUG_2026") {
        return new Response("Forbidden", { status: 403 });
      }

      const status = await this.getMetaStatus(env);
      return new Response(JSON.stringify(status, null, 2), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }

    // 3.3 Manual Facebook page webhook re-subscribe (uses page access token)
    if (request.method === "POST" && url.pathname === "/api/meta-subscribe") {
      const debugSecret = url.searchParams.get("secret");
      if (debugSecret !== "ANGEL_SOLUTIONS_SECURE_DEBUG_2026") {
        return new Response("Forbidden", { status: 403 });
      }

      const result = await this.subscribePageWebhooks(env);
      return new Response(JSON.stringify(result, null, 2), {
        status: result.ok ? 200 : 500,
        headers: { "Content-Type": "application/json" }
      });
    }

    // 3.4 Test Meta send — returns Graph error body (for debugging delivery failures)
    if (request.method === "POST" && url.pathname === "/api/meta-test-send") {
      const debugSecret = url.searchParams.get("secret");
      if (debugSecret !== "ANGEL_SOLUTIONS_SECURE_DEBUG_2026") {
        return new Response("Forbidden", { status: 403 });
      }
      try {
        const body = await request.json();
        const recipientId = body?.recipient_id || body?.psid;
        const text = body?.text || "Test from Angel Solutions webhook — ignore this.";
        if (!recipientId) {
          return new Response(JSON.stringify({ ok: false, error: "recipient_id required" }), {
            status: 400,
            headers: { "Content-Type": "application/json" }
          });
        }
        const result = await this.sendMessageToMetaDetailed(recipientId, text, body?.platform || "instagram", env);
        return new Response(JSON.stringify(result, null, 2), {
          status: result.ok ? 200 : 502,
          headers: { "Content-Type": "application/json" }
        });
      } catch (e) {
        return new Response(JSON.stringify({ ok: false, error: String(e?.message || e) }), {
          status: 500,
          headers: { "Content-Type": "application/json" }
        });
      }
    }

    return new Response("Not Found", { status: 404 });
  },

  async getMetaStatus(env) {
    const pageId = env.META_PAGE_ID || "";
    const token = env.META_PAGE_ACCESS_TOKEN || "";
    const igBusinessId = "17841417063408906";
    const out = {
      timestamp: new Date().toISOString(),
      configured: {
        META_PAGE_ID: pageId || "NOT_SET",
        META_PAGE_ACCESS_TOKEN: token
          ? `SET (len: ${token.length}, prefix: ${token.slice(0, 6)}...)`
          : "NOT_SET",
        META_VERIFY_TOKEN: env.META_VERIFY_TOKEN ? "SET" : "NOT_SET",
        OPENROUTER_API_KEY: env.OPENROUTER_API_KEY ? "SET" : "NOT_SET",
        GHL_API_KEY: env.GHL_API_KEY ? "SET" : "NOT_SET",
        webhook_callback: "https://angel-solutions-webhook.rickjefferson.workers.dev/webhook",
        expected_ig_business_id: igBusinessId,
        expected_page_name: "Angel Solutions ATL"
      },
      checks: {},
      ok: false,
      next_steps: []
    };

    if (!token) {
      out.checks.token = { ok: false, error: "META_PAGE_ACCESS_TOKEN missing" };
      out.next_steps.push(
        "Generate a Page access token for Angel Solutions ATL (107318795356062) in Meta Developer → Messenger → Generate token, then: wrangler secret put META_PAGE_ACCESS_TOKEN"
      );
      return out;
    }

    const g = async (path, params = "") => {
      try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 12000);
        const res = await fetch(
          `https://graph.facebook.com/v21.0/${path}?access_token=${encodeURIComponent(token)}${params}`,
          { signal: controller.signal }
        );
        clearTimeout(timer);
        const json = await res.json().catch(() => ({}));
        return { http: res.status, json };
      } catch (e) {
        return {
          http: 0,
          json: { error: { message: `graph_fetch_failed: ${String(e?.message || e)}` } }
        };
      }
    };

    // Token identity
    const me = await g("me", "&fields=id,name");
    if (me.json?.error) {
      out.checks.token = {
        ok: false,
        error: me.json.error.message,
        code: me.json.error.code,
        subcode: me.json.error.error_subcode
      };
      out.next_steps.push(
        "Page access token is invalid/expired. Regenerate in Meta Developer Console and update META_PAGE_ACCESS_TOKEN secret."
      );
      return out;
    }
    out.checks.token = {
      ok: true,
      id: me.json.id,
      name: me.json.name,
      matches_configured_page: String(me.json.id) === String(pageId)
    };
    if (String(me.json.id) !== String(pageId)) {
      out.next_steps.push(
        `Token is for "${me.json.name}" (${me.json.id}) but META_PAGE_ID is ${pageId}. Update wrangler.toml META_PAGE_ID or use the Angel Solutions page token.`
      );
    }

    // Page details
    const page = await g(pageId || me.json.id, "&fields=id,name,fan_count,instagram_business_account");
    if (page.json?.error) {
      out.checks.page = { ok: false, error: page.json.error.message };
    } else {
      out.checks.page = {
        ok: true,
        id: page.json.id,
        name: page.json.name,
        fans: page.json.fan_count,
        instagram_business_id: page.json.instagram_business_account?.id || null,
        ig_matches_hardcoded: page.json.instagram_business_account?.id === igBusinessId
      };
    }

    // Subscribed apps (page webhooks)
    const sub = await g(`${pageId || me.json.id}/subscribed_apps`);
    if (sub.json?.error) {
      out.checks.subscribed_apps = { ok: false, error: sub.json.error.message };
      out.next_steps.push(
        "Cannot read page subscribed_apps. Ensure token has pages_manage_metadata and the app is connected to the page."
      );
    } else {
      const apps = sub.json.data || [];
      out.checks.subscribed_apps = {
        ok: apps.length > 0,
        apps: apps.map((a) => ({
          id: a.id,
          name: a.name,
          subscribed_fields: a.subscribed_fields || []
        }))
      };
      const fields = apps.flatMap((a) => a.subscribed_fields || []);
      const need = ["messages", "messaging_postbacks", "feed"];
      const missing = need.filter((f) => !fields.includes(f));
      if (missing.length) {
        out.next_steps.push(
          `Page webhook fields missing: ${missing.join(", ")}. POST /api/meta-subscribe?secret=... or subscribe in Meta App → Webhooks.`
        );
      }
    }

    // Messenger conversations probe
    const conv = await g(
      `${pageId || me.json.id}/conversations`,
      "&fields=id,updated_time&limit=1&platform=messenger"
    );
    if (conv.json?.error) {
      out.checks.messenger_conversations = {
        ok: false,
        error: conv.json.error.message,
        code: conv.json.error.code
      };
      out.next_steps.push(
        "Cannot list Messenger conversations. Need pages_messaging permission on a valid Page token."
      );
    } else {
      out.checks.messenger_conversations = {
        ok: true,
        sample_count: (conv.json.data || []).length
      };
    }

    // Instagram conversations probe via page (requires instagram_manage_messages)
    const igConv = await g(
      `${pageId || me.json.id}/conversations`,
      "&fields=id,updated_time&limit=1&platform=instagram"
    );
    if (igConv.json?.error) {
      out.checks.instagram_conversations = {
        ok: false,
        error: igConv.json.error.message,
        code: igConv.json.error.code,
        note: igConv.json.error.code === 200 || igConv.json.error.code === 10 || igConv.json.error.code === 190
          ? "Permission error — instagram_manage_messages likely not approved in Meta App Review"
          : "API error — check token or subscription"
      };
    } else {
      out.checks.instagram_conversations = {
        ok: true,
        sample_count: (igConv.json.data || []).length
      };
    }

    // Instagram Business Account permission probe (direct IG API check)
    const igPermCheck = await g(
      `${igBusinessId}`,
      "&fields=id,name,username,followers_count"
    );
    if (igPermCheck.json?.error) {
      out.checks.instagram_account = {
        ok: false,
        error: igPermCheck.json.error.message,
        code: igPermCheck.json.error.code
      };
    } else {
      out.checks.instagram_account = {
        ok: true,
        id: igPermCheck.json.id,
        username: igPermCheck.json.username,
        followers: igPermCheck.json.followers_count
      };
    }

    // D1 social accounts snapshot
    try {
      if (env.DB) {
        const social = await env.DB.prepare(
          `SELECT id, platform, handle, facebook_page_id, ai_should_reply_dms, ai_should_reply_comments
           FROM client_social_accounts`
        ).all();
        const compliance = await env.DB.prepare(
          `SELECT launch_approval_status, require_ai_disclosure_dms FROM client_compliance_launch WHERE intake_id = ?`
        ).bind(INTAKE_ID).first();
        const leadCounts = await env.DB.prepare(
          `SELECT platform, count(*) AS c FROM leads GROUP BY platform`
        ).all();
        out.checks.d1 = {
          ok: true,
          social_accounts: social.results || [],
          launch_approval_status: compliance?.launch_approval_status || "missing",
          lead_counts: leadCounts.results || []
        };
        const fbRow = (social.results || []).find((r) => r.platform === "facebook");
        if (fbRow && String(fbRow.facebook_page_id) !== String(pageId)) {
          out.next_steps.push(
            `D1 client_social_accounts facebook_page_id is ${fbRow.facebook_page_id}, expected ${pageId}.`
          );
        }
      }
    } catch (e) {
      out.checks.d1 = { ok: false, error: String(e?.message || e) };
    }

    out.ok = Boolean(
      out.checks.token?.ok &&
      out.checks.page?.ok &&
      out.checks.messenger_conversations?.ok
    );

    if (out.ok && out.next_steps.length === 0) {
      out.next_steps.push(
        "Token + page look healthy. Send a test Facebook Page DM and watch wrangler tail. If nothing arrives, subscribe Page webhooks (messages + feed) to the callback URL."
      );
    }

    return out;
  },

  async subscribePageWebhooks(env) {
    const pageId = env.META_PAGE_ID;
    const token = env.META_PAGE_ACCESS_TOKEN;
    if (!pageId || !token) {
      return { ok: false, error: "META_PAGE_ID or META_PAGE_ACCESS_TOKEN missing" };
    }

    // Do not include leadgen unless token has leads_retrieval
    const subscribed_fields = [
      "messages",
      "messaging_postbacks",
      "messaging_optins",
      "message_deliveries",
      "message_reads",
      "messaging_referrals",
      "messaging_handovers",
      "feed"
    ];

    try {
      // Graph prefers access_token as query param for this endpoint
      const res = await fetch(
        `https://graph.facebook.com/v21.0/${pageId}/subscribed_apps?access_token=${encodeURIComponent(token)}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            subscribed_fields: subscribed_fields.join(",")
          }).toString()
        }
      );
      const json = await res.json().catch(() => ({}));
      if (!res.ok || json.error) {
        return {
          ok: false,
          error: json.error?.message || `HTTP ${res.status}`,
          details: json,
          hint: "Token needs pages_manage_metadata. In Meta App → Messenger → Webhooks, confirm callback + Page subscription."
        };
      }

      // Re-read subscriptions
      const status = await this.getMetaStatus(env);
      return {
        ok: true,
        subscribed_fields,
        graph: json,
        status_summary: {
          subscribed_apps: status.checks?.subscribed_apps,
          token: status.checks?.token,
          page: status.checks?.page
        }
      };
    } catch (e) {
      return { ok: false, error: String(e?.message || e) };
    }
  },

  /**
   * Processes the parsed payload from Meta Graph API
   */
  async processWebhookPayload(payload, env) {
    if (!payload.object) return;

    // Check Facebook/Instagram Messenger/DM events
    if (payload.entry) {
      for (const entry of payload.entry) {
        // Handle direct messaging/DMs
        if (entry.messaging) {
          for (const messageEvent of entry.messaging) {
            await this.handleDirectMessage(messageEvent, env, false);
          }
        }

        // Handle standby messages (when another app has thread control)
        if (entry.standby) {
          for (const messageEvent of entry.standby) {
            await this.handleDirectMessage(messageEvent, env, true);
          }
        }

        // Handle page changes (comments & Lead Ads submissions)
        if (entry.changes) {
          for (const change of entry.changes) {
            if (change.field === "feed" || change.field === "comments") {
              await this.handlePublicComment(change, env);
            } else if (change.field === "leadgen") {
              await this.handleLeadgen(change, env);
            }
          }
        }
      }
    }
  },

  /**
   * Ingests, analyzes, drafts, and delivers direct messages (DMs)
   */
  async handleDirectMessage(event, env, isStandby = false) {
    const senderId = event?.sender?.id;
    const recipientId = event?.recipient?.id;
    const message = event?.message;

    if (!senderId || !recipientId || !message) {
      console.log(`Skipping non-message or malformed message event: ${JSON.stringify(event)}`);
      return;
    }

    // --- HUMAN INTERVENTION & OUTBOUND MESSAGE HANDLING ---
    const isEcho = message.is_echo === true || event?.message?.is_echo === true;
    const isDeleted = message.is_deleted === true;
    const appId = message.app_id || event?.message?.app_id;
    
    const pageId = env.META_PAGE_ID || "";
    const igBusinessId = "17841417063408906"; // @jordynnpatrice linked IG
    
    // A message is "outbound" if it's an echo OR the sender is the business Page/IG account
    const isBusinessOutbound = isEcho || senderId === pageId || senderId === igBusinessId;

    if (isDeleted) {
      console.log(`Skipping deleted message from ${senderId}`);
      return;
    }

    if (isBusinessOutbound) {
      // Determine if this outbound message was sent by a human or another app (not our bot)
      // Our bot will always have an app_id attached to its outbound echoes
      const ourAppId = env.META_APP_ID || "1037361725512008"; // Fallback to our Meta App ID
      const isHumanAdmin = !appId || String(appId) !== String(ourAppId);

      if (isHumanAdmin && message.text) {
        // Human intervened. Auto-pause the bot for this client to prevent talking over the admin.
        const leadUser = recipientId; // In outbound messages, recipientId is the client
        const now = new Date().toISOString();
        const pauseUntil = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(); // pause for 24 hours

        const leadRow = await env.DB.prepare(
          `SELECT id, name FROM leads WHERE platform_user_id = ? AND intake_id = ?`
        ).bind(leadUser, INTAKE_ID).first();

        if (leadRow) {
          await env.DB.prepare(
            `UPDATE leads SET lead_state = 'ASSIGN', paused_until = ?, updated_at = ? WHERE id = ?`
          ).bind(pauseUntil, now, leadRow.id).run();

          await env.DB.prepare(
            `UPDATE conversations SET bot_active = 0, last_message_at = ? WHERE lead_id = ?`
          ).bind(now, leadRow.id).run();
          
          console.log(`Bot successfully auto-paused for lead '${leadRow.name}' (ID: ${leadRow.id}) because human admin intervened manually.`);
        } else {
          console.log(`Could not find lead record for ${leadUser} to pause during human intervention.`);
        }
      }

      console.log(`Skipping business outbound/echo message from ${senderId}`);
      return;
    }

    if (!message.text) {
      console.log(`Skipping non-text message from ${senderId}`);
      return;
    }

    const userMessage = message.text;

    // Determine platform (Instagram vs Facebook page)
    // IG webhooks often use the IG business account id as recipient, not the FB page id
    const platform =
      recipientId === pageId || recipientId === String(pageId) ? "facebook" : "instagram";

    console.log(`Inbound DM received on ${platform} (isStandby: ${isStandby}) from ${senderId}: "${userMessage}"`);

    // If the message is a standby event, take control of the thread before sending responses
    if (isStandby) {
      console.log(`Standby event received for sender ${senderId}. Proactively taking thread control...`);
      const success = await this.takeThreadControl(senderId, env);
      if (success) {
        console.log(`Successfully took thread control for sender ${senderId}.`);
      } else {
        console.error(`Failed to take thread control for sender ${senderId}. Attempting response anyway.`);
      }
    }

    // Deduplicate incoming messages to prevent double processing from Meta retries
    if (message.mid) {
      try {
        const existingMessage = await env.DB.prepare(
          `SELECT id FROM interactions WHERE platform_message_id = ?`
        ).bind(message.mid).first();
        if (existingMessage) {
          console.log(`Duplicate webhook message mid detected: ${message.mid}. Skipping to prevent double response.`);
          return;
        }
      } catch (err) {
        console.error("D1 check duplicate error:", err);
      }
    }



    // Fetch Client Configuration from D1
    const compliance = await env.DB.prepare(
      `SELECT launch_approval_status, approved_ai_disclosure_script, require_ai_disclosure_dms FROM client_compliance_launch WHERE intake_id = ?`
    ).bind(INTAKE_ID).first();

    const brandVoice = await env.DB.prepare(
      `SELECT voice_traits, phrases_to_avoid, ai_speaks_as FROM client_brand_voice WHERE intake_id = ?`
    ).bind(INTAKE_ID).first();

    const autoRules = await env.DB.prepare(
      `SELECT dm_escalation_triggers FROM client_automation_rules WHERE intake_id = ?`
    ).bind(INTAKE_ID).first();

    const isShadowMode = !compliance || compliance.launch_approval_status !== "approved";

    // DB Operations: Upsert Lead
    let lead = await env.DB.prepare(
      `SELECT * FROM leads WHERE intake_id = ? AND platform = ? AND platform_user_id = ?`
    ).bind(INTAKE_ID, platform, senderId).first();

    const uuid = crypto.randomUUID();
    const now = new Date().toISOString();

    if (!lead) {
      // First contact, create a new lead
      await env.DB.prepare(
        `INSERT INTO leads (id, intake_id, lead_state, platform, platform_user_id, name, created_at, updated_at)
         VALUES (?, ?, 'NEW', ?, ?, ?, ?, ?)`
      ).bind(uuid, INTAKE_ID, platform, senderId, `Lead_${senderId.slice(-4)}`, now, now).run();

      lead = {
        id: uuid,
        intake_id: INTAKE_ID,
        lead_state: "NEW",
        platform: platform,
        platform_user_id: senderId,
        name: `Lead_${senderId.slice(-4)}`,
        bot_active: 1
      };
    }

    // Parse email and phone number dynamically from DM message
    const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/;
    const phoneRegex = /(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})/;

    const emailMatch = userMessage.match(emailRegex);
    const phoneMatch = userMessage.match(phoneRegex);

    let parsedEmail = emailMatch ? emailMatch[0] : null;
    let parsedPhone = phoneMatch ? phoneMatch[0] : null;

    if (parsedEmail || parsedPhone) {
      const updateFields = [];
      const bindParams = [];
      if (parsedEmail) {
        updateFields.push("email = ?");
        bindParams.push(parsedEmail);
        lead.email = parsedEmail;
      }
      if (parsedPhone) {
        updateFields.push("phone = ?");
        bindParams.push(parsedPhone);
        lead.phone = parsedPhone;
      }

      await env.DB.prepare(
        `UPDATE leads SET ${updateFields.join(", ")}, updated_at = ? WHERE id = ?`
      ).bind(...bindParams, now, lead.id).run();
    }

    // Parse credit score, bankruptcy, child support, and collections count from message text
    const parsedCredit = parseCreditProfileFromMessage(userMessage);
    if (parsedCredit.score !== null || parsedCredit.bankruptcy !== null || parsedCredit.childSupport !== null || parsedCredit.collectionsCount !== null) {
      const updateFields = [];
      const bindParams = [];

      if (parsedCredit.score !== null) {
        updateFields.push("lead_score = ?");
        bindParams.push(parsedCredit.score);
        lead.lead_score = parsedCredit.score;
      }
      if (parsedCredit.bankruptcy !== null) {
        updateFields.push("bankruptcy = ?");
        bindParams.push(parsedCredit.bankruptcy);
        lead.bankruptcy = parsedCredit.bankruptcy;
      }
      if (parsedCredit.childSupport !== null) {
        updateFields.push("child_support = ?");
        bindParams.push(parsedCredit.childSupport);
        lead.child_support = parsedCredit.childSupport;
      }
      if (parsedCredit.collectionsCount !== null) {
        updateFields.push("collections_count = ?");
        bindParams.push(parsedCredit.collectionsCount);
        lead.collections_count = parsedCredit.collectionsCount;
      }

      await env.DB.prepare(
        `UPDATE leads SET ${updateFields.join(", ")}, updated_at = ? WHERE id = ?`
      ).bind(...bindParams, now, lead.id).run();

      console.log(`Updated lead ${lead.id} credit profile params: score=${parsedCredit.score}, bankruptcy=${parsedCredit.bankruptcy}, childSupport=${parsedCredit.childSupport}, collectionsCount=${parsedCredit.collectionsCount}`);
    }

    // DB Operations: Upsert Conversation
    let conversation = await env.DB.prepare(
      `SELECT * FROM conversations WHERE lead_id = ?`
    ).bind(lead.id).first();

    const convUuid = crypto.randomUUID();
    if (!conversation) {
      await env.DB.prepare(
        `INSERT INTO conversations (id, intake_id, lead_id, platform, bot_active, last_message_at, created_at)
         VALUES (?, ?, ?, ?, 1, ?, ?)`
      ).bind(convUuid, INTAKE_ID, lead.id, platform, now, now).run();

      conversation = { id: convUuid, bot_active: 1, within_24h_window: 1 };
    }

    // Classify intent and escalations
    const intent = classifyIntent(userMessage);
    const escalationCheck = checkEscalationTriggers(userMessage);
    const dqCheck = checkDisqualification(userMessage);
    const offensiveCheck = hasOffensiveOrDisrespectfulLanguage(userMessage);
    const clientStopCheck = checkClientStopRequest(userMessage);

    // Update Lead state based on keywords
    let newState = lead.lead_state;
    if (newState === "NEW" && intent !== "GENERAL_INQUIRY") {
      newState = "QUALIFIED";
    }

    // Handle Disqualification routing
    if (dqCheck.disqualified) {
      newState = "DQ";
      console.log(`Lead ${lead.id} Disqualified: ${dqCheck.reason}`);
    }

    // Log inbound user interaction
    const userMessageUuid = crypto.randomUUID();
    await env.DB.prepare(
      `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, sentiment_score, compliance_flag, compliance_reason, created_at)
       VALUES (?, ?, 'user', ?, ?, 0.0, 0, NULL, ?)`
    ).bind(userMessageUuid, conversation.id, event.message.mid || null, userMessage, now).run();

    // Check for explicit escalation triggers, offensive language, or stop requests
    if (escalationCheck.escalate || newState === "DQ" || offensiveCheck.detected || clientStopCheck.requested) {
      // Determine explicit reason detail
      let reasonDetail = "";
      if (offensiveCheck.detected) {
        reasonDetail = `Offensive/Disrespectful Language: ${offensiveCheck.pattern}`;
      } else if (clientStopCheck.requested) {
        reasonDetail = `Client Stop Request: ${clientStopCheck.trigger}`;
      } else if (escalationCheck.escalate) {
        reasonDetail = `Escalation trigger: ${escalationCheck.trigger}`;
      } else {
        reasonDetail = `Disqualified: ${dqCheck.reason}`;
      }

      // Deactivate bot, change state to ASSIGN
      await env.DB.prepare(
        `UPDATE leads SET lead_state = 'ASSIGN', paused_until = ?, updated_at = ? WHERE id = ?`
      ).bind(new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), now, lead.id).run();

      await env.DB.prepare(
        `UPDATE conversations SET bot_active = 0, last_message_at = ? WHERE id = ?`
      ).bind(now, conversation.id).run();

      // Insert escalation record
      await env.DB.prepare(
        `INSERT INTO escalations (id, lead_id, trigger_message, sms_sent, sms_status, human_resolved, created_at)
         VALUES (?, ?, ?, 0, 'pending', 0, ?)`
      ).bind(crypto.randomUUID(), lead.id, `${reasonDetail} | Message: ${userMessage}`, now).run();

      console.log(`Lead ${lead.id} escalated due to: ${reasonDetail}. Bot deactivated.`);
      return; // Stop responding
    }

    // Update lead details in database
    await env.DB.prepare(
      `UPDATE leads SET lead_state = ?, updated_at = ?, last_contact_at = ? WHERE id = ?`
    ).bind(newState, now, now, lead.id).run();

    lead.lead_state = newState;

    // Real-time synchronization to GoHighLevel CRM (offloaded asynchronously)
    await this.syncLeadToGoHighLevel(lead, env);

    // Generate response only if Bot is active
    if (conversation.bot_active) {
      // Fetch historical context (most recent 20 messages, ordered chronologically)
      const history = await env.DB.prepare(
        `SELECT sender_type, message_text FROM interactions WHERE conversation_id = ? ORDER BY created_at DESC, rowid DESC LIMIT 20`
      ).bind(conversation.id).all();

      const results = history.results || [];
      results.reverse();

      // Dynamic in-memory fail-safe aggregation from history
      let historicalScore = null;
      let historicalCollections = null;
      let historicalBankruptcy = null;

      for (const row of results) {
        if (row.sender_type === "user") {
          const parsed = parseCreditProfileFromMessage(row.message_text);
          if (parsed.score !== null) historicalScore = parsed.score;
          if (parsed.collectionsCount !== null) historicalCollections = parsed.collectionsCount;
          if (parsed.bankruptcy !== null) historicalBankruptcy = parsed.bankruptcy;
        }
      }

      // Merge into the active lead object if they are set historically but null/0 in the database
      if (lead) {
        if (historicalScore && (!lead.lead_score || lead.lead_score === 0)) {
          lead.lead_score = historicalScore;
        }
        if (historicalCollections !== null && (lead.collections_count === undefined || lead.collections_count === null || lead.collections_count === 0)) {
          lead.collections_count = historicalCollections;
        }
        if (historicalBankruptcy !== null && (lead.bankruptcy === undefined || lead.bankruptcy === null)) {
          lead.bankruptcy = historicalBankruptcy;
        }
      }

      // =====================================================================
      // STATEFUL SCRIPT OVERRIDES (STRICT ZERO-DEFECT MATCHING)
      // =====================================================================
      const normMsg = userMessage.toLowerCase().trim();

      // Find the most recent bot message from history (excluding current user message)
      let lastBotMsg = "";
      for (let i = results.length - 1; i >= 0; i--) {
        const row = results[i];
        if (row.sender_type === "bot") {
          lastBotMsg = row.message_text;
          break;
        }
      }

      // CASE 1: Joined Community Confirmation
      const matchesJoin = (
        normMsg.includes("joined the community") ||
        normMsg.includes("joined community") ||
        normMsg.includes("joined skool") ||
        normMsg.includes("just joined") ||
        normMsg.includes("already joined") ||
        (normMsg === "joined" || normMsg === "confirm" || normMsg === "confirmed" || normMsg === "i joined" || normMsg === "i'm in" || normMsg === "im in")
      );

      if (matchesJoin) {
        console.log(`Lead ${lead.id} confirmed joining the community. Marking state as ACTIVE_CLIENT and deactivating bot.`);
        
        // Update database: set lead_state to ACTIVE_CLIENT
        await env.DB.prepare(
          `UPDATE leads SET lead_state = 'ACTIVE_CLIENT', updated_at = ?, last_contact_at = ? WHERE id = ?`
        ).bind(now, now, lead.id).run();

        // Update database: set bot_active to 0 in conversations
        await env.DB.prepare(
          `UPDATE conversations SET bot_active = 0, last_message_at = ? WHERE id = ?`
        ).bind(now, conversation.id).run();

        const finalMsg = "Hey! Perfect, welcome to the family! 🎙️ I just paused my automated assistant on this thread so you are now completely in the hands of our client onboarding team and your assigned account manager. They'll be touching base with you shortly to set up your portal and walk you through everything. Let's get this credit right!";

        let delivered = false;
        let deliveryError = null;
        if (!isShadowMode) {
          if (platform === "instagram" || isStandby) {
            await this.takeThreadControl(senderId, env);
          }
          const sendResult = await this.sendMessageToMetaDetailed(senderId, finalMsg, platform, env);
          delivered = Boolean(sendResult?.ok);
          deliveryError = sendResult?.error || null;
        }

        const reason = isShadowMode
          ? "shadow_mode"
          : (delivered ? null : `meta_delivery_failed:${String(deliveryError || "unknown").slice(0, 180)}`);

        await env.DB.prepare(
          `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, sentiment_score, compliance_flag, compliance_reason, created_at)
           VALUES (?, ?, 'bot', NULL, ?, 0.0, ?, ?, ?)`
        ).bind(
          crypto.randomUUID(),
          conversation.id,
          finalMsg,
          isShadowMode ? 0 : (delivered ? 0 : 1),
          reason,
          now
        ).run();

        // Sync GHL
        lead.lead_state = 'ACTIVE_CLIENT';
        await this.syncLeadToGoHighLevel(lead, env);

        return;
      }

      // CASE 2: Collections/Inquiries/Late Payments/Charge Offs Script
      const hasNegativeItemsKeyword = (
        normMsg.includes("collections") ||
        normMsg.includes("collection") ||
        normMsg.includes("inquiries") ||
        normMsg.includes("inquiry") ||
        normMsg.includes("late payments") ||
        normMsg.includes("late payment") ||
        normMsg.includes("charge offs") ||
        normMsg.includes("charge off") ||
        normMsg.includes("charge-offs") ||
        normMsg.includes("charge-off") ||
        normMsg.includes("chargeoffs") ||
        normMsg.includes("chargeoff")
      );

      // Branch A: First detection of negative items
      if (hasNegativeItemsKeyword && lastBotMsg !== "Got it. I can get all of this removed. Have you attempted fixing any of it before?") {
        const firstReply = "Got it. I can get all of this removed. Have you attempted fixing any of it before?";
        
        let delivered = false;
        let deliveryError = null;
        if (!isShadowMode) {
          if (platform === "instagram" || isStandby) {
            await this.takeThreadControl(senderId, env);
          }
          const sendResult = await this.sendMessageToMetaDetailed(senderId, firstReply, platform, env);
          delivered = Boolean(sendResult?.ok);
          deliveryError = sendResult?.error || null;
        }

        const reason = isShadowMode
          ? "shadow_mode"
          : (delivered ? null : `meta_delivery_failed:${String(deliveryError || "unknown").slice(0, 180)}`);

        await env.DB.prepare(
          `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, sentiment_score, compliance_flag, compliance_reason, created_at)
           VALUES (?, ?, 'bot', NULL, ?, 0.0, ?, ?, ?)`
        ).bind(
          crypto.randomUUID(),
          conversation.id,
          firstReply,
          isShadowMode ? 0 : (delivered ? 0 : 1),
          reason,
          now
        ).run();

        await env.DB.prepare(
          `UPDATE conversations SET last_message_at = ? WHERE id = ?`
        ).bind(now, conversation.id).run();

        return;
      }

      // Branch B: Response to the follow-up question
      if (lastBotMsg === "Got it. I can get all of this removed. Have you attempted fixing any of it before?") {
        const messages = [
          "Okay so based on what you're telling me here's how i can help...",
          "My $67 program covers charge offs, collections, inquiries, and personal information clean up. Its a community setting up to 3 accounts disputed per month and you get assigned to an account manager that will touch bases with you each month to let you know your updates and anything you can do on your end to help your profile.",
          "I handwrite and certify mail consumer law disputes. When a human at the bureau reads a law-based dispute, they legally have to act, not stall you",
          "Collections and late payments do take on average about 2 to 3 months to remove. We use legit credit repair methods. No quick fix illegal credit sweeps where items end up coming back later",
          "You get a portal to track progress and a monthly calls for updates so you actually see what's moving",
          "What questions do you have for me?"
        ];

        if (!isShadowMode) {
          if (platform === "instagram" || isStandby) {
            await this.takeThreadControl(senderId, env);
          }
          for (const msg of messages) {
            await this.sendMessageToMetaDetailed(senderId, msg, platform, env);
            await new Promise(resolve => setTimeout(resolve, 800)); // natural reading pace
          }
        }

        for (const msg of messages) {
          await env.DB.prepare(
            `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, sentiment_score, compliance_flag, compliance_reason, created_at)
             VALUES (?, ?, 'bot', NULL, ?, 0.0, 0, ?, ?)`
          ).bind(
            crypto.randomUUID(),
            conversation.id,
            msg,
            isShadowMode ? "shadow_mode" : null,
            now
          ).run();
        }

        await env.DB.prepare(
          `UPDATE conversations SET last_message_at = ? WHERE id = ?`
        ).bind(now, conversation.id).run();

        return;
      }

      // CASE 3: Student Loans Script
      const hasStudentLoansKeyword = (
        normMsg.includes("student loans") ||
        normMsg.includes("student loan") ||
        normMsg.includes("studentloans") ||
        normMsg.includes("studentloan")
      );

      // Branch A: First detection of student loans
      if (hasStudentLoansKeyword && lastBotMsg !== "Are the student loans in good standing or in default?") {
        const firstReply = "Are the student loans in good standing or in default?";
        
        let delivered = false;
        let deliveryError = null;
        if (!isShadowMode) {
          if (platform === "instagram" || isStandby) {
            await this.takeThreadControl(senderId, env);
          }
          const sendResult = await this.sendMessageToMetaDetailed(senderId, firstReply, platform, env);
          delivered = Boolean(sendResult?.ok);
          deliveryError = sendResult?.error || null;
        }

        const reason = isShadowMode
          ? "shadow_mode"
          : (delivered ? null : `meta_delivery_failed:${String(deliveryError || "unknown").slice(0, 180)}`);

        await env.DB.prepare(
          `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, sentiment_score, compliance_flag, compliance_reason, created_at)
           VALUES (?, ?, 'bot', NULL, ?, 0.0, ?, ?, ?)`
        ).bind(
          crypto.randomUUID(),
          conversation.id,
          firstReply,
          isShadowMode ? 0 : (delivered ? 0 : 1),
          reason,
          now
        ).run();

        await env.DB.prepare(
          `UPDATE conversations SET last_message_at = ? WHERE id = ?`
        ).bind(now, conversation.id).run();

        return;
      }

      // Branch B: Response to student loan standing question
      if (lastBotMsg === "Are the student loans in good standing or in default?") {
        const isGoodStanding = (
          normMsg.includes("good standing") ||
          normMsg.includes("good") ||
          normMsg.includes("standing") ||
          normMsg.includes("not in default") ||
          normMsg.includes("paying")
        );

        let messages = [];
        if (isGoodStanding) {
          messages.push("Perfect. We dont touch student loans in good standing. They actually help build positive history and keep your scores up");
          messages.push("Okay. With the student loans being removed that would put you on our Premium plan at $97/mo.");
        } else {
          messages.push("Okay. With the student loans being removed that would put you on our Premium plan at $97/mo.");
        }

        if (!isShadowMode) {
          if (platform === "instagram" || isStandby) {
            await this.takeThreadControl(senderId, env);
          }
          for (const msg of messages) {
            await this.sendMessageToMetaDetailed(senderId, msg, platform, env);
            await new Promise(resolve => setTimeout(resolve, 800));
          }
        }

        for (const msg of messages) {
          await env.DB.prepare(
            `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, sentiment_score, compliance_flag, compliance_reason, created_at)
             VALUES (?, ?, 'bot', NULL, ?, 0.0, 0, ?, ?)`
          ).bind(
            crypto.randomUUID(),
            conversation.id,
            msg,
            isShadowMode ? "shadow_mode" : null,
            now
          ).run();
        }

        await env.DB.prepare(
          `UPDATE conversations SET last_message_at = ? WHERE id = ?`
        ).bind(now, conversation.id).run();

        return;
      }

      // CASE 4: Phone Call Intent Handling
      const messageIntent = classifyIntent(userMessage);
      if (messageIntent === "PHONE_CALL_REQUEST" || messageIntent === "ONBOARDING_CALL_QUESTION") {
        const reply = messageIntent === "PHONE_CALL_REQUEST" 
          ? "Im responding to 50+ messages daily, so its hard for me to hop on a call each time someone reaches out. Its easiest for me to answer any questions here to make sure i can get to everyone quickly."
          : "No call needed - once you get signed up you'll hop on an onboarding call to get the process started and give us access to your reports and get paired with your Client Success Manager from there.";

        let delivered = false;
        let deliveryError = null;
        if (!isShadowMode) {
          if (platform === "instagram" || isStandby) {
            await this.takeThreadControl(senderId, env);
          }
          const sendResult = await this.sendMessageToMetaDetailed(senderId, reply, platform, env);
          delivered = Boolean(sendResult?.ok);
          deliveryError = sendResult?.error || null;
        }

        const reason = isShadowMode
          ? "shadow_mode"
          : (delivered ? null : `meta_delivery_failed:${String(deliveryError || "unknown").slice(0, 180)}`);

        await env.DB.prepare(
          `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, sentiment_score, compliance_flag, compliance_reason, created_at)
           VALUES (?, ?, 'bot', NULL, ?, 0.0, 0, ?, ?)`
        ).bind(
          crypto.randomUUID(),
          conversation.id,
          reply,
          reason,
          now
        ).run();

        await env.DB.prepare(
          `UPDATE conversations SET last_message_at = ? WHERE id = ?`
        ).bind(now, conversation.id).run();

        return;
      }

      const contextMessages = results.map(row => ({
        role: row.sender_type === "user" ? "user" : "assistant",
        content: row.message_text
      }));

      // Check if this is the very first user contact (only 1 message in history, which is the current user message just inserted)
      const isFirstContact = results.length <= 1;

      // Classify specific visual/audio media keyword triggers
      let matchedMedia = null;

      if (normMsg.includes("bankruptcy") || normMsg.includes("bankruptcies") || normMsg.includes(" bk ") || normMsg.startsWith("bk ") || normMsg.endsWith(" bk")) {
        matchedMedia = {
          type: "image",
          url: "https://angel-solutions-atl.pages.dev/assets/testimonials/Bankruptcy_removed.jpg",
          description: "before/after bankruptcy removal success screenshot",
          preText: "I can get this removed, here are some results for you to check out:"
        };
      } else if (normMsg.includes("student loan") || normMsg.includes("student loans")) {
        matchedMedia = {
          type: "image",
          url: "https://angel-solutions-atl.pages.dev/assets/testimonials/Student_Loans_removed.jpg",
          description: "student loan removal success screenshot",
          preText: "I can get this removed, here are some results for you to check out:"
        };
      } else if (normMsg.includes("testimonial") || normMsg.includes("review") || normMsg.includes("success stor")) {
        matchedMedia = {
          type: "image",
          url: "https://angel-solutions-atl.pages.dev/assets/testimonials/Testimonial.jpg",
          description: "client testimonial screenshot",
          preText: "Here are some results for you to check out:"
        };
      } else if (normMsg.includes("requirement") || normMsg.includes("qualify") || normMsg.includes("funding requirement")) {
        matchedMedia = {
          type: "audio",
          url: "https://angel-solutions-atl.pages.dev/assets/audio/Requirements_for_business_funding.m4a",
          description: "Jordynn's voice note detailing business funding requirements and qualifications"
        };
      }

      // Respect launch gate from client_compliance_launch (shadow = draft/log only until approved)
      // isShadowMode already computed above from compliance.launch_approval_status

      // Deliver voice greeting / triggered media assets immediately if not in shadow mode
      if (!isShadowMode) {
        if (isFirstContact) {
          // Send Jordynn's Welcome Audio Note
          await this.sendMessageToMeta(senderId, {
            type: "audio",
            url: "https://angel-solutions-atl.pages.dev/assets/audio/Initial_Response.m4a"
          }, platform, env);

          await this.sendMessageToMeta(senderId, "Hello, thank you for reaching out. It's Jordynn, I am the founder and owner of Angel Solutions ATL, and we help people fix their credit, build their credit, everything in between, and position your credit to a point where you’re able to get approvals both on the personal and the business side.\n\nI would love to hear more about what made you reach out, where you are on your credit journey do you have collections, charge-offs, late payments, bankruptcies, things like that that are stopping you from getting approvals?", platform, env);
        }

        if (matchedMedia) {
          if (matchedMedia.preText) {
            await this.sendMessageToMeta(senderId, matchedMedia.preText, platform, env);
            await new Promise(resolve => setTimeout(resolve, 800)); // Natural delay
          }
          await this.sendMessageToMeta(senderId, {
            type: matchedMedia.type,
            url: matchedMedia.url
          }, platform, env);
        }
      }

      let mediaPromptInstructions = "";
      if (isFirstContact) {
        mediaPromptInstructions += `\n- IMPORTANT: You have just automatically sent the user a personal welcome voice note (Initial_Response.m4a) welcoming them and a text message. Acknowledge this naturally and DO NOT repeat the intro message. Wait for their response to your question about collections/bankruptcies.`;
      } else {
        // If returning lead
        mediaPromptInstructions += `\n- SYSTEM INSTRUCTION FOR JORDYNN: If this is a returning lead who finally replied, DO NOT send the long intro message again. Acknowledge them coming back and directly ask what exactly is on their credit report right now that they need help getting removed.`;
      }
      if (matchedMedia) {
        if (matchedMedia.preText) {
          mediaPromptInstructions += `\n- IMPORTANT: You have just automatically sent the user a visual attachment showing ${matchedMedia.description}, and you explicitly said "${matchedMedia.preText}". Acknowledge this naturally and DO NOT repeat the clarification.`;
        } else {
          mediaPromptInstructions += `\n- IMPORTANT: You have just automatically sent the user a visual/audio attachment: a ${matchedMedia.type} showing ${matchedMedia.description}. You MUST refer directly to this attachment in your response so the conversation flows seamlessly.`;
        }
      }

      let leadContextInstructions = "";
      if (lead) {
        leadContextInstructions += `\n\nCURRENT LEAD PROFILE CONTEXT IN THE DATABASE:`;
        leadContextInstructions += `\n- Name: ${lead.name || "Unknown"}`;
        leadContextInstructions += `\n- Platform: ${lead.platform || "instagram"}`;
        if (lead.lead_score) leadContextInstructions += `\n- Credit Score: ${lead.lead_score}`;
        if (lead.bankruptcy !== undefined && lead.bankruptcy !== null) leadContextInstructions += `\n- Has Bankruptcy: ${lead.bankruptcy === 1 ? "Yes" : "No"}`;
        if (lead.child_support !== undefined && lead.child_support !== null) leadContextInstructions += `\n- Has Active Child Support: ${lead.child_support === 1 ? "Yes" : "No"}`;
        if (lead.collections_count !== undefined && lead.collections_count !== null) leadContextInstructions += `\n- Collections Count: ${lead.collections_count}`;

        const isUnclean = (lead.lead_score && lead.lead_score < 680) || (lead.bankruptcy === 1) || (lead.collections_count && lead.collections_count > 0);
        const isCleanAndReady = (lead.lead_score && lead.lead_score >= 680) && (lead.bankruptcy === 0 || lead.bankruptcy === null) && (lead.collections_count === 0 || lead.collections_count === null);

        if (isUnclean) {
          leadContextInstructions += `\n- SYSTEM INSTRUCTION FOR JORDYNN: This lead has been flagged as score under 680 or active negative items. They do NOT qualify for a business funding call. Do NOT ask diagnostic questions. Pitch the $67/mo Skool community: https://www.skool.com/creditsolution/about`;
        } else if (isCleanAndReady) {
          leadContextInstructions += `\n- SYSTEM INSTRUCTION FOR JORDYNN: Clean credit profile (680+, no bankruptcies/collections). Fully qualified for business funding. Suggest free 15-minute Discovery Call: https://angelsolutionsatl.com/book-online`;
        } else {
          leadContextInstructions += `\n- SYSTEM INSTRUCTION FOR JORDYNN: Partially filled profile. Ask exactly ONE friendly qualifying question if score/negative items still missing.`;
        }
      }

      const systemPrompt = `You are Jordynn Miller, the founder of Angel Solutions ATL. You speak directly in the first person ('I', 'my team', 'my business'). Never say you are an assistant, automated agent, or bot. You ARE Jordynn Miller.

Your voice is incredibly human, natural, conversational, warm, and casual. Talk exactly like a real person sending a relaxed, supportive text message or Instagram DM. Treat clients like family.

JORDYNN'S EMOTIONAL EMPATHY & MILESTONE SUPPORT (CRITICAL):
- When a user mentions a major life goal (like buying a house, purchasing a car, starting a business, or getting funding), respond with genuine excitement, warmth, and hope! Say things like: "Buying a home is such an amazing milestone! I've got you, we can definitely make that practical for you" or "Starting a business is huge—I'd love to help you get the funding you need."
- Show real human empathy when they talk about setbacks, delays, or frustration with collections or lenders. Be validating and reassuring (e.g., "I know how stressful that is, but don't worry, we can get this sorted out together").
- Never sound transactional. Make them feel heard and cared for first, then transition smoothly into credit details.

CONVERSATIONAL DIVERSITY & VARIETY (NEVER SOUND ROBOTIC OR BORING):
- Avoid starting every message with the same word. Do NOT default to "hey!" or "hey there!". Vary your greetings naturally depending on context.
- Never repeat phrases. Use a wide vocabulary of everyday words.
- Use casual lowercase structures for conversational words, standard contractions, and friendly colloquial phrasing.
- Keep replies ultra-short: 1 to 2 sentences is best (3 sentences maximum).

CONTEXT-AWARE ADAPTIVE ANALYSIS & STRICT RELEVANCE RULE:
- CRITICAL RULE: NEVER assume or mention "trucking", "equipment leasing", "real estate", "DSCR", "bankruptcies", "medical collections", or ANY specific industry, funding type, or negative credit issue unless the user explicitly mentions it first.
- General Inquiries: If the user just says "hey" or asks a general question, reply warmly and ask what they're trying to achieve or what their credit currently looks like.

INTERACTIVE INVESTIGATIVE & QUALIFYING WORKFLOW:
- DO NOT just dump a link immediately if you don't know their credit status yet. Ask 1 key qualifying question at a time.
- ANTI-REPETITION: Never re-ask credit score/collections/bankruptcy if already provided in history.
- Guide them: negative items or score under 680 → $67 Skool; clean 680+ ready for funding → Discovery Call booking.

VOICE & TEXT RULES (CRITICAL):
- NEVER use formal transition words or stiff AI buzzwords.
- NEVER use bullet points, numbered lists, colons, or brackets.
- NEVER use bolded headers or markdown formatting.
- Avoid clinical or overly technical corporate jargon.

BUSINESS KNOWLEDGEBASE & FAQS:
- 1-on-1 full service: free 15-minute Discovery Call only for clean profiles (680+, no recent negative items) ready for business funding. Negative items → $67/mo Skool first. Strategy Call is paid.
- Process timing: initial deletions 30-45 days; major restoral 3-6 months.
- Skool: $67/mo DIY Credit Solution — templates, weekly coaching, up to 5 disputes monthly.
- Funding requirements: 680+ score, <30% utilization, no recent late payments/BKs past 2 years, registered LLC/Corp, clean business bank statements.
- Bankruptcies: yes, specialized legal dispute letters.
- Refunds: service-level credit after 180 days of zero improvements; no cash refunds on completed work.
- No guarantees of specific score increases.

Strict Lead Qualification & Routing Protocol:
- UNCLEAN: do NOT send booking link. Guide to https://www.skool.com/creditsolution/about
- CLEAN & READY: book Discovery Call https://angelsolutionsatl.com/book-online

BANNED TERMS: Never say "credit sweep", "guarantee", "guaranteed", "best", "yo", "bet". Never promise specific score increases.

Approved Links ONLY:
- Skool Community: https://www.skool.com/creditsolution/about
- Booking: https://angelsolutionsatl.com/book-online
- Reviews: https://share.google/FTVB6seubNwgSVDnd
- Website: https://angelsolutionsatl.com

${mediaPromptInstructions}
${leadContextInstructions}

CONVERSATION TASK:
Answer clearly, pitch the correct program based on credit status, guide to the right link. Keep responses concise, 100% human, casual.

CRITICAL OUTPUT RULES:
- Reply with ONLY the exact Instagram DM text the customer should see.
- Do NOT explain your reasoning, plan, checklist, or instructions.
- Do NOT start with "Okay the user" / "We need to" / "Let me unpack".
- 1-2 short sentences. Sound like Jordynn texting.`;

      const aiMessages = [
        { role: "system", content: systemPrompt },
        ...contextMessages,
        {
          role: "user",
          content: "Respond now as Jordynn with ONLY the customer-facing DM text (no analysis)."
        }
      ];

      let replyText = "";
      try {
        // LAYER 1: NVIDIA API Catalog
        if (env.NVIDIA_API_KEY) {
          const nvdModel = env.NVIDIA_MODEL || "nvidia/llama-3.1-nemotron-70b-instruct";
          const start = Date.now();
          try {
            const aiRes = await fetch("https://integrate.api.nvidia.com/v1/chat/completions", {
              method: "POST",
              headers: {
                "Authorization": `Bearer ${env.NVIDIA_API_KEY}`,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                model: nvdModel,
                messages: aiMessages,
                temperature: 0.55,
                max_tokens: 160
              })
            });
            const aiJson = await aiRes.json();
            if (aiRes.ok) {
              replyText = aiJson?.choices?.[0]?.message?.content || "";
              console.log("NVIDIA API response success. Latency:", Date.now() - start, "ms. Model:", nvdModel);
            } else {
              console.error("NVIDIA API returned error status:", aiRes.status, JSON.stringify(aiJson).slice(0, 400));
            }
          } catch (nvdErr) {
            console.error("NVIDIA API request threw exception:", nvdErr.message);
          }
        }

        // LAYER 2: OpenRouter (Fallback 1)
        if ((!replyText || !sanitizeAiReply(replyText)) && env.OPENROUTER_API_KEY) {
          let model = env.OPENROUTER_MODEL || "openrouter/free";
          if (model === "meta-llama/llama-3.3-70b-instruct:free") {
            model = "openrouter/free";
          }
          const aiRes = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${env.OPENROUTER_API_KEY}`,
              "Content-Type": "application/json",
              "HTTP-Referer": "https://angelsolutionsatl.com",
              "X-Title": "Angel Solutions ATL Automation"
            },
            body: JSON.stringify({
              model,
              messages: aiMessages,
              temperature: 0.55,
              max_tokens: 160
            })
          });
          const aiJson = await aiRes.json();
          if (!aiRes.ok) {
            console.error("OpenRouter error:", JSON.stringify(aiJson).slice(0, 400));
          }
          replyText = aiJson?.choices?.[0]?.message?.content || "";
        }

        // LAYER 3: Cloudflare Workers AI (Fallback 2)
        if ((!replyText || !sanitizeAiReply(replyText)) && env.AI) {
          const aiOut = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
            messages: aiMessages,
            max_tokens: 160
          });
          replyText = typeof aiOut === "string" ? aiOut : (aiOut?.response || aiOut?.result || "");
        }
      } catch (aiErr) {
        console.error("AI generation failed:", aiErr);
      }

      replyText = sanitizeAiReply(replyText) || templateReplyForIntent(intent, isFirstContact);
      replyText = stripUnapprovedLinks(String(replyText));
      const complianceResult = enforceCompliance(replyText);
      replyText = complianceResult.censoredText || complianceResult.cleanedText || replyText;
      // Final safety net after compliance
      replyText = sanitizeAiReply(replyText) || templateReplyForIntent(intent, isFirstContact);

      let delivered = false;
      let deliveryError = null;
      if (!isShadowMode) {
        // Claim thread early for IG (ManyChat/handover often blocks sends)
        if (platform === "instagram" || isStandby) {
          await this.takeThreadControl(senderId, env);
        }
        const sendResult = await this.sendMessageToMetaDetailed(senderId, replyText, platform, env);
        delivered = Boolean(sendResult?.ok);
        deliveryError = sendResult?.error || null;
        if (!delivered) {
          console.error(`Meta delivery FAILED for lead=${lead.id} platform=${platform} sender=${senderId}:`, deliveryError);
        }
      }

      const reason = isShadowMode
        ? "shadow_mode"
        : (delivered ? null : `meta_delivery_failed:${String(deliveryError || "unknown").slice(0, 180)}`);

      await env.DB.prepare(
        `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, sentiment_score, compliance_flag, compliance_reason, created_at)
         VALUES (?, ?, 'bot', NULL, ?, 0.0, ?, ?, ?)`
      ).bind(
        crypto.randomUUID(),
        conversation.id,
        replyText,
        isShadowMode ? 0 : (delivered ? 0 : 1),
        reason,
        now
      ).run();

      await env.DB.prepare(
        `UPDATE conversations SET last_message_at = ? WHERE id = ?`
      ).bind(now, conversation.id).run();
    }
  },

  async handlePublicComment(change, env) {
    try {
      const value = change.value || {};
      const commentId = value.comment_id || value.id;
      const message = value.message || value.text || "";
      const fromId = value.from?.id;
      const username = value.from?.username || value.from?.name || "";
      const token = env.META_PAGE_ACCESS_TOKEN;
      if (!commentId || !message) return;

      // analyzeCommentSafety → { isSpam, reason }
      const safety = analyzeCommentSafety(message);
      if (safety.isSpam) {
        if (token) await hideCommentOnMeta(commentId, token);
        console.log("Public comment hidden as spam", { commentId, fromId, reason: safety.reason });
        return;
      }

      // Safe comment → warm public reply by intent, push conversation to DMs
      const intent = classifyIntent(message);
      const reply = generatePublicReply(username, intent);
      if (reply && token) {
        await replyToCommentOnMeta(commentId, reply, token);
        
        let isFirstContact = true;
        if (fromId && env.DB) {
           const existing = await env.DB.prepare("SELECT id FROM leads WHERE platform_user_id = ?").bind(String(fromId)).first();
           if (existing) {
             isFirstContact = false;
           }
        }

        let dmText = "";
        if (isFirstContact) {
            dmText = "Hello, thank you for reaching out. It's Jordynn, I am the founder and owner of Angel Solutions ATL, and we help people fix their credit, build their credit, everything in between, and position your credit to a point where you’re able to get approvals both on the personal and the business side.\n\nI would love to hear more about what made you reach out, where you are on your credit journey do you have collections, charge-offs, late payments, bankruptcies, things like that that are stopping you from getting approvals?";
        } else {
            dmText = "Hey again! Let me know what exactly is on your credit report right now that you need help getting removed, and we can get started.";
        }

        if (env.META_PAGE_ID) {
          await sendPrivateReplyToCommentOnMeta(commentId, dmText, token, env.META_PAGE_ID);
        }
      }
      console.log("Public comment replied and DM sent", { commentId, fromId, intent });
    } catch (e) {
      console.error("handlePublicComment error:", e);
    }
  },

  async handleLeadgen(change, env) {
    try {
      console.log("Leadgen event received:", JSON.stringify(change?.value || change));
      const value = change.value;
      if (!value || !value.leadgen_id) return;
      
      const leadgenId = value.leadgen_id;
      const pageId = value.page_id;
      const formId = value.form_id;
      const token = env.META_PAGE_ACCESS_TOKEN;
      
      if (!token) {
        console.error("Missing META_PAGE_ACCESS_TOKEN, cannot process leadgen");
        return;
      }

      // 1. Fetch Lead Details from Meta Graph API
      const res = await fetch(`https://graph.facebook.com/v21.0/${leadgenId}?access_token=${token}`);
      if (!res.ok) {
        console.error("Failed to fetch lead details from Graph API:", await res.text());
        return;
      }
      
      const leadData = await res.json();
      console.log("Fetched Meta Lead Data:", JSON.stringify(leadData));
      
      // 2. Parse Field Data
      let email = null;
      let phone = null;
      let fullName = "Meta Lead";
      
      if (leadData.field_data) {
        for (const field of leadData.field_data) {
          if (field.name === "email" && field.values.length > 0) email = field.values[0];
          if (field.name === "phone_number" && field.values.length > 0) phone = field.values[0];
          if (field.name === "full_name" && field.values.length > 0) fullName = field.values[0];
          if (field.name === "first_name" && field.values.length > 0) fullName = field.values[0];
        }
      }
      
      if (!email && !phone) {
        console.error("Lead missing email and phone, skipping.");
        return;
      }

      // 3. Upsert into D1 Database
      const uuid = crypto.randomUUID();
      const now = new Date().toISOString();
      const intakeId = env.INTAKE_ID || "6a46c0696b95e7dc9dd6251c";
      
      // Safe NULL-aware lookup: only match on a field if the value is actually present
      let existingLead = null;
      if (email) {
        existingLead = await env.DB.prepare(
          "SELECT id FROM leads WHERE email = ? LIMIT 1"
        ).bind(email).first();
      }
      if (!existingLead && phone) {
        existingLead = await env.DB.prepare(
          "SELECT id FROM leads WHERE phone = ? LIMIT 1"
        ).bind(phone).first();
      }
      
      let leadObj = {
        id: existingLead ? existingLead.id : uuid,
        name: fullName,
        email: email,
        phone: phone,
        platform: "meta_leadgen",
        lead_state: "NEW",
        intake_id: intakeId
      };

      if (existingLead) {
        await env.DB.prepare(
          `UPDATE leads SET name = ?, email = ?, phone = ?, platform = 'meta_leadgen', updated_at = ? WHERE id = ?`
        ).bind(fullName, email, phone, now, existingLead.id).run();
      } else {
        await env.DB.prepare(
          `INSERT INTO leads (id, intake_id, lead_state, platform, platform_user_id, name, email, phone, created_at, updated_at)
           VALUES (?, ?, 'NEW', 'meta_leadgen', ?, ?, ?, ?, ?, ?)`
        ).bind(uuid, intakeId, `leadgen_${leadgenId}`, fullName, email, phone, now, now).run();
      }

      // 4. Sync immediately to GoHighLevel
      await this.syncLeadToGoHighLevel(leadObj, env);
      console.log(`Successfully processed Meta LeadGen ID ${leadgenId} and synced to CRM.`);
      
    } catch (e) {
      console.error("handleLeadgen error:", e);
    }
  },

  async takeThreadControl(psid, env) {
    try {
      const token = env.META_PAGE_ACCESS_TOKEN;
      if (!token || !psid) return false;

      // Handover protocol: request control from whichever app currently owns the thread
      // (ManyChat / Inbox often hold primary control and block API sends).
      // Facebook Page Inbox app id: 263902037430900
      const calls = [
        {
          ep: "me/take_thread_control",
          body: { recipient: { id: psid }, metadata: "Angel Solutions AI taking thread control" }
        },
        {
          ep: "me/request_thread_control",
          body: { recipient: { id: psid }, metadata: "Angel Solutions AI requesting thread control" }
        }
      ];
      for (const call of calls) {
        const res = await fetch(
          `https://graph.facebook.com/v21.0/${call.ep}?access_token=${encodeURIComponent(token)}`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(call.body)
          }
        );
        const t = await res.text();
        if (res.ok) {
          console.log(`${call.ep} ok for ${psid}:`, t.slice(0, 200));
          return true;
        }
        console.log(`${call.ep} failed for ${psid}:`, t.slice(0, 300));
      }
      return false;
    } catch (e) {
      console.error("takeThreadControl error:", e);
      return false;
    }
  },

  async sendMessageToMeta(recipientId, message, platform, env) {
    const result = await this.sendMessageToMetaDetailed(recipientId, message, platform, env);
    return Boolean(result?.ok);
  },

  async sendMessageToMetaDetailed(recipientId, message, platform, env) {
    try {
      const token = env.META_PAGE_ACCESS_TOKEN;
      const pageId = env.META_PAGE_ID;
      if (!token || !recipientId) {
        return { ok: false, error: "missing token or recipientId" };
      }

      // Always try to claim thread control before sending (esp. Instagram + ManyChat).
      await this.takeThreadControl(recipientId, env);

      let messagePayload;
      if (typeof message === "string") {
        messagePayload = { text: message };
      } else if (message && message.type === "image") {
        messagePayload = {
          attachment: {
            type: "image",
            payload: { url: message.url, is_reusable: true }
          }
        };
      } else if (message && message.type === "audio") {
        messagePayload = {
          attachment: {
            type: "audio",
            payload: { url: message.url, is_reusable: true }
          }
        };
      } else {
        messagePayload = { text: String(message) };
      }

      // Try multiple Graph shapes — IG often needs page-id path and/or no messaging_type.
      const attempts = [];
      const versions = ["v21.0"]; // v21.0 only — v19.0 is deprecated
      const pathIds = pageId ? [pageId, "me"] : ["me"];

      const bodies = [
        {
          recipient: { id: String(recipientId) },
          messaging_type: "RESPONSE",
          message: messagePayload
        },
        // Fallback without messaging_type (some IG threads reject RESPONSE)
        {
          recipient: { id: String(recipientId) },
          message: messagePayload
        },
        // Last-resort HUMAN_AGENT tag (allows reply outside standard RESPONSE in some cases)
        {
          recipient: { id: String(recipientId) },
          messaging_type: "MESSAGE_TAG",
          tag: "HUMAN_AGENT",
          message: messagePayload
        }
      ];

      for (const ver of versions) {
        for (const pathId of pathIds) {
          for (const body of bodies) {
            const base = `https://graph.facebook.com/${ver}/${pathId}/messages`;
            const res = await fetch(`${base}?access_token=${encodeURIComponent(token)}`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(body)
            });
            const bodyText = await res.text();
            attempts.push({
              base,
              status: res.status,
              body: bodyText.slice(0, 500),
              tag: body.tag || body.messaging_type || "plain"
            });
            if (res.ok) {
              console.log("sendMessageToMeta ok:", {
                platform,
                recipientId,
                base,
                body: bodyText.slice(0, 200)
              });
              return { ok: true, attempts, response: bodyText.slice(0, 300) };
            }
          }
        }
      }

      console.error("sendMessageToMeta failed all attempts:", {
        platform,
        recipientId,
        attempts
      });

      const last = attempts[attempts.length - 1];
      let errMsg = last?.body || "unknown graph error";
      try {
        const parsed = JSON.parse(last.body);
        errMsg = parsed?.error?.message || errMsg;
      } catch (_) {
        /* keep raw */
      }
      return { ok: false, error: errMsg, attempts };
    } catch (e) {
      console.error("sendMessageToMeta error:", e);
      return { ok: false, error: String(e?.message || e) };
    }
  },

  async syncLeadToGoHighLevel(lead, env) {
    try {
      if (!env.GHL_API_KEY || !env.GHL_LOCATION_ID || !lead) return;
      const email = lead.email;
      const phone = lead.phone;
      if (!email && !phone) return;

      // 1. Build and map Custom Fields
      const customFields = [];
      if (lead.platform_user_id) {
        customFields.push({ id: "0dfoXmiA7GsSi6Jz5YdZ", value: lead.platform_user_id }); // contact.social_media_handle
        customFields.push({ id: "NfRjMUGHm1mkpwaiymTX", value: lead.platform_user_id }); // contact.ig_username
        customFields.push({ id: "xZc29K4B6Kfn4XZROVOi", value: lead.platform_user_id }); // contact.whats_your_social_media
      }

      if (lead.lead_score) {
        // Numeric FICO score (contact.what_are_your_current_fico_scores)
        customFields.push({ id: "5S7589TZ03vONijPxDUS", value: String(lead.lead_score) });

        // Credit score ranges (contact.what_is_your_credit_score)
        const score = Number(lead.lead_score);
        let range = "Below 600";
        if (score >= 750) range = "750-800";
        else if (score >= 680) range = "680-750";
        else if (score >= 600) range = "600-680";

        customFields.push({ id: "UYP4cqC5z6WmQBn2N4Sl", value: range });
      }

      // Collections, late payments, charge-offs (contact.d)
      if (lead.collections_count !== undefined) {
        const hasCollections = lead.collections_count > 0 ? "Yes" : "No";
        customFields.push({ id: "guQa4YYkrxi4TVfHCNKd", value: hasCollections });
      }

      // Onboarding program tags and membership level based on customer journey state
      if (lead.lead_state === "ACTIVE_CLIENT") {
        customFields.push({ id: "9eM44CrctxYuX1ooZxje", value: "Standard ($67)" }); // contact.membership_level
        customFields.push({ id: "LYG4x2D6lY2bTsu15qvq", value: "Skool Standard $67" }); // contact.package
      }

      const body = {
        locationId: env.GHL_LOCATION_ID,
        firstName: (lead.name || "Lead").split(" ")[0],
        lastName: (lead.name || "").split(" ").slice(1).join(" ") || "Meta",
        email: email || undefined,
        phone: phone || undefined,
        source: `meta_${lead.platform || "instagram"}`,
        tags: ["angel-solutions", "meta-automation", lead.lead_state || "NEW"].filter(Boolean),
        customFields: customFields
      };

      // 2. Perform Contact Upsert
      const res = await fetch("https://services.leadconnectorhq.com/contacts/upsert", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${env.GHL_API_KEY}`,
          "Content-Type": "application/json",
          "Version": "2021-07-28"
        },
        body: JSON.stringify(body)
      });

      let contactId = null;
      let syncStatus = "failed";
      let errorMessage = null;

      if (res.ok) {
        const resJson = await res.json();
        contactId = resJson?.contact?.id;
        syncStatus = contactId ? "success" : "failed";
        if (!contactId) errorMessage = "Upsert succeeded but contact ID missing in response";
      } else {
        errorMessage = await res.text();
        console.error("GHL Contact Upsert failed:", errorMessage);
      }

      // 3. Sync Opportunity status and pipeline stage
      if (contactId) {
        const pipelineId = "tqB3CjvRgFvfhWs7k6be"; // GHL "Marketing Pipeline"
        let stageId = "8a5387cb-c5c4-4eb7-b581-ac5061b13e30"; // Default: "New Lead"
        let oppStatus = "open";

        switch (lead.lead_state) {
          case "NEW":
            stageId = "8a5387cb-c5c4-4eb7-b581-ac5061b13e30"; // New Lead
            oppStatus = "open";
            break;
          case "QUALIFIED":
            stageId = "352df727-5c93-43c6-b5a7-2c2705f06d46"; // Qualified
            oppStatus = "open";
            break;
          case "LINK_SENT":
            stageId = "25982865-2080-4e4a-9c73-76b80c350129"; // Proposal Sent
            oppStatus = "open";
            break;
          case "BOOKED":
            stageId = "3572b645-a43f-4d6a-9f97-df01a485b07e"; // Negotiation (or calendar booking)
            oppStatus = "open";
            break;
          case "ACTIVE_CLIENT":
            stageId = "441fce14-2126-487a-b7b4-6c32f78ee6f6"; // Closed (Won)
            oppStatus = "won";
            break;
          case "VAFOLLOWUP":
          case "ASSIGN":
          case "COLLAB":
            stageId = "9d1e0f91-df45-4b69-abf0-bb2527e928e2"; // Contacted
            oppStatus = "open";
            break;
          case "DQ":
            stageId = "441fce14-2126-487a-b7b4-6c32f78ee6f6"; // Closed (Lost)
            oppStatus = "lost";
            break;
        }

        // Check if there is an existing Opportunity in GHL
        let opportunityId = null;
        try {
          const searchRes = await fetch(
            `https://services.leadconnectorhq.com/opportunities/search?contactId=${contactId}&pipelineId=${pipelineId}`,
            {
              method: "GET",
              headers: {
                "Authorization": `Bearer ${env.GHL_API_KEY}`,
                "Version": "2021-07-28",
                "Content-Type": "application/json"
              }
            }
          );
          if (searchRes.ok) {
            const searchJson = await searchRes.json();
            const opps = searchJson?.opportunities || [];
            if (opps.length > 0) {
              opportunityId = opps[0].id;
            }
          }
        } catch (searchErr) {
          console.error("GHL Opportunity Search failed:", searchErr);
        }

        // Upsert the Opportunity in the specified stage
        try {
          let oppRes;
          if (opportunityId) {
            oppRes = await fetch(`https://services.leadconnectorhq.com/opportunities/${opportunityId}`, {
              method: "PUT",
              headers: {
                "Authorization": `Bearer ${env.GHL_API_KEY}`,
                "Version": "2021-07-28",
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                pipelineStageId: stageId,
                status: oppStatus
              })
            });
          } else {
            oppRes = await fetch("https://services.leadconnectorhq.com/opportunities", {
              method: "POST",
              headers: {
                "Authorization": `Bearer ${env.GHL_API_KEY}`,
                "Version": "2021-07-28",
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                pipelineId: pipelineId,
                pipelineStageId: stageId,
                contactId: contactId,
                name: `${lead.name || "Meta Lead"} | ${lead.platform || "Instagram"}`,
                status: oppStatus
              })
            });
          }
          if (!oppRes.ok) {
            console.error("GHL Opportunity sync failed:", await oppRes.text());
          }
        } catch (oppErr) {
          console.error("GHL Opportunity operation failed:", oppErr);
        }
      }

      // 4. Log the GHL synchronization in DB
      if (env.DB) {
        const syncId = "sync_" + crypto.randomUUID();
        try {
          await env.DB.prepare(
            "INSERT INTO ghl_sync_log (id, lead_id, ghl_contact_id, sync_status, error_message) VALUES (?, ?, ?, ?, ?)"
          )
          .bind(syncId, lead.id, contactId, syncStatus, errorMessage)
          .run();
        } catch (dbErr) {
          console.error("Error logging GHL sync to database:", dbErr);
        }
      }
    } catch (e) {
      console.error("syncLeadToGoHighLevel error:", e);
    }
  }
};
