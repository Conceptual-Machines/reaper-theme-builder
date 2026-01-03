# DarkMinimal REAPER Theme Builder

A custom dark theme for REAPER DAW with Material Icons transport bar and blue FX accents.

## Features

- **Custom Transport Bar**: Material Design icons (play, stop, record, etc.)
- **Blue FX Indicators**: Custom TCP/MCP FX text and power icons
- **Dark Color Palette**: Carefully tuned backgrounds and accents
- **Figma Integration**: Design assets in Figma, export to theme

## Quick Start

### Prerequisites

- Python 3.9+
- Base theme: LCS Flat 7 (place in `theme_source/LCS_Flat-7.ReaperThemeZip`)

### Local Build

```bash
# Install dependencies
pip install -r requirements.txt

# Build theme
python scripts/build_all.py

# Output: DarkMinimal.ReaperThemeZip
```

### Install Theme

Copy `DarkMinimal.ReaperThemeZip` to your REAPER ColorThemes folder:
- **macOS**: `~/Library/Application Support/REAPER/ColorThemes/`
- **Windows**: `%APPDATA%\REAPER\ColorThemes\`
- **Linux**: `~/.config/REAPER/ColorThemes/`

Then in REAPER: **Options → Themes → Load theme...**

## Project Structure

```
├── assets/
│   ├── transport/     # Transport bar icons (56x56 PNG)
│   ├── fx/            # FX button assets
│   └── track/         # Track control buttons
├── scripts/
│   ├── build_all.py       # Master build script
│   ├── build_theme.py     # Package and deploy
│   ├── create_sprites.py  # Generate transport sprites
│   ├── create_fx_sprites.py
│   ├── apply_colors.py    # Apply color palette
│   └── update_rtconfig.py # Update layout settings
├── theme_source/      # Base theme (not committed)
├── build/             # Build output (not committed)
└── .github/workflows/ # CI configuration
```

## CI/CD

The project includes GitHub Actions workflow for automated builds:

1. On push to `main`: Builds and uploads artifact
2. On tag `v*`: Creates GitHub release with theme zip

### Required Secrets (optional)

- `THEME_SOURCE_URL`: URL to download base theme (if not committed)

## Customization

### Colors

Edit `scripts/apply_colors.py` to modify the color palette:

```python
PALETTE = {
    "bg_deep": "#1a1a1a",
    "bg_surface": "#242424",
    "accent_blue": "#3b82fa",
    # ...
}
```

### Transport Icons

1. Design icons in Figma (56x56, transparent background)
2. Export to `assets/transport/` as `{name}_off.png` and `{name}_on.png`
3. Run `python scripts/create_sprites.py`

### FX Buttons

1. Export from Figma to `assets/fx/`
2. Run `python scripts/create_fx_sprites.py`

## Figma Integration

Install the Cursor-Talk-To-Figma MCP for live design:

```bash
cd tools/cursor-talk-to-figma
bun install
bun socket  # Start WebSocket server
```

Then connect from Figma using the plugin.

## License

Theme customizations: MIT
Base theme (LCS Flat 7): See original license
