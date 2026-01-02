# REAPER Theme Builder

A toolkit for building custom REAPER themes using Figma for design.

## Project Structure

```
reaper-theme-builder/
├── assets/                  # Figma exports (source images)
│   ├── track_controls/      # Mute, Solo, Recarm buttons
│   └── ...
├── scripts/                 # Build scripts
│   ├── build_all.py         # Master build script
│   ├── build_theme.py       # Package and deploy
│   ├── create_sprites.py    # Transport icon sprites
│   ├── create_track_sprites.py  # Track button sprites
│   └── update_rtconfig.py   # Theme config updates
├── src/                     # Source files
│   └── transport/           # Transport bar icons
├── tools/                   # External tools (submodules)
│   └── cursor-talk-to-figma/
├── docs/                    # Documentation
└── build/                   # Generated output (gitignored)
```

## Setup

### Prerequisites
- Python 3.x with Pillow (`pip install Pillow`)
- REAPER (for testing themes)
- Figma account (for design)

### Figma Integration
1. Install the Figma plugin from `tools/cursor-talk-to-figma/`
2. Run the WebSocket server: `cd tools/cursor-talk-to-figma && bun socket`
3. Connect Cursor via MCP

## Building

Run the full build:
```bash
python scripts/build_all.py
```

This will:
1. Update rtconfig.txt settings
2. Generate transport icon sprites
3. Generate track button sprites
4. Package and deploy to REAPER

## Theme Design

### Transport Bar
- Icons exported at 56x56 from Figma
- Converted to sprite sheets (3 states: normal, hover, active)
- Configurable size via `update_rtconfig.py`

### Track Controls
- Mute (M), Solo (S), Recarm (R) buttons
- Exported at 36x36 from Figma
- Converted to 60x20 sprite sheets

## Customization

Edit the settings in `scripts/update_rtconfig.py`:
- `TRANSPORT_HEIGHT` - Transport bar height
- `BUTTON_WIDTH` / `BUTTON_HEIGHT` - Button dimensions
- `STATUS_WIDTH` - Time display width
