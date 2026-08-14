/**
 * Internet Archive S3 & Wayback Machine Edge-Native Client
 * Architected for Cloudflare Workers runtime.
 */

export class InternetArchiveClient {
  private accessKey: string;
  private secretKey: string;

  constructor(accessKey: string, secretKey: string) {
    this.accessKey = accessKey;
    this.secretKey = secretKey;
  }

  /**
   * Check if a URL is currently preserved on the Wayback Machine
   */
  async checkWayback(url: string): Promise<{ archived: boolean; snapshotUrl?: string; timestamp?: string }> {
    const targetUrl = `https://archive.org/wayback/available?url=${encodeURIComponent(url)}`;
    try {
      const response = await fetch(targetUrl, {
        headers: { "User-Agent": "PrometheusEdgeClient/3.1.0" }
      });
      if (!response.ok) return { archived: false };

      const data: any = await response.json();
      const snapshot = data.archived_snapshots?.closest;

      if (snapshot && snapshot.available) {
        return {
          archived: true,
          snapshotUrl: snapshot.url,
          timestamp: snapshot.timestamp
        };
      }
      return { archived: false };
    } catch (err) {
      console.error("Wayback Machine available check failed:", err);
      return { archived: false };
    }
  }

  /**
   * Search Internet Archive catalog using search parameters
   */
  async search(query: string, limit: number = 50): Promise<any[]> {
    const targetUrl = `https://archive.org/advancedsearch.php?q=${encodeURIComponent(query)}&fl[]=identifier&fl[]=title&fl[]=mediatype&fl[]=description&rows=${limit}&output=json`;
    try {
      const response = await fetch(targetUrl);
      if (!response.ok) return [];

      const data: any = await response.json();
      return data.response?.docs || [];
    } catch (err) {
      console.error("Advanced Search query failed:", err);
      return [];
    }
  }

  /**
   * Get metadata properties for a specific item identifier
   */
  async getMetadata(identifier: string): Promise<any> {
    const targetUrl = `https://archive.org/metadata/${encodeURIComponent(identifier)}`;
    try {
      const response = await fetch(targetUrl);
      if (!response.ok) return null;
      return await response.json();
    } catch (err) {
      console.error("Metadata lookup failed for ID:", identifier, err);
      return null;
    }
  }

  /**
   * Stream files list from S3 metadata list
   */
  async getFiles(identifier: string): Promise<any[]> {
    const meta = await this.getMetadata(identifier);
    return meta?.files || [];
  }

  /**
   * Natively proxy and download an archive asset and upload directly to Cloudflare R2
   */
  async mirrorToR2(identifier: string, fileName: string, r2Bucket: any): Promise<boolean> {
    const downloadUrl = `https://archive.org/download/${encodeURIComponent(identifier)}/${encodeURIComponent(fileName)}`;
    try {
      const res = await fetch(downloadUrl);
      if (!res.ok) return false;

      const body = res.body;
      if (!body) return false;

      // Stream download body directly to R2 bucket to save memory usage on V8 isolates
      await r2Bucket.put(`${identifier}/${fileName}`, body, {
        httpMetadata: {
          contentType: res.headers.get("content-type") || "application/octet-stream"
        }
      });
      return true;
    } catch (err) {
      console.error("Mirror to R2 stream failed:", downloadUrl, err);
      return false;
    }
  }
}
