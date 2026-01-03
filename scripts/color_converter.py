#!/usr/bin/env python3
"""
REAPER Theme Color Converter
Converts hex colors to REAPER's BGR decimal format
"""

def hex_to_reaper(hex_color: str) -> int:
    """Convert hex color (#RRGGBB) to REAPER RGB decimal format"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    # REAPER uses RGB format: R + G*256 + B*65536
    return r + (g * 256) + (b * 65536)

def reaper_to_hex(reaper_color: int) -> str:
    """Convert REAPER BGR decimal to hex color (#RRGGBB)"""
    if reaper_color < 0:
        # Handle negative values (alpha blending)
        reaper_color = reaper_color & 0xFFFFFFFF
    b = reaper_color % 256
    g = (reaper_color // 256) % 256
    r = (reaper_color // 65536) % 256
    return f"#{r:02x}{g:02x}{b:02x}"

# =============================================================================
# FIGMA DARK MINIMAL PALETTE
# =============================================================================

FIGMA_PALETTE = {
    # Backgrounds
    "bg_deep": "#0d0d0d",       # Deepest background
    "bg_surface": "#1a1a1a",    # Surface background  
    "bg_elevated": "#292929",   # Elevated elements
    "bg_button": "#1f1f1f",     # Button background (off state)
    "bg_transport": "#141414",  # Transport bar background
    
    # Accent colors
    "accent_blue": "#3b82fa",   # Primary accent (play, loop)
    "danger_red": "#e53333",    # Record, danger, clip
    "mute_orange": "#ff9900",   # Mute active
    
    # Text colors
    "text_primary": "#e0e0e0",  # Primary text
    "text_muted": "#808080",    # Muted/inactive icons
    "text_dim": "#666666",      # Dimmed text
    
    # VU Meter colors
    "meter_red": "#e53333",     # Clip zone
    "meter_yellow": "#ffcc00",  # High zone
    "meter_green": "#33d459",   # Normal zone
}

# Convert all to REAPER format
REAPER_COLORS = {name: hex_to_reaper(hex_val) for name, hex_val in FIGMA_PALETTE.items()}

# Print conversions
if __name__ == "__main__":
    print("=" * 60)
    print("FIGMA → REAPER COLOR CONVERSION")
    print("=" * 60)
    print()
    
    for name, hex_val in FIGMA_PALETTE.items():
        reaper_val = hex_to_reaper(hex_val)
        print(f"{name:20} {hex_val} → {reaper_val}")
    
    print()
    print("=" * 60)
    print("REAPER THEME COLOR MAPPINGS")
    print("=" * 60)
    print()
    
    # Map Figma colors to REAPER theme variables
    mappings = {
        # Main UI
        "col_main_bg2": "bg_deep",
        "col_main_bg": "bg_surface",
        "col_main_text": "text_primary",
        "col_main_text2": "text_muted",
        
        # Transport
        "col_trans_bg": "bg_transport",
        "col_trans_fg": "text_muted",
        "col_transport_editbk": "bg_deep",
        
        # Track list / Mixer
        "col_tracklistbg": "bg_deep",
        "col_mixerbg": "bg_deep",
        "col_arrangebg": "bg_surface",
        
        # Track backgrounds (alternating)
        "col_tr1_bg": "bg_surface",
        "col_tr2_bg": "bg_elevated",
        
        # Selected track
        "col_seltrack": "accent_blue",
        
        # TCP (Track Control Panel) text
        "col_tcp_text": "text_primary",
        "col_tcp_textsel": "text_primary",
        
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
    
    for theme_var, palette_name in mappings.items():
        reaper_val = REAPER_COLORS[palette_name]
        hex_val = FIGMA_PALETTE[palette_name]
        print(f"{theme_var}={reaper_val}  # {hex_val} ({palette_name})")

