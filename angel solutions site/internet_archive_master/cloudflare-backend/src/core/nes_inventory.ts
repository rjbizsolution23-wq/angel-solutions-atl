/**
 * Prometheus Curated Retro Console Game Inventory
 * Maps legendary classic games to their verified, open-access Internet Archive S3 identifiers and ROM files.
 */

export interface RetroGameItem {
  id: string;
  title: string;
  console: "nes" | "snes" | "genesis" | "gba";
  archiveId: string; // Internet Archive ID
  fileName: string;  // ROM File Name in Archive
  coverUrl: string;  // Curated cover art placeholders
  description: string;
}

export const RETRO_GAME_INVENTORY: RetroGameItem[] = [
  // 🕹️ Nintendo Entertainment System (NES)
  {
    id: "nes-super-mario",
    title: "Super Mario Bros.",
    console: "nes",
    archiveId: "super-mario-snes-vba-gba",
    fileName: "Super Mario Bros. (World).nes",
    coverUrl: "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=250&auto=format&fit=crop",
    description: "The legendary platformer that defined an entire industry. Rescue Princess Peach from Bowser across 8 worlds."
  },
  {
    id: "nes-zelda-1",
    title: "The Legend of Zelda",
    console: "nes",
    archiveId: "legend0of0zelda0collection1",
    fileName: "nes/Legend of Zelda, The (USA).zip",
    coverUrl: "https://images.unsplash.com/photo-1593305841991-05c297ba4575?q=80&w=250&auto=format&fit=crop",
    description: "Begin Link's first adventure. Explore the land of Hyrule, conquer the dungeons, and piece together the Triforce."
  },
  {
    id: "nes-metroid",
    title: "Metroid",
    console: "nes",
    archiveId: "metroid-usa_202512",
    fileName: "Metroid (USA).zip",
    coverUrl: "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=250&auto=format&fit=crop",
    description: "Navigate the deep caverns of Planet Zebes as bounty hunter Samus Aran to defeat Mother Brain."
  },
  {
    id: "nes-castlevania",
    title: "Castlevania",
    console: "nes",
    archiveId: "action-games-gba-snes-roms",
    fileName: "Castlevania (USA).nes",
    coverUrl: "https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=250&auto=format&fit=crop",
    description: "Wield the legendary whip as Simon Belmont to conquer Dracula's demonic castle."
  },
  {
    id: "nes-megaman-2",
    title: "Mega Man 2",
    console: "nes",
    archiveId: "mega-man-2-usa_202606",
    fileName: "Mega Man 2 (USA).nes",
    coverUrl: "https://images.unsplash.com/photo-1551103782-8ab07afd45c1?q=80&w=250&auto=format&fit=crop",
    description: "Slay Dr. Wily's 8 Robot Masters in this absolute peak of classic 8-bit platforming action."
  },
  {
    id: "nes-tetris",
    title: "Tetris",
    console: "nes",
    archiveId: "tetris-usa_202512",
    fileName: "Tetris (USA).zip",
    coverUrl: "https://images.unsplash.com/photo-1605899435973-ca2d1a8861cf?q=80&w=250&auto=format&fit=crop",
    description: "Stack falling tetrominoes in the timeless puzzle classic that captured the world."
  },
  // 🕹️ Super Nintendo (SNES)
  {
    id: "snes-mario-world",
    title: "Super Mario World",
    console: "snes",
    archiveId: "super-mario-snes-vba-gba",
    fileName: "Super Mario World (USA).sfc",
    coverUrl: "https://images.unsplash.com/photo-1566577134770-3d85bb3a9cc4?q=80&w=250&auto=format&fit=crop",
    description: "Take Yoshi along on Mario's legendary 16-bit adventure across Dinosaur Land."
  },
  {
    id: "snes-zelda-lttp",
    title: "The Legend of Zelda: A Link to the Past",
    console: "snes",
    archiveId: "legend-of-zelda-the-a-link-to-the-past-usa_202501",
    fileName: "Legend of Zelda, The - A Link to the Past (USA).zip",
    coverUrl: "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?q=80&w=250&auto=format&fit=crop",
    description: "Link travels between the Light and Dark worlds in one of the greatest games ever created."
  },
  // 🕹️ Sega Genesis
  {
    id: "genesis-sonic-2",
    title: "Sonic the Hedgehog 2",
    console: "genesis",
    archiveId: "sonic-2-long-version-v-1.8-2016-platform-megadrive",
    fileName: "Sonic 2 - Long Version (v1.8) (2016) (Platform) (Megadrive).zip",
    coverUrl: "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=250&auto=format&fit=crop",
    description: "The blue blur and Tails team up to stop Dr. Robotnik's Death Egg at blistering speeds."
  }
];

export function queryGameInventory(query?: string, consoleType?: "nes" | "snes" | "genesis" | "gba"): RetroGameItem[] {
  let list = RETRO_GAME_INVENTORY;
  if (consoleType) {
    list = list.filter(game => game.console === consoleType);
  }
  if (query) {
    const normalized = query.toLowerCase();
    list = list.filter(
      game =>
        game.title.toLowerCase().includes(normalized) ||
        game.description.toLowerCase().includes(normalized)
    );
  }
  return list;
}
