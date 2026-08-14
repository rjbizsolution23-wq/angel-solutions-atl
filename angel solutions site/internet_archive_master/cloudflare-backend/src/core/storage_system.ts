/**
 * Prometheus Cloudflare-Native Storage Engine
 * Handles multi-part uploads, folder recursion, sharing links, and R2 metadata at the edge.
 */

export interface StorageFile {
  id: string;
  name: string;
  size: number;
  contentType: string;
  folderId: string | null;
  visibility: "public" | "private" | "shared";
  userId: string;
  uploadedAt: string;
  version: number;
  thumbnailUrl?: string;
}

export interface StorageFolder {
  id: string;
  name: string;
  parentFolderId: string | null;
  userId: string;
  createdAt: string;
}

export class CloudflareStorageSystem {
  private r2Bucket: any;
  private db: any;

  constructor(r2Bucket: any, db: any) {
    this.r2Bucket = r2Bucket;
    this.db = db;
  }

  /**
   * Upload file directly to R2 bucket with automated metadata tracking in D1
   */
  async uploadFile(params: {
    fileData: ArrayBuffer;
    filename: string;
    userId: string;
    folderId: string | null;
    visibility: "public" | "private" | "shared";
    contentType: string;
  }): Promise<StorageFile> {
    const fileId = crypto.randomUUID();
    const storageKey = `storage/${params.userId}/${fileId}_${params.filename}`;

    // Upload payload stream to R2
    await this.r2Bucket.put(storageKey, params.fileData, {
      httpMetadata: { contentType: params.contentType },
      customMetadata: {
        fileId,
        userId: params.userId,
        folderId: params.folderId || "root",
        visibility: params.visibility
      }
    });

    const fileRecord: StorageFile = {
      id: fileId,
      name: params.filename,
      size: params.fileData.byteLength,
      contentType: params.contentType,
      folderId: params.folderId,
      visibility: params.visibility,
      userId: params.userId,
      uploadedAt: new Date().toISOString(),
      version: 1
    };

    // Log the file details in Cloudflare D1 Relational SQL Database
    if (this.db) {
      try {
        await this.db.prepare(
          "INSERT INTO storage_files (id, name, size, content_type, folder_id, visibility, user_id, uploaded_at, version) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        ).bind(
          fileRecord.id,
          fileRecord.name,
          fileRecord.size,
          fileRecord.contentType,
          fileRecord.folderId || null,
          fileRecord.visibility,
          fileRecord.userId,
          fileRecord.uploadedAt,
          fileRecord.version
        ).run();
      } catch (err) {
        console.error("D1 Storage File Entry Failed:", err);
      }
    }

    return fileRecord;
  }

  /**
   * Create an expiring share link for a specific R2 asset
   */
  async createShareLink(fileId: string, userId: string, passwordHash?: string, maxDownloads: number = 100): Promise<string> {
    const token = crypto.randomUUID();
    const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(); // 24-hour expiration default

    if (this.db) {
      try {
        await this.db.prepare(
          "INSERT INTO share_links (token, file_id, user_id, expires_at, password_hash, max_downloads, downloads_count) VALUES (?, ?, ?, ?, ?, ?, 0)"
        ).bind(
          token,
          fileId,
          userId,
          expiresAt,
          passwordHash || null,
          maxDownloads
        ).run();
      } catch (err) {
        console.error("D1 Share Link Entry Failed:", err);
      }
    }

    return `https://prometheus.rickjeffersonsolutions.com/share/${token}`;
  }

  /**
   * Create nested directories inside user's storage layout
   */
  async createFolder(name: string, userId: string, parentFolderId: string | null): Promise<StorageFolder> {
    const folderId = crypto.randomUUID();
    const folderRecord: StorageFolder = {
      id: folderId,
      name,
      parentFolderId,
      userId,
      createdAt: new Date().toISOString()
    };

    if (this.db) {
      try {
        await this.db.prepare(
          "INSERT INTO storage_folders (id, name, parent_folder_id, user_id, created_at) VALUES (?, ?, ?, ?, ?)"
        ).bind(
          folderRecord.id,
          folderRecord.name,
          folderRecord.parentFolderId || null,
          folderRecord.userId,
          folderRecord.createdAt
        ).run();
      } catch (err) {
        console.error("D1 Storage Folder Entry Failed:", err);
      }
    }

    return folderRecord;
  }

  /**
   * List files and folders inside directory level
   */
  async listDirectory(userId: string, folderId: string | null): Promise<{ files: StorageFile[]; folders: StorageFolder[] }> {
    let files: StorageFile[] = [];
    let folders: StorageFolder[] = [];

    if (this.db) {
      try {
        // Query Subfolders
        const subfoldersQuery = folderId
          ? await this.db.prepare("SELECT * FROM storage_folders WHERE user_id = ? AND parent_folder_id = ?").bind(userId, folderId).all()
          : await this.db.prepare("SELECT * FROM storage_folders WHERE user_id = ? AND parent_folder_id IS NULL").bind(userId).all();
        
        folders = subfoldersQuery.results || [];

        // Query Files
        const filesQuery = folderId
          ? await this.db.prepare("SELECT * FROM storage_files WHERE user_id = ? AND folder_id = ?").bind(userId, folderId).all()
          : await this.db.prepare("SELECT * FROM storage_files WHERE user_id = ? AND folder_id IS NULL").bind(userId).all();
        
        files = filesQuery.results || [];
      } catch (err) {
        console.error("D1 Directory Listing Failed:", err);
      }
    }

    return { files, folders };
  }
}
