/**
 * Prometheus Save-State and ROM Caching Engine
 * Optimized for Cloudflare edge routing and ultra-fast retrieval.
 */

export class GameSessionManager {
  private r2Bucket: any;

  constructor(r2Bucket: any) {
    this.r2Bucket = r2Bucket;
  }

  /**
   * Cache a ROM locally in R2 from the Internet Archive to avoid slow scraping speeds.
   * This serves ROMs at sub-10ms edge CDN speeds after first download.
   */
  async getCachedRomOrFetch(identifier: string, fileName: string): Promise<Response> {
    const cacheKey = `roms/${identifier}/${fileName}`;
    
    // Check if the ROM is already mirrored in Cloudflare R2
    const existing = await this.r2Bucket.get(cacheKey);
    if (existing) {
      console.log(`[ROM_CACHE] Hit! Served ${fileName} directly from R2 Edge CDN.`);
      return new Response(existing.body, {
        headers: {
          "Content-Type": existing.httpMetadata?.contentType || "application/octet-stream",
          "Cache-Control": "public, max-age=31536000, immutable",
          "X-Cache-Status": "HIT"
        }
      });
    }

    // Cache Miss - Scrape from Internet Archive S3 servers
    console.log(`[ROM_CACHE] Miss. Scraping ${fileName} from Internet Archive...`);
    const sourceUrl = `https://archive.org/download/${encodeURIComponent(identifier)}/${encodeURIComponent(fileName)}`;
    
    try {
      const response = await fetch(sourceUrl);
      if (!response.ok) {
        return new Response(`Internet Archive returned status ${response.status}`, { status: response.status });
      }

      // Read stream and mirror directly to R2 bucket asynchronously
      const bodyClone = response.clone();
      const contentType = response.headers.get("content-type") || "application/octet-stream";

      // Put to R2
      await this.r2Bucket.put(cacheKey, bodyClone.body, {
        httpMetadata: { contentType }
      });

      console.log(`[ROM_CACHE] Successfully cached ${fileName} to R2 bucket.`);
      
      return new Response(response.body, {
        headers: {
          "Content-Type": contentType,
          "Cache-Control": "public, max-age=31536000, immutable",
          "X-Cache-Status": "MISS"
        }
      });
    } catch (err: any) {
      return new Response(`Failed fetching from Internet Archive source: ${err.message}`, { status: 500 });
    }
  }

  /**
   * Save game freeze-frames (.sav / SRAM / Save States) to R2 Object Storage
   */
  async uploadSaveState(userId: string, romHash: string, saveLabel: string, fileData: ArrayBuffer, contentType: string = "application/octet-stream"): Promise<string> {
    const saveKey = `saves/${userId}/${romHash}/${Date.now()}_${saveLabel}.state`;
    
    await this.r2Bucket.put(saveKey, fileData, {
      httpMetadata: { contentType },
      customMetadata: {
        userId,
        romHash,
        saveLabel,
        uploadedAt: new Date().toISOString()
      }
    });

    return saveKey;
  }

  /**
   * List all available save states for a user and ROM
   */
  async listSaveStates(userId: string, romHash: string): Promise<any[]> {
    const prefix = `saves/${userId}/${romHash}/`;
    const objects = await this.r2Bucket.list({ prefix });
    
    return objects.objects.map((obj: any) => ({
      key: obj.key,
      size: obj.size,
      uploadedAt: obj.uploadedAt,
      saveLabel: obj.key.split("_").pop()?.replace(".state", "") || "AutoSave"
    }));
  }

  /**
   * Download a specific save state stream
   */
  async downloadSaveState(saveKey: string): Promise<Response | null> {
    const object = await this.r2Bucket.get(saveKey);
    if (!object) return null;

    return new Response(object.body, {
      headers: {
        "Content-Type": object.httpMetadata?.contentType || "application/octet-stream",
        "X-Save-Label": object.customMetadata?.saveLabel || "AutoSave"
      }
    });
  }
}
