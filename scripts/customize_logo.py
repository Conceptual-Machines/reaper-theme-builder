#!/usr/bin/env python3
"""
Customize REAPER logo icon with theme colors.
"""

from PIL import Image
from pathlib import Path

LOGO_PATH = Path(__file__).parent.parent / "assets" / "reaper-logo-icon.png"

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def lerp_color(color1, color2, t):
    """Linearly interpolate between two colors"""
    return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

def customize_logo():
    """Make background darker, add gradient to axe blade"""

    # Theme colors
    WARM_BLUE = hex_to_rgb("#5B9FD4")  # Main warm blue
    LIGHT_BLUE = hex_to_rgb("#7BB8E8")  # Lighter blue for highlights
    DARK_BG = hex_to_rgb("#1a1a1a")     # Darker background

    img = Image.open(LOGO_PATH).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    blue_changes = 0
    dark_changes = 0

    # First pass: identify min/max coordinates of white pixels for gradient
    min_x, min_y = width, height
    max_x, max_y = 0, 0

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 200 and r > 200 and g > 200 and b > 200:  # White pixels
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    # Second pass: apply colors
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # Skip fully transparent pixels
            if a < 10:
                continue

            # Check if this is the white axe blade (high brightness, high alpha)
            if a > 200 and r > 200 and g > 200 and b > 200:
                # Create diagonal gradient from top-left to bottom-right
                # Normalize position within the blade bounds
                if max_x > min_x and max_y > min_y:
                    gradient_t = ((x - min_x) / (max_x - min_x) + (y - min_y) / (max_y - min_y)) / 2
                else:
                    gradient_t = 0.5

                # Interpolate from light blue (top-left) to warm blue (bottom-right)
                color = lerp_color(LIGHT_BLUE, WARM_BLUE, gradient_t)
                pixels[x, y] = (*color, a)
                blue_changes += 1
            elif a > 200:  # All other opaque colored pixels become dark background
                pixels[x, y] = (*DARK_BG, a)
                dark_changes += 1

    img.save(LOGO_PATH)
    print(f"✓ Customized logo icon")
    print(f"  Axe blade: {blue_changes} pixels with gradient (light blue → warm blue)")
    print(f"  Background: {dark_changes} pixels → darker grey")

if __name__ == "__main__":
    customize_logo()
