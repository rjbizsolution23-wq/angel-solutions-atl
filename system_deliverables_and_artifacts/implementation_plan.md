# Implementation Plan — Webhook Execution Timeout & Delivery Reliability Guard

This document details the step-by-step engineering plan to resolve the Facebook Messenger and Instagram bot silence. Under heavy traffic or model congestion, slow API responses from OpenRouter exceed Cloudflare Workers' 30-second wall-time limit, causing the background `waitUntil()` context to be aborted by the V8 runtime. We will implement robust fetch timeouts, fallback racing, and defensive integrations to guarantee sub-10-second response delivery.

---

## 1. Root Cause Analysis & Architectural Findings

### A. The `waitUntil` Isolation Cutoff
* **Finding:** When a webhook arrives, the worker responds to Meta with `200 OK` immediately and executes the slow LLM pipeline asynchronously via `ctx.waitUntil()`.
* **Vulnerability:** On Cloudflare Workers, background execution after returning a response is aggressively throttled or capped at a maximum of **30 seconds** of wall-clock time.
* **Failure Mode:** Live logs show that the OpenRouter free models (`openrouter/free`) often take more than 25-30 seconds to reply during periods of API congestion. When this occurs, the entire V8 isolate is aborted with:
  > `"waitUntil() tasks did not complete within the allowed time after invocation end and have been cancelled."`
* **Result:** No message is ever dispatched to the Meta Graph API, and the conversation stalls indefinitely.

### B. Heavy API Congestion in Free Router
* **Finding:** The default `openrouter/free` router pools multiple models and is subject to severe latency spikes. If the primary model hangs, subsequent models in the candidate sequence are never tried because the worker is killed first.
* **Impact:** A single slow HTTP request blocks the entire flow.

---

## 2. Proposed Structural Changes

We will modify [src/index.js](file:///Users/kalivibecoding/Downloads/_ORGANIZED_DOWNLOADS/Uncategorized/angel-solutions-complete-system/cloudflare-worker/src/index.js) to implement defensive network timeouts and fallback racing.

### [Component 1] Network Timeout Guard on OpenRouter
We will add a strict 7-second `AbortController` timeout for each individual OpenRouter request in the model loop. If a model fails to reply in 7 seconds, we abort the request, catch the error, and immediately move to the next model or the local Workers AI fallback.

```javascript
// Inside the candidate model loop:
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 7000); // Strict 7s timeout

try {
  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    signal: controller.signal,
    headers: {
      "Authorization": `Bearer ${env.OPENROUTER_API_KEY}`,
      "Content-Type": "application/json",
      "HTTP-Referer": "https://angelsolutionsatl.com",
      "X-Title": "Angel Solutions ATL Automation"
    },
    body: JSON.stringify({
      model: modelName,
      messages: aiMessages,
      temperature: 0.5,
      max_tokens: 1024
    })
  });
  
  clearTimeout(timeoutId); // Clear timeout if successful
  
  if (response.ok) {
    const data = await response.json();
    if (data && data.choices && data.choices[0] && data.choices[0].message) {
      replyText = data.choices[0].message.content;
      usedProvider = `OpenRouter (${modelName})`;
      console.log(`Successfully generated response using model: ${modelName}`);
      break; 
    }
  } else {
    const errBody = await response.text();
    console.warn(`OpenRouter model ${modelName} returned status ${response.status}: ${errBody}`);
  }
} catch (err) {
  clearTimeout(timeoutId);
  if (err.name === "AbortError") {
    console.warn(`OpenRouter model ${modelName} TIMED OUT after 7 seconds. Trying next candidate...`);
  } else {
    console.error(`Error attempting OpenRouter model ${modelName}:`, err);
  }
}
```

### [Component 2] Network Timeout Guard on GoHighLevel Sync
GoHighLevel API requests can also occasionally lag or hang. We will implement a strict 6-second timeout for the GHL sync `fetch` call to prevent CRM syncing from delaying response generation.

```javascript
// Inside syncLeadToGoHighLevel:
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 6000); // 6s CRM sync limit

try {
  const response = await fetch("https://services.leadconnectorhq.com/contacts/", {
    method: "POST",
    signal: controller.signal,
    headers: {
      "Authorization": `Bearer ${ghlApiKey}`,
      "Content-Type": "application/json",
      "Version": "2021-04-15"
    },
    body: JSON.stringify(payload)
  });
  
  clearTimeout(timeoutId);
  // Process response...
} catch (err) {
  clearTimeout(timeoutId);
  if (err.name === "AbortError") {
    console.error(`GHL Webhook Sync TIMED OUT after 6 seconds.`);
  } else {
    console.error(`GHL Webhook Sync failed:`, err);
  }
}
```

### [Component 3] Optimize Candidate Sequence & Fast Fallback
* Reduce the default sequence to focus on the absolute fastest responding free models:
  * Primary: `openrouter/free` (User configured)
  * Secondary: `google/gemma-4-26b-a4b-it:free` (Small, highly responsive, extremely low latency)
  * Tertiary: `nvidia/nemotron-nano-9b-v2:free` (Ultra lightweight)
* If these candidates fail or time out, fall back immediately to Cloudflare's edge-native `@cf/meta/llama-3.1-8b-instruct` which runs in under 1 second.

---

## 3. Verification Plan

### Automated Webhook Simulation
1. **Mock Webhook Test:** Run `python3 send_mock_webhook.py` or trigger a local event to verify that the worker processes the message and generates a response under 10 seconds.
2. **Timeout Simulation:** Simulate a slow API endpoint or slow model call to verify that the `AbortController` triggers properly, aborts at exactly 7 seconds, and falls back gracefully to the next candidate model or Workers AI.

### Live Production Deploy & Monitoring
1. Deploy the updated worker using `pnpm run deploy` or `wrangler deploy`.
2. Monitor live logs using the active wrangler tail process (`task-7724.log`) to confirm that incoming messages (like Ricky's DMs) receive immediate, successful replies.

---

> [!NOTE]
> All changes are non-destructive, strictly add timeouts, and ensure 100% compliance with both OpenRouter and Cloudflare execution limits.
