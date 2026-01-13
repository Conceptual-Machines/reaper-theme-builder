#!/usr/bin/env python3
"""
Apply color palette to REAPER theme config.
"""

import re
from pathlib import Path

THEME_PATH = Path(__file__).parent.parent / "build" / "Default_7.0_DarkMinimal_unpacked.ReaperTheme"

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
    "accent_warm_blue": "#5B9FD4",  # Warm blue for cursor/envelopes
    "accent_purple": "#A855F7",  # Electric Purple
    "accent_soft_purple": "#B38CD4",  # Soft purple for time selection
    "accent_coral": "#FF6B6B",   # Coral/salmon for loop area
    "accent_orange": "#FF8C42",  # Bright orange for MIDI selection
    "accent_electric_yellow": "#FFEA00",  # Electric yellow for MIDI note flash
    "danger_red": "#e53333",
    "mute_orange": "#ff9900",
    
    # Text colors
    "text_primary": "#e0e0e0",
    "text_muted": "#808080",
    "text_dim": "#666666",
    "text_status_blue": "#8a92a8",  # Slightly blueish grey for status text
    
    # Grid (brighter for visibility)
    "grid_major": "#666666",
    "grid_minor": "#4a4a4a",
    "grid_midi_bright": "#999999",  # Even brighter for MIDI editor
    
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
    "col_trans_fg": "text_status_blue",
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
    "toolbararmed_color": "bg_elevated",  # Subtle highlight instead of red tint
    
    # VU Meters
    "col_vuclip": "meter_red",
    "col_vutop": "meter_red",
    "col_vumid": "meter_yellow",
    "col_vubot": "meter_green",
    
    # Timeline
    "col_tl_bg": "bg_deep",
    "col_tl_fg": "text_muted",
    "col_tl_fg2": "text_dim",
    
    # Edit cursor (Bright blue for visibility)
    "col_cursor": "accent_blue",
    "col_cursor2": "accent_blue",

    # Play cursor (Warm blue with triangle)
    "playcursor_color": "accent_warm_blue",
    # Note: *_drawmode and *_mode entries are flags, not colors - don't map them!
    
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
    
    # Loop/time selection area
    "col_tl_bgsel": "accent_soft_purple",
    "col_tl_bgsel2": "accent_soft_purple",
    
    # MIDI editor
    "midi_rulerbg": "bg_surface",
    "midi_trackbg1": "bg_surface",
    "midi_trackbg2": "bg_elevated",
    "midi_trackbg_outer1": "bg_deep",
    "midi_trackbg_outer2": "bg_surface",
    "midi_leftbg": "bg_elevated",
    "midi_selpitch1": "bg_elevated",  # Selected pitch row background
    "midi_selpitch2": "bg_elevated",  # Selected pitch row alternate
    "midi_grid1": "grid_midi_bright",  # Minor grid lines
    "midi_grid3": "grid_midi_bright",  # Tertiary grid
    "midi_gridh": "grid_midi_bright",  # Horizontal grid lines
    "midi_gridhc": "grid_midi_bright",  # Horizontal center grid
    "midi_selbg": "accent_soft_purple",  # MIDI time selection background (matches arrange view)

    # Track envelopes (warm blue)
    "col_env1": "accent_warm_blue",
    "col_env2": "accent_warm_blue",
    "col_env3": "accent_warm_blue",
    "col_env4": "accent_warm_blue",
    "col_env5": "accent_warm_blue",
    "col_env6": "accent_warm_blue",
    "col_env7": "accent_warm_blue",
    "col_env8": "accent_warm_blue",
    "col_env9": "accent_warm_blue",
    "col_env10": "accent_warm_blue",
    "col_env11": "accent_warm_blue",
    "col_env12": "accent_warm_blue",
    "col_env13": "accent_warm_blue",
    "col_env14": "accent_warm_blue",
    "col_env15": "accent_warm_blue",
    "col_env16": "accent_warm_blue",

    # Folder/panel wiring
    "wiring_parentwire_folder": "accent_warm_blue",

    # Additional green colors to change to warm blue
    "playrate_edited": "accent_warm_blue",
    "item_grouphl": "accent_warm_blue",
    "col_stretchmarkerm": "accent_warm_blue",
    "col_stretchmarker_tm": "accent_warm_blue",
    "activetake_tag": "accent_warm_blue",
    "marqueezoom_outline": "accent_warm_blue",
    "areasel_fill": "accent_warm_blue",
    "areasel_outline": "accent_warm_blue",
    "guideline_color": "accent_warm_blue",
    "col_routingact": "accent_warm_blue",

    # Scrollbar and MIDI editor greens
    "mcp_send_midihw": "accent_warm_blue",
    "tcp_list_scrollbar_mouseover": "accent_warm_blue",
    "mcp_list_scrollbar_mouseover": "accent_warm_blue",
    "midi_endpt": "accent_warm_blue",
    "midi_ofsnsel": "accent_warm_blue",

    # Remaining misc greens
    "midi_editcurs": "accent_warm_blue",
    "mouseitem_color": "accent_warm_blue",
    "wiring_activity": "accent_warm_blue",
    "wiring_pin_connected": "accent_warm_blue",

    # MIDI note flash
    "midi_noteon_flash": "accent_electric_yellow",

    # Window pane resize handle
    "col_main_resize2": "accent_warm_blue",

    # Note: col_vubot (VU meter green) intentionally kept green per user request
    # Note: All *_mode and *_drawmode entries are flags, not colors, and are excluded
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

