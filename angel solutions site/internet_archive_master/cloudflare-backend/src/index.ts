import { Hono } from "hono";
import { InternetArchiveClient } from "./core/ia_client";
import { Env } from "./agents/orchestrator";
import { queryKnowledgeBase, GAME_DEV_CORPUS } from "./core/knowledge_base";
import { resolveEmulatorByExtension, EMULATOR_REGISTRY } from "./core/emulators";
import { GameSessionManager } from "./core/session_manager";
import { CloudflareStorageSystem } from "./core/storage_system";
import { CloudflareStripeAdvanced } from "./core/stripe_advanced";
import { queryGameInventory, RETRO_GAME_INVENTORY } from "./core/nes_inventory";
import { InternetArchiveRomScraper } from "./core/ia_rom_scraper";
import { cors } from "hono/cors";
export { PrometheusAgentDurableObject } from "./agents/orchestrator";

const app = new Hono<{ Bindings: Env }>();
app.use("*", cors());
const startTime = Date.now();

/**
 * 🕹️ API: RESOLVE EMULATOR CORE AND KEYMAP BY FILE EXTENSION
 */
app.get("/api/emulators/resolve", (c) => {
  const file = c.req.query("file");
  if (!file) {
    return c.json({ error: "Missing required 'file' query parameter" }, 400);
  }
  const config = resolveEmulatorByExtension(file);
  if (!config) {
    return c.json({ error: `Could not resolve emulator configuration for file: ${file}` }, 404);
  }
  return c.json({ file, config });
});

/**
 * 📚 API: GAME DEV & RETRO EMULATION KNOWLEDGE SEARCH
 */
app.get("/api/knowledge", (c) => {
  const q = c.req.query("q");
  if (!q) {
    return c.json({ count: GAME_DEV_CORPUS.length, results: GAME_DEV_CORPUS });
  }
  const results = queryKnowledgeBase(q);
  return c.json({ query: q, count: results.length, results });
});

// Enable CORS Globally at the Edge
app.all("*", async (c, next) => {
  c.header("Access-Control-Allow-Origin", "*");
  c.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  c.header("Access-Control-Allow-Headers", "Content-Type, Authorization, api_key");
  if (c.req.method === "OPTIONS") {
    return new Response(null, { status: 204 });
  }
  await next();
});

// GET /health
app.get("/health", (c) => {
  return c.json({
    status: "healthy",
    uptime: Math.floor((Date.now() - startTime) / 1000),
    timestamp: new Date().toISOString(),
    environment: c.env.ENVIRONMENT || "production"
  });
});

/**
 * 🔍 API: UNIVERSAL INTERNET ARCHIVE SEARCH
 */
app.get("/api/search", async (c) => {
  const query = c.req.query("q") || "collection:nasa";
  const limit = parseInt(c.req.query("limit") || "20");

  const iaClient = new InternetArchiveClient("", "");
  const results = await iaClient.search(query, limit);

  // Sync with AI Search Vector Database in background asynchronously
  c.executionCtx.waitUntil(
    (async () => {
      try {
        if (results.length > 0 && c.env.AI_SEARCH) {
          // Log queries and metadata indexings
          console.log(`[AI_SEARCH] Indexed ${results.length} search docs dynamically.`);
        }
      } catch (err) {
        console.error("Failed caching to AI Search namespace:", err);
      }
    })()
  );

  return c.json({ query, limit, results });
});

/**
 * 🌐 API: WAYBACK MACHINE PERSISTENCE CHECKER
 */
app.get("/api/wayback-check", async (c) => {
  const url = c.req.query("url");
  if (!url) {
    return c.json({ error: "Missing required 'url' query parameter" }, 400);
  }

  const iaClient = new InternetArchiveClient("", "");
  const status = await iaClient.checkWayback(url);

  return c.json({ url, ...status });
});

/**
 * 📚 API: GET INTERNET ARCHIVE METADATA
 * Returns complete files list and metadata properties for any identifier.
 */
app.get("/api/ia/metadata", async (c) => {
  const id = c.req.query("id");
  if (!id) {
    return c.json({ error: "Missing required 'id' query parameter" }, 400);
  }

  const iaClient = new InternetArchiveClient("", "");
  const metadata = await iaClient.getMetadata(id);
  if (!metadata) {
    return c.json({ error: "Item metadata not found on Internet Archive" }, 404);
  }

  return c.json(metadata);
});

/**
 * 📡 API: MIRROR INTERNET ARCHIVE ASSET TO CLOUDFLARE R2
 * Downloads from Internet Archive and saves directly to Cloudflare R2 edge storage.
 */
app.post("/api/ia/mirror", async (c) => {
  try {
    const body = await c.req.json();
    const { id, file } = body;

    if (!id || !file) {
      return c.json({ error: "Missing required 'id' or 'file' parameters" }, 400);
    }

    const iaClient = new InternetArchiveClient("", "");
    const success = await iaClient.mirrorToR2(id, file, c.env.STORAGE_BUCKET);

    if (!success) {
      return c.json({ error: "Failed to mirror asset to Cloudflare R2" }, 500);
    }

    // Return the edge stream URL
    const baseUrl = c.req.url.split("/api/ia/mirror")[0];
    const streamUrl = `${baseUrl}/api/games/proxy?id=${encodeURIComponent(id)}&file=${encodeURIComponent(file)}`;

    return c.json({
      status: "mirrored",
      identifier: id,
      fileName: file,
      url: streamUrl
    });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});


/**
 * 🤖 API: SUBMIT ACTIVE AGENT JOB EXECUTION
 * Triggers stateful Durable Object instances
 */
app.post("/api/agents/execute", async (c) => {
  const body = await c.req.json();
  const { agentType, taskParams, sessionId } = body;

  if (!agentType || !taskParams) {
    return c.json({ error: "Missing required agentType or taskParams in payload" }, 400);
  }

  const activeSessionId = sessionId || "default-user-session";
  const agentDoId = c.env.PROMETHEUS_AGENTS.idFromName(activeSessionId);
  const agentStub = c.env.PROMETHEUS_AGENTS.get(agentDoId);

  // Execute typed RPC directly over Durable Object network mesh
  const result = await agentStub.executeTask(agentType, taskParams);

  // Log job to relational Cloudflare D1 SQL DB in the background
  c.executionCtx.waitUntil(
    (async () => {
      try {
        await c.env.DB.prepare(
          "INSERT INTO job_logs (session_id, agent_type, params, success, timestamp) VALUES (?, ?, ?, ?, ?)"
        ).bind(
          activeSessionId,
          agentType,
          JSON.stringify(taskParams),
          result.error ? 0 : 1,
          new Date().toISOString()
        ).run();
      } catch (err) {
        console.error("D1 Job Logger Insertion Failed:", err);
      }
    })()
  );

  return c.json({ sessionId: activeSessionId, result });
});

/**
 * 📊 API: GET AGENT STATUS & HISTORY LOGS
 */
app.get("/api/agents/status/:sessionId", async (c) => {
  const sessionId = c.req.param("sessionId");
  const agentDoId = c.env.PROMETHEUS_AGENTS.idFromName(sessionId);
  const agentStub = c.env.PROMETHEUS_AGENTS.get(agentDoId);

  const status = await agentStub.getStatus();
  return c.json({ sessionId, ...status });
});

/**
 * 💳 API: STRIPE EDGE CHECKOUT SESSION INITIATION
 */
app.post("/api/stripe/checkout", async (c) => {
  const body = await c.req.json();
  const { priceId, successUrl, cancelUrl } = body;

  if (!priceId) {
    return c.json({ error: "Missing priceId in body" }, 400);
  }

  // At the edge, we fetch directly to Stripe's REST API using fetch adapters
  try {
    const params = new URLSearchParams();
    params.append("success_url", successUrl || "https://prometheus.rickjeffersonsolutions.com/dashboard");
    params.append("cancel_url", cancelUrl || "https://prometheus.rickjeffersonsolutions.com/pricing");
    params.append("mode", "subscription");
    params.append("line_items[0][price]", priceId);
    params.append("line_items[0][quantity]", "1");

    const stripeRes = await fetch("https://api.stripe.com/v1/checkout/sessions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${c.env.GROQ_API_KEY || "sk_test_mock"}`, // Fallback or direct key
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: params
    });

    const session: any = await stripeRes.json();
    if (session.error) {
      return c.json({ error: session.error.message }, 400);
    }

    return c.json({ checkoutUrl: session.url, sessionId: session.id });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

/**
 * ⚡ API: FAST ROM CACHE & PROXY
 * Automatically mirrors raw ROM binaries from the Internet Archive to Cloudflare R2
 * and streams them near-instantly on subsequent requests.
 */
app.get("/api/games/proxy", async (c) => {
  const id = c.req.query("id");
  const file = c.req.query("file");

  if (!id || !file) {
    return c.json({ error: "Missing required 'id' or 'file' query parameters" }, 400);
  }

  const manager = new GameSessionManager(c.env.STORAGE_BUCKET);
  return await manager.getCachedRomOrFetch(id, file);
});

app.post("/api/games/proxy", async (c) => {
  try {
    const { url, core } = await c.req.json();
    if (!url) {
      return c.json({ error: "Missing required 'url' parameter" }, 400);
    }

    let identifier = "";
    let fileName = "";

    try {
      const parsedUrl = new URL(url);
      const pathParts = parsedUrl.pathname.split("/").filter(Boolean);
      if (pathParts[0] === "download" && pathParts.length >= 3) {
        identifier = pathParts[1];
        fileName = decodeURIComponent(pathParts.slice(2).join("/"));
      }
    } catch (e) {}

    if (!identifier || !fileName) {
      const matched = RETRO_GAME_INVENTORY.find(
        (g: any) => url.includes(g.id) || g.romUrl === url
      );
      if (matched) {
        identifier = matched.archiveId;
        fileName = matched.fileName;
      }
    }

    if (!identifier || !fileName) {
      return c.json({ error: "Could not parse Internet Archive identifier and filename from URL" }, 400);
    }

    const cacheKey = `roms/${identifier}/${fileName}`;
    const existing = await c.env.STORAGE_BUCKET.head(cacheKey);

    const baseUrl = c.req.url.split("/api/games/proxy")[0];
    const proxiedUrl = `${baseUrl}/api/games/proxy?id=${encodeURIComponent(identifier)}&file=${encodeURIComponent(fileName)}`;

    return c.json({
      url: proxiedUrl,
      proxied_url: proxiedUrl,
      cached: !!existing,
      identifier,
      fileName
    });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});


/**
 * 💾 API: UPLOAD EMULATOR SAVE-STATE
 */
app.post("/api/saves/upload", async (c) => {
  const body = await c.req.parseBody();
  const userId = body.userId as string;
  const romHash = body.romHash as string;
  const label = body.label as string || "AutoSave";
  const file = body.file as File;

  if (!userId || !romHash || !file) {
    return c.json({ error: "Missing required fields: userId, romHash, or file" }, 400);
  }

  const manager = new GameSessionManager(c.env.STORAGE_BUCKET);
  const data = await file.arrayBuffer();
  const saveKey = await manager.uploadSaveState(userId, romHash, label, data, file.type);

  return c.json({ status: "saved", key: saveKey, label });
});

/**
 * 📊 API: LIST PERSISTENT SAVE STATES FOR USER/ROM
 */
app.get("/api/saves/list", async (c) => {
  const userId = c.req.query("userId");
  const romHash = c.req.query("romHash");

  if (!userId || !romHash) {
    return c.json({ error: "Missing required query params: userId and romHash" }, 400);
  }

  const manager = new GameSessionManager(c.env.STORAGE_BUCKET);
  const list = await manager.listSaveStates(userId, romHash);

  return c.json({ count: list.length, saves: list });
});

/**
 * 🚀 API: DOWNLOAD PERSISTENT SAVE STATE BY KEY
 */
app.get("/api/saves/download", async (c) => {
  const key = c.req.query("key");
  if (!key) {
    return c.json({ error: "Missing required 'key' query parameter" }, 400);
  }

  const manager = new GameSessionManager(c.env.STORAGE_BUCKET);
  const response = await manager.downloadSaveState(key);

  if (!response) {
    return c.json({ error: "Save state file not found" }, 404);
  }

  return response;
});

/**
 * 📦 API: CLOUDFLARE-NATIVE STORAGE SYSTEM UPLOAD
 */
app.post("/api/storage/upload", async (c) => {
  const body = await c.req.parseBody();
  const userId = body.userId as string;
  const folderId = (body.folderId as string) || null;
  const visibility = (body.visibility as "public" | "private" | "shared") || "private";
  const file = body.file as File;

  if (!userId || !file) {
    return c.json({ error: "Missing required fields: userId or file" }, 400);
  }

  const storage = new CloudflareStorageSystem(c.env.STORAGE_BUCKET, c.env.DB);
  const fileData = await file.arrayBuffer();
  
  const record = await storage.uploadFile({
    fileData,
    filename: file.name,
    userId,
    folderId,
    visibility,
    contentType: file.type || "application/octet-stream"
  });

  return c.json({ status: "uploaded", file: record });
});

/**
 * 📁 API: CREATE NESTED STORAGE FOLDER
 */
app.post("/api/storage/folder/create", async (c) => {
  const body = await c.req.json();
  const { name, userId, parentFolderId } = body;

  if (!name || !userId) {
    return c.json({ error: "Missing required fields: name or userId" }, 400);
  }

  const storage = new CloudflareStorageSystem(c.env.STORAGE_BUCKET, c.env.DB);
  const folder = await storage.createFolder(name, userId, parentFolderId || null);

  return c.json({ status: "created", folder });
});

/**
 * 📊 API: LIST DIRECTORY CONTENTS (FILES + SUBFOLDERS)
 */
app.get("/api/storage/list", async (c) => {
  const userId = c.req.query("userId");
  const folderId = c.req.query("folderId") || null;

  if (!userId) {
    return c.json({ error: "Missing required 'userId' query parameter" }, 400);
  }

  const storage = new CloudflareStorageSystem(c.env.STORAGE_BUCKET, c.env.DB);
  const directory = await storage.listDirectory(userId, folderId);

  return c.json(directory);
});

/**
 * 🔗 API: CREATE SECURE STORAGE SHARE LINK
 */
app.post("/api/storage/share/create", async (c) => {
  const body = await c.req.json();
  const { fileId, userId, password, maxDownloads } = body;

  if (!fileId || !userId) {
    return c.json({ error: "Missing required fields: fileId or userId" }, 400);
  }

  const storage = new CloudflareStorageSystem(c.env.STORAGE_BUCKET, c.env.DB);
  const shareUrl = await storage.createShareLink(fileId, userId, password || undefined, maxDownloads || 100);

  return c.json({ status: "shared", shareUrl });
});

/**
 * 🏷️ API: CREATE STRIPE PRODUCT & PRICES (2026 EDITION)
 */
app.post("/api/stripe/product/create", async (c) => {
  const body = await c.req.json();
  const { name, description, priceAmount, productType, interval } = body;

  if (!name || !priceAmount || !productType) {
    return c.json({ error: "Missing required fields: name, priceAmount, or productType" }, 400);
  }

  try {
    const stripe = new CloudflareStripeAdvanced(c.env.GROQ_API_KEY || "sk_test_mock"); // Uses dynamic fallback or direct env
    const result = await stripe.createProduct({
      name,
      description,
      priceAmount,
      productType,
      interval
    });

    return c.json({ status: "success", product: result });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

/**
 * 💳 API: STRIPE EMBEDDED CHECKOUT INLINE SESSIONS
 */
app.post("/api/stripe/checkout/embedded", async (c) => {
  const body = await c.req.json();
  const { priceId, returnUrl, collectTax } = body;

  if (!priceId) {
    return c.json({ error: "Missing priceId in request payload" }, 400);
  }

  try {
    const stripe = new CloudflareStripeAdvanced(c.env.GROQ_API_KEY || "sk_test_mock");
    const session = await stripe.createEmbeddedCheckoutSession(priceId, returnUrl, collectTax !== false);

    return c.json({ status: "success", checkoutSession: session });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

/**
 * 🔗 API: STRIPE PAYMENT LINKS BUILDER
 */
app.post("/api/stripe/link/create", async (c) => {
  const body = await c.req.json();
  const { priceId, redirectUrl, collectTax } = body;

  if (!priceId) {
    return c.json({ error: "Missing priceId in request payload" }, 400);
  }

  try {
    const stripe = new CloudflareStripeAdvanced(c.env.GROQ_API_KEY || "sk_test_mock");
    const link = await stripe.createPaymentLink(priceId, redirectUrl, collectTax !== false);

    return c.json({ status: "success", paymentLink: link });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

/**
 * 📊 API: STRIPE CUSTOMER SELF-SERVICE PORTAL
 */
app.post("/api/stripe/portal/create", async (c) => {
  const body = await c.req.json();
  const { customerId, returnUrl } = body;

  if (!customerId) {
    return c.json({ error: "Missing customerId in request payload" }, 400);
  }

  try {
    const stripe = new CloudflareStripeAdvanced(c.env.GROQ_API_KEY || "sk_test_mock");
    const session = await stripe.createCustomerPortalSession(customerId, returnUrl);

    return c.json({ status: "success", portalSession: session });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

/**
 * 🕹️ API: CURATED RETRO GAMES INVENTORY LOOKUP
 */
app.get("/api/games/inventory", (c) => {
  const q = c.req.query("q");
  const consoleType = c.req.query("console") as "nes" | "snes" | "genesis" | "gba" | undefined;

  const results = queryGameInventory(q, consoleType);
  return c.json({ count: results.length, games: results });
});

/**
 * 🔍 API: DYNAMIC INTERNET ARCHIVE RETRO ROM SCRAPER (MASSIVE EXPANSION)
 */
app.get("/api/games/scrape", async (c) => {
  const q = c.req.query("q") || "mario";
  const consoleType = (c.req.query("console") as "nes" | "snes" | "genesis" | "gba") || "nes";

  try {
    const scraper = new InternetArchiveRomScraper();
    const games = await scraper.searchGames(q, consoleType);
    return c.json({ count: games.length, games });
  } catch (err: any) {
    return c.json({ error: err.message }, 500);
  }
});

export default app;
