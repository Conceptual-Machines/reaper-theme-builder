#!/usr/bin/env python3
"""
Recolor all green icons/images to warm blue in the theme.

Converts green pixels (hue ~120°) to warm blue (hue ~205°)
while preserving brightness and saturation.
"""

from PIL import Image
import colorsys
from pathlib import Path

BUILD_DIR = Path(__file__).parent.parent / "build" / "DarkMinimal_unpacked"

# Target hue shift: green (120°) -> warm blue (205°)
GREEN_HUE_MIN = 80 / 360   # ~80° in normalized 0-1 range
GREEN_HUE_MAX = 160 / 360  # ~160° in normalized 0-1 range
TARGET_BLUE_HUE = 205 / 360  # Warm blue ~205°


def is_green_pixel(r, g, b, a, min_saturation=0.2):
    """Check if a pixel is green (and not grayscale)."""
    if a < 10:  # Skip transparent pixels
        return False

    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

    # Check if hue is in green range and has enough saturation
    return GREEN_HUE_MIN <= h <= GREEN_HUE_MAX and s >= min_saturation


def shift_green_to_blue(r, g, b, a):
    """Shift green pixel to warm blue while preserving saturation and value."""
    if a < 10:  # Keep transparent pixels
        return (r, g, b, a)

    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

    # If it's in the green range, shift to blue
    if GREEN_HUE_MIN <= h <= GREEN_HUE_MAX and s >= 0.2:
        # Shift hue to warm blue
        new_r, new_g, new_b = colorsys.hsv_to_rgb(TARGET_BLUE_HUE, s, v)
        return (int(new_r * 255), int(new_g * 255), int(new_b * 255), a)

    return (r, g, b, a)


def recolor_image(image_path):
    """Recolor green pixels in an image to warm blue."""
    try:
        img = Image.open(image_path).convert('RGBA')
        pixels = img.load()
        width, height = img.size

        modified = False
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]

                if is_green_pixel(r, g, b, a):
                    pixels[x, y] = shift_green_to_blue(r, g, b, a)
                    modified = True

        if modified:
            img.save(image_path)
            return True
        return False

    except Exception as e:
        print(f"  ✗ Error processing {image_path.name}: {e}")
        return False


def recolor_all_icons():
    """Recolor all green icons in the theme to warm blue."""

    # Patterns to match - focus on UI icons, not transport (we have custom transport)
    patterns = [
        "*fx*.png",
        "*expand*.png",
        "*collapse*.png",
        "*arrow*.png",
        "gen_*.png",
        "mcp_*.png",
        "tcp_*.png",
        "item_*.png",
        "track_*.png",
        "table_*.png",
    ]

    all_files = set()
    for pattern in patterns:
        all_files.update(BUILD_DIR.glob(pattern))
        all_files.update((BUILD_DIR / "150").glob(pattern))
        all_files.update((BUILD_DIR / "200").glob(pattern))

    modified_count = 0
    skipped_count = 0

    for image_path in sorted(all_files):
        # Skip our custom transport icons
        if "transport_" in image_path.name:
            continue

        if recolor_image(image_path):
            print(f"  ✓ {image_path.relative_to(BUILD_DIR)}")
            modified_count += 1
        else:
            skipped_count += 1

    print(f"\n✓ Recolored {modified_count} icons")
    print(f"  Skipped: {skipped_count} (no green found)")


if __name__ == "__main__":
    print("=" * 50)
    print("Green → Warm Blue Icon Recoloring")
    print("=" * 50)
    recolor_all_icons()
    print("=" * 50)
