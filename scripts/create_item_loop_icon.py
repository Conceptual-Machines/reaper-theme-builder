#!/usr/bin/env python3
"""
Create media item loop toolbar icon.
"""

from PIL import Image, ImageDraw
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "assets" / "toolbar_icons_source"

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_loop_icon(size, color, bg_color=None):
    """Create a loop/repeat icon (circular arrow)"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fill background if specified
    if bg_color:
        draw.rectangle([0, 0, size, size], fill=bg_color)

    # Calculate dimensions
    margin = size // 5
    arrow_width = size // 12

    # Draw circular loop with arrows
    # Main circle arc
    bbox = [margin, margin, size - margin, size - margin]

    # Draw loop circle (two arcs to create arrows)
    draw.arc(bbox, start=45, end=315, fill=color, width=arrow_width)

    # Draw arrow heads
    # Top-right arrow
    arrow_size = size // 6
    x1 = size - margin - arrow_size // 2
    y1 = margin + arrow_size
    points_right = [
        (x1, y1),
        (x1 + arrow_size, y1 - arrow_size // 2),
        (x1, y1 - arrow_size)
    ]
    draw.polygon(points_right, fill=color)

    # Bottom-left arrow
    x2 = margin + arrow_size // 2
    y2 = size - margin - arrow_size
    points_left = [
        (x2, y2),
        (x2 - arrow_size, y2 + arrow_size // 2),
        (x2, y2 + arrow_size)
    ]
    draw.polygon(points_left, fill=color)

    return img

def create_toolbar_icon():
    """Create 3-state toolbar icon (normal, hover, active)"""

    # Colors
    NORMAL_ICON = hex_to_rgb("#808080")
    NORMAL_BG = hex_to_rgb("#242424")
    HOVER_ICON = hex_to_rgb("#FFFFFF")
    HOVER_BG = hex_to_rgb("#3a3a3a")
    ACTIVE_ICON = hex_to_rgb("#5B9FD4")
    ACTIVE_BG = hex_to_rgb("#3a3a3a")

    # Create icons for each DPI (30px base, matching other toolbar icons)
    for dpi, size in [(100, 30), (150, 45), (200, 60)]:
        # Create 3-state horizontal sprite (width = size * 3)
        sprite = Image.new('RGBA', (size * 3, size), (0, 0, 0, 0))

        # Normal state
        normal = create_loop_icon(size, NORMAL_ICON, NORMAL_BG)
        sprite.paste(normal, (0, 0))

        # Hover state
        hover = create_loop_icon(size, HOVER_ICON, HOVER_BG)
        sprite.paste(hover, (size, 0))

        # Active state
        active = create_loop_icon(size, ACTIVE_ICON, ACTIVE_BG)
        sprite.paste(active, (size * 2, 0))

        # Save
        output_path = OUTPUT_DIR / str(dpi) / "media_item_loop.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        sprite.save(output_path)
        print(f"✓ Created {output_path.relative_to(OUTPUT_DIR.parent)}")

if __name__ == "__main__":
    create_toolbar_icon()
    print("\n✓ Media item loop icon created")
    print("  Copy to toolbar_icons with:")
    print("  build_theme.py (includes toolbar icon deployment)")
