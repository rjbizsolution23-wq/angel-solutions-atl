#!/bin/zsh

# RJ PROMETHEUS RPG MASTER CABINET LAUNCHER
# Designed exclusively for Rick Jefferson | RJ Business Solutions

echo "===================================================="
echo "🎮 BOOTING PROMETHEUS RPG MASTER CABINET... 🎮"
echo "===================================================="

# Locate absolute path to the local cabinet
CABINET_PATH="$(pwd)/rpg_cabinet.html"

if [[ -f "$CABINET_PATH" ]]; then
  echo "Opening Master RPG Cabinet..."
  open "$CABINET_PATH"
  echo "✅ CABINET BOOTED SUCCESSFULLY!"
else
  echo "❌ Error: 'rpg_cabinet.html' not found. Run 'python3 cli/install_rpgs.py' first."
fi
