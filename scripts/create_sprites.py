#!/usr/bin/env python3
"""
Create REAPER sprite sheets from single icon images.
REAPER expects 3 states horizontally: [Normal] [Hover] [Active]
"""

from PIL import Image, ImageEnhance
import os
from pathlib import Path

# Paths
SRC_DIR = Path(__file__).parent.parent / "src" / "transport"
BUILD_DIR = Path(__file__).parent.parent / "build" / "DarkMinimal_unpacked"

# Wider frames to prevent horizontal squashing
FRAME_SIZE = (48, 42)
# Gap between frames  
FRAME_GAP = 4


def create_sprite_sheet(img, brightness_factors=(1.0, 1.1, 1.2)):
    """
    Create a 3-frame horizontal sprite sheet from a single image.
    
    Args:
        img: PIL Image
        brightness_factors: Tuple of 3 brightness multipliers for each state
    
    Returns:
        PIL Image with 3 frames side by side
    """
    # Resize to frame size
    frame = img.resize(FRAME_SIZE, Image.Resampling.LANCZOS)
    
    # Create 3 variations
    frames = []
    for factor in brightness_factors:
        if factor != 1.0:
            enhancer = ImageEnhance.Brightness(frame)
            frames.append(enhancer.enhance(factor))
        else:
            frames.append(frame.copy())
    
    # Combine horizontally with gaps
    cell_width = FRAME_SIZE[0] + FRAME_GAP
    sprite_width = cell_width * 3
    sprite_height = FRAME_SIZE[1]
    sprite = Image.new('RGBA', (sprite_width, sprite_height), (0, 0, 0, 0))
    
    for i, f in enumerate(frames):
        sprite.paste(f, (i * cell_width, 0))
    
    return sprite


def process_transport_icons():
    """Process all transport icons and create sprite sheets."""
    
    # Mapping: (source_file, dest_file, brightness_factors)
    # brightness_factors = (normal, hover, active)
    mappings = [
        # Play button
        ("play_off.png", "transport_play.png", (1.0, 1.15, 1.0)),
        ("play_on.png", "transport_play_on.png", (1.0, 1.1, 1.2)),
        ("play_off.png", "transport_play_ol.png", (1.1, 1.2, 1.3)),
        ("play_off.png", "transport_play_sync.png", (1.0, 1.15, 1.0)),
        ("play_on.png", "transport_play_sync_on.png", (1.0, 1.1, 1.2)),
        ("play_off.png", "transport_play_sync_ol.png", (1.1, 1.2, 1.3)),
        
        # Stop button
        ("stop_off.png", "transport_stop.png", (1.0, 1.15, 1.0)),
        
        # Pause button
        ("pause_off.png", "transport_pause.png", (1.0, 1.15, 1.0)),
        ("pause_on.png", "transport_pause_on.png", (1.0, 1.1, 1.2)),
        
        # Record button
        ("record_off.png", "transport_record.png", (1.0, 1.15, 1.0)),
        ("record_on.png", "transport_record_on.png", (1.0, 1.1, 1.2)),
        ("record_off.png", "transport_record_ol.png", (1.1, 1.2, 1.3)),
        ("record_off.png", "transport_record_item.png", (1.0, 1.15, 1.0)),
        ("record_on.png", "transport_record_item_on.png", (1.0, 1.1, 1.2)),
        ("record_off.png", "transport_record_item_ol.png", (1.1, 1.2, 1.3)),
        ("record_off.png", "transport_record_loop.png", (1.0, 1.15, 1.0)),
        ("record_on.png", "transport_record_loop_on.png", (1.0, 1.1, 1.2)),
        ("record_off.png", "transport_record_loop_ol.png", (1.1, 1.2, 1.3)),
        
        # Navigation buttons
        ("rewind_off.png", "transport_previous.png", (1.0, 1.15, 1.0)),
        ("forward_off.png", "transport_next.png", (1.0, 1.15, 1.0)),
        ("prev_off.png", "transport_home.png", (1.0, 1.15, 1.0)),
        ("next_off.png", "transport_end.png", (1.0, 1.15, 1.0)),
        
        # Repeat/Loop button
        ("loop_off.png", "transport_repeat_off.png", (1.0, 1.15, 1.0)),
        ("loop_on.png", "transport_repeat_on.png", (1.0, 1.1, 1.2)),
        ("loop_off.png", "transport_repeat_ol.png", (1.1, 1.2, 1.3)),
    ]
    
    cell_width = FRAME_SIZE[0] + FRAME_GAP
    print("Creating sprite sheets...")
    print(f"Frame size: {FRAME_SIZE[0]}x{FRAME_SIZE[1]}, gap: {FRAME_GAP}")
    print(f"Sprite size: {cell_width * 3}x{FRAME_SIZE[1]}")
    print()
    
    # DPI folders
    dpi_scales = {
        "": 1.0,
        "150": 1.5,
        "200": 2.0,
    }
    
    for src_name, dest_name, brightness in mappings:
        src_path = SRC_DIR / src_name
        
        if not src_path.exists():
            print(f"  ⚠ Missing: {src_name}")
            continue
        
        img = Image.open(src_path)
        
        for dpi_folder, scale in dpi_scales.items():
            # Scale frame size and gap for DPI
            scaled_frame = (int(FRAME_SIZE[0] * scale), int(FRAME_SIZE[1] * scale))
            scaled_gap = int(FRAME_GAP * scale)
            scaled_cell = scaled_frame[0] + scaled_gap
            
            # Resize source to scaled frame size
            frame = img.resize(scaled_frame, Image.Resampling.LANCZOS)
            
            # Create 3 variations
            frames = []
            for factor in brightness:
                if factor != 1.0:
                    enhancer = ImageEnhance.Brightness(frame)
                    frames.append(enhancer.enhance(factor))
                else:
                    frames.append(frame.copy())
            
            # Combine horizontally with gaps
            sprite_width = scaled_cell * 3
            sprite_height = scaled_frame[1]
            sprite = Image.new('RGBA', (sprite_width, sprite_height), (0, 0, 0, 0))
            
            for i, f in enumerate(frames):
                sprite.paste(f, (i * scaled_cell, 0))
            
            # Save
            if dpi_folder:
                dest_dir = BUILD_DIR / dpi_folder
            else:
                dest_dir = BUILD_DIR
            
            dest_path = dest_dir / dest_name
            sprite.save(dest_path)
        
        print(f"  ✓ {src_name} → {dest_name}")
    
    print()
    print("Done! Run build_theme.py to package and deploy.")


if __name__ == "__main__":
    process_transport_icons()

