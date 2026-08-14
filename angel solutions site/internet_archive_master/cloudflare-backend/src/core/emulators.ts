/**
 * Prometheus Emulator Resolution & Controls Configuration Engine
 * Maps console identifiers to correct retro emulation cores, keymaps, and BIOS resources.
 */

export interface EmulatorConfig {
  console: string;
  core: string;
  coreUrl: string;
  defaultControls: Record<string, string>;
  biosRequired: boolean;
  biosUrl?: string;
}

export const EMULATOR_REGISTRY: Record<string, EmulatorConfig> = {
  snes: {
    console: "Super Nintendo (SNES)",
    core: "snes9x",
    coreUrl: "https://cdn.jsdelivr.net/npm/emulatorjs@latest/cores/snes9x.js",
    biosRequired: false,
    defaultControls: {
      DPad_Up: "ArrowUp",
      DPad_Down: "ArrowDown",
      DPad_Left: "ArrowLeft",
      DPad_Right: "ArrowRight",
      Button_A: "KeyX",
      Button_B: "KeyZ",
      Button_X: "KeyS",
      Button_Y: "KeyA",
      Button_L: "KeyQ",
      Button_R: "KeyW",
      Button_Start: "Enter",
      Button_Select: "ShiftLeft"
    }
  },
  genesis: {
    console: "Sega Genesis / Mega Drive",
    core: "genesis_plus_gx",
    coreUrl: "https://cdn.jsdelivr.net/npm/emulatorjs@latest/cores/genesis_plus_gx.js",
    biosRequired: false,
    defaultControls: {
      DPad_Up: "ArrowUp",
      DPad_Down: "ArrowDown",
      DPad_Left: "ArrowLeft",
      DPad_Right: "ArrowRight",
      Button_A: "KeyZ",
      Button_B: "KeyX",
      Button_C: "KeyC",
      Button_Start: "Enter",
      Button_Mode: "ShiftLeft"
    }
  },
  nes: {
    console: "Nintendo Entertainment System (NES)",
    core: "fceumm",
    coreUrl: "https://cdn.jsdelivr.net/npm/emulatorjs@latest/cores/fceumm.js",
    biosRequired: false,
    defaultControls: {
      DPad_Up: "ArrowUp",
      DPad_Down: "ArrowDown",
      DPad_Left: "ArrowLeft",
      DPad_Right: "ArrowRight",
      Button_A: "KeyX",
      Button_B: "KeyZ",
      Button_Start: "Enter",
      Button_Select: "ShiftLeft"
    }
  },
  gba: {
    console: "Game Boy Advance (GBA)",
    core: "mgba",
    coreUrl: "https://cdn.jsdelivr.net/npm/emulatorjs@latest/cores/mgba.js",
    biosRequired: false,
    defaultControls: {
      DPad_Up: "ArrowUp",
      DPad_Down: "ArrowDown",
      DPad_Left: "ArrowLeft",
      DPad_Right: "ArrowRight",
      Button_A: "KeyX",
      Button_B: "KeyZ",
      Button_L: "KeyQ",
      Button_R: "KeyW",
      Button_Start: "Enter",
      Button_Select: "ShiftLeft"
    }
  },
  dos: {
    console: "DOS (x86 Emulation)",
    core: "dosbox",
    coreUrl: "https://cdn.jsdelivr.net/npm/emulatorjs@latest/cores/dosbox.js",
    biosRequired: false,
    defaultControls: {
      Keyboard: "Standard_QWERTY",
      Mouse_Capture: "Click_To_Lock"
    }
  }
};

/**
 * Resolve correct emulator core configurations for a ROM file extension
 */
export function resolveEmulatorByExtension(fileName: string): EmulatorConfig | null {
  const ext = fileName.split(".").pop()?.toLowerCase();
  switch (ext) {
    case "sfc":
    case "smc":
    case "snes":
      return EMULATOR_REGISTRY.snes;
    case "md":
    case "gen":
    case "bin":
    case "smd":
      return EMULATOR_REGISTRY.genesis;
    case "nes":
      return EMULATOR_REGISTRY.nes;
    case "gba":
      return EMULATOR_REGISTRY.gba;
    case "exe":
    case "com":
    case "bat":
    case "zip":
      return EMULATOR_REGISTRY.dos;
    default:
      return null;
  }
}
