#!/usr/bin/env python3
"""
Recolor all remaining green/teal icons to warm blue.
"""

from PIL import Image
import colorsys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
THEME_SOURCE = PROJECT_ROOT / "theme_source/Default_7.0_unpacked"

# Hue range for green/teal
GREEN_HUE_MIN = 80 / 360   # Green starts ~80°
GREEN_HUE_MAX = 200 / 360  # Include teal/cyan up to 200°
TARGET_BLUE_HUE = 205 / 360  # Warm blue ~205°


def shift_green_to_blue(r, g, b, a):
    """Shift green/teal pixel to warm blue."""
    if a < 10:  # Keep transparent pixels
        return (r, g, b, a)

    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

    # If it's green/teal with decent saturation, shift to blue
    if GREEN_HUE_MIN <= h <= GREEN_HUE_MAX and s >= 0.15:
        new_r, new_g, new_b = colorsys.hsv_to_rgb(TARGET_BLUE_HUE, s, v)
        return (int(new_r * 255), int(new_g * 255), int(new_b * 255), a)

    return (r, g, b, a)


def recolor_icon(icon_path):
    """Recolor a single icon."""
    img = Image.open(icon_path).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    modified = False
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            new_pixel = shift_green_to_blue(r, g, b, a)

            if new_pixel != (r, g, b, a):
                pixels[x, y] = new_pixel
                modified = True

    if modified:
        img.save(icon_path)
        return True
    return False


def recolor_all_icons():
    """Recolor all green icons in envelope controls and item buttons."""

    # Specific files to recolor
    patterns = [
        # Envelope control panel
        "envcp_arm_on.png",
        "envcp_fader.png",
        "envcp_faderbg.png",
        "envcp_knob_stack.png",
        "envcp_parammod_on.png",
        "envcp_learn_on.png",
        "envcp_bypass_off.png",
        "envcp_bypass_on.png",

        # General UI on states
        "gen_midi_on.png",
        "gen_pause_on.png",
        "gen_play_on.png",
        "gen_repeat_on.png",

        # Table/expand icons
        "table_expand_on.png",
        "table_collapse_on.png",

        # Item buttons on states
        "item_env_on.png",
        "item_fx_on.png",
        "item_fx_on_hidpi.png",
        "item_group_sel.png",
        "item_group_sel_hidpi.png",
        "item_note_on.png",
        "item_note_on_hidpi.png",
        "item_pooled_on.png",
        "item_pooled_on_hidpi.png",
        "item_props_on_hidpi.png",
        "item_timebase_beat_on.png",
        "item_timebase_beat_on_hidpi.png",
        "item_timebase_time_on.png",
        "item_timebase_time_on_hidpi.png",
    ]

    recolored = 0

    for pattern in patterns:
        # Root directory
        icon_path = THEME_SOURCE / pattern
        if icon_path.exists():
            if recolor_icon(icon_path):
                print(f"  ✓ {pattern}")
                recolored += 1

        # DPI folders
        for dpi in ["150", "200"]:
            dpi_path = THEME_SOURCE / dpi / pattern
            if dpi_path.exists():
                if recolor_icon(dpi_path):
                    recolored += 1

    print(f"\n✓ Recolored {recolored} green icons")


if __name__ == "__main__":
    print("=" * 50)
    print("Recoloring All Green Icons → Warm Blue")
    print("=" * 50)
    recolor_all_icons()
    print("=" * 50)
