/**
 * Prometheus Master Game Development & Retro Emulation Knowledge Corpus
 * Fully structures all elite repos, SDKs, papers, and compilation specs for edge agents.
 */

export interface KnowledgeItem {
  name: string;
  category: "retro" | "engines" | "repos" | "ai_ml" | "pcg" | "physics" | "audio" | "networking" | "assets";
  url: string;
  description: string;
  compilation_spec?: string;
}

export const GAME_DEV_CORPUS: KnowledgeItem[] = [
  // 🕹️ Retro Console Game Development
  {
    name: "SGDK (Sega Genesis Development Kit)",
    category: "retro",
    url: "https://github.com/Stephane-D/SGDK",
    description: "Complete C development kit for Sega Genesis / Mega Drive. Includes sprite engine, sound driver, and tile compression algorithms.",
    compilation_spec: "git clone https://github.com/Stephane-D/SGDK.git && export SGDK_PATH=$(pwd)/SGDK"
  },
  {
    name: "PVSnesLib (SNES Complete C SDK)",
    category: "retro",
    url: "https://github.com/alekmaul/pvsneslib",
    description: "Complete C library for Super Nintendo Entertainment System development.",
    compilation_spec: "git clone https://github.com/alekmaul/pvsneslib.git"
  },
  {
    name: "SNES-IDE",
    category: "retro",
    url: "https://github.com/BrunoRNS/SNES-IDE",
    description: "Visual integrated development environment for 16-bit Super Famicom / SNES assembly & C development."
  },
  {
    name: "nes-starter-kit",
    category: "retro",
    url: "https://github.com/cppchriscpp/nes-starter-kit",
    description: "C-based project template and scaffolding for Nintendo Entertainment System (NES) development."
  },

  // 🎮 Top Modern Engines
  {
    name: "Godot Engine",
    category: "engines",
    url: "https://github.com/godotengine/godot",
    description: "Multi-platform 2D and 3D open-source game engine. Uses GDScript, C#, and C++.",
    compilation_spec: "git clone https://github.com/godotengine/godot.git && scons platform=linuxbsd target=editor"
  },
  {
    name: "Phaser 3",
    category: "engines",
    url: "https://github.com/photonstorm/phaser",
    description: "High-performance JavaScript and TypeScript 2D game framework for HTML5 canvas in modern browsers."
  },
  {
    name: "Bevy",
    category: "engines",
    url: "https://github.com/bevyengine/bevy",
    description: "Data-driven, high-performance Game Entity Component System (ECS) built natively in Rust."
  },
  {
    name: "MonoGame",
    category: "engines",
    url: "https://github.com/MonoGame/MonoGame",
    description: "C# open-source cross-platform game framework succeeding XNA."
  },

  // 💎 Legendary Source Codes
  {
    name: "DOOM (id Software)",
    category: "repos",
    url: "https://github.com/id-Software/DOOM",
    description: "Original 1993 legendary Doom C engine. Master reference for raycasting, bsp trees, and retro tick rates.",
    compilation_spec: "git clone https://github.com/id-Software/DOOM.git && make"
  },
  {
    name: "Quake (id Software)",
    category: "repos",
    url: "https://github.com/id-Software/Quake",
    description: "Revolutionary full-3D game engine source code in C."
  },
  {
    name: "OpenRA",
    category: "repos",
    url: "https://github.com/OpenRA/OpenRA",
    description: "Real-time strategy game engine for Command & Conquer / Red Alert built in C#.",
    compilation_spec: "git clone https://github.com/OpenRA/OpenRA.git && make"
  },
  {
    name: "0 A.D.",
    category: "repos",
    url: "https://github.com/0ad/0ad",
    description: "High-quality 3D real-time strategy historical warfare game engine."
  },

  // 🧠 Game AI & ML
  {
    name: "Unity ML-Agents",
    category: "ai_ml",
    url: "https://github.com/Unity-Technologies/ml-agents",
    description: "Open-source reinforcement learning plugin wrapping PyTorch models to train neural network behaviors in game environments."
  },
  {
    name: "stable-baselines3",
    category: "ai_ml",
    url: "https://github.com/DLR-RM/stable-baselines3",
    description: "Set of clean PyTorch reinforcement learning algorithms for training gameplay models."
  },

  // 🎨 Procedural Content Generation (PCG)
  {
    name: "Wave Function Collapse",
    category: "pcg",
    url: "https://github.com/mxgmn/WaveFunctionCollapse",
    description: "Bitmap and tile synthesis algorithm generating infinite procedural maps, textures, and dungeons based on constraint rules."
  },
  {
    name: "FastNoiseLite",
    category: "pcg",
    url: "https://github.com/Auburn/FastNoiseLite",
    description: "GPU-accelerated noise generation library (Perlin, Simplex, cellular noise) for voxel and heightmap terrain generation."
  },

  // 🛠️ High-Performance Physics
  {
    name: "Box2D",
    category: "physics",
    url: "https://github.com/erincatto/box2d",
    description: "Industry-standard 2D rigid body physics engine used in millions of mobile and desktop games."
  },
  {
    name: "Jolt Physics",
    category: "physics",
    url: "https://github.com/jrouwe/JoltPhysics",
    description: "State-of-the-art multi-core friendly 3D physics engine used in Horizon Forbidden West."
  },

  // 🌐 Networking & Authoritative Servers
  {
    name: "Nakama",
    category: "networking",
    url: "https://github.com/heroiclabs/nakama",
    description: "Distributed social server and authoritative real-time game backend framework."
  },
  {
    name: "Colyseus",
    category: "networking",
    url: "https://github.com/colyseus/colyseus",
    description: "Authoritative multiplayer state synchronization game server framework in Node.js."
  },

  // 🎨 Asset Libraries
  {
    name: "OpenGameArt",
    category: "assets",
    url: "https://opengameart.org",
    description: "Comprehensive registry of public domain, CC-licensed game graphics, sprites, and sound effects."
  },
  {
    name: "Kenney Assets",
    category: "assets",
    url: "https://www.kenney.nl",
    description: "Thousands of premium quality, completely free game development 2D sprites, 3D models, and UI blocks."
  }
];

/**
 * Perform a keyword search over the game dev knowledge catalog
 */
export function queryKnowledgeBase(query: string): KnowledgeItem[] {
  const normalized = query.toLowerCase();
  return GAME_DEV_CORPUS.filter(
    item =>
      item.name.toLowerCase().includes(normalized) ||
      item.category.toLowerCase().includes(normalized) ||
      item.description.toLowerCase().includes(normalized)
  );
}
