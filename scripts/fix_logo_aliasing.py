#!/usr/bin/env python3
"""
Fix aliasing pixels on logo borders.
"""

from PIL import Image
from pathlib import Path

LOGO_PATH = Path(__file__).parent.parent / "assets" / "reaper-logo-icon.png"

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def fix_aliasing():
    """Fix border aliasing pixels"""

    LIGHT_BLUE = hex_to_rgb("#7BB8E8")
    DARK_BG = hex_to_rgb("#1a1a1a")

    img = Image.open(LOGO_PATH).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    fixed = 0

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # Skip fully transparent pixels
            if a < 10:
                continue

            # Skip pixels we already processed (dark bg or blue gradient)
            brightness = (r + g + b) / 3

            # Check if this is a "mixed" aliasing pixel
            # These will have intermediate alpha (not fully opaque) or odd colors
            is_mixed = False

            # Semi-transparent pixels
            if 50 < a < 200:
                is_mixed = True
            # Fully opaque but not dark bg or blue
            elif a >= 200:
                # Not dark background
                if not (r < 40 and g < 40 and b < 40):
                    # Not blue gradient area
                    if not (80 < r < 140 and 140 < g < 200 and 180 < b < 240):
                        is_mixed = True

            if is_mixed:
                # Decide based on brightness: lighter -> light blue, darker -> black
                if brightness > 60:
                    pixels[x, y] = (*LIGHT_BLUE, 255)
                else:
                    pixels[x, y] = (*DARK_BG, 255)
                fixed += 1

    img.save(LOGO_PATH)
    print(f"✓ Fixed {fixed} aliasing pixels")

if __name__ == "__main__":
    fix_aliasing()
