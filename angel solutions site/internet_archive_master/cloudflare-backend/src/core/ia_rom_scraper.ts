import { InternetArchiveClient } from "./ia_client";

export interface ScrapedGame {
  title: string;
  archiveId: string;
  fileName: string;
  console: string;
  downloadUrl: string;
  size?: number;
}

/**
 * Intelligent Internet Archive Retro ROM Scraper
 * Dynamically queries massive console collections and extracts working ROM paths on the fly.
 */
export class InternetArchiveRomScraper {
  private client: InternetArchiveClient;

  constructor() {
    this.client = new InternetArchiveClient("", "");
  }

  /**
   * Search for ROM files based on query and console format
   */
  async searchGames(query: string, consoleType: "nes" | "snes" | "genesis" | "gba" = "nes"): Promise<ScrapedGame[]> {
    let collectionQuery = "";
    let fileExtension = "";

    switch (consoleType) {
      case "nes":
        collectionQuery = "collection:Nintendo_nes_library OR collection:nesroms";
        fileExtension = ".nes";
        break;
      case "snes":
        collectionQuery = "collection:nintendo_snes_library OR collection:snesroms";
        fileExtension = ".sfc"; // or .smc
        break;
      case "genesis":
        collectionQuery = "collection:sega_genesis_library OR collection:genesisroms";
        fileExtension = ".md"; // or .gen
        break;
      case "gba":
        collectionQuery = "collection:nintendo_gba_library OR collection:gbaroms";
        fileExtension = ".gba";
        break;
    }

    // Build advanced search query combining search term and console collection filter
    const fullQuery = `(${query}) AND (${collectionQuery})`;
    const docs = await this.client.search(fullQuery, 30);
    const results: ScrapedGame[] = [];

    for (const doc of docs) {
      if (!doc.identifier) continue;

      try {
        // Fetch specific file listings for this item
        const files = await this.client.getFiles(doc.identifier);
        
        // Find first file matching targeted console extension
        const romFile = files.find((f: any) => 
          f.name && (f.name.toLowerCase().endsWith(fileExtension) || 
                     f.name.toLowerCase().endsWith(".smc") || 
                     f.name.toLowerCase().endsWith(".zip"))
        );

        if (romFile) {
          results.push({
            title: doc.title || doc.identifier,
            archiveId: doc.identifier,
            fileName: romFile.name,
            console: consoleType,
            downloadUrl: `https://archive.org/download/${doc.identifier}/${romFile.name}`,
            size: romFile.size ? parseInt(romFile.size) : undefined
          });
        }
      } catch (err) {
        console.error(`Failed scraping files for IA identifier: ${doc.identifier}`, err);
      }
    }

    return results;
  }
}
