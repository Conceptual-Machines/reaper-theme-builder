#!/usr/bin/env python3
"""
Create REAPER sprite sheets for track buttons (mute, solo, recarm).
REAPER expects 3 states horizontally: [Normal] [Hover] [Active]
"""

from PIL import Image, ImageEnhance
from pathlib import Path

# Paths
ASSETS_DIR = Path(__file__).parent.parent / "assets" / "track_controls"
BUILD_DIR = Path(__file__).parent.parent / "build" / "DarkMinimal_unpacked"

# Target size for each frame (REAPER track buttons are 20x20)
FRAME_SIZE = (20, 20)
FRAME_GAP = 0  # No gap for track buttons


def create_sprite_sheet(img, brightness_factors=(1.0, 1.15, 1.0)):
    """Create a 3-frame horizontal sprite sheet from a single image."""
    frame = img.resize(FRAME_SIZE, Image.Resampling.LANCZOS)
    
    frames = []
    for factor in brightness_factors:
        if factor != 1.0:
            enhancer = ImageEnhance.Brightness(frame)
            frames.append(enhancer.enhance(factor))
        else:
            frames.append(frame.copy())
    
    sprite_width = FRAME_SIZE[0] * 3
    sprite_height = FRAME_SIZE[1]
    sprite = Image.new('RGBA', (sprite_width, sprite_height), (0, 0, 0, 0))
    
    for i, f in enumerate(frames):
        sprite.paste(f, (i * FRAME_SIZE[0], 0))
    
    return sprite


def process_track_buttons():
    """Process all track button icons and create sprite sheets."""
    
    # Mapping: (source_file, dest_files, brightness_factors)
    mappings = [
        # Mute button (source is track_mute.png for off state)
        ("track_mute.png", ["track_mute_off.png", "track_mute_off_ol.png"], (1.0, 1.15, 1.0)),
        ("track_mute_on.png", ["track_mute_on.png"], (1.0, 1.1, 1.2)),
        
        # Solo button
        ("track_solo_off.png", ["track_solo_off.png", "track_solo_off_ol.png"], (1.0, 1.15, 1.0)),
        ("track_solo_on.png", ["track_solo_on.png"], (1.0, 1.1, 1.2)),
        
        # Record arm button
        ("track_recarm_off.png", ["track_recarm_off.png", "track_recarm_off_ol.png", "track_recarm_norec.png", "track_recarm_norec_ol.png"], (1.0, 1.15, 1.0)),
        ("track_recarm_on.png", ["track_recarm_on.png", "track_recarm_on_ol.png"], (1.0, 1.1, 1.2)),
        
        # Also update generic mute/solo buttons
        ("track_mute.png", ["gen_mute_off.png"], (1.0, 1.15, 1.0)),
        ("track_mute_on.png", ["gen_mute_on.png"], (1.0, 1.1, 1.2)),
        ("track_solo_off.png", ["gen_solo_off.png"], (1.0, 1.15, 1.0)),
        ("track_solo_on.png", ["gen_solo_on.png"], (1.0, 1.1, 1.2)),
    ]
    
    print("Creating track button sprite sheets...")
    print(f"Frame size: {FRAME_SIZE[0]}x{FRAME_SIZE[1]}")
    print(f"Sprite size: {FRAME_SIZE[0] * 3}x{FRAME_SIZE[1]}")
    print()
    
    # DPI folders
    dpi_scales = {
        "": 1.0,
        "150": 1.5,
        "200": 2.0,
    }
    
    for src_name, dest_names, brightness in mappings:
        src_path = ASSETS_DIR / src_name
        
        if not src_path.exists():
            print(f"  ⚠ Missing: {src_name}")
            continue
        
        img = Image.open(src_path)
        
        for dest_name in dest_names:
            for dpi_folder, scale in dpi_scales.items():
                scaled_frame = (int(FRAME_SIZE[0] * scale), int(FRAME_SIZE[1] * scale))
                
                frame = img.resize(scaled_frame, Image.Resampling.LANCZOS)
                
                frames = []
                for factor in brightness:
                    if factor != 1.0:
                        enhancer = ImageEnhance.Brightness(frame)
                        frames.append(enhancer.enhance(factor))
                    else:
                        frames.append(frame.copy())
                
                sprite_width = scaled_frame[0] * 3
                sprite_height = scaled_frame[1]
                sprite = Image.new('RGBA', (sprite_width, sprite_height), (0, 0, 0, 0))
                
                for i, f in enumerate(frames):
                    sprite.paste(f, (i * scaled_frame[0], 0))
                
                if dpi_folder:
                    dest_dir = BUILD_DIR / dpi_folder
                else:
                    dest_dir = BUILD_DIR
                
                dest_path = dest_dir / dest_name
                sprite.save(dest_path)
            
        print(f"  ✓ {src_name} → {', '.join(dest_names)}")
    
    print()
    print("Done! Run build_theme.py to package and deploy.")


if __name__ == "__main__":
    process_track_buttons()

