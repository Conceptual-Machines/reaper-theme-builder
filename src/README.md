# Theme Source Assets

## Folder Structure
```
src/
├── transport/     # Transport bar buttons (play, stop, record, etc.)
├── tcp/           # Track Control Panel elements
├── mcp/           # Mixer Control Panel elements
├── toolbar/       # Toolbar buttons and icons
├── meters/        # VU meters and level indicators
└── general/       # Shared/general UI elements
```

## Naming Convention
Use descriptive names in source, they get renamed during build:
- `play_off.png` → `transport_play.png`
- `play_on.png` → `transport_play_on.png`
- etc.
