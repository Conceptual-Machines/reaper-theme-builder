#!/usr/bin/env python3
"""
Analyze colors in the REAPER logo.
"""

from PIL import Image
from pathlib import Path
from collections import Counter

LOGO_PATH = Path(__file__).parent.parent / "assets" / "reaper-logo-icon.png"

def analyze_logo():
    """Find dominant colors in logo"""
    img = Image.open(LOGO_PATH).convert('RGBA')
    pixels = img.load()
    width, height = img.size

    colors = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            # Include all visible pixels
            if a > 10:
                colors.append((r, g, b, a))

    # Count colors
    color_counts = Counter(colors)
    print(f"Total visible pixels: {len(colors)}")
    print("Top 20 colors in logo:")
    for color, count in color_counts.most_common(20):
        r, g, b, a = color
        brightness = (r + g + b) / 3
        print(f"  RGB({r},{g},{b}) Alpha={a} Brightness={brightness:.0f} - {count} pixels")

if __name__ == "__main__":
    analyze_logo()
