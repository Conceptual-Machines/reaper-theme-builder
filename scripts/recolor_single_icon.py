#!/usr/bin/env python3
"""
Test script to recolor a single icon from green/teal to warm blue.
"""

from PIL import Image
import colorsys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
THEME_SOURCE = PROJECT_ROOT / "theme_source/Default_7.0_unpacked"

# Hue ranges for green/teal/cyan to recolor
GREEN_HUE_MIN = 80 / 360   # Green starts ~80°
GREEN_HUE_MAX = 200 / 360  # Cyan/teal ends ~200°
TARGET_BLUE_HUE = 205 / 360  # Warm blue ~205°


def shift_green_to_blue(r, g, b, a):
    """Shift green/teal/cyan pixel to warm blue."""
    if a < 10:  # Keep transparent pixels
        return (r, g, b, a)

    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

    # If it's in the green/teal/cyan range with decent saturation, shift to blue
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
        print(f"✓ Recolored {icon_path.name}")
        return True
    else:
        print(f"⊗ No green/teal found in {icon_path.name}")
        return False


if __name__ == "__main__":
    # Test on track_fxon_h.png (horizontal FX button - ON state)
    test_icon = THEME_SOURCE / "track_fxon_h.png"

    print("=" * 50)
    print(f"Testing recolor on: {test_icon.name}")
    print("=" * 50)

    recolor_icon(test_icon)

    # Also do the DPI versions
    for dpi in ["150", "200"]:
        dpi_icon = THEME_SOURCE / dpi / "track_fxon_h.png"
        if dpi_icon.exists():
            recolor_icon(dpi_icon)

    print("=" * 50)
