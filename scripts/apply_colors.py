#!/usr/bin/env python3
"""
Apply Figma color palette to REAPER theme config.
"""

import re
from pathlib import Path

THEME_PATH = Path(__file__).parent.parent / "build" / "DarkMinimal_unpacked.ReaperTheme"

def hex_to_reaper(hex_color: str) -> int:
    """Convert hex color (#RRGGBB) to REAPER RGB decimal format"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r + (g * 256) + (b * 65536)

# =============================================================================
# FIGMA DARK MINIMAL PALETTE
# =============================================================================

PALETTE = {
    # Backgrounds (lightened - less black)
    "bg_deep": "#1a1a1a",
    "bg_surface": "#242424",
    "bg_elevated": "#333333",
    "bg_button": "#2a2a2a",
    "bg_transport": "#1e1e1e",
    
    # Accent colors
    "accent_blue": "#3b82fa",
    "danger_red": "#e53333",
    "mute_orange": "#ff9900",
    
    # Text colors
    "text_primary": "#e0e0e0",
    "text_muted": "#808080",
    "text_dim": "#666666",
    
    # Grid
    "grid_major": "#444444",
    "grid_minor": "#333333",
    
    # VU Meter colors
    "meter_red": "#e53333",
    "meter_yellow": "#ffcc00",
    "meter_green": "#33d459",
}

# Color mappings: theme_var -> palette_key
COLOR_MAPPINGS = {
    # Main UI backgrounds
    "col_main_bg2": "bg_deep",
    "col_tracklistbg": "bg_deep",
    "col_mixerbg": "bg_deep",
    "col_arrangebg": "bg_surface",
    
    # Transport
    "col_trans_bg": "bg_transport",
    "col_trans_fg": "text_muted",
    "col_transport_editbk": "bg_deep",
    
    # Track backgrounds
    "col_tr1_bg": "bg_surface",
    "col_tr2_bg": "bg_elevated",
    
    # Selected track
    "col_seltrack": "accent_blue",
    "col_seltrack2": "accent_blue",
    
    # TCP text
    "col_tcp_text": "text_primary",
    "col_tcp_textsel": "text_primary",
    
    # MCP text  
    "col_mcp_text": "text_primary",
    "col_mcp_textsel": "text_primary",
    
    # Toolbar
    "col_toolbar_text": "text_muted",
    "col_toolbar_text_on": "text_primary",
    "toolbararmed_color": "danger_red",
    
    # VU Meters
    "col_vuclip": "meter_red",
    "col_vutop": "meter_red",
    "col_vumid": "meter_yellow",
    "col_vubot": "meter_green",
    
    # Timeline
    "col_tl_bg": "bg_deep",
    "col_tl_fg": "text_muted",
    "col_tl_fg2": "text_dim",
    
    # Cursor
    "col_cursor": "accent_blue",
    "col_cursor2": "accent_blue",
    "playcursor_color": "accent_blue",
    
    # Grid
    "col_gridlines": "grid_major",
    "col_gridlines2": "grid_minor",
    "col_gridlines3": "grid_minor",
    
    # Docker/tabs
    "docker_bg": "bg_deep",
    "docker_shadow": "bg_deep",
    "docker_selface": "accent_blue",
    "docker_unselface": "bg_elevated",
    "docker_text": "text_muted",
    "docker_text_sel": "text_primary",
    "windowtab_bg": "bg_deep",
    
    # Region/marker lanes
    "region_lane_bg": "bg_deep",
    "marker_lane_bg": "bg_deep",
    "ts_lane_bg": "bg_deep",
    
    # MIDI editor
    "midi_rulerbg": "bg_surface",
    "midi_trackbg1": "bg_surface",
    "midi_trackbg2": "bg_elevated",
    "midi_trackbg_outer1": "bg_deep",
    "midi_trackbg_outer2": "bg_surface",
    "midi_leftbg": "bg_elevated",
}


def apply_colors():
    """Apply color palette to .ReaperTheme file"""
    
    with open(THEME_PATH, 'r') as f:
        content = f.read()
    
    # Update transport font - make smaller (F3 = -13 -> F6 = -10)
    # Original: F3FFFFFF... (size -13)
    # New:      F6FFFFFF... (size -10)
    content = re.sub(
        r"(trans_font=)F3FFFFFF",
        r"\1F6FFFFFF",
        content
    )
    
    changes = 0
    for theme_var, palette_key in COLOR_MAPPINGS.items():
        hex_color = PALETTE[palette_key]
        reaper_val = hex_to_reaper(hex_color)
        
        # Match pattern: theme_var=number (key=value format in .ReaperTheme)
        pattern = rf"^({theme_var})=(-?\d+)"
        
        def replacer(m):
            nonlocal changes
            changes += 1
            return f"{m.group(1)}={reaper_val}"
        
        content = re.sub(pattern, replacer, content, flags=re.MULTILINE)
    
    with open(THEME_PATH, 'w') as f:
        f.write(content)
    
    print(f"✓ Applied {changes} color changes")
    print(f"  Palette: {len(PALETTE)} colors defined")
    print(f"  Mappings: {len(COLOR_MAPPINGS)} theme variables")


if __name__ == "__main__":
    apply_colors()

