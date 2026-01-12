#!/usr/bin/env python3
"""
Recolor mixer panel FX icons from green to warm blue.
"""

from PIL import Image
import colorsys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
THEME_SOURCE = PROJECT_ROOT / "theme_source/Default_7.0_unpacked"

# Hue range for green
GREEN_HUE_MIN = 80 / 360   # Green starts ~80°
GREEN_HUE_MAX = 160 / 360  # Green ends ~160°
TARGET_BLUE_HUE = 205 / 360  # Warm blue ~205°


def shift_green_to_blue(r, g, b, a):
    """Shift green pixel to warm blue."""
    if a < 10:  # Keep transparent pixels
        return (r, g, b, a)

    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

    # If it's green with decent saturation, shift to blue
    if GREEN_HUE_MIN <= h <= GREEN_HUE_MAX and s >= 0.3:
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


def recolor_mcp_fx_icons():
    """Recolor all mixer panel FX icons."""

    # MCP FX icon files to recolor
    mcp_patterns = [
        "mcp_fx_norm.png",
        "mcp_fx_in_norm.png",
        "mcp_fxlist_norm.png",
        "mcp_fxparm_norm.png",
    ]

    recolored = 0

    for pattern in mcp_patterns:
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

    print(f"\n✓ Recolored {recolored} mixer FX icons")


if __name__ == "__main__":
    print("=" * 50)
    print("Recoloring Mixer FX Icons: Green → Warm Blue")
    print("=" * 50)
    recolor_mcp_fx_icons()
    print("=" * 50)
