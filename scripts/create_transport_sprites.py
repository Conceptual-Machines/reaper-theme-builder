#!/usr/bin/env python3
"""
Create transport sprite sheets from Figma assets.

Input: Single icon PNGs (e.g., play_off.png, play_on.png)
Output: 3-frame horizontal sprites (e.g., transport_play.png, transport_play_on.png)

REAPER transport buttons are 96x30 (3 frames of 32x30).
"""

from PIL import Image
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets" / "transport"
BUILD_DIR = PROJECT_ROOT / "build" / "Default_7.0_DarkMinimal_unpacked"

# Target frame size for transport buttons (matches LCS)
FRAME_WIDTH = 32
FRAME_HEIGHT = 30

# Mapping: (asset_name_off, asset_name_on) -> (reaper_name_off, reaper_name_on, reaper_name_off_explicit)
# Third element is optional - if provided, creates an explicit _off variant
TRANSPORT_MAPPINGS = {
    ("play_off.png", "play_on.png"): ("transport_play.png", "transport_play_on.png", None),
    ("stop_off.png", "stop_on.png"): ("transport_stop.png", "transport_stop_on.png", None),
    ("pause_off.png", "pause_on.png"): ("transport_pause.png", "transport_pause_on.png", None),
    ("record_off.png", "record_on.png"): ("transport_record.png", "transport_record_on.png", None),
    ("rewind_off.png", "rewind_on.png"): ("transport_rew.png", "transport_rew_on.png", None),
    ("forward_off.png", "forward_on.png"): ("transport_fwd.png", "transport_fwd_on.png", None),
    ("prev_off.png", "prev_on.png"): ("transport_home.png", None, None),  # home = prev marker
    ("next_off.png", "next_on.png"): ("transport_end.png", None, None),   # end = next marker
    ("loop_off.png", "loop_on.png"): ("transport_repeat.png", "transport_repeat_on.png", "transport_repeat_off.png"),
}


def create_sprite(img, frame_size=(FRAME_WIDTH, FRAME_HEIGHT)):
    """
    Create a 3-frame horizontal sprite from single image.
    Frames: normal, mouseover, pressed (all same for now).
    """
    # Scale image to fit frame while maintaining aspect ratio
    scale_w = frame_size[0] / img.width
    scale_h = frame_size[1] / img.height
    scale = min(scale_w, scale_h)  # Fill the frame
    
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Create centered frame
    frame = Image.new('RGBA', frame_size, (0, 0, 0, 0))
    x = (frame_size[0] - new_w) // 2
    y = (frame_size[1] - new_h) // 2
    frame.paste(resized, (x, y), resized)
    
    # Create 3-frame sprite (normal, hover, pressed - all same)
    sprite_width = frame_size[0] * 3
    sprite = Image.new('RGBA', (sprite_width, frame_size[1]), (0, 0, 0, 0))
    
    for i in range(3):
        sprite.paste(frame, (i * frame_size[0], 0))
    
    return sprite


def save_with_dpi(img, base_path):
    """Save image at 1x, 1.5x, 2x DPI."""
    for folder, scale in [('', 1.0), ('150', 1.5), ('200', 2.0)]:
        if folder:
            out_dir = base_path.parent / folder
            out_dir.mkdir(exist_ok=True)
            out_path = out_dir / base_path.name
        else:
            out_path = base_path
        
        if scale != 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            scaled = img.resize(new_size, Image.Resampling.LANCZOS)
            scaled.save(out_path)
        else:
            img.save(out_path)


def process_transport_sprites():
    """Create all transport sprites from Figma assets."""

    for (off_name, on_name), mapping in TRANSPORT_MAPPINGS.items():
        reaper_off = mapping[0]
        reaper_on = mapping[1] if len(mapping) > 1 else None
        reaper_off_explicit = mapping[2] if len(mapping) > 2 else None

        # Process OFF state
        off_path = ASSETS_DIR / off_name
        if off_path.exists():
            img = Image.open(off_path)
            sprite = create_sprite(img)
            save_with_dpi(sprite, BUILD_DIR / reaper_off)
            print(f"  ✓ {reaper_off}")

            # Also create explicit _off variant if specified
            if reaper_off_explicit:
                save_with_dpi(sprite, BUILD_DIR / reaper_off_explicit)
                print(f"  ✓ {reaper_off_explicit}")
        else:
            print(f"  ⚠ {off_name} not found")

        # Process ON state (if it has one)
        if reaper_on:
            on_path = ASSETS_DIR / on_name
            if on_path.exists():
                img = Image.open(on_path)
                sprite = create_sprite(img)
                save_with_dpi(sprite, BUILD_DIR / reaper_on)
                print(f"  ✓ {reaper_on}")
            else:
                print(f"  ⚠ {on_name} not found")


if __name__ == '__main__':
    print("=" * 50)
    print("Transport Sprite Generator")
    print("=" * 50)
    
    process_transport_sprites()
    
    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)

