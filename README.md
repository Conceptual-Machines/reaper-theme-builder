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

# Configure deployment paths (optional)
cp deploy_config.example.py deploy_config.py
# Edit deploy_config.py to set your REAPER ColorThemes directories

# Build theme
python scripts/build_all.py

# Output: DarkMinimal.ReaperThemeZip
```

The build will automatically deploy to directories configured in `deploy_config.py`. If this file doesn't exist, the theme will only be created in the project root.

### Deployment Configuration

Create `deploy_config.py` from the example file and customize paths for your system:

```python
from pathlib import Path

DEPLOY_DIRS = [
    # Portable REAPER
    Path("/path/to/reaper-portable/ColorThemes"),

    # System REAPER (macOS)
    Path.home() / "Library/Application Support/REAPER/ColorThemes",

    # System REAPER (Windows)
    # Path.home() / "AppData/Roaming/REAPER/ColorThemes",

    # System REAPER (Linux)
    # Path.home() / ".config/REAPER/ColorThemes",
]
```

**Note**: `deploy_config.py` is gitignored, so you can customize it for your local setup without affecting the repository.

### Manual Install

If not using auto-deployment, copy `DarkMinimal.ReaperThemeZip` to your REAPER ColorThemes folder:
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

The project uses GitHub Actions for automated builds and releases:

### Workflow

1. **Feature branches**: Create a branch, make changes, open PR
2. **Pull Request**: CI builds and uploads artifact for testing
3. **Merge to main**: Automatically:
   - Builds the theme
   - Bumps patch version (0.1.0 → 0.1.1)
   - Creates a GitHub release with the theme zip
   - Tags the release (v0.1.1)

### Versioning

- Version stored in `VERSION` file (semver: MAJOR.MINOR.PATCH)
- Patch auto-incremented on each merge to main
- Bump MINOR/MAJOR manually for significant changes

### Manual Release

To release a specific version:
```bash
echo "1.0.0" > VERSION
git add VERSION && git commit -m "chore: bump to v1.0.0"
git push
```

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
