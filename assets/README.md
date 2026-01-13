# Assets Directory Structure

## Folders

### `transport/`
Transport button source images (play, stop, record, etc.)
- Used by `scripts/create_transport_sprites.py` to generate theme transport buttons

### `toolbar_icons_source/`
Toolbar icon source files organized by DPI:
- `100/` - Standard resolution (1x)
- `150/` - 150% scaling (1.5x)
- `200/` - 200% scaling for Retina/HiDPI displays (2x)

Icons are automatically copied to REAPER's Data/toolbar_icons folder during build.

## Available Toolbar Icons

- **auto read play outline** - Automation read mode
- **fx** - FX browser/chain
- **grid snap magnet** - Grid/snap toggle
- **info outline rounded** - Info/help
- **insert** - Insert item/track
- **media link** - Media explorer/browser
- **metronome** - Metronome toggle
- **mixer settings vertical** - Mixer settings
- **trim start** - Trim item start
- **tuner pitched** - Tuner

## Adding New Toolbar Icons

1. Export zip from toolbar icon generator with 100/150/200 DPI variants
2. Save zip to `toolbar_icons_zips/`
3. Extract to `toolbar_icons_source/` folders
4. Run build script or manually copy to REAPER's `Data/toolbar_icons/` folder

## Color Scheme

All toolbar icons use the theme's color palette:
- **Normal**: Icon #808080, Background #242424 or transparent
- **Hover**: Icon #FFFFFF (white), Background #3a3a3a
- **Active**: Icon #5B9FD4 (warm blue), Background #3a3a3a
